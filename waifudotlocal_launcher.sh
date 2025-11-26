#!/bin/bash
# Uncomment the commented lines if you're using TLS + Gunicorn
NAME="waifudotlocal"
VENVDIRECTORY="/home/tim/waifu-dot-local/.venv/"
CONNECTIONS=4
IPADDR="0.0.0.0:8000"
#IPADDR="0.0.0.0:8443"
#SSLCERT="waifu.crt"
#SSLKEY="waifu.key"

echo "Launching waifudotlocal service"

cd $VENVDIRECTORY
source bin/activate
gunicorn -w $CONNECTIONS -b $IPADDR 'waifudotlocal:create_app()'
#gunicorn --certfile=$SSLCERT --keyfile=$SSLKEY -w $CONNECTIONS -b $IPADDR 'waifudotlocal:create_app()'