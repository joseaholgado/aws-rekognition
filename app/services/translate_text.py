import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Asegúrate de cargar las variables de entorno en la función
def translate_text(text, source_lang='en', target_lang='es'):
    """
    Traduce un texto usando AWS Translate.

    :param text: El texto que se va a traducir.
    :param source_lang: El idioma de origen del texto.
    :param target_lang: El idioma al que se traducirá el texto.
    :return: El texto traducido.
    """
    load_dotenv()  # Cargar las variables de entorno (si no se ha hecho anteriormente)
    
    accessKeyId = os.environ.get('ACCESS_KEY_ID')
    secretKey = os.environ.get('ACCESS_SECRET_KEY')
    region = os.environ.get('REGION')

    # Crear el cliente de AWS Translate especificando la región
    translate_client = boto3.Session(
        aws_access_key_id=accessKeyId,
        aws_secret_access_key=secretKey,
        region_name=region).client('translate')

    try:
        # Llamada al servicio de AWS Translate para traducir el texto
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )

        # Extraer y devolver el texto traducido
        return response['TranslatedText']

    except ClientError as e:
        # Manejo de errores en caso de que falle la traducción
        print(f"Error al traducir el texto: {e}")
        return None
