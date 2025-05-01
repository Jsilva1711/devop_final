#!/bin/bash
echo "Starting service A..."
cd /home/ctf/services/service-A
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
