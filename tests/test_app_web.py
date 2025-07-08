import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_web_exact_match(client):
    response = client.post("/", data={"question": "How do I open the DVT Console?"})
    assert b"DVT Console" in response.data

def test_web_fallback_message(client):
    response = client.post("/", data={"question": "gibberishxyz"})
    text = response.data.decode("utf-8")
    assert "Sorry, I don’t know yet." in text
