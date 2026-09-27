#!/usr/bin/env python3
"""Z6-wave detached launcher (double-fork + start_new_session, the silent-death fix).
Lanes: LR3 (moment values Lean cert), LR3b (reduction lemma lane), M05B (r4-table
audit), MC1 (c0(q) linearity). Exits after spawning (rc 0)."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = [("LR3_m05_moments_lean.py", "LR3_m05_moments.out", "LR3_m05_moments.err"),
         ("LR3b_reduction_lean.py", "LR3b_reduction.out", "LR3b_reduction.err"),
         ("M05B_r4_bug_audit.py", "M05B_r4_bug_audit.out", "M05B_r4_bug_audit.err"),
         ("MC1_c0_linearity.py", "MC1_c0_linearity.out", "MC1_c0_linearity.err")]

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
print("Z6WAVE spawned:", ", ".join(s for s, _, _ in LANES))
