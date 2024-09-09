#!/bin/bash

#  input and output directories
input_dir="/media/GnomAD4.1/TEST"
output_dir="/media/GnomAD4.1/FILTERED_TSV"
# Python script path to extract necessary fields
python_script="/media/GnomAD4.1/process_vcf.py"


if [ ! -d "$input_dir" ]; then
  echo "Error: Input directory does not exist"
  exit 1
fi

# if output directory does not exist, create it
if [ ! -d "$output_dir" ]; then
  echo "Output directory does not exist. Creating it."
  mkdir -p "$output_dir"
fi

#change running directory
cd ${input_dir}

# Loop through each file with the pattern "*.bgz" in the input directory
for file in "$input_dir"/*.bgz; do
  if [ -f "$file" ]; then
    echo "Processing file: $file"
    
    base_name=$(basename "$file" .vcf.bgz)
    #unzip from .gz format
    #gzip -d $file
    #unzip from .bgz format
    bgzip -d -c ${base_name}.vcf.bgz > ${base_name}.vcf

    # Run the Python script and store the output in the output directory
    python3 "$python_script" "${base_name}.vcf"
    
    # Move the generated output to the output directory
    output_file="${base_name}_filtered.tsv.gz"
    mv "$output_file" "$output_dir"
    
    echo "Output stored in $output_dir/$output_file"
  else
    echo "No matching files found in $input_dir."
  fi
done
