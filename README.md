# Collection of short python scripts for bioinformatics

## Data scrapping

## Kmers analysis

Compute kmer frequences percents for coverage plot.

```bash
python compute_kmer_coverage.py input_file output_file
```

## PacBio analysis

Convert bax.h5 files into fasta and fastq files.

```bash
ls | grep bax.h5 | xargs -n 1 --max-procs 64 python baxh5_to_fastq.py

cat *fasta > pacbio.fasta

cat *fastq > pacbio.fastq
```
