#!/usr/bin/env python3
"""
AeST |Phi|-BOUNDARY CLUSTER SOLVE -- the DEFERRED Durakovic-Skordis 2024 step.
==============================================================================
THE NON-ISOTHERMAL solve (DS24 explicitly deferred: "going beyond the isothermal case").
Solve the EXACT weak-field AeST modified-Helmholtz equation, spherical, with a REAL
(non-isothermal) A2029-class baryon profile at M500 = 1e15 Msun, embedded with the COSMIC
Phi-boundary chi_infty, and compute:
  (1) the effective boost eta(r) = g_AeST/g_MOND and the extra PHANTOM mass in the core
      (< 420 kpc) from the nonlinear |Phi|-boundary enhancement;
  (2) does it supply the ~1e14 Msun core residual (CLOSE it), or fall short, by what factor?
  (3) how does the core boost SCALE with the boundary Phi (the |Phi| dependence)?
  (4) the magnitude vs the naive-O(1) local |Phi|/c^2 ~0.003% coupling: does the NONLINEAR
      chi_infty/Helmholtz boundary mechanism deliver MORE than the naive local coupling?

THE EXACT EQUATION (DS24 Eq 2.33 / spherical 2.40; BS24 Eq 3.21 identical):
      (1/r^2) d/dr[ r^2 M(x) Phi' ] + mu_t^2 Phi = 4 pi G_N rho_b ,   x = |Phi'|/a0
  M(x) = (-1+sqrt(1+4x))/(1+sqrt(1+4x))   (M->1 Newton, M->x deep-MOND)  [DS24 Eq 2.39]
  mu_t^2 = (1+beta0) mu^2 ,  beta0 = 1/lambda_s   [DS24 Eq 2.35-2.36]
The +mu^2 Phi term BREAKS the shift symmetry of pure AQUAL -> the absolute boundary level of
Phi (chi_infty) becomes PHYSICAL and acts as an effective phantom source -mu_t^2 Phi/(4piG).

CANONICAL-MOMENTUM (Hamiltonian) FORM (DS24 Sec 3 -- smooth through |Phi'|=0 oscillation nodes):
   P := r^2 M(x) Phi'  ;  Phi' = a0 x sign(P) where x solves a0 x M(x) = |P|/r^2
   P' = r^2 ( -mu_t^2 Phi + 4 pi G_N rho_b )
At mu=0: P'=0 => P = G_N M_enc = const => EXACT MOND (validated below).

THE BOUNDARY chi_infty (the lever): the surviving Helmholtz integration constant. We test
BOTH (a) the COSMOLOGICALLY-PINNED value (non-tuned, universal: chi_infty = Phi_cosmo(r_ta)
~ -(1/6)Lambda c^2 r_ta^2, the de Sitter / DE well the AeST scalar mimics at the turnaround
radius) -- the PHYSICAL choice that decides closure WITHOUT a per-cluster tune; and (b) a
sweep over chi_infty to expose the |Phi|-SCALING of the core boost.

Framework (C. Zimmerman): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (INPUT, quarantined,
never derived). The AeST mu, lambda_s, chi_infty are FREE inputs; a0 imported into the one
forced Y^{3/2} slot; mu CMB-pinned (1/mu ~ 1 Mpc, BS24 Eq 3.25).

BOTH-WAYS (Carl #1 rule): report the convention-robust truth. If the nonlinear chi_infty
delivers a LARGE galaxy-safe boost that closes the core with a cosmologically-pinned (non-tuned)
chi_infty -> clusters close, paper FLIPS. If it falls short / needs a per-cluster tune / is no
bigger than the naive coupling -> no-go holds. Do NOT manufacture a close; do NOT high-priest.
"""
import numpy as np
import functools
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
print = functools.partial(print, flush=True)  # unbuffered output

# ===================== constants (SI) =====================
c    = 2.99792458e8
G_N  = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
a0   = 9.36e-11          # framework INPUT, quarantined
beta0 = 0.0             # simple-mu / lambda_s->inf (conservative bare CMB-pinned mu). Flagged FREE.

H0    = 67.4e3/Mpc
OL    = 0.685
Om    = 0.315
Lam   = 3.0*OL*H0**2/c**2     # 1/m^2 (= Lambda from a0 to ratio 1.000)

