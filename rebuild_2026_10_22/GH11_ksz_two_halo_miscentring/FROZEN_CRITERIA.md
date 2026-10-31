# GH11_ksz_two_halo_miscentring: FROZEN CRITERIA (committed alone, before the template or any fit exists)

**Not blind:** GH10's T(θ) has been seen. The choices below are fixed before any new number is computed.

**Questions.** On GH10's differential bin (CIGALE log M★ 10.5–11, published DR2 points):
- **Q1:** does miscentring remove the inner deficit?
- **Q2:** can a data-built two-halo shape explain the rise past 0.9 Mpc?
- **Q3 (verdict):** after both, could the remaining gas supply route E's budget?

## Data (nothing new fetched)

GH10's T_bin and C_bin; DR1 BGS `gh6_bgs.npz` as the neighbour field.

## Two-halo template (shape only; no power spectrum)

- **Lenses:** 20,000 random DR1 BGS galaxies in the bin at z 0.1–0.4, seed 1111. **Neighbours:** all DR1 BGS with |Δv| < 2000 km/s along the line of sight, velocities being coherent on those scales.
- Excluded inside R_hole = **1 Mpc proper** (their signal is one-halo or same-halo); variant 0.5 Mpc.
- Excess neighbour surface density in 0.1′ annuli to 22′, minus the same around positions displaced by 1°–2° (lens z kept).
- **Weights:** primary by number, T_n; variant by M★, T_m.
- Convolved with the k = 1 gas image + beam at the mean z, then the same CAP. b ≥ 0 is free.

## Miscentring

- **Primary:** satellite fraction f_s = 0.24, from nesting the paper's values (0.279 at > 10.5, 0.364 at > 11; provisional). Satellites get the same gas image, smeared by a 2D Gaussian offset, σ_off = 300 kpc proper.
- **Bracket:** f_s = 0.5, σ_off = 500 kpc, chosen as an extreme, not an estimate.
- Host gas is ignored; it would add signal.

## Fits

T = A m_k + b T_n, with m_k Zhang's gas per GH10 (mass offset on) with miscentring, for k = 1, 1.8, 3, 5, 8. Full C_bin; dof 11; b ≥ 0. Mass M_gas(k) = A × 1.84 M★ × (Zhang mass ratio k to 1) mixed over the same cells. The discrete k list is fixed here and is not a tuned parameter; no finer scan.

## Verdict

**Q1:** at k = 1.8, b free: A(1.8) with primary and bracket miscentring, graded BELOW if A + 2σ < 1 (adding the 10 % r systematic in quadrature).

**Q2:** TWO-HALO SHAPE SUFFICES if at k = 1.8 the fit has p > 0.01, b/σ_b ≥ 2 and Δχ² ≥ 4 against b = 0. Otherwise NOT SHOWN. This is a shape statement, since b is free.

**Q3:** need = M_need, Zhang's gas to 1.8 R_vir at the bin's mass (GH2's k* route, b free in the data fit).
- **BUDGET SUPPLIED:** some k has p > 0.01 and M_gas − 2σ ≥ M_need.
- **BUDGET EXCLUDED:** for every k with p > 0.01, M_gas + 2σ < M_need; or no k has p > 0.01.
- **BUDGET ALLOWED, NOT SHOWN:** otherwise.

Reported: all k with b = 0, T_m, R_hole 0.5, bracket; the mass at b = 0 at the largest k; A(k) with the inner θ ≤ 3′.

**Interpretation lock.**
- b absorbs extended gas as well as two-halo: extended gas and two-halo can be degenerate. A large b doesn't prove gas is absent, and b = 0 doesn't prove it's present.
- SUPPLIED means only that gas mass of that size fits this stack. It's not a lensing pass (GH2's best route E χ² 141 stands). EXCLUDED holds within the Zhang-shaped family only.
- The stop rule fires only on BUDGET EXCLUDED, and then only for extended gas of this family.
- Nothing here says the law wins.

## Checks

- **K1:** b = 0, f_s = 0, k = 1.8 reproduces GH10's A within 1e-3.
- **K2:** σ_off → 0 returns the unsmeared model within 1 %.
- **K3:** injected A = 0.5, b = template-scaled returns both within 1e-6.
- **K4:** the template built around random sky positions (rotated in RA by 5°) has CAP within 3σ of zero at every θ, jackknife over 10 lens subsets.
- **MUTATE:** T → −T flips the unconstrained A exactly.

**Scope.** κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework. Published points are not native (GH10). One thread, nice 15, RSS < 6 GB.
