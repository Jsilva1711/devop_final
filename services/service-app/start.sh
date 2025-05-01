#!/bin/bash
echo "Starting service app..."
cd /home/ctf/services/service-app
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
