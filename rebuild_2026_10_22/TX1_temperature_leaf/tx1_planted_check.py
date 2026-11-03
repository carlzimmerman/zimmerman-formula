#!/usr/bin/env python3
"""TX1 planted recovery from the search's own output: any harvested form with residual rms < 1e-6 on train X-COP and train SPARC, holdouts G3, G5 LINE. python3 -I tx1_planted_check.py ARM LEVEL [FOOT]. kappa = 1/2 FITTED; not theory closed."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
arm, lev = sys.argv[1:3]; foot = sys.argv[3] if len(sys.argv) > 3 else "canonical"; a0 = A0S[foot]; XT = xrows(a0, 0); XH = xrows(a0, 1); ST = sparc(1, a0); best = []
J = json.load(open(os.path.join(LANE, f"tx1_train_{lev}_{foot}_{arm}.json"))); rows = {r["F"]: r for r in J["T"] + J["train_pass"]}; P_ = PLANTS[arm]
for f in rows:
    a = np.log10(ev(P_, XT) / ev(f, XT)); b = np.log10(ev(P_, ST) / ev(f, ST)); c = np.log10(ev(P_, XH) / ev(f, XH)); best.append((float(np.sqrt((a * a).mean())), float(np.sqrt((b * b).mean())), float(np.sqrt((c * c).mean())), f))
best.sort(key=lambda t: max(t[0], t[1])); t = best[0]; ok = max(t[0], t[1], t[2]) < 1e-6; print(f"[{'PASS' if ok else 'FAIL'}] {arm} {lev} {foot}: plant {P_}; closest of {len(best)} forms: train X {t[0]:.2e} SPARC {t[1]:.2e} holdout X {t[2]:.2e}: {t[3][:100]}"); sys.exit(0 if ok else 1)
