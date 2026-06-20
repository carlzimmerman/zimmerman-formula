#!/usr/bin/env python3
"""
ROUTE 3 -- full 3D QUMOND grid: DISCRETE clumps vs SMOOTH, the overlap/collective phantom.

QUMOND algorithm (Milgrom 2010, the standard quasi-linear MOND):
  1. Newtonian potential Phi_N from the baryon density (here: analytic superposition of
     point/Plummer sources -- linear, exact).
  2. g_N = -grad Phi_N.
  3. Phantom density rho_ph = -(1/4piG) div[ (nu(|g_N|/a0) - 1) g_N ].
  4. Total phantom inside R = volume integral of rho_ph (== Gauss surface flux of (nu-1)g_N).

This is EXACT QUMOND (not the algebraic g_obs=nu*gN single-source shortcut): the phantom is
sourced by the FULL multi-source g_N field, so all overlap/superposition nonlinearity is in.

We compute M_phantom(<R_core) for:
  (A) DISCRETE: N member galaxies as Plummer clumps + smooth ICM gas  (Carl's clumpy/overlap)
  (B) SMOOTH:   same total baryon mass as one smooth spherical profile
and compare. If (A) >> (B) -> overlap adds binding (Carl right). If (A) ~ (B) -> enclosed-mass
theorem holds, clumpiness only redistributes (Carl's effect already in the smooth calc).

Both ways. Quarantine held (a0 input).
"""
import numpy as np

G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
a0   = 9.36e-11

def nu_minus_1(gN):
    """ (nu-1) for the framework's g_obs=sqrt(gN^2+gN a0): nu=sqrt(1+a0/gN). """
    y = gN / a0
    return np.sqrt(1.0 + 1.0/y) - 1.0

# ---- cluster core setup (matches route3_longrange_horizon.py / banked ledger) -------------
M500       = 1.0e15 * Msun
R_core     = 420.0 * kpc
M_gas_core = 0.30 * 0.095 * M500
M_star_core= 0.50 * 0.015 * M500
M_bar_core = M_gas_core + M_star_core

# member galaxies
N_gal  = 200
rng    = np.random.default_rng(42)
M_bcg  = 0.10 * M_star_core
ranks  = np.arange(1, N_gal)
w      = ranks**(-1.0)
m_sat  = (M_star_core - M_bcg) * w / w.sum()
m_gal  = np.concatenate([[M_bcg], m_sat])

# galaxy positions: NFW-like / King core distribution within R_core (3D), isotropic.
# draw radii from a cored profile rho ~ 1/(1+(r/rs)^2) with rs = 200 kpc, truncated at R_core
rs_gal = 200.0 * kpc
def sample_radii(n):
    out = []
    while len(out) < n:
        r = rng.uniform(0, R_core, size=4*n)
        # acceptance ~ r^2/(1+(r/rs)^2)  (number density * shell)
        pdf = r**2 / (1.0 + (r/rs_gal)**2)
        pdf /= pdf.max()
        keep = r[rng.uniform(size=r.size) < pdf]
        out.extend(keep.tolist())
    return np.array(out[:n])
r_gal  = sample_radii(N_gal)
costh  = rng.uniform(-1, 1, N_gal)
phi    = rng.uniform(0, 2*np.pi, N_gal)
sinth  = np.sqrt(1 - costh**2)
gal_xyz= np.column_stack([r_gal*sinth*np.cos(phi),
                          r_gal*sinth*np.sin(phi),
                          r_gal*costh])
# Plummer softening per galaxy: a galaxy's stellar scale ~ a few kpc. Use 3 kpc.
b_gal  = 3.0 * kpc

# gas: smooth beta-model-ish core, all in core radius. Represent as a smooth analytic sphere
# with enclosed mass profile M_gas(<r) = M_gas_core * (r/R_core)^... -> use beta=2/3 model.
rc_gas = 150.0 * kpc
def Mgas_enc(r):
    # beta-model rho ~ (1+(r/rc)^2)^(-3/2); enclosed mass normalized to M_gas_core at R_core
    def menc(rr):
        # integral of 4 pi r^2 (1+(r/rc)^2)^-1.5  -> closed form ~ asinh - r/sqrt
        x = rr/rc_gas
        return np.arcsinh(x) - x/np.sqrt(1+x**2)
    return M_gas_core * menc(r/1.0)/menc(R_core/1.0) if np.isscalar(r) else \
           M_gas_core * menc(r)/menc(R_core)