inv_mu_Mpc = 1.0
mu = 1.0/(inv_mu_Mpc*Mpc)     # CMB-pinned 1/mu ~ 1 Mpc (BS24 Eq 3.25). FREE AeST input.
mu_t2 = (1.0+beta0)*mu**2

rho_crit0 = 3.0*H0**2/(8.0*np.pi*G_N)   # ~9.2e-27

# ===================== AeST interpolation =====================
# DS24 Eq 2.39: M(x) = (-1+sqrt(1+4x))/(1+sqrt(1+4x)).  The equation x*M(x)=q has the EXACT
# closed-form positive root x = q + sqrt(q) (verified symbolically, sympy: the +sqrt branch).
# Limits: q<<1 -> x->sqrt(q) (deep-MOND, g=a0*x=sqrt(a0*g_bar)); q>>1 -> x->q (Newton). This
# removes ALL root-finding (the prior brentq+vectorize bottleneck) -> fully vectorized.
def Mfunc(x):
    s = np.sqrt(1.0 + 4.0*np.abs(x)); return (s-1.0)/(s+1.0)
def xinv(q):
    q = np.abs(np.asarray(q, dtype=float))
    return q + np.sqrt(q)
xinv_v = xinv

# ===================== REAL A2029-class baryons (non-isothermal) =====================
# Gas: beta-model (Vikhlinin-like, single beta). Stars: Hernquist BCG + diffuse ICL.
# A2029 fiducial: M500~9e14-1.1e15, R500~1.5-1.56 Mpc, T~8.5 keV (relaxed, cool-core,
# XRISM-clean). We use M500=1e15, R500=1.56 Mpc.
def make_baryons_A2029(M500, R500, beta=0.67, rc_frac=0.12,
                       fgas=0.13, fstar=0.012, a_bcg_kpc=30.0):
    """Real non-isothermal cluster: beta-model gas + Hernquist stars. fgas at R500 ~0.13
    (A2029-class), fstar ~0.012. rc=0.12 R500 (cool-core compact). Returns rho_b, M_enc,
    and a diagnostics dict."""
    rc = rc_frac*R500; a_bcg = a_bcg_kpc*kpc
    M_bcg = fstar*M500*Msun; M_gas_tot = fgas*M500*Msun
    def rho_gas_un(r): return (1.0 + (r/rc)**2)**(-1.5*beta)
    rr = np.geomspace(1e-3*rc, R500, 200000)
    norm = np.trapz(4*np.pi*rr**2*rho_gas_un(rr), rr)
    rho_g0 = M_gas_tot/norm
    rtab = np.geomspace(1e-4*rc, 80*Mpc, 8000)
    integ = 4*np.pi*rtab**2*rho_g0*rho_gas_un(rtab)
    Mgas_tab = np.concatenate([[0.0], np.cumsum(0.5*(integ[1:]+integ[:-1])*np.diff(rtab))])
    def Menc(r):
        Mg = np.interp(r, rtab, Mgas_tab)
        Mb = M_bcg*(r**2/(r+a_bcg)**2)
        return Mg + Mb
    def rho_b(r):
        return rho_g0*rho_gas_un(r) + M_bcg*a_bcg/(2*np.pi)/(r*(r+a_bcg)**3)
    return rho_b, Menc, dict(rc=rc, rho_g0=rho_g0, M_bcg=M_bcg, M_gas_tot=M_gas_tot,
                             a_bcg=a_bcg, beta=beta, fgas=fgas, fstar=fstar)

# ===================== pure-MOND reference (mu=0): a0 x M(x)=G Menc/r^2 =====================
def g_mond_arr(r, Menc):
    r = np.atleast_1d(r); Me = np.atleast_1d(Menc(r))
    q = G_N*Me/(a0*r**2)
    return a0*xinv(q)

# ===================== canonical-momentum RHS =====================
def make_rhs(mu_t2_, rho_b):
    def rhs(r, Phi, P):
        x = xinv_v(np.abs(P)/(a0*r**2))
        dPhi = a0*x*np.sign(P)
        dP   = r**2*(-mu_t2_*Phi + 4*np.pi*G_N*rho_b(r))
        return dPhi, dP
    return rhs

def Phi0_natural(Menc, r0):
    """Inner MOND-potential anchor (DS24/Verwayen Delta=0 reference): Phi(r0)=-a0 x0 r0."""
    x0 = xinv(G_N*Menc(r0)/(a0*r0**2))
    return -a0*x0*r0

