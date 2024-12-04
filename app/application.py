import boto3
import os
import json
import requests
from flask import Flask, request, Response, abort, render_template, jsonify
from dotenv import load_dotenv
from services.detect_labels import detect_labels 
from services.chance_voice import chance_voice, chance_voice_es
from services.translate_text import translate_text
from services.detect_faces import detect_face_expressions


# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener variables de entorno
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
bucket_source = os.environ.get('BUCKET_SOURCE')
bucket_dest = os.environ.get('BUCKET_DEST')

# Crear aplicación Flask
application = Flask(__name__)

# Crear el recurso de S3 y asignar credenciales
s3 = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey).resource('s3')

# Ruta principal para la página de inicio
@application.route('/', methods=['GET'])
def index():
    try:
        files = [obj.key for obj in s3.Bucket(bucket_source).objects.all()]
    except Exception as e:
        application.logger.error(f"Error al obtener los archivos del bucket: {str(e)}")
        files = []
    
    return render_template('index.html', files=files)

# Ruta para la descarga de archivos desde el bucket S3
@application.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    try:
        # Obtener el objeto desde el bucket de S3
        obj = s3.Object(bucket_dest, file_name)
        # Descargar el archivo en el cliente (con el nombre original)
        response = obj.get()
        
        # Devolver el archivo como una respuesta de descarga
        return Response(
            response['Body'].read(),
            content_type='application/octet-stream',
            headers={'Content-Disposition': f'attachment; filename={file_name}'}
        )
    except Exception as e:
        application.logger.error(f"Error al descargar el archivo: {str(e)}")
        return jsonify({'error': 'Error al descargar el archivo'}), 500

# Ruta para obtener archivos del bucket destino
@application.route('/get-dest-files', methods=['GET'])
def get_dest_files():
    files_from_dest = get_files_from_bucket(bucket_dest)
    return jsonify({'files': files_from_dest})

# Función para obtener archivos de un bucket específico
def get_files_from_bucket(bucket_name):
    try:
        # Obtener los objetos del bucket especificado
        files = [obj.key for obj in s3.Bucket(bucket_name).objects.all()]
        return files
    except Exception as e:
        application.logger.error(f"Error al obtener los archivos del bucket {bucket_name}: {str(e)}")
        return []

# Ruta para el procesamiento de la imagen
@application.route('/process-image', methods=['POST'])
def process_image():
    data = request.get_json()
    file_name = data.get('file_name')

    if not file_name:
        return jsonify({"message": "Falta el nombre del archivo"}), 400

    analyze_url = f'http://localhost:5000/api/analyze'
    response = requests.post(analyze_url, json={'key': file_name})

    if response.status_code == 200:
        return jsonify({"message": f"Imagen {file_name} procesada correctamente","reload": True})
    else:
        return jsonify({"message": "Error al procesar la imagen","reload": False}), 500

# Ruta para la vista previa de un archivo
@application.route('/file-preview/<file_name>', methods=['GET'])
def file_preview(file_name):
    try:
        obj = s3.Object(bucket_source, file_name)
        return Response(obj.get()['Body'].read(), content_type='image/jpeg')
    except Exception as e:
        application.logger.error(f"Error al obtener el archivo de S3: {str(e)}")
        abort(404)

# Ruta para subir un archivo al bucket
@application.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Subir archivo al bucket S3
        s3.Bucket(bucket_source).put_object(Key=file.filename, Body=file)
        return jsonify({'message': 'Archivo subido correctamente'}), 200
    except Exception as e:
        application.logger.error(f"Error al subir el archivo a S3: {str(e)}")
        return jsonify({'error': f'Error al subir el archivo: {str(e)}'}), 500

# Ruta para la API de análisis de imagen
@application.route('/api/analyze', methods=['POST'])
def analyze_image():
    # Obtener el nombre del archivo desde el request
    data = request.get_json()
    key = data.get('key')
    if not key:
        abort(400, description="La clave 'key' es requerida en el JSON de entrada")
    
    try:
        # Detectar etiquetas en la imagen y guardarlas en un archivo JSON
        labels = detect_labels(key)
        labels_json = json.dumps(labels, indent=4)
        json_file_name = f"labels_{key}.json"
        
        # Guardar el archivo JSON en el bucket de destino
        s3.Object(bucket_dest, json_file_name).put(Body=labels_json)

        # Generar una descripción en lenguaje natural basada en las etiquetas
        if labels:
            texto_etiquetas = f"In the image '{key}' you can see " + ", ".join(labels[:-1]) + " and " + labels[-1] + "."
        else:
            texto_etiquetas = f"No significant labels were detected in the image '{key}'."

        # Generar archivo de voz a partir de la descripción
        voice_file_name = chance_voice(texto_etiquetas, key)

        # Subir archivo de voz al bucket de destino
        with open(voice_file_name, "rb") as voice_file:
            s3.Object(bucket_dest, voice_file_name).put(Body=voice_file)

        # Traducir el texto a español 
        translated_text = translate_text(texto_etiquetas, source_lang='en', target_lang='es')

        if translated_text:
            # Guardar el texto traducido en un archivo de texto en el bucket S3
            translated_file_name = f"translated_{key}.txt"
            s3.Object(bucket_dest, translated_file_name).put(Body=translated_text)

            voice_file_name_es = chance_voice_es(translated_text, key)
            s3.Object(bucket_dest, voice_file_name_es).put(Body=translated_text)

        # Detectar las expresiones faciales en la imagen
        face_expressions = detect_face_expressions(bucket_source, key)

        # Guardar las expresiones faciales detectadas en un archivo JSON
        if isinstance(face_expressions, list):  # Si se detectan expresiones faciales
            face_expressions_json = json.dumps(face_expressions, indent=4)
            expressions_file_name = f"expressions_{key}.json"
            s3.Object(bucket_dest, expressions_file_name).put(Body=face_expressions_json)
        else:
            # Si no se detectan expresiones, puedes poner un mensaje indicando esto
            expressions_file_name = f"expressions_{key}.json"
            s3.Object(bucket_dest, expressions_file_name).put(Body=json.dumps({"message": face_expressions}))

    except Exception as error:
        print(f"Error en el procesamiento: {error}")
        abort(500, description="Error interno en el servidor")
    
    return Response(status=200)

# Ejecutar la aplicación
if __name__ == "__main__":
    application.debug = True
    application.run()
