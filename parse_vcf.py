import pandas as pd
import streamlit as st

def parse_vcf(uploaded_file):
    """
    Ultimate VCF parser with comprehensive error handling
    Handles encoding issues, malformed lines, and data validation
    """
    variants = []
    skipped_lines = []
    encoding_issues = False

    try:
        # Reset and read file content
        uploaded_file.seek(0)
        raw_bytes = uploaded_file.read()

        # Detect encoding if UTF-8 fails
        try:
            content = raw_bytes.decode('utf-8-sig')  # Handle BOM
        except UnicodeDecodeError:
            st.warning("Attempting Latin-1 decoding...")
            try:
                content = raw_bytes.decode('latin-1')
                encoding_issues = True
            except Exception:
                st.error("Unsupported file encoding")
                return pd.DataFrame()

        # Process content
        for line_num, line in enumerate(content.splitlines(), 1):
            try:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                fields = line.split('\t')
                if len(fields) < 8:
                    skipped_lines.append((line_num, "Insufficient columns"))
                    continue

                # Validate critical fields
                chrom = fields[0]
                pos = int(fields[1])  # Will error on non-integer
                vid = fields[2] if fields[2].startswith('rs') else f"var_{line_num}"
                ref = fields[3]
                alt = fields[4] if len(fields[4]) > 0 else 'N'

                variants.append({
                    'chromosome': chrom,
                    'position': pos,
                    'id': vid,
                    'reference': ref,
                    'alternate': alt
                })

            except Exception as e:
                skipped_lines.append((line_num, str(e)))
                continue

        # Show quality report
        if encoding_issues:
            st.warning("File used fallback Latin-1 encoding. Some characters may be misrepresented.")
            
        if skipped_lines:
            st.warning(f"Skipped {len(skipped_lines)} problematic lines")
            if st.checkbox("Show skipped lines details"):
                st.table(pd.DataFrame(skipped_lines, columns=["Line", "Error"]))

        return pd.DataFrame(variants) if variants else pd.DataFrame()

    except Exception as e:
        st.error(f"Critical failure: {str(e)}")
        return pd.DataFrame()
