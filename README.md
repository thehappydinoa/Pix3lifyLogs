# Pix3lifyLogs

Anonymous log sharing for Heroku

## Install Locally

Virtualenv Setup

    virtualenv venv -p python3

Install Requirements and Run

    pip install -r requirements.txt
    python server.py

## Uploading

    curl -T logs.tar.xz http://logs.pix3lify.com/submit
    # OR
    curl -F logs=@logs.tar.xz http://logs.pix3lify.com/submit