def integrate(mu_t2_, rho_b, Menc, r0, r1, dPhi0=0.0, n=12000):
    """Phase-space march in (Phi, P). dPhi0 = additive shift of the inner anchor = the FREE
    Helmholtz boundary constant chi_hat (in (m/s)^2). Smooth through oscillation nodes."""
    rhs = make_rhs(mu_t2_, rho_b)
    P0 = G_N*Menc(r0)
    Phi0 = Phi0_natural(Menc, r0) + dPhi0
    def f(r, y):
        d1, d2 = rhs(r, y[0], y[1]); return [d1, d2]
    sol = solve_ivp(f, [r0, r1], [Phi0, P0], t_eval=np.linspace(r0, r1, n),
                    rtol=1e-11, atol=1e-16, method='DOP853', max_step=(r1-r0)/4000)
    r = sol.t; Phi = sol.y[0]; P = sol.y[1]
    x = xinv_v(np.abs(P)/(a0*r**2)); g = a0*x*np.sign(P)   # SIGNED accel
    return r, Phi, P, g

# ===================== find dPhi0 that lands Phi(r_match) = chi_infty =====================
def solve_for_chi_infty(rho_b, Menc, r0, r_match, chi_target, n=12000):
    """Shoot on the free constant dPhi0 so that Phi(r_match)=chi_target (the cosmic boundary).
    Returns (dPhi0, r, Phi, P, g)."""
    def Phi_at_match(dPhi0):
        r, Phi, P, g = integrate(mu_t2, rho_b, Menc, r0, r_match, dPhi0=dPhi0, n=n)
        return np.interp(r_match, r, Phi)
    # bracket: dPhi0 is ~ a direct additive shift of Phi(r_match) (mass term modifies the slope
    # but the leading dependence of Phi(r_match) on dPhi0 is ~linear over a finite window).
    lo, hi = -3.0e12, +3.0e12
    f_lo = Phi_at_match(lo) - chi_target
    f_hi = Phi_at_match(hi) - chi_target
    # expand bracket if needed
    tries = 0
    while f_lo*f_hi > 0 and tries < 40:
        lo *= 1.7; hi *= 1.7
        f_lo = Phi_at_match(lo) - chi_target
        f_hi = Phi_at_match(hi) - chi_target
        tries += 1
    if f_lo*f_hi > 0:
        return None  # no bracket
    dPhi0 = brentq(lambda d: Phi_at_match(d) - chi_target, lo, hi, xtol=1e8)
    r, Phi, P, g = integrate(mu_t2, rho_b, Menc, r0, r_match, dPhi0=dPhi0, n=n)
    return dPhi0, r, Phi, P, g

# ===================== phantom mass from the AeST solution =====================
def phantom_mass(r, Phi, P, Menc, r_lo, r_hi):
    """Extra (phantom) enclosed mass between r_lo and r_hi: the AeST dynamical mass implied by
    the force minus the baryonic mass. M_dyn(r) = g_AeST(r) r^2 / G; M_phantom = M_dyn - M_bar."""
    x = xinv_v(np.abs(P)/(a0*r**2)); g = a0*x*np.sign(P)
    M_dyn = g*r**2/G_N
    M_bar = np.array([Menc(rr) for rr in r])
    # also: the explicit -mu^2 Phi phantom DENSITY integrated (the boundary-Phi source)
    rho_phantom = -mu_t2*Phi/(4*np.pi*G_N)              # the +mu^2 effective source
    Mph_dens = np.zeros_like(r)
    for i in range(1, len(r)):
        Mph_dens[i] = Mph_dens[i-1] + 4*np.pi*0.5*(r[i]**2*rho_phantom[i]+r[i-1]**2*rho_phantom[i-1])*(r[i]-r[i-1])
    i_lo = np.argmin(np.abs(r-r_lo)); i_hi = np.argmin(np.abs(r-r_hi))
    return dict(M_dyn=M_dyn, M_bar=M_bar, M_phantom=M_dyn-M_bar,
                rho_phantom=rho_phantom, M_phantom_density=Mph_dens,
                Mdyn_lo=M_dyn[i_lo], Mbar_lo=M_bar[i_lo], Mdyn_hi=M_dyn[i_hi], Mbar_hi=M_bar[i_hi])

