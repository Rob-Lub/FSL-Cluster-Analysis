# Script by Robert Lubomierski. Function: Split a thresholded map into seperat clusters (>99 voxels/threshold) and analyse the clusters using an atlas.
# The script is based on fslmaths and atlasq. Make sure FSL is installed.
# Input 1: Text file containing list of clusters. Normally automatically created by FEAT. e.g. "cluster_zstat1_std.txt"
# Input 2: NIFTI image file of the cluster masks. Normally automatically created by FEAT. e.g. "cluster_mask_zstat1.nii.gz"
# Input 3: Atlas for analysis. Numerous atlases come per default with FSL. Input needs to look like this [--atlases "Example_Atlas"](without bracles). 
# Multiple atlases are possible. Just add them after another [--atlases "Example_Atlas_1" "Example_Atlas_2" "Example_Atlas_3"].
# Input 4: Optional! Change the threshold for inclusion of cluster size. Default threshold = 99. Only clusters larger than threshold will be analysed. 

# If you use this script in your research, please cite the following DOI.
# DOI: 10.5281/zenodo.10377036


import sys
import subprocess
import argparse
import os

# Specify the directory to save output files
output_files = []
output_directory = "Split Cluster Masks"

def read_txt_file(file_path, threshold):
    first_column_data = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Skip the first row
            if line_num == 1:
                continue
            
            # Split each line by tabs
            columns = line.strip().split('\t')
            
            # Assuming there are at least two columns
            if len(columns) >= 2:
                # Convert the first two columns to integers
                first_column = int(columns[0])
                second_column = int(columns[1])
                
                # Check if the number in the second column is larger than the specified threshold
                if second_column > threshold:
                    # Append the first column to first_column_data only if the condition is met
                    first_column_data.append(first_column)
    
    return first_column_data

def run_fslmaths(input_file, number):
    global output_directory  # Use the global variable

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    output_file = os.path.join(output_directory, f"output_cluster_{number}.nii.gz")

    command = [
        "fslmaths",
        input_file,
        "-thr", str(number),
        "-uthr", str(number),
        "-bin",
        output_file,
    ]
#    For debugging
#    print(f"Running command: {' '.join(command)}")

    output_files.append(output_file)

    subprocess.run(command)

def run_atlasq(input_file, atlases):
    # Splitting the input_file into directory, file name, and extention. This allows the text files to be saved elsewhere.
    input_directory, input_fullname = os.path.split(input_file)
    input_fullname2, input_extension = os.path.splitext(input_fullname)
    input_name, input_extension = os.path.splitext(input_fullname2)

    for atlas in atlases:
        command = [
            "atlasq", "ohi",
            "-a", atlas,
            "-m", input_file,
        ]

        print(f' ')
#        For debugging
#        print(f"Running command: {' '.join(command)}")
        print(f' ')
        print(f'The cluster {input_name} was analysed with infos from "{atlas}"')

        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if there was an error (non-zero exit code)
        if result.returncode != 0:
            # Print the error and raise an exception to stop the script
            print(f"")
            print(f"Error for {atlas}: {result.stdout}")
            continue

        # Check if the output contains the phrase "Invalid atlas name. Try one of:"
        if result.stdout.find("Invalid atlas name.") >= 0:
            # Print the output and skip to the next atlas
            print(f"")
            print(result.stdout)
            continue


        # Save the output to a text file
        output_txt_file = f"{input_name}_{atlas}.txt"
        with open(output_txt_file, 'w') as txt_file:
            txt_file.write(f"Cluster: {input_name}\n")
            txt_file.write(f"Atlas: {atlas}\n\n")
            txt_file.write(result.stdout)

        print(f"Results saved to: {output_txt_file}")

def main(file_path, input_file, threshold, atlases):

    print(f"Only clusters larger than threshold = {threshold} are analysed.")

    # Call the read_txt_file function with the provided file path
    first_column_data = read_txt_file(file_path, threshold)

    # Loop through numbers in first_column_data and run fslmaths for each
    for number in first_column_data:
        run_fslmaths(input_file, number)

    # Loop through output_files and run atlasq for each output file
    for output_file in output_files:
        run_atlasq(output_file, atlases)

    # Print the list of output file names
    print(f"")
    print("List of separate cluster image files:")
    for output_file in output_files:
        print(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to split a thresholded map into clusters and analyze using atlases.")
    parser.add_argument("file_path", help="Path to the text file.")
    parser.add_argument("input_file", help="Input file for fslmaths.")
    parser.add_argument("--threshold", type=int, default=99, help="Threshold value for fslmaths.")
    parser.add_argument("--atlases", nargs="+", required=True, help="List of atlases.")

    args = parser.parse_args()

    main(args.file_path, args.input_file, args.threshold, args.atlases)