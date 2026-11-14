#!/usr/bin/env python3
"""RRL2 POST HOC (after the graded run; changes no word): does the own-cells RR Lyrae sample reject the full-sky
broken law (5.293 / 3.934 / 39.0)? Runs rrl2.py's source up to its own-cells fit (output tag _posthoc), then compares
-ln L of the own-cells stars at the full-sky shape, at the own best broken law and at the own best single law, and
calibrates the full-sky-shape deficit with 100 mocks drawn from the full-sky law on the own cells.
Usage: same three arguments as rrl2.py. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys
os.environ["RRL2_TAG"] = "_posthoc"
HERE0 = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE0, "rrl2.py")).read().split("# ================================================================== primary and brackets")[0]
g = {"__file__": os.path.join(HERE0, "rrl2.py"), "__name__": "rrl2_head"}
exec(compile(src, "rrl2.py", "exec"), g)
np, say, sec, nll, fit_both, mock = g["np"], g["say"], g["sec"], g["nll"], g["fit_both"], g["mock"]
X, W, akF, OWNC = g["OWNFIT"]["X"], g["Wo"], g["akF"], g["OWNC"]
sec("POST HOC: own-cells stars against the full-sky law (shape fixed, normalisation free)")
nF = nll(akF, X, W); nB = g["bO"]["nll"]; nS = g["sO"]["nll"]
d_obs = 2 * (nF - nB)
say(f"  -lnL: full-sky shape {nF:.2f}; own broken {nB:.2f}; own single {nS:.2f}; 2 dlnL (own broken - full-sky shape) {d_obs:.2f}; (own single - full-sky shape) {2 * (nF - nS):.2f}")
rng = np.random.default_rng(777001); D = []
for t in range(100):
    Xm = mock(OWNC, 1.0, akF, len(X), rng); s, b = fit_both(Xm, W, OWNC["rbr"]); D.append(2 * (nll(akF, Xm, W) - b["nll"]))
D = np.array(D)
say(f"  mocks from the full-sky law on own cells: 2 dlnL median {np.median(D):.2f}, 95th {np.percentile(D, 95):.2f}, 99th {np.percentile(D, 99):.2f}; fraction >= observed {np.mean(D >= d_obs):.3f}")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
