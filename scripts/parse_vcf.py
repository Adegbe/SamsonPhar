import vcfpy
from io import BytesIO
from scripts.preprocess import preprocess_genotype_file

def parse_vcf(uploaded_file):
    """
    Parse a preprocessed VCF file and return a list of variants.
    """
    try:
        # Preprocess the file into a valid VCF format
        preprocessed_file = preprocess_genotype_file(uploaded_file)

        # Convert the preprocessed file to a binary stream
        binary_stream = BytesIO(preprocessed_file.getvalue().encode('utf-8'))

        # Use vcfpy to parse the VCF file
        reader = vcfpy.Reader.from_stream(binary_stream)
        variants = []

        # Extract variants
        for record in reader:
            variant = {
                "id": record.ID,
                "chrom": record.CHROM,
                "pos": record.POS,
                "ref": record.REF,
                "alt": [str(a) for a in record.ALT],
            }
            variants.append(variant)

        return variants

    except Exception as e:
        print(f"Error parsing VCF file: {e}")
        return []
