import pandas as pd

def load_data():
    """
    Load clinical variant and annotation data from the data folder.
    """
    clinical_variants = pd.read_csv('data/clinicalVariants.tsv', sep='\t')
    clinical_annotations = pd.read_csv('data/clinical_annotations.tsv', sep='\t')

    # Standardize column names to avoid KeyErrors
    clinical_variants.columns = clinical_variants.columns.str.strip().str.lower()
    clinical_annotations.columns = clinical_annotations.columns.str.strip().str.lower()

    return clinical_variants, clinical_annotations

def query_variant_data(rsid, clinical_variants):
    """
    Query clinicalVariants.tsv for a specific rsID.
    """
    if 'variant' not in clinical_variants.columns:
        raise KeyError("The 'variant' column is missing from clinicalVariants.tsv. Check the file structure.")

    result = clinical_variants[clinical_variants['variant'].str.contains(rsid, na=False, case=False)]
    if not result.empty:
        return result.to_dict(orient='records')
    else:
        return f"No data found for rsID {rsid}"

def query_clinical_annotations(rsid, clinical_annotations):
    """
    Query clinicalAnnotations.tsv for a specific rsID.
    """
    if 'variant/haplotypes' not in clinical_annotations.columns:
        raise KeyError("The 'variant/haplotypes' column is missing from clinical_annotations.tsv. Check the file structure.")

    result = clinical_annotations[clinical_annotations['variant/haplotypes'].str.contains(rsid, na=False, case=False)]
    if not result.empty:
        return result.to_dict(orient='records')
    else:
        return f"No clinical annotations found for rsID {rsid}"
