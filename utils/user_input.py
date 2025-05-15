##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This utility module provides a function to prompt the user to select an image file             #
# using a GUI file dialog (Tkinter). It performs basic validation to ensure the selected         #
# file exists, and exits the program gracefully if not.                                          #
#                                                                                                #
# This module is intended to be reused anywhere in the pipeline where user-driven                #
# image selection is needed.                                                                     #
##################################################################################################
import logging
##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import sys
import tkinter as tk
from tkinter import filedialog
from utils.logs_config import logger

##################################################################################################
#                                USER IMAGE SELECTION FUNCTION                                   #
#                                                                                                #
# Prompts the user with a GUI file dialog to select an image file (JPG or PNG).                  #
# Performs validation on the selected file and exits gracefully if no valid file is provided.    #
#                                                                                                #
# Returns:                                                                                       #
#     str: Full path to the selected Sudoku image file                                           #
##################################################################################################

def prompt_user_for_image():

    # Initialize Tkinter root and hide the main window
    root = tk.Tk()
    root.withdraw()

    # Open file selection dialog (restrict to JPG/PNG)
    file_path = filedialog.askopenfilename(
        title="Select a Sudoku image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    # Exit if no file is selected
    if not file_path:
        logger.error("❌ No image selected. Exiting.")
        sys.exit(1)

    # Exit if file does not exist
    if not os.path.exists(file_path):
        logger.error(f"❌ File does not exist: {file_path}")
        sys.exit(1)

    return file_path
