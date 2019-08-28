#!/bin/bash
conda create -n safari
conda activate safari

pip install -r requirements.txt
python -m spacy download en_core_web_md

cd src && python app.py
