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
import numpy as np

# Specify the directory to save output files
output_files = []
output_directory = "Split Cluster Masks"

# Specify the matrix to save the cluster informations in
matrix_data = np.array([0, 0, 0, 0, 0], dtype=str)

# Specify a counting variable
counting_var = 0


def read_txt_file(file_path, threshold):
    # Use the global matrix and counting variable
    global matrix_data
    global counting_var

    first_column_data = []
    local_maximum_data = []
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
                first_column = str(columns[0])
                second_column = float(columns[1])
                
                # Check if the number in the second column is larger than the specified threshold
                if second_column > threshold:
                    # Append the first column to first_column_data only if the condition is met
                    first_column_data.append(first_column)
    
            # Assuming there are at least 8 columns
            if len(columns) >= 8:
                # Extract values at positions 6, 7, and 8
                value_6 = float(columns[5])
                value_7 = float(columns[6])
                value_8 = float(columns[7])
                
                # Check if the value in the seventh column is larger than the specified threshold
                if second_column > threshold:
                    # Append the extracted values to the list
                    local_maximum_data.append((first_column, value_6, value_7, value_8))

                    # Append the matrix
                    new_row = np.array([first_column, second_column, value_6, value_7, value_8])
                    matrix_data = np.vstack([matrix_data, new_row])

    return first_column_data, local_maximum_data


def run_maximum(local_maximum_data, atlas):

    label_maxima = []
    i = 0
    for data_set in local_maximum_data:
        # Create a new list saving the labels
        i +=1

        first_column, value_6, value_7, value_8 = data_set
        # Concatenate values into a single string
        values_string = f"{value_6}, {value_7}, {value_8}"

        command = [
            "atlasq", "ohi",
            "-a", atlas,
            "-c", values_string,
        ]
#        print(values_string)
        result = subprocess.run(command, capture_output=True, text=True)
        output_lines = result.stdout.split('<br>', 1)  # Split at the first occurrence of <br>
        label_maximum = output_lines[1].strip() if len(output_lines) > 1 else ""  # Take the second part and strip whitespace
#        print(label_maximum)  # Print for verification
        label_maxima.append(label_maximum)

        print(f"Number of Clusters in {atlas} analysed = {i}")
#        Print for debugging
#        print(label_maxima)

    return label_maxima


def run_label_loop(atlases, local_maximum_data):
    global matrix_data

    # Maybe the label loop has to be done here..
    i = 0
    for atlas in atlases:

        #Additional loop
        i += 1
        if i == 1:
            # Change the list
            row_to_remove = 0

            # Remove the specified row
            matrix_data = np.delete(matrix_data, row_to_remove, axis=0)

        # Create some list to capture the information about the labels of each atlas
        label_maxima = run_maximum(local_maximum_data, atlas)

        # Start the script to add the labels to the cluster matrix
        new_column = np.array([label_maxima], dtype=str)
        matrix_data = np.hstack([matrix_data, new_column.reshape(-1, 1)])
#        print(label_maxima)
    

# Save the matrix information in a text file
def run_table_txt(atlases):
    global matrix_data

    np.set_printoptions(precision=None, suppress=True)
    print(f"")
    print(f"List of all clusters with peak maximum and atlas label:")
    print(f"")
    print(matrix_data)

    # Save the matrix to a text file
    matrix_txt_file = f"Table_Cluster_Maxima_labeled.txt"
    with open(matrix_txt_file, 'w') as txt_file:
        # Write headers
        headers = ["Cluster_Index", "Size", "Z-MAX X (mm)", "Z-MAX Y (mm)", "Z-MAX Z (mm)"] + [f"Label_{atlas}" for atlas in atlases]
        txt_file.write("\t".join(headers) + "\n")

        # Write matrix_data
        for row in matrix_data:
            txt_file.write("\t\t".join(row) + "\n")


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
#    print(output_file)

    subprocess.run(command)



def run_atlasq(input_file, atlases, counting_var):
    # Splitting the input_file into directory, file name, and extention. This allows the text files to be saved elsewhere.
    input_directory, input_fullname = os.path.split(input_file)
    input_fullname2, input_extension = os.path.splitext(input_fullname)
    input_name, input_extension = os.path.splitext(input_fullname2)

    # Import the matrix
    global matrix_data

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

        # Set the vaiable to insert the cluster size
        row_index = int(counting_var)
        cluster_size = matrix_data[row_index, 1]
        integer_value = int(float(cluster_size))
        cluster_size_str = str(integer_value)


        # Save the output to a text file
        output_txt_file = f"{input_name}_{atlas}.txt"
        with open(output_txt_file, 'w') as txt_file:
            txt_file.write(f"Cluster: {input_name}\n")
            txt_file.write(f"Size: {cluster_size_str}\n")
            txt_file.write(f"Atlas: {atlas}\n\n")
            txt_file.write(result.stdout)

        print(f"Results saved to: {output_txt_file}")



def main(file_path, input_file, threshold, atlases):
    # Import the global counting variable
    global counting_var
    global matrix_data

    print(f"Only clusters larger than threshold = {threshold} are analysed.")

    # Call the read_txt_file function with the provided file path
    first_column_data, local_maximum_data = read_txt_file(file_path, threshold)


    run_label_loop(atlases, local_maximum_data)
    run_table_txt(atlases)


    # Loop through numbers in first_column_data and run fslmaths for each
    for number in first_column_data:
        run_fslmaths(input_file, number)


    # Loop through output_files and run atlasq for each output file
    for output_file in output_files:
        run_atlasq(output_file, atlases, counting_var)
        # Increase the number of the counter by one
        counting_var = counting_var + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to split a thresholded map into clusters and analyze using atlases.")
    parser.add_argument("file_path", help="Path to the text file.")
    parser.add_argument("input_file", help="Input file for fslmaths.")
    parser.add_argument("--threshold", type=int, default=99, help="Threshold value for fslmaths.")
    parser.add_argument("--atlases", nargs="+", required=True, help="List of atlases.")

    args = parser.parse_args()

    main(args.file_path, args.input_file, args.threshold, args.atlases)
