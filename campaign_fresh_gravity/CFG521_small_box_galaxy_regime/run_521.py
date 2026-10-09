#!/usr/bin/env python3
"""CFG521 launcher (FROZEN_CRITERIA.md), run detached (nohup): 256^3 seed 359 NSEED 256, 6 threads each, nice 10, two runs at a time.
Stages (argv, run in order):  k0   K0 engine identity: cfg521 vs cfg518 copy, L = 200, 128^3, census canonical (+ cfg521 S0 L = 200 128^3, reported)
  50a  S0 + DC-can (L = 50)      50b  DC-alt + MUTATE (L = 50)      50c  K1 (L = 50)
  25a/25b/25c  the same at L = 25 (fallback, only if L = 50 fails the f_ret achievement test)      100  S0 + DC-can (L = 100, reported)"""
import os, sys, subprocess, time, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg521_work"))
os.makedirs(WORK, exist_ok=True)
def start(name, sw="RES", foot="canonical", L=50.0, npg=256, mode="census", nocomp="0", th="6", engine=None, rmin=None):
    env = dict(os.environ, CFG521_THREADS=th, CFG521_NSEED="256", CFG521_FRET_MODE=mode, CFG521_NOCOMP=nocomp,
               CFG521_L=f"{L:g}", CFG521_RMIN=str(rmin if rmin is not None else 2 * L / 256))
    env.update(CFG518_THREADS=th, CFG518_NSEED="256", CFG518_FRET_MODE=mode, CFG518_NOCOMP=nocomp)
    return subprocess.Popen(["nice", "-n", "10", sys.executable, engine or os.path.join(HERE, "cfg521_pm.py"), sw, "FLAT", foot, str(npg), "0", "MIXA"],
                            stdout=open(os.path.join(WORK, f"cfg521_{name}.log"), "w"), stderr=subprocess.STDOUT, env=env)
def k0_ref():
    d = os.path.join(WORK, "k0_ref"); os.makedirs(d, exist_ok=True)
    s = open(os.path.join(HERE, "..", "CFG518_depletion_consistent_growth", "cfg518_pm.py")).read()
    old = 'os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg518_work"))'
    assert s.count(old) == 1
    open(os.path.join(d, "cfg518_pm_k0ref.py"), "w").write(s.replace(old, repr(d)))
    shutil.copy(os.path.join(WORK, "cfg361_delta_ta_table.json"), d)
    return os.path.join(d, "cfg518_pm_k0ref.py")
def box(L):
    return {f"{L}a": lambda: [(f"S0_L{L}", start(f"S0_L{L}", sw="S0", L=L)), (f"DCcan_L{L}", start(f"DCcan_L{L}", L=L))],
            f"{L}b": lambda: [(f"DCalt_L{L}", start(f"DCalt_L{L}", foot="alt", L=L)), (f"MUTATE_L{L}", start(f"MUTATE_L{L}", L=L, nocomp="1"))],
            f"{L}c": lambda: [(f"K1_L{L}", start(f"K1_L{L}", L=L, mode="one"))]}
STAGES = {"k0": lambda: [("K0_cfg521", start("K0_cfg521", L=200.0, npg=128, rmin=1.56)),
                         ("K0_cfg518ref", start("K0_cfg518ref", L=200.0, npg=128, rmin=1.56, engine=k0_ref()))],
          "k0s": lambda: [("S0_L200_N128", start("S0_L200_N128", sw="S0", L=200.0, npg=128, rmin=1.56))],
          "100": lambda: [("S0_L100", start("S0_L100", sw="S0", L=100.0)), ("DCcan_L100", start("DCcan_L100", L=100.0))]}
STAGES.update(box(50)); STAGES.update(box(25))
with open(os.path.join(WORK, "run_521_launcher.log"), "a") as lg:
    print("start", time.strftime("%Y-%m-%d %H:%M"), sys.argv[1:], file=lg, flush=True)
    for st in sys.argv[1:]:
        for n, p in STAGES[st]():
            print(st, n, "rc", p.wait(), time.strftime("%Y-%m-%d %H:%M"), file=lg, flush=True)
