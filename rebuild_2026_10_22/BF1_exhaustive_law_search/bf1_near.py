#!/usr/bin/env python3
"""BF1 L4, interim: closest prefilter hits on gate 2, no verdict. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
sys.argv = [sys.argv[0], "real"]
import numpy as np
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bf1.py")).read().split('if __name__ == "__main__"')[0])
W = os.path.join(HERE, "chunks", "real_L4"); names = json.load(open(os.path.join(W, "names.json"))); R = []
RT = np.sqrt((np.log10(ST[:, 1] / law(ST[:, 0], A0)) ** 2).mean())
for l in open(os.path.join(W, "hits.jsonl")):
    i, o, j, w = json.loads(l); s = f"({names[i]}{o}{names[j]})"
    try: d = full(s, w, ST); dx = full(s, w, XT); dh = full(s, w, SH); dxh = full(s, w, XH)
    except Exception: continue
    if not (np.all(np.isfinite(d)) and np.all(np.isfinite(dh))): continue
    R.append((float(np.sqrt((d*d).mean())), float(np.median(d)), float(dx.mean()), float(np.sqrt((dx*dx).mean())), float(dxh.mean()), float(np.sqrt((dxh*dxh).mean())), float(np.sqrt((dh*dh).mean())), w, s))
R.sort(); print(f"hits scored {len(R)}; law train rms {RT:.4f}, gate 2 line {1.05*RT:.4f}")
for r in R[:8]: print(f"rms {r[0]:.3f} med {r[1]:+.3f} X {r[2]:+.3f},{r[3]:.3f} | Xhold {r[4]:+.3f},{r[5]:.3f} Shold {r[6]:.3f} W{r[7]} {r[8][:80]}")
print("share using y*f-like g_gas:", sum("f" in r[8] and "y" in r[8] for r in R), "of", len(R)); print("X-COP train passes at rms <= 0.20:", sum(r[0] <= .20 for r in R))
