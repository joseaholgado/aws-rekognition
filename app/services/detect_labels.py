#!/usr/bin/python3

import os
import json
import boto3
import logger
import logging
from botocore.exceptions import ClientError

from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

# Get env variables
accessKeyId = os.environ.get('ACCESS_KEY_ID')
secretKey = os.environ.get('ACCESS_SECRET_KEY')
bucket = os.environ.get('BUCKET_SOURCE')
region = os.environ.get('REGION')

# Create the service Rekognition and assign credentials
rekognition_client = boto3.Session(
    aws_access_key_id=accessKeyId,
    aws_secret_access_key=secretKey,
    region_name=region).client('rekognition')

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Aqui me busca en la imagen las etiquetas hasta un max de 10
def detect_labels(image, max_labels=10):
    """
    Detects labels in the image. Labels are objects and people.

    :param image: The image data (S3 object) to analyze.
    :param max_labels: The maximum number of labels to return.
    :return: A list of labels detected in the image.
    """
    try:
        # Call Rekognition service to detect labels
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': image}},  # Assuming image is from S3
            MaxLabels=max_labels
        )
        
        # Extract just the label names
        labels = [label['Name'] for label in response["Labels"]]
        logger.info("Found %s labels in image %s.", len(labels), image)
        
          # Save the labels to a JSON file
        with open('detected_labels.json', 'w') as json_file:
            json.dump(labels, json_file, indent=4)  # Write labels to a JSON file with indentation
        
    except ClientError as e:
        logger.error("Couldn't detect labels in %s: %s", image, e)
        raise Exception("An error occurred during label detection.")
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        raise
    
    return labels