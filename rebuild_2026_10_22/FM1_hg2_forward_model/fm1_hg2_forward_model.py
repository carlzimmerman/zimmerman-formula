#!/usr/bin/env python3
"""FM1_hg2_forward_model: HG2's D for the base picture, forward-modelled through HG2's own binning on (model) sigma.
Frozen criteria 9c9d980ba0 (committed alone). Machinery: GA1's committed script (133f61510d) executed read-only up to its graded runs.

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, not a particle; not theory closed;
nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I fm1_hg2_forward_model.py      (FM1_MUTATE=1 twin)
"""
import os, sys, json, math, hashlib, resource
import numpy as np

MUT = os.environ.get("FM1_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
GA1 = os.path.join(REB, "GA1_group_gas_audit", "ga1_group_gas_audit.py")
src = open(GA1).read(); src = src[:src.index('RES = dict(criteria="5afacf2b5c"')]
os.environ.pop("GA1_MUTATE", None)
NS = {"__file__": os.path.join(HERE, "ga1_ro.py"), "__name__": "ga1_ro"}
exec(compile(src, GA1, "exec"), NS)
P, hg1, hg2, ref, FEET, SEED, audit = (NS[k] for k in ("P", "hg1", "hg2", "ref", "FEET", "SEED", "audit"))
HO = NS["NS"]; MPC = hg1.MPC
P("\n================ FM1_hg2_forward_model (criteria 9c9d980ba0)" + ("  [MUTATE: s_int forced to 0]" if MUT else ""))
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

k1 = True; k2 = True
for f in FEET:
    gp = HO["group_pred"](f)[0]; lgp = np.log10(gp)
    res = np.log10(gobs) - lgp
    s_all = 1.4826 * float(np.median(np.abs(res[sup] - np.median(res[sup]))))
    s_fnt = 1.4826 * float(np.median(np.abs(res[sup & faint] - np.median(res[sup & faint]))))
    if MUT: s_all = s_fnt = 0.0
    k2 &= s_all > 0 and s_fnt > 0
    # K1: s = 0, binning on observed sigma -> HO1(b)'s D_pred
    D_k1 = hg1.D_stat(rows, lgp - lref)[0]; ref_k1 = {"canonical": 0.30590, "alt": 0.28210}[f]
    k1 &= abs(D_k1 - ref_k1) < 5e-5
    # noise-free, re-binned on model sigma
    sig0 = np.sqrt(gp * rr / 3) / 1e3
    D0 = D_with_sigma(sig0, lgp - lref)
    out = dict(s_int=s_all, s_faint=s_fnt, D_pred_observed_binning=D_k1, D_noise_free_model_binning=D0, variants={})
    P(f"\n=== [{f}] s_int (all) {s_all:.3f} dex, (FAINT) {s_fnt:.3f} dex; K1 D_pred observed-binning {D_k1:+.4f} (HO1/GA1 {ref_k1:+.4f}); noise-free model-binned D {D0:+.4f}")
    for lab, s in (("PRIMARY s_int", s_all), ("V FAINT-only s", s_fnt), ("V 0.5 s_int", 0.5 * s_all), ("V 1.5 s_int", 1.5 * s_all)):
        rng = np.random.default_rng(20261028); Ds = np.empty(NREAL)
        for k in range(NREAL):
            lgm = lgp + rng.normal(0.0, s, len(rows)) if s > 0 else lgp.copy()
            sig = np.sqrt(10 ** lgm * rr / 3) / 1e3
            Ds[k] = D_with_sigma(sig, lgm - lref)
        Ds = Ds[np.isfinite(Ds)]
        q = float(np.mean(Ds <= Dm)); med = float(np.median(Ds)); lo95, hi95 = float(np.percentile(Ds, 2.5)), float(np.percentile(Ds, 97.5))
        cls = "CONDITIONING EXPLAINS THE SIGN" if 0.025 <= q <= 0.975 else ("CONDITIONING PARTLY EXPLAINS" if med < 0 else "CONDITIONING DOES NOT EXPLAIN")
        out["variants"][lab] = dict(s=s, q=q, median=med, p2_5=lo95, p97_5=hi95, n=len(Ds), cls=cls)
        P(f"  {lab:16s} s {s:.3f}: D_mod median {med:+.4f} [95%: {lo95:+.4f}, {hi95:+.4f}]; q(D_mod <= D_meas) {q:.3f} -> {cls}")
    out["verdict"] = out["variants"]["PRIMARY s_int"]["cls"]
    RES["footings"][f] = out
checks["K1"] = bool(k1); checks["K2"] = bool(k2)
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; checks["K3"] = peak < 1.0
RES["checks"] = checks
P(f"\n  K1 {'PASS' if k1 else 'FAIL'}; K2 s_int > 0 {'PASS' if k2 else 'FAIL'}; K3 peak RSS {peak:.2f} GB")
P(f"=== VERDICT: canonical {RES['footings']['canonical']['verdict']}; alt {RES['footings']['alt']['verdict']}")
fn = os.path.join(HERE, f"fm1_hg2_forward_model_results{TAG}.json")
json.dump(RES, open(fn, "w"), indent=1, default=float)
P(f"checks {sum(checks.values())}/{len(checks)}; results sha256 {hashlib.sha256(open(fn, 'rb').read()).hexdigest()}")
open(os.path.join(HERE, f"fm1_hg2_forward_model{TAG}.out"), "w").write("\n".join(HO["OUT"]).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(checks.values()) else 1)
