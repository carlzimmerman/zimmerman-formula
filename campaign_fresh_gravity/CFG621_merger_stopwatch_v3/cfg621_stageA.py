#!/usr/bin/env python3
"""CFG621 stage A (FROZEN_CRITERIA_A.md): noise floor of the declared lensing-peak estimator on ISOLATED halos only.
48 runs = {main, sub} x alpha {0, 1} x footings {can, alt} x seeds {599, 621..625}, 0.6 Gyr each.  No merger run.
Run: nice -n 10 python3 cfg621_stageA.py  -> cfg621_stageA.out, cfg621_stageA_results.json (per-run series cached in runs_A/)
kappa = 1/2 fitted; the cold energy's mass is required (an input)."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import sys, json, time
import multiprocessing as mp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)

RUNS = os.path.join(HERE, "runs_A"); os.makedirs(RUNS, exist_ok=True)
HALOS = ["main", "sub"]; ALPHAS = [0.0, 1.0]; FEET = ["can", "alt"]; SEEDS = [599, 621, 622, 623, 624, 625]
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def name_of(c):
    return f"iso_{c['iso_which']}_a{c['alpha']:g}_{c['foot']}_s{c['seed']}"


def _round(o):
    if isinstance(o, float):
        return round(o, 4)
    if isinstance(o, list):
        return [_round(x) for x in o]
    if isinstance(o, dict):
        return {k: _round(v) for k, v in o.items()}
    return o


def worker(c):
    import cfg621_sim as S
    fn = os.path.join(RUNS, name_of(c) + ".json")
    if os.path.exists(fn):
        return
    res = S.run(dict(c))
    json.dump(_round(res), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


def series(r, w):
    out = dict(dL=[], dG=[], s=[], gal_r=[], M300=[])
    for d in r["diag"]:
        m = d[w]; g = np.array(m["gal"])
        out["dL"].append(float(np.hypot(*(np.array(m["lens"]) - g))))
        out["dG"].append(float(np.hypot(*(np.array(m["gas"]) - g))))
        out["s"].append(float(m["lens_spread"]))
        out["gal_r"].append(float(np.hypot(*g)))
        out["M300"].append(m["M300"])
    return out


def main():
    T0 = time.time()
    P("CFG621 stage A: isolated-halo noise floor of the declared estimator (FROZEN_CRITERIA_A.md). No merger run.")
    P("estimator E-1: shrinking circle R0 300 / R_min 75 kpc (galaxy, gas, lensing); spread variants (300,60) (300,90) (200,75) (400,75)")
    cfgs = [dict(alpha=a, foot=f, mode="isolated", iso_which=w, t_iso=0.6, seed=s)
            for w in HALOS for a in ALPHAS for f in FEET for s in SEEDS]
    todo = [c for c in cfgs if not os.path.exists(os.path.join(RUNS, name_of(c) + ".json"))]
    if todo:
        P(f"running {len(todo)} isolated run(s) on <= 4 processes ...")
        with mp.get_context("fork").Pool(min(4, len(todo))) as pool:
            pool.map(worker, todo, chunksize=1)
    R = {"lane": "CFG621", "stage": "A", "runs": {}}
    pooled = dict(dL=[], dG=[], s=[]); sub_dL = []
    groups = {}
    for c in cfgs:
        r = json.load(open(os.path.join(RUNS, name_of(c) + ".json")))
        w = c["iso_which"]
        se = series(r, w)
        drift = se["M300"][-1] / se["M300"][0] - 1
        R["runs"][name_of(c)] = dict(max_dL=max(se["dL"]), max_dG=max(se["dG"]), max_s=max(se["s"]), median_dL=float(np.median(se["dL"])),
                                     max_gal_from_true=max(se["gal_r"]), M300_drift=drift, n_epochs=len(se["dL"]),
                                     t0=dict(dL=se["dL"][0], dG=se["dG"][0], gal_r=se["gal_r"][0]), wall_s=r["wall_s"], series=se)
        for k in pooled:
            pooled[k] += se[k]
        if w == "sub":
            sub_dL += se["dL"]
        groups.setdefault((w, c["alpha"], c["foot"]), []).append(se)
    P95 = {k: float(np.percentile(v, 95)) for k, v in pooled.items()}
    TL, TG = 3 * P95["dL"], 3 * P95["dG"]
    R["n_epochs_pooled"] = len(pooled["dL"])
    R["P95_L"], R["P95_G"], R["P95_spread"] = P95["dL"], P95["dG"], P95["s"]
    R["T_L"], R["T_G"] = TL, TG
    P(f"\nT-1/T-2 pooled over {len(pooled['dL'])} epochs (48 runs x 61): P95_L = {P95['dL']:.2f} kpc -> T_L = {TL:.2f} kpc; "
      f"P95_G = {P95['dG']:.2f} kpc -> T_G = {TG:.2f} kpc")
    # T-4 C4(b) evaluated on the stage-A runs (gate for stage B)
    fails = []
    for n, rr in R["runs"].items():
        if rr["max_dL"] > TL or rr["max_dG"] > TG or abs(rr["M300_drift"]) > 0.10:
            fails.append(n)
    R["C4b_T4"] = dict(ok=not fails, failing_runs=fails, max_dL_all=max(pooled["dL"]), max_dG_all=max(pooled["dG"]),
                       max_abs_M300_drift=max(abs(rr["M300_drift"]) for rr in R["runs"].values()))
    P(f"T-4 (stage-B C4(b)) on all 48 runs: max d_L {max(pooled['dL']):.2f} (<= {TL:.2f}), max d_G {max(pooled['dG']):.2f} (<= {TG:.2f}), "
      f"max |M(<300) drift| {R['C4b_T4']['max_abs_M300_drift']:.4f} (<= 0.10): {'PASS' if not fails else 'FAIL ' + str(fails)}")
    # R-1 per configuration
    P("\nR-1 per configuration (6 seeds x 61 epochs): P95 / max of d_L, d_G, spread s [kpc]; median d_L; max galaxy offset from true centre")
    R["per_config"] = {}
    for (w, a, f), lst in groups.items():
        dl = sum((x["dL"] for x in lst), []); dg = sum((x["dG"] for x in lst), []); ss = sum((x["s"] for x in lst), [])
        gr = sum((x["gal_r"] for x in lst), [])
        e = dict(P95_dL=float(np.percentile(dl, 95)), max_dL=max(dl), median_dL=float(np.median(dl)), P95_dG=float(np.percentile(dg, 95)),
                 max_dG=max(dg), P95_s=float(np.percentile(ss, 95)), max_s=max(ss), max_gal_from_true=max(gr))
        R["per_config"][f"{w}_a{a:g}_{f}"] = e
        P(f"  {w:4s} alpha {a:g} {f}: d_L {e['P95_dL']:5.2f}/{e['max_dL']:5.2f}  d_G {e['P95_dG']:5.2f}/{e['max_dG']:5.2f}  "
          f"s {e['P95_s']:5.2f}/{e['max_s']:5.2f}  median d_L {e['median_dL']:5.2f}  gal {e['max_gal_from_true']:5.2f}")
    R["alpha1_minus_alpha0_median_dL"] = {}
    for w in HALOS:
        for f in FEET:
            dm = R["per_config"][f"{w}_a1_{f}"]["median_dL"] - R["per_config"][f"{w}_a0_{f}"]["median_dL"]
            R["alpha1_minus_alpha0_median_dL"][f"{w}_{f}"] = dm
    P("  alpha 1 minus alpha 0 median d_L [kpc]: " + json.dumps({k: round(v, 2) for k, v in R["alpha1_minus_alpha0_median_dL"].items()}))
    # R-2
    unst = float(np.mean(np.array(pooled["s"]) > TL))
    R["R2_unstable_fraction_isolated"] = unst
    P(f"\nR-2 pooled P95 of the lensing spread s = {P95['s']:.2f} kpc; fraction of isolated epochs UNSTABLE under T-3 (s > T_L): {unst:.4f}")
    # R-3
    p95sub = float(np.percentile(sub_dL, 95))
    NB = p95sub / (194.0 * 0.125)
    R["P95_L_sub"] = p95sub; R["N_B"] = NB
    P(f"R-3 P95_L (sub only) = {p95sub:.2f} kpc; N_B = P95_L,sub / (194 x 0.125 kpc) = {NB:.3f}  ({'> 1: stage B VOID' if NB > 1 else '<= 1: Bullet score diagnostic'})")
    # R-4
    r4 = R["runs"]["iso_main_a1_can_s599"]
    R["R4_cfg599_realisation"] = {k: r4[k] for k in ("max_dL", "max_dG", "max_s", "M300_drift")}
    P(f"R-4 CFG599's realisation (main, alpha 1, can, seed 599) with E-1: max d_L {r4['max_dL']:.2f} kpc (CFG599 R_min 50: 18.17), "
      f"max d_G {r4['max_dG']:.2f}, max s {r4['max_s']:.2f}, M(<300) drift {r4['M300_drift']:+.4f}")
    # t = 0 (reported; C4(a) is re-run in stage B)
    t0max = max(max(rr["t0"]["dL"], rr["t0"]["dG"], rr["t0"]["gal_r"]) for rr in R["runs"].values())
    R["t0_max_offset"] = t0max
    P(f"t = 0 (reported): largest of d_L, d_G, galaxy-from-true over the 48 starts = {t0max:.2f} kpc")
    R["wall_s"] = time.time() - T0
    for rr in R["runs"].values():
        rr.pop("series")
    open(os.path.join(HERE, "cfg621_stageA.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(R, open(os.path.join(HERE, "cfg621_stageA_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
