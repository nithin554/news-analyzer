terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"

  cloud {
    organization = "news-analyzer"

    workspaces {
      name = "news-analyzer-workspace"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
