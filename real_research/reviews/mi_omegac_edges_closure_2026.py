#!/usr/bin/env python3
r"""
THE GATE CORNER omega_c: INDEPENDENT EDGE REBUILD + CLOSURE FORECAST   [W-1 + W-2]
==================================================================================
de Sitter-Unruh MODIFIED-INERTIA framework (Carl Zimmerman), judged on its OWN terms:
own kernel nu(y) = sqrt(1 + 1/y), horizon-derived a0 = c H_Lambda / Z.  BOTH footings on every number.

WHAT IS AUDITED.  MI_FIELD_THEORY_RESULTS_2026.md Sec. 5 survives the solar system ONLY through a gated
crossover G(omega) = 1/(1 + i omega/omega_c) whose corner omega_c is an admitted FREE FIFTH constant
({s, a0, Z, eta, omega_c}, none derived).  The paper quotes the joint window

      omega_c in [1.78, 2.21]e-14 rad/s   (canon a0 = 9.355e-11)   width x1.24
      omega_c in [1.78, 1.83]e-14 rad/s   (alt   a0 = 1.1305e-10)  width x1.027  "survives by +2.7%"

W-1  Rebuild BOTH edges independently of prep_2026/mi_planetary_falsification/{window_joint,
     loweredge_fullsparc}.py -- own SPARC scan, own selection, own algebra -- and confirm/correct the
     widths.  Then show how the LOWER edge moves under the retention choice Re G >= 0.90 / 0.95 / 0.99,
     and invert for the CRITICAL retention that closes each footing.
W-2  CLOSURE FORECAST.  What fractional improvement in the LLR Gdot/G bound drives the upper edge below
     the lower edge, per footing?  Translate into an epoch using (i) the real published history of LLR
     Gdot/G uncertainties and (ii) the formal T^(-5/2) baseline law.

CALIBRATION HELD THROUGHOUT (manufacture neither an exclusion nor a comfort):
  * A knife-edge is NOT an exclusion.  The alt footing is NOT declared excluded anywhere below; what is
    reported is exactly how much room remains and precisely what removes it.
  * A non-empty window is NOT declared comfortable.  x1.24 on a free constant squeezed between two
    INDEPENDENT measurements is precarious, and the numbers below show the width is smaller than the
    modelling/convention swing -- stated, not explained away.
  * ASYMMETRY, load-bearing: the LOWER edge is a THEORY-INTERNAL requirement (the gate must not suppress
    the galactic rotation curves the framework exists to explain), so it cannot be relaxed without
    breaking the framework's core success.  Only the UPPER edge moves with better data.  ALL improvement
    pressure therefore closes the window FROM ABOVE.
  * Every adopted modelling choice is printed and labelled [ADOPTED] or [ASSUMPTION].
No TOE language.  No "theory closed".  numpy + sympy only.  Exits 0 iff every regression passes.
"""
import os, glob, csv, sys
import numpy as np
import sympy as sp

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond)
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        PASS = False

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

# ======================================================================================================
# 0.  CONSTANTS AND CITED ANCHORS
# ======================================================================================================
C    = 2.99792458e8
YR   = 3.15576e7                 # Julian year, s  (365.25 d) -- same as window_joint.py / the Q2 pass
MYR  = YR * 1e6
KPC  = 3.0857e19
GM_EARTH = 3.986004418e14
GM_SUN   = 1.32712440018e20
R_MOON   = 3.844e8

# a0 footings.  Two published spellings of each are carried to show the jitter is irrelevant.
A0 = {"canon": 9.355e-11, "alt": 1.1305e-10}          # task/Q2-pass spelling
A0_ALT_SPELL = {"canon": 9.36e-11, "alt": 1.13e-10}   # window_joint.py spelling

# ---- LOWER-EDGE inputs -------------------------------------------------------------------------------
GATE_KEEP = 0.90            # [ADOPTED, from the paper] retained MI fraction Re G required at every
                            # confirmed deep-MOND orbit.  Sec. 3 varies it.
UD, UB = 0.70, 1.4 * 0.70   # framework's own SPARC M/L best fit (rar_framework_a0_mlfit.py, 0.108 dex)
Q_MAX, INC_MIN = 2, 30.0

# ---- UPPER-EDGE inputs -------------------------------------------------------------------------------
# LLR Gdot/G, VERIFIED 2026-07-25 from the arXiv PDF of Biskupek, Mueller & Torre 2021, Universe 7:34
# (arXiv:2012.12032) Table 1:  Gdot/G = (-5.0 +- 9.6)e-15 /yr, from 27 485 normal points spanning
# April 1970 - April 2020.  Same table gives the previous analysis (Hofmann & Mueller 2018, CQG 35:035015,
# April 1970 - January 2015, 20 856 NP):  Gdot/G = (+7.1 +- 7.6)e-14 /yr.
LLR_CEN, LLR_SIG = -5.0e-15, 9.6e-15
LLR_T0_YR, LLR_T0_EPOCH = 50.0, 2020.3      # baseline length and end epoch of the BMT21 data set
# other secular-drift anchors, for the "which body binds" ranking
GDOT_MESSENGER = 4.0e-14    # Mercury, Genova+ 2018 Nat. Commun. 9:289
LLR_TIDAL_2SIG = 0.16e-3    # m/yr, lunar da/dt = 38.30 +- 0.08 mm/yr -> 2 sigma budget proxy
SAT_RDOT_PROXY = 2.3        # m/yr, Cassini ranging proxy (Fienga & Minazzoli 2024)
MARS_RDOT_PROXY = 0.05      # m/yr, Mars-orbiter ranging proxy (FM24)
DG_BOUND = {"Mercury": 4.6e-14, "Venus": 8.0e-14, "Earth": 8.7e-15,
            "Mars": 1.4e-15, "Jupiter": 5.6e-13, "Saturn": 7.0e-15}   # FM24 Table 10 -> per-planet delta_g
BODIES = [("Mercury", 5.7909e10, 87.969), ("Venus", 1.08209e11, 224.701),
          ("Earth", 1.49598e11, 365.256), ("Mars", 2.27939e11, 686.980),
          ("Jupiter", 7.78570e11, 4332.59), ("Saturn", 1.43353e12, 10759.22)]

