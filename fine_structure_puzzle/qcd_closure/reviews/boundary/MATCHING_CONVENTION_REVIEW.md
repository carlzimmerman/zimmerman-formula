# Review of the common-regulator bulk/collar convention match

2026-10-19 UTC. This is a separate follow-up review. The original
`RAW_INDEPENDENT_FSP005.md` and `REVIEW_FSP005.md` remain frozen.

## Claim and verdict

The target compares h=v-a/r and B=n_mag rhat/r^2 against h=v, B=0 at fixed
v=pi/L, on the same relative wall, with a smooth fixed interior cutoff and
the common four-dimensional PV prescription. It claims the inverse-R
coefficient of the specified local charged bulk-plus-outer-collar functionals
is

\[
C_{\Gamma,\mathrm{local}}={L\over\pi}
\left[{11\log2\over3}(a^2+n_{\rm mag}^2)
+{7a^2\over6}-{a^4\over3}\right],
\qquad C_{\log\mathrm{weight},\mathrm{local}}=-C_{\Gamma,\mathrm{local}}.
\]

**Primary verdict: conditional on the named local-expansion input.** All
displayed coefficients, the convention conversion, the center sum, and
the two consistently matched local sums pass this independent check.
The conditions are the stated local gapped derivative expansion and
boundary inventory, the declared magnetic finite subtraction, fixed
asymptotic-v comparison path, and zero additional finite boundary matching
functions. No discrepancy requiring a target correction was found.

The decisive convention result is

\[
\Gamma_{\rm bulk,diag}-\Gamma_{\rm bulk,IBP}
={1\over12\pi}\int_\partial\partial_{\rm out}F_0(h),
\quad
\Gamma_{\rm collar,diag}-\Gamma_{\rm collar,IBP}
=-{1\over12\pi}\int_\partial\partial_{\rm out}F_0(h).
\]

The frozen Duhamel collar belongs to the fully integrated-by-parts bulk.
Using it unchanged with diagonal bulk overcounts
`+La^2/(3*pi*R)` in Gamma at center holonomy. The new target removes exactly
that mismatch.

## Provenance and exact revisions

Before reading the new target, I recomputed the diagonal heat coefficients,
the Duhamel first variation, the common-PV surface term, and the combined
unsubtracted local coefficient. That packet is
`CONVENTION_RAW_BEFORE_MATCH_TARGET.md`, SHA256
`65cbe517a21eb11d3fd9a61a7c3e14740c97d11c91760e94ce5c89d2f3beabaf`.
The delegation supplied the suspected flux relation; its sign and
normalization were checked afresh rather than treated as proof.

Targets read subsequently:

| Artifact | SHA256 |
|---|---|
| `common_regulator_match/INDEPENDENT_RAW.md` | `512b40d6f3f517f240b841a2d6170e3b4641074668e21e9d5432b54dff927b13` |
| `common_regulator_match/CONTRACT.md` | `13c33f3fb6e2f187974d12fa1dafbd32c3ca9c04bec1bd9b867b381e607dc1f7` |

The pre-target packet retained the common constant geometric collar term
16 K1/315. The target is explicitly a profile-minus-constant-reference
comparison on the same wall; that term cancels. This cancellation is made
explicit below, and no such constant term is included in the reviewed
comparison coefficient.

Prior frozen review hashes, retained without modification:

- `RAW_INDEPENDENT_FSP005.md`:
  `c0ef2e2eec2924c02d9c7082bccb7da06eb457b4bd77f446ca4a0be7196a08e0`.
- `REVIEW_FSP005.md`:
  `529571e3cf5e5ea783478aba0eeb645ef2de972953c5b3d1542a008986534653`.

## Independent derivation of the representative

For V=mu^2 the free Brownian bridge gives

\[
K(x,x;t)=(4\pi t)^{-3/2}e^{-tV}
\left[1-{t^2\over6}\Delta V+{t^3\over12}(\partial V)^2+\cdots\right].
\]

