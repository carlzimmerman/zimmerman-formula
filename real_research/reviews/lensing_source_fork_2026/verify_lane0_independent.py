#!/usr/bin/env python3
"""
ADVERSARIAL VERIFICATION of Lane 0 (the target) -- independent re-derivation.
Fresh constants, fresh code path. Checks:
 (A) decisive ratio: naked M_eff inside Saturn vs Pitjev&Pitjeva 2013 bound, both footings
 (B) the SAME source expressed as anomalous acceleration -> Saturn perihelion precession,
     vs Pitjeva&Pitjev 2013 measured extra precession (-0.32 +/- 0.47 mas/cy).
     This tests the report's 'ephemeris-marginal' characterization of the a0/2 tail.
 (C) internal consistency: 'naked source' and 'nu-screened source' are the SAME object at Saturn
 (D) what high-g tail steepness a mechanism actually needs to pass Saturn
 (E) budget ratio a0/g_ext exactness + Omega arithmetic
 (F) nu=2 radius, isothermal slope, deep-MOND ratio at 2 Mpc (spot re-derivations)
"""
import math

G    = 6.67430e-11
Msun = 1.98892e30
AU   = 1.495978707e11
kpc  = 3.08568e19

for tag, a0 in [("CANON", 9.36e-11), ("ALT", 1.13e-10)]:
    print(f"\n================ footing {tag}: a0={a0:.3e} ================")
    # (A) naked M_eff inside Saturn
    r_sat = 9.5826 * AU
    g_sat = G * Msun / r_sat**2
    y = g_sat / a0
    nu_m1 = math.sqrt(1.0 + 1.0/y) - 1.0
    Meff_sat = nu_m1  # in units of Msun (M_eff = Msun*(nu-1))
    bound = 7.9e-11   # Pitjev & Pitjeva 2013, Msun, unmodeled mass inside Saturn's orbit
    over = Meff_sat / bound
    print(f"(A) g(Saturn)={g_sat:.4e} m/s^2  nu-1={nu_m1:.4e}")
    print(f"    naked M_eff(<Saturn) = {Meff_sat:.3e} Msun vs bound {bound:.1e} Msun")
    print(f"    OVERSHOOT = {over:.3e} = 10^{math.log10(over):.2f}")

    # (B) same source as anomalous constant sunward acceleration -> perihelion precession
    A = nu_m1 * g_sat            # = a0/2 to high accuracy
    print(f"(B) anomalous accel A = (nu-1)g = {A:.4e} m/s^2   (a0/2 = {a0/2:.4e})")
    # Gauss perturbation, constant radial (sunward) accel:
    # <d(omega)/dt> = -A*sqrt(1-e^2)/(n a) * <cos f>_t / e ; <cos f>_t = -e  =>
    # <d(omega)/dt> = +A*sqrt(1-e^2)/(n a) ... magnitude |A|*sqrt(1-e^2)/(n a)
    e_sat = 0.0565
    T_sat = 29.4571 * 365.25 * 86400.0
    n = 2 * math.pi / T_sat
    a_sma = r_sat  # use semi-major axis 9.5826 AU
    na = n * a_sma
    prec = A * math.sqrt(1 - e_sat**2) / na          # rad/s
    cy = 100 * 365.25 * 86400.0
    prec_mas_cy = prec * cy * (180/math.pi) * 3600e3  # mas/century
    meas_sigma = 0.47  # mas/cy, Pitjeva & Pitjev 2013 extra-precession uncertainty for Saturn
    print(f"    perihelion drift from constant tail = {prec_mas_cy:.3e} mas/cy")
    print(f"    vs Saturn extra-precession uncertainty ~{meas_sigma} mas/cy (Pitjeva&Pitjev 2013)")
    print(f"    -> tail OVER ephemeris sensitivity by {prec_mas_cy/meas_sigma:.2e} = 10^{math.log10(prec_mas_cy/meas_sigma):.2f}")
    # cross-check the acceleration sensitivity implied by the mass bound:
    A_sens_from_mass = g_sat * bound  # delta_g = g * dM/M  (Msun units cancel)
    print(f"    accel sensitivity implied by the mass bound: {A_sens_from_mass:.2e} m/s^2 "
          f"(vs A = {A:.2e} -> same ~4 orders)")

    # (C) internal consistency
    print(f"(C) 'nu-screened' source AT SATURN *IS* the naked source: extra accel = (nu-1)g = a0/2.")
    print(f"    Calling (A) dead-by-4-orders and (B) 'marginal' is the same object counted twice.")

    # (D) required tail steepness: need A_resid < ~7e-15 m/s^2 (mass-bound framing)
    for name, Ares in [("y^-1 (framework nu)", a0/2),
                       ("y^-3/2", a0**1.5 / g_sat**0.5),
                       ("y^-2 (standard-MOND-like)", a0**2 / g_sat)]:
        status = "PASS" if Ares < A_sens_from_mass else "FAIL"
        print(f"    tail {name:28s}: A(Saturn) = {Ares:.2e} m/s^2  -> {status} vs {A_sens_from_mass:.1e}")

    # (E) budget
    Mb = 1e11 * Msun
    for fext in (0.01, 0.03, 0.10):
        gext = fext * a0
        rcut = math.sqrt(G * Mb * a0) / gext
        Mtot = math.sqrt(a0 * Mb / G) * rcut
        assert abs(Mtot / Mb - a0/gext) < 1e-9
    print(f"(E) M_eff_tot/M_bar = a0/g_ext EXACT (verified). Omega_dm/Omega_b = {0.2607/0.0490:.2f};"
          f" band w/ 10-20% galactic baryons: {0.2607/0.0490/0.20:.1f}-{0.2607/0.0490/0.10:.1f}; a0/gext@0.03a0 = 33.3 -> inside")

    # (F) spot re-derivations
    r_nu2 = math.sqrt(3 * G * Mb / a0)
    slope = math.sqrt(a0 * Mb / G)
    r2 = 2000 * kpc
    y2 = (G * Mb / r2**2) / a0
    ratio_iso = (math.sqrt(1 + 1/y2) - 1) / (1/math.sqrt(y2))
    print(f"(F) nu=2 radius = {r_nu2/kpc:.1f} kpc | iso slope = {slope*kpc/Msun:.3e} Msun/kpc | "
          f"iso ratio @2Mpc = {ratio_iso:.4f}")

print("\nEXIT 0")
