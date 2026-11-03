#!/usr/bin/env python3
"""TX1 summary and frozen labels from the lane's JSON. python3 -I tx1_summary.py. kappa = 1/2 FITTED; not theory closed."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p))) if os.path.exists(os.path.join(H, p)) else None; OUT = []
def P(s): print(s); OUT.append(s)
def kp(o):
    if o.get("missing"): return False
    return all(o["cells"][h]["n_ok"] == 15 and o["cells"][h]["p"] >= 0.05 and abs(o["cells"][h]["M3_tot"]) < 2 for h in o["cells"])
def ks(o): return "MISSING" if o.get("missing") else " ".join(f"{h[-3:]}: {o['cells'][h]['n_ok']}/15 M3 {o['cells'][h]['M3']:+.2f} chi2 {o['cells'][h]['chi2']:.3g} p {o['cells'][h]['p']:.2g}" for h in o["cells"])
for f in ("canonical", "alt"):
    P(f"== {f}")
    P("arm | enumerated | T hits | distinct T | X-COP LINE | X-COP ERR | train LINE | train ERR | train ERR + Cassini | T-free train LINE / ERR | top-10 keys 15/15, p, M3")
    real_k = None; ctrl = []
    for a in ("real", "c1", "c2", "c3", "label"):
        T = J(f"tx1_train_TL0_{f}_{a}.json"); K = J(f"tx1_keys_{f}_{a}.json")
        if T is None: P(f"{a} missing"); continue
        c = T["counts"]; nk = None if K is None else sum(kp(o) for o in K[1:11])
        P(f"{a} | {T['tally']['enum']:.3g} | {c['T_hits']} | {c['distinct_T']} | {c['g3_line']} | {c['g3_err']} | {c['train_line']} | {c['train_err']} | {c['train_err_cass']} | {c['F_train_line']} / {c['F_train_err']} | {nk}")
        if a == "real": real_k = (nk, c["distinct_T"])
        elif nk is not None: ctrl.append((a, nk, c["distinct_T"]))
    K = J(f"tx1_keys_{f}_real.json")
    if K:
        P("keys, real: law first, then top 10 T, then best T-free by Z, then BK2 row (a)")
        for o in K: P(f"  {o['F'][:95]} | {ks(o)}")
    S2 = J(f"tx1_stage2_{f}.json"); best = None
    if S2 and K:
        kk = {o["F"]: o for o in K}
        for o in S2:
            p = o["pass"]; err = dict(G1=p["G1"], S=p["S"], G3=p["G3E"], G5=p["G5E"], G5b=p["G5b"], LT=p["LTE"], GR=p["GR"], KEYS=kp(kk[o["F"]]) if o["F"] in kk else False); o["err_pass"] = err
            P(f"  stage2 {o['F'][:80]} | ERR fails {[k for k, v in err.items() if not v]} | LINE fails {[k for k, v in p.items() if not v]}")
        Tj = [o for o in S2[1:11] if all(o["err_pass"].values())]; P(f"T forms passing every frozen-label gate on ERR, keys included: {len(Tj)}")
    for a in ("post", "top3_median", "top3_cut"):
        K2 = J(f"tx1_keys_{f}_{a}.json")
        if K2:
            P(f"keys POST/sensitivity {a}: {sum(kp(o) for o in K2[1:])} of {len(K2)-1} pass 15/15, p >= 0.05, M3 < 2")
            for o in K2[1:]: P(f"  {o['F'][:90]} | {ks(o)}")
open(os.path.join(H, "tx1_summary.out"), "w").write("\n".join(OUT) + "\n")
