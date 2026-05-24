# Exercise 10: Infrastructure as Code GitOps Simulation

## Overview
This exercise demonstrates GitOps principles where infrastructure is defined in Git and automatically deployed to Kubernetes.

## GitOps Philosophy

```
Git is the single source of truth
Code Review → Merge → Automatic Deployment
```

## Repository Structure

```
k8s/
├── deployment.yaml    (Pod configuration)
├── service.yaml       (Load balancing)
└── ingress.yaml       (External routing)
```

## Part 1: Base Kubernetes Manifests

### Deployment (deployment.yaml)
- 3 replicas for high availability
- Health checks (liveness & readiness probes)
- Resource requests/limits
- Environment configuration

**Commit:** 7d90b33

### Service (service.yaml)
- ClusterIP: Internal service discovery
- LoadBalancer: External access
- Port mapping: 80 → 5000

**Commit:** 20be20c

### Ingress (ingress.yaml)
- TLS/HTTPS support
- Domain-based routing
- Rate limiting
- Let's Encrypt integration

**Commit:** d14eda1

## Part 2: Feature Branches for Infrastructure Changes

### Feature 1: Scaling (feature/k8s-scaling)
**Changes:**
- Replicas: 3 → 5
- Add HorizontalPodAutoscaler (HPA)
  - Min replicas: 2
  - Max replicas: 10
  - CPU threshold: 70%
  - Memory threshold: 80%

**Commit:** f86863f

**YAML Diff:**
```yaml
spec:
  replicas: 3        → 5
  # Added HPA section:
  - minReplicas: 2
  - maxReplicas: 10
  - metrics: CPU/Memory
```

### Feature 2: Ingress Enhancement (feature/k8s-ingress-enhancement)
**Changes:**
- Multi-domain support
- Additional security annotations
- CORS enabled
- ModSecurity enabled
- SSL redirect enforced

**Commit:** 108ecdd

**YAML Changes:**
```yaml
annotations:
  # Added security enhancements
  nginx.ingress.kubernetes.io/ssl-redirect: "true"
  nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
  nginx.ingress.kubernetes.io/enable-cors: "true"
  nginx.ingress.kubernetes.io/enable-modsecurity: "true"

tls:
  hosts:
    - cloud-optimizer.example.com
    - api.cloud-optimizer.example.com  # NEW
```

### Feature 3: Resource Limits (feature/k8s-resource-limits)
**Changes:**
- Memory requests: 256Mi → 512Mi
- CPU requests: 100m → 250m
- Memory limits: 512Mi → 1Gi
- CPU limits: 500m → 1000m

**Commit:** 3cd1019

**YAML Changes:**
```yaml
resources:
  requests:
    memory: "256Mi"  → "512Mi"
    cpu: "100m"      → "250m"
  limits:
    memory: "512Mi"  → "1Gi"
    cpu: "500m"      → "1000m"
```

## Part 3: GitOps Workflow

### Standard Git-to-Kubernetes Flow

```
Developer
    ↓
Feature Branch (feature/k8s-*)
    ↓
Code Review (YAML validation)
    ↓
Merge to main
    ↓
Git webhook triggered
    ↓
ArgoCD/Flux detects change
    ↓
Apply manifests to cluster
    ↓
Kubernetes reconciliation
    ↓
✅ Deployed
```

### Pull Request Checklist for IaC

```
✅ YAML syntax valid (kubeval)
✅ Kubernetes API schema validation
✅ Resource limits reasonable
✅ Image tags specified (no "latest")
✅ Security context defined
✅ Health checks configured
✅ Documentation updated
✅ Reviewed by ops team
```

## Part 4: YAML Best Practices Demonstrated

### 1. Labels for Organization
```yaml
labels:
  app: cloud-optimizer
  version: v1.0
```

### 2. Resource Requests/Limits
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### 3. Health Checks
```yaml
livenessProbe:      # Restart if unhealthy
  httpGet:
    path: /health
    port: 5000
    
readinessProbe:     # Remove from LB if unhealthy
  httpGet:
    path: /health
    port: 5000
```

### 4. Security
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    readOnlyRootFilesystem: true
```

### 5. Configuration Management
```yaml
env:
- name: FLASK_ENV
  value: "production"
- name: PORT
  value: "5000"
```

## Part 5: Infrastructure Change Management

### Workflow: Adding New Feature

**Scenario:** Need to scale up due to increased traffic

```bash
# 1. Create feature branch
git checkout -b feature/k8s-scaling

# 2. Edit deployment.yaml
# Change replicas: 3 → 5
# Add HPA configuration

# 3. Validate YAML
kubeval k8s/deployment.yaml

# 4. Test locally
kubectl apply -f k8s/ --dry-run=client

