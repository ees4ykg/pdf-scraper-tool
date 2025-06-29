import base64
import json
import re
from io import BytesIO

from document_to_image import pdf_to_images
from text_from_image import extract_text_from_images

def parse_multipart(event):
    content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
    boundary = re.search('boundary=(.*)', content_type).group(1)
    decoded_body = base64.b64decode(event['body'])

    # Split by boundary
    parts = decoded_body.split(f'--{boundary}'.encode())[1:-1]

    files = []
    for part in parts:
        if b'Content-Disposition' in part:
            # Extract the binary content after two CRLFs
            headers, file_bytes = part.split(b'\r\n\r\n', 1)
            file_bytes = file_bytes.rsplit(b'\r\n', 1)[0]  # Remove trailing newline
            files.append(BytesIO(file_bytes))

    return files



def lambda_handler(event, context):
    try:
        files = parse_multipart(event)

        full_text = ""
        for file in files:
            pdf_bytes = file.read()
            images = pdf_to_images(pdf_bytes)
            full_text += extract_text_from_images(images)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:8080",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(full_text)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
