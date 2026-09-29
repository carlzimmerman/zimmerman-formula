#!/usr/bin/env python3
"""CFG185 -- the high-g tails of nu_mono and P2 against the Solar System, reconciled with GATES 4.01.

Frozen criteria: FROZEN_CRITERIA.md in this directory (572c4aefc).
  Q1  nu_mono's phantom h(y) = y (nu - 1) rebuilt from FP1's definition with my own code (the RAR phantom y/(e^sqrt(y) - 1),
      its derivative floored at 0.05 H_P/(y + Y_P), integrated by the trapezoid rule on the same log grid) vs CFG4_common's;
      the tail derived from the floor: for y >= Y_P, h(y) = h(Y_P) + 0.05 H_P ln((y + Y_P)/(2 Y_P)).
  Q2  a_anom = h a0 at Earth / Mars (the Sun's g_N) vs the record's verified delta A_R bounds 3.66e-14 / 3.72e-14 m/s^2.
  Q3  the monopole ratios vs GATES 4.01's Q2 tide (a different quantity); which applies to candidate B.
  Q4  a committed grep of the record for 'Solar-System safe' statements about nu_mono or P2.
MUTATE=1 removes the floor (the pure RAR kernel): the tail must then decay.
Run: python3 campaign_fresh_gravity/CFG185_kernel_tail/cfg185_kernel_tail.py
"""
import os, sys, re, math, glob
import numpy as np
import sympy as sp
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "1")
R = C.Report("cfg185_kernel_tail", MODE == "1")
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())

G, MSUN, A0 = K.G_SI, K.MSUN, K.A0
AU = 1.495978707e11
RSUN = 6.957e8
BOUND = {"Earth": 3.66e-14, "Mars": 3.72e-14}                     # STANDING.md (Sereno & Jetzer 2006 via EPM2004), 2 sigma


# ------------------------------------------------------------------ my own rebuild of nu_mono (written from FP1's definition)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)


YP = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0)
HP = float(h_rar(YP))
LG = np.linspace(-14, 14, 280001)
YG = 10 ** LG
floor = 0.0 if MODE == "1" else 1.0                                 # MUTATE=1: no floor (the pure RAR kernel)
DH = np.maximum(dh_rar(YG), floor * 0.05 * HP / (YG + YP)) if floor else dh_rar(YG)
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])


def h_mine(y):
    return np.interp(np.log10(np.maximum(np.asarray(y, float), 1e-14)), LG, HM)


def h_of(nu, y):
    y = np.asarray(y, float)
    return y * (nu(y) - 1.0)


# ================================================================== controls
R.banner("CONTROLS")
yy = np.logspace(-6, 14, 2001)
# (fixed after the first run, kept as *_firstrun*: that run compared y (nu - 1) from CFG4's nu_mono, which loses ~1% to float
#  cancellation at y ~ 1e14 where nu - 1 ~ 1e-14, and so failed on precision, not on the kernel.  CFG4's own h table is compared here.)
_KNS = K._KNS
h_cfg4 = lambda y: np.interp(np.log10(np.maximum(np.asarray(y, float), 1e-14)), _KNS["LYG"], _KNS["_HM"])
d1 = float(np.max(np.abs(h_mine(yy) - h_cfg4(yy))))
dnu = float(np.max(np.abs((1.0 + h_mine(yy) / yy) - K.nu_mono(yy))))
check("C1 CONTROL: my rebuild of nu_mono's phantom equals CFG4_common's nu_mono to 1e-6 over y in [1e-6, 1e14]"
      + ("  [MUTATE: floor removed, must FAIL]" if MODE else ""), f"max |h_mine - h_CFG4 table| = {d1:.2e}; as nu: max |nu_mine - nu_mono| = {dnu:.2e}",
      d1 < 1e-6)
ys = sp.symbols("y", positive=True)
hp2 = ys * (sp.sqrt(1 + 1 / ys) - 1)
# (fixed after the first run: that run expanded to O(1/y^2) and compared with the O(1/y) form, so it failed on its own truncation)
ser = sp.series(hp2.subs(ys, 1 / sp.Symbol("e", positive=True)), sp.Symbol("e", positive=True), 0, 2).removeO()
ser = sp.simplify(ser.subs(sp.Symbol("e", positive=True), 1 / ys))
check("C2 CONTROL: P2's phantom y (sqrt(1 + 1/y) - 1) -> 1/2 - 1/(8 y) at large y (sympy)", f"series: {ser}",
      sp.simplify(ser - (sp.Rational(1, 2) - 1 / (8 * ys))) == 0)
