echo $(which python)
echo $(python -V)
python -m venv venv
source venv/bin/activate
echo $(which pip)
pip install discretisedfield pytest
pip install -e ../.
pytest 
deactivate
rm -r venv
