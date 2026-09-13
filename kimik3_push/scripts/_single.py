#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, '.')
import nb_engine as E
# single particle, mass 1e-4, released at rest at R0=3 in central field mb=1.
# eps irrelevant for central term.  Exact: radial plunge, E=-1/3*mp.
mp = 1e-4; eps = 0.3; mb = 1.0; eps2 = eps*eps
pos = np.array([[3.0,0,0]]); vel = np.array([[0.0,0,0]])
acc = np.zeros_like(pos)
E.accel_numba(pos, acc, mp, eps2, mb)
eta = 0.05
def choose_dt(pos):
    r2 = (pos*pos).sum(1) + eps2
    return min(0.3, eta*np.sqrt((r2**1.5).min()/(mb)))
dt = choose_dt(pos)
t=0.0
ke0,pp0,pb0 = E.energy_numba(pos, vel, mp, eps, mb)
E0 = ke0+pp0+pb0
print(f"E0={E0:.6e}  dt0={dt:.3e}")
for k in range(2000):
    vel += 0.5*dt*acc
    pos += dt*vel
    t += dt
    E.accel_numba(pos, acc, mp, eps2, mb)
    vel += 0.5*dt*acc
    dt = choose_dt(pos)
    ke,pp,pb = E.energy_numba(pos, vel, mp, eps, mb)
    if k % 100 == 0 or abs(pos[0,0])<0.6:
        x = float(pos[0,0]); vx = float(vel[0,0])
        print(f"k={k:4d} t={t:7.3f} x={x:+9.4f} vx={vx:+10.4f} dt={dt:.2e} "
              f"E/mp={((ke+pp+pb)/mp):+.5f} (exact {-1/3:.5f})")
    if abs(pos[0,0]) > 5: 
        print("ESCAPED"); break
