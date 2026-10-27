#!/usr/bin/env python3
"""X55 step 0, item 3 (FROZEN_CRITERIA.md section 4): rerun EM1's committed em1_emergent.py UNCHANGED in a scratch copy
(outputs land only in the scratch copy, removed afterwards) and compare its R1 relation with the committed (11.18, 0.90).

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x55_step0_em1.py   -> x55_step0_em1.out, x55_step0_em1_results.json
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, shutil, subprocess, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.dirname(HERE)
REPO = os.path.dirname(REB)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

T0 = time.time()
tmp = tempfile.mkdtemp(prefix="x55_step0_")
os.makedirs(os.path.join(tmp, "rebuild_2026_10_22", "EM1_emergent_dust_law"))
os.symlink(os.path.join(REPO, "real_research"), os.path.join(tmp, "real_research"))
os.symlink(os.path.join(REPO, "campaign_fresh_gravity"), os.path.join(tmp, "campaign_fresh_gravity"))
os.symlink(os.path.join(REB, "F3_growth_audit"), os.path.join(tmp, "rebuild_2026_10_22", "F3_growth_audit"))
d = os.path.join(tmp, "rebuild_2026_10_22", "EM1_emergent_dust_law")
shutil.copy2(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"), d)
env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
r = subprocess.run([sys.executable, "em1_emergent.py"], cwd=d, env=env, capture_output=True, text=True)
P(f"  ran EM1_emergent_dust_law/em1_emergent.py (scratch copy): exit {r.returncode} [{time.time() - T0:.0f} s]")
if r.returncode != 0:
    P(r.stderr[-2000:])
J = json.load(open(os.path.join(d, "em1_emergent_results.json")))
REF = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
ROWS = {}
ok = True
for t, (a0, b0) in (("A_c2b_refit", (11.18, 0.90)), ("B_cfg886_bg", (11.20, 0.90))):
    r1 = J["rows"][t]["R1"]; rms0 = REF["rows"][t]["R1"]["rms"]
    p = abs(r1["a"] - a0) < 1e-9 and abs(r1["b"] - b0) < 1e-9 and abs(r1["rms"] - rms0) < 1e-4
    ok &= p
    ROWS[t] = dict(a=r1["a"], b=r1["b"], rms=r1["rms"], frozen=dict(a=a0, b=b0, rms=rms0), pass_=p)
    P(f"  EM1 R1 [{t}]: a {r1['a']:.2f} b {r1['b']:.2f} rms {r1['rms']:.5f}  (committed {a0:.2f} / {b0:.2f} / {rms0:.5f}): {'PASS' if p else 'FAIL'}")
P(f"STEP 0 item 3 (EM1): {'PASS' if ok else 'FAIL'}   [{time.time() - T0:.0f} s]")
shutil.rmtree(tmp, ignore_errors=True)
json.dump(dict(lane="X55 step 0 item 3", rows=ROWS, pass_=bool(ok)), open(os.path.join(HERE, "x55_step0_em1_results.json"), "w"), indent=1)
open(os.path.join(HERE, "x55_step0_em1.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok else 1)
