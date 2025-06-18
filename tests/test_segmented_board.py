##################################################################################################
#                                      TEST OVERVIEW                                             #
#                                                                                                #
# Unit test for the board segmenter module. Validates that a Sudoku image                        #
# is correctly segmented into 81 individual cell readme_images.                                         #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from vision.board_segmenter import extract_cells_from_image

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def test_extract_cells_from_image_returns_81_cells():
    """
    Unit test for the board segmenter module.

    Verifies that the input Sudoku image is segmented into exactly 81 non-null cell readme_images.
    """

    image_path = "tests/resources/inputs/easy.jpg"
    cells = extract_cells_from_image(image_path)

    assert isinstance(cells, list), "Cells should be returned as a list"
    assert len(cells) == 81, "Should extract exactly 81 cells"
    assert all(cell is not None for cell in cells), "No cell should be None"
