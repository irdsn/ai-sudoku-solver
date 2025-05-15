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
import copy
from vision.image_parser import extract_board_from_image            # Extracts 9x9 board from image
from solver.bckt_logic_solver import SudokuSolver                   # Sudoku solver - Backtracking logic
from solver.ai_agent_solver import SudokuSolverAgent                # Sudoku solver - AI Agent
from utils.logs_config import logger                                # Logs and events
from utils.reporter import save_solution_report                     # Optional: save report as markdown
from utils.user_input import prompt_user_for_image                  # GUI-based image selector
from utils.extracted_board_editor import edit_board_interactively   # Optional board editor
from utils.extracted_board_editor import print_board                # Print board functionality

##################################################################################################
#                                          CONFIGURATION                                         #
##################################################################################################

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

SAVE_REPORT = True                       # Set to True to generate markdown report
USE_AGENT = True  # Toggle between backtracking and AI agent

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
    logger.info(f"📸 Loading Sudoku from: {IMAGE_PATH}")
    board = extract_board_from_image(IMAGE_PATH)

    if not isinstance(board, list) or len(board) != 9:
        logger.error("❌ Failed to extract board from image.")
        return

    logger.info("\n🧩 Extracted Sudoku Board:")
    print_board(board)

    ##################################################################################################
    #                               OPTIONAL USER CORRECTION BEFORE SOLVING                          #
    ##################################################################################################
    edit_board_interactively(board)

    # Create copies of the user-corrected board
    logic_board = copy.deepcopy(board)
    agent_board = copy.deepcopy(board)

    ##################################################################################################
    #                              SOLVE WITH LOGIC (BACKTRACKING)                                   #
    ##################################################################################################

    logic_solver = SudokuSolver(logic_board)
    logger.info("\n🧠 Solving with logic-based solver...")
    print_board(logic_solver.board)

    logic_success = logic_solver.solve()

    if logic_success:
        logger.info("\n✅ Logic Solver: Puzzle solved!")
        print_board(logic_solver.board)
    else:
        logger.warning("⚠️ Logic Solver could not solve the puzzle.")

    ##################################################################################################
    #                                 SOLVE WITH AI AGENT (LLM)                                      #
    ##################################################################################################

    agent_solver = SudokuSolverAgent(agent_board)
    logger.info("\n🤖 Solving with AI Agent...")
    print(agent_solver.format_board())

    agent_solver.solve_step_by_step()

    ##################################################################################################
    #                                    GENERATE MARKDOWN REPORT                                    #
    ##################################################################################################

    if SAVE_REPORT and logic_success:
        save_solution_report(
            original_board=board,
            solved_board=logic_solver.board,
            image_path=IMAGE_PATH
        )

##################################################################################################
#                                            ENTRY POINT                                         #
##################################################################################################

if __name__ == "__main__":
    main()
