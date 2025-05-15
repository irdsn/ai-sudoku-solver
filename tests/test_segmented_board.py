##################################################################################################
#                                      TEST OVERVIEW                                             #
#                                                                                                #
# Unit test for the board segmenter module. Validates that a Sudoku image                        #
# is correctly segmented into 81 individual cell images.                                         #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from vision.board_segmenter import extract_cells_from_image

##################################################################################################
#                                CELL SEGMENTATION TEST CASE                                     #
#                                                                                                #
# Ensures that the board segmenter returns exactly 81 cells from a full Sudoku board image.      #
# Each cell should be a non-null image array.                                                    #
##################################################################################################

def test_extract_cells_from_image_returns_81_cells():
    image_path = "tests/resources/easy.jpg"
    cells = extract_cells_from_image(image_path)

    assert isinstance(cells, list), "Cells should be returned as a list"
    assert len(cells) == 81, "Should extract exactly 81 cells"
    assert all(cell is not None for cell in cells), "No cell should be None"
