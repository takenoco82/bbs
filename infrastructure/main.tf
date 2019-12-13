terraform {
  # Terraformのバージョンを固定する
  #   ※同じバージョンを使わないと、微妙なバージョン違いで意図しない差分が出ることがあるため
  #   なお、Terraformのバージョン切り替えには tfenv を使うとよい
  required_version = "= 0.12.16"

  # tfstateファイルをS3で管理する
  #   リモートで管理しているtfstateファイルは `terraform state pull` で標準出力できる
  #   リモートで管理するS3等はTerraformの管理対象外にしたほうがいいらしい
  #     https://www.terraform.io/docs/backends/types/s3.html
  #
  #   S3への接続情報は別ファイルにして `terraform init -backend-config=backend.tfvars` のように初期化時に指定する
  #     https://www.terraform.io/docs/backends/config.html#partial-configuration
  backend "s3" {}
}

provider "aws" {
  # Terraformプロバイダのバージョンを固定する
  version = "= 2.38.0"
  profile = var.aws_profile
  region  = var.aws_region
}

# VPC
# https://www.terraform.io/docs/providers/aws/r/vpc.html
resource "aws_vpc" "main" {
  cidr_block                       = "10.0.0.0/16"
  enable_dns_hostnames             = true
  enable_dns_support               = true
  instance_tenancy                 = "default"
  assign_generated_ipv6_cidr_block = false

  tags = {
    # 弊社で使っているAWSリソースの命名規則を紹介します ｜ Developers.IO
    # https://dev.classmethod.jp/cloud/aws/aws-name-rule/
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-vpc"
  }
}

# Subnet
# https://www.terraform.io/docs/providers/aws/r/subnet.html
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-subnet-public"
  }
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  tags = {
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-subnet-private"
  }
}

# Internet Gateway
# https://www.terraform.io/docs/providers/aws/r/internet_gateway.html
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-internet-gateway"
  }
}

# Route Table
# https://www.terraform.io/docs/providers/aws/r/route_table.html
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags = {
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-route-table-public"
  }
}

# Route
# https://www.terraform.io/docs/providers/aws/r/route.html
resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

# Association between a subnet and routing table
# https://www.terraform.io/docs/providers/aws/r/route_table_association.html
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security group
# https://www.terraform.io/docs/providers/aws/r/security_group.html
resource "aws_security_group" "allow-all-outbound" {
  name        = "allow-all-outbound"
  description = "Allow ALL outbound traffic"
  vpc_id      = aws_vpc.main.id
  tags = {
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-sg-allow-all-outbound"
  }
}

resource "aws_security_group" "allow-ssh" {
  name        = "allow-ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = aws_vpc.main.id
  tags = {
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-sg-allow-ssh"
  }
}

# Security group rule
# https://www.terraform.io/docs/providers/aws/r/security_group_rule.html
resource "aws_security_group_rule" "outbound" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.allow-all-outbound.id
}

resource "aws_security_group_rule" "ssh" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = [var.aws_sg_ssh_my_ip]
  description       = "from My IP"
  security_group_id = aws_security_group.allow-ssh.id
}

# EC2 instance
# https://www.terraform.io/docs/providers/aws/r/instance.html
resource "aws_instance" "ap" {
  count = var.aws_instance_count_ap
  # aws ec2 describe-images --image-ids ami-0c3fd0f5d33134a76
  ami                         = "ami-0c3fd0f5d33134a76"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [
    aws_security_group.allow-all-outbound.id,
    aws_security_group.allow-ssh.id
  ]
  key_name                    = var.aws_instance_key_name
  associate_public_ip_address = true
  tags = {
    Application = var.app_name
    Env         = var.env
    Name        = "${var.app_name}-${var.env}-ap${count.index + 1}"
  }
}
