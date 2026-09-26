#!/usr/bin/env python3
"""Z3-wave detached launcher (V03c/Z2wave silent-death fix: double-fork + start_new_session,
grandchildren orphaned to launchd, cannot be killed by session teardown).
Lanes: QF3 (Q SE-shrink), A3 (U-band rule), M04b (J10-I(z) at OB1 recipe).
Exits after spawning (rc 0)."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = [("QF3_q_se_shrink.py", "QF3_q_se_shrink.out", "QF3_q_se_shrink.err"),
         ("A3_u_band_rule.py", "A3_u_band_rule.out", "A3_u_band_rule.err"),
         ("M04b_j10z_at_ob1.py", "M04b_j10z_at_ob1.out", "M04b_j10z_at_ob1.err")]

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
print("Z3WAVE spawned:", ", ".join(s for s, _, _ in LANES))
