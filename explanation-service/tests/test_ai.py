from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import httpx
import pytest
from fastapi import HTTPException
from openai import APIConnectionError
from pydantic import SecretStr, ValidationError

from app.api.routes.ai import create_ai_explanation
from app.core.config import settings
from app.main import app
from app.schemas.ai import AIRequest
from app.services.ai_connection import (
    AIConfigurationError,
    AIUnavailableError,
    explicar_texto,
)


def test_ai_route_registered():
    operation = app.openapi()['paths']['/v1/ai']['post']
    assert '200' in operation['responses']


def test_ai_route_success():
    with patch('app.api.routes.ai.explicar_texto', return_value='Explicação simples.') as service:
        result = create_ai_explanation(AIRequest(texto='  Texto jurídico  '))
    service.assert_called_once_with('Texto jurídico')
    assert result.model_dump() == {
        'success': True, 'data': {'explanation': 'Explicação simples.'},
    }


@pytest.mark.parametrize('texto', ['', '   ', 'a' * 10001])
def test_ai_rejects_invalid_text(texto):
    with pytest.raises(ValidationError):
        AIRequest(texto=texto)


@pytest.mark.parametrize('error,status', [
    (AIConfigurationError('secret'), 503),
    (AIUnavailableError('secret'), 502),
])
def test_route_hides_provider_errors(error, status):
    with patch('app.api.routes.ai.explicar_texto', side_effect=error):
        with pytest.raises(HTTPException) as caught:
            create_ai_explanation(AIRequest(texto='Texto jurídico'))
    assert caught.value.status_code == status
    assert 'secret' not in caught.value.detail


def test_missing_key_does_not_create_client(monkeypatch):
    monkeypatch.setattr(settings, 'nvidia_api_key', SecretStr(''))
    with patch('app.services.ai_connection.OpenAI') as client:
        with pytest.raises(AIConfigurationError):
            explicar_texto('Texto')
    client.assert_not_called()


def test_service_calls_provider(monkeypatch):
    monkeypatch.setattr(settings, 'nvidia_api_key', SecretStr('test-key'))
    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=' Resposta '))],
    )
    with patch('app.services.ai_connection.OpenAI') as factory:
        factory.return_value.__enter__.return_value = client
        assert explicar_texto('Texto') == 'Resposta'
    payload = client.chat.completions.create.call_args.kwargs
    assert payload['model'] == settings.nvidia_model
    assert 'Texto' in payload['messages'][1]['content']


@pytest.mark.parametrize('choices', [[], [SimpleNamespace(message=SimpleNamespace(content=None))]])
def test_service_rejects_empty_response(monkeypatch, choices):
    monkeypatch.setattr(settings, 'nvidia_api_key', SecretStr('test-key'))
    with patch('app.services.ai_connection.OpenAI') as factory:
        client = factory.return_value.__enter__.return_value
        client.chat.completions.create.return_value = SimpleNamespace(choices=choices)
        with pytest.raises(AIUnavailableError):
            explicar_texto('Texto')


def test_service_handles_connection_failure(monkeypatch):
    monkeypatch.setattr(settings, 'nvidia_api_key', SecretStr('test-key'))
    with patch('app.services.ai_connection.OpenAI') as factory:
        client = factory.return_value.__enter__.return_value
        client.chat.completions.create.side_effect = APIConnectionError(
            request=httpx.Request('POST', 'https://example.com'),
        )
        with pytest.raises(AIUnavailableError):
            explicar_texto('Texto')
