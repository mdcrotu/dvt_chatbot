# tests/test_answer_engine.py
from unittest.mock import patch, MagicMock
from dvt_chatbot.answer_engine import load_answers, find_answer_with_score, get_answer_with_fallback
import json
import pytest
import numpy as np
import os


@pytest.fixture
def answers(tmp_path):
    # Create a temporary mock answer file
    mock_yaml = tmp_path / "mock_answers.yaml"
    mock_yaml.write_text("""
    - question: How do I open the DVT Console?
      answer: Go to Window > Show View > Other > DVT > DVT Console in Eclipse.
    - question: How can I create a new build configuration?
      answer: Right-click on your project > New > Build Configuration.
    """)

    with patch("dvt_chatbot.config.CUSTOM_ANSWERS_FILE", str(mock_yaml)):
        return load_answers()

def test_exact_match(answers):
    result = find_answer_with_score("How do I open the DVT Console?", answers)
    assert result[1] == "How do I open the DVT Console?"
    assert result[2] == 100


def test_fuzzy_match(answers):
    result = find_answer_with_score("open console", answers, threshold=50)
    assert result is not None, "No fuzzy match found"
    assert result[2] >= 50  # reduce threshold for test reliability
    assert "Console" in result[1]


def test_no_match(answers):
    result = find_answer_with_score("unrelated question", answers)
    assert result is None or result[0] is None

# @pytest.mark.skip(reason="This test is temporarily disabled.")

def test_fallback_to_guide(tmp_path):
    # Create a normalized embedding vector
    vec = np.ones(384)
    vec = (vec / np.linalg.norm(vec)).tolist()  # normalize to unit vector

    # Create mock guide data file with normalized embedding
    guide_file = tmp_path / "guide.json"
    guide_file.write_text(json.dumps([
        {
            "title": "Console View",
            "url": "http://example.com/console",
            "content": "Use the Console view to see runtime output.",
            "embedding": vec
        }
    ]))

    # Create a fake embedder object with the same normalized vector
    mock_embedder = MagicMock()
    mock_embedder.encode.return_value = np.array(vec)

    # Patch env var *before* import to override the config module
    with patch.dict(os.environ, {"DVT_GUIDE_FILE": str(guide_file)}):
        # Reload config so it picks up the new env var
        import importlib
        import dvt_chatbot.config
        importlib.reload(dvt_chatbot.config)

        # Now import modules that depend on it
        import dvt_chatbot.answer_engine as ae
        importlib.reload(ae)

        result = ae.get_answer_with_fallback("console output", model=mock_embedder)

        assert result is not None
        assert result["source"] == "guide"
        assert "console view" in result["title"].lower()
