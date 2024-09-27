import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
import logging
import json

class S3Uploader:
    def __init__(self, bucket):
        self.s3 = boto3.client('s3')
        self.bucket = bucket
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger('S3Uploader')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('s3_upload.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def check_bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket)
            self.logger.info(f"Bucket {self.bucket} exists and you have access to it.")
            return True
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                self.logger.error(f"Bucket {self.bucket} does not exist.")
            elif error_code == 403:
                self.logger.error(f"You do not have access to bucket {self.bucket}.")
            else:
                self.logger.error(f"Error checking bucket {self.bucket}: {str(e)}")
            return False

    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            self.logger.info(f"Available buckets: {', '.join(buckets)}")
            return buckets
        except Exception as e:
            self.logger.error(f"Error listing buckets: {str(e)}")
            return []

    def upload_file(self, local_path, s3_path):
        try:
            self.logger.debug(f"Attempting to upload {local_path} to {self.bucket}/{s3_path}")
            self.s3.upload_file(local_path, self.bucket, s3_path)
            self.logger.info(f"Uploaded {local_path} to {self.bucket}/{s3_path}")
            return True
        except FileNotFoundError:
            self.logger.error(f"The file {local_path} was not found")
        except NoCredentialsError:
            self.logger.error("Credentials not available")
        except Exception as e:
            self.logger.error(f"Error uploading {local_path}: {str(e)}")
        return False

    def upload_directory(self, local_directory, data_type):
        s3_directory = data_type  # 'raw' or 'processed'
        success = True
        
        self.logger.debug(f"Starting upload of directory: {local_directory}")
        for root, _, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_directory, relative_path)
                
                if not self.upload_file(local_path, s3_path):
                    success = False

        self.logger.debug(f"Finished upload of directory: {local_directory}")
        return success




def get_aws_credentials():
    session = boto3.Session()
    credentials = session.get_credentials()
    return {
        'AccessKeyId': credentials.access_key,
        'SecretAccessKey': credentials.secret_key,
        'Region': session.region_name
    }

# Usage
bucket_name = 'bwf-data-thedarianwong' 
uploader = S3Uploader(bucket_name)

# Print AWS credentials (redacted)
creds = get_aws_credentials()
print(f"AWS Access Key ID: {creds['AccessKeyId'][:5]}...{creds['AccessKeyId'][-3:]}")
print(f"AWS Secret Access Key: {creds['SecretAccessKey'][:5]}...{creds['SecretAccessKey'][-3:]}")
print(f"AWS Region: {creds['Region']}")

# Check if bucket exists
if not uploader.check_bucket_exists():
    available_buckets = uploader.list_buckets()
    print(f"Available buckets: {', '.join(available_buckets)}")
    print("Bucket does not exist or you don't have access. Check s3_upload.log for details.")
else:
    # Get the project root directory (one level up from aws directory)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"Project root directory: {project_root}")

    # For raw data
    local_raw_directory = os.path.join(project_root, "data", "raw")
    print(f"Raw data directory: {local_raw_directory}")
    if os.path.exists(local_raw_directory):
        print(f"Files in raw directory: {os.listdir(local_raw_directory)}")
        uploaded_raw = uploader.upload_directory(local_raw_directory, "raw")
    else:
        print(f"Raw data directory does not exist: {local_raw_directory}")

    # For processed data
    local_processed_directory = os.path.join(project_root, "data", "processed")
    print(f"Processed data directory: {local_processed_directory}")
    if os.path.exists(local_processed_directory):
        print(f"Files in processed directory: {os.listdir(local_processed_directory)}")
        uploaded_processed = uploader.upload_directory(local_processed_directory, "processed")
    else:
        print(f"Processed data directory does not exist: {local_processed_directory}")

# Print out the contents of the log file
with open('s3_upload.log', 'r') as log_file:
    print("\nContents of s3_upload.log:")
    print(log_file.read())