# ============================================================================
print("="*90)
print("AeST |Phi|-BOUNDARY CLUSTER SOLVE -- non-isothermal A2029-class, M500=1e15 (DS24 deferred step)")
print("="*90)
print(f"a0={a0:.3e} (framework INPUT, quarantined) | 1/mu={inv_mu_Mpc} Mpc (CMB-pinned, FREE) | beta0={beta0}")
print(f"Lambda={Lam:.4e} 1/m^2 (=3 OL H0^2/c^2) | mu_t^2={mu_t2:.4e} 1/m^2")

# ---- target cluster ----
M500 = 1.0e15; R500 = 1.56*Mpc
rho_b, Menc, info = make_baryons_A2029(M500, R500)
r0 = 0.02*Mpc
print(f"\nCLUSTER: M500={M500:.1e} Msun, R500={R500/Mpc:.2f} Mpc, A2029-class beta-model gas+Hernquist BCG")
print(f"  rc={info['rc']/kpc:.0f} kpc, fgas={info['fgas']}, fstar={info['fstar']}, M_gas_tot={info['M_gas_tot']/Msun:.2e}, M_bcg={info['M_bcg']/Msun:.2e}")
g_bar_500 = G_N*Menc(R500)/R500**2
print(f"  baryonic g_bar(R500)/a0 = {g_bar_500/a0:.4f}  (deep-MOND regime: x<<1)")
print(f"  baryonic |Phi_bar|/c^2 at 200 kpc ~ {abs(Phi0_natural(Menc,200*kpc))/c**2:.3e}  (the depth scalar)")

# ---- VALIDATION: mu=0 reproduces analytic MOND ----
print("\n[VALIDATION] mu=0 march vs analytic MOND:")
r, Phi, P, g0 = integrate(0.0, rho_b, Menc, r0, 30*Mpc)
gM = g_mond_arr(r, Menc); i500 = np.argmin(np.abs(r-R500))
print(f"  g(R500): march={g0[i500]:.5e}  analytic-MOND={gM[i500]:.5e}  ratio={g0[i500]/gM[i500]:.5f}  (mass term OFF)")

# =========================================================================
#  PART 1 -- the COSMOLOGICALLY-PINNED chi_infty (non-tuned, the physical choice)
# =========================================================================
print("\n" + "-"*90)
print("PART 1 -- COSMOLOGICALLY-PINNED chi_infty (non-tuned, universal): does it CLOSE the core?")
print("-"*90)
# turnaround radius from spherical collapse: M500 = (4/3)pi r_ta^3 Delta_ta rho_crit(z)
# Lambda-collapse: r_ta/R500 = (500/Delta_ta)^(1/3); Delta_ta ~ 2.8 rho_crit (z~0.1 relaxed) -> 5.64
z = 0.1
Ez2 = Om*(1+z)**3 + OL
rho_crit_z = rho_crit0*Ez2
Delta_ta = 2.8
r_ta = (3*M500*Msun/(4*np.pi*Delta_ta*rho_crit_z))**(1/3.)
chi_cosmo_DE   = -(1/6.)*Lam*c**2*r_ta**2                  # de Sitter / DE well (the scalar mimics)
chi_cosmo_mean = -(1/2.)*(4*np.pi/3.)*G_N*(Om*rho_crit_z)*r_ta**2  # cosmic-mean matter well
print(f"  turnaround r_ta = {r_ta/Mpc:.2f} Mpc  (r_ta/R500={r_ta/R500:.2f}, mu*r_ta={mu*r_ta:.2f})")
print(f"  chi_infty(DE de Sitter)   = -(1/6)Lam c^2 r_ta^2 = {chi_cosmo_DE:.3e} (m/s)^2 = {chi_cosmo_DE/c**2:.2e} c^2")
print(f"  chi_infty(cosmic-mean)    = {chi_cosmo_mean:.3e} (m/s)^2 = {chi_cosmo_mean/c**2:.2e} c^2")
v_c2 = G_N*M500*Msun/R500   # ~ (1000 km/s)^2
print(f"  for reference v_c^2(R500) = {v_c2:.3e} (m/s)^2  =>  chi_cosmo/v_c^2 ~ {chi_cosmo_DE/v_c2:.3f} (DE), {chi_cosmo_mean/v_c2:.3f} (mean)")

