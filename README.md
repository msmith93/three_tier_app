# three_tier_app

## Flask App
Based loosely on DigitalOcean's tutorial: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

## Infrastructure
Based on https://learn.hashicorp.com/tutorials/terraform/eks

### Setup
Manually set up the following resources:
* ECR repository named helloworld
* S3 bucket named mksmithterraformstate
* ACM certificate

To deploy EKS cluster and helm charts, run the following:
```
cd terraform
terraform init
terraform apply
```

When performing updates, for some reason, the helm chart must first be uninstalled:
```
helm uninstall hello-world-release
terraform apply
```

It seems as though the `helm_release` resource does not upgrade even if a new latest version exists.

## Testing
Get ALB hostname:
```
> kubectl get ingress -o json | jq '.items[0].status.loadBalancer.ingress[0].hostname'
"ae1fb740-default-helloworl-95b0-417308526.us-west-2.elb.amazonaws.com"
```

Get hostname that cert accepts:
```
✗ kubectl get ingress -o json | jq '.items[0].spec.rules[0].host'
"hello.mksmith.xyz"
```

Curl endpoint:
```
curl --resolve hello.mksmith.xyz:443:<ip_of_alb> https://hello.mksmith.xyz/diag | jq .
```

## Future Plans
Multi region implementation: https://disaster-recovery.workshop.aws/en/services/containers/eks/eks-cluster-multi-region.html 

