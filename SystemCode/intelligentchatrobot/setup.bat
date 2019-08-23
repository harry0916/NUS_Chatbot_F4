@set name = safari 
@conda.exe create -n %name% python=3.6 -y -f
@CALL activate %name%

@python.exe -m pip install --upgrade pip
@echo "Installing dependencies packages..."
@pip.exe install -r requirements.txt
@python.exe -m spacy download en_core_web_md

@cd src
@python.exe app.py
@cd ..