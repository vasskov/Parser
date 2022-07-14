#!/bin/bash
echo "starting..."
source venv/bin/activate
result=$(which python)
echo $result
python3 book_parser.py
echo "cloasing...."
deactivate
