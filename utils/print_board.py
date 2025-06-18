##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This utility module provides a simple CLI function to print a 9x9 Sudoku board in              #
# a human-readable format. Useful for debugging, logging or verifying board state                #
# before or after solving.                                                                       #
##################################################################################################

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def print_board(board: list[list[int]]) -> None:
    """
    Displays a 9x9 Sudoku board in a human-readable grid format.

    Groups digits into 3x3 blocks with separators for better visual clarity.
    Empty cells are displayed as dots (.) to distinguish them from filled ones.

    Args:
        board (list[list[int]]): The 9x9 Sudoku board to display.
    """

    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()

