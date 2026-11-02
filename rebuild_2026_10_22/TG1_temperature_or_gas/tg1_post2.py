#!/usr/bin/env python3
"""TG1 POST-RESULT, after seeing split and joint lean opposite ways: joint fit through the same mocks, and split slopes with residual imbalance solved out. No label moves. kappa = 1/2 FITTED; not theory closed."""
from tg1_common import *
OUT = []; SP = json.load(open(os.path.join(HERE, "tg1_split.json")))
def P(s=""): print(s, flush=True); OUT.append(str(s))
def fld(a, b):
    d = a.mean(0) - b.mean(0); C = (np.cov(a.T) + np.cov(b.T)) / 2; return float(np.sqrt(d @ np.linalg.solve(C, d)))
for fi, f in enumerate(FEET):
    for hi_, h in enumerate(HS):
        S = sample(f, h); mk = Mock(S, 0); e0 = (S["n"] - S["V"]).sum(1); w0 = S["W"].sum(1); one = np.ones(mk.N); th = joint(e0, w0, (one, S["t"], S["g"]))[1:]
        Z = {}
        for k, hy in enumerate(("H0", "HT", "HG")):
            rg = np.random.default_rng([SEED, 3000 + 100 * fi + 10 * hi_, k]); o = np.zeros((NM, 2))
            for r in range(NM):
                e, w, t, g = mk.draw(rg, hy); o[r] = joint(e, w, (one, t, g))[1:]
            Z[hy] = o
        s = Z["H0"].std(0, ddof=1); z0 = th / s; P(f"{f} {h} joint: data b_T {th[0]:+.1f} b_G {th[1]:+.1f}; mock sd {s[0]:.1f}, {s[1]:.1f}; z ({z0[0]:+.2f}, {z0[1]:+.2f}); means in z: H0 {np.round(Z['H0'].mean(0)/s,2).tolist()} HT {np.round(Z['HT'].mean(0)/s,2).tolist()} HG {np.round(Z['HG'].mean(0)/s,2).tolist()}; sd HT {np.round(Z['HT'].std(0)/s,2).tolist()}; F_LD {fld(Z['HT']/s, Z['HG']/s):.2f}; p(|z_T| | HG) {(np.abs(Z['HG'][:,0]/s[0])>=abs(z0[0])).mean():.3f}, p(|z_G| | HT) {(np.abs(Z['HT'][:,1]/s[1])>=abs(z0[1])).mean():.3f}, p(|z_T| | HT) {(np.abs(Z['HT'][:,0]/s[0])>=abs(z0[0])).mean():.3f}, p(|z_G| | HG) {(np.abs(Z['HG'][:,1]/s[1])>=abs(z0[1])).mean():.3f}")
        c = SP["cells"][f"{f}|{h}"]; a = abs(np.array(c["dg_T"])).sum() / abs(np.array(c["dt_T"])).sum(); b = abs(np.array(c["dt_G"])).sum() / abs(np.array(c["dg_G"])).sum(); M = np.array([[1, a], [b, 1]]); x = np.linalg.solve(M, [c["bT"], c["bG"]]); P(f"  split imbalance solved out, rough: b_T {x[0]:+.1f}, b_G {x[1]:+.1f} (mixing {a:.3f}, {b:.3f}); a linear reading, data errors not propagated")
open(os.path.join(HERE, "tg1_post2.out"), "w").write("\n".join(OUT) + "\n")