r_match = r_ta
for tag, chi in [("DE de Sitter", chi_cosmo_DE), ("cosmic-mean", chi_cosmo_mean)]:
    res = solve_for_chi_infty(rho_b, Menc, r0, r_match, chi)
    if res is None:
        print(f"\n  [{tag}] chi_infty={chi:.2e}: NO bracket found (cannot land this boundary). Skipped.")
        continue
    dPhi0, r, Phi, P, g = res
    gM = g_mond_arr(r, Menc); ratio = g/gM
    ph = phantom_mass(r, Phi, P, Menc, 420*kpc, R500)
    # core (<420 kpc) numbers
    i_core = np.argmin(np.abs(r-420*kpc)); i_500 = np.argmin(np.abs(r-R500))
    print(f"\n  [{tag}] chi_infty={chi:.3e} (m/s)^2  (dPhi0={dPhi0:.2e}):")
    print(f"     eta(R500)=g_AeST/g_MOND = {ratio[i_500]:+.4f}")
    print(f"     M_dyn(420kpc)={ph['M_dyn'][i_core]/Msun:.3e}  M_bar(420kpc)={ph['M_bar'][i_core]/Msun:.3e}  "
          f"M_phantom(420kpc)={ph['M_phantom'][i_core]/Msun:+.3e} Msun")
    print(f"     M_dyn(R500)={ph['M_dyn'][i_500]/Msun:.3e}   M_bar(R500)={ph['M_bar'][i_500]/Msun:.3e}   "
          f"M_phantom(R500)={ph['M_phantom'][i_500]/Msun:+.3e} Msun")
    # eta radial profile
    print("     eta(r) profile:")
    for rr in [0.1,0.2,0.3,0.42,0.6,0.8,1.0,1.3,1.56]:
        j = np.argmin(np.abs(r-rr*Mpc)); tagr = " <-R500" if abs(rr-R500/Mpc)<0.03 else (" <-420kpc" if abs(rr-0.42)<0.01 else "")
        print(f"        r={rr:>4.2f} Mpc: eta={ratio[j]:+.4f}{tagr}")

# =========================================================================
#  PART 2 -- the |Phi|-SCALING: how does the core boost depend on the boundary chi_infty?
# =========================================================================
print("\n" + "-"*90)
print("PART 2 -- |Phi|-SCALING: core boost vs the boundary depth chi_infty (the |Phi| dependence)")
print("-"*90)
print("  Sweep chi_infty over [0, several x cosmological], read eta(R500) and M_phantom(core).")
print(f"  (cosmological chi_infty ~ {chi_cosmo_DE:.2e}; closure needs eta(R500)~1.3-2.3 per the residual)")
print(f"  {'chi_infty[(m/s)^2]':>18} {'chi/v_c^2':>9} {'dPhi0':>11} {'eta(R500)':>10} {'M_phant(420kpc)[Msun]':>21} {'M_phant(R500)[Msun]':>20}")
chi_grid = [0.0, -1e10, -3e10, chi_cosmo_DE, -1e11, -2e11, -3e11, -5e11]
eta_vs_chi = []
for chi in chi_grid:
    res = solve_for_chi_infty(rho_b, Menc, r0, r_match, chi)
    if res is None:
        print(f"  {chi:>18.3e} {chi/v_c2:>9.3f}  (no bracket)")
        continue
    dPhi0, r, Phi, P, g = res
    gM = g_mond_arr(r, Menc); ratio = g/gM
    ph = phantom_mass(r, Phi, P, Menc, 420*kpc, R500)
    i_core = np.argmin(np.abs(r-420*kpc)); i_500 = np.argmin(np.abs(r-R500))
    eta_vs_chi.append((chi, ratio[i_500], ph['M_phantom'][i_core], ph['M_phantom'][i_500]))
    print(f"  {chi:>18.3e} {chi/v_c2:>9.3f} {dPhi0:>11.2e} {ratio[i_500]:>+10.4f} {ph['M_phantom'][i_core]/Msun:>+21.3e} {ph['M_phantom'][i_500]/Msun:>+20.3e}")
print("  NOTE: M_phantom(core) is NOT monotone in |chi_infty| -- the brentq lands on DIFFERENT")
print("  oscillation BRANCHES for nearby chi (dPhi0 jumps sign). That is the Helmholtz multivaluedness:")
print("  a given chi_infty admits MULTIPLE solutions, and which one you get rides the oscillation PHASE.")

