# Terraform Infrastructure for News Analyzer

This directory contains Terraform configuration to deploy the News Analyzer application on AWS using ECS Fargate.

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) installed (>= 1.2.0).
2. AWS CLI configured with appropriate credentials.

## Resources Created

- **VPC**: A new VPC with public subnets.
- **ECR**: An Elastic Container Registry to store the Docker image.
- **ALB**: An Application Load Balancer to distribute traffic.
- **ECS Cluster**: An ECS cluster running Fargate tasks.
- **ECS Service**: Manages the application replicas.
- **IAM Roles**: Execution and Task roles for ECS.
- **Security Groups**: Network security rules.

## Usage

1. **Initialize Terraform**:
   ```bash
   terraform init
   ```

2. **Configure Variables**:
   Fill in your values.
   ```bash
   # Edit terraform.tfvars with your API keys and DB credentials
   ```

3. **Plan**:
   Review the changes that will be made.
   ```bash
   terraform plan
   ```

4. **Apply**:
   Create the infrastructure.
   ```bash
   terraform apply
   ```

5. **Push Docker Image**:
   After the infrastructure is created, you need to build and push your Docker image to the created ECR repository.
   
   ```bash
   # Login to ECR
   aws ecr get-login-password --region <aws_region> | docker login --username AWS --password-stdin <ecr_repository_url>
   
   # Build
   docker build -t news-analyzer ../
   
   # Tag
   docker tag news-analyzer:latest <ecr_repository_url>:latest
   
   # Push
   docker push <ecr_repository_url>:latest
   ```

   *Note: You can get the `<ecr_repository_url>` from the terraform output.*

6. **Redeploy Service** (if needed):
   If you push a new image, restart the ECS service to pick it up.
   ```bash
   aws ecs update-service --cluster news-analyzer-cluster --service news-analyzer-service --force-new-deployment
   ```

## Outputs

- `alb_hostname`: The URL to access the Streamlit application.
- `ecr_repository_url`: The URL of the ECR repository.
