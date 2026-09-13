#!/usr/bin/env python3
import numpy as np, sys, time
sys.path.insert(0, '.')
import nb_engine as E
# test-particle collapse: mu -> tiny so particle-particle forces vanish,
# only the central point mass acts.  Isolates the integrator.
for mu in (1e-6, 0.3):
    N, R0, eps = 3000, 3.0, 0.3
    mp = mu/N
    pos, vel = E.make_ic_top_hat(N, R0, mu, rng=7)
    t0=time.time()
    hist, snaps = E.run(pos, vel, mp, eps, 1.0, 0.3, 200.0, dE_every=20.0,
                        snap_times=(200.0,), verbose=False, tag=f"mu{mu}", eta=0.05)
    E0 = hist["ke"][0]+hist["pe_pp"][0]+hist["pe_b"][0]
    E1 = hist["ke"][-1]+hist["pe_pp"][-1]+hist["pe_b"][-1]
    rf = np.sqrt((snaps[200.0][0]**2).sum(1))
    print(f"mu={mu}: wall={time.time()-t0:.0f}s steps={hist['nsteps']} "
          f"dE/E={(E1-E0)/abs(E0):.2e}  r50={np.median(rf):.3f} r90={np.quantile(rf,0.9):.3f}")
