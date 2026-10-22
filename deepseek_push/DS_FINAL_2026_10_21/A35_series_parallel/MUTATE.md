# MUTATE — A35_series_parallel

## Mutation

`--mutate` changes exactly one thing: the medium element's constitutive law. It is made
**self-depleting** instead of an ideal reservoir — the element's admittance becomes its
remaining budget, `Y_m = a0 − λA` with `λ = 1` instead of `λ = 0`:

```python
LAM = 1.0 if MUTATE else 0.0      # 0 = ideal reservoir (n=1), 1 = fully depleted (n=2)
```

Every other thing is fixed: constants, the algebraic identities about *both* laws, the
variational functional, the noise model, the grid. `LAM` enters only through `resp_exact()`,
i.e. only where the lane *identifies* which element the medium is.

This is the mutation with teeth because the whole claim is "n − 1 *is* the depletion
fraction, and only `λ = 0` is stationary": if the checks survive a self-depleting element
then they are not testing the identification at all.

## Why it must break

With `λ = 1` the identified law becomes `A = g + a0/2 − sqrt(g²+a0²/4)`, so:

* K1 — `1/A = 1/g + 1/a0` fails by `0.118034` (dimensionless; the true n=2 value of
  `1/A − 1/g − 1/a0` at `g = a0`).
* K4 — the identified capacity is `a0/2`, not `a0`: measured `0.5`, threshold `1.0`.
* K9 — the identified law is no longer the argmin of `Ψ`, nor the Lagrange solution:
  deviation `0.118034`.
* K21 — the identified law's discriminator moves: skew flip at `0.3750 a0` (not `a0`) and
  the noise ratio becomes `34.4859` (not `22.3422`).

The 18 other checks are *law-level* statements that hold for both laws and for the whole
`λ`-family (the prompt's guess being `g_N`, the composition algebra, the n=2 residual
`2−√5`, `F'(θ₂)`, `σ(θ₂)`, the Nyquist ratio, homogeneity). They **should** survive, and they
do — a mutation that broke everything would mean the checks were not independent.

## Mutated output

```
K1 FAIL 0.1180339887498949 1e-15  # 1/A=1/g+1/a0 exact; A=harmonic sum of g and a0 (compliances add, i.e. series springs)
K2 PASS 0.0 1e-15  # sqrt(g^2+a0^2/4)-a0/2 == g_N exactly (not A); guess/A = phi = 1.618034 at g=a0
K3 PASS 0.0 1e-15  # 1/A = 1/g + 1/(a0-A): n=2 is a series string with a self-limiting (depleting) element
K4 FAIL 0.5 1.0  # capacity: lam=0 -> a0 (ideal reservoir); lam=1 -> a0/2 (response meets its own headroom); ratio 2
K5 PASS 0.0 1e-15  # both laws (and every lam) have gN = g^2/a0 + O(g^3): the deep limit measures a0, not the capacity
K6 PASS 0.0009999981285083066 0.002  # cubic coefficient = 1-lam: n=2 is the unique even member of the family (A2's evenness criterion)
K7 PASS -1.0 1e-15  # parallel admittances: A = g+a0, gN = -a0 < 0 (anti-gravitating) and no finite capacity -- excluded
K8 PASS 0.0 1e-15  # both wirings reproduce the SAME law (parallel: N gates c=a0/N,s=a0; series: c=a0,s=a0/N); composite capacity Nc or c, never a0/2
K9 FAIL 0.1180339887498949 1e-15  # argmin_A [A^2/2a0 + (g-A)^2/2g] = a0 g/(g+a0); Lagrange over two displacements DERIVES theta_A = theta_N = g/(g+a0) (common occupancy is an output, not an assumption)
K10 PASS -0.2360679774997897 0.001  # n=2 residual R = A/g+A/a0-1 != 0 everywhere; R(a0) = 2-sqrt5; excess Psi(a0) = (9-4sqrt5)a0/4 > 0
K11 PASS 1.0 1e-15  # A_n2 is not Langmuir(C) for any C (g^2 forces C=a0, g^3 then is -1/a0 != 0)
K12 PASS 1.1743590056195488 0.0  # F'(theta_1)=0 identically; F'(theta_2)=kT ln2phi = 1.174359 at g=a0 and -> kT ln4; theta_2>theta_1 always
K13 PASS 0.6199018949890067 0.0  # sigma(theta_1)=0 (detailed balance); sigma(theta_2)>0 for all g, = 0.619902 a0 k_a at g=a0
K14 PASS 9.47213595499958 1e-06  # K cancels: g = a0 u/(a0-u); Z1(a0)=4, Z2(a0)=5+2sqrt5=9.472136
K15 PASS 0.0006671281903963042 0.001  # tau=L/c=3.262e4 yr (10 kpc); omega*tau=6.671e-04, phase 0.0382 deg: the RAR is a dc measurement
K16 PASS 22.342179120754853 0.01  # sigma(log g) ratios 0.3a0/3a0: n1=22.3422 n2=34.4859; a0/10a0: 22.9984/30.3822; slope -1.4998
K17 PASS 0.375 0.375  # skew flips at g=a0 (n1) and g=3a0/8 (n2); at g=a0/2 skews are +0.7071 / -0.3483 (opposite)
K18 PASS 2.368033988749895 1e-05  # Nyquist S2/S1 = (5+2sqrt5)/4 = 2.368034 at g=a0; S2 diverges at g=a0/2, S1 -> 4 only
K19 PASS 0.0 1e-15  # both laws homogeneous degree 1: a0 is the only dimensionful input
K20 PASS 8.0 8.0  # same law, both wirings; Var(A) ratio series/parallel = N = 8 (one collective coordinate vs N independent)
K21 FAIL 0.3750075401257972 1.0  # identified law: skew flip at g = 0.3750 a0, noise ratio 34.4859 (n=1 values)
K22 PASS 2.0 0.0  # A(0)=0, A(a0->0)=0, A'(0)=1 for BOTH laws: requirement (i) is degenerate, it cannot select n
A35 COMPLETE: 18/22 checks PASS.
FAILED: K1,K4,K9,K21
```

Exit code 1. The four failures are precisely the checks that assert *which element the medium
is*; the 18 survivors are the law-level and class-level identities (including K22, the
degeneracy of the vanishing conditions, which holds for both laws).

## Second mutation considered and rejected as a declared flag

Halving `a0` globally (`A0 → A0/2`) breaks **nothing at all**: both laws are homogeneous of
degree 1 in `(g, a0)` (K19), so every dimensionless number in the lane — capacities, ratios,
residuals, skews, impedances — is `a0`-blind, and `a0` appears only inside the two absolute
numbers that are *defined* to be `a0`-scaled. That is a null mutation, so it is recorded here
rather than shipped as the flag. The `λ` mutation is the only one with teeth, because `λ`
is the one thing the lane claims to *identify*.
