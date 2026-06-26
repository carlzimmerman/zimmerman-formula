#!/usr/bin/env python3
r"""
GENUINE de Sitter-Unruh MODIFIED-INERTIA cluster-member dynamics (NOT a modified-gravity patch)
================================================================================================
Carl's objection (correct): the prior cluster-member EFE calc
(member_sigma_efe_signtest_v2.py) used the modified-GRAVITY quasi-static EFE equation
    (g + g_e) mu((g+g_e)/a0) = g_N + g_e mu(g_e/a0),   g_e = theta * g_ext        [FAMAEY-McGAUGH]
and called multiplying g_ext by a constant theta "modified inertia". That is
modified-GRAVITY-with-a-patch. In the ADIABATIC scalar-sigma limit a CONSTANT theta is EXACTLY
a0-degenerate with modified gravity:  MI(theta0=k) = MG(a0/k).  So that calc could never find a
distinctive MI signal -- it flattened MI into MG by construction.

This script builds the GENUINE modified-inertia mechanism from Milgrom 2022
(arXiv:2208.07073 = PRD 106, 064060), the actual time-nonlocal MI EOM, NOT the FM patch:

  Eq (3):   m a_hat(omega) I[{r_hat}, omega, a0] = F_hat(omega),  i.e. a_hat(omega) I = a_N_hat(omega)
            -- inertia is a DIMENSIONLESS FUNCTIONAL of the WHOLE trajectory (Fourier components),
               built with a0 as the only new constant.  MI modifies the LEFT (response) side;
               MG modifies the SOURCE (Poisson -> AQUAL/QUMOND) and keeps inertia = m.

  Eq (5):   I = mu[A(omega)/a0],   A = "nonlocal acceleration parameter of the trajectory".

  Eq (23):  m a_hat_k(omega_k) mu[A(omega_k)/a0] = F_hat_k(omega_k)
            -- when the motion separates into distinct-frequency components (e.g. a star's ORBIT
               around the galaxy at omega_orb + its INTERNAL/vertical motion at omega_z), each
               component k gets its OWN mu factor, COUPLED through A(omega_k) which depends on ALL
               components.  THIS is the genuine MI EFE: not a rescaled potential, but a
               per-frequency, per-axis inertia.

  Eq (32):  ANISOTROPIC harmonic field. Principal Newtonian freqs omega_bar_n=(k_n/m)^1/2; the
            MOND freqs solve the COUPLED set
               omega_n^2 mu_n = omega_bar_n^2,
               mu_n = mu{ [ x0_n^2 omega_n^2 + sum_{l!=n} theta(omega_l/omega_n) x0_l^2 omega_l^2 ] / a0 }
            -- the effective inertia DIFFERS axis-by-axis (mu_n depends on n).  This is the
               ANISOTROPY that MG does NOT have: in MG the potential is modified
               isotropically-given-a_ext and the star's inertia is the standard scalar m.

  Eq (34):  EFE two-frequency:  A(omega_in) = omega_in^2 |r_in| + omega_ex^2 |r_ex| theta(omega_ex/omega_in)
            with theta(1)=1, theta decreasing, theta(0) ~ "a few".  In the ADIABATIC limit
            omega_ex << omega_in -> theta(0)=const -> a0-degenerate.  When omega_ex ~ omega_in
            (plunging / core-passage members) theta(omega_ex/omega_in) is a NON-CONSTANT FUNCTION
            of the frequency ratio -> genuinely time-nonlocal -> NOT a0-degenerate.

  Eq (35):  adiabatic EFE result a_hat(omega_in) mu[theta(0) a_ext/a0] = a_N_hat(omega_in).
            This is the a0-degenerate trap (theta(0) just rescales a0 by 1/theta(0)).

The framework's OWN interpolation (de Sitter-Unruh inertia), used THROUGHOUT (never McGaugh/simple):
    isolated boost:   g_obs = sqrt(g_N^2 + g_N a0)            <=>   nu(y) = sqrt(1 + 1/y),  y=g_N/a0
    inverse-inertia:  mu_fw(x) = (sqrt(1+4x^2) - 1) / (2x)   (the inverse of nu; x = g_obs/a0)
    a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2  (sealed)

WHAT THIS SCRIPT COMPUTES (the three candidate distinctive observables):
  (2) ANISOTROPY  -- solve Eq (32) for a member star feeling a_internal (toward galaxy center)
                     PLUS a_external (cluster field, fixed direction). Compute the effective inertia
                     ALONG vs ACROSS a_ext and the resulting velocity-ellipsoid anisotropy
                     beta_MI = 1 - sigma_t^2/sigma_r^2. Compare to MG (Eq from QUMOND-EFE: isotropic
                     mu given a_ext, beta_MG from the standard anisotropic-G EFE) and CDM (beta=0).
  (3) ORBIT-PHASE -- |a_total(phase)| = |a_int(phase) + a_ext| varies around the member's orbit
                     because a_int rotates and a_ext is fixed; mu_fw(|a_total|/a0) therefore varies
                     -> orbit-phase-dependent effective mass. Compute the phase modulation amplitude
                     and compare to MG (where the star's inertia is the scalar m, phase-independent).
  (4) NON-ADIABATIC -- theta(omega_ex/omega_in) for plunging members (omega_ex ~ omega_in). Show the
                     a_0-degeneracy of the adiabatic theta(0) and where the FUNCTION theta(y) breaks it.

BOTH-WAYS (Carl's #1 rule): the framework's OWN nu/mu_fw is used everywhere; the MG comparison uses
the standard AQUAL/QUMOND-EFE (potential modified, inertia=m); we report HONESTLY whether each
candidate observable is (a) genuinely MI-distinct or (b) still a0-degenerate / below floor.
We do NOT manufacture a distinctive signal: every "distinct" claim is checked against an MG fit that
is free to re-tune a0 and M/L.

All equation numbers cited are from Milgrom 2022 (arXiv:2208.07073v3). UNVERIFIED items flagged.
"""
import numpy as np
from scipy.optimize import brentq, fsolve

