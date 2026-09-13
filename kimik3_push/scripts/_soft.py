#!/usr/bin/env python3
import numpy as np, sys, time
sys.path.insert(0, '.')
import importlib
import nb_engine as E

# monkeypatch: soften the central point mass with eps_b
def make_soft(eps_b):
    from numba import njit, prange
    @njit(parallel=True, fastmath=True)
    def accel(pos, acc, mp, eps2, mb):
        n = pos.shape[0]
        for i in prange(n):
            xi=pos[i,0]; yi=pos[i,1]; zi=pos[i,2]
            ax=ay=az=0.0
            for j in range(n):
                if j==i: continue
                dx=xi-pos[j,0]; dy=yi-pos[j,1]; dz=zi-pos[j,2]
                r2=dx*dx+dy*dy+dz*dz+eps2
                inv=1.0/(r2*np.sqrt(r2)); w=mp*inv
                ax-=w*dx; ay-=w*dy; az-=w*dz
            r2b=xi*xi+yi*yi+zi*zi+eps_b*eps_b
            invb=1.0/(r2b*np.sqrt(r2b))
            ax-=mb*xi*invb; ay-=mb*yi*invb; az-=mb*zi*invb
            acc[i,0]=ax; acc[i,1]=ay; acc[i,2]=az
    @njit(parallel=True, fastmath=True)
    def energy(pos, vel, mp, eps, mb):
        n=pos.shape[0]; ke=pp=pb=0.0
        for i in prange(n):
            xi=pos[i,0]; yi=pos[i,1]; zi=pos[i,2]
            ke+=0.5*mp*(vel[i,0]**2+vel[i,1]**2+vel[i,2]**2)
            rb=np.sqrt(xi*xi+yi*yi+zi*zi+eps_b*eps_b)
            pb-=mp*mb/rb
            p=0.0
            for j in range(n):
                if j==i: continue
                dx=xi-pos[j,0]; dy=yi-pos[j,1]; dz=zi-pos[j,2]
                r=np.sqrt(dx*dx+dy*dy+dz*dz+eps*eps)
                p-=mp*mp/r
            pp+=0.5*p
        return ke, pp, pb
    return accel, energy

def collapse_dE(N, mu, eps, eps_b, R0=3.0, eta=0.05, t_end=2.0, seed=7):
    accel, energy = make_soft(eps_b)
    mp = mu/N
    pos, vel = E.make_ic_top_hat(N, R0, mu, rng=seed)
    eps2 = eps*eps; mb = 1.0
    acc = np.zeros_like(pos)
    accel(pos, acc, mp, eps2, mb)
    def choose_dt(pos):
        r2 = (pos*pos).sum(1) + eps_b*eps_b
        return min(0.3, eta*np.sqrt((r2**1.5).min()/(mb+mu)))
    dt = choose_dt(pos)
    t=0.0
    ke0,pp0,pb0 = energy(pos, vel, mp, eps, mb)
    E0 = ke0+pp0+pb0
    dEmax = 0.0
    while t < t_end:
        vel += 0.5*dt*acc
        pos += dt*vel
        t += dt
        accel(pos, acc, mp, eps2, mb)
        vel += 0.5*dt*acc
        dt = choose_dt(pos)
        ke,pp,pb = energy(pos, vel, mp, eps, mb)
        dEmax = max(dEmax, abs((ke+pp+pb-E0)/abs(E0)))
    return E0, dEmax

print("N      mu     eps   eps_b  E0        max|dE/E|  (t_end=2)")
for N in (2000, 4000):
    for eps_b in (0.1, 0.3):
        E0, dE = collapse_dE(N, 0.3, 0.3, eps_b)
        print(f"{N:5d}  0.3   0.3   {eps_b:.1f}   {E0:8.4f}  {dE:.2e}")
