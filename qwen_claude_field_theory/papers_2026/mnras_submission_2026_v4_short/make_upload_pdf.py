#!/usr/bin/env python3
"""make_upload_pdf.py -- builds the ScholarOne upload PDF with the corresponding author's e-mail typeset in.
The address is read from ../mnras_submission_2026_v3/author_private.tex (git-ignored) and written ONLY into the git-ignored
upload_bundle/ of this folder; the tracked .tex and .pdf keep the placeholder.  Refuses to run if the numbers checks fail.
Run:  python3 make_upload_pdf.py
"""
import os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
priv = open(os.path.join(HERE, "..", "mnras_submission_2026_v3", "author_private.tex")).read()
m = re.search(r"\\newcommand\{\\authoremail\}\{([^}]*)\}", priv)
if not m or "@" not in m.group(1):
    sys.exit("no e-mail found in author_private.tex")
if subprocess.run([sys.executable, os.path.join(HERE, "short_numbers.py")], capture_output=True).returncode != 0:
    sys.exit("short_numbers.py has failing checks; not building the upload PDF")
out = os.path.join(HERE, "upload_bundle"); build = os.path.join(out, "build")
os.makedirs(build, exist_ok=True)
tex = open(os.path.join(HERE, "mnras_a0_lambda_short.tex")).read()
placeholder = r"\newcommand{\authoremail}{address supplied at submission}"
assert tex.count(placeholder) == 1
open(os.path.join(build, "mnras_a0_lambda_short.tex"), "w").write(tex.replace(placeholder, r"\newcommand{\authoremail}{%s}" % m.group(1)))
for f in ("references.bib", "fig1_laws_amplification.pdf"):
    shutil.copy(os.path.join(HERE, f), build)
r = subprocess.run(["tectonic", "--keep-intermediates", "mnras_a0_lambda_short.tex"], cwd=build, capture_output=True, text=True)
pdf = os.path.join(build, "mnras_a0_lambda_short.pdf")
if not os.path.exists(pdf):
    sys.exit("build failed:\n" + r.stderr[-1500:])
shutil.copy(pdf, os.path.join(out, "01_manuscript_for_review.pdf"))
shutil.copy(os.path.join(HERE, "ALT_TEXT.txt"), os.path.join(out, "04_alt_text_for_figures.txt"))
text = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
print("email typeset in PDF:", m.group(1) in text.replace("\n", ""), "| placeholder gone:", "address supplied at submission" not in text)
print("pages:", [l for l in subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")])
print("size (MB): %.2f" % (os.path.getsize(pdf) / 1e6))
