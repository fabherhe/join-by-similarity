import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import io

# Establecer el modo de página ancha (wide mode)
st.set_page_config(layout="wide")

# Título de la aplicación
st.title('Join usando Similaridad Semántica')

# Cargar el modelo de Sentence Transformer
@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

model = load_model()

# Crear dos columnas para la subida de archivos
col1, col2 = st.columns(2)

# Función para leer el archivo según el tipo, el offset, y la hoja seleccionada en caso de Excel
def read_file(file, has_header, offset, sheet_name=None):
    header_row = 0 if has_header else None
    if file.name.endswith(".csv"):
        return pd.read_csv(file, header=header_row, skiprows=offset)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file, sheet_name=sheet_name, header=header_row, skiprows=offset)
    else:
        st.error("Formato de archivo no soportado")
        return None

# Subida del primer archivo en la primera columna
with col1:
    uploaded_file1 = st.file_uploader("Sube el primer archivo (CSV o Excel)", type=["csv", "xlsx"], key="file1")
    header1 = st.checkbox("¿El archivo 1 tiene encabezado?", value=True, key="header1")
    offset1 = st.number_input("Offset (filas a saltarse) archivo 1", min_value=0, value=0, step=1, key="offset1")

    # Si es un archivo Excel, mostrar las hojas disponibles para seleccionar
    if uploaded_file1 and uploaded_file1.name.endswith(".xlsx"):
        xls1 = pd.ExcelFile(uploaded_file1)
        sheet1 = st.selectbox("Selecciona la hoja del archivo 1", xls1.sheet_names)

# Subida del segundo archivo en la segunda columna
with col2:
    uploaded_file2 = st.file_uploader("Sube el segundo archivo (CSV o Excel)", type=["csv", "xlsx"], key="file2")
    header2 = st.checkbox("¿El archivo 2 tiene encabezado?", value=True, key="header2")
    offset2 = st.number_input("Offset (filas a saltarse) archivo 2", min_value=0, value=0, step=1, key="offset2")

    # Si es un archivo Excel, mostrar las hojas disponibles para seleccionar
    if uploaded_file2 and uploaded_file2.name.endswith(".xlsx"):
        xls2 = pd.ExcelFile(uploaded_file2)
        sheet2 = st.selectbox("Selecciona la hoja del archivo 2", xls2.sheet_names)

