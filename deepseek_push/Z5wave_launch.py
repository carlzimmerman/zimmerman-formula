#!/usr/bin/env python3
"""Z5-wave detached launcher (double-fork + start_new_session, the silent-death fix).
Lanes: LR2 (J09p general-p window Lean cert), VE2 (LOS-corrected discriminator
plane), OA1 (M-RISE exclusion design card). Exits after spawning (rc 0)."""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = [("LR2_lean_j09p.py", "LR2_j09p_window.out", "LR2_j09p_window.err"),
         ("VE2_los_corrected_plane.py", "VE2_los_corrected_plane.out", "VE2_los_corrected_plane.err"),
         ("OA1_mrise_design_card.py", "OA1_mrise_design_card.out", "OA1_mrise_design_card.err")]

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
print("Z5WAVE spawned:", ", ".join(s for s, _, _ in LANES))
