import pytest
import httpx

from unittest.mock import patch, Mock

from backend.app.llm.service import LLMService


def test_successful_generation():

    service = LLMService()

    with patch(
        "backend.app.llm.service.httpx.post"
    ) as mock_post:

        # Simulate a successful Ollama response
        response = Mock()

        response.json.return_value = {
            "message": {
                "content": "CodePilot uses RAG."
            }
        }

        mock_post.return_value = response

        answer = service.generate("What is CodePilot?")

        assert answer == "CodePilot uses RAG."

        mock_post.assert_called_once()

        # Inspect the outgoing request
        payload = mock_post.call_args.kwargs["json"]

        assert payload["model"] == service.model
        assert payload["stream"] is False
        assert payload["messages"][1]["content"] == "What is CodePilot?"


def test_empty_prompt():

    service = LLMService()

    with patch(
        "backend.app.llm.service.httpx.post"
    ) as mock_post:

        with pytest.raises(ValueError):
            service.generate("   ")

        mock_post.assert_not_called()


def test_request_timeout():

    service = LLMService()

    with patch(
        "backend.app.llm.service.httpx.post"
    ) as mock_post:

        # Simulate a timeout
        mock_post.side_effect = httpx.TimeoutException(
            "Request timed out"
        )

        with pytest.raises(RuntimeError, match="timed out"):
            service.generate("Explain RAG")


def test_connection_error():

    service = LLMService()

    with patch(
        "backend.app.llm.service.httpx.post"
    ) as mock_post:

        # Simulate Ollama being unavailable
        mock_post.side_effect = httpx.ConnectError(
            "Connection refused"
        )

        with pytest.raises(RuntimeError, match="Cannot connect"):
            service.generate("Explain RAG")


def test_http_error():

    service = LLMService()

    with patch(
        "backend.app.llm.service.httpx.post"
    ) as mock_post:

        request = httpx.Request(
            "POST",
            "http://localhost:11434/api/chat"
        )

        response = httpx.Response(
            500,
            request=request
        )

        # Simulate an internal server error
        mock_post.return_value = response

        with pytest.raises(RuntimeError, match="request failed"):
            service.generate("Explain RAG")