#!/usr/bin/env python3
"""
wb_a0_amplitude_budget.py -- CAN GAIA WIDE BINARIES SUPPLY AN a0-AMPLITUDE CONSTRAINT
WHOSE SYSTEMATICS ARE ORTHOGONAL TO THE DWARF a0-LINE, SO THE JOINT BEATS THE STEP-A FLOOR?
===========================================================================================
STEP B of the showstopper chain.  STEP A (committed, reproduced here from its JSON):
  prep_2026/a0_line/reach_target.py + per_galaxy_budget.py
    gas-dominated a0-line box            = 16.10%
    3-sigma canon-vs-ALT target           =  6.31%
    SPARC-alone floor (best stack)        = 11.62%   (GLS-committed U+G floor 10.90%)
    best conditional (2 external priors)  =  6.78%
  => the dwarf line is SHARED-SYSTEMATIC-owned (Upsilon 8.1% + gas-cal 7.3% + estimator 8.8%),
     and adding galaxies cannot cross the floor.

THE HYPOTHESIS UNDER TEST (not assumed): WB systematics (triples, deprojection, eccentricity
prior, PHOTOMETRIC masses) are disjoint from galaxy systematics (Upsilon, gas-cal, distance,
estimator choice).  If WB delivers sigma(a0)/a0 at comparable precision, the joint adds in
quadrature and beats 11.6%.  This script asks whether WB delivers that precision AT ALL.

THE FRAMEWORK, ON ITS OWN TERMS (working-rule 1, MI first, never the standard-MOND lens):
  modified INERTIA, a0 = cH_Lambda/Z = 9.36e-11 (canonical) / 1.13e-10 (ALT footing),
  its own dS-Unruh interpolation nu(y) = sqrt(1 + 1/y), i.e. g_obs = sqrt(g_bar^2 + g_bar a0).
  WB observable: gamma_v = v_rms/v_rms,Newton.  Deep asymptote (banked
  wb_dr4_prereg_framework_curve.py, hash-frozen in PREREGISTRATION_DR4.md):
     MI  per-star EFE prescription -> gamma_v = 1.1015  (band 1.05-1.10 w/ observable dilution)
     MG  AQUAL-EFE point-field     -> gamma_v = 1.1389  (the MG number, NOT the framework's)
  Generic committed law (milgrom_linear_noefe_wb.py):  gamma = (1 + C/y)^(1/4).
  For the deep WB asymptote the relevant y is the EXTERNAL field ratio y_extN(a0), and the
  prescription is carried entirely by C:  C = 1 exactly for MG, C = 0.69 for the MI per-star
  law (computed below, not assumed).

WHAT THIS SCRIPT COMPUTES (all numerical / closed-form; no field theory):
  S1  forward map gamma_v(a0) from the framework's own MI prescription + the MG reading
  S2  the SENSITIVITY d ln a0 / d gamma -- the 1/4-power DESENSITIZATION, analytic + numeric
  S3  the C-a0 DEGENERACY: the exactly-degenerate combination, a 2-parameter Fisher on the
      frozen DR4 binning, and whether the curve SHAPE (transition location) breaks it
  S4  the WB a0 ERROR BUDGET: contamination (dominant), deprojection/orbit prior, eccentricity
      prior, PHOTOMETRIC stellar mass (honestly non-zero), g_ext calibration, statistics
  S5  achievable sigma(a0)/a0 -- DR3 today and DR4 forecast -- and the JOINT with STEP A

HONESTY RAILS: a manufactured GO and a manufactured NO-GO are penalized equally.  Both a0
footings carried on every load-bearing number.  Both frozen g_ext conventions carried.  The
prior overstatement "WB masses are systematic-free" is CORRECTED, not repeated: the WB mass
systematic is quantified and its SMALLNESS IN PERCENT is shown not to help, because the WB
amplification factor is ~9 while the dwarf line's is ~1.  Assumption-driven inputs (residual
triple fraction, coherent mass zero-point) are labeled ASSUMED and carried as bands, and the
verdict's dependence on them is shown.  Exit 0 = numbers computed, NOT a verdict.  No TOE.
"""
import numpy as np, os, json, math

BAR = "=" * 100
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

G, MSUN, AU = 6.674e-11, 1.989e30, 1.496e11

A0C = 9.36e-11          # canonical  cH_Lambda/Z   (banked)
A0A = 1.13e-10          # ALT footing rho_total/cH0 (banked)
A0M = 1.20e-10          # Milgrom conventional, for the degeneracy interleave check

GEXT_P = 1.778e-10      # frozen PRIMARY  solar-neighborhood observed external field
GEXT_A = 2.078e-10      # frozen ALT      convention Vc^2/R0 (Vc=229, R0=8.178 kpc)

MTOT = 1.5 * MSUN       # typical DR4 pair; the asymptote is M-independent

# --- STEP A committed anchors (read from the committed JSON, never retyped by hand) --------
SA = json.load(open(os.path.join(REPO, "prep_2026", "a0_line", "reach_target_results.json")))
TARGET     = SA["target_pct"] / 100.0            # 6.313%  3-sigma canon-vs-ALT requirement
DWARF_NOW  = SA["box_now_pct"] / 100.0           # 16.10%  current box
DWARF_FLOOR= SA["best_sparc_alone_pct"] / 100.0  # 11.62%  best SPARC-alone stack
DWARF_COND = SA["best_conditional_pct"] / 100.0  #  6.78%  with BOTH external priors

# --- frozen DR4 pre-registration anchors (PREREGISTRATION_DR4.md sec 1.3-1.5) -------------
SIGFIT_30K = 0.0191     # gate spread-check rms at N=30,000 (the pipeline's conservative rule)
N_GATE     = 30000
SIGSYS_FRZ = 0.02       # frozen sigma_sys allowance
GAM_DR3    = 1.2050     # DR3 dry run, canonical footing
SIG_DR3    = 0.0350
N_DR3      = 10624
ECC_SHIFT  = 0.0150     # gate-measured flat-vs-thermal eccentricity shift
MASS_PP    = 0.055      # Banik+2024 sec 2.3.3 per-pair mass error (5.5%)
BINS_LOG10Y= [-1.5, -1.1, -0.8, -0.5, -0.2, 0.1, 0.5, 1.0, 2.2]   # frozen bin edges

# ============================================================ kernel + EFE prescriptions ===
def nu(y):
    return np.sqrt(1.0 + 1.0 / y)


def y_newt(y_obs):
    """Invert g_obs = sqrt(g_N^2 + g_N a0):  y_N^2 + y_N - y_obs^2 = 0 (framework's own)."""
    return 0.5 * (-1.0 + np.sqrt(1.0 + 4.0 * y_obs ** 2))


NCOS = 4001
COS = np.linspace(-1.0, 1.0, NCOS)


def boost_MG(y_int, yE):
    """AQUAL-EFE point-field: force boost = <nu(|y_int e + yE z|)>_angles."""
    yt = np.sqrt(y_int ** 2 + yE ** 2 + 2.0 * y_int * yE * COS)
    return np.mean(nu(yt))


