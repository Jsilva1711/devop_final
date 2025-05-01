#!/bin/bash

# Define the services and teams
teams=("red-team" "fuchsia-team")
services=("service-A" "service-B")  # adjust names if different
ports=("5000" "5001")  # corresponding ports for service-A and service-B

# Write the Python script inline
python3 <<EOF
import requests

teams = ["red-team", "fuchsia-team"]
services = ["service-A", "service-B"]
ports = [5000, 5001]

for team in teams:
    for service, port in zip(services, ports):
        try:
            url = f"http://{team}:{port}"
            response = requests.get(url, timeout=2)
            if response.text.strip():
                status = "passed"
            else:
                status = "**FAILED**"
        except Exception:
            status = "**FAILED**"
        print(f"{team} : {service} : {status}")
EOF

