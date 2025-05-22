##################################################################################################
#                                       TEST OVERVIEW                                            #
#                                                                                                #
# Unit tests for the SudokuSolver class. Verifies that the solver can correctly handle           #
# solvable puzzles and reject unsolvable ones.                                                   #
# Uses PyTest for structured testing and assertion handling.                                     #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from solver.bckt_logic_solver import SudokuSolver

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def test_solver_solves_valid_board():
    """
    Tests that the SudokuSolver can correctly solve a valid Sudoku puzzle.

    Verifies that the solver returns True and completes the puzzle successfully.
    """

    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    solver = SudokuSolver(board)
    solved = solver.solve()

    assert solved, "Solver failed to solve a valid puzzle"

def test_solver_rejects_invalid_board():
    """
    Tests that the SudokuSolver correctly rejects an invalid puzzle.

    The board contains conflicting values and should not be solvable.
    The solver is expected to return False.
    """

    invalid_board = [
        [5, 3, 5, 0, 7, 0, 0, 0, 0],  # ← duplicate 5 in row
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    solver = SudokuSolver(invalid_board)
    solved = solver.solve()

    assert not solved, "Solver should fail on an invalid puzzle"
