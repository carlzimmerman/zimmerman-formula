#!/usr/bin/env python3
"""QX33 (criteria 5741430147): CLASH lookback concentration of the law's missing mass vs baryons, HIGH z>=0.40 vs LOW.
    python3 qx33.py     # qx33.json / qx33.out
kappa = 1/2 FITTED; not theory closed. 1 thread, seconds."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "qx33"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * gN)
def ginv(g, a0): return g ** 2 / (g + a0)
# ---- data
rows = []
for line in open(os.path.join(ROOT, "real_research", "data", "clash_rar_tian2020_fig2.tsv")):
    if line.startswith("#") or not line.strip(): continue
    f = line.rstrip("\n").split("\t")
    try: rows.append((f[1].strip(), float(f[2]), float(f[3]), float(f[4]), float(f[5]), float(f[6])))
    except (ValueError, IndexError): continue
names = sorted({r[0] for r in rows})
# MCXC by position (RA hh mm, Dec sign dd) -> z, R500 [Mpc]; MACS0416 by hand (Postman+2012), disclosed
POS = {"A209": "J0131.8-1336", "A383": "J0248.0-0332", "A611": "J0800.9+3602", "A2261": "J1722.4+3208",
       "MACS0329": "J0329.6-0211", "MACS0429": "J0429.5-0253", "MACS0647": "J0647.8+7014", "MACS0717": "J0717.5+3745",
       "MACS0744": "J0744.8+3927", "MACS1115": "J1115.8+0129", "MACS1149": "J1149.5+2224", "MACS1206": "J1206.2-0848",
       "MACS1720": "J1720.2+3536", "MACS1931": "J1931.8-2634", "MS2137": "J2140.2-2339", "RXJ1347": "J1347.5-1144",
       "RXJ1532": "J1532.9+3021", "RXJ2129": "J2129.6+0005", "RXJ2248": "J2248.7-4431"}
MC = {}
for line in open(os.path.join(ROOT, "gext_vectors_2026", "data", "raw", "mcxc.tsv")):
    if line.startswith("#") or not line.startswith("J"): continue
    f = line.rstrip("\n").split("\t")
    try: MC[f[0].strip()] = (float(f[4]), float(f[7]))
    except (ValueError, IndexError): pass
Z = {}; R5 = {}
for n in names:
    if n == "MACS0416": Z[n], R5[n] = 0.396, float("nan")
    else: Z[n], R5[n] = MC[POS[n]]
HIGH = [n for n in names if Z[n] >= 0.40]; LOW = [n for n in names if Z[n] < 0.40]
RES = dict(tag=TAG, criteria="5741430147", note="kappa = 1/2 FITTED; not theory closed", z=Z, R500_Mpc=R5, HIGH=HIGH, LOW=LOW)
K2 = len(rows) == 84 and len(names) == 20 and all(n in Z for n in names)
P(f"QX33: {len(rows)} points, {len(names)} clusters; HIGH (z>=0.40) {len(HIGH)}: {HIGH}; LOW {len(LOW)}")
P(f"  K2 (parse 84/20, all z matched): {'PASS' if K2 else 'FAIL'}")

def per_cluster(a0, rmin=0.0, rscale=False, mut=None):
    out = {}
    for n in names:
        pts = [r for r in rows if r[0] == n and r[1] >= rmin]
        if len(pts) < 2: continue
        r = np.array([p[1] for p in pts]); lb = np.array([p[2] for p in pts]); lt = np.array([p[3] for p in pts])
        eb = np.array([p[4] for p in pts]); et = np.array([p[5] for p in pts])
        if mut == "A" and n in HIGH: lt = lt - 0.3 * np.log10(r / 100.0)
        if mut == "B": lt = lt + 0.5 * np.log10(r / 100.0)
        gt = 10 ** lt; gb = 10 ** lb
        if a0 > 0: lR = np.log10(ginv(gt, a0) / gb)
        else: lR = np.log10(gt / gb)
        dl = (gt + 2 * a0) / (gt + a0) if a0 > 0 else np.ones_like(gt)   # d log gN_need / d log g_tot
        sig = np.sqrt((dl * et) ** 2 + eb ** 2); w = 1 / sig ** 2
        x = np.log10(r / (1e3 * R5[n]) if (rscale and np.isfinite(R5[n])) else r)
        if rscale and not np.isfinite(R5[n]): continue
        X = np.vstack([np.ones_like(x), x]).T; W = np.diag(w)
        beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ lR)
        A200 = float(np.interp(math.log10(200.0), np.log10(r), lR)) if r.min() <= 200 <= r.max() else float("nan")
        out[n] = dict(s=float(beta[1]), A200=A200, npts=int(len(r)))
    return out

rng = np.random.default_rng(3333); rngp = np.random.default_rng(3334)
def boot_med(v, B=10000):
    v = np.asarray(v); m = np.median(rng.choice(v, size=(B, len(v)), replace=True), axis=1)
    return float(np.median(v)), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))
def q1(v):
    med, lo, hi = boot_med(v)
    if med <= -0.10 and hi < 0: lab = "MORE CONCENTRATED THAN BARYONS"
    elif lo >= -0.10 and hi <= 0.10: lab = "TRACES BARYONS"
    elif med >= 0.10 and lo > 0: lab = "LESS CONCENTRATED"
    else: lab = "UNRESOLVED"
    return dict(median=med, ci=[lo, hi], label=lab)
def q2(pc, key, B=10000):
    hi = [pc[n][key] for n in HIGH if n in pc and np.isfinite(pc[n][key])]; lo = [pc[n][key] for n in LOW if n in pc and np.isfinite(pc[n][key])]
    d = float(np.median(hi) - np.median(lo)); allv = np.array(hi + lo); nh = len(hi); ds = []
    for _ in range(B):
        p = rngp.permutation(allv); ds.append(np.median(p[:nh]) - np.median(p[nh:]))
    ds = np.abs(np.array(ds)); p = float((np.sum(ds >= abs(d)) + 1) / (B + 1)); hw = float(np.percentile(ds, 95))
    return dict(delta=d, p=p, halfwidth95=hw, n_high=nh, n_low=len(lo), evolves=bool(abs(d) >= 0.10 and p < 0.05))
def spearman(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b)); return float(np.corrcoef(ra, rb)[0, 1])

# K1, K3
gt = 10 ** np.array([r[3] for r in rows]); k1 = max(float(np.max(np.abs(glaw(ginv(gt, a0), a0) - gt) / gt)) for a0 in A0.values())
K1 = k1 < 1e-10
lt = np.array([r[3] for r in rows]); lb = np.array([r[2] for r in rows]); k3 = float(np.max(np.abs(np.log10(ginv(gt, 1e-30) / 10 ** lb) - (lt - lb))))
K3 = k3 < 1e-6
P(f"  K1 (exact inverse): max rel err {k1:.2e} -> {'PASS' if K1 else 'FAIL'}; K3 (a0->0 = Newton): {k3:.2e} dex -> {'PASS' if K3 else 'FAIL'}")
RES.update(K1=dict(err=k1, pass_=bool(K1)), K2=bool(K2), K3=dict(err=k3, pass_=bool(K3)))

RES["footings"] = {}
for f, a0 in A0.items():
    pc = per_cluster(a0); R = dict(per_cluster=pc)
    sH = [pc[n]["s"] for n in HIGH]; sA = [pc[n]["s"] for n in names]; sL = [pc[n]["s"] for n in LOW]
    R["Q1_HIGH"] = q1(sH); R["Q1_ALL_reported"] = q1(sA); R["Q1_LOW_reported"] = q1(sL)
    R["Q2_s"] = q2(pc, "s"); R["Q2_A200"] = q2(pc, "A200")
    R["Q2_label"] = "EVOLVES" if (R["Q2_s"]["evolves"] or R["Q2_A200"]["evolves"]) else "NO EVOLUTION DETECTED"
    zz = [Z[n] for n in names]; R["spearman_s_z"] = spearman(zz, sA); R["spearman_A200_z"] = spearman(zz, [pc[n]["A200"] for n in names])
    P(f" [{f}] per cluster (z, s, A200, n):")
    for n in sorted(names, key=lambda n: Z[n]): P(f"     {n:9s} z {Z[n]:.3f}  s {pc[n]['s']:+.3f}  A200 {pc[n]['A200']:+.3f}  n {pc[n]['npts']}")
    for k in ("Q1_HIGH", "Q1_LOW_reported", "Q1_ALL_reported"):
        P(f"   {k}: median s {R[k]['median']:+.3f} [{R[k]['ci'][0]:+.3f}, {R[k]['ci'][1]:+.3f}] -> {R[k]['label']}")
    for k in ("Q2_s", "Q2_A200"):
        P(f"   {k}: Delta(HIGH-LOW) {R[k]['delta']:+.3f}, p {R[k]['p']:.3f}, 95% perm half-width {R[k]['halfwidth95']:.3f} -> {'EVOLVES' if R[k]['evolves'] else 'no'}")
    P(f"   Q2 LABEL: {R['Q2_label']}; Spearman(s, z) {R['spearman_s_z']:+.2f}, Spearman(A200, z) {R['spearman_A200_z']:+.2f}")
    # variants (reported)
    for vn, kw in (("drop_r_lt_50kpc", dict(rmin=50.0)), ("r_over_R500", dict(rscale=True))):
        pv = per_cluster(a0, **kw); vH = [pv[n]["s"] for n in HIGH if n in pv]; vL = [pv[n]["s"] for n in LOW if n in pv]
        R[vn] = dict(Q1_HIGH=q1(vH), Q1_LOW=q1(vL), Q2_s=q2(pv, "s"), n=len(pv))
        P(f"   [variant {vn}, {len(pv)} clusters] HIGH {R[vn]['Q1_HIGH']['median']:+.3f} {R[vn]['Q1_HIGH']['ci']} {R[vn]['Q1_HIGH']['label']}; "
          f"LOW {R[vn]['Q1_LOW']['median']:+.3f} {R[vn]['Q1_LOW']['label']}; Delta_s {R[vn]['Q2_s']['delta']:+.3f} p {R[vn]['Q2_s']['p']:.3f}")
    # MUTATEs
    pa = per_cluster(a0, mut="A"); mA = q2(pa, "s"); R["MUTATE_A"] = dict(Q2_s=mA, bites=bool(mA["evolves"]))
    pb = per_cluster(a0, mut="B"); mB = q1([pb[n]["s"] for n in HIGH]); R["MUTATE_B"] = dict(Q1=mB, bites=bool(mB["label"] != R["Q1_HIGH"]["label"]))
    P(f"   MUTATE A (HIGH slope -0.3): Delta_s {mA['delta']:+.3f} p {mA['p']:.4f} -> {'BITES' if mA['evolves'] else 'NO BITE'}; "
      f"MUTATE B (all +0.5): Q1 {mB['label']} (median {mB['median']:+.3f}) -> {'BITES' if R['MUTATE_B']['bites'] else 'NO BITE'}")
    ok = K1 and K2 and K3 and R["MUTATE_A"]["bites"] and R["MUTATE_B"]["bites"]
    R["LABEL"] = (f"Q1 {R['Q1_HIGH']['label']}; Q2 {R['Q2_label']}") if ok else "NO VERDICT (control failed)"
    P(f"   LABEL [{f}]: {R['LABEL']}")
    RES["footings"][f] = R
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