def boost_MI(y_rel, yE):
    """Framework per-star MI-EFE prescription, equal masses (banked script, verbatim)."""
    ys = 0.5 * y_rel
    s_ = np.sqrt(1.0 - COS ** 2)
    y1z, y1x = yE + ys * COS, ys * s_
    y2z, y2x = yE - ys * COS, -ys * s_
    m1, m2 = np.hypot(y1z, y1x), np.hypot(y2z, y2x)
    az = nu(m1) * y1z - nu(m2) * y2z
    ax = nu(m1) * y1x - nu(m2) * y2x
    return np.mean(np.hypot(az, ax) / y_rel)


def gamma_asy(a0, gext, law):
    """Deep (y_rel -> 0) velocity-boost asymptote for a given a0 and external field."""
    yE = y_newt(gext / a0)
    b = boost_MI(1e-6, yE) if law == "MI" else boost_MG(1e-6, yE)
    return math.sqrt(b), yE


def gamma_curve(a0, gext, law, s_kAU):
    yE = y_newt(gext / a0)
    yr = G * MTOT / (s_kAU * 1e3 * AU) ** 2 / a0
    f = boost_MI if law == "MI" else boost_MG
    return np.array([math.sqrt(f(y, yE)) for y in np.atleast_1d(yr)]), yE, yr


# ================================================================================== S0 ====
print(BAR)
print("S0 -- ANCHORS: STEP A (committed) + the frozen DR4 pre-registration + banked MI curve")
print(BAR)
print(f"  STEP A dwarf a0-line : box now {100*DWARF_NOW:.2f}%   SPARC-alone floor "
      f"{100*DWARF_FLOOR:.2f}%   with-2-external-priors {100*DWARF_COND:.2f}%")
print(f"  3-sigma canon-vs-ALT requirement (the bar to beat) : {100*TARGET:.2f}%")
print(f"  frozen DR4: sigma_fit(N=30k) = {SIGFIT_30K:.4f}, sigma_sys = {SIGSYS_FRZ:.3f}"
      f"  -> sigma_tot = {math.hypot(SIGFIT_30K, SIGSYS_FRZ):.4f}")
print(f"  frozen DR3 dry run: gamma = {GAM_DR3:.4f} +- {SIG_DR3:.4f} (N={N_DR3:,}) -- "
      f"in the >1.20 CONTAMINATION-GUARD zone = evidence for NOTHING")

gMI, yE_c = gamma_asy(A0C, GEXT_P, "MI")
gMG, _ = gamma_asy(A0C, GEXT_P, "MG")
assert abs(gMG - 1.137) < 0.005, "MG asymptote drifted off the banked 1.137"
assert 1.095 < gMI < 1.105, "MI asymptote drifted off the banked upper edge"
assert abs(yE_c - 1.4647) < 2e-3, "y_extN drifted off the frozen 1.4647"
print(f"  banked MI/MG reproduced: y_extN = {yE_c:.4f}, gamma_MI = {gMI:.4f}, "
      f"gamma_MG = {gMG:.4f}  [regression anchor OK]")

# effective C in the committed law gamma = (1 + C/y)^{1/4}, y -> y_extN  (COMPUTED, not posited)
C_MI = (gMI ** 4 - 1.0) * yE_c
C_MG = (gMG ** 4 - 1.0) * yE_c
print(f"  effective C in the committed gamma=(1+C/y)^(1/4) at y=y_extN:  "
      f"C_MI = {C_MI:.4f}   C_MG = {C_MG:.4f}  (MG is C=1 to {abs(C_MG-1):.4f})")
print(f"  => the MI-vs-MG prescription IS a multiplicative ambiguity in C of "
      f"{100*(1-C_MI/C_MG):.1f}%  (this is S3's problem)")

# ================================================================================== S1 ====
print()
print(BAR)
print("S1 -- FORWARD MAP gamma_v(a0): how an observed gamma would map to an a0 amplitude")
print(BAR)
print("  Physics: the WB deep asymptote is set by the EXTERNAL field ratio y_extN = g_extN/a0.")
print("  g_ext is FIXED BY THE GALAXY (measured), so a0 enters ONLY through that ratio --")
print("  this is the amplitude handle, and it is the ONLY one (S3 shows the shape adds none).")
print()
print(f"  {'a0 [m/s^2]':>12} {'y_extN':>8} {'gamma_MI':>9} {'gamma_MG':>9} | "
      f"{'y_extN(alt gext)':>17} {'gMI':>7} {'gMG':>7}")
a0grid = [7.0e-11, 8.0e-11, A0C, 1.0e-10, A0A, A0M, 1.35e-10, 1.6e-10]
for a0 in a0grid:
    g1, yy = gamma_asy(a0, GEXT_P, "MI"); g2, _ = gamma_asy(a0, GEXT_P, "MG")
    h1, y2 = gamma_asy(a0, GEXT_A, "MI"); h2, _ = gamma_asy(a0, GEXT_A, "MG")
    tag = "  <- canonical" if a0 == A0C else ("  <- ALT" if a0 == A0A else
          ("  <- Milgrom" if a0 == A0M else ""))
    print(f"  {a0:>12.3e} {yy:>8.4f} {g1:>9.4f} {g2:>9.4f} | {y2:>17.4f} {h1:>7.4f} "
          f"{h2:>7.4f}{tag}")
print("  READ: over the ENTIRE contested a0 band 9.36e-11 -> 1.20e-10 (+28%), the MI asymptote")
print(f"  moves {gamma_asy(A0C,GEXT_P,'MI')[0]:.4f} -> {gamma_asy(A0M,GEXT_P,'MI')[0]:.4f}"
      f" = {abs(gamma_asy(A0M,GEXT_P,'MI')[0]-gMI):.4f} in gamma. The frozen sigma_sys alone is "
      f"{SIGSYS_FRZ:.2f}.")

# ================================================================================== S2 ====
print()
print(BAR)
print("S2 -- SENSITIVITY: the 1/4-POWER DESENSITIZATION, d ln a0 / d ln gamma  (analytic+numeric)")
print(BAR)
print("  Closed form.  gamma = (1 + C/yE)^(1/4),  yE = y_newt(g_ext/a0):")
print("    d ln gamma / d ln yE   = -(1/4) (C/yE) / (1 + C/yE)")
print("    d ln yE   / d ln y_obs = 2 y_obs^2 / (yE sqrt(1+4 y_obs^2)),   y_obs = g_ext/a0")
print("    d ln y_obs/ d ln a0    = -1")
print("  =>  A_log  == d ln a0 / d ln gamma  =  -1 / [ (dlngamma/dlnyE)(dlnyE/dlny_obs) ]")
print("      A_abs  == d ln a0 / d gamma     =  A_log / gamma        (per ABSOLUTE gamma unit)")


