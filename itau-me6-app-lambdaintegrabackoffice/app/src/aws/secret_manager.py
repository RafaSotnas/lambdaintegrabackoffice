from boto3 import (
    client
)
from botocore.exceptions import ClientError
import json
from src.util.monta_erro import payload_erro
import os

import logging


__PREFIXO_CREDENCIAIS__ = os.environ.get('PrefixoCredenciais')


def get_client(sm_client=None):

    if not sm_client:
        sm_client = client(
            service_name='secretsmanager',
            region_name='sa-east-1'
        )

    return sm_client


def get_private_key(path_certificate_manager: str) -> str:

    try:

        logging.info('Busca as informações da chave privada na AWS')

        cli = get_client()

        response = cli.get_secret_value(
            SecretId=path_certificate_manager
        )

        return response['SecretString']

    except (ClientError, Exception) as e:

        erro = payload_erro({"Exception": [{"msg": e}]},
                            "get_private_key()")

        raise Exception(erro)


def get_credencial_integracao(canal: str) -> str:

    logging.info('Monta path_secret')

    path_secret = f'{__PREFIXO_CREDENCIAIS__}{canal}'

    chaves = get_private_key(path_secret)

    return json.loads(chaves)
