import {
  to = module.eks.aws_eks_addon.before_compute["vpc-cni"]
  id = "eks-devops-senior:vpc-cni"
}

import {
  to = module.eks.aws_eks_addon.before_compute["kube-proxy"]
  id = "eks-devops-senior:kube-proxy"
}

import {
  to = module.eks.aws_eks_addon.this["coredns"]
  id = "eks-devops-senior:coredns"
}