def sens(a0, gext, law):
    """Analytic + finite-difference sensitivity of a0 to gamma at the deep asymptote."""
    g, yE = gamma_asy(a0, gext, law)
    C = (g ** 4 - 1.0) * yE
    yo = gext / a0
    dlng_dlnyE = -0.25 * (C / yE) / (1.0 + C / yE)
    dlnyE_dlnyo = 2.0 * yo ** 2 / (yE * math.sqrt(1.0 + 4.0 * yo ** 2))
    dlng_dlna0 = -dlng_dlnyE * dlnyE_dlnyo          # (dlny_obs/dlna0 = -1)
    A_log = 1.0 / dlng_dlna0
    # numeric check: central difference in ln a0 with C HELD FIXED by the prescription
    h = 1e-4
    gp = gamma_asy(a0 * math.exp(h), gext, law)[0]
    gm = gamma_asy(a0 * math.exp(-h), gext, law)[0]
    A_num = 1.0 / ((math.log(gp) - math.log(gm)) / (2 * h))
    # LOAD-BEARING choice: the NUMERIC derivative is the correct one, because the MI per-star
    # prescription's effective C drifts weakly with yE (C_MG = 1 identically, so MG matches the
    # closed form exactly; the MI residual IS that drift and is reported, not hidden).
    return dict(gamma=g, yE=yE, C=C, A_log=A_num, A_abs=A_num / g, A_closed=A_log,
                Cdrift_pct=100 * abs(A_num - A_log) / abs(A_log))


print()
print(f"  {'footing':<12}{'g_ext':<10}{'law':<5}{'gamma':>8}{'y_extN':>9}{'A_log':>9}"
      f"{'A_closed':>10}{'A_abs':>9}   meaning")
rows = []
for fl, a0 in (("canonical", A0C), ("ALT", A0A)):
    for gl, gx in (("primary", GEXT_P), ("alt-conv", GEXT_A)):
        for law in ("MI", "MG"):
            r = sens(a0, gx, law)
            rows.append(dict(footing=fl, gext=gl, law=law, **r))
            print(f"  {fl:<12}{gl:<10}{law:<5}{r['gamma']:>8.4f}{r['yE']:>9.4f}"
                  f"{r['A_log']:>9.3f}{r['A_closed']:>10.3f}{r['A_abs']:>9.3f}"
                  f"   1% in gamma -> {r['A_log']:.1f}% in a0")
for r in rows:
    tol = 1e-6 if r["law"] == "MG" else 3e-2
    assert abs(r["A_log"] - r["A_closed"]) < tol * abs(r["A_closed"]), \
        ("analytic vs numeric mismatch", r)
print("  [MG rows: closed form == finite difference to 1e-6 (C = 1 identically -> the closed")
print("   form is exact). MI rows differ by "
      f"{max(r['Cdrift_pct'] for r in rows if r['law']=='MI'):.1f}% because the per-star MI")
print("   prescription's effective C drifts weakly with y_extN. The NUMERIC value is used")
print("   everywhere below; for MI it is the SMALLER (more GENEROUS to WB) of the two, so the")
print("   verdict is not helped by this choice.]")

PRIM = [r for r in rows if r["footing"] == "canonical" and r["gext"] == "primary"]
A_MI = [r for r in PRIM if r["law"] == "MI"][0]
A_MG = [r for r in PRIM if r["law"] == "MG"][0]
print()
print(f"  FRAMEWORK-FIRST NUMBER (MI, canonical, primary g_ext): A_log = {A_MI['A_log']:.2f}, "
      f"A_abs = {A_MI['A_abs']:.2f} per unit gamma.")
print(f"    -> a 1% gamma error is a {A_MI['A_log']:.1f}% a0 error;  "
      f"sigma(a0)/a0 = {A_MI['A_abs']:.2f} x sigma(gamma).")
print(f"  MG reading is MILDER ({A_MG['A_log']:.2f}) because C=1 > C_MI={C_MI:.3f} puts the")
print("    asymptote further from 1; the framework's own MI reading is the WORSE case, and")
print("    working-rule 1 says the MI reading is the one that decides.")
print("  WHY: two stacked desensitizations. (i) the 1/4 power; (ii) the EFE saturation --")
print("    a0 enters only inside y_extN, and y_newt() COMPRESSES it "
      f"(d ln yE/d ln a0 = -{2*(GEXT_P/A0C)**2/(yE_c*math.sqrt(1+4*(GEXT_P/A0C)**2)):.3f}, not -1).")
# the dwarf-line amplification, for contrast (a0 = (g_obs^2-g_bar^2)/g_bar is DIRECT)
print(f"  CONTRAST -- the dwarf a0-line: a0 = (g_obs^2 - g_bar^2)/g_bar is a DIRECT amplitude,")
print(f"    d ln a0 / d ln g_obs = 2 g_obs^2/(g_obs^2-g_bar^2) -> 2 deep; d ln a0/d ln Upsilon")
print(f"    = -phi(2y+1) -> O(1). Amplification ~1-2, vs WB's ~{A_MI['A_log']:.0f}. THAT ratio "
      f"(~{A_MI['A_log']/2:.0f}x) is the structural")
print("    reason WB's *smaller percentage* systematics do not buy a smaller a0 error.")

# ================================================================================== S3 ====
print()
print(BAR)
print("S3 -- THE C-a0 DEGENERACY (the risk flagged in the brief): does WB constrain a0 or C*a0^p?")
print(BAR)
print("  Take logs of the committed law:  ln(gamma^4 - 1) = ln C - ln yE(a0).  Therefore")
print("     d ln(gamma^4-1) = d ln C + p d ln a0,     p == -d ln yE/d ln a0 = "
      f"{2*(GEXT_P/A0C)**2/(yE_c*math.sqrt(1+4*(GEXT_P/A0C)**2)):.4f}")
p_deg = 2 * (GEXT_P / A0C) ** 2 / (yE_c * math.sqrt(1 + 4 * (GEXT_P / A0C) ** 2))
print(f"  A SINGLE measured gamma therefore constrains EXACTLY ONE combination: "
      f"C * a0^{p_deg:.3f} = const.")
print("  a0 is extractable ONLY if C is known a priori -- i.e. only if the EFE prescription is")
print("  FIXED. It is not: the MI-vs-MG choice is precisely a choice of C.")
# the prescription-induced a0 shift at FIXED measured gamma
def a0_from_gamma(gobs, gext, law, lo=3e-11, hi=6e-10):
    """Invert gamma_asy(a0) for a0 under a GIVEN prescription (monotone increasing in a0)."""
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if gamma_asy(mid, gext, law)[0] < gobs:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


print()
print("  DEMONSTRATION -- feed the SAME observed gamma to both prescriptions:")
print(f"  {'observed gamma':>15}{'a0 | MI reading':>18}{'a0 | MG reading':>18}{'ratio':>9}")
for gobs in (1.06, 1.09, gMI, 1.12, gMG, 1.16):
    aMI = a0_from_gamma(gobs, GEXT_P, "MI")
    aMG = a0_from_gamma(gobs, GEXT_P, "MG")
    print(f"  {gobs:>15.4f}{aMI:>18.3e}{aMG:>18.3e}{aMI/aMG:>9.3f}")
r_presc = a0_from_gamma(gMI, GEXT_P, "MI") / a0_from_gamma(gMI, GEXT_P, "MG")
print(f"  => the prescription ambiguity ALONE moves the extracted a0 by "
      f"{100*abs(r_presc-1):.1f}%  (= {100*abs(r_presc-1)/(100*TARGET):.1f}x the "
      f"{100*TARGET:.2f}% target),")
print("     with NO measurement error at all. And the framework's MI completion is UNWRITTEN")
print("     (banked: the per-star MI-EFE law is a PRESCRIPTION, not a theorem) -- so C is not")
print("     going to be pinned by theory before DR4.")

