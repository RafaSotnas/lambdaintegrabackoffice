
data "aws_caller_identity" "current" {}

module "iamsr_module" {
    source = "git::https://github.com/itau-corp/itau-ey4-modulo-iamsr.git?ref=v1.1.1"
    
    iam_policies = [
        {
            name = "lambdaintegrabackoffice-policy-iamsr-custom"
            document = "iamsr/policy/policy-lambda.json"
        }
    ]
    
    iam_roles = [
        {
            name = "lambdaintegrabackoffice-role-lambda"
            trust_policy_document = "iamsr/trust/trust-lambda.json"
            attached_policies     = [
                "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/iamsr/lambdaintegrabackoffice-policy-iamsr-custom"
            ]
        }
    ]
}

## CALLING ALL VARIABLES
module "lambda" {
  source                  = "git::https://github.com/itau-corp/itau-ei3-modules-terraform-lambda.git?ref=v1.1.2"
  availability_zones      = var.availability_zones
  runtime                 = var.runtime
  timeout                 = var.timeout
  description             = var.description
  execution_role_arn      = module.iamsr_module.roles[0].arn
  function_name           = var.lambda_name[0]
  handler                 = var.handler
  concurrent_executions   = var.concurrent_executions
  code                    = var.code
  environment_variables   = var.environment_variables
  owner_team_email        = var.owner_team_email
  tech_team_email         = var.tech_team_email
  github_repo_id          = var.github_repo_id
  tags                    = var.tags
  create_kms              = var.create_kms
  egress_rules            = var.egress_rules
  create_cw_metric_filter = var.create_cw_metric_filter
  cw_metric_filter        = var.cw_metric_filter
}

# Alarmes no cloud watch 

# RECURSOS LAMBDAS - INICIO

resource "aws_cloudwatch_metric_alarm" "Lambda_concurrent" {

  alarm_name                = "alarm-Lambda-ConcurrentExecutions-showroomconfiabilidade-Severity:2"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "3"
  metric_name               = "ConcurrentExecutions"
  namespace                 = "AWS/Lambda"
  period                    = "300"
  threshold                 = "2000"
  statistic                 = "Maximum"
  unit                      = "Count"
  alarm_description         = "O número de instâncias de função que estão processando eventos. Se esse número atingir sua cota de execuções simultâneas para a região ou o limite de simultaneidade reservada que você configurou na função, o Lambda limitará as solicitações de invocação adicionais."
  insufficient_data_actions = []
  treat_missing_data        = "notBreaching"
}

resource "aws_cloudwatch_metric_alarm" "Lambda_Duration" {
  count                     = length(var.lambda_name)

  alarm_name                = "alarm-Lambda-${var.lambda_name[count.index]}-Duration-showroomconfiabilidade-Severity:2"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "1"
  metric_name               = "Duration"
  namespace                 = "AWS/Lambda"
  period                    = "60"
  threshold                 = "7000"
  statistic                 = "Maximum"
  alarm_description         = "A quantidade de tempo que seu código de função gasta processando um evento."
  insufficient_data_actions = []
  treat_missing_data        = "notBreaching"
  dimensions = {
    FunctionName = var.lambda_name[count.index]
  }
}

resource "aws_cloudwatch_metric_alarm" "Lambda_Errors" {
  count                     = length(var.lambda_name)

  alarm_name                = "alarm-Lambda-${var.lambda_name[count.index]}-Errors-showroomconfiabilidade-Severity:2"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "3"
  metric_name               = "Errors"
  namespace                 = "AWS/Lambda"
  period                    = "300"
  threshold                 = "20"
  statistic                 = "Sum"
  unit                      = "Count"
  alarm_description         = "O número de invocações que resultam em um erro de função. Os erros de função incluem exceções lançadas pelo seu código e exceções lançadas pelo tempo de execução do Lambda."
  insufficient_data_actions = []
  treat_missing_data        = "notBreaching"
  dimensions = {
    FunctionName = var.lambda_name[count.index]
  }
}

resource "aws_cloudwatch_metric_alarm" "Lambda_Throttles" {
  count                     = length(var.lambda_name)

  alarm_name                = "alarm-Lambda-${var.lambda_name[count.index]}-Throttles-showroomconfiabilidade-Severity:2"
  comparison_operator       = "GreaterThanThreshold"
  evaluation_periods        = "1"
  metric_name               = "Throttles"
  namespace                 = "AWS/Lambda"
  period                    = "60"
  threshold                 = "0"
  statistic                 = "Sum"
  unit                      = "Count"
  alarm_description         = "O número de solicitações de chamada que são limitadas. Quando todas as instâncias de função estão processando solicitações e nenhuma simultaneidade está disponível para escalar verticalmente, o Lambda rejeita solicitações adicionais com um erro TooManyRequestsException"
  insufficient_data_actions = []
  treat_missing_data        = "notBreaching"
  dimensions = {
    FunctionName = var.lambda_name[count.index]
  }
}

# RECURSOS LAMBDAS - FIM


