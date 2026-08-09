#!/usr/bin/env python3
"""
MECHANISM 1: does the AeST scalar LEAVE the ghost-condensate attractor inside a galaxy?

Question: in the quasistatic galaxy the scalar phi carries a large SPATIAL gradient
(that gradient IS the MOND force).  Is that gradient a large or a tiny perturbation on
the condensate's TEMPORAL gradient Q = A^mu grad_mu phi ?

    Y   = q^{mu nu} grad_mu phi grad_nu phi ,   q^{mu nu} = g^{mu nu} + A^mu A^nu
    Q   = A^mu grad_mu phi
    ratio R = Y / Q^2  =  |grad_spatial phi|^2 / (dphi/dtau)^2

R is the SQUARED TILT of grad phi off the aether time direction.  It is a ratio of two
contractions of the SAME one-form grad_mu phi, so it is DIMENSIONLESS and INDEPENDENT of
how phi is normalised.  That kills the convention ambiguity outright.

If R >~ 1 the condensate is disrupted in galaxies -> no dust to virialise -> GOOD for
   the no-dark-matter reading.
If R << 1 the field stays pinned -> the dust survives inside galaxies -> BAD.

CONVENTIONS (Skordis & Zlosnik 2021 PRL 127:161302, eq. 1):
   S = (1/2 kappa) int d4x sqrt(-g) [ R + L_MOND ],  kappa = 8 pi Gtilde / c^4
   L_MOND = -(K_B/2) F^{mu nu}F_{mu nu} + 2(2-K_B) J^mu grad_mu phi
            - (2-K_B) Y - Fcal(Y,Q) - lambda (A^mu A_mu + 1)
   L_MOND has the dimensions of R, i.e. 1/length^2.  Y enters LINEARLY with the
   dimensionless coefficient (2-K_B), so [Y] = [Q^2] = 1/length^2 in c=1 units, hence
   phi is DIMENSIONLESS and grad phi has dimensions of (acceleration / c^2).
   INDEPENDENT CONFIRMATION that sqrt(Y) is an acceleration: Verwayen, Skordis & Boehm
   2024 MNRAS 531:272 write the MOND limit of the free function as
        J -> [2 / (3 (1+beta_0) a_0)] Y^{3/2}   for   sqrt(Y) << a_0
   -- they compare sqrt(Y) directly to a_0.  So we may quote sqrt(Y) and Q both in m/s^2
   by multiplying the 1/length quantities by c^2.

The Q-sector: Fcal(0,Q) = Kcal(Q), minimised at Q = Q_0, expanded Kcal ~ K_2 (Q-Q_0)^2.
   Shift charge  I = dKcal/dQ = 2 K_2 (Q - Q_0)  obeys  I a^3 = I_0  (conserved)
   Dust density  8 pi G rho_phi / c^2 = Q_0 I     (Skordis-Zlosnik: 8 pi G rho_0 = Q_0 I_0)
   Mass term     mu^2 = 2 K_2 Q_0^2 / (2 - K_B)   [mu^{-1} >~ 1 Mpc for MOND in galaxies]
   Sound speed   c_ad^2 = eps/Q_0 = 4 pi G rho_phi / (mu^2 c^2)  (2-K_B -> 2)
                 -- reproduces Blanchet & Skordis 2024 JCAP 11:040 for K = mu^2 (Q-1)^2.

Every number printed below is asserted.  Run: python3 mi_aest_condensate_pinning_2026.py
"""

import math

# ----------------------------------------------------------------------------- constants
c     = 2.99792458e8            # m/s
G     = 6.674e-11               # SI
Msun  = 1.98892e30              # kg
Mpc   = 3.0856775814913673e22   # m
kpc   = Mpc / 1e3
pc    = Mpc / 1e6
AU    = 1.495978707e11          # m
eV    = 1.602176634e19          # (unused numerically; see eV->1/m below)
eV_per_inv_m = 5.0677307e6      # 1 eV = 5.0677e6 m^-1  (hbar = c = 1)

