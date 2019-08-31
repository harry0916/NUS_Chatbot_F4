@set name=safari_1

@call conda create -n %name% python=3.6 -y -f
@CALL activate %name%

@python.exe -m pip install --upgrade pip

@echo
@echo Installing dependencies packages...
pip.exe install -r requirements.txt
python.exe -m spacy download en_core_web_md

@cd src
@echo
@echo Running backend app...
@python.exe app.py
@cd ..
