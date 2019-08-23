@echo off
set name=safari
set pwd=%cd%
set ngrok_dir=%USERPROFILE%\ngrok
call conda create -n %name% python=3.6 -y -f
CALL activate %name%

python.exe -m pip install --upgrade pip

echo
echo Installing dependencies packages...
pip.exe install -r requirements.txt
python.exe -m spacy download en_core_web_md

echo
echo "Installing ngrok service..."
md "%ngrok_dir%"
cd /d %ngrok_dir%
certutil -urlcache -split -f https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip
unzip ngrok-stable-windows-amd64.zip
set PATH=%PATH%;%ngrok_dir%

cd /d %pwd%\src

echo "Running backend app..."
python.exe app.py
cd ..
