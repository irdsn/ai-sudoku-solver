##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module orchestrates the full image-to-board pipeline:                                     #
# It takes a Sudoku image, segments it into 81 individual cells, classifies each one using a     #
# pre-trained CNN model, and reconstructs the final 9x9 board composed of digits and zeros.      #
# Zeros are used to represent empty or unrecognized cells.                                       #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from typing import List
from vision.board_segmenter import extract_cells_from_image
from cnn_classifier.digit_classifier import classify_cell

##################################################################################################
#                                    MAIN FUNCTION INTERFACE                                     #
#                                                                                                #
# Executes the complete pipeline: loads the image, segments it into 81 cells,                    #
# classifies each cell using the CNN model, and returns a 9x9 board matrix.                      #
#                                                                                                #
# Args:                                                                                          #
#     image_path (str): Path to the input Sudoku image file (e.g., .jpg or .png).                #
#                                                                                                #
# Returns:                                                                                       #
#     List[List[int]]: 9x9 matrix where each cell is a digit (1–9) or 0 for empty.               #
##################################################################################################

def extract_board_from_image(image_path: str) -> List[List[int]]:

    #print(f"📸 Loading image: {image_path}")

    cells = extract_cells_from_image(image_path)
    if len(cells) != 81:
        raise ValueError("Expected 81 cells from segmenter, got: {}".format(len(cells)))

    board = []
    for row in range(9):
        row_digits = []
        for col in range(9):
            idx = row * 9 + col
            digit = classify_cell(cells[idx])
            row_digits.append(digit)
        board.append(row_digits)

    '''
    print("🧩 Extracted Sudoku Board:\n")
    for r in board:
        print(" ".join(str(d) if d != 0 else "." for d in r))
    '''
    return board

