import os
import pandas as pd
from collections import namedtuple
from openai import OpenAI, Moderation


ModerationInfo = namedtuple("ModerationInfo", "flagged reason scores")


def about() -> pd.DataFrame:
    return pd.DataFrame(
        data=[
            {
                "Categoria (Inglês)": "hate",
                "Categoria (Português)": "ódio",
                "Descrição": (
                    "Conteúdo que expressa, incita ou promove ódio com base em raça, gênero, etnia, "
                    "religião, nacionalidade, orientação sexual, status de deficiência ou casta."
                ),
            },
            {
                "Categoria (Inglês)": "hate/threatening",
                "Categoria (Português)": "ódio/ameaçador",
                "Descrição": (
                    "Conteúdo odioso que também inclui violência ou danos graves em relação ao grupo "
                    "alvo com base em raça, gênero, etnia, religião, nacionalidade, orientação sexual,"
                    "status de deficiência ou casta."
                ),
            },
            {
                "Categoria (Inglês)": "harassment",
                "Categoria (Português)": "assédio",
                "Descrição": (
                    "Conteúdo que expressa, incita ou promove linguagem de assédio contra qualquer"
                    " alvo."
                ),
            },
            {
                "Categoria (Inglês)": "harassment/threatening",
                "Categoria (Português)": "assédio/ameaçador",
                "Descrição": (
                    "Conteúdo de assédio que também inclui violência ou danos graves em relação"
                    "a qualquer alvo."
                ),
            },
            {
                "Categoria (Inglês)": "self-harm",
                "Categoria (Português)": "autoagressão",
                "Descrição": (
                    "Conteúdo que promove, encoraja ou descreve atos de autolesão, como suicídio,"
                    " cortes e distúrbios alimentares."
                ),
            },
            {
                "Categoria (Inglês)": "self-harm/intent",
                "Categoria (Português)": "autoagressão/intenção",
                "Descrição": (
                    "Conteúdo em que o autor expressa que está realizando ou pretende realizar atos"
                    " de autolesão, como suicídio, cortes e distúrbios alimentares."
                ),
            },
            {
                "Categoria (Inglês)": "self-harm/instructions",
                "Categoria (Português)": "autoagressão/instruções",
                "Descrição": (
                    "Conteúdo que incentiva a realização de atos de autolesão, como suicídio, cortes"
                    " e distúrbios alimentares, ou que dá instruções ou conselhos sobre como cometer"
                    " tais atos."
                ),
            },
            {
                "Categoria (Inglês)": "sexual",
                "Categoria (Português)": "sexual",
                "Descrição": (
                    "Conteúdo destinado a excitar sexualmente, como a descrição de atividades sexuais"
                    "ou que promove serviços sexuais (excluindo educação sexual e bem-estar)."
                ),
            },
            {
                "Categoria (Inglês)": "sexual/minors",
                "Categoria (Português)": "sexual/menores",
                "Descrição": "Conteúdo sexual que inclui um indivíduo menor de 18 anos.",
            },
            {
                "Categoria (Inglês)": "violence",
                "Categoria (Português)": "violência",
                "Descrição": "Conteúdo que retrata morte, violência ou lesões físicas.",
            },
            {
                "Categoria (Inglês)": "violence/graphic",
                "Categoria (Português)": "violência/gráfico",
                "Descrição": (
                    "Conteúdo que retrata morte, violência ou lesões físicas em detalhes gráficos."
                ),
            },
        ]
    )


def moderation(expression: str) -> ModerationInfo:
    flag_mapping = {
        "hate": "ódio",
        "hate/threatening": "ódio/ameaçador",
        "harassment": "assédio",
        "harassment/threatening": "assédio/ameaçador",
        "self-harm": "autoagressão",
        "self-harm/intent": "autoagressão/intenção",
        "self-harm/instructions": "autoagressão/instruções",
        "sexual": "sexual",
        "sexual/minors": "sexual/menores",
        "violence": "violência",
        "violence/graphic": "violência/gráfico",
    }
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response: Moderation = client.moderations.create(input=expression)
    flagged = response.results[0].flagged
    scores = None
    reason = str()

    if flagged:
        categories = response.results[0].categories.to_dict()
        scores = response.results[0].category_scores.to_dict()
        flagged_categories = [
            flag_mapping[key] for key, value in categories.items() if value
        ]

        if len(flagged_categories) == 0:
            rule = "Foi detectado o seguinte discurso de ódio"
        else:
            rule = "Foram detectados os seguintes discursos de ódio"

        if len(flagged_categories) > 1:
            flagged_categories = (
                ", ".join(flagged_categories[:-1]) + " e " + flagged_categories[-1]
            )
        else:
            flagged_categories = flagged_categories[0]

        reason = (
            "Lamento, mas a sua mensagem foi sinalizada como inapropriada, e por isso não foi processada."
            f" {rule}: {flagged_categories}."
            f" Reformule a sua mensagem e tente novamente."
        )

    return ModerationInfo(flagged, reason, scores)
