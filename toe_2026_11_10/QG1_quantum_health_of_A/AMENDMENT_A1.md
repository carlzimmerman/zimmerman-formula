# QG1 AMENDMENT A1 (POST HOC, after development runs, before the graded run)

Committed alone, after the criteria (9f78e93383) and after three development runs of `qg1.py` in the session scratchpad,
before the graded run in this folder. No threshold of FROZEN_CRITERIA.md changes and no criterion is loosened. Adopts
nothing. kappa = 1/2 FITTED; not theory closed.

**What the development runs were.** Run 1 crashed in KA1 before any number (sympy's `euler_equations` drops an identity
0 = 0, so taking `[0]` of the difference's equations raised IndexError; the check now compares the Euler-Lagrange
expressions of the two Lagrangians separately). Run 2 completed; its output is kept as `qg1_devrun_preA1.out`. Run 3
had the three changes below. Its labels are the ones the graded run is expected to reproduce. It is not graded.

## 1. Criterion (i)(a): eigenvalues computed in closed form (check-code defect)

Run 2 read (i)(a) FAIL on MINK (minimum eigenvalue -2.1e9 K canonical, -1.0e9 K alt). That is round-off. At k = 1e3 x the
band top, gamma_L k^2/K is about 1e50, and `mp.eigsy` at 40 digits cannot resolve eigenvalues of order K next to one of
order 1e50 K. H_P = K diag(1+u, 1+u, (1+u)^2) is positive definite and the stiffness adds a positive semi-definite rank-one
term, so no eigenvalue can be negative. The graded script uses closed forms. The eigenvalue along the axis orthogonal to
Pbar and khat is sW K (1+u), which the stiffness does not touch. The other two come from the 2x2 block, with
lambda_min = det/lambda_max. The criterion is unchanged.

## 2. Criterion (i)(b): the tensor correction is the anisotropic stress (check-code defect)

The frozen text asks for "the non-GR correction to [the tensor's] omega^2". Run 2 used the bound
K (|G| + W + n_d) L^2. That bound counts isotropic background energy (the dust charge, W). Isotropic energy does not
enter the transverse-traceless equation. Only anisotropic stress does, through 2K pi_T. A perfect fluid, such as the
clock's dust on FRW or ordinary matter in GR, gives no tensor mass term. With the wrong bound, run 2 read (i)(b) FAIL on
FRW1100 (0.0044) and FRW1 (8.1e-6 against 1e-6). The graded script computes 2K |pi_T| L^2 from the pieces of QX17 E4
that carry a free P_m: K W' P_m P_n/|P|, 2 P_(m d_n) l and -2 gamma_L P_(m curlyD_n). Their size is bounded by
|pi_T| <= (pbar/K)(K W'(pbar) + 2 g + 2 g_N); g_N stands in for gamma_L |grad Pi|, which it equals exactly at the
hedgehog. The bound is 0 on MINK and FRW (P = 0) and at most 1e-12 on the static rows. The 1e-6 threshold is unchanged.

## 3. The switch measure: a reported diagnostic is added; the graded definition is kept

For Pi_bar > 0 the frozen measure is c_cross = min(1, |dPi|/Pi_bar), multiplied by gamma_L k^2 m0/2. At large k this
treats a vacuum fluctuation much smaller than Pi_bar as if it reached the switch in proportion to |dPi|/Pi_bar. A Gaussian
vacuum fluctuation reaches it with a probability of order exp(-Pi_bar^2/(2 dPi^2)). The frozen measure is therefore very
conservative. In run 3 it sets Lambda_s on every charged row (about 1/(2e3 to 3e4 km) on PM and SUN), and it gives
Lambda_s x 1 mm = 4.8e-10 for the reported Earth-surface laboratory. The frozen ramp can only lower Lambda_s, so it can
never turn a FAIL into a PASS. **It stays the graded definition.**

Added, reported only and never graded: the same ratio with
c_cross^G = 2 E[(Pi_bar + X)^2 1{X < -Pi_bar}]/sigma^2, where X ~ N(0, sigma^2) and sigma = |dPi|. In closed form,
c_cross^G = 2[(1 + c^2) Phi(-c) - c phi(c)] with c = Pi_bar/sigma. It equals the frozen value 1 at Pi_bar = 0, so MINK
and FRW are unchanged, and it falls as exp(-c^2/2) when the fluctuation is far below the switch. Check C2: the closed
form agrees with direct quadrature to 1e-30 at c = 0, 0.5, 1, 3.

Run 3, as a disclosure only: no graded row changes label under c_cross^G. The reported Earth laboratory becomes
Lambda_s = 1/(19 um), Lambda_s x 1 mm = 52 / 51. RESULT.md quotes both measures there and says which one is graded.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
