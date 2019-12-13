# 変数定義ファイル
#   ここで定義した変数は terraform.tfvars で上書きされる
#   または `terraform apply -var-file="production.tfvars"` のようにしてコマンド実行時に指定することができる

variable "app_name" {
  default = "bbs"
}
variable "env" {
  default = "dev"
}
variable "aws_instance_count_ap" {
  default = 1
}
variable "aws_instance_key_name" {}
variable "aws_public_host_zone_id" {}
variable "aws_profile" {}
variable "aws_region" {
  default = "ap-northeast-1"
}
variable "aws_sg_ssh_my_ip" {}
