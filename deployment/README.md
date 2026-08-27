# Deployment Notes

The root `docker-compose.yml` is the recommended local deployment.

For Kubernetes, the application can later be extended with:

- Deployment
- Service
- ConfigMap
- Secret
- Readiness probe
- Liveness probe
- Ingress
- HorizontalPodAutoscaler

This first version intentionally keeps Kubernetes manifests out of the initial project so the learning progression remains manageable.
