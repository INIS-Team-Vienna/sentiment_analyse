"""
Step 2: Quarterly Data Segmentation Module
Functionality: Split timestamped data into separate quarterly files
Input: Excel files with timestamp columns
Output: Files named by year_quarter (e.g., 2024_Q1.xlsx)
"""
import os
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from config import Config


class QuarterlyDataProcessor:
    """Processor for organizing data by quarters"""
    
    def __init__(self, source_folder: str = None):
        """Initialize processor with data folder"""
        self.source_folder = source_folder or Config.BASE_DATA_PATH
        
    def get_quarter(self, month: int) -> str:
        """Get quarter based on month number"""
        if 1 <= month <= 3:
            return "Q1"
        elif 4 <= month <= 6:
            return "Q2"
        elif 7 <= month <= 9:
            return "Q3"
        else:
            return "Q4"
    
    def process_single_file(self, file_path: str) -> None:
        """Process a single file and split data by quarters"""
        print(f"=== Processing file: {file_path} ===")
        
        try:
            # Read data
            df = pd.read_excel(file_path)
            
            # Use UTC_Time column
            if "UTC_Time" not in df.columns:
                raise ValueError("No UTC_Time column found in file")
            
            timestamp_column = "UTC_Time"
            
            # Ensure timestamp is datetime type
            df[timestamp_column] = pd.to_datetime(df[timestamp_column], errors='coerce')
            # Remove timezone info
            df[timestamp_column] = df[timestamp_column].dt.tz_localize(None)
            
            # Extract year from filename or data
            filename = os.path.basename(file_path)
            try:
                year = filename.split("_")[-1].split(".")[0]
                if not year.isdigit():
                    # Try to extract year from data
                    valid_dates = df[timestamp_column].dropna()
                    if len(valid_dates) > 0:
                        year = str(valid_dates.dt.year.mode()[0])
                    else:
                        year = "unknown"
            except:
                year = "unknown"
            
            # Create quarterly data dictionary
            quarterly_data = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
            processed_count = 0
            skipped_count = 0
            
            # Process data row by row
            for _, row in df.iterrows():
                if pd.notna(row[timestamp_column]):
                    quarter = self.get_quarter(row[timestamp_column].month)
                    quarterly_data[quarter].append(row)
                    processed_count += 1
                else:
                    skipped_count += 1
            
            print(f"Processed {processed_count} records, skipped {skipped_count} invalid timestamp records")
            
            # Save quarterly files
            saved_files = []
            for quarter, rows in quarterly_data.items():
                if rows:  # Only create file if data exists
                    quarter_file_path = Config.get_quarterly_file_path(year, quarter)
                    
                    # Merge with existing file if exists
                    if os.path.exists(quarter_file_path):
                        existing_df = pd.read_excel(quarter_file_path)
                        new_df = pd.concat([existing_df, pd.DataFrame(rows)], ignore_index=True)
                        print(f"Merged with existing file: {quarter_file_path}")
                    else:
                        new_df = pd.DataFrame(rows)
                        print(f"Created new file: {quarter_file_path}")
                    
                    new_df.to_excel(quarter_file_path, index=False)
                    saved_files.append(f"{year}_{quarter}.xlsx ({len(rows)} records)")
            
            print(f"✅ Successfully generated quarterly files: {', '.join(saved_files)}\n")
            
        except Exception as e:
            print(f"❌ Failed to process file: {e}\n")
    
    def process_all_files(self) -> None:
        """Process all qualifying files in the folder"""
        print(f"=== Starting to process folder: {self.source_folder} ===")
        
        # Find all qualifying files
        if not os.path.exists(self.source_folder):
            print(f"❌ Source folder does not exist: {self.source_folder}")
            return
        
        # Look for sentiment result files
        files = []
        for year in Config.ANALYSIS_YEARS:
            filename = f"results_{year}_sentiment.xlsx"
            if os.path.exists(os.path.join(self.source_folder, filename)):
                files.append(filename)
        
        if not files:
            print(f"❌ No qualifying files found in {self.source_folder}")
            return
        
        print(f"Found {len(files)} files to process:")
        for file in files:
            print(f"  - {file}")
        print()
        
        # Process each file
        for file in files:
            file_path = os.path.join(self.source_folder, file)
            self.process_single_file(file_path)
        
        print("🎉 All files processed successfully!")


def main():
    """Main function for quarterly data processing"""
    processor = QuarterlyDataProcessor()
    processor.process_all_files()


if __name__ == "__main__":
    main()
