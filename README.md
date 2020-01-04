# pytexpdf
Python module to generate cropped PDFs of LaTeX typeset strings.

## Usage

- Instantiate the `PyTexPdf` object. It only holds any packages you want to use.

- `UsePackage(package: str)` adds a package to the environment. It can be called multiple times to add multiple packages.

- `MakeTexPdf(texString: str, fileName="pytexpdf", isEqn=True) -> str` generates a PDF of the given `texString`.
	- `texString` is a LaTeX format string, e.g. `"\sin(2 \pi \omega t)"`
	-  `filename` is the output PDF file name. If none is given, the PDF will use generic names up to `pytexpdf9.pdf` before it gets upset with you.
	- `isEqn` determines to typeset the `texString` in LaTeX math mode or normal text mode. If not given, it assumes you want to typeset an equation, i.e. a math block.
	- The method returns the name of the output PDF

### Example

```python
import pytexpdf

texPdfEnv = pytexpdf.PyTexPdf()
texPdfEnv.UsePackage("amsmath")
texPdfEnv.MakeTexPdf(r"howdy \int_0^\infty f(x) \mathrm{d}x")
texPdfEnv.MakeTexPdf(r"howdy $\int_0^\infty f(x) \mathrm{d}x$", fileName="blurb", isEqn=False)
```

Provides the output:

[pytexpdf0.pdf](pytexpdf0.pdf) and  [blurb.pdf](blurb.pdf)

## Dependencies

- LaTeX distribution with pdflatex
- Python 3.x
- Linux and macOS
	- Pull request for Windows is welcome

## Difference between pytexpdf, PyLaTeX, and pytexit

- Pytexpdf generates cropped PDFs of a single LaTeX equation (or text) with a single function

- PyLaTeX generates a whole PDF document, headings and all, with several new classes and methods

- Pytexit converts a computable python equation to a typeset-able TeX equation

## Troubleshooting

Pytexpdf writes a .TEX file of the form,

```latex
\documentclass[border=1pt]{standalone}

% whatever packages you added

\begin{document}

$\displaystyle % used if isEqn=True
% your texString
$ % used if isEqn=True

\end{document}
```

and compiles the file with `pdflatex -interaction=nonstopmode`. This combination tends ignore parts or commands of the `texString` that it does not recognize and compiles anyway. Hopefully this will help you google your errors.