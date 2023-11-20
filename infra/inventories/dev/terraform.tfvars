####
# This is a file to be used for dev environment
####

create_kms              = true
create_kms_alias        = true
execution_role_arn      = "arn:aws:iam::779726708338:role/iamsr/lambdaintegrabackoffice-role-lambda-states"

environment_variables = {
  "ENVIRONMENT"         = "DEV",
  "VALIDATE"            = "TRUE",
  "PrefixoCredenciais"  = "CredenciaisIntegracao",
  "LOG_LEVEL"           = "DEBUG"
}

availability_zones      = ["sa-east-1a", "sa-east-1b", "sa-east-1c"]
function_name           = "lambdaintegrabackoffice"
runtime                 = "python3.9"
timeout                 = 30
handler                 = "lambda_function.lambda_handler"
code                    = "code/application.zip"
concurrent_executions   = 100
description             = "Lambda genérica de integração com o salesforce para gravame"
owner_team_email        = "SquadProcessosOperacionais-MoedaNacional@correio.itau.com.br"
tech_team_email         = "SquadProcessosOperacionais-MoedaNacional@correio.itau.com.br"

egress_rules = [
  {
    description     = "default egress rule for lambda - RFC1918"
    from_port       = 0
    to_port         = 0
    protocol        = -1
    cidr_blocks     = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "0.0.0.0/0"]
    self            = false
    security_groups = []
    prefix_list_ids = []
  }
]

lambda_name = [
  "lambdaintegrabackoffice"
]