# Si los archivos han sido cargados
if uploaded_file1 and uploaded_file2:
    # Leer ambos archivos con el offset y la hoja seleccionada (si es Excel)
    if uploaded_file1.name.endswith(".xlsx"):
        df1 = read_file(uploaded_file1, header1, offset1, sheet1)
    else:
        df1 = read_file(uploaded_file1, header1, offset1)

    if uploaded_file2.name.endswith(".xlsx"):
        df2 = read_file(uploaded_file2, header2, offset2, sheet2)
    else:
        df2 = read_file(uploaded_file2, header2, offset2)

    if df1 is not None and df2 is not None:
        st.write("Archivos cargados correctamente.")

        # Mostrar vista previa de las primeras 2 filas de ambos archivos junto con el conteo de filas
        st.write("Vista previa de los archivos:")

        # Crear dos columnas para la vista previa de los archivos
        preview_col1, preview_col2 = st.columns(2)

        with preview_col1:
            st.write(f"Archivo 1 - Número total de filas: {len(df1)}")
            st.write("Primeras 2 filas del archivo 1:")
            st.dataframe(df1.head(2))

        with preview_col2:
            st.write(f"Archivo 2 - Número total de filas: {len(df2)}")
            st.write("Primeras 2 filas del archivo 2:")
            st.dataframe(df2.head(2))

        # Añadir nota antes de la selección de columnas
        st.write("**Nota:** Solo se pueden seleccionar columnas de texto para realizar el join basado en similitud semántica.")

        # Selección de columnas para hacer el match
        col1_select, col2_select = st.columns(2)

        with col1_select:
            column1 = st.selectbox("Selecciona la columna del archivo 1 para hacer el match", df1.columns)

        with col2_select:
            column2 = st.selectbox("Selecciona la columna del archivo 2 para hacer el match", df2.columns)

        # Verificar si las columnas seleccionadas son de tipo object (texto)
        if df1[column1].dtype != 'object' or df2[column2].dtype != 'object':
            st.error("Las columnas seleccionadas deben ser de tipo texto (object). Por favor, selecciona columnas que contengan texto para realizar el join basado en similitud semántica.")
        else:
            # Agregar un umbral de similitud en una grilla de una columna
            st.write("Opciones de similitud:")
            threshold = st.slider("Selecciona el umbral de similitud (0 a 1)", min_value=0.0, max_value=1.0, value=0.7, step=0.01)

            # Opción para seleccionar el tipo de join
            join_type = st.radio("Selecciona el tipo de join:", ["Inner Join", "Left Join", "Right Join", "Outer Join"])

            # Verificar duplicados problemáticos en la tabla correspondiente según el tipo de join
            hay_duplicados_problema = False
            problematic_keys = []

            if join_type == "Left Join":
                # Para Left Join, verificamos duplicados problemáticos en df2 (archivo derecho)
                df_to_check = df2
                key_column = column2
                side = "archivo 2"
            elif join_type == "Right Join":
                # Para Right Join, verificamos duplicados problemáticos en df1 (archivo izquierdo)
                df_to_check = df1
                key_column = column1
                side = "archivo 1"
            else:
                df_to_check = None

            if df_to_check is not None:
                # Identificar duplicados en la columna clave
                duplicates = df_to_check[df_to_check.duplicated(subset=[key_column], keep=False)]
                # Excluir duplicados exactos (filas idénticas)
                duplicates_exact = duplicates[duplicates.duplicated(keep=False)]
                duplicates_problematic = duplicates.drop_duplicates().merge(duplicates_exact.drop_duplicates(), indicator=True, how='left').loc[lambda x: x['_merge'] == 'left_only'].drop('_merge', axis=1)
                # Retornar los valores de la columna clave que tienen duplicados problemáticos
                problematic_keys = duplicates_problematic[key_column].unique()

                if len(problematic_keys) > 0:
                    st.warning(f"El {side} tiene valores duplicados en la columna '{key_column}' con diferencias en otras columnas. Los siguientes valores presentan este problema:")
                    st.write(problematic_keys)
                    hay_duplicados_problema = True

                    # Preguntar al usuario cómo desea proceder
                    action = st.selectbox(
                        f"Selecciona cómo deseas manejar los duplicados en el {side}:",
                        ["Conservar primer duplicado", "Conservar último duplicado", "Eliminar duplicados", "Detener el programa y arreglarlo manualmente"]
                    )

                    if action == "Detener el programa y arreglarlo manualmente":
                        st.stop()
                    elif action == "Conservar primer duplicado":
                        # Conservar el primer duplicado
                        df_to_check = df_to_check.drop_duplicates(subset=[key_column], keep='first')
                    elif action == "Conservar último duplicado":
                        # Conservar el último duplicado
                        df_to_check = df_to_check.drop_duplicates(subset=[key_column], keep='last')
                    elif action == "Eliminar duplicados":
                        # Eliminar todos los duplicados
                        df_to_check = df_to_check.drop_duplicates(subset=[key_column], keep=False)

                    # Actualizar df2 o df1 según corresponda
                    if side == "archivo 2":
                        df2 = df_to_check
                    else:
                        df1 = df_to_check

            # Continuar con el procesamiento si no se detuvo
            # Botón para ejecutar el match
            if st.button("Realizar Match"):
                # Resetear los índices de df1 y df2
                df1 = df1.reset_index(drop=True)
                df2 = df2.reset_index(drop=True)

                # Determinar la dirección del match según el tipo de join
                if join_type == "Right Join":
                    # Para Right Join, hacemos el match desde df2 hacia df1
                    source_df = df2
                    source_column = column2
                    target_df = df1
                    target_column = column1
                else:
                    # Para Left Join, Inner Join, Outer Join, hacemos el match desde df1 hacia df2
                    source_df = df1
                    source_column = column1
                    target_df = df2
                    target_column = column2

                # Obtener los nombres y sus índices en source_df
                source_names = source_df[source_column].dropna().unique()
                source_indices = source_df[source_column].dropna().reset_index()
                source_to_indices = source_indices.groupby(source_column)['index'].apply(list).to_dict()

                # Obtener los nombres de la columna objetivo
                target_names = target_df[target_column].dropna().unique()

                # Calcular los embeddings
                source_embeddings = model.encode(source_names.tolist(), convert_to_tensor=True)
                target_embeddings = model.encode(target_names.tolist(), convert_to_tensor=True)

                # Calcular la similitud de coseno entre los embeddings
                cosine_scores = util.pytorch_cos_sim(source_embeddings, target_embeddings)

                # Convertir las similitudes a un DataFrame
                similarity_df = pd.DataFrame(cosine_scores.numpy(), index=source_names, columns=target_names)

                # Encontrar el mejor match para cada nombre
                best_matches = similarity_df.idxmax(axis=1)
                best_scores = similarity_df.max(axis=1)

                # Crear un DataFrame con los resultados
                match_results = pd.DataFrame({
                    source_column: source_names,
                    'Best Match': best_matches.values,
                    'Similarity Score': best_scores.values
                })

                # Asignar NaN a los que no cumplen el umbral
                match_results.loc[match_results['Similarity Score'] < threshold, ['Best Match', 'Similarity Score']] = [None, None]

                # Mapear los resultados de vuelta a los índices originales en source_df
                match_list = []
                for _, row in match_results.iterrows():
                    name = row[source_column]
                    indices = source_to_indices.get(name, [])
                    for idx in indices:
                        original_row = source_df.loc[idx].copy()
                        original_row['Best Match'] = row['Best Match']
                        original_row['Similarity Score'] = row['Similarity Score']
                        match_list.append(original_row)

                # Crear un DataFrame con todos los matches
                result_df = pd.DataFrame(match_list)

                # Realizar el merge según el tipo de join seleccionado
                if join_type == "Inner Join":
                    result = result_df.dropna(subset=['Best Match'])
                    result = pd.merge(result, target_df, left_on='Best Match', right_on=target_column, how='inner', suffixes=('_left', '_right'))
                elif join_type == "Left Join" or join_type == "Right Join":
                    result = pd.merge(result_df, target_df, left_on='Best Match', right_on=target_column, how='left', suffixes=('_left', '_right'))
                elif join_type == "Outer Join":
                    result = pd.merge(result_df, target_df, left_on='Best Match', right_on=target_column, how='outer', suffixes=('_left', '_right'))

                # Mostrar el resultado
                st.write(f"Resultado del Match ({join_type}) según el umbral seleccionado:")
                st.write(f"Número total de filas en el resultado: {len(result)}")
                st.dataframe(result.sort_values(by='Similarity Score', ascending=False))

                # Botón para descargar el resultado como Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result.to_excel(writer, index=False, sheet_name='Resultado')
                processed_data = output.getvalue()

                st.download_button(
                    label="Descargar resultado como Excel",
                    data=processed_data,
                    file_name='resultado_match.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

                # Mensaje final
                st.write("""
                Ahora puedes descargar el archivo usando el ícono de descarga. Recuerda que puedes revisar tus datos en Excel para asegurarte de que todo esté correcto. ¡Espero que haya sido de ayuda!
                """)

else:
    st.write("Por favor sube ambos archivos para continuar.")
