##################################################################################################
#                                        FASTAPI ENTRYPOINT                                      #
#                                                                                                #
# This FastAPI application exposes a single endpoint to upload Sudoku readme_images, solve puzzles,     #
# and return the parsed and solved board with solver metrics.                                    #
#                                                                                                #
# Endpoints:                                                                                     #
#   - /healthcheck (GET): Simple status check.                                                   #
#   - /solve (POST): Upload a Sudoku image and get the solved board.                             #
#                                                                                                #
# The solution is generated using a logic-based backtracking algorithm.                          #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import shutil
import os
import uuid
import json

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from vision.image_parser import extract_board_from_image
from solver.bckt_logic_solver import SudokuSolver

from utils.logs_config import logger
from utils.reporter import save_solution_report, generate_trace_filename

##################################################################################################
#                                     FASTAPI INITIALIZATION                                     #
##################################################################################################

app = FastAPI(
    title="AISudokuSolver API",
    description=(
        "A pipeline to solve Sudoku puzzles from readme_images, using computer vision for digit extraction, "
        "a backtracking algorithm for solving, and LLMs for analytical summaries. "
        "This API supports seamless integration for automatic puzzle solving and report generation."
    ),
    version="1.0.0"
)

##################################################################################################
#                                           ENDPOINTS                                            #
##################################################################################################

@app.get("/healthcheck")
def healthcheck():
    """
    Health check endpoint to verify that the server is running.
    """
    return {"status": "ok"}


@app.post("/solve")
async def solve_sudoku(image: UploadFile = File(...)):
    """
    Upload a Sudoku image, extract the board, solve it, and return the result.

    Args:
        image (UploadFile): Uploaded Sudoku image (JPG/PNG).

    Returns:
        JSON containing the parsed and solved board, steps taken, and duration.
    """
    if not image.filename.endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Only JPG/PNG readme_images are supported")

    # Save the uploaded file temporarily
    temp_filename = f"temp_{uuid.uuid4()}.png"
    with open(temp_filename, "wb") as f:
        shutil.copyfileobj(image.file, f)

    try:
        # Step 1: Parse board from image
        parsed_board = extract_board_from_image(temp_filename)
        if not isinstance(parsed_board, list) or len(parsed_board) != 9:
            raise ValueError("Board extraction failed")

        # Step 2: Solve using logic
        solver = SudokuSolver(parsed_board)
        success = solver.solve()

        if not success:
            return JSONResponse(status_code=422, content={"detail": "Could not solve the puzzle"})

        # Step 3: Save trace and report
        solved_board = solver.get_board()
        trace_path = generate_trace_filename(temp_filename)

        final_trace = [
            {"row": i, "col": j, "value": solved_board[i][j]}
            for i in range(9)
            for j in range(9)
            if parsed_board[i][j] == 0
        ]

        with open(trace_path, "w") as f:
            json.dump(final_trace, f, indent=2)

        save_solution_report(
            input_board=parsed_board,
            solved_board=solved_board,
            bckt_metrics={
                "method": "Backtracking",
                "solved": success,
                "steps": solver.steps,
                "duration": solver.time_taken
            },
            image_path=temp_filename
        )

        return {
            "parsed_board": parsed_board,
            "solved_board": solved_board,
            "steps": solver.steps,
            "duration": solver.time_taken,
        }

    except Exception as e:
        logger.exception("❌ Failed to solve puzzle.")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)