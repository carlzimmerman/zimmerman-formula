#!/usr/bin/env python3
"""
LANE 2 -- THE INERTIAL DEFICIT as the lensing source.

Candidate mechanism:
  In modified inertia (MI), each body's inertial response is mu = 1/nu < 1 in
  the low-acceleration regime. IF total energy is conserved with the frame /
  vacuum sector absorbing the difference, the "missing inertial energy"
  (1-mu) m c^2 per body is posited to be real stress that gravitates.

Required target (banked): effective source with enclosed mass
  M_eff(r) = M_bar(r) * (nu(y)-1),  y = g_bar/a0,  nu = sqrt(1+1/y)
  deep-MOND: M_eff -> sqrt(a0 M_bar / G) * r  (isothermal-like, Sigma~1/R shear)

Tests (framework's own premises: g_obs = sqrt(g_bar^2 + g_bar a0), mu = 1/nu):
 (1) AMOUNT: M_def(r) = INT_0^r (1 - mu(a(r'))) dM_bar(r')  vs  M_eff(r).
     Analytic check: constant-nu limit gives M_def/M_eff = 1/nu exactly.
     Hard bound: M_def <= M_bar ALWAYS (deficit cannot exceed rest mass),
     while M_eff grows ~ r without bound.
 (2) LOCATION: the deficit sits AT the baryons (it is their reduced inertia).
     Compute galaxy-galaxy lensing excess DeltaSigma(R) for the
     deficit-at-baryons source vs the required isothermal-like source,
     at 30-300 kpc where the measurement lives.
 (3) LICENSE: is "the deficit gravitates in the frame sector" forced by the
     action, or a new posit? (printed audit below)

Also computed: the KINETIC-only reading (the energy actually touched by an
inertia modification at galactic speeds is O(v^2/c^2) of rest mass), because
the rest-mass reading is already the maximally generous one.

Both footings: a0 = 9.36e-11 (canonical, cH_Lambda/Z) and 1.13e-10 (cH0 alt).
Exit 0. No fabricated numbers: everything below is computed here.
"""

import numpy as np

# ----------------------------- constants ------------------------------------
G     = 6.674e-11          # m^3 kg^-1 s^-2
MSUN  = 1.989e30           # kg
KPC   = 3.0857e19          # m
C     = 2.998e8            # m/s

A0_CANON = 9.36e-11        # m/s^2  (cH_Lambda / Z, canonical)
A0_ALT   = 1.13e-10        # m/s^2  (rho_total / cH0 alt footing)

M_BAR = 1.0e11 * MSUN      # baryonic mass of the test galaxy
R_D   = 3.5 * KPC          # exponential-disk scale length (typical L* spiral)

# Hernquist spherical proxy for the baryon distribution, matched to the
# exponential disk's half-mass radius R_half = 1.678 R_d:
#   Hernquist M(<r) = M r^2/(r+a)^2, half-mass at r = (1+sqrt(2)) a
A_HERN = 1.678 * R_D / (1.0 + np.sqrt(2.0))

V_CIRC_TYP = 200e3         # m/s, typical flat rotation speed (kinetic reading)


def nu_of_y(y):
    """The framework's OWN interpolation: nu(y) = sqrt(1 + 1/y)."""
    return np.sqrt(1.0 + 1.0 / y)


def M_bar_enc(r):
    """Hernquist enclosed baryonic mass (spherical proxy)."""
    return M_BAR * r**2 / (r + A_HERN)**2


def rho_bar(r):
    """Hernquist density."""
    return M_BAR * A_HERN / (2.0 * np.pi * r * (r + A_HERN)**3)


def g_bar(r, Menc=None):
    if Menc is None:
        Menc = M_bar_enc(r)
    return G * Menc / r**2


