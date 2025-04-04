import os
import subprocess
from dotenv import load_dotenv
from utils.aws_client import session

load_dotenv()

lambda_client = session.client("lambda")

def zip_lambda(lambda_name: str, source_file: str, zip_path: str):
    print(f"Zipping {lambda_name} code...")
    subprocess.run(["zip", "-j", zip_path, source_file], check=True)

def update_lambda(lambda_name: str, zip_path: str):
    print(f"Updating Lambda {lambda_name}...")
    with open(zip_path, "rb") as f:
        lambda_client.update_function_code(
            FunctionName=lambda_name,
            ZipFile=f.read(),
            Publish=True
        )
    print(f"Deployed {lambda_name} successfully!")

if __name__ == "__main__":
    os.makedirs("dist", exist_ok=True)

    lambdas = {
        "ingestion-lambda": "lambdas/ingestion_lambda.py",
        "consumer-lambda": "lambdas/consumer_lambda.py"
    }

    for name, path in lambdas.items():
        zip_path = f"dist/{name}.zip"
        zip_lambda(name, path, zip_path)
        update_lambda(name, zip_path) 