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

##################################################################################################
#                                SOLUTION REPORT GENERATION FUNCTION                             #
#                                                                                                #
# Generates a professional Markdown report comparing the solving performance of two methods:     #
# Backtracking and AI Agent. Also includes Sudoku boards at each step and full console log.      #
#                                                                                                #
# Args:                                                                                           #
#     input_board (list[list[int]]): Board selected by the user.                                 #
#     parsed_board (list[list[int]]): Board parsed from the image.                               #
#     edited_board (list[list[int]] | None): Board after user edition (if any).                  #
#     solved_board (list[list[int]]): Final solved board.                                        #
#     bckt_metrics (dict): Metrics for the backtracking solver.                                  #
#     ai_metrics (dict): Metrics for the AI Agent.                                               #
#     image_path (str): Path to the original input image.                                        #
##################################################################################################

def save_solution_report(input_board, parsed_board, edited_board, solved_board, bckt_metrics, ai_metrics, image_path):

    os.makedirs("outputs", exist_ok=True)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    report_name = f"{base_name}_solution.md"
    report_path = os.path.join("outputs", report_name)

    # Copy and rename image to outputs/ so it can be rendered in markdown
    image_ext = os.path.splitext(image_path)[1]
    image_filename = f"{base_name}_readme{image_ext}"
    local_img_path = os.path.join("outputs", image_filename)
    shutil.copy(image_path, local_img_path)

    '''
    def format_board_table(board):
        rows = []
        for i, row in enumerate(board):
            if i > 0 and i % 3 == 0:
                rows.append("|   |   |   |   |   |   |   |   |   |   |   |   |")
            formatted_row = []
            for j, val in enumerate(row):
                if j > 0 and j % 3 == 0:
                    formatted_row.append(" ")
                formatted_row.append(str(val) if val != 0 else " ")
            row_line = "| " + " | ".join(formatted_row) + " |"
            rows.append(row_line)
        header = rows[0]
        num_cols = header.count('|') - 1
        separator = "|" + "---|" * num_cols
        return "\n".join([header, separator] + rows[1:])

    
    def format_board_table(board):
        rows = []
        for i, row in enumerate(board):
            formatted_row = []
            for j, val in enumerate(row):
                if j > 0 and j % 3 == 0:
                    formatted_row.append("|")
                formatted_row.append(str(val) if val != 0 else " ")
            row_line = "| " + " | ".join(formatted_row) + " |"
            rows.append(row_line)
            if (i + 1) % 3 == 0 and i != 8:
                sep_row = []
                for j in range(len(formatted_row)):
                    if (j + 1) % 4 == 0:
                        sep_row.append("+")
                    else:
                        sep_row.append("-")
                rows.append("| " + " | ".join(sep_row) + " |")

        header = rows[0]
        num_cols = header.count('|') - 1
        separator = "|" + "---|" * num_cols
        return "\n".join([header, separator] + rows[1:])
    '''
    def format_board_table(board):
        rows = []
        for i, row in enumerate(board):
            formatted_row = []
            for j, val in enumerate(row):
                if j > 0 and j % 3 == 0:
                    formatted_row.append("ll")
                formatted_row.append(str(val) if val != 0 else " ")
            row_line = "| " + " | ".join(formatted_row) + " |"
            rows.append(row_line)
            if (i + 1) % 3 == 0 and i != 8:
                sep_row = []
                for j in range(len(formatted_row)):
                    if (j + 1) % 4 == 0:
                        sep_row.append("+")
                    else:
                        sep_row.append("=")
                rows.append("| " + " | ".join(sep_row) + " |")

        header = rows[0]
        num_cols = header.count('|') - 1
        separator = "|" + "---|" * num_cols
        return "\n".join([header, separator] + rows[1:])

    def compare_boards(board1, board2):
        return board2 is not None and board1 != board2

    edited = compare_boards(parsed_board, edited_board)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append(f"# Sudoku Solver Report\n")
    lines.append(f"**Solved at:** {timestamp}\n")
    lines.append(f"## Input Image\n")
    lines.append(f"![Sudoku Input]({image_filename})\n")
    lines.append("---\n")

    #lines.append("## Input Board (Selected by User)\n")
    #lines.append(format_board_table(input_board) + "\n")
    #lines.append("---\n")

    lines.append("## Parsed Board (Extracted from Image)\n")
    lines.append(format_board_table(parsed_board) + "\n")
    lines.append("---\n")

    lines.append(f"## Edited Board (User Corrections Applied){' (Edited)' if edited else ' (No Edits)'}\n")
    lines.append(format_board_table(edited_board if edited_board else parsed_board) + "\n")
    lines.append("---\n")

    lines.append("## Final Solved Board\n")
    lines.append(format_board_table(solved_board) + "\n")
    lines.append("---\n")

    lines.append("## Comparative Performance Table\n")
    lines.append("| Method       | Solved | Steps | Time (s) |")
    lines.append("|--------------|--------|-------|----------|")
    lines.append(f"| Backtracking | {'Yes' if bckt_metrics['solved'] else 'No'} | {bckt_metrics['steps']} | {bckt_metrics['duration']:.4f} |")
    lines.append(f"| AI Agent     | {'Yes' if ai_metrics['solved'] else 'No'} | {ai_metrics['steps']} | {ai_metrics['duration']:.4f} |")
    lines.append("---\n")

    # Attempt to include console output if log file exists
    log_path = os.path.join("outputs", f"{base_name}_console.log")
    if os.path.exists(log_path):
        lines.append("## Full Console Log\n")
        with open(log_path, "r") as log_file:
            lines.append("```bash")
            lines.extend(log_file.readlines())
            lines.append("```")

    with open(report_path, "w") as f:
        f.write("\n".join(lines))

    logger.info(f"\n📁 Report saved to: {report_path}")