# ---- 2-parameter Fisher on the frozen DR4 binning: is a0 marginally constrained at all? ---
print()
print("  RIGOROUS VERSION -- 2-parameter Fisher (ln a0, ln C) on the FROZEN DR4 binning/shape:")
print("    frozen shape gamma(y) = 1 + (Gamma(a0,C)-1) * yE(a0)/(yE(a0)+y),  Gamma=(1+C/yE)^(1/4)")
print("    bins = frozen log10(y) edges; y_b fixed by PHYSICAL g_N (a0-independent binning of")
print("    the sky data), pair counts ~ dN/dlog s from a Opik-like s^-1.5 separation law,")
print("    per-bin sigma calibrated so the 1-PARAMETER (Gamma-only) error reproduces "
      f"{SIGFIT_30K:.4f}.")

edges = np.array(BINS_LOG10Y)
ycen = 10 ** (0.5 * (edges[1:] + edges[:-1]))         # bin centres in y at the canonical a0
gN_b = ycen * A0C                                     # PHYSICAL g_N per bin (frozen by the sky)
s_b = np.sqrt(G * MTOT / gN_b) / (1e3 * AU)           # equivalent separation, kAU
# pair counts: dN/ds ~ s^-1.5 (Opik-like), restricted to the frozen 2-30 kAU window
inwin = (s_b > 2.0) & (s_b < 30.0)
wraw = np.where(inwin, s_b ** -1.5 * np.gradient(s_b), 0.0)
wraw = np.abs(wraw)
n_b = N_GATE * wraw / wraw.sum()


def gmodel(y, a0, C, gext=GEXT_P):
    yE = y_newt(gext / a0)
    Gam = (1.0 + C / yE) ** 0.25
    return 1.0 + (Gam - 1.0) * yE / (yE + y)


def fisher(a0, C, sig_b, gext=GEXT_P):
    h = 1e-4
    y = gN_b / a0                     # y depends on a0 (physical g_N fixed)
    dA = (gmodel(gN_b / (a0 * math.exp(h)), a0 * math.exp(h), C, gext)
          - gmodel(gN_b / (a0 * math.exp(-h)), a0 * math.exp(-h), C, gext)) / (2 * h)
    dC = (gmodel(y, a0, C * math.exp(h), gext)
          - gmodel(y, a0, C * math.exp(-h), gext)) / (2 * h)
    m = sig_b > 0
    F = np.zeros((2, 2))
    F[0, 0] = np.sum(dA[m] ** 2 / sig_b[m] ** 2)
    F[1, 1] = np.sum(dC[m] ** 2 / sig_b[m] ** 2)
    F[0, 1] = F[1, 0] = np.sum(dA[m] * dC[m] / sig_b[m] ** 2)
    return F


# calibrate per-bin sigma: 1-param (Gamma only, shape fixed) error must equal SIGFIT_30K
def sig1_of_k(k):
    sb = np.where(n_b > 0, k / np.sqrt(np.maximum(n_b, 1e-9)), np.inf)
    yE = y_newt(GEXT_P / A0C)
    dG = yE / (yE + gN_b / A0C)                      # d gamma_b / d Gamma
    m = np.isfinite(sb)
    return 1.0 / math.sqrt(np.sum(dG[m] ** 2 / sb[m] ** 2))


lo, hi = 1e-4, 1e3
for _ in range(200):
    mid = math.sqrt(lo * hi)
    if sig1_of_k(mid) < SIGFIT_30K:
        lo = mid
    else:
        hi = mid
KCAL = math.sqrt(lo * hi)
sig_b = np.where(n_b > 0, KCAL / np.sqrt(np.maximum(n_b, 1e-9)), np.inf)
assert abs(sig1_of_k(KCAL) - SIGFIT_30K) < 1e-4
print(f"    calibration: per-bin sigma = {KCAL:.3f}/sqrt(n_b) reproduces sigma(Gamma) = "
      f"{sig1_of_k(KCAL):.4f} at N={N_GATE:,}")
print(f"    {'log10 y':>9}{'g_N [m/s^2]':>13}{'s [kAU]':>9}{'n_b':>8}{'sigma_b':>9}")
for i in range(len(ycen)):
    if n_b[i] > 0:
        print(f"    {math.log10(ycen[i]):>9.2f}{gN_b[i]:>13.3e}{s_b[i]:>9.2f}"
              f"{n_b[i]:>8.0f}{sig_b[i]:>9.4f}")

for law, Cv in (("MI", C_MI), ("MG", C_MG)):
    F = fisher(A0C, Cv, sig_b)
    Cov = np.linalg.inv(F)
    s_a0_marg = math.sqrt(Cov[0, 0]); s_a0_cond = 1.0 / math.sqrt(F[0, 0])
    rho = Cov[0, 1] / math.sqrt(Cov[0, 0] * Cov[1, 1])
    # degeneracy direction: eigenvector of the SMALL eigenvalue of F
    ev, EV = np.linalg.eigh(F)
    v = EV[:, 0]                                     # flat (small-eigenvalue) direction
    dlnC_dlna0 = v[1] / v[0] if abs(v[0]) > 1e-12 else np.inf
    print(f"\n    [{law}, C={Cv:.4f}]  sigma(ln a0) with C FIXED (conditional) = "
          f"{100*s_a0_cond:6.2f}%")
    print(f"    {' ':17}sigma(ln a0) with C FREE  (marginal)    = "
          f"{100*s_a0_marg:6.2f}%   correlation rho = {rho:+.4f}")
    print(f"    {' ':17}flat direction:  d ln C / d ln a0 = {dlnC_dlna0:+.4f}  vs the "
          f"asymptote-only analytic {-p_deg:+.4f}")
    print(f"    {' ':17}(the {100*abs(dlnC_dlna0/(-p_deg)-1):.0f}% offset IS the shape's "
          f"degeneracy-breaking power -- and it is why the")
    print(f"    {' ':17} marginal error is {s_a0_marg/s_a0_cond:.0f}x the conditional one, "
          f"not infinite)")
    s_C_cond = 1.0 / math.sqrt(F[1, 1])
    print(f"    {' ':17}REVERSED (the useful direction): a0 FIXED by the dwarf line ->"
          f"  sigma(ln C) = {100*s_C_cond:.2f}%")
    if law == "MI":
        SIG_A0_MARG_MI, SIG_A0_COND_MI, RHO_MI = s_a0_marg, s_a0_cond, rho
        SIG_C_COND_MI = s_C_cond
print()
print(f"  READING: with the prescription FREE the marginal sigma(ln a0) EXPLODES "
      f"(rho = {RHO_MI:+.4f}, |rho|->1);")
print("  the 8-bin shape does NOT break the degeneracy at any realistic N. The reason is S3b.")

