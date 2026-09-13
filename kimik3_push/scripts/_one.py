#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, '.')
import nb_engine as E
# REAL collapse, N=2000, mu=0.3, eps=0.3 -- track the FIRST energy jump
N, mu, R0, eps = 2000, 0.3, 3.0, 0.3
mp = mu/N
pos, vel = E.make_ic_top_hat(N, R0, mu, rng=7)
eps2 = eps*eps; mb = 1.0
acc = np.zeros_like(pos)
E.accel_numba(pos, acc, mp, eps2, mb)
eta = 0.05
def choose_dt(pos):
    r2 = (pos*pos).sum(1) + eps2
    return min(0.3, eta*np.sqrt((r2**1.5).min()/(mb+mu)))
dt = choose_dt(pos)
t=0.0
ke0,pp0,pb0 = E.energy_numba(pos, vel, mp, eps, mb)
E0 = ke0+pp0+pb0
print(f"E0={E0:.4f} dt0={dt:.3e}")
lastE = E0
for k in range(30000):
    vel += 0.5*dt*acc
    pos += dt*vel
    t += dt
    E.accel_numba(pos, acc, mp, eps2, mb)
    vel += 0.5*dt*acc
    dt = choose_dt(pos)
    if k % 100 == 0:
        ke,pp,pb = E.energy_numba(pos, vel, mp, eps, mb)
        Et = ke+pp+pb
        r = np.sqrt((pos**2).sum(1))
        v2 = (vel**2).sum(1)
        i = int(np.argmax(v2))
        jump = (Et-lastE)/abs(E0)
        print(f"k={k:5d} t={t:7.3f} E={Et:10.4f} jump/step100={jump:+.2e} "
              f"dt={dt:.2e} rmin={r.min():.4f} vmax={np.sqrt(v2.max()):8.3f} r@vmax={r[i]:.4f}")
        if abs(jump) > 0.1:
            print(f"  --> BIG JUMP. particle {i}: r={r[i]:.4f} v={np.sqrt(v2[i]):.3f} "
                  f"(KE={0.5*mp*v2[i]:.3f}), escape v at r: {np.sqrt(2*mb/r[i]):.3f}")
            break
        lastE = Et