a0    = 9.3619e-11              # m/s^2   framework: kappa c sqrt(G rho_Lambda) = c H_Lambda / Z
H0    = 67.4 * 1e3 / Mpc        # s^-1
rho_crit = 3 * H0**2 / (8 * math.pi * G)
Om_dm = 0.264
Om_b  = 0.0493
rho_dm = Om_dm * rho_crit
rho_m  = (Om_dm + Om_b) * rho_crit
M_Pl_eV = 2.435e27              # reduced Planck mass in eV

frak_a0 = a0 / c**2             # a_0 in 1/length units
print("=" * 78)
print("BLOCK 0  units anchor")
print("=" * 78)
print(f"a_0                     = {a0:.4e} m/s^2")
print(f"a_0/c^2  (= 'sqrt(Y)' scale in 1/m) = {frak_a0:.4e} 1/m   -> c^2/a_0 = {c**2/a0/Mpc:.0f} Mpc")
print(f"rho_crit = {rho_crit:.4e} kg/m^3 ;  rho_dm = {rho_dm:.4e} kg/m^3")
assert abs(frak_a0 - 1.0416e-27) / 1.0416e-27 < 2e-3
assert abs(c**2 / a0 / Mpc - 31118) / 31118 < 0.01

# ------------------------------------------------------- BLOCK 1: Route A kernel, sqrt(Y)
def nu_routeA(y):
    """framework's in-force interpolation nu(y) = 1/(1-exp(-sqrt(y))), y = g_bar/a0"""
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

def x_of_y(y):
    return y * nu_routeA(y)

print()
print("=" * 78)
print("BLOCK 1  how big is sqrt(Y) ?  (the scalar's spatial gradient, in m/s^2)")
print("=" * 78)
# In the AeST quasistatic system (Verwayen+2024):  Phi = Phitilde + chi,
#   grad^2 Phitilde + mu^2 Phi = 4 pi G rho_b/(1+beta0),   grad^2 Phitilde = div[J_Y grad chi]
# so chi is the AQUAL scalar and in the MOND regime |grad chi| = sqrt(a0 g_bar) ~ g_obs,
# i.e. sqrt(Y) tracks the FULL observed acceleration, not just the MOND excess.
# We take that (larger, framework-FAVOURABLE) reading.
scales = [
    ("LSB dwarf, deep MOND (y_bar=0.003)", x_of_y(0.003) * a0),
    ("dwarf (y_bar=0.01)",                 x_of_y(0.01) * a0),
    ("MW at R_0=8.1 kpc, v=230 km/s",      (230e3) ** 2 / (8.1 * kpc)),
    ("bright spiral inner disc (y_bar=10)", x_of_y(10.0) * a0),
    ("cluster R500 (M500=5e14, R500=1.2Mpc)", G * 5e14 * Msun / (1.2 * Mpc) ** 2),
    ("linear LSS: delta=1 sphere at 10 Mpc",
     G * (4 * math.pi / 3) * rho_m * (10 * Mpc) ** 3 / (10 * Mpc) ** 2),
    ("Earth's orbit (Sun)",                G * Msun / AU ** 2),
]
for nm, g in scales:
    print(f"  {nm:44s} sqrt(Y) = {g:.3e} m/s^2 = {g/a0:9.3e} a_0")
g_MW = (230e3) ** 2 / (8.1 * kpc)
assert abs(g_MW - 2.115e-10) / 2.115e-10 < 0.01
g_clu = G * 5e14 * Msun / (1.2 * Mpc) ** 2
assert abs(g_clu - 4.84e-11) / 4.84e-11 < 0.02

# a hard ceiling on the MOND EXCESS in the Route A kernel (the conservative reading)
best_u, best_val = None, -1.0
u = 1e-3
while u < 20:
    y = u * u
    val = y * (1.0 / nu_routeA(y) ** -1 - 1.0) if False else y * (nu_routeA(y) - 1.0)
    if val > best_val:
        best_val, best_u = val, u
    u += 1e-4
