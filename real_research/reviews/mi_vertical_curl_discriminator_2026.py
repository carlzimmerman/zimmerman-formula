#!/usr/bin/env python3
r"""mi_vertical_curl_discriminator_2026.py -- TURNING THE OBSTRUCTION INTO A FRONT. The non-variationality
of the MI law is not only a defect: because AQUAL/QUMOND are conservative BY CONSTRUCTION and algebraic MI
is not, the circulation is a genuine MI-vs-MG DISCRIMINATOR in VERTICAL DISC DYNAMICS -- and it grows
toward the midplane, where the data is best.

WHY THIS IS WORTH A SWING. Three days of results closed the action programme for the published form
class: the law is not variational in a disc (mi_law_is_nonvariational_2026), the u-contraction is
(v/c)^2-suppressed for ANY kernel (mi_nonlocal_amplitude_nogo_2026), and |a|^2 is not in Box_u's spectrum
so no F(Box_u) fixes it (mi_eigenvalue_a2_operator_nogo_2026). All three are no-goes. This script asks
the constructive question they leave: WHAT IS THE OBSERVABLE CONSEQUENCE?

  B1  ANY variational, time-translation-invariant theory has INT F.dl = 0 around every closed loop. The
      algebraic MI law does not. The midplane RADIAL force is pinned by rotation curves, so the required
      deviation is forced into the VERTICAL force. Quantified leg by leg.
  B2  LOOP-FAMILY SCAN over 16 contours: the required fractional deviation is NONZERO for every one, so
      it cannot be tuned away by choice of contour -- and it GROWS toward the midplane, 2-4% out at
      |z| ~ 3 kpc rising to 19-29% within |z| < 0.5 kpc.
  B3  THE DISCRIMINATOR. AQUAL and QUMOND both have force = -grad(Phi_eff), so their circulation is
      IDENTICALLY ZERO by construction. Verified against a genuine gradient field: 3e-8 relative versus
      1.1e-2 for the MI law, a 3.5e5 separation. So this is NOT MOND-shared, and it does not involve a0's
      value, so it is NOT a0-degenerate either -- the two properties that have neutralised almost every
      other front in this corpus.
  B4  MAGNITUDE VERSUS DATA PRECISION -- the reason this is a front and not a curiosity.
  B5  THE TWO READINGS, both of which give a vertical signature, and which one is defensible.
  B6  HONEST SCOPE: what is NOT done here.

CONTROLS. A genuine gradient field must return zero circulation; the first version of that control used a
field whose cross-derivatives were unequal (1/2 vs 1/6) and it correctly FAILED, which is recorded here
because it is the control earning its place. A constant nu must also return zero.

Both a0 footings and both kernels throughout. Exit 0 = ran and every check held. No hard-coded verdicts.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import sys

import numpy as np

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t: str) -> None:
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


# reuse the verified disc model and force law rather than re-deriving them
_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("mlnv", os.path.join(_HERE, "mi_law_is_nonvariational_2026.py"))
mlnv = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(mlnv)
KPC, T = mlnv.KPC, mlnv._TRAPZ
NUS, FOOTINGS = mlnv.NUS, mlnv.FOOTINGS


def circ(fn, R1, R2, z1, z2, N=3000):
    """INT F.dl anticlockwise around the meridional rectangle, for a callable fn(R,z)->(F_R,F_z)."""
    Rs, zs = np.linspace(R1, R2, N), np.linspace(z1, z2, N)
    dR, dz = Rs[1] - Rs[0], zs[1] - zs[0]
    return (T(fn(Rs, np.full_like(Rs, z1))[0], dx=dR) + T(fn(np.full_like(zs, R2), zs)[1], dx=dz)
            - T(fn(Rs, np.full_like(Rs, z2))[0], dx=dR) - T(fn(np.full_like(zs, R1), zs)[1], dx=dz))


def mi_force(nufun, a0):
    return lambda R, z: mlnv.force(R, z, nufun, a0)


def vertical_legs(nufun, a0, R1, R2, z2, N=3000):
    zs = np.linspace(0.0, z2, N)
    dz = zs[1] - zs[0]
    r = T(mlnv.force(np.full_like(zs, R2), zs, nufun, a0)[1], dx=dz)
    l = T(mlnv.force(np.full_like(zs, R1), zs, nufun, a0)[1], dx=dz)
    return abs(r) + abs(l)


banner("B1  THE CIRCULATION IS FORCED INTO THE VERTICAL FORCE, BECAUSE THE MIDPLANE IS PINNED")

R1, R2, z1, z2 = mlnv.LOOP
print(f"  loop: R = {R1/KPC:.0f}-{R2/KPC:.0f} kpc, z = 0-{z2/KPC:.0f} kpc, Miyamoto-Nagai MW disc\n")
print(f"  {'kernel':<9}{'footing':<7}{'bottom z=0 (PINNED)':>22}{'top z=2kpc':>14}{'vertical legs':>15}{'total':>13}")
print("  " + "-" * 92)
rows = {}
for kn, nf in NUS.items():
    for fn_, a0 in FOOTINGS.items():
        Rs, zs = np.linspace(R1, R2, 3000), np.linspace(z1, z2, 3000)
        dR, dz = Rs[1] - Rs[0], zs[1] - zs[0]
        bot = T(mlnv.force(Rs, np.full_like(Rs, z1), nf, a0)[0], dx=dR)
        top = -T(mlnv.force(Rs, np.full_like(Rs, z2), nf, a0)[0], dx=dR)
        vleg = vertical_legs(nf, a0, R1, R2, z2)
        tot = circ(mi_force(nf, a0), R1, R2, z1, z2)
        rows[(kn, fn_)] = (bot, top, vleg, tot)
        print(f"  {kn:<9}{fn_:<7}{bot:>22.4e}{top:>14.4e}{vleg:>15.4e}{tot:>13.4e}")
check(all(abs(v[3]) > 0 for v in rows.values()),
      "B1 the circulation is nonzero on every kernel and footing, so a conservative theory cannot "
      "reproduce this force field")
fr = {k: abs(v[3]) / v[2] for k, v in rows.items()}
print(f"\n  required fractional change in the VERTICAL legs, all four combinations:")
for k, v in fr.items():
    print(f"    {k[0]:<9}{k[1]:<7}{v:>8.2%}")
check(all(0.02 < v < 0.5 for v in fr.values()),
      f"B1b the required deviation is {min(fr.values()):.2%}-{max(fr.values()):.2%} across kernels and "
      f"footings -- a few percent, not a rounding error and not order unity")


banner("B2  LOOP-FAMILY SCAN -- it cannot be tuned away, and it GROWS toward the midplane")

print(f"  {'R1-R2 [kpc]':>13}{'z_max [kpc]':>13}{'circulation':>15}{'req. frac':>12}")
print("  " + "-" * 56)
scan, by_z = [], {}
for (a, b) in ((4, 12), (6, 10), (3, 15), (8, 12)):
    for zt in (0.5, 1.0, 2.0, 3.0):
        L = (a * KPC, b * KPC, 0.0, zt * KPC)
        c = circ(mi_force(NUS["alpha=1"], FOOTINGS["canon"]), *L)
        v = vertical_legs(NUS["alpha=1"], FOOTINGS["canon"], a * KPC, b * KPC, zt * KPC)
        f = abs(c) / v
        scan.append(f)
        by_z.setdefault(zt, []).append(f)
        print(f"  {a:>5}-{b:<7}{zt:>13.1f}{c:>15.3e}{f:>12.2%}")
check(all(f > 0.01 for f in scan),
      f"B2 every one of the {len(scan)} contours gives a required deviation above 1% "
      f"({min(scan):.2%}-{max(scan):.2%}) -- it cannot be tuned away by choice of loop")
means = {zt: sum(v) / len(v) for zt, v in by_z.items()}
print(f"\n  mean required deviation by z_max: " + ", ".join(f"{zt} kpc -> {mn:.1%}" for zt, mn in means.items()))
check(means[0.5] > means[3.0] * 3,
      f"B2b *** IT GROWS TOWARD THE MIDPLANE ***: {means[0.5]:.1%} within |z| < 0.5 kpc against "
      f"{means[3.0]:.1%} out to 3 kpc, a factor {means[0.5]/means[3.0]:.1f} -- and the midplane is where "
      f"vertical-force data is best, not worst")


banner("B3  THE DISCRIMINATOR: AQUAL/QUMOND ARE CONSERVATIVE BY CONSTRUCTION")

# Psi = sin(R/3kpc) exp(-z/2kpc); cross-derivatives verified equal below, so F = -grad(Psi) exactly.
def grad_field(Rv, zv):
    e = np.exp(-zv / (2 * KPC))
    return -np.cos(Rv / (3 * KPC)) * e / (3 * KPC), +np.sin(Rv / (3 * KPC)) * e / (2 * KPC)


h = 1.0e-4 * KPC
Rt, zt_ = 7.0 * KPC, 0.8 * KPC
dFRdz = (grad_field(Rt, zt_ + h)[0] - grad_field(Rt, zt_ - h)[0]) / (2 * h)
dFzdR = (grad_field(Rt + h, zt_)[1] - grad_field(Rt - h, zt_)[1]) / (2 * h)
print(f"  control field: F = -grad(Psi), Psi = sin(R/3kpc)exp(-z/2kpc)")
print(f"    dF_R/dz = {dFRdz:.6e}   dF_z/dR = {dFzdR:.6e}   -> curl = {dFRdz-dFzdR:.3e}")
check(abs(dFRdz - dFzdR) < 1e-6 * max(abs(dFRdz), abs(dFzdR)),
      "B3 the control field really IS a gradient (cross-derivatives agree to 1e-6 relative). The first "
      "version of this control used a field whose cross-derivatives differed by 1/2 vs 1/6 and it "
      "correctly FAILED -- recorded because that is the control earning its place")
g = circ(grad_field, R1, R2, z1, z2)
Rs = np.linspace(R1, R2, 400)
gscale = np.max(np.abs(grad_field(Rs, np.zeros(400))[0])) * (R2 - R1)
mi = circ(mi_force(NUS["alpha=1"], FOOTINGS["canon"]), R1, R2, z1, z2)
mscale = np.max(np.abs(mlnv.force(Rs, np.zeros(400), NUS["alpha=1"], FOOTINGS["canon"])[0])) * (R2 - R1)
print(f"\n  gradient field : circulation/scale = {abs(g)/gscale:.3e}   (numerical zero)")
print(f"  MI algebraic   : circulation/scale = {abs(mi)/mscale:.3e}")
check(abs(g) / gscale < 1e-6 and abs(mi) / mscale > 1e-3,
      f"B3b a genuine gradient gives {abs(g)/gscale:.1e} while the MI law gives {abs(mi)/mscale:.1e} -- a "
      f"separation of {(abs(mi)/mscale)/(abs(g)/gscale):.1e}. AQUAL and QUMOND both have "
      f"force = -grad(Phi_eff), so their circulation is IDENTICALLY zero: this is a real MI-vs-MG test")
# and it is not a0-degenerate: the required FRACTION barely moves between footings
spread = max(fr.values()) / min(fr.values())
check(spread < 1.4,
      f"B3c and it is NOT a0-degenerate: the required fraction moves only {spread:.2f}x between the two a0 "
      f"footings (which differ by 21%), so the signal is the CURL's existence, not a0's value")


banner("B4  MAGNITUDE VERSUS DATA PRECISION")

print(f"""  The required deviation from the algebraic law, in the vertical force, is
      {means[0.5]:.0%} within |z| < 0.5 kpc,  {means[1.0]:.0%} within 1 kpc,  {means[2.0]:.0%} within 2 kpc.
  Local vertical-force determinations -- the surface density Sigma(|z| < 1.1 kpc) from stellar
  kinematics -- are quoted in the literature at roughly the 5-10% level. On those numbers the required
  deviation at |z| <~ 1 kpc EXCEEDS current precision by a factor of a few.

  *** SO THIS IS A LIVE FRONT, and it has the two properties this corpus has almost never had at once:
  it is NOT MOND-shared (AQUAL/QUMOND are conservative by construction, B3) and it is NOT a0-degenerate
  (B3c). Nearly every other front in the standing record fails on one or the other. ***""")
check(means[1.0] > 0.10,
      f"B4 the required deviation within |z| < 1 kpc is {means[1.0]:.1%}, above the ~5-10% level at which "
      f"local vertical-force work is quoted -- so the front is testable with existing classes of data")
print("""
  ⚠️ THE OBSERVATIONAL PRECISION FIGURES ABOVE ARE FROM MEMORY AND ARE NOT SOURCED HERE. They must be
  taken from the primary literature before any confrontation is claimed. What this script establishes is
  the REQUIRED DEVIATION, which is computed; the comparison is indicative only.""")


banner("B5  THE TWO READINGS -- both give a vertical signature")

print("""  READING 1 -- the algebraic law IS the theory. Then it is non-conservative, which is a defect, but
  it is also a signature: the predicted vertical force differs from any conservative model's, and orbits
  crossing the plane do not conserve energy. Weakness: a non-conservative "theory" is not a theory, so
  "it predicts X" is a strained thing to say, and no N-body or Jeans machinery is available to say it with.

  READING 2 -- the true MI theory is some variational completion that agrees with the algebraic law where
  the RAR is fit (the midplane radial force) and deviates elsewhere. Then the deviation is FORCED to be at
  least the circulation, distributed over the remaining legs -- the numbers in B1-B2. This is the
  defensible reading, and the honest way to state the prediction: ANY variational MI completion matching
  the rotation curve must differ from the algebraic law in the vertical force by the amounts above.

  Either way the observable lives in VERTICAL disc dynamics at the several-percent level, and MG predicts
  exactly zero there. That is the front.""")


banner("B6  WHAT IS NOT DONE HERE")

print(f"""   * NO DATA CONFRONTATION. No Sigma(z), no K_z, no vertical Jeans solution, no real galaxy. This
     establishes that the front EXISTS, is not MOND-shared, is not a0-degenerate, and sits at a magnitude
     comparable to or above current precision. The actual test needs a vertical Jeans analysis against
     primary data and is the owed next step.
   * ONE DISC MODEL. Miyamoto-Nagai with MW-like parameters. The effect must be shown robust to the disc
     model (exponential + Bessel, a real SPARC mass model) before any number is quoted as a prediction.
   * THE SIGN AND PATTERN of the deviation are not derived -- only its minimum magnitude. Which way the
     vertical force must move, and how it varies with R, requires the completion itself, which the three
     no-goes say is not of the published form.
   * NO CLAIM THAT THIS FALSIFIES OR CONFIRMS ANYTHING. It identifies where to look.

  UNTOUCHED: the RAR fit, the a0-line, the BTFR, all spherical work, and a0 = kappa c sqrt(G rho_Lambda).""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: a new MI-vs-MG front identified, with the gradient control verified to be a gradient.")
