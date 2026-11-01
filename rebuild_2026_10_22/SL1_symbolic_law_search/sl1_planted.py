#!/usr/bin/env python3
"""SL1 K8: synthetic data from a tree in the grammar. The GA must reach L_gate 0. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
os.environ.setdefault("SL1_HERE", os.path.dirname(os.path.abspath(__file__)))
exec(compile(open(os.path.join(os.environ["SL1_HERE"], "discover_law.py")).read().split('if __name__ == "__main__" and "--sweep"')[0], "discover_law", "exec"), globals())
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
PL = sys.argv[1] if len(sys.argv) > 1 else "A"
At = ("inv1p", ("div", "q", ("mul", "eta", "eta"))); Bt = "1"
if PL == "JOINT": At = ("sqrt", ("inv1p", ("div", ("log1p", "q"), ("sqrt", "cf")))); Bt = ("add", "1", ("mul", "xb", ("inv1p", ("mul", "fl", "q"))))
D = Data(); a0 = D.a0["canonical"]; assert tier1(At, "A"); iU = int(np.argmin(abs(D.UPS - 0.6)))
for t in TAGS:
    o = D.sparc(D.split["train"], t); A = o["s"].rho(At); P(f"plant A range on {t}: {A.min():.3f}..{A.max():.3f}"); Mc = o["s"].Mfrac(A, o["Rm"], o["gid"]); Bp = 1.0 if Bt == "1" else ev(Bt, dict(xb=o["GB"][:, iU] / a0, xc=o["gc0"] / a0, fl=o["Mb"][:, iU] / o["M0"], q=o["q_p"][:, 0])); o["lgo"] = np.log10(np.maximum(o["GB"][:, iU] + D.c["GE"] * Mc * Bp / o["Rm"] ** 2, 1e-300))
    Es = D.lt_E(t, At, Bt, a0); D.lt[t]["lgo"] = D.lt[t]["lgo"] - Es + np.random.default_rng(1).normal(0, 0.0, len(Es))
o = D.sparc(D.split["train"], TA); A = o["s"].rho(At); S = D.S_eff(o["s"], A); iv = []
for (l, h) in BINS:
    m = (o["vf"] >= l) & (o["vf"] < h if h < 400 else o["vf"] <= h); sm = float(np.median(S[m])); iv.append((sm * 0.85, sm * 1.15))
meas = {}
for h in HKS:
    V = D.cluster_V(h, At, Bt, a0); cap = dict(capture=True, pred_out={}); keys_core(D.C["clusters"], V, "canonical", h, cap); meas[h] = cap["pred_out"][h]
D.pl = dict(iv=iv, meas=meas, ltoff={t: 0.0 for t in TAGS})
g = D.grade(At, Bt); b = D.grade("1", "1"); P(f"plant {to_s(At)}: gate at plant {g['gate']:.4f}; gate at identity {b['gate']:.3f} (g1 {b['g1']:.2f} g2 {b['g2']:.2f} g3 {b['g3']:.2f} g4 {b['g4']:.2f})")
S_ = Search(D, "SPEC", 8, tag="PLANTED" + PL); 
if os.path.exists(S_.f): os.remove(S_.f)
R = S_.run(stop_on_hit=True); hit = R["hits"][0] if R["hits"] else None; ok = bool(hit) and g["gate"] == 0 and b["gate"] > 0
P(f"K8 GA reached L_gate 0: {bool(hit)} at generation {R['gen']}, {R['n_eval']} evaluations: {hit['A'] if hit else None} / {hit['B'] if hit else None}: {'PASS' if ok else 'FAIL'}")
if PL == "JOINT": open(os.path.join(HERE, "sl1_planted_joint.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
E = Enum(D, "A", "SPEC")
for s_ in range(2, 7): r_ = E.grow(s_); P(f"  sweep A size {s_}: {E.counts.get(s_, 0)} values, {len(E.surv.get(s_, []))} Tier 1")
tr = [simplify(E.tree(i)) for s_ in E.surv for i in E.surv[s_]]; gg = [(D.grade(t, "1") or dict(gate=9e9))["gate"] for t in tr]; zero = [to_s(t) for t, v in zip(tr, gg) if v == 0]; k8b = len(zero) > 0; ok = ok and k8b; P(f"K8b sweep to size 6 finds the plant's size-{size(At)} tree: {len(zero)} zero-gate trees: {zero[:4]}: {'PASS' if k8b else 'FAIL'}")
open(os.path.join(HERE, "sl1_planted.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
