#!/bin/bash
# Azure Web App (Linux) startup script
# Wird in Azure Portal unter: Konfiguration > Allgemeine Einstellungen > Startbefehl hinterlegt:
#   bash startup.sh
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=2 app:app
