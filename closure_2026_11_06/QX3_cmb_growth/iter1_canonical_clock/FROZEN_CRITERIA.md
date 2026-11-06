# QX3 iter1 frozen criteria: can AC2q's dark-energy clock supply the CMB-lensing potential?

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Rules: ../../SWARM_BRIEF.md.

## Mechanism

AC2q has no dust. Its only extra cosmological component is the canonical clock phi with X - V, sound speed c_s^2 = 1.
WG2 already graded the a0 law on the web from a baryons-only start, and it FAILS under every rule. The question here is
whether the clock's own perturbations can add the missing linear power.

## Claim graded (analytic, Lean-certified)

- C1: a fluid with c_s^2 = 1 has physical Jeans wavenumber k_J^2 = 4 pi G rho_phi / c^2. With rho_phi <= rho_tot and the
  Friedmann equation 8 pi G rho_tot = 3 H^2, this gives k_J <= sqrt(3/2) H/c, i.e. it clusters only on scales comparable to
  the Hubble radius or larger.
- C2: CMB lensing at L 8-400 probes comoving k = (L + 1/2)/chi. Report the smallest ratio k/(a H/c) over L in 8-400 and z in
  0.1-10, computed on a framework-native background (flat; Omega_m bracket {0.05, 0.3, 1} and H0 {65, 75}, as WG1).
  On sub-Jeans scales the clock's density contrast is suppressed by at most (k_J/k)^2 relative to the metric potential.

## Lines

- FAIL (no-go for the mechanism) if (k_J/k)^2 <= 0.05 at every graded (L, z, corner). The clock then adds at most 5 % to the
  potential on graded scales, far below the factor 3-14 (in power) that WG2 found missing.
- OPEN if the ratio exceeds 0.05 somewhere: the clock could matter there, and a full perturbation solve is owed.

## Controls

- Lean: C1's inequality with a _MUTATE twin claiming k_J^2 <= H^2/(10 c^2) for all rho_phi <= rho_tot, which must fail to build.
- Numeric MUTATE: set c_s^2 = 1e-6. The same ratio must then exceed 0.05 (the test sees a slow fluid when there is one).
