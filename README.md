# FSL-Cluster-Analysis

Python script using the FSL atlasq command to analyse thresholded FEAT results. 

Usage: Automation of cluster analysis for FEAT results. The thresholded masks are split into separate clusters and labelled according the selected atlas. For each cluster a text file is created containing the percentages of brain areas within each cluster. 

Necessary inputs: 

        Text file containing the clusters from FEAT e.g. "cluster_zstat1_std.txt"
        NIFTI file containing the clusters from FEAT e.g. "cluster_mask_zstat1.nii.gz"
        "--atlases". Name of the applied atlas e.g. "Harvard-Oxford Cortical Structural Atlas".

Optional inputs:

        "--threshold". This allows to manually set the cluster size cut-off. The default is set at >99 voxels. 
        "--atlases". Enter more than one atlas for multiple analyses e.g. "--atlases "MNI Structural Atlas" "Juelich Histological Atlas" "

Notes:

    The script does check if the atlas and the input image have the same field of view. If the field of view doesnt match no results will be computed. 
    Own atlases can be included. This allows to analyse results which are not in MNI152 space. 
