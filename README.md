*sbgntikz* is a [Ti*k*Z](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) library that allows drawing [SBGN maps](http://www.sbgn.org) directly into LaTeX using the powerfull [Ti*k*Z](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) package.
All three SBGN languages (PD, AF and ER) are supported.
A complete documentation for the latest version is available [here](https://github.com/Adrienrougny/sbgntikz/blob/master/documentation/v1.1/sbgntikz_v1_1.pdf), as well as a set of [examples](https://github.com/Adrienrougny/sbgntikz/tree/master/examples).

## Installation

The directory `tikz-sbgn` should be copied to a directory where it can be found by your TeX engine:
* in the directory of your TeX source file or
* in a local `texmf` directory, whose location depends on the OS you are using:
  * Linux: in `/home/<user>/texmf/tex/generic/pgf/`. The index must then be updated using the `texhash /home/<user>/texmf` command.
  * MacOs: in `/Users/Library/texmf/tex/generic/pgf/`.
  * Windows: in `C:\Users\<user>\texmf\`. In the case you are using MikTeX you will need to add this directory to the TEXMF root directories in the `Directories` tab of the `Settings` page. 

Ti*k*Z should already be installed within your TeX distribution.
If not, you may install it via your TeX distribution, or download the latest build [here](http://www.texample.net/tikz/builds/).

## Getting started

*sbgntikz* is a Ti*k*Z package.
Usually, Ti*k*Z is installed within your TeX distribution, so it can be imported directly into your LaTeX source file.
The two first steps are to import the Ti*k*Z package and the *sbgntikz* library:

```tex
\usepackage{tikz}
\usetikzlibrary{sbgn}
```
SBGN maps can then be straightforwardly drawn using a `tikzpicture` environment together with the `sbgn` key:

```tex
\begin{tikzpicture}[sbgn]
  % tikz code to draw an SBGN map
\end{tikzpicture}
```

Nodes and nodes attributes can be drawn using the Ti*k*Z `\node` command, while arcs can be drawn using the `\draw` command.
The type of glyph to be drawn is specified using a keyword that is the name of the type (e.g `macromolecule` for the macromolecule glyph, `necessary stimulation` for the necessary stimulation glyph).
Here is a small SBGN PD example:

```tex
\usetikzlibrary{positioning} %for relative positioning

\begin{tikzpicture}[sbgn]
    %ERK
    \node[macromolecule] (erk) {ERK};
    \node[sv] at (erk.120) {};
    %process
    \node[generic process, connectors = horizontal, right = of erk] (p) {};
    %p-ERK
    \node[macromolecule, right = of p] (perk) {ERK};
    \node[sv] at (perk.120) {P};
    %atp
    \node[simple chemical, below left = of p] (atp) {ATP};
    %adp
    \node[simple chemical, below right = of p] (adp) {ADP};
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

Here is the rendering:

![alt text](https://github.com/Adrienrougny/sbgntikz/blob/master/example.png)

## SBGN-ML to SBGNTi*k*Z converter

SBGNTi*k*Z includes an [SBGN-ML](https://github.com/sbgn/sbgn/wiki/SBGN_ML) to Ti*k*Z [converter](https://github.com/Adrienrougny/sbgntikz/tree/master/converter).
Basic usage is as follows:

```shell
sbgnml2tikz.py [options] INPUT
```

All options can be listed using the following:

```shell
sbgnml2tikz.py --help
```
Examples of rendering using the converter are available [here](https://github.com/Adrienrougny/sbgntikz/tree/master/converter/examples/).
