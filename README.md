Summary:
The Harris corner detector is a computer vision algorithm used to identify key features (corners) in an image. 
This program detects corners, overlays them on the original image, and saves the processed results.

Features:
- Identifies corners and marks their locations
- Saves images in the output folder
- Displays key parameters used in the algorithm

Algorithm:
- Calculates spatial derivatives in the X and Y directions
- Constructs a structure tensor matrix
- Calculate Harris response using the structure tensor
- Identify local maximum values
- Overlay these values onto the original image

Todo:
- Take command line parameters


2025
