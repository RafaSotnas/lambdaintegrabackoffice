import lambda_function
from unittest import (
    mock,
    TestCase
)

from dataclasses import (
    dataclass
)


def context():
    @dataclass
    class LambdaContext:
        function_name: str = "test_unitario"
        aws_request_id: str = "88888888-4444-4444-4444-121212121212"
        invoked_function_arn: str = "arn:aws:lambda:regiao:conta:function:test"

    return LambdaContext()


__EVENT__ = {"canal": "BackofficeMN",
             "composite": {"allOrNone": True,
                           "compositeRequest": [
                                {
                                  "method": "GET",
                                  "referenceId": "AccountRef1",
                                  "url": "/services/data/v52.0"
                                },
                                {
                                  "method": "PATCH",
                                  "referenceId": "AccountRef1",
                                  "url": "/services/data/v52.0",
                                  "body": {"Name": "NewName"}
                                },
                                {
                                  "method": "POST",
                                  "referenceId": "AccountRef1",
                                  "url": "/services/data/v52.0",
                                  "body": {"Name": "NewName"}
                                }
                            ]}
             }


class client_mock():

    def __init__(self, service_name=None, region_name=None):
        service_name: str = service_name
        region_name: str = region_name

    def get_secret_value(self, SecretId=None):

        response = {
            "Name": "BackofficeMN",
            "VersionId": "1",
            "SecretString": ('{"audience": "https://test",'
                             '"issuer": "dsd3dVdsiuërEds",'
                             '"subject": "integracao.moedanacional",'
                             '"url_token": "https://test/token",'
                             '"url_endpoint": "/serv/data/v52.0/composite",'
                             '"certificado": "/ME6/Certificado"'
                             '}'
                             )
            }

        return response


class client_nok_mock():

    def __init__(self, service_name=None, region_name=None):
        service_name: str = service_name
        region_name: str = region_name

    def get_secret_value(self, SecretId=None):

        raise Exception("Erro ao buscar o secret")


class requests_mock():

    status_code: int = 200
    sc_get: int = 200
    sc_post: int = 201

    def __init__(self, url=None, data=None, headers=None, status_code=None):

        self.status_code = status_code
        self.url = url
        self.data = data
        self.headers = headers

    def json(self):

        if self.status_code == 200:
            body: dict = {
                "access_token": "sDsdfgngfgmlkgHgFtJju",
                "token_type": "Bearer",
                "instance_url": "https://test.salesforce.com",
                "compositeResponse": [
                                        {"httpStatusCode": self.sc_get},
                                        {"httpStatusCode": self.sc_post},
                                        {"httpStatusCode": self.sc_get}
                                      ]
            }
        else:
            body: dict = {
                "error": "400",
                "error_description": "falhou a chamada"
            }

        return body


class requests_nok_mock():

    status_do_code: int = 999

    def __init__(self, url=None, data=None, headers=None, status_code=None):

        self.status_do_code = status_code
        self.url = url
        self.data = data
        self.headers = headers


requests_jwt_200: requests_mock() = requests_mock(status_code=200)
requests_jwt_400: requests_mock() = requests_mock(status_code=400)
requests_jwt_nok: requests_nok_mock() = requests_nok_mock(status_code=0)
requests_sales_nok: requests_nok_mock() = requests_nok_mock(status_code=0)
requests_sales_400: requests_mock() = requests_mock(status_code=200)
requests_sales_400.sc_get = 400


