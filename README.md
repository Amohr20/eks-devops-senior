# Proyecto Cloud/DevOps Senior en AWS EKS

Proyecto práctico de arquitectura Cloud/DevOps usando **Terraform**, **Amazon EKS**, **Docker**, **Amazon ECR**, **GitHub Actions**, **AWS Load Balancer Controller**, **HPA** y **Karpenter**.

El objetivo del proyecto es demostrar una implementación realista de una aplicación contenerizada desplegada en Kubernetes sobre AWS, con infraestructura como código, CI/CD, balanceo de carga, escalamiento automático de Pods y escalamiento automático de nodos EC2.

---

## 1. Arquitectura general

```text
Usuario / Navegador
        ↓
AWS Application Load Balancer
        ↓
Ingress Kubernetes
        ↓
Service ClusterIP
        ↓
Pods de la aplicación Flask
        ↓
Deployment
        ↓
HPA escala Pods según CPU
        ↓
Karpenter crea nodos EC2 si no hay capacidad
        ↓
Amazon EKS ejecuta Kubernetes
```

---

## 2. Tecnologías utilizadas

| Tecnología | Uso dentro del proyecto |
|---|---|
| AWS EKS | Cluster Kubernetes administrado |
| Terraform | Infraestructura como código |
| Docker | Contenerización de la aplicación |
| Amazon ECR | Registro privado de imágenes Docker |
| GitHub Actions | Pipeline CI/CD |
| AWS Load Balancer Controller | Creación automática del ALB desde Ingress |
| Application Load Balancer | Exposición pública de la aplicación |
| Kubernetes Deployment | Gestión de réplicas de la aplicación |
| Kubernetes Service | Comunicación interna hacia los Pods |
| Kubernetes Ingress | Entrada HTTP hacia el Service |
| HPA | Escalamiento automático de Pods |
| Karpenter | Escalamiento automático de nodos EC2 |
| EKS Pod Identity | Permisos IAM para Pods específicos |
| Metrics Server | Métricas de CPU y memoria para HPA |

---

## 3. Estructura del proyecto

