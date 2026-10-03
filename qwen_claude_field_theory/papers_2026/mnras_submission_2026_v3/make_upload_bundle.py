#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
make_upload_bundle.py -- writes upload_bundle/ (git-ignored): everything that is pasted or uploaded at ScholarOne.

The corresponding author's e-mail is deliberately absent from the repository.  Put it in a one-line file next to this
script, author_private.tex, which is git-ignored:

    \newcommand{\authoremail}{name@example.org}
    \newcommand{\authororcid}{0000-0000-0000-0000}      (optional)

The author's name and affiliation are read from the manuscript's byline, so no tracked file other than the .tex names
the author.

Then run:  python3 make_upload_bundle.py
It (1) checks the e-mail is set, (2) builds a copy of the manuscript with the e-mail typeset INSIDE upload_bundle/build
(the tracked .tex and .pdf never contain it), (3) refuses to continue
if the build fails, the PDF exceeds 10 MB, the abstract exceeds 250 words (by a plain whitespace count AND with every
math span counted as one word), or paper_numbers.py has a failing check, (4) reads the PAPER6 switch of the .tex
(\papersixfalse / \papersixtrue; an owner decision, SUBMISSION_CHECKLIST.md TODO-PAPER6) and picks the matching paragraph
of COVER_LETTER.md, and (5) writes:

    upload_bundle/01_manuscript_for_review.pdf     the single file MNRAS wants at first submission
    upload_bundle/02_title_abstract_keywords.txt   plain text for the web form
    upload_bundle/03_cover_letter.txt              with the signature block completed
    upload_bundle/04_alt_text_for_figures.txt      required for every figure at submission
    upload_bundle/05_source_for_acceptance.zip     flattened .tex (+ .bbl, .bib, fig1.pdf ... fig6.pdf, readme); only
                                                   needed after acceptance
