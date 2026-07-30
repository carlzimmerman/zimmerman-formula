#!/usr/bin/env python3
r"""mi_local_anisotropy_origin_2026.py -- WHY are local conditions anisotropic, and is there a
novel computable door for the modified-inertia framework?

PART 1 -- WHY. The answer is statistical and rather beautiful, and it is classical (Doroshkevich
1970, Zel'dovich 1970). Collapse is governed by the deformation tensor -- the Hessian of the
gravitational potential -- which for a Gaussian random field is a RANDOM SYMMETRIC MATRIX. Random
symmetric matrices exhibit EIGENVALUE REPULSION: the probability of two eigenvalues being nearly
equal is suppressed. Since spherical collapse requires all THREE eigenvalues equal, sphericity is
not merely rare -- it is measure zero. Anisotropy is not something the universe had to be given.
It is what a generic draw looks like.

PART 2 -- THE DOOR. Anisotropic collapse is RADIAL INFALL, i.e. maximally NON-CIRCULAR. And the
framework has a documented open choice that CIRCLES CANNOT SEE: the off-circular closure. The
repo's own verdict (mi_offcircular_completion_SPEC.py) is FREE, bounded -- because on a circular
orbit |a| is constant, so every time-weighting of |a|^2 coincides, and only non-circular
trajectories split them. So anisotropic collapse is precisely the regime that would FIX or BRACKET
the framework's remaining closure ambiguity. This script quantifies the spread.

NOVELTY, assessed honestly at the end rather than asserted here.

Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math
import numpy as np

G = 6.67430e-11
MSUN = 1.98892e30
KPC = 3.0857e19
A0 = 9.36e-11
A0_ALT = 1.13e-10

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)

def nu(y):
    return math.sqrt(1.0 + 1.0 / y)


def main() -> int:
    banner("PART 1. WHY local collapse is anisotropic: eigenvalue repulsion (Doroshkevich 1970)")
    print("  Collapse is set by the deformation tensor d^2 phi / dx_i dx_j -- a symmetric 3x3")
    print("  matrix. For a Gaussian random density field this is a random symmetric matrix drawn")
    print("  from the Gaussian Orthogonal Ensemble. Spherical collapse needs lambda_1 = lambda_2 =")
    print("  lambda_3. Random-matrix theory says near-degeneracies are SUPPRESSED (level repulsion,")
    print("  beta = 1: P(spacing s) ~ s for small s). So sphericity is measure zero.\n")
    rng = np.random.default_rng(20260729)
    N = 400_000
    # GOE: symmetric with iid N(0,1) off-diagonals scaled, N(0,2) diagonal
    A = rng.normal(size=(N, 3, 3))
    H = (A + np.transpose(A, (0, 2, 1))) / math.sqrt(2)
    ev = np.linalg.eigvalsh(H)                     # ascending
    l1, l2, l3 = ev[:, 2], ev[:, 1], ev[:, 0]      # l1 >= l2 >= l3
    # ellipticity / prolateness style measures
    spread = (l1 - l3) / (np.abs(l1) + np.abs(l2) + np.abs(l3) + 1e-300)
    print(f"  {N:,} random deformation tensors:")
    for tol in (0.30, 0.10, 0.03, 0.01):
        frac = float(np.mean((np.abs(l1 - l2) < tol * np.abs(l1)) &
                             (np.abs(l2 - l3) < tol * np.abs(l2))))
        print(f"    fraction with all three eigenvalues equal to within {tol*100:>4.0f}% : {frac:.6f}")
    frac30 = float(np.mean((np.abs(l1 - l2) < 0.30*np.abs(l1)) &
                           (np.abs(l2 - l3) < 0.30*np.abs(l2))))
    check(frac30 < 0.05,
          f"even allowing 30% tolerance, only {100*frac30:.2f}% of draws are near-spherical")
    print(f"\n  mean normalised eigenvalue spread (l1-l3)/sum|l| = {spread.mean():.4f}")
    print("  So a TYPICAL patch is strongly triaxial. The collapse then proceeds along the")
    print("  largest-eigenvalue axis FIRST -- Zel'dovich pancakes -- then filaments, then halos.")
    print("  ANISOTROPY IS THE GENERIC CASE. Isotropy would be the thing needing explanation.")
    # also show the ordering statistics: how often is collapse effectively 1-D first
    dom = float(np.mean((l1 - l2) > (l2 - l3)))
    print(f"  fraction where the top gap exceeds the bottom gap (1-D collapse dominates): {dom:.3f}")

    banner("PART 2. THE FRAMEWORK DOOR: radial infall SPLITS the off-circular closure")
    print("  The repo's own open item: on a CIRCULAR orbit |a| is constant, so every time-weighting")
    print("  of |a|^2 in the first-moment closure gives the SAME answer -- circles are DEGENERATE")
    print("  and cannot distinguish closures (mi_offcircular_completion_SPEC.py: FREE, bounded).")
    print("  Anisotropic collapse is RADIAL INFALL: |a| varies enormously along the trajectory, so")
    print("  the closures separate. Quantify it on a clean radial infall from rest.\n")
    # radial infall from rest at r0 onto point mass M; energy: v^2 = 2GM(1/r - 1/r0)
    M = 1e12 * MSUN
    for r0_kpc in (300.0, 100.0, 30.0):
        r0 = r0_kpc * KPC
        # sample the trajectory in r from r0 down to r0/100, weight by dt = dr/v
        r = np.linspace(r0 * 0.999, r0 / 100.0, 20000)
        v = np.sqrt(np.maximum(2 * G * M * (1.0 / r - 1.0 / r0), 1e-30))
        a = G * M / r**2
        dt = np.abs(np.gradient(r)) / v
        T = dt.sum()
        # closure A: time-average of |a|^2 (the "rms" weighting)
        a2_mean = float((a**2 * dt).sum() / T)
        yA = math.sqrt(a2_mean) / A0
        # closure B: time-average of |a| then square (the "mean" weighting)
        a_mean = float((a * dt).sum() / T)
        yB = a_mean / A0
        # closure C: instantaneous at the start (quasi-static reading)
        yC = (G * M / r0**2) / A0
        nA, nB, nC = nu(yA), nu(yB), nu(yC)
        spread_pct = 100 * (max(nA, nB, nC) - min(nA, nB, nC)) / min(nA, nB, nC)
        print(f"  infall from {r0_kpc:>5.0f} kpc onto 1e12 Msun:")
        print(f"    closure A  <|a|^2>^1/2 : y = {yA:8.3f}  nu = {nA:.4f}")
        print(f"    closure B  <|a|>       : y = {yB:8.3f}  nu = {nB:.4f}")
        print(f"    closure C  instantaneous at r0 : y = {yC:8.3f}  nu = {nC:.4f}")
        print(f"    -> closure SPREAD in nu = {spread_pct:.1f}%")
    # do it once more for the record and check the spread is non-trivial
    r0 = 300.0 * KPC
    r = np.linspace(r0 * 0.999, r0 / 100.0, 20000)
    v = np.sqrt(np.maximum(2 * G * M * (1.0 / r - 1.0 / r0), 1e-30))
    a = G * M / r**2
    dt = np.abs(np.gradient(r)) / v
    T = dt.sum()
    yA = math.sqrt(float((a**2 * dt).sum() / T)) / A0
    yC = (G * M / r0**2) / A0
    spread = 100 * abs(nu(yA) - nu(yC)) / min(nu(yA), nu(yC))
    check(spread > 5.0,
          f"radial infall splits the closures by {spread:.0f}% in nu -- circles give 0% by construction")
    print(f"\n  CONTRAST: on a circular orbit all three closures agree EXACTLY (|a| constant), so")
    print(f"  the spread is 0% by construction. Radial infall gives {spread:.0f}%. That is the")
    print(f"  measurement that could fix the closure -- and it only exists in anisotropic collapse.")

    banner("PART 3. IS THIS A NOVEL DOOR?  Assessed honestly")
    print("  WHAT IS NOT NOVEL:")
    print("   * WHY collapse is anisotropic: Doroshkevich 1970 + Zel'dovich 1970, textbook. The")
    print("     random-matrix eigenvalue-repulsion framing is standard.")
    print("   * MOND structure formation and collapse: extensively simulated -- Llinares, Angus,")
    print("     Katz N-body work, and Nusser 2002 on MOND peculiar velocities. Anisotropic MOND")
    print("     collapse is NOT unexplored territory in general.")
    print()
    print("  WHAT IS GENUINELY UNTRIED, and it is narrow but real:")
    print("   * All that prior work is modified-GRAVITY (AQUAL/QUMOND-type). THIS framework is")
    print("     modified-INERTIA with a specific kernel K(Box_u/a0^2) whose off-circular closure is")
    print("     an OPEN, DOCUMENTED, BOUNDED choice. Nobody has computed that closure in a")
    print("     collapse geometry, because the framework's own linear cosmology is unbuilt.")
    print(f"   * And it is DECIDABLE rather than open-ended: radial infall separates the closures")
    print(f"     by ~{spread:.0f}% in nu, so a collapse calculation either fixes the closure or")
    print("     brackets it -- the same both-ways discipline the DC/AC branch got.")
    print("   * Concretely computable next step: a spherical-vs-triaxial collapse with the")
    print("     first-moment family evaluated along the actual worldline, both a0 footings, and")
    print("     the closure spread reported. No new physics needed -- just the calculation.")
    print()
    print("  WHAT IT WOULD AND WOULD NOT BUY:")
    print("   * WOULD: close (or bracket) the last documented O(1) freedom in the matter-sector")
    print("     closure, which currently makes every non-circular prediction quasi-linear rather")
    print("     than sharp. That is real internal progress and it is prerequisite to the MI linear")
    print("     cosmology the bulk-flow work needs.")
    print("   * WOULD NOT: explain anisotropy or spin (Part 1 -- statistics, in the Newtonian")
    print("     regime at high z), derive a0 or Z, or produce a new observable by itself.")
    print("  So: a real door, MODEST novelty -- new for this framework, not new to physics.")

    banner("VERDICT")
    print("  WHY local conditions are anisotropic: because the deformation tensor is a random")
    print("  symmetric matrix and eigenvalue repulsion makes three-fold degeneracy MEASURE ZERO.")
    print(f"  Even at 30% tolerance only {100*frac30:.2f}% of random patches are near-spherical.")
    print("  Anisotropy is the generic draw; isotropy would need explaining. Classical result.")
    print("  THE ONE NOVEL-FOR-THIS-FRAMEWORK DOOR: anisotropic collapse is radial infall, which")
    print(f"  SPLITS the off-circular closure by ~{spread:.0f}% in nu where circles give exactly 0%.")
    print("  That makes the framework's last documented O(1) freedom DECIDABLE by calculation.")
    print("  Modest, bounded, prerequisite to the unbuilt linear cosmology -- and honestly labelled")
    print("  as new to the framework rather than new to the field.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
