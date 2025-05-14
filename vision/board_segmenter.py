##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script handles Sudoku grid segmentation. It takes a JPG/PNG image of a Sudoku puzzle,     #
# detects the board using contour detection and perspective transformation, and segments it      #
# into 81 individual cell images (9x9). These can then be passed to OCR modules for digit        #
# extraction.                                                                                    #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import cv2
import numpy as np
import os

##################################################################################################
#                                    IMAGE SEGMENTATION LOGIC                                    #
#                                                                                                #
# These helper functions handle all stages of preprocessing and grid extraction:                 #
# - Preprocessing the image with grayscale, blur and thresholding                                #
# - Finding the largest contour assumed to be the board                                          #
# - Warping the board into a clean top-down perspective                                          #
# - Splitting the 450x450 grid into 81 cell images (50x50 each)                                  #
##################################################################################################


##################################################################################################
#                               IMAGE PREPROCESSING FUNCTION                                     #
#                                                                                                #
# Enhances the image to highlight the grid structure for contour detection.                      #
# Applies grayscale conversion, Gaussian blur, and adaptive thresholding.                        #
#                                                                                                #
# Args:                                                                                          #
#     image (np.ndarray): Original BGR Sudoku image.                                             #
# Returns:                                                                                       #
#     np.ndarray: Preprocessed binary image highlighting grid lines.                             #
##################################################################################################

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    return thresh

##################################################################################################
#                                CONTOUR DETECTION FUNCTION                                      #
#                                                                                                #
# Detects the largest external contour in the binary image, which is assumed to be the           #
# Sudoku grid. This contour will be used for warping the board into a square.                    #
#                                                                                                #
# Args:                                                                                          #
#     thresh_img (np.ndarray): Preprocessed binary image.                                        #
# Returns:                                                                                       #
#     np.ndarray: Largest contour found in the image.                                            #
##################################################################################################

def find_largest_contour(thresh_img):
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return max(contours, key=cv2.contourArea)


##################################################################################################
#                           GRID WARPING AND ORIENTATION CORRECTION                              #
#                                                                                                #
# Applies a perspective transform to the detected 4-point Sudoku contour to obtain a             #
# top-down, square view of the grid. Also rotates and flips the image to correct orientation.    #
#                                                                                                #
# Args:                                                                                          #
#     image (np.ndarray): Original image.                                                        #
#     contour (np.ndarray): 4-point contour of the detected grid.                                #
#     size (int): Output size of the warped image (default: 450x450).                            #
# Returns:                                                                                       #
#     np.ndarray: Warped and correctly oriented grid image.                                      #
# Raises:                                                                                        #
#     ValueError: If the contour does not have exactly 4 points.                                 #
##################################################################################################

def warp_perspective(image, contour, size=450):

    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

    if len(approx) != 4:
        raise ValueError("Could not find 4-cornered grid contour.")

    points = approx.reshape(4, 2)
    points = sorted(points, key=lambda x: x[0] + x[1])
    tl, tr = sorted(points[:2], key=lambda x: x[0])
    bl, br = sorted(points[2:], key=lambda x: x[0])

    src = np.array([tl, tr, br, bl], dtype="float32")
    dst = np.array([[0, 0], [size-1, 0], [size-1, size-1], [0, size-1]], dtype="float32")

    matrix = cv2.getPerspectiveTransform(src, dst)

    warped = cv2.warpPerspective(image, matrix, (size, size))

    # 💡 FIX ORIENTATION
    warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)
    warped = cv2.flip(warped, 1)  # Horizontal flip

    return warped

##################################################################################################
#                                CELL SEGMENTATION FUNCTION                                      #
#                                                                                                #
# Splits the warped 450x450 Sudoku board into 81 square cells (9x9 grid), each of equal size.    #
# These cell images are used for individual digit classification.                                #
#                                                                                                #
# Args:                                                                                          #
#     warped_grid (np.ndarray): Top-down view of the Sudoku grid (450x450).                      #
# Returns:                                                                                       #
#     list[np.ndarray]: List of 81 cell images.                                                  #
##################################################################################################

def segment_cells(warped_grid):

    cells = []
    size = warped_grid.shape[0]  # assuming square
    cell_size = size // 9

    for y in range(9):
        for x in range(9):
            x1, y1 = x * cell_size, y * cell_size
            cell = warped_grid[y1:y1 + cell_size, x1:x1 + cell_size]
            cells.append(cell)
    return cells

##################################################################################################
#                                    MAIN FUNCTION INTERFACE                                     #
#                                                                                                #
# This function loads an image, detects and warps the Sudoku grid, and returns 81 segmented      #
# cell images for further processing.                                                            #
##################################################################################################

def extract_cells_from_image(image_path: str) -> list:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    preprocessed = preprocess_image(image)
    contour = find_largest_contour(preprocessed)
    warped = warp_perspective(image, contour)
    cell_images = segment_cells(warped)
    return cell_images