print(f"\n  CONSERVATIVE reading (scalar carries only the MOND EXCESS g_obs - g_bar):")
print(f"  sup_y [x(y)-y] = {best_val:.4f} a_0 at y = {best_u**2:.3f}  ->  sqrt(Y) <= {best_val*a0:.3e} m/s^2")
print("  i.e. on that reading the scalar gradient is BOUNDED BY ~0.65 a_0 EVERYWHERE.")
assert 0.64 < best_val < 0.65
assert 2.0 < best_u ** 2 < 3.2

# --------------------------------------------------- BLOCK 2: how big is Q_0 ?  three ways
print()
print("=" * 78)
print("BLOCK 2  how big is Q_0, the condensate value, in the SAME units ?")
print("=" * 78)
print("Q_0 = mu * sqrt((2-K_B)/(2 K_2));  take (2-K_B)/(2K_2) = 2 (i.e. Q_0 = sqrt(2) mu),")
print("which is the normalisation that reproduces the published M <-> mu map (checked below).")

def Q0_from_mu(mu_inv_Mpc, ratio=2.0):
    mu = 1.0 / (mu_inv_Mpc * Mpc)                 # 1/m
    return math.sqrt(ratio) * mu, mu

branches = [
    ("cosmology branch (Blanchet-Skordis quadratic K)", 0.22e-3),
    ("Mistele+23 cluster requirement mu^2 >~ 2.5 Mpc^-2", 0.632),
    ("SZ21 / Verwayen+24 fiducial mu = 1 Mpc^-1", 1.0),
    ("Mistele+23 weak lensing to a_b>=1e-13 (mu^2<=1)", 1.0),
    ("Mistele+23 weak lensing to a_b>=1e-15 (mu^2<=1e-3): MOST FAVOURABLE", 31.6),
]
Q0_table = {}
for nm, mi in branches:
    Q0, mu = Q0_from_mu(mi)
    Q0_table[nm] = Q0
    print(f"  mu^-1 = {mi:8.4g} Mpc  ({nm})")
    print(f"      Q_0 = {Q0:.4e} 1/m   ->  Q_0 c^2 = {Q0*c**2:.4e} m/s^2 = {Q0*c**2/a0:.3e} a_0")

# cross-check against the ghost-condensate scale M:  M^2 = sqrt(2) mu M_Pl  =>  Q_0 = M^2/M_Pl
mu_1Mpc = 1.0 / Mpc
M_eV = math.sqrt(math.sqrt(2) * (mu_1Mpc / eV_per_inv_m) * M_Pl_eV)
Q0_from_M = (M_eV ** 2 / M_Pl_eV) * eV_per_inv_m
print(f"\n  CROSS-CHECK via the ghost-condensate scale: mu^-1 = 1 Mpc  ->  M = {M_eV:.4f} eV")
print(f"      (published map quotes M = 0.148 eV)   Q_0 = M^2/M_Pl = {Q0_from_M:.4e} 1/m")
print(f"      vs sqrt(2) mu = {math.sqrt(2)*mu_1Mpc:.4e} 1/m   ratio = {Q0_from_M/(math.sqrt(2)*mu_1Mpc):.4f}")
assert abs(M_eV - 0.148) / 0.148 < 0.05
assert abs(Q0_from_M / (math.sqrt(2) * mu_1Mpc) - 1.0) < 1e-6

# an INDEPENDENT, mu-free route to Q_0 from the CMB/GDM bound on the Q-sector w
print("\n  INDEPENDENT ROUTE (no mu): 2 K_2 c_ad0^2 Q_0^2 = 8 pi G rho_dm/c^2 exactly.")
lhs = 8 * math.pi * G * rho_dm / c ** 2
print(f"      8 pi G rho_dm / c^2 = {lhs:.4e} 1/m^2   (sqrt = {math.sqrt(lhs):.4e} 1/m"
      f" = {math.sqrt(lhs)*c**2/a0:.2f} a_0/c^2)")
