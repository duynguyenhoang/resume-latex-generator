#!/bin/bash

touch /data/output/resume.tex
python /app/render.py "$@"
pdflatex  -output-directory /data output/resume.tex
