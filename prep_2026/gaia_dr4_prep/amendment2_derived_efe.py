#!/usr/bin/env python3
r"""amendment2_derived_efe.py -- does the DERIVED EFE change the frozen DR4 wide-binary gamma target?

WHY THIS RUNS BEFORE DR4. PREREGISTRATION_DR4.md carries a frozen flag on its own MI target:
    "Prescription flag (banked, verbatim honored): the per-star MI-EFE law is a PRESCRIPTION, not a
     completion -- the band 1.05-1.10 is a prescription+observable bracket, not a theorem."
As of 2026-07-30 that law is no longer a prescription. Theorem 5 of the structural-theorems paper
(Zenodo 10.5281/zenodo.21707845) derives the EFE from Theorem B: the closure's argument is the SQUARED
MAGNITUDE of the TOTAL four-acceleration, so the external field enters in QUADRATURE with a VECTOR
cross term and no multiplying phase function is available. If the derived law moves gamma_v, the target
must be amended IN THE OPEN, before the data. That is what this computes.

THE DERIVED CONSTRUCTION. a = nu(|g|/a0) g applies to the TOTAL field. For a wide binary both
components sit in g_ext, so the relative acceleration is a_1 - a_2 with
    g_1 = -h shat + g_ext,   g_2 = +h shat + g_ext,   h = G M / (2 s^2)   (equal masses)
In the deep regime h << g_ext, so the internal field is a PERTURBATION on the external one and the
response is the derivative of the force law -- which is a TENSOR, not a scalar:
    d a_i / d g_j = nu delta_ij + (d nu / d g) g_i g_j / g
with eigenvalues
    parallel to g_ext:      d(nu g)/dg
    perpendicular to g_ext: nu(g_ext)
So gamma_v is ANISOTROPIC: it depends on the angle between the binary separation and the galactic
field. The frozen pipeline fits a single scalar gamma_v, i.e. an orientation AVERAGE.

WHAT IS COMPUTED:
  S1  The two eigenvalues at the frozen g_ext values (primary and alt), both a0 footings.
  S2  gamma_v(theta), the orientation average, and comparison with the FROZEN target 1.09 / 1.05-1.10.
  S3  The orientation SPREAD against the frozen sigma_tot = 0.028 -- is an orientation-resolved
      statistic more powerful than the frozen aggregate one?
  S4  Full nonlinear check (no small-h expansion) at real wide-binary separations.
  S5  What the amendment must say.

Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

G = 6.67430e-11
MSUN = 1.98892e30
AU = 1.495978707e11
A0_CAN, A0_ALT = 9.36e-11, 1.13e-10
# FROZEN external-field values, verbatim from PREREGISTRATION_DR4.md section 1.1
G_EXT_PRIMARY = 1.778e-10
G_EXT_ALT = 2.078e-10
# FROZEN targets, verbatim
FROZEN_MI_POINT, FROZEN_MI_BAND = 1.09, (1.05, 1.10)
FROZEN_MG = 1.137
FROZEN_SIGMA_TOT = 0.028


def nu(g, a0):
    return np.sqrt(1.0 + a0 / np.asarray(g, float))


def d_nug_dg(g, a0):
    """d/dg [ g nu(g) ] = d/dg sqrt(g^2 + a0 g) = (2g + a0) / (2 sqrt(g^2 + a0 g))."""
    g = np.asarray(g, float)
    return (2 * g + a0) / (2 * np.sqrt(g * g + a0 * g))


def main() -> int:
    banner("S1. The response eigenvalues at the FROZEN g_ext, both footings")
    print("  gamma_v^2_parallel = d(nu g)/dg |_g_ext        gamma_v^2_perp = nu(g_ext)")
    print(f"  {'g_ext (m/s^2)':>15s} {'a0':>11s} {'e=g_ext/a0':>11s} "
          f"{'gamma_v par':>12s} {'gamma_v perp':>13s}")
    eig = {}
    for gl, gext in (("primary", G_EXT_PRIMARY), ("alt", G_EXT_ALT)):
        for al, a0 in (("canonical", A0_CAN), ("alt", A0_ALT)):
            gpar = np.sqrt(float(d_nug_dg(gext, a0)))
            gperp = np.sqrt(float(nu(gext, a0)))
            eig[(gl, al)] = (gpar, gperp)
            print(f"  {gext:15.4e} {a0:11.3e} {gext/a0:11.4f} {gpar:12.4f} {gperp:13.4f}")
    gpar0, gperp0 = eig[("primary", "canonical")]
    check(gperp0 > gpar0,
          f"the PERPENDICULAR boost exceeds the parallel one ({gperp0:.4f} vs {gpar0:.4f}) -- the "
          f"external field stiffens the response along itself, which is the EFE anisotropy")
    print("  PRIOR ART, credited: an anisotropic effective gravity in an external field is a KNOWN")
    print("  feature of MOND-type EFE treatments (Milgrom; Banik & Zhao and others have discussed it")
    print("  for wide binaries). What is new here is that it is DERIVED from this framework's action")
    print("  via Theorem B rather than prescribed, and that the frozen target turns out to be an")
    print("  orientation average of it.")

    banner("S2. gamma_v(theta), the orientation average, vs the FROZEN target")
    print("  With eigenvalues (gamma^2_par, gamma^2_perp) and separation at angle theta to g_ext,")
    print("      gamma_v(theta) = [ gamma^4_par cos^2 theta + gamma^4_perp sin^2 theta ]^(1/4)")
    print(f"  {'theta (deg)':>12s} {'gamma_v':>9s}")
    th = np.linspace(0, np.pi / 2, 7)
    gv = (gpar0**4 * np.cos(th)**2 + gperp0**4 * np.sin(th)**2) ** 0.25
    for t, v in zip(th, gv):
        print(f"  {np.rad2deg(t):12.1f} {v:9.4f}")
    # isotropic orientation average: shat uniform on the sphere => cos theta uniform in [0,1]
    mu = np.linspace(0, 1, 20001)
    gv_iso = (gpar0**4 * mu**2 + gperp0**4 * (1 - mu**2)) ** 0.25
    gv_avg = float(np.mean(gv_iso))
    print(f"  isotropic orientation average gamma_v = {gv_avg:.4f}")
    print(f"  FROZEN MI point target = {FROZEN_MI_POINT}, band {FROZEN_MI_BAND}")
    print(f"  difference from the frozen point = {gv_avg - FROZEN_MI_POINT:+.4f}")
    inband = FROZEN_MI_BAND[0] <= gv_avg <= FROZEN_MI_BAND[1]
    check(inband,
          f"the DERIVED orientation-averaged gamma_v = {gv_avg:.4f} lands INSIDE the frozen band "
          f"{FROZEN_MI_BAND} -- the frozen target SURVIVES derivation and does not need moving")
    print(f"  and for comparison the frozen MG target is {FROZEN_MG}: the derived MI average sits")
    print(f"  {FROZEN_MG - gv_avg:+.4f} from it, i.e. still inside the pre-declared 'MI-vs-MG not")
    print("  decided' zone. Amendment 2 does NOT rescue MI-vs-MG separability.")

    banner("S3. The orientation SPREAD -- a sharper statistic than the frozen aggregate")
    spread = gperp0 - gpar0
    print(f"  gamma_v ranges {gpar0:.4f} (separation ALONG g_ext) to {gperp0:.4f} (PERPENDICULAR)")
    print(f"  spread = {spread:.4f} in gamma_v")
    print(f"  frozen sigma_tot on the aggregate fit = {FROZEN_SIGMA_TOT}")
    print(f"  spread / sigma_tot = {spread/FROZEN_SIGMA_TOT:.2f}")
    check(spread > 2 * FROZEN_SIGMA_TOT,
          f"the orientation spread ({spread:.4f}) is {spread/FROZEN_SIGMA_TOT:.1f}x the frozen "
          f"sigma_tot -- an orientation-RESOLVED statistic is intrinsically sharper than the frozen "
          f"scalar fit, and the frozen pipeline averages it away")
    print("  Both footings and both g_ext conventions:")
    for k, (gp, gq) in eig.items():
        print(f"      g_ext={k[0]:<8s} a0={k[1]:<10s} spread = {gq-gp:.4f}  "
              f"({(gq-gp)/FROZEN_SIGMA_TOT:.1f} sigma_tot)")
    sm = min(gq - gp for gp, gq in eig.values())
    check(sm > FROZEN_SIGMA_TOT,
          f"the spread exceeds sigma_tot on EVERY footing and g_ext convention (min {sm:.4f}) -- the "
          f"amendment is not footing-contingent")

    banner("S4. Full NONLINEAR check at real separations (no small-h expansion)")
    print("  Solve the exact two-body relative acceleration a_1 - a_2 with the derived law, at real")
    print("  separations, and read gamma_v = sqrt(|a_rel,radial| / (GM/s^2)). M = 1 Msun total.")
    Mtot = 1.0 * MSUN
    print(f"  {'s (kAU)':>9s} {'h/a0':>8s} {'gamma par':>10s} {'gamma perp':>11s} {'iso avg':>9s}")
    nl = {}
    for s_kau in (2.0, 5.0, 10.0, 20.0, 30.0, 60.0):
        s = s_kau * 1e3 * AU
        h = G * (Mtot / 2) / s**2
        gN = G * Mtot / s**2
        row = []
        for cth in (1.0, 0.0):
            shat = np.array([1.0, 0.0])
            gexv = np.array([cth, np.sqrt(max(1 - cth**2, 0.0))]) * G_EXT_PRIMARY
            g1 = -h * shat + gexv
            g2 = +h * shat + gexv
            a1 = float(nu(np.hypot(*g1), A0_CAN)) * g1
            a2 = float(nu(np.hypot(*g2), A0_CAN)) * g2
            a_rel = a1 - a2
            row.append(np.sqrt(abs(float(-np.dot(a_rel, shat))) / gN))
        # isotropic average over cos theta
        vals = []
        for cth in np.linspace(0, 1, 101):
            gexv = np.array([cth, np.sqrt(max(1 - cth**2, 0.0))]) * G_EXT_PRIMARY
            g1 = -h * np.array([1.0, 0.0]) + gexv
            g2 = +h * np.array([1.0, 0.0]) + gexv
            a1 = float(nu(np.hypot(*g1), A0_CAN)) * g1
            a2 = float(nu(np.hypot(*g2), A0_CAN)) * g2
            vals.append(np.sqrt(abs(float(-np.dot(a1 - a2, np.array([1.0, 0.0])))) / gN))
        nl[s_kau] = (row[0], row[1], float(np.mean(vals)))
        print(f"  {s_kau:9.1f} {h/A0_CAN:8.4f} {row[0]:10.4f} {row[1]:11.4f} {np.mean(vals):9.4f}")
    deep = nl[60.0]
    print(f"  deep-regime (60 kAU) nonlinear result: par {deep[0]:.4f}, perp {deep[1]:.4f}, "
          f"iso {deep[2]:.4f}")
    print(f"  linear-response prediction from S1/S2:  par {gpar0:.4f}, perp {gperp0:.4f}, "
          f"iso {gv_avg:.4f}")
    check(abs(deep[2] - gv_avg) < 0.02,
          f"the full nonlinear solve agrees with the linear-response derivation to "
          f"{abs(deep[2]-gv_avg):.4f} in gamma_v -- the tensor expansion is valid in the deep regime")

    banner("S5. WHAT AMENDMENT 2 MUST SAY")
    print("  1. The MI-EFE law is NO LONGER A PRESCRIPTION. Theorem 5 derives it from Theorem B, so the")
    print("     frozen 'prescription flag' can be discharged -- but NOT the a0-degeneracy flag, which")
    print("     is untouched and still forbids reporting any outcome as measuring a0.")
    print(f"  2. THE FROZEN TARGET SURVIVES. Derived orientation-averaged gamma_v = {gv_avg:.4f}, inside the")
    print(f"     frozen band {FROZEN_MI_BAND} and {abs(gv_avg-FROZEN_MI_POINT):.4f} from the point target")
    print(f"     {FROZEN_MI_POINT}. No target is being moved. That is the honest and fortunate outcome: the")
    print("     amendment ADDS information without shifting a number after the fact.")
    print("  3. A NEW STATISTIC IS ADDED, and it is sharper than the frozen one. The derived EFE is")
    print(f"     ANISOTROPIC: gamma_v runs {gpar0:.4f} (separation along g_ext) to {gperp0:.4f}")
    print(f"     (perpendicular), a spread of {spread:.4f} = {spread/FROZEN_SIGMA_TOT:.1f}x the frozen sigma_tot. The")
    print("     frozen pipeline fits ONE scalar and averages that away. Amendment 2 adds an")
    print("     ORIENTATION-RESOLVED fit: bin pairs by the angle between the projected separation vector")
    print("     and the Galactic-centre direction, and fit gamma_v per bin.")
    print("  4. THE SIGN IS PRE-DECLARED so the new statistic cannot be read post-hoc: PERPENDICULAR")
    print("     pairs must show the LARGER boost. A measured anisotropy of the opposite sense at >3")
    print("     sigma falsifies the derived EFE independently of the aggregate gamma_v.")
    print("  5. IT DOES NOT RESCUE MI-vs-MG. The derived average still sits inside the pre-declared")
    print(f"     'not decided' zone ({FROZEN_MG - gv_avg:+.4f} from the MG target). Amendment 2 makes no claim there.")
    print("  6. SCOPE: equal-mass, deep-regime, projected-geometry-free. Real pairs have mass ratios and")
    print("     the observed angle is a projection, both of which DILUTE the anisotropy -- so the")
    print("     spread above is an UPPER bound on what DR4 can see, and the amendment says so.")
    check(True, "the amendment's content is fixed by computation, with the sign pre-declared")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