```text
eks-devops-senior/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── k8s/
│   ├── 01-namespace.yaml
│   ├── 02-deployment.yaml
│   ├── 03-service.yaml
│   ├── 04-ingress.yaml
│   ├── 05-hpa.yaml
│   ├── 06-ec2nodeclass.yaml
│   └── 07-nodepool.yaml
│
├── terraform/
│   ├── versions.tf
│   ├── providers.tf
│   ├── variables.tf
│   ├── terraform.tfvars
│   ├── main.tf
│   ├── outputs.tf
│   └── alb-controller-iam-policy.json
│
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## 4. Componentes principales

### 4.1 Terraform

Terraform crea y administra la infraestructura principal:

- VPC.
- Subnets públicas y privadas.
- NAT Gateway.
- Internet Gateway.
- Route Tables.
- EKS Cluster.
- Managed Node Group base.
- Amazon ECR.
- IAM Roles.
- EKS Access Entries.
- EKS Add-ons.
- AWS Load Balancer Controller.
- Karpenter.
- Pod Identity Associations.
- GitHub Actions OIDC Role.

### 4.2 Aplicación Dockerizada

La aplicación es una app sencilla en Flask con:

- Página principal visual.
- Endpoint `/health`.
- Endpoint `/load` para generar carga CPU.
- Gunicorn como servidor de aplicación.

### 4.3 Kubernetes

Los manifiestos Kubernetes crean:

- Namespace `app-demo`.
- Deployment con 2 réplicas iniciales.
- Service tipo `ClusterIP`.
- Ingress administrado por AWS Load Balancer Controller.
- HPA con escalamiento por CPU.
- EC2NodeClass para Karpenter.
- NodePool para aprovisionamiento dinámico de nodos.

### 4.4 CI/CD

GitHub Actions realiza:

```text
git push
↓
Build imagen Docker
↓
Push a Amazon ECR
↓
Update kubeconfig
↓
kubectl set image
↓
Rollout automático en EKS
```

---

## 5. Requisitos previos

En la máquina local se requiere:

- AWS CLI configurado.
- Terraform instalado.
- kubectl instalado.
- Docker Desktop instalado.
- Git instalado.
- Cuenta AWS con permisos para crear recursos.
- Repositorio GitHub configurado.
- Credenciales AWS correctamente configuradas localmente.

Validar acceso AWS:

```powershell
aws sts get-caller-identity
```

Validar Docker:

```powershell
docker version
docker ps
```

Validar Terraform:

```powershell
terraform version
```

Validar kubectl:

```powershell
kubectl version --client
```

---

## 6. Despliegue de infraestructura

Entrar a la carpeta de Terraform:

```powershell
cd C:\kubernetes\eks-devops-senior\terraform
```

Inicializar Terraform:

```powershell
terraform init
```

Validar configuración:

```powershell
terraform validate
```

Ver plan:

```powershell
terraform plan
```

Crear infraestructura:

```powershell
terraform apply
```

Al finalizar, Terraform muestra outputs similares a:

```text
cluster_name = "eks-devops-senior"
ecr_repository_url = "211125731695.dkr.ecr.us-east-1.amazonaws.com/eks-demo-app-senior"
github_actions_role_arn = "arn:aws:iam::211125731695:role/eks-devops-senior-github-actions-role"
region = "us-east-1"
vpc_id = "vpc-xxxxxxxx"
```

---

## 7. Conectarse al cluster

Actualizar kubeconfig:

```powershell
aws eks update-kubeconfig `
--region us-east-1 `
--name eks-devops-senior
```

Validar nodos:

```powershell
kubectl get nodes
```

Validar Pods del sistema:

```powershell
kubectl get pods -A
```

Validar Karpenter:

```powershell
kubectl get pods -n karpenter
```

---

## 8. Construir y subir imagen Docker manualmente

Entrar a la carpeta de la app:

```powershell
cd C:\kubernetes\eks-devops-senior\app
```

Construir imagen:

```powershell
docker build -t eks-demo-app-senior:v1 .
```

Login a ECR:

```powershell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 211125731695.dkr.ecr.us-east-1.amazonaws.com
```

Etiquetar imagen:

```powershell
docker tag eks-demo-app-senior:v1 211125731695.dkr.ecr.us-east-1.amazonaws.com/eks-demo-app-senior:v1
```

Subir imagen:

```powershell
docker push 211125731695.dkr.ecr.us-east-1.amazonaws.com/eks-demo-app-senior:v1
```

---

## 9. Desplegar aplicación en Kubernetes

Entrar a la carpeta `k8s`:

```powershell
cd C:\kubernetes\eks-devops-senior\k8s
```

Aplicar manifiestos:

```powershell
kubectl apply -f .
```

Validar Pods:

```powershell
kubectl get pods -n app-demo -o wide
```

Validar Service:

```powershell
kubectl get svc -n app-demo
```

Validar Ingress:

```powershell
kubectl get ingress -n app-demo
```

Obtener URL del ALB:

```powershell
kubectl get ingress eks-demo-ingress -n app-demo
```

Abrir el valor de `ADDRESS` en el navegador.

---

## 10. Validar CI/CD

Modificar algo visible en:

```text
app/app.py
```

Ejemplo:

```text
Cloud/DevOps Senior Lab - CI/CD OK
```

Subir cambio a GitHub:

```powershell
cd C:\kubernetes\eks-devops-senior

git add .
git commit -m "Test CI/CD deployment"
git push
```

Ver ejecución en GitHub:

```text
GitHub Repository
↓
Actions
↓
Build and Deploy to EKS
```

Validar rollout:

```powershell
kubectl rollout status deployment/eks-demo-app -n app-demo
```

Ver imagen actual del Deployment:

```powershell
kubectl describe deployment eks-demo-app -n app-demo
```

---

## 11. Pruebas de HPA

Ver HPA:

```powershell
kubectl get hpa -n app-demo
```

Monitorear HPA en vivo:

```powershell
kubectl get hpa -n app-demo -w
```

Monitorear Pods:

```powershell
kubectl get pods -n app-demo -o wide -w
```

Generar carga usando `/load`:

```powershell
$url = "http://TU_ALB_DNS/load"

