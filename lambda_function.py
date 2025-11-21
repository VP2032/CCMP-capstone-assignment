import boto3
from PIL import Image
import io
import os
import json

s3 = boto3.client('s3')

SOURCE_BUCKET = os.environ['SOURCE_BUCKET']
DEST_BUCKET = os.environ['DEST_BUCKET']

def lambda_handler(event, context):
    key = event["key"]

    obj = s3.get_object(Bucket=SOURCE_BUCKET, Key=key)
    img_data = obj["Body"].read()

    image = Image.open(io.BytesIO(img_data))

    image.thumbnail((128, 128))

    buffer = io.BytesIO()
    image.save(buffer, format=image.format or "JPEG")
    buffer.seek(0)

    resized_key = f"thumb-{key}"

    s3.put_object(
        Bucket=DEST_BUCKET,
        Key=resized_key,
        Body=buffer,
        ContentType=obj["ContentType"]
    )

    return {
        "statusCode": 200,
        "resized_key": resized_key
    }
