# -*- coding: utf-8 -*-
"""Generate the JWST forecast note as a clean publishable PDF (reportlab + DejaVu Serif)."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                HRFlowable, Image)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/opt/homebrew/Caskroom/miniconda/base/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf"
pdfmetrics.registerFont(TTFont("DJ", f"{FD}/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DJ-Bold", f"{FD}/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DJ-It", f"{FD}/DejaVuSerif-Italic.ttf"))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-Bold", italic="DJ-It", boldItalic="DJ-Bold")
OUT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/JWST_Forecast_Zimmerman.pdf"

ss = getSampleStyleSheet()
def st(n, **k):
    p = k.pop("parent", ss["Normal"]); k.setdefault("fontName", "DJ")
    return ParagraphStyle(n, parent=p, **k)
S_t   = st("t", fontName="DJ-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=3)
S_sub = st("sub", fontName="DJ-It", fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#333"), spaceAfter=6)
S_au  = st("au", fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#555"), spaceAfter=9)
S_h   = st("h", fontName="DJ-Bold", fontSize=11.5, leading=14, spaceBefore=11, spaceAfter=4, textColor=colors.HexColor("#1a2a44"))
S_b   = st("b", fontSize=9.6, leading=14.2, alignment=TA_JUSTIFY, spaceAfter=6)
S_eq  = st("eq", fontName="DJ-Bold", fontSize=11, leading=15, alignment=TA_CENTER, spaceBefore=2, spaceAfter=6,
           textColor=colors.HexColor("#11204a"))
S_cap = st("cap", fontSize=8, leading=10.5, alignment=TA_CENTER, textColor=colors.HexColor("#555"), spaceAfter=8)
S_f   = st("f", fontSize=7.8, leading=10.5, alignment=TA_JUSTIFY, textColor=colors.HexColor("#444"), spaceAfter=2)

def P(t, s=S_b): return Paragraph(t, s)
S = []
S += [P("A Falsifiable Forecast for JWST", S_t),
      P("The MOND acceleration scale as the cosmic dynamical acceleration — and what it predicts for early galaxies", S_sub),
      P("Carl Zimmerman &nbsp;·&nbsp; June 2026 &nbsp;·&nbsp; all results reproducible from the cited code", S_au),
      HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#999"), spaceAfter=8)]

S += [P("The idea, in one paragraph", S_h),
 P("Modified Newtonian Dynamics (MOND) has a single critical acceleration, "
   "a<sub>0</sub> ≈ 1.2×10<super>−10</super> m/s<super>2</super>, below which the dynamics of galaxies "
   "depart from Newton's law. For forty years it has been noticed that this scale is numerically close "
   "to the cosmic acceleration cH<sub>0</sub> — the speed of light times the expansion rate. This note "
   "takes that coincidence literally: it supposes that a<sub>0</sub> is <i>set by the mean density of "
   "the universe</i>,"),
 P("a<sub>0</sub> = (c/2)·√(G ρ<sub>c</sub>) = cH/Z,  Z = 2√(8π/3) ≈ 5.79.", S_eq),
 P("I want to be honest about what this is and isn't. The √(8π/3) is exact Friedmann physics; the "
   "remaining factor of two is a posited O(1) number — a clean choice, but not derived, and shared in "
   "spirit with Milgrom's and Verlinde's readings of the same coincidence. So this is a <i>novel "
   "framing</i> of a known relation, not a derivation. Its value is not in the coefficient. Its value is "
   "in the one thing the framing forces — a single, sharp, falsifiable prediction.")]

S += [P("The one sharp consequence: a<sub>0</sub> evolves", S_h),
 P("If a<sub>0</sub> tracks the cosmic density, and the density falls as the universe expands, then "
   "a<sub>0</sub> must have been <i>larger in the past</i>:"),
 P("a<sub>0</sub>(z) = a<sub>0</sub>(0)·E(z),  E(z) = √(Ω<sub>m</sub>(1+z)<super>3</super> + Ω<sub>Λ</sub>).", S_eq),
 P("This prediction is <b>coefficient-free</b> — the posited number Z cancels in the ratio — so it "
   "cannot be tuned. It is the single distinctive claim, and it is already testable. Fitting the 2026 "
   "data (the local SPARC scale, Vărăşteanu's z≈0.05 sample, and the MUSE-DARK measurement at z≈0.9) "
   "gives a<sub>0</sub> ∝ E(z)<super>p</super> with <b>p = 0.80 ± 0.17: constant a<sub>0</sub> is "
   "rejected at 5σ</b>, and so is the matter-only (1+z)<super>3/2</super> alternative. The data, for "
   "the first time, lean toward evolution.")]

S += [Spacer(1,3),
 Image("real_research/figures/fig1_a0_evolution.png", width=4.75*inch, height=3.04*inch, hAlign='CENTER'),
 P("Figure 1.  The MOND acceleration scale measured at three redshifts. A constant a<sub>0</sub> "
   "(dashed) is excluded at 5σ; the data favor a<sub>0</sub> ∝ E(z) with exponent 0.80 ± 0.17 "
   "(navy). The shaded band marks where JWST kinematics at z &gt; 2 will decide it. "
   "[a0_decisive_pipeline.py]", S_cap)]


S += [P("Why JWST is the decisive instrument", S_h),
 P("The effect grows fast with redshift. By z = 6, a<sub>0</sub> would be ten times its local value; by "
   "z = 10, twenty times. JWST reaches exactly this regime. And the crucial point — the thing that makes "
   "this a real test rather than a story — is that <b>every observable scales with the same number, "
   "E(z)</b>. A coherent dependence across many independent measurements, all driven by one quantity, is "
   "a signature that no combination of ΛCDM with measurement systematics can counterfeit.")]
tab = Table([["redshift","E(z) = a₀(z)/a₀(0)","M_dyn/M*  (×√E)","velocities (×E¼)","Tully–Fisher shift (−log E)"],
             ["2","3.0","×1.7","+32%","−0.48 dex"],
             ["6","10.4","×3.2","+80%","−1.0 dex"],
             ["10","20.5","×4.5","+113%","−1.3 dex"]],
            colWidths=[0.85*inch,1.7*inch,1.35*inch,1.2*inch,1.7*inch])
tab.setStyle(TableStyle([("FONTNAME",(0,0),(-1,-1),"DJ"),("FONTSIZE",(0,0),(-1,-1),8),
  ("FONTNAME",(0,0),(-1,0),"DJ-Bold"),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e8ecf4")),
  ("LINEBELOW",(0,0),(-1,0),0.5,colors.HexColor("#888")),("LINEBELOW",(0,-1),(-1,-1),0.5,colors.HexColor("#ccc")),
  ("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
S += [tab, Spacer(1,6)]

S += [Image("real_research/figures/fig2_predictions.png", width=4.75*inch, height=3.04*inch, hAlign='CENTER'),
 P("Figure 2.  Each JWST observable is a different power of the SAME quantity E(z), so the whole "
   "prediction set rises and falls together with one number. The star marks de Graaff (2024) "
   "M<sub>dyn</sub>/M<sub>*</sub> ≈ 40 at z ≈ 6. Coherence across channels is the signature; "
   "independent scatter would refute it. [jwst_full_predictions.py]", S_cap)]


S += [P("The predictions", S_h),
 P("<b>Dynamical masses rise as √E(z).</b> In MOND the apparent “dark matter” of a galaxy — the gap "
   "between its kinematic mass and its baryonic mass — grows with a<sub>0</sub>. So the ratio "
   "M<sub>dyn</sub>/M<sub>*</sub> measured from JWST spectroscopy should climb with redshift as √E: a "
   "factor of three by z≈6, four and a half by z≈10. This is already hinted at: de Graaff and "
   "collaborators (2024) find dynamical-to-stellar ratios as high as 40 in JADES galaxies at z ≈ "
   "5.5–7.4, values that an unchanging a<sub>0</sub> struggles to reach."),
 P("<b>The Tully–Fisher and Faber–Jackson relations shift.</b> Because v<super>4</super> = G·M·"
   "a<sub>0</sub>(z), a galaxy of fixed baryonic mass spins faster at high redshift, and the zero-point "
   "of the mass–velocity relation moves by −log<sub>10</sub>E(z) — roughly half a dex by z = 2, a full "
   "dex by z = 6. The intermediate-redshift precedent already exists: Übler and collaborators (2017) "
   "measured a shift of −0.45 dex at z ≈ 2.3, almost exactly the −0.48 the relation predicts."),
 P("<b>Velocities and dispersions are boosted as E(z)<super>1/4</super></b>, about +80% by z = 6 at "
   "fixed baryonic mass. <b>The radial-acceleration relation's knee moves to higher acceleration.</b> "
   "Galaxies enter the deep-MOND regime at <b>smaller radius</b> (the characteristic scale shrinks as "
   "1/√E), and their <b>critical surface density rises as E(z)</b>, so early disks should be denser."),
 P("<b>One clean null test.</b> Build a galaxy scaling relation from a sample spanning a range of "
   "redshifts. If a<sub>0</sub> evolves, the relation is artificially <i>broadened</i> — by an amount "
   "log E(z<sub>max</sub>) — because each galaxy carries a different a<sub>0</sub>. Rescale each by its "
   "own E(z) and the relation should snap back to its intrinsic, tight form. Do-nothing-broadens, "
   "rescaling-tightens: a built-in falsifier that needs no external calibration.")]

S += [P("What this does <i>not</i> predict — and why that matters", S_h),
 P("A theory is only as trustworthy as the claims it refuses to make. The evolving a<sub>0</sub> is "
   "<b>absent from the linear growth of cosmic structure</b> (this follows from the structure of the "
   "only relativistic completion that fits the microwave background). The consequence is important and "
   "deflationary: <b>evolving a<sub>0</sub> does not, by itself, make galaxies form earlier or in "
   "greater number.</b> It changes the <i>dynamics</i> of galaxies that have already formed, not the "
   "<i>census</i> of how many exist. So the much-discussed “impossible” early massive galaxies are "
   "addressed by this framework <b>only</b> where their masses are inferred dynamically — in which case "
   "those masses are over-estimated by √E(z), and the galaxies are lighter in baryons than they appear. "
   "Where a mass excess comes from stellar light, or where the puzzle is the sheer abundance of luminous "
   "sources, this framework is <b>silent</b>. It likewise says nothing about metallicities, "
   "reionization, dust, or the ultraviolet luminosity function — those are the physics of gas and stars, "
   "not of a<sub>0</sub>. Naming them as victories, as earlier versions of this work did, was a mistake. "
   "The honest boundary is part of the prediction.")]

S += [P("How to run the test", S_h),
 P("Do not fit a single galaxy. <b>Measure the dynamical-mass ratio, the Tully–Fisher zero-point, the "
   "dispersions, the sizes, and the surface densities across a span of redshift, and ask whether they "
   "all key off the same E(z).</b> If M<sub>dyn</sub>/M<sub>*</sub> ∝ √E <i>and</i> the zero-point ∝ "
   "−log E <i>and</i> the dispersions ∝ E<super>1/4</super>, simultaneously, with one consistent "
   "expansion history — that coherence is the fingerprint of an evolving a<sub>0</sub>, and nothing else "
   "makes it. If the channels scatter independently, the idea is wrong, and the same data say so "
   "cleanly. The single most decisive measurement is a clean determination of "
   "M<sub>dyn</sub>/M<sub>baryon</sub> at a known baryonic acceleration in a galaxy at z &gt; 2.")]

S += [P("What is actually being claimed", S_h),
 P("Not a theory of everything; not a derivation of the MOND scale; not a solution to the dozens of "
   "problems earlier drafts of this idea claimed. The claim is narrow and, for that reason, testable: "
   "<b>that the acceleration scale governing galaxies is the cosmic density's own acceleration, so it "
   "must evolve as E(z) — and JWST is now precise enough to see it.</b> The universe's largest scale "
   "would then be reaching into its smallest dynamics: <i>here</i> would be set by <i>everywhere</i>. "
   "That is either true or it isn't, and the next few years of JWST kinematics will decide it.")]

S += [HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#bbb"), spaceBefore=4, spaceAfter=5),
 P("<i>Reproducibility:</i> a0_decisive_pipeline.py (the 5σ data fit), jwst_full_predictions.py (the "
   "full prediction map), bridge1_aest_equations.md (why a<sub>0</sub> is absent from linear growth), "
   "and the repository at github.com/carlzimmerman/zimmerman-formula. &nbsp; <i>Key data:</i> McGaugh, "
   "Lelli &amp; Schombert 2016 (SPARC); Übler et al. 2017 (KMOS³ᴰ); de Graaff et al. 2024 (JADES); "
   "Vărăşteanu et al. 2025; MUSE-DARK III 2026. &nbsp; <i>Foundations:</i> Milgrom 1983; Skordis &amp; "
   "Złośnik 2021 (the relativistic completion); Verlinde 2017.", S_f)]

SimpleDocTemplate(OUT, pagesize=letter, topMargin=0.7*inch, bottomMargin=0.65*inch,
                  leftMargin=0.85*inch, rightMargin=0.85*inch, title="A Falsifiable Forecast for JWST",
                  author="Carl Zimmerman").build(S)
print("WROTE", OUT)
