The Harris corner detector is a computer vision algorithm used to identify key features in an image. 
This program detects corners, overlays them on the original image, and saves the processed results.
 

Features:
- Identifies corners and marks their locations
- Saves images in the output folder
- Displays key parameters used in the algorithm
- Full error handling, including fallback image
 

Process:
- Calculate spatial derivatives in the X and Y directions
- Build the structure tensor matrix
- Calculate the Harris response using the structure tensor
- Identify relative maximum values
- Overlay these values onto the original image
- Save and display results
 

Usage (default image):
```
python3 main.py
```
 

Usage (custom image):
```
python3 main.py ./path/to/an/image.png
```
 

Note: Requires python, opencv2, and numpy installed.
 

2025
