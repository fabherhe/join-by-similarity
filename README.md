# Join usando Embeddings para encontrar Similaridad Semántica

Una aplicación de Streamlit que permite unir dos conjuntos de datos basándose en la similitud semántica entre columnas de texto seleccionadas.

## Descripción

Esta herramienta facilita la combinación de dos archivos (CSV o Excel) mediante un **join** basado en la similitud semántica de los textos en columnas específicas. Utiliza modelos de transformación de oraciones para calcular la similitud entre los textos y permite al usuario ajustar el umbral de similitud y el tipo de join a realizar.

La aplicación está disponible en línea y puedes acceder a ella directamente sin necesidad de instalación:

🔗 **[Acceder a la aplicación](https://fuzzyjoin.streamlit.app/)**

## Características

- **Carga de Archivos**: Permite subir dos archivos en formato CSV o Excel.
- **Selección de Hojas y Columnas**: Si se trata de archivos Excel, se pueden seleccionar las hojas específicas. También se pueden elegir las columnas de texto para realizar el match.
- **Ajuste de Opciones**:
  - Indicar si los archivos tienen encabezados y establecer offsets (filas a saltar).
  - Seleccionar el umbral de similitud (entre 0 y 1).
  - Elegir el tipo de join: Inner Join, Left Join, Right Join, Outer Join.
- **Manejo de Duplicados**: Detecta duplicados problemáticos y ofrece opciones para manejarlos (conservar primero, conservar último, eliminar duplicados).
- **Resultados**:
  - Muestra una vista previa de los archivos y el resultado del match.
  - Permite descargar el resultado en formato Excel.

## Uso

1. **Acceder a la Aplicación**

   Visita el siguiente enlace en tu navegador web:

   🔗 **[https://fuzzyjoin.streamlit.app/](https://fuzzyjoin.streamlit.app/)**

2. **Cargar Archivos**

   - Sube el primer y segundo archivo (CSV o Excel) utilizando los botones de carga.
   - Si los archivos son de Excel, selecciona la hoja que deseas usar.

3. **Configurar Opciones de Carga**

   - Indica si cada archivo tiene encabezado.
   - Establece el offset (número de filas a saltar al inicio del archivo).

4. **Vista Previa de Datos**

   - La aplicación mostrará una vista previa de las primeras dos filas de cada archivo y el número total de filas.

5. **Seleccionar Columnas para el Match**

   - Elige las columnas de texto de cada archivo que deseas comparar.

6. **Ajustar Opciones de Similitud**

   - Selecciona el umbral de similitud deseado mediante el control deslizante.
   - Elige el tipo de join que deseas realizar.

7. **Manejo de Duplicados**

   - Si hay duplicados problemáticos en las columnas seleccionadas, la aplicación te notificará y ofrecerá opciones para resolverlos.

8. **Realizar el Match**

   - Haz clic en el botón **"Realizar Match"** para iniciar el proceso de comparación y unión.

9. **Visualizar y Descargar Resultados**

   - La aplicación mostrará el resultado del match, ordenado por puntaje de similitud.
   - Puedes descargar el resultado en formato Excel utilizando el botón de descarga.

## Detalles Técnicos

- **Modelo de Similitud Semántica**: Utiliza el modelo `sentence-transformers/all-MiniLM-L6-v2` para generar embeddings de los textos y calcular la similitud coseno entre ellos.
- **Tipos de Join Soportados**:
  - **Inner Join**: Combina registros que tienen coincidencias en ambos archivos.
  - **Left Join**: Todos los registros del archivo izquierdo y los coincidentes del derecho.
  - **Right Join**: Todos los registros del archivo derecho y los coincidentes del izquierdo.
  - **Outer Join**: Todos los registros cuando hay coincidencia o no en ambos archivos.
- **Umbral de Similitud**: Los registros con un puntaje de similitud por debajo del umbral establecido serán considerados como no coincidentes.

## Consideraciones

- **Columnas de Texto**: Solo se pueden seleccionar columnas de tipo texto (dtype `object`) para realizar el match.
- **Manejo de Nulos**: Las filas con valores nulos en las columnas seleccionadas serán ignoradas en el proceso de matching.
- **Duplicados**: Es importante manejar los duplicados para evitar resultados inesperados. La aplicación proporciona opciones para gestionar duplicados problemáticos.
- **Rendimiento**: Para conjuntos de datos muy grandes, el proceso puede ser intensivo en recursos y demorar más tiempo.

## Ejemplo de Uso

Supongamos que tienes dos archivos:

- **Archivo 1**: Lista de productos con una columna "Descripción Producto".
- **Archivo 2**: Lista de inventario con una columna "Detalle Ítem".

Quieres unir ambos archivos para encontrar productos similares basándote en las descripciones, incluso si los textos no son exactamente iguales.

Pasos:

1. Accede a la aplicación y carga ambos archivos.
2. Selecciona las columnas "Descripción Producto" y "Detalle Ítem" para hacer el match.
3. Ajusta el umbral de similitud según lo estricto que desees que sea el match (por ejemplo, 0.8).
4. Elige el tipo de join, por ejemplo, Inner Join.
5. Realiza el match y revisa los resultados.
6. Descarga el archivo resultante para su posterior análisis.

## Preguntas Frecuentes

- **¿Qué hace el umbral de similitud?**

  El umbral determina qué tan similares deben ser dos textos para ser considerados una coincidencia. Un valor cercano a 1 requiere una alta similitud, mientras que un valor más bajo permite coincidencias más flexibles.

- **¿Puedo usar columnas numéricas para el match?**

  No, actualmente la aplicación solo soporta columnas de texto para realizar el match basado en similitud semántica.

- **El proceso es lento, ¿qué puedo hacer?**

  Para mejorar el rendimiento, puedes reducir el tamaño de tus datos o aumentar el umbral de similitud para reducir el número de comparaciones.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Créditos

- [Streamlit](https://streamlit.io/) - Framework web utilizado para crear la aplicación.
- [Sentence Transformers](https://www.sbert.net/) - Biblioteca utilizada para calcular la similitud semántica.
- [Pandas](https://pandas.pydata.org/) - Biblioteca para manipulación y análisis de datos.

## Contacto

Para preguntas o sugerencias:

- **GitHub**: fabherhe

---

¡Gracias por usar esta aplicación! Esperamos que te sea de gran utilidad en tus proyectos de análisis de datos.
