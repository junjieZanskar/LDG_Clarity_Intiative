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

def analyze_excel_file(file_path: str):
    """
    Read and analyze the structure of the Excel file.
    Print out information about sheets, columns, and data types.
    
    Args:
        file_path: Path to the Excel file
    """
    print(f"\nAnalyzing Excel file: {file_path}")
    
    # Read all sheets
    excel_file = pd.ExcelFile(file_path)
    print(f"\nFound sheets: {excel_file.sheet_names}")
    
    # Analyze each sheet
    for sheet_name in excel_file.sheet_names:
        print(f"\nAnalyzing sheet: {sheet_name}")
        
        # Read the sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Print basic information
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print("\nColumns and their data types:")
        for col in df.columns:
            print(f"- {col}: {df[col].dtype}")
        
        # Print first few rows
        print("\nFirst few rows of data:")
        print(df.head())
        print("\n" + "="*80)

def process_excel_file(input_path: str, output_path: str):
    """
    Process the Excel file:
    1. Keep the Overview sheet unchanged
    2. Split the raw data into separate sheets by year using the Year column
    
    Args:
        input_path: Path to the input Excel file
        output_path: Path to save the processed Excel file
    """
    print(f"\nProcessing Excel file: {input_path}")
    
    # Read the Excel file
    excel_file = pd.ExcelFile(input_path)
    
    # Create Excel writer for output
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Copy Overview sheet unchanged
        if 'Overview' in excel_file.sheet_names:
            df_overview = pd.read_excel(input_path, sheet_name='Overview')
            df_overview.to_excel(writer, sheet_name='Overview', index=False)
            print("Copied Overview sheet")
        
        # Process raw data
        df_raw = pd.read_excel(input_path, sheet_name='Raw data')
        
        # Get unique years from Year column
        years = sorted(df_raw['Year'].unique())
        print(f"\nFound years in data: {years}")
        
        # Show count of entries per year
        year_counts = df_raw['Year'].value_counts().sort_index()
        print("\nNumber of entries per year:")
        print(year_counts)
        
        # Create a sheet for each year
        for year in years:
            # Filter data for this year
            df_year = df_raw[df_raw['Year'] == year].copy()
            
            # Create sheet
            sheet_name = f'Data_{year}'
            df_year.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"\nCreated sheet for year {year} with {len(df_year)} rows")
            
            # Format the sheet
            worksheet = writer.sheets[sheet_name]
            
            # Set column widths
            for idx, col in enumerate(df_year.columns):
                # Get the Excel column letter
                col_letter = chr(65 + idx)
                
                if col == 'Date':
                    worksheet.column_dimensions[col_letter].width = 12
                else:
                    # Calculate max width needed
                    max_length = max(
                        df_year[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[col_letter].width = max_length + 2
                
                # Format numeric columns
                if df_year[col].dtype in ['float64', 'int64']:
                    for cell in worksheet[col_letter][1:]:  # Skip header
                        cell.number_format = '0.00'
    
    print(f"\nCreated processed Excel file at: {output_path}")

def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Set up GCP credentials
    # set_gcp_credentials()
    
    # Configuration
    BUCKET_NAME = "comsol_ldg"  # Replace with your bucket name
    FILE_NAME = 'Eagle_Vision_Working_Data_Warehouse/Tracer_Data_Compiled.xlsx'
        
    RAW_DATA_FOLDER = os.path.join(parent_dir, "RawData")
    CLEAN_DATA_FOLDER = os.path.join(parent_dir, "CleanData")
    
    INPUT_PATH = os.path.join(RAW_DATA_FOLDER, "Tracer_Data_Compiled.xlsx")
    OUTPUT_PATH = os.path.join(CLEAN_DATA_FOLDER, "Tracer.xlsx")
    
    # Ensure directories exist
    ensure_directory(RAW_DATA_FOLDER)
    ensure_directory(CLEAN_DATA_FOLDER)
    
    # Download file from GCP
    downloaded_files = download_from_gcp(
        bucket_name=BUCKET_NAME,
        file_names=[FILE_NAME],
        destination_folder=RAW_DATA_FOLDER
    )
    
    # Process the Excel file
    process_excel_file(INPUT_PATH, OUTPUT_PATH)

if __name__ == "__main__":
    main() 