import os
import boto3
from dotenv import load_dotenv
import glob
from utils.aws_client import session

load_dotenv()

# Initialize S3 client
s3_client = session.client('s3')

def upload_file(file_path, bucket, key):
    """Upload a file to S3."""
    try:
        print(f"Uploading {file_path} to s3://{bucket}/{key}")
        s3_client.upload_file(file_path, bucket, key)
        print(f"Successfully uploaded {file_path}")
    except Exception as e:
        print(f"Error uploading {file_path}: {str(e)}")
        raise

def upload_metadata():
    """Upload metadata file to S3."""
    metadata_path = 'data/metadata_api.json'
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    
    bucket = os.getenv('METADATA_BUCKET')
    key = 'metadata/metadata_api.json'
    
    upload_file(metadata_path, bucket, key)

def upload_telemetry():
    """Upload telemetry files to S3."""
    telemetry_files = glob.glob('data/telemetry_data_*.csv')
    if not telemetry_files:
        raise FileNotFoundError("No telemetry files found in data directory")
    
    bucket = os.getenv('TELEMETRY_BUCKET')
    
    for file_path in telemetry_files:
        file_name = os.path.basename(file_path)
        key = f'raw/{file_name}'
        
        upload_file(file_path, bucket, key)

def main():
    print("Starting S3 upload process...")
    
    try:
        # Upload metadata
        print("\nUploading metadata...")
        upload_metadata()
        
        # Upload telemetry data
        print("\nUploading telemetry data...")
        upload_telemetry()
        
        print("\nUpload process completed successfully!")
        
    except Exception as e:
        print(f"\nError during upload process: {str(e)}")
        raise

if __name__ == "__main__":
    main() 