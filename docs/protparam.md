# Getting ProtParam results quickly

Calculate protein properties for a large number of proteins really quickly.

## What you need

Either a fasta file containing all your protein sequences, or a .csv file containing all your sequences under a column named sequences, sequences_alignment_aa, or even VHH.
This means that for our NGS data, you can just download the data as a csv, and feed it directly into this script (maybe remove the spaces in its name though)


## What it does

For each sequence, it calculates:
- **Length** (number of residues)  
- **Molecular Weight (MW)** in Daltons  
- **Isoelectric Point (pI)** 
- **Extinction Coefficient**, based on W/Y/C content  
- **Instability Index**
- **Aliphatic Index**
- **Predicted Half-Life**

and places them nicely in a .csv for you.


## Usage
```
python csvprot.py /path/to/csv
OR
python fastaprot.py /path/to/fasta
```

For these Python scripts the output file will be written to whatever directory you’re currently in when you run the command — i.e., your present working directory (```pwd```).