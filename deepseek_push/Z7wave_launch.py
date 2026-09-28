#!/usr/bin/env python3
"""Z7-wave detached launcher (double-fork + start_new_session, Z6 pattern).
Lanes: MC2 (c0 higher power), LR5 (E[D^2] bound Lean leg). LR4 runs after the
conductor probe phase (separate spawn). Exits after spawning (rc 0)."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = [("MC2_c0_highpower.py", "MC2_c0_highpower.out", "MC2_c0_highpower.err"),
         ("LR5_ed2_bound.py", "LR5_ed2_bound.out", "LR5_ed2_bound.err")]

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
print("Z7WAVE spawned:", ", ".join(s for s, _, _ in LANES))