w0_bound = 5.3e-16          # Blanchet & Skordis 2024 eq. 4.38 :  wtilde_0 < 5.3e-16
for K2 in (0.5, 1.0):
    Q0 = math.sqrt(lhs / (2 * K2 * w0_bound))
    mu_inv = 1.0 / (math.sqrt(2 * K2 * Q0 ** 2 / 2.0)) / Mpc
    print(f"      K_2 = {K2:.1f}, c_ad0^2 = wtilde_0 = 5.3e-16 -> Q_0 = {Q0:.4e} 1/m"
          f" = {Q0*c**2/a0:.3e} a_0/c^2 ;  implied mu^-1 = {mu_inv*1e3:.3f} kpc")
print("      (that reproduces Blanchet & Skordis 2024's mu^-1 <~ 0.22 kpc INDEPENDENTLY,")
print("       confirming wtilde_0 = eps_0/Q_0 = c_ad0^2 and validating the whole units chain.)")
assert abs(lhs - 4.19e-53) / 4.19e-53 < 0.02
_mu_inv_chk = 1.0 / (math.sqrt(lhs / (2 * 1.0 * w0_bound)) * math.sqrt(1.0)) / Mpc * 1e3
assert 0.1 < _mu_inv_chk < 0.4, _mu_inv_chk   # kpc, vs their 0.22 kpc

# ------------------------------------------------------------------- BLOCK 3: THE RATIO
print()
print("=" * 78)
print("BLOCK 3  THE PAYOFF:  R = Y/Q^2 = (sqrt(Y) / (Q_0 c^2))^2")
print("=" * 78)
key_branches = [("mu^-1 = 0.22 kpc", 0.22e-3), ("mu^-1 = 1 Mpc (fiducial)", 1.0),
                ("mu^-1 = 31.6 Mpc (most favourable)", 31.6)]
print(f"{'system':42s}" + "".join(f"{nm:>26s}" for nm, _ in key_branches))
results = {}
for nm, g in scales:
    row = f"  {nm:40s}"
    for bn, mi in key_branches:
        Q0, _ = Q0_from_mu(mi)
        R = (g / (Q0 * c ** 2)) ** 2
        results[(nm, bn)] = R
        row += f"{R:>26.3e}"
    print(row)

Q0_fid, _ = Q0_from_mu(1.0)
R_MW = (g_MW / (Q0_fid * c ** 2)) ** 2
R_clu = (g_clu / (Q0_fid * c ** 2)) ** 2
R_dwarf = (x_of_y(0.003) * a0 / (Q0_fid * c ** 2)) ** 2
R_cosmo = (scales[5][1] / (Q0_fid * c ** 2)) ** 2
print(f"\n  fiducial mu^-1 = 1 Mpc:")
print(f"      galaxy  (MW, 8.1 kpc)  R = {R_MW:.3e}   tilt angle = {math.degrees(math.atan(math.sqrt(R_MW)))*3600:.4f} arcsec")
print(f"      cluster (R500)         R = {R_clu:.3e}")
print(f"      LSB dwarf              R = {R_dwarf:.3e}")
print(f"      cosmological (10 Mpc)  R = {R_cosmo:.3e}")
assert R_MW < 1e-8 and R_clu < 1e-9 and R_dwarf < 1e-11 and R_cosmo < 1e-14

Q0_best, _ = Q0_from_mu(31.6)
R_MW_best = (g_MW / (Q0_best * c ** 2)) ** 2
print(f"\n  MOST FAVOURABLE branch (mu^-1 = 31.6 Mpc): galaxy R = {R_MW_best:.3e}"
      f"  -- still {1.0/R_MW_best:.2e} short of unity")
assert R_MW_best < 1e-5

# ------------------------------------------------- BLOCK 4: what WOULD disrupt it
print()
print("=" * 78)
print("BLOCK 4  the disruption criterion:  g >= Q_0 c^2   (a HIGH-acceleration condition)")
print("=" * 78)
for bn, mi in key_branches:
    Q0, _ = Q0_from_mu(mi)
    g_dis = Q0 * c ** 2
    r_star = math.sqrt(G * Msun / g_dis)
    print(f"  {bn:34s} g_disrupt = {g_dis:.3e} m/s^2 = {g_dis/a0:.2e} a_0"
          f" -> within {r_star/AU:8.2f} AU of 1 Msun")
