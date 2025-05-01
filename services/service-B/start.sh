#!/bin/bash
echo "Starting service B..."
cd /home/ctf/services/service-B
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
