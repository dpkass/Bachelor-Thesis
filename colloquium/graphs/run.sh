#!/bin/bash

# Usage: ./run.sh basefilename (without .tex extension)

filename="$1"
shortfn="${filename##*/}"
shortfn="${shortfn%.*}"

template="\documentclass[tikz, border=5pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{graphdrawing, graphs, arrows.meta, positioning}
\usegdlibrary{layered}
\begin{document}
\input{${filename}}
\end{document}"

echo $template > fig.tex && \
lualatex -shell-escape fig.tex && \
pdfcrop fig.pdf && \
magick convert -density 600 -transparent white fig-crop.pdf "${shortfn}.png" && \
rm fig.tex fig.pdf fig-crop.pdf texput.log fig.aux fig.log
