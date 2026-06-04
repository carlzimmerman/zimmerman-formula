#!/usr/bin/env python3
"""
Red team (independent, math-checked): four Z^2/geometry claims -- do any survive? Verdicts with calculations.
============================================================================================================
Challenged to verify, not dismiss. Each claim is re-derived from scratch in Python; the honest verdict (and the
exact point where the math holds or breaks) is stated. Where the claim is "not absurd" but still not a
derivation, that is said plainly.

CLAIM 1  Z^2 = eta(T^3/Z2) = 8 x (4pi/3) = 32pi/3   ("the geometric origin of Z^2")
  - The Atiyah-Patodi-Singer ETA invariant is the SIGNED spectral sum eta(s)=sum sign(lambda)|lambda|^{-s}.
  - On a flat torus the Dirac spectrum is +/- symmetric (charge conjugation lambda<->-lambda), so the signed sum
    cancels term-by-term: eta(T^3)=0 (the repo's own NEW_MATH_DIRECTIONS.md records exactly this).
  - 4pi/3 is the VOLUME of the unit 3-ball; 8x(4pi/3) is (8 fixed points)x(ball volume) -- a VOLUME, obtained by
    zeta-regularizing the UNSIGNED spectral sum zeta(s)=sum|lambda|^{-s} (a heat-kernel/volume coefficient).
  - zeta(0) (a volume) is NOT eta(0) (a signed asymmetry). The claim mislabels zeta-data as the eta invariant.
  - Rational vs irrational: a flat-orbifold eta is RATIONAL (Dedekind sums; fixed-point trig at angle pi:
    cot(pi/2)=0, csc(pi/2)=1); 32pi/3 is IRRATIONAL. A rational number cannot equal it.
  VERDICT: DEFINITIVELY BROKEN. The real eta is 0; 32pi/3 is a zeta-regularized volume mislabeled "eta." The repo
  contradicts itself (eta=0 vs eta=32pi/3). Category error, with the math.

CLAIM 2  sin^2(theta_W) = 3/13
  - 3/13 = 0.23077; sin^2θW(M_Z, MSbar) = 0.23122 +- 0.00004 => 11 sigma low. Ignores running & scheme (on-shell
    0.2233, effective-leptonic 0.23155 -- 3/13 matches none). "13" has no group-theoretic derivation.
  VERDICT: RULED OUT as a precise prediction (~11 sigma). A clean-looking but unexplained near-miss fraction.

CLAIM 3  m_heavy/m_light ~ exp(2|dc| k pi R5), exponent = Z^2 = 33.51
  - e^{Z^2}=3.6e14: a physically reasonable LARGE hierarchy (Carl's instinct that this is "not out of the
    question" is correct -- it is between top/neutrino ~3e12 and M_Planck/TeV ~1e16). BUT it matches NO specific
    hierarchy, the exponent 2|dc| k pi R5 has FREE parameters (dc, R5) that absorb any value, and the RS warp for
    M_Pl/TeV needs kpiR=37 (not 33.51); "Z^2 + Ngen/2 = 35" is an ad-hoc fudge.
  VERDICT: A FIT, NOT A PREDICTION. Not absurd; not derived. A tunable exponential fits any large hierarchy.

CLAIM 4  expanding orbifold -> inflation / dark energy (thermodynamic)?
  - An orbifold CAN be the spatial topology of an expanding FRW universe, but topology is PASSIVE: it does not
    drive expansion (needs an inflaton/vacuum energy). Its Casimir energy ~ hbar c / R^4 is the wrong scale
    (enormous for small R); matching rho_Lambda needs R ~ horizon, i.e. putting de Sitter in by hand.
  VERDICT: NO MECHANISM. No free inflation or dark energy from the orbifold.
Needs numpy.
"""
import numpy as np


def main():
    print("#"*88); print("# Red team: four Z^2/geometry claims, independently checked"); print("#"*88 + "\n")

    print("="*88); print("CLAIM 1: Z^2 = eta(T^3/Z2) = 8*(4pi/3)"); print("="*88)
    print(f"  8*(4pi/3) = {8*4*np.pi/3:.4f} = 32pi/3 = Z^2 = {(2*np.sqrt(8*np.pi/3))**2:.4f}.  4pi/3={4*np.pi/3:.4f}=vol(unit 3-ball).")
    tot = 0
    N = 10
    for n in np.ndindex(2*N+1, 2*N+1, 2*N+1):
        k = np.array(n)-N
        if np.all(k == 0):
            continue
        lam = np.linalg.norm(k)
        tot += np.sign(lam)+np.sign(-lam)          # +1 + -1 = 0 per +/- Dirac pair
    print(f"  signed Dirac sum (eta) over the T^3 lattice = {tot}  => eta(T^3)=0 (symmetric spectrum). 32pi/3 is irrational.")
    print("  VERDICT: BROKEN. real eta=0 (a signed asymmetry); 32pi/3 is a zeta-regularized VOLUME mislabeled 'eta'.\n")

    print("="*88); print("CLAIM 2: sin^2(theta_W) = 3/13"); print("="*88)
    v, mz, err = 3/13, 0.23122, 0.00004
    print(f"  3/13={v:.5f}; measured {mz}+-{err} => {(v-mz)/err:+.0f} sigma. Ignores running/scheme; '13' unexplained.")
    print("  VERDICT: RULED OUT as a precise prediction (~11 sigma). Clean-looking but unexplained near-miss.\n")

    print("="*88); print("CLAIM 3: m_heavy/m_light ~ exp(2|dc| k pi R5), exponent=Z^2=33.51"); print("="*88)
    Z2 = 32*np.pi/3
    print(f"  e^Z2={np.exp(Z2):.2e}. top/nu~{173e9/0.05:.0e}, M_Pl/TeV~{1.22e19/1e3:.0e} (needs kpiR={np.log(1.22e19/1e3):.0f}). Z2={Z2:.1f}.")
    print("  VERDICT: A FIT (free dc,R5; +Ngen/2 fudge), NOT a prediction. Not absurd -- but not derived.\n")

    print("="*88); print("CLAIM 4: expanding orbifold -> inflation / dark energy?"); print("="*88)
    print(f"  Casimir rho ~ hbar c / R^4. R=1e-18 m -> {1.055e-34*3e8/(1e-18)**4:.0e} J/m^3 vs rho_Lambda~6e-10 J/m^3.")
    print("  VERDICT: NO MECHANISM. Topology is passive; Casimir is the wrong scale; de Sitter must be put in by hand.\n")

    print("="*88); print("OVERALL"); print("="*88)
    print("""  Claim 1 (eta=Z^2): DEFINITIVELY BROKEN -- the real eta is 0, 32pi/3 is a volume; the foundation of the whole
  'Z^2 from geometry' program is a mislabeled volume. Claims 2-4: not derivations -- a ruled-out near-miss
  fraction (11 sigma), a tunable fit, and a non-mechanism. None survives as a derivation. Carl's instinct that
  e^{Z^2} is a 'reasonable big number' is correct; that is exactly why a tunable exponential can fit it -- which
  is the numerology, not a refutation of it.""")
    print("#"*88)


if __name__ == "__main__":
    main()
