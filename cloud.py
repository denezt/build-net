import boto3
from google.cloud import storage
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def upload_to_cloud(local_dir: str, provider: str):
    """Upload processed files to cloud storage"""
    if provider == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
        )
        for path in Path(local_dir).glob("*.json"):
            s3.upload_file(str(path), os.getenv("AWS_BUCKET"), path.name)
    elif provider == "gcs":
        client = storage.Client()
        bucket = client.get_bucket(os.getenv("GCS_BUCKET"))
        for path in Path(local_dir).glob("*.json"):
            blob = bucket.blob(path.name)
            blob.upload_from_filename(str(path))
