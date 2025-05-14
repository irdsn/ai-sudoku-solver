##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script loads a Sudoku image, applies board segmentation, and visually displays:           #
# - The warped (flattened) Sudoku board.                                                         #
# - A 9x9 grid of individual cell previews.                                                      #
#                                                                                                #
# It is intended for manual visual inspection to verify segmentation quality, orientation,       #
# rotation correctness, or preprocessing accuracy before generating training data for a CNN.     #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import cv2
import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vision.board_segmenter import extract_cells_from_image, warp_perspective, preprocess_image, find_largest_contour

##################################################################################################
#                                         CONFIGURATION                                          #
#                                                                                                #
# Path to the input Sudoku image. This file will be preprocessed, warped, and segmented.         #
##################################################################################################


IMAGE_PATH = "../datasets/sudokus/easy_2.jpg"

##################################################################################################
#                                        VISUALIZATION                                           #
#                                                                                                #
# Display the extracted 81 cells in a visual grid using OpenCV. Each cell is placed in a         #
# 9x9 composite image to simulate the original board layout.                                     #
# Args:                                                                                          #
#     cells (list of np.ndarray): List of 81 cell images extracted from the warped board.        #
##################################################################################################

def visualize_cells(cells: list):

    cell_size = cells[0].shape[0]
    grid_image = np.zeros((cell_size * 9, cell_size * 9), dtype=np.uint8)

    for idx, cell in enumerate(cells):
        row, col = divmod(idx, 9)
        grid_image[row*cell_size:(row+1)*cell_size, col*cell_size:(col+1)*cell_size] = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

    cv2.imshow("🧩 81 Segmented Cells", grid_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

##################################################################################################
#                                              MAIN                                              #
#                                                                                                #
# Full pipeline:                                                                                 #
# - Load and preprocess image.                                                                   #
# - Detect and extract largest contour (the Sudoku grid).                                        #
# - Warp the grid to a top-down perspective.                                                     #
# - Segment into 81 cells and display them for verification.                                     #
##################################################################################################

if __name__ == "__main__":
    image = cv2.imread(IMAGE_PATH)
    preprocessed = preprocess_image(image)
    contour = find_largest_contour(preprocessed)
    warped = warp_perspective(image, contour)

    # Show the warped (flattened) board before splitting
    cv2.imshow("📐 Warped Sudoku Board", warped)

    # Segment the board
    cells = []
    cell_size = warped.shape[0] // 9
    for y in range(9):
        for x in range(9):
            cell = warped[y*cell_size:(y+1)*cell_size, x*cell_size:(x+1)*cell_size]
            cells.append(cell)

    visualize_cells(cells)
