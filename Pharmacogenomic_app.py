import pandas as pd
import streamlit as st

# ------------------- STEP 1: LOAD LOCAL DATA ------------------- #
@st.cache_data
def load_data():
    """ Load clinical variants and clinical annotations from local datasets. """
    clinical_variants = pd.read_csv('data/clinicalVariants.tsv', sep='\t')
    clinical_annotations = pd.read_csv('data/clinical_annotations.tsv', sep='\t')
    return clinical_variants, clinical_annotations

# ------------------- STEP 2: PARSE VCF FILE ------------------- #
def parse_vcf(file):
    """ Parse VCF file and extract valid rsIDs. """
    variants = []
    skipped_count = 0

    try:
        for line_number, line in enumerate(file, start=1):
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
                    "rsID": variant_id,  # Ensure consistency with local data column names
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

# ------------------- STEP 3: COMPARE VCF WITH LOCAL DATA ------------------- #
def compare_vcf_with_local(vcf_data, clinical_variants, clinical_annotations):
    """ Compare extracted VCF rsIDs with clinical data. """
    variant_matches = clinical_variants[clinical_variants['variant'].isin(vcf_data['rsID'])]
    annotation_matches = clinical_annotations[clinical_annotations['Variant/Haplotypes'].isin(vcf_data['rsID'])]
    return variant_matches, annotation_matches

# ------------------- STEP 4: STREAMLIT UI ------------------- #
st.title("🔬 Pharmacogenomics Tool")

st.subheader("Upload a VCF File")
uploaded_file = st.file_uploader("Upload your VCF file here", type=["vcf"])

if uploaded_file:
    with st.spinner("Processing VCF file..."):
        # Parse the uploaded VCF file using the improved function
        vcf_data = parse_vcf(uploaded_file)

        if vcf_data.empty:
            st.error("No valid variants extracted from the VCF file.")
            st.stop()

    st.success("✅ VCF file loaded successfully!")

    # Load local data
    clinical_variants, clinical_annotations = load_data()

    # Compare the VCF file with local data
    variant_matches, annotation_matches = compare_vcf_with_local(vcf_data, clinical_variants, clinical_annotations)

    # ------------------- STEP 5: DISPLAY RESULTS ------------------- #
    st.subheader("🧬 Matching Variant Data")
    if not variant_matches.empty:
        st.write(variant_matches)
        st.download_button(
            label="📥 Download Variant Matches as CSV",
            data=variant_matches.to_csv(index=False),
            file_name="variant_matches.csv",
            mime="text/csv",
        )
    else:
        st.warning("⚠ No matching variants found in clinicalVariants.")

    st.subheader("📑 Matching Clinical Annotations")
    if not annotation_matches.empty:
        st.write(annotation_matches)
        st.download_button(
            label="📥 Download Annotation Matches as CSV",
            data=annotation_matches.to_csv(index=False),
            file_name="annotation_matches.csv",
            mime="text/csv",
        )
    else:
        st.warning("⚠ No matching annotations found in clinical_annotations.")
