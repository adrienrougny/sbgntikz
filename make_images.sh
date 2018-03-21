mkdir -p figures/pdf/pd
mkdir -p figures/pdf/af
mkdir -p figures/png/pd
mkdir -p figures/png/af
pdflatex --shell-escape highlights.tex
find ./figures/pdf/pd -iname '*.pdf' -exec mogrify -format png -density 300 -quality 100 figures/png/pd/{} +
find ./figures/pdf/af -iname '*.pdf' -exec mogrify -format png -density 300 -quality 100 figures/png/pd/{} +
