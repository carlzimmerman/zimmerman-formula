#!/usr/bin/env python3
"""CFG666: do the 'dark' strong-lens perturbers need mass with no baryons? (criteria b9b9009ad)

For each published perturber solution, the baryonic mass the law needs (R-iso: cold mass settled while isolated, M_obs =
M_b nu_mono(g_N/a0); R-EFE: Newtonian, M_b = M_obs) and the stellar light that implies (Upsilon_max = 8), against the
published 3-sigma light limit. J0946 luminous solution: forward prediction of M(<1 kpc) from its measured light.
Inputs are the papers' published numbers (read from paper text 2026-10-12), listed in FROZEN_CRITERIA.md. No halo model.
kappa = 1/2 FITTED; cold energy mass required; not theory closed.
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUT = os.environ.get("CFG666_MUTATE", "0") == "1"
MODE = os.environ.get("CFG666_M", "") if MUT else ""
TAG = f"_MUTATE{MODE}" if MUT else ""
G, MSUN, KPC = C4.G_SI, C4.MSUN, C4.KPC
A0 = dict(C4.A0)
if MODE == "M1":
    A0 = {f: 1e-30 for f in A0}                      # pure Newton
UPS_MAX = 1e4 if MODE == "M2" else 8.0
OUT, RES = [], {"lane": "CFG666", "criteria": "b9b9009ad", "mutate": MUT, "mode": MODE, "Upsilon_max": UPS_MAX}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def nu(y):
    return float(C4.nu_mono(np.asarray([y], float))[0])


def mb_iso(M_obs, r, a0):
    """baryonic mass M_b (Msun) with M_b * nu(G M_b / (r^2 a0)) = M_obs"""
    f = lambda lm: math.log(10 ** lm * nu(G * 10 ** lm * MSUN / (r * r * a0))) - math.log(M_obs)
    return 10 ** brentq(f, math.log10(M_obs) - 12, math.log10(M_obs) + 1, xtol=1e-12)


def m_law(Mb, r, a0):
    return Mb * nu(G * Mb * MSUN / (r * r * a0))


# published inputs (FROZEN_CRITERIA.md section 0)
INV = [  # name, M_obs (Msun), r (kpc), 3-sigma light limit (Lsun) or None
    ("J0946 dark (Vegetti+2010) M3D<0.3kpc", 5.8e8, 0.3, 5.0e6),
    ("J0946 dark (Vegetti+2010) M3D<0.6kpc", 1.1e9, 0.6, 5.0e6),
    ("B1938 A (Vegetti+2012) M3D<0.6kpc", 1.13e8, 0.6, 5.4e7),
    ("B1938 V (Powell+2025) m80 projected", 1.13e6, 0.08, None),
]
P("CFG666 — strong-lens perturbers vs the law" + (f"   [MUTATE {MODE}]" if MUT else ""))
P(f"Upsilon_max = {UPS_MAX}; kernel nu_mono; footings {A0}")
for f in ("canonical", "alt"):
    a0 = A0[f]; RES[f] = {}
    P(f"\n== footing {f} (a0 = {a0:.4e}) ==")
    for name, M, rk, Llim in INV:
        r = rk * KPC
        gobs = G * M * MSUN / r ** 2
        Mi, Me = mb_iso(M, r, a0), M
        Li, Le = Mi / UPS_MAX, Me / UPS_MAX
        if Llim is None or min(Li, Le) <= Llim:
            cls = "NOT DIAGNOSTIC"
        elif min(Li, Le) > 10 * Llim:
            cls = "EXCLUDED"
        else:
            cls = "TENSION (1-10x the light limit)"
        RES[f][name] = dict(M_obs=M, r_kpc=rk, gobs_over_a0=gobs / a0, Mb_iso=Mi, Mb_efe=Me, L_req_iso=Li, L_req_efe=Le,
                            L_limit=Llim, ratio_iso=(Li / Llim if Llim else None), cls=cls)
        P(f"  {name}: g_obs/a0 = {gobs/a0:.2f}; M_b,req iso {Mi:.3e} / EFE {Me:.3e} Msun; L_req >= {min(Li,Le):.2e} Lsun"
          + (f" vs limit {Llim:.1e} (x{min(Li,Le)/Llim:.1f})" if Llim else " (no limit)") + f"  -> {cls}")
    # J0946 luminous solution: forward prediction
    h = 0.75 / 1.678                                   # exponential scale length from R_half
    x = 1.0 / h
    fin = 1 - (1 + x) * math.exp(-x)
    lo_b = 10 ** 8.2 * 1.0 * fin; hi_b = 10 ** 8.5 * 4.0 * fin
    pred_lo = lo_b                                      # R-EFE, lowest baryons
    pred_hi = m_law(hi_b, KPC, a0)                      # R-iso, highest baryons
    meas = (10 ** 8.1, 10 ** 10.0)
    overlap = pred_hi >= meas[0] and pred_lo <= meas[1]
    cls_lum = "CONSISTENT" if overlap else "EXCLUDED"
    med_iso = m_law(10 ** 8.4 * 2.0 * fin, KPC, a0)
    RES[f]["J0946 luminous (2506.07978)"] = dict(f_in=fin, Mb_range=[lo_b, hi_b], pred_band=[pred_lo, pred_hi],
                                                  pred_median_iso=med_iso, measured_95=list(meas), cls=cls_lum)
    P(f"  J0946 luminous: f_in(<1 kpc) = {fin:.3f}; M_b(<1 kpc) {lo_b:.2e}..{hi_b:.2e}; predicted M(<1 kpc) band "
      f"{math.log10(pred_lo):.2f}..{math.log10(pred_hi):.2f} dex (median iso, Upsilon 2: {math.log10(med_iso):.2f}) vs measured "
      f"8.1..10.0 (median 8.9)  -> {cls_lum}")
    dark = RES[f]["J0946 dark (Vegetti+2010) M3D<0.3kpc"]["cls"]
    RES[f]["label"] = ("NOT DIAGNOSTIC (model-selection-limited)" if dark == "EXCLUDED" and cls_lum == "CONSISTENT"
                       else f"dark: {dark}; luminous: {cls_lum}")
    P(f"  LABEL ({f}): {RES[f]['label']}")

code = 0
if MUT:
    if MODE == "M1":
        bite = all(abs(RES[f][n]["Mb_iso"] / RES[f][n]["Mb_efe"] - 1) < 1e-6 for f in ("canonical", "alt") for n, *_ in INV)
    else:
        bite = all(RES[f]["J0946 dark (Vegetti+2010) M3D<0.3kpc"]["cls"] == "NOT DIAGNOSTIC" for f in ("canonical", "alt"))
    P(f"\nMUTATE {MODE}: tooth {'BITES' if bite else 'DOES NOT BITE'}"); RES["bite"] = bite; code = 1 if bite else 0
with open(os.path.join(HERE, f"cfg666_results{TAG}.json"), "w") as fh:
    json.dump(RES, fh, indent=1)
with open(os.path.join(HERE, f"cfg666{TAG}.out"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(code)
