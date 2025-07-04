@echo off
flake8 . --format=html --htmldir=flake8_report
echo Rapport HTML généré dans flake8_report\index.html
pause
