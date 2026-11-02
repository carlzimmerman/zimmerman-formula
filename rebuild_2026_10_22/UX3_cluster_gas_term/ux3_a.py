#!/usr/bin/env python3
"""UX3 Part A (FROZEN_CRITERIA.md): where the family breaks discs, odd SPARC names only. --mutate shuffles f. kappa = 1/2 FITTED; not theory closed."""
import json, sys
from ux3_common import *
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; OUT = []; R = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
S = sparc(); ST = S[1].copy(); X, _ = xcop(); XT = X[X[:, 4].astype(int) % 2 == 0]; XH = X[X[:, 4].astype(int) % 2 == 1]
if MUT: ST[:, 3] = ST[np.random.default_rng(20261102).permutation(len(ST)), 3]
P(f"UX3 Part A{TAG}; train SPARC {len(ST)} points, X-COP train {len(XT)} rows; canonical and alt separately; kappa = 1/2 FITTED")
def bins(A, a0):
    y = A[:, 0] / a0; t = np.quantile(y, [1 / 3, 2 / 3]); f = A[:, 3]; vf = A[:, 7]; rr = A[:, 6]
    b = {f"f {l}-{h}": (f >= l) & (f < h + (1e-9 if h == 1 else 0)) for l, h in ((0, .25), (.25, .5), (.5, .75), (.75, 1))}
    b.update({"y low": y < t[0], "y mid": (y >= t[0]) & (y < t[1]), "y high": y >= t[1], "Vflat none": vf <= 0, "Vflat <60": (vf > 0) & (vf < 60), "Vflat 60-120": (vf >= 60) & (vf < 120), "Vflat >120": vf >= 120, "R/Rl <1/3": rr < 1 / 3, "R/Rl 1/3-2/3": (rr >= 1 / 3) & (rr < 2 / 3), "R/Rl >2/3": rr >= 2 / 3, "GASRICH f>.5,V<120": (f > .5) & (vf > 0) & (vf < 120)})
    return b
K = 0
for ft, a0 in A0S.items():
    R[ft] = {}; d0 = resid(ST, a0, lambda y, f, A: 1.0 + 0 * y); r0 = st(d0)[1]; P(f"\n=== {ft}: law rms {r0:.3f}, median {np.median(d0):+.3f}; y median {np.median(ST[:,0]/a0):.3f}; g_gas/a0 median {np.median(ST[:,0]/a0*ST[:,3]):.3f}; X-COP train y median {np.median(XT[:,0]/a0):.3f}, g_gas/a0 {np.median(XT[:,0]/a0*XT[:,3]):.3f}")
    rows = {f"B {n}": (lambda fn: (lambda y, f, A: fn(f) + PI2 * y * f))(fn) for n, fn in BMEM.items()}; rows["F1 A=1"] = lambda y, f, A: 1 + PI2 * y * f
    for n, fn in BMEM.items(): rows[f"const only {n}"] = (lambda fn: (lambda y, f, A: fn(f)))(fn)
    for n, H in rows.items():
        d = resid(ST, a0, H); ex = d * d - d0 * d0; tot = ex.sum(); dx = resid(XT, a0, H); dh = resid(XH, a0, H); dsh = resid(S[0], a0, H); o = dict(rms=st(d)[1], med=st(d)[2], xt=st(dx)[:2], xh=st(dh)[:2], sh=st(dsh)[1], bins={})
        if n.startswith("B") and ft == "canonical" and not MUT:
            q = BF1LINE[n[2:]]; K = max(K, abs(o["xt"][0] - q[0]), abs(o["xt"][1] - q[1]), abs(o["rms"] - q[2]), abs(o["xh"][0] - q[3]), abs(o["xh"][1] - q[4]), abs(o["sh"] - q[5]))
        B = bins(ST, a0)
        for b, m in B.items():
            dr = d.copy(); dr[m] = d0[m]; o["bins"][b] = dict(n=int(m.sum()), share=float(ex[m].sum() / tot), med=float(np.median(d[m])) if m.any() else None, medlaw=float(np.median(d0[m])) if m.any() else None, rms=float(np.sqrt((d[m] ** 2).mean())) if m.any() else None, rms_reset=float(np.sqrt((dr ** 2).mean())))
        R[ft][n] = o; P(f"\n{n}: rms {o['rms']:.3f}, med {o['med']:+.3f}; X train {o['xt'][0]:+.3f},{o['xt'][1]:.3f}; X hold {o['xh'][0]:+.3f},{o['xh'][1]:.3f}")
        for g in (("f 0-0.25", "f 0.25-0.5", "f 0.5-0.75", "f 0.75-1"), ("y low", "y mid", "y high"), ("Vflat none", "Vflat <60", "Vflat 60-120", "Vflat >120"), ("R/Rl <1/3", "R/Rl 1/3-2/3", "R/Rl >2/3"), ("GASRICH f>.5,V<120",)):
            P("  " + " | ".join(f"{b}: N {o['bins'][b]['n']}, share {o['bins'][b]['share']:.2f}, med {o['bins'][b]['med']:+.3f} (law {o['bins'][b]['medlaw']:+.3f}), reset {o['bins'][b]['rms_reset']:.3f}" for b in g if o['bins'][b]['n']))
            if len(g) > 1: assert abs(sum(o["bins"][b]["share"] for b in g) - 1) < 1e-9
        gr, inn = o["bins"]["GASRICH f>.5,V<120"]["share"], o["bins"]["R/Rl <1/3"]["share"]; o["label"] = "GAS-RICH DWARFS" if gr >= .5 else "INNER DISCS" if inn >= .5 else "WHOLE DISC"
        if gr >= .5 and inn >= .5: o["label"] = "GAS-RICH DWARFS and INNER DISCS"
        P(f"  LABEL {o['label']}: gas-rich share {gr:.2f}, inner share {inn:.2f}, y-high share {o['bins']['y high']['share']:.2f}")
    # separation
    from scipy.stats import rankdata
    def auc(a, b): r = rankdata(np.r_[a, b]); na = len(a); return float((r[:na].sum() - na * (na + 1) / 2) / (na * len(b)))
    def feats(A):
        R_ = A[:, 2]; g = A[:, 0] * A[:, 3]; Mg = g * R_ ** 2 / G / MS; return {"y": A[:, 0] / a0, "g_gas/a0": g / a0, "f": A[:, 3], "ell": R_ * a0 / C ** 2, "gas slope": A[:, 8], "Sigma_gas mean": Mg / (math.pi * (R_ / PC) ** 2), "rho_gas mean": Mg / (R_ / PC) ** 3}
    fs, fx = feats(ST), feats(XT); R[ft]["sep"] = {}
    for k in fs:
        a = auc(fx[k], fs[k]); R[ft]["sep"][k] = dict(auc=a, sparc_q=np.percentile(fs[k], [5, 50, 95]).tolist(), xcop_q=np.percentile(fx[k], [5, 50, 95]).tolist()); P(f"  sep {k}: AUC(X-COP > SPARC) {a:.3f}; SPARC 5/50/95 {np.array2string(np.percentile(fs[k],[5,50,95]),precision=3)}; X-COP {np.array2string(np.percentile(fx[k],[5,50,95]),precision=3)}")
if not MUT: P(f"\nK3 BF1 lines max |d| {K:.4f}: {'PASS' if K <= .002 else 'FAIL'}"); R["K3"] = K
json.dump(R, open(f"ux3_a{TAG}.json", "w"), indent=1, default=float); open(f"ux3_a{TAG}.out", "w").write("\n".join(OUT) + "\n")
