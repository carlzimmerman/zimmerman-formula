#!/usr/bin/env python3
"""Independent validation of the Legendre EFE solve:
(1) direct 3D Green's-function quadrature of the phantom field at the two
    evaluation points (completely different Poisson path);
(2) small-e linearity scan (signal vs noise floor);
(3) closed-orbit debug scan f(v0);
(4) gamma dependence at perturbative e."""
import numpy as np, sys
sys.path.insert(0, ".")
from laneA_predictions import (solve_qumond, F_inward, phantom_density,
                               nu_fw, nup_fw, asym_local, closed_orbit,
                               plane_accel)

def direct_field(nup, e, x_eval, nr=400, nc=240, nphi=96, rmin=1e-3, rmax=2e3):
    """g_ph at point x_eval (3-vector) by brute quadrature over the phantom.
    Axisymmetric density; do full 3D midpoint-ish quadrature."""
    r_edges = np.geomspace(rmin, rmax, nr+1)
    r = np.sqrt(r_edges[1:]*r_edges[:-1]); dr = np.diff(r_edges)
    c_edges = np.linspace(-1, 1, nc+1)
    c = 0.5*(c_edges[1:]+c_edges[:-1]); dc = np.diff(c_edges)
    ph_edges = np.linspace(0, 2*np.pi, nphi+1)
    ph = 0.5*(ph_edges[1:]+ph_edges[:-1]); dph = ph_edges[1]-ph_edges[0]
    R, C = np.meshgrid(r, c, indexing="ij")
    rho = phantom_density(nup, e, R, C)              # (nr, nc)
    vol_rc = (R**2)[..., ] * dr[:, None] * dc[None, :]   # per phi: *dph
    S = np.sqrt(1-C*C)
    g = np.zeros(3)
    eps = 0.0
    for p, in zip(ph[:, None]):
        xs = R*S*np.cos(p); ys = R*S*np.sin(p); zs = R*C
        dx = xs - x_eval[0]; dy = ys - x_eval[1]; dz = zs - x_eval[2]
        d2 = dx*dx+dy*dy+dz*dz + eps
        w = rho*vol_rc*dph/d2**1.5
        g[0] += np.sum(w*dx); g[1] += np.sum(w*dy); g[2] += np.sum(w*dz)
    return g

print("== (1) direct quadrature vs Legendre solve ==")
for (x, e) in [(0.10, 0.05), (0.10, 0.20)]:
    sol = solve_qumond(nu_fw, nup_fw, e)
    r = x**-0.5
    for c0, lab in [(+1.0, "aligned"), (-1.0, "anti")]:
        # Legendre: inward radial force
        F_leg = F_inward(sol, r, c0)
        # direct: g_ph at (0,0,c0*r); inward = -(gz*c0) - point - CM
        gd = direct_field(nup_fw, e, np.array([0, 0, c0*r]))
        # need gz0 direct too: field at origin
        g0 = direct_field(nup_fw, e, np.array([0, 0, 1e-4]))
        F_dir = 1.0/r**2 - c0*(gd[2] - g0[2])
        print(f"  x={x} e={e} {lab:8s}: F_legendre={F_leg:.6f}  F_direct={F_dir:.6f} "
              f" ratio={F_leg/F_dir:.4f}")

print("\n== (2) small-e linearity (x=0.10, gamma=0) ==")
for e in (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 2e-2):
    A = asym_local(solve_qumond(nu_fw, nup_fw, e), 0.10, 0.0)[0]
    print(f"  e={e:8.1e}  A={A*100:+.5f}%   A/e={A/e:+.3f}")

print("\n== (3) closed-orbit scan f(v0), x=0.10 e=0.05 ==")
sol = solve_qumond(nu_fw, nup_fw, 0.05)
r0 = 0.10**-0.5
from scipy.integrate import solve_ivp
def rhs(t, s):
    gx, gz = plane_accel(sol, s[0], s[1])
    return [s[2], s[3], gx, gz]
vc = np.sqrt(r0*F_inward(sol, r0, 1.0))
for fac in (0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15):
    v0 = fac*vc
    ev = lambda t, s: s[0]
    ev.terminal, ev.direction = True, -1.0
    s = solve_ivp(rhs, [0, 50*r0**1.5], [0.0, r0, v0, 0.0],
                  rtol=1e-10, atol=1e-12, events=ev)
    if len(s.y_events[0]):
        se = s.y_events[0][0]
        print(f"  v0={fac:.2f}vc: event Z={se[1]:+.4f} vX={se[2]:+.4f} vZ={se[3]:+.5f}")
    else:
        print(f"  v0={fac:.2f}vc: NO EVENT (t_end={s.t[-1]:.1f}, "
              f"r_end={np.hypot(s.y[0,-1], s.y[1,-1]):.3f})")

print("\n== (4) gamma dependence at perturbative e=0.02, x=0.10 ==")
sol = solve_qumond(nu_fw, nup_fw, 0.02)
for g in (0, 30, 60, 80):
    A = asym_local(sol, 0.10, g)[0]
    print(f"  gamma={g:2d}: A={A*100:+.4f}%  A/cos(g)={A/np.cos(np.radians(g))*100:+.4f}%")
