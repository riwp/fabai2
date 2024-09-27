#!/bin/bash

# Define the services
services=("fabai_aiwebui.service" "fabai_get_ai_insights.service")

# Loop through each service, stop and disable it, then remove it
for service in "${services[@]}"; do
  echo "Stopping $service..."
  sudo systemctl stop $service
  
  echo "Disabling $service..."
  sudo systemctl disable $service
  
  echo "Removing $service..."
  sudo rm /etc/systemd/system/$service
  
  echo "Reloading systemd daemon..."
  sudo systemctl daemon-reload
  
  echo "$service has been stopped, disabled, and removed."
done

echo "Done."
