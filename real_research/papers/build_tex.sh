#!/bin/bash
# Rebuild the Overleaf-ready .tex from the .md.   Usage:  bash build_tex.sh
# Produces ZIMMERMAN_THEORY_OF_GRAVITY.tex that compiles on Overleaf with XeLaTeX OR pdfLaTeX,
# with the 8 figures resolving whether they sit in a figures/ folder or the project root.
cd "$(dirname "$0")"
# ensure the graphicspath fallback is in the header
grep -q graphicspath unicode_header.tex || printf '\\graphicspath{{figures/}{./}}\n' >> unicode_header.tex
# pandoc -> tex
pandoc ZIMMERMAN_THEORY_OF_GRAVITY.md -s --include-in-header=unicode_header.tex -o ZIMMERMAN_THEORY_OF_GRAVITY.tex
# Overleaf-compatibility fixes: drop pandoc's alt= (older graphicx rejects it) and the figures/ path prefix
python3 - <<'PY'
import re
f = "ZIMMERMAN_THEORY_OF_GRAVITY.tex"
t = open(f, encoding="utf-8").read()
t = re.sub(r",alt=\{[^}]*\}", "", t)
t = re.sub(r"(\\includegraphics\[[^\]]*\]\{)figures/", r"\1", t)
open(f, "w", encoding="utf-8").write(t)
print("rebuilt", f, "| figures:", t.count("\\includegraphics"), "| alt= left:", t.count("alt="))
PY
