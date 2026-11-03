# KT6_lattice_cell: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: prove c_E = 1. κ = 1/2 FITTED. Footings never pooled, and none is used. Not theory closed. No cold component, no particle. **Not blind:** worked by hand knowing the target, and I expect the equation of state to fail.

## Mechanism
KT5's premise T m0^3 = rho c^2 read as counting: a classical real scalar on a cubic lattice, spacing a, one mode per cell, thermal at T, mass m = (1 - chi)/a.

Named inputs:
- **L1:** one real mode per cell a^3. A cube has no 4 pi/3, which is why this could remove the pi.
- **L2:** rho c^2 is the mean energy density U/V = T/a^3 (kinetic T/2 plus potential T/2).
- **L3:** unit coupling, m a = 1 - chi. This stays an assumption here.

## Checks
- **Q1, universality.** Near the vacuum, m a << 1, the continuum m^3 term can be used even though the lattice is not a continuum at m a = 1. Compute lattice G(m^2) = int_0^inf dtau exp(-m^2 tau) [exp(-2 tau) I0(2 tau)]^3 at a = 1. Confirm [G(0) - G(m^2)]/m -> 1/(4 pi) as m -> 0, to 1 percent at the smallest m used. If it holds, kappa depends only on the slope at the vacuum and c_E = 1 follows from L1 to L3.
- **Q2, selector.** Static-only ensemble gives T/2 per mode: c_E = 2, kappa 0.707. Is L2's full T forced? Answer from which energy gravity sources.
- **Q3, equation of state.** Dark energy needs w = -1, that is rho + p = 0. For N modes in volume V with cells created as V grows, p = -F/V, so rho + p = T S / V. For classical oscillators F per mode = T ln(hbar omega / T), so w = -F/U = ln(T/(hbar omega)). Sympy: state w, and its sign when KT5's H4, T >> hbar omega, holds.

## Labels
- **c_E = 1 PROVED** only if L1 to L3 follow from an equation with nothing assumed and Q3 gives w = -1. Then the second prediction is still owed.
- **COUNTING WORKS, EOS FAILS:** Q1 holds and w != -1 where the classical limit is valid.
- **NO:** Q1 fails.

MUTATE: replace [..]^3 by [..]^2 (2D lattice). Expected: the m coefficient isn't 1/(4 pi), since 2D goes logarithmic. `_MUTATE`, exit 1. Register row after. No download. Seconds.