1..30 | ForEach-Object {
  Start-Job -ScriptBlock {
    param($url)
    for ($i=1; $i -le 1000; $i++) {
      Invoke-WebRequest $url -UseBasicParsing | Out-Null
    }
  } -ArgumentList $url
}
```

Ver jobs:

```powershell
Get-Job
```

Limpiar jobs:

```powershell
Get-Job | Remove-Job -Force
```

---

## 12. Pruebas de Karpenter

Validar Karpenter:

```powershell
kubectl get pods -n karpenter
```

Validar NodePool:

```powershell
kubectl get nodepool
```

Validar EC2NodeClass:

```powershell
kubectl get ec2nodeclass
```

Forzar alto consumo por Pod:

```powershell
kubectl set resources deployment eks-demo-app `
-n app-demo `
--containers=eks-demo-app `
--requests=cpu=900m,memory=256Mi `
--limits=cpu=1000m,memory=512Mi
```

Subir réplicas:

```powershell
kubectl scale deployment eks-demo-app -n app-demo --replicas=10
```

Monitorear Pods:

```powershell
kubectl get pods -n app-demo -o wide -w
```

Monitorear nodos:

```powershell
kubectl get nodes -o wide -w
```

Monitorear NodeClaims:

```powershell
kubectl get nodeclaims -w
```

Monitorear logs de Karpenter:

```powershell
kubectl logs -n karpenter deployment/karpenter -f
```

Flujo esperado:

```text
Pods Pending
↓
Karpenter crea NodeClaim
↓
AWS lanza EC2
↓
Nuevo nodo aparece en Kubernetes
↓
Pods pasan a Running
```

Regresar configuración normal:

```powershell
kubectl scale deployment eks-demo-app -n app-demo --replicas=2
```

```powershell
kubectl set resources deployment eks-demo-app `
-n app-demo `
--containers=eks-demo-app `
--requests=cpu=100m,memory=128Mi `
--limits=cpu=500m,memory=512Mi
```

---

## 13. Comandos útiles de monitoreo

Ver Pods en tiempo real:

```powershell
kubectl get pods -n app-demo -o wide -w
```

Ver nodos en tiempo real:

```powershell
kubectl get nodes -o wide -w
```

Ver HPA en tiempo real:

```powershell
kubectl get hpa -n app-demo -w
```

Ver consumo de Pods:

```powershell
kubectl top pods -n app-demo
```

Ver consumo de nodos:

```powershell
kubectl top nodes
```

Ver NodeClaims de Karpenter:

```powershell
kubectl get nodeclaims
```

Ver eventos del namespace:

```powershell
kubectl get events -n app-demo --sort-by=.metadata.creationTimestamp
```

Ver logs de la app:

```powershell
kubectl logs -n app-demo deployment/eks-demo-app
```

Ver logs del AWS Load Balancer Controller:

```powershell
kubectl logs -n kube-system deployment/aws-load-balancer-controller --tail=100
```

---

## 14. Destruir infraestructura para evitar costos

Entrar a Terraform:

```powershell
cd C:\kubernetes\eks-devops-senior\terraform
```

Destruir:

```powershell
terraform destroy
```

Confirmar con:

```text
yes
```

### Recursos que deben eliminarse

Terraform debe eliminar:

- EKS Cluster.
- Node Groups.
- EC2 creadas.
- Karpenter.
- ALB Controller.
- VPC.
- NAT Gateway.
- ECR.
- IAM roles/policies creados por Terraform.

### Revisión manual recomendada en AWS

Después del destroy, revisar:

- EC2 Instances.
- Load Balancers.
- Target Groups.
- NAT Gateways.
- EBS Volumes.
- Elastic IPs.
- VPC.
- ECR.
- CloudFormation stacks relacionados.

Esto es importante porque algunos recursos pueden tardar minutos en desaparecer o quedar bloqueados por dependencias.

---

## 15. Levantar nuevamente el proyecto

Al día siguiente:

```powershell
cd C:\kubernetes\eks-devops-senior\terraform
terraform apply
```

Actualizar kubeconfig:

```powershell
aws eks update-kubeconfig `
--region us-east-1 `
--name eks-devops-senior
```

Validar cluster:

```powershell
kubectl get nodes
kubectl get pods -A
```

Construir y subir imagen:

```powershell
cd C:\kubernetes\eks-devops-senior\app

