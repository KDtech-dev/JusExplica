from zeep import Client, Settings as ZeepSettings
from zeep.helpers import serialize_object
from zeep.transports import Transport
import requests

from app.core.config import settings


class CatalogUnavailableError(Exception):
    """Indica que não foi possível consultar o catálogo oficial."""


def search_movement_by_code(code: str) -> list[dict]:
    """
    Consulta o catálogo oficial de movimentos processuais do CNJ.

    M = tabela de movimentos.
    C = pesquisa por código.

    Retorna os registros encontrados no SGT.
    """
    session = requests.Session()

    transport = Transport(
        session=session,
        timeout=10,
        operation_timeout=15,
    )

    try:
        client = Client(
            wsdl=settings.tpu_wsdl_url,
            transport=transport,
            settings=ZeepSettings(strict=False),
        )

        result = client.service.pesquisarItemPublicoWS(
            "M",
            "C",
            str(code),
        )

        serialized = serialize_object(result)

        if serialized is None:
            return []

        if isinstance(serialized, list):
            return [
                item
                for item in serialized
                if isinstance(item, dict)
            ]

        if isinstance(serialized, dict):
            return [serialized]

        return []

    except Exception as exc:
        raise CatalogUnavailableError(
            "Não foi possível consultar o catálogo processual do CNJ."
        ) from exc

    finally:
        session.close()