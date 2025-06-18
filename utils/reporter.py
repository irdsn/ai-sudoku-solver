##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module generates a detailed Markdown report summarizing the Sudoku solving process.       #
# The report includes:                                                                           #
#   - Timestamp of execution                                                                     #
#   - Embedded input image (copied locally)                                                      #
#   - The original 9x9 board extracted from the image                                            #
#   - The solved 9x9 board after applying the solver                                             #
#   - A summary of the solving process and performance metrics                                   #
#                                                                                                #
# Output is saved under `outputs/` using the image's filename as base.                           #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import shutil
from pathlib import Path
from datetime import datetime
from utils.logs_config import logger
from utils.ai_summarizer import generate_summary_from_trace
from utils.config import OUTPUT_DIR

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def save_solution_report(input_board, solved_board, bckt_metrics, image_path):
    """
    Generates a Markdown report summarizing the Sudoku solving process.

    Args:
        input_board (list[list[int]]): Board parsed automatically from the image.
        solved_board (list[list[int]]): Final solved board.
        bckt_metrics (dict): Dictionary with backtracking performance data.
        image_path (str): Path to the input image used for board extraction.

    Output:
        Saves a Markdown file in `outputs/` describing the entire solving pipeline.
    """

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    report_name = f"{base_name}_REPORT.md"
    report_path = str(OUTPUT_DIR / report_name)

    # Normalize and resolve absolute path
    image_path = Path(image_path).resolve()
    image_ext = image_path.suffix

    image_filename = f"{base_name}_input{image_ext}"
    local_img_path = OUTPUT_DIR / image_filename

    # Copy only if it's not already in OUTPUT_DIR with correct name
    if image_path != local_img_path.resolve():
        shutil.copy(image_path, local_img_path)

    def format_board_table(board):
        """
        Formats a 9x9 Sudoku board as a Markdown table for visual display in the report.
        """

        rows = []
        for i, row in enumerate(board):
            formatted_row = [str(val) if val != 0 else " " for val in row]
            row_line = "| " + " | ".join(formatted_row) + " |"
            rows.append(row_line)
        header = rows[0]
        num_cols = header.count('|') - 1
        separator = "|" + "---|" * num_cols
        return "\n".join([header, separator] + rows[1:])

    # Generate summary using solving trace
    summary = generate_summary_from_trace(
        trace_path=str(OUTPUT_DIR / f"{base_name}_solution_trace.json"),
        steps=bckt_metrics["steps"],
        duration=bckt_metrics["duration"]
    )

    lines = []
    lines.append(f"# Sudoku Solver Report\n")
    lines.append(f"**Solved at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")

    lines.append("## Solution Overview\n")
    lines.append(summary + "\n")
    lines.append("---\n")

    lines.append(f"## Input Image\n")
    lines.append("Original image used to extract the Sudoku board.\n")
    #lines.append(f"![Sudoku Input]({image_filename})\n") # Original
    lines.append(f'<img src="{image_filename}" alt="Sudoku Input" width="400"/>\n') # Resized
    lines.append("---\n")

    lines.append("## Parsed Board (Extracted from Image)\n")
    lines.append("Board generated automatically via OCR and grid detection.\n")
    lines.append(format_board_table(input_board) + "\n")

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

    with open(report_path, "w") as f:
        f.write("\n".join(lines))

    logger.info(f"\nReport saved to: {report_path}")

def generate_trace_filename(image_path: str) -> str:
    """
    Creates a standard filename for saving the solution trace of a Sudoku image.

    Args:
        image_path (str): Path to the original input image.

    Returns:
        str: Full path to the corresponding JSON file in the outputs directory.
    """
    base = os.path.splitext(os.path.basename(image_path))[0]
    return str(OUTPUT_DIR / f"{base}_solution_trace.json")