def run_amount(a0, label, point_mass=False):
    """Part (1): galaxy-integrated deficit vs the required M_eff."""
    print(f"\n===== PART 1 (AMOUNT), footing {label}: a0 = {a0:.3e} m/s^2, "
          f"baryons = {'POINT MASS' if point_mass else 'Hernquist proxy'} =====")

    # radial grid (log) out to 300 kpc
    r = np.logspace(np.log10(0.01 * KPC), np.log10(300.0 * KPC), 4000)

    if point_mass:
        Menc = np.full_like(r, M_BAR)
    else:
        Menc = M_bar_enc(r)

    gb  = g_bar(r, Menc)
    y   = gb / a0
    nu  = nu_of_y(y)
    mu  = 1.0 / nu
    one_minus_mu = 1.0 - mu                      # deficit fraction per unit mass

    # required effective (phantom) mass -- the banked target
    M_eff = Menc * (nu - 1.0)

    # galaxy-integrated deficit: each mass shell dM at r' contributes (1-mu(r')) dM
    dM = np.gradient(Menc, r)
    M_def = np.concatenate([[0.0], np.cumsum(0.5 * (one_minus_mu[1:] * dM[1:] +
                                                    one_minus_mu[:-1] * dM[:-1])
                                             * np.diff(r))])

    # kinetic-only reading: energy actually touched by the inertia modification
    # at orbital speeds is ~ (1-mu) * (1/2) m v^2 -> mass deficit suppressed
    # by v^2/(2 c^2)
    kin_suppress = V_CIRC_TYP**2 / (2.0 * C**2)
    M_def_kin = M_def * kin_suppress

    print(f"  kinetic suppression factor v^2/2c^2 (v=200 km/s) = {kin_suppress:.3e}")
    print(f"\n  {'r[kpc]':>7} {'y':>9} {'nu':>7} {'(1-mu)':>7} "
          f"{'M_eff/Mb':>9} {'M_def/Mb':>9} {'M_def/M_eff':>12} "
          f"{'1/nu(r)':>8} {'kin/M_eff':>10}")
    rows = {}
    for rk in [5, 10, 20, 50, 100, 200, 300]:
        i = np.argmin(np.abs(r - rk * KPC))
        ratio = M_def[i] / M_eff[i]
        rows[rk] = dict(y=y[i], nu=nu[i], Meff=M_eff[i] / M_BAR,
                        Mdef=M_def[i] / M_BAR, ratio=ratio,
                        kin=M_def_kin[i] / M_eff[i])
        print(f"  {rk:>7} {y[i]:>9.4f} {nu[i]:>7.3f} {one_minus_mu[i]:>7.3f} "
              f"{M_eff[i]/M_BAR:>9.3f} {M_def[i]/M_BAR:>9.3f} {ratio:>12.4f} "
              f"{1.0/nu[i]:>8.4f} {M_def_kin[i]/M_eff[i]:>10.2e}")

    # hard bound check
    print(f"\n  HARD BOUND: M_def(300 kpc)/M_bar = {M_def[-1]/M_BAR:.4f} "
          f"(<= 1 by construction: deficit cannot exceed rest mass)")
    print(f"  Required M_eff(300 kpc)/M_bar    = {M_eff[-1]/M_BAR:.3f} "
          f"(grows ~ r, unbounded)")
    print(f"  => even the MAXIMAL deficit (mu -> 0 everywhere, M_def = M_bar) "
          f"falls short by nu-1 = {M_eff[-1]/M_BAR:.1f}x at 300 kpc")
    return r, Menc, mu, nu, M_eff, M_def, rows


def analytic_check(a0):
    """Constant-nu limit: M_def/M_eff must equal 1/nu exactly."""
    print("\n===== ANALYTIC CHECK: constant-nu limit =====")
    # all baryons in a thin shell at one radius -> single y for every particle
    for y0 in [10.0, 1.0, 0.1, 0.01]:
        nu0 = nu_of_y(y0)
        Mdef_over_Mb  = 1.0 - 1.0 / nu0          # (nu-1)/nu
        Meff_over_Mb  = nu0 - 1.0
        ratio = Mdef_over_Mb / Meff_over_Mb
        print(f"  y={y0:>6}: nu={nu0:8.4f}  M_def/M_eff = {ratio:.6f}  "
              f"vs 1/nu = {1.0/nu0:.6f}  -> {'MATCH' if abs(ratio-1/nu0)<1e-12 else 'MISMATCH'}")
    print("  => M_def/M_eff = 1/nu exactly (analytic identity: (nu-1)/nu / (nu-1) = 1/nu).")
    print("     Deep MOND: nu ~ (a0/g_bar)^(1/2) -> shortfall factor grows ~ r.")


