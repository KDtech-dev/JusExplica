import re
import unicodedata

from app.schemas.explanation import ExplanationData, MovementInput


LIMITATION = (
    "Esta explicação é informativa e considera apenas a descrição "
    "da movimentação recebida. Consulte o processo ou um profissional "
    "do Direito para confirmar o significado no contexto do caso."
)


UNKNOWN_EXPLANATION = (
    "Ainda não consigo explicar esta movimentação com segurança "
    "a partir das regras disponíveis. Consulte a descrição completa "
    "no sistema do tribunal para obter mais informações."
)


# Cada regra contém as expressões que podem identificar uma movimentação
# e a explicação correspondente.
RULES = [
    {
        "name": "expedicao_mandado",
        "phrases": (
            "expedicao de mandado",
            "mandado expedido",
        ),
        "explanation": (
            "O registro indica que foi emitido um mandado, documento "
            "utilizado para formalizar uma ordem ou providência judicial. "
            "O que deve ser realizado depende do conteúdo do documento."
        ),
    },
    {
        "name": "juntada_peticao",
        "phrases": (
            "juntada de peticao",
            "peticao juntada",
        ),
        "explanation": (
            "Uma petição foi anexada aos autos do processo. Ela pode conter "
            "um pedido, uma manifestação ou outras informações apresentadas "
            "por uma das partes ou por seu representante."
        ),
    },
    {
        "name": "conclusos_decisao",
        "phrases": (
            "conclusos para decisao",
            "concluso para decisao",
            "autos conclusos",
        ),
        "explanation": (
            "O processo foi encaminhado para análise judicial. "
            "Esse registro, por si só, não informa qual será o resultado "
            "nem quando uma decisão será tomada."
        ),
    },
    {
        "name": "citacao",
        "phrases": (
            "citacao",
            "citado para",
            "citada para",
        ),
        "explanation": (
            "O registro está relacionado à citação, ato pelo qual uma pessoa "
            "é formalmente chamada para tomar conhecimento de um processo "
            "e, quando cabível, apresentar sua defesa."
        ),
    },
    {
        "name": "intimacao",
        "phrases": (
            "intimacao",
            "intimado para",
            "intimada para",
        ),
        "explanation": (
            "O registro indica uma intimação, utilizada para comunicar "
            "uma pessoa sobre um ato ou informação do processo. O conteúdo "
            "da comunicação determina o que precisa ser observado."
        ),
    },
    {
        "name": "audiencia_designada",
        "phrases": (
            "audiencia designada",
            "designada audiencia",
            "audiencia marcada",
        ),
        "explanation": (
            "Foi registrada a designação de uma audiência. Para saber "
            "a data, o horário, a finalidade e quem deve comparecer, "
            "é necessário consultar os detalhes do processo."
        ),
    },
    {
        "name": "sentenca",
        "phrases": (
            "sentenca proferida",
            "sentenca publicada",
            "sentenca registrada",
        ),
        "explanation": (
            "O registro indica que há uma sentença associada ao processo. "
            "Para compreender o resultado, seus efeitos e eventuais "
            "providências, é necessário consultar o conteúdo da sentença."
        ),
    },
    {
        "name": "certidao",
        "phrases": (
            "certidao expedida",
            "expedida certidao",
            "certidao juntada",
            "certidao emitida",
        ),
        "explanation": (
            "O registro está relacionado a uma certidão, documento que "
            "formaliza uma informação ou ocorrência processual. O conteúdo "
            "da certidão esclarece qual fato foi registrado."
        ),
    },
]


def normalize_text(value: str) -> str:
    """
    Padroniza o texto para facilitar a comparação de expressões.

    Exemplo:
        '  CONCLUSOS para DECISÃO  '
        -> 'conclusos para decisao'
    """
    normalized = unicodedata.normalize("NFKD", value.casefold())

    without_accents = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )

    # Trata pontuação e espaços consecutivos.
    normalized_spaces = re.sub(
        r"[^\w]+",
        " ",
        without_accents,
    )

    return " ".join(normalized_spaces.split())


def classify_movement(description: str) -> dict | None:
    """
    Identifica uma categoria usando expressões conhecidas.

    Retorna a regra identificada ou None quando não encontra
    uma correspondência.
    """
    normalized_description = normalize_text(description)

    for rule in RULES:
        for phrase in rule["phrases"]:
            normalized_phrase = normalize_text(phrase)

            # A expressão precisa corresponder a palavras completas.
            pattern = (
                rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)"
            )

            if re.search(pattern, normalized_description):
                return rule

    return None


def explain_movement(movement: MovementInput) -> ExplanationData:
   
    rule = classify_movement(movement.description)

    if rule is None:
        return ExplanationData(
            explanation=UNKNOWN_EXPLANATION,
            limitations=[
                "Movimentação não reconhecida pelas regras atuais.",
                LIMITATION,
            ],
        )

    return ExplanationData(
        explanation=rule["explanation"],
        limitations=[LIMITATION],
    )