import pandas as pd

# Load PharmGKB data
clinical_variants = pd.read_csv("data/clinicalVariants.tsv", sep="\t")

def find_drug_recommendations(rsid):
    """Query clinical variants data"""
    variant_data = clinical_variants[clinical_variants["Variant"] == rsid]
    if not variant_data.empty:
        return variant_data[["Drug(s)", "Evidence Level"]].to_dict(orient="records")
    return "No recommendations found for this variant."
