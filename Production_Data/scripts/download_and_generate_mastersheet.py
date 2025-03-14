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

def download_from_gcp(bucket_name: str, file_names: List[str], destination_folder: str) -> List[str]:
    """
    Download specific files from GCP bucket to local folder.
    
    Args:
        bucket_name: Name of the GCP bucket
        file_names: List of file names to download from the bucket
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
        
        # Download each specified file
        for file_name in file_names:
            blob = bucket.blob(file_name)
            destination_file = os.path.join(destination_folder, os.path.basename(file_name))
            
            try:
                blob.download_to_filename(destination_file)
                print(f"Downloaded: {file_name} to {destination_file}")
                downloaded_files.append(destination_file)
            except Exception as e:
                print(f"Error downloading {file_name}: {str(e)}")
        
        if not downloaded_files:
            raise Exception("No files were downloaded successfully")
            
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
    for file_path in file_paths[:2]:
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
    parent_dir = os.path.dirname(script_dir)
    
    # Set up GCP credentials
    # set_gcp_credentials()
    
    # Configuration
    BUCKET_NAME = "comsol_ldg"  # Replace with your bucket name
    prefix = 'Eagle_Vision_Working_Data_Warehouse/'  # Added trailing slash for path joining

    base_files = [
        "13-7.json",
        "17-7.json",
        "32-18.json",
        "45-7.json",
        "45A-7.json",
        "53-7ST.json",
        "55-7.json",
        "63-7.json",
        "66-7.json",
        "66A-7.json",
        "75-7.json",
        "76-7.json"
    ]

    # Create full file paths by joining prefix with each file name
    FILE_NAMES = [prefix + file_name for file_name in base_files]
        
    RAW_DATA_FOLDER = os.path.join(parent_dir, "RawData")
    MASTERSHEET_PATH = os.path.join(parent_dir, "CleanData/Production.csv")
    
    # Download files from GCP
    downloaded_files = download_from_gcp(
        bucket_name=BUCKET_NAME,
        file_names=FILE_NAMES,
        destination_folder=RAW_DATA_FOLDER
    )
    
    # Combine files into mastersheet
    combine_csv_files(
        file_paths=downloaded_files,
        output_path=MASTERSHEET_PATH
    )

if __name__ == "__main__":
    main() 