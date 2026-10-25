X48 smoke evidence (10-25, engineering only, no production number):
- ng 16, M 1e14 seed 1: uninterrupted 1069 steps in 31 s; SIGTERM at step 252 -> exit 75 + checkpoint; --resume -> exit 0, final x, v bit-identical; second --resume -> exit 0 at once (idempotent).
- max-steps bug found (stub wrote done.json); fixed: unfinished run checkpoints and exits 3; max-steps 50 + resume vs uninterrupted (M 1e13 seed 2, ng 16): bit-identical.
- cost at ng 38 (N 12149): ~2.6 s/step, peak footprint 0.47 GB; ng 48 (N 24405): ~16 s/step, 0.82 GB (10-step timing runs).
- constraints c1, c2 met to ~1e-16; momentum drift ~1e-16; analysis K3 recovers synthetic NFW c = 4 as 3.84, MUTATE c = 8 fails K3.
