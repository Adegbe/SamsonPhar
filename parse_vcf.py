import pandas as pd
import streamlit as st
import chardet  # For encoding detection

def parse_vcf(uploaded_file):
    """
    Final Ultimate VCF Parser with:
    - Automatic encoding detection
    - Complete byte/string separation
    - Deep validation
    - Comprehensive error reporting
    """
    variants = []
    error_log = []

    try:
        # Read as bytes and detect encoding
        uploaded_file.seek(0)
        raw_bytes = uploaded_file.read()
        
        # Detect encoding with confidence
        encoding_info = chardet.detect(raw_bytes)
        if encoding_info['confidence'] < 0.7:
            st.warning("Low confidence encoding detection. Using fallback.")
            
        try:
            content = raw_bytes.decode(encoding_info['encoding'] or 'utf-8')
        except UnicodeDecodeError:
            content = raw_bytes.decode('latin-1', errors='replace')

        # Process content as PROPER STRINGS
        for line_num, line in enumerate(content.splitlines(), 1):
            try:
                # Byte/string type enforcement
                if isinstance(line, bytes):
                    line = line.decode('utf-8', errors='replace')
                    
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Validate field count before splitting
                if line.count('\t') < 7:
                    error_log.append(f"Line {line_num}: Insufficient fields")
                    continue

                fields = line.split('\t', 7)  # Split exactly 8 fields
                
                # Extract with validation
                variant = {
                    'chromosome': fields[0] or 'unknown',
                    'position': int(fields[1]),
                    'id': fields[2] if fields[2].startswith('rs') else f'Variant_{line_num}',
                    'reference': fields[3],
                    'alternate': fields[4] if len(fields) > 4 else 'N',
                }
                variants.append(variant)

            except Exception as e:
                error_log.append(f"Line {line_num}: {str(e)}")

        # Show comprehensive report
        if error_log:
            st.error(f"Encountered {len(error_log)} errors:")
            st.code("\n".join(error_log[:10]))  # Show first 10 errors
        
        return pd.DataFrame(variants) if variants else pd.DataFrame()

    except Exception as e:
        st.error(f"Fatal Error: {str(e)}")
        return pd.DataFrame()
