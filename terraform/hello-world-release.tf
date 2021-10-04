provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
    exec {
      api_version = "client.authentication.k8s.io/v1alpha1"
      args        = ["eks", "get-token", "--cluster-name", local.cluster_name]
      command     = "aws"
    }
  }
}

resource "helm_release" "hello_world_release" {
  name            = "hello-world-release"
  repository      = "https://msmith93.github.io/three_tier_app/"
  chart           = "helloworld"
  cleanup_on_fail = true

  values = [
    "${file("values.yaml")}"
  ]

  set {
    name  = "cluster.enabled"
    value = "true"
  }

  set {
    name = "ingress_cert"
    #value = "arn:aws:acm:us-west-2:148660894061:certificate/b985d09b-6622-4525-aacc-78b53002cddd" # aws_acm_certificate.cert.arn
    value = "arn:aws:acm:us-west-2:148660894061:certificate/c3a4d137-6457-4787-9401-498f6b66ea18"
  }

  # Ensure helm release is not installed before ALB ingress controller is installed
  depends_on = [module.alb_ingress_controller.aws_iam_role_arn]
}
