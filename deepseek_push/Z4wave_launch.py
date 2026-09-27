#!/usr/bin/env python3
"""Z4-wave detached launcher (V03b/V03c/Z2/Z3 silent-death fix: double-fork +
start_new_session, grandchildren orphaned to launchd, cannot be killed by session
teardown). Lanes: QF4 (Q-closure finer-tau0 rerun), VE1 (LOS-frame window
correction), LR1 (Lean J09 window certificate). Exits after spawning (rc 0)."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = [("QF4_q_finer_tau0.py", "QF4_q_finer_tau0.out", "QF4_q_finer_tau0.err"),
         ("VE1_los_window.py", "VE1_los_window.out", "VE1_los_window.err"),
         ("LR1_lean_j09.py", "LR1_j09_window.out", "LR1_j09_window.err")]

def spawn_detached(script, out, err):
    def grandchild():
        os.setsid()
        def child2():
            os.setsid()
            with open(os.path.join(HERE, out), "ab", 0) as fo, open(os.path.join(HERE, err), "ab", 0) as fe:
                p = subprocess.Popen([sys.executable, os.path.join(HERE, script)],
                                     stdout=fo, stderr=fe, cwd=HERE, start_new_session=True)
                p.wait()
                os._exit(0)
        pid = os.fork()
        if pid == 0:
            child2()
        os._exit(0)
    pid = os.fork()
    if pid == 0:
        grandchild()
    os.waitpid(pid, 0)

for s, o, e in LANES:
    spawn_detached(s, o, e)
print("Z4WAVE spawned:", ", ".join(s for s, _, _ in LANES))
