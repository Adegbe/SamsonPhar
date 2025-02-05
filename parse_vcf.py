import vcfpy

def parse_vcf(file_path):
    """ Fast VCF parsing: Skips malformed lines efficiently and extracts valid rsIDs. """
    variants = []
    skipped_count = 0  # Track skipped entries

    try:
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if not line.startswith("#")]  # Remove headers

        for line_number, line in enumerate(lines, start=1):
            fields = line.split("\t")

            # Fast filter: Skip lines with fewer than 8 columns
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

        return variants

    except Exception as e:
        st.error(f"❌ Error parsing VCF file: {e}")
        return []

def display_variant_ids(variants):
    """ Display extracted rsIDs before querying ClinVar. """
    valid_rsids = [v["id"] for v in variants if v["id"].startswith("rs")]

    if not valid_rsids:
        st.error("❌ No valid rsIDs extracted from the VCF file. Please check the file format.")
        return False

    st.subheader("✅ Extracted rsIDs for Debugging")
    st.write(f"Total valid rsIDs: {len(valid_rsids)}")
    st.write("Sample rsIDs:", valid_rsids[:10])  # Show first 10
