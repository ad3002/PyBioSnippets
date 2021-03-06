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
python fragments_length_from_sam.py -o image_file -i sam_file
```

## Functions related to SAM file

Count unmapped reads:

```python
from PyBioSnippets.sam.sam_functions import count_unmapped

(mapped, unmapped) = count_unmapped(sam_file)
```

Save unmapped reads from SAM file to fasta file:

```python
from PyBioSnippets.sam.sam_functions import save_unmapped_to_fasta

save_unmapped_to_fasta(sam_file, fasta_file)
```

Compute fragment lengths statistics for first l lines.

```bash
python fragments_length_from_sam.py -o stat.png -i data.sam -l 100000
```

Count FLAG values for given SAM file:

```bash
python hiseq/sam_stats.py -i data.sam
```


## Fastq operations

Join splitted HiSeq files:

```bash
python hiseq/join_fastq.py --remove False --input some_folder --mask read_L001_R1
```

Fix too long quality scores in corrupted HiSeq files

```python
fix_uncorrect_long_quality(fastq_file, corrected_fastq_output)
```

Iterator for pair end files:

```python
for read_obj1, read_obj2 in iter_pe_data(fastq_file1, fastq_file2):
	do_somethind()
```

Convert fastq to fasta:

```python
python hiseq/fastq_to_fasta.py -i data.fastq -o data.fasta
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
