#!/bin/bash

CURDIR=${PWD} 

source $CURDIR/.venv/bin/activate

python r2rpull-remote.py

deactivate 

echo Archiving process has ended. Confirm backup present in sciget. 