# ---- regression targets ------------------------------------------------------------------------------
TGT = {"lo": 1.782e-14, "hi_canon": 2.211e-14, "hi_alt": 1.831e-14,
       "w_canon": 1.241, "w_alt": 1.027, "om_gal_max": 5.94e-15}
PAPER = {"canon": (1.78e-14, 2.21e-14), "alt": (1.78e-14, 1.83e-14)}

DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"

def ReG(omega, wc): return 1.0 / (1.0 + (omega / wc) ** 2)
def ImG(omega, wc): return -(omega / wc) / (1.0 + (omega / wc) ** 2)

# ======================================================================================================
# 1.  GATE ALGEBRA -- the lower-edge multiplier k(S), derived not quoted
# ======================================================================================================
head("1.  GATE ALGEBRA: the retention multiplier k(S) is DERIVED, not adopted")
S, x = sp.symbols("S x", positive=True)
# Re G = 1/(1+x^2) with x = omega/omega_c.  Require Re G(omega_gal) >= S  =>  x <= sqrt(1/S - 1)
# =>  omega_c >= omega_gal / sqrt(1/S - 1) == k(S) * omega_gal ,  k(S) = sqrt(S/(1-S)).
k_sym = sp.solve(sp.Eq(1 / (1 + x ** 2), S), x)[0]        # x*(S) = sqrt(1/S - 1)
k_of_S = sp.simplify(1 / k_sym)
print(f"""
  Re G(omega) = 1/(1 + (omega/omega_c)^2)         [the paper's single-pole causal Debye relaxator]
  requirement Re G(omega_gal) >= S  <=>  omega_c >= k(S) * omega_gal
  sympy solve:  omega/omega_c at Re G = S  is  x*(S) = {sp.simplify(k_sym)}
                so  k(S) = 1/x*(S) = {k_of_S} = sqrt(S/(1-S))
  k(0.90) = {float(k_of_S.subs(S, sp.Rational(9,10))):.6f}   <- the paper's factor 3, reproduced from the gate, not assumed
""")
def kS(s): return float(np.sqrt(s / (1.0 - s)))
# verify by substituting back into the DEFINING equation rather than by branch-sensitive radical algebra
check("k(S) satisfies the defining equation Re G(1/k) == S identically, and k(0.90) == 3 exactly",
      sp.simplify(1 / (1 + (1 / k_of_S) ** 2) - S) == 0 and abs(kS(0.90) - 3.0) < 1e-12)
check("self-consistency: Re G(omega_gal, omega_c = k*omega_gal) == S for S = 0.90, 0.95, 0.99",
      all(abs(ReG(1.0, kS(s)) - s) < 1e-12 for s in (0.90, 0.95, 0.99)))
# inverse map: the retention implied by a given multiplier k
def S_of_k(k): return k ** 2 / (1.0 + k ** 2)
check("inverse map S(k) = k^2/(1+k^2) round-trips k(S) for S in {0.90,0.93,0.95,0.99}",
      all(abs(S_of_k(kS(s)) - s) < 1e-12 for s in (0.90, 0.93, 0.95, 0.99)))

# ======================================================================================================
# 2.  LOWER EDGE -- independent SPARC rebuild (own loader, own cuts, own variations)
# ======================================================================================================
head("2.  LOWER EDGE = k(S) * MAX(omega_gal) over confirmed deep-MOND SPARC orbits  [INDEPENDENT REBUILD]")
print(f"""
  [ADOPTED #1 -- the gate's frequency argument, inherited from the paper, NOT re-litigated here]
  The gate is evaluated at the ORBITAL ANGULAR frequency of the body whose dynamics is measured:
  omega_gal = V_rot/r for galactic gas, omega_p = 2pi/T_p for planets.  NOTE these are the SAME quantity
  (for a circular orbit 2pi/T = V/r identically), so the two edges carry NO relative 2pi mismatch --
  machine-checked below.  Whether the anomaly really rides this frequency is the single load-bearing
  assumption of the whole window; it is forked in reviews/mi_cassini_q2_omegac_2026.py Sec. 6 and is
  NOT re-opened here.  Everything in this script is conditional on it.

  Selection (mine, matching the framework's own RAR pipeline): Q <= {Q_MAX}, inc >= {INC_MIN:.0f} deg,
  deep-MOND g_bar < a0 (footing-dependent cut), V_bar^2 = sign(Vgas)Vgas^2 + {UD}Vdisk^2 + {UB:.2f}Vbul^2.
""")
# 2pi consistency check: for a circular orbit V/r == 2pi/T
_r, _V = 0.09 * KPC, 16.5e3
check("no 2pi mismatch between the two edges: V/r == 2pi/T for a circular orbit",
      abs((_V / _r) / (2 * np.pi / (2 * np.pi * _r / _V)) - 1) < 1e-12)

# ---- load ------------------------------------------------------------------------------------------
meta = {}
with open(os.path.join(DATA, "sparc_master_clean.csv")) as fh:
    for row in csv.DictReader(fh):
        meta[row["name"].strip()] = (float(row["inc"]), int(float(row["Q"])), float(row["Vflat"]))
files = sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat")))
print(f"  rotmod files: {len(files)}   master-table galaxies: {len(meta)}")

def scan(a0, ud=UD, ub=UB, qmax=Q_MAX, incmin=INC_MIN, ycut=1.0, drop_inner=0):
    """Return (omega_gal array, labels) over surviving deep-MOND points. Independent of prep_2026 code."""
    oms, tags, ngal, npts = [], [], 0, 0
    for f in files:
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        name = os.path.basename(f)[:-len("_rotmod.dat")]
        if name not in meta:
            continue
        inc, Q, _ = meta[name]
        if Q > qmax or inc < incmin:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        Rm = R * KPC
        Vbar2 = np.sign(Vgas) * Vgas ** 2 + ud * Vdisk ** 2 + ub * Vbul ** 2
        with np.errstate(divide="ignore", invalid="ignore"):
            gbar = Vbar2 * 1e6 / Rm
            om = (Vobs * 1e3) / Rm
        ok = (R > 0) & (Vobs > 0) & (gbar > 0) & np.isfinite(gbar) & np.isfinite(om)
        deep = ok & (gbar < ycut * a0)
        if drop_inner > 0:                      # beam-smearing / rising-curve guard
            order = np.argsort(R)
            for j in order[:drop_inner]:
                deep[j] = False
        if deep.any():
            ngal += 1
            npts += int(deep.sum())
            for j in np.where(deep)[0]:
                oms.append(om[j]); tags.append((name, R[j], Vobs[j], gbar[j] / a0))
    return np.array(oms), tags, ngal, npts

