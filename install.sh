#!/bin/bash
sudo apt update

sudo apt install python3
sudo apt install pip
python3 -m pip install --user virtualenv
python3 -m venv venv
source venv/bin/activate
echo $(which python)

pip install -r requirements.txt

echo "#!/bin/bash
echo 'starting...'
source venv/bin/activate
result=$(which python)
echo $result
python3 book_parser.py
echo 'cloasing....'
deactivate" > PDF_Parser.sh

chmod +x PDF_Parser.sh

deactivate