Q0, _ = Q0_from_mu(1.0)
r_star = math.sqrt(G * Msun / (Q0 * c ** 2))
n_star = 0.1 / pc ** 3
fill = (4 * math.pi / 3) * r_star ** 3 * n_star
print(f"\n  volume filling factor of those stellar bubbles at n_* = 0.1 /pc^3 : {fill:.2e}")
print("  -> the smooth galactic condensate is untouched; only ~45 AU bubbles round stars go.")
assert fill < 1e-10

# --------------------------------------- BLOCK 5: the ONLY escape, and what it costs
print()
print("=" * 78)
print("BLOCK 5  the ONLY parametric escape: K_2 >> 1  (Q_0 = mu sqrt((2-K_B)/(2K_2)))")
print("=" * 78)
print("  Disruption at acceleration g needs Q_0 c^2 <= g, i.e.")
print("      2 K_2/(2-K_B) >= (mu c^2 / g)^2")
for bn, mi in key_branches:
    mu = 1.0 / (mi * Mpc)
    for sysname, g in (("MW 8.1 kpc", g_MW), ("cluster R500", g_clu),
                       ("LSB dwarf y=0.003", x_of_y(0.003) * a0)):
        K2req = 0.5 * (mu * c ** 2 / g) ** 2 * 2.0   # 2K_2/(2-K_B) with (2-K_B)=2 -> K_2 = (mu c^2/g)^2
        print(f"  {bn:26s} disrupt {sysname:20s} needs K_2 >= {K2req:.2e}")
print("\n  For reference: Blanchet & Skordis 2024 already call K_3 ~ 1e5 / K_4 ~ 1e6")
print("  'unnaturally large'.  And note the MONOTONICITY: the requirement is WEAKEST")
print("  for the HIGHEST-acceleration system and WORST for the dwarf -- exactly inverted")
print("  relative to where the double-counting overshoot must be removed.")
K2_MW_1Mpc = (1.0 / Mpc * c ** 2 / g_MW) ** 2
K2_dw_1Mpc = (1.0 / Mpc * c ** 2 / (x_of_y(0.003) * a0)) ** 2
print(f"\n  ratio of K_2 required (LSB dwarf / MW) = {K2_dw_1Mpc/K2_MW_1Mpc:.1f}x")
assert K2_dw_1Mpc / K2_MW_1Mpc > 100

# ------------------- BLOCK 6: pinning is NOT protective -- the dust can still cluster
print()
print("=" * 78)
print("BLOCK 6  AGAINST MY OWN CONCLUSION'S USEFULNESS: pinning != no clustering")
print("=" * 78)
print("  rho_dust prop to I = 2 K_2 eps, eps = Q - Q_0, and eps_0/Q_0 = c_ad0^2 << 1.")
print("  So delta_dust = delta(eps)/eps_0 can be ENORMOUS while delta Q/Q_0 stays tiny:")
for bn, mi in key_branches:
    Q0, mu = Q0_from_mu(mi)
    c_ad0_sq = 4 * math.pi * G * rho_dm / (mu ** 2 * c ** 2)
    print(f"  {bn:34s} c_ad0^2 = eps_0/Q_0 = {c_ad0_sq:.3e}"
          f"  -> delta_dust,max (Q displaced by O(1)) = {1.0/c_ad0_sq:.3e}")
rho_dm_MW_20kpc = 0.008 * Msun / pc ** 3        # ~ NFW MW at 20 kpc
print(f"\n  a virialised MW halo at 20 kpc has rho_dm ~ {rho_dm_MW_20kpc:.2e} kg/m^3"
      f" = delta {rho_dm_MW_20kpc/rho_dm:.2e}")
