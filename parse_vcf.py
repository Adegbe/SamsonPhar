import pandas as pd
import streamlit as st

def parse_vcf(uploaded_file):
    """
    Robust VCF parsing that extracts valid variants and handles malformed lines.
    Properly handles byte/string decoding and provides clear error messages.
    """
    variants = []
    skipped_count = 0

    try:
        # Reset file cursor and read content
        uploaded_file.seek(0)
        file_content = uploaded_file.read().decode("utf-8").splitlines()

        for line_number, line in enumerate(file_content, 1):
            line = line.strip()
            
            # Skip headers and empty lines
            if line.startswith("#") or not line:
                continue

            # Split line into columns
            fields = line.split("\t")
            
            # Validate minimum required columns
            if len(fields) < 8:
                skipped_count += 1
                continue

            # Extract variant information
            try:
                chrom = fields[0]
                pos = int(fields[1])  # Validate integer position
                variant_id = fields[2] if fields[2].startswith("rs") else "Unknown"
                ref = fields[3]
                alt = fields[4] if len(fields) > 4 else "."

                variants.append({
                    "chromosome": chrom,
                    "position": pos,
                    "id": variant_id,
                    "reference": ref,
                    "alternate": alt
                })
            except (IndexError, ValueError) as e:
                skipped_count += 1
                st.debug(f"Skipping line {line_number}: {str(e)}")

        if skipped_count:
            st.warning(f"Skipped {skipped_count} malformed/invalid lines.")
            
        return pd.DataFrame(variants) if variants else pd.DataFrame()

    except UnicodeDecodeError:
        st.error("Invalid file encoding. Please ensure the file is UTF-8 encoded.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Critical parsing error: {str(e)}")
        return pd.DataFrame()