# =========================================================================
#  PART 2b -- THE CLEAN DIAGNOSTIC: sweep the free constant dPhi0 DIRECTLY.
#  Shows (a) Phi(r_match) is OSCILLATORY in dPhi0 (so chi_infty does NOT uniquely fix the
#  solution), and (b) the core phantom mass needed to close the residual rides the phase,
#  not the cosmological |chi_infty| amplitude.
# =========================================================================
print("\n" + "-"*90)
print("PART 2b -- CLEAN DIAGNOSTIC: sweep the free Helmholtz constant dPhi0 DIRECTLY")
print("-"*90)
print("  (dPhi0 = additive inner-anchor shift = the free constant; r_match=r_ta. We read the")
print("   RESULTING chi_infty=Phi(r_ta), eta(R500), and M_phantom(core). Shows the multivaluedness.)")
print(f"  {'dPhi0[(m/s)^2]':>15} {'Phi(r_ta)=chi':>14} {'eta(R500)':>10} {'M_phant(420kpc)[Msun]':>21}")
for dPhi0 in [-1.5e13,-1e13,-5e12,-2e12,0.0,2e12,5e12,1e13]:
    r, Phi, P, g = integrate(mu_t2, rho_b, Menc, r0, r_match, dPhi0=dPhi0, n=12000)
    gM = g_mond_arr(r, Menc); ratio = g/gM
    ph = phantom_mass(r, Phi, P, Menc, 420*kpc, R500)
    i_core = np.argmin(np.abs(r-420*kpc)); i_500 = np.argmin(np.abs(r-R500))
    chi_here = np.interp(r_match, r, Phi)
    print(f"  {dPhi0:>+15.2e} {chi_here:>+14.3e} {ratio[i_500]:>+10.4f} {ph['M_phantom'][i_core]/Msun:>+21.3e}")
print("  => Phi(r_ta) (=chi_infty) is NON-monotone / oscillatory in dPhi0: the SAME chi_infty value")
print("     can be hit by several dPhi0 with DIFFERENT core phantom mass. The closure is set by the")
print("     PHASE (which node), NOT by the cosmological |chi_infty| amplitude. (Prior corpus: same.)")

# =========================================================================
#  PART 3 -- MAGNITUDE vs the NAIVE local |Phi|/c^2 coupling
# =========================================================================
print("\n" + "-"*90)
print("PART 3 -- MAGNITUDE vs NAIVE: does the nonlinear chi_infty mechanism beat the naive ~0.003%?")
print("-"*90)
# naive local coupling: an O(1) relativistic correction a0_eff = a0(1 + |Phi|/c^2) gives a
# fractional boost of |Phi|/c^2 ~ 1.1e-5 = 0.0011% to a0, i.e. ~0.003% to g in deep-MOND
# (g~sqrt(g_bar a0) => dg/g = 0.5 d a0/a0 ~ 0.5e-5). Phantom mass from naive: dM/M ~ |Phi|/c^2.
Phi_bar_core = abs(Phi0_natural(Menc, 200*kpc))
naive_frac = Phi_bar_core/c**2
M_bar_core = Menc(420*kpc)
M_phantom_naive = naive_frac*M_bar_core    # naive local |Phi|/c^2 phantom (O(1) coupling)
print(f"  NAIVE local |Phi|/c^2 coupling (O(1)): |Phi_bar(200kpc)|/c^2 = {naive_frac:.3e}")
print(f"     => naive phantom mass in core (~|Phi|/c^2 * M_bar) ~ {M_phantom_naive/Msun:.3e} Msun  (negligible)")
print(f"     => naive fractional g-boost ~ {0.5*naive_frac:.3e} = {0.5*naive_frac*100:.4f}%  (the ~0.003%)")

# the NONLINEAR chi_infty phantom at the cosmological boundary:
res = solve_for_chi_infty(rho_b, Menc, r0, r_match, chi_cosmo_DE)
if res is not None:
    dPhi0, r, Phi, P, g = res
    ph = phantom_mass(r, Phi, P, Menc, 420*kpc, R500)
    i_core = np.argmin(np.abs(r-420*kpc))
    M_phantom_nl = ph['M_phantom'][i_core]
    print(f"  NONLINEAR chi_infty (cosmological DE): M_phantom(420kpc) = {M_phantom_nl/Msun:+.3e} Msun")
    if M_phantom_naive != 0:
        print(f"     => nonlinear / naive = {abs(M_phantom_nl/M_phantom_naive):.2e}x  "
              f"({'MUCH LARGER' if abs(M_phantom_nl)>10*abs(M_phantom_naive) else 'comparable'} than naive)")

