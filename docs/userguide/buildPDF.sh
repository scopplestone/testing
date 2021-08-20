python3 -m sphinx -b latex -D language=en -d _build/doctrees . _build/latex

cd _build/latex

latexmk -r latexmkrc -pdf -f -dvi- -ps- -jobname=piclas -interaction=nonstopmode
