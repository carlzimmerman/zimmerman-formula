#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
route5_caustics_multistream_2026.py
===================================
ROUTE 5 -- CAUSTICS AND MULTI-STREAMING as the support mechanism for the dark sector.

THE PROPOSAL UNDER TEST.  nbody_2026's stage 3 declined a particle run on the ground that
"the khronon dust is an irrotational potential flow, so it has no angular momentum, no
shell-crossing, and no substructure".  Route 5 says that is a statement about the SINGLE-STREAM
(Madelung / Zel'dovich) description, which is exactly the description that fails at a caustic.
Past a caustic the flow is multi-stream, and multi-streaming manufactures a genuine velocity
dispersion -- i.e. the (p_r, p_t) of virial order that two prior analyses flagged as decisive and
neither adjudicated.  If that dispersion supplies the support, the framework needs no second field,
no mediator, and -- the prize -- NO MODIFIED POISSON EQUATION IN THE BARYON SECTOR, hence no
phantom, hence NO Cassini quadrupole Q2 at all.

FIVE GATES (the run's standing gates).  Priced from the first line, not bolted on:
  (1) amplitude law / flat curves at the BTFR value   [threshold, nearly free -- see the deflation]
  (2) screening the FORCE, not the information
  (3) Q2 <= 5.2e-27 s^-2 at g_ext = 1.9-2.6 a0, AND the 1-AU monopole under per-planet EPM budgets
  (4) theoretical health: no ghost / gradient instability / Cherenkov, c_T = 1, w = -1, CMB intact
  (5) no double count: whatever carries Omega_dm must not ALSO feed the rotation curve

WHAT IS COMPUTED HERE, IN ORDER (number first, check written around the computed value):
  PART 1  the SIS identity sigma = v_c/sqrt(2), symbolically and numerically, both footings; and
          WHAT SETS THE TEMPERATURE -- answered by solving the Jeans equation, including the
          anisotropy dependence, which is where the irrotational premise bites.
  PART 2  when the framework's own dust forms caustics, with its OWN derived a_0(z).  Includes an
          ADVERSE-TO-THE-BRIEF correction: a_0(z) is back to ~1.00 a_0(0) by z ~ 10-20, so galaxy
          caustics do NOT form in a Newtonian regime.
  PART 3  THE OVERTURN.  Can the field multi-stream at all?  The semiclassical parameter, computed
          from stage 3's OWN k^4 dispersion relation, with a fuzzy-DM negative control.
  PART 4  A 1D RADIAL MULTI-STREAM RUN -- the calculation stage 3 declined.  Cold irrotational
          initial conditions, shells allowed to cross, self-consistent enclosed mass.  Measures the
          caustic epoch, the post-caustic radial dispersion, and the density slope.
  PART 5  THE CRUX.  Does a purely-clustering dark sector with the right temperature reproduce the
          RAR's tightness, or is it CDM with a fine-tuned profile?  Acceleration-scale running and
          scatter propagation, both computed.
  PART 6  THE PRIZE, audited: is the Q2 escape real?  And the trilemma the route actually produces.
  PART 7  which nbody stage is overturned, with the direction of every correction stated.

HONESTY CONSTRAINTS carried from the programme: both footings on every dimensionful result; every
"dead" verified as hard as every "works"; negative controls on every estimator; and where a number
is taken from outside literature it is labelled UNVERIFIED-EXTERNAL.
"""

import sys
import numpy as np
import sympy as sp

FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


# ------------------------------------------------------------------ constants (SI)
G = 6.67430e-11
C = 2.99792458e8
HBAR = 1.054571817e-34
MPC = 3.0856775814913673e22
KPC = MPC / 1000.0
PC = KPC / 1000.0
AU = 1.495978707e11
MSUN = 1.98892e30
YR = 3.155693e7
GYR = 1e9 * YR

H0 = 67.4 * 1000.0 / MPC
OM_M, OM_L, OM_B = 0.315, 0.685, 0.0493
RHO_CRIT0 = 3 * H0 ** 2 / (8 * np.pi * G)
RHO_M0 = OM_M * RHO_CRIT0

A0_CANON = 9.3619e-11
A0_ALT = 1.1279e-10
FOOTINGS = (("canonical", A0_CANON), ("alt", A0_ALT))

# framework's derived a_0(z) law (stage 17 / stage 26), nu_0 window
NU0_FLOOR, NU0_CEIL = 2.14e-5, 1.77e-4

# stage 3's own k^4 machinery
HBARC_EVM = 1.9733e-7                 # hbar c in eV m
M_NAT_EV = 2.24e-3                    # rho_Lambda^(1/4), the natural condensate scale
FUZZY_M_EV = 1e-22

print(__doc__)


def Hz(z):
    return H0 * np.sqrt(OM_M * (1 + z) ** 3 + OM_L)


def a0_of_z(z, nu0, a0):
    nu = nu0 * (1 + z) ** 3
    return a0 * np.sqrt(np.sqrt(1 + nu0 ** 2) / np.sqrt(1 + nu ** 2))


# =================================================================================================
print("=" * 100)
print("PART 1 -- THE SINGULAR ISOTHERMAL SPHERE IDENTITY, AND WHAT SETS THE TEMPERATURE")
print("=" * 100)

r_, s_, M_, a0_, G_, b_ = sp.symbols("r sigma M a_0 G beta", positive=True)

# Carl's amplitude law (the phantom / halo density that makes the rotation curve flat at BTFR):
rho_amp = sp.sqrt(G_ * M_ * a0_) / (4 * sp.pi * G_ * r_ ** 2)
# Singular isothermal sphere:
rho_sis = s_ ** 2 / (2 * sp.pi * G_ * r_ ** 2)

sol = sp.solve(sp.Eq(rho_amp, rho_sis), s_)
sigma_sym = sp.simplify(sol[0])
vc_sym = (G_ * M_ * a0_) ** sp.Rational(1, 4)          # v_c^4 = G M a_0
ratio_sym = sp.simplify(sigma_sym / vc_sym)

check(sp.simplify(ratio_sym - 1 / sp.sqrt(2)) == 0,
      f"1.1  SYMBOLIC: rho_amp == rho_SIS  <=>  sigma = v_c/sqrt(2) exactly.  sigma = {sigma_sym}, "
      f"sigma/v_c = {ratio_sym}",
      "the amplitude law IS the statement 'the dark sector is an SIS with sigma = v_c/sqrt(2)'")

print("\n   M_b = 1e11 Msun spiral")
print("   footing        a_0 [m/s^2]     v_c [km/s]     sigma [km/s]    sigma/v_c")
ratios = []
for name, a0 in FOOTINGS:
    vc = (G * 1e11 * MSUN * a0) ** 0.25
    sig = vc / np.sqrt(2)
    ratios.append(sig / vc)
    print(f"   {name:<12s} {a0:>10.4e}   {vc/1e3:>10.3f}   {sig/1e3:>12.3f}    {sig/vc:>12.9f}")

check(all(abs(x - 2 ** -0.5) < 1e-15 for x in ratios),
      "1.2  NUMERIC both footings: sigma/v_c = 0.707106781 to machine precision",
      "matches the brief's 132.764 / 139.094 km/s")

# --- THE DEFLATION TEST.  Does this identity carry ANY information about a_0 or about the kernel?
d_ratio_d_lna0 = sp.simplify(a0_ * sp.diff(sp.log(ratio_sym), a0_))
d_ratio_d_lnM = sp.simplify(M_ * sp.diff(sp.log(ratio_sym), M_))
check(d_ratio_d_lna0 == 0 and d_ratio_d_lnM == 0,
      f"1.3  DEFLATION: d ln(sigma/v_c)/d ln a_0 = {d_ratio_d_lna0}, d/d ln M = {d_ratio_d_lnM}. "
      "The ratio 1/sqrt(2) is a property of rho ~ r^-2 ALONE",
      "*** so 'sigma = v_c/sqrt(2)' is a THIRD face of the run's deflation: SIS <=> flat curve <=> "
      "amplitude law.  It is NOT evidence for Carl's a_0 and NOT evidence for his kernel ***")

# --- WHAT SETS THE TEMPERATURE?  Solve the spherical Jeans equation for rho ~ r^-2, sigma_r const.
#     d(rho sigma_r^2)/dr + 2 beta rho sigma_r^2 / r = - rho v_c^2 / r
sr = sp.Symbol("sigma_r", positive=True)
A = sp.Symbol("A", positive=True)                 # rho = A/r^2
rho_p = A / r_ ** 2
vc2 = sp.Symbol("v_c2", positive=True)
jeans = sp.diff(rho_p * sr ** 2, r_) + 2 * b_ * rho_p * sr ** 2 / r_ + rho_p * vc2 / r_
sr2_sol = sp.solve(sp.Eq(jeans, 0), sr ** 2)
sr2 = sp.simplify(sr2_sol[0])
check(sp.simplify(sr2 - vc2 / (2 - 2 * b_)) == 0,
      f"1.4  JEANS: for rho ~ r^-2 with constant sigma_r, sigma_r^2 = {sr2} = v_c^2/(2-2 beta)",
      "so the 'temperature' is FORCED by the profile + hydrostatic support; it is an output of "
      "rho ~ r^-2, not an independent fact.  ISOTROPIC beta=0 reproduces v_c^2/2")

check(sp.limit(sr2, b_, 1, "-") == sp.oo,
      "1.5  *** THE IRROTATIONAL PREMISE BITES HERE: beta -> 1 (PURELY RADIAL orbits, which is what "
      "an irrotational flow's shell-crossing produces in spherical symmetry) sends the required "
      "sigma_r^2 to INFINITY.  A radially-anisotropic multi-stream system CANNOT support an SIS ***",
      "support needs TANGENTIAL dispersion, i.e. genuinely 3D (non-spherical) caustics.  Priced "
      "in PART 4 (1D, beta = 1 by construction) and named as UNDETERMINED for 3D in PART 7")

# how much tangential dispersion is needed?
beta_needed = sp.solve(sp.Eq(sr2, vc2 / 2 * sp.Symbol("k", positive=True)), b_)
info("1.6  required anisotropy", "sigma_r^2 = v_c^2/2 needs beta = 0 exactly; sigma_r^2 = v_c^2 "
     "needs beta = 1/2; any beta >= 1 is unsupportable at ANY finite dispersion")


# =================================================================================================
print()
print("=" * 100)
print("PART 2 -- WHEN DOES THE FRAMEWORK'S OWN DUST FORM CAUSTICS?")
print("=" * 100)
print("""
  The brief supplied a premise: 'MOND is OFF early, a_0(1090)/a_0(0) = 0.0060, so early collapse is
  essentially Newtonian.'  That premise is CHECKED here against the framework's own derived law
  before it is used.  a_0(z) = a_0 sqrt( sqrt(1+nu_0^2)/sqrt(1+nu^2) ),  nu = nu_0 (1+z)^3,
  nu_0 in [2.14e-5, 1.77e-4]  (stage 17 / stage 26).
""")

print("      z        a_0(z)/a_0(0)  [nu_0 floor]   [nu_0 ceil]")
a0z_tab = {}
for z in (0, 1, 2, 3, 5, 10, 17, 20, 30, 50, 100, 1090):
    lo = a0_of_z(z, NU0_FLOOR, 1.0)
    hi = a0_of_z(z, NU0_CEIL, 1.0)
    a0z_tab[z] = (lo, hi)
    print(f"   {z:>6d}          {lo:>12.5f}   {hi:>12.5f}")

check(abs(a0z_tab[1090][0] - 0.0060) < 3e-4 and abs(a0z_tab[1090][1] - 0.0021) < 3e-4,
      f"2.1  the banked recombination suppression is reproduced: {a0z_tab[1090][0]:.4f} (floor) / "
      f"{a0z_tab[1090][1]:.4f} (ceil) -- the corpus's 0.0060 / 0.0021",
      "so this is the framework's own law, not a re-derivation")

zt_lo = NU0_FLOOR ** (-1.0 / 3.0) - 1
zt_hi = NU0_CEIL ** (-1.0 / 3.0) - 1
check(a0z_tab[3][0] > 0.999 and a0z_tab[3][1] > 0.999 and a0z_tab[5][1] > 0.99,
      f"2.2  *** ADVERSE TO THE BRIEF'S PREMISE: the transition is at z_t = nu_0^(-1/3)-1 = "
      f"{zt_hi:.1f} (ceil) to {zt_lo:.1f} (floor).  By z = 5 a_0(z) is already "
      f"{min(a0z_tab[5]):.4f}-{max(a0z_tab[5]):.4f} of today's.  Galaxy-scale collapse (z ~ 2-5) "
      "happens with MOND FULLY ON, not 'essentially Newtonian' ***",
      "DIRECTION OF THE CORRECTION: it makes caustics form EARLIER (MOND boosts the collapse), so "
      "it runs IN FAVOUR of caustics existing -- I state it because the brief's reason was wrong "
      "even though its conclusion (caustics form) survives")

# ---- linear sigma(M) with an Eisenstein-Hu (zero-baryon) transfer function, normalised to sigma_8
h = H0 * MPC / 1e5          # dimensionless Hubble parameter (H0 = 100 h km/s/Mpc)
OM_H2 = OM_M * h * h
OB_H2 = OM_B * h * h
NS = 0.965
SIGMA8 = 0.811
THETA = 2.7255 / 2.7


def T_EH98_zb(k_hMpc):
    """Eisenstein & Hu 1998 'zero-baryon' shape (their eqs 26-31).  k in h/Mpc."""
    k = np.atleast_1d(k_hMpc) * h                      # -> 1/Mpc
    s = 44.5 * np.log(9.83 / OM_H2) / np.sqrt(1 + 10 * OB_H2 ** 0.75)      # Mpc
    alpha_g = (1 - 0.328 * np.log(431 * OM_H2) * OB_H2 / OM_H2
               + 0.38 * np.log(22.3 * OM_H2) * (OB_H2 / OM_H2) ** 2)
    gam_eff = OM_M * h * (alpha_g + (1 - alpha_g) / (1 + (0.43 * k * s) ** 4))
    q = k * THETA ** 2 / gam_eff
    L0 = np.log(2 * np.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def _sigma_R(R_hMpc, norm=1.0, npts=40000):
    lk = np.linspace(np.log(1e-4), np.log(5e2), npts)
    k = np.exp(lk)
    W = 3 * (np.sin(k * R_hMpc) - k * R_hMpc * np.cos(k * R_hMpc)) / (k * R_hMpc) ** 3
    integ = k ** (3 + NS) * T_EH98_zb(k) ** 2 * W ** 2
    return np.sqrt(norm * np.trapz(integ, lk) / (2 * np.pi ** 2))


_norm = (SIGMA8 / _sigma_R(8.0)) ** 2


def sigma_M(M_msun):
    R = (3 * M_msun * MSUN / (4 * np.pi * RHO_M0)) ** (1.0 / 3.0) / MPC * h   # Lagrangian R, h^-1 Mpc
    return _sigma_R(R, _norm)


check(abs(_sigma_R(8.0, _norm) - SIGMA8) < 1e-6,
      f"2.3  P(k) normalisation control: sigma_8 = {_sigma_R(8.0, _norm):.4f} (target {SIGMA8})")
# RESOLUTION CONTROL -- the oscillatory top-hat window is easy to under-sample, and a coarse grid
# silently INFLATES sigma(M) (caught here at 6000 points: sigma(1e12) came out 15.3 instead of 2.5).
_res = [_sigma_R((3*1e12*MSUN/(4*np.pi*RHO_M0))**(1/3.)/MPC*h, _norm, n) for n in (20000, 40000, 80000)]
check(max(_res)/min(_res) - 1 < 0.01,
      f"2.3b RESOLUTION CONTROL on sigma(1e12): {_res[0]:.4f} / {_res[1]:.4f} / {_res[2]:.4f} at "
      f"20k/40k/80k grid points -- converged to {100*(max(_res)/min(_res)-1):.3f}%",
      "TWO estimator errors were caught by the range check 2.4 on the first two runs -- a coarse "
      "6000-point grid, and h mis-defined by 100x.  BOTH inflated sigma(M), i.e. BOTH would have "
      "been false WINS (caustics too early).  Recorded per the standing rule")
s_1e12 = sigma_M(1e12)
check(0.9 < s_1e12 < 4.0,
      f"2.4  sanity: sigma(M = 1e12 Msun) = {s_1e12:.3f}   (LambdaCDM literature ~ 2.2-2.6)",
      "UNVERIFIED-EXTERNAL comparison; the check is a range, not an equality")


def D_growth(z):
    """LambdaCDM linear growth, normalised D(0)=1 (Carroll-Press-Turner fit)."""
    def g(zz):
        E2 = OM_M * (1 + zz) ** 3 + OM_L
        om = OM_M * (1 + zz) ** 3 / E2
        ol = OM_L / E2
        return 2.5 * om / (om ** (4.0 / 7.0) - ol + (1 + om / 2) * (1 + ol / 70))
    return (g(z) / (1 + z)) / g(0.0)


def z_of_D(target):
    zs = np.linspace(0, 60, 60001)
    Ds = np.array([D_growth(z) for z in zs])
    if Ds[0] < target:
        return -1.0
    return float(np.interp(-target, -Ds, zs))


DELTA_C = 1.686        # spherical top-hat
DELTA_ZA = 1.0         # Zel'dovich: FIRST caustic when D * lambda_1 = 1; for a 1-D collapse
print("\n   caustic / collapse epoch for a 1-sigma peak (Newtonian growth -- the CONSERVATIVE case)")
print("   M [Msun]    sigma(M)     z_caustic (ZA, delta=1)   z_collapse (top-hat, 1.686)")
zc_tab = {}
for M in (1e9, 1e10, 1e11, 1e12, 1e13, 1e14):
    sM = sigma_M(M)
    zc = z_of_D(DELTA_ZA / sM)
    zv = z_of_D(DELTA_C / sM)
    zc_tab[M] = (zc, zv)
    print(f"   {M:>8.0e}    {sM:>7.3f}     {zc:>18.2f}      {zv:>22.2f}")

check(all(zc_tab[M][0] > 0 for M in (1e9, 1e10, 1e11, 1e12)),
      f"2.5  *** CAUSTICS FORM.  A 1-sigma galaxy-scale (1e12 Msun) perturbation reaches the "
      f"Zel'dovich caustic at z = {zc_tab[1e12][0]:.2f} and virialises at z = {zc_tab[1e12][1]:.2f}; "
      f"1e9 Msun caustics at z = {zc_tab[1e9][0]:.2f}.  The dark sector is MULTI-STREAM inside every "
      "galaxy halo today ***",
      "and this is the Newtonian growth rate -- the framework's own MOND-on collapse is FASTER "
      "(stage 26: 1.34-1.96x), so these redshifts are LOWER BOUNDS on the caustic epoch")

# is the collapse deep-MOND at turnaround?  compute y = g_N/a_0(z) at r_ta = 2 r_200
print("\n   is the collapse Newtonian or MONDian at turnaround?   y = g_N(r_ta)/a_0(z), r_ta = 2 r_200")
print("   M [Msun]   z_ta    r_200 [kpc]   y (canonical)   y (alt)     regime")
y_min = 1e99
for M, z in ((1e9, 6.0), (1e10, 5.0), (1e11, 4.0), (1e12, 2.5), (1e13, 1.2)):
    rho_c = 3 * Hz(z) ** 2 / (8 * np.pi * G)
    r200 = (3 * M * MSUN / (800 * np.pi * rho_c)) ** (1.0 / 3.0)
    rta = 2 * r200
    gN = G * M * MSUN / rta ** 2
    ys = []
    for name, a0 in FOOTINGS:
        a0z = a0_of_z(z, NU0_CEIL, a0)
        ys.append(gN / a0z)
    y_min = min(y_min, min(ys))
    reg = "deep-MOND" if max(ys) < 1 else ("transition" if min(ys) < 10 else "Newtonian")
    print(f"   {M:>8.0e}  {z:>5.1f}    {r200/KPC:>9.2f}   {ys[0]:>13.4f}   {ys[1]:>8.4f}    {reg}")

check(y_min < 10.0,
      f"2.6  turnaround sits in or below the MOND transition (min y = {y_min:.3f}), so the "
      "framework's caustics form under a BOOSTED force, confirming 2.2's direction",
      "consequence: if the modified Poisson equation is kept, caustic formation is EARLIER and the "
      "clustered dark sector is MORE concentrated -- which makes the double count WORSE, not better")
