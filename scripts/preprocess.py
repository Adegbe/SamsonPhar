import pandas as pd
import os

def preprocess_genotype_file(uploaded_file):
    try:
        # Read the file while treating everything as string and ignoring comment lines
        data = pd.read_csv(
            uploaded_file,
            sep="\t",  # Use tab as the delimiter
            comment="#",  # Skip lines starting with '#'
            header=None,  # Treat the file as having no predefined header
            dtype=str,  # Treat all columns as strings
            low_memory=False  # Disable chunking for simplicity
        )

        # Print the first few rows for debugging
        print(f"First 5 rows of raw data:\n{data.head()}")

        # Manually set the header (based on the format from your screenshot)
        data.columns = ["rsid", "chromosome", "position", "genotype"]

        # Log the detected columns for debugging
        print(f"Detected columns: {list(data.columns)}")

        # Normalize column names (in case of user input variation)
        data.columns = [col.lower().strip() for col in data.columns]

        # Check for 'chromosome' column
        if 'chromosome' not in data.columns:
            raise ValueError("Input file is missing a 'chromosome' column.")

        # Ensure no missing or invalid data in critical columns
        if data['chromosome'].isnull().any() or data['chromosome'].str.strip().eq("").any():
            raise ValueError("The 'chromosome' column contains missing or invalid values.")

        # Save the processed file in-memory for Streamlit
        processed_file_path = os.path.join("processed_data.vcf")
        data.to_csv(processed_file_path, sep="\t", index=False)
        print(f"File successfully preprocessed: {processed_file_path}")

        return processed_file_path

    except Exception as e:
        raise ValueError(f"Error preprocessing the file: {e}")