base = {}
print(f"\n  {'footing':<8}{'a0':>12}{'gal':>6}{'deep pts':>10}{'MAX omega_gal':>16}{'set by':>34}")
print("  " + "-" * 92)
for lab, a0 in A0.items():
    oms, tags, ngal, npts = scan(a0)
    j = int(np.argmax(oms))
    base[lab] = dict(om=oms, tags=tags, om_max=oms[j], who=tags[j], ngal=ngal, npts=npts)
    nm, r, v, y = tags[j]
    print(f"  {lab:<8}{a0:>12.4e}{ngal:>6}{npts:>10}{oms[j]:>16.4e}"
          f"{f'{nm} r={r:.2f}kpc V={v:.1f} y={y:.2f}':>34}")
om_max = base["canon"]["om_max"]
print(f"""
  Both footings are bound by the SAME orbit, so MAX(omega_gal) -- and therefore the whole LOWER edge --
  is FOOTING-INDEPENDENT: it is set by galaxy kinematics, with no a0 anywhere in omega_gal = V/r.
  (a0 enters only the deep-MOND SELECTION cut, and the binding point clears both cuts.)
  MAX(omega_gal) = {om_max:.4e} rad/s   ->   LOWER EDGE = 3 x MAX = {3*om_max:.4e} rad/s
""")
check(f"regression: MAX(omega_gal) reproduces the committed 5.94e-15 within 1% (got {om_max:.4e})",
      abs(om_max / TGT["om_gal_max"] - 1) < 0.01)
check("lower edge is footing-independent (identical MAX on canon and alt)",
      abs(base["canon"]["om_max"] / base["alt"]["om_max"] - 1) < 1e-12)
lo_base = kS(GATE_KEEP) * om_max
check(f"regression: lower edge 3*MAX reproduces the committed 1.782e-14 within 1% (got {lo_base:.4e})",
      abs(lo_base / TGT["lo"] - 1) < 0.01)

# ---- how robust is MAX(omega_gal)? --------------------------------------------------------------------
print("  ROBUSTNESS OF MAX(omega_gal) -- selection variations (all at S = 0.90, canon cut).")
print("  width columns use the Sec.4 upper edges 2.211e-14 / 1.831e-14 (regression-confirmed there):")
print(f"  {'variation':<42}{'MAX omega_gal':>15}{'lower edge':>13}{'x base':>8}"
      f"{'W canon':>9}{'W alt':>8}{'binding gal':>13}")
print("  " + "-" * 104)
variations = [
    ("baseline (Q<=2, inc>=30, y<1, Ud=0.70)", dict()),
    ("M/L Ud=0.50 (Lelli+2016 fiducial)",      dict(ud=0.50, ub=0.70)),
    ("M/L Ud=1.00",                            dict(ud=1.00, ub=1.40)),
    ("quality Q<=1 only",                      dict(qmax=1)),
    ("inclination >= 45 deg",                  dict(incmin=45.0)),
    ("deeper cut y < 0.5",                     dict(ycut=0.5)),
    ("deeper cut y < 0.3",                     dict(ycut=0.3)),
    ("drop innermost 1 pt/galaxy (beam guard)", dict(drop_inner=1)),
    ("drop innermost 2 pts/galaxy",             dict(drop_inner=2)),
]
var_res = {}
for name, kw in variations:
    oms, tags, _, _ = scan(A0["canon"], **kw)
    j = int(np.argmax(oms))
    var_res[name] = oms[j]
    lo_v = 3 * oms[j]
    print(f"  {name:<42}{oms[j]:>15.4e}{lo_v:>13.4e}{oms[j]/om_max:>7.3f}x"
          f"{TGT['hi_canon']/lo_v:>8.3f}x{TGT['hi_alt']/lo_v:>7.3f}x{tags[j][0]:>13}")
beam = var_res["drop innermost 1 pt/galaxy (beam guard)"]
print(f"""
  The binding MAX is driven by ONE innermost, beam-scale point (UGC05721 at r = 0.09 kpc, one SPARC
  radial bin).  Dropping each galaxy's innermost radius moves MAX to {beam:.3e} ({beam/om_max:.2f}x) --
  a {100*(1-beam/om_max):.0f}% swing on the single most load-bearing input of the lower edge.  Both directions are
  defensible: beam smearing biases inner V_rot LOW (so the true omega_gal there could be HIGHER, pushing
  the lower edge UP and squeezing harder), while the same smearing makes the point unreliable at all.
  Reported both ways; the baseline (keep it) is the CONSERVATIVE-for-the-theory choice and is kept.

  Percentile view (baseline canon deep-MOND sample, N = {base['canon']['npts']}), i.e. what the lower edge
  becomes if the requirement is 'gate open at all but the fastest few' instead of literally every orbit:""")
oms_c = np.sort(base["canon"]["om"])
for p in (100.0, 99.9, 99.5, 99.0, 95.0):
    q = np.percentile(oms_c, p)
    print(f"      {p:>5.1f}th pct omega_gal = {q:.3e}  ->  lower edge {3*q:.3e}  ({3*q/lo_base:.3f}x baseline)")