class test_lambda(TestCase):

    # Testar a execução ok da lambda
    @mock.patch(
        'src.aws.secret_manager.client',
        return_value=(client_mock())
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.jwt.encode',
        return_value="eyJhbOiJI.NiIsI6IpXVCJ9.eyzb21lIjo.F5G9hZCJ9"
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.requests.post',
        return_value=requests_jwt_200
    )
    @mock.patch(
        'src.salesforce.sales_force.post',
        return_value=requests_jwt_200
    )
    def test_validate_lambda_ok(self, *mocks):

        event = __EVENT__

        retorno = lambda_function.lambda_handler(event, context())

        assert retorno is not None

    # Testar a execução não ok da lambda
    @mock.patch(
        'src.aws.secret_manager.client',
        return_value=(client_mock())
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.jwt.encode',
        return_value="eyJhbOiJI.NiIsI6IpXVCJ9.eyzb21lIjo.F5G9hZCJ9"
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.requests.post',
        return_value=requests_jwt_200
    )
    @mock.patch(
        'src.salesforce.sales_force.post',
        return_value=requests_jwt_400
    )
    def test_validate_lambda_nok(self, *mocks):

        event = __EVENT__

        try:

            retorno = lambda_function.lambda_handler(event, context())

        except Exception as e:

            retorno = e.args

            assert retorno is not None

    # Testar a execução não ok da lambda por falta da tag "canal"
    def test_validate_lambda_falta_tag_nok(self, *mocks):

        event = __EVENT__.copy()
        del event['canal']

        try:

            retorno = lambda_function.lambda_handler(event, context())

        except Exception as e:

            retorno = e.args

            assert retorno is not None

    # Testar a Exception no send_composite da lambda
    @mock.patch(
        'src.aws.secret_manager.client',
        return_value=(client_mock())
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.jwt.encode',
        return_value="eyJhbOiJI.NiIsI6IpXVCJ9.eyzb21lIjo.F5G9hZCJ9"
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.requests.post',
        return_value=requests_jwt_200
    )
    @mock.patch(
        'src.salesforce.sales_force.post',
        return_value=requests_sales_nok
    )
    def test_validate_send_composite_nok(self, *mocks):

        event = __EVENT__

        try:

            retorno = lambda_function.lambda_handler(event, context())

        except Exception as e:

            retorno = e.args

            assert retorno is not None

    # Testar send_composite com return <> 200 e 201 da lambda
    @mock.patch(
        'src.aws.secret_manager.client',
        return_value=(client_mock())
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.jwt.encode',
        return_value="eyJhbOiJI.NiIsI6IpXVCJ9.eyzb21lIjo.F5G9hZCJ9"
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.requests.post',
        return_value=requests_jwt_200
    )
    @mock.patch(
        'src.salesforce.sales_force.post',
        return_value=requests_sales_400
    )
    def test_validate_send_composite_400_nok(self, *mocks):

        event = __EVENT__

        try:

            retorno = lambda_function.lambda_handler(event, context())

        except Exception as e:

            retorno = e.args

            assert retorno is not None

    # Teste de erro 400 no jwt
    @mock.patch(
        'src.aws.secret_manager.client',
        return_value=(client_mock())
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.jwt.encode',
        return_value="eyJhbOiJI.NiIsI6IpXVCJ9.eyzb21lIjo.F5G9hZCJ9"
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.requests.post',
        return_value=requests_jwt_400
    )
    @mock.patch(
        'src.salesforce.sales_force.post',
        return_value=requests_jwt_400
    )
    def test_validate_jwt_400(self, *mocks):

        event = __EVENT__

        try:

            retorno = lambda_function.lambda_handler(event, context())

        except Exception as e:

            retorno = e.args

            assert retorno is not None

    # Teste de exception no jwt
    @mock.patch(
        'src.aws.secret_manager.client',
        return_value=(client_mock())
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.jwt.encode',
        return_value="eyJhbOiJI.NiIsI6IpXVCJ9.eyzb21lIjo.F5G9hZCJ9"
    )
    @mock.patch(
        'src.salesforce.jwt_salesforce.requests.post',
        return_value=requests_jwt_nok
    )
    @mock.patch(
        'src.salesforce.sales_force.post',
        return_value=requests_jwt_nok
    )
    def test_validate_jwt_nok(self, *mocks):

        event = __EVENT__

        try:

            retorno = lambda_function.lambda_handler(event, context())

        except Exception as e:

            retorno = e.args

            assert retorno is not None

    # Teste de recuperação do secret não ok
    @mock.patch(
        'src.aws.secret_manager.client',
        return_value=(client_nok_mock())
    )
    def test_validate_get_private_key_nok(self, *mocks):

        event = __EVENT__

        try:

            retorno = lambda_function.lambda_handler(event, context())

        except Exception as e:

            retorno = e.args

            assert retorno is not None
