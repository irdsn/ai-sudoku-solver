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
#                                        IMPLEMENTATION                                          #
##################################################################################################

def test_extract_board_returns_valid_matrix():
    """
    Unit test for the image parser module.

    Verifies that a Sudoku image is correctly processed into a valid 9x9 matrix.
    Ensures that the result is a list of 9 lists, each containing 9 elements.
    """

    image_path = "tests/resources/easy.jpg"
    board = extract_board_from_image(image_path)

    assert isinstance(board, list), "Board should be a list"
    assert len(board) == 9, "Board should have 9 rows"
    assert all(isinstance(row, list) and len(row) == 9 for row in board), "Each row must have 9 elements"
