####
# GENERAL VARIABLES
####

variable "availability_zones" {
  type        = list(string)
  description = "List of availability zones to connect your lambda to"
}

variable "runtime" {
  type        = string
  description = "Runtime to run your function"
}

variable "execution_role_arn" {
  type        = string
  description = "Lambda execution role arn"
}

variable "function_name" {
  type        = string
  description = "Lambda function Name"
}

variable "lambda_name" {
  description = "Nome dos Lambdas"
  type        = list(string)
  default     = []
}

variable "handler" {
  type        = string
  description = "Lambda function handler"
}

variable "code" {
  type        = string
  description = "File path with the function code in ZIP format"
}

variable "description" {
  type        = string
  description = "function description."
  default     = null
}

variable "environment_variables" {
  type        = map(string)
  description = "environment variables to create on the lambda function"
  default     = {}
}

variable "concurrent_executions" {
  description = "Lambda concurrent executions.Set to 0 to stop executions or -1 to set to 'Unlimited'"
  type        = number
  default     = -1
}


####
# TAGS
####

variable "owner_team_email" {
  type        = string
  description = "Owner team contact email. Mandatory tag for lambda resource."
}

variable "tech_team_email" {
  type        = string
  description = "tech team contact email. Mandatory tag for lambda resource."
}

variable "github_repo_id" {
  description = "Github repository ID"
  type = string
  default = "GITHUB_REPOSITORY_TAG_PLACEHOLDER"
}

variable "tags" {
  type        = map(string)
  description = "extra tags for resources"
  default     = {}
}

####
# CW METRIC FILTER
####

variable "create_cw_metric_filter" {
  type        = bool
  description = "create a Cloudwatch metric filter for Logs"
  default     = false
}

variable "cw_metric_filter" {
  type        = any
  description = "object the metric transformation to be monitored by the cloudwatch metric filter"
  default     = null
}

variable "timeout" {
  type        = number
  description = "lambda function execution timeout"
  default     = 900
}


####
# KMS VARIABLES
####

variable "create_kms" {
  type        = bool
  description = "Create a new KMS Key for the lambda function"
  default     = true
}

variable "create_kms_alias" {
  type        = bool
  description = "Create an alias to the KMS key"
  default     = false
}

variable "egress_rules" {
  type = list(object({
    description     = string
    from_port       = number
    to_port         = number
    protocol        = any
    cidr_blocks     = list(string)
    self            = bool
    security_groups = list(string)
    prefix_list_ids = list(string)
  }))
  description = "Egress rules for lambda security group. If omitted, a default rule is assigned"
  default     = []
}