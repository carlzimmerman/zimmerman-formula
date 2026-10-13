#!/usr/bin/env python3
"""CFG667: sealed prediction for JWST GO 12088 (J0946+1006 lens perturber). Criteria 44bf95584.
Q_max(M_lens, R) = M_lens / M_b,iso where M_b,iso * nu_mono(G M_b,iso / (R^2 a0)) = M_lens; the law brackets
Q = M_lens/M_b in [1, Q_max]. kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, io, json, math, hashlib, contextlib
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUT = os.environ.get("CFG667_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC = C4.G_SI, C4.MSUN, C4.KPC
A0 = {f: (1e-30 if MUT else v) for f, v in C4.A0.items()}
nu = lambda y: float(C4.nu_mono(np.asarray([y], float))[0])

def qmax(M, Rk, a0):
    R = Rk * KPC
    f = lambda lm: math.log(10 ** lm * nu(G * 10 ** lm * MSUN / (R * R * a0))) - math.log(M)
    mb = 10 ** brentq(f, math.log10(M) - 12, math.log10(M) + 1, xtol=1e-12)
    return M / mb, mb

MG = [10 ** x for x in np.round(np.arange(7.0, 10.01, 0.25), 2)]
RG = [0.1, 0.2, 0.3, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0]
PTS = [("Vegetti+2010 dark, M3D<0.3kpc", 5.8e8, 0.3), ("Vegetti+2010 dark, M3D<0.6kpc", 1.1e9, 0.6),
       ("2506.07978 luminous, Mproj<1kpc median", 10 ** 8.9, 1.0), ("2506.07978 luminous, 95% low", 10 ** 8.1, 1.0),
       ("2506.07978 luminous, 95% high", 10 ** 10.0, 1.0)]
out = {"lane": "CFG667", "criteria": "44bf95584", "target": "JWST GO 12088, SDSS J0946+1006 lens perturber",
       "statement": "M_lens/nu_mono <= M_b(<R) <= M_lens; Q = M_lens/M_b in [1, Q_max]; SURVIVES Q_obs <= 1.25 Q_max; "
                    "EXCLUDED Q_obs > 3 Q_max at >= 2 sigma", "a0": A0, "mutate": MUT, "grid": {}, "points": {}}
lines = []
for foot, a0 in A0.items():
    out["grid"][foot] = {f"{R}": {f"{math.log10(M):.2f}": round(qmax(M, R, a0)[0], 4) for M in MG} for R in RG}
    out["points"][foot] = {}
    lines.append(f"== {foot} (a0 = {a0:.4e}) ==")
    for name, M, R in PTS:
        q, mb = qmax(M, R, a0)
        out["points"][foot][name] = {"M_lens": M, "R_kpc": R, "Q_max": round(q, 4), "M_b_min": mb, "M_b_max": M,
                                     "kill_if_Q_obs_above": round(3 * q, 3), "survive_if_Q_obs_below": round(1.25 * q, 3)}
        lines.append(f"  {name}: M_lens {M:.2e} at {R} kpc -> M_b in [{mb:.2e}, {M:.2e}]; Q_max {q:.3f}; "
                     f"SURVIVES Q_obs <= {1.25*q:.2f}; EXCLUDED Q_obs > {3*q:.2f}")
js = json.dumps(out, indent=1, sort_keys=True)
with open(os.path.join(HERE, f"cfg667_predictions{TAG}.json"), "w") as fh: fh.write(js + "\n")
h = hashlib.sha256((js + "\n").encode()).hexdigest()
lines.append(f"sha256(cfg667_predictions{TAG}.json) = {h}")
with open(os.path.join(HERE, f"cfg667{TAG}.out"), "w") as fh: fh.write("\n".join(lines) + "\n")
print("\n".join(lines))
if MUT:
    bite = all(abs(v - 1) < 1e-6 for f in out["grid"].values() for r in f.values() for v in r.values())
    print("MUTATE a0->0:", "BITES (Q_max = 1 everywhere)" if bite else "DOES NOT BITE"); sys.exit(1 if bite else 0)
