import numpy as np
import cv2
import sys

# returns the determinant of a 2x2 matrix.
def det(M):
    a = M[0][0]
    b = M[0][1]
    c = M[1][0]
    d = M[1][1]
    return a * d - b * c

# returns the trace of a 2x2 matrix.
def trace(M):
    a = M[0][0]
    d = M[1][1]
    return a + d

# returns a matrix used in cornerness calculation.
def generate_M(Ixx, Ixy, Iyy, window_radius, center_x, center_y):
    a, b, c, d = 0, 0, 0, 0
    for x in range(center_x-window_radius, center_x+window_radius+1):
        for y in range(center_y-window_radius, center_y+window_radius+1):
            a += Ixx[y][x]
            b += Ixy[y][x]
            c += Ixy[y][x]
            d += Iyy[y][x]
    return [[a, b], [c, d]]

# calculates cornerness in a defined radius.
def calculate_cornerness(image_path, k, window_radius):
    loaded_image = cv2.imread(image_path, 0)
    height, width = loaded_image.shape[0:2]
    # get data
    Ix = np.zeros((height, width), np.float32)
    Iy = np.zeros((height, width), np.float32)
    Ixx = np.zeros((height, width), np.float32)
    Iyy = np.zeros((height, width), np.float32)
    Ixy = np.zeros((height, width), np.float32)
    for x in range(1, width-1):
        for y in range(1, height-1):
            Iy[y][x] = float(loaded_image[y + 1][x]) - float(loaded_image[y][x])
            Ix[y][x] = float(loaded_image[y][x + 1]) - float(loaded_image[y][x])
            Ixx[y][x] = Ix[y][x] ** 2
            Iyy[y][x] = Iy[y][x] ** 2
            Ixy[y][x] = Iy[y][x] * Ix[y][x]
    # get cornerness
    cornerness = np.zeros((height, width), np.float32)
    for x in range(window_radius, width-window_radius):
        for y in range(window_radius, height-window_radius):
            M = generate_M(Ixx, Ixy, Iyy, window_radius, x, y)
            det_M = det(M)
            trace_M = trace(M)
            C = det_M - k * (trace_M**2)
            cornerness[y][x] = C
    return cornerness

# finds corners using a fraction of the maximum value as a threshold.
def find_corners(cornerness, fraction):
    height, width = cornerness.shape[0:2]
    max_value = 0
    for x in range(width):
        for y in range(height):
            max_value = max_value if max_value > cornerness[y][x] else cornerness[y][x]
    corners = np.zeros((height, width), np.float32)
    for x in range(width):
        for y in range(height):
            corners[y][x] = 0 if (max_value * fraction) > cornerness[y][x] else cornerness[y][x]
    return corners

# overlays corners onto the original image.
def create_overlay(corners, image_path):
    loaded_image = cv2.imread(image_path)
    height, width = corners.shape[0:2]
    for x in range(width):
        for y in range(height):
            if corners[y][x] > 0:
                loaded_image[y][x] = (0,0,255)
    return loaded_image

if __name__ == "__main__":
    # variables
    image_name = "checkerboard.png"
    # image must be in ./images
    image_path = f"./images/{image_name}"
    threshold = 0.2
    k = 0.05
    window_radius = 1
    # computation
    cornerness = calculate_cornerness(image_path, k, window_radius)
    corners = find_corners(cornerness, threshold)
    overlay = create_overlay(corners, image_path)
    # display results
    cv2.imshow("final image", overlay)
    cv2.waitKey(0)
    try:
        cv2.imwrite(f"output/{image_name}_{k}_{window_radius}_{threshold}.png", overlay)
        print("successfully wrote to ./output.")
        print("\ngeneration info:")
        print(f"image_name: {image_name}\nk: {k}\nwindow_radius: {window_radius}\nthreshold: {threshold}\n")
    except Exception as e:
        print("failed to write to ./output.")
        raise e;
