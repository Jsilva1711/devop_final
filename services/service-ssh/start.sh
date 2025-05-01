#!/bin/bash
echo "Starting service ssh..."
cd /home/ctf/services/service-ssh
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
