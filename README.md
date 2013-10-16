# Collection of short python scripts for bioinformatics

## Data scrapping

## Tandem repeats search with TRF

Search tandem repeats in given folder with fasta files:

```bash
python parallel_trf.py input_folder output_folder mask threads
```

Example:

```bash
python parallel_trf.py ~/human_genome/fasta ~/human_genome/trf fa 20
```

## Illumina run statistics

Compute and draw distribution of PE fragment lengths:

```bash
python fragments_length_from_sam.py -o image_file -i sam_fiel
```

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

## Chromosome statistics

Get dictionary with chromosome lengths

```python
chr2length = get_chromosome_lengths(rerence_multifasta)
```
