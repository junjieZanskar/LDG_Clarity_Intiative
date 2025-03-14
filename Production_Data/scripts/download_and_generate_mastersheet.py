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

def process_json(file_path: str) -> pd.DataFrame:
    """
    Process a single JSON file and return a properly formatted DataFrame.
    The DataFrame will be indexed by Date and sorted chronologically from past to present.
    Only includes Flow, Press, and Temp columns with their respective units.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        pd.DataFrame: Processed DataFrame with Date index and filtered columns
    """
    # Read JSON file
    with open(file_path, 'r') as f:
        import json
        json_data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(json_data)
    
    # Ensure Date column exists
    if 'Date' not in df.columns:
        raise ValueError(f"No 'Date' column found in {file_path}")
    
    # Filter columns that contain Flow, Press, or Temp
    columns_to_keep = []
    for col in df.columns:
        if any(keyword in col for keyword in ['Flow', 'Press', 'Temp']):
            columns_to_keep.append(col)
    
    # Keep only the filtered columns plus Date
    df = df[['Date'] + columns_to_keep]
    
    # Rename columns to include units
    column_mapping = {}
    for col in columns_to_keep:
        if 'Flow' in col:
            column_mapping[col] = f"{col} (gpm)"
        elif 'Press' in col:
            column_mapping[col] = f"{col} (psi)"
        elif 'Temp' in col:
            column_mapping[col] = f"{col} (F)"
    
    df = df.rename(columns=column_mapping)
    
    # Convert Date to datetime and set as index
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Keep only the date part (YYYY-MM-DD) and format as string
    df['Date'] = df['Date'].dt.date.astype(str)
    df.set_index('Date', inplace=True)
    
    # Sort index chronologically (oldest to newest)
    df.sort_index(inplace=True)
    
    return df

def combine_json_files(file_paths: List[str], output_path: str):
    """
    Process multiple JSON files into separate sheets in an Excel file.
    Each JSON file will be transformed into a DataFrame with its own sheet.
    Each sheet will have Date as index, sorted chronologically.
    
    Args:
        file_paths: List of JSON file paths to combine
        output_path: Path where the Excel file will be saved
    """
    # Change output extension to xlsx
    output_path = output_path.replace('.csv', '.xlsx')
    
    # Create Excel writer object
    with pd.ExcelWriter(output_path, engine='openpyxl', datetime_format='yyyy-mm-dd') as writer:
        for file_path in file_paths:
            try:
                # Get well name from file name (remove .json extension)
                well_name = os.path.basename(file_path).replace('.json', '')
                
                # Process JSON file into DataFrame
                df = process_json(file_path)
                
                # Write to Excel with datetime formatting
                df.to_excel(writer, sheet_name=well_name)
                
                # Get the worksheet
                worksheet = writer.sheets[well_name]
                
                # Set column widths and format
                # First column (A) is the index (Date)
                worksheet.column_dimensions['A'].width = 12  # Date column width (shorter now)
                
                # Format other columns
                for idx, col in enumerate(df.columns, start=1):  # Start from B column
                    col_letter = chr(65 + idx)  # B, C, D, etc.
                    
                    # Calculate max width needed
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[col_letter].width = max_length + 2
                    
                    # Format numeric columns
                    if df[col].dtype in ['float64', 'int64']:
                        for cell in worksheet[col_letter][1:]:
                            cell.number_format = '0.00'
                
                print(f"Processed {well_name} data with columns: {', '.join(df.columns)}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
    
    print(f"\nCreated Excel workbook with multiple sheets at: {output_path}")

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
    MASTERSHEET_PATH = os.path.join(parent_dir, "CleanData/Production.xlsx")  # Changed to xlsx
    
    # Ensure CleanData directory exists
    ensure_directory(os.path.dirname(MASTERSHEET_PATH))
    
    # Download files from GCP
    downloaded_files = download_from_gcp(
        bucket_name=BUCKET_NAME,
        file_names=FILE_NAMES,
        destination_folder=RAW_DATA_FOLDER
    )
    
    # Combine files into Excel workbook with multiple sheets
    combine_json_files(
        file_paths=downloaded_files,
        output_path=MASTERSHEET_PATH
    )

if __name__ == "__main__":
    main() 