module "eks-external-dns" {
  source  = "lablabs/eks-external-dns/aws"
  version = "0.8.0"
  cluster_identity_oidc_issuer =  module.eks.cluster_oidc_issuer_url 
  cluster_identity_oidc_issuer_arn = module.eks.oidc_provider_arn
  cluster_name = local.cluster_name
}


resource "aws_acm_certificate" "cert" {
  domain_name       = "hello.helloworld.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}