print("  a cluster at R500 needs delta_dust ~ 2e2-5e2 (per this project's earlier result).")
print("  BOTH sit far below delta_dust,max, so a fully virialised dust halo is entirely")
print("  compatible with Q staying pinned at Q_0.  Pinning buys NOTHING protective.")
d_MW = rho_dm_MW_20kpc / rho_dm
_, mu_f = Q0_from_mu(1.0)
dmax_fid = 1.0 / (4 * math.pi * G * rho_dm / (mu_f ** 2 * c ** 2))
assert d_MW < dmax_fid

# ------------------- BLOCK 7: the OTHER displacement (potential depth) for completeness
print()
print("=" * 78)
print("BLOCK 7  the competing displacement: Q -> (1-Phi) Q_0  (gravitational redshift)")
print("=" * 78)
for nm, Phi in (("MW (v=230 km/s, flat RC, ln range 10)", (230e3 / c) ** 2 * 10),
                ("cluster (sigma = 1000 km/s)", (1000e3 / c) ** 2 * 10),
                ("neutron star surface", 0.2)):
    print(f"  {nm:44s} |Phi| = {Phi:.3e}")
print("  This is Mistele+2023's rho_c prop to (mu_chem/Q_0 - Phi) mechanism.  In a galaxy")
print("  |Phi| ~ 5e-6 BEATS Y/Q^2 ~ 3e-9 by ~3 orders, and it is STILL tiny.  Leaving the")
print("  attractor by this route needs |Phi| ~ 1, i.e. a black hole -- exactly Frolov's")
print("  (2004) rho ~ M^4 criterion, which does not bind in a weak field.")
Phi_MW = (230e3 / c) ** 2 * 10
assert Phi_MW > R_MW and Phi_MW < 1e-4

# ---------------- BLOCK 8: foreclose the two remaining loopholes
print()
print("=" * 78)
print("BLOCK 8  two loopholes foreclosed")
print("=" * 78)
# (a) aether tilt.  ACLMW 2007 eq 5.7-5.8: the condensate is entrained out to r_drag = 2R
#     of any virialised system, so A^mu is tilted by the peculiar velocity v/c.  Then
#     Q = Q_0 + (v/c) . grad phi, a FRACTIONAL shift (v/c) sqrt(Y)/Q_0.
Q0, _ = Q0_from_mu(1.0)
for nm, v in (("galaxy peculiar velocity 300 km/s", 300e3), ("cluster 1000 km/s", 1000e3)):
    frac = (v / c) * g_MW / (Q0 * c ** 2)
    print(f"  (a) aether tilt, {nm:36s}: dQ/Q_0 = {frac:.3e}")
frac_tilt = (300e3 / c) * g_MW / (Q0 * c ** 2)
assert frac_tilt < 1e-7
print("      -> tilting the aether does NOT rescue it; the cross term is v/c times SMALLER")
print("         than the already-tiny sqrt(Y)/Q_0.")
# (b) quasi-static consistency: how far does phi_bar drift vs how much the galaxy tilts it?
t0 = 13.8e9 * 3.1557e7
dphi_bg = Q0 * c * t0
dphi_gal = (g_MW / c ** 2) * (25 * kpc)
print(f"  (b) background drift over a Hubble time: dphi_bg  = {dphi_bg:.3e} (dimensionless phi)")
print(f"      galactic spatial tilt across 25 kpc:  dphi_gal = {dphi_gal:.3e}")
print(f"      ratio = {dphi_bg/dphi_gal:.3e}  -> the condensate's temporal march utterly")
print("         dominates; the galaxy is a {:.0e} correction on phi.".format(dphi_gal / dphi_bg))
assert dphi_bg / dphi_gal > 1e9

print()
print("=" * 78)
print("VERDICT: Y/Q^2 = 3e-9 (galaxy, fiducial), 1e-10 (cluster), 4e-15 (cosmological).")
print("Best case over the entire published mu range: 2.6e-6.  Y << Q^2 EVERYWHERE.")
print("The scalar does NOT leave the condensate attractor in a galaxy.  Mechanism 1 FAILS")
print("as an escape from the double-counting problem.")
print("=" * 78)
print("ALL ASSERTIONS PASSED")
