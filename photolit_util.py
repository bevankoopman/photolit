from google.cloud import storage
from google.oauth2 import service_account
from tabulate import tabulate
import argparse
import os
from tqdm import tqdm
from datetime import datetime
import json

key_json = os.getenv("GCP_SERVICE_ACCOUNT_KEY")

if key_json is None:
    print("GCP service account key not found. Please set the GCP_SERVICE_ACCOUNT_KEY environment variable.")
    exit(1)

key_dict = json.loads(key_json)
credentials = service_account.Credentials.from_service_account_info(key_dict)
client = storage.Client(credentials=credentials, project=key_dict["project_id"])
bucket = client.bucket("photolit")
blobs = list(bucket.list_blobs())

def list_bucket_files(bucket_name):
    """List all files in a GCS bucket with formatted output"""
    try:


        files_data = [
            [blob.name, f"{blob.size / 1024:.2f} KB", blob.updated.strftime('%Y-%m-%d %H:%M:%S')]
            for i, blob in enumerate(blobs) if "1_image" in blob.name.strip()
        ]

        headers = ['File Name', 'Size', 'Last Modified']
        print(tabulate(files_data, headers=headers, tablefmt='grid'))
        print(f"\nTotal files: {len(blobs)}")
        print(f"Total kids: {len(files_data)} ({len(blobs)/len(files_data):.1f} photos per kid on average)")

    except Exception as e:
        print(f"Error: {str(e)}")

def sync_files(bucket_name, local_dir):
    """Sync files from bucket to local directory"""
    try:

        # Create local directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)

        current_files = os.listdir(local_dir)

        files_to_download = [blob.name for blob in blobs if blob.name not in current_files]
        print(f"Found {len(files_to_download)} files to download")

        for files_to_download in tqdm(files_to_download, desc="Syncing files"):
            blob = bucket.blob(files_to_download)
            local_path = os.path.join(local_dir, files_to_download)
            blob.download_to_filename(local_path)



    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Google Cloud Storage bucket utilities')
    parser.add_argument('--bucket_name', type=str, default='photolit', help='Name of the GCS bucket')
    parser.add_argument('--sync', help='Local directory to sync files to')
    args = parser.parse_args()

    list_bucket_files(args.bucket_name)

    if args.sync:
        print(f"\nSyncing files to {args.sync}")
        sync_files(args.bucket_name, args.sync)

if __name__ == "__main__":
    main()