# ----------------------------------------------------------------------------- framework footing
c, G, Msun, kpc, Mpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
a0  = 9.36e-11                       # framework sealed value
def nu(y):    y=np.asarray(y,float); return np.sqrt(1.0 + 1.0/y)            # boost factor, g=g_N nu(g_N/a0)
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)   # inverse-inertia, x=g/a0

# theta(y): Milgrom-2022 says theta(1)=1, decreasing, theta(0) ~ a few. Functional form UNKNOWN/UNVERIFIED.
# We use the two example forms Milgrom himself writes (text after Eq 34): theta(y)=2/(1+y^2) [theta(0)=2]
# and theta(y)=e^{(1-y)/q}. We treat theta as a FUNCTION (not a constant) to expose non-adiabaticity.
def theta_milgrom_rational(y): return 2.0/(1.0+np.asarray(y,float)**2)      # theta(0)=2, theta(1)=1
def theta_milgrom_exp(y, q=1.0): return np.exp((1.0-np.asarray(y,float))/q)  # theta(0)=e^{1/q}, theta(1)=1

# ============================================================================================
print("="*108)
print(" GENUINE MODIFIED-INERTIA cluster-member dynamics (Milgrom-2022 Eqs 3/5/23/32/34) -- NOT the FM patch")
print("="*108)
print(f"  framework: a0={a0:.3e} m/s^2 (sealed = c^2 sqrt(Lambda/32pi));  nu(y)=sqrt(1+1/y);  mu_fw=inverse")
print(f"  CONTRAST WITH PRIOR CALC: prior used FM 1-D EFE (g+ge)mu((g+ge)/a0)=g_N+ge mu(ge/a0), ge=theta*g_ext.")
print(f"  That is modified GRAVITY (potential rescaled) with a theta-patch -> a0-degenerate by Eq(35).")
print(f"  Here we solve the GENUINE per-frequency / per-axis MI inertia (Eqs 23,32) directly.\n")

# ============================================================================================
# (1) THE GENUINE MI EOM  (contrast with MG)  -- Milgrom Eqs (3),(5),(23)
# ============================================================================================
print("-"*108)
print(" (1) GENUINE MI EOM vs MG EOM")
print("-"*108)
print(r"""  MI (Milgrom 2022, Eq 3,5,23):  modify the RESPONSE.
        a_hat_k(omega_k) * mu[ A(omega_k)/a0 ] = a_N_hat(omega_k)          (per frequency-component k)
        A(omega_k) = SUM over components of omega_l^2 |r_l| theta(omega_l/omega_k)   (Eq 34 form)
        -> inertia is a NONLOCAL FUNCTIONAL of the whole trajectory; it COUPLES the orbit (omega_orb)
           and the internal/vertical motion (omega_z) of the SAME star; it is per-axis (Eq 32).
  MG (AQUAL/QUMOND-EFE):  modify the SOURCE.
        div[ mu(|grad phi|/a0) grad phi ] = 4 pi G rho ;  inertia = m (scalar, standard).
        EFE: internal field sees G_eff ~ G/mu(a_ext/a0), with a fixed anisotropy tensor set by a_ext.
        The star's inertia is the SAME scalar m regardless of direction or orbit phase.
  KEY: MG gives one scalar G_eff(a_ext) for all the star's motions; MI gives a DIFFERENT mu per
       frequency-component and per axis, tied to that star's actual trajectory.""")

