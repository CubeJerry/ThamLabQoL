# Running AlphaFold3 Predictions on Milton

This script submits an AlphaFold3 prediction job to the GPU queue on Milton.  
It has been set up to generate a larger number of predictions than our default settings, hopefully enhancing quality.

## What you need

A fasta file with your protein sequences, and the scripts here.


## What it does

1. Takes a `.fasta` sequence file and automatically converts it into a `.json` file (required by AlphaFold3).
2. Creates an output directory for results.
3. Loads the appropriate AlphaFold3 environment on Milton.
4. Runs the prediction and saves all model outputs inside your specified folder.



## Usage

NOTE FOR BEGINNERS: You may need to run ``` cd ./ThamLabQoL/alphafold ``` to correctly find the script.

From your Milton terminal (either via **Open OnDemand → Open in Terminal** or via SSH) run:

```
sbatch af3predict.sh <fasta_name> <output_dir>

```
**IMPORTANT: FASTA_NAME HERE IS JUST THE NAME OF YOUR FASTA WITHOUT THE .FASTA PART**

So if you had a fasta file ```9dx6.fasta``` of Mel's structure for Fab826827 (PDB: 9DX6) in your personal drive, and wanted to store its output in a new folder called ```outputs```, you'd run

```
sbatch af3predict.sh /home/users/allstaff/[USERNAME]/9dx6 /home/users/allstaff/[USERNAME]/outputs

```
Of course, those of you more familiar with file paths will know that this can be made way shorter.


