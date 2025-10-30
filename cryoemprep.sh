#!/bin/bash
set -euo pipefail

# Prompt for Mediaflux token and project name
echo "Jerry's CryoSparc script activated."
echo "Enter your Mediaflux download token:"
read -r TOKEN
[[ -z "$TOKEN" ]] && { echo "Error: No token entered."; exit 1; }

echo "Enter a name for the project:"
read -r PROJECT
[[ -z "$PROJECT" ]] && { echo "Error: Project name cannot be empty."; exit 1; }

# Setup paths and download files

BASE_DIR="/vast/scratch/users/${USER}"
PROJECT_DIR="${BASE_DIR}/${PROJECT}"
mkdir -p "$PROJECT_DIR"

module purge
module load mediaflux-data-mover

echo "Downloading files to $PROJECT_DIR..."
mediaflux-data-mover-cli -v -download "$TOKEN" "$PROJECT_DIR"
echo "✅ File download complete."


#!/bin/bash
module load EMAN2

echo "Beginning file conversion..."

sleep_time=5   # seconds between job status checks
dep_ids=()      # array to store submitted job IDs

sanitize_filenames() {
  for ext in emi ser; do
    for f in *."$ext"; do
      [[ -f "$f" ]] || continue
      new_name="${f// /_}"
      if [[ "$f" != "$new_name" ]]; then
        mv "$f" "$new_name"
      fi
    done
  done
}

# Find unique folders 3+ levels deep containing .emi/.ser files
folders=$(find "$PROJECT_DIR" -mindepth 3 -type f \( -iname "*.emi" -o -iname "*.ser" \) \
  | sed -E 's|/[^/]+$||' | sort -u)

for folder in $folders; do
  echo "Submitting job for folder: $folder"

  # Submit job and capture job ID
  jobid=$(sbatch --parsable <<EOF
#!/bin/bash
#SBATCH --job-name=eman2
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null

module load EMAN2
cd "$folder" || exit 1

sanitize_filenames() {
  for ext in emi ser; do
    for f in *."$ext"; do
      [[ -f "\$f" ]] || continue
      new_name="\${f// /_}"
      if [[ "\$f" != "\$new_name" ]]; then
        mv "\$f" "\$new_name"
      fi
    done
  done
}

sanitize_filenames

for i in *.emi; do
  [[ -f "\$i" ]] || continue
  cat "\$i" | LANG=C sed 's|Real\ Space\(.*\)\</Object\>|\1|' | \
    LANG=C sed -n -e '/\<ObjectInfo\>/,\$p' | \
    LANG=C sed 's/^[^<]*</</' | head -n 3 > "\${i}.xml"

  MAG=\$(grep -a -E -o "Magnification>.{10,23}" "\${i}.xml" | sed -nr 's/.*>(.*)<\/M.*/\1/p')
  MAG2="\${MAG// /}"

  filename="\${i%.emi}"
  ser_file="\${filename}_1.ser"

  if [[ -f "\$ser_file" ]]; then
    echo "Converting \$ser_file → \${filename}_\${MAG2}.mrc → \${filename}_\${MAG2}.jpg"
    e2proc2d.py "\$ser_file" "\${filename}_\${MAG2}.mrc"
    e2proc2d.py "\${filename}_\${MAG2}.mrc" "\${filename}_\${MAG2}.jpg"
    rm "\$i" "\$ser_file"
  else
    echo "SER file missing: \$ser_file"
  fi
done
EOF
)

  echo "Submitted job $jobid for $folder"
  dep_ids+=("$jobid")
done

# Wait for all jobs to finish
echo "Waiting for all jobs to complete..."
while true; do
  unfinished=0

  for job in "${dep_ids[@]}"; do
    if squeue -j "$job" -h | grep -q .; then
      unfinished=$((unfinished + 1))
    fi
  done

  if [ "$unfinished" -eq 0 ]; then
    echo "All jobs finished successfully."
    break
  else
    echo "$unfinished jobs still running. Sleeping $sleep_time seconds..."
    sleep "$sleep_time"
  fi
done

echo "Conversion completed."
