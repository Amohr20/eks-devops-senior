from flask import Flask, render_template_string, jsonify
import socket
import time
import math
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>EKS DevOps Senior</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
    }

    body {
      min-height: 100vh;
      background:
        radial-gradient(circle at top left, rgba(59,130,246,.45), transparent 35%),
        radial-gradient(circle at bottom right, rgba(34,197,94,.35), transparent 35%),
        linear-gradient(135deg, #020617, #0f172a, #1e293b);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 32px;
    }

    .card {
      width: 100%;
      max-width: 1050px;
      background: rgba(15, 23, 42, 0.78);
      border: 1px solid rgba(148, 163, 184, 0.28);
      border-radius: 32px;
      padding: 48px;
      box-shadow: 0 30px 90px rgba(0,0,0,.45);
      backdrop-filter: blur(20px);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(34,197,94,.12);
      color: #86efac;
      border: 1px solid rgba(134,239,172,.35);
      padding: 9px 16px;
      border-radius: 999px;
      font-size: 14px;
      font-weight: 800;
      margin-bottom: 24px;
    }

    h1 {
      font-size: clamp(36px, 6vw, 64px);
      line-height: 1.05;
      margin-bottom: 20px;
      letter-spacing: -1.5px;
    }

    .subtitle {
      font-size: 19px;
      color: #cbd5e1;
      line-height: 1.7;
      max-width: 860px;
      margin-bottom: 34px;
    }

    .buttons {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 34px;
    }

    .btn {
      text-decoration: none;
      color: #020617;
      background: #f8fafc;
      padding: 14px 20px;
      border-radius: 15px;
      font-weight: 900;
      box-shadow: 0 15px 30px rgba(0,0,0,.25);
    }

    .btn.secondary {
      color: white;
      background: rgba(255,255,255,.10);
      border: 1px solid rgba(255,255,255,.22);
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-top: 28px;
    }

    .item {
      background: rgba(2, 6, 23, .58);
      border: 1px solid rgba(148,163,184,.22);
      border-radius: 22px;
      padding: 22px;
    }

    .item span {
      display: block;
      font-size: 12px;
      color: #93c5fd;
      text-transform: uppercase;
      letter-spacing: .12em;
      margin-bottom: 10px;
      font-weight: 800;
    }

    .item strong {
      font-size: 19px;
      color: #f8fafc;
      word-break: break-word;
    }

    .footer {
      margin-top: 30px;
      color: #94a3b8;
      font-size: 14px;
      line-height: 1.6;
    }

    @media (max-width: 640px) {
      .card {
        padding: 30px;
        border-radius: 24px;
      }
    }
  </style>
</head>
<body>
  <main class="card">
    <div class="badge">● Running on Amazon EKS</div>

    <h1>Cloud/DevOps Senior Lab</h1>

    <p class="subtitle">
      Aplicación Dockerizada desplegada en Amazon EKS con Terraform, Amazon ECR,
      Kubernetes Deployment, Service, ALB Ingress, HPA y Karpenter para autoscaling
      de Pods, nodos EC2 y CI/CD con GitHub Actions.
    </p>

    <div class="buttons">
      <a class="btn" href="/health">Health Check</a>
      <a class="btn secondary" href="/load">Generar carga CPU</a>
    </div>

    <section class="grid">
      <div class="item">
        <span>Estado</span>
        <strong>Healthy</strong>
      </div>

      <div class="item">
        <span>Pod actual</span>
        <strong>{{ pod }}</strong>
      </div>

      <div class="item">
        <span>Versión</span>
        <strong>{{ version }}</strong>
      </div>

      <div class="item">
        <span>Plataforma</span>
        <strong>AWS EKS</strong>
      </div>

      <div class="item">
        <span>Autoscaling Pods</span>
        <strong>Horizontal Pod Autoscaler</strong>
      </div>

      <div class="item">
        <span>Autoscaling Nodos</span>
        <strong>Karpenter</strong>
      </div>
    </section>

    <div class="footer">
      Angel Mohr - laboratorio profesional Cloud/DevOps con infraestructura como código y despliegue automatizable.
    </div>
  </main>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        pod=socket.gethostname(),
        version=os.getenv("APP_VERSION", "v1")
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "pod": socket.gethostname(),
        "version": os.getenv("APP_VERSION", "v1")
    })

@app.route("/load")
def load():
    end = time.time() + 5
    result = 0

    while time.time() < end:
        result += math.sqrt(12345.6789)

    return jsonify({
        "message": "Carga CPU generada correctamente",
        "pod": socket.gethostname(),
        "result": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)