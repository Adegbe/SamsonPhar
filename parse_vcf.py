import vcfpy

def parse_vcf(uploaded_file):
    """ 
    Fast VCF parsing: Skips malformed lines efficiently and extracts valid rsIDs.
    Fixes bytes decoding issue and ensures proper file handling in Streamlit.
    """
    variants = []
    skipped_count = 0  # Track skipped entries

    try:
        # Decode file content from bytes to string
        file_content = uploaded_file.read().decode("utf-8").splitlines()

        for line_number, line in enumerate(file_content, start=1):
            line = line.strip()

            # Ensure it's a valid VCF data line (skip headers)
            if line.startswith("#") or not line:
                continue

            fields = line.split("\t")

            # Skip malformed lines with fewer than 8 columns
            if len(fields) < 8:
                skipped_count += 1
                continue

            # Extract variant data
            try:
                variant_id = fields[2] if fields[2].startswith("rs") else "Unknown"

                variants.append({
                    "chromosome": fields[0],
                    "position": int(fields[1]),
                    "id": variant_id,
                    "reference": fields[3],
                    "alternate": fields[4] if len(fields) > 4 else ".",
                })
            except (IndexError, ValueError):
                skipped_count += 1
                continue  # Skip bad entries

        if skipped_count > 0:
            st.warning(f"⚠ Skipped {skipped_count} malformed lines.")

        return pd.DataFrame(variants)  # Convert list to DataFrame

    except Exception as e:
        st.error(f"❌ Error parsing VCF file: {e}")
        return pd.DataFrame()