# ---- Newtonian g_N from the FULL baryon distribution -------------------------------------
def gN_discrete(P):
    """Newtonian g vector at points P (Mx3) from N Plummer galaxies + smooth gas sphere."""
    g = np.zeros_like(P)
    # galaxies (Plummer)
    d  = P[:,None,:] - gal_xyz[None,:,:]          # M x N x 3
    r2 = (d**2).sum(-1) + b_gal**2                 # softened
    inv= G * m_gal[None,:] / r2**1.5               # M x N
    g -= (inv[:,:,None] * d).sum(1)
    # gas (spherical, enclosed mass)
    rr = np.linalg.norm(P, axis=1)
    Mg = np.array([Mgas_enc(x) for x in rr])
    with np.errstate(divide='ignore', invalid='ignore'):
        gg = np.where(rr>0, G*Mg/rr**2, 0.0)
    g -= (gg/np.maximum(rr,1e-30))[:,None] * P
    return g

def gN_smooth(P):
    """Newtonian g from the SAME total baryon mass as ONE smooth sphere (gas+stars combined),
    using a representative cored profile so M_bar(<R_core)=M_bar_core."""
    rr = np.linalg.norm(P, axis=1)
    # combined cored profile (same rc_gas core), normalized to M_bar_core at R_core
    def menc(r):
        x = r/rc_gas
        return np.arcsinh(x) - x/np.sqrt(1+x**2)
    Mb = M_bar_core * menc(rr)/menc(R_core)
    with np.errstate(divide='ignore', invalid='ignore'):
        gg = np.where(rr>0, G*Mb/rr**2, 0.0)
    return -(gg/np.maximum(rr,1e-30))[:,None] * P

# ---- total phantom mass inside R via Gauss flux of (nu-1) g_N over a sphere ---------------
def phantom_mass_enclosed(gfunc, R, n_ang=4000):
    """M_ph(<R) = -(1/4piG) * closed surface integral (nu-1) g_N . dA over sphere radius R.
       Outward normal n = r_hat; flux = integral (nu-1) g_N . r_hat dA.
       rho_ph integrates to -(1/4piG) * flux of (nu-1)gN (since rho_ph=-(1/4piG)div[(nu-1)gN]).
    """
    # Fibonacci sphere of directions
    i  = np.arange(n_ang) + 0.5
    ph = np.arccos(1 - 2*i/n_ang)
    th = np.pi*(1+5**0.5)*i
    nhat = np.column_stack([np.sin(ph)*np.cos(th), np.sin(ph)*np.sin(th), np.cos(ph)])
    P  = R * nhat
    g  = gfunc(P)                     # n_ang x 3
    gmag = np.linalg.norm(g, axis=1)
    nm1 = nu_minus_1(gmag)
    flux_integrand = (nm1[:,None]*g * nhat).sum(1)   # (nu-1) g . r_hat  (negative: g inward)
    mean_flux = flux_integrand.mean() * 4*np.pi*R**2  # surface integral
    # rho_ph = -(1/4piG) div[(nu-1)gN]; M_ph(<R)= integral rho_ph dV = -(1/4piG)*surface flux
    M_ph = -(1.0/(4*np.pi*G)) * mean_flux
    return M_ph

# ---- run both ways at multiple radii ------------------------------------------------------
radii = np.array([100, 200, 300, 420, 600, 1000, 1500]) * kpc
print(f"{'R(kpc)':>8} {'Mbar_enc(disc)':>16} {'Mph_DISCRETE':>14} {'Mph_SMOOTH':>12} "
      f"{'ratio D/S':>10}")
for R in radii:
    # enclosed baryon (discrete) for reference
    dgal = np.linalg.norm(gal_xyz, axis=1)
    Mbar_d = m_gal[dgal<R].sum() + (Mgas_enc(R) if R<=R_core else M_gas_core)
    Mph_d = phantom_mass_enclosed(gN_discrete, R)
    Mph_s = phantom_mass_enclosed(gN_smooth,   R)
    print(f"{R/kpc:8.0f} {Mbar_d/Msun:16.3e} {Mph_d/Msun:14.3e} {Mph_s/Msun:12.3e} "
          f"{Mph_d/Mph_s:10.3f}")

print("\n--- CORE (<420 kpc) verdict ---")
Mph_d = phantom_mass_enclosed(gN_discrete, R_core)
Mph_s = phantom_mass_enclosed(gN_smooth,   R_core)
print(f"DISCRETE/clumpy phantom in core: {Mph_d/Msun:.3e} Msun")
print(f"SMOOTH           phantom in core: {Mph_s/Msun:.3e} Msun")
print(f"OVERLAP excess (D - S): {(Mph_d-Mph_s)/Msun:.3e} Msun  = "
      f"{100*(Mph_d-Mph_s)/Mph_s:+.1f}% of smooth")
M_gap = 1.006e14 * Msun
print(f"Bare core gap to close: {M_gap/Msun:.3e} Msun")
print(f"Overlap excess closes {100*(Mph_d-Mph_s)/M_gap:+.1f}% of the bare gap")
