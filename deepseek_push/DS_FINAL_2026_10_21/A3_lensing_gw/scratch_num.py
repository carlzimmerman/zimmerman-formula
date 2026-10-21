#!/usr/bin/env python3
"""Milky-Way-like static spherical solution: leading-order MOND profile,
then the O(eps^2) slip ODE."""
import numpy as np

c = 2.99792458e8
G = 6.67430e-11
Msun = 1.98892e30
kpc = 3.0856775814913673e19
a0 = 9.36e-11
Mb = 6.0e10*Msun
ah = 4.0*kpc

r = np.geomspace(1e-3*kpc, 600*kpc, 60000)
Mb_r = Mb*r**2/(r+ah)**2
gN = G*Mb_r/r**2
g = 0.5*gN*(1.0+np.sqrt(1.0+4*a0/gN))
u = a0*g/(a0+g)
phi_p = g/c**2                       # dPhi/dr  (dimensionless / length)
# Phi(r) = -int_r^inf phi_p dr  (Phi(inf)=0); integrate inward from Rmax with Phi(Rmax)
dphi = phi_p
Phi = np.zeros_like(r)
Phi[-1] = 0.0
for i in range(len(r)-2, -1, -1):
    Phi[i] = Phi[i+1] - 0.5*(dphi[i]+dphi[i+1])*(r[i+1]-r[i])
    # Phi(r) - Phi(r+dr) = -int_r^{r+dr} phi_p  -> Phi(r)=Phi(r+dr)-avg*dr
# note sign: Phi' = +phi_p  => Phi(r) = Phi(r+dr) - avg*dr
u_geom = u/c**2
F_src = 2.0*(np.gradient(np.gradient(Phi**2, r), r) + 2*np.gradient(Phi**2, r)/r) \
        - 0.5*phi_p**2 - 0.5*u_geom**2 + u_geom*phi_p
# GR baseline source
F_gr = 2.0*(np.gradient(np.gradient(Phi**2, r), r) + 2*np.gradient(Phi**2, r)/r) - 0.5*phi_p**2
F_p = F_src - F_gr


def solve_lap(F, r):
    """S with lap S = F, S regular at 0, S->0 at inf."""
    m = np.concatenate([[0.0], np.cumsum(0.5*(F[1:]*r[1:]**2 + F[:-1]*r[:-1]**2)*np.diff(r))]) 
    Sp = m/r**2
    S = np.zeros_like(r)
    for i in range(len(r)-2, -1, -1):
        S[i] = S[i+1] - 0.5*(Sp[i]+Sp[i+1])*(r[i+1]-r[i])
    return S, m, Sp

S_tot, _, _ = solve_lap(F_src, r)
S_gr, _, _ = solve_lap(F_gr, r)
S_p = S_tot - S_gr
for rr in [3, 5, 10, 20, 50, 100]:
    i = np.argmin(abs(r-rr*kpc))
    print(f"r={rr:4d} kpc  g={g[i]:.3e} m/s2  u={u[i]:.3e}  Phi={Phi[i]:.4e}  "
          f"S_tot={S_tot[i]:.3e}  S_gr={S_gr[i]:.3e}  S_p={S_p[i]:.3e}  "
          f"S_tot/Phi={S_tot[i]/Phi[i]:.3e}  S_p/Phi={S_p[i]/Phi[i]:.3e}")