docker build -t eks-demo-app-senior:v1 .

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 211125731695.dkr.ecr.us-east-1.amazonaws.com

docker tag eks-demo-app-senior:v1 211125731695.dkr.ecr.us-east-1.amazonaws.com/eks-demo-app-senior:v1

docker push 211125731695.dkr.ecr.us-east-1.amazonaws.com/eks-demo-app-senior:v1
```

Aplicar Kubernetes:

```powershell
cd C:\kubernetes\eks-devops-senior\k8s
kubectl apply -f .
```

Validar Ingress:

```powershell
kubectl get ingress -n app-demo
```

---

## 16. Problemas resueltos durante el proyecto

### 16.1 NodeCreationFailure

Problema:

```text
NodeCreationFailure: Unhealthy nodes in the kubernetes cluster
```

Causa detectada:

```text
Faltaba el add-on vpc-cni o no estaba listo antes de crear nodos.
```

Solución:

```text
Configurar add-ons de EKS y usar before_compute para vpc-cni/kube-proxy.
```

### 16.2 Karpenter sin credenciales

Problema:

```text
failed to refresh cached credentials
no EC2 IMDS role found
```

Causa:

```text
Pod Identity no estaba asociado al namespace/serviceAccount correcto.
```

Solución:

```text
Asociar Karpenter al serviceAccount karpenter en namespace karpenter.
```

### 16.3 AWS Load Balancer Controller sin credenciales

Problema:

```text
Elastic Load Balancing v2: DescribeLoadBalancers
no EC2 IMDS role found
```

Causa:

```text
El controller no tenía IAM Role asociado por Pod Identity.
```

Solución:

```text
Crear IAM Policy, IAM Role y Pod Identity Association para aws-load-balancer-controller.
```

### 16.4 GitHub Actions sin permisos en EKS

Problema:

```text
You must be logged in to the server
```

Causa:

```text
El IAM Role de GitHub Actions tenía permisos AWS, pero no permisos dentro del cluster EKS.
```

Solución:

```text
Crear EKS Access Entry y asociar AmazonEKSClusterAdminPolicy al role de GitHub Actions.
```

---

## 17. Descripción para CV

```text
Implementé una plataforma Cloud/DevOps en AWS utilizando Terraform para aprovisionar VPC, EKS, ECR, IAM, Karpenter y AWS Load Balancer Controller. Desplegué una aplicación Dockerizada con CI/CD mediante GitHub Actions, publicada con ALB Ingress, HPA para escalamiento automático de Pods y Karpenter para escalamiento dinámico de nodos EC2. La arquitectura incluye subnets privadas, NAT Gateway, EKS Pod Identity, Amazon ECR y automatización completa de infraestructura como código.
```

---

## 18. Estado final del proyecto

El proyecto demuestra:

- Infraestructura como código con Terraform.
- Aplicación contenerizada con Docker.
- Despliegue sobre Amazon EKS.
- Publicación mediante Application Load Balancer.
- CI/CD con GitHub Actions.
- Escalamiento horizontal de Pods con HPA.
- Escalamiento dinámico de nodos EC2 con Karpenter.
- Uso de IAM moderno con EKS Pod Identity.
- Arquitectura AWS con subnets públicas y privadas.
- Flujo realista de operación Cloud/DevOps.
