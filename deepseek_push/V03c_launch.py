#!/usr/bin/env python3
"""V03c relauncher (conductor, 2026-09-25 ~22:50 EDT).

V03b/V03c both died silently: they were children of the spawning
session and were killed at that session's teardown. This launcher
double-forks + setsid so the lane is orphaned to launchd and survives
any session teardown. Output appends to deepseek_push/V03b_trio_fix.out
(append-only house rule); results land in deepseek_push/V03b_trio_results.json.
No physics changes: same locked grid, falsifiers V03_PRE.txt verbatim.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANE = os.path.join(ROOT, "deepseek_push", "V03b_trio_fix_run.py")
OUT = os.path.join(ROOT, "deepseek_push", "V03b_trio_fix.out")

pid = os.fork()
if pid > 0:
    print("PARENT_OK grandchild", pid)
    os._exit(0)
os.setsid()
pid2 = os.fork()
if pid2 > 0:
    os._exit(0)
out = os.open(OUT, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
os.dup2(out, 1)
os.dup2(out, 2)
os.chdir(ROOT)
os.execv(sys.executable, [sys.executable, "-u", LANE])
