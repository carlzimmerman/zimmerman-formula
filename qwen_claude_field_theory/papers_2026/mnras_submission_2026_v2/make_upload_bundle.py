#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
make_upload_bundle.py -- writes upload_bundle/ (git-ignored): everything that is pasted or uploaded at ScholarOne.

The corresponding author's e-mail is deliberately absent from the repository.  Put it in a one-line file next to this
script, author_private.tex, which is git-ignored:

    \newcommand{\authoremail}{name@example.org}

Then run:  python3 make_upload_bundle.py
It (1) checks the e-mail is set, (2) builds a copy of the manuscript with the e-mail typeset INSIDE upload_bundle/build
(the tracked .tex and .pdf never contain it), (3) refuses to continue
if the build fails, the PDF exceeds 10 MB, the abstract exceeds 250 words, or paper_numbers.py has a failing check,
and (4) writes:

    upload_bundle/01_manuscript_for_review.pdf     the single file MNRAS wants at first submission
    upload_bundle/02_title_abstract_keywords.txt   plain text for the web form
    upload_bundle/03_cover_letter.txt              with the signature block completed
    upload_bundle/04_alt_text_for_figures.txt      required for every figure at submission
    upload_bundle/05_source_for_acceptance.zip     flattened .tex (+ .bbl, .bib, fig1.pdf ... fig5.pdf, readme); only
                                                   needed after acceptance