# ---- S3b: does the transition LOCATION carry independent a0 information? -----------------
print()
print("  S3b -- WHY THE SHAPE CANNOT BREAK IT: where is the transition, physically?")
print("    In the EFE-saturated regime the boost turns on where the INTERNAL Newtonian field")
print("    drops below the EXTERNAL one, g_N(s) ~ g_extN -- and g_extN = yE(a0)*a0 is almost")
print("    a0-INDEPENDENT because y_newt compresses the ratio. Numerically:")
print(f"    {'a0':>11}{'g_extN = yE*a0':>16}{'s_half [kAU]':>14}{'s(g_N=a0) [kAU]':>17}")
sh = {}
for a0 in (A0C, 1.0e-10, A0A, A0M):
    yE = y_newt(GEXT_P / a0); gextN = yE * a0
    s_half = math.sqrt(G * MTOT / gextN) / (1e3 * AU)
    s_a0 = math.sqrt(G * MTOT / a0) / (1e3 * AU)
    sh[a0] = s_half
    print(f"    {a0:>11.3e}{gextN:>16.4e}{s_half:>14.3f}{s_a0:>17.3f}")
dln_sh = math.log(sh[A0M] / sh[A0C]) / math.log(A0M / A0C)
print(f"    d ln s_half / d ln a0 = {dln_sh:+.4f}  ->  a 1% shift in the measured transition")
print(f"    location would be a {abs(1/dln_sh):.1f}% a0 measurement -- but the transition location is")
print("    itself only measurable to tens of percent (the boost amplitude is ~0.1 and the")
print("    curve is a shallow single-decade rollover), so this channel is WEAKER than the")
print("    amplitude, not a rescue. And it is degenerate with g_ext, not just with C.")
print("  ==> CONFIRMED, as the frozen pre-registration already states (sec 1.1): 'DR4 gamma_v")
print("      constrains the nu+EFE prescription, NOT the value a0 = 9.36e-11.' This script")
print("      supplies the quantitative version of that frozen sentence.")

# ================================================================================== S4 ====
print()
print(BAR)
print("S4 -- THE WB a0 ERROR BUDGET (built in gamma, mapped to a0 with A_abs, framework-MI)")
print(BAR)
AA = A_MI["A_abs"]     # d ln a0 / d gamma, MI/canonical/primary  (framework-first)
AA_MG = A_MG["A_abs"]

# --- (a) contamination: unresolved triples / hierarchicals.  THE DOMINANT TERM. -----------
# Anchor (repo-committed): wb_threshold_audit finds a Newtonian population needs
# f_triple ~ 0.19-0.20 to absorb the DR3 deep-bin excess that produced gamma = 1.205.
# => the LEVER  d gamma / d f_triple  is bracketed by the two truth hypotheses:
LEV_LO = (GAM_DR3 - 1.09) / 0.195     # if the truth were MI 1.09
LEV_HI = (GAM_DR3 - 1.00) / 0.195     # if the truth were Newton 1.00
FTRIP_DR3 = 0.195                     # DR3-era residual (3 of Banik's screens NOT implementable)
# DR4 residual after RUWE<1.4 + NSS + RV + resolved-companion search: ASSUMED BAND.
FTRIP_DR4 = (0.02, 0.04, 0.08)        # ASSUMED (low / central / high); NSS completeness for the
                                      # relevant inner-companion period range is unpublished
print(f"  (a) CONTAMINATION (unresolved triples/hierarchicals) -- ONE-SIDED, biases gamma HIGH")
print(f"      committed lever from wb_threshold_audit: f_triple = {FTRIP_DR3:.3f} absorbs the")
print(f"      DR3 deep excess -> d gamma/d f_triple in [{LEV_LO:.2f}, {LEV_HI:.2f}] "
      f"(MI-truth / Newton-truth brackets)")
print(f"      DR3 residual f_triple ~ {FTRIP_DR3:.3f} (3 Banik screens not implementable at eDR3)")
print(f"      DR4 residual f_triple = {FTRIP_DR4} = **ASSUMED BAND** (NSS completeness for the")
print("        inner-companion period range that matters is not yet published)")
lev_c = 0.5 * (LEV_LO + LEV_HI)
contam = {"DR3": FTRIP_DR3 * lev_c,
          "DR4_lo": FTRIP_DR4[0] * LEV_LO, "DR4_mid": FTRIP_DR4[1] * lev_c,
          "DR4_hi": FTRIP_DR4[2] * LEV_HI}
for k, v in contam.items():
    print(f"        {k:<8} gamma bias/uncertainty = {v:.4f}  ->  a0: {100*AA*v:6.1f}%")
print("      NOTE the SIGN: contamination pushes gamma UP, hence the extracted a0 UP, i.e.")
print("      TOWARD the 1.13-1.20e-10 cluster. An uncorrected WB 'measurement' would appear to")
print("      DISFAVOUR the canonical footing as a pure artifact. Flagged so it is never cited.")

# --- (b) PHOTOMETRIC stellar mass -- correcting the prior overstatement ------------------
print()
print("  (b) PHOTOMETRIC STELLAR MASS -- CORRECTION OF THE PRIOR OVERSTATEMENT")
print("      WB masses are NOT systematic-free. They come from the Banik+2024 eq.6 cubic")
print(f"      M_G -> M (Pecaut-Mamajek/FLAME calibrated), per-pair error {100*MASS_PP:.1f}% "
      f"(his sec 2.3.3).")
print("      Propagation: gamma is v_obs / sqrt(G M_tot / s), so gamma ~ M^(-1/2):")
print("         d ln gamma = -0.5 d ln M   ->   d gamma = -0.5 gamma d ln M")
print("      SPLIT (the load-bearing distinction, exactly as in STEP A):")
print(f"        * per-pair RANDOM {100*MASS_PP:.1f}%: AVERAGES DOWN -> "
      f"{100*0.5*MASS_PP/math.sqrt(N_GATE):.3f}% in gamma at N=30k. Negligible. TRUE 'tighter than Upsilon'.")
MZP = (0.02, 0.035, 0.05)   # ASSUMED coherent zero-point band for the MS M-L calibration
print(f"        * COHERENT ZERO-POINT of the M-L relation: {MZP} = **ASSUMED BAND** "
      f"({100*MZP[0]:.0f}-{100*MZP[2]:.0f}%).")
print("          Grounds (stated, not hidden): main-sequence M-L calibrations are good to a few")
print("          per cent, BUT the sample-average metallicity/age offset, the Gaia G-band")
print("          bandpass/extinction zero-point, and residual unresolved-faint-companion light")
print("          (which biases photometric M HIGH) are all coherent across the whole catalog.")
print("          This is genuinely TIGHTER than the galaxy Upsilon 0.10 dex (=23%) -- by ~6x --")
print("          and it STILL does not help, because of the amplification (see the a0 column).")
mass_g = tuple(0.5 * gMI * m for m in MZP)
for m, gg in zip(MZP, mass_g):
    print(f"          coherent {100*m:>4.1f}% mass -> gamma {gg:.4f} -> a0 {100*AA*gg:5.1f}%")
print(f"      HONEST HEADLINE: galaxy Upsilon 23% x amplification ~1 = ~8% in a0 (STEP A's sysU");
print(f"      is 8.1%);  WB mass {100*MZP[1]:.1f}% x amplification {AA:.1f} = "
      f"{100*AA*mass_g[1]:.1f}% in a0. The 6x tighter")
print("      calibration is MORE than undone by the ~9x worse lever. 'No Upsilon at all' is FALSE.")

