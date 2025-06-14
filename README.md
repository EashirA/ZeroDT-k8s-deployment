# 🚀 Zero Downtime Kubernetes Deployments

![Docker Build and Push](https://github.com/<your-username>/ZeroDT-k8s-deployment/actions/workflows/docker-publish.yml/badge.svg)

This project demonstrates zero-downtime deployment strategies on Kubernetes using a versioned web application and Docker images. It covers:

- Blue-Green Deployment
- Rolling Update Strategy
- Canary Deployment using Argo Rollouts
- GitHub Actions CI/CD integration

---

## 📁 Project Structure

```
app/                     # Source code for the web app
k8s/
  blue-green/            # Blue/Green strategy manifests
  rolling/               # Rolling update manifests
  canary/                # Argo Rollout manifests
.github/workflows/       # GitHub Actions workflow
screenshots/             # Proof of deployments
```

---

## 🐳 Docker Images

- `mdea87/k8s-0dt-app:v1`
- `mdea87/k8s-0dt-app:v2`
- `mdea87/k8s-0dt-app:latest`

---

## 🛠 Deployment Strategy Summary

This project implements and validates three Kubernetes deployment strategies to achieve **zero downtime** application updates:

### ☸️ 1. Blue-Green Deployment

- Two separate deployments are created: `zero-app-blue` using `v1` and `zero-app-green` using `v2`.
- A single Kubernetes Service (`zero-app-svc`) is used to direct traffic.
- Initially, the Service targets the `blue` deployment.
- During a switch, the Service selector is updated to target the `green` deployment (v2).
- ✅ **Zero downtime** is achieved by ensuring both versions run in parallel, and traffic is cut over instantly without interruption.

### 🔁 2. Rolling Update

- A single deployment (`zero-app-rolling`) uses a rolling update strategy with:
  - `maxSurge: 1`
  - `maxUnavailable: 0`
- These values ensure that at least one extra pod is added and none are taken down before a new one becomes available.
- New image versions are applied via `kubectl apply`, and rollout progress is observed with:
  ```bash
  kubectl rollout status deployment/zero-app-rolling
  ```
- ✅ **Zero downtime** is maintained by updating pods one-by-one while keeping the service continuously available.

### 🚦 3. Canary Deployment (Argo Rollouts)

- Canary deployments are implemented using Argo Rollouts via a custom `Rollout` resource.
- The rollout includes gradual traffic shifting steps using `setWeight` and `pause`, e.g.:
  - 25% → pause
  - 50% → pause
  - 100% → complete
- The rollout is monitored live with:
  ```bash
  kubectl argo rollouts get rollout zero-app-rollout --watch
  ```
- ✅ **Zero downtime** is achieved by exposing small portions of user traffic to the new version, allowing real-time validation and rollback if needed.

### ❤️ Health Probes (Optional)

- You may configure liveness and readiness probes using the `/health` endpoint for further assurance.
- This allows Kubernetes to automatically detect and replace failing containers during a rollout.

---

Each strategy was tested and validated using:
- Continuous `curl` or browser-based monitoring
- Docker Hub image versioning
- Argo CLI status monitoring
- Service endpoint responses during the update