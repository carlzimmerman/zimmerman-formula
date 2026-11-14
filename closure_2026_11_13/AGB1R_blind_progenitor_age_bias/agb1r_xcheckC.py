"""AGB1R cross-check (not a frozen step) of the Part C fits nearest a threshold: the A = 1 fork on `full`
(dchi2_today 3.57, threshold 4). Re-runs the A = 1 best fit and the q0 = 0 fit from 8 extra seeded random starts and
compares with agb1r_C_full.json. Executes the model section of agb1r_partC.py unchanged (only its log path is swapped,
so the Part C log is not overwritten). Writes agb1r_xcheckC.json / .out."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "agb1r_partC.py")).read()
head = src.split("out = dict(mode=MODE)")[0]
old = 'logf = open(os.path.join(HERE, f"agb1r_C_{MODE}.out"), "w")'
assert old in head
head = head.replace(old, 'logf = open(os.path.join(HERE, "agb1r_xcheckC.out"), "w")')
sys.argv = ["agb1r_partC.py", "full"]
ns = {"__name__": "agb1r_partC_model", "__file__": os.path.join(HERE, "agb1r_partC.py")}
exec(compile(head, os.path.join(HERE, "agb1r_partC.py"), "exec"), ns)
fit, fmt, log, h_from_theta = ns["fit"], ns["fmt"], ns["log"], ns["h_from_theta"]
ref = json.load(open(os.path.join(HERE, "agb1r_C_full.json")))["forks"]["A1"]
rng = np.random.default_rng(20261114)
extra = []
for _ in range(8):
    w0 = rng.uniform(-1.0, 0.0); wa = rng.uniform(-2.8, 0.5)
    if w0 + wa >= 0: wa = -w0 - 0.2
    ob = 0.02223 + rng.normal(0, 3e-4); obc = 0.14208 + rng.normal(0, 3e-3)
    extra.append((h_from_theta(ob, obc, w0, wa), ob, obc, w0, wa))
b = fit(1.0, "free", extra=extra)
q = fit(1.0, "q0", extra=extra)
d = q["chi2"] - b["chi2"]
log(f"A = 1 fork, frozen starts + 8 random starts:\n  best  {fmt(b)}\n  q0=0  {fmt(q)}\n  dchi2_today {d:.4f}")
log(f"Part C run: best chi2 {ref['best']['chi2']:.4f}, q0=0 chi2 {ref['q0zero']['chi2']:.4f}, dchi2_today "
    f"{ref['dchi2_today']:.4f}")
json.dump(dict(best=b, q0zero=q, dchi2_today=d, run_best=ref["best"]["chi2"], run_q0=ref["q0zero"]["chi2"],
               run_dchi2_today=ref["dchi2_today"]), open(os.path.join(HERE, "agb1r_xcheckC.json"), "w"), indent=1,
          default=float)
