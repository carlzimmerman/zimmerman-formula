#!/usr/bin/env python3
"""Z2-wave detached launcher (V03c/Zwave silent-death fix: double-fork + start_new_session,
grandchildren orphaned to launchd, cannot be killed by session teardown).
Lanes: A2 (atlas sufficiency), QF2 (Q noise-floor gate), OB2 (JWST block recipe).
Light single-process lanes per the load gate (box load 45.9/16 at spawn). Exits after
spawning (rc 0)."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = [("A2_atlas_sufficiency.py", "A2_atlas_sufficiency.out", "A2_atlas_sufficiency.err"),
         ("QF2_q_noise_floor.py", "QF2_q_noise_floor.out", "QF2_q_noise_floor.err"),
         ("OB2_jwst_block_recipe.py", "OB2_jwst_block_recipe.out", "OB2_jwst_block_recipe.err")]

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
print("Z2WAVE spawned:", ", ".join(s for s, _, _ in LANES))
