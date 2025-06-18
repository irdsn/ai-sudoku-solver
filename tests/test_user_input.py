import pytest
import sys
from unittest.mock import patch
from utils.user_input import prompt_user_for_image


def test_prompt_user_returns_valid_path():
    with patch("utils.user_input.filedialog.askopenfilename") as mock_dialog, \
            patch("utils.user_input.os.path.exists") as mock_exists:
        mock_dialog.return_value = "/fake/path/image.png"
        mock_exists.return_value = True

        result = prompt_user_for_image()
        assert result == "/fake/path/image.png"


def test_prompt_user_no_selection_exits():
    with patch("utils.user_input.filedialog.askopenfilename", return_value=""), \
            patch("utils.user_input.os.path.exists") as mock_exists, \
            patch("utils.user_input.sys.exit") as mock_exit:
        mock_exists.return_value = True
        prompt_user_for_image()
        mock_exit.assert_called_once_with(1)


def test_prompt_user_file_does_not_exist_exits():
    with patch("utils.user_input.filedialog.askopenfilename", return_value="/fake/path/image.png"), \
            patch("utils.user_input.os.path.exists", return_value=False), \
            patch("utils.user_input.sys.exit") as mock_exit:
        prompt_user_for_image()
        mock_exit.assert_called_once_with(1)
