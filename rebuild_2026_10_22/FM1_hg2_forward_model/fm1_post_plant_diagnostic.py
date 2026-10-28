#!/usr/bin/env python3
"""FM1_hg2_forward_model: HG2's D for the base picture, forward-modelled through HG2's own binning on (model) sigma.
Frozen criteria 9c9d980ba0 (committed alone). Machinery: GA1's committed script (133f61510d) executed read-only up to its graded runs.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I fm1_hg2_forward_model.py      (FM1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np

MUT = False
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
GA1 = os.path.join(REB, "GA1_group_gas_audit", "ga1_group_gas_audit.py")
src = open(GA1).read(); src = src[:src.index('RES = dict(criteria="5afacf2b5c"')]
os.environ.pop("GA1_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "ga1_ro_post.py"), "__name__": "ga1_ro"}
exec(compile(src, GA1, "exec"), NS)
P, hg1, hg2, ref, FEET, SEED, audit = (NS[k] for k in ("P", "hg1", "hg2", "ref", "FEET", "SEED", "audit"))
HO = NS["NS"]; MPC = hg1.MPC
P("\n================ FM1 POST-RESULT DIAGNOSTIC (not graded): can the forward-modelled statistic see a planted BRIGHT excess?")
checks = {}
NREAL = 2000

rows, emg, _, _ = audit("ac")
HO["rows"] = rows; HO["EMG"] = emg
dm = hg2.deltas(rows, ref); Dm = hg1.D_stat(rows, dm)[0]
rng0 = np.random.default_rng(SEED); hg1.power(rows, dm, rng0); lo, hi, _ = hg2.bootstrap(rows, ref, rng0)
gbar = np.array([r["gbar"] for r in rows]); lref = ref.logref(gbar)
gobs = np.array([r["gobs"] for r in rows]); rr = np.array([r["r_mpc"] * MPC for r in rows])
sup = np.isfinite(dm); faint = np.array([r["flag"] == "FAINT" for r in rows])
checks["K0"] = abs(Dm - (-0.36229)) < 5e-5
RES = dict(criteria="9c9d980ba0", machinery="GA1 133f61510d (read-only)", mutate=MUT, D_meas=Dm, ci95=[lo, hi], footings={})
P(f"  measured D {Dm:+.4f} [{lo:+.4f}, {hi:+.4f}] (GA1 PRIMARY): K0 {'PASS' if checks['K0'] else 'FAIL'}")

def D_with_sigma(sig, dl):
    rs = [dict(r, sigma=float(s)) for r, s in zip(rows, sig)]
    return hg1.D_stat(rs, dl)[0]


bright = np.array([r["flag"] == "BRIGHT" for r in rows])
POST = {}
for f in FEET:
    gp = HO["group_pred"](f)[0]; lgp = np.log10(gp); res = np.log10(gobs) - lgp
    s_all = 1.4826 * float(np.median(np.abs(res[sup] - np.median(res[sup]))))
    for plant in (0.0, 0.2, 0.4, -0.2):
        rng = np.random.default_rng(20261028); Ds = []
        for k in range(2000):
            lgm = lgp + plant * bright + rng.normal(0.0, s_all, len(rows))
            sig = np.sqrt(10 ** lgm * rr / 3) / 1e3
            Ds.append(D_with_sigma(sig, lgm - lref))
        Ds = np.array(Ds); Ds = Ds[np.isfinite(Ds)]
        q = float(np.mean(Ds <= Dm))
        POST[f"{f}_plant{plant:+.1f}"] = dict(median=float(np.median(Ds)), p2_5=float(np.percentile(Ds, 2.5)), p97_5=float(np.percentile(Ds, 97.5)), q=q)
        P(f"  [{f}] planted BRIGHT excess {plant:+.1f} dex: D_mod median {np.median(Ds):+.4f} [95%: {np.percentile(Ds, 2.5):+.4f}, {np.percentile(Ds, 97.5):+.4f}]; q {q:.3f} -> {'consistent with D_meas' if 0.025 <= q <= 0.975 else 'EXCLUDED by D_meas'}")
json.dump(POST, open(os.path.join(HERE, "fm1_post_plant_diagnostic.json"), "w"), indent=1)
open(os.path.join(HERE, "fm1_post_plant_diagnostic.out"), "w").write("\n".join(HO["OUT"][-12:]).replace(REPO, "<repo>") + "\n")