# ======================================================================================================
# 3.  LOWER-EDGE SENSITIVITY TO THE RETENTION REQUIREMENT  (0.90 vs 0.95 vs 0.99)
# ======================================================================================================
head("3.  RETENTION SENSITIVITY -- what Re G >= 0.95 or 0.99 does to the lower edge")
print(f"""
  Re G >= S is a TOLERANCE CHOICE, not a measurement: it is how much galactic-RAR degradation at the
  worst orbit the framework is willing to eat.  S = 0.90 means the gate is allowed to remove 10% of the
  MI boost at UGC05721's innermost point.  The lower edge scales as k(S) = sqrt(S/(1-S)), which is STEEP
  near 1: k(0.90) = 3, k(0.95) = {kS(0.95):.3f}, k(0.99) = {kS(0.99):.3f}.
""")
print(f"  {'retention S':<14}{'k(S)':>9}{'lower edge':>14}{'vs canon upper 2.211e-14':>27}{'vs alt upper 1.831e-14':>25}")
print("  " + "-" * 92)
UP = {}   # filled properly in Sec. 4; provisional literals used only for this display
for s in (0.90, 0.95, 0.99):
    lo = kS(s) * om_max
    print(f"  {s:<14.2f}{kS(s):>9.4f}{lo:>14.4e}{TGT['hi_canon']/lo:>26.3f}x{TGT['hi_alt']/lo:>24.3f}x")
S_crit = {}
for lab, hi in (("canon", TGT["hi_canon"]), ("alt", TGT["hi_alt"])):
    kc = hi / om_max
    S_crit[lab] = S_of_k(kc)
print(f"""
  INVERSION -- the CRITICAL retention at which the window closes (lower edge == upper edge):
      canon:  k_crit = upper/MAX = {TGT['hi_canon']/om_max:.4f}  ->  S_crit = {S_crit['canon']:.4f}
      alt:    k_crit = upper/MAX = {TGT['hi_alt']/om_max:.4f}  ->  S_crit = {S_crit['alt']:.4f}

  So the canonical window exists only if the framework accepts >= {100*(1-S_crit['canon']):.1f}% MI-boost loss at the
  fastest confirmed deep-MOND orbit, and the alt window only if it accepts >= {100*(1-S_crit['alt']):.1f}%.  Demanding
  Re G >= 0.95 (a 5% RAR tolerance) closes BOTH footings; the alt footing closes at a retention demand
  of just {S_crit['alt']:.3f}, i.e. 0.5 percentage points above the adopted 0.90.
  With the beam guard (MAX -> {beam:.3e}) the critical retentions relax to
      canon S_crit = {S_of_k(TGT['hi_canon']/beam):.4f}   alt S_crit = {S_of_k(TGT['hi_alt']/beam):.4f}
  -> the retention lever and the beam-guard lever are comparable in size and pull OPPOSITE ways.
  HONEST READING: the 0.90 tolerance is defensible (10% at one orbit sits inside the framework's own
  0.108 dex = 28% SPARC RAR scatter) but it is a CHOICE, and the window's width is a function of it.
""")
check("Re G >= 0.95 closes both footings (k(0.95)*MAX exceeds both upper edges)",
      kS(0.95) * om_max > TGT["hi_canon"] and kS(0.95) * om_max > TGT["hi_alt"])
check("critical retentions are ordered and bracket the adopted 0.90 tightly (alt within 1 pp)",
      0.90 < S_crit["alt"] < S_crit["canon"] < 1.0 and S_crit["alt"] - 0.90 < 0.01)

# ======================================================================================================
# 4.  UPPER EDGE -- independent LLR rebuild, plus the "which body binds" ranking
# ======================================================================================================
head("4.  UPPER EDGE = (LLR Gdot/G 2-sigma ceiling) x g_N(Moon)/a0   [INDEPENDENT REBUILD]")
# the causal drift channel, re-derived (not quoted): Im G is forced once Re G is frequency-dependent.
wc_t, om_t = 3.3e-14, 2.6617e-6
ident = ReG(om_t, wc_t) ** 2 + ImG(om_t, wc_t) ** 2 - ReG(om_t, wc_t)
check("1-pole KK identity |G|^2 = Re G (the dissipative channel is causally forced, not inserted)",
      abs(ident) < 1e-15)
a0c = A0["canon"]
gN_moon = GM_EARTH / R_MOON ** 2
# Keplerian-consistent pair for the identity check (g_N = omega^2 r exactly), so the test probes the
# DRIFT ALGEBRA and not the ~1% mismatch between the Moon's sidereal omega and GM_E/r^2 at mean r.
om_kep = np.sqrt(GM_EARTH / R_MOON ** 3)
f_t = (a0c / 2) * abs(ImG(om_kep, wc_t))
drift_direct = 2 * f_t / (om_kep * R_MOON)
drift_asymp = a0c * wc_t / gN_moon
check(f"drift closed form d ln r/dt = a0 wc/g_N reproduces 2 f_t/(omega r) at the Moon "
      f"(ratio {drift_direct/drift_asymp:.6f})", abs(drift_direct / drift_asymp - 1) < 1e-3)
check(f"the Moon's sidereal omega vs Keplerian sqrt(GM/r^3) differ by <2% (so using g_N = GM/r^2 in the "
      f"upper edge, as the paper does, is a <2% choice: ratio {om_t/om_kep:.4f})",
      abs(om_t / om_kep - 1) < 0.02)

LLR_CEIL = abs(LLR_CEN) + 2 * LLR_SIG
print(f"""
  g_N(Moon) = GM_E/r^2 = {gN_moon:.6e} m/s^2
  LLR Gdot/G = ({LLR_CEN*1e15:+.1f} +- {LLR_SIG*1e15:.1f})e-15 /yr  [Biskupek, Mueller & Torre 2021,
    Universe 7:34 / arXiv:2012.12032 Table 1 -- VERIFIED against the arXiv PDF on 2026-07-25]
  [ADOPTED #2, the paper's convention]  one-sided ceiling on a secular EXPANSION = |cen| + 2 sigma
    = {LLR_CEIL:.3e} /yr.  This is defensible HERE because the measured central value leans in the
    expansion direction (Gdot/G < 0 <=> d ln a/dt = -Gdot/G > 0 for L^2 = GMa), i.e. the data mildly
    lean WITH the MI drift at {abs(LLR_CEN)/LLR_SIG:.2f} sigma.  Sec. 6 forks the convention.
  UPPER EDGE:  a0 omega_c/g_N <= ceiling  =>  omega_c <= (ceiling/yr) g_N(Moon)/a0
""")
def upper(a0, ceil=LLR_CEIL): return (ceil / YR) * gN_moon / a0
edges = {}
print(f"  {'footing':<8}{'a0 [task spelling]':>21}{'upper edge':>14}"
      f"{'a0 [window_joint]':>20}{'upper edge':>14}{'paper':>10}")
