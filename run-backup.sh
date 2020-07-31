#!/bin/bash

cd /home/r2r-backup

source /home/r2r-backup/.venv/bin/activate

python /home/r2r-backup/r2rpull-remote.py

deactivate