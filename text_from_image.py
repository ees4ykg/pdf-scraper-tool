import os
from PIL import Image
import boto3
from io import BytesIO



def extract_text_from_image(image_filelike):
    """
    Extract text from a single image using Amazon Textract.
    `image_filelike` must be a file-like object (e.g. BytesIO)
    """
    try:
        image_bytes = image_filelike.read()
        textract = boto3.client("textract")

        response = textract.detect_document_text(Document={'Bytes': image_bytes})

        text_lines = [
            block["Text"]
            for block in response.get("Blocks", [])
            if block["BlockType"] == "LINE"
        ]

        return "\n".join(text_lines).strip()

    except Exception as e:
        print(f"Error processing image with Textract: {e}")
        return ""

def extract_text_from_images(images):
    """
    Extract text from all images in a directory
    """
    text = ""
    for image in images:
        text += extract_text_from_image(BytesIO(image))
    return text.strip()