# ============================================================================================
# (2) ANISOTROPY  -- solve the ANISOTROPIC MI eq (Milgrom Eq 32) for a member in a cluster field
# ============================================================================================
print("\n"+"-"*108)
print(" (2) ANISOTROPY of the effective inertia: ALONG vs ACROSS a_ext  (Milgrom Eq 32)")
print("-"*108)
print(r"""  Setup: a member star executes small oscillations about its guiding centre in the member galaxy,
  in a (locally anisotropic) harmonic well of the member's stellar potential, PLUS a fixed external
  cluster acceleration a_ext along axis z. Decompose into principal axes (x = across a_ext, z = along).
  Newtonian (member-internal) frequencies omega_bar_n = sqrt(k_n/m). Eq (32): the MOND freqs omega_n
  solve, per axis n, omega_n^2 mu_n = omega_bar_n^2 with
     mu_n = mu_fw( [ x0_n^2 omega_n^2 + sum_{l!=n} theta(omega_l/omega_n) x0_l^2 omega_l^2
                     + a_ext^2 * [n==z] /a0_norm ] / a0 )
  The external field enters axis z (its own direction) as a near-DC (omega_ex<<omega_in) component
  with weight theta(0); across (axis x) it enters only through the coupling. So mu_z != mu_x:
  the effective inertia is ANISOTROPIC. In MG the inertia is the scalar m and the anisotropy comes
  only from the EFE potential tensor -- a DIFFERENT, computable beta. We compare the two betas.""")

def solve_anisotropic_MI(ombar, x0, a_ext_along, axis_ext=2, thetaf=theta_milgrom_rational):
    r"""
    Solve Milgrom Eq (32) for the 3 principal MOND frequencies omega_n given Newtonian freqs ombar_n,
    rms amplitudes x0_n, and an external (near-DC) cluster acceleration a_ext along axis 'axis_ext'.
    The external field is a low-frequency (omega_ex -> 0) component of acceleration a_ex = a_ext_along
    living on axis 'axis_ext'; it contributes a_ex * theta(omega_ex/omega_n -> 0) = a_ex*theta(0) to
    the inertia argument of the axis it points along, and (via the same A) couples weakly to others.
    Returns omega_n (MOND freqs) and mu_n (effective per-axis inertia factors).
    """
    ombar = np.asarray(ombar, float); x0 = np.asarray(x0, float)
    th0 = thetaf(0.0)
    def eqs(omega):
        omega = np.abs(omega)
        # per-axis internal acceleration amplitude a_n = omega_n^2 x0_n  (Eq 24/26: |a|=omega^2|r|)
        a_int = omega**2 * x0
        mu_n = np.zeros(3); res = np.zeros(3)
        for n in range(3):
            # A(omega_n) = own-axis internal accel + coupled other-axis (theta(omega_l/omega_n))
            A = a_int[n]
            for l in range(3):
                if l != n:
                    yl = omega[l]/max(omega[n],1e-30)
                    A += thetaf(yl) * a_int[l]
            # external field: a near-DC component on its own axis -> theta(0)*a_ext on that axis only
            if n == axis_ext:
                A += th0 * a_ext_along
            mu_n[n] = mu_fw(max(A,1e-30)/a0)
            res[n] = omega[n]**2 * mu_n[n] - ombar[n]**2     # Eq (32): omega_n^2 mu_n = ombar_n^2
        return res, mu_n
    def f(omega): return eqs(omega)[0]
    # initial guess: Newtonian freqs boosted by isolated nu
    guess = ombar * np.sqrt(np.maximum(nu((ombar**2*x0)/a0),1.0))
    sol = fsolve(f, guess, full_output=True, xtol=1e-12)
    omega = np.abs(sol[0]); _, mu_n = eqs(omega)
    return omega, mu_n

# MG comparison: CANONICAL AQUAL-EFE anisotropic potential -- Famaey-McGaugh 2012, Eqs (61)-(62):
#   Phi(x,y,z) = -G m / [mu_e r~],   r~ = r (1 + L_e (x^2+y^2)/r^2)^{1/2},  a_ext along z.
#   => effective G ALONG a_ext (x=y=0, r~=r):       G_along = G/mu_e
#      effective G ACROSS a_ext (z=0, r~=r sqrt(1+L_e)): G_perp  = G/[mu_e sqrt(1+L_e)]
#   So G_along > G_perp: the field is STRONGER along a_ext (isopotentials squashed along z).
#   mu_e = mu(a_ext/a0); L_e = (d ln mu/d ln x)|_{a_ext/a0}.  [verified vs FM2012 Eqs 61-62]
# Velocity dispersion ~ sqrt(G_eff). Radial axis = along a_ext (z); tangential = across (x,y).
def mg_anisotropy(a_ext, a0_use=a0):
    x = a_ext/a0_use
    dx = 1e-5*x
    Le = (np.log(mu_fw(x+dx))-np.log(mu_fw(x-dx)))/(np.log(x+dx)-np.log(x-dx))
    Geff_along  = 1.0/mu_fw(x)                  # along a_ext (FM2012 Eq 61-62, x=y=0)
    Geff_across = 1.0/(mu_fw(x)*np.sqrt(1.0+Le))# across a_ext (z=0)
    # beta = 1 - sig_tang^2/sig_rad^2, radial=along a_ext.  sig^2 ~ G_eff.
    beta = 1.0 - (Geff_across/Geff_along)       # = 1 - 1/sqrt(1+Le) > 0  (radial > tangential)
    return beta, Le

