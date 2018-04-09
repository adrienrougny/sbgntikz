
*sbgntikz* is a [TikZ](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) library that allows drawing [SBGN maps](sbgn.org) directly into LaTex using the powerfull [TikZ](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) package.
All three SBGN languages (PD, AF and ER) are supported.

## Installation

The directory `tikz-sbgn` should be copied to a directory where it can be found by the Tex engine:
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

```tex
\begin{tikzpicture}[node distance = 1.5cm]
    %ERK
    \node[macromolecule] (erk) {ERK};
    \node[sv] (sv-erk) at (erk.120) {};
    %process
    \node[genericprocess, connectors = horizontal, right = of erk] (p) {};
    %p-ERK
    \node[macromolecule, right = of p] (perk) {ERK};
    \node[sv] (sv-erk) at (perk.120) {P};
    %atp
    \node[simplechemical, below left = of p] (atp) {ATP};
    %adp
    \node[simplechemical, below right = of p] (adp) {ADP};
    %p-MEK
    \node[macromolecule, above = 2cm of p] (pmek) {MEK};
    \node[sv] at (pmek.120) {P};
    %arcs
    \draw[consumption] (erk) -- (p.west);
    \draw[consumption] (atp) to [bend left=40] (p.west);
    \draw[production] (p.east) -- (perk);
    \draw[production] (p.east) to [bend left=40] (adp);
    \draw[catalysis] (pmek) -- (p);
\end{tikzpicture}
```
