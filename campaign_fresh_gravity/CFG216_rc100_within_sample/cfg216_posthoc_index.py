#!/usr/bin/env python3
"""CFG216 POST HOC (written after the frozen run's numbers were seen; reported only, never a verdict): the a0(z) power-law index that RC100's
decompositions prefer.  a0(z) = A0_canonical x 10^c x (1 + z)^p.  Solve for (c, p) so that the median delta = 0 and the Theil-Sen slope of delta on z = 0,
with a galaxy bootstrap (2,000 resamples, seed 216) for the intervals.  Flat is p = 0 (c = 0); the rival a0 ~ E(z) is p ~ 1.3-1.4 over z 0.6-2.5.
Uses nu_mono, canonical footing (the alt footing is reported in the summary line).  The same data, quantities and exclusions as cfg216_rc100.py.
Run: python3 campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_posthoc_index.py
"""
import os, sys, csv, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import fsolve, brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG4_common as K

G2SI = 1e6 / 3.0856775814913673e19
OM = 0.315
NB, SEED = 2000, 216
out = []


def P(s=""):
    print(s); out.append(s)


CORR = os.environ.get("RC100_INPUT", "").strip() == "corrected"      # input-correction switch, as in cfg216_rc100.py
RC100_PATH = (os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv") if CORR
              else os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))
raw = list(csv.DictReader(open(RC100_PATH, newline="")))
z, D, gb = [], [], []
for r in raw:
    zz, Re, Vc, fd = (float(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re"))
    if 0 < fd < 1:
        z.append(zz); D.append(1 / (1 - fd)); gb.append((1 - fd) * Vc ** 2 / Re * G2SI)
z, D, gb = map(np.array, (z, D, gb))
E = lambda zz: np.sqrt(OM * (1 + zz) ** 3 + 1 - OM)


def delta(zv, Dv, gv, a0, c, p):
    return np.log10(Dv / K.nu_mono(gv / (a0 * 10 ** c * (1 + zv) ** p)))


def ts(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m]))


def solve(zv, Dv, gv, a0, x0=(0.0, 0.0)):
    f = lambda v: [np.median(delta(zv, Dv, gv, a0, v[0], v[1])), ts(zv, delta(zv, Dv, gv, a0, v[0], v[1]))]
    sol, info, ier, msg = fsolve(f, x0, full_output=True, xtol=1e-10)
    return sol if ier == 1 else np.array([np.nan, np.nan])


rng = np.random.default_rng(SEED)
P(__doc__.split("Run:")[0].strip())
P(f"\n  n = {len(z)}; z {z.min():.2f}-{z.max():.2f}")
rival_p = np.polyfit(np.log(1 + z), np.log(E(z)), 1)[0]
P(f"  the rival a0 ~ E(z) corresponds to p = {rival_p:.2f} over this sample's z (log-log slope of E against 1 + z)")
for foot, a0 in (("canonical", K.A0["canonical"]), ("alt", K.A0["alt"])):
    c, p = solve(z, D, gb, a0)
    bs = []
    for _ in range(NB):
        ix = rng.integers(0, len(z), len(z))
        s = solve(z[ix], D[ix], gb[ix], a0, x0=(c, p))
        if np.all(np.isfinite(s)):
            bs.append(s)
    bs = np.array(bs)
    plo, phi = np.percentile(bs[:, 1], [2.5, 97.5]); clo, chi = np.percentile(bs[:, 0], [2.5, 97.5])
    ps = np.std(bs[:, 1])
    P(f"  {foot:9s}: p = {p:+.2f} [{plo:+.2f}, {phi:+.2f}] (sigma {ps:.2f}; {len(bs)} of {NB} resamples solved);  c = {c:+.3f} [{clo:+.3f}, {chi:+.3f}] dex "
      f"(a0(z=0) x {10 ** c:.2f});  flat (p = 0) is {abs(p) / ps:.1f} sigma away, the rival (p = {rival_p:.2f}) {abs(p - rival_p) / ps:.1f} sigma away")
open(os.path.join(LANE, "cfg216_posthoc_index" + ("_corrected" if CORR else "") + ".out"), "w").write("\n".join(out) + "\n")
