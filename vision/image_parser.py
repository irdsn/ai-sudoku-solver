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
from utils.logs_config import logger

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def extract_board_from_image(image_path: str) -> List[List[int]]:
    """
    Extracts a 9x9 Sudoku board from an input image using cell segmentation and digit classification.

    The image is split into 81 cells, each of which is passed through a CNN model to detect the digit.
    Unrecognized or empty cells are represented with a 0.

    Args:
        image_path (str): Path to the input image file (.jpg or .png).

    Returns:
        List[List[int]]: A 9x9 matrix representing the Sudoku board.
    """

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
    logger.info("🧩 Extracted Sudoku Board:\n")
    for r in board:
        logger.info(" ".join(str(d) if d != 0 else "." for d in r))
    '''
    return board
