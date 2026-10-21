"""CFG957 POST HOC (dated 2026-10-21, written after the MAIN run; reported only, NO class weight).

The owner's idea (2026-10-21): a0(z) oscillates like a wave.  MAIN's r_max uses CFG689's band (z <= 2.33) and -p positivity
only.  At m >= 10 H0 those r_max values put early-dark-energy-like energy at z 3-16 that shifts D_M(z*) by 0.8-1.9% (MAIN (d)).
CFG689's theta* rows are not citable (K9 failed as frozen), so no class rests on theta*.  This file brackets how much that
caveat could matter:
  PH1  the curvature change that would absorb each D_M(z*) shift at fixed chi (CFG689's primary has curvature free);
  PH2  a "theta*-tight" bracket: the largest r_i with |dD_M/D_M| <= 3 x 0.029% (no refit of h or omega_k), and the
       high-z predictions and the frozen testability rule at min(r_theta, r_max(reading)).
kappa = 1/2 FITTED; footings never pooled; not theory closed.

Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg957_posthoc.py   (about a minute; < 0.5 GB)
"""
import json
import math
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

import cfg957 as C

OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


MAIN = json.load(open(os.path.join(HERE, "cfg957.json")))["results"]
TH_TOL = 3 * 0.00030 / 1.04109


def chi_star(o):
    N = o["N"]
    f = np.exp(-N) / np.sqrt(o["H2"])
    chi = C.TRAPZ(f, N)
    V0, r_i = o["V0"], o["r_i"]
    chi += quad(lambda x: 1 / (x * x * math.sqrt(C.OM * x**-3 + C.OMR * x**-4 + C.WK * x**-2 + V0 * (1 + r_i))),
                1 / (1 + C.ZSTAR), C.AI, epsabs=0, epsrel=1e-12)[0]
    return chi


def DM(chi, wk):
    return math.sinh(math.sqrt(wk) * chi) / math.sqrt(wk) if wk > 0 else chi


P("CFG957 POST HOC (2026-10-21; reported only, no class weight). The owner's idea (2026-10-21).")
ob0 = C.model(10.0, 0.0, ngrid=50001)
chi0 = chi_star(ob0)
D0 = DM(chi0, C.WK)
P(f"comparison background: chi(z*) = {chi0:.5f} c/H100, D_M = {D0:.5f} c/H100 ({D0 * 2997.92458:.1f} Mpc)")
P("")
P("PH1  curvature that absorbs the D_M(z*) shift at fixed chi (MAIN's r_max(eps) curves)")
PH1 = {}
OK_half_primary = 0.5 * (C.J689["BAO+SN"]["P0"]["Omega_k_q"][3] - C.J689["BAO+SN"]["P0"]["Omega_k_q"][1])
for mH0 in C.XMASS:
    r_i = MAIN["M1_X"][str(mH0)]["rmax"]["r_max"]["eps"]
    o = C.model(mH0, r_i, ngrid=50001)
    chi = chi_star(o)
    wk_new = brentq(lambda w: DM(chi, w) - D0, 1e-8, 0.5)
    dwk = wk_new - C.WK
    PH1[str(mH0)] = dict(r_i=r_i, dDM=DM(chi, C.WK) / D0 - 1, d_omega_k=dwk, d_Omega_k=dwk / C.H2_0)
    P(f"  m {mH0:4.0f} H0 r_i {r_i:.4g}: dD_M/D_M {DM(chi, C.WK) / D0 - 1:+.3e}; absorbed by d omega_k {dwk:+.5f} (d Omega_k {dwk / C.H2_0:+.4f}) "
      f"vs CFG689 primary Omega_k 68% half-width {OK_half_primary:.3f}; CFG689 T mode (theta*) [0.000, 0.003]")
P("  => with curvature free (CFG689 primary), theta* alone cannot exclude these shifts; a joint theta* + BAO + SN fit")
P("     (CFG689's T modes, blocked by K9) would be needed, and would likely cut r_max where |d Omega_k| >> 0.0015.")
P("")
P("PH2  theta*-tight bracket (no refit): largest r_i with |dD_M/D_M| <= 3 x 0.029%; predictions at min(r_theta, r_max(reading))")
PH2 = {}
for mH0 in C.XMASS:
    def f(lr):
        o = C.model(mH0, 10**lr, ngrid=20001)
        return abs(DM(chi_star(o), C.WK) / D0 - 1) - TH_TOL
    lo, hi = -6.0, math.log10(MAIN["M1_X"][str(mH0)]["rmax"]["r_band"])
    if f(hi) <= 0:
        rth = 10**hi
    elif f(lo) > 0:
        rth = 0.0
    else:
        rth = 10 ** brentq(f, lo, hi, xtol=1e-6)
    row = dict(r_theta=rth, readings={})
    for rd in C.READ:
        r_i = min(rth, MAIN["M1_X"][str(mH0)]["rmax"]["r_max"][rd])
        ob = C.model(mH0, r_i, ngrid=50001)
        rr = C.ratio(ob, rd)
        pred = {str(z): float(np.log10(C.interp_z(ob, rr, z))) for z in C.ZPRED}
        nh = sum(abs(pred[str(z)]) >= 0.15 for z in C.WHIGH)
        o100 = C.model(mH0, r_i, a_end=100.0, ngrid=60001)
        ext5 = C.count_ext(o100, rd, C.lnz_N(5), 0)
        row["readings"][rd] = dict(r_i=r_i, pred_log10=pred, n_high_ge015=nh, testable_high=nh >= 2, extrema_z5=ext5)
        P(f"  m {mH0:4.0f} H0 {rd:3s} r_i {r_i:.4g}: log10 a0(z)/a0(0) z 2.5..5: " +
          " ".join(f"{pred[str(z)]:+.3f}" for z in C.WHIGH) + f" | >= 0.15 dex at {nh} -> {'TESTABLE' if nh >= 2 else 'untestable'}; extrema z<=5 {ext5}")
    PH2[str(mH0)] = row
P("")
P("Reported only. The frozen classes rest on MAIN; PH2 shows how much a working native theta* could change them.")
P("kappa = 1/2 FITTED; footings never pooled; not theory closed; the owner's idea (2026-10-21).")
open(os.path.join(HERE, "cfg957_posthoc.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(label="POST HOC 2026-10-21, reported only, no class weight", chi0=chi0, D_M0=D0, PH1=PH1, PH2=PH2,
               note="the owner's idea (2026-10-21); kappa = 1/2 FITTED"),
          open(os.path.join(HERE, "cfg957_posthoc.json"), "w"), indent=1)
