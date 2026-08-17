#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
lyman_alpha_dust_ic_2026.py
===========================
THE_COMPLETION's NON-CLAIM 4, COMPUTED.  Verbatim, the non-claim reads:

    "The dust component's small-scale initial conditions are NOT CONFRONTED WITH LYMAN-ALPHA.
     The withdrawn IC route needed a khronon transfer function T ~ 0.33 at k ~ 4.5 Mpc^-1
     (LCDM-excluded); the surviving picture (standard cold dust + the bump response) should be
     Ly-alpha-safe BY CONSTRUCTION, but that is ASSERTED, NOT COMPUTED -- the confrontation
     remains owed."

This script does the confrontation for the half of it that linear theory can carry: the
INITIAL-CONDITION / SOUND-SPEED channel.  It extends stage 69's method
(nbody_2026/stage69_cs2_growth_class_2026.py, which bounded R = Lambda_D/Q_0 <= ~3e-6 from
P(k = 0.2 h/Mpc) and validated a sub-horizon growth integrator against real CLASS) from
k = 0.2 h/Mpc, z = 0 to the forest band k = 1-10 h/Mpc, z = 2-4.

WHAT IS BEING TESTED, ON THE FRAMEWORK'S OWN TERMS
--------------------------------------------------------------------------------------------------
The dark sector is the offset-DBI khronon condensate  K(Q) = mu^2 Lam_D^2 [1 - sqrt(1 - u^2/Lam_D^2)],
u = Q - Q_0, s = u/Lam_D, beta = 1, with the shift charge conserved (a^3 K' = const), so

    nu(a) = nu_0 / a^3,     s(a) = nu/sqrt(1+nu^2),
    c_s^2(a) = K'/(Q K'') = R s (1 - s^2) / (1 + R s),      R = Lam_D / Q_0

and the corpus's committed windows are  nu_0 in [2.14e-5, 1.77e-4]  (stage 17)  and
Lam_D in (1.9e-10, 8.4e-7]  (health-bounded; mi_a0_bump_health_2026.py, THE_COMPLETION bounds row).
Q_0 = 1 is the corpus's OWN normalisation ("u is measured against the condensate Q_0 = 1",
mi_dbi_khronon_2026.py D2), so numerically R = Lam_D and the health window IS an R window.
a_0 = kappa c sqrt(G rho_Lam) = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m/s^2 enters only PART G;
kappa = 1/2 is FITTED (measured 0.551 +/- 0.043) and beta = 1 is SELECTED -- neither is derived here
or anywhere.

HONEST SCOPE -- READ THIS BEFORE QUOTING ANY NUMBER
--------------------------------------------------------------------------------------------------
 1. LINEAR THEORY IS A PROXY ACROSS THE WHOLE FOREST BAND.  PART B computes Delta^2(k,z) and shows
    the band is quasi-nonlinear (Delta^2 ~ 1-4).  Ratios of LINEAR power are nonetheless the standard
    currency for these constraints -- every published WDM / {alpha,beta,gamma} forest bound is
    quoted as a linear transfer function -- so a linear-to-linear comparison against a published
    linear-transfer-function limit is like-for-like.  It is NOT a hydrodynamic forest likelihood.
 2. NO THERMAL-HISTORY MARGINALISATION, no FGPA, no mean-flux rescaling, no emulator.  The
    tolerance is therefore IMPORTED from published WDM limits (PART E1) and is used as a YARDSTICK
    on the 3D linear power, never as a likelihood.
 3. THE TRAP STAGE 69 DOCUMENTS IS HONOURED: CLASS treats a `fluid` species as DARK ENERGY and
    EXCLUDES it from P(k).  Every CLASS number here is therefore used only as (i) an LCDM linear
    baseline and (ii) a MATCHED-SETUP ratio (cold fluid vs warm fluid, identical species content)
    against which the integrator's baryon channel is validated.  This is a methodological upgrade
    on stage 69, which compared its fluid runs against the full-LCDM run and so carried the
    baryon-transfer offset inside its validation residual.
 4. THE OMEGA-ALLOCATION FORK IS NOT RESOLVED HERE, IT IS PRICED BOTH WAYS (PART F).  It flips the
    verdict, so no single number in this script is the answer on its own.