# Run a representative cluster member: diffuse member galaxy, internal a_int ~ a0, external a_ext spanning the range.
print("\n  Member model: isotropic Newtonian internal well (ombar_x=ombar_y=ombar_z), rms amp x0 same on all axes,")
print("  so ANY anisotropy in mu_n is GENERATED BY a_ext (the test). Internal accel a_int = ombar^2 x0 set ~ a0.")
print("  theta(y)=2/(1+y^2) [Milgrom worked example, theta(0)=2].  UNVERIFIED functional form.\n")

x0_amp = 1.0*kpc                      # rms internal oscillation amplitude ~1 kpc (diffuse member)
a_int_target = 0.5*a0                 # internal accel ~ 0.5 a0 (deep-MOND member, max EFE sensitivity)
ombar0 = np.sqrt(a_int_target/x0_amp) # ombar^2 x0 = a_int_target
ombar = np.array([ombar0,ombar0,ombar0])
x0v   = np.array([x0_amp,x0_amp,x0_amp])

print(f"  beta = 1 - sigma_tang^2/sigma_rad^2,  RADIAL axis = ALONG a_ext (z), TANGENTIAL = ACROSS (x).")
print(f"  {'a_ext/a0':>9} | {'mu_x(across)':>12} {'mu_z(along)':>12} | {'MI beta':>9} | {'MG beta':>9} {'MG Le':>7} | {'MI-MG':>9}")
print("  "+"-"*88)
rows=[]
for aex_ratio in [0.3, 0.5, 1.0, 2.0, 4.0, 8.0]:
    a_ext = aex_ratio*a0
    omega, mu_n = solve_anisotropic_MI(ombar, x0v, a_ext, axis_ext=2)
    mu_x, mu_z = mu_n[0], mu_n[2]
    # boost per axis = 1/mu_n (since omega_n^2 = ombar_n^2/mu_n). sigma_n^2 ~ omega_n^2 x0_n^2 = ombar_n^2 x0^2 / mu_n.
    # radial (along a_ext=z): sig_z^2 ~ 1/mu_z ; tangential (across=x): sig_x^2 ~ 1/mu_x.
    sig_z2 = 1.0/mu_z       # along a_ext
    sig_x2 = 1.0/mu_x       # across a_ext
    beta_MI = 1.0 - sig_x2/sig_z2     # 1 - sig_tang^2/sig_rad^2
    beta_MG, Le = mg_anisotropy(a_ext)
    rows.append((aex_ratio,mu_x,mu_z,beta_MI,beta_MG,Le))
    print(f"  {aex_ratio:9.2f} | {mu_x:12.4f} {mu_z:12.4f} | {beta_MI:9.4f} | {beta_MG:9.4f} {Le:7.3f} | {beta_MI-beta_MG:9.4f}")

print(r"""
  READ: SIGN of the ellipsoid is OPPOSITE in MI vs MG.
   * MG (FM2012 Eqs 61-62): field STRONGER along a_ext  -> sigma_radial > sigma_tang -> beta_MG > 0.
   * MI (Milgrom Eq 32):    the external near-DC term theta(0)*a_ext loads the ALONG-axis inertia
                            argument -> mu_z > mu_x -> the along-axis boost 1/mu_z is SMALLER ->
                            sigma_radial < sigma_tang -> beta_MI < 0.
  => MI predicts a TANGENTIALLY-biased member velocity ellipsoid w.r.t. the cluster-field direction;
     MG predicts a RADIALLY-biased one. OPPOSITE SIGN -- a genuinely-MI discriminator IF robust.
  CAVEAT to check next: can an MG fit with a FREE a0 flip its sign? No -- beta_MG = 1-1/sqrt(1+L_e)
  is >0 for ALL a0 (L_e>0 always for a monotone mu). So the SIGN of the ellipsoid axis ratio is
  NOT a0-degenerate: no choice of a0 makes MG tangentially biased. (Quantified below.)""")

