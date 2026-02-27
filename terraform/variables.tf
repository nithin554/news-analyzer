variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-north-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "news-analyzer"
}

variable "environment" {
  description = "Environment (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "container_port" {
  description = "Port exposed by the docker container"
  type        = number
  default     = 8501
}

variable "google_api_key" {
  description = "Google API Key"
  type        = string
  sensitive   = true
}

variable "db_url" {
  description = "Database URL"
  type        = string
  sensitive   = true
}

variable "db_username" {
  description = "Database Username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database Password"
  type        = string
  sensitive   = true
}

variable "langsmith_api_key" {
  description = "Langsmith API Key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "langsmith_project" {
  description = "Langsmith Project"
  type        = string
  default     = "news_analyzer_agent"
}
