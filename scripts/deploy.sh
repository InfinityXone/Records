#!/bin/bash

# Deploy Infinity X One components to Kubernetes
#
# This script assumes you have built and pushed the following images to
# your container registry:
#   - yourdockerregistry/infinity-handshake-server:latest
#   - yourdockerregistry/infinity-worker:latest
#
# It creates a Kubernetes secret from your environment file and applies
# the manifests.  Adjust paths and registry names as needed.

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 path/to/env/file"
  echo "The env file should contain your Supabase keys, Vercel hook and other secrets."
  exit 1
fi

ENV_FILE="$1"

NAMESPACE="infinity-x-one"

echo "Creating Kubernetes secret from env file..."
kubectl delete secret infinityx-env -n "$NAMESPACE" --ignore-not-found || true
kubectl create secret generic infinityx-env -n "$NAMESPACE" --from-env-file="${ENV_FILE}"

echo "Applying Kubernetes manifests..."
kubectl apply -f ../k8s/namespace.yaml
kubectl apply -f ../k8s/env-secret.yaml
kubectl apply -f ../k8s/agent-deployment.yaml
kubectl apply -f ../k8s/backend-service.yaml
kubectl apply -f ../k8s/ingress.yaml

# Legacy manifests for handshake server and workers remain for backward compatibility.
if [ -f ../k8s/handshake-server.yaml ]; then
  kubectl apply -f ../k8s/handshake-server.yaml
fi
if [ -f ../k8s/workers.yaml ]; then
  kubectl apply -f ../k8s/workers.yaml
fi
if [ -f ../k8s/cronjobs.yaml ]; then
  kubectl apply -f ../k8s/cronjobs.yaml
fi

echo "Deployment complete.  Monitor your pods with:\n  kubectl get pods -n $NAMESPACE"