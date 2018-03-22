
**sbgntikz** is a [tikz](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) library that allows drawing [SBGN maps](sbgn.org) directly into Latex using the powerfull [tikz](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) package.

## Installation

The file `tikzlibrarysbgn.code.tex` should be copied to a directory where it can be found by the tex engine:
* in the directory of your tex source file
* in your local `texmf` directory (`/home/<user>/texmf/` under Linux, `/Users/Library/texmf/` under MacOS).

## Getting started

**sbgntikz** is a tikz package.
Usually, tikz is installed within your tex distribution, so it can be used directly into your latex file.
The two first steps are to import the tikz package and the sbgntikz library:

```tex
\usepackage{tikz}
\usetikzlibrary{sbgn}
```
