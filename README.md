# Resume Latex Generator

LaTeX CV Generator using Jinja2

Based off of
- [jakegut/resume](https://github.com/jakegut/resume)
- [mdauthentic/latex-cv-gen](https://github.com/mdauthentic/latex-cv-gen)


## How to use

> To get hep, use python render.py --help

Following step is required once you are new here

```bash
cp resources/resume-example.yaml resources/resume.yaml
# You should modify it and store it permanently for future use
python render.py resources/resume.yaml
docker build -t latex-resume .
docker run --rm -i -v "$PWD":/data latex-resume pdflatex -output-directory output output/resume.tex
```

**If you modify and would like to generate pdf again**

```sh
python render.py resources/resume.yaml && docker run --rm -i -v "$PWD":/data latex-resume pdflatex -output-directory output output/resume.tex
```

## TODO

- [ ] Pack everything to Docker image
