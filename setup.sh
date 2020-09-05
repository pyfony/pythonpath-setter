#!/bin/bash -e

python3 -m venv $PWD/.venv

INSTALL_DIR="$PWD"
PYTHON_EXECUTABLE="$PWD/.venv/bin/python3"

echo "Installing boto3"
$PYTHON_EXECUTABLE -m pip install --upgrade boto3

echo "Setting up crontab"
(crontab -l 2>/dev/null; echo "0 5 * * * AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} $PYTHON_EXECUTABLE "$INSTALL_DIR/backup.py" >/dev/null 2>&1") | crontab -

echo "All done, check crontab by calling crontab -e"
