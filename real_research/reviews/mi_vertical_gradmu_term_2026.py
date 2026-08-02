#!/usr/bin/env python3
r"""mi_vertical_gradmu_term_2026.py -- THE TERM THE VERTICAL-FORCE ANALYSIS DROPS, and why it is not a
small correction in the regime where the measurement is made.

WHERE THIS COMES FROM. mi_vertical_force_data_confrontation_2026 found the framework's alpha=2 kernel
sits 3.8-9.4 sigma from the local boost mu_0 = 0.64 +- 0.03 measured by Syaifudin, Arifyanto, Wulandari &
Mulki 2024 (MNRAS 534, 3387; arXiv:2401.11534). This script examines HOW mu_0 is extracted.

THE EXACT AQUAL FIELD EQUATION and the approximation. Bekenstein & Milgrom (1984):
    4 pi G rho = div[ mu(|grad Phi|/a0) grad Phi ] = mu * lap(Phi) + grad(mu) . grad(Phi)
Syaifudin et al. Section 3.3 reduce this to their working equation (17), lap(Phi) = 4 pi G rho / mu_0,
by dropping grad(mu).grad(Phi). Their stated justification, quoted verbatim from the paper:
    "In small volumes, where the total acceleration |grad Phi| is approximately constant, the modified
     Poisson's equation (15) can be simplified to ..."
So mu_0 is defined by mu_0 = 4 pi G rho / lap(Phi), and the exact relation instead gives
    mu_exact = mu_0 - [ grad(mu) . grad(Phi) ] / lap(Phi).

  R1  The decomposition, and the ratio |grad(mu).grad(Phi)| / |mu lap(Phi)| as a function of height above
      a Miyamoto-Nagai Milky Way disc at R0 = 8 kpc.
  R2  WHY it diverges with height, which is the physical point: lap(Phi) = 4 pi G rho falls to nothing
      above the disc while grad(mu).grad(Phi) stays finite. Above a disc the AQUAL equation is
      mu lap(Phi) + grad(mu).grad(Phi) ~ 0 -- the two terms BALANCE, so the dropped term is the LEADING
      one there, not a correction to it.
  R3  THE SIGN, which is the part that bears on the framework: grad(mu).grad(Phi) < 0, so
      mu_exact > mu_0. That is the direction that EASES a framework predicting a high mu.
  R4  MUTATION CONTROL isolating the mechanism: thicken the disc so rho falls off more slowly and the
      ratio must shrink; flatten it and the ratio must grow.
  R5  WHAT THIS DOES AND DOES NOT ESTABLISH. It does NOT vindicate the framework, and the single
      observation that would kill this line is named explicitly.

Exit 0 = ran and every internal check held. No hard-coded verdicts.
"""
from __future__ import annotations

import math
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


G = 6.67430e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
M_DISC = 6.0e10 * MSUN
GM = G * M_DISC
R0 = 8.0 * KPC
H = 1.0e-3 * KPC

MU0_MEAS, MU0_STAT = 0.64, 0.03           # Syaifudin+2024, their extracted local boost
MU_FW_PRED = 0.9227                       # framework alpha=2, canonical a0, from the confrontation script
A0 = {"canon": 9.36e-11, "alt": 1.13e-10}


def make_disc(a_kpc: float, b_kpc: float):
    """Miyamoto-Nagai potential and the operators built from it, by finite differences."""
    A, B = a_kpc * KPC, b_kpc * KPC

    def Phi(R, z):
        return -GM / np.sqrt(R * R + (A + np.sqrt(z * z + B * B)) ** 2)

    def grad(R, z):
        return ((Phi(R + H, z) - Phi(R - H, z)) / (2 * H),
                (Phi(R, z + H) - Phi(R, z - H)) / (2 * H))

    def gmag(R, z):
        gR, gz = grad(R, z)
        return np.hypot(gR, gz)

    def lap(R, z):
        dR = (Phi(R + H, z) - Phi(R - H, z)) / (2 * H)
        d2R = (Phi(R + H, z) - 2 * Phi(R, z) + Phi(R - H, z)) / H**2
        d2z = (Phi(R, z + H) - 2 * Phi(R, z) + Phi(R, z - H)) / H**2
        return d2R + dR / R + d2z

    return Phi, grad, gmag, lap


def mu2(x):
    return x / np.sqrt(1.0 + x * x)


def dmu2(x):
    return 1.0 / (1.0 + x * x) ** 1.5


def terms(gmag, grad, lap, R, z, a0):
    """Return (mu, mu*lap, gradmu.gradPhi, ratio)."""
    gR, gz = grad(R, z)
    x = gmag(R, z) / a0
    dgR = (gmag(R + H, z) - gmag(R - H, z)) / (2 * H)
    dgz = (gmag(R, z + H) - gmag(R, z - H)) / (2 * H)
    gmu_gPhi = dmu2(x) / a0 * (dgR * gR + dgz * gz)
    L = lap(R, z)
    return mu2(x), mu2(x) * L, gmu_gPhi, gmu_gPhi / (mu2(x) * L)


