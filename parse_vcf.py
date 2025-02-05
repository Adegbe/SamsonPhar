import pandas as pd
import streamlit as st

def parse_vcf(uploaded_file):
    """
    Handles VCF parsing with proper byte/string conversion and error handling
    """
    variants = []
    skipped_count = 0

    try:
        # Read as bytes first then decode
        uploaded_file.seek(0)
        byte_content = uploaded_file.read()
        
        # Validate UTF-8 decoding
        try:
            decoded_content = byte_content.decode('utf-8')
        except UnicodeDecodeError:
            st.error("File encoding error: Not valid UTF-8")
            return pd.DataFrame()

        # Process decoded string lines
        for line_number, line in enumerate(decoded_content.splitlines(), 1):
            line = line.strip()
            
            # Skip headers/comments using string check
            if line.startswith('#'):
                continue

            # Split columns and validate
            parts = line.split('\t')
            if len(parts) < 8:
                skipped_count += 1
                continue

            # Extract fields with validation
            try:
                variant_info = {
                    "chromosome": parts[0],
                    "position": int(parts[1]),
                    "id": parts[2] if parts[2].startswith("rs") else "Unknown",
                    "reference": parts[3],
                    "alternate": parts[4] if len(parts) > 4 else ".",
                }
                variants.append(variant_info)
            except (IndexError, ValueError) as e:
                skipped_count += 1
                st.debug(f"Line {line_number} error: {str(e)}")

        # Show quality warnings
        if skipped_count > 0:
            st.warning(f"Skipped {skipped_count} malformed/incomplete records")
            
        return pd.DataFrame(variants) if variants else pd.DataFrame()

    except Exception as e:
        st.error(f"Critical parsing failure: {str(e)}")
        return pd.DataFrame()
