#!/usr/bin/env python3
import numpy as np, time, sys
sys.path.insert(0, '.')
import nb_engine as E
N, mu, R0, eps = 4000, 0.3, 3.0, 0.05
mp = mu/N
pos, vel = E.make_ic_top_hat(N, R0, mu, rng=7)
t0 = time.time()
hist, snaps = E.run(pos, vel, mp, eps, 1.0, 0.3, 20.0, dE_every=1.0,
                    snap_times=(20.0,), verbose=True, tag="col", eta=0.03)
t1 = time.time()
E0 = hist["ke"][0]+hist["pe_pp"][0]+hist["pe_b"][0]
E1 = hist["ke"][-1]+hist["pe_pp"][-1]+hist["pe_b"][-1]
rf = np.sqrt((snaps[20.0][0]**2).sum(1))
print(f"COLLAPSE 4k t=20: wall={t1-t0:.0f}s steps={hist['nsteps']} dE/E={(E1-E0)/abs(E0):.2e}")
print("  r50(t):", np.array2string(hist['rmed'][::2], precision=2))
print("  dt(t):", np.array2string(hist['dt'][::2], precision=2))
print(f"  final r50={np.median(rf):.3f} r90={np.quantile(rf,0.9):.3f}")