yh = np.logspace(math.log10(YP) + 0.01, 3, 200)
check("C3 CONTROL: the RAR kernel's phantom y/(e^sqrt(y) - 1) decreases for y > Y_P", f"Y_P = {YP:.4f}, H_P = {HP:.4f}; "
      f"h_rar(10) = {float(h_rar(10)):.4f}, h_rar(100) = {float(h_rar(100)):.2e}", bool(np.all(np.diff(h_rar(yh)) < 0)))

# ================================================================== Q1: the tail
R.banner("Q1  THE TAIL: h(y) = y (nu - 1) for y >= Y_P (anomalous acceleration in units of a0)")
ytail = np.logspace(math.log10(YP), 14, 4001)
hmin = float(np.min(h_mine(ytail)))
hYP = float(h_mine(YP))
ana = hYP + 0.05 * HP * np.log((ytail + YP) / (2 * YP))
dev = float(np.max(np.abs(h_mine(ytail) - ana)))
check("Q1a non-decaying: h(y) >= H_P - 1e-3 for every y in [Y_P, 1e14]" + ("  [MUTATE: must FAIL]" if MODE else ""),
      f"min h = {hmin:.4f} (H_P = {HP:.4f}); h(Y_P) = {hYP:.4f}", hmin >= HP - 1e-3)
check("Q1b (reported) the analytic tail h(Y_P) + 0.05 H_P ln((y + Y_P)/(2 Y_P)) matches the table for y >= Y_P",
      f"max |table - analytic| = {dev:.2e}", True, load_bearing=False)
bodies = [("Sun (photosphere)", RSUN), ("Mercury", 0.387 * AU), ("Venus", 0.723 * AU), ("Earth", 1.0 * AU), ("Mars", 1.524 * AU),
          ("Jupiter", 5.203 * AU), ("Saturn", 9.537 * AU), ("Uranus", 19.19 * AU), ("Neptune", 30.07 * AU)]
tab = {}
for f in K.FOOTS:
    for name, r in bodies:
        y = G * MSUN / r ** 2 / A0[f]
        row = dict(y=y, h_mono=float(h_mine(y)), h_mono_cfg4=float(h_of(K.nu_mono, y)), h_p2=float(h_of(K.nu_p2, y)),
                   h_rar=float(h_rar(y)))
        tab[(f, name)] = row
for f in K.FOOTS:
    P(f"  footing {f} (a0 = {A0[f]:.4e} m/s^2):")
    for name, _ in bodies:
        t = tab[(f, name)]
        P(f"    {name:18s} y = {t['y']:.3e}:  nu_mono h = {t['h_mono']:.4f} (a_anom {t['h_mono'] * A0[f]:.3e} m/s^2);  "
          f"P2 h = {t['h_p2']:.4f};  RAR h = {t['h_rar']:.2e}")
yclamp = float(h_mine(1e14))
P(f"  the table's clamp: h(1e14) = {yclamp:.4f} (nu_mono is constant in h beyond y = 1e14: the interpolation clamps)")
hE = tab[("canonical", "Earth")]["h_mono"]
check("Q1c '1.18 a0 at Earth' (canonical): h(Earth) within 0.02 of 1.18" + ("  [MUTATE: must FAIL]" if MODE else ""),
      f"h(Earth) = {hE:.4f}", abs(hE - 1.18) <= 0.02)

# ================================================================== Q2: against the planetary bounds
R.banner("Q2  a_anom = h a0 vs the verified delta A_R bounds (Earth 3.66e-14, Mars 3.72e-14 m/s^2, 2 sigma)")
rat = {}
for ker in ("h_mono", "h_p2"):
    for f in K.FOOTS:
        for b in ("Earth", "Mars"):
            rat[(ker, f, b)] = tab[(f, b)][ker] * A0[f] / BOUND[b]
    vals = [rat[(ker, f, b)] for f in K.FOOTS for b in ("Earth", "Mars")]
    P(f"  {ker:7s}: " + ";  ".join(f"{f} {b} {rat[(ker, f, b)]:.0f}x" for f in K.FOOTS for b in ("Earth", "Mars"))
      + f"   (range {min(vals):.0f}-{max(vals):.0f}x)")