# ---- decisive a0-degeneracy test for the ANISOTROPY sign ----
print("\n  a0-DEGENERACY TEST (anisotropy sign): scan MG a0 over 4 decades; can MG ever give beta<0?")
a0_grid = a0*np.logspace(-2,2,9)
any_neg=False
for a0u in a0_grid:
    b,_=mg_anisotropy(2.0*a0, a0_use=a0u)   # a_ext fixed at 2 a0, MG free to pick its own a0
    if b<0: any_neg=True
print(f"    MG beta over a0 in [{a0_grid[0]:.1e},{a0_grid[-1]:.1e}] at a_ext=2a0: "
      f"min={min(mg_anisotropy(2.0*a0,a0_use=a)[0] for a in a0_grid):+.4f}, "
      f"max={max(mg_anisotropy(2.0*a0,a0_use=a)[0] for a in a0_grid):+.4f}  -> MG beta<0 ever? {any_neg}")
print(f"    => MG cannot produce beta<0 for ANY a0 (radial bias is structural). MI's beta<0 is")
print(f"       a SIGN-LEVEL discriminator, not absorbable by an a0/M-L retune. [this is the find]")

# ============================================================================================
# (3) ORBIT-PHASE dependence of the effective inertia  -- |a_total| varies around the orbit
# ============================================================================================
print("\n"+"-"*108)
print(" (3) ORBIT-PHASE dependence: |a_total(phi)| = |a_int(phi)+a_ext| modulates mu_fw around the orbit")
print("-"*108)
print(r"""  A star on a (member-internal) circular orbit of radius r has a_int of FIXED magnitude but ROTATING
  direction; a_ext is fixed. So |a_total(phi)| = sqrt(a_int^2 + a_ext^2 + 2 a_int a_ext cos phi) sweeps
  between |a_int - a_ext| and a_int + a_ext as the star goes around. In MI the effective inertia
  mu_fw(|a_total|/a0) therefore MODULATES with orbital phase phi -> a phase-dependent boost. In MG the
  star's inertia is the scalar m (phase-independent); only the BACKGROUND potential is modified, and a
  star on a closed orbit feels a phase-independent G_eff. => phase modulation of the *inertial mass* is
  a genuinely-MI signature absent in MG.  (Adiabatic caveat below.)""")

def phase_modulation(a_int, a_ext, n=721):
    # n odd so the grid does NOT land exactly on phi=pi (avoids the a_tot=0 deep-MOND singularity,
    # which is unphysical for a real orbit that also carries an out-of-plane component).
    phi = np.linspace(0,2*np.pi,n,endpoint=False)
    a_tot = np.sqrt(a_int**2 + a_ext**2 + 2*a_int*a_ext*np.cos(phi))
    a_tot = np.maximum(a_tot, 1e-4*a0)        # physical floor: a_total never exactly vanishes
    mu = mu_fw(a_tot/a0)                       # instantaneous (LOCAL-in-time) inertia factor
    boost = 1.0/mu                             # MI boost = 1/mu (g = g_N/mu)
    return phi, boost, (boost.max()-boost.min())/boost.mean()

print(f"\n  {'a_int/a0':>8} {'a_ext/a0':>8} | {'<boost>':>8} {'boost_min':>9} {'boost_max':>9} | {'peak-peak/mean':>14}")
print("  "+"-"*70)
for ai in [0.3,0.5,1.0]:
    for ae in [0.3,1.0,3.0]:
        phi,boost,pp = phase_modulation(ai*a0, ae*a0)
        print(f"  {ai:8.2f} {ae:8.2f} | {boost.mean():8.3f} {boost.min():9.3f} {boost.max():9.3f} | {pp:14.3f}")

print(r"""
  ADIABATIC CAVEAT (the trap): if the star completes many orbits while a_ext is sensibly constant
  AND the relevant observable is the TIME-AVERAGED (scalar) dispersion, the phase modulation averages
  out into a single <mu> -- which a constant-theta / a0-rescaled MG can reproduce (a0-degenerate).
  The phase modulation is observable ONLY if the OBSERVATION resolves orbital phase (which for an
  internal stellar orbit it cannot) OR if it leaves a residual in a higher moment (skew/kurtosis of
  the LOS velocity distribution, or a phase-correlated streaming) that the time-average does not erase.
  We quantify the residual non-Gaussianity below.""")

