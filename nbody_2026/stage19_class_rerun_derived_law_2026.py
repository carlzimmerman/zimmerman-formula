#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage19_class_rerun_derived_law_2026.py
=======================================
THE CLASS RE-RUN WITH THE DERIVED a_0(z) LAW -- non-claim 2e's owed item (i), executed.

Stage 18 proved the perturbation EQUATIONS are identical (every promotion entry vanishes on FRW,
exactly).  So what a CMB re-run can actually test is the BACKGROUND -- and at beta = 1 the background
is exact and closed-form.  From the committed thermodynamics rho = (Q_0+u)K' - K, p = K with the pure
DBI K = -M^4 sqrt(1 - mu^2 u^2/M^4):

    *** rho_nd(nu) = M^4 sqrt(1 + nu^2) ,   p_nd(nu) = -M^4/sqrt(1 + nu^2) ,  nu = nu_0 (1+z)^3 ***

(nd = the non-dust piece; the Q_0 n dust share, Omega_kd <= 4.4e-7, rides along and is 280x smaller
than everything below.)  So versus LambdaCDM the derived-law universe differs by ONE thing: the
DE-like component interpolates from rho_Lambda today to a COLD a^-3 trace of today-equivalent density
rho_Lambda nu_0 at high z, with an a^-6 transient bounded by nu_0^2 <= 3.2e-8.  Its equation of state
is w_nd(z) = -1/(1+nu^2): the pressure dies exactly where the CMB needs the sector pressureless, and
|1+w| <= 2.4e-5 at every redshift SN/BAO surveys reach (z <= 2, window ceiling).

