from openai import APIError, OpenAI

from app.core.config import settings


class AIConfigurationError(Exception):
    """A integração com a IA não está configurada."""


class AIUnavailableError(Exception):
    """O provedor não retornou uma explicação válida."""


SYSTEM_PROMPT = """Você é um assistente especializado em
interpretar documentos jurídicos brasileiros.

Seu objetivo é transformar textos jurídicos
complexos em explicações simples e acessíveis.

Instruções:
- Utilize português brasileiro.
- Explique termos jurídicos desconhecidos.
- Preserve o significado original.
- Não invente informações.
- Destaque direitos, deveres e prazos.
- Explique as consequências práticas.
- Utilize exemplos quando necessário.
- Diferencie fatos do documento de interpretações.
- Caso faltem informações, deixe isso claro.
- a explicação deve ter no máximo 200 palavras, mas completa
"""


def explicar_texto(texto: str) -> str:
    if not settings.nvidia_api_key.get_secret_value().strip():
        raise AIConfigurationError("Configure NVIDIA_API_KEY no .env.")

    try:
        with OpenAI(
            base_url=settings.nvidia_base_url,
            api_key=settings.nvidia_api_key.get_secret_value(),
            timeout=45.0,
            max_retries=0,
        ) as client:
            completion = client.chat.completions.create(
                model=settings.nvidia_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Explique o seguinte texto:\n\n{texto}"},
                ],
                temperature=0.3,
                top_p=0.95,
                max_tokens=4096,
                extra_body={"chat_template_kwargs": {"enable_thinking": True}},
            )
    except APIError as exc:
        raise AIUnavailableError("Não foi possível consultar a IA.") from exc

    if not completion.choices:
        raise AIUnavailableError("A IA retornou uma resposta vazia.")

    answer = completion.choices[0].message.content
    if not isinstance(answer, str) or not answer.strip():
        raise AIUnavailableError("A IA retornou uma resposta vazia.")

    return answer.strip()
