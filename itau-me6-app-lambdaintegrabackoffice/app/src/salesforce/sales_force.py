
import json
from src.salesforce.jwt_salesforce import jwt_token
from requests import post, exceptions
from src.util.monta_erro import payload_erro
from src.aws.secret_manager import (
    get_credencial_integracao
)

import logging

from src.log.logger import (
    print_debug
)


def get_acessos_salesforce(canal: str):

    try:

        logging.info('Busca as informações dos acessos ao salesforce '
                     'nas credenciais na AWS')

        chaves_acesso = get_credencial_integracao(canal)

        logging.info('Busca das informações dos acessos ao salesforce '
                     'nas credenciais na AWS com sucesso')

        return True, chaves_acesso

    except Exception as e:

        erro = payload_erro({"Exception": [{"msg": e}]},
                            "get_acessos_salesforce()")

        return False, erro


def send_composite_salesforce(dados_sales):

    logging.info('Envia composite para executar na salesforce')

    exec_ok, retorno = jwt_token(dados_sales['acessos_sales'])

    if not exec_ok:

        erro = payload_erro({"Exception": [{"msg": retorno}]}, "jwt_token()")

        logging.error(erro, exc_info=True)

        return False, erro

    try:

        logging.info('Capturando composite do payload de entrada')

        composite = json.dumps(dados_sales["composite"])

        logging.info("Capturando 'access_token' e "
                     "'token_type' do token gerado")

        token_sales = retorno["access_token"]
        token_type = retorno["token_type"]

        __END_POINT__ = dados_sales['acessos_sales']["url_endpoint"]
        url = f"{retorno['instance_url']}{__END_POINT__}"

        print_debug(f">>> END POINT COMPOSITE: {url}")

        headers = {
            "Authorization": f"{token_type} {token_sales}",
            "Content-Type": "application/json",
        }

        logging.info('Executando post')

        response = post(url=url, data=composite, headers=headers)

        if response.status_code == 200:

            logging.info('status_code 200 - post executado com sucesso')

            json_retorno = response.json()

            exec_ok = check_status_code_composite(json_retorno)

            if exec_ok:

                return True, json_retorno

        erro = payload_erro(
            {
                "Exception": [
                    {
                        "status_code": response.status_code,
                        "msg": response.json(),
                    }
                ]
            },
            "send_composite_salesforce()",
        )

        return False, erro

    except (exceptions.RequestException, Exception) as e:

        erro = payload_erro(
            {"Exception": [e]},
            "send_composite_salesforce()RequestException"
        )

        return False, erro


def check_status_code_composite(json_retorno):
    """
        verifica todos os retornos do composite

        :return True se todos os status code forem (200, 201 e 204) \
        ou False se algum for diferente
    """

    logging.info('Checando todos os status code de dentro da composite')

    qtde_itens = len(json_retorno['compositeResponse'])
    qtde_ok = 0

    for i in range(qtde_itens):

        status_post = int(
            json_retorno['compositeResponse'][i]['httpStatusCode']
        )

        if (status_post == 200 or status_post == 201 or status_post == 204):
            qtde_ok += 1

    if qtde_ok == qtde_itens:

        logging.info('Ok - Status code (200 ou 201 ou 204) '
                     'dentro da composite')

        return True

    logging.info('Erro - Status code de dentro da composite '
                 'diferente de (200 ou 201 ou 204)')

    return False