# ------------------------- Part 2: lensing shear -----------------------------
def sigma_projected(rho_func, R, r_max=3000.0 * KPC):
    """Surface density Sigma(R) = 2 INT_0^inf rho(sqrt(R^2+z^2)) dz."""
    z = np.logspace(np.log10(1e-4 * KPC), np.log10(r_max), 2000)
    out = np.empty_like(R)
    for j, Rj in enumerate(R):
        rr = np.sqrt(Rj**2 + z**2)
        out[j] = 2.0 * np.trapz(rho_func(rr), z)
    return out


def delta_sigma(rho_func, R_eval):
    """Excess surface density DeltaSigma(R) = Sigma_bar(<R) - Sigma(R)."""
    R_grid = np.logspace(np.log10(1e-3 * KPC), np.log10(400.0 * KPC), 800)
    Sig = sigma_projected(rho_func, R_grid)
    # cumulative M2D(<R)
    integrand = 2.0 * np.pi * R_grid * Sig
    M2D = np.concatenate([[0.0],
                          np.cumsum(0.5 * (integrand[1:] + integrand[:-1])
                                    * np.diff(R_grid))])
    Sig_bar = M2D / (np.pi * R_grid**2)
    dS = Sig_bar - Sig
    return np.interp(R_eval, R_grid, dS), np.interp(R_eval, R_grid, Sig_bar)


def run_lensing(a0, label):
    """Part (2): shear profile of deficit-at-baryons vs required isothermal-like."""
    print(f"\n===== PART 2 (LOCATION / SHEAR), footing {label}: a0 = {a0:.3e} =====")

    r = np.logspace(np.log10(0.01 * KPC), np.log10(3000.0 * KPC), 6000)
    Menc = M_bar_enc(r)
    gb = g_bar(r, Menc)
    nu = nu_of_y(gb / a0)
    mu = 1.0 / nu

    # (a) deficit source: rho_def(r) = (1-mu(r)) * rho_bar(r)  -- sits AT baryons
    def rho_def(rr):
        Me = M_bar_enc(rr)
        gg = g_bar(rr, Me)
        nn = nu_of_y(gg / a0)
        return (1.0 - 1.0 / nn) * rho_bar(rr)

    # (b) required source: rho_eff = (1/4 pi r^2) dM_eff/dr, M_eff = M_bar(r)(nu-1)
    M_eff = Menc * (nu - 1.0)
    dMeff = np.gradient(M_eff, r)
    rho_eff_grid = np.maximum(dMeff, 0.0) / (4.0 * np.pi * r**2)

    def rho_eff(rr):
        return np.interp(rr, r, rho_eff_grid)

    R_eval = np.array([30, 50, 100, 200, 300]) * KPC
    dS_def, _ = delta_sigma(rho_def, R_eval)
    dS_req, _ = delta_sigma(rho_eff, R_eval)

    print(f"  {'R[kpc]':>7} {'dSig_def[Msun/pc^2]':>20} {'dSig_req[Msun/pc^2]':>20} "
          f"{'def/req':>10} {'shortfall':>10}")
    unit = MSUN / (3.0857e16)**2  # Msun/pc^2 in kg/m^2
    ratios = {}
    for j, Rk in enumerate([30, 50, 100, 200, 300]):
        rat = dS_def[j] / dS_req[j]
        ratios[Rk] = rat
        print(f"  {Rk:>7} {dS_def[j]/unit:>20.4f} {dS_req[j]/unit:>20.4f} "
              f"{rat:>10.4f} {1.0/rat:>9.1f}x")

    # slope check: point-like source gives DeltaSigma ~ R^-2, isothermal ~ R^-1
    lg = np.log10([30, 300])
    slope_def = (np.log10(dS_def[-1]) - np.log10(dS_def[0])) / (lg[1] - lg[0])
    slope_req = (np.log10(dS_req[-1]) - np.log10(dS_req[0])) / (lg[1] - lg[0])
    print(f"  log-slope 30->300 kpc: deficit source = {slope_def:.2f} "
          f"(point-mass-like -2), required = {slope_req:.2f} (isothermal-like -1)")
    return ratios, slope_def, slope_req


