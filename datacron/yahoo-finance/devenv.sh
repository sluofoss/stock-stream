rm -rf ./devenv
python -m venv ./devenv
source ./devenv/bin/activate
echo "start installing"
pip install -r ./requirements.txt -q
echo "finished installing"