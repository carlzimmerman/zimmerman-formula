#!/usr/bin/env python3
"""HIS1R comparison (written after RESULT_BLIND.md was committed and pushed): HIS1's his1.json against HIS1R's his1r.json,
number by number, plus the two diagnostics that explain the differences. TEST lane; adopts nothing.
Usage: python3 his1r_compare.py -> his1r_compare.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import his1r as H
A = json.load(open(os.path.join(HERE, "..", "HIS1_history_reading", "his1.json"))); B = json.load(open(os.path.join(HERE, "his1r.json")))
OUT = []
def P(s=""): print(s); OUT.append(str(s))
def fl(x):
    try: return float(x)
    except Exception: return float("nan")
rows = []
def add(name, a, b):
    a, b = fl(a), fl(b); rows.append((name, a, b, b - a if math.isfinite(a) and math.isfinite(b) else float("nan")))
MP = {"SPARC gas-rich (f_g >= 0.5)": "SPARC gas-rich", "faint rotators, Ti1 < 0": "faint rotators Ti1<0"}
for f in ("canonical", "alt"):
    h = A["tests"][f]; F = A["controls"][f]["force"]; R = B["footings"][f]["main"]
    for q in ("Y", "dL"):
        add(f"{f} H1 median {q}", h["H1"][q]["med"], R["H1"][q]["med"]); add(f"{f} H1 se {q}", h["H1"][q]["se"], R["H1"][q]["se"])
    add(f"{f} H2 count below", h["H2"]["n_below"], R["H2"]["a_count"])
    for x in R["H2"]["c"]:
        v = h["H2"]["DF"][x["sys"]]
        for q, k in (("Y", "Y"), ("d_L", "dL"), ("e", "e")): add(f"{f} H2 {x['sys']} {q}", v[k], x[k])
    for part in ("a", "b", "c"):
        for nm, s in h["H3"][part].items():
            k = MP.get(nm, nm); t = R["H3"]["sets"][k]
            for q in ("med", "se", "n"): add(f"{f} H3{part} {k} {q}", s[q], t[q])
    for p in R["H5"]["pairs"]:
        q = h["H5"]["pairs"][p["pair"]]
        for k in ("rho", "p", "n"): add(f"{f} H5 {p['pair']} {k}", q[k], p[k])
    add(f"{f} F1 median d_L", F["F1"]["dL"]["med"], R["H1"]["dL"]["med"])
    add(f"{f} F2 count", F["F2"]["n_below_law"], R["force"]["F2_count"])
    add(f"{f} F4 median", F["F4"]["dL_last"]["med"], R["force"]["F4_stat"]["med"]); add(f"{f} F4 se", F["F4"]["dL_last"]["se"], R["force"]["F4_stat"]["se"])
    add(f"{f} force score", F["score"], R["force"]["score"])
    add(f"{f} no-rule holds", A["labels"][f]["shuffled_holds"], R["norule"]["holds"])
    P(f"{f}: HIS1 label {A['labels'][f]['label']} | HIS1R {R['label']} {R['outcomes']}")
    P(f"{f}: F3 off the law HIS1 {F['F3']['off_law']} | HIS1R {[k for k, v in R['force']['F3_sets'].items() if not v]}")
big = [r for r in rows if not (abs(r[3]) <= 5e-12)]
P(f"compared {len(rows)} numbers; differing beyond 5e-12: {len(big)}")
for r in big: P(f"   {r[0]}: HIS1 {r[1]:.6g}  HIS1R {r[2]:.6g}  diff {r[3]:+.3g}")
# diagnostics
sk = sorted(f"{c}|{n}" for c, n in H.KEYS); labs = [k.split("|", 1)[0] for k in sk]
perm = np.random.default_rng(7).permutation(len(sk)); shuf = {sk[i]: labs[perm[i]] for i in range(len(sk))}
lab = np.array([shuf[f"{c}|{n}"] for c, n in H.KEYS], dtype=object)
for f, a0 in H.FOOT.items():
    S = H.systems(H.Y0, a0); R = H.grade(S, lab, {}, controls=False)
    empty = sorted({k for k in H.H3A + H.H3B + H.H3C if R["H3"]["sets"][k]["n"] == 0})
    P(f"{f}: HIS1's permutation (sorted keys) graded by HIS1R's rules: {dict((h, R[h]['outcome']) for h in ('H1', 'H2', 'H3', 'H5'))}; empty H3 sets {empty}")
    xm = H.CLS0 == "X-COP"
    P(f"{f}: F4 se with e_sys (median over the system's points) {H.cstat(S['Dlast'][xm], S['E'][xm])['se']:.4f}; with the last point's own e {H.cstat(S['Dlast'][xm], S['Elast'][xm])['se']:.4f}")
P(f"KA2 table-Y check: HIS1 vs the rounded Mdyn_over_Mbar column, max {A['KA']['KA2']['max_dY']:.4f}; HIS1R vs M_dyn / M_bar columns, max "
  f"{max(abs(x) for x in B['KA']['KA2']['table_minus_logratio']):.4f}")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "his1r_compare.out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