Indeed its covariance is 2[min(s,s')-ss'/t]; the integrated quadratic
Taylor term is -t^2 Delta V/6 and half the double covariance of the
linear Taylor term is +t^3 (partial V)^2/12. The scalar orbital multiplicity
of the charged vector/ghost pair is two. Performing the minus proper-time
integral gives

\[
\mathcal L_{\rm diag,scalar}={\Delta V\over24\pi\mu}
-{(\partial V)^2\over96\pi\mu^3},
\quad
\mathcal L_{\rm IBP,scalar}={(\partial V)^2\over96\pi\mu^3},
\]

whose difference is Delta mu/(12*pi). This fixes the sign and factor of
the outward surface flux.

The exact first Duhamel variation around constant V has only its volume
insertion in the integrated bulk. In the mixed smeared heat coefficient
the flat first-normal-jet response is proportional to str chi=0. The
diagonal bulk, in contrast, has the linear Delta(delta V)/(24*pi*mu)
term. Its flux must be subtracted from the collar. Thus the old Duhamel
collar is the IBP collar. The surviving curved K*partial_in mu/mu term
belongs to a different heat order and cannot serve as this compensator.

With q_k=2*pi*k/L+h and mu_kj=sqrt(q_k^2+M_j^2), define

\[
F_0(h)=\sum_{k,j}c_j\mu_{kj}(h),\qquad
F_0''(h)=\sum_{k,j}c_j{M_j^2\over\mu_{kj}^3}.
\]

Inside the gapped chamber the physical second derivative is zero. Each
heavy term tends to L/pi by rescaling q/M and using the integral 2 of
(1+t^2)^(-3/2). Since the heavy coefficients sum to -1,
F0'' -> -L/pi. Reflection at center gives F0'(pi/L)=0, and hence

\[
F_0'(h)=1-{Lh\over\pi},\qquad
{1\over12\pi}\int_{S_R^2}\partial_{\rm out}F_0
={a\over3}F_0'(v-a/R)={La^2\over3\pi R}
\]

at v=pi/L. A fixed annular inner surface changes only the R-independent
piece. For a physical unregulated mode q/|q| is constant in the gapped
collar, so its flux has no inverse-R part; the finite tower contribution
is therefore invisible to a modewise M=0 calculation.

## Check of the combined local terms

Write

\[
K_1=\sum_{k,j}{c_j\over\mu_{kj}},\qquad
K_3=\sum_{k,j}{c_jM_j^2\over\mu_{kj}^3}\longrightarrow-{L\over\pi}.
\]

The two orbital traces give q^2/(24*pi*mu^3) to E^2 in the IBP
representative and 1/(24*pi*mu) to B^2. The latter follows from the
spatial connection-curvature coefficient. The Lorentz spin trace gives
-1/(2*pi*mu) to each of E^2 and B^2. Consequently

\[
\mathcal L_{\rm IBP,2der}
=-{11K_1+K_3\over24\pi}E^2
-{11K_1\over24\pi}B^2.
\]

For E=a/r^2 and B=n_mag/r^2, the inverse-R term of the interior radial
integral is the negative of the exterior tail. This gives

\[
C_{\rm bulk,IBP}={11\over6}(a^2+n_{\rm mag}^2)K_1
-{La^2\over6\pi},
\quad
C_{\rm bulk,diag}={11\over6}(a^2+n_{\rm mag}^2)K_1
+{La^2\over6\pi}.
\]

The difference is the positive surface flux already derived. These signs
also follow directly from the diagonal scalar density before any IBP.

The frozen collar's lower term -8R mu_b/3 yields
-4a^2 K3/3 -> +4La^2/(3*pi). The combined logarithm and curved first jet
are odd in q at center and cancel under k -> -k-1 at every finite common
PV mass. Subtracting the diagonal compensator leaves

\[
C_{\rm collar,IBP}={4La^2\over3\pi},\qquad
C_{\rm collar,diag}={La^2\over\pi}.
\]

These are profile-minus-reference coefficients. The common geometric
term +16 K1/(315R), including its pure cubic wall counterterm, is the
same on the two profiles to this order: shifting the wall mass by O(1/R)
changes that term only at O(R^-2). It cancels rather than contributing
16 K1/315 to this comparison.

For the GPY potential W=-sum c_j mu_kj^3/(3*pi), the exact fourth
derivative of mu^3 is 9 M^4/mu^5. Its real-line integral is 12, so each
heavy Matsubara sum tends to 6L/pi. Using the heavy coefficient sum -1
gives W''''=2L/pi^2. The center symmetry kills its cubic Taylor term.
The quartic tail is La^4/(12*pi^2*r^4), whose interior integral supplies

\[
C_{\rm potential}=-{La^4\over3\pi}.
\]

Thus either matched pair gives, before assigning the magnetic finite part,

\[
C_{\Gamma,\mathrm{local}}={11\over6}(a^2+n_{\rm mag}^2)K_1^H
+{L\over\pi}\left({7a^2\over6}-{a^4\over3}\right).
\]

The target declares K1^H=2L log(2)/pi. Its stated half-integer harmonic
comparison gives precisely that value: one dimensionless tail difference
is 2 log(2), the two tails give 4 log(2), and multiplication by L/(2*pi)
gives K1^H. This is a specified finite scheme, rather than a universal
absolute value obtained merely by removing the regulator.

For a=n_mag=1 the result is

\[
C_{\Gamma,\mathrm{local}}={L\over\pi}
\left({22\log2\over3}+{5\over6}\right).
\]

The sign in the logweight is opposite. A common finite coupling change
delta_kappa shifts C by -4*pi*delta_kappa*(a^2+n_mag^2), as stated in the
target. The separately displayed classical tail has the correct negative
interior-tail sign with its stipulated trace convention; it is not part
of this one-loop coefficient.

## Obligation matrix and scope

| Obligation | Result |
|---|---|
| Diagonal heat coefficients and scalar multiplicity | passed by bridge expansion and proper-time integration |
| Duhamel collar's actual bulk convention | passed: fully IBP bulk |
| Outward flux sign and factor | passed: bulk +La^2/(3*pi*R), diagonal collar its negative |
| Common-PV nondecoupling | passed for the local coefficient sums |
| Electric a^2 term | passed in both matched representatives |
| Magnetic n_mag^2 term | passed in the declared harmonic finite scheme |
| GPY a^4 term | passed by the fourth derivative and common-PV Riemann sum |
| Center odd sum | passed exactly at finite common PV masses |
| Boundary PV mass term | passed; +4La^2/(3*pi) in the IBP collar |
| Same-wall geometric reference cancellation | passed at inverse-R order |
| Additional finite boundary data | conditional: fixed to zero for this benchmark |
| Uniform full-trace remainder, core and global spectrum | not addressed |
| Physical monopole determinant, stress and alpha | out of scope |

The target correctly retains the finite-wall matching limitation. For
example integral_boundary K w(h) shifts the center comparison by
4*pi*a^2*w''(v)/R, while integral_boundary z(h)*partial_out h shifts it
by -4*pi*a^2*z'(v)/R, in addition to lower powers. Pure geometric wall
cancellation does not fix those background-dependent data. The fixed-v
comparison path is also essential; fixing the wall value instead changes
the entire bulk profile and mixes lower radial powers into the expansion.

The formal local coefficient is verified. Promotion to the full regulated
determinant still requires a regulator-uniform remainder, the specified
smooth complete operator/core, neutral and angular matching, and physical
boundary data. Neither a physical stress nor electromagnetic normalization
has been derived here.

No numerical computation or run was needed or used. This review uses
analytic heat, Duhamel, spin/orbital, and Riemann-sum calculations. Target
content hashes were recorded, and final mathematical proofreading covered
this new file only; no prior mathematical tokens were changed.