print("  " + "-" * 92)
for lab in ("canon", "alt"):
    e1, e2 = upper(A0[lab]), upper(A0_ALT_SPELL[lab])
    edges[lab] = e1
    print(f"  {lab:<8}{A0[lab]:>21.4e}{e1:>14.4e}{A0_ALT_SPELL[lab]:>20.4e}{e2:>14.4e}"
          f"{PAPER[lab][1]:>10.2e}")
check(f"regression: canon upper edge reproduces the committed 2.211e-14 within 1% (got {edges['canon']:.4e})",
      abs(edges["canon"] / TGT["hi_canon"] - 1) < 0.01)
check(f"regression: alt upper edge reproduces the committed 1.831e-14 within 1% (got {edges['alt']:.4e})",
      abs(edges["alt"] / TGT["hi_alt"] - 1) < 0.01)
check("upper edge is FOOTING-DEPENDENT and scales exactly as 1/a0",
      abs((edges["canon"] * A0["canon"]) / (edges["alt"] * A0["alt"]) - 1) < 1e-12)
check("a0 spelling jitter (9.355 vs 9.36; 1.1305 vs 1.13) shifts the upper edge by < 0.1%",
      all(abs(upper(A0[l]) / upper(A0_ALT_SPELL[l]) - 1) < 1e-3 for l in A0))

print("\n  WHICH BODY BINDS?  All solar-system ceilings on omega_c, canon footing:")
ceils = []
for nm, a, T in BODIES:                                  # reactive per-planet: wc <= omega_p sqrt(2 dg/a0)
    ceils.append((f"{nm} reactive delta_g [FM24]", (2*np.pi/(T*86400.0)) * np.sqrt(2*DG_BOUND[nm]/a0c)))
ceils.append(("Mercury Gdot/G [Genova+18]", (GDOT_MESSENGER/YR)*(GM_SUN/5.7909e10**2)/a0c))
ceils.append(("Mars ranging proxy [FM24]", ((MARS_RDOT_PROXY/2.27939e11)/YR)*(GM_SUN/2.27939e11**2)/a0c))
ceils.append(("Saturn ranging proxy [FM24]", ((SAT_RDOT_PROXY/1.43353e12)/YR)*(GM_SUN/1.43353e12**2)/a0c))
ceils.append(("Moon tidal budget [LLR]", ((LLR_TIDAL_2SIG/R_MOON)/YR)*gN_moon/a0c))
ceils.append(("Moon Gdot/G [BMT21] <-- BINDING", upper(a0c)))
for nm, v in sorted(ceils, key=lambda t: t[1]):
    print(f"      omega_c <= {v:.3e}   {nm}   ({v/upper(a0c):>8.1f}x the LLR edge)")
check("LLR Gdot/G is the BINDING (smallest) solar-system ceiling on omega_c",
      min(v for _, v in ceils) == upper(a0c))

# ======================================================================================================
# 5.  THE WIDTHS  -- W-1 headline
# ======================================================================================================
head("5.  W-1 HEADLINE -- the window widths, both footings")
W = {lab: edges[lab] / lo_base for lab in edges}
print(f"\n  {'footing':<8}{'lower (SPARC, theory-internal)':>32}{'upper (LLR, data)':>20}{'WIDTH':>10}{'paper':>9}{'room':>10}")
print("  " + "-" * 92)
for lab in ("canon", "alt"):
    print(f"  {lab:<8}{lo_base:>32.4e}{edges[lab]:>20.4e}{W[lab]:>10.4f}{TGT['w_'+lab]:>9.3f}"
          f"{100*(W[lab]-1):>+9.1f}%")
check(f"regression: canon width reproduces 1.241 within 1% (got {W['canon']:.4f})",
      abs(W["canon"] / TGT["w_canon"] - 1) < 0.01)
check(f"regression: alt width reproduces 1.027 within 1% (got {W['alt']:.4f})",
      abs(W["alt"] / TGT["w_alt"] - 1) < 0.01)
print(f"""
  CONFIRMED, independently: canon x{W['canon']:.3f} (+{100*(W['canon']-1):.1f}%), alt x{W['alt']:.3f} (+{100*(W['alt']-1):.1f}%).
  The alt footing's window IS only ~{100*(W['alt']-1):.1f}% wide, and this is established from SPARC rotation curves
  plus LLR Gdot/G ALONE -- no a0-line slope estimator anywhere in it.  So it is a genuinely INDEPENDENT
  line of pressure on the footing question.
  BUT IT IS NOT AN EXCLUSION, and the reason is quantitative, not rhetorical: the +{100*(W['alt']-1):.1f}% margin is far
  SMALLER than the swing from the choices that set the edges --
      retention S 0.90 -> 0.95           : lower edge x{kS(0.95)/kS(0.90):.2f}  (closes both footings)
      beam guard (drop innermost point)  : lower edge x{beam/om_max:.2f}  (opens alt to x{edges['alt']/(3*beam):.2f})
      LLR 2-sigma convention fork (Sec.6): upper edge x{(2*LLR_SIG)/LLR_CEIL:.2f} to x{(abs(LLR_CEN)+3*LLR_SIG)/LLR_CEIL:.2f}
  The margin sits INSIDE the systematic noise floor of its own construction.  Correct verdict: the alt
  footing is at the closure threshold, neither excluded nor safe.  What would close it decisively:
  (i) a confirmed deep-MOND orbit with omega_gal > {edges['alt']/3:.3e} rad/s (only {100*(edges['alt']/3/om_max-1):.1f}% above today's max),
  or (ii) an LLR Gdot/G ceiling below {LLR_CEIL/W['alt']:.3e}/yr (Sec. 7), or (iii) a resolved verdict on the
  beam-scale innermost SPARC point that keeps it.  None of the three is in hand.
""")

