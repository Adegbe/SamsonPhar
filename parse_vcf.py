import vcf

def parse_vcf(file_path):
    vcf_reader = vcf.Reader(file_path)
    variants = []
    for record in vcf_reader:
        variants.append({
            "chromosome": record.CHROM,
            "position": record.POS,
            "id": record.ID,
            "reference": record.REF,
            "alternate": str(record.ALT[0])
        })
    return variants
