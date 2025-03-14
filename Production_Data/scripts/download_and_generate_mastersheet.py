#!/usr/bin/env python3

import os
from google.cloud import storage
import pandas as pd
from typing import List

def set_gcp_credentials():
    """
    Set up GCP credentials from the service account key file.
    The key file should be named 'service-account-key.json' and placed in the same directory as this script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(script_dir, 'service-account-key.json')
    
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"GCP credentials file not found at {credentials_path}. "
            "Please place your service-account-key.json file in the same directory as this script."
        )
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    print(f"GCP credentials set from: {credentials_path}")

def ensure_directory(directory: str):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_from_gcp(bucket_name: str, source_blob_prefix: str, destination_folder: str) -> List[str]:
    """
    Download files from GCP bucket to local folder.
    
    Args:
        bucket_name: Name of the GCP bucket
        source_blob_prefix: Prefix to filter blobs in the bucket
        destination_folder: Local folder to save downloaded files
        
    Returns:
        List of downloaded file paths
    """
    # Ensure the destination folder exists
    ensure_directory(destination_folder)
    
    try:
        # Initialize GCP client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        downloaded_files = []
        
        # List all blobs with the given prefix
        blobs = bucket.list_blobs(prefix=source_blob_prefix)
        
        for blob in blobs:
            # Skip if it's a directory
            if blob.name.endswith('/'):
                continue
                
            destination_file = os.path.join(destination_folder, os.path.basename(blob.name))
            blob.download_to_filename(destination_file)
            print(f"Downloaded: {blob.name} to {destination_file}")
            downloaded_files.append(destination_file)
        
        return downloaded_files
        
    except Exception as e:
        print(f"Error accessing GCP bucket: {str(e)}")
        print("Please verify your credentials and bucket configuration.")
        raise

def combine_csv_files(file_paths: List[str], output_path: str):
    """
    Combine multiple CSV files into a single mastersheet.
    
    Args:
        file_paths: List of CSV file paths to combine
        output_path: Path where the combined CSV will be saved
    """
    # Read and combine all CSV files
    dataframes = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        dataframes.append(df)
    
    # Concatenate all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Save the combined dataframe
    combined_df.to_csv(output_path, index=False)
    print(f"Created mastersheet: {output_path}")

def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set up GCP credentials
    set_gcp_credentials()
    
    # Configuration
    BUCKET_NAME = "your-bucket-name"  # Replace with your bucket name
    SOURCE_PREFIX = "your/prefix/"    # Replace with your prefix
    RAW_DATA_FOLDER = os.path.join(script_dir, "RawData")
    MASTERSHEET_PATH = os.path.join(script_dir, "mastersheet.csv")
    
    # Download files from GCP
    downloaded_files = download_from_gcp(
        bucket_name=BUCKET_NAME,
        source_blob_prefix=SOURCE_PREFIX,
        destination_folder=RAW_DATA_FOLDER
    )
    
    # Combine files into mastersheet
    combine_csv_files(
        file_paths=downloaded_files,
        output_path=MASTERSHEET_PATH
    )

if __name__ == "__main__":
    main() 