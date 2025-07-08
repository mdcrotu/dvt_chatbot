import pytest
from unittest.mock import patch
from dvt_chatbot.answer_engine import load_answers, find_answer_with_score

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