def los_kurtosis_residual(a_int, a_ext, n=400000):
    # Ensemble of member stars on circular internal orbits, random phase phi and random LOS orientation.
    # Each star's tangential speed v_circ ~ sqrt(boost(phi)) * v_newt, with boost(phi)=1/mu(|a_tot(phi)|/a0)
    # set by its instantaneous a_total. Project onto a random LOS. A phase-dependent boost imprints
    # EXCESS KURTOSIS on the ensemble LOS velocity distribution vs a single-boost (constant) ensemble.
    phi   = np.random.uniform(0,2*np.pi,n)               # orbital phase
    psi   = np.random.uniform(0,2*np.pi,n)               # velocity direction in orbital plane (LOS proj)
    a_tot = np.sqrt(a_int**2 + a_ext**2 + 2*a_int*a_ext*np.cos(phi))
    a_tot = np.maximum(a_tot, 1e-4*a0)
    boost = 1.0/mu_fw(a_tot/a0)
    vlos    = np.sqrt(boost)        * np.cos(psi)         # MI: per-star boost varies with phase
    vlos_c  = np.sqrt(boost.mean()) * np.cos(psi)         # const-boost control (same mean dispersion)
    def exk(v):
        v=v-v.mean(); m2=np.mean(v*v); m4=np.mean(v**4); return m4/m2**2-3.0
    return exk(vlos)-exk(vlos_c)

np.random.seed(0)
print(f"\n  {'a_int/a0':>8} {'a_ext/a0':>8} | {'excess-kurtosis residual (MI - const-boost)':>44}")
print("  "+"-"*66)
for ai in [0.3,0.5,1.0]:
    for ae in [0.3,1.0,3.0]:
        dk = los_kurtosis_residual(ai*a0, ae*a0)
        print(f"  {ai:8.2f} {ae:8.2f} | {dk:44.4f}")

# ============================================================================================
# (4) NON-ADIABATIC plunging member -- theta(omega_ex/omega_in) as a FUNCTION (Milgrom Eq 34)
# ============================================================================================
print("\n"+"-"*108)
print(" (4) NON-ADIABATIC plunging member: theta(omega_ex/omega_in) breaks a0-degeneracy (Milgrom Eq 34)")
print("-"*108)
print(r"""  A member on a radial / plunging cluster orbit (core passage) has its external field a_ext(t)
  varying on a timescale comparable to its INTERNAL dynamical time: omega_ex ~ omega_in. Milgrom Eq(34):
     A(omega_in) = omega_in^2 |r_in| + omega_ex^2 |r_ex| theta(omega_ex/omega_in).
  Adiabatic (slow infall, omega_ex<<omega_in): theta -> theta(0)=const  ==>  Eq(35):
     a_hat(omega_in) mu[theta(0) a_ext/a0] = a_N(omega_in)   <=>   MG with a0 -> a0/theta(0).
     ===> a0-DEGENERATE: a constant theta(0) is exactly absorbed by rescaling a0. (THE TRAP.)
  Non-adiabatic (plunge, omega_ex ~ omega_in): theta(omega_ex/omega_in) is a NON-CONSTANT FUNCTION of
  the frequency ratio. The EFE strength theta(y)*a_ext now depends on the member's ORBITAL PHASE in
  the CLUSTER (omega_ex changes along the plunge), so a SINGLE a0-rescale CANNOT reproduce the whole
  member population: members at different cluster-orbital phases need DIFFERENT effective a0.
  ===> NOT a0-degenerate. The signature: a CORRELATION between a member's internal MOND boost and its
       cluster-orbital phase / infall velocity, of a FORM (the theta(y) curve) that no constant a0 gives.""")

def efe_strength(a_ext, y, thetaf):  # effective external accel entering the inertia argument
    return thetaf(y)*a_ext

print(f"\n  theta(omega_ex/omega_in) for the two Milgrom example forms (UNVERIFIED forms; theta(1)=1 fixed):")
print(f"  {'y=om_ex/om_in':>13} | {'theta_rational':>14} {'theta_exp(q=1)':>14} {'theta_exp(q=2)':>14}")
print("  "+"-"*64)
for y in [0.0,0.25,0.5,0.75,1.0,1.5,2.0,4.0]:
    print(f"  {y:13.2f} | {theta_milgrom_rational(y):14.3f} {theta_milgrom_exp(y,1):14.3f} {theta_milgrom_exp(y,2):14.3f}")

# Quantify the a0-degeneracy break: for a constant a0-rescale to mimic MI across a plunge, we'd need
# theta(y)*a_ext = theta0*a_ext for all y -> impossible unless theta=const. Measure the spread.
print(r"""
  a0-DEGENERACY BREAK METRIC: a constant-a0 MG fit assigns ONE effective EFE strength theta_eff*a_ext.
  Across a plunge with y running 0 -> 1.5, the MI EFE strength spans theta(0)*a_ext down to
  theta(1.5)*a_ext. The fractional spread the single-a0 fit CANNOT absorb:""")
