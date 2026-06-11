# VARIANT ANNOTATION PIPELINE

A bioinformatics project.

---

# SETUP

1. Create virtual environment (`pip install -r requirements-dev.txt`)
2. Ensure `bcftools` is available (`brew install bcftools`) 
3. Activate environment (`. venv/bin/activate`)
4. `cd` into `data` and download ClinVar annotation variant files: `curl -O https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz` and `curl -O https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi`
5. From `data`, download reference "patient" HG002: `curl -O https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz` and `curl -O https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz.tbi`
6. You can use `bcftools` to peer at the data: 
    - `bcftools view -h clinvar.vcf.gz | tail -25` --> the header
    - `bcftools view clinvar.vcf.gz | head -40` --> the first true variant rows

---

# INFO

Example `./main.py` output:

```py
% ./main.py                                            

Script starting...

1 66926 AG ['A'] OR4F5:79501 Uncertain_significance
1 69134 A ['G'] OR4F5:79501 Likely_benign
1 69241 C ['T'] OR4F5:79501 Uncertain_significance
1 69308 A ['G'] OR4F5:79501 Uncertain_significance
1 69314 T ['G'] OR4F5:79501 Uncertain_significance
1 69404 T ['C'] OR4F5:79501 Uncertain_significance
```

This shows the 
- chromosome (CHROM, 1)
- position (POS, 66926)
- the reference allele (REF, AG)
- the variant allele (list of ALT, ['A'])
- the gene name (INFO.get("GENEINFO"), OR4F5:79501) where the part before ':' is the gene name and the part after the ':' is its NCBI gene ID
- ClinVar's clinical verdict (INFO.get("CLINSIG"), 'Uncertain_significance')

---

# REFERENCES

1. Brent S Pedersen, Aaron R Quinlan, cyvcf2: fast, flexible variant analysis with Python, Bioinformatics, Volume 33, Issue 12, June 2017, Pages 1867–1869, https://doi.org/10.1093/bioinformatics/btx057