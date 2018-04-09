
*sbgntikz* is a [tikz](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) library that allows drawing [SBGN maps](sbgn.org) directly into LaTex using the powerfull [TikZ](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) package.

## Installation

The file `tikzlibrarysbgn.code.tex` should be copied to a directory where it can be found by the Tex engine:
* in the directory of your Tex source file
* in your local `texmf` directory (`/home/<user>/texmf/` under Linux, `/Users/Library/texmf/` under MacOS).

## Getting started

*sbgntikz* is a TikZ package.
Usually, TikZ is installed within your Tex distribution, so it can be imported directly into your LaTex source file.
The two first steps are to import the TikZ package and the *sbgntikz* library:

```tex
\usepackage{tikz}
\usetikzlibrary{sbgn}
```
SBGN maps can then be straightforwardly drawn using a `tikzpicture` environment:

```tex
\begin{tikzpicture}
  % tikz code to draw an SBGN map
\end{tikzpicture}
```

Nodes and nodes attributes can be drawn using the TikZ `\node` command, while arcs can be drawn using the `\draw` or `edge` commands.
The type of glyph to be drawn is specified using a keyword that is the name of the type (e.g `macromolecule` for the macromolecule glyph, `necessarystimulation` for the necessary stimulation glyph).
Here is a small example:

```
To be written
```
