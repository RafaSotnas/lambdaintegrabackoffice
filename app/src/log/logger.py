import os
from pythonjsonlogger import jsonlogger
import pytz
import datetime
from logging import basicConfig, getLogger, WARNING, StreamHandler

log_level = os.getenv('LOG_LEVEL', 'INFO')


class JsonCustomFormat(jsonlogger.JsonFormatter):

    def __init__(self, *args, **kwargs):
        self.aws_request_id = kwargs.pop('aws_request_id')
        self.function_name = kwargs.pop('function_name')
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        asctime = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
        log_record['aws_request_id'] = self.aws_request_id
        log_record['application_name'] = self.function_name
        log_record["severity"] = log_record['levelname']
        log_record["date_time"] = asctime.strftime("%d-%m-%Y %H:%M:%S")
        del log_record["levelname"]
        del log_record["asctime"]
        return log_record


def config_log(context):

    basicConfig()
    getLogger("boto3").setLevel(WARNING)
    getLogger("botocore").setLevel(WARNING)
    root_logger = getLogger()

    root_logger.setLevel(log_level)
    log_handler = StreamHandler()
    formatter = JsonCustomFormat(
        fmt='%(levelname)s %(message)s %(asctime)s \
    %(lineno)s \
    %(pathname)s \
    %(filename)s %(funcName)s %(module)s',
        aws_request_id=context.aws_request_id,
        function_name=context.function_name
    )
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)
    root_logger.removeHandler(root_logger.handlers[0])


def print_debug(message):
    if log_level == 'DEBUG':
        print(f'DEBUG\t{message}')
