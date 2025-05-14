##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module handles digit classification for individual Sudoku cell images.                    #
# It loads a previously trained Convolutional Neural Network (CNN) model,                        #
# and uses it to predict whether a given grayscale image represents a digit from 1 to 9,         #
# or if the cell is empty.                                                                       #
#                                                                                                #
# The input is expected to be a 2D NumPy array (grayscale image of a cell).                      #
# The output is an integer:                                                                      #
#     - 1 to 9 → predicted digit                                                                 #
#     - 0      → if the cell is classified as empty                                              #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model

###################################################################################################
#                                        CONFIGURATION                                           #
#                                                                                                #
# Loads the trained CNN model from disk using the standard .keras format.                        #
# Defines the input image size expected by the model.                                            #
# Sets up class labels for mapping prediction outputs to digits (1–9) or 'empty'.                #
##################################################################################################

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "digit_model.keras")
IMG_SIZE = 64

model = load_model(MODEL_PATH)
class_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'empty']

##################################################################################################
#                                     CELL CLASSIFICATION FUNCTION                               #
#                                                                                                #
# Predicts the digit contained in a Sudoku cell using a trained CNN model.                       #
# The input image is first resized, normalized, and reshaped to fit model input format.          #
# The model outputs a class label which is mapped to its numeric value (1–9) or 0 if empty.      #
#                                                                                                #
# Args:                                                                                          #
#     cell_img (np.ndarray): Grayscale cell image as a 2D NumPy array.                           #
#                                                                                                #
# Returns:                                                                                       #
#     int: Predicted digit (1–9) or 0 if classified as empty.                                    #
##################################################################################################

def classify_cell(cell_img: np.ndarray) -> int:

    # Resize and normalize
    cell = cv2.resize(cell_img, (IMG_SIZE, IMG_SIZE))

    # Force grayscale in case cell is RGB
    if len(cell.shape) == 3 and cell.shape[2] == 3:
        cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

    cell = cell.astype("float32") / 255.0
    cell = np.expand_dims(cell, axis=-1)   # → (64, 64, 1)
    cell = np.expand_dims(cell, axis=0)    # → (1, 64, 64, 1)

    pred = model.predict(cell, verbose=0)
    predicted_class = np.argmax(pred)

    label = class_names[predicted_class]
    return int(label) if label != "empty" else 0
