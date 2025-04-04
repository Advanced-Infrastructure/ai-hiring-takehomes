import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def run_all():
    """Run all scripts in sequence"""
    print("Starting data generation and upload process...")
    
    # Generate test data
    print("\nGenerating test data...")
    subprocess.run(["python3", "scripts/generate_data.py"], check=True)
    
    # Upload to S3
    print("\nUploading data to S3...")
    subprocess.run(["python3", "scripts/upload_to_s3.py"], check=True)
    
    print("\nProcess completed successfully!")

if __name__ == "__main__":
    run_all() 