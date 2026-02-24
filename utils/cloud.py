import os
import boto3
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# This module handles uploading processed files to
# cloud storage providers like AWS S3.
def upload_to_cloud(local_dir: str, provider: str):
    """Upload processed files to cloud storage"""
    if provider == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
        )
        for path in Path(local_dir).glob("*.json"):
            s3.upload_file(str(path), os.getenv("AWS_S3_BUCKET"), path.name)
    else:
        raise ValueError(f"Unsupported cloud provider: {provider}")