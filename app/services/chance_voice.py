import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
region = os.environ.get('REGION')

# Crear el cliente de Polly especificando la región
polly_client = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey,
    region_name=region).client('polly')

def chance_voice(file, key):
    """
    Convierte el texto a voz y guarda el archivo con el nombre 'voice_{key}.mp3'.

    :param file: El texto que se convertirá a voz.
    :param key: El nombre del archivo para generar un nombre único para el archivo de salida.
    :return: El nombre del archivo de voz.
    """
    
    # Llamar al servicio Polly para sintetizar la voz
    response = polly_client.synthesize_speech(Text=file, OutputFormat='mp3', VoiceId='Joanna')

    # Leer el flujo de audio de la respuesta
    body = response["AudioStream"].read()

    # Crear el archivo de salida
    file_name = f"voice_{key}.mp3"
    with open(file_name, "wb") as output_file:
        output_file.write(body)

    return file_name

def chance_voice_es(file, key):
    """
    Convierte el texto a voz y guarda el archivo con el nombre 'voice_{key}.mp3'.

    :param file: El texto que se convertirá a voz.
    :param key: El nombre del archivo para generar un nombre único para el archivo de salida.
    :return: El nombre del archivo de voz.
    """
    
    # Llamar al servicio Polly para sintetizar la voz
    response = polly_client.synthesize_speech(Text=file, OutputFormat='mp3', VoiceId='Miguel')

    # Leer el flujo de audio de la respuesta
    body = response["AudioStream"].read()

    # Crear el archivo de salida
    file_name = f"translate_voice_{key}.mp3"
    with open(file_name, "wb") as output_file:
        output_file.write(body)

    return file_name
