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
#                              CLASSIFIER PREDICTION TEST CASE                                   #
#                                                                                                #
# Uses a white dummy image as input. Ensures that the classifier                                 #
# returns an integer between 0 and 9 (0 = empty).                                                #
##################################################################################################

def test_classify_cell_returns_digit_or_zero():
    dummy_cell = np.ones((64, 64), dtype="uint8") * 255  # white image

    prediction = classify_cell(dummy_cell)

    assert isinstance(prediction, int), "Prediction must be an integer"
    assert 0 <= prediction <= 9, "Prediction must be between 0 and 9"
