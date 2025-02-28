#!/bin/bash
script_dir=$(cd $(dirname $0); pwd)
cd $script_dir
source .venv/bin/activate
python cal.py
