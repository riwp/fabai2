#!/bin/bash

# Define the services
services=("fabai_aiwebui.service" "fabai_get_ai_insights.service")

# Loop through each service
for service in "${services[@]}"; do
  echo "Copying $service to /etc/systemd/system/"
  
  # Use full path for source files, change to your actual source directory if needed
  src_file="./$service"  # Assuming the script runs in the directory where the .service files are located

  # Check if the source file exists
  if [ -f "$src_file" ]; then
    sudo cp "$src_file" /etc/systemd/system/
    
    # Check if cp was successful
    if [ $? -eq 0 ]; then
      echo "$service copied successfully."
    else
      echo "Failed to copy $service. Please check your permissions or the destination."
    fi
  else
    echo "Source file $src_file does not exist. Please check the path."
  fi
done

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Done. Now modify user configured in service files commands below:"

echo "sudo nano fabai_aiwebui.service"
echo "sudo nano fabai_get_ai_insights.service"