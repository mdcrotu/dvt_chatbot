import builtins
from unittest.mock import patch, MagicMock
from dvt_chatbot import app


def test_cli_fallback(monkeypatch, capsys):
    # Simulate a console output question and fallback answer
    test_question = "console output"
    test_answer = {
        "answer": "Use the Console view to see runtime output.",
        "source": "guide",
        "score": 0.93,
        "title": "Console View",
        "url": "http://example.com/console"
    }

    inputs = iter([test_question, "exit"])  # simulate two inputs: question then exit

    with patch.object(builtins, "input", lambda _: next(inputs)), \
         patch("dvt_chatbot.answer_engine.get_answer_with_fallback", return_value=test_answer):

        app.main_cli()  # assumes you moved CLI logic into `main_cli()` function

        output = capsys.readouterr().out
        assert "Use the Console view to see runtime output." in output
        assert "Console View" in output
