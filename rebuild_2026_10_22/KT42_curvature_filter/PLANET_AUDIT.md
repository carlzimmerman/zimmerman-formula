# Independent audit of the KT42 planetary monopole

**Primary verdict: computationally verified only in the stated range.** The
enclosed-source and Gaussian-vector reductions have the correct sign, radial
measure and 4pi normalization. The full B return is present. The first-order
secular orbit formula matches AZ12. No blocking mathematical or implementation
defect remains after the separately recorded additional controls.

Reviewer: `/root/audit_dynamic_options`, separate from the planetary
implementer, 2026-11-04. This is an independent reconstruction and source/result
review, not a fresh numerical field or orbit calculation. Current manifest
validation remains the root's task. The reviewed artifacts and exact hashes
are in `PLANET_AUDIT_INPUTS.json`. This new audit leaves the already pinned
`FINAL_AUDIT.md` unchanged.

## Claim, source and retained conventions

The tested law is exactly KT42, with unfiltered g and Gaussian-filtered H,
p=9/8 and ell3kpc. The finite population is four physical widths
.0001,.001,.1,.3kpc, Mars/Saturn, and two original acceleration footings:
16 rows. The point-Sun exterior convention and uniform auxiliary external
gradient with H_ext=0 remain as in the Solar calculation.

AZ11/AZ12 supply the supplementary comparison definitions and orbital
averaging formula, not a replacement source model. The code correctly keeps
KT42's GM=1.3274648756e20 SI and eta=GEXT/a0, with GEXT=2.32e-10 SI. It does
not silently import AZ12's GM=1.32712440018e20 or its converted external field.
Both GM values are explicitly recorded. The four widths, footings and cuts
are not adjusted to improve a result.

The actual archived cuts are read from RQ3's `tolerances.json`:

| Planet | Semimajor axis [AU] | Eccentricity | EPM [mas/year] | INPOP [mas/year] | dg_tight [m/s^2] |
|---|---:|---:|---:|---:|---:|
| Mars | 1.524 | .093 | .00037 | .0015 | 1.4e-15 |
| Saturn | 9.58 | .054 | .0047 | .0065 | 7e-15 |

The radial diagnostic uses sigma_g=dg_tight max(EPM,INPOP)/min(EPM,INPOP).
The secular-rate diagnostic uses sigma_rate=max(EPM,INPOP). The unchanged
line is absolute predicted value divided by the respective summary <=2.
These are archived supplementary-error comparisons, not a fresh observational
data extraction or a fitted ephemeris likelihood.

## Enclosed-source derivation

In rM/a0 units the B source is S_B=-partial_i partial_j(T_alpha B_ij).
The mean radial potential derivative is inward-positive, so Gauss' identity
gives

    g_B(R)=(1/(4 pi R^2)) integral_(|x|<R) S_B(x) d^3x.

Let W_R=T_alpha 1_(|x|<R). Self-adjointness and two integrations by parts give

    g_B(R)=-(1/(4 pi R^2)) integral B_ij(y) partial_i partial_j W_R(y) d^3y.

