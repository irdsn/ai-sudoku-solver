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
        self.domains = self._initialize_domains()

    ##################################################################################################
    #                                       FIND EMPTY CELL                                          #
    #                                                                                                #
    # Searches the board for the next empty cell (represented by 0).                                 #
    # Returns:                                                                                       #
    #     tuple[int, int] or None: Coordinates (row, col) of the empty cell or None if full.         #
    ##################################################################################################

    def find_mrv_cell(self):
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
        find = self.find_mrv_cell()
        if not find:
            return True  # Solved

        row, col = find
        options = self.domains.get((row, col), [])

        for num in options:
            print(f"  ➤ Testing {num} at ({row},{col})")
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                prev_domains = copy.deepcopy(self.domains)
                if self.is_valid(num, (row, col)):
                    self.board[row][col] = num
                    if self._forward_check(row, col, num):
                        print(f"✅ Placed {num} at ({row},{col}) [Step {self.steps + 1}]")
                        self.steps += 1
                        if self._backtrack():
                            return True
                        print(f"❌ Backtrack on ({row},{col}), removing {num}")

                    # Backtrack
                    self.board[row][col] = 0
                    self.domains = prev_domains

        return False

    def _initialize_domains(self):
        domains = {}
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    domains[(i, j)] = [n for n in range(1, 10) if self.is_valid(n, (i, j))]
        return domains

    def _forward_check(self, row, col, value):
        affected = []

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 and (i, j) in self.domains and (
                        i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3)):
                    if value in self.domains[(i, j)]:
                        self.domains[(i, j)].remove(value)
                        affected.append((i, j))
                        if not self.domains[(i, j)]:
                            return False  # No valid values left → inconsistencia
        return True

    ##################################################################################################
    #                                      GET CURRENT BOARD                                         #
    #                                                                                                #
    # Returns the current state of the board.                                                        #
    # Returns:                                                                                       #
    #     list[list[int]]: The 9x9 Sudoku board as a nested list.                                    #
    ##################################################################################################

    def get_board(self):
        return self.board



##################################################################################################
#                                      GET CURRENT BOARD                                         #
#                                                                                                #
# Returns the current state of the board.                                                        #
# Returns:                                                                                       #
#     list[list[int]]: The 9x9 Sudoku board as a nested list.                                    #
##################################################################################################
if __name__ == "__main__":
    from vision.image_parser import extract_board_from_image  # Extracts 9x9 board from image
    from utils.extracted_board_editor import edit_board_interactively, print_board
    from utils.reporter import save_solution_report
    from utils.logs_config import logger

    IMAGE_PATH = "../inputs/extreme.jpg"

    # Extraer tablero desde imagen
    parsed_board = extract_board_from_image(IMAGE_PATH)

    if not isinstance(parsed_board, list) or len(parsed_board) != 9:
        logger.error("❌ Failed to extract board from image.")
        exit()

    logger.info("\n🧩 Extracted Sudoku Board:")
    print_board(parsed_board)

    # Lanzar editor visual (te devuelve la tabla posiblemente corregida)
    edited_board = parsed_board.copy()
    edit_board_interactively(edited_board)

    # Mostrar el tablero final antes de resolver
    print("\n📋 Edited board:")
    print_board(edited_board)

    # Resolver con backtracking y trazas activadas
    solver = SudokuSolver(edited_board)
    success = solver.solve(verbose=True)

    if success:
        print("\n✅ Solved board:")
        print_board(solver.get_board())
    else:
        print("\n❌ Failed to solve the board.")

    # Guardar reporte (sea éxito o no)
    save_solution_report(
        input_board=parsed_board,
        parsed_board=parsed_board,
        edited_board=edited_board,
        solved_board=solver.get_board(),
        bckt_metrics={
            "solved": success,
            "steps": solver.steps,
            "duration": solver.time_taken,
        },
        image_path=IMAGE_PATH
    )
