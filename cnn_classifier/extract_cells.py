##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script prepares a datasets for training a custom CNN digit classifier.                    #
# It loads a Sudoku image, segments it into 81 cells, and saves each cell as an image            #
# in a folder based on the image name.                                                           #
# These can then be manually labeled and organized into folders for training.                    #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import cv2
import sys
from utils.logs_config import logger
from vision.board_segmenter import extract_cells_from_image

##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Path to image to segment
IMAGE_PATH = "../datasets/sudokus/extreme_6.jpg"

# Output folder
OUTPUT_DIR = "../datasets/raw"

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def save_cells_from_image(image_path: str):
    """
    Segments a Sudoku image into 81 individual cell readme_images and saves them to disk.

    Given a path to a full Sudoku board image, this function uses the board segmenter
    to extract each of the 81 cells. The resulting cell readme_images are saved as individual
    PNG files in a subdirectory named after the source image.

    Args:
        image_path (str): Path to the input Sudoku image file.

    Output:
        81 PNG readme_images saved to a subfolder within OUTPUT_DIR.
    """

    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(OUTPUT_DIR, image_name)

    os.makedirs(output_path, exist_ok=True)

    logger.info(f"📸 Processing image: {image_path}")
    cells = extract_cells_from_image(image_path)

    logger.info(f"💾 Saving 81 extracted cells to: {output_path}")

    for idx, cell in enumerate(cells):
        filename = f"{image_name}_cell_{idx:02}.png"
        cv2.imwrite(os.path.join(output_path, filename), cell)

    logger.info("✅ Done! Now label the readme_images manually.")

##################################################################################################
#                                               MAIN                                             #
##################################################################################################

if __name__ == "__main__":
    save_cells_from_image(IMAGE_PATH)
