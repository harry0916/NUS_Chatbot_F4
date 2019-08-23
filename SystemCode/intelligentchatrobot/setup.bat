conda.exe create -n safari python=3.6
conda.exe activate safari

echo "Installing dependencies packages..."
pip.exe install -r requirements.txt

cd src
python.exe app.py
