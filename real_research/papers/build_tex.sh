#!/bin/bash
# Rebuild ZIMMERMAN_THEORY_OF_GRAVITY.tex AND .pdf from the .md.   Usage:  bash build_tex.sh
# Notes:
#  - figure paths are made bare (+ \graphicspath) so images resolve in figures/ OR the project root
#  - pandoc's alt= is stripped (older graphicx rejects it)
#  - the .md source uses ASCII for primes/fractions (V', 1/2, 1/4) so XeTeX/unicode-math is happy
set -e
cd "$(dirname "$0")"
grep -q graphicspath unicode_header.tex || printf '\\graphicspath{{figures/}{./}}\n' >> unicode_header.tex
pandoc ZIMMERMAN_THEORY_OF_GRAVITY.md -s --include-in-header=unicode_header.tex -o ZIMMERMAN_THEORY_OF_GRAVITY.tex
sed -i '' -e 's/,alt=\{[^}]*\}//g' -e 's#\(\\includegraphics\[[^]]*\]{\)figures/#\1#g' ZIMMERMAN_THEORY_OF_GRAVITY.tex
echo "tex rebuilt."
if command -v tectonic >/dev/null; then
  tectonic ZIMMERMAN_THEORY_OF_GRAVITY.tex && echo "PDF built: ZIMMERMAN_THEORY_OF_GRAVITY.pdf"
else
  echo "tectonic not installed — upload the .tex + figures/ to Overleaf (XeLaTeX) for the PDF."
fi
