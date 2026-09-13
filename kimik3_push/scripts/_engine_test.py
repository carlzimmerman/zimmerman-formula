#!/usr/bin/env python3
"""Engine validation tests (K001 internal)."""
import numpy as np, time, sys
sys.path.insert(0, '.')
import nb_engine as E

# TEST A: e=0.9 Kepler orbit (pericentre 0.1, a=1)
pos = np.array([[1.9, 0, 0.]])
vel = np.array([[0, np.sqrt(1*(2/1.9-1/1.0)), 0]])
mp = 1e-12
hist, snaps = E.run(pos, vel, mp, 1e-6, 1.0, 1.0, 6*np.pi, dE_every=2.0,
                    snap_times=(6*np.pi,), verbose=False, tag="kep", eta=0.03)
E0 = hist["ke"][0]+hist["pe_pp"][0]+hist["pe_b"][0]
E1 = hist["ke"][-1]+hist["pe_pp"][-1]+hist["pe_b"][-1]
r = np.sqrt((snaps[6*np.pi][0]**2).sum(1))
print(f"KEPLER e=0.9: steps={hist['nsteps']}  dE/E={(E1-E0)/abs(E0):.2e}  r(3P)={r[0]:.4f} (expect 1.9)")

# TEST B: cold collapse N=4k, t=50
N, mu, R0, eps = 4000, 0.3, 3.0, 0.05
mp = mu/N
pos, vel = E.make_ic_top_hat(N, R0, mu, rng=7)
t0 = time.time()
hist, snaps = E.run(pos, vel, mp, eps, 1.0, 0.3, 50.0, dE_every=2.0,
                    snap_times=(50.0,), verbose=False, tag="col", eta=0.03)
t1 = time.time()
E0 = hist["ke"][0]+hist["pe_pp"][0]+hist["pe_b"][0]
E1 = hist["ke"][-1]+hist["pe_pp"][-1]+hist["pe_b"][-1]
rf = np.sqrt((snaps[50.0][0]**2).sum(1))
print(f"COLLAPSE 4k: wall={t1-t0:.0f}s steps={hist['nsteps']} dE/E={(E1-E0)/abs(E0):.2e}")
print("  r50(t):", np.array2string(hist['rmed'][::5], precision=2))
print(f"  final r50={np.median(rf):.3f} r90={np.quantile(rf,0.9):.3f}")
