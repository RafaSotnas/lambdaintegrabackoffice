
from src.util.monta_erro import payload_erro

import logging


def valida_tags(payload):

    logging.info('Valida se existe as tags canal e '
                 'composite no payload de entrada')

    if 'canal' in payload and 'composite' in payload:

        logging.info('Tags canal e composite existentes '
                     'no payload de entrada')

        return True, payload

    erro = payload_erro(
            {"Exception": [
                    {"msg": (
                                "Não existe(m) a(s) tag(s) 'canal' "
                                "e/ou 'composite' no payload de entrada"
                            )
                     }
                ]
             },
            "valida_tags()"
        )

    return False, erro