def part3_license():
    print("\n===== PART 3 (LICENSE AUDIT) =====")
    print("""  Is 'the deficit energy gravitates in the frame sector' forced by the action?
  S = S_EH[g] + S_u(passive unit-timelike frame, 0 dof) + S_matter,
  S_matter = -1/2 INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ].

  (i)  NO RESERVOIR: the frame sector S_u is passive with ZERO propagating
       degrees of freedom (v4 Dirac closure; v11: no (grad u)^2 generated at
       one loop). There is nothing in the action for the deficit energy to
       live IN. A frame-sector stress large enough to bend light 5-10x the
       baryons would be a dynamical energy density -- exactly what the 0-dof
       constraint structure forbids.
  (ii) NO CONSERVATION THEOREM FORCES IT: diffeomorphism invariance gives
       nabla_mu T^munu_total = 0 for the T from METRIC VARIATION of the full
       action -- and that variation (still an open item in the completion) is
       what decides what gravitates. 'Energy bookkeeping of the worldline
       inertia' is not a source term unless the metric variation says so.
  (iii) SIGN RISK: the natural metric variation of -1/2 rho_m s u K u makes the
       gravitating source ~ mu_eff * rho_m <= rho_m in deep MOND, i.e. the
       direct reading REDUCES the source at the baryons (anti-lensing), it
       does not add a positive halo.
  (iv) DOUBLE-COUNT (banked audit): if the deficit DID gravitate at the
       baryons, it perturbs g_bar itself; with the MI response calibrated on
       the baryonic field, rotation curves over-predict by the same factor.
  => VERDICT: 'deficit gravitates' is a NEW POSIT (three posits, in fact:
     it exists as positive localized stress; it sits somewhere; it is exempt
     from the rotation-curve budget) -- not a theorem of the action.""")


def main():
    print("=" * 78)
    print("LANE 2: INERTIAL-DEFICIT SOURCE vs REQUIRED M_eff = M_bar(nu-1)")
    print(f"Galaxy: M_bar = 1e11 Msun, Hernquist proxy a = {A_HERN/KPC:.2f} kpc "
          f"(half-mass = {1.678*R_D/KPC:.1f} kpc, matches R_d = 3.5 kpc disk)")
    print("=" * 78)

    analytic_check(A0_CANON)

    all_rows = {}
    for a0, label in [(A0_CANON, "CANONICAL"), (A0_ALT, "ALT")]:
        _, _, _, _, _, _, rows = run_amount(a0, label)
        all_rows[label] = rows
    # bracketing: point-mass baryons (max concentration -> minimal deficit)
    run_amount(A0_CANON, "CANONICAL", point_mass=True)

    shear = {}
    for a0, label in [(A0_CANON, "CANONICAL"), (A0_ALT, "ALT")]:
        shear[label] = run_lensing(a0, label)

    part3_license()

    print("\n" + "=" * 78)
    print("BOTTOM LINE (computed above):")
    r100 = all_rows["CANONICAL"][100]
    r300 = all_rows["CANONICAL"][300]
    s = shear["CANONICAL"]
    print(f"  AMOUNT: M_def/M_eff = 1/nu analytically; at 100 kpc the integrated "
          f"deficit covers {100*r100['ratio']:.0f}% of the required phantom mass "
          f"(shortfall {1/r100['ratio']:.0f}x), at 300 kpc {100*r300['ratio']:.0f}% "
          f"({1/r300['ratio']:.0f}x); the shortfall grows ~ r without bound "
          f"because M_def <= M_bar always.")
    print(f"  LOCATION: deficit-at-baryons shear is point-mass-like (slope ~ -2) "
          f"vs required isothermal-like (slope ~ -1); DeltaSigma shortfall "
          f"{1/s[0][30]:.0f}x at 30 kpc -> {1/s[0][300]:.0f}x at 300 kpc.")
    print(f"  KINETIC-ONLY reading (the energy MI actually touches): additional "
          f"~{V_CIRC_TYP**2/(2*C**2):.1e} suppression -> dead by ~7 more orders.")
    print(f"  LICENSE: not forced by the action; requires >= 3 new posits and "
          f"trips the banked rotation-curve double-count.")
    print("=" * 78)


if __name__ == "__main__":
    main()
    raise SystemExit(0)
