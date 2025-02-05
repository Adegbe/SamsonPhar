import vcfpy

def parse_vcf(file):
    """ Parse VCF file and extract valid rsIDs. """
    variants = []
    skipped_count = 0

    try:
        # Decode file from bytes to string
        file_content = file.getvalue().decode("utf-8").splitlines()

        for line_number, line in enumerate(file_content, start=1):
            line = line.strip()
            if line.startswith("#"):  # Skip headers
                continue 

            fields = line.split("\t")

            # Skip malformed lines with fewer than 8 fields
            if len(fields) < 8:
                skipped_count += 1
                continue
            
            try:
                variant_id = fields[2] if fields[2].startswith("rs") else "Unknown"

                variants.append({
                    "chromosome": fields[0],
                    "position": int(fields[1]),
                    "variant": variant_id,  # Standardized to match clinicalVariants.tsv
                    "reference": fields[3],
                    "alternate": fields[4] if len(fields) > 4 else ".",
                })
            except (IndexError, ValueError):
                skipped_count += 1
                continue

        if skipped_count > 0:
            st.warning(f"⚠ Skipped {skipped_count} malformed lines.")

        return pd.DataFrame(variants)  # Convert list to DataFrame

    except Exception as e:
        st.error(f"❌ Error parsing VCF file: {e}")
        return pd.DataFrame()
