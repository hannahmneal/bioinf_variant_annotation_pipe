#!./bio_venv/bin/python3.14

from cyvcf2 import VCF
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


PATHOGENIC_CLINICAL_SIGNATURES = ["Pathogenic", "Likely_pathogenic"]

patient_id = "HG002"


def collect_pathogenic_signatures(clnsig):
    """
    """

    # First, ensure `CLNSIG` is defined and has a non-null value
    if not clnsig:
        return False
    # ClinVar may combine pathogenic CLNSIGs, e.g., "Pathogenic/Likely_pathogenic". Ensure this is accounted for:
    signatures = clnsig.replace("|", "/").split("/")

    return any(s in PATHOGENIC_CLINICAL_SIGNATURES for s in signatures)


def harmonized_chrom(chrom):
    """
    A utility function that harmonizes the designation of "chromosome" between ClinVar's designation (e.g., an integer such as 1) and other files whose designation begins with "chr" (e.g., chr1). 
    Returns: the integer form of the chromosome.
    """
    return chrom[3:] if chrom.startswith("chr") else chrom


def key(chrom, pos, ref, alt):
    """
    Returns a tuple that includes a harmonized form of "chromosome", the position of the gene on the chromosome, the reference allele, and the variant(s) allele(s).
    """
    return (harmonized_chrom(chrom), pos, ref, alt)


def build_pathogenic_lookup(path):
    """
    Returns a dictionary of pathogenic allele(s) from the list of alternate allele(s).

    Example: {"gene": 1, "clnsig": "Likely_pathogenic"}
    """
    print(f"\nBuilding a lookup of pathogenic alleles (please be patient!)...\n")


    lookup = {}
    for v in VCF(path):
        CLNSIG = v.INFO.get("CLNSIG")
        if not collect_pathogenic_signatures(clnsig=CLNSIG):
            continue
        for a in v.ALT:
            lookup[key(v.CHROM, v.POS, v.REF, a)] = {
                "gene": v.INFO.get("GENEINFO"),
                "clnsig": CLNSIG,
            }

    return lookup


def gather_pathogenic_variants(path, lookup):
    """
    Scans the variants of the given patient and keeps only those that ClinVar has identified as being pathogenic or likely pathogenic.
    """
    variants = []
    for v in VCF(path):
        for alt in v.ALT:
            match = lookup.get(key(v.CHROM, v.POS, v.REF, alt))

            if match:
                variants.append({
                    "chrom": harmonized_chrom(v.CHROM),
                    "position": v.POS,
                    "ref_allele": v.REF,
                    "alt_allele": alt,
                    "gene": match["gene"],
                    "clinical_significance": match["clnsig"],
                })

    return variants


def main():
    print("\nScript starting...\n")

    print(
        f"\nFinding pathogenic clinical signatures {PATHOGENIC_CLINICAL_SIGNATURES} for patient... \n"
    )

    lookup = build_pathogenic_lookup(f"data/{os.getenv("URL_CLINVAR")}")
    print(f"\n{len(lookup):,} pathogenic variants identified...\n")

    print("\nGathering pathogenic variants...\n")
    variants = gather_pathogenic_variants(f"data/{os.getenv("URL_REFERENCE_PATIENT")}", lookup)
    if not variants:
        print("\nNo pathogenic variants found for this patient.\n")
        return

    df = pd.DataFrame(variants).sort_values(["chrom", "position"]).reset_index(drop=True)
    df.to_csv("pathogenic_variant_report_for_HG002.csv", index=False)

    print(f"\nFound {len(df)} pathogenic variants for {patient_id}\n")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
