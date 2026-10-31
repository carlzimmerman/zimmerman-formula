#!/usr/bin/env python3
"""SN1 POST-RESULT (after sn1.out, no frozen verdict): replace EM1's extrapolated M200 with a free line lg M200 = a + b (lg M* - 7).
Which (S, a, b) put all five classes at |Z| < 2? (i) flat S; (ii) k x measured rule. Also V2 at the frozen step 0.01. One thread."""
import contextlib, io, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "sn1.py")).read(); src = src[:src.index("RES = dict(frozen")]
g = {"__file__": os.path.join(HERE, "sn1.py"), "__name__": "sn1_ro"}; sys.argv = ["sn1.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, g["__file__"], "exec"), g)
REB = g["REB"]; sys.path.insert(0, os.path.join(REB, "RG1_native_n_regrade")); import rg1_lib as L
MSUN, PC, G, BS, CLS = g["MSUN"], g["PC"], g["G"], g["BS"], g["CLS"]; U = g["U"]
LMG = np.round(np.arange(4.5, 13.01, 0.1), 2); LSG = np.round(np.arange(0.8, 3.01, 0.05), 2); RES = {}
def Etable(Q):
    T = np.zeros((len(Q), len(LMG), len(LSG)))
    for i, q in enumerate(Q):
        for j, lm in enumerate(LMG):
            M = 10 ** lm * MSUN; R = (3 * M / (4 * math.pi * 200 * g["RHOC"])) ** (1 / 3); qq = dict(q, M200=M, R200=R)
            for k, ls in enumerate(LSG): T[i, j, k] = g["Eof"](qq, 10 ** ls, BS)
    return T
def bilin(T, lM, lS):
    x = np.clip((lM - LMG[0]) / 0.1, 0, len(LMG) - 1.001); y = np.clip((lS - LSG[0]) / 0.05, 0, len(LSG) - 1.001); i = x.astype(int); j = y.astype(int); u = x - i; v = y - j; n = np.arange(T.shape[0])
    return T[n, i, j] * (1 - u) * (1 - v) + T[n, i + 1, j] * u * (1 - v) + T[n, i, j + 1] * (1 - u) * v + T[n, i + 1, j + 1] * u * v
Qc = g["systems"]("canonical"); T = Etable(Qc); LSR = np.log10([max(L.S_nat(10 ** m) if m >= 6 else L.S_nat(1e6), 1e-3) for m in LMG])
for f in g["FEET"]:
    Q = g["systems"](f); idx = g["boot_setup"](Q); lm = np.array([q["lm"] for q in Q]); F = RES[f] = {}
    # check against sn1's E path at EM1's mass, Sigma 29.4
    E0 = bilin(T, np.log10([q["M200"] / MSUN for q in Q]), np.full(len(Q), math.log10(29.4))); Ed = np.array([g["Eof"](q, 29.4, BS) for q in Q]); F["K_interp_max"] = float(np.median(abs(E0 - Ed)))
    def mz(E): z = g["clsZ"](E, Q, idx); return max(abs(v[2]) for v in z.values()), z
    A = np.round(np.arange(6.0, 11.01, 0.1), 2); Bs = np.round(np.arange(-0.2, 1.61, 0.1), 2)
    flat = []; best = (9, None)
    for ls in LSG:
        for a in A:
            for b in Bs:
                m, _ = mz(bilin(T, a + b * (lm - 7), np.full(len(Q), ls)))
                if m < 2: flat.append((float(10 ** ls), float(a), float(b)))
                if m < best[0]: best = (m, (float(10 ** ls), float(a), float(b)))
    fl = np.array(flat) if flat else np.zeros((0, 3))
    F["flat"] = dict(n=len(flat), best_maxZ=best[0], best=best[1], S_range=[float(fl[:, 0].min()), float(fl[:, 0].max())] if flat else None, a_range=[float(fl[:, 1].min()), float(fl[:, 1].max())] if flat else None, b_range=[float(fl[:, 2].min()), float(fl[:, 2].max())] if flat else None)
    if flat:
        F["flat"]["lgM200_at_lmstar"] = {str(x): [float((fl[:, 1] + fl[:, 2] * (x - 7)).min()), float((fl[:, 1] + fl[:, 2] * (x - 7)).max())] for x in (4, 6, 8, 9)}
        by = {};
        for s in sorted(set(fl[:, 0])): by[f"{s:.1f}"] = int((fl[:, 0] == s).sum())
        F["flat"]["count_by_S"] = by
    # rule x k
    rule = {};
    for k in (1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0):
        n = 0; bst = (9, None)
        for a in A:
            for b in Bs:
                lM = a + b * (lm - 7); lS = np.interp(lM, LMG, LSR) + math.log10(k); m, _ = mz(bilin(T, lM, lS))
                n += m < 2
                if m < bst[0]: bst = (m, (float(a), float(b)))
        rule[str(k)] = dict(n=int(n), best_maxZ=bst[0], best=bst[1])
    F["rule_k"] = rule
    # EM1's own line in these coordinates
    a_, b_ = g["EM"]["a"], g["EM"]["b"]; F["EM1_line"] = dict(a=a_ + b_ * (7 - 10), b=b_)
    print(f, json.dumps(F, default=float)[:2600], flush=True)
json.dump(RES, open(os.path.join(HERE, "sn1_post_results.json"), "w"), indent=1, default=float)
