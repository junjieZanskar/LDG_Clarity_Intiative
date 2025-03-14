#!/usr/bin/env python3

import pandas as pd
import os
import numpy as np

def clean_numeric_data(value):
    """
    Clean numeric data by converting to float.
    
    Args:
        value: Value to convert
    Returns:
        float: Cleaned numeric value
    """
    try:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Remove any non-numeric characters except decimal point and minus
            value = ''.join(c for c in value if c.isdigit() or c in '.-')
            return float(value) if value else np.nan
        return np.nan
    except:
        return np.nan

def process_temperature_profile(input_file: str, output_file: str):
    """
    Process temperature profile data and create an Excel file with separate sheets for each well.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to save the output Excel file
    """
    print(f"Reading data from: {input_file}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # If the file doesn't have headers, set them
        if 'Temp_degC' in df.iloc[0].values:
            df.columns = ['X', 'Y', 'Z', 'Temp_degC', 'Well']
            df = df.iloc[1:]  # Remove the first row which contains header names
        
        print("Cleaning numeric data...")
        # Clean numeric columns
        df['X'] = df['X'].apply(clean_numeric_data)
        df['Y'] = df['Y'].apply(clean_numeric_data)
        df['Z'] = df['Z'].apply(clean_numeric_data)
        df['Temp_degC'] = df['Temp_degC'].apply(clean_numeric_data)
        
        # Remove rows with invalid data
        df = df.dropna(subset=['X', 'Y', 'Z', 'Temp_degC'])
        
        # Convert Well to string to handle any numeric well numbers
        df['Well'] = df['Well'].astype(str)
        
        # Get unique wells
        wells = sorted(df['Well'].unique())
        print(f"\nFound {len(wells)} unique wells in the data")
        
        if len(wells) == 0:
            raise ValueError("No valid wells found in the data")
        
        # Create Excel writer
        print(f"\nCreating Excel file: {output_file}")
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Create a summary sheet
            summary_data = []
            for well in wells:
                well_data = df[df['Well'] == well]
                max_depth = well_data['Z'].max()
                min_depth = well_data['Z'].min()
                summary_data.append({
                    'Well': well,
                    'Number_of_Points': len(well_data),
                    'Min_Depth': min_depth,
                    'Max_Depth': max_depth,
                    'Depth_Range': f"{max_depth:.2f} - {min_depth:.2f}",
                    'Min_Temperature': well_data['Temp_degC'].min(),
                    'Max_Temperature': well_data['Temp_degC'].max(),
                    'Avg_Temperature': well_data['Temp_degC'].mean()
                })
            
            # Create summary sheet
            df_summary = pd.DataFrame(summary_data)
            # Sort summary by Well number
            df_summary = df_summary.sort_values('Well')
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            print("Created Summary sheet")
            
            # Format summary sheet
            worksheet = writer.sheets['Summary']
            for idx, col in enumerate(df_summary.columns):
                col_letter = chr(65 + idx)
                max_length = max(
                    df_summary[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[col_letter].width = max_length + 2
                
                # Format numeric columns
                if col in ['Min_Depth', 'Max_Depth', 'Min_Temperature', 'Max_Temperature', 'Avg_Temperature']:
                    for cell in worksheet[col_letter][1:]:  # Skip header
                        cell.number_format = '0.00'
            
            # Create a sheet for each well
            for well in wells:
                try:
                    # Filter data for this well
                    df_well = df[df['Well'] == well].copy()
                    
                    # Sort by Z coordinate (depth) in descending order
                    df_well = df_well.sort_values('Z', ascending=False)
                    
                    # Create sheet name (ensure it's valid for Excel)
                    sheet_name = f'Well_{str(well).replace("/", "_")}'[:31]  # Excel sheet names limited to 31 chars
                    
                    # Write to Excel
                    df_well.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"Created sheet for Well {well} with {len(df_well)} points")
                    
                    # Format the sheet
                    worksheet = writer.sheets[sheet_name]
                    for idx, col in enumerate(df_well.columns):
                        col_letter = chr(65 + idx)
                        max_length = max(
                            df_well[col].astype(str).apply(len).max(),
                            len(col)
                        )
                        worksheet.column_dimensions[col_letter].width = max_length + 2
                        
                        # Format numeric columns
                        if col in ['X', 'Y', 'Z', 'Temp_degC']:
                            for cell in worksheet[col_letter][1:]:  # Skip header
                                cell.number_format = '0.00'
                except Exception as e:
                    print(f"Warning: Error processing Well {well}: {str(e)}")
                    continue
            
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Set up input and output paths
    input_file = os.path.join(parent_dir, "RawData", "Temperature_Profile_Data.csv")
    output_file = os.path.join(parent_dir, "CleanData", "Temperature_Profile.xlsx")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Process the data
    process_temperature_profile(input_file, output_file)
    print(f"\nProcessing complete. Output saved to: {output_file}")

if __name__ == "__main__":
    main() 