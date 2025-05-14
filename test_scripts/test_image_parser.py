##################################################################################################
#                                      TEST SCRIPT OVERVIEW                                      #
#                                                                                                #
# This test script runs the full board extraction pipeline on a sample Sudoku image.             #
# It loads the image, processes it through the image parser, and returns a 9x9 matrix            #
# representation of the puzzle.                                                                  #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from vision.image_parser import extract_board_from_image

##################################################################################################
#                                         CONFIGURATION                                          #
#                                                                                                #
# Define the image path for testing. Replace this with any valid image path to test extraction.  #
##################################################################################################

# Path to test image
image_path = "../inputs/easy_42.jpg"

##################################################################################################
#                                   RUN BOARD EXTRACTION PIPELINE                                #
#                                                                                                #
# Executes the full image parsing process: segmentation → digit classification → board matrix.   #
# Returns:                                                                                       #
#     list[list[int]]: 9x9 board with digits and zeros for empty cells.                          #
##################################################################################################

# Run extraction
board = extract_board_from_image(image_path)