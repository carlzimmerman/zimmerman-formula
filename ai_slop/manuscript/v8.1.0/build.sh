#!/bin/bash
# Build script for Z² Framework manuscript v8.1.0
# Requires: pdflatex or xelatex with amsmath, physics packages

set -e

echo "Building Z² Framework Manuscript v8.1.0..."

# Run pdflatex twice for references/TOC
pdflatex -interaction=nonstopmode zimmerman_formula_v8.1.0.tex
pdflatex -interaction=nonstopmode zimmerman_formula_v8.1.0.tex

# Clean auxiliary files
rm -f *.aux *.log *.out *.toc

echo "Done! Output: zimmerman_formula_v8.1.0.pdf"
