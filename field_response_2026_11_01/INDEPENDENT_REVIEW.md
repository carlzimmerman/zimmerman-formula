# FR01 independent scientific and implementation review

Reviewer: `/root/fr01_independent_review`, 2026-11-01. Scope: the bounded
radial energy screen and fixed-dark-mass Plummer response in this directory.
No author code, contracts, results, or external project files were changed.

**Normalized claim.** For the six specified PN28 static backgrounds, the
declared isotropic fluid-plus-scalar quadratic energy admits a negative
fixed-dark-mass radial direction in the tested finite displacement space.
Separately, a prescribed spherical Plummer field produces some checked
fixed-dark-mass static endpoints under the frozen continuation protocol.

**Primary verdict: correct only after a stated restriction.** The restriction
is the explicitly imposed isotropic fluid closure and its declared positive
linear inertia. The reviewed calculations support negative radial energy
directions for all six backgrounds in this model. They do not establish
instability of unrestricted collisionless kinetic evolution. The static
results establish only the converged cases listed below; the requested full
response grid was not completed successfully.

**Computation review status: audited, not executed.** I reconstructed the
critical algebra, inspected both numerical implementations and their
serialization amendments, read the final result files and manifests, and
independently verified all manifest input/output hashes against disk. I did
not launch a new scientific computation or independently reproduce the
floating-point solves. Numerical interpretation remains conditional on the
reported discretization/convergence checks, without interval certification.

## Dependency chain and checked obligations

The dependency chain is:

1. Specified PN28 potential, canonical phase level and isotropic relation
   `K=k rho^(5/3)` (model assumptions).
2. Static energy plus Poisson gravity (internal definition).
3. Equilibrium equations, constrained Hessian, scalar stress and mass
   condition (internal algebra, reconstructed here).
4. Positive declared fluid/scalar inertia and a self-adjoint energy-form
   realization (restricted linear completion).
