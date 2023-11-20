import jwt
import requests
import datetime
from pathlib import Path
from src.aws.secret_manager import get_private_key
from src.util.monta_erro import payload_erro

import logging

from src.log.logger import (
    print_debug
)


root = f'{Path(__file__).parent.parent}'


def jwt_token(dados_acesso):

    try:

        logging.info('Gerando o token de acesso ao salesforce')

        __AUDIENCE__ = dados_acesso["audience"]
        __ISSUER__ = dados_acesso["issuer"]
        __SUBJECT__ = dados_acesso["subject"]
        __URL_SALES_FORCE__ = dados_acesso["url_token"]
        __PATH_CERTIFICATE__ = dados_acesso["certificado"]

        logging.info('Buscando certificado no path')

        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=45)

        secret = get_private_key(__PATH_CERTIFICATE__)

        jwt_payload = jwt.encode(
            {
                "exp": exp,
                "iss": __ISSUER__,
                "aud": __AUDIENCE__,
                "sub": __SUBJECT__,
            },
            bytes(secret, 'utf-8'),
            algorithm="RS256",
        )

        data_post = {
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": jwt_payload,
            }

        logging.info('Executando post')

        result = requests.post(
            __URL_SALES_FORCE__,
            data=data_post
        )

        print_debug(f'RESPOSTA DO REQUEST DA SALESFORCE {result}')

        if result.status_code == 200:
            logging.info('status_code 200 - Token gerado com sucesso')
            return True, result.json()
        else:
            logging.info('status_code diferente de 200')
            return False, result.json()

    except Exception as e:

        erro = payload_erro({"Exception": [{"msg": e}]}, "jwt_token()")

        return False, erro
