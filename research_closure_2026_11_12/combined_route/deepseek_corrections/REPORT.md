# DeepSeek corrections and the mass-retention / external-field route

Date: 2026-11-12. Original-source snapshot: `2ffc012fa56dcdcbb4b3d5f169ba757fe482bcb8`.
Status: **the G238–G242 errors are corrected forward; the combined physical route remains conditional.**

The four live scripts now dispatch to corrected implementations in this directory.
Their original scripts, READMEs, `.out` files and JSON results are retained byte-for-byte
under `archive/`; `original_sources.json` records their hashes. Historical outputs in
the original lane directories were not overwritten. Each old README begins with an
unmistakable correction notice. No frozen empirical criterion has been rewritten.

## 1. Corrected claims and regression witnesses

`corrected_claims.py` passed 12 checks in `claims_run/`.

**G238 — density slope.** If `p = d ln M / d ln r`, then

```text
rho = M'/(4 pi r^2)
d ln rho / d ln r = p - 3 + d ln p / d ln r
d ln(mean enclosed density) / d ln r = p - 3.
```

The counterexample `M=C(r+b)` has local density slope exactly -2, while the old
proxy is `-2-b/(r+b)`. The omitted derivative matters. The replacement therefore
does not claim a local-density measurement or a density-slope falsifier from the
13 enclosed-mass points. It also corrects the old log-fit weights: approximate
`sigma_logM = sigma_M/M`, not `sigma_M`. The descriptive power-law mass fit is
`p = 0.911190`, with diagonal-only formal error `0.041889`, hence mean-enclosed-density
slope `-2.088810`. The covariance of the joint profile is unavailable; this is not
a calibrated detection or exclusion significance. A zero-density exterior of a
point mass has no defined local logarithmic density slope, despite the mean-density
proxy taking the value -3.

**G240 — external-field normalization and Green function.** Both theories now use
the simple pair `mu(x)=x/(1+x)`, `nu(y)=(1+sqrt(1+4/y))/2`, and the same point source.
For Newtonian external field `y_e=0.01273`, the physical field is
`x_e=(y_e+sqrt(y_e^2+4y_e))/2 = 0.11937169548748`.
The original solver interpreted its `eta` as a physical field; it had been given
the Newtonian number. The difference was not an AQUAL-versus-QUMOND effect.

Linearizing AQUAL about the physical external field gives

```text
mu_e (Delta + L_e partial_z^2) deltaPhi = 4 pi G rho
deltaPhi = -GM/[mu_e r sqrt(1+L_e sin(theta)^2)]
M_eff,infinity/Mb = atan(sqrt(L_e))/(mu_e sqrt(L_e)).
```

The correct solid-angle average includes `sin(theta)`. At physical fields 0.5
and 0.01273, the analytic monopoles are 2.515819 and 62.625294, agreeing with the
historical numerical plateaus 2.514 and approximately 62.5. The old 21.42
benchmark and the nonconvergence inference based on it are withdrawn.
At matched fields the analytic monopoles are AQUAL 7.512472 and QUMOND 7.902356.
QUMOND's flux integral supplies its monopole; it does not supply its full pointwise
curl-free acceleration field.

**G241 — completion inference.** The inverse constitutive identity is retained as
algebra. It does not derive general modified-inertia trajectories or their EFE.
Milgrom's 1994 source derives the algebraic relation for circular orbits in an
axisymmetric potential; its general action-based dynamics is nonlocal. Lensing
does not uniquely select AQUAL. The old function calling itself through another
name and the hard-coded `True` asserting a completion are removed from live code.
The lensing objection applies to a baryons-only GR metric with inertia-only changes;
it is not an exclusion of every relativistic modified-inertia extension.

**G242 — conditional radius ratio.** The assumed field model still gives
`R_set=sqrt(Mb/(rho_m R_struct))`, and the algebraic ratio condition opens for
growth `g > 1.649347`, because `0.608705*g^(-1/6) <= 0.56`.
Fixed mass fails. The model has not derived `R_set = R_EFE`, measured the relevant
assembly history, matched the two populations, or rerun the forest/KiDS likelihoods.
`R_struct` controls the absolute radius; its history also matters unless fixed.
A uniform mean cosmic density does not determine a vector external acceleration:
the density contrast, geometry, coherence scale and boundary conditions must be
specified. The no-free-parameter and proxy-artefact closure claims are withdrawn.