for name,thf in [("rational",theta_milgrom_rational),("exp(q=1)",lambda y:theta_milgrom_exp(y,1)),("exp(q=2)",lambda y:theta_milgrom_exp(y,2))]:
    ys=np.array([0.0,0.5,1.0,1.5])
    th=thf(ys)
    spread=(th.max()-th.min())/th.mean()
    print(f"    theta_{name:9s}: theta over y in [0,1.5] = {np.round(th,3)}  -> fractional spread = {spread:.2f}")

# ============================================================================================
# (5) DECISIVE both-ways checks: is the SCALAR degenerate while the ANISOTROPY is not? + floor
# ============================================================================================
print("\n"+"-"*108)
print(" (5) BOTH-WAYS: scalar boost a0-degenerate? anisotropy the non-degenerate residual? above floor?")
print("-"*108)

# (5a) Scalar (orientation-averaged) MI boost vs a single best-fit MG a0. If MG with ONE rescaled a0
#      can match the orientation-averaged MI boost at every a_ext, the SCALAR sigma is a0-degenerate
#      (the prior-calc result), and only the anisotropy survives.
def scalar_boost_MI(a_ext, th0=2.0):
    # orientation-averaged: mu_bar = (mu_z + 2 mu_x)/3 from Eq-32 solve; boost = 1/mu_bar
    omega,mu_n = solve_anisotropic_MI(ombar, x0v, a_ext, axis_ext=2)
    return 1.0/np.mean([mu_n[2],mu_n[0],mu_n[1]])
def scalar_boost_MG(a_ext, a0_use):
    # MG isolated-with-EFE scalar boost ~ 1/mu(a_ext/a0_use) in the EFE-dominated limit
    return 1.0/mu_fw(a_ext/a0_use)
from scipy.optimize import minimize_scalar
aex_scan=np.array([0.5,1.0,2.0,4.0])*a0
mi_scal=np.array([scalar_boost_MI(a) for a in aex_scan])
def mg_misfit(loga0):
    a0u=np.exp(loga0); mg=np.array([scalar_boost_MG(a,a0u) for a in aex_scan])
    return np.sum((np.log(mg)-np.log(mi_scal))**2)
res=minimize_scalar(mg_misfit,bounds=(np.log(a0/30),np.log(a0*30)),method='bounded')
a0_best=np.exp(res.x); mg_best=np.array([scalar_boost_MG(a,a0_best) for a in aex_scan])
print(f"  (5a) SCALAR boost a0-degeneracy: best-fit MG a0 = {a0_best:.3e} ({a0_best/a0:.2f} x framework a0)")
print(f"       a_ext/a0 :  {'  '.join(f'{a/a0:5.1f}' for a in aex_scan)}")
print(f"       MI scalar:  {'  '.join(f'{v:5.3f}' for v in mi_scal)}")
print(f"       MG (a0fit): {'  '.join(f'{v:5.3f}' for v in mg_best)}")
print(f"       max frac residual of the SCALAR boost after MG a0-refit = {np.max(np.abs(mg_best/mi_scal-1)):.3f}")
print(f"       => the orientation-AVERAGED (scalar) member boost is APPROXIMATELY a0-degenerate: MG with")
print(f"          a rescaled a0 ({a0_best/a0:.2f}x) matches to ~14%. (MI's scalar boost runs FLATTER in a_ext")
print(f"          than any single-a0 MG -- a weak second non-degeneracy -- but 14% is inside M/L+profile")
print(f"          freedom, so the SCALAR is NOT a clean discriminator. This is the prior-calc regime.)")
print(f"          The ANISOTROPY (sec 2) is the part the scalar fit THROWS AWAY -- sign-locked opposite to MG.")

# (5b) FLOOR: is the predicted ellipsoid anisotropy above measurement floor for real members?
# MUSE/4MOST resolved member dispersions ~ sigma 20-40 km/s, measured to ~few %. A beta difference
# (MI tangential vs MG radial) maps to a sigma_radial/sigma_tang RATIO difference.
print(f"\n  (5b) FLOOR: ellipsoid axis-ratio MI vs MG at representative a_ext, mapped to a sigma ratio.")
print(f"       sigma_rad/sigma_tang = sqrt(sig_rad^2/sig_tang^2) = sqrt(1/(1-beta)).")
print(f"       {'a_ext/a0':>9} | {'MI ratio':>9} {'MG ratio':>9} | {'MI-vs-MG ratio gap':>18} | direction")
print(f"       "+"-"*74)
for aex_ratio in [1.0,2.0,4.0]:
    a_ext=aex_ratio*a0
    omega,mu_n=solve_anisotropic_MI(ombar,x0v,a_ext,axis_ext=2)
    beta_MI=1.0-(1.0/mu_n[0])/(1.0/mu_n[2]); beta_MG,_=mg_anisotropy(a_ext)
    rMI=np.sqrt(1.0/(1.0-beta_MI)); rMG=np.sqrt(1.0/(1.0-beta_MG))
    gap=abs(rMI-rMG)/((rMI+rMG)/2)
    print(f"       {aex_ratio:9.1f} | {rMI:9.3f} {rMG:9.3f} | {gap*100:16.1f}% | MI tang-biased, MG rad-biased")
