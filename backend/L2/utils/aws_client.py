import boto3
from dotenv import load_dotenv
import os

load_dotenv()

class AWSSession:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'ap-south-1')
        )

    def client(self, service_name):
        return self.session.client(service_name)

    def resource(self, service_name):
        return self.session.resource(service_name)

session = AWSSession() 