# ======================================================================================================
# 6.  CONVENTION FORK ON THE LLR CEILING -- the width is convention-limited, not data-limited
# ======================================================================================================
head("6.  CONVENTION FORK -- how much of the width is the 2-sigma convention, not the measurement?")
conv = [("|cen| + 2 sigma  [the paper's, ADOPTED]", abs(LLR_CEN) + 2*LLR_SIG),
        ("2 sigma only (central-agnostic)",         2*LLR_SIG),
        ("|cen| + 3 sigma (conservative)",          abs(LLR_CEN) + 3*LLR_SIG),
        ("|cen| + 1 sigma (aggressive)",            abs(LLR_CEN) + LLR_SIG)]
print(f"\n  {'ceiling convention':<40}{'ceiling [/yr]':>16}{'canon upper':>14}{'width':>9}"
      f"{'alt upper':>13}{'width':>9}")
print("  " + "-" * 102)
for nm, ce in conv:
    uc, ua = upper(A0["canon"], ce), upper(A0["alt"], ce)
    print(f"  {nm:<40}{ce:>16.3e}{uc:>14.3e}{uc/lo_base:>9.3f}{ua:>13.3e}{ua/lo_base:>9.3f}")
w2s_c, w2s_a = upper(A0['canon'], 2*LLR_SIG)/lo_base, upper(A0['alt'], 2*LLR_SIG)/lo_base
print(f"""
  READ THIS STRAIGHT, BOTH WAYS.  Under the paper's own convention both footings are open.  Under an
  equally standard central-agnostic 2-sigma reading (ceiling = 2 sigma = {2*LLR_SIG:.2e}/yr) the canonical
  window is EMPTY by {100*(1-w2s_c):.1f}% (x{w2s_c:.3f}) and the alt window EMPTY by {100*(1-w2s_a):.1f}% (x{w2s_a:.3f}).
  Under |cen| + 3 sigma both are comfortably open.  The width therefore spans x{min(upper(A0['alt'],c)/lo_base for _,c in conv):.2f} to
  x{max(upper(A0['canon'],c)/lo_base for _,c in conv):.2f} across defensible conventions -- a range LARGER than either quoted width.
  Neither reading is forced by the data, and NEITHER is adopted as the verdict here.  What this does
  establish: the window's non-emptiness currently rides on the LLR central value's {abs(LLR_CEN)/LLR_SIG:.2f} sigma lean in
  the MI direction.  And that lean is not a stable feature -- the immediately preceding analysis
  (Hofmann & Mueller 2018) had Gdot/G = (+7.1 +- 7.6)e-14/yr, i.e. the OPPOSITE sign.  The sign of the
  central value has already flipped once between consecutive LLR analyses.
""")
check("the convention fork spans a wider factor than the canonical quoted width (width is "
      "convention-limited, not measurement-limited)",
      (max(upper(A0['canon'], c) for _, c in conv) / min(upper(A0['canon'], c) for _, c in conv)) > W["canon"])

# ======================================================================================================
# 7.  W-2 CLOSURE FORECAST
# ======================================================================================================
head("7.  W-2 CLOSURE FORECAST -- the factor F in Gdot/G that closes each footing, and roughly when")
# Identity: upper edge is LINEAR in the ceiling, so the closure factor IS the width.
Csym, Ls, gs, as_, ks_, oms_ = sp.symbols("C L g a k Omega", positive=True)
u_sym = (Csym / Ls) * gs / as_                        # upper edge
lo_sym = ks_ * oms_                                   # lower edge
F_sym = sp.simplify(sp.solve(sp.Eq(u_sym / sp.Symbol("F", positive=True), lo_sym),
                             sp.Symbol("F", positive=True))[0] / (u_sym / lo_sym))
print(f"""
  Closure condition:  upper(ceiling/F) < lower  <=>  F > upper/lower  ==  the WINDOW WIDTH.
  sympy: F_required / (upper/lower) = {F_sym}  (must be 1) -- the closure factor IS the width, exactly,
  because the upper edge is strictly LINEAR in the Gdot/G ceiling and the lower edge does not move.
  This is the quantitative form of the ASYMMETRY: the lower edge is theory-internal and non-negotiable
  (relaxing it means gating off the rotation curves the framework exists to explain), so every
  improvement in Gdot/G closes the window FROM ABOVE and nothing pushes back.
""")
check("closure factor F equals the window width identically (symbolic)", sp.simplify(F_sym - 1) == 0)
print(f"  {'footing':<8}{'F (whole-ceiling)':>19}{'required ceiling [/yr]':>25}"
      f"{'F on sigma, cen held':>22}{'required sigma':>16}")
print("  " + "-" * 92)
FORE = {}
for lab in ("canon", "alt"):
    F = W[lab]
    ceil_req = LLR_CEIL / F
    sig_req = (ceil_req - abs(LLR_CEN)) / 2.0
    F_sig = LLR_SIG / sig_req
    FORE[lab] = dict(F=F, ceil_req=ceil_req, sig_req=sig_req, F_sig=F_sig)
    print(f"  {lab:<8}{F:>19.4f}{ceil_req:>25.4e}{F_sig:>22.4f}{sig_req:>16.4e}")
