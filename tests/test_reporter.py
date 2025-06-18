import json
from pathlib import Path
from unittest.mock import patch
from utils.reporter import save_solution_report
from utils.config import OUTPUT_DIR

def test_save_solution_report_creates_markdown(tmp_path):
    # Simulate 9x9 boards: parsed, edited and solved
    parsed_board = [[5, 3, 0, 0, 7, 0, 0, 0, 0]] * 9
    edited_board = [[5, 3, 4, 6, 7, 8, 9, 1, 2]] * 9
    solved_board = [[5, 3, 4, 6, 7, 8, 9, 1, 2]] * 9
    input_board = parsed_board

    # Fake solving metrics
    bckt_metrics = {
        "solved": True,
        "steps": 42,
        "duration": 1.2345
    }

    # Create dummy input image
    dummy_image = tmp_path / "sudoku_input.png"
    dummy_image.write_bytes(b"fake image content")

    # Create expected trace file in outputs/ (as required by reporter logic)
    base_name = dummy_image.stem
    trace_path = Path("outputs") / f"{base_name}_solution_trace.json"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_path, "w") as f:
        json.dump({"0_0": {"value": 5, "step": 1, "action": "place"}}, f)

    # Patch OpenAI call and image copying
    with patch("utils.reporter.generate_summary_from_trace") as mock_summary, \
         patch("utils.reporter.shutil.copy") as mock_copy:

        mock_summary.return_value = "LLM summary for the Sudoku puzzle."
        mock_copy.return_value = None

        # Create dummy console log file expected by reporter
        log_path = Path("outputs") / f"{base_name}_console.log"
        log_path.write_text("Log line 1\nLog line 2")

        # Call the reporting function
        save_solution_report(
            input_board=input_board,
            solved_board=solved_board,
            bckt_metrics=bckt_metrics,
            image_path=str(dummy_image)
        )

        # Assert that the report file was created correctly
        report_path = OUTPUT_DIR / f"{base_name}_REPORT.md"
        assert report_path.exists()

        # Validate basic contents of the Markdown report
        with open(report_path, "r") as f:
            content = f.read()
            assert "# Sudoku Solver Report" in content
            assert "LLM summary" in content
            assert "Final Solved Board" in content