banner("R1  THE DROPPED TERM, MEASURED AGAINST THE RETAINED ONE, ABOVE A MILKY-WAY DISC")

Phi, grad, gmag, lap = make_disc(3.0, 0.3)
a0 = A0["canon"]
print(f"  Miyamoto-Nagai: M = {M_DISC/MSUN:.1e} Msun, a = 3.0 kpc, b = 0.3 kpc, at R0 = 8 kpc, "
      f"a0 = {a0:.3e}\n")
print(f"  {'z [kpc]':>9}{'x=|gPhi|/a0':>13}{'mu':>8}{'mu*lap':>13}{'gradmu.gPhi':>14}{'ratio':>10}"
      f"{'mu_exact':>11}")
print("  " + "-" * 80)
prof = {}
for zk in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0):
    z = zk * KPC
    m, mlap, gg, ratio = terms(gmag, grad, lap, R0, z, a0)
    mu_ex = MU0_MEAS - gg / lap(R0, z)
    prof[zk] = (ratio, mu_ex)
    print(f"  {zk:>9.2f}{gmag(R0,z)/a0:>13.3f}{m:>8.4f}{mlap:>13.3e}{gg:>14.3e}{ratio:>10.3f}"
          f"{mu_ex:>11.4f}")
check(abs(prof[0.05][0]) < 0.15,
      f"R1 close to the midplane the dropped term is genuinely small ({abs(prof[0.05][0]):.3f} at "
      f"z = 0.05 kpc), so the approximation is defensible THERE and the criticism is not generic")
check(abs(prof[1.0][0]) > 1.0 and abs(prof[2.0][0]) > 5.0,
      f"R1b but it OVERTAKES the retained term with height: ratio {abs(prof[1.0][0]):.2f} at 1 kpc and "
      f"{abs(prof[2.0][0]):.1f} at 2 kpc, so the dropped term dominates over most of the analysed volume")
cross = [zk for zk in sorted(prof) if abs(prof[zk][0]) >= 1.0]
zc = min(cross) if cross else None
check(zc is not None and 0.3 < zc < 1.0,
      f"R1c the crossover where the dropped term equals the retained one is at z ~ {zc} kpc -- inside the "
      f"|z| < 1.1 kpc range over which the local surface density is quoted (Bovy & Rix 2013)")


banner("R2  WHY IT DIVERGES -- and the physical point that follows")

print(f"  {'z [kpc]':>9}{'lap(Phi) = 4 pi G rho':>24}{'gradmu.gradPhi':>18}")
print("  " + "-" * 54)
for zk in (0.05, 0.5, 1.0, 2.0):
    z = zk * KPC
    _, _, gg, _ = terms(gmag, grad, lap, R0, z, a0)
    print(f"  {zk:>9.2f}{lap(R0,z):>24.4e}{gg:>18.4e}")
l_lo, l_hi = lap(R0, 0.05 * KPC), lap(R0, 2.0 * KPC)
_, _, g_lo, _ = terms(gmag, grad, lap, R0, 0.05 * KPC, a0)
_, _, g_hi, _ = terms(gmag, grad, lap, R0, 2.0 * KPC, a0)
check(l_lo / l_hi > 100 and abs(g_lo / g_hi) < 3,
      f"R2 the retained term collapses by {l_lo/l_hi:.0f}x from z = 0.05 to 2 kpc (it is 4 pi G rho, and "
      f"the density is vanishing) while the dropped term changes by only {abs(g_lo/g_hi):.2f}x -- so the "
      f"ratio diverges because the RETAINED term dies, not because the dropped one grows")
print("""
  THE PHYSICAL POINT. Above a disc there is almost no matter, so the AQUAL equation reads
      mu lap(Phi) + grad(mu).grad(Phi) ~ 0,
  i.e. the two terms BALANCE. In that region the dropped term is not a correction to the retained one --
  it is the same size, with opposite sign. An approximation that discards it is not making a small error
  in the low-density region; it is discarding one of the two leading terms. And the low-density region
  above the plane is exactly where vertical-force tracers live.""")


banner("R3  THE SIGN, AND WHERE THE CORRECTED EXTRACTION LANDS")

check(all(prof[zk][0] < 0 for zk in prof),
      "R3 grad(mu).grad(Phi) is NEGATIVE at every height tested, so mu_exact = mu_0 - (that)/lap > mu_0 "
      "-- the correction runs in the direction that EASES a framework predicting a HIGH mu")
mu_at = {zk: prof[zk][1] for zk in prof}
print(f"  the framework predicts mu = {MU_FW_PRED:.4f} (alpha=2, canonical a0). The corrected extraction:")
for zk in (0.05, 0.2, 0.4, 0.5, 0.6):
    print(f"    z = {zk:.2f} kpc -> mu_exact = {mu_at[zk]:.4f}"
          f"{'   <-- brackets the framework value' if mu_at[zk] > MU_FW_PRED else ''}")
