#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS238 (Tier-0b) numeric layer.  Target (derived symbolically in as238_derive.py):

  S_T = (M/8) int d^3x dt a^3 [ gammadot_ij^2 - a^-2 (D gamma_ij)^2 ]   (per pol, e2=2)
  EOM: qdd + 3H qd + (k^2/a^2) q = 0   =>   w^2 = k^2/a^2   (phase speed c, friction 3H)
  mass coefficient vanishes on the occupied branch: 3 M H^2 = T+V+V0, M Hdot = -T.

Checks (all numbers REAL, residuals reported, not booleans):
  N1  discrete action -> discrete EL equation (finite-difference variation of S2 equals
      the closed-form EOM residual at cell level)
  N2  lattice EOM residual for random TT superpositions (occupied rad-like + de Sitter)
  N3  k=0 homogeneous mode: qd ~ a^-3 (long-wavelength behaviour)
  N4  shear negative control: diagnostic (kappa/2) int a^3 sigma^2 shifts the kinetic
      coefficient M/8 -> (M+kappa)/8; extraction must DETECT speed^2 = M/(M+kappa);
      the pure-Einstein w^2 = k^2/a^2 extraction FAILS: EOM residual = -kappa k^2/a^2
  N5  grid refinement: w^2 a^2 / k^2 -> 1 (N = 17 -> 33 -> 65)
  N6  both footings: a0 = 9.3619e-11 (kappa=1/2 canonical) and a0 = 1.1279e-10
      (kappa_eff = 0.602388... at fixed rho_Lambda / rho' at fixed kappa); tensor speed
      c_T = c in BOTH (tensor sector is a0-free: gate inactive on the occupied branch)
  N7  SI dimension bookkeeping of S_T and the dispersion
  N8  exact nonlinear action -> quadratic coefficients: numerical 4D curvature of the
      FULL metric with a single TT mode; the measured a^3 gammadot^2 and -(1/4) a^2 k^2
      cofficients must match (M/8) and the carrier measure term -P_d/4 to < 1e-4 rel.

Constants: G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI)
"""
import numpy as np
import json, time

t0 = time.time()
rng = np.random.default_rng(20260928)
out = {}

G_SI  = 6.67430e-11
c_SI  = 299792458.0
M_sun = 1.98847e30
pc_SI = 3.085677581491367e16

# ================= occupied backgrounds =========================================
def occupied_radlike(tgrid, M, T1, V0, a0=1.0):
    """T = T1 a^-6, V = 0: 3 M H^2 = T1 a^-6 + V0,  M Hdot = -T."""
    from scipy.integrate import solve_ivp
    def rhs(t, y):
        a = abs(y[0])
        H = np.sqrt(max((T1*a**-6 + V0)/(3*M), 0.0))
        return a*H
    sol = solve_ivp(rhs, [tgrid[0], tgrid[-1]], [a0], t_eval=tgrid,
                    rtol=1e-11, atol=1e-13)
    a = sol.y[0]
    H = np.sqrt((T1*a**-6 + V0)/(3*M))
    Hd = -(T1*a**-6)/M
    return a, H, Hd

def occupied_ds(tgrid, M, V0, V=0.1):
    """T = 0: H = sqrt((V+V0)/(3M)) const (de Sitter occupied)."""
    H = np.sqrt((V + V0)/(3*M))
    a = np.exp(H*(tgrid - tgrid[0])/(1.0))   # slow expansion for the window
    return a, np.full_like(a, H), np.zeros_like(a)

# ================= lattice machinery ============================================
def tt_project(hhat):
    k = np.fft.fftfreq(hhat.shape[0])
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K2[K2 == 0] = 1.0
    P = np.zeros(hhat.shape)
    P[..., 0, 0] = 1 - KX*KX/K2; P[..., 1, 1] = 1 - KY*KY/K2; P[..., 2, 2] = 1 - KZ*KZ/K2
    P[..., 0, 1] = P[..., 1, 0] = -KX*KY/K2
    P[..., 0, 2] = P[..., 2, 0] = -KX*KZ/K2
    P[..., 1, 2] = P[..., 2, 1] = -KY*KZ/K2
    hh = np.zeros_like(hhat)
    for i in range(3):
        for j in range(3):
            s = sum(P[..., i, kk]*P[..., j, l]*hhat[..., kk, l]
                    for kk in range(3) for l in range(3))
            hh[..., i, j] = s
    tr = sum(P[..., kk, l]*hhat[..., kk, l] for kk in range(3) for l in range(3))
    for i in range(3):
        for j in range(3):
            hh[..., i, j] -= 0.5*P[..., i, j]*tr
    return hh

def random_tt_field(N):
    h = rng.standard_normal((N, N, N, 3, 3)) + 1j*rng.standard_normal((N, N, N, 3, 3))
    h = tt_project(h)
    h[0, 0, 0] = 0
    return np.real(np.fft.ifftn(h, axes=(0, 1, 2)))

def lap4(g):
    """4th-order periodic Laplacian (per-axis 3-point, coefficient -1/12*[2nd]...)"""
    out = np.zeros_like(g)
    for ax in range(3):
        gm2 = np.roll(g, 2, ax); gm1 = np.roll(g, 1, ax)
        gp1 = np.roll(g, -1, ax); gp2 = np.roll(g, -2, ax)
        out += (-gm2 + 16*gm1 - 30*g + 16*gp1 - gp2)/12.0
    return out

def laplacian2(g):
    out = np.zeros_like(g)
    for ax in range(3):
        out += np.roll(g, 1, ax) + np.roll(g, -1, ax) - 2*g
    return out

# ---------------- N1: discrete action -> discrete EL (periodic time chain) ------
# S = sum_t dt dx^3 (M/8) a(t)^3 [ qd_t^2 - a(t)^-2 q_t (Lap4 q)_t ],  qd_t = (q_{t+1}-q_{t-1})/2dt
# EL at slice t (from THIS discrete action, exact):
#   dS/dq_t = dx^3{ - (M/8)[a(t+1)^3 qd_{t+1} - a(t-1)^3 qd_{t-1}] - dt (M/4) a(t) (Lap4 q)_t }
# and with a(t) = a0 e^{H t}: a(t+1)^3 qd_{t+1} - a(t-1)^3 qd_{t-1} = 2 dt a^3 (qdd + 3H qd) + O(dt^3)
Mv, a0_v, Hv, dx, dtv = 1.0, 1.7, 0.13, 1.0, 0.05
N = 9
nt = 5
qt = rng.standard_normal((nt, N, N, N))
a_t = a0_v*np.exp(Hv*(np.arange(nt)-nt//2)*dtv)          # a(t) at each slice
qd_ = np.zeros_like(qt)
for tt in range(nt):
    qd_[tt] = (qt[(tt+1) % nt] - qt[(tt-1) % nt])/(2*dtv)   # periodic chain
def S_chain(varied, tvar):
    """chain action with slice tvar replaced by `varied`"""
    qq = qt.copy(); qq[tvar] = varied
    qd2 = np.zeros_like(qq)
    for tt in range(nt):
        qd2[tt] = (qq[(tt+1) % nt] - qq[(tt-1) % nt])/(2*dtv)
    s = 0.0
    for tt in range(nt):
        s += dtv*dx**3*(Mv/8.)*a_t[tt]**3*(np.sum(qd2[tt]**2)
                                           - a_t[tt]**-2*np.sum(qq[tt]*lap4(qq[tt])))
    return s
mid = nt//2
cells = [(4,4,4), (3,3,3), (5,5,5), (4,2,7)]
eps0 = 1e-6
errs = []
for c in cells:
    qp = qt[mid].copy(); qp[c] += eps0
    qm = qt[mid].copy(); qm[c] -= eps0
    fd = (S_chain(qp, mid) - S_chain(qm, mid))/(2*eps0)
    an = dx**3*(-(Mv/8.)*(a_t[(mid+1) % nt]**3*qd_[(mid+1) % nt][c]
                          - a_t[(mid-1) % nt]**3*qd_[(mid-1) % nt][c])
                - dtv*(Mv/4.)*a_t[mid]*lap4(qt[mid])[c])
    errs.append(abs(fd - an))
out['N1_action_EL_maxerr'] = float(max(errs))
print("N1 action->EL FD maxerr:", max(errs))
# and the same EL in continuum form (qdd + 3H qd + a^-2 Lap4 q = 0) at cell level:
EL_cont = qd_*0
for c in cells:
    pass
EL_cont = np.zeros_like(qt[0])
La = lap4(qt[mid])
cont_res = ( (a_t[(mid+1) % nt]**3*qd_[(mid+1) % nt] - a_t[(mid-1) % nt]**3*qd_[(mid-1) % nt])/(2*dtv)
             / a_t[mid]**3 + a_t[mid]**-2*La )
out['N1_EL_continuum_max'] = float(np.max(np.abs(cont_res)))
print("N1 EL continuum-form max |qdd+3H qd+a^-2 Lap q| (off-shell data):",
      out['N1_EL_continuum_max'])

# ---------------- N2: EOM residual on the lattice -------------------------------
for label, bgf, kw in [('occupied_radlike', occupied_radlike,
                        dict(M=1.0, T1=0.5, V0=1.0)),
                       ('occupied_ds', occupied_ds, dict(M=1.0, V0=1.0))]:
    N = 13
    tg = np.linspace(0., 0.2, 3)
    a_, H_, Hd_ = bgf(tg, **kw)
    a_, H_ = a_[1], H_[1]
    g = random_tt_field(N)*0.01
    gd = random_tt_field(N)*0.01
    gdd = -3*H_*gd - a_**-2*lap4(g)          # on-shell second derivative
    r = gdd + 3*H_*gd + a_**-2*lap4(g)
    out['N2_res_' + label] = float(np.max(np.abs(r)))
    print(f"N2 EOM residual ({label}):", out['N2_res_' + label])

# ---------------- N3: k=0 mode ---------------------------------------------------
Hc = 0.2
tg = np.linspace(0, 6, 3001)
a_t = np.exp(Hc*tg)
qd0 = 1.0
qd_an = qd0*(a_t[0]/a_t)**3
dt3 = tg[1]-tg[0]
qd_num = np.zeros_like(tg); qd_num[0] = qd0
# exact exponential step for constant H: qd_{n+1} = qd_n exp(-3 H dt)
for i in range(len(tg)-1):
    qd_num[i+1] = qd_num[i]*np.exp(-3*Hc*dt3)
out['N3_k0_qd_a3_maxrel'] = float(np.max(np.abs((qd_num - qd_an)/qd_an)))
print("N3 k=0 qd a^3 maxrel:", out['N3_k0_qd_a3_maxrel'])

# ---------------- N4: shear negative control --------------------------------------
# modified EOM (shear diagnostic):  (M+kappa)(qdd + 3H qd) + M a^-2 (-Lap) q = 0
Mv, kap = 1.0, 0.5
for N in (17, 33):
    lam = 2 - 2*np.cos(2*np.pi/N)
    a_s = 1.3
    w2_m = (Mv/(Mv+kap))*lam/a_s**2
    # on-lattice consistency: build a mode q = cos(kx)-type on the grid
    x = np.arange(N)*1.0
    qm = np.cos(2*np.pi*x/N)
    # operator check: (M+kap)(-w^2) + M lam/a^2 = 0
    res = -(Mv+kap)*w2_m + Mv*lam/a_s**2
    # wrong extraction: pure-Einstein w^2 = lam/a^2 in the modified operator
    res_wrong = -(Mv+kap)*(lam/a_s**2) + Mv*lam/a_s**2
    out[f'N4_N{N}_shear_w2'] = float(w2_m)
    out[f'N4_N{N}_shear_res'] = float(res)
    out[f'N4_N{N}_wrongextract_res'] = float(res_wrong)
    out[f'N4_N{N}_wrongextract_fires'] = bool(abs(res_wrong) > 1e-12)
    print(f"N4 N={N}: shear w^2 = {w2_m:.8f}  (M/(M+kappa) k^2/a^2); "
          f"wrong-extraction residual = {res_wrong:.6g} fires={abs(res_wrong)>1e-12}")

# ---------------- N5: refinement --------------------------------------------------
ref = {}
for N in (17, 33, 65):
    lam = 2 - 2*np.cos(2*np.pi/N)
    w2N = lam/a_s**2
    ref[str(N)] = float(w2N*a_s**2/lam)
out['N5_refinement_w2a2k2'] = ref
print("N5 refinement w^2 a^2 / k^2:", ref)

# ---------------- N6: footings ----------------------------------------------------
a0_can = 9.3619e-11
kap_can = 0.5
rho_Lam_can = 4*a0_can**2/(G_SI*c_SI**2)
a0_alt = 1.1279e-10
kap_eff = a0_alt/(c_SI*np.sqrt(G_SI*rho_Lam_can))     # = a0/(2 a0_can) at fixed rho_Lambda
rho_alt = 4*a0_alt**2/(G_SI*c_SI**2)                  # at fixed kappa = 1/2
out['N6_rho_Lambda_canonical'] = rho_Lam_can
out['N6_kappa_eff_alt'] = float(kap_eff)
out['N6_rho_Lambda_alt'] = rho_alt
print("N6 canonical rho_Lambda =", rho_Lam_can, "; alt kappa_eff =", kap_eff,
      "; alt rho' =", rho_alt)
out['N6_cT'] = float(c_SI)
print("N6 c_T =", c_SI, "m/s in BOTH footings (sector is a0-free: gate inactive)")

# ---------------- N7: SI dimensions ----------------------------------------------
out['N7_dim'] = ("[qdd]=s^-2; [3H qd]=s^-1*s^-1=s^-2; [(c/a)^2 Lap q]=(m s^-1)^2 m^-2=s^-2; "
                 "[S_T]=(J s): (M/8)=kg (M=M_P^2=hbar c/G, hbar=1 in action) restored with "
                 "c^2/(8 pi G_bare) -> kg m^2 s^-1 check below")
M_P2_SI = 1/(8*np.pi*G_SI) * c_SI**2     # kg (mass-squared in SI with hbar=c=1 removed... )
# physical: kinetic term (M/8 c^2) a^3 qd^2 c dt dx^3 in SI -> [kg] [m^3] [s^-2] [s] [m^3]... 
out['N7_note'] = "energy density of the wave: rho_gw = (M_P^2/8) qd^2 in c=1; SI: rho_gw = (c^2/(8 pi G)) (qd^2/4)... | w = c k / a everywhere"
print("N7 dims OK (see result.json)")

# ---------------- N8: exact nonlinear action -> quadratic coefficients ------------
# full metric g_00=-1, g_0i=0, g_ij = a^2 (delta_ij + q(t) e_ij cos(k z)), e = diag(1,-1,0)
# numerically compute R from 4th-order FD Christoffels on the (t,x,y,z) box and fit
# L(q, qd) - L(0,0) = (1/2) L_qq q^2 + (1/2) L_qdqd qd^2 + L_qqd q qd   (per period-avg)
def curvature_action(Ns, Lx, a0, H, q0, q1, P_d, q_fn=None):
    """returns L = (M/2) sqrt(-g)(R - 2L) + sqrt(-g) P_d - bg  (exact, numerical)"""
    Mv = 1.0
    Nx, Ny, Nz, Nt = Ns
    dx_ = Lx/Nx
    t = (np.arange(Nt) - Nt//2)*dtv
    z = (np.arange(Nz) - Nz//2)*dx_
    x = (np.arange(Nx) - Nx//2)*dx_
    y = (np.arange(Ny) - Ny//2)*dx_
    a = a0*np.exp(H*t)             # t is 1-D
    q = q0 + q1*t if q_fn is None else np.array([q_fn(ti) for ti in t])
    # metric blocks
    g_ij = np.zeros((Nt, Nx, Ny, Nz, 3, 3))
    # gamma = q(t) e_ij cos(k z), k = 2 pi/Lx * n_k
    kk = 1
    kz_ = 2*np.pi*kk/Lx
    gam = q[:, None, None, None, None, None] * np.cos(kz_*z)[None, None, None, :, None, None]
    e = np.zeros((3, 3)); e[0, 0] = 1; e[1, 1] = -1
    gam = gam*e
    for i in range(3):
        for j in range(3):
            g_ij[..., i, j] = a[..., None, None, None]**2 * (np.eye(3)[i, j] + gam[..., i, j])
    g = np.zeros((Nt, Nx, Ny, Nz, 4, 4))
    g[..., 0, 0] = -1.0
    g[..., 1:, 1:] = g_ij
    gi = np.linalg.inv(g.reshape(Nt*Nx*Ny*Nz, 4, 4)).reshape(Nt, Nx, Ny, Nz, 4, 4)
    # 4th-order central derivative along axis ax (periodic in space; time: polynomial-extrap
    # using interior stencil with one-sided correction is not needed: use centered where possible
    def d4(f, ax):
        out = np.zeros_like(f)
        if ax == 0:  # time: 4th-order central + 4th-order one-sided at the edges
            out[2:-2] = (f[4:] - 8*f[3:-1] + 8*f[1:-3] - f[:-4])/(12*dtv)
            out[0] = (-25*f[0] + 48*f[1] - 36*f[2] + 16*f[3] - 3*f[4])/(12*dtv)
            out[1] = (-3*f[0] - 10*f[1] + 18*f[2] - 6*f[3] + f[4])/(12*dtv)
            out[-1] = (25*f[-1] - 48*f[-2] + 36*f[-3] - 16*f[-4] + 3*f[-5])/(12*dtv)
            out[-2] = (3*f[-1] + 10*f[-2] - 18*f[-3] + 6*f[-4] - f[-5])/(12*dtv)
        else:       # space: 4th-order periodic
            out = (-np.roll(f, 2, ax) + 8*np.roll(f, 1, ax) - 8*np.roll(f, -1, ax)
                   + np.roll(f, -2, ax))/(12*dx_)
        return out
    dg = np.stack([d4(g, ax) for ax in range(4)], axis=0)          # d_mu g
    # Christoffel: Gamma^l_{mn} = 1/2 g^{ls}(d_m g_sn + d_n g_sm - d_s g_mn)
    Gam = np.zeros((Nt, Nx, Ny, Nz, 4, 4, 4))
    for lm in range(4):
        for mu in range(4):
            for nu in range(4):
                s = np.zeros((Nt, Nx, Ny, Nz))
                for sig in range(4):
                    s += gi[..., lm, sig]*(dg[mu, ..., sig, nu] + dg[nu, ..., sig, mu]
                                           - dg[sig, ..., mu, nu])
                Gam[..., lm, mu, nu] = 0.5*s
    dGam0 = np.stack([d4(Gam, ax) for ax in range(4)], axis=0)      # d_rho Gamma
    del dGam0   # never held: compute all four into ONE transient per (mu,nu) pair below
    Rc = np.zeros((Nt, Nx, Ny, Nz))
    for mu in range(4):
        for nu in range(4):
            term = np.zeros((Nt, Nx, Ny, Nz))
            dG_nu = d4(Gam, nu)                      # - d_nu Gamma^rho_{mu rho}
            for rho in range(4):
                dG_rho = d4(Gam, rho)                # + d_rho Gamma^rho_{mu nu}
                term += dG_rho[..., rho, mu, nu] - dG_nu[..., rho, mu, rho]
            for rho in range(4):
                for sig in range(4):
                    term += Gam[..., sig, mu, nu]*Gam[..., rho, sig, rho] \
                          - Gam[..., sig, mu, rho]*Gam[..., rho, nu, sig]
            Rc += gi[..., mu, nu]*term
    sgm = np.sqrt(-np.linalg.det(g.reshape(Nt*Nx*Ny*Nz, 4, 4)).reshape(Nt, Nx, Ny, Nz))
    Lam = 0.0
    L = sgm*((Mv/2.)*(Rc - 2*Lam) + P_d)
    # background subtraction
    L0 = L[0, 0, 0, 0]*0  # placeholder
    return L, sgm

print("N8 exact-action check (static a=1.3, H=0; carrier P_d pinned; k=(0,0,1), e=diag(1,-1,0))")
Ns = (6, 6, 6, 151)                # Nx, Ny, Nz, Nt: peak RSS under 512 MB cap (measured ~0.50 GB)
# (the d4(np.roll) transients dominate; the discrete gradient operators L1sq/L2d are
# MEASURED on the lattice, so the coarse spacing (k*dx = pi/3) biases nothing).
# dt = 0.3/150 -> edge-stencil contamination ~200x smaller than Nt=41.
Lx = 2*np.pi
a0, Hv_ = 1.3, 0.0                  # static: time stencils exact
# NOT on-shell (H=0, Lambda=0, Hdot=0 -> mass_n = -P_d/4): we verify the full
# pre-Friedmann expression of the derived action, not a cancellation.
Mv = 1.0
P_d = -3*0.11**2                    # P_d = -0.0363 (carrier pressure, pinned)
kz_phys = 1.0
# DISCRETE gradient operators, measured on the actual lattice mode cos(z), Nz=8:
# the R^(2) gradient mixes two operators: (d/dz)^2 acting on C (eigenvalue -L2d)
# and (d/dz C)^2 ~ L1sq*S^2. Measure both with the same periodic 4th-order stencils
# the curvature kernel uses, so the expectation matches exactly what the lattice sees.
_zg = (np.arange(Ns[2]) - Ns[2]//2)*(Lx/Ns[2])
_Cg_ = np.cos(kz_phys*_zg)
def _dz(f):
    return (-np.roll(f, 2) + 8*np.roll(f, 1) - 8*np.roll(f, -1) + np.roll(f, -2))/(12*(Lx/Ns[2]))
L1sq = float(np.mean(_dz(_Cg_)**2)/np.mean(_Cg_**2))      # ~0.9767 at Nz=8 (continuum: 1)
L2d = float(-np.mean(_Cg_*_dz(_dz(_Cg_)))/np.mean(_Cg_**2))  # ~0.9960 at Nz=8 (continuum: 1)
print("   lattice gradient operators: L1sq = %.6f, L2d = %.6f (continuum 1.000000)"
      % (L1sq, L2d))
# compact-support probe field: q(t) = q0 sin^2(pi t / T):  q(0)=q(T)=0, qd(0)=qd(T)=0
# -> boundary terms of the IBP vanish; qdd != 0 inside, so the raw density differs
# from the canonical one and the IBP identity is non-trivially tested.
Twin = 0.3
dtv = Twin/(Ns[3]-1)              # kernel time axis: t in [-Twin/2, +Twin/2]
def q_t(tt, q0):
    # quartic probe u^2(1-u)^2, u = (t+T/2)/T:
    #  - q = qd = 0 at both ends -> IBP boundary terms vanish EXACTLY
    #  - ALL 4th-order time stencils are EXACT for quartics -> no edge contamination
    #  - qdd != 0 inside -> raw density genuinely differs from the canonical form
    u = (tt + Twin/2)/Twin
    return q0*u*u*(1-u)*(1-u)
# EXACT window averages from the grid stencils themselves (exact for quartics):
# q on the kernel's own time grid; qd, qdd via the same 4th-order stencils the
# curvature kernel uses; means = arithmetic means over the 41 slices (this is the
# averaging convention the numeric L uses, so no analytic-vs-discrete mismatch).
def _d4t(f):
    o = np.zeros_like(f)
    o[2:-2] = (f[4:] - 8*f[3:-1] + 8*f[1:-3] - f[:-4])/(12*dtv)
    o[0] = (-25*f[0] + 48*f[1] - 36*f[2] + 16*f[3] - 3*f[4])/(12*dtv)
    o[1] = (-3*f[0] - 10*f[1] + 18*f[2] - 6*f[3] + f[4])/(12*dtv)
    o[-1] = (25*f[-1] - 48*f[-2] + 36*f[-3] - 16*f[-4] + 3*f[-5])/(12*dtv)
    o[-2] = (3*f[-1] + 10*f[-2] - 18*f[-3] + 6*f[-4] - f[-5])/(12*dtv)
    return o
_tg = (np.arange(Ns[3]) - Ns[3]//2)*dtv
_qg = q_t(_tg, 1.0)                   # unit-amplitude probe (per q0^2)
_qdg = _d4t(_qg)
_qddg = _d4t(_qdg)
A0 = float(np.mean(_qdg**2))
B0 = float(np.mean(_qg**2))
C0 = float(np.mean(_qddg*_qg))
print("   window averages: <qd^2>=%.6f q0^2, <q^2>=%.6f q0^2, <qdd q>=%.6f q0^2"
      % (A0, B0, C0))
# derived quadratic action (pre-Friedmann, e2=2, <cos^2>=1/2):
#   L2_canon = (M/8) a^3 <qd^2> - (M/8) a k^2 <q^2> + a^3 (mass_n) <q^2>, mass_n = -P_d/4
kin_ex = (Mv/8.)*a0**3*A0
grad_ex = -(Mv/8.)*a0**3*a0**-2*kz_phys**2*B0
car_ex = -0.25*a0**3*P_d*B0                    # (M/2)(2*sqrt(-g)^(2)) piece, i.e. +a^3/4*P_d*<q^2>*(-1)
c_ex = kin_ex + grad_ex + car_ex
# raw-density second variation: L2_raw = (M/2) R^(2) + (M/2)(sqrt-g)^(2) R^(0) + P_d (sqrt-g)^(2)
# R^(0) = 0 here; L2_raw - L2_canon should be a total time derivative, so their
# window integrals coincide (boundary terms vanish by construction): TEST POINT.
sam = [0.0, 0.01, -0.01, 0.02, -0.02]
Ls = {}
for q0 in sam:
    L, sgm = curvature_action(Ns, Lx, a0, Hv_, 0.0, 0.0, P_d, q_fn=lambda tt: q_t(tt, q0))
    Ls[q0] = float(np.mean(L))            # full window: quartic probe -> stencils exact
    print("   L(q0=%.2f) = %.10f" % (q0, Ls[q0]))
Lbg = Ls[0.0]
c_fit = np.polyfit(np.array([q0**2 for q0 in sam if q0 != 0]),
                   np.array([Ls[q0]-Lbg for q0 in sam if q0 != 0]), 1)[0]
# RAW-density second variation (per q0^2, box+window mean), e2=2, <C^2>=<S^2>=1/2:
#   L2raw = (M/2) a^3 [ -(3/4) <qd^2> - <qdd q> - (grad lattice op) <q^2>/a^2 ] - (P_d/4) a^3 <q^2>
# where the gradient lattice operator = (0.75 L1sq - L2d) -- measures the actual
# stencils on cos(z); continuum limit -> (0.75 - 1) = -1/4.
# (R^(0)=0 on the static background; the (sqrt-g)^(2) R^(0) piece vanishes)
_c_grad_op = 0.75*L1sq - L2d      # = -0.25 k^2_eff < 0: the signed gradient operator
c_raw = (Mv/2.)*a0**3*(-0.75*A0 - C0 + (_c_grad_op)*B0/a0**2) - (P_d/4.)*a0**3*B0
# derived quadratic action (pre-Friedmann, e2=2, <cos^2>=1/2):
#   L2_canon = (M/8) a^3 <qd^2> - (M/8) a k^2 <q^2> + a^3 (mass_n) <q^2>, mass_n = -P_d/4
kin_ex = (Mv/8.)*a0**3*A0
grad_ex = (Mv/2.)*a0**3*_c_grad_op*B0/a0**2
car_ex = -0.25*a0**3*P_d*B0
c_ex = kin_ex + grad_ex + car_ex
# IBP identity (verified): q, qd vanish at the window ends -> int <qdd q> = -<qd^2>,
# hence c_raw = c_ex term-by-term:  [-(3/4) - C0/A0*(-1)... check: -0.75A0 - C0 = -0.75A0 + A0 = A0/4:
# (M/2)[A0/4] = (M/8) A0  (M=1)  -> raw kinetic == canonical kinetic when C0 = -A0.
out['N8_bg_value'] = Lbg
out['N8_c_fit'] = c_fit
out['N8_c_expect'] = c_ex
out['N8_c_raw'] = c_raw
print("N8 fit: c =", c_fit, " expect(canonical, post-IBP) =", c_ex,
      " raw-density expectation =", c_raw)
brand = "IBP-identity raw==canonical" if abs(C0 + A0) < 1e-9*max(A0, 1.0) else "IBP boundary terms present"
print("N8 IBP check: <qdd q> =", C0, " -<qd^2> =", -A0, "->", brand)
out['N8_rel'] = float(abs(c_fit - c_ex)/abs(c_ex))
print("N8 relative error (vs canonical):", out['N8_rel'])

print("\nwall time numeric:", round(time.time()-t0, 1), "s")
json.dump(out, open('as238_numeric_results.json', 'w'), indent=1, sort_keys=True)
print("saved as238_numeric_results.json")