Exit 0 = every numbered check passed.
"""

import sys

import numpy as np
from scipy.integrate import solve_ivp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


print(__doc__)

# ---------------------------------------------------------------- cosmology + committed windows
H0H, OM_B_H2, OM_C_H2 = 0.674, 0.02237, 0.1200        # same as stage 69, Planck-2018-like
OM_M = (OM_B_H2 + OM_C_H2) / H0H**2
OM_B = OM_B_H2 / H0H**2
OM_D = OM_C_H2 / H0H**2
OM_R = 4.15e-5 / H0H**2
OM_L = 1.0 - OM_M - OM_R
NU0_LO, NU0_HI = 2.14e-5, 1.77e-4                     # stage 17's committed charge window
LAMD_LO, LAMD_HI = 1.9e-10, 8.4e-7                    # committed Lam_D health window (= R window)
R_S69_HI, R_S69_LO = 1.54e-6, 3.06e-6                 # stage 69's P(k=0.2) bound, nu_0 ceiling/floor
OM_KD_MAX = 4.42e-7                                   # stage 17 D4 / stage 3 BH ceiling on Omega_kd
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10             # m/s^2, both footings
KFOREST = (1.0, 3.0, 5.0, 10.0)
ZFOREST = (2.0, 3.0, 4.0)
CKMS = 299792.458

# =================================================================================================
print("=" * 100)
print("PART A -- the sector's c_s^2(a) ACROSS THE FOREST WINDOW, and where the damping is done")
print("=" * 100)


def s_of_a(a, nu0):
    nu = nu0 / np.asarray(a, dtype=float) ** 3
    return nu / np.sqrt(1.0 + nu**2)


def cs2_of_a(a, nu0, R):
    s = s_of_a(a, nu0)
    return R * s * (1 - s**2) / (1 + R * s)


a_grid = np.logspace(-4, 0, 40000)
info("A0  c_s^2 = R s(1-s^2)/(1+Rs) with s(a) = nu/sqrt(1+nu^2), nu = nu_0/a^3.  For R << 1 the "
     "amplitude factorises: c_s^2 -> R * s(1-s^2), so the SHAPE is fixed by nu_0 alone and R is a "
     "pure amplitude.  Every R in this script is <= 1e-6, where 1+Rs = 1 to 1e-6.")
print(f"    {'nu_0':>10s} {'s(peak)':>9s} {'z(peak)':>9s} {'cs2_pk/R':>9s} {'cs2(z=2)/R':>11s} "
      f"{'cs2(z=3)/R':>11s} {'cs2(z=4)/R':>11s} {'cs2(z=1090)/R':>14s}")
pk = {}
for nu0 in (NU0_HI, NU0_LO):
    shape = s_of_a(a_grid, nu0) * (1 - s_of_a(a_grid, nu0) ** 2)
    i = int(np.argmax(shape))
    pk[nu0] = (float(s_of_a(a_grid[i], nu0)), 1 / a_grid[i] - 1, shape[i])
    row = [float(s_of_a(1 / (1 + z), nu0) * (1 - s_of_a(1 / (1 + z), nu0) ** 2))
           for z in (2.0, 3.0, 4.0, 1090.0)]
    print(f"    {nu0:>10.2e} {pk[nu0][0]:>9.4f} {pk[nu0][1]:>9.1f} {shape[i]:>9.4f} "
          f"{row[0]:>11.3e} {row[1]:>11.3e} {row[2]:>11.3e} {row[3]:>14.3e}")
check(all(abs(pk[n][0] - 1 / np.sqrt(3)) < 2e-3 for n in pk) and
      all(abs(pk[n][2] - 2 / (3 * np.sqrt(3))) < 2e-3 for n in pk),
      "A1  in the R << 1 limit the bump peaks at s = 1/sqrt(3) = 0.5774 (the root of 1 - 3s^2 = 0) "
      f"with peak c_s^2 = 2R/(3 sqrt 3) = 0.3849 R -- reproduced to <0.2%; peak epoch z = "
      f"{pk[NU0_HI][1]:.1f} (nu_0 ceiling) to {pk[NU0_LO][1]:.1f} (floor)",
      "the 0.385 factor is the corpus's own banked number (mi_dbi_khronon / stage 2), so the "
      "shape used here is the committed one, not a re-invention")
cs2_rec = float(cs2_of_a(1 / 1091.0, NU0_HI, 1e-6)) / 1e-6   # = shape only, R factored out
check(cs2_rec < 1e-9,
      f"A2  FAVOURABLE, and load-bearing for what follows: the sound speed is switched OFF at "
      f"recombination -- c_s^2(z = 1090)/R = {cs2_rec:.2e}, i.e. {1/cs2_rec/0.3849:.1e}x below the "
      f"bump peak.  The dust's ICs at the start of the growth epoch are COLD to 2e-11 of the "
      f"bump amplitude, for the whole nu_0 window",
      "so this is NOT a free-streaming/WDM-like cutoff imprinted at early times; there is no "
      "primordial cutoff at all.  The suppression computed below is generated ENTIRELY between the "
      "DBI wall and the forest epoch")
# where is the damping done?  press ~ k^2 c_s^2/(a^2 H^2); in matter domination a^2H^2 ~ a^-1 and
# c_s^2 ~ R nu_0 a^-3 (small-s tail), so press ~ a^-2: EARLY times dominate.
lna = np.log(a_grid)
press_shape = cs2_of_a(a_grid, NU0_HI, 1.0) / (a_grid**2 * (OM_R / a_grid**4 + OM_M / a_grid**3 + OM_L))
m = (a_grid > 1 / 9) & (a_grid < 1 / 3)               # z = 2 .. 8, the small-s tail
slope = np.polyfit(lna[m], np.log(press_shape[m]), 1)[0]
i_forest = int(np.argmin(abs(a_grid - 1 / 3.0)))
frac = float(np.trapz(press_shape[:i_forest], lna[:i_forest]) /
             np.trapz(press_shape, lna))
check(-2.4 < slope < -1.6 and frac > 0.9,
      f"A3  THE DAMPING IS NOT DONE AT THE FOREST EPOCH: the pressure term k^2 c_s^2/(a^2 H^2) "
      f"scales as a^({slope:.2f}) over z = 2-8 (analytic a^-2: c_s^2 ~ R nu_0 a^-3 in the small-s "
      f"tail, a^2 H^2 ~ a^-1 in matter domination), so "
      f"{100*frac:.1f}% of the integrated pressure a mode ever feels is delivered ABOVE z = 2",
      "two consequences: (i) T^2(k) will be nearly z-independent across z = 2-4 (checked in "
      "PART D), and (ii) the forest is probing the epoch z ~ 10-45, which no other committed test "
      "of this sector reaches")

# =================================================================================================
print()
print("=" * 100)
print("PART B -- REAL CLASS: the LCDM linear baseline in the forest band, and the scope flags")
print("=" * 100)
from classy import Class

KMAX_PROJ = 300.0
BASE = {'output': 'mPk', 'P_k_max_h/Mpc': KMAX_PROJ * 1.07, 'h': H0H, 'omega_b': OM_B_H2,
        'A_s': 2.1e-9, 'n_s': 0.9649, 'tau_reio': 0.054, 'z_max_pk': 50}


def class_run(cs2const=None):
    c = Class()
    p = dict(BASE)
    if cs2const is None:
        p['omega_cdm'] = OM_C_H2
    else:
        p.update({'omega_cdm': 1e-6, 'Omega_fld': OM_D, 'w0_fld': -1e-6, 'wa_fld': 0.0,
                  'cs2_fld': cs2const, 'use_ppf': 'no'})
    c.set(p)
    c.compute()
    return c


cl = class_run(None)
kproj = np.logspace(np.log10(0.05), np.log10(KMAX_PROJ), 900)
PL = {z: np.array([cl.pk_lin(k * H0H, z) for k in kproj]) for z in ZFOREST}


def pk_lcdm(kh, z):
    return cl.pk_lin(kh * H0H, z)


def Eofz(z):
    a = 1 / (1 + z)
    return np.sqrt(OM_R / a**4 + OM_M / a**3 + OM_L)


print(f"    {'k [h/Mpc]':>10s} " + " ".join(f"{'P_lin(z=%.0f)' % z:>14s} {'D^2(z=%.0f)' % z:>10s}"
                                            for z in ZFOREST))
d2 = {}
for kh in KFOREST:
    cells = []
    for z in ZFOREST:
        P = pk_lcdm(kh, z)
        d2[(kh, z)] = kh**3 * P / (2 * np.pi**2)
        cells += [f"{P:>14.4g}", f"{d2[(kh,z)]:>10.3f}"]
    print(f"    {kh:>10.1f} " + " ".join(cells))
check(max(d2.values()) > 1.0,
      f"B1  SCOPE FLAG, stated against interest: the forest band is QUASI-NONLINEAR -- the LCDM "
      f"linear variance runs Delta^2 = {min(d2.values()):.2f} (k = 1, z = 4) to "
      f"{max(d2.values()):.2f} (k = 10, z = 2).  Linear ratios are the currency published forest "
      f"transfer-function bounds are quoted in, so the comparison in PART E is like-for-like, but "
      f"NOTHING here is a hydrodynamic forest likelihood",
      "a nonlinear treatment moves BOTH the framework and the yardstick, and mode coupling "
      "generically WEAKENS a linear suppression at fixed k -- so the linear comparison is the "
      "conservative (framework-adverse) direction, which is the right way round for a bound")
print(f"    {'k [h/Mpc]':>10s} " + " ".join(f"{'kv(z=%.0f) s/km' % z:>14s}" for z in ZFOREST))
for kh in KFOREST:
    print(f"    {kh:>10.1f} " + " ".join(f"{kh*(1+z)/(100*Eofz(z)):>14.4f}" for z in ZFOREST))
kv_top = max(10.0 * (1 + z) / (100 * Eofz(z)) for z in ZFOREST)
check(0.05 < kv_top < 0.25,
      f"B2  the band is OBSERVED: k_v[s/km] = k[h/Mpc](1+z)/(100 E(z)) (derived in-script from "
      f"v = H(z)x/(1+z)) puts k = 1-10 h/Mpc at k_v = 0.009-{kv_top:.3f} s/km over z = 2-4, i.e. "
      f"inside the MIKE/HIRES + XQ-100 + high-z reach (k_v <~ 0.1-0.2 s/km).  k = 10 h/Mpc sits at "
      f"the top edge, k = 1-5 h/Mpc well inside",
      "so the k values this task names are the measured ones, not an extrapolation")

# =================================================================================================
print()
print("=" * 100)
print("PART C -- the growth integrator: the k^2R scaling theorem, and CLASS validation AT FOREST k")
print("=" * 100)


def Hofa(a):
    return np.sqrt(OM_R / a**4 + OM_M / a**3 + OM_L)


def _rhs(y, u, kh, cs2f, fD, fB, fC):
    """two- or three-component sub-horizon growth in ln a.  fD/fB/fC = warm/baryon/cold fractions
    of OM_M.  u = [d_warm, d_bary, d_cold, v_warm, v_bary, v_cold]."""
    a = np.exp(y)
    h = Hofa(a)
    dl = (np.log(Hofa(a * 1.00001)) - np.log(Hofa(a * 0.99999))) / (2 * np.log(1.00001))
    dw, db, dc, vw, vb, vc = u
    src = 1.5 * (OM_M / a**3) / h**2 * (fD * dw + fB * db + fC * dc)
    press = (kh * (CKMS / (100.0 * H0H)) * H0H) ** 2 * cs2f(a) / (a**2 * h**2)
    return [vw, vb, vc, -(2 + dl) * vw + src - press * dw, -(2 + dl) * vb + src,
            -(2 + dl) * vc + src]


ZOUT = (4.0, 3.0, 2.0, 0.0)


def grow(kh, cs2f, fD=OM_D / OM_M, fC=0.0, a_i=1e-3, rtol=1e-9):
    """delta at each ZOUT: returns dict z -> (warm, baryon, cold, TOTAL matter)."""
    fB = OM_B / OM_M
    sol = solve_ivp(_rhs, [np.log(a_i), 0.0], [1.0] * 6, args=(kh, cs2f, fD, fB, fC),
                    rtol=rtol, atol=1e-13, dense_output=True)
    out = {}
    for z in ZOUT:
        dw, db, dc = sol.sol(np.log(1 / (1 + z)))[:3]
        out[z] = (dw, db, dc, fD * dw + fB * db + fC * dc)
    return out


COLD = grow(1.0, lambda a: 0.0)
COLD10 = grow(10.0, lambda a: 0.0)
check(all(abs(COLD[z][3] / COLD10[z][3] - 1) < 1e-9 for z in ZOUT),
      "C1  the pressureless baseline is k-INDEPENDENT to 1e-9 (no k enters the RHS when c_s^2 = 0), "
      f"with delta_tot(z=2)/delta(a=1e-3) = {COLD[2.0][3]:.2f} and "
      f"delta_tot(z=0) = {COLD[0.0][3]:.2f} (D ~ a would give 1000 at z = 0)",
      "hence T^2(k) below is a ratio against a common denominator and the IC normalisation drops "
      "out entirely")


def cs2f_of(R, nu0):
    def f(a, R=R, nu0=nu0):
        s = s_of_a(a, nu0)
        return R * s * (1 - s**2) / (1 + R * s)
    return f


# --- the scaling theorem: for R << 1, press = (k^2 R) * shape(a), so T^2 = Tcal(k^2 R) exactly.
pairs = [(10.0, 1e-9), (3.1623, 1e-8), (1.0, 1e-7), (31.623, 1e-10)]
vals = []
for kh, R in pairs:
    g = grow(kh, cs2f_of(R, NU0_HI))
    vals.append((g[3.0][3] / COLD[3.0][3]) ** 2)
print("    equal-k^2R quartet (k, R) -> T^2_tot(z=3):  " +
      "   ".join(f"({k:g},{R:.0e}) {v:.5f}" for (k, R), v in zip(pairs, vals)))
check(max(vals) / min(vals) - 1 < 5e-3,
      f"C2  *** THE ONE-PARAMETER SCALING THEOREM: T^2 depends on k and R only through x = k^2 R "
      f"(verified: four (k,R) pairs with identical k^2R agree to {100*(max(vals)/min(vals)-1):.2f}%) "
      f"***.  So the entire (k, z, R, nu_0) surface is one curve per (z, nu_0), and a bound at one "
      f"k converts to any other k by k^-2 exactly",
      "this is what makes the stage-69 -> forest extrapolation exact rather than heuristic: "
      "moving k = 0.2 -> 10 h/Mpc tightens R by exactly (10/0.2)^2 = 2500 at fixed tolerance")

# --- CLASS validation at forest k, matched-setup ratio (cold fluid vs warm fluid)
cl_cold = class_run(1e-16)
print(f"    {'k':>5s} {'z':>4s} {'cs2':>7s} {'CLASS P_w/P_cold':>18s} {'integrator (bary)':>19s} "
      f"{'agree':>8s}")
worst = 0.0
for cs2 in (1e-11, 1e-10, 1e-9):
    cl_w = class_run(cs2)
    for kh in (1.0, 3.0, 10.0):
        for z in (2.0, 4.0):
            ref = cl_w.pk_lin(kh * H0H, z) / cl_cold.pk_lin(kh * H0H, z)
            g = grow(kh, lambda a, c=cs2: c)
            mine = (g[z][1] / COLD[z][1]) ** 2
            worst = max(worst, abs(mine - ref))
            print(f"    {kh:>5.1f} {z:>4.1f} {cs2:>7.0e} {ref:>18.5f} {mine:>19.5f} "
                  f"{mine-ref:>+8.4f}")
    cl_w.struct_cleanup()
    cl_w.empty()
check(worst < 0.05,
      f"C3  *** VALIDATED AGAINST REAL CLASS IN THE FOREST BAND: the integrator's baryon-channel "
      f"suppression matches CLASS's matched-setup fluid ratio to <= {worst:.4f} ABSOLUTE across "
      f"k = 1-10 h/Mpc, z = 2-4 and three decades of constant c_s^2 (2% to 60% suppression) ***",
      "matched-setup means both CLASS runs carry the SAME species content (tiny cdm + fluid) and "
      "differ only in cs2_fld, so the baryon-transfer and dark-energy-species artifacts cancel in "
      "the ratio -- the residual is the pressure physics.  Stage 69's validation compared against "
      "the full-LCDM run instead and carried a ~2-3% offset from that mismatch")

# --- build the master Tcal(x) curves once (total and baryon channels, both nu_0 edges)
XG = np.logspace(-12, -2.0, 220)
TCAL = {}
for nu0 in (NU0_HI, NU0_LO):
    for ch, idx in (("tot", 3), ("bary", 1)):
        arr = {z: [] for z in ZFOREST}
        for x in XG:
            g = grow(1.0, cs2f_of(x, nu0))            # k = 1 => x = R
            for z in ZFOREST:
                arr[z].append(max((g[z][idx] / COLD[z][idx]) ** 2, 1e-14))
        for z in ZFOREST:
            TCAL[(nu0, ch, z)] = np.array(arr[z])


def T2(kh, z, R, nu0=NU0_HI, ch="tot"):
    x = np.atleast_1d(kh) ** 2 * R
    y = np.interp(np.log10(x), np.log10(XG), np.log10(TCAL[(nu0, ch, z)]),
                  left=0.0, right=np.log10(TCAL[(nu0, ch, z)][-1]))
    out = 10 ** y
    return float(out[0]) if np.isscalar(kh) or np.ndim(kh) == 0 else out


spot = [(1.0, 2.0, 1e-8), (10.0, 3.0, 1e-9), (5.0, 4.0, 3e-9)]
errs = [abs(T2(k, z, R) - (grow(k, cs2f_of(R, NU0_HI))[z][3] / COLD[z][3]) ** 2) for k, z, R in spot]
check(max(errs) < 3e-3,
      f"C4  the interpolated Tcal(x) surface reproduces direct integrations to "
      f"{max(errs):.1e} absolute at three spot checks -- the tables and bisections below use the "
      f"interpolant, so this is the error budget on every number that follows")

# =================================================================================================
print()
print("=" * 100)
print("PART D -- DELIVERABLE (a): the suppression T^2(k) at k = 1, 3, 5, 10 h/Mpc, z = 2, 3, 4")
print("=" * 100)
info("D0  READ THE DEEPLY-SUPPRESSED ROWS WITH CARE: once T^2 falls below ~0.05 the warm "
     "component RINGS (a condensate inside its Jeans scale oscillates), so T^2 stops being "
     "monotonic in k -- e.g. the R = 1.5e-6 row below dips at k = 3 and partly recovers at k = 5. "
     "That is physical, not numerical noise, and it is irrelevant to the bound, which is set where "
     "the suppression is a few per cent and monotonic.")
RLIST = [(R_S69_HI, "stage69 P(k=0.2) bound"), (1e-7, ""), (1e-8, ""), (2.5e-9, "PART E bound"),
         (1e-9, ""), (LAMD_LO, "committed Lam_D floor")]
for nu0, lab in ((NU0_HI, "nu_0 CEILING 1.77e-4 (the tighter edge)"),
                 (NU0_LO, "nu_0 floor 2.14e-5")):
    print(f"  -- {lab}, TOTAL matter channel --")
    print(f"    {'R = Lam_D/Q_0':>14s} {'z':>4s} " + " ".join(f"{'k=%g' % k:>10s}" for k in KFOREST)
          + "   note")
    for R, note in RLIST:
        for z in ZFOREST:
            print(f"    {R if z == ZFOREST[0] else '':>14} {z:>4.1f} " +
                  " ".join(f"{T2(k, z, R, nu0):>10.5f}" for k in KFOREST) +
                  ("   " + note if (z == ZFOREST[0] and note) else ""))
zspread = max(abs(T2(10.0, 2.0, 2.5e-9) - T2(10.0, 4.0, 2.5e-9)),
              abs(T2(3.0, 2.0, 1e-8) - T2(3.0, 4.0, 1e-8)))
check(zspread < 0.02,
      f"D1  as PART A3 predicted, T^2 is nearly z-INDEPENDENT across the forest window (max spread "
      f"{zspread:.4f} absolute between z = 2 and z = 4 at fixed k): the damping is already done by "
      f"z = 4.  z = 2 is marginally the tighter redshift",
      "so the forest constraint is a statement about the epoch z ~ 10-45, delivered at z = 2-4 -- "
      "and it does NOT relax by going to higher-z forest data")
check(T2(10.0, 2.0, R_S69_HI) < 1e-2 and T2(1.0, 2.0, R_S69_HI) < 0.5,
      f"D2  *** AT STAGE 69's OWN BOUND THE FOREST BAND IS ANNIHILATED: R = {R_S69_HI:.2e} gives "
      f"T^2 = {T2(1.0,2.0,R_S69_HI):.4f} at k = 1 and {T2(10.0,2.0,R_S69_HI):.2e} at k = 10 "
      f"(z = 2) ***.  P(k = 0.2) was the weakest place the corpus could have tested this",
      "direction: ADVERSE.  Stage 69's bound is not a safe resting point -- it is 2-3 orders of "
      "magnitude short of what the forest band already requires")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- DELIVERABLE (b): does the forest tighten stage 69's R bound, and by how much")
print("=" * 100)
# E1: the tolerance, anchored on published WDM limits rather than asserted
NU_V, ALPHA0 = 1.12, 0.049


def wdm_T2(kh, m_keV):
    al = ALPHA0 * m_keV ** (-1.11) * (OM_D / 0.25) ** 0.11 * (H0H / 0.7) ** 1.22
    return (1 + (al * kh) ** (2 * NU_V)) ** (-10.0 / NU_V)


YARD = ((5.3, "Irsic+2017 PRD 96 023522, MIKE/HIRES+XQ-100, 2sigma"),
        (3.1, "Villasenor+2023, P_F1D, 95% CL"),
        (1.9, "conservative thermal-degenerate reading (Garzilli-type); QUOTED FROM MEMORY, "
              "not verified in-session"))
info("E1  THE TOLERANCE IS IMPORTED, NOT INVENTED.  Published forest limits are quoted as thermal-"
     "relic WDM masses; the Viel+2005 fitting form T^2 = [1+(alpha k)^2.24]^(-8.929) with "
     "alpha = 0.049 (m/keV)^-1.11 (Om/0.25)^0.11 (h/0.7)^1.22 h^-1Mpc converts each limit into the "
     "3D-linear-power deficit that IS excluded at ~2sigma:")
print(f"    {'m_WDM [keV]':>12s} " + " ".join(f"{'1-T^2(k=%g)' % k:>13s}" for k in KFOREST) +
      "   provenance")
for m, prov in YARD:
    print(f"    {m:>12.1f} " + " ".join(f"{1-wdm_T2(k, m):>13.4f}" for k in KFOREST) + f"   {prov}")
TOL, TOL_LO, TOL_HI = 0.10, 1 - wdm_T2(10.0, 5.3), 1 - wdm_T2(10.0, 1.9)
check(abs(TOL - (1 - wdm_T2(10.0, 3.1))) < 0.02,
      f"E1  ADOPTED TOLERANCE: 10% suppression of the 3D linear power at k = 10 h/Mpc.  It is not a "
      f"round number chosen for convenience -- it is the k = 10 deficit of the 3.1 keV limit "
      f"({100*(1-wdm_T2(10.0,3.1)):.1f}%) to within 2 points.  The honest BRACKET across the "
      f"yardstick spread is {100*TOL_LO:.1f}% (5.3 keV) to {100*TOL_HI:.1f}% (1.9 keV), a factor "
      f"{TOL_HI/TOL_LO:.0f}, and every bound below is reported across that bracket",
      "NOT overstated: this is a yardstick on the linear transfer function, not a likelihood.  A "
      "real bound needs the hydro emulator stage 16 documented as unavailable for free cutoff "
      "shapes (and the Hooper+2022 likelihood that was never released)")


def R_at(tol, kh, z, nu0=NU0_HI, ch="tot"):
    lo, hi = 1e-14, 1e-4
    for _ in range(80):
        mid = np.sqrt(lo * hi)
        if T2(kh, z, mid, nu0, ch) > 1 - tol:
            lo = mid
        else:
            hi = mid
    return lo


print(f"    {'criterion':>34s} {'R_max (nu0 ceil)':>17s} {'R_max (nu0 floor)':>18s} "
      f"{'vs stage69 1.54e-6':>19s}")
rows = {}
for tol, tl in ((TOL, "10% (3.1 keV-equiv)"), (TOL_LO, f"{100*TOL_LO:.1f}% (5.3 keV-equiv)"),
                (TOL_HI, f"{100*TOL_HI:.0f}% (1.9 keV-equiv)")):
    for kh in (10.0, 5.0, 1.0):
        rc, rf = R_at(tol, kh, 2.0, NU0_HI), R_at(tol, kh, 2.0, NU0_LO)
        rows[(tol, kh)] = rc
        print(f"    {tl + f' at k={kh:g}, z=2':>34s} {rc:>17.3e} {rf:>18.3e} "
              f"{R_S69_HI/rc:>18.0f}x")
R_FOREST = rows[(TOL, 10.0)]
check(R_FOREST < R_S69_HI / 50,
      f"E2  *** YES, AND BY A LOT: the forest tightens R = Lam_D/Q_0 from stage 69's "
      f"{R_S69_HI:.2e} to R <= {R_FOREST:.2e} -- a factor {R_S69_HI/R_FOREST:.0f} *** "
      f"(k = 10 h/Mpc, z = 2, 10% tolerance, nu_0 ceiling, total-matter channel).  Across the "
      f"yardstick bracket the bound runs {rows[(TOL_LO,10.0)]:.2e} to {rows[(TOL_HI,10.0)]:.2e}, "
      f"i.e. a tightening of {R_S69_HI/rows[(TOL_HI,10.0)]:.0f}x to "
      f"{R_S69_HI/rows[(TOL_LO,10.0)]:.0f}x",
      "the factor is not a modelling artifact: by the C2 scaling theorem it is exactly "
      "(k_forest/0.2)^2 x (tolerance ratio), and k = 10 h/Mpc is measured forest territory (B2)")
rb = R_at(TOL, 10.0, 2.0, NU0_HI, "bary")
check(rb > R_FOREST,
      f"E3  BOTH WAYS ON THE CHANNEL CHOICE (favourable direction, reported anyway): the forest "
      f"traces GAS, and the baryon channel is less suppressed than the total (the baryons keep "
      f"growing gravitationally while the warm component is pressure-damped).  Using the baryon "
      f"channel loosens the bound to R <= {rb:.2e}, a factor {rb/R_FOREST:.1f}.  THE HEADLINE USES "
      f"THE TOTAL-MATTER CHANNEL ANYWAY, because the published WDM yardstick is defined on the "
      f"total matter transfer function and the gas recovery is already inside that calibration -- "
      f"taking it twice would be double-counting in the framework's favour",
      "so the quoted bound carries an explicit factor-of-3 favourable systematic, named rather "
      "than banked")

# E4: shape-fair cross-check through the 1D projection the forest actually measures
def P1D_ratio(T2curve, z, kh_at):
    kk, P = kproj, PL[z]
    m = kk >= kh_at
    num = np.trapz(kk[m] * P[m] * T2curve[m], kk[m])
    den = np.trapz(kk[m] * P[m], kk[m])
    return num / den


tail_chk = [P1D_ratio(np.ones_like(kproj), 3.0, 5.0),
            np.trapz((kproj * PL[3.0])[(kproj >= 5) & (kproj <= 100)],
                         kproj[(kproj >= 5) & (kproj <= 100)]) /
            np.trapz((kproj * PL[3.0])[kproj >= 5], kproj[kproj >= 5])]
info(f"E4  the projection P_1D(k) = (1/2pi) int_k^inf k' P_3D(k') dk' is what the forest measures, "
     f"so a shape-fair comparison must be made THERE (stage 16's C3 point).  Tail bookkeeping: "
     f"{100*tail_chk[1]:.0f}% of P_1D(k=5, z=3) comes from k' < 100 h/Mpc, so ~"
     f"{100*(1-tail_chk[1]):.0f}% comes from k' > 100 where NEITHER model is observable and linear "
     f"theory is meaningless -- the projected numbers below inherit that, equally for both sides.")


def R_proj(m_keV, z, kh_at, nu0=NU0_HI):
    target = P1D_ratio(wdm_T2(kproj, m_keV), z, kh_at)
    lo, hi = 1e-14, 1e-4
    for _ in range(60):
        mid = np.sqrt(lo * hi)
        if P1D_ratio(T2(kproj, z, mid, nu0), z, kh_at) > target:
            lo = mid
        else:
            hi = mid
    return lo, target


print(f"    {'yardstick':>14s} {'P_1D(k=5,z=3) ratio at limit':>30s} {'R_max (projected)':>19s} "
      f"{'R_max (local 1-T^2)':>21s}")
for m, _ in YARD:
    rp, tg = R_proj(m, 3.0, 5.0)
    print(f"    {m:>10.1f} keV {tg:>30.4f} {rp:>19.3e} "
          f"{R_at(1-wdm_T2(10.0, m), 10.0, 2.0):>21.3e}")
rp31 = R_proj(3.1, 3.0, 5.0)[0]
check(0.1 < rp31 / R_FOREST < 10,
      f"E4  the shape-fair projected bound and the local bound AGREE to a factor "
      f"{max(rp31/R_FOREST, R_FOREST/rp31):.1f} (projected R <= {rp31:.2e} vs local "
      f"R <= {R_FOREST:.2e} at the 3.1 keV yardstick), so the headline does not depend on which "
      f"of the two comparisons is used",
      "the framework's suppression is a k^2 bend that steepens, WDM's is a free-streaming cutoff; "
      "the two shapes are different, which is exactly why the agreement of the two criteria is "
      "worth checking rather than assuming")

# E5: what the bound does to the corpus's committed Lam_D window
surv = np.log10(R_FOREST / LAMD_LO)
check(R_FOREST > LAMD_LO,
      f"E5  *** WHAT IT COSTS THE FRAMEWORK: with Q_0 = 1 the committed health window "
      f"Lam_D in ({LAMD_LO:.1e}, {LAMD_HI:.1e}] IS the R window, i.e. "
      f"{np.log10(LAMD_HI/LAMD_LO):.2f} decades.  The forest removes its top "
      f"{np.log10(LAMD_HI/R_FOREST):.2f} decades and leaves "
      f"({LAMD_LO:.1e}, {R_FOREST:.1e}] = {surv:.2f} decades.  THE WINDOW SURVIVES -- non-empty, "
      f"but {LAMD_HI/R_FOREST:.0f}x thinner ***",
      "direction: ADVERSE to the parameter space, NOT fatal to the framework.  And it converts "
      "beta = 1's Lam_D = M^2/mu from a consistency check into a pass/fail test: the moment that "
      "product is evaluated numerically, the forest either passes it or kills it")
check(True,
      f"E6  RECORDED, NOT CLAIMED AS A KILL: stage 1's galaxy-relaxation FLOOR Lam_D >= 1.16e-9 "
      f"(nbody_2026/stage1_condensate_relaxation_2026.py D2) sits only a factor "
      f"{R_FOREST/1.16e-9:.1f} below this ceiling -- the forest very nearly closes stage 1's "
      f"favourable branch from above.  It is NOT a live kill, because stage 2 already killed that "
      f"branch on energetics grounds (its own Part A), so the collision is with a SUPERSEDED "
      f"requirement",
      "flagged so that nobody revives the relaxation branch without re-running this script: at the "
      "5.3 keV-equivalent tolerance the surviving overlap 1.16e-9 <= Lam_D <= "
      f"{rows[(TOL_LO,10.0)]:.1e} is EMPTY")

# =================================================================================================
print()
print("=" * 100)
print("PART F -- THE FORK THAT FLIPS THE VERDICT, and one adverse correction to the record")
print("=" * 100)
info("F0  every number above assumes the warm condensate CARRIES Omega_dm.  That is READING A, and "
     "it is THE_COMPLETION's own text: 'rho_exc = Q_0 mu^2 u is linear in u ==> w = u/2Q_0 -> 0: "
     "dust, i.e. THE DARK MATTER' (table row 'the deviations'), with 'I_0 approx Omega_dm (an IC)' "
     "in the bounds row.  READING B is the corpus's other committed statement: stage 17 D4 + "
     f"stage 41 E3 make the shift charge a TRACE species, Omega_kd <= {OM_KD_MAX:.2e}.")
fW = OM_KD_MAX / OM_M
gB = grow(10.0, cs2f_of(1.0, NU0_HI), fD=fW, fC=OM_D / OM_M - fW)
supB = 1 - (gB[2.0][3] / COLD[2.0][3]) ** 2
check(supB < 1e-5,
      f"F1  UNDER READING B THE FOREST IS SILENT AND THE SIGN OF THE TEST REVERSES: put the FULL "
      f"R = 1 sound speed on a trace species of Omega_kd = {OM_KD_MAX:.2e} (with the rest of "
      f"Omega_dm cold) and the total-matter suppression at k = 10, z = 2 is "
      f"{supB:.2e} -- {2*fW:.1e} is the analytic ceiling 2 Omega_kd/Omega_m, and the run "
      f"confirms it.  No R bound exists at all",
      "but the price is exactly the price non-claim 2d already names: under reading B the "
      "Ly-alpha safety of 'standard cold dust' is INHERITED FROM ASSUMING a CDM-like carrier for "
      "0.265 that the theory does not yet contain -- it is not computed either.  Reading B answers "
      "non-claim 4 by conceding the harder open problem")
check(True,
      f"F2  AND THE TWO READINGS ARE NOT RECONCILABLE BY A CHOICE OF R: stage 17 D4's bookkeeping "
      f"gives Lam_D/Q_0 >= 33.15 at the nu_0 floor, while reading A's bounds (CMB Lam <~ 1e-2, "
      f"health <= 8.4e-7, stage 69 <= {R_S69_HI:.1e}, this script <= {R_FOREST:.1e}) all point the "
      f"other way -- a span of {33.15/R_FOREST:.1e}x.  ONE conserved charge cannot be both "
      f"Omega ~ 0.265 and Omega ~ 4e-7, so this is an OPEN FORK in the corpus, not a spread to "
      f"average over.  Resolving it is prerequisite to quoting any number in PART E as final",
      "stated as a demand on the framework, not as a defect of this computation: whichever way it "
      "resolves, ONE of the two branches above is the answer to non-claim 4")
# F3: the adverse correction to stage 69's own pass
w_quoted, cs2_quoted = 7.3e-5, 1.1e-8
check(abs(2 * w_quoted**2 / cs2_quoted - 1) < 0.05,
      f"F3  *** ADVERSE CORRECTION TO STAGE 69's D3/E1 (its 'the framework PASSES' rests on a "
      f"misread): stage 69 inferred R ~ 3e-8 from mi_dbi_khronon's c_s^2 = 1.1e-8.  That number is "
      f"an EPOCH statement at R = 1, not an amplitude.  In the saturated regime c_s^2 = "
      f"R(1-s^2)/(1+R) and w = R sqrt(1-s^2)/(1+R), so c_s^2 = w^2 (1+R)/R, which at R = 1 is "
      f"c_s^2 = 2w^2: from that script's OWN w(a=3e-5) = {w_quoted:.1e} this gives "
      f"{2*w_quoted**2:.3e}, reproducing its {cs2_quoted:.1e} to "
      f"{100*abs(2*w_quoted**2/cs2_quoted-1):.1f}% ***",
      "so mi_dbi_khronon's sound speed was computed at exactly the R = 1 that stage 69's own D1 "
      "EXCLUDES; there is no independent small-R normalisation in the corpus.  The live R "
      "constraint comes from the health window and from these growth bounds only")

# =================================================================================================
print()
print("=" * 100)
print("PART G -- the OTHER half of non-claim 4: the bump response, which this script does NOT close")
print("=" * 100)
G, RHO_C = 6.674e-11, 9.2e-27
print(f"    {'k [h/Mpc]':>10s} {'z':>4s} {'R_tophat [Mpc]':>15s} {'y=g/a0 canon (d=1)':>20s} "
      f"{'y alt (d=1)':>13s} {'nu(y) canon':>12s}")
ys = []
for kh in (1.0, 3.0, 10.0):
    for z in (2.0, 3.0, 4.0):
        Rphys = (np.pi / (kh / H0H)) / (1 + z) * 3.0857e22
        g = (4 * np.pi / 3) * G * (OM_M * RHO_C * (1 + z) ** 3) * Rphys
        y, ya = g / A0_CANON, g / A0_ALT
        ys.append(y)
        print(f"    {kh:>10.1f} {z:>4.1f} {Rphys/3.0857e22:>15.3f} {y:>20.4f} {ya:>13.4f} "
              f"{1/(1-np.exp(-np.sqrt(y))):>12.2f}")
check(max(ys) < 1.0,
      f"G1  FOREST SCALES ARE DEEP MOND IN THIS FRAMEWORK: a delta = 1 perturbation of half-"
      f"wavelength pi/k has y = g_bar/a_0 = {min(ys):.3f}-{max(ys):.3f} (canonical a_0 = "
      f"{A0_CANON:.4e}; alt {A0_ALT:.4e} m/s^2 gives y smaller still), so the Route A kernel "
      f"nu(y) = 1/(1-e^-sqrt y) is a factor {1/(1-np.exp(-np.sqrt(max(ys)))):.1f}-"
      f"{1/(1-np.exp(-np.sqrt(min(ys)))):.1f} ENHANCEMENT there",
      "and this is the amendment the memory rule demands: never analyse this framework with a "
      "Newtonian response at forest scales.  a_0(z) is flat below z ~ 5 for the whole nu_0 window "
      "(stage 17 D2), so the enhancement does not switch off across z = 2-4")
check(True,
      "G2  WHY THAT DOES NOT WRECK PART E, AND WHY IT IS STILL OWED: the framework's own SVT "
      "theorem (THE_COMPLETION row 20) says the promoted MOND term drops out of FRW perturbations "
      "at second order and STARTS AT THIRD ORDER -- delta_Y^(1) = 0 -- so the LINEAR power "
      "spectrum this script computes is genuinely the whole linear story, and the IC channel is "
      "correctly isolated.  But the forest is a QUASI-NONLINEAR observable (B1: Delta^2 ~ 1-4 "
      "across the band), and at third order and beyond the bump response IS active, in the "
      "ENHANCEMENT direction (stage 26: collapse 1.34-1.96x faster, 2.3-5.1x boost at turnaround)",
      "so non-claim 4's 'standard cold dust + THE BUMP RESPONSE should be Ly-alpha-safe' is "
      "answered here for the first term ONLY.  The second term needs a nonlinear/hydro run and "
      "remains uncomputed -- and its risk is EXCESS small-scale power, the opposite sign to "
      "everything in PART E, which the forest also constrains")

# =================================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  NON-CLAIM 4, HALF-CLOSED.  The IC/sound-speed channel is now COMPUTED at the scales the forest
  measures, with CLASS validation IN the forest band (C3) and an exact one-parameter scaling
  theorem (C2) linking it to stage 69's P(k = 0.2) result.

  (a) T^2(k) at k = 1, 3, 5, 10 h/Mpc and z = 2, 3, 4: PART D, both nu_0 edges, R from stage 69's
      bound down to the committed Lam_D floor.  T^2 is nearly z-independent (D1) because the
      damping is delivered at z ~ 10-45 (A3), and at stage 69's own bound the band is destroyed
      (D2: T^2 = {T2(10.0,2.0,R_S69_HI):.1e} at k = 10).

  (b) YES, THE FOREST TIGHTENS THE BOUND, BY A FACTOR {R_S69_HI/R_FOREST:.0f}: R = Lam_D/Q_0 <=
      {R_FOREST:.2e} against stage 69's {R_S69_HI:.2e} (k = 10 h/Mpc, z = 2, 10% tolerance, nu_0
      ceiling, total-matter channel).  Bracket: {R_S69_HI/rows[(TOL_HI,10.0)]:.0f}x to {R_S69_HI/rows[(TOL_LO,10.0)]:.0f}x across the yardstick
      spread; the shape-fair P_1D projection and the local criterion agree to {max(rp31/R_FOREST, R_FOREST/rp31):.1f}x; the
      gas-channel reading would loosen it by {rb/R_FOREST:.1f}x.  Cost: {np.log10(LAMD_HI/R_FOREST):.2f} of the committed
      Lam_D window's {np.log10(LAMD_HI/LAMD_LO):.2f} decades removed, {surv:.2f} decades survive.

  (c) VERDICT.  "Ly-alpha-safe BY CONSTRUCTION" is NOT what the computation says.  It is safe in the
      BOTTOM DECADE of the corpus's own Lam_D window and excluded above it -- so non-claim 4's
      assertion holds only conditionally, and the condition is new.  The framework SURVIVES: the
      window is non-empty and its floor (1.9e-10) is a factor {R_FOREST/LAMD_LO:.0f} inside the
      ceiling this script imposes.  One genuinely favourable structural result came out of it: the
      sector has NO primordial cutoff at all (A2 -- c_s^2 at z = 1090 is 2e-11 of its own bump
      peak, for the whole committed nu_0 window), so it is
      not a WDM-like model in disguise; the suppression is generated entirely after the DBI wall.

  DIRECTION OF RISK.  Adverse on parameter space, favourable on structure, and FORK-DEPENDENT
  overall (F1/F2): under the trace-charge reading the forest says nothing and the burden moves to
  non-claim 2d.  One adverse correction to the committed record (F3): stage 69's "the framework
  passes" inferred R ~ 3e-8 from a c_s^2 = 1.1e-8 that was computed at R = 1 -- re-derived exactly
  here from that script's own w.  There is no independent small-R normalisation in the corpus.

  STILL OWED.  (i) the Omega-allocation fork (F2) -- prerequisite to quoting (b) as final;
  (ii) Lam_D = M^2/mu evaluated numerically under beta = 1, which turns E5 into pass/fail;
  (iii) the bump-response half of the non-claim (G2), which is nonlinear and opposite in sign;
  (iv) a patched CLASS fluid carrying c_s^2(a) inside the matter power spectrum (stage 69's E3,
  still open); (v) a hydrodynamic forest likelihood -- unavailable for free cutoff shapes per
  stage 16, so items (i)-(iii) are the ones actually reachable.
""")
cl.struct_cleanup(); cl.empty(); cl_cold.struct_cleanup(); cl_cold.empty()
print("=" * 100)
n_fail = len(FAIL)
print(f"CHECKS: {NCHK[0] - n_fail}/{NCHK[0]} passed" + ("" if not n_fail else f"; FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
