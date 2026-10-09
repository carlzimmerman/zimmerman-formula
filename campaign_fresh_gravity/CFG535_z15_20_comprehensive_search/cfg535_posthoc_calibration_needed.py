#!/usr/bin/env python3
"""CFG535 POST HOC (not frozen; written after cfg535_forecast.out was seen): how tight must the shared calibrations be before F1/F2 become CRISP?
Same machinery as cfg535_forecast.py; only the nuisance priors change.  Labelled sensitivity, never a pass line.  kappa = 1/2 FITTED."""
import os, sys, json
os.environ.setdefault("OMP_NUM_THREADS", "2")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
import importlib.util, io, contextlib
spec = importlib.util.spec_from_file_location("F", os.path.join(HERE, "cfg535_forecast.py"))
F = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    # importing re-runs the frozen forecast (seconds) and rewrites its JSON identically (same seeds)
    spec.loader.exec_module(F)

SCEN = {
    "S0_frozen_priors":            dict(sM=0.15, smu=0.25, fR=(1.0, 2.0), ssig=8.0, P="mix"),
    "S1_pressure_known_PK":        dict(sM=0.15, smu=0.25, fR=(1.0, 2.0), ssig=3.0, P="K"),
    "S2_PK_gas0.10_Mstar0.10":     dict(sM=0.10, smu=0.10, fR=(1.0, 2.0), ssig=3.0, P="K"),
    "S3_PK_gas0.10_extent_known":  dict(sM=0.10, smu=0.10, fR=(1.4, 1.6), ssig=3.0, P="K"),
    "S4_PB_gas0.10_extent_known":  dict(sM=0.10, smu=0.10, fR=(1.4, 1.6), ssig=3.0, P="B"),
    "S5_PK_all0.05_extent_known":  dict(sM=0.05, smu=0.05, fR=(1.4, 1.6), ssig=3.0, P="K"),
}


def draw(rng, n, p):
    PK = rng.random(n) < 0.5 if p["P"] == "mix" else np.full(n, p["P"] == "K")
    return dict(dM=rng.normal(0, p["sM"], n), dmu=rng.normal(0, p["smu"], n), fR=rng.uniform(*p["fR"], n),
                sig=45 + rng.normal(0, p["ssig"], n), PK=PK)


out = {}
for sn, p in SCEN.items():
    for fn in ("canonical", "alt"):
        a0, nu = F.FOOT[fn], F.KERN["nu_mono"]
        rng = np.random.default_rng([535, 99, list(SCEN).index(sn), list(F.FOOT).index(fn)])
        thc = draw(rng, F.NN, p)
        cl = {L: F.predict(thc, a0, nu, L) for L in ("FLAT", "H(z)")}
        thm = draw(rng, F.NM, p)
        zz = {}
        for name, idx in (("A_only", [0]), ("S_only", [1]), ("joint", [0, 1])):
            zt = []
            for truth, wrong in (("FLAT", "H(z)"), ("H(z)", "FLAT")):
                pm = F.predict(thm, a0, nu, truth)
                X = np.stack([pm["A"] + rng.normal(0, F.SIG_A, F.NM), pm["S"] + rng.normal(0, 0.05, F.NM)], 1)[:, idx]
                c2 = {}
                for L in (truth, wrong):
                    Y = np.stack([cl[L]["A"], cl[L]["S"]], 1)[:, idx]
                    cov = np.atleast_2d(np.cov(Y.T)) + np.diag([[F.SIG_A ** 2, 0.05 ** 2][i] for i in idx])
                    c2[L] = F.chi2(X, Y.mean(0), cov)
                md = float(np.median(c2[wrong] - c2[truth]))
                zt.append(float(np.sign(md) * np.sqrt(abs(md))))
            zz[name] = min(zt)
        out[f"{sn}|{fn}"] = {"Z_eff_min_over_truths": zz,
                             "S_flat": float(cl["FLAT"]["S"].mean()), "S_rival": float(cl["H(z)"]["S"].mean()),
                             "S_sd": float(max(cl["FLAT"]["S"].std(), cl["H(z)"]["S"].std()))}
        print(f"{sn:28s} {fn:9s} S flat {out[f'{sn}|{fn}']['S_flat']:+.3f} rival {out[f'{sn}|{fn}']['S_rival']:+.3f} sd {out[f'{sn}|{fn}']['S_sd']:.3f} | "
              + "  ".join(f"{k} {v:+.2f}" for k, v in zz.items()))
json.dump(out, open(os.path.join(HERE, "cfg535_posthoc_calibration_needed_results.json"), "w"), indent=1)