print(f"""
  STATED AS ASKED:
      a factor {FORE['canon']['F']:.3f} tighter LLR Gdot/G ceiling KILLS the CANONICAL footing's window.
      a factor {FORE['alt']['F']:.3f} tighter LLR Gdot/G ceiling KILLS the ALT footing's window.
      (equivalently, holding the central value at -5.0e-15: sigma tighter by x{FORE['canon']['F_sig']:.3f} / x{FORE['alt']['F_sig']:.3f})
      A single factor {FORE['canon']['F']:.3f} closes BOTH footings simultaneously.
  For comparison, the paper's own falsifier (iv) says "a x3 ephemeris/LLR secular refit closes or detects
  the window."  The rebuild says x3 is a {3/FORE['canon']['F']:.1f}x OVERSTATEMENT of what is needed: x{FORE['canon']['F']:.2f} suffices.
  And if the central value regresses to zero as a null should, the ceiling falls to 2 sigma with NO
  precision gain at all -- which already closes both footings (Sec. 6).
""")
# a SECOND, independent closure lever: the runner-up ceiling is much closer than the paper implies
sat_ceil = {l: ((SAT_RDOT_PROXY / 1.43353e12) / YR) * (GM_SUN / 1.43353e12 ** 2) / A0[l] for l in A0}
print(f"""  A SECOND, INDEPENDENT LEVER (flagged, not developed here -- it is W-3's remit).  The runner-up
  ceiling in Sec. 4 is NOT far behind LLR: the Saturn ranging proxy (Cassini ~2.3 m/yr, Fienga &
  Minazzoli 2024) gives omega_c <= {sat_ceil['canon']:.3e} (canon) / {sat_ceil['alt']:.3e} (alt) -- only x{sat_ceil['canon']/edges['canon']:.2f} / x{sat_ceil['alt']/edges['alt']:.2f}
  looser than the LLR edge.  Closing the window from that channel alone needs x{sat_ceil['canon']/lo_base:.2f} (canon) /
  x{sat_ceil['alt']/lo_base:.2f} (alt).  So there are TWO independent channels within a factor ~2 of closure, not one,
  and a metre-level INPOP/DE440-class secular refit is the obvious place the real bound already sits.
  Whether a modern ephemeris ceiling already lies BELOW the LLR edge is exactly the W-3 question; this
  script does not answer it and its widths would have to be recomputed if it does.
""")
check("the runner-up (Saturn ranging) ceiling is within a factor 2 of the LLR edge -- two independent "
      "channels are near closure, not one",
      sat_ceil["canon"] / edges["canon"] < 2.0)

# ---- historical rate --------------------------------------------------------------------------------
HIST = [(2004.0, 9.0e-13,  "Williams, Turyshev & Boggs 2004 PRL 93:261101   Gdot/G = (+4 +- 9)e-13/yr"),
        (2010.0, 3.8e-13,  "Hofmann, Mueller & Biskupek 2010 A&A 522:L5    (-0.7 +- 3.8)e-13/yr"),
        (2018.0, 7.6e-14,  "Hofmann & Mueller 2018 CQG 35:035015           (+7.1 +- 7.6)e-14/yr  [VERIFIED]"),
        (2021.0, 9.6e-15,  "Biskupek, Mueller & Torre 2021 Universe 7:34   (-5.0 +- 9.6)e-15/yr  [VERIFIED]")]
print("  HISTORICAL IMPROVEMENT RATE of the LLR Gdot/G uncertainty (published anchors):")
for y, s_, src in HIST:
    print(f"      {y:.0f}  sigma = {s_:.2e} /yr   {src}")
print(f"\n  {'interval':<14}{'years':>7}{'sigma factor':>14}{'-> per decade':>15}")
print("  " + "-" * 52)
rates = []
for (y1, s1, _), (y2, s2, _) in zip(HIST[:-1], HIST[1:]):
    dy = y2 - y1
    f = s1 / s2
    per_dec = f ** (10.0 / dy)
    rates.append(per_dec)
    print(f"  {int(y1)}-{int(y2):<9}{dy:>7.0f}{f:>14.2f}{per_dec:>14.1f}x")
overall = (HIST[0][1] / HIST[-1][1]) ** (10.0 / (HIST[-1][0] - HIST[0][0]))
slowest = min(rates)
print(f"  {'2004-2021 all':<14}{HIST[-1][0]-HIST[0][0]:>7.0f}{HIST[0][1]/HIST[-1][1]:>14.2f}{overall:>14.1f}x  <- overall")
print(f"""
  [ASSUMPTION, flagged]  These gains are DISCRETE (infrared normal points, remodelled lunar interior,
  longer arcs), not a smooth accumulation, so extrapolating the decadal rate is a rough guide only.  The
  conservative floor is the formal statistical law: a Gdot/G signature enters the range quadratically in
  time, so for uniform sampling at fixed per-point noise sigma ~ T^(-5/2).  BMT21 used T = {LLR_T0_YR:.0f} yr
  (April 1970 - April 2020, 27 485 NP).  BASELINE GROWTH ALONE therefore gives:
""")
def epoch_for(factor):
    """years of total baseline needed for sigma to shrink by `factor` under T^-5/2, and the epoch."""
    T = LLR_T0_YR * factor ** 0.4
    return T, LLR_T0_EPOCH - LLR_T0_YR + T
print(f"  {'target':<34}{'F needed':>10}{'baseline T [yr]':>18}{'epoch (T^-5/2 floor)':>23}"
      f"{'epoch (hist. rate)':>21}")
print("  " + "-" * 106)
for lab in ("canon", "alt"):
    for tag, Fv in (("whole ceiling scales", FORE[lab]["F"]), ("sigma only, cen held", FORE[lab]["F_sig"])):
        T, ep = epoch_for(Fv)
        ep_hist = 2021.0 + np.log(Fv) / np.log(overall) * 10.0
        print(f"  {lab+': '+tag:<34}{Fv:>10.3f}{T:>18.2f}{ep:>23.1f}{ep_hist:>21.1f}")
T_c, ep_c = epoch_for(FORE["canon"]["F_sig"])
T_a, ep_a = epoch_for(FORE["alt"]["F_sig"])
print(f"""
  FORECAST, stated plainly (today = 2026.6):
    * ALT footing: needs x{FORE['alt']['F_sig']:.3f} on sigma -- i.e. essentially NOTHING.  Baseline growth alone
      passed that threshold around {ep_a:.0f}.  On the published record the alt window is already at or past
      its closure point; it stands only on the |cen|+2sigma convention and the beam-scale SPARC point.
    * CANONICAL footing: needs x{FORE['canon']['F_sig']:.3f} on sigma (or x{FORE['canon']['F']:.3f} on the whole ceiling).  Under the
      T^(-5/2) floor that arrives at total baseline T = {T_c:.1f} yr, epoch ~{ep_c:.0f}; at the historical
      2004-2021 rate ({overall:.0f}x/decade) it arrives ~{2021.0 + np.log(FORE['canon']['F_sig'])/np.log(overall)*10.0:.0f}.  Both are IN THE PAST OR NOW.
    * CONCLUSION: the required improvement is smaller than the analysis-to-analysis scatter of LLR
      Gdot/G itself.  The window is not "closing in a decade" -- it is AT the closure threshold now, and
      the next published LLR Gdot/G analysis is a live two-sided test.  Honest symmetry: a next analysis
      with an INFLATED sigma or a LARGER |central| REOPENS the window just as easily.  That is what a
      free constant sandwiched between two independent measurements looks like -- precarious, not dead.
""")
check("the closure factor for BOTH footings is under x1.5 (i.e. inside one analysis-to-analysis step)",
      FORE["canon"]["F"] < 1.5 and FORE["alt"]["F"] < 1.5)
