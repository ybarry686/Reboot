import requests
from unittest.mock import Mock, patch
from services.gemini_client import get_recommendation, FALLBACK_MESSAGE
from config import Config


def test_no_api_key(monkeypatch):
    monkeypatch.setattr(Config, "GEMINI_API_KEY", "")
    result = get_recommendation("Sore muscles", [{"name": "Restore", "services": []}])
    assert result == FALLBACK_MESSAGE


def test_no_studios(monkeypatch):
    monkeypatch.setattr(Config, "GEMINI_API_KEY", "fake_key")
    result = get_recommendation("Back pain", [])
    assert result == "No studios matched yet"

@patch("gemini_client.requests.post")
def test_successful_response(mock_post, monkeypatch):
    monkeypatch.setattr(Config, "GEMINI_API_KEY", "fake_key")

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": "Restore is the best option"}
                    ]
                }
            }
        ]
    }
    mock_post.return_value = mock_response

    result = get_recommendation(
        "Leg soreness",
        [{"name": "Restore", "services": [{"name": "Saune"}]}]
    )

    assert result == "Restore is the best option"


@patch("gemini_client.requests.post")
def test_api_failure(mock_post, monkeypatch):
    monkeypatch.setattr(Config, "GEMINI_API_KEY", "fake_key")

    mock_post.side_effect = requests.RequestException

    result = get_recommendation(
        "Leg soreness",
        [{"name": "Restore", "services": []}]
    )

    assert result == FALLBACK_MESSAGE