# --- (c) eccentricity prior ---------------------------------------------------------------
print()
print(f"  (c) ECCENTRICITY PRIOR: gate-measured flat-vs-thermal shift = {ECC_SHIFT:.4f} in gamma")
print("      (Hwang+2022 SUPERTHERMAL lies beyond thermal on the same axis, same magnitude,")
print(f"      opposite sign -> carried symmetric).  -> a0: {100*AA*ECC_SHIFT:.1f}%")

# --- (d) deprojection / orbit (semi-major-axis) prior ------------------------------------
DEPROJ = (0.010, 0.020, 0.035)   # ASSUMED band, anchored on the committed MC finding below
print()
print("  (d) DEPROJECTION / ORBITAL-a PRIOR: the committed wb_mond_orbit_mc.py finding is that")
print("      a log-uniform 3D semi-major-axis prior leaks deep-regime apocentre boost into")
print("      high-acceleration sky bins -- Newton-pop returns 0.60-0.67 vtilde vs the validated")
print("      conditioned baseline 0.55 (a ~9-22% baseline error), i.e. sky-projected data do NOT")
print(f"      constrain the a-prior.  Carried as {DEPROJ} in gamma = **ASSUMED BAND** anchored on")
print("      that committed result (the frozen pipeline's Kepler forward model fixes ONE prior).")
for d in DEPROJ:
    print(f"        {d:.3f} in gamma -> a0 {100*AA*d:5.1f}%")

# --- (e) g_ext calibration: enters at 1:1, NOT amplified ---------------------------------
print()
print("  (e) g_ext CALIBRATION -- a term with NO amplification, and that is the point:")
gr = math.log(GEXT_A / GEXT_P)
print(f"      a0 and g_ext enter ONLY as the ratio y_obs = g_ext/a0, so d ln a0 = d ln g_ext")
print(f"      EXACTLY (1:1).  Frozen convention spread 1.778 vs 2.078e-10 = "
      f"{100*gr:.1f}% -> a0 {100*gr:.1f}%.")
gMI_alt = gamma_asy(A0C, GEXT_A, "MI")[0]
print(f"      (cross-check through gamma: gamma_MI {gMI:.4f} -> {gMI_alt:.4f}, "
      f"Delta = {gMI_alt-gMI:+.4f}; x A_abs = {100*AA*abs(gMI_alt-gMI):.1f}% ~ {100*gr:.1f}% OK)")
print("      If instead the kinematic Vc^2/R0 is adopted with its own error (Vc 229+-2 km/s,")
print("      R0 8.178+-0.026 kpc -> ~2%), this term falls to ~2-3%. BOTH carried: 2-16%.")
GEXT_TERMS = (0.025, gr)

# --- (f) statistics ----------------------------------------------------------------------
def sigfit(N):
    return SIGFIT_30K * math.sqrt(N_GATE / N)


print()
print("  (f) STATISTICS (frozen pipeline scaling sigma_fit = 0.0191 sqrt(30000/N)):")
print(f"      {'N pairs':>10}{'sigma_fit':>11}{'-> a0':>9}")
for N in (5000, N_DR3, N_GATE, 60000, 150000, 500000):
    print(f"      {N:>10,}{sigfit(N):>11.4f}{100*AA*sigfit(N):>8.1f}%")

# ================================================================================== S5 ====
print()
print(BAR)
print("S5 -- ACHIEVABLE sigma(a0)/a0 FROM WIDE BINARIES, AND THE JOINT WITH STEP A")
print(BAR)


def q(*x):
    return math.sqrt(sum(v * v for v in x))


scen = {}
# --- DR3 today ---------------------------------------------------------------------------
g_dr3 = q(SIG_DR3, contam["DR3"], ECC_SHIFT, DEPROJ[1], mass_g[1])
scen["DR3 today (contamination-limited)"] = dict(
    sig_gamma=g_dr3, note="contamination term is the DR3 residual f_trip~0.195 (guard zone)")
# --- DR4, frozen allowance only (the pre-registration's own sigma_tot) -------------------
g_dr4_frz = q(sigfit(N_GATE), SIGSYS_FRZ)
scen["DR4 frozen sigma_tot (prereg, hypothesis-test use)"] = dict(
    sig_gamma=g_dr4_frz, note="the frozen 0.02 sys allowance; does NOT include a contamination sigma")
# --- DR4, a0-AMPLITUDE use: contamination MUST be carried -------------------------------
for tag, ft, lev, mz, dp, ge in (
        ("DR4 optimistic", FTRIP_DR4[0], LEV_LO, MZP[0], DEPROJ[0], GEXT_TERMS[0]),
        ("DR4 central",    FTRIP_DR4[1], lev_c,  MZP[1], DEPROJ[1], GEXT_TERMS[0]),
        ("DR4 conservative",FTRIP_DR4[2], LEV_HI, MZP[2], DEPROJ[2], GEXT_TERMS[1])):
    sg = q(sigfit(N_GATE), ft * lev, ECC_SHIFT, dp, 0.5 * gMI * mz)
    scen[f"{tag} (a0-amplitude use)"] = dict(sig_gamma=sg, gext=ge,
                                            note=f"f_trip={ft}, mass zp={mz}, deproj={dp}")
# --- the theoretical best: perfect gamma, only the irreducible non-gamma terms -----------
scen["DR4 'perfect gamma' limit (sigma_gamma=0)"] = dict(sig_gamma=0.0, gext=GEXT_TERMS[0],
                                                        note="only g_ext + prescription remain")

print(f"  mapping: sigma(ln a0) = quadrature[ A_abs*sigma(gamma) , sigma(ln g_ext) ,")
print(f"           prescription C ambiguity ]   with A_abs = {AA:.2f} (MI) / {AA_MG:.2f} (MG)")
print(f"  prescription (MI-vs-MG) a0 ambiguity, computed in S3 = {100*abs(r_presc-1):.1f}%")
print()
hdr = (f"  {'scenario':<52}{'sig(gam)':>9}{'a0 gam':>8}{'a0 +gext':>10}"
       f"{'a0 +presc':>11}{'beats 6.31%?':>13}")
print(hdr)
res = {}
for k, v in scen.items():
    sg = v["sig_gamma"]; ge = v.get("gext", GEXT_TERMS[0])
    a_g = AA * sg
    a_gg = q(a_g, ge)
    a_all = q(a_gg, abs(r_presc - 1))
    res[k] = dict(sig_gamma=sg, a0_gamma=a_g, a0_gext=a_gg, a0_full=a_all)
    print(f"  {k:<52}{sg:>9.4f}{100*a_g:>7.1f}%{100*a_gg:>9.1f}%{100*a_all:>10.1f}%"
          f"{('YES' if a_all <= TARGET else 'no'):>13}")

WB_BEST = min(res[k]["a0_full"] for k in res)
WB_BEST_G = min(res[k]["a0_gamma"] for k in res if res[k]["sig_gamma"] > 0)
print()
print(f"  BEST-CASE WB sigma(a0)/a0 (full, incl. prescription) = {100*WB_BEST:.1f}%")
print(f"  BEST-CASE WB sigma(a0)/a0 counting ONLY the gamma budget (prescription+g_ext ASSUMED")
print(f"  AWAY, i.e. the most generous possible reading) = {100*WB_BEST_G:.1f}%")

print()
print("  --- THE JOINT: does WB + dwarf beat the STEP-A floor? (orthogonality granted) ---")
print("  Orthogonality audit (the hypothesis's premise): dwarf terms {Upsilon, gas-cal,")
print("  estimator choice, distance, inclination} vs WB terms {triples, deprojection/a-prior,")
print("  eccentricity prior, photometric M-L zero-point, g_ext, EFE prescription C}.")
print("  These lists are DISJOINT -- the premise is GRANTED, not disputed. Quadrature applies.")
print(f"  {'combination':<64}{'joint sigma(a0)/a0':>20}{'beats 6.31%?':>14}")
joint = {}
for dl, dv in (("SPARC-alone floor 11.62%", DWARF_FLOOR),
               ("with BOTH external priors 6.78%", DWARF_COND)):
    for wl, wv in (("WB full best", WB_BEST), ("WB gamma-only best", WB_BEST_G),
                   ("WB frozen-prereg sigma_tot", res["DR4 frozen sigma_tot (prereg, hypothesis-test use)"]["a0_gamma"])):
        j = 1.0 / math.sqrt(1.0 / dv ** 2 + 1.0 / wv ** 2)
        joint[f"{dl} + {wl}"] = j
        print(f"  {dl + '  (+)  ' + wl:<64}{100*j:>19.2f}%"
              f"{('YES' if j <= TARGET else 'no'):>14}")

# what would WB need to deliver?
need_floor = 1.0 / math.sqrt(max(1.0 / TARGET ** 2 - 1.0 / DWARF_FLOOR ** 2, 1e-12))
need_cond = 1.0 / math.sqrt(max(1.0 / TARGET ** 2 - 1.0 / DWARF_COND ** 2, 1e-12))
need_gam_floor = need_floor / AA
N_need = N_GATE * (SIGFIT_30K / max(need_gam_floor, 1e-9)) ** 2
print()
print(f"  REQUIREMENT INVERSION -- for the JOINT to reach {100*TARGET:.2f}%:")
print(f"    against the SPARC-alone floor {100*DWARF_FLOOR:.2f}%, WB must deliver "
      f"sigma(a0)/a0 <= {100*need_floor:.2f}%")
print(f"      = sigma(gamma) <= {need_gam_floor:.4f}  (vs the FROZEN sigma_sys allowance alone = "
      f"{SIGSYS_FRZ:.3f})")
print(f"      = N >= {N_need:,.0f} pairs on statistics alone, AND every systematic in S4 driven")
print(f"        below {need_gam_floor:.4f} in gamma, AND the C-prescription pinned to better than "
      f"{100*need_floor*p_deg:.1f}% in C.")
print(f"    against the with-both-priors dwarf {100*DWARF_COND:.2f}%, WB must deliver "
      f"<= {100*need_cond:.2f}%.")
print(f"    Every one of these is beaten by the prescription ambiguity ({100*abs(r_presc-1):.1f}%) "
      f"ALONE, before any data.")
print()
print("  HOW CLOSE DOES WB GET IN ITS SINGLE MOST GENEROUS CORNER? (stated so the NO-GO is not")
print("  overstated: this is a shortfall factor, not an order of magnitude)")
print(f"    most generous corner = dwarf at its conditional {100*DWARF_COND:.2f}% (both external")
print(f"    priors delivered) + WB with the prescription and g_ext ASSUMED AWAY entirely")
print(f"    ({100*WB_BEST_G:.1f}%): WB is short by a factor "
      f"{WB_BEST_G/need_cond:.2f}x (needs <= {100*need_cond:.2f}%).")
print(f"    against the realistic SPARC-alone floor the shortfall factor is "
      f"{WB_BEST_G/need_floor:.1f}x (gamma-only) / {WB_BEST/need_floor:.1f}x (full).")
print()
print("  THE ONE JOINT DIRECTION THAT DOES WORK (and it is not an a0 measurement):")
print(f"    run the inference BACKWARDS -- fix a0 from the dwarf line and let WB measure the EFE")
dlnC_gap = math.log(C_MG / C_MI)
nsig_C = dlnC_gap / SIG_C_COND_MI
print(f"    prescription C. Fisher, C conditional on a0: sigma(ln C) = {100*SIG_C_COND_MI:.1f}% at "
      f"N=30k.")
nsig_g = (gMG - gMI) / SIGFIT_30K
print(f"    MI-vs-MG separation, three ways (reported side by side, none hidden):")
print(f"      (i)   linearized in ln C: gap ln(C_MG/C_MI) = {dlnC_gap:.3f} / sigma(lnC) "
      f"{SIG_C_COND_MI:.3f} = {nsig_C:.2f} sigma  -> 3 sigma at N ~ {N_GATE*(3/nsig_C)**2:,.0f}")
print(f"      (ii)  direct in gamma, COMPUTED asymptotes {gMI:.4f} vs {gMG:.4f}: "
      f"{nsig_g:.2f} sigma -> 3 sigma at N ~ {N_GATE*(3/nsig_g)**2:,.0f}")
print(f"      (iii) the frozen pipeline's own forecast, which uses the frozen POINT TARGET 1.09")
print(f"            (not the computed 1.1015): gap 0.047 -> 2.46 sigma -> N ~ 44,689")
print(f"    These differ by up to {N_GATE*(3/nsig_C)**2/44689:.1f}x. The spread is NOT noise: (iii)")
print(f"    uses a 25% larger gap than (ii), and (i) is the linearization of a finite 37% C ratio.")
print(f"    The like-for-like number is (ii), N ~ {N_GATE*(3/nsig_g)**2:,.0f} for 3 sigma -- i.e. the frozen")
print("    pre-registration's 'MI-vs-MG likely UNDECIDABLE in DR4' stands, and if anything the")
print("    computed-asymptote gap makes it HARDER than the frozen forecast, not easier.")
print("    That is exactly the frozen pre-registration's own Door-4A test, and it is where WB's")
print("    real value sits. The dwarf line supplies a0; WB supplies C. Not the reverse.")

# ================================================================================ VERDICT =
print()
print(BAR)
print("VERDICT (honest, both directions -- a manufactured GO and a manufactured NO-GO are equal)")
print(BAR)
print(f"  1. THE SENSITIVITY IS THE KILLER, NOT THE SYSTEMATICS LIST. The 1/4 power PLUS EFE")
print(f"     saturation give d ln a0/d ln gamma = {A_MI['A_log']:.2f} (MI, the framework's own")
print(f"     reading; {A_MG['A_log']:.2f} for MG). Per absolute gamma unit, "
      f"sigma(a0)/a0 = {AA:.2f} sigma(gamma).")
print(f"     The dwarf a0-line's amplification is ~1-2. WB needs ~{AA/1.5:.0f}x better fractional")
print("     precision than the dwarf line just to TIE it. It does not have it.")
print(f"  2. THE DEGENERACY BLOCKS THE AMPLITUDE EXTRACTION OUTRIGHT. A single gamma constrains")
print(f"     C * a0^{p_deg:.3f} only (exact, S3). With C free the Fisher marginal sigma(ln a0) is")
print(f"     {100*SIG_A0_MARG_MI:.0f}% (rho = {RHO_MI:+.4f}); with C fixed by prescription it is "
      f"{100*SIG_A0_COND_MI:.1f}%.")
print(f"     Choosing MI vs MG alone slides the extracted a0 by {100*abs(r_presc-1):.1f}% = "
      f"{abs(r_presc-1)/TARGET:.1f}x the target,")
print("     with zero measurement error -- and the MI completion that would pin C is UNWRITTEN.")
print("     The frozen pre-registration already forbids reporting DR4 gamma as an a0 measurement")
print("     (sec 1.1); this is the quantitative backing for that frozen sentence.")
print(f"  3. CONTAMINATION IS THE SECOND WALL, ONE-SIDED AND UPWARD. DR3's gamma = {GAM_DR3:.3f} is")
print(f"     absorbable by f_triple ~ {FTRIP_DR3:.2f} (committed audit); the DR3-today WB a0 error is")
print(f"     ~{100*res['DR3 today (contamination-limited)']['a0_full']:.0f}%. WB CANNOT supply a usable a0 amplitude TODAY.")
print("     Its bias direction pushes a0 UP, toward the ALT/MOND cluster -- so a naive WB number")
print("     would look like evidence against the canonical footing purely as an artifact.")
print(f"  4. THE MASS-SYSTEMATIC OVERSTATEMENT IS CORRECTED. WB photometric masses are ~6x")
print(f"     tighter than galaxy Upsilon in PERCENT ({100*MZP[1]:.1f}% coherent vs 23%), and that buys")
print(f"     NOTHING: {100*AA*mass_g[1]:.1f}% in a0 vs the dwarf line's 8.1% sysU. 'No Upsilon at all'")
print("     is false; the correct statement is 'a smaller mass error through a much worse lever'.")
print(f"  5. ORTHOGONALITY IS REAL BUT WORTHLESS HERE. The systematics lists ARE disjoint, so the")
print(f"     joint is a legitimate quadrature -- but {100*DWARF_FLOOR:.2f}% (+) "
      f"{100*WB_BEST:.0f}% = "
      f"{100*joint['SPARC-alone floor 11.62% + WB full best']:.2f}%: the dwarf floor barely")
print(f"     moves. Even the most generous reading (prescription and g_ext assumed away, WB at")
print(f"     {100*WB_BEST_G:.1f}%) gives "
      f"{100*joint['SPARC-alone floor 11.62% + WB gamma-only best']:.2f}% -- still above "
      f"{100*TARGET:.2f}%.")
print("  6. ANSWER TO THE POSED QUESTION: **NO.** Gaia wide binaries cannot supply an")
print(f"     a0-AMPLITUDE constraint that helps the Step-A floor -- not today "
      f"(~{100*res['DR3 today (contamination-limited)']['a0_full']:.0f}%, contamination-")
print(f"     limited), and not with DR4 ({100*res['DR4 optimistic (a0-amplitude use)']['a0_full']:.0f}"
      f"-{100*res['DR4 conservative (a0-amplitude use)']['a0_full']:.0f}% across the assumed")
print(f"     contamination band, with a hard {100*abs(r_presc-1):.0f}% floor from the prescription alone even at")
print(f"     sigma(gamma)=0). Shortfall factors: {WB_BEST_G/need_floor:.1f}x against the SPARC-alone floor,")
print(f"     {WB_BEST_G/need_cond:.1f}x in the single most generous corner. The blocking reason is NOT the")
print("     orthogonality premise (which HOLDS) but (i) the ~9x desensitization of the 1/4-power")
print("     EFE-saturated map and (ii) the exact C-a0 degeneracy that only a WRITTEN MI")
print("     completion could break. Both are structural, not fixable with more pairs.")
print("  7. WHAT WB IS STILL GOOD FOR (unchanged, and not diminished): the frozen DR4 test of")
print("     the nu+EFE PRESCRIPTION -- Newton vs framework-MI 1.09 is forecast DECIDABLE at")
print("     N >~ 12,200. That is a test of the interpolation+EFE physics, not of a0's value.")
print("     No door is closed here; the a0-amplitude door in WB is simply not open, and the")
print("     dwarf a0-line's external-data path (TRGB + M/L + HI campaign) remains the live one.")

# ------------------------------------------------------------------------------------ JSON
out = dict(
    stepA=dict(target=TARGET, box_now=DWARF_NOW, sparc_alone_floor=DWARF_FLOOR,
               conditional=DWARF_COND),
    anchors=dict(gamma_MI=gMI, gamma_MG=gMG, y_extN=yE_c, C_MI=C_MI, C_MG=C_MG,
                 gamma_DR3=GAM_DR3, sig_DR3=SIG_DR3),
    sensitivity=[{k: v for k, v in r.items()} for r in rows],
    A_log_MI=A_MI["A_log"], A_abs_MI=AA, A_log_MG=A_MG["A_log"], A_abs_MG=AA_MG,
    degeneracy=dict(p_exponent=p_deg, combination=f"C * a0^{p_deg:.4f}",
                    prescription_a0_shift=abs(r_presc - 1),
                    fisher_sigma_lna0_Cfixed=SIG_A0_COND_MI,
                    fisher_sigma_lna0_Cfree=SIG_A0_MARG_MI, fisher_rho=RHO_MI,
                    dln_shalf_dln_a0=dln_sh),
    budget_gamma=dict(contamination=contam, mass_coherent={str(m): 0.5*gMI*m for m in MZP},
                      mass_perpair_random=0.5*MASS_PP/math.sqrt(N_GATE),
                      eccentricity=ECC_SHIFT, deprojection=list(DEPROJ),
                      gext_lnratio=gr, statistics={str(N): sigfit(N) for N in
                                                   (5000, N_DR3, N_GATE, 60000, 150000, 500000)}),
    scenarios={k: res[k] for k in res},
    wb_best_full=WB_BEST, wb_best_gamma_only=WB_BEST_G,
    joint=joint, need_wb_vs_floor=need_floor, need_wb_vs_conditional=need_cond,
    need_sigma_gamma=need_gam_floor, need_N=N_need,
    assumed_inputs=dict(ftrip_DR4=list(FTRIP_DR4), mass_zeropoint=list(MZP),
                        deprojection=list(DEPROJ),
                        note="labeled ASSUMED bands; verdict shown robust across all three"),
    verdict="NO -- WB cannot supply a usable a0 AMPLITUDE. Blocked by (i) A_abs~9 desensitization "
            "of the 1/4-power EFE-saturated map and (ii) the exact C*a0^p degeneracy (MI-vs-MG "
            "alone = 30% in a0). DR3 today is contamination-limited (~100%+). DR4 forecast "
            "~20-30%. Joint with the dwarf floor moves 11.62% -> ~10-11%, never to 6.31%. "
            "Orthogonality premise GRANTED and still insufficient. WB remains valuable for the "
            "frozen nu+EFE PRESCRIPTION test, which is not an a0 measurement.")
json.dump(out, open(os.path.join(HERE, "wb_a0_amplitude_budget_results.json"), "w"),
          indent=1, default=float)
print(f"\n[wb_a0_amplitude_budget_results.json written]")
print("EXIT 0: WB a0-amplitude sensitivity + error budget computed. Exit code is not a verdict.")
