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
#   6. Solves the puzzle using both classic backtracking algorithm and AI Agent.                 #
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
import io
import copy
import logging
from vision.image_parser import extract_board_from_image            # Extracts 9x9 board from image
from solver.bckt_logic_solver import SudokuSolver                   # Sudoku solver - Backtracking logic
from solver.ai_agent_solver import SudokuSolverAgent                # Sudoku solver - AI Agent
from utils.logs_config import logger                                # Logs and events
from utils.reporter import save_solution_report                     # save report as markdown
from utils.user_input import prompt_user_for_image                  # GUI-based image selector
from utils.extracted_board_editor import edit_board_interactively   # Optional board editor
from utils.extracted_board_editor import print_board                # Print board functionality


##################################################################################################
#                                          CONFIGURATION                                         #
##################################################################################################

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

SAVE_REPORT = True  # Set to True to generate markdown report
USE_AGENT = True    # Toggle between backtracking and AI agent

##################################################################################################
#                                     DUAL OUTPUT STREAM WRAPPER                                 #
#                                                                                                #
# This utility class redirects output to multiple streams simultaneously.                        #
# It is used to mirror `stdout` and `stderr` to both the terminal and an in-memory buffer,       #
# allowing real-time console display while also capturing the entire execution log for reporting.#
#                                                                                                #
# Useful for generating full reproducible logs inside the Markdown report.                       #
##################################################################################################

class DualOutput:
    def __init__(self, *outputs):
        self.outputs = outputs

    def write(self, message):
        for out in self.outputs:
            out.write(message)
            out.flush()

    def flush(self):
        for out in self.outputs:
            out.flush()

##################################################################################################
#                                      MAIN EXECUTION LOGIC                                      #
#                                                                                                #
# High-level orchestration of the Sudoku solving pipeline.                                       #
# 1. Loads an image selected by the user                                                         #
# 2. Extracts a 9x9 grid of digits using CNN-based OCR                                           #
# 3. Optionally allows the user to modify detected values                                        #
# 4. Solves the puzzle with backtracking                                                         #
# 5. Generates a Markdown report of the solution                                                 #
##################################################################################################

def main():
    IMAGE_PATH = prompt_user_for_image()

    # Prepare in-memory capture of stdout/stderr
    log_capture = io.StringIO()
    sys.stdout = DualOutput(sys.__stdout__, log_capture)
    sys.stderr = DualOutput(sys.__stderr__, log_capture)

    capture_handler = logging.StreamHandler(log_capture)
    capture_handler.setLevel(logging.DEBUG)
    capture_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

    # Add temporary handler to the logger
    logger.addHandler(capture_handler)

    logger.info(f"📸 Loading Sudoku from: {IMAGE_PATH}")
    parsed_board = extract_board_from_image(IMAGE_PATH)

    if not isinstance(parsed_board, list) or len(parsed_board) != 9:
        logger.error("❌ Failed to extract board from image.")
        return

    logger.info("\n🧩 Extracted Sudoku Board:")
    print_board(parsed_board)

    ##################################################################################################
    #                               OPTIONAL USER CORRECTION BEFORE SOLVING                          #
    ##################################################################################################

    input_board = copy.deepcopy(parsed_board)
    edit_board_interactively(parsed_board)
    edited_board = parsed_board

    # Create copies of the user-corrected board
    logic_board = copy.deepcopy(edited_board)
    agent_board = copy.deepcopy(edited_board)

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

    bckt_metrics = {
        "method": "Backtracking",
        "solved": logic_success,
        "steps": logic_solver.steps,
        "duration": logic_solver.time_taken
    }

    ##################################################################################################
    #                                 SOLVE WITH AI AGENT (LLM)                                      #
    ##################################################################################################

    agent_solver = SudokuSolverAgent(agent_board)
    logger.info("\n🤖 Solving with AI Agent...")
    print(agent_solver.format_board())

    agent_solver.solve_step_by_step()

    ai_metrics = {
        "method": "AI Agent",
        "solved": agent_solver.is_solved(),
        "steps": agent_solver.steps,
        "duration": agent_solver.time_taken,
        "final_board": agent_solver.board
    }

    logger.info("\n🧾 Final board by AI Agent:\n")
    print_board(agent_solver.board)

    ##################################################################################################
    #                                    GENERATE MARKDOWN REPORT                                    #
    ##################################################################################################

    # Restore and save captured console output to file
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    console_log_path = os.path.join("outputs", f"{os.path.splitext(os.path.basename(IMAGE_PATH))[0]}_console.log")
    with open(console_log_path, "w") as f:
        f.write(log_capture.getvalue())

    if SAVE_REPORT and logic_success:
        save_solution_report(
            input_board=input_board,
            parsed_board=input_board,
            edited_board=edited_board,
            solved_board=logic_solver.board,
            bckt_metrics=bckt_metrics,
            ai_metrics=ai_metrics,
            image_path=IMAGE_PATH
        )

    logger.removeHandler(capture_handler)

##################################################################################################
#                                            ENTRY POINT                                         #
##################################################################################################

if __name__ == "__main__":
    main()
