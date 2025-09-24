import boto3
import argparse
import logging
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- IMPORTANT ---
# Replace this with your actual S3 bucket name.
# It must be globally unique.
S3_BUCKET_NAME = "my-unique-data-bucket-1234-5"


def list_files(bucket_name):
    """
    Lists files in an S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    """
    s3_client = boto3.client('s3')
    try:
        logging.info(f"Listing files in bucket: {bucket_name}")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for item in response['Contents']:
                print(f"- {item['Key']} (Size: {item['Size']} bytes)")
        else:
            print("Bucket is empty.")
    except ClientError as e:
        logging.error(f"Could not list files in bucket {bucket_name}: {e}")
        return False
    return True


def upload_file(bucket_name, file_path, object_name=None):
    """
    Upload a file to an S3 bucket.

    :param bucket_name: Bucket to upload to.
    :param file_path: Path to the file to upload.
    :param object_name: S3 object name. If not specified, file_path is used.
    :return: True if file was uploaded, else False.
    """
    if object_name is None:
        object_name = file_path

    s3_client = boto3.client('s3')
    try:
        logging.info(f"Uploading {file_path} to {bucket_name}/{object_name}...")
        s3_client.upload_file(file_path, bucket_name, object_name)
        logging.info("Upload successful.")
    except FileNotFoundError:
        logging.error(f"The file was not found: {file_path}")
        return False
    except ClientError as e:
        logging.error(f"Could not upload file: {e}")
        return False
    return True


def download_file(bucket_name, object_name, file_path):
    """
    Download a file from an S3 bucket.

    :param bucket_name: Bucket to download from.
    :param object_name: S3 object name.
    :param file_path: Local path to save the downloaded file.
    :return: True if file was downloaded, else False.
    """
    s3_client = boto3.client('s3')
    try:
        logging.info(f"Downloading {bucket_name}/{object_name} to {file_path}...")
        s3_client.download_file(bucket_name, object_name, file_path)
        logging.info("Download successful.")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logging.error(f"The object {object_name} does not exist in bucket {bucket_name}.")
        else:
            logging.error(f"Could not download file: {e}")
        return False
    return True


if __name__ == "__main__":
    if S3_BUCKET_NAME == "your-unique-bucket-name-here":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! PLEASE EDIT THE SCRIPT AND SET `S3_BUCKET_NAME`    !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        parser = argparse.ArgumentParser(description="AWS S3 File Management Script")
        parser.add_argument("action", choices=['list', 'upload', 'download'], help="The action to perform.")
        parser.add_argument("source", nargs='?', help="Source file for upload, or S3 object for download.")
        parser.add_argument("destination", nargs='?', help="Destination path for upload or download.")

        args = parser.parse_args()

        if args.action == "list":
            list_files(S3_BUCKET_NAME)
        elif args.action == "upload":
            if not args.source:
                print("Error: Upload action requires a source file path.")
            else:
                upload_file(S3_BUCKET_NAME, args.source, args.destination)
        elif args.action == "download":
            if not args.source or not args.destination:
                print("Error: Download action requires an S3 object name (source) and a local file path (destination).")
            else:
                download_file(S3_BUCKET_NAME, args.source, args.destination)
