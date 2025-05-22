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

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import sys
import tkinter as tk
from tkinter import filedialog
from utils.logs_config import logger

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def prompt_user_for_image():
    """
    Opens a GUI dialog to let the user select a Sudoku image file (JPG or PNG).

    Performs validation on the file path and exits gracefully if the selection is invalid.

    Returns:
        str: Full path to the selected image file.
    """

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
