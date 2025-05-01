#!/bin/bash
echo "Starting service B..."
cd "$(dirname "$0")" || exit

source ./env/bin/activate

pip install -r requirements.txt

python app.py

