##################################################################################################
#                                      TEST OVERVIEW                                             #
#                                                                                                #
# Unit test for the digit classifier module. Verifies that the classifier returns                #
# a valid digit (0–9) when provided with a dummy grayscale cell image.                           #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import numpy as np
from cnn_classifier.digit_classifier import classify_cell

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def test_classify_cell_returns_digit_or_zero():
    """
    Unit test for the digit classifier.

    Verifies that the classifier returns an integer between 0 and 9
    (where 0 indicates an empty cell) when given a dummy grayscale image.
    """

    dummy_cell = np.ones((64, 64), dtype="uint8") * 255  # white image

    prediction = classify_cell(dummy_cell)

    assert isinstance(prediction, int), "Prediction must be an integer"
    assert 0 <= prediction <= 9, "Prediction must be between 0 and 9"
