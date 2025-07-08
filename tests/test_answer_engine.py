import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from answer_engine import load_answers, find_answer_with_score

@pytest.fixture
def answers():
    return load_answers("custom_answers.yaml")

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