The minus sign survives: two integrations move the derivatives with positive
sign, while the original source already has a minus. W_R is radial. Since
B=D[h_t I+(h_r-h_t)nn], its contraction is
D[h_r W_R''+2h_t W_R'/r]. Azimuth contributes2pi; the remaining angular
integral is d0(r)=integral_-1^1 D dmu. Therefore

    g_B(R)=-(1/(2R^2)) integral_0^infinity r^3 d0(r)
                         [h_r W_R''+2h_t W_R'/r] dlogr.

This exactly matches the proposed formula. There is no missing G or a0 in
these dimensionless variables; the final physical acceleration is multiplied
by a0 once. The factor4pi here comes from the Laplacian Green/Gauss identity,
not from a second matter-density normalization.

The source need not be spherical. The rotational average defining its
monopole commutes with the isotropic filter and derivatives. It gives the
equivariant tensor with radial eigenvalues b_r=d0 h_r/2 and b_t=d0 h_t/2.
The derivation does not replace the entire axisymmetric force by a spherical
one; it extracts only the specified monopole observable.

## Independent vector reduction and finite-R Gaussian-ball check

For that radial tensor, (div B)_r=b_r'+2(b_r-b_t)/r. Its radial vector
convolution uses

    integral_-1^1 mu exp(z mu) dmu = 2 i1(z),
    i1(z)=(z cosh z-sinh z)/z^2,
    C_alpha=4pi/(2pi alpha^2)^(3/2).

Starting with -T_alpha div B and integrating the b_r' term by parts cancels
the explicit 2b_r/r contribution. The result is

    g_B(R)=(C_alpha/2) integral d0 exp[-(R^2+r^2)/(2alpha^2)]
      {h_r[-r^4 i1/alpha^2+r^3 R i1'/alpha^2]
                    +2r^2 h_t i1} dlogr.

`Monopole.B` implements this with C_alpha/2=sqrt(2/pi)/(2alpha^3). It is a
second reduction of the same exact monopole, with no numerical differentiation
of the physical B field. At fixed alpha>0 the origin boundary term vanishes
because B=O(r^2), and the outer convolution is Gaussian damped.

For the independently evaluated ball pairing, differentiate the Gaussian
under the observation-ball integral. Its Hessian is

    partial_i partial_j G_alpha(x-y)
      =G_alpha[(x_i-y_i)(x_j-y_j)/alpha^4-delta_ij/alpha^2].

Integrating azimuth gives the coefficient R^3/(sqrt(2pi)alpha^5) in both
W derivatives. The radial factor is (u-epsilon v xi)^2-1. The tangential
factor is epsilon^2 v^2(1-xi^2)/2-1: the one-half comes from the azimuthal
average of a single transverse Cartesian square. These agree with
`B_ball`, including its final prefactor -R/(2sqrt(2pi)alpha^5).

Taking epsilon=R/alpha to zero yields

    g_B(R)=-R/(3sqrt(2pi)alpha^5) integral r^3 d0 exp[-r^2/(2alpha^2)]
                    [h_r(r^2/alpha^2-1)-2h_t] dlogr + O(R^3).

The main calculation uses the finite-R expression; `B_linear` is only a
reported comparison. Neither the orbit computation nor the score substitutes
this small-R approximation. The recorded maximum absolute difference from
the linear B approximation is8.04e-12 in acceleration/a0.

The Gaussian-ball and vector routes share the primitive, smoothed point
Hessian and radial grid; their agreement independently tests the observable
kernel and prefactors, not every upstream ingredient. Their maximum recorded
relative discrepancy is5.52e-16. Those upstream quantities also have the
separate Solar action and Cartesian-Hessian controls already reviewed.

## Secular rate and force sign

For inward-positive A(r), the usual outward radial perturbation is -A.
The radial Gauss equation therefore has positive coefficient multiplying
A cos(f). With eccentric anomaly E,

    cos(f)=(cos E-e)/(1-e cos E),
    dt=(1-e cos E)dE/n.

Time averaging cancels these factors and gives

    <omega_dot>=sqrt(1-e^2)/(n a e)
       integral_0^(2pi) A(a[1-e cos E])(cos E-e) dE/(2pi).

This is exactly `rate` and the archived AZ12 definition. It is an exact
quadrature of the **first-order perturbative rate on a Kepler orbit**, not
an exact nonlinear planetary solution. a here is semimajor axis, distinct
from the filter width. Both A and returned B are evaluated at every sampled
orbital radius before averaging. YEAR/MAS performs the correct seconds-to-year
and radians-to-milliarcseconds conversion.

The constant inward force oracle is negative (retrograde),
-A sqrt(1-e^2)/(n a). In units a=n=1, the harmonic oracle is
-1.5sqrt(1-e^2), and the inverse-square oracle is zero. The latter correctly
distinguishes a change in central GM from a precessing radial anomaly.
All six recorded oracle errors are below7.73e-14.

## Controls identified during review and resolved separately

The original98-check run completed before this reviewer raised three
control/reporting issues. Its scientific code and result were preserved.
`control_amendment.md`, `controls.py` and the separate prospectively contracted
`controls_001` resolve them:

1. The original `Newtonian_zero` passed a literal zero force to the orbital
   integrator. That was only an integrator control. The new test injects R=1
   through the shared primitive API, builds a new Monopole under that null,
   and executes actual A, returned B, Gaussian-ball B and orbital pathways.
   All32 recorded outputs across eight retained configurations are exactly
   zero. The primitive is restored in a finally block.
2. The original plain-QUMOND comparison removes the curvature response;
   it does not omit only the return filter. The new mutation evaluates
   -[b_r'+2(b_r-b_t)/R] with the same smoothed Hbar but no outer Gaussian.
   Three derivative steps agree; the maximum normalized last-step change is
   7.60e-11. The mutation differs strongly, reaching a discrepancy1.6843e6
   in acceleration/a0, while the correct returned B remains finite and small.
   This is evidence that the control discriminates the omitted-adjoint error,
   not an alternative physical prediction.
3. The original `max_i1_argument` is the semimajor-axis bound. The additional
   control multiplies by1+eccentricity to cover aphelion. The conservative
   maximum is .0117487654, below the declared .02. Six/eight i1-series terms
   agree to recorded floating precision at this larger bound.

All five supplementary controls pass. No physical input, width, cut or
acceptance tolerance was changed. The original98 checks and these five checks
serve different purposes and should retain their separate provenance.

## Finite outcome and interpretation

All16 tested rows fail both supplementary diagnostics. The full returned B
does not cancel the nearly constant A contribution:

| At filter width0.1pc | A/a0 | B/a0 | Secular rate [mas/year] | Rate/error |
|---|---:|---:|---:|---:|
| Canonical Mars | .999999983 | -.0000229785 | -25.13977 | 16759.85 |
| Canonical Saturn | 1.000028476 | -.000144445 | -63.20661 | 9724.09 |
| Alternate Mars | .999999974 | -.0000234480 | -30.38160 | 20254.40 |
| Alternate Saturn | 1.000026790 | -.000147397 | -76.38500 | 11751.54 |

At1pc, the largest tested opposing B term is approximately-.0139183a0
(canonical Saturn); the corresponding rate/error remains9522.28. The
largest source/grid/domain refinement change is4.56e-12 in the radial
diagnostic ratio and3.18e-10 in the orbit diagnostic ratio. These are observed
finite convergence results, not rigorous interval bounds.

The mechanism is consistent with the equations: at fixed positive filter
width the raw point-source gradient eventually dominates the finite filtered
curvature, so the simple interpolation leaves A approaching a0 inward. The
returned B force is smooth and odd and therefore begins linearly in R. It
cannot cancel a nonzero constant in the strict origin limit. The actual
planetary failures above rely on the finite-radius calculation, not that limit
alone. No claim that every arbitrarily small positive filter width fails at
fixed planetary radius follows: the a->0 and R->0 limits are nonuniform.

**These ratios are not N-sigma statistical exclusions.** The archived
`prep_2026/planetary_doors/BOUNDS.md` itself warns against interpreting
un-refitted supplementary residual summaries as a complete theory likelihood.
The present test uses the inherited conditional monopole screen. Higher
multipoles, orbit orientation, covariance, fitted initial conditions and
simultaneous parameter refits remain outside it. Passing Q2 was already
insufficient to clear this separate radial observable.

## Final obligation status

| Obligation | Status |
|---|---|
| Enclosed-source B sign and 4pi/2pi factors | passed analytically |
| Vector-convolution B kernel and Gaussian-ball Hessian | passed analytically; finite cross-check passed |
| Full returned B in the force and orbit integral | present and independently discriminated |
| AZ12 rate, units and three force-shape oracles | passed |
| Correct actual orbital series domain | corrected in separate control record |
| Real model-level Newtonian null | passed in separate control record |
| Every tested width/planet/footing score | fails the declared supplementary screens |
| All widths or a complete refitted ephemeris likelihood | not established |

No blocking defect remains for the stated16-row diagnostic. The review did
not modify production inputs/results or the pinned earlier final audit. Local
mathematical proofreading checked signs, dimensions, radial measures and
scope distinctions. Root's fresh manifest verification and phase synthesis
remain separate from this review.