"""
import os, re, sys, shutil, subprocess, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "upload_bundle")
TEX = os.path.join(HERE, "mnras_a0_lambda_v2.tex")
PRIV = os.path.join(HERE, "author_private.tex")
def die(msg): print("STOP: " + msg); sys.exit(1)

# ---- 1. the e-mail
if not os.path.exists(PRIV): die("author_private.tex is missing; see the docstring of this script.")
m = re.search(r"\\newcommand\{\\authoremail\}\{([^}]+)\}", open(PRIV).read())
if not m or "@" not in m.group(1): die("author_private.tex does not define \\authoremail with an e-mail address.")
EMAIL = m.group(1).strip()

# ---- 2. numbers must pass, then build (the build is gated: no bundle from a stale or failed PDF)
r = subprocess.run([sys.executable, os.path.join(HERE, "paper_numbers.py")], capture_output=True, text=True)
if r.returncode != 0: die("paper_numbers.py has failing checks:\n" + r.stdout[-600:])
# the e-mail-bearing copy is built inside the git-ignored bundle, never next to the tracked source
figs = ["fig1_rar.pdf", "fig2_kappa.pdf", "fig_deep.pdf", "fig3_laws.pdf", "fig4_amplification.pdf", "fig5_rc100.pdf"]   # manuscript Figures 1-6, in order
PLACEHOLDER = r"\newcommand{\authoremail}{address supplied at submission}"
src = open(TEX).read()
if PLACEHOLDER not in src: die("the placeholder e-mail line was not found in the .tex")
flat = src.replace(PLACEHOLDER, r"\newcommand{\authoremail}{" + EMAIL + "}")
for i, fg in enumerate(figs, 1): flat = flat.replace("{" + fg + "}", "{fig%d.pdf}" % i)
if os.path.isdir(OUT): shutil.rmtree(OUT)
BUILD = os.path.join(OUT, "build"); os.makedirs(BUILD)
open(os.path.join(BUILD, "mnras_a0_lambda_v2.tex"), "w").write(flat)
shutil.copy(os.path.join(HERE, "references.bib"), BUILD)
for i, fg in enumerate(figs, 1): shutil.copy(os.path.join(HERE, fg), os.path.join(BUILD, "fig%d.pdf" % i))
r = subprocess.run(["tectonic", "--keep-intermediates", "mnras_a0_lambda_v2.tex"], cwd=BUILD, capture_output=True, text=True)
PDF = os.path.join(BUILD, "mnras_a0_lambda_v2.pdf")
if r.returncode != 0 or not os.path.exists(PDF): die("tectonic build failed:\n" + r.stderr[-800:])
size_mb = os.path.getsize(PDF) / 1e6
if size_mb > 10: die(f"PDF is {size_mb:.1f} MB; MNRAS allows 10 MB for the manuscript file.")

# ---- 3. text for the web form
title = re.search(r"\\title\[[^\]]*\]\{(.+?)\}\n", src, re.S).group(1)
abstract = src[src.index(r"\begin{abstract}") + len(r"\begin{abstract}"):src.index(r"\end{abstract}")].strip()
keywords = src[src.index(r"\begin{keywords}") + len(r"\begin{keywords}"):src.index(r"\end{keywords}")].strip()
def plain(t):
    for a, b in ((r"c\sqrt{G\rho_\Lambda}", "c sqrt(G rho_Lambda)"), (r"\tfrac12", "(1/2)"), (r"\sqrt{G\rho_\Lambda}", "sqrt(G rho_Lambda)"), (r"\rho_\Lambda", "rho_Lambda"), (r"\kappa", "kappa"), (r"\Lambda", "Lambda"),
                 (r"\Omega_\Lambda", "Omega_Lambda"), (r"\times", "x"), (r"\pm", "+/-"), (r"\simeq", "~"), (r"\pi", "pi"), (r"\,", " "), ("--", "-"), (r"\ ", " "), ("~", " ")):
        t = t.replace(a, b)
    t = re.sub(r"\^\{([^}]*)\}", r"^\1", t); t = re.sub(r"_\{?\\rm\s*([A-Za-z]+)\}?", r"_\1", t); t = re.sub(r"_\{([^}]*)\}", r"_\1", t)
    t = t.replace("$", "").replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"[ \t]+", " ", t).strip()
nwords = len(re.sub(r"\\[a-zA-Z]+", "", re.sub(r"\$[^$]*\$", "X", abstract)).split())
if nwords > 250: die(f"abstract has about {nwords} words; the MNRAS limit is 250.")

ALT = [
 ("Figure 1", "Scatter plot of observed against baryonic acceleration for 2803 points in 164 SPARC galaxies on logarithmic axes. The points follow a single curved relation that joins the one-to-one line at high acceleration and lies above it at low acceleration. Three nearly identical model curves are overlaid, for acceleration scales of 1.19, 1.13 and 0.936 times ten to the minus ten metres per second squared. A lower panel shows that the curves differ from one another by at most 0.05 dex, inside a grey band marking the 0.14 dex scatter of the data."),
 ("Figure 2", "Three panels. Panel a: the fitted coefficient kappa falls steeply as the assumed stellar mass-to-light ratio of discs rises from 0.35 to 0.85, from 0.9 to 0.34 when measured against the cosmological-constant density and from 0.75 to 0.28 against the critical density; both curves cross one half inside the shaded population-synthesis range of 0.5 to 0.7. Panel b: two horizontal error bars, estimator A at 0.465 plus or minus 0.076 and estimator B at 0.55 plus or minus 0.17, overlap four vertical lines marking candidate coefficients at 0.461, 0.5, 0.557 and 0.583. Panel c: predicted acceleration scale against the Hubble constant for kappa of one half and of 0.461; the point for one half at the Planck Hubble constant and the point for 0.461 at the SH0ES Hubble constant lie at the same height."),
 ('Figure 3', "Two panels. Panel a: the logarithmic slope of observed against baryonic acceleration in the deep regime, plotted against the ratio of baryonic acceleration to the acceleration scale on a logarithmic axis from 0.003 to 0.25. A black curve, the slope predicted by the relation, rises slowly from 0.51 to 0.61. Four filled points with vertical error bars, the measured median per-galaxy slopes of SPARC at three disc mass-to-light ratios (0.62, 0.61 and 0.58, each plus or minus about 0.03) and of MIGHTEE-HI (0.60 plus or minus 0.08), sit just above open diamonds that mark the slope the relation predicts at the same points (0.56 to 0.58). Dotted horizontal lines at 0.75 and at 1, the Newtonian slope, lie well above all the points. Panel b: the coefficient kappa measured in the deep regime for nine cases, drawn as horizontal error bars against a solid vertical line at one half, a dashed line at 0.60 for the critical-density reading, and a grey band from 0.39 to 0.54 for estimator A. SPARC at disc ratios 0.5, 0.6 and 0.7 gives 0.60, 0.52 and 0.46. MIGHTEE-HI gives 0.89 in our fit and 0.90, 1.10 and 0.79 under three of the survey's own mass-to-light conventions, but 0.58 with a fixed K-band ratio of 0.6, next to the SPARC values. SPARC with mass-to-light ratios fitted to the rotation curves themselves gives 0.28, far to the left."),
 ("Figure 4", "Line plot of the logarithmic change of the acceleration scale against redshift from 0 to 4. A thick horizontal line at zero is the prediction of a scale anchored to the cosmological constant. A dashed curve, for a scale proportional to the Hubble rate, rises to 0.58 dex at redshift 2.5 and 0.8 dex at redshift 4. A solid curve with a grey band, for the scale that emerges from cold dark matter haloes, rises to 0.33 dex at redshift 2.5 with a band from 0.23 to 0.46. A dotted curve for a second halo scaling lies close to the dashed curve. A narrow band falling to minus 0.2 dex at redshift 4 shows a scale that follows an evolving dark-energy density. Two square markers at redshift 2.5, at 0 and at 0.33, carry error bars of 0.13 dex."),
 ("Figure 5", "Two curves of error amplification against the ratio of baryonic acceleration to the acceleration scale, on a logarithmic horizontal axis from 0.005 to 16. The amplification of kinematic errors starts at 2 and that of baryonic-mass errors at 1 at the lowest accelerations; both stay nearly flat below a ratio of 0.3, a region shaded and labelled as the proposed gate, and then rise steeply, passing 4 and 3 near a ratio of 1.5 and exceeding 10 beyond a ratio of 8. A grey band from 0.33 to 5.3 marks where the RC100 galaxies lie."),
 ("Figure 6", "Scatter plot of the inferred acceleration scale against redshift from 0.6 to 2.5 for 99 galaxies, spread over nearly two dex vertically. Points are coloured by the acceleration at which each galaxy is measured: galaxies measured at low acceleration lie high in the plot and those at high acceleration lie low. A fitted straight line declines gently, by 0.11 plus or minus 0.06 dex per unit redshift. Two thin rising lines show the halo-emergent prediction and the prediction of a scale proportional to the Hubble rate."),
]

# ---- 4. write the bundle
shutil.copy(PDF, os.path.join(OUT, "01_manuscript_for_review.pdf"))
with open(os.path.join(OUT, "02_title_abstract_keywords.txt"), "w") as f:
    f.write("TITLE\n" + plain(title) + "\n\nRUNNING HEAD\nThe a0-Lambda relation and its redshift test\n\n")
    f.write(f"ABSTRACT (about {nwords} words; limit 250)\n" + plain(abstract) + "\n\n")
    f.write("KEYWORDS (six, all from the MNRAS list)\n" + plain(keywords) + "\n\n")
    f.write("ARTICLE TYPE\nPaper (Main Journal)\n\nCORRESPONDING AUTHOR\nCarl P. Zimmerman, Briar Creek Tech, USA; " + EMAIL + "; ORCID 0009-0008-3508-7982\n\n")
    f.write("FUNDING\nNone.\n\nCONFLICT OF INTEREST\nNone.\n\nDATA AVAILABILITY\nStatement included in the manuscript (public repository; SPARC; Nestor Shachar et al. 2023; MIGHTEE-HI points digitised from Varasteanu et al. 2025).\n")
cl = open(os.path.join(HERE, "COVER_LETTER.md")).read()
body = cl.split("\n---\n")[1].strip()
with open(os.path.join(OUT, "03_cover_letter.txt"), "w") as f:
    f.write(body + "\n" + EMAIL + "\n")
with open(os.path.join(OUT, "04_alt_text_for_figures.txt"), "w") as f:
    for k, v in ALT: f.write(k + "\n" + v + "\n\n")
with zipfile.ZipFile(os.path.join(OUT, "05_source_for_acceptance.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("mnras_a0_lambda_v2.tex", flat)
    z.write(os.path.join(HERE, "references.bib"), "references.bib")
    bbl = os.path.join(BUILD, "mnras_a0_lambda_v2.bbl")
    if os.path.exists(bbl): z.write(bbl, "mnras_a0_lambda_v2.bbl")
    for i, fg in enumerate(figs, 1): z.write(os.path.join(HERE, fg), "fig%d.pdf" % i)
    z.writestr("readme.txt", "MNRAS source files. Main file: mnras_a0_lambda_v2.tex (class mnras.cls, natbib, mnras.bst). Bibliography: mnras_a0_lambda_v2.bbl "
               "(generated from references.bib). Figures: fig1.pdf to fig6.pdf, one per file, vector PDF. Build: pdflatex, bibtex, pdflatex, pdflatex.\n")
print(f"bundle written to {OUT}")
print(f"  PDF {size_mb:.2f} MB; abstract about {nwords} words; e-mail typeset; {len(figs)} figures; alt text for each.")
