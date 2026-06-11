#!./bio_venv/bin/python3.14

from cyvcf2 import VCF

def main():
    print("\nScript starting...\n")

    # VCF on GRCh38 published by ClinVar
    URL_CLINVAR_VCF_ON_GRCH38 = (
        "ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz"
    )

    # High-confidence variant reference individual ("patient"):
    URL_REF_HG002 = (
        "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/"
    "AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/"
    "HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz"
    )

    # Gets the fields of interest for this project:
    for i, v in enumerate(VCF("data/clinvar.vcf.gz")):
        print(
            v.CHROM, v.POS, v.REF, list(v.ALT), v.INFO.get("GENEINFO"), v.INFO.get("CLNSIG")
        )
        if i >= 5:
            break


if __name__ == "__main__":
    main()
