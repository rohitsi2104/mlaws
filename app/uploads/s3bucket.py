import boto3
from botocore.exceptions import NoCredentialsError
import uuid
import os

unique_filename = str(uuid.uuid4())

class S3Uploader:
    def __init__(self, s3_bucket_name):
        self.s3_bucket_name = s3_bucket_name
        self.s3 = boto3.client('s3')

    def upload_model(self, file_path):
        try:

            file_extension = os.path.splitext(file_path)[1]

            unique_file_path = unique_filename + file_extension

            with open(file_path, 'rb') as file:
                self.s3.upload_fileobj(file, self.s3_bucket_name, unique_file_path)

            print(f"Model file '{file_path}' uploaded successfully to S3 bucket '{self.s3_bucket_name}' with unique filename '{unique_file_path}'")

        except NoCredentialsError:
            print("AWS credentials not available. Make sure your AWS credentials are configured.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
