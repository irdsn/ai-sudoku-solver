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
import copy
from utils.logs_config import logger

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class SudokuSolver:

    def __init__(self, board):
        """
        Initializes the SudokuSolver with a given 9x9 board.

        Args:
            board (list[list[int]]): A 9x9 Sudoku board where empty cells are represented by 0.
        """

        self.board = board
        self.steps = 0  # Number of recursive steps taken during solving
        self.time_taken = 0  # Total solving time in seconds
        self.domains = self._initialize_domains()
        self.final_trace = []  # Capture solving trace

    def find_mrv_cell(self):
        """
        Finds the empty cell with the fewest legal values (MRV heuristic).

        Returns:
            tuple[int, int] or None: Coordinates of the most constrained empty cell,
            or None if the board is fully filled.
        """

        min_options = 10
        best_cell = None

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    options = [num for num in range(1, 10) if self.is_valid(num, (i, j))]
                    if len(options) < min_options:
                        min_options = len(options)
                        best_cell = (i, j)
                        if min_options == 1:
                            return best_cell  # Early exit

        return best_cell

    def is_valid(self, num, pos):
        """
        Checks whether a number can be legally placed in a given cell.

        Args:
            num (int): The number to place (1–9).
            pos (tuple[int, int]): Coordinates (row, col) of the target cell.

        Returns:
            bool: True if the placement is valid, False otherwise.
        """

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

    def solve(self, verbose=True):
        """
        Attempts to solve the Sudoku board using recursive backtracking with MRV and forward checking.

        Args:
            verbose (bool): If True, logs step count and total solving time.

        Returns:
            bool: True if the puzzle was successfully solved, False otherwise.
        """

        start = time.perf_counter()
        solved = self._backtrack()
        end = time.perf_counter()

        self.time_taken = round(end - start, 4)

        if verbose:
            logger.info(f"🧠 Steps taken: {self.steps}")
            logger.info(f"⏱️ Time taken: {self.time_taken:.4f} seconds")

        return solved

    def _backtrack(self):
        """
        Core recursive backtracking solver.

        Returns:
            bool: True if a valid solution is found, False if backtracking fails.
        """

        find = self.find_mrv_cell()
        if not find:
            return True  # Solved

        row, col = find
        options = self.domains.get((row, col), [])

        for num in options:
            logger.debug(f"  ➤ Testing {num} at ({row},{col})")

            if self.is_valid(num, (row, col)):
                prev_domains = copy.deepcopy(self.domains)

                self.board[row][col] = num

                if self._forward_check(row, col, num):
                    self.steps += 1
                    logger.debug(f"✅ Placed {num} at ({row},{col}) [Step {self.steps}]")

                    # Save final trace (only when it is actually placed)
                    self.final_trace.append({
                        "row": row,
                        "col": col,
                        "value": num,
                        "step": self.steps
                    })

                    if self._backtrack():
                        return True

                    logger.debug(f"❌ Backtrack on ({row},{col}), removing {num}")

                self.board[row][col] = 0
                self.domains = prev_domains

        return False

    def _initialize_domains(self):
        """
        Initializes the domain of possible values for each empty cell.

        Returns:
            dict: Mapping of cell coordinates to lists of valid numbers.
        """

        domains = {}
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    domains[(i, j)] = [n for n in range(1, 10) if self.is_valid(n, (i, j))]
        return domains

    def _forward_check(self, row, col, value):
        """
        Performs forward checking by updating domains of related cells.

        Args:
            row (int): Row index of the placed value.
            col (int): Column index of the placed value.
            value (int): The value placed in the cell.

        Returns:
            bool: True if no domain is emptied (i.e., no conflicts), False otherwise.
        """

        affected = []

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and (i, j) in self.domains and (
                        i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3)):
                    if value in self.domains[(i, j)]:
                        self.domains[(i, j)].remove(value)
                        affected.append((i, j))
                        if not self.domains[(i, j)]:
                            return False  # No valid values left
        return True

    def get_board(self):
        """
        Returns the current state of the Sudoku board.

        Returns:
            list[list[int]]: The 9x9 board as a nested list.
        """

        return self.board