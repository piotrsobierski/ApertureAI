import boto3
import json
from dotenv import load_dotenv

load_dotenv()

def get_image_labels(image_bytes: bytes, max_labels: int = 10, min_confidence: float = 75.0) -> dict:
    """
    Detects labels in an image using Amazon Rekognition.

    Args:
        image_bytes: The image data as bytes.
        max_labels: The maximum number of labels to return.
        min_confidence: The minimum confidence level for labels to be returned.

    Returns:
        A dictionary containing the labels detected by Rekognition.
        See AWS Rekognition DetectLabels API documentation for response structure.
    
    Raises:
        Exception: If the API call to Rekognition fails.
    """
    try:
        rekognition_client = boto3.client('rekognition')
        response = rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )
        return response
    except Exception as e:
        print(f"Error calling Rekognition DetectLabels: {e}")
        raise