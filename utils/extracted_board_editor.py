##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This utility module provides an interactive command-line interface to manually edit            #
# a 9x9 Sudoku board that was previously extracted from an image.                                #
#                                                                                                #
# The user can update specific cells by entering their coordinates and new values.               #
# This is useful to correct OCR errors before solving the puzzle.                                #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from utils.logs_config import logger

##################################################################################################
#                                  BOARD VISUALIZATION FUNCTION                                  #
#                                                                                                #
# Displays the current state of the 9x9 Sudoku board in a human-readable format.                 #
# Numbers are grouped into 3x3 blocks with visual separators. Empty cells are shown as dots (.)  #
# to distinguish them clearly from filled values.                                                #
#                                                                                                #
# Args:                                                                                          #
#     board (list[list[int]]): The 9x9 Sudoku board to display.                                  #
##################################################################################################

def print_board(board: list[list[int]]) -> None:
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()

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
        # Prompt user to confirm if they want to edit a cell
        choice = input("\n✏️  Do you want to edit any cell? (y/n): ").strip().lower()
        if choice != 'y':
            break

        try:
            # Get cell coordinates from user
            coords = input("Enter cell coordinates to edit (format: row,col — example: 0,6): ")

            row, col = map(int, coords.split(","))

            if not (0 <= row < 9 and 0 <= col < 9):
                logger.warning("🚫 Invalid coordinates. Must be between 0 and 8.")
                continue

            # Get new value for the cell
            value = int(input("Enter digit to assign (1–9), or 0 to clear the cell: "))
            if not (0 <= value <= 9):
                logger.warning("🚫 Invalid value. Must be between 0 and 9.")
                continue

            # Update the board and print the result
            board[row][col] = value
            logger.info("✅ Cell updated successfully.")
            print_board(board)

        except Exception as e:
            logger.error(f"⚠️  Exception: {e}. Try again.")
