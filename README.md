# FSL-Cluster-Analysis

Python script using the FSL atlasq command to analyse thresholded FEAT results. 

Usage: Automation of cluster analysis for FEAT results. The thresholded masks are split into separate clusters and labelled according the selected atlas. For each cluster a text file is created containing the percentages of brain areas within each cluster. 

Necessary inputs: 

       - Text file containing the clusters from FEAT e.g. "cluster_zstat1_std.txt"
       - NIFTI file containing the clusters from FEAT e.g. "cluster_mask_zstat1.nii.gz"
       - "--atlases". Name of the applied atlas e.g. "Harvard-Oxford Cortical Structural Atlas".

Optional inputs:

       - "--threshold". This allows to manually set the cluster size cut-off. The default is set at >99 voxels. 
       - "--atlases". Enter more than one atlas for multiple analyses e.g. "--atlases "MNI Structural Atlas" 
         "Juelich Histological Atlas" "

Notes:

    The script does check if the atlas and the input image have the same field of view. 
    If the field of view doesnt match no results will be computed. 
    Own atlases can be included. This allows to analyse results which are not in MNI152 space. 



Resulting files will have the following form:

```objc

Cluster: output_cluster_13
Size: 2214
Atlas: Adjusted_Atlas_HOSPA

Out of bounds:1.7320\
Left Cerebral White Matter:11.5770\
Left Cerebral Cortex:0.6381\
Left Lateral Ventricle:0.4102\
Left Thalamus:12.5798\
Left Caudate:10.6655\
Left Putamen:1.4585\
Left Pallidum:1.5041\
Left Accumbens:0.9116\
Right Cerebral White Matter:31.2215\
Right Cerebral Cortex:5.3783\
Right Lateral Ventricle:1.6864\
Right Thalamus:6.8824\
Right Caudate:11.1212\
Right Putamen:0.1367\
Right Accumbens:2.0966\

```
The results are percentages of voxels attributed to the atlas labels. 


Additionally, there is a text file created "Table_Cluster_Maxima_labeled". This file contains the coordinates for the Z-Max and the according labels from all choosen atlases. 

```objc

Cluster_Index	Size	       Z-MAX X (mm)	       Z-MAX Y (mm)	Z-MAX Z (mm)	Havard-Oxford Cortical      Havard-Oxford Subcortical
10		37903.0	       	       61.5		-38.5		39.5		Supramarginal Gyrus	       Right Cerebral Cortex
9		12226.0		       -62.5		-42.5		29.5		Supramarginal Gyrus	       Left Cerebral Cortex
8		2214.0		       -40.5		37.5		25.5		Frontal Pole		       Left Cerebral Cortex
7		402.0		       -32.5		45.5		-18.5		Frontal Pole		       Left Cerebral Cortex
6		353.0		       -18.5		-36.5		3.5		Out of bounds		       Left Thalamus
5		220.0		       35.5		-82.5		-36.5		Out of bounds		       Out of bounds
4		161.0		       -22.5		-82.5		-40.5		Out of bounds		       Out of bounds
3		122.0		       1.5		-96.5		-14.5		Out of bounds		       Out of bounds

```
