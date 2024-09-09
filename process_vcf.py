import gzip
import csv
import argparse
import os

def process_vcf(vcf_file, output_file):
    # Predefined keys to extract from INFO field
    info_keys = ['AC_joint', 'AN_joint', 'AF_joint', 'grpmax_joint', 'AC_exomes', 'AN_exomes', 'AF_exomes', 'grpmax_exomes',
                 'AC_genomes', 'AN_genomes', 'AF_genomes', 'grpmax_genomes', 'AC_joint_XX', 'AF_joint_XX', 'AN_joint_XX', 'nhomalt_joint_XX',
                 'AC_joint_XY', 'AF_joint_XY', 'AN_joint_XY', 'nhomalt_joint_XY', 'nhomalt_joint', 'AC_exomes_XX', 'AF_exomes_XX', 'AN_exomes_XX',
                 'nhomalt_exomes_XX', 'AC_exomes_XY', 'AF_exomes_XY', 'AN_exomes_XY', 'nhomalt_exomes_XY', 'nhomalt_exomes', 'AC_genomes_XX',
                 'AF_genomes_XX', 'AN_genomes_XX', 'nhomalt_genomes_XX', 'AC_genomes_XY', 'AF_genomes_XY', 'AN_genomes_XY', 'nhomalt_genomes_XY',
                 'nhomalt_genomes', 'age_hist_het_bin_freq_joint', 'age_hist_hom_bin_freq_joint']

    # The fixed columns we are keeping from the VCF format
    fixed_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER']

    # Prepare final headers
    headers = fixed_columns + info_keys

    with gzip.open(vcf_file, 'rt') if vcf_file.endswith('.gz') else open(vcf_file, 'r') as vcf, \
         gzip.open(output_file, 'wt') as tsv_gz:

        # Initialize CSV writer
        writer = csv.DictWriter(tsv_gz, fieldnames=headers, delimiter='\t')
        writer.writeheader()

        # Process the VCF file line by line
        for line in vcf:
            if line.startswith('#'):
                continue  # Skip header lines

            columns = line.strip().split('\t')
            chrom, pos, var_id, ref, alt, qual, flt, info = columns[:8]

            # Split the INFO field by ";", then by "=" to get key-value pairs
            info_dict = dict(kv.split('=') if '=' in kv else (kv, '') for kv in info.split(';'))

            # Prepare row data with fixed columns
            row = {
                '#CHROM': chrom,
                'POS': pos,
                'ID': var_id,
                'REF': ref,
                'ALT': alt,
                'QUAL': qual,
                'FILTER': flt
            }

            # Add only the predefined info keys and fill missing values with "."
            for key in info_keys:
                row[key] = info_dict.get(key, '.')

            # Write the row to the output file
            writer.writerow(row)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process VCF and extract specific INFO fields.")
    parser.add_argument('vcf_file', type=str, help="Input VCF file (can be .vcf or .vcf.gz)")
    args = parser.parse_args()

    # Generate the output file name by appending '_filtered.tsv.gz' to the input file base name
    input_file = args.vcf_file
    base_name = os.path.basename(input_file).rsplit('.', 1)[0]
    output_file = f"{base_name}_filtered.tsv.gz"

    # Process the VCF file
    process_vcf(input_file, output_file)
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
