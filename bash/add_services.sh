#!/bin/bash

# Define the services
services=("fabai_aiwebui.service" "fabai_get_ai_insights.service")

# Loop through each service
for service in "${services[@]}"; do
  echo "Copying $service to /etc/systemd/system/..."
  sudo cp "$service" /etc/systemd/system/
  
  if [ $? -eq 0 ]; then
    echo "$service copied successfully."
  else
    echo "Failed to copy $service. Please check if the source file exists."
  fi
done

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Done."
