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
import json
import logging
from vision.image_parser import extract_board_from_image            # Extracts 9x9 board from image
from solver.bckt_logic_solver import SudokuSolver                   # Sudoku solver - Backtracking logic
from utils.logs_config import logger                                # Logs and events
from utils.reporter import save_solution_report                     # save report as markdown
from utils.user_input import prompt_user_for_image                  # GUI-based image selector
from utils.extracted_board_editor import edit_board_interactively   # Optional board editor
from utils.extracted_board_editor import print_board                # Print board functionality
from utils.reporter import generate_trace_filename                  # Solution traces


##################################################################################################
#                                          CONFIGURATION                                         #
##################################################################################################

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

class DualOutput:
    """
    Custom output stream that duplicates stdout and stderr messages to multiple destinations.

    Used to display console output in real-time while also capturing it for later use
    (e.g., in Markdown reports).
    """

    def __init__(self, *outputs):
        self.outputs = outputs

    def write(self, message):
        """
        Writes a message to all attached output streams.

        Args:
            message (str): The string message to write.
        """

        for out in self.outputs:
            out.write(message)
            out.flush()

    def flush(self):
        """
        Flushes all attached output streams to ensure data is written immediately.
        """

        for out in self.outputs:
            out.flush()

def main():
    """
    Main function that executes the full Sudoku solving pipeline.

    Steps:
    - Prompts the user to select an input image.
    - Extracts and reconstructs the Sudoku board using computer vision and OCR.
    - Allows manual correction of recognition errors.
    - Solves the board using a backtracking algorithm.
    - Saves a Markdown report and final solving trace for review.
    """

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
    edited_board = copy.deepcopy(parsed_board)

    # Create copies of the user-corrected board
    logic_board = copy.deepcopy(edited_board)

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

        # Save only final cell assignments (not all trial steps)
        trace_path = generate_trace_filename(IMAGE_PATH)
        os.makedirs("outputs", exist_ok=True)

        final_trace = []
        solved_board = logic_solver.get_board()

        for i in range(9):
            for j in range(9):
                if edited_board[i][j] == 0:
                    final_trace.append({
                        "row": i,
                        "col": j,
                        "value": solved_board[i][j]
                    })

        with open(trace_path, "w") as f:
            json.dump(final_trace, f, indent=2)

        logger.info(f"🧾 Final trace saved to: {trace_path}")

        # Restore and save captured console output to file
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        console_log_path = os.path.join("outputs", f"{os.path.splitext(os.path.basename(IMAGE_PATH))[0]}_console.log")
        with open(console_log_path, "w") as f:
            f.write(log_capture.getvalue())

        save_solution_report(
            input_board=input_board,
            parsed_board=input_board,
            edited_board=edited_board,
            solved_board=logic_solver.board,
            bckt_metrics={
                "method": "Backtracking",
                "solved": logic_success,
                "steps": logic_solver.steps,
                "duration": logic_solver.time_taken
            },
            image_path=IMAGE_PATH
        )

    else:
        logger.warning("⚠️ Logic Solver could not solve the puzzle.")
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    logger.removeHandler(capture_handler)

##################################################################################################
#                                               MAIN                                             #
##################################################################################################

if __name__ == "__main__":
    main()