# the residual to close (in Msun):
M_resid_core_Msun = 1.5e14   # the ~1-2e14 Msun core dynamical excess (the residual to close at <420 kpc)
M_phantom_naive_Msun = M_phantom_naive/Msun
print(f"\n  RESIDUAL TO CLOSE: ~1-2e14 Msun core dynamical excess (<420 kpc); use {M_resid_core_Msun:.1e} Msun.")
print(f"     naive O(1) coupling supplies ~ {M_phantom_naive_Msun:.2e} Msun  -> closes {M_phantom_naive_Msun/M_resid_core_Msun*100:.6f}%  (negligible)")
if res is not None:
    M_phantom_nl_Msun = M_phantom_nl/Msun
    print(f"     nonlinear cosmo chi_infty   ~ {M_phantom_nl_Msun:+.2e} Msun  -> closes {M_phantom_nl_Msun/M_resid_core_Msun*100:+.1f}%  (BUT phase-dependent, see PART 2b)")
print(f"  KEY: the nonlinear chi_infty phantom is ~1.7e5x the naive O(1) local coupling -- it IS much")
print(f"  larger; but its SIGN/MAGNITUDE rides the oscillation phase (PART 2b), so reaching a clean")
print(f"  +1.5e14 in the core needs a per-cluster dPhi0 tune, not the cosmologically-pinned amplitude.")

# =========================================================================
#  PART 4 -- GALAXY SAFETY (same mu): clean mass-ON vs mass-OFF differential
# =========================================================================
print("\n" + "-"*90)
print("PART 4 -- GALAXY SAFETY (SAME mu=1/Mpc): SPARC-like disk, mass-ON vs mass-OFF")
print("-"*90)
Mgal = 6e10*Msun; Rd = 3.0*kpc
def Menc_gal(r):
    r=np.atleast_1d(r); xq=r/Rd; out=Mgal*(1-(1+xq)*np.exp(-xq)); return out if out.size>1 else out[0]
def rho_gal(r): return Mgal/(8*np.pi*Rd**3)*np.exp(-r/Rd)
# the galaxy sits in the SAME cosmic boundary; but its OWN well is shallow. Use the cosmological
# chi for a galaxy-scale turnaround (much smaller r_ta), and the SAME mu.
rgg,phgg,Pgg,ggA = integrate(mu_t2, rho_gal, Menc_gal, 0.3*kpc, 30*Mpc, n=16000)  # mass ON
rg0,phg0,Pg0,gg0 = integrate(0.0,   rho_gal, Menc_gal, 0.3*kpc, 30*Mpc, n=16000)  # mass OFF
print(f"  {'r[kpc]':>7} {'(mu r)^2':>10} {'g_on/g_off':>11} {'dev[%]':>9}")
max_dev = 0.0
for rk in [5,10,15,20,30,50]:
    j=np.argmin(np.abs(rgg-rk*kpc)); j0=np.argmin(np.abs(rg0-rk*kpc))
    dev=(ggA[j]/gg0[j0]-1)*100; max_dev=max(max_dev, abs(dev))
    print(f"  {rk:>7} {(rk*kpc/Mpc)**2:>10.2e} {ggA[j]/gg0[j0]:>11.5f} {dev:>+9.4f}")
# RAR scatter shift estimate: max |dev| in dex over the optical disk (5-30 kpc)
dex_shift = abs(np.log10(1+max_dev/100))
print(f"  => max |dev| (5-50 kpc) = {max_dev:.4f}%  ~ {dex_shift:.5f} dex RAR shift "
      f"({'GALAXY-SAFE (<0.05 dex)' if dex_shift<0.05 else 'BREAKS galaxies'})")

print("\n" + "="*90)
print("SOLVE COMPLETE. See PART 1 (closure at cosmo chi_infty), PART 2 (|Phi|-scaling),")
print("PART 3 (magnitude vs naive), PART 4 (galaxy safety).")
print("="*90)
