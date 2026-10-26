import unicodedata

from app.schemas.explanation import ExplanationData, MovementInput


LIMITATION = (
    "Esta explicação é informativa e considera apenas a descrição "
    "da movimentação recebida. Consulte o processo ou um profissional "
    "do Direito para confirmar o significado no contexto do caso."
)


RULES = [
    (
        ("expedicao de mandado",),
        (
            "O registro indica que foi emitido um mandado, documento "
            "utilizado para formalizar uma ordem ou providência judicial. "
            "O que deve ser realizado depende do conteúdo do documento."
        ),
    ),
    (
        ("juntada de peticao", "juntada de petição"),
        (
            "Uma petição foi anexada aos autos do processo. Ela pode conter "
            "um pedido, uma manifestação ou outras informações apresentadas "
            "por uma das partes ou por seu representante."
        ),
    ),
    (
        ("conclusos para decisao", "conclusos para decisão"),
        (
            "O processo foi encaminhado ao responsável pela análise judicial "
            "para apreciação ou decisão. Esse registro, por si só, não "
            "informa qual será o resultado."
        ),
    ),
    (
        ("citacao", "citação"),
        (
            "O registro está relacionado à citação, ato pelo qual uma pessoa "
            "é formalmente chamada para tomar conhecimento de um processo "
            "e, quando cabível, apresentar sua defesa."
        ),
    ),
    (
        ("intimacao", "intimação"),
        (
            "O registro indica uma intimação, utilizada para comunicar "
            "uma pessoa sobre um ato ou informação do processo. O conteúdo "
            "da comunicação determina o que precisa ser observado."
        ),
    ),
    (
        ("audiencia designada", "audiência designada"),
        (
            "Foi registrada a designação de uma audiência. Para saber "
            "a data, o horário, a finalidade e quem deve comparecer, "
            "é necessário consultar os detalhes do processo."
        ),
    ),
    (
        ("sentenca", "sentença"),
        (
            "O registro menciona uma sentença, decisão judicial que resolve "
            "determinadas questões do processo. Para compreender o resultado, "
            "é necessário consultar o conteúdo da sentença."
        ),
    ),
    (
        ("certidao", "certidão"),
        (
            "O registro está relacionado a uma certidão, documento que "
            "formaliza uma informação ou ocorrência processual. O conteúdo "
            "da certidão esclarece qual fato foi registrado."
        ),
    ),
]


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())

    return "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )


def explain_movement(movement: MovementInput) -> ExplanationData:
    description = normalize_text(movement.description)

    for keywords, explanation in RULES:
        if any(normalize_text(keyword) in description for keyword in keywords):
            return ExplanationData(
                explanation=explanation,
                limitations=[LIMITATION],
            )

    return ExplanationData(
        explanation=(
            "Ainda não consigo explicar esta movimentação com segurança "
            "a partir das regras disponíveis. Consulte a descrição completa "
            "no sistema do tribunal para obter mais informações."
        ),
        limitations=[
            "Movimentação não reconhecida pelas regras atuais.",
            LIMITATION,
        ],
    )