##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script handles Sudoku grid segmentation. It takes a JPG/PNG image of a Sudoku puzzle,     #
# detects the board using contour detection and perspective transformation, and segments it      #
# into 81 individual cell readme_images (9x9). These can then be passed to OCR modules for digit        #
# extraction.                                                                                    #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import cv2
import numpy as np
import os

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def preprocess_image(image):
    """
    Applies grayscale, Gaussian blur, and adaptive thresholding to enhance the Sudoku grid.

    Args:
        image (np.ndarray): Original BGR Sudoku image.

    Returns:
        np.ndarray: Preprocessed binary image highlighting grid lines.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    return thresh

def find_largest_contour(thresh_img):
    """
    Finds the largest external contour in a thresholded image.

    Assumes the largest contour corresponds to the Sudoku board.

    Args:
        thresh_img (np.ndarray): Binary preprocessed image.

    Returns:
        np.ndarray: Contour of the Sudoku grid.
    """

    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return max(contours, key=cv2.contourArea)

def warp_perspective(image, contour, size=450):
    """
    Warps a detected grid contour into a top-down square view.

    Applies a perspective transform and fixes orientation for consistency.

    Args:
        image (np.ndarray): Original image.
        contour (np.ndarray): 4-point contour of the Sudoku grid.
        size (int): Desired output size (default: 450).

    Returns:
        np.ndarray: Warped, oriented square image of the Sudoku grid.

    Raises:
        ValueError: If the contour does not have exactly 4 points.
    """

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

def segment_cells(warped_grid):
    """
    Splits a warped Sudoku grid into 81 equal-sized cell readme_images.

    Args:
        warped_grid (np.ndarray): Top-down 450x450 Sudoku grid image.

    Returns:
        list[np.ndarray]: List of 81 cell readme_images in row-major order.
    """

    cells = []
    size = warped_grid.shape[0]  # assuming square
    cell_size = size // 9

    for y in range(9):
        for x in range(9):
            x1, y1 = x * cell_size, y * cell_size
            cell = warped_grid[y1:y1 + cell_size, x1:x1 + cell_size]
            cells.append(cell)
    return cells

def extract_cells_from_image(image_path: str) -> list:
    """
    Full pipeline to extract 81 cell readme_images from a Sudoku puzzle image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        list[np.ndarray]: List of 81 segmented cell readme_images.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    preprocessed = preprocess_image(image)
    contour = find_largest_contour(preprocessed)
    warped = warp_perspective(image, contour)
    cell_images = segment_cells(warped)
    return cell_images
