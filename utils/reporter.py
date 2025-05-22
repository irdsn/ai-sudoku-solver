##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module generates a detailed Markdown report summarizing the Sudoku solving process.       #
# The report includes:                                                                           #
#   - Timestamp of execution                                                                     #
#   - Embedded input image (copied locally)                                                      #
#   - The original 9x9 board extracted from the image                                            #
#   - The solved 9x9 board after applying the solver                                             #
#   - A comparative performance table between solvers                                            #
#   - Full console output log at the end                                                         #
#                                                                                                #
# Output is saved under `outputs/` using the image's filename as base.                           #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import shutil
from datetime import datetime
from utils.logs_config import logger
from utils.ai_summarizer import generate_summary_from_trace

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def save_solution_report(input_board, parsed_board, edited_board, solved_board, bckt_metrics, image_path):
    """
    Generates a Markdown report summarizing the Sudoku solving process.

    The report includes:
    - A timestamp of when the solution was generated.
    - The original image used as input.
    - The parsed, optionally edited, and solved boards in table format.
    - A natural language summary of the solving strategy and performance.
    - A performance table showing steps taken and execution time.

    Args:
        input_board (list[list[int]]): Initial user-selected board.
        parsed_board (list[list[int]]): Board parsed automatically from the image.
        edited_board (list[list[int]]): Optionally edited version of the parsed board.
        solved_board (list[list[int]]): Final solved board.
        bckt_metrics (dict): Dictionary with backtracking performance data.
        image_path (str): Path to the input image used for board extraction.

    Output:
        Saves a Markdown file in `outputs/` describing the entire solving pipeline.
    """

    os.makedirs("outputs", exist_ok=True)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    report_name = f"{base_name}_REPORT.md"
    report_path = os.path.join("outputs", report_name)

    # Copy and rename image to outputs/ so it can be rendered in markdown
    image_ext = os.path.splitext(image_path)[1]
    image_filename = f"{base_name}_markdown{image_ext}"
    local_img_path = os.path.join("outputs", image_filename)
    shutil.copy(image_path, local_img_path)

    def format_board_table(board):
        """
        Formats a 9x9 Sudoku board as a Markdown table for visual display in the report.
        """

        rows = []
        for i, row in enumerate(board):
            formatted_row = []

            for j, val in enumerate(row):
                '''if j > 0 and j % 3 == 0:
                    formatted_row.append("ll")'''
                formatted_row.append(str(val) if val != 0 else " ")
            row_line = "| " + " | ".join(formatted_row) + " |"
            rows.append(row_line)
            '''if (i + 1) % 3 == 0 and i != 8:
                sep_row = []
                for j in range(len(formatted_row)):
                    if (j + 1) % 4 == 0:
                        sep_row.append("+")
                    else:
                        sep_row.append("=")
                rows.append("| " + " | ".join(sep_row) + " |")'''

        header = rows[0]
        num_cols = header.count('|') - 1
        separator = "|" + "---|" * num_cols
        return "\n".join([header, separator] + rows[1:])

    def compare_boards(board1, board2):
        """
        Compares two boards and returns True if they differ.
        """

        return board2 is not None and board1 != board2

    edited = compare_boards(parsed_board, edited_board)


    summary = generate_summary_from_trace(
        trace_path=os.path.join("outputs", f"{base_name}_solution_trace.json"),
        steps=bckt_metrics["steps"],
        duration=bckt_metrics["duration"]
    )

    lines = []
    lines.append(f"# Sudoku Solver Report\n")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"**Solved at:** {timestamp}\n")

    lines.append("---\n")

    lines.append("## Solution Overview\n")
    lines.append(summary + "\n")

    lines.append("---\n")

    lines.append(f"## Input Image\n")
    lines.append("Original image used to extract the Sudoku board.\n")
    #lines.append(f"![Sudoku Input]({image_filename})\n") # Original
    lines.append(f'<img src="{image_filename}" alt="Sudoku Input" width="400"/>\n') # Resized

    lines.append("---\n")

    #lines.append("## Input Board (Selected by User)\n")
    #lines.append(format_board_table(input_board) + "\n")

    #lines.append("---\n")

    lines.append("## Parsed Board (Extracted from Image)\n")
    lines.append("Board generated automatically via OCR and grid detection.\n")
    lines.append(format_board_table(parsed_board) + "\n")

    lines.append("---\n")

    lines.append(f"## Edited Board {' (Edited)' if edited else ' (No Edits)'}\n")
    lines.append("Board after optional manual correction of digit recognition errors.\n")
    lines.append(format_board_table(edited_board if edited_board else parsed_board) + "\n")

    lines.append("---\n")

    lines.append("## Final Solved Board (Backtracking)\n")
    lines.append("Completed Sudoku board after applying the backtracking algorithm.\n")
    lines.append(format_board_table(solved_board) + "\n")

    lines.append("---\n")

    lines.append("## Backtracking Performance\n")
    lines.append("Summary of solver performance, including total steps and execution time.\n")
    lines.append("| Solved | Steps | Time (s) |")
    lines.append("|--------|-------|----------|")
    lines.append(f"| {'Yes' if bckt_metrics['solved'] else 'No'} | {bckt_metrics['steps']} | {bckt_metrics['duration']:.4f} |")

    '''
    lines.append("---\n")

    # Attempt to include console output if log file exists
    log_path = os.path.join("outputs", f"{base_name}_console.log")
    if os.path.exists(log_path):
        lines.append("## Full Console Log\n")
        with open(log_path, "r") as log_file:
            lines.append("```bash")
            lines.extend(log_file.readlines())
            lines.append("```")
    '''

    with open(report_path, "w") as f:
        f.write("\n".join(lines))

    logger.info(f"\n📁 Report saved to: {report_path}")

def generate_trace_filename(image_path: str) -> str:
    """
    Creates a standard filename for saving the solution trace of a Sudoku image.

    Args:
        image_path (str): Path to the original input image.

    Returns:
        str: Full path to the corresponding JSON file in the outputs directory.
    """

    base = os.path.splitext(os.path.basename(image_path))[0]
    return os.path.join("outputs", f"{base}_solution_trace.json")