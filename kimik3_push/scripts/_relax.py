#!/usr/bin/env python3
import numpy as np, sys, time
sys.path.insert(0, '.')
import nb_engine as E

N, mu, R0, eps = 3000, 0.3, 3.0, 0.2   # epsb defaults to eps
mp = mu/N
pos, vel = E.make_ic_top_hat(N, R0, mu, rng=7)
t0=time.time()
hist, snaps = E.run(pos, vel, mp, eps, 1.0, 0.5, 400.0, dE_every=20.0,
                    snap_times=(100.0, 200.0, 400.0), verbose=False, tag="col", eta=0.05)
t1=time.time()
E0 = hist["ke"][0]+hist["pe_pp"][0]+hist["pe_b"][0]
E1 = hist["ke"][-1]+hist["pe_pp"][-1]+hist["pe_b"][-1]
print(f"wall={t1-t0:.0f}s steps={hist['nsteps']} dE/E={(E1-E0)/abs(E0):.2e}")
for ts in (100.0, 200.0, 400.0):
    if ts in snaps:
        p, v = snaps[ts]
        r = np.sqrt((p**2).sum(1))
        edges = np.logspace(np.log10(0.15), np.log10(8.0), 25)
        rho, _ = E.density_profile(p, mp, edges)
        rc = np.sqrt(edges[1:]*edges[:-1])
        slope, nfit = E.fit_slope(rc, rho, 0.3, 3.0)
        sig2, nsh = E.sigma_profile(p, v, edges)
        m2 = (rc>0.3)&(rc<3.0)&np.isfinite(sig2)
        s2 = np.mean(sig2[m2]) if m2.sum()>0 else np.nan
        print(f"t={ts:6.0f}: r50={np.median(r):7.3f} r90={np.quantile(r,0.9):7.3f} "
              f"slope(0.3-3)={slope:+.3f} (n={nfit})  <sig2_3d>={s2:.4f}")
print("r50(t) every ~40:", np.array2string(hist['rmed'][::2], precision=2))
