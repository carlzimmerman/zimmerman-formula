#!/usr/bin/env python3
import numpy as np, sys, time
sys.path.insert(0, '.')
import nb_engine as E

def relax(N, eps, t_end=250.0, seed=7, mu=0.3, R0=3.0):
    mp = mu/N
    pos, vel = E.make_ic_top_hat(N, R0, mu, rng=seed)
    t0=time.time()
    hist, snaps = E.run(pos, vel, mp, eps, 1.0, 0.5, t_end, dE_every=50.0,
                        snap_times=(t_end,), verbose=False, tag=f"N{N}", eta=0.05)
    wall=time.time()-t0
    E0 = hist["ke"][0]+hist["pe_pp"][0]+hist["pe_b"][0]
    E1 = hist["ke"][-1]+hist["pe_pp"][-1]+hist["pe_b"][-1]
    p, v = snaps[t_end]
    r = np.sqrt((p**2).sum(1))
    edges = np.logspace(np.log10(0.15), np.log10(8.0), 25)
    rho, _ = E.density_profile(p, mp, edges)
    rc = np.sqrt(edges[1:]*edges[:-1])
    slope, nfit = E.fit_slope(rc, rho, 0.3, 3.0)
    sig2, nsh = E.sigma_profile(p, v, edges)
    m2 = (rc>0.3)&(rc<3.0)&np.isfinite(sig2)
    s2 = np.mean(sig2[m2]) if m2.sum()>0 else np.nan
    return dict(N=N, eps=eps, wall=wall, steps=hist['nsteps'], dE=(E1-E0)/abs(E0),
                r50=np.median(r), r90=np.quantile(r,0.9), slope=slope, sig2=s2)

for N, eps in ((2000,0.2),(4000,0.2),(8000,0.15)):
    res = relax(N, eps)
    print(f"N={res['N']:5d} eps={res['eps']}: wall={res['wall']:.0f}s steps={res['steps']} "
          f"dE/E={res['dE']:+.1e} r50={res['r50']:.3f} r90={res['r90']:.3f} "
          f"slope={res['slope']:+.3f} sig2={res['sig2']:.4f}", flush=True)
