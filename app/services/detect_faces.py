import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
region = os.environ.get('REGION')

# Crear el cliente de Rekognition especificando la región
rekognition_client = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey,
    region_name=region).client('rekognition')

def detect_face_expressions(bucket_name, file_name):
    """
    Detecta las expresiones faciales de una imagen en un bucket de S3 utilizando Amazon Rekognition.

    :param bucket_name: El nombre del bucket S3 que contiene la imagen.
    :param file_name: El nombre del archivo de imagen en S3.
    :return: Las expresiones faciales detectadas en la imagen.
    """
    try:
        # Llamar al servicio Rekognition para detectar caras en la imagen
        response = rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': file_name}},
            Attributes=['ALL']  # Obtener todas las características, incluidas las expresiones faciales
        )

        # Verificar si se detectaron caras
        if not response['FaceDetails']:
            return "No se detectaron caras en la imagen."

        # Extraer las expresiones faciales de los resultados
        face_expressions = []
        for face in response['FaceDetails']:
            emotions = face.get('Emotions', [])
            for emotion in emotions:
                expression = emotion['Type']
                confidence = emotion['Confidence']
                face_expressions.append(f"{expression}: {confidence:.2f}%")

        # Si no hay expresiones, decir que no hay emociones claras
        if not face_expressions:
            return "No se detectaron expresiones faciales claras."

        return face_expressions
    
    except Exception as e:
        return f"Error al procesar la imagen: {str(e)}"
