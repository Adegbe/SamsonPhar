import pandas as pd
import streamlit as st

# Load the local datasets
@st.cache_data
def load_data():
    clinical_variants = pd.read_csv('data/clinicalVariants.tsv', sep='\t')
    clinical_annotations = pd.read_csv('data/clinical_annotations.tsv', sep='\t')
    return clinical_variants, clinical_annotations

# Compare the VCF rsIDs with local data and generate a report
def compare_vcf_with_local(vcf_data, clinical_variants, clinical_annotations):
    # Extract matching rsIDs from clinicalVariants
    variant_matches = clinical_variants[clinical_variants['variant'].isin(vcf_data['rsID'])]

    # Extract matching rsIDs from clinical_annotations
    annotation_matches = clinical_annotations[clinical_annotations['Variant/Haplotypes'].isin(vcf_data['rsID'])]

    return variant_matches, annotation_matches

# Streamlit App
st.title("Pharmacogenomics Tool")

st.subheader("Upload a VCF File")
uploaded_file = st.file_uploader("Upload your VCF file here", type=["vcf", "txt"])

if uploaded_file:
    # Parse the VCF file
    try:
        vcf_data = pd.read_csv(
            uploaded_file,
            sep="\t",
            comment='#',
            names=['rsID', 'chromosome', 'position', 'genotype']
        )
        st.success("VCF file loaded successfully!")
    except Exception as e:
        st.error(f"Error loading VCF file: {e}")
        st.stop()

    # Load local data
    clinical_variants, clinical_annotations = load_data()

    # Compare the VCF file with local data
    variant_matches, annotation_matches = compare_vcf_with_local(vcf_data, clinical_variants, clinical_annotations)

    # Display results
    st.subheader("Matching Variant Data")
    if not variant_matches.empty:
        st.write(variant_matches)
        st.download_button(
            label="Download Variant Matches as CSV",
            data=variant_matches.to_csv(index=False),
            file_name="variant_matches.csv",
            mime="text/csv",
        )
    else:
        st.warning("No matching variants found in clinicalVariants.")

    st.subheader("Matching Clinical Annotations")
    if not annotation_matches.empty:
        st.write(annotation_matches)
        st.download_button(
            label="Download Annotation Matches as CSV",
            data=annotation_matches.to_csv(index=False),
            file_name="annotation_matches.csv",
            mime="text/csv",
        )
    else:
        st.warning("No matching annotations found in clinical_annotations.")
