# -*- coding: utf-8 -*-
"""Generate the scaling-MOND writeup PDF (reportlab + DejaVu Serif for full Unicode math)."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                HRFlowable, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/opt/homebrew/Caskroom/miniconda/base/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf"
pdfmetrics.registerFont(TTFont("DJSerif", f"{FD}/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DJSerif-Bold", f"{FD}/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJSerif-Italic", f"{FD}/DejaVuSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DJMono", f"{FD}/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DJSerif", normal="DJSerif", bold="DJSerif-Bold",
                              italic="DJSerif-Italic", boldItalic="DJSerif-Bold")

OUT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/Zimmerman_Scaling_MOND_2026.pdf"

styles = getSampleStyleSheet()
def st(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    kw.setdefault("fontName", "DJSerif")
    return ParagraphStyle(name, parent=base, **kw)

S_title = st("t", fontName="DJSerif-Bold", fontSize=15, leading=19, alignment=TA_CENTER, spaceAfter=4)
S_auth  = st("a", fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#333333"), spaceAfter=2)
S_date  = st("d", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#666666"), spaceAfter=10)
S_h     = st("h", fontName="DJSerif-Bold", fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
             textColor=colors.HexColor("#1a2a44"))
S_body  = st("b", fontSize=9.3, leading=13.4, alignment=TA_JUSTIFY, spaceAfter=5)
S_abs   = st("abs", fontSize=9, leading=12.6, alignment=TA_JUSTIFY, leftIndent=14, rightIndent=14,
             textColor=colors.HexColor("#222222"))
S_eq    = st("eq", fontSize=10, leading=15, alignment=TA_CENTER, spaceBefore=3, spaceAfter=6)
S_cap   = st("cap", fontSize=8, leading=10.5, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=8)
S_ref   = st("r", fontSize=8, leading=11, leftIndent=12, firstLineIndent=-12, spaceAfter=2)

def P(t, s=S_body): return Paragraph(t, s)
def H(t): return Paragraph(t, S_h)
def EQ(t): return Paragraph(t, S_eq)

story = []
story.append(P("The MOND Acceleration Scale as the Cosmic Dynamical Acceleration", S_title))
story.append(P("A scaling-MOND cosmology, its over-constrained web, and three honest bridges toward a theory of the dark sector", S_auth))
story.append(Spacer(1, 3))
story.append(P("Carl Zimmerman &nbsp;·&nbsp; Independent Researcher", S_auth))
story.append(P("June 2026 &nbsp;·&nbsp; analysis assisted by Claude (Anthropic); all results reproducible from the cited scripts", S_date))
story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#999999"), spaceAfter=8))

story.append(P("<b>Abstract.</b> We examine the proposal that the MOND acceleration scale is the "
  "cosmic dynamical acceleration, a<sub>0</sub> = (c/2)√(Gρ<sub>c</sub>) = cH(z)/Z with "
  "Z = 2√(8π/3) ≈ 5.789. Algebraically this is Milgrom's coincidence a<sub>0</sub> ≈ cH<sub>0</sub> "
  "re-expressed through the Friedmann relation; its distinctive, coefficient-free consequence is "
  "that a<sub>0</sub> <i>evolves</i> as a<sub>0</sub>(z) = a<sub>0</sub>(0)·E(z) — an idea due to "
  "Milgrom (2014); our contribution is an explicit covariant realization and a proof of its "
  "CMB-safety. Fitting a<sub>0</sub> ∝ E(z)<super>p</super> to the 2026 data (SPARC, Vărăşteanu, "
  "MUSE-DARK) gives p = 0.80 ± 0.17; constant a<sub>0</sub> is excluded at 5σ in the nominal fit, but "
  "a jackknife and an inter-method systematic reduce this to ≈2σ, so we treat it as a suggestive hint, "
  "not a detection. From the AeST action, promoting a<sub>0</sub> to the aether expansion "
  "a<sub>0</sub> = cθ/3Z, we show — by order-counting reinforced by the exact identity "
  "δq<super>00</super> = 0 — that a<sub>0</sub> is absent from the linear perturbations, so running "
  "a<sub>0</sub> leaves the linear CMB exactly invariant (confirmed numerically: r<sub>s</sub> = 144.3 "
  "Mpc, ℓ<sub>A</sub> = 301.7). The boundaries are explicit: the O(1) coefficient is a posit; the "
  "Standard-Model constants do not follow; and the apparent-a<sub>0</sub> evolution is itself "
  "reproduced by ΛCDM simulations, so the amplitude does not discriminate. The one prediction that "
  "does — a redshift-weakening external field effect, η = g<sub>ext</sub>/a<sub>0</sub>(z) ∝ 1/E(z) — "
  "is forecast to require a dedicated z &gt; 4 campaign.",
  S_abs))
story.append(Spacer(1, 6))

story.append(H("1.&nbsp; The premise and its one novel framing"))
story.append(P("The empirical anchor is the MOND acceleration scale measured from 175 SPARC rotation "
  "curves, a<sub>0</sub> = (1.1–1.2)×10<super>−10</super> m/s<super>2</super> [McGaugh et al. 2016]. "
  "The proposal writes it as half the surface gravity of the cosmic free-fall density:"))
story.append(EQ("<i>a</i><sub>0</sub> = (c/2)·√(G ρ<sub>c</sub>) = c<super>2</super>/(2R), &nbsp;&nbsp; "
  "R = √(8π/3)·c/H = c·t<sub>ff</sub>."))
story.append(P("Via the Friedmann relation H<super>2</super> = (8π/3)Gρ<sub>c</sub>, this equals "
  "a<sub>0</sub> = cH/Z with Z = 2√(8π/3). The √(8π/3) factor is genuine Friedmann physics; the "
  "remaining factor of 2 — the Schwarzschild surface-gravity reading c<super>2</super>/2R — is the "
  "only un-derived element. The density / surface-gravity <i>form</i> appears to be novel (it is not "
  "the cH<sub>0</sub> or √Λ form used in Milgrom's papers), but it is a re-expression of a known "
  "coincidence, not new physics, and the coefficient is not unique: the de-Sitter-horizon readings of "
  "Milgrom (Z = 2π) and Verlinde (Z ≈ 6) fit the same data equally well."))

story.append(H("2.&nbsp; The falsifiable prediction, confronted with data"))
story.append(P("Because a<sub>0</sub> tracks a cosmic density, it evolves. The prediction is "
  "coefficient-free — Z cancels in the ratio:"))
story.append(EQ("<i>a</i><sub>0</sub>(z) / <i>a</i><sub>0</sub>(0) = E(z) = "
  "√(Ω<sub>m</sub>(1+z)<super>3</super> + Ω<sub>Λ</sub>)."))
story.append(P("Fitting a<sub>0</sub>(z) = A·E(z)<super>p</super> to the real compilation, marginalizing "
  "the normalization A, yields the result below. In the nominal fit, constant a<sub>0</sub> (p = 0) and "
  "the matter-only branch (p = 3/2) are each excluded at 5σ and the premise (p = 1) is consistent at "
  "1.1σ. This significance is fragile, and we say so: a jackknife shows the rejection of constant "
  "a<sub>0</sub> rests almost entirely on the single z ≈ 0.9 point (dropping it leaves 1.2σ), and the "
  "1.7σ discrepancy between the two near-coincident local anchors (1.20 vs 1.69 at z ≈ 0) evidences an "
  "inter-method systematic σ<sub>sys</sub> ≈ 0.28 that, folded in, reduces the rejection to ≈2σ — a "
  "suggestive hint, not a detection. Two honest caveats: (i) an evolving relation is also expected in "
  "ΛCDM — Magneticum simulations find apparent a<sub>0</sub> rising ×3 by z = 2.3, matching "
  "E(2.3) = 3.46 with no fundamental evolution, so the data favor 'evolving over constant', not this "
  "framework over ΛCDM; (ii) de Graaff's z ≈ 6 ratios M<sub>dyn</sub>/M<sub>★</sub> ~ 40 are <i>not</i> "
  "support — the evolving-a<sub>0</sub> boost reaches only ~3 for such compact (near-Newtonian) systems."))
data = [
  ["z", "a₀ (10⁻¹⁰ m/s²)", "source"],
  ["0.00", "1.20 ± 0.26", "SPARC — McGaugh, Lelli & Schombert 2016"],
  ["0.05", "1.69 ± 0.13", "Vărăşteanu et al. 2025"],
  ["0.90", "2.38 ± 0.11", "MUSE-DARK III 2026"],
]
t = Table(data, colWidths=[0.7*inch, 1.5*inch, 3.6*inch])
t.setStyle(TableStyle([
  ("FONTNAME",(0,0),(-1,-1),"DJSerif"), ("FONTSIZE",(0,0),(-1,-1),8.3),
  ("FONTNAME",(0,0),(-1,0),"DJSerif-Bold"),
  ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e8ecf4")),
  ("LINEBELOW",(0,0),(-1,0),0.5,colors.HexColor("#888888")),
  ("LINEBELOW",(0,-1),(-1,-1),0.5,colors.HexColor("#cccccc")),
  ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
  ("ALIGN",(0,0),(1,-1),"CENTER")]))
story.append(t)
story.append(P("Fit (a₀_decisive_pipeline.py): best p = 0.80 ± 0.17; constant a₀ χ² = 27 vs E(z) "
  "χ² = 3.8 vs (1+z)^1.5 χ² = 27.5. A single clean a₀ at z = 3 (3%) sharpens p to ≈ 0.99 ± 0.04.", S_cap))

story.append(H("3.&nbsp; The over-constrained web"))
story.append(P("The content is a single dimensionless invariant, a<sub>0</sub>/cH = 1/Z = 0.173, held "
  "fixed at every epoch and cast by dimensional analysis into six unit-costumes — an acceleration "
  "(the radial-acceleration relation), a length (ℓ = c<super>2</super>/a<sub>0</sub> = Z·R<sub>H</sub>), "
  "a surface density (Σ = a<sub>0</sub>/G), a velocity (the baryonic Tully–Fisher zero-point), a "
  "temperature (T<sub>dS</sub>/Z), and a time (the cosmic free-fall time). From the one premise about "
  "a set of relations follow as forced consequences. The web is <i>over-constrained</i>: the same "
  "a<sub>0</sub> must simultaneously fit the SPARC scale, the de-Sitter (Λ) floor "
  "a<sub>0</sub>(0)√Ω<sub>Λ</sub>, and the intermediate-z points (Vărăşteanu, MUSE-DARK) — several "
  "determinations across cosmic time keyed to one number (the relation H<sub>0</sub> = Za<sub>0</sub>/c "
  "is an identity, not an independent check). We use this to draw the honest line: a real relation is "
  "z-invariant (a<sub>0</sub>/cH stays 1/Z); a coincidence between cosmic numbers is not. The same test "
  "that keeps these edges <i>rejects</i> the Standard-Model-constant 'derivations' (Section 5)."))

story.append(H("4.&nbsp; Three bridges toward a theory of the dark sector"))
story.append(P("<b>Bridge 1 (relativistic completion — CMB-safety, established).</b> The covariant home "
  "is the Aether–Scalar–Tensor theory [Skordis &amp; Złošnik 2021], the one relativistic MOND that "
  "fits the CMB. Promoting its fixed a<sub>0</sub> to a<sub>0</sub>(z) by coupling to the aether "
  "expansion θ = ∇·A = 3H is a minimal modification. From the AeST action, a<sub>0</sub> enters only "
  "the spatial free-function term <i>F</i> ∝ <i>Y</i><super>3/2</super>/a<sub>0</sub>; on the FRW background the "
  "scalar is temporal, so <i>Y</i> = O(δφ<super>2</super>) and the a<sub>0</sub>-term is O(δφ<super>3</super>) "
  "— absent from the linear equations. The one term the standard order-counting omits, "
  "δq<super>00</super>·(dφ/dt)<super>2</super>, also vanishes exactly: the unit-timelike constraint "
  "forces δq<super>00</super> = δg<super>00</super> + 2A<super>0</super>δA<super>0</super> = 2Ψ − 2Ψ = 0, "
  "even with the aether perturbed. Hence running a<sub>0</sub> leaves the linear CMB and matter "
  "power spectrum <i>exactly</i> invariant. A direct solution of the linear Einstein–Boltzmann system "
  "confirms this numerically (the running-a<sub>0</sub> effect is 0) and reproduces the Planck sound "
  "horizon r<sub>s</sub> = 144.3 Mpc and acoustic scale ℓ<sub>A</sub> = 301.7. The CMB-fitting dust "
  "mode lives in the separate temporal sector <i>K</i>(<i>Q</i>) and is a<sub>0</sub>-independent."))
story.append(P("<b>Bridge 2 (the coefficient — reported straight, does not close).</b> Horizon "
  "thermodynamics derives the evolution a<sub>0</sub> ∝ H route-independently and the order of "
  "magnitude, but does <i>not</i> pin the O(1) coefficient: legitimate matchings give Z = 1, 2π, ≈ 6, "
  "and 5.789, clustering within 8.5% — inside a<sub>0</sub>'s ~20% systematic. The framework's "
  "'Schwarzschild' reading is not self-consistent (the enclosed mass is 8π/3 times the Schwarzschild "
  "mass for R, so R is not a real horizon). The factor of 2 remains a posit. This costs the framework "
  "nothing, because the falsifiable prediction is the <i>evolution</i>, which is Z-independent."))
story.append(P("<b>Bridge 3 (dark matter = dark energy — sourced, falsifiable).</b> In AeST the single "
  "temporal function <i>K</i>(<i>Q</i>) = −2Λ + <i>K</i><sub>2</sub>(<i>Q</i>−<i>Q</i><sub>0</sub>)<super>2</super> carries both the "
  "dark-matter-mimicking dust mode (ρ ∝ a<super>−3</super>) and dark energy (−2Λ) — one function, two "
  "terms, tied by the evolving a<sub>0</sub> that floors at the Λ value. The test is "
  "a<sub>0</sub>-cosmography: H(z) = Z·a<sub>0</sub>(z)/c reconstructs the expansion from galaxy "
  "dynamics. It lands on the Planck/local band at z = 0 and shows the known ~25% tension at z ≈ 0.9."))

story.append(H("5.&nbsp; Boundaries — what is explicitly <i>not</i> claimed"))
story.append(P("This is a candidate theory of the <i>dark sector</i> (gravity, dark matter, dark "
  "energy), not a Theory of Everything. The Standard-Model constants do not connect: a 34,000-formula "
  "search hits an arbitrary O(100) target to 0.004% about 20% of the time, 52 of 64 published "
  "Z<super>2</super> 'derivations' contain no Z at all, and a <i>random</i> number reproduces "
  "α<super>−1</super> and the mass ratios to the same precision as 32π/3. Those retrodictions carry "
  "≈ 0 bits and are not part of this framework. Likewise the coefficient is a posit, and the full "
  "CMB peak heights require a dedicated Boltzmann implementation. Stating these limits is what keeps "
  "the surviving result trustworthy."))

story.append(H("6.&nbsp; The decisive test"))
story.append(P("Pinning the exponent p by measuring a<sub>0</sub> at z &gt; 2 tests evolution against "
  "constant a<sub>0</sub>, but does <i>not</i> separate this framework from ΛCDM, whose apparent "
  "a<sub>0</sub> also rises as E(z) (Section 2). The deep-MOND cascade (M<sub>dyn</sub>/M<sub>★</sub> ∝ "
  "√E, σ ∝ E<super>1/4</super>, Tully–Fisher zero-point ∝ −log E) shares this degeneracy. The one "
  "discriminating observable is the external field effect: with a<sub>0</sub> → a<sub>0</sub>(z), "
  "η = g<sub>ext</sub>/a<sub>0</sub>(z) ∝ 1/E(z), so the EFE <i>weakens</i> with redshift — distinct "
  "from ΛCDM (no host effect) and constant-a<sub>0</sub> MOND (constant EFE). Solving the MOND EFE, the "
  "distinctive signal is ≈0.1 dex, below the per-galaxy scatter (~0.3 dex); a 3σ detection needs "
  "~600–1600 extended, environment-classified, kinematically-resolved galaxies at z &gt; 4 — a "
  "dedicated multi-cycle JWST/ALMA(/ELT) program. That measurement, not a single pointing, decides it."))

story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#bbbbbb"), spaceAfter=5))
story.append(P("References", S_h))
refs = [
 "Milgrom, M. 1983, ApJ 270, 365. — 2011, arXiv:1110.2580. — 2014, Phys. Rev. D 91, 044009; arXiv:1412.4344 (cosmological variation of the MOND constant, a₀ ∝ cH).",
 "McGaugh, S., Lelli, F., Schombert, J. 2016, Phys. Rev. Lett. 117, 201101 (SPARC radial-acceleration relation).",
 "Skordis, C. &amp; Złošnik, T. 2021, Phys. Rev. Lett. 127, 161302; arXiv:2007.00082 (Aether–Scalar–Tensor theory).",
 "Tian, Y. et al. 2022, MNRAS 518, 257; arXiv:2206.04333 (apparent a₀ evolution in ΛCDM; Magneticum).",
 "Verlinde, E. 2017, SciPost Phys. 2, 016; Gnedin, O. 2008, arXiv:0809.2790; Famaey &amp; McGaugh 2012, Living Rev. Rel. 15, 10.",
 "de Graaff, A. et al. 2024 (JADES dynamical masses, z = 5.5–7.4); MUSE-DARK III 2026; Vărăşteanu et al. 2025.",
 "Reproducibility: real_research/ — a0_powerlaw_confrontation.py, bridge1_linear_boltzmann.py, "
 "reviews/theta_3H_coupling.py (a₀=cθ/3Z, δq⁰⁰=0), reviews/stresstest_piece3_evolution.py (5σ→2σ), "
 "reviews/efe_evolution_forecast.py, reviews/parameter_space_map.py, false_discovery_rate.py; full "
 "assessment in COMPLETE_ASSESSMENT.md (github.com/carlzimmerman/zimmerman-formula).",
]
for r in refs:
    story.append(Paragraph(r, S_ref))

doc = SimpleDocTemplate(OUT, pagesize=letter, topMargin=0.7*inch, bottomMargin=0.7*inch,
                        leftMargin=0.85*inch, rightMargin=0.85*inch,
                        title="Scaling-MOND Cosmology", author="Carl Zimmerman")
doc.build(story)
print("WROTE", OUT)
