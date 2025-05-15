##################################################################################################
#                                      TEST OVERVIEW                                             #
#                                                                                                #
# Unit test for the image parser module. Ensures that a Sudoku image can be correctly            #
# processed into a 9x9 board matrix using computer vision and digit classification.              #
# Requires a valid test image to be present under inputs/.                                       #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from vision.image_parser import extract_board_from_image

##################################################################################################
#                                 BOARD EXTRACTION TEST CASE                                     #
#                                                                                                #
# Tests that the image parser returns a valid 9x9 matrix from a sample image.                    #
# Validates the structure of the board (list of lists with 9 elements each).                     #
##################################################################################################

def test_extract_board_returns_valid_matrix():
    image_path = "tests/resources/easy.jpg"
    board = extract_board_from_image(image_path)

    assert isinstance(board, list), "Board should be a list"
    assert len(board) == 9, "Board should have 9 rows"
    assert all(isinstance(row, list) and len(row) == 9 for row in board), "Each row must have 9 elements"
