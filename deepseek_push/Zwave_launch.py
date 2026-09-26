#!/usr/bin/env python3
"""Z-wave detached launcher (the V03c silent-death fix: double-fork + start_new_session,
grandchildren orphaned to launchd, cannot be killed by session teardown).
Lanes: QF1 (Q-functional closure), OB1 (JWST observation design), MR1 (corrected moment discipline).
Output appended to each lane's .out / .err. Launcher exits after spawning (rc 0)."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = [("QF1_q_closure.py", "QF1_q_closure.out", "QF1_q_closure.err"),
         ("OB1_jwst_design.py", "OB1_jwst_design.out", "OB1_jwst_design.err"),
         ("MR1_corrected_discipline.py", "MR1_corrected_discipline.out", "MR1_corrected_discipline.err")]

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
print("ZWAVE spawned:", ", ".join(s for s, _, _ in LANES))
