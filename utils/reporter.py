##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This module generates a detailed Markdown report summarizing the Sudoku solving process.       #
# The report includes:                                                                           #
#   - Timestamp of execution                                                                     #
#   - Embedded input image (if available)                                                        #
#   - The original 9x9 board extracted from the image                                            #
#   - The solved 9x9 board after applying the solver                                             #
#                                                                                                #
# Output is saved under `outputs/` using the image's filename as base.                           #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
from datetime import datetime
from utils.logs_config import logger

##################################################################################################
#                                   REPORT GENERATION FUNCTION                                   #
#                                                                                                #
# Generates a Markdown report summarizing the Sudoku solving process.                            #
# The report includes both the original and solved 9x9 boards in Markdown table format, along    #
# with a timestamp and reference to the source image used.                                       #
#                                                                                                #
# Args:                                                                                          #
#     original_board (list[list[int]]): 9x9 board extracted from the image (0 = empty).          #
#     solved_board (list[list[int]]): Completed 9x9 board after solving.                         #
#     image_path (str): Path to the input Sudoku image (used to derive output filename).         #
##################################################################################################

def save_solution_report(original_board, solved_board, image_path):

    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)

    # Build filename based on original image
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    report_name = f"{base_name}_solution.md"
    report_path = os.path.join("outputs", report_name)
    relative_img_path = os.path.relpath(image_path, start=os.path.dirname(report_path))

    # Format a Sudoku board as a 9x9 grid-style Markdown table.
    def format_board_grid(board):

        lines = []
        for i, row in enumerate(board):
            row_str = "| " + " | ".join(str(val) if val != 0 else " " for val in row) + " |"
            lines.append(row_str)
            if i == 0:
                lines.insert(1, "|---" * 9 + "|")  # Header separator once
        return "\n".join(lines)

    # Generate report content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""# Sudoku Solver Report

    **Solved at:**: {timestamp}

    ### Input Image
    ![Sudoku Input]({relative_img_path})

    ---

    ### Original Board

    {format_board_grid(original_board)}

    ---

    ### Solved Board

    {format_board_grid(solved_board)}
    """

    # Write to file
    with open(report_path, "w") as f:
        f.write(content)

    logger.info(f"\n📁 Report saved to: {report_path}")
