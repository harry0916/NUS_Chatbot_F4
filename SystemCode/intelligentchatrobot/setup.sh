#!/bin/bash
conda create -n safari --yes
conda activate safari --yes

pip install -r requirements.txt
python -m spacy download en_core_web_md

cd src && python app.py
