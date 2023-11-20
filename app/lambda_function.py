'''

    Lambda usada para levar os dados de gravame para o Salesforce através
    do composite.

    Descrição: Recebe um payload indicando o canal e a composite pronta.
               Pega as informações do canal e com essa informação busca
               os dados de conexão da salesforce.

    Projeto: Gravame
    Squad2020: Inovativos - Moeda Nacional

    Criado por: Edson Silva
    Data : jul/2023

    Modificado por:
    Data :

    Dados app:
    Nome: itau-me6-app-lambdaintegrabackoffice
    Sigla App: ME6-L1012
    conta aws: plataformabackofficeativos

'''


from src.salesforce.sales_force import (
    get_acessos_salesforce,
    send_composite_salesforce
)

from src.util.validate import (
    valida_tags
)

from src.error_wf.error_cls import (
    gravame_error
)

import logging

from src.log.logger import (
    config_log
)


def lambda_handler(event, context):

    config_log(context)     # Configuração padrão de log a ser usado

    logging.info('Inicio Execução lambda_handler()',
                 extra={'payload_entrada': event}
                 )

    payload_entrada = event

    exec_ok, retorno = valida_tags(payload_entrada)

    if exec_ok:

        canal = payload_entrada['canal']

        exec_ok, retorno = get_acessos_salesforce(canal)

        if exec_ok:

            dados_sales = {}

            dados_sales['acessos_sales'] = retorno
            dados_sales['composite'] = payload_entrada['composite']

            exec_ok, retorno = send_composite_salesforce(dados_sales)

            if exec_ok:

                logging.info('Composite executada com sucesso na salesforce')

                return retorno

    logging.error(retorno)

    raise gravame_error(retorno)