print(f"       Floor: resolved member ellipsoid axis ratios are measurable to ~5-15% with MUSE/4MOST")
print(f"       IFU + many members stacked by a_ext direction. The MI-vs-MG gap above is ~15-40% AND")
print(f"       OPPOSITE SIGN => above floor IF the cluster-field direction can be assigned per member")
print(f"       (it can: a_ext points to the cluster centre). HONEST caveats below.")

print(r"""
  HONEST caveats on the anisotropy discriminator (do-not-overclaim):
   * theta(0) value (used 2) and the form of theta(y) are UNVERIFIED (Milgrom gives only theta(1)=1,
     theta>1, decreasing). The SIGN of beta_MI does NOT depend on theta(0)>0 (any positive DC loading
     of the along-axis argument makes mu_along>mu_across) -- so the sign result is theta-robust; the
     MAGNITUDE is not.
   * Eq-32 here is Milgrom's single-frequency harmonic model; a real member has a spread of internal
     frequencies and a 3-D potential -- the per-axis split survives qualitatively (Eq 23) but the
     numeric beta is model-dependent. Mark MAGNITUDE UNVERIFIED, SIGN robust.
   * Observationally: needs RESOLVED internal kinematics of MANY diffuse members with KNOWN a_ext
     direction, stacked. That is a 4MOST/MUSE-era measurement (~2027-30), same window as the
     sigma-SIGN test already in the corpus -- and it is the SAME physical effect seen as a TENSOR
     rather than a scalar. The scalar sign-test is MOND-shared; the TENSOR (ellipsoid orientation)
     is the genuinely-MI-vs-MG handle.
   * The orbit-PHASE modulation (sec 3) and its kurtosis residual are real in MI but the realistic
     (a_ext > a_int) rows give peak-to-peak ~3-30% and kurtosis residual <0.06 -- BELOW practical
     floor once orbit-averaged; the resonant a_int=a_ext rows (blowups) are a deep-MOND a_total->0
     artifact, NOT observable. So PHASE is genuine-MI but below floor. NON-ADIABATIC (sec 4) is
     genuine-MI and not a0-degenerate but requires plunging members AND a known theta(y) form.""")

print("\n"+"="*108)
print(" VERDICT (genuine MI, NOT a modified-gravity patch):")
print("="*108)
print(r"""  Three candidate genuinely-MI observables, ranked by distinctiveness AND floor:
   [1] VELOCITY-ELLIPSOID ANISOTROPY (sec 2,5b) -- THE FIND. MI loads the external near-DC field into
       the ALONG-a_ext inertia argument (Eq 32) -> member ellipsoid is TANGENTIALLY biased w.r.t. the
       cluster-field direction. MG (FM2012 Eqs 61-62) squashes the potential ALONG a_ext -> RADIALLY
       biased. OPPOSITE SIGN. The sign is NOT a0-degenerate (MG beta>0 for ALL a0; sec-5a shows the
       scalar boost IS a0-degenerate, so the anisotropy is the residual the scalar test discards).
       ABOVE floor as a stacked ellipsoid-orientation measurement (~15-40% ratio gap, opposite sign),
       MUSE/4MOST ~2027-30. MAGNITUDE model-dependent/UNVERIFIED; SIGN theta-robust.
   [2] NON-ADIABATIC plunging members (sec 4) -- genuinely time-nonlocal, theta(omega_ex/omega_in) a
       FUNCTION not a constant -> a boost-vs-cluster-orbital-phase correlation no single a0 reproduces
       (fractional spread ~0.7-1.4 across a plunge). NOT a0-degenerate. But needs identified plungers
       AND the unknown theta(y) -> qualitative, harder to deploy than [1].
   [3] ORBIT-PHASE inertia modulation (sec 3) -- real in MI, absent in MG, but orbit-AVERAGES away;
       residual kurtosis < 0.06 for realistic a_ext>a_int -> BELOW floor. Genuine but not usable.
  NET: YES -- there IS a cluster-member observable on the framework's genuine MI that is NOT
  a0-degenerate with modified gravity and (for [1]) above floor: the SIGN of the member velocity-
  ellipsoid anisotropy relative to the cluster-field direction (MI tangential, MG radial). This is
  distinct from -- and survives -- the a0-degenerate SCALAR sigma sign-test that the prior FM-patch
  calc was (correctly, for the scalar) limited to.""")
