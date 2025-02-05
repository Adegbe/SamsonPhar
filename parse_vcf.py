import streamlit as st
import pandas as pd

def parse_vcf(uploaded_file):
    """Streamlit-compatible VCF parser preserving your original logic"""
    variants = []
    skipped_count = 0

    try:
        # Read and decode bytes upfront
        content = uploaded_file.read().decode('utf-8')
        lines = [line.strip() for line in content.split('\n') if not line.startswith("#")]

        for line_number, line in enumerate(lines, start=1):
            fields = line.split("\t")
            
            if len(fields) < 8:
                skipped_count += 1
                continue

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

        if skipped_count > 0:
            st.warning(f"⚠ Skipped {skipped_count} malformed lines.")

        return pd.DataFrame(variants) if variants else pd.DataFrame()

    except UnicodeDecodeError:
        st.error("Invalid file encoding. Try UTF-8 or Latin-1 files.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Critical error: {str(e)}")
        return pd.DataFrame()
