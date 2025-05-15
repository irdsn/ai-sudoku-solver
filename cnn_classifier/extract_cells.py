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
#                                                                                                #
# Define paths for input Sudoku image and output directory where extracted cell images           #
# will be saved. The output directory is automatically created if it does not exist.             #
##################################################################################################

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Path to image to segment
IMAGE_PATH = "../datasets/sudokus/extreme_6.jpg"

# Output folder
OUTPUT_DIR = "../datasets/raw"

##################################################################################################
#                                      CELL EXTRACTION LOGIC                                     #
#                                                                                                #
# This function loads a Sudoku image, segments it into its 81 individual cells using the         #
# board segmenter, and saves each cell as a PNG image.                                           #
#                                                                                                #
# Input:                                                                                         #
# - image_path (str): Path to the Sudoku image file to process.                                  #
#                                                                                                #
# Output:                                                                                        #
# - 81 cell images saved to disk under a subfolder named after the original image.               #
##################################################################################################

def save_cells_from_image(image_path: str):
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(OUTPUT_DIR, image_name)

    os.makedirs(output_path, exist_ok=True)

    logger.info(f"📸 Processing image: {image_path}")
    cells = extract_cells_from_image(image_path)

    logger.info(f"💾 Saving 81 extracted cells to: {output_path}")

    for idx, cell in enumerate(cells):
        filename = f"{image_name}_cell_{idx:02}.png"
        cv2.imwrite(os.path.join(output_path, filename), cell)

    logger.info("✅ Done! Now label the images manually.")

##################################################################################################
#                                               MAIN                                             #
#                                                                                                #
# Script entry point. Executes the cell extraction pipeline for the image defined in             #
# IMAGE_PATH.                                                                                    #
##################################################################################################

if __name__ == "__main__":
    save_cells_from_image(IMAGE_PATH)
