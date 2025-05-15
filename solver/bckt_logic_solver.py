##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module defines a AISudokuSolver class that solves 9x9 Sudoku puzzles using backtracking.  #
# It provides a method to solve the puzzle and a pretty printer to display it in grid format.    #
# The board is expected to be a 9x9 list of lists with 0 representing empty cells.               #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import time
from utils.extracted_board_editor import print_board
from utils.logs_config import logger

##################################################################################################
#                                            CLASS                                               #
#                                                                                                #
# AISudokuSolver encapsulates logic to solve 9x9 Sudoku puzzles using a recursive backtracking   #
# algorithm. Empty cells should be represented as 0.                                             #
#                                                                                                #
# Core Features:                                                                                 #
# - Pretty-print the board for visualization.                                                    #
# - Validate moves for rows, columns, and 3x3 subgrids.                                          #
# - Solve the puzzle recursively with backtracking.                                              #
# - Tracks solving steps and execution time (optional).                                          #
##################################################################################################

class SudokuSolver:

    ##################################################################################################
    #                                  INITIALIZE SOLVER INSTANCE                                    #
    #                                                                                                #
    # Initializes the solver with a given 9x9 Sudoku board.                                          #
    # Args:                                                                                          #
    #     board (list[list[int]]): The Sudoku puzzle as a nested list.                               #
    ##################################################################################################

    def __init__(self, board):
        self.board = board
        self.steps = 0  # Number of recursive steps taken during solving
        self.time_taken = 0  # Total solving time in seconds

    ##################################################################################################
    #                                       FIND EMPTY CELL                                          #
    #                                                                                                #
    # Searches the board for the next empty cell (represented by 0).                                 #
    # Returns:                                                                                       #
    #     tuple[int, int] or None: Coordinates (row, col) of the empty cell or None if full.         #
    ##################################################################################################

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    ##################################################################################################
    #                                     VALIDITY CHECK FOR MOVE                                    #
    #                                                                                                #
    # Determines whether a given number can be legally placed at a specific position.                #
    # It checks the row, column, and corresponding 3x3 subgrid.                                      #
    #                                                                                                #
    # Args:                                                                                          #
    #     num (int): Number to place (1–9).                                                          #
    #     pos (tuple[int, int]): Coordinates (row, col) of the cell.                                 #
    # Returns:                                                                                       #
    #     bool: True if valid placement, False otherwise.                                            #
    ##################################################################################################

    def is_valid(self, num, pos):
        row, col = pos

        # Row check
        if any(self.board[row][i] == num for i in range(9) if i != col):
            return False

        # Column check
        if any(self.board[i][col] == num for i in range(9) if i != row):
            return False

        # 3x3 subgrid check
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    ##################################################################################################
    #                                 SOLVE BOARD USING BACKTRACKING                                 #
    #                                                                                                #
    # Attempts to solve the Sudoku puzzle using backtracking.                                        #
    # Fills in values recursively, backtracking if a dead-end is reached.                            #
    #                                                                                                #
    # Returns:                                                                                       #
    #     bool: True if the board was successfully solved, False if no solution exists.              #
    ##################################################################################################

    def solve(self, verbose=True):

        start = time.perf_counter()
        solved = self._backtrack()
        end = time.perf_counter()

        self.time_taken = round(end - start, 4)

        if verbose:
            logger.info(f"🧠 Steps taken: {self.steps}")
            logger.info(f"⏱️ Time taken: {self.time_taken:.4f} seconds")

        return solved

    def _backtrack(self):
        find = self.find_empty()
        if not find:
            return True  # Solved

        row, col = find
        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                self.steps += 1

                if self._backtrack():
                    return True

                # Backtrack
                self.board[row][col] = 0

        return False

    ##################################################################################################
    #                                      GET CURRENT BOARD                                         #
    #                                                                                                #
    # Returns the current state of the board.                                                        #
    # Returns:                                                                                       #
    #     list[list[int]]: The 9x9 Sudoku board as a nested list.                                    #
    ##################################################################################################

    def get_board(self):
        return self.board