## 2. Matched-field finite-radius rerun

`corrected_aqual.py` used the pinned historical solver, a point baryonic mass
`Mb=6.681e10 Msun`, physical `x_e=0.11937169548748`, and separate canonical/alt
accelerations `9.36e-11` / `1.13e-10 m/s^2`. The 320x96 and 512x128 grids span
`1e-4 <= r/rM <= 1e4`; both completed in 20 iterations. The final iteration
criterion is about `9e-12`. On the fine grid, independently rebuilt nonlinear
scaled residual is `5.56e-10` and Gauss-flux error is at most `5.79e-4` over
`1 < r/rM < 100`. Interpolation, rather than nearest-grid-bin selection, is used.

| Fine-grid result | Canonical | Alt |
|---|---:|---:|
| M_eff(<80 kpc) / Msun | 4.486839e11 | 4.579205e11 |
| M_eff(<200 kpc) / Msun | 4.939944e11 | 4.954813e11 |
| Operational r200c / kpc | 166.8105 | 167.0609 |
| Operational M200c / Msun | 4.901428e11 | 4.923532e11 |

The maximum grid difference over sampled 20–300 kpc radii is **0.129%**. This is
a numerical-resolution check, not a full physical error budget. The old 1.33e12
rescue does not survive matched boundary fields. At the direct 80-kpc datum
6.36e11 with reported 0.50e11 error, the fixed-proxy pulls are approximately
-3.75 and -3.56; no baryonic or model systematic is included, so these are not
calibrated exclusions of an arbitrary completion.

The overdensity result solves `M_eff(<r)/(4 pi r^3/3)=200 rho_crit`, at H0=67.4,
self-consistently. It is an operational spherical-monopole effective mass,
not a conserved cold-rest-mass measurement. It is deliberately not compared to
the paper's NFW-extrapolated M200c as if that were a direct independent datum.
The supplied point-source approximation is not the full McMillan disk/bulge
model or a tracer Jeans likelihood.

## 3. The conditional capacity field and aperture

The combined route uses **cold excess** `Xc=Mc/Mb=59.5`, corresponding to total
enhancement `F_A=60.5` if the effective monopole is identified with total mass.
Solving the AQUAL plateau equation gives
`x_e=0.0131841657256641`, `y_e=0.000171560345850136`.
This is a chosen field realizing that capacity, not an independent prediction of
the environment. Define `R_E=rM/x_e=75.848561 rM` by field balance.

| Radius | Fine-grid M_eff/Mb | Effective cold excess / 59.5 |
|---|---:|---:|
| 0.5 R_E | 36.42814 | 0.59543 |
| R_E | 54.21017 | 0.89429 |
| 2 R_E | 58.96899 | 0.97427 |
| 3 R_E | 59.88506 | 0.98966 |
| 5 R_E | 60.29688 | 0.99659 |
| 10 R_E | 60.42446 | 0.99873 |

At the field-balance aperture the excess is **10.57% below** the asymptotic
capacity. The EFE produces a smooth profile, not a sharp boundary. A baryon/cold
retention comparison must use the same specified aperture.

Both capacity grids are monotonically increasing on the sampled domain
`1 <= r/rM <= 1000`; their maxima there are 60.41375 and 60.43482, below 60.5.
Small negative derivatives near the old zero outer-potential boundary are not
accepted as physical. Replacing that boundary with the anisotropic Green function
in `rmax=1e4` and `1e5` boxes gives positive derivatives through the sampled 30 R_E.
At 30 R_E the total enhancements are 60.46078 and 60.43143; the box difference is
about 0.05%. This is finite-domain evidence, not a proof of global monotonicity.
No converged spherical-average negative-density witness was found here.

## 4. Local source sign and a possible positive background

Independently differentiating the external-field potential gives, away from the
point source,

```text
rho_eff = Mb L_e [(3+L_e) cos(theta)^2 - (1+L_e)]
          / [4 pi mu_e r^3 (1+L_e sin(theta)^2)^(5/2)].
```

