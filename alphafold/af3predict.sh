#!/bin/bash
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:A100:1
#SBATCH --mem=64G
#SBATCH --time=16:00:00
#SBATCH --job-name=AF3Predictions
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null

# === Input arguments ===
NAME="$1"        # e.g. 7abc
OUTPUT_DIR="$2"  # e.g. results_7abc
FASTA_FILE="${NAME}.fasta"
JSON_FILE="${NAME}.json"

if [[ -z "$NAME" || -z "$OUTPUT_DIR" ]]; then
    echo "❌ Error: Missing input arguments."
    echo "Usage: sbatch af3_job.sh <name> <output_dir>"
    echo "Example: sbatch af3_job.sh 7abc AF3Outputs_7abc"
    exit 1
fi

# === Check FASTA file exists ===
if [[ ! -f "$FASTA_FILE" ]]; then
    echo "❌ Error: FASTA file '$FASTA_FILE' not found."
    exit 1
fi

# === Convert FASTA → JSON if needed ===
if [[ -f "$JSON_FILE" ]]; then
    echo "⚠️ JSON file '$JSON_FILE' already exists, skipping conversion."
else
    echo "🔄 Converting $FASTA_FILE → $JSON_FILE ..."
    python fasta2json.py "$FASTA_FILE"
fi

# === Prepare output directory ===
mkdir -p "$OUTPUT_DIR"

# === Load modules ===
module purge
module load apptainer/1.4.1
module load alphafold/3.0.0
cat << 'EOF'
  _______ _    _          __  __    _               ____  
 |__   __| |  | |   /\   |  \/  |  | |        /\    |  _ \ 
    | |  | |__| |  /  \  | \  / |  | |       /  \   | |_) |
    | |  |  __  | / /\ \ | |\/| |  | |      / /\ \  |  _ < 
    | |  | |  | |/ ____ \| |  | |  | |____ / ____ \ | |_) |
    |_|  |_|  |_/_/    \_\_|  |_|  |______/_/    \_\ ____/ 
                                                          
EOF

# === Run AlphaFold3 ===
echo "Running AlphaFold3 on $JSON_FILE ..."
alphafold3 -o "$OUTPUT_DIR" -i "$JSON_FILE"