check("the alt footing's required improvement is under 5% (already inside the historical noise)",
      FORE["alt"]["F"] < 1.05)

# ======================================================================================================
# 8.  VERDICT
# ======================================================================================================
head("8.  VERDICT  (W-1 + W-2)")
print(f"""
  W-1  EDGES, REBUILT INDEPENDENTLY -- both confirmed, no correction needed:
        LOWER  = k(0.90) x MAX(omega_gal) = 3 x {om_max:.4e} = {lo_base:.4e} rad/s
                 FOOTING-INDEPENDENT (galaxy kinematics only; a0 enters just the deep-MOND cut).
                 THEORY-INTERNAL and NOT NEGOTIABLE: relaxing it gates off the rotation curves.
        UPPER  = (|cen|+2sig LLR ceiling / yr) x g_N(Moon)/a0
                 = {edges['canon']:.4e} (canon) / {edges['alt']:.4e} (alt) rad/s.  FOOTING-DEPENDENT, exactly 1/a0.
        WIDTHS = x{W['canon']:.4f} (canon, +{100*(W['canon']-1):.1f}%)  and  x{W['alt']:.4f} (alt, +{100*(W['alt']-1):.1f}%).
                 Paper's x1.24 / x1.027 CONFIRMED to <1%.
        RETENTION SENSITIVITY: lower edge scales as sqrt(S/(1-S)).  S=0.95 -> {kS(0.95)*om_max:.3e} and
                 S=0.99 -> {kS(0.99)*om_max:.3e}: BOTH footings CLOSE at S=0.95.  Critical retentions
                 S_crit = {S_crit['canon']:.4f} (canon) / {S_crit['alt']:.4f} (alt).  The alt window needs the tolerance
                 to be no stricter than {S_crit['alt']:.3f} -- 0.5 percentage points of slack.

  IS THE ALT FOOTING NEARLY EXCLUDED BY SPARC + LLR ALONE, INDEPENDENTLY OF THE a0-LINE ESTIMATOR?
        The pressure is REAL and INDEPENDENT: no slope estimator, no RAR fit, no M/L inference enters
        the width -- SPARC orbital frequencies and LLR ranging alone give +{100*(W['alt']-1):.1f}%.  As a second,
        methodologically disjoint line on the footing question it is worth having.
        It is NOT an exclusion.  Room remaining, precisely: the alt window closes if MAX(omega_gal)
        exceeds {edges['alt']/3:.3e} rad/s (+{100*(edges['alt']/3/om_max-1):.1f}% over today's binding orbit), OR if the LLR ceiling
        falls below {FORE['alt']['ceil_req']:.3e}/yr (x{FORE['alt']['F']:.3f}), OR if the retention demand rises above {S_crit['alt']:.3f}.
        Against that, the beam guard on the single binding innermost SPARC point reopens alt to
        x{edges['alt']/(3*beam):.2f}, and the |cen|+3sigma convention reopens it to x{upper(A0['alt'], abs(LLR_CEN)+3*LLR_SIG)/lo_base:.2f}.  The +{100*(W['alt']-1):.1f}% margin is
        SMALLER than every one of those levers.  Verdict: AT THE THRESHOLD, NOT EXCLUDED.

  W-2  CLOSURE FACTORS (exact identity: F_required == the window width):
        a factor {FORE['canon']['F']:.3f} tighter LLR Gdot/G ceiling KILLS the CANONICAL footing.
        a factor {FORE['alt']['F']:.3f} tighter LLR Gdot/G ceiling KILLS the ALT footing.
        Required ceilings: {FORE['canon']['ceil_req']:.3e}/yr (canon), {FORE['alt']['ceil_req']:.3e}/yr (alt), vs today's {LLR_CEIL:.3e}/yr.
        On sigma with the central held: x{FORE['canon']['F_sig']:.3f} / x{FORE['alt']['F_sig']:.3f}.
        EPOCH: the T^(-5/2) baseline floor reaches x{FORE['canon']['F_sig']:.2f} at total baseline {T_c:.0f} yr, epoch ~{ep_c:.0f};
        the historical 2004-2021 rate ({overall:.0f}x/decade, slowest sub-interval {slowest:.1f}x/decade) reaches it
        ~{2021.0 + np.log(FORE['canon']['F_sig'])/np.log(overall)*10.0:.0f}.  Both epochs are ALREADY HERE.  The alt threshold was passed ~{ep_a:.0f}.

  NOT COMFORTABLE, AND SAID SO: a x1.24 window on a free fifth constant, pinned between two independent
  measurements, with all improvement pressure acting from above and a required closure factor of only
  x1.24, is a precarious position.  The width is also convention-limited: the same LLR datum read at
  2 sigma (central-agnostic) rather than |cen|+2 sigma gives EMPTY on both footings; read at |cen|+3 sigma
  it gives x{upper(A0['canon'], abs(LLR_CEN)+3*LLR_SIG)/lo_base:.2f} / x{upper(A0['alt'], abs(LLR_CEN)+3*LLR_SIG)/lo_base:.2f}.  No reading is adopted as the verdict; the spread IS the result.

  SCOPE: this script rebuilds two edges and forecasts one closure.  It says nothing about whether the
  gate's frequency prescription (omega = orbital angular frequency, [ADOPTED #1]) is right -- that fork
  is the load-bearing open question and lives in reviews/mi_cassini_q2_omegac_2026.py Sec. 6.  Nothing
  here is a claim about the framework beyond these numbers.  No door is declared closed.
""")
print(RULE)
print(f"mi_omegac_edges_closure_2026.py: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print(RULE)
sys.exit(0 if PASS else 1)
