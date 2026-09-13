#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, '.')
import nb_engine as E

def collapse_dE(N, mu, eps, R0=3.0, eta=0.05, t_end=2.0, seed=7):
    mp = mu/N
    pos, vel = E.make_ic_top_hat(N, R0, mu, rng=seed)
    eps2 = eps*eps; mb = 1.0
    acc = np.zeros_like(pos)
    E.accel_numba(pos, acc, mp, eps2, mb)
    def choose_dt(pos):
        r2 = (pos*pos).sum(1) + eps2
        return min(0.3, eta*np.sqrt((r2**1.5).min()/(mb+mu)))
    dt = choose_dt(pos)
    t=0.0
    ke0,pp0,pb0 = E.energy_numba(pos, vel, mp, eps, mb)
    E0 = ke0+pp0+pb0
    dEmax = 0.0
    while t < t_end:
        vel += 0.5*dt*acc
        pos += dt*vel
        t += dt
        E.accel_numba(pos, acc, mp, eps2, mb)
        vel += 0.5*dt*acc
        dt = choose_dt(pos)
        ke,pp,pb = E.energy_numba(pos, vel, mp, eps, mb)
        dEmax = max(dEmax, abs((ke+pp+pb-E0)/abs(E0)))
    return E0, dEmax

print("=== scaling of energy error (t_end=2, one collapse) ===")
print("N      mu     eps    E0        max|dE/E|")
for N in (1000, 2000, 4000):
    for eps in (0.3, 0.5):
        E0, dE = collapse_dE(N, 0.3, eps)
        print(f"{N:5d}  0.3   {eps:.1f}  {E0:8.4f}  {dE:.2e}")
print("--- test-particle limit (mu=1e-4, isolates central field) ---")
for N in (1000, 2000):
    E0, dE = collapse_dE(N, 1e-4, 0.3)
    print(f"{N:5d}  1e-4  0.3   {E0:8.6f}  {dE:.2e}")
