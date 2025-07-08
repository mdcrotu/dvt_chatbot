import pytest
from unittest.mock import patch
from dvt_chatbot.app import app as flask_app
import tempfile

@pytest.fixture
def client(tmp_path):
    # Create a mock answers file
    mock_yaml = tmp_path / "mock_answers.yaml"
    mock_yaml.write_text("""
    - question: How do I open the DVT Console?
      answer: Go to Window > Show View > Other > DVT > DVT Console in Eclipse.
    """)

    # Patch config before initializing test client
    with patch("dvt_chatbot.config.CUSTOM_ANSWERS_FILE", str(mock_yaml)):
        flask_app.config["TESTING"] = True
        with flask_app.test_client() as client:
            yield client

def test_web_exact_match(client):
    response = client.post("/", data={"question": "How do I open the DVT Console?"})
    assert b"DVT Console" in response.data

def test_web_fallback_message(client):
    response = client.post("/", data={"question": "gibberishxyz"})
    text = response.data.decode("utf-8")
    assert "Sorry, I don’t know yet." in text