It is negative in an equatorial belt for every `L_e>0`, positive near the poles,
and has zero angular shell average at this asymptotic order. Thus the literal
identity `rho_cold = rho_eff >= 0` fails. This is a scoped obstruction to that
identity, not a universal no-go for field theories or signed density contrasts.
QX17's allowance for signed polarization is compatible with this result.

For `Xc=59.5`, H0=67.4, Omega_c=0.265 and z=0, the canonical equatorial
`abs(rho_eff)/(Omega_c rho_crit)` is:

| Mb / Msun | 2 R_E | 3 R_E | 5 R_E |
|---|---:|---:|---:|
| 1e9 | 10.1666 | 3.01233 | 0.65066 |
| 1e10 | 3.21497 | 0.95258 | 0.20576 |
| 1e11 | 1.01666 | 0.30123 | 0.06507 |

The maximal internal/external acceleration ratios are 0.2533, 0.1126, 0.04053
at these radii. Only the 5 R_E column is a clean approximately 4% far-field
perturbation. There, a uniform positive cosmic cold background is large enough
to cover the negative contrast on both acceleration footings for the tested
masses. It follows that the sign check alone does **not** exclude a positive-total-
density embedding. Such a background must be incorporated consistently in the
field equations, conservation law and environment; it cannot be added merely as
an accounting offset. `density_excess_run/` contains both footings and both
critical-density and cosmic-cold-density comparisons.

## 5. What remains necessary for closure

1. Specify one healthy parent action or kinetic dynamics and derive its field
   equation, lensing response and external-field boundary rule. Lensing does not
   supply this choice by itself.
2. Separate nonnegative conserved cold rest density from signed effective
   gravitational source. If the EFE-dependent enclosed mass is interpreted as a
   material inventory, its change under evolving environment needs an explicit
   current and continuity equation.
3. Derive the external vector field from density contrast and environment and
   establish a settling law. A scalar mean density and chosen coherence length
   do not establish either.
4. Predict the baryon/cold retention relation for actual populations and matched
   apertures, with no reuse of fitted mass fractions as independent predictions.
5. Propagate that same law through both full forest and lensing likelihoods and
   the galaxy constraints. A conditional two-redshift radius inequality is not
   a likelihood pass.

## 6. Reproduction and provenance

Every primary numerical run has a v2 bounded-runner manifest, stdout, stderr,
structured results and hashed declared inputs. Each manifest contains the exact
argv; copy that argv to a **new** output directory to reproduce. Runs used one
numerical-library thread and bounded time/output. No input changed during a run.

Accepted run directories: `claims_run`, `aqual_320_96`, `aqual_512_128`,
`capacity_320_96`, `capacity_512_128`, `boundary_1e4`,
`boundary_1e5_verified`, `density_excess_run`.

`density_run` is retained as a correctly labelled alternative **total** enhancement
59.5; it is not the combined-route cold-excess convention. `boundary_1e5` is
retained as the initial exploratory box run whose copied contract understated
rmax; `boundary_1e5_verified` reran the same computation with the corrected
contract. Neither superseded record is silently rewritten.

`summarize_runs.py` generates `summary.json` with numerical cross-checks and input
hashes; its seven comparison checks pass. `artifact_hashes.json` and
`verification.json` record final output hashes, manifest validation and preservation
of old outputs. Live scripts require a fresh output directory in this correction
lane; defaults use a unique timestamp and cannot overwrite historical results.

Primary-source checks used in the audit:

- [Milgrom 1994, astro-ph/9303012v1, sections III–IV](https://arxiv.org/html/astro-ph/9303012v1): scope of the circular-orbit constitutive equation and general nonlocal dynamics.
- [Milgrom 2010, arXiv:0911.5464v2](https://arxiv.org/html/0911.5464v2): QUMOND's Poisson formulation and distinction from the pointwise algebraic field.
- [Banik and Zhao, arXiv:1509.08457v3, equations 11 and 18](https://arxiv.org/html/1509.08457v3): AQUAL's external-field linearization and anisotropic Green function.

The formulas and source scope were independently audited; agreement of numerical
checks does not turn these conditional constructions into a derived cosmology.
