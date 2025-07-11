# Deteccion-fracturas-curvelets
Bienvenido a mi solución a mi examen para el ramo Procesamiento Multiescala de Imágenes, el cual intenta detectar fracturas en radiografías de mano utilizando la transformada curvelet

# Como utilizar
Primero es necesario descargar el dataset FracAtlas [1]. La carpeta de este dataset debe colocarse en el mismo directorio que el resto de archivos de este repositorio. Esto es por la definición de la función *read_json* en *auxiliar.py*. 

## Contenido
* *auxiliar.py*: Contiene funciones auxiliares para facilitar creación de gráficos, lectura del dataset y preprocesamiento de imagen
* *curvelet.py*: Contiene funciones creadas basadas en la librería *curvelets* [2], entre ellas, aplicaciones de la transformada, su inversa, y threshold de sus coeficientes
* *test.ipynb* : Arhivo de test donde se muestran ejemplos de implementación de la transformada curvelet para detectar radiografías

# Referencias
[1] I. Abedeen et al. “FracAtlas: A Dataset for Fracture
Classification, Localization and Segmentation of Muscu-
loskeletal Radiographs”. In: Scientific Data 10.1 (2023),
p. 521. DOI: 10.1038/s41597-023-02432-4. URL: https:
//doi.org/10.1038/s41597-023-02432-4.

[2] Carlos Alberto Da Costa Filho. Curvelets documentation.
https : / / curvelets . readthedocs . io / en / latest / index . html.
Made with Sphinx and @pradyunsg’s Furo. 2024

