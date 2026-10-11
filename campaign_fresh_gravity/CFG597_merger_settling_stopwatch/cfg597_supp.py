#!/usr/bin/env python3
"""CFG597 supplementary S1 (POST-FREEZE, disclosed in README D-3, REPORTED ONLY, no verdict):
the frozen gas model (beta-model r_c = 0.1 r200) strips the sub's gas wholesale before pericentre, so the frozen runs have
gas-galaxy separations ~800-930 kpc at the 720-kpc epoch instead of the Bullet's 194 kpc.  S1 repeats L-2S, canonical, 10:1 with
a compact sub gas core (r_c = 0.03 r200 ~ 30 kpc, a cool-core-like bullet; ordinary gas physics) to see whether the alpha
dependence survives a Bullet-like geometry.  Same v0 as the frozen L 10:1 cell, same scores.
Run: nice -n 10 python3 cfg597_supp.py  (after cfg597_main.py)  -> cfg597_supp.out, cfg597_supp_results.json"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import sys, json, math
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg597_lib as L
import cfg597_main as M

ALPHAS = [0.0, 0.1, 0.3, 1.0, math.inf]
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def nm(c):
    return f"S1_rc003_r10_L_2S_a{M.astr(c['alpha'])}_can"


def work(c):
    import cfg597_sim as S
    fn = os.path.join(M.RUNS, nm(c) + ".json")
    if not os.path.exists(fn):
        json.dump(M._round(S.run(c)), open(fn, "w"))
    return fn


def main():
    R0 = json.load(open(os.path.join(HERE, "cfg597_results.json")))
    v0 = R0["calibration"]["10_L"]["v0_kms"]
    cfgs = [dict(ratio="10", case="L", rule="2S", alpha=a, foot="can", v0=v0 * L.KMS, sub_rc_frac=0.03) for a in ALPHAS]
    with mp.get_context("fork").Pool(4) as pool:
        fns = pool.map(work, cfgs, chunksize=1)
    P("CFG597 S1 (post-freeze, reported only): compact sub gas core r_c = 0.03 r200, L-2S canonical 10:1, v0 = %.0f km/s" % v0)
    P(f"{'alpha':>6s} {'t_obs':>6s} {'dSG':>6s} {'f150':>7s} {'f100':>7s} {'Z_B':>6s} | {'bbar150':>7s} {'Z_H':>6s}")
    res = {}
    for c, fn in zip(cfgs, fns):
        r = json.load(open(fn)); b = M.bullet_stat(r, "sub"); h = M.harvey_stat(r)
        res[M.astr(c["alpha"])] = dict(bullet=b, harvey=h, t_peri=r["t_peri"])
        if b and b.get("reached") and h and "Z" in h:
            P(f"{M.astr(c['alpha']):>6s} {b['t_obs_after_peri']:6.3f} {b['dSG_kpc']:6.0f} {b['f150']:+7.3f} {b['f100']:+7.3f} {b['Z']:+6.2f} | "
              f"{h['beta150']:+7.3f} {h['Z']:+6.2f}")
        else:
            P(f"{M.astr(c['alpha']):>6s} not scorable: {b} {h}")
    open(os.path.join(HERE, "cfg597_supp.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(dict(lane="CFG597", part="S1 supplementary (post-freeze, reported only)", sub_rc_frac=0.03, v0_kms=v0, results=res),
              open(os.path.join(HERE, "cfg597_supp_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
