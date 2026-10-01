#!/usr/bin/env python3
"""Debug N8: verify the numeric 4D curvature against known analytic values."""
import numpy as np

dtv = 0.05

def d4(f, ax, dt_or_dx, wrap_t=False):
    out = np.zeros_like(f)
    if ax == 0:
        if wrap_t:
            out = (-np.roll(f, 2, 0) + 8*np.roll(f, 1, 0) - 8*np.roll(f, -1, 0)
                   + np.roll(f, -2, 0))/(12*dt_or_dx)
        else:
            out[2:-2] = (f[4:] - 8*f[3:-1] + 8*f[1:-3] - f[:-4])/(12*dt_or_dx)
            for i, sl in [(0, (slice(0,2),)), (1, (slice(0,3),))]:
                pass
            out[0] = (-25*f[0] + 48*f[1] - 36*f[2] + 16*f[3] - 3*f[4])/(12*dt_or_dx)
            out[1] = (-3*f[0] - 10*f[1] + 18*f[2] - 6*f[3] + f[4])/(12*dt_or_dx)
            out[-1] = (25*f[-1] - 48*f[-2] + 36*f[-3] - 16*f[-4] + 3*f[-5])/(12*dt_or_dx)
            out[-2] = (3*f[-1] + 10*f[-2] - 18*f[-3] + 6*f[-4] - f[-5])/(12*dt_or_dx)
    else:
        out = (-np.roll(f, 2, ax) + 8*np.roll(f, 1, ax) - 8*np.roll(f, -1, ax)
               + np.roll(f, -2, ax))/(12*dt_or_dx)
    return out

def R_num(Ns, Lx, a0, H, q0, q1, P_d, wrap_t=False):
    Mv = 1.0
    Nx, Ny, Nz, Nt = Ns
    dx_ = Lx/Nx
    t = (np.arange(Nt) - Nt//2)*dtv if not wrap_t else (np.arange(Nt))*dtv
    z = (np.arange(Nz) - Nz//2)*dx_
    a = a0*np.exp(H*t)
    q = q0 + q1*t
    g_ij = np.zeros((Nt, Nx, Ny, Nz, 3, 3))
    kk_ = 1
    kz_ = 2*np.pi*kk_/Lx
    e = np.zeros((3, 3)); e[0, 0] = 1; e[1, 1] = -1
    gam = q[:, None, None, None, None, None]*np.cos(kz_*z)[None, None, None, :, None, None]*e
    for i in range(3):
        for j in range(3):
            g_ij[..., i, j] = a[..., None, None, None]**2*(np.eye(3)[i, j] + gam[..., i, j])
    g = np.zeros((Nt, Nx, Ny, Nz, 4, 4))
    g[..., 0, 0] = -1.0
    g[..., 1:, 1:] = g_ij
    gi = np.linalg.inv(g.reshape(Nt*Nx*Ny*Nz, 4, 4)).reshape(Nt, Nx, Ny, Nz, 4, 4)
    dg = np.stack([d4(g, ax, dtv if ax == 0 else dx_, wrap_t and ax == 0) for ax in range(4)], axis=0)
    Gam = np.zeros((Nt, Nx, Ny, Nz, 4, 4, 4))
    for lm in range(4):
        for mu in range(4):
            for nu in range(4):
                s = np.zeros((Nt, Nx, Ny, Nz))
                for sig in range(4):
                    s += gi[..., lm, sig]*(dg[mu, ..., sig, nu] + dg[nu, ..., sig, mu]
                                           - dg[sig, ..., mu, nu])
                Gam[..., lm, mu, nu] = 0.5*s
    dGam = np.stack([d4(Gam, ax, dtv if ax == 0 else dx_, wrap_t and ax == 0) for ax in range(4)], axis=0)
    Rc = np.zeros((Nt, Nx, Ny, Nz))
    for mu in range(4):
        for nu in range(4):
            term = np.zeros((Nt, Nx, Ny, Nz))
            for rho in range(4):
                term += dGam[rho, ..., rho, mu, nu] - dGam[nu, ..., rho, mu, rho]
            for rho in range(4):
                for sig in range(4):
                    term += Gam[..., sig, mu, nu]*Gam[..., rho, sig, rho] \
                          - Gam[..., sig, mu, rho]*Gam[..., rho, nu, sig]
            Rc += gi[..., mu, nu]*term
    sg = np.sqrt(-np.linalg.det(g.reshape(Nt*Nx*Ny*Nz, 4, 4)).reshape(Nt, Nx, Ny, Nz))
    L = sg*((Mv/2.)*(Rc) + P_d)
    return Rc, sg, L, g, gi

# Test 1: pure de Sitter background, q=0: R should be 12 H^2 everywhere
H = 0.11
a0 = 1.3
P_d = -3*H**2
Rc, sg, L, g, gi = R_num((9, 24, 24, 24), 2*np.pi, a0, H, 0.0, 0.0, P_d, wrap_t=False)
print("dS: numeric R range:", Rc.min(), Rc.max(), " analytic 12H^2 =", 12*H**2)
# interior only:
Ri = Rc[2:-2]
print("dS: interior R mean:", Ri.mean(), " analytic:", 12*H**2)
print("dS: L_bg numeric mean:", L.mean(), " analytic a^3(6H^2+P_d) with a=a0:",
      a0**3*(6*H**2 + P_d))

# Test 2: flat space Minkowski + TT wave: known quadratic piece of R:
# R^(2) for gamma_ij TT: R = -(1/4) sum (dl gamma_ij)(d^l gamma^ij) + O(g^3): check numeric
H = 0.0
a0 = 1.0
q0, q1 = 0.01, 0.01
Rc2, sg2, L2, _, _ = R_num((9, 32, 32, 32), 2*np.pi, a0, H, q0, q1, 0.0, wrap_t=True)
Lm = L2.mean()
# analytic L2(avg) = (1/2)a^3*R^(2)avg = (M/2)*R2avg: R2avg = (1/4)*[q1^2 - k^2 q0^2]*2*(1/2)
# (M/2)*(1/4)*(q1^2 - k^2 q0^2) = 1/8 (q1^2 - q0^2) k=1
print("Minkowski: L2 numeric mean:", Lm, " analytic (1/8)(q1^2-k^2 q0^2):", (1/8.)*(q1**2 - 1*q0**2))
# also with q0=0: pure kinetic
_, _, Lk, _, _ = R_num((9, 32, 32, 32), 2*np.pi, 1.0, 0.0, 0.0, 0.01, 0.0, wrap_t=True)
print("Minkowski kinetic-only: L mean:", Lk.mean(), " expect (1/8) q1^2 =", (1/8.)*0.01**2)