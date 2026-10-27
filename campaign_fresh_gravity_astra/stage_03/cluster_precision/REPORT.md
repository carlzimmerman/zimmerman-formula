# Cluster precision result at frozen base eccd1c0

The surviving cluster residual now has a direct force-sign discriminator and a
coupled measurement test. Within the stated conventional gas momentum law,
unchanged central baryonic profiles, spherical steady source-free radial flow,
and an extra scalar pressure that decreases outward, the seven reconstructed
clusters cannot satisfy both Euler balance and mass conservation. This is a
conditional obstruction to that explanation, not closure of gravity or an
observational exclusion with quantified confidence.

The derivation is in [DERIVATION.md](DERIVATION.md). The final authoritative
computation is [run_003/manifest.json](run_003/manifest.json), based on Git
`eccd1c0e59459b5ec1acf2e916fb7a05a7f67971` with a dirty shared checkout.
Only this agent's exclusive `stage_03/cluster_precision/` directory was written.
No literature search, additional data, imputed stars, halo fit or commit was used.

## Strongest constraint

Let `Delta=gH-F(B;a)>0`. With outward-positive radial velocity u and additional
pressure Pnt, elementary Euler balance gives

    partial_t u + u partial_r u = Delta -(1/rho) dPnt/dr.

If `dPnt/dr<=0`, the right side is positive. In a steady spherical source-free
flow, mass conservation gives `r^2 rho u=constant`. On a gas-mass interpolation
interval `Mgas=C r^s`, its left side instead equals

    u du/dr = (1-s) u^2/r.

All 189 intervals overlapping 100–1000 kpc have `s>1`, spanning
**1.185516–2.678286**. All **252 shell/branch evaluations** (seven clusters,
three radii, Q/R/M, two normalizations and vacuum/H scaling) have both positive
Delta and negative `1-s`. Each shell lies strictly inside its gas interpolation
interval. Zero velocity does not help, because the left side becomes zero.

Consequently this specific steady-flow explanation fails on the declared
central reconstruction. Uniform density/distance rescalings preserve s, so
they cannot alter the continuity sign while leaving a positive residual.
This conclusion needs no assertion that sampled Delta positivity holds at
every unsampled radius: contradiction at the evaluated interior shells is
already sufficient. The uncertain physical link is treating the interpolated
gas-mass derivative as the actual density profile and the hydrostatic-equivalent
gH as the thermal pressure force.

Euler alone would have demanded a minimum outer radial speed from

    u(1000 kpc)^2-u(100 kpc)^2 >= 2 integral Delta dr.

The resulting lower speeds range **1922–2565 km/s** over all clusters and
registered branches. For canonical vacuum R they range **1979–2512 km/s**.
These are necessary conditional bounds, not measured velocities or viable
constructed steady flows: continuity supplies the stronger obstruction above.
Time-dependent gas motions, nonspherical stresses, mass sources, a changed
gas reconstruction or modified matter inertia remain outside this exclusion.

## Coupled calibration result

For density ratio eta, pressure ratio pi, distance ratio d, stellar
mass-to-light ratio upsilon and the SAME angular shell, the direct volume and
pressure-gradient transformations are

    B' = eta d Bgas + upsilon Bstar,
    gH' = pi/(eta d) gH.

At fixed composition, simple thermal observation maps give X-ray amplitude
`chi=eta^2 ell d`, SZ amplitude `psi=pi d`, and temperature ratio `tau=pi/eta`,
where ell is the X-ray emissivity-coefficient ratio. They obey

    d = psi^2 ell/(chi tau^2).

If all these observed ratios and ell are fixed to one, there is no nontrivial
calibration freedom in this family. The cached profiles do not independently
fix these quantities with a joint likelihood, so constructed roots must not
be presented as evidence that such corrections occur.

For canonical vacuum R at 300 kpc, the seven pointwise equality requirements
are:

| Controlled route | Median required factor | Range | Additional prediction |
|---|---:|---:|---|
| Density eta, fixed pressure and distance | 2.1208 | 1.9743–2.4285 | At fixed emissivity, X-ray amplitude rises by median 4.4978; temperature ratio is median 0.4715 |
| Distance d, fixed X-ray amplitude, temperature and emissivity | 2.5118 | 2.3108–2.9764 | SZ amplitude must rise by sqrt(d) |
| Distance d, fixed X-ray and SZ amplitudes and emissivity | 1.9394 | 1.8292–2.1932 | Temperature ratio must be d^-1/2, median 0.7181 |

In the density route, hiding the X-ray change instead requires an emissivity
ratio eta^-2. In the final route, fixed emissivity is only a conditional slice:
real temperature changes generally change emissivity, which must be computed
with the spectrum and detector response. Distance calibration is varied at
fixed branch a0; these are not self-consistent changes in cosmological
parameters or H0.

The roots are not a sixfold source-mass relabeling: the calculation changes
both baryonic acceleration and inferred thermal acceleration. They also do
not make a common explanation. For the three canonical vacuum R routes,
one shared nuisance over all 21 shells has minimum possible largest
multiplicative force mismatch **1.6612, 1.6262, 1.6095**, respectively. Even
allowing a different X-ray/SZ-preserving distance per cluster leaves each
cluster's three radii with a minimum largest mismatch **1.2587–1.4703**.
These scalar minimax discrepancies describe the central-profile shapes;
they carry no observational significance and do not exclude a larger family
with several correlated or radius-dependent nuisances.

The branch sensitivity remains explicit:

| Kernel | a0 footing | Scaling | Median density eta | Median fixed-temperature distance d | Median X-ray/SZ distance d | Euler speed range, km/s | Common X-ray/SZ distance minimum mismatch |
|---|---|---|---:|---:|---:|---:|---:|
| Q | canonical | vacuum | 2.3025 | 2.7796 | 2.0849 | 2045–2565 | 1.6308 |
| Q | canonical | H | 2.2869 | 2.7543 | 2.0708 | 2039–2559 | 1.6330 |
| Q | alternative | vacuum | 2.2055 | 2.6244 | 1.9980 | 2000–2529 | 1.6373 |
| Q | alternative | H | 2.1895 | 2.5992 | 1.9839 | 1993–2522 | 1.6393 |
| R | canonical | vacuum | 2.1208 | 2.5118 | 1.9394 | 1979–2512 | 1.6095 |
| R | canonical | H | 2.1062 | 2.4894 | 1.9267 | 1972–2505 | 1.6111 |
| R | alternative | vacuum | 2.0308 | 2.3754 | 1.8616 | 1929–2473 | 1.6129 |
| R | alternative | H | 2.0162 | 2.3535 | 1.8491 | 1922–2465 | 1.6145 |
| M | canonical | vacuum | 2.1208 | 2.5118 | 1.9394 | 1979–2512 | 1.6095 |
| M | canonical | H | 2.1062 | 2.4894 | 1.9267 | 1972–2505 | 1.6111 |
| M | alternative | vacuum | 2.0308 | 2.3754 | 1.8616 | 1929–2473 | 1.6129 |
| M | alternative | H | 2.0162 | 2.3535 | 1.8491 | 1922–2465 | 1.6145 |

The nuisance medians refer to 300 kpc; speed bounds use 100–1000 kpc; the
common mismatch uses 100, 300 and 1000 kpc. M was evaluated separately using
its inherited monotone interpolation. Its agreement with R at displayed
precision does not assert equality of the laws.

## Verification and self-audit

Primary mathematical verdict: **conditional on a named input**—the spherical
central gas/pressure reconstruction and conventional local gas momentum law.
The finite numerical assertions are verified over the stated grid and branches.
This is self-review, not an independent referee audit.

| Dependency/obligation | Status | Evidence or limitation |
|---|---|---|
| Gas volume and pressure chain-rule scaling | Passed | Direct derivation plus analytic rho and pressure test |
| Stellar distance response | Conditional | Fixed angular flux, composition, redshift and stellar mass-to-light convention |
| Q/R/M force and branch conventions | Passed | Separate evaluations; all baseline ratios reproduce original run_002 to 4.44e-16 relative |
| Euler force signs | Passed under stated mechanics | Outward-positive A=gH+gnt-F; decreasing Pnt increases required A |
| Continuity signs | Passed under stated geometry | r²rho u constant gives coefficient 1-s; every evaluated s>1 |
| Density reconstruction | Conditional | Piecewise power-law enclosed mass differentiates to the declared density; no raw deprojection audit |
| Calibration roots | Passed finite test | 756 forward recoveries; maximum relative error 3.06e-13 |
| Shared scalar nuisance minima | Passed | 288 monotone residual problems with equal opposite extrema |
| Radial force integrals | Passed finite test | 168 knot-split quadratures checked independently; max difference 1.31e-8 relative |
| Positivity at every real radius | Not asserted | Dense grid plus knots only; shell contradiction needs only the evaluated interior points |
| Instrument constraints and confidence | Not addressed | No joint raw X-ray/SZ/temperature likelihood or covariance |
| Lensing/cosmology/covariant completion | Out of scope | Hydrostatic data are not direct lensing observations |

All mass/radius units were checked, all evaluated shells stayed inside the
three original supports, and duplicated NFW values agree to the original
1% unit-alignment tolerance. The NFW values enter no force calculation.
Run provenance pins every input SHA-256 before and after execution and hashes
all five scientific result files. The software was Python 3.13.9, NumPy 1.26.4,
SciPy 1.14.1 and Astropy 7.2.0 on macOS arm64. The run enforces a 120 s wall
limit, 100 s per-process CPU limit, 1 MiB log cap and cooperative one-thread
library cap; no memory or CPU-affinity cap is claimed. No randomness is used.

The first run failed because NumPy 1.26.4 lacks `np.trapezoid`; the implementation
was changed to SciPy's available `trapezoid`. Run 002 completed before the
continuity extension. Both are retained as historical records and are
superseded by run 003; their code hashes deliberately do not identify the
current expanded script. The final run 003 manifest validates against current
inputs and outputs.

Reproduce into a fresh directory from the repository root:

```sh
/opt/homebrew/Caskroom/miniconda/base/bin/python campaign_fresh_gravity_astra/stage_03/cluster_precision/run.py run_004
```

Validation already executed successfully:

```sh
/opt/homebrew/Caskroom/miniconda/base/bin/python /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py campaign_fresh_gravity_astra/stage_03/cluster_precision/run_003/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

First unresolved implication: establish whether independent gas-density slope,
pressure-gradient and thermal/distance calibration measurements permit changing
the reconstructed Delta or s enough to evade the sign contradiction while
satisfying the coupled observation equations. The cheapest discriminating
observation-level check is a joint density/pressure/temperature reconstruction
at the same angular shells, including the actual emissivity response. The
cached mass profiles alone do not establish that needed measurement model.

Proofreading self-review covered the full new derivation and report. Routine
edits: clarified geometry and mechanical scope. Mathematical-token typo
changes: none. No unresolved notation or cross-reference errors found.
