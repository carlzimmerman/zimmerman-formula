#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, '.')
import nb_engine as E
N, mu, R0, eps = 3000, 0.3, 3.0, 0.05
mp = mu/N
pos, vel = E.make_ic_top_hat(N, R0, mu, rng=7)
eps2 = eps*eps
acc = np.zeros_like(pos)
E.accel_numba(pos, acc, mp, eps2, 1.0)

def choose_dt(pos, eta=0.03):
    r2 = (pos*pos).sum(1) + eps2
    tau = np.sqrt(r2**1.5 / (1.0 + mp*N))
    return eta * tau.min()

dt = min(0.3, choose_dt(pos))
t = 0.0
ke0, pp0, pb0 = E.energy_numba(pos, vel, mp, eps, 1.0)
E0 = ke0+pp0+pb0
print(f"t=0 E0={E0:.4f} dt0={dt:.3e} rmin={np.sqrt((pos**2).sum(1)).min():.3f}")
for k in range(4000):
    vel += 0.5*dt*acc
    pos += dt*vel
    t += dt
    E.accel_numba(pos, acc, mp, eps2, 1.0)
    vel += 0.5*dt*acc
    dt = min(0.3, choose_dt(pos))
    if k % 200 == 0:
        ke,pp,pb = E.energy_numba(pos, vel, mp, eps, 1.0)
        r = np.sqrt((pos**2).sum(1))
        v2 = (vel**2).sum(1)
        imax = np.argmax(v2)
        print(f"t={t:7.3f} E={ke+pp+pb:9.4f} dE={(ke+pp+pb-E0)/abs(E0):+.2e} "
              f"dt={dt:.2e} r50={np.median(r):7.3f} rmin={r.min():.3f} "
              f"vmax={np.sqrt(v2.max()):7.3f} r@vmax={r[imax]:.3f}")