# 5. Commit and push
git add k8s/
git commit -m "feature/k8s-scaling: Increase replicas from 3 to 5 and add HPA"
git push origin feature/k8s-scaling

# 6. Create pull request
# Team reviews YAML changes
# Approvals required

# 7. Merge to main
git merge feature/k8s-scaling

# 8. GitOps operator detects change
# Automatically applies to cluster
```

### Rollback Strategy

If something goes wrong:

```bash
# 1. Identify bad commit
git log --oneline k8s/

# 2. Revert the change
git revert <bad-commit>
git push origin main

# 3. GitOps operator detects revert
# Automatically rolls back deployment

# Alternative: Direct kubectl
kubectl rollout undo deployment/cloud-optimizer
```

## Part 6: Scaling Changes in Detail

### Before
```yaml
replicas: 3
# No HPA - manual scaling only
```

### After
```yaml
replicas: 5  # Baseline increased

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cloud-optimizer-hpa
spec:
  scaleTargetRef:
    kind: Deployment
    name: cloud-optimizer
  minReplicas: 2      # Never scale below 2
  maxReplicas: 10     # Never scale above 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        averageUtilization: 70  # Scale up at 70% CPU
  - type: Resource
    resource:
      name: memory
      target:
        averageUtilization: 80  # Scale up at 80% memory
```

## Part 7: Ingress Security Enhancements

### Before
```yaml
annotations:
  kubernetes.io/ingress.class: nginx
  cert-manager.io/cluster-issuer: letsencrypt-prod
  nginx.ingress.kubernetes.io/rate-limit: "100"
```

### After (Enhanced)
```yaml
annotations:
  # Existing
  kubernetes.io/ingress.class: nginx
  cert-manager.io/cluster-issuer: letsencrypt-prod
  nginx.ingress.kubernetes.io/rate-limit: "100"
  
  # Security enhancements
  nginx.ingress.kubernetes.io/ssl-redirect: "true"
  nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
  nginx.ingress.kubernetes.io/enable-cors: "true"
  nginx.ingress.kubernetes.io/cors-allow-origin: "*"
  nginx.ingress.kubernetes.io/enable-modsecurity: "true"
```

### Multi-Domain Support
```yaml
tls:
- hosts:
  - cloud-optimizer.example.com
  - api.cloud-optimizer.example.com      # NEW: API subdomain
  secretName: cloud-optimizer-tls

rules:
- host: cloud-optimizer.example.com
  http:
    paths:
    - path: /
      backend:
        service:
          name: cloud-optimizer
          port:
            number: 80
            
- host: api.cloud-optimizer.example.com   # NEW: Separate API ingress
  http:
    paths:
    - path: /
      backend:
        service:
          name: cloud-optimizer
          port:
            number: 80
```

## Part 8: GitOps Operators

### ArgoCD (Most Popular)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cloud-optimizer
spec:
  project: default
  source:
    repoURL: https://github.com/A96-45/cloud-engineering-challenge
    targetRevision: main
    path: k8s/
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Flux (Alternative)
```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta1
kind: GitRepository
metadata:
  name: cloud-optimizer
spec:
  interval: 1m
  url: https://github.com/A96-45/cloud-engineering-challenge
  ref:
    branch: main

---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta1
kind: Kustomization
metadata:
  name: cloud-optimizer
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: cloud-optimizer
  path: ./k8s/
```

## Key Concepts Demonstrated

✅ Infrastructure as Code (IaC)
✅ Version control for infrastructure
✅ Code review for infrastructure changes
✅ Declarative configuration
✅ GitOps automation
✅ Multi-tier deployment (Deployment, Service, Ingress)
✅ Scaling strategies (manual + automatic)
✅ Security best practices
✅ Health check configuration
✅ Resource management

## Real-World Improvements

### For Production
```
Add: NetworkPolicies for pod-to-pod communication
Add: PodDisruptionBudgets for high availability
Add: RBAC for access control
Add: Namespace isolation
Add: Monitoring/Observability (Prometheus, Grafana)
Add: Backup/Disaster Recovery
Add: Pod Security Policies
Add: ConfigMaps for application config
Add: Secrets for sensitive data
```

### Validation Tools
```bash
# YAML syntax validation
kubeval k8s/

# Kubernetes schema validation
kubectl apply -f k8s/ --dry-run=client

# Security scanning
kubesec scan k8s/deployment.yaml

# Policy enforcement
kyverno apply k8s/
```

## Exercise Completion

✅ Created base Kubernetes manifests (Deployment, Service, Ingress)
✅ Implemented scaling feature branch
✅ Implemented ingress enhancement feature
✅ Implemented resource limits feature
✅ Demonstrated YAML best practices
✅ Explained GitOps workflow
✅ Documented infrastructure changes
✅ Showed rollback strategies
✅ Provided real-world enhancements

---
