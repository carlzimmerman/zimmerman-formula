"""SRH1R post hoc reading (after unblinding; reported, never graded): a directed outer/inner statistic on my own model,
to see whether the difference from SRH1's G4 is the statistic or the model.  k is fitted on the inner bins 7-12 (weighted
by the jackknife errors), refitted in every jackknife replicate; A_out = amplitude of data against model on bins 0-3.
Usage: python3 -I srh1r_posthoc.py <work dir>.  kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, runpy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "srh1r_grade.py")).read(); G = {"__name__": "lib", "__file__": os.path.join(HERE, "srh1r_grade.py")}
sys.argv = [sys.argv[0], sys.argv[1]]; exec(compile(src[:src.index("RES = dict(lane=")], "srh1r_grade.py", "exec"), G)
m, L, model, Stack, KF, NP, SAMP, typ = (G[k] for k in ("m", "L", "model", "Stack", "KF", "NP", "SAMP", "typ"))
from scipy.optimize import brentq
OUTB, INB = np.arange(0, 4), np.arange(7, 13); OUT = []; RES = {}
def P(*a):
    s = " ".join(str(v) for v in a); print(s, flush=True); OUT.append(s)
def amp(D, M, s, b): return float((D[b] * M[b] / s[b] ** 2).sum() / (M[b] ** 2 / s[b] ** 2).sum())
def read(S):
    s = np.sqrt((NP - 1) / NP * ((S.Dj - S.Dj.mean(0)) ** 2).sum(0))
    def one(D, Mfun):
        k = brentq(lambda k: amp(D, Mfun(k), s, INB) - 1.0, 0.3, 12.0); return amp(D, Mfun(k), s, OUTB), k
    A, k = one(S.D, lambda k: S.M(min(max(k, 0.5), 8.0))[0]); Aj = np.array([one(S.Dj[i], lambda k, i=i: S.M(min(max(k, 0.5), 8.0))[1][i])[0] for i in range(NP)])
    sig = math.sqrt((NP - 1) / NP * ((Aj - Aj.mean()) ** 2).sum()); return A, sig, k
for foot in m.FOOTS:
    for case in ("f0.40", "f0.50", "f0.70", "ref", "one1"):
        own, nb, nul, _ = model(foot, case); row = {}
        for sn in ("all", "late", "early"):
            A, sig, k = read(Stack(L["F1.6_tieR"] & SAMP[sn], own + nb)); row[sn] = dict(A_out=A, sigma=sig, z=(A - 1) / sig, k_inner=k)
        RES[f"{foot}_{case}"] = row
        P(f"{foot} {case}: " + "  ".join(f"{sn} A_out {v['A_out']:.3f} +- {v['sigma']:.3f} (z {v['z']:+.2f}, k {v['k_inner']:.3f})" for sn, v in row.items()))
json.dump(dict(lane="SRH1R", post_hoc=True, readings=RES, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, "srh1r_posthoc.json"), "w"), indent=1)
open(os.path.join(HERE, "srh1r_posthoc.out"), "w").write("\n".join(OUT) + "\n")
