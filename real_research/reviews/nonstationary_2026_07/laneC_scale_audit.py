#!/usr/bin/env python3
"""
Lane C, part 3 -- SCALE AUDIT of the finite-time broadening on galactic orbits.

From laneC_finite_time_response.py: a Gaussian window of width T adds a broadening
term in exact quadrature, a_eff = sqrt(a^2 + H^2c^2 + kappa^2 c^2/T^2), kappa = 1.746
(fit residual <0.2%). On a quasi-circular orbit the acceleration DIRECTION rotates at
Omega = v/R, so the longest stationarity window available to a comoving detector is
T ~ 1/Omega -> window acceleration scale a_T = kappa * c * Omega = kappa * c * v / R.

Questions:
  (i)  Is a_T universal, or velocity-dependent?  a_T/a_cent = kappa*c/v -- NOT universal.
  (ii) Where does a_T cross the framework a0 (both footings)?
  (iii) What window WOULD land on a0? T* = kappa*c/a0 -- compare to 1/H_Lambda.
"""
import numpy as np, math, sys

c = 2.998e8            # m/s
kpc = 3.0857e19        # m
Mpc = 1e3 * kpc
Gyr = 3.156e16         # s
Z = math.sqrt(32 * math.pi / 3)
KAPPA = 1.746          # from laneC_finite_time_response.py quadrature fit
FOOTINGS = {"canonical rho_DE/cH_Lambda": 9.36e-11, "alternate rho_total/cH0": 1.13e-10}

print("=" * 95)
print("Galactic band: Omega = v/R, window T = 1/Omega, a_T = kappa*c*Omega, a_cent = v*Omega")
print(f"kappa = {KAPPA} (numerically fitted); baseline kappa=1 scales all a_T down by {KAPPA:.2f}x only")
print("=" * 95)
vs = np.array([30., 100., 200., 300.]) * 1e3
Rs = np.array([0.5, 2., 10., 30.]) * kpc
a0c, a0a = FOOTINGS["canonical rho_DE/cH_Lambda"], FOOTINGS["alternate rho_total/cH0"]
hdr = (f"{'v[km/s]':>8} {'R[kpc]':>7} {'T_orb=2piR/v[Myr]':>18} {'a_cent[m/s2]':>13} "
       f"{'a_T[m/s2]':>11} {'a_T/a_cent':>10} {'a_T/a0can':>10} {'a_T/a0alt':>10}")
print(hdr)
ratios_cent, ratios_a0 = [], []
for v in vs:
    for R in Rs:
        Om = v / R
        aT = KAPPA * c * Om
        ac = v * Om
        Torb = 2 * math.pi / Om / (1e6 * 3.156e7)
        ratios_cent.append(aT / ac); ratios_a0.append(aT / a0c)
        print(f"{v/1e3:8.0f} {R/kpc:7.1f} {Torb:18.1f} {ac:13.3e} {aT:11.3e} "
              f"{aT/ac:10.0f} {aT/a0c:10.2e} {aT/a0a:10.2e}")
print(f"\n(i) a_T/a_cent = kappa*c/v: spans {min(ratios_cent):.0f}x .. {max(ratios_cent):.0f}x")
print("    over v = 30..300 km/s -- the window scale is VELOCITY-DEPENDENT (not universal)")
print("    and sits 3-4 orders of magnitude ABOVE the local acceleration everywhere in the band.")
print(f"    a_T/a0 spans {min(ratios_a0):.1e} .. {max(ratios_a0):.1e} (canonical footing):")
print("    if the finite-window term entered the physical quadrature, it would DOMINATE both")
print("    g_bar and a0 at every galactic (v,R) -- predicting a transition at a ~ c*v/R,")
print("    2-5 orders above a0 and v-dependent, in flat contradiction with the universal-a0")
print("    RAR (the framework's own 0.108-dex SPARC fit REQUIRES universality).")

print()
print("(ii) crossing radius R* where a_T = a0  (R* = kappa*c*v/a0):")
for lbl, a0 in FOOTINGS.items():
    for v in vs:
        print(f"    {lbl:32s} v={v/1e3:4.0f} km/s: R* = {KAPPA*c*v/a0/Mpc:7.1f} Mpc")
print("    -> R* = 4.5..54 Mpc on both footings: the window term only decays to a0 at")
print("       SUPER-galactic separations; inside real disks (R <= 30 kpc) a_T >> a0 always.")

print()
print("(iii) the window that WOULD reproduce a0: T* = kappa*c/a0")
for lbl, a0 in FOOTINGS.items():
    Ts = KAPPA * c / a0
    HL = Z * a0 / c            # framework's horizon rate on this footing (a0 = cH/Z)
    print(f"    {lbl:32s}: T* = {Ts:.3e} s = {Ts/Gyr:6.1f} Gyr = {Ts*HL:5.1f} / H")
print("    -> T* ~ 10/H: the ONLY window that lands on a0 is ~10 horizon times, i.e. the")
print("       STATIONARY (infinite-window) limit -- exactly the regime already covered by")
print("       the passive-state theorems (III/IV). There is no intermediate window that is")
print("       both genuinely non-stationary AND lands on a universal 9.36e-11.")

print()
print("Cross-check vs persistence: MOND phenomenology needs mu<1 sustained >= 10 orbits")
Tper = np.array([10 * 2 * math.pi * R / v for v in vs for R in Rs])
print(f"    10 T_orb = {Tper.min()/Gyr*1e3:.0f} Myr .. {Tper.max()/Gyr:.1f} Gyr; over such spans the orbit-")
print("    averaged bath is stationary-KMS to enormous accuracy (dS drift power deficit")
print("    ~2.9e10, established Theorem III audit) -- the transient corner cannot persist.")

# sanity assertions (script must be self-verifying)
assert min(ratios_cent) > 900 and max(ratios_cent) < 2.1e4
assert min(ratios_a0) > 1e2                       # a_T > a0 everywhere in the band
assert abs((KAPPA * c / a0c) * (Z * a0c / c) - KAPPA * Z) < 1e-9  # T* * H_Lambda = kappa*Z ~ 10.1
print("\nOVERALL: PASS")
sys.exit(0)
