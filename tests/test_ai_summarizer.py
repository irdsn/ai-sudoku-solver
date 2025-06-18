import json
import tempfile
from unittest.mock import patch
from utils.ai_summarizer import generate_summary_from_trace


def test_generate_summary_from_trace_success():
    # Simulate minimal trace
    dummy_trace = {
        "0_0": {"value": 5, "step": 1, "action": "place"},
        "0_1": {"value": 3, "step": 2, "action": "place"},
        "1_1": {"value": 7, "step": 3, "action": "place"}
    }

    # Create temporary file with the dummy trace
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        json.dump(dummy_trace, tmp)
        tmp_path = tmp.name

    # Mock OpenAI's response
    fake_response = "The puzzle was solved using constraint-based reasoning in under 3 seconds."

    with patch("utils.ai_summarizer.client.chat.completions.create") as mock_openai:
        mock_openai.return_value.choices = [
            type("Choice", (object,), {"message": type("Msg", (object,), {"content": fake_response})()})
        ]

        summary = generate_summary_from_trace(tmp_path, steps=42, duration=2.89)

        assert fake_response in summary
        assert "constraint-based" in summary.lower()

def test_generate_summary_trace_file_not_found():
    # Provide a path to a non-existent trace file
    summary = generate_summary_from_trace("nonexistent_trace.json", steps=10, duration=1.0)

    # Expect a clear error message about file reading
    assert "Failed to read trace file" in summary


def test_generate_summary_llm_failure(tmp_path):
    # Create a valid trace file
    trace_path = tmp_path / "trace.json"
    trace_path.write_text(json.dumps({
        "0_0": {"value": 1, "step": 1, "action": "place"}
    }))

    # Patch the LLM call to simulate an exception
    with patch("utils.ai_summarizer.client.chat.completions.create", side_effect=Exception("Simulated failure")):
        summary = generate_summary_from_trace(str(trace_path), steps=5, duration=0.5)

        assert "LLM call failed" in summary
