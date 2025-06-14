Zero Downtime Kubernetes Deployments

Author
Md Eashir Arafat  
**Project Title:** Zero Downtime Deployments with Blue-Green, Rolling, and Canary Strategies  

Objective

The goal of this project was to design and validate three Kubernetes deployment strategies that ensure **zero downtime** during application updates:
- Blue-Green Deployment  
- Rolling Update  
- Canary Release using Argo Rollouts

A simple versioned web application was containerized and deployed using each strategy to assess upgrade safety and traffic control effectiveness.

---
Technologies Used

| Tool             | Purpose                               |
|------------------|----------------------------------------|
| Docker           | Containerization                      |
| Docker Hub       | Hosting container images              |
| Kubernetes       | Deployment & orchestration platform   |
| Minikube         | Local Kubernetes cluster              |
| `kubectl`        | Kubernetes command-line client        |
| Argo Rollouts    | Progressive delivery & canary control |
| Git + GitHub     | Version control & workflow automation |

---

Application

A lightweight Python HTTP server was created that serves a static HTML file showing version number:

- `v1` → displays `Version 1`  
- `v2` → displays `Version 2`  

Docker Hub Repository:  
👉 [https://hub.docker.com/r/mdea87/k8s-0dt-app](https://hub.docker.com/r/mdea87/k8s-0dt-app)

Strategy 1 – Blue-Green Deployment

- Two separate deployments: `zero-app-blue` (v1) and `zero-app-green` (v2)
- A single Service (`zero-app-svc`) initially routes to the `v1` deployment
- A manual selector switch (`version: v2`) was applied to transition traffic
- Tested with `curl` to verify zero downtime

Outcome: Smooth traffic cutover with zero downtime

---

Strategy 2 – Rolling Update

- A single deployment (`zero-app-rolling`) was configured with:
  - `maxSurge: 1`
  - `maxUnavailable: 0`
- Updated image from `v1` to `v2` using `kubectl apply`
- Service remained uninterrupted during rollout
- Verified with continuous `curl` monitoring

Outcome: Rolling updates occurred without any service disruption

---

Strategy 3 – Canary Deployment (Argo Rollouts)

- Canary rollout created using `Rollout` resource with these steps:
  - `setWeight: 25`
  - `pause: 20s`
  - `setWeight: 50`
  - `pause: 20s`
  - `setWeight: 100`
- Live monitoring with:
  ```bash
  kubectl argo rollouts get rollout zero-app-rollout --watch