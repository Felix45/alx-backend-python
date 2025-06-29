#!/bin/bash

set -e

DEPLOYMENT="messaging_app_blue"
SERVICE_NAME="messaging_app_service"

echo "Applying updated deployment with image version 2.0..."
kubectl apply -f blue_deployment.yaml

echo "Monitoring rollout status..."
kubectl rollout status deployment/$DEPLOYMENT

echo "Starting curl requests to test for downtime..."
kubectl port-forward service/$SERVICE_NAME 8000:8000 &
PORT_PID=$!

sleep 5  

for i in {1..20}; do
  response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
  timestamp=$(date +"%T")
  echo "$timestamp - HTTP Status: $response"
  sleep 1
done

echo "Stopping port-forward..."
kill $PORT_PID

echo "Current running pods:"
kubectl get pods -l version=blue
