# Proyecto de IA con AWS

Este proyecto es una aplicación web desarrollada con Flask, que utiliza los servicios de IA de AWS para procesar imágenes cargadas por los usuarios. La aplicación detecta etiquetas, analiza expresiones faciales, genera descripciones de imágenes, las convierte en voz y las traduce a diferentes idiomas.

## Índice

1. [Descripción](#descripción)
2. [Características](#características)
3. [Requisitos](#requisitos)
4. [Instalación](#instalación)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Uso](#uso)
7. [Licencia](#licencia)

## Descripción

Este proyecto utiliza una arquitectura basada en Flask para el backend, junto con los servicios de Amazon Web Services (AWS), como Amazon Rekognition, Amazon Polly y Amazon Translate, para realizar el procesamiento de imágenes y generar resultados interactivos para el usuario. La aplicación permite al usuario cargar imágenes, que son luego analizadas para detectar etiquetas, expresiones faciales y convertir esas descripciones en voz, así como traducirlas a otros idiomas.

## Características

- **Cargar imágenes**: El usuario puede cargar imágenes desde su dispositivo.
- **Detección de etiquetas**: Amazon Rekognition detecta etiquetas asociadas con la imagen.
- **Análisis de expresiones faciales**: Reconocimiento de expresiones faciales en la imagen.
- **Generación de voz**: Amazon Polly convierte la descripción de la imagen en un archivo de voz.
- **Traducción**: Amazon Translate traduce las descripciones generadas al español.
- **Almacenamiento en la nube**: Las imágenes y los resultados se almacenan de manera segura en Amazon S3.

## Requisitos

- Python 3.x
- Flask
- Boto3 (AWS SDK para Python)
- Otras dependencias de Python listadas en `requirements.txt`.

### Instalación de dependencias

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tuusuario/proyecto_ia_aws.git

2. Navega al dirertorio del proyecto

    ```bash
    cd proyecto_ia_aws

3. Crea un entorno virtual (opcional pero recomendado)

    ```bash
    python3 -m venv venv
    source venv/bin/activate 

4. Instala las dependencias:

    ```bash
    pip install -r requirements.txt

5. Configura las credenciales de AWS:

- Asegúrate de tener configuradas las credenciales de AWS en tu máquina


## Estructura del Proyecto

   
    PROYECTO_IA_AWS/
    ├── app/
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── chance_voice.py
    │   │   ├── detect_faces.py
    │   │   ├── detect_labels.py
    │   │   └── translate_text.py
    │   ├── static/
    │   │   ├── css/
    │   │   │   └── styles.css
    │   │   └── js/
    │   │       ├── functions.js
    │   │       └── main.js
    │   ├── templates/
    │   │   └── index.html
    │   ├── application.py
    │   ├── .env
    │   ├── README.md
    │   └── requirements.txt
    ├── __pycache__/
    └── .gitignore

## Uso

1. Ejecuta la aplicación:

    ```bash
    python app/application.py

2. Abre tu navegador y ve a http://localhost:5000.

3. Carga una imagen desde tu dispositivo usando la interfaz web.

4. La imagen será procesada y se generarán resultados como:

- Descripción en texto de la imagen.
- Archivo de voz con la descripción.
- Traducción al español de la descripción.

5. Descarga los archivos procesados (JSON, MP3, TXT) desde la interfaz de usuario.