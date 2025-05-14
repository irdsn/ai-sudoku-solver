##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# Main entry point for the complete Sudoku solving pipeline.                                     #
#                                                                                                #
# This script orchestrates the entire process from image to solution:                            #
#   1. Prompts the user to select a Sudoku image (JPG/PNG).                                      #
#   2. Uses computer vision techniques to detect and extract the Sudoku grid.                    #
#   3. Segments the board into 81 individual cells and classifies each using a trained CNN.      #
#   4. Reconstructs the 9x9 board with digits and blank cells.                                   #
#   5. Displays the detected board to the user, offering manual correction if needed.            #
#   6. Solves the puzzle using a classic backtracking algorithm.                                 #
#   7. Optionally generates a Markdown report with both the original and solved board.           #
#                                                                                                #
# Output:                                                                                        #
#   - Displays results to the console.                                                           #
#   - Saves markdown report to `outputs/` folder if enabled.                                     #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import sys
import os
import tkinter as tk
from tkinter import filedialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from vision.image_parser import extract_board_from_image    # Extracts 9x9 board from image
from solver.sudoku_solver import SudokuSolver               # Sudoku solver agent
from utils.reporter import save_solution_report             # Optional: save report as markdown

##################################################################################################
#                                          CONFIGURATION                                         #
##################################################################################################

SAVE_REPORT = True                       # Set to True to generate markdown report

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

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select a Sudoku image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        print("❌ No image selected. Exiting.")
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"❌ File does not exist: {file_path}")
        sys.exit(1)

    return file_path

##################################################################################################
#                             INTERACTIVE BOARD EDITING FUNCTION                                 #
#                                                                                                #
# Allows the user to modify specific cells in the extracted board before solving.                #
# Users can input cell coordinates (row,col) and values (1–9) or 0 to clear the cell.            #
# A live view of the board is printed after each edit to verify changes.                         #
#                                                                                                #
# Args:                                                                                          #
#     board (list[list[int]]): 9x9 Sudoku board extracted from the image                         #
##################################################################################################

def edit_board_interactively(board):

    while True:
        choice = input("\n✏️  Do you want to edit any cell? (y/n): ").strip().lower()
        if choice != 'y':
            break

        try:
            coords = input("Enter cell coordinates as row,col (0-based): ")
            row, col = map(int, coords.split(","))

            if not (0 <= row < 9 and 0 <= col < 9):
                print("❌ Invalid coordinates. Must be between 0 and 8.")
                continue

            value = int(input("Enter value (1-9) or 0 to clear: "))
            if not (0 <= value <= 9):
                print("❌ Invalid value. Must be between 0 and 9.")
                continue

            board[row][col] = value
            print("✅ Cell updated.")
            agent = SudokuSolver(board)
            agent.print_board()

        except Exception as e:
            print(f"❌ Error: {e}. Try again.")

##################################################################################################
#                                      MAIN EXECUTION LOGIC                                      #
#                                                                                                #
# High-level orchestration of the Sudoku solving pipeline.                                       #
# 1. Loads an image selected by the user                                                         #
# 2. Extracts a 9x9 grid of digits using CNN-based OCR                                           #
# 3. Optionally allows the user to modify detected values                                        #
# 4. Solves the puzzle with backtracking                                                         #
# 5. Optionally generates a Markdown report of the solution                                      #
##################################################################################################

def main():
    IMAGE_PATH = prompt_user_for_image()
    print(f"📸 Loading Sudoku from: {IMAGE_PATH}")
    board = extract_board_from_image(IMAGE_PATH)

    print(f"\n📋 Raw board data: {board}")

    if not board or not isinstance(board, list):
        print("❌ Failed to extract board from image.")
        return

    print("\n🧩 Extracted Sudoku Board:")
    agent = SudokuSolver(board)
    agent.print_board()

    # Optional editing
    edit_board_interactively(agent.board)

    print("\n🧠 Solving...")
    if agent.solve():
        print("\n✅ Sudoku Solved:")
        agent.print_board()

        if SAVE_REPORT:
            save_solution_report(
                original_board=board,
                solved_board=agent.board,
                image_path=IMAGE_PATH
            )
    else:
        print("❌ Could not solve the Sudoku.")

##################################################################################################
#                                            ENTRY POINT                                         #
##################################################################################################

if __name__ == "__main__":
    main()