The re-run therefore has three rigorous parts:
  B  EXACT background integrals both window ends vs LambdaCDM: max |dH/H|, the comoving distance to
     last scattering, the sound horizon, and theta_* -- against Planck's 2.9e-4 fractional precision.
  C  REAL CLASS RUNS: baseline (the committed run's Planck parameters) vs the derived-law bracket
     (the exact a^-3 trace added as cold matter, budget closed at z = 0), compared per-multipole
     against COSMIC VARIANCE -- the harshest possible yardstick, stricter than Planck noise.
  D  the MOND-off input the committed run assumed, now delivered BY the law: a_0(z_*) in
     [0.0021, 0.0060] x a_0(0) across the window (the old CPL dressing gave 0.0060 -- equalled at
     the floor, beaten 3x at the ceiling).

WHAT THIS IS NOT (Part E): a full Einstein-Boltzmann implementation of AeST + promotion -- the same
limitation the committed CMB run stated for itself (CLASS's stock fluid takes constant c_s^2).  The
bracket treats the trace as extra cold matter, which is EXACT at high z (it is cold and a^-3 there --
that is stage 9's theorem applied to the wall-climbing excitation) and conservative at low z (where
its |1+w| <= 2.4e-5 makes it MORE Lambda-like than the bracket assumes, i.e. closer to LambdaCDM
than what is tested here).
"""

import sys
import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
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
    return True


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# committed CLASS-run parameters (mi_dbi_cmb_class_run_2026.py) -- reused verbatim
OMB, OMC, H0, NS, AS, TAU = 0.02237, 0.1200, 67.36, 0.9649, 2.1e-9, 0.0544
h = H0 / 100.0
OM_G = 2.4729e-5 / h ** 2                     # photons, T = 2.7255 K
OM_R = OM_G * (1.0 + 0.2271 * 3.046)          # + massless neutrinos (bracket level)
OM_M = (OMB + OMC) / h ** 2
OM_L = 1.0 - OM_M - OM_R
Z_STAR = mp.mpf("1089.9")

NU0_FLOOR = mp.mpf("2.14e-5")                 # stage 17's window
NU0_CEIL = mp.mpf("1.77e-4")

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the exact background, from the committed thermodynamics")
print("=" * 100)

u_s, Q0_s, mu_s, M4_s, nu_s = sp.symbols("u Q_0 mu M4 nu", positive=True)
K_pure = -M4_s * sp.sqrt(1 - mu_s ** 2 * u_s ** 2 / M4_s)          # beta = 1: the pure DBI
n_s = sp.diff(K_pure, u_s)
rho_nd = sp.simplify(u_s * n_s - K_pure)                            # non-dust piece (Q_0 n rides apart)
# invert the charge: nu = n/(mu^2 Lambda_D) with Lambda_D = M^2/mu  =>  u = (M^2/mu) nu/sqrt(1+nu^2)
u_of_nu = (sp.sqrt(M4_s) / mu_s) * nu_s / sp.sqrt(1 + nu_s ** 2)
rho_check = sp.simplify(rho_nd.subs(u_s, u_of_nu) - M4_s * sp.sqrt(1 + nu_s ** 2))
p_check = sp.simplify(K_pure.subs(u_s, u_of_nu) + M4_s / sp.sqrt(1 + nu_s ** 2))
check(rho_check == 0 and p_check == 0,
      "A1  *** EXACT: rho_nd = M^4 sqrt(1+nu^2), p_nd = -M^4/sqrt(1+nu^2) *** -- DE today, cold "
      "a^-3 at high z, w_nd = -1/(1+nu^2), all from the pure DBI with no approximation",
      "sympy, from the committed thermodynamics; rho_nd p_nd = -M^8 is an exact invariant of the law")

w_z2_ceil = -1 / (1 + (NU0_CEIL * 27) ** 2)
check(abs(1 + w_z2_ceil) < mp.mpf("3e-5"),
      f"A2  the DE-like piece is indistinguishable from Lambda where DE is measured: |1+w| = "
      f"{sig(abs(1 + w_z2_ceil), 2)} at z = 2 (window ceiling) against survey precision ~0.03",
      "a thousand times below current constraints; the deviation lives only above z_t ~ 17-35")


def dH2_frac(z, nu0):
    """(H_derived^2 - H_LCDM^2)/H_LCDM^2 at redshift z."""
    z = mp.mpf(z)
    nu = nu0 * (1 + z) ** 3
    extra = OM_L * (mp.sqrt(1 + nu ** 2) / mp.sqrt(1 + nu0 ** 2) - 1)
    lcdm = OM_R * (1 + z) ** 4 + OM_M * (1 + z) ** 3 + OM_L
    return extra / lcdm


# =================================================================================================
print()
print("=" * 100)
print("PART B -- exact background integrals: H(z), distances, theta_*")
print("=" * 100)

zs_scan = [0.5, 2, 10, 30, 100, 500, 1090, 3000]
print("\n     z     dH^2/H^2 (floor)    dH^2/H^2 (ceiling)")
for z in zs_scan:
    print(f"  {z:>6}      {sig(dH2_frac(z, NU0_FLOOR), 3):>10s}          "
          f"{sig(dH2_frac(z, NU0_CEIL), 3):>10s}")

max_dH = max(dH2_frac(z, NU0_CEIL) / 2 for z in range(1, 3500, 7))
check(max_dH < mp.mpf("2.5e-4"),
      f"B1  max |dH/H| over the whole expansion history = {sig(max_dH, 3)} at the window CEILING "
      f"(it asymptotes to Omega_L nu_0/(2 Omega_m) = "
      f"{sig(OM_L * NU0_CEIL / (2 * OM_M), 3)} in the matter era -- a constant a^-3 offset, which is "
      f"exactly why it is degenerate with omega_cdm)",
      "at the floor it is 8.3x smaller still")


def Hfrac(z, nu0=None):
    """H(z)/H0; nu0 = None -> LambdaCDM."""
    z = mp.mpf(z)
    de = OM_L if nu0 is None else OM_L * mp.sqrt(1 + (nu0 * (1 + z) ** 3) ** 2) / mp.sqrt(1 + nu0 ** 2)
    return mp.sqrt(OM_R * (1 + z) ** 4 + OM_M * (1 + z) ** 3 + de)


def comoving_to_star(nu0=None):
    return mp.quad(lambda z: 1 / Hfrac(z, nu0), [0, 10, 100, Z_STAR])


def sound_horizon(nu0=None):
    Rb = lambda z: 0.75 * (OMB / h ** 2) / OM_G / (1 + z)
    integ = lambda z: 1 / (Hfrac(z, nu0) * mp.sqrt(3 * (1 + Rb(z))))
    return mp.quad(integ, [Z_STAR, 5000, 5e4, 5e6])


DC_l, DC_d = comoving_to_star(), comoving_to_star(NU0_CEIL)
RS_l, RS_d = sound_horizon(), sound_horizon(NU0_CEIL)
th_l, th_d = RS_l / DC_l, RS_d / DC_d
dtheta = abs(th_d / th_l - 1)
check(dtheta < mp.mpf("2.9e-4"),
      f"B2  *** theta_* moves by {sig(dtheta, 3)} (fractional) at the window CEILING -- "
      f"{sig(dtheta / mp.mpf('2.9e-4'), 3)}x Planck's full 100 theta_* precision (2.9e-4). "
      f"The acoustic geometry is untouched ***",
      f"D_C shift {sig(abs(DC_d / DC_l - 1), 3)}, r_s shift {sig(abs(RS_d / RS_l - 1), 3)} -- both "
      "shrink the same way, which is why the ANGLE barely moves")

dth_floor = abs(sound_horizon(NU0_FLOOR) / comoving_to_star(NU0_FLOOR) / th_l - 1)
info(f"B3  at the window floor the same shift is {sig(dth_floor, 3)} -- "
     f"{sig(dth_floor / mp.mpf('2.9e-4'), 3)}x Planck precision.  The whole window passes the "
     "geometric test with two orders of margin.")


# =================================================================================================
print()
print("=" * 100)
print("PART C -- the REAL CLASS runs: derived-law bracket vs the committed baseline")
print("=" * 100)

from classy import Class

BASE = {
    "output": "tCl,pCl,lCl", "lensing": "yes", "l_max_scalars": 2500,
    "h": h, "omega_b": OMB, "n_s": NS, "A_s": AS, "tau_reio": TAU,
    "N_ur": 3.046,
}


def run_class(omega_cdm):
    c = Class()
    c.set(dict(BASE, omega_cdm=omega_cdm))
    c.compute()
    cl = c.lensed_cl(2500)
    th = c.theta_s_100()
    c.struct_cleanup()
    c.empty()
    return cl, th


# the exact trace, expressed as extra cold matter with the budget closed at z = 0 by CLASS itself
d_omega = float(OM_L * NU0_CEIL * h ** 2)
cl_b, th_b = run_class(OMC)
cl_d, th_d100 = run_class(OMC + d_omega)

ell = cl_b["ell"][2:]
fr_tt = np.abs(cl_d["tt"][2:] / cl_b["tt"][2:] - 1.0)
fr_ee = np.abs(cl_d["ee"][2:] / cl_b["ee"][2:] - 1.0)
chi2_cv = float(np.sum((2 * ell + 1) / 2.0 * (cl_d["tt"][2:] / cl_b["tt"][2:] - 1.0) ** 2)
                + np.sum((2 * ell + 1) / 2.0 * (cl_d["ee"][2:] / cl_b["ee"][2:] - 1.0) ** 2))
n_modes = 2 * len(ell)

info(f"C1  CLASS runs done: baseline omega_cdm = {OMC}, derived-law bracket omega_cdm = "
     f"{OMC + d_omega:.6f} (the exact a^-3 trace {d_omega:.2e} = {d_omega / OMC * 100:.3f}% of "
     f"omega_cdm, window ceiling), Omega_Lambda closed at z = 0 by CLASS.")

check(float(np.max(fr_tt)) < 5e-3 and float(np.max(fr_ee)) < 5e-3,
      f"C2  max |dC_l/C_l| = {np.max(fr_tt) * 100:.4f}% (TT), {np.max(fr_ee) * 100:.4f}% (EE) across "
      f"l = 2-2500 -- a factor ~2-4 amplification of the 0.046% omega_cdm shift at the acoustic "
      f"peaks (the normal dC_l/d omega_cdm response), and well below Planck's best per-bandpower "
      f"precision (~0.5%)",
      "per-multipole shifts are not detections; the significance lives in C3's chi^2, where the "
      "shifts are summed with their actual weights")

check(chi2_cv < 2.0,
      f"C3  against COSMIC VARIANCE (no noise, full sky -- harsher than any real experiment): "
      f"Delta chi^2 = {chi2_cv:.3f} over {n_modes} TT+EE multipoles, vs the sqrt(2N) ~ "
      f"{np.sqrt(2 * n_modes):.0f} threshold for a 1-sigma distinction",
      "an ideal experiment could not tell the derived-law universe from the committed one")

check(abs(th_d100 / th_b - 1) < 2.9e-4,
      f"C4  CLASS's own 100 theta_s confirms Part B: fractional shift {abs(th_d100 / th_b - 1):.2e} "
      f"({abs(th_d100 / th_b - 1) / 2.9e-4:.3f}x Planck precision)",
      f"exact integrals said {sig(dtheta, 3)} -- same answer from independent machinery")

info(f"C5  and the whole effect is absorbed by a {d_omega / 0.0012:.3f} sigma shift of omega_cdm "
     f"(Planck sigma = 0.0012): in any real fit the trace vanishes into the CDM budget, which is "
     f"the GDM degeneracy theorem doing exactly what the committed corpus said it does.")


# =================================================================================================
print()
print("=" * 100)
print("PART D -- the MOND-off input, now an output")
print("=" * 100)


def a0_ratio(z, nu0):
    z = mp.mpf(z)
    nu = nu0 * (1 + z) ** 3
    return (mp.sqrt(1 + nu0 ** 2) / mp.sqrt(1 + nu ** 2)) ** mp.mpf("0.5")


off_f = a0_ratio(Z_STAR, NU0_FLOOR)
off_c = a0_ratio(Z_STAR, NU0_CEIL)
check(off_f < mp.mpf("0.0061") and off_c < off_f,
      f"D1  a_0(z_*)/a_0(0) = {sig(off_f, 3)} (floor) to {sig(off_c, 3)} (ceiling): the committed "
      f"run's MOND-off assumption -- which the old CPL dressing supplied as 0.0060 -- is now "
      f"DELIVERED BY THE ACTION, equalled at the floor and beaten 2.9x at the ceiling",
      "with row 19 guaranteeing no perturbation-level MOND leakage on FRW at any order in y")

# =================================================================================================
print()
print("=" * 100)
print("PART E -- scope, honestly")
print("=" * 100)

info("E1  This is the SAME rigor level as the committed CMB pass, not more: CLASS stock modules, the "
     "trace bracketed as cold matter (exact at high z by stage 9's theorem -- the wall-climbing "
     "excitation is cold; conservative at low z where |1+w| <= 2.4e-5 makes reality CLOSER to "
     "LambdaCDM than the bracket).  A full Einstein-Boltzmann AeST+promotion pipeline remains the "
     "referee-grade version, exactly as it did for the committed run.")

info("E2  Footing note: nothing here depends on the a_0 normalisation (canonical vs alt) -- the "
     "window variable nu_0 is the only dial, so this result is footing-independent.")

info("E3  OWED after this stage: the MUSE/MSA-3D re-exam against the bumpless law, and the beta = 1 "
     "derivation.  Non-claim 2e's item (i) -- the CLASS re-run -- is CLOSED.")

print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  THE CLASS RE-RUN IS DONE AND THE DERIVED LAW PASSES WITHOUT VISIBLE EFFECT:

  1. the exact background differs from LambdaCDM by one cold a^-3 trace (today-density
     rho_Lambda nu_0 <= 1.2e-4 rho_crit) plus an a^-6 transient below 3.2e-8 -- nothing else;
  2. theta_* moves by {sig(dtheta, 3)} (ceiling) -- {sig(dtheta / mp.mpf('2.9e-4'), 2)}x Planck precision; max |dH/H| = {sig(max_dH, 2)};
  3. real CLASS: max |dC_l/C_l| = {np.max(fr_tt) * 100:.4f}% TT, Delta chi^2 = {chi2_cv:.2f} against cosmic
     variance over {n_modes} multipoles -- an IDEAL experiment could not distinguish them;
  4. the MOND-off-at-recombination input of the committed pass is now an OUTPUT: a_0(z_*) =
     {sig(off_c, 2)}-{sig(off_f, 2)} of today across the window.

  The committed CMB pass transfers to the v7 action.  Non-claim 2e(i) is closed; still owed:
  MUSE/MSA re-exam, beta = 1 derivation, covariant SVT.
""")

print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
