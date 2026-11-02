#!/usr/bin/env python3
"""AN1 post-result, reported only (A2): held start, smallest cell compression reached over 14 Gyr, excluding the outer 5 % of cells;
N 1200, 2400; kick 1 % and 10 %. Run: python3 an1_held2.py checks"""
import json, os, sys, time
sys.argv = [sys.argv[0], "x"]
from an1 import *
out = open(os.path.join(HERE, "an1_held2.jsonl"), "w")
for key in ("1e12", "1e15"):
    for mu in (0.1, 1.0):
        for foot in AF:
            for N, kick in ((1200, 0.01), (2400, 0.01), (1200, 0.1)):
                if foot == "alt" and (N, kick) != (1200, 0.01):
                    continue
                S = static_branch(key, mu, foot, N=N)
                if S is None:
                    continue
                dm = np.diff(np.concatenate([[0.0], S["Md"]]))
                r = S["r"]
                neg = np.where(dm <= 0)[0]
                if len(neg):
                    r = r[: neg[0] + 1]
                    dm = dm[: neg[0]]
                Vc = np.sqrt(np.maximum(np.interp(r, S["x"], S["E"]) * r, 0))
                v = kick * Vc * np.sin(np.pi * r / r[-1])
                R = Run(r, v, dm, S["a0"], S["mu"], Mb_fn=S["MB"], uo=float(np.interp(r[-1], S["x"], S["h"])))
                R.u = np.interp(0.5 * (r[1:] + r[:-1]), S["x"], S["h"])
                R.pinf[-1] = True
                q0 = np.diff(r)
                R.forces()
                n95 = int(0.95 * len(dm))
                tmax = 14 / TU
                cmin = 1.0
                t0w = time.time()
                res = "END"
                tf = None
                while R.t < tmax - 1e-12 and time.time() - t0w < 400:
                    R.step(tmax)
                    C = np.diff(R.r) / q0
                    if C[:n95].min() < cmin:
                        cmin = float(C[:n95].min())
                    if cmin < 1e-2 or getattr(R, "crossed", False):
                        res = "INNER FOLD"
                        tf = R.t * TU
                        break
                    if C.min() < 1e-3:
                        res = "OUTER WALL CELL CLOSES"
                        tf = R.t * TU
                        break
                else:
                    if R.t < tmax - 1e-12:
                        res = "BUDGET"
                d = dict(key=key, mu=mu, foot=foot, N=N, kick=kick, res=res, t_Gyr=R.t * TU, t_event_Gyr=tf, cmin=cmin, steps=R.nstep, Rout=float(r[-1]))
                print(d, flush=True)
                out.write(json.dumps(d) + "\n")
                out.flush()