m_rng = (min(rat[("h_mono", f, b)] for f in K.FOOTS for b in BOUND), max(rat[("h_mono", f, b)] for f in K.FOOTS for b in BOUND))
p_rng = (min(rat[("h_p2", f, b)] for f in K.FOOTS for b in BOUND), max(rat[("h_p2", f, b)] for f in K.FOOTS for b in BOUND))
check("Q2a (reported) nu_mono's ratio range vs the relayed 2.9-3.6e3 (confirmed if within 5% of that range)",
      f"{m_rng[0]:.0f}-{m_rng[1]:.0f}x", True, load_bearing=False)
check("Q2b (reported) P2's ratio range vs the relayed 1257-1540 (confirmed if within 5% of that range)",
      f"{p_rng[0]:.0f}-{p_rng[1]:.0f}x", True, load_bearing=False)
R.num("Q2", {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in rat.items()})
R.num("tab", {f"{k[0]}|{k[1]}": v for k, v in tab.items()})

# ================================================================== Q3: reconciliation (stated; the Q2 tide is cited, not recomputed)
R.banner("Q3  RECONCILIATION")
P("  - The ratios above are the MONOPOLE: a constant (P2) or slowly growing (nu_mono) SUNWARD anomalous acceleration h a0, carried")
P("    by the Sun in the strict (bare) law, against the planetary radial-acceleration bound delta A_R (ranging).")
P("  - GATES 4.01's '4.0-5.7x the ceiling' is Q2: the TIDAL quadrupole (s^-2) of the Solar-System field in the Galaxy's external")
P("    field, against the ephemeris bound Q2 <= 5.2e-27 s^-2. A different observable of the same strict law; both hold together.")
P("  - Candidate B passes 4.01 by OWNERSHIP (the phantom belongs to the host; the Sun carries none): the host-phantom tide is")
P("    1.6-2.6e-31 s^-2 (GATES 4.01). Under ownership the Sun carries no monopole either, so neither bare-law number applies to B.")
P("  - So: as a BARE law, neither kernel is Solar-System safe; nu_mono's tail is non-decaying and larger than P2's a0/2.")

# ================================================================== Q4: the record's statements
R.banner("Q4  GREP: 'Solar-System safe' statements about nu_mono or P2 in the record (*.md)")
pat = re.compile(r"(nu_mono|ν_mono|\bP2\b).{0,120}(Solar[- ]System[- ]safe|Cassini[- ]safe|ephemeris[- ]safe|safe in the Solar)", re.I)
hits = []
# scope (declared after a repo-wide glob over ~35k .md files did not finish; no Q4 output had been seen): the record's documents --
# root *.md, campaign_fresh_gravity/*.md, its closure_map/*.md and lane READMEs, real_research/*.md and real_research/reviews/*.md
SCOPE = (glob.glob(os.path.join(REPO, "*.md")) + glob.glob(os.path.join(CFG, "*.md")) + glob.glob(os.path.join(CFG, "closure_map", "*.md"))
         + glob.glob(os.path.join(CFG, "*", "README.md")) + glob.glob(os.path.join(REPO, "real_research", "*.md"))
         + glob.glob(os.path.join(REPO, "real_research", "reviews", "*.md")))
P(f"  scope: {len(SCOPE)} files (the record's documents; see the comment in the script)")
for path in sorted(set(SCOPE)):
    if "ai_slop" in path or "node_modules" in path:
        continue
    try:
        for i, line in enumerate(open(path, encoding="utf-8", errors="ignore"), 1):
            if pat.search(line):
                hits.append((os.path.relpath(path, REPO), i, line.strip()[:160]))
    except OSError:
        pass
for p_, i, l in hits[:40]:
    P(f"    {p_}:{i}: {l}")
P(f"  {len(hits)} line(s) found" + (" (first 40 shown)" if len(hits) > 40 else ""))
R.num("Q4_hits", [f"{p_}:{i}" for p_, i, _ in hits])
nf = R.write(LANE)
raise SystemExit(1 if nf else 0)
