#!/usr/bin/env python3
"""CFG668: sealed magnitude prediction for JWST GO 8281 (B1938+666 perturbers A, V). Criteria a0b9c9bf7.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, io, json, math, hashlib, contextlib
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUT = os.environ.get("CFG668_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC = C4.G_SI, C4.MSUN, C4.KPC
A0 = {f: (1e-30 if MUT else v) for f, v in C4.A0.items()}
nu = lambda y: float(C4.nu_mono(np.asarray([y], float))[0])
Z, DM = 0.881, 43.8212
KS = 2.5 * math.log10(1 + Z)
BANDS = {"F115W": {"Msun": 4.65, "ups": (0.5, 5.0)}, "F277W": {"Msun": 4.71, "ups": (0.3, 1.5)}}
PERT = {"A": (1.13e8, 0.6), "V": (1.13e6, 0.08)}
DEPTH_NOTE = "GO 8281 depth not measured here; point-source 5 sigma for 88 ks NIRCam is roughly 31 AB (ETC-scale estimate, context)"

def mb_iso(M, Rk, a0):
    R = Rk * KPC
    f = lambda lm: math.log(10 ** lm * nu(G * 10 ** lm * MSUN / (R * R * a0))) - math.log(M)
    return 10 ** brentq(f, math.log10(M) - 12, math.log10(M) + 1, xtol=1e-12)

def mag(Mstar, ups, Msun):
    return Msun - 2.5 * math.log10(Mstar / ups) + DM - KS

out = {"lane": "CFG668", "criteria": "a0b9c9bf7", "target": "JWST GO 8281, B1938+666", "z": Z, "DM": DM, "a0": A0,
       "mutate": MUT, "depth_note": DEPTH_NOTE, "pred": {}}
L = []
for foot, a0 in A0.items():
    out["pred"][foot] = {}; L.append(f"== {foot} (a0 = {a0:.4e}) ==")
    for p, (M, Rk) in PERT.items():
        mbmin = mb_iso(M, Rk, a0); mbmax = M
        msmin, msmax = 0.8 * mbmin, mbmax
        d = {"M_lens": M, "R_kpc": Rk, "R_arcsec": Rk / 7.9623, "M_b_range": [mbmin, mbmax], "M_star_range": [msmin, msmax]}
        for b, s in BANDS.items():
            bright = mag(msmax, s["ups"][0], s["Msun"]); faint = mag(msmin, s["ups"][1], s["Msun"])
            d[b] = {"bright_AB": round(bright, 2), "faint_AB": round(faint, 2), "exclude_if_2sigma_limit_fainter_than": round(faint + 1.19, 2)}
            L.append(f"  {p} ({M:.2e} in {Rk} kpc = {Rk/7.9623:.3f}\"): M_* {msmin:.2e}-{msmax:.2e}; {b} predicted "
                     f"{bright:.2f}..{faint:.2f} AB; EXCLUDED if 2sig limit fainter than {faint+1.19:.2f}")
        out["pred"][foot][p] = d
L.append(DEPTH_NOTE)
js = json.dumps(out, indent=1, sort_keys=True) + "\n"
open(os.path.join(HERE, f"cfg668_predictions{TAG}.json"), "w").write(js)
L.append(f"sha256(cfg668_predictions{TAG}.json) = {hashlib.sha256(js.encode()).hexdigest()}")
open(os.path.join(HERE, f"cfg668{TAG}.out"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
if MUT:
    bite = all(abs(out["pred"][f][p]["M_b_range"][0] / out["pred"][f][p]["M_lens"] - 1) < 1e-6 for f in out["pred"] for p in PERT)
    print("MUTATE a0->0:", "BITES" if bite else "DOES NOT BITE"); sys.exit(1 if bite else 0)