"""
import os, re, sys, shutil, subprocess, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "upload_bundle")
TEX = os.path.join(HERE, "mnras_a0_lambda_v3.tex")
PRIV = os.path.join(HERE, "author_private.tex")
def die(msg): print("STOP: " + msg); sys.exit(1)

# ---- 1. the e-mail
if not os.path.exists(PRIV): die("author_private.tex is missing; see the docstring of this script.")
m = re.search(r"\\newcommand\{\\authoremail\}\{([^}]+)\}", open(PRIV).read())
if not m or "@" not in m.group(1): die("author_private.tex does not define \\authoremail with an e-mail address.")
EMAIL = m.group(1).strip()
_tex0 = open(TEX).read()
_sw = re.findall(r"^\\papersix(true|false)\s*$", _tex0, re.M)
if len(_sw) != 1: die("the .tex must contain exactly one line \\papersixtrue or \\papersixfalse (the PAPER6 owner decision)")
PAPER6 = _sw[0] == "true"
_mo = re.search(r"\\newcommand\{\\authororcid\}\{([^}]+)\}", open(PRIV).read())
ORCID = _mo.group(1).strip() if _mo else ""            # optional second line of author_private.tex
_src0 = open(TEX).read()
AUTHOR = re.search(r"\\author\[[^\]]*\]\{([^$]+)\$", _src0).group(1).strip()            # the byline of the manuscript
AFFIL = re.search(r"^\$\^\{1\}\$([^}\n]+)\}", _src0, re.M).group(1).strip()        # the line "$^{1}$<affiliation>}"
SIGNATURE = AUTHOR + "\n" + AFFIL + ("\nORCID " + ORCID if ORCID else "")

# ---- 2. numbers must pass, then build (the build is gated: no bundle from a stale or failed PDF)
r = subprocess.run([sys.executable, os.path.join(HERE, "paper_numbers.py")], capture_output=True, text=True)
if r.returncode != 0: die("paper_numbers.py has failing checks:\n" + r.stdout[-600:])
import json
PN = json.load(open(os.path.join(HERE, "paper_numbers.json")))       # the alt text quotes the same numbers as the text
# the e-mail-bearing copy is built inside the git-ignored bundle, never next to the tracked source
figs = ["fig1_rar.pdf", "fig2_kappa.pdf", "fig_deep.pdf", "fig3_laws.pdf", "fig4_amplification.pdf", "fig5_rc100.pdf"]   # manuscript Figures 1-6, in order
PLACEHOLDER = r"\newcommand{\authoremail}{address supplied at submission}"
src = open(TEX).read()
if PLACEHOLDER not in src: die("the placeholder e-mail line was not found in the .tex")
flat = src.replace(PLACEHOLDER, r"\newcommand{\authoremail}{" + EMAIL + "}")
for i, fg in enumerate(figs, 1): flat = flat.replace("{" + fg + "}", "{fig%d.pdf}" % i)
if os.path.isdir(OUT): shutil.rmtree(OUT)
BUILD = os.path.join(OUT, "build"); os.makedirs(BUILD)
open(os.path.join(BUILD, "mnras_a0_lambda_v3.tex"), "w").write(flat)
shutil.copy(os.path.join(HERE, "references.bib"), BUILD)
for i, fg in enumerate(figs, 1): shutil.copy(os.path.join(HERE, fg), os.path.join(BUILD, "fig%d.pdf" % i))
r = subprocess.run(["tectonic", "--keep-intermediates", "mnras_a0_lambda_v3.tex"], cwd=BUILD, capture_output=True, text=True)
PDF = os.path.join(BUILD, "mnras_a0_lambda_v3.pdf")
if r.returncode != 0 or not os.path.exists(PDF): die("tectonic build failed:\n" + r.stderr[-800:])
size_mb = os.path.getsize(PDF) / 1e6
if size_mb > 10: die(f"PDF is {size_mb:.1f} MB; MNRAS allows 10 MB for the manuscript file.")

# ---- 3. text for the web form
title = re.search(r"\\title\[[^\]]*\]\{(.+?)\}\n", src, re.S).group(1)
abstract = src[src.index(r"\begin{abstract}") + len(r"\begin{abstract}"):src.index(r"\end{abstract}")].strip()
keywords = src[src.index(r"\begin{keywords}") + len(r"\begin{keywords}"):src.index(r"\end{keywords}")].strip()
def plain(t):
    for a, b in ((r"c\sqrt{G\rho_\Lambda}", "c sqrt(G rho_Lambda)"), (r"\tfrac12", "(1/2)"), (r"\sqrt{G\rho_\Lambda}", "sqrt(G rho_Lambda)"), (r"\rho_\Lambda", "rho_Lambda"), (r"\kappa", "kappa"), (r"\Lambda", "Lambda"),
                 (r"\Omega_\Lambda", "Omega_Lambda"), (r"\times", "x"), (r"\pm", "+/-"), (r"\simeq", "≈"), (r"\propto", " ∝ "), (r"\pi", "pi"), (r"\,", " "), ("--", "-"), (r"\ ", " "), ("~", " ")):
        t = t.replace(a, b)
    t = re.sub(r"\^\{([^}]*)\}", r"^\1", t); t = re.sub(r"_\{?\\rm\s*([A-Za-z]+)\}?", r"_\1", t); t = re.sub(r"_\{([^}]*)\}", r"_\1", t)
    t = t.replace("$", "").replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"[ \t]+", " ", t).strip()
nwords = len(re.sub(r"\\[a-zA-Z]+", "", re.sub(r"\$[^$]*\$", " X ", abstract)).split())     # every math span one word
nplain = len(abstract.split())                                                              # plain whitespace count
if max(nwords, nplain) > 250: die(f"abstract has {nplain} words by a plain count and {nwords} with math spans as words; the MNRAS limit is 250.")

_t = PN["S2"]["table"]; _M = PN["S3"]["meas"]; _sp = PN["S6"]["sparc"]; _kin = PN["S6"]["kinematic_ratios"]["amp"]["kappa_L"]
_bx = [PN["S3"]["box_A"], PN["S3"]["box_B"], PN["S3"]["box_C"]]
ALT = [
 ("Figure 1", "Scatter plot of observed against baryonic acceleration for 2803 points in 164 SPARC galaxies on logarithmic axes, with the Hubble-flow distances placed on a Hubble constant of 67.4. The points follow a single curved relation that joins the one-to-one line at high acceleration and lies above it at low acceleration. Three nearly identical model curves are overlaid, for acceleration scales of " + f"{_t[1]['a0']/1e-10:.2f}" + ", 1.13 and 0.936 times ten to the minus ten metres per second squared. A lower panel shows that the curves differ from one another by much less than the grey band marking the " + f"{_t[1]['rms']:.2f}" + " dex scatter of the data."),
 ("Figure 2", "Three panels. Panel a: the fitted coefficient kappa falls steeply as the assumed stellar mass-to-light ratio of discs rises from 0.35 to 0.85, from about 0.8 to 0.3 when measured against the cosmological-constant density and from about 0.66 to 0.25 against the critical density; the first curve crosses one half at a ratio of " + f"{PN['S2']['ud_for_half_L']:.2f}" + ", inside the shaded population-synthesis range of 0.5 to 0.7, and the second at " + f"{PN['S2']['ud_for_half_C']:.2f}" + ", just below it. Panel b: three horizontal error bars, estimator A at " + f"{_M[0][1]:.2f} plus or minus {_M[0][2]:.2f}, estimator B at {_M[1][1]:.2f} plus or minus {_M[1][2]:.2f} and estimator C at {_M[2][1]:.2f} plus or minus {_M[2][2]:.2f}" + ", each with a grey bar below it spanning its values over four Hubble-constant conventions (" + ", ".join(f"{min(b.values()):.2f} to {max(b.values()):.2f}" for b in _bx) + "), overlap vertical lines marking candidate coefficients at 0.461, 0.5, 0.557 and 0.583. Panel c: predicted acceleration scale against the Hubble constant for kappa of one half and of 0.461; the point for one half at the Planck Hubble constant and the point for 0.461 at the SH0ES Hubble constant lie at the same height."),
 ('Figure 3', "Two panels. Panel a: the logarithmic slope of observed against baryonic acceleration in the deep regime, plotted against the ratio of baryonic acceleration to the acceleration scale on a logarithmic axis from 0.003 to 0.25. A black curve, the slope predicted by the relation, rises slowly from 0.51 to 0.61. Four filled points with vertical error bars, the measured median per-galaxy slopes of SPARC at three disc mass-to-light ratios (0.62, 0.61 and 0.58, each plus or minus about 0.03) and of MIGHTEE-HI (0.60 plus or minus 0.08), sit just above open diamonds that mark the slope the relation predicts at the same points (0.56 to 0.58). Dotted horizontal lines at 0.75 and at 1, the Newtonian slope, lie well above all the points. Panel b: the coefficient kappa measured in the deep regime for nine cases, drawn as horizontal error bars against a solid vertical line at one half, a dashed line at 0.60 for the critical-density reading, and a grey band for estimator A. SPARC at disc ratios 0.5, 0.6 and 0.7 gives " + ", ".join(f"{_sp[u]['amp']['kappa_L']:.2f}" for u in ("0.5", "0.6", "0.7")) + ". MIGHTEE-HI gives 0.89 in our fit and 0.90, 1.10 and 0.79 under three of the survey's own mass-to-light conventions, but 0.58 with a fixed K-band ratio of 0.6, next to the SPARC values. SPARC with mass-to-light ratios fitted to the rotation curves themselves gives " + f"{_kin:.2f}" + ", far to the left."),
 ("Figure 4", "Line plot of the logarithmic change of the acceleration scale against redshift from 0 to 4. A thick horizontal line at zero is the prediction of a scale anchored to the cosmological constant. A dashed curve, for a scale proportional to the Hubble rate, rises to 0.58 dex at redshift 2.5 and 0.8 dex at redshift 4. A solid curve with a dark band, for the scale that emerges from the cold dark matter haloes of the low-mass discs the proposed gate selects, rises to " + f"{PN['S4']['delta_gate']:.2f}" + " dex at redshift 2.5; a dot-dashed curve for haloes of ten to the twelve solar masses rises to 0.33 dex, inside a lighter band for the range over halo mass and concentration relation. A dotted curve for a second halo scaling lies close to the dashed curve. A narrow band falling to minus 0.2 dex at redshift 4 shows a scale that follows an evolving dark-energy density. Two square markers at redshift 2.5, at 0 and at " + f"{PN['S4']['delta_gate']:.2f}" + ", carry error bars of " + f"{PN['S4']['se_rec'][0]:.2f} and {PN['S4']['se_rec'][1]:.2f}" + " dex, the error of the mean of the recommended design."),
 ("Figure 5", "Two curves of error amplification against the ratio of baryonic acceleration to the acceleration scale, on a logarithmic horizontal axis from 0.005 to 16. The amplification of kinematic errors starts at 2 and that of baryonic-mass errors at 1 at the lowest accelerations; both stay nearly flat below a ratio of 0.3, a region shaded and labelled as the proposed gate, and then rise steeply, passing 4 and 3 near a ratio of 1.5 and exceeding 10 beyond a ratio of 8. A grey band from " + f"{PN['S5']['y_percentiles'][0]:.2f} to {PN['S5']['y_percentiles'][2]:.1f}" + " marks where the RC100 galaxies lie."),
 ("Figure 6", "Scatter plot of the inferred acceleration scale against redshift from 0.6 to 2.5 for 99 galaxies, spread over nearly two dex vertically. Points are coloured by the acceleration at which each galaxy is measured: galaxies measured at low acceleration lie high in the plot and those at high acceleration lie low. A fitted straight line declines gently, by " + f"{abs(PN['S5']['slope']):.2f} plus or minus {PN['S5']['slope_err']:.2f}" + " dex per unit redshift. Two thin rising lines show the halo-emergent prediction for haloes of ten to the twelve solar masses and the prediction of a scale proportional to the Hubble rate."),
]

# ---- 4. write the bundle
shutil.copy(PDF, os.path.join(OUT, "01_manuscript_for_review.pdf"))
with open(os.path.join(OUT, "02_title_abstract_keywords.txt"), "w") as f:
    f.write("TITLE\n" + plain(title) + "\n\nRUNNING HEAD\nThe a0-Lambda relation and its redshift test\n\n")
    f.write(f"ABSTRACT ({nplain} words by a plain count, {nwords} with each math span as one word; limit 250)\n" + plain(abstract) + "\n\n")
    f.write("KEYWORDS (six, all from the MNRAS list)\n" + plain(keywords) + "\n\n")
    f.write("ARTICLE TYPE\nPaper (Main Journal)\n\nCORRESPONDING AUTHOR\n" + AUTHOR + ", " + AFFIL + "; " + EMAIL + ("; ORCID " + ORCID if ORCID else "") + "\n\n")
    f.write("FUNDING\nNone.\n\nCONFLICT OF INTEREST\nNone.\n\nDATA AVAILABILITY\nStatement included in the manuscript (public repository, tagged release mnras-v3.1; SPARC; Nestor Shachar et al. 2023, arXiv v1 table, corrected transcription; MIGHTEE-HI points digitised from Varasteanu et al. 2025; Price et al. 2021; KURVS, Puglisi et al. 2023; MUSE-DARK public products; Varasteanu et al. 2026).\n")
cl = open(os.path.join(HERE, "COVER_LETTER.md")).read()
body = cl.split("\n---\n")[1].strip().replace("[SIGNATURE]", SIGNATURE)
# the earlier-postings paragraph: keep the variant that matches the PAPER6 switch of the .tex, drop the other
_keep, _drop = ("PAPER6-NOTE", "PAPER6-REMOVED") if PAPER6 else ("PAPER6-REMOVED", "PAPER6-NOTE")
body = re.sub(r"\[" + _drop + r"\].*?\[/" + _drop + r"\]\n?", "", body, flags=re.S)
body = re.sub(r"\[/?" + _keep + r"\]\n?", "", body)
if "PAPER6" in body: die("the cover letter's PAPER6 variant markers were not resolved")
if PAPER6 != ("22559892" in open(os.path.join(BUILD, "mnras_a0_lambda_v3.bbl")).read() if os.path.exists(os.path.join(BUILD, "mnras_a0_lambda_v3.bbl")) else PAPER6):
    die("the PAPER6 switch and the built bibliography disagree")
if "[SIGNATURE]" in body or AUTHOR not in body: die("the cover letter's signature block was not filled")
with open(os.path.join(OUT, "03_cover_letter.txt"), "w") as f:
    f.write(body + "\n" + EMAIL + "\n")
with open(os.path.join(OUT, "04_alt_text_for_figures.txt"), "w") as f:
    for k, v in ALT: f.write(k + "\n" + v + "\n\n")
with zipfile.ZipFile(os.path.join(OUT, "05_source_for_acceptance.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("mnras_a0_lambda_v3.tex", flat)
    z.write(os.path.join(HERE, "references.bib"), "references.bib")
    bbl = os.path.join(BUILD, "mnras_a0_lambda_v3.bbl")
    if os.path.exists(bbl): z.write(bbl, "mnras_a0_lambda_v3.bbl")
    for i, fg in enumerate(figs, 1): z.write(os.path.join(HERE, fg), "fig%d.pdf" % i)
    z.writestr("readme.txt", "MNRAS source files. Main file: mnras_a0_lambda_v3.tex (class mnras.cls, natbib, mnras.bst). Bibliography: mnras_a0_lambda_v3.bbl "
               "(generated from references.bib). Figures: fig1.pdf to fig6.pdf, one per file, vector PDF. Build: pdflatex, bibtex, pdflatex, pdflatex.\n")
print(f"bundle written to {OUT}")
print(f"  PDF {size_mb:.2f} MB; abstract {nplain} words (plain) / {nwords} (math spans as words); e-mail typeset; {len(figs)} figures; alt text for each; PAPER6 variant: {'cited with note' if PAPER6 else 'removed'}.")