below = [zk for zk in sorted(mu_at) if mu_at[zk] < MU_FW_PRED]
above = [zk for zk in sorted(mu_at) if mu_at[zk] > MU_FW_PRED]
check(bool(below) and bool(above),
      f"R3b the corrected mu_exact SWEEPS THROUGH the framework's predicted {MU_FW_PRED:.3f}: below it for "
      f"z <= {max(below):.2f} kpc, above it by z >= {min(above):.2f} kpc. So once the term is restored the "
      f"'measured' mu_0 is not a single number to be compared against -- it is height-dependent, and it "
      f"passes through the framework's value inside the analysed volume")
check(mu_at[1.0] > 1.0,
      f"R3c and the corrected value exceeds mu = 1 by z = 1 kpc ({mu_at[1.0]:.2f}), which is UNPHYSICAL "
      f"(mu <= 1 by construction) -- an independent sign that the extraction, not the framework, is what "
      f"has broken down there")


banner("R4  MUTATION CONTROL -- isolate the mechanism by changing the density falloff")

print(f"  {'disc b [kpc]':>13}{'ratio at z=0.5 kpc':>21}{'ratio at z=1.0 kpc':>21}")
print("  " + "-" * 56)
ratios_by_b = {}
for bk in (0.1, 0.3, 1.0, 3.0):
    P2, g2, gm2, l2 = make_disc(3.0, bk)
    r05 = terms(gm2, g2, l2, R0, 0.5 * KPC, a0)[3]
    r10 = terms(gm2, g2, l2, R0, 1.0 * KPC, a0)[3]
    ratios_by_b[bk] = (r05, r10)
    print(f"  {bk:>13.1f}{abs(r05):>21.3f}{abs(r10):>21.3f}")
check(abs(ratios_by_b[0.1][1]) > abs(ratios_by_b[3.0][1]),
      f"R4 MUTATION: thickening the disc from b = 0.1 to 3.0 kpc shrinks the ratio at z = 1 kpc from "
      f"{abs(ratios_by_b[0.1][1]):.2f} to {abs(ratios_by_b[3.0][1]):.2f} -- confirming the mechanism is "
      f"the DENSITY FALLOFF and not the choice of kernel, a0 or radius")
check(abs(ratios_by_b[3.0][1]) < 1.0,
      f"R4b and for a thick enough mass distribution the approximation becomes valid again "
      f"({abs(ratios_by_b[3.0][1]):.2f} < 1), which is why it is a sound approximation in the spherical "
      f"systems it was designed for and unsound above a thin disc")


banner("R5  WHAT THIS DOES AND DOES NOT ESTABLISH")

print(f"""  ESTABLISHED:
   * The extraction of mu_0 in Syaifudin et al. 2024 drops grad(mu).grad(Phi) on the stated grounds that
     |grad Phi| is approximately constant. Above a thin disc that fails: the dropped term equals the
     retained one at z ~ {zc} kpc and exceeds it by {abs(prof[1.0][0]):.1f}x at 1 kpc, because the retained term is
     4 pi G rho and the density is vanishing there.
   * The correction has the sign that EASES the framework, and the corrected mu_exact sweeps through the
     framework's predicted {MU_FW_PRED:.3f} inside the analysed volume, exceeding the physical bound mu <= 1
     by z = 1 kpc.
   * So the 3.8-9.4 sigma reported previously is a comparison against a quantity whose extraction is not
     valid over most of the volume it was extracted from. That sigma should NOT be quoted as a
     measurement of a discrepancy with the framework.

  NOT ESTABLISHED, and this is the honest half:
   * THIS DOES NOT VINDICATE THE FRAMEWORK. It removes a claimed discrepancy; it does not supply
     agreement. The correct procedure is to solve AQUAL (or QUMOND) properly on a Milky-Way baryon model
     and refit the vertical tracers with the framework's a0 held FIXED. That has not been done here.
   * The correction is evaluated on the NEWTONIAN Miyamoto-Nagai field, not on the self-consistent MOND
     potential, so the numbers are a first-order estimate of a size, not a corrected measurement.
   * ONE OBSERVATION WOULD KILL THIS LINE ENTIRELY: if any published analysis solves the full AQUAL or
     QUMOND field equation numerically -- dropping nothing -- and still infers nu ~ 1.4-1.6, then the
     approximation is not the explanation and the tension is real. Lisanti et al. 2019 (PRD) infers
     nu = 1.44 (+0.13/-0.08) independently and is the specific paper to check. Until that check is done
     this reconciliation is a CANDIDATE, not a result.
   * The other direction in the literature -- that MOND OVER-predicts the vertical force -- is still
     unreconciled by this script; what is offered here is a mechanism by which a mu_0-style extraction
     could read high, which would move Claim A toward Claim B, but the primary sources for Claim B have
     not been read here.

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
print("  Exit 0: the dropped term is quantified, its sign established, and the killing test named.")