5. Negative finite Rayleigh numerator (author's numerical evidence).

The static response uses steps 1–3 with an external baryon potential. It
does not use a theorem asserting stability, adiabatic tracking, formation,
or closure of the full kinetic hierarchy. No external theorem or citation
was required for the finite-dimensional negative-Rayleigh-quotient check.

| Obligation | Review status |
|---|---|
| Fixed dark mass and free matter edge | Passed analytically and in code |
| Density/scalar Hessian coefficients and gravitational sign | Passed analytically and in code |
| Scalar minimization and reciprocal mixed term | Passed analytically and in code |
| Exterior scalar stiffness | Passed for the stated asymptotic Robin screen |
| Positive inertia | Passed within the declared linear completion |
| Static Plummer source, gauge and boundary slope | Passed analytically and in code |
| Total anisotropic stress and separate external virial | Passed analytically and in code |
| Numerical six-case negative energy evidence | Conditional on recorded floating-point checks; all reported gates pass |
| Complete static response grid | Not achieved; failed/skipped cases retained |
| Exact continuum growth rates | Not addressed by these Ritz computations |
| Persistence of isotropic closure in kinetic evolution | Not established |
| Full kinetic stability or instability | Not established |
| Microscopic selection, observed acceleration or galaxy calibration | Out of scope |

## Decisive algebra and implementation findings

For a radial mass displacement, the admissible first density variation is
`q=-(r^2 n xi)'/r^2`. The polynomial basis satisfies `xi=O(r)` at the center
and remains finite at the moving matter edge. Since `n(R)=0`, total mass
variation vanishes without imposing `xi(R)=0`. A small smooth Lagrangian
displacement supplies a nonnegative mass-preserving path; a finite Eulerian
linear density increment need not remain nonnegative arbitrarily close to
the edge and is not the claimed path. The `n~(R-r)^(3/2)` edge makes the
quadratic density term integrable.

Differentiating the dimensionless local energy
`(3/2)n^(5/3)exp(-2s)+exp(3s)-3s-1` gives, on the stationary background,

```text
a=(5/3)psi/n,  b=-5psi,  c=6n psi+9exp(3s).
```

The implementation's `a=(5/3)exp(-3s)/sqrt(psi)` is exactly the same
coefficient. The gravity term is `-(5/2)n^2 xi^2`, with no extra factor
one half in the second variation. The scalar equation
`(-3epsilon Delta+c)sigma=-bq` has the correct sign and the assembled mixed
term contains both reciprocal contributions. Its Robin stiffness term
`3epsilon L^2[sqrt(3/epsilon)+1/L]sigma(L)^2` is retained. These checks reveal
no factor/sign defect that would explain away the negative directions.

The independently derived homology/amplitude energy identity is useful
corroboration of the Hessian assembly: its direct quadratic value and actual
mass-preserving energy finite differences agree in the stored results.
Those particular homology trial curvatures are positive in all six cases;
they are controls, not the negative witnesses themselves. The negative
witnesses use the broader displacement/scalar space.

For static forcing, the code correctly imposes
`-L^2 psi'(L)=M+m_b(L)`, with **dark** mass `M` fixed and central `psi` free.
It reconstructs the self-potential with
`mu=psi(L)-M/L+phi_b(L)` and `phi_d=mu-psi-phi_b`; this retains the Plummer
tail and fixes the self-potential gauge. The analytic source and enclosed
mass are positive and satisfy `Delta phi_b=n_b`.

The stresses `Pi_r=A-U+(3epsilon/2)s'^2` and
`Pi_t=A-U-(3epsilon/2)s'^2` give
`Pi_r'+2(Pi_r-Pi_t)/r=(5/2)n psi'`. The code differentiates the stress
independently. Its self-gravity potential energy has coefficient `5/4`,
while the prescribed external potential energy has coefficient `5/2`.
The external virial is the force integral, and is correctly distinguished
from the Plummer potential-energy integral. Matter mass, scalar source,
virial, edge and opposite-baryon-sign controls match the declared scope.

## Stored finite evidence

`radial_run_003/manifest.json` records status `completed`, exit status zero,
and all listed hashes match the reviewed files. All six case-control maps
are true. The refined scaled negative margins lie between approximately
`-0.03564` and `-0.02549`, well beyond the frozen `-1e-5` gate. The stored
mass-variation errors are about `1e-8`, and scalar-response identity errors
are below `3e-10`. Nested basis and doubled-quadrature/tighter-scalar checks
pass. This is numerical evidence for negative directions of the specified
energy, not a certified continuum spectrum.

`static_run_002/manifest.json` records status `failed`, exit status one,
with complete declared result files and matching hashes. Its status is
expected because not all requested continuations succeeded. There are:

- 12 passed zero-forcing records, duplicating the six baselines across the
  two forcing families;
- 12 passed nonzero weak-diffuse records;
- 9 first-step failures: six node-limit exits and three singular-Jacobian
  exits;
- 27 later continuation records explicitly not attempted;
- one passed endpoint refinement and three unavailable refinements.

The three completed nonzero-forcing families are:

| Baseline `psi_c` | `epsilon` | Family | Final `C_q/C_q0` |
|---|---:|---|---:|
| 0.95 | 0.0001 | weak_diffuse | 0.8243303633 |
| 0.95 | 0.01 | weak_diffuse | 0.8404381153 |
| 0.99 | 0.01 | weak_diffuse | 0.8037911113 |

Only the last endpoint was among the available predetermined refinements;
its largest recorded change among radius, central density and column is
about `2.92e-7`, below `5e-5`. No strong-compact forced state was verified.
The decreasing columns are static outputs on these branches, not an
adiabatic evolution prediction. A failed continuation is neither a proof
of nonexistence nor a stability test.

Both amendments preserve the scientific algorithms: radial v2 converts
NumPy scalars during JSON serialization, while static v2 retains nonfinite
failed-solve diagnostics as null with explicit paths. Neither silently
changes a physical failure to a pass. The initial unsuccessful runs are
historical diagnostics, not substitutes for the final result files.

## Required interpretation and remaining gap

One output label needs care: `reduced_mode_efolding_time` in radial v2 is
computed from a generalized Ritz eigenvalue with a statically minimized
scalar subspace and finite-domain inertia. The infinite scalar tail's
inertia is not included, and the true dynamical exterior has a
frequency-dependent decay constant. The field is therefore a **finite
Galerkin trial diagnostic**, not an established continuum mode growth
time. The same limitation applies to treating `lowest_omega2_ritz` as an
exact physical frequency. This does not invalidate the negative energy
sign. The coordinator was notified before final reporting.

The strongest safe conclusion is that all six tested backgrounds fail the
radial energy screen of the declared isotropic fluid completion. Their
static response does not establish a viable stable halo mechanism. The
calculation leaves the full kinetic parent's stability unresolved: an
arbitrary locally isotropic fluid displacement is not automatically an
invariant or dynamically accessible collisionless perturbation, and the
kinetic stress hierarchy and general vacuum dynamics are not supplied by
this closure. Neither agent agreement nor numerical refinement closes
that missing implication.

The cheapest remaining reporting check is to ensure every presentation of
growth times and static endpoints carries those qualifications. A new
physical investigation would require a declared conserving kinetic
perturbation/evolution model and its admissible phase-space variations;
merely increasing the present polynomial basis cannot establish that
kinetic implication.

## Review provenance and exact revisions

This was a separately dispatched, read-only implementation and algebra
review. It used the raw source and equations as well as the author's
derivation. It is independent in execution role, but not an independent
numerical implementation or reproduction. The numerical commands recorded
in the author manifests are:

```text
python3 field_response_2026_11_01/radial_stability_v2.py field_response_2026_11_01/radial_run_003/result.json
python3 field_response_2026_11_01/static_response_v2.py field_response_2026_11_01/static_run_002/result.json
```

Review commands were source reads, a source diff, JSON inspection and
SHA256 comparisons, without git commands or new solver runs. All listed
input/output hashes in both final manifests were recomputed and matched.
The exact reviewed files below are relative to this directory:

| File | SHA256 |
|---|---|
| `CONTRACT.md` | `10e38d294abfacb37c44197e86b619dc60cd83d4b5f449fd73fdf2f8cf1cb667` |
| `CONTRACT_STATIC.md` | `30137060dadb69571fb11cef6cbc5fae57289995b4e54ef137d4f41cbff61ccb` |
| `THEORY_REVIEW.md` | `76a7ed331b8b15d93e8ad484ca0ebffdb14662575154b1c2ac0104a4b3c68b48` |
| `STATIC_DERIVATION.md` | `2efe2cd3ff8dfb3e9be21f6e3a2114f8bde62a9a1b54619e6346173466cda65d` |
| `static_response.py` | `51faf8f19b3471a3fb0bd40dc1e76fc47c0697c43d313397bbad124ca682dfa5` |
| `static_response_v2.py` | `92c425005f14da57e100a2973bcc11f688624edf7b9738800a2ea13cda0da95c` |
| `radial_stability.py` | `c3d312ec7b1ea9c42c9996ed56cc5c489fee2730d01da16b8b01cefa4a38b904` |
| `radial_stability_v2.py` | `62dcd08272baf83d091956f4db5cf38c5d5fb5ab2f543e1d433ec09d59998fb7` |
| `test_controls.py` | `be238666948755f7fbeb3a795f76eb2f2b5475ad28495a398192b93df2cc0ee6` |
| `STATIC_AMENDMENT_A1.md` | `ac604b5e356b93e56afb2d4b3fd8459374850fc57dbee3fc39d012706d3c8476` |
| `RADIAL_AMENDMENT_A1.md` | `cf08d61d8ce5649c5d3fdbeaabb45059ef07f43a516d7323d701e7d7c72d489c` |
| `inputs/check_gradient.py` | `1f5cb1020eda2238f65a624a8eebac8a77ec2fb07f22fdfec9bd2dca8c562652` |
| `inputs/PARENT.md` | `6deea173491b9c8e4d88b528ac0895faf2c6ec99273aa86c9d6e73d7c7d8537d` |
| `inputs/EOS.md` | `05f919345cb73c8b96e3f07d5fdb421ae8ee1d24a01e177abc9551aab4092274` |
| `radial_run_003/manifest.json` | `e812317fde5128b681eb1ee1f61b7a1f423348a10a3907bf0184d0f823c74d68` |
| `radial_run_003/result.json` | `1dd536890711fb5d37b34d705f4d89197dac6831abcc449ff4ff86f87f2f4dcb` |
| `static_run_002/manifest.json` | `22ae34cc22cea1b479187e810592689f4a7368d3ffeaa79289f3c59ebb3a8432` |
| `static_run_002/result.json` | `55bcf84e6b9b2b5e83ffd7a40235c8ea2cb2fc4eecc04682a70941311d127f33` |

Final mathematical proofreading covered this report's equations, signs,
normalizations, counts and scope qualifiers. No author mathematical tokens
were edited. No new scientific computation was run by this reviewer.

## Follow-up review: canonical kinetic energy, 2026-11-01

This addendum reviews `CONTRACT_KINETIC.md`, the new canonical-deformation
addendum to `THEORY_REVIEW.md`, both kinetic screen versions, their control
amendment, and `kinetic_run_002`. The initial review above remains the record
of the fluid/static calculation. This new calculation addresses a specific
gap in transferring its energy directions to the kinetic phase space.

**Follow-up claim and verdict: computationally verified only in a stated
range.** The corrected energy has negative canonical radial directions in
the specified 12-dimensional family for all six backgrounds, subject to the
recorded numerical checks. These are accessible kinetic energy saddles of
the specified stationary waterbag-plus-scalar configuration. They are not
a theorem of exponentially growing Vlasov modes or nonlinear instability.
Review status remains **audited, not independently executed**.

I independently checked the finite transformation. For a radial map with
principal stretches `a=1+t xi'` and `b=1+t xi/r` twice, the cotangent lift
`p=J^(-T)p0` is canonical and preserves phase-space volume and each angular
momentum vector. Taking sufficiently small `t` keeps both stretches
positive. The initial even momentum distribution remains even, so its
canonical mean current is zero. With scalar momentum zero, the parent
Hamiltonian's mean-current and scalar-momentum squares vanish along this
configuration path. This does not assume that the deformed momentum
ellipsoid is isotropic.

The integrated kinetic factor is `(a^(-2)+2b^(-2))/3`. The fluid closure
on the same mass density and scalar path instead has `(a b^2)^(-2/3)`.
Their difference vanishes through first order and has second derivative
`(8/9)(xi'-xi/r)^2`. Thus the added dimensionless quadratic form is

```text
delta Q = (4/3) integral_0^R n psi (xi'-xi/r)^2 r^2 dr.
```

No further scalar mixed term is generated: the factor multiplying this
difference contributes only its background value at second order. Gravity,
scalar potential and scalar gradient are identical on the two shared
configuration paths. Consequently reuse of the scalar minimizer is valid.
`shear_matrix` implements this expression with the existing basis and
quadrature. Homology has exactly zero correction, and the matrix is
positive semidefinite. The generalized eigenproblem's inherited fluid
metric serves only as a positive normalization; it is not asserted to be
the kinetic equation of motion.

The original fluid-minimizing vectors all acquire **positive** curvature
after adding shear. This matters: the old witnesses did not transfer to
the kinetic model. Reoptimizing the corrected form produces different,
negative witnesses. The stored refined results are:

| `psi_c` | `epsilon` | Minimum normalized kinetic curvature | Scaled negative margin |
|---|---:|---:|---:|
| 0.8 | 0.0001 | -0.01577394015 | -0.01516103637 |
| 0.8 | 0.01 | -0.01482514071 | -0.01432282926 |
| 0.95 | 0.0001 | -0.09161850682 | -0.04822042451 |
| 0.95 | 0.01 | -0.09914846739 | -0.04941944347 |
| 0.99 | 0.0001 | -0.08736959403 | -0.04803266193 |
| 0.99 | 0.01 | -0.10905979473 | -0.05030315292 |

The 4/8/12-dimensional nesting, 256/512-node quadrature comparison, shear
positivity, homology, scalar identity and mass-variation checks all pass.
`kinetic_run_002` records status `completed`, exit zero and
`all_controls_pass=true`; all its listed input/output hashes independently
match disk.

The finite-difference amendment is justified without changing the gate.
For the failed original control `A=2,D=-1`, the exact factor difference
expands as `4t^2-(20/3)t^3+25t^4+O(t^5)`. Its centered second difference is
therefore `8+50h^2+O(h^4)`, explaining the original finest-step relative
error near `3.9e-7`. Version 2 cancels that leading truncation term using
the two already prescribed finest steps. Its only source change is this
Richardson estimator and its recorded value; the raw differences, `3e-7`
accuracy gate and every physical energy matrix remain unchanged.

A metadata limitation should be retained explicitly: the kinetic v2
contract/manifest inherited wording about a fluid completion and lists
both old scalar tolerances. The kinetic code actually uses the canonical
shear family and only `3e-7` scalar BVP tolerance. The frozen
`CONTRACT_KINETIC.md` and this review disambiguate that scope. This is a
metadata clarification, not evidence for treating the fluid metric as a
Vlasov inertia. The historical manifest should not be silently rewritten.

The new energy calculation supplies canonical accessibility for these
specific perturbations; it does not prove preservation of isotropic
closure during evolution. A kinetic growth inference still needs the
actual linearized Hamiltonian operator and its constraints/vacuum domain,
or an applicable energy principle with all hypotheses checked. Merely
inserting this shear matrix into the old fluid dynamical eigenproblem
would not supply that missing step.

As an orthogonal numerical check, I recommended evaluating the actual
finite-deformation energy for an optimized witness: push forward the
matter with `x=r+t xi(r)`, transform momentum by the cotangent lift, retain
the Eulerian scalar path `s_t(x)=s0(x)+t sigma(x)`, and use the exact shell
self-energy at the moved shell radius. Symmetric energy differences can
then be compared directly with `Q_fluid+delta Q`, independently of the
Hessian assembly. Such an additional run is not asserted by this addendum.

The new `DIAGNOSTIC_DICTIONARY.md` addresses the earlier growth-time-label
finding: it explicitly limits the stored fluid e-folding time to a finite
Galerkin diagnostic and retains the original output for provenance.

Exact additional reviewed SHA256 values are:

| File | SHA256 |
|---|---|
| `CONTRACT_KINETIC.md` | `8170be4835b28b38232ab955e6e8a3654fa926c8223906f79da947e727537f4a` |
| `KINETIC_AMENDMENT_A1.md` | `d8f6da5f1dd5dbcb7337f488f71b40e6630ea17832aa3105518d51754b6e7a33` |
| `THEORY_REVIEW.md` including canonical addendum | `c40e02375e77c1db6b20e81ab7dd8cec29d1d6d630040323975261a86af96374` |
| `kinetic_screen.py` | `8dbac53b8c4bd58d7121105f48daf1baadf698c67f3fb5800b24a6ed2f43b0a0` |
| `kinetic_screen_v2.py` | `eb526da3459a400f28894059cecaf74341c39ef933aac0c4a293c6e772d905f5` |
| `test_kinetic_control.py` | `a92575b8d8983f168dae22a953c5fb1371690a367c351f60dbbf729000ca9d42` |
| `kinetic_contract_v2.json` | `1a99411e19700581b5ee05deb1af2361c759c04738dc82f887111db2339ee2e3` |
| `kinetic_run_002/manifest.json` | `289d15780345fb67cf86e073a52b3d190695bd1a7f3f90cdc237a265eac699ea` |
| `kinetic_run_002/result.json` | `7889b2e74bf6011d5f002a3999c67439b86dd1f5d076cf2fa6bc740a0920cfc1` |
| `DIAGNOSTIC_DICTIONARY.md` | `d72704c9c28f3f5cb0de3e8ac928fcb1d1d6cfe61e266be26c87969ef3ae0950` |

This addendum received a mathematical proofreading pass for the factor of
two in the second derivative, dimensionless normalization, phase-space
constraints and the separation of energy saddles from growth theorems.

## Follow-up review: direct finite energy and dilute controls, 2026-11-01

The additional direct-energy check recommended above is now implemented in
`canonical_energy_check.py` and recorded in `canonical_energy_run_001`.
I reviewed its frozen JSON contract, full implementation, result and report,
and the targeted dilute-state stability/static extensions. No new solver
execution was performed by this reviewer. All listed input/output hashes
in these three new run manifests independently match disk.

**Direct-energy verdict: computationally verified only in the stated six
cases and prescribed finite steps.** The new implementation correctly
evaluates the actual canonical deformation energy, rather than merely
repeating the matrix quadratic form. It retains each supplied optimized
vector, independently solves for the combined scalar response at `3e-8`,
and evaluates both signs of four prescribed step sizes at 512 and 1024
quadrature points per region.

The relative kinetic energy uses the exact cotangent momentum factor and
samples the Eulerian scalar at the moved matter positions. The scalar
potential and gradient use the fixed physical scalar domain. The shell
gravity is `-(5/2) integral m0(r)n0(r)r^2/[r+t xi(r)] dr`, which correctly
preserves shell mass and radial ordering. Its stable increment has the
positive coefficient `+(5/2)m0 n0 t xi/[r(r+t xi)]`. The code's rational
stretch increments and `expm1` scalar increments reproduce the exact
finite formulas while avoiding subtraction of large total energies. The
separately calculated first variation has the correct kinetic, scalar,
gravity and boundary terms. No missing Jacobian, factor of two, or
scalar/displacement cross term was found.

All six supplied directions lower energy in **both** signs at the two
required smallest steps at both quadratures. The largest absolute
independent first variation is about `2.09e-11`; the largest finest-step
relative curvature discrepancy is about `8.53e-6`. The full report's
six-case numbers match the result file. The complete run has status
`completed`, exit zero and every control true. These finite decreases
corroborate the accessible energy-saddle conclusion without relying solely
on the Hessian assembly. The frozen displacement was not reoptimized in
this check.

The approximation boundaries remain explicit: the background solver is
shared, scalar tails use the same asymptotic quadratic exterior model,
and numerical quadrature/positive-stretch checks are not interval
certificates. The first-variation and both-sign controls address residual
equilibrium error; they do not turn a finite numerical check into a
universal theorem. The kinetic dynamical growth question remains open.

**Dilute controls.** `dilute_stability.py` calls the already reviewed fluid
and canonical routines unchanged at `psi_c=.2,.4,.6`, `epsilon=.01`, as
declared before execution. All controls pass. The refined fluid minima
are approximately `0.0130685, 0.0314559, 0.0326427`; the corresponding
canonical minima are `0.0132245, 0.0315722, 0.0338983`. Thus these three
states reveal no negative direction in the tested spaces. They have not
been proved continuum-stable. The dense-state adverse result must not be
reported as a result for every state of this parent.

**Dilute static response.** The new wrapper preserves the original
fixed-dark-mass solver and its physical checks. Its additional observable
tracks the dark mass initially enclosed by the original quarter-density
radius, then solves for the radius containing that same mass after
forcing. This is a valid material-core observable and is distinct from
the changing density-threshold core. Independent density quadrature and
the total slope minus enclosed Plummer mass agree at both queried radii.

`static_dilute_run_001` preserves all 246 contracted records: 173 pass,
three fail at the node limit, and 70 are explicitly not attempted. Its
global status remains `failed`, reflecting incomplete continuations.
The three completed endpoints are:

| Initial `psi_c` | Family | `C_q/C_q0` | Radius of original core mass / original core radius |
|---:|---|---:|---:|
| 0.2 | weak_diffuse | 1.0815883 | 0.9644391 |
| 0.2 | strong_compact | 3.0370840 | 0.6856207 |
| 0.4 | weak_diffuse | 1.1089230 | 0.9564673 |

These establish conditional static contraction for those specific
dimensionless forcing families. They do not establish formation,
adiabatic access, stability, or observational calibration. This extension
does not include a new domain/tolerance refinement, consistent with its
contract. The unfinished families remain numerical inconclusiveness.

For the separately planned endpoint energy screen, reusing the existing
Eulerian Hessian with the new equilibrium is algebraically justified:
the prescribed external potential energy is linear in density and has
zero Eulerian second derivative. Terms from the second-order density
change along a mass-preserving path cancel through **total** equilibrium
stationarity `e_rho+Phi_dark+Phi_b=mu`. No additional external-gravity
quadratic term should be inserted. The canonical shear correction is
unchanged. Endpoint numerical results are not asserted by this addendum.

The exact additional reviewed hashes are:

| File | SHA256 |
|---|---|
| `canonical_energy_contract.json` | `9e0a62b71a30027df05f820e63c376999a1371664d1e5c9ae8547ebc99ebba93` |
| `canonical_energy_check.py` | `21b22db22f7d3cd15c1f7c0e3206157e72c6ab8eeed6bdae0c041009617f8f6d` |
| `CANONICAL_ENERGY_REPORT.md` | `23bfeb470e65c4e77089367380df8d73ad3862b91ad52b3da43feb6488c0de08` |
| `canonical_energy_run_001/manifest.json` | `0ac6f945c5dea1dd15868b4b98ca31141fb6ded9f016639e87d6da0b74243c8e` |
| `canonical_energy_run_001/result.json` | `69e1963435ba60b67f4f7c42fd89d6bbca638c9f412f040b10f1792cc1052e2c` |
| `CONTRACT_DILUTE_STABILITY.md` | `39a4ec52ecc3d8f38eea8d80cacc0085d5508baaa6bd0b906954a9a9718010d6` |
| `dilute_stability.py` | `62562e28f54935f5eeae21f3af2b2c507e4024f5391f362e2118fa738aa9e335` |
| `dilute_stability_run_001/manifest.json` | `d7b6d114d2685f82f9e68aedd0effeaec9b884591f6ac002220c76bf766dc7d4` |
| `dilute_stability_run_001/result.json` | `12e5147f09b63930d9da98b5e94598a1577d3be6de71bc7e86c2fddd110edca8` |
| `CONTRACT_DILUTE.md` | `91d5af9178b4b6a4dc306254a6740871b0ba96fa366b3a02f917d097753f9a49` |
| `static_dilute.py` | `8080278061dad1e5ff509f7462912e1255594080948be93b1d715e36b7a046c7` |
| `static_dilute_run_001/manifest.json` | `313101dc93d46b7113e05791e5fe167c57542564b6ca32046d5c3ef252b65bda` |
| `static_dilute_run_001/result.json` | `fa055839b9fd55d9ea9410c13ac4745a499e02578e0d2e578233be79291dc78c` |

Mathematical proofreading covered the finite-map Jacobians, gravity
increment sign, first/second variation distinction, fixed-core observable,
case counts and finite-scope qualifications in this addendum.

## Final targeted review: three dilute endpoints, 2026-11-01

`endpoint_stability_run_001` now supplies the separately planned endpoint
screen. I reviewed `CONTRACT_ENDPOINT_STABILITY.md`, the reconstruction
helper, screen implementation, result and manifest. The reconstruction
replays the same `.025` continuation for exactly the three previously
passing endpoints; it uses actual BVP solutions rather than interpolating
the presentation profiles. Every intermediate static/material-core gate
passes, and all six saved/reconstructed observable comparisons are exactly
zero in the stored floating-point records.

The implementation correctly reuses the Eulerian fluid Hessian and
canonical shear form on each baryon-forced equilibrium, with dark density
alone in the self-gravity term. It does not reuse the inapplicable
zero-baryon homology identity. The independently checked variational reason
for the absent explicit baryon Hessian term is given in the preceding
addendum. All recorded inertia, scalar-identity, mass, reconstruction and
quadrature gates pass.

| Initial state and forcing | Fluid minimum, 512 quadrature | Canonical minimum, 512 quadrature |
|---|---:|---:|
| `psi_c=.2`, weak_diffuse | 0.01567648131 | 0.01589508074 |
| `psi_c=.2`, strong_compact | 0.04715535845 | 0.04822427611 |
| `psi_c=.4`, weak_diffuse | 0.03719032730 | 0.03731948044 |

**Verdict: computationally verified only in the stated finite spaces.**
None of these endpoints reveals a negative radial energy direction in the
tested full 12-mode displacement space with its minimized scalar. This
supports reporting the static contraction examples together with a passed
finite energetic screen. It does not establish continuum stability,
kinetic growing-mode absence, or an actual assembly trajectory. The strong
compact `.2` example therefore supplies a conditional equilibrium response
and finite energy check, not a calibrated galaxy prediction.

Actual endpoint coverage is the full 12-mode space at scalar tolerance
`3e-7`, with quadratures 256 and 512. The JSON contract/manifest retains
inherited arrays listing 4/8/12 and both old scalar tolerances; explicit
nested endpoint solves were not performed. Positivity of the full
finite-space quadratic form also implies positivity on its coordinate
subspaces, but that algebraic implication should not be described as
separate numerical runs. This metadata limitation does not change the
reported positive 12-mode results.

The run status is `completed`, exit zero. Every listed manifest input and
output hash was independently recomputed and matched disk. All earlier
failed continuation records remain part of the evidence; these endpoint
screens do not erase or replace them. Exact additional reviewed hashes:

| File | SHA256 |
|---|---|
| `CONTRACT_ENDPOINT_STABILITY.md` | `70ac46f7deada01ec130ed29111c2337626a459062d43e7f1094e342f20c215e` |
| `endpoint_stability.py` | `c4cd9b31064f8875e9947fb6c2e4a6825ae2839b0a76b2ee19adbe70cda08292` |
| `endpoint_reconstruction.py` | `345ba91e993057a4322a72e44a7ed32cca340c976d6b7bc24d6e1d279bd5dd65` |
| `endpoint_stability_run_001/manifest.json` | `a3ec53f36057ff05c8301ec4332784877cfd73becfd7aa37f2a3587b34efbcf6` |
| `endpoint_stability_run_001/result.json` | `9c45038813b25406f6a00ebb8552b6aef3b81f9ac1dea6ff8bf2fd212b8de37c` |

The final targeted addendum was proofread for the distinction between an
endpoint and its initial state, full-space and nested checks, and finite
positivity versus continuum stability. No scientific calculations were
launched and no author implementation or evidence files were edited by
this reviewer.
