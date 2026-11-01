# DR01 independent mathematical and implementation review

Reviewer: `/root/fr01_independent_review`, 2026-11-01. The review covers the
contracted fast-scalar kinetic shell calculation, source reconstruction,
orbital features, interaction matrices, finite Hamiltonian propagation,
forcing normalization, work and torque. It does not claim an independent
derivation of the PN28 parent or a new background equilibrium.

**Normalized claim and primary verdict: computationally verified only in a
stated range.** The implementation computes a self-consistent finite
Galerkin/Fourier response of the specified canonical waterbag parent in the
declared `F^2 -> 0`, fixed-`C_s` limit. Its finite conservative dynamics and
energy/angular-momentum ledger are supported by independent analytic checks
and direct small-system time integrations. Halo work requires the separately
reported orbital, spatial and Krylov convergence evidence. Neither stable
finite curvature nor finite-pulse positive work proves continuum stability,
irreversible heating, radiative cooling or a permanent core change.

## Model and dependency audit

The dependency chain is the PN28 Hamiltonian and stationary waterbag ->
linear perturbation on the energy shell -> declared instantaneous scalar
elimination -> reciprocal gravity/scalar/current kernels -> weighted
orbital Fourier truncation -> positive finite Hamiltonian propagation ->
finite pulse work and torque. The first model, waterbag state and fast-scalar
limit are assumptions. The intermediate algebra was checked independently
against the raw parent, not inferred from a static fluid Hessian.

In particular, the perturbation Hamiltonian must retain
`(1-exp(-2s0)) p.j1/n`. The code does so. Freezing all induced fields would
instead give a bare tracer response; the separately labeled bare controls
do not replace the dressed calculation. The scalar temporal parameter is
not selected by the static profile: this experiment explicitly removes it
through a singular fast-scalar limit. It consequently has no scalar
radiation. The nonuniform free-edge limit and nonlinear vacuum evolution
remain outside its claim.

The linear waterbag perturbation `f1=f_* delta(mu-h0) eta` is appropriate
for zero initial perturbation driven by a Hamiltonian source. The shell
equation `eta_dot=-i nu(eta+h1)` has the correct sign. The orbit-average
zero-frequency population cannot be driven and is correctly excluded from
the dynamical solve. It is retained in the full Gram normalization check.
Thus the causal static response is restricted to the active subspace;
it must not be equated with a neighboring hydrostatic equilibrium that
changes orbit populations.

## Feature, kernel and normalization checks

The canonical shell action measure is
`f_* (2pi)^3 (2L/Omega_r) dL`, with `f_*=3/(4pi 2^(3/2))`.
The orientation average for one fixed `l=2,m` contributes `1/5`.
The planar harmonics have only `k=-2,0,2`; their squared amplitudes divided
by five sum to `1/(4pi)`. These factors match the implementation.

The feature matrix stores conjugated Fourier coefficients. It therefore
maps weighted shell amplitudes to density/current source moments, and its
conjugate transpose maps field coefficients back to orbit Hamiltonians.
The forcing vector uses the unconjugated Fourier coefficients. The core
observable uses the same convention. I found no misplaced conjugation in
this chain.

For `S=1.5n/psi`, the independent complete shell Gram formulas are

```text
scalar: integral r^2 S(r) u_i*(r) u_j(r) dr,
current: integral r^2 [n/exp(-2s0)]
                  [Wr_i Wr_j+6 Wt_i Wt_j] dr,
scalar-current cross terms: zero.
```

The direct spatial Gram in `response_v2.py` implements these formulas.
The current vertex `p_r Wr+i k p_t Wt` retains radial and poloidal
components. Toroidal first-order response is excluded by parity for the
scalar quadrupole on an isotropic spherical background; omission here is
not a radial-only fluid closure.

The density interaction is negative `-G^-1`, the scalar interaction is
negative `-A_s^-1` with source vertex `2psi u`, and the reciprocal current
interaction is positive `C^-1`, where `C` uses
`1/gamma=n/(1-exp(-2s0))`. The Cholesky transformations produce precisely
`K=V† diag(signs) V`. The gravity exterior stiffness is the exact `l=2`
vacuum value `3R`; the scalar tail uses the `l=2` logarithmic derivative
and propagates it through the nonzero background scalar exterior. No
monopole scalar boundary condition is substituted.

The high-frequency current sum rule provides an additional normalization
check. In the complete representation,

```text
b† Omega H Omega b = integral n(r)[r^2 U'(r)^2+6U(r)^2] dr.
```

The bare result instead has `exp(-2s0)n` in the integral. Gravity and scalar
feedback have zero contribution to this odd-current moment; the reciprocal
current term restores the physical mass-current coefficient. A finite
current basis approximates the dressed identity, so its residual is a
spatial-resolution diagnostic rather than an exact finite-matrix identity.

## Finite dynamics, pulse and ledger

For positive `H=I+K`, setting `y=H^(1/2)z` gives the Hermitian operator
`A=H^(1/2) Omega H^(1/2)` and source `H^(1/2) Omega b`. The low-rank square
root and inverse square root match this transformation. The two-pass
reorthogonalized Lanczos implementation is appropriate for that Hermitian
operator. Its finite positivity demonstrates stability of that finite
conservative matrix, not stability of all omitted shell functions.

The analytic pulse integral correctly solves a zero-initial-state
sin-squared-envelope drive, including the carrier and both sideband
resonances. The post-pulse factor is the unforced unitary propagation.
There is no inserted imaginary frequency or damping coefficient.

Taking the real part of a unit-normalized complex `m=2` harmonic introduces
the following physical factors, all correctly present in the code:

```text
E = z†H z/4,
P = Re[(b†z)* F_dot]/2,
torque_z = Im[(b†z)*F],
J_z = (1/2) sum_n |z_n|^2/nu_n.
```

Consequently `P=Omega_p torque_z+envelope_power`, and after the source
returns to zero its integrated work equals the retained perturbation
energy. The source interaction energy is needed during the pulse; it
vanishes at the endpoints used for the work comparison. The signed
frequencies in the angular-momentum formula are necessary and are retained.

Two review findings were corrected in a separately preserved implementation:

- The original zero-feedback matrix had no retained low-rank eigenvectors
  and failed before the bare calculation. Version 2 returns the identity
  exactly in that case. The independent control reproduces the old failure.
- The original projected residual divided by a source norm that omitted
  the drive amplitude, although its numerator included that amplitude.
  Version 2 divides by amplitude as well and labels the quantity explicitly.

The original dressed numerical results are not altered by those fixes.
Version 2 also adds the force-sum diagnostic and contracted isolated
resolution controls.

## Independent numerical controls and their failed first run

I wrote `check_response.py` and its frozen contract without changing author
code. The root executed it through the bounded runner. It compares the
low-rank matrix functions to independent dense eigendecomposition, the
analytic pulse to direct DOP853 integration including exact resonances,
and bare/dressed eight-mode dynamics to direct integration of the original
complex `z` equation. Work, torque and envelope work are integrated as
separate reference ODE components. It also reconstructs the harmonic-well
shell scalar/current Gram and the force-sum from full orbital Fourier
coefficients and analytic radial beta-function integrals.

`independent_checks_001` correctly remains a failed evidence record. Its
matrix, pulse, angular and harmonic-shell controls passed, and the direct
state evolution agreed closely. Its uniform absolute ODE tolerance was
insufficient for the reference's own nearly cancelling work integrals at
the two highest synthetic drive frequencies. The failing reference also
failed its own work-energy identity by the same amounts. This did not
demonstrate a defect in the analytic pulse solution.

The preserved v2 control rescales `z` by amplitude and ledgers by amplitude
squared, uses tighter componentwise reference tolerances and bounded steps,
then converts back before the unchanged comparisons. No synthetic matrix,
frequency, physical amplitude or pass gate changed.
`independent_checks_002` has status `completed` and every control passes:

- Matrix square-root/inverse errors are below `7e-16`.
- Scalar pulse/late propagation errors are below `3.2e-12`.
- Angular normalization errors are below `9e-16`.
- Harmonic-shell Gram error is about `8.14e-13`; force-sum error is about
  `1.38e-13`.
- The worst bare finite-system comparison is `4.14e-7`, and the worst
  dressed comparison is `3.38e-7`, both below the frozen `2e-6` gate.

The controls are independent implementations of the finite dynamics and
spatial/angular normalization, while sharing the audited orbital library.
They are not an independent solution of the entire halo continuum problem.

## Halo evidence and limits on interpretation

Reviewed baseline and compact runs have positive finite Hamiltonians,
consistent shell/spatial Gram checks and accurate finite-pulse energy and
torque ledgers. For the `(64,1024,24,10)` grid, the minimum Hamiltonian
eigenvalues are about `0.643293` and `0.731477`. The dressed and bare
works differ substantially and nonuniformly across the forcing band,
showing that the calculation contains self-consistent feedback rather
than merely frozen-background trajectories.

The final baseline and compact short-pulse results meet the contracted
one-percent work target on the reported refinement comparisons. The
compact highest frequency was spatially sensitive in the initial
refinements: work divided by amplitude squared changed from `6.1163` at
10 radial basis functions to `6.2657` at 12 and `6.4037` at 16. The
contracted 20/24-basis follow-up resolves that named error to a maximum
work difference of about `0.0756%` across all five frequencies. A separate
1152/1536 Krylov comparison on the final 24-basis grid changes work by
at most `3.47e-10` relatively. Baseline 10/12-basis work differences are
at most about `0.173%`. These are convergence observations for the
specified smooth forcing and pulse, not rigorous error bounds for every
possible perturbation.

The final compact current-basis matrix has condition number about
`2.25e11`, and its full normalized feature-Gram discrepancy is about
`0.0010414` (`0.104%`). These numerical limitations must not be hidden by
the much smaller work-ledger error. The force-sum residual for the smooth
forcing is about `1.34e-7` relatively, and the final work is stable under
the specific spatial and Krylov comparisons. Those facts support the
finite forced-response result without certifying the whole continuum
operator or all high-degree basis functions.

The late quadrupole diagnostic is much more sensitive to Krylov and
spectral choices than integrated pulse work. It must not be used as a
measured damping time, an irreversible phase-mixing rate or evidence of
thermalization. Positive injected work can remain in coherent motion.
Likewise, forcing work restricted to the original material-core radius
does not include transport and field-energy flux through that radius;
it is not net heat retained in the core. This linear `l=2` result does not
calculate a second-order spherical expansion or reverse FR01 contraction.

Cross-state comparisons also need care: the contract defines frequency
and pulse duration using each state's own `omega_dyn`. Equal pattern
ratios therefore correspond to different absolute dimensionless drive
frequencies and durations before and after compaction. Their work ratio
does not isolate compaction under one identical forcing history.

No unresolved sign, conjugation or normalization defect was found in the
corrected finite dynamics. Remaining obligations concern finite
convergence and physical scope, not a license to infer a finite-speed
scalar, continuum damping, formation or an observed galaxy response.

## Exact reviewed revisions and provenance

The listed input/output hashes in `independent_checks_001`,
`independent_checks_002`, `baseline_L64_001`, `compact_L64_001`,
`baseline_bare_001`, `compact_bare_001`, `baseline_basis12_001` and
`compact_basis16_001` were recomputed independently and matched disk.
The failed first independent run is preserved. Primary halo runs were
read and audited rather than reexecuted by this reviewer. The root ran
the independent authored controls; commands and observed software versions
are in their manifests.

| Artifact | SHA256 |
|---|---|
| `CONTRACT.md` | `2094e071a4a3497e84fda0c5fa8b4455328e3b7500055300362faa86b1223700` |
| `THEORY.md` | `f236376b0adcb109ec70aa3960ef2fc7efa8210551fbe034038006279ac874c2` |
| `response.py` | `d2232a52f7a43c8c59cc5742ce004bb88f95d1fa3c2d5fa59bac23b69ba6ae5c` |
| `response_v2.py` | `10507c6646e4ab7c52fcee93c06e560857e24aa352c6170762b26b6d2beec3e5` |
| `orbits.py` | `c2540c2c55d69a4e69dfc4844f288c3286c7adc7664ca68beead2f3ff2aed9d2` |
| `background.py` | `ef4ab9d878c297e7a569acf9beb1b74c09800a11572c0589138014096b2b6893` |
| `check_response.py` | `62f5885eeb0d5a0f4fe24554e097bed3b0e5c890e7029d366375a7118f2cfc8c` |
| `check_response_v2.py` | `70a611204123cd17223d6168f4d40bb0ac717569428944f0aa25e8cc62b2d69d` |
| `check_response_contract_v2.json` | `b2004ca0cb1a9748c3a8afa39ed2c65717efa553a4905abfd8d51d1145bf1df7` |
| `INDEPENDENT_CONTROL_AMENDMENT_A1.md` | `8c72644fb65f96c4ef9b351931dbdb8f864dfacbe4329d3d2993f67c7d01c0ea` |
| `independent_checks_001/result.json` | `a92487d3666f72e5ef368f2b6608e6201cdb358d4723121371a843144c5a5574` |
| `independent_checks_002/result.json` | `3b089226299d5f5b07ea467664ad681a8cf957581dcc2def15879469ec2706a7` |
| `baseline_L64_001/result.json` | `f348529a4d4dad1670f5b86dcef968664359be6901748f6201c24f9c9a77a05f` |
| `compact_L64_001/result.json` | `9e80062cf60655bd12eaaeaa0fae1fbcf17642cc9471038bdcc8402680fa123d` |
| `baseline_bare_001/result.json` | `0e333a0ea99d82c16ec6cd1f851c0a54665cb3cfc065f6dc9ccce1b7d5eb072f` |
| `compact_bare_001/result.json` | `76432e6f021b549746dd074fb9185585f3dd05ffe6ab2d133c52375c71703bdc` |
| `baseline_basis12_001/result.json` | `202668d17700087843ee2600dacf5530e9b91c35425e640624c473c31381ef57` |
| `compact_basis16_001/result.json` | `5cd9f9aafdb88cc043d8003ac414c9309c559233c8418404ed64fd2f6367ef6e` |

Mathematical proofreading covered the shell measure, interaction signs,
complex conjugation, real-harmonic factors, pulse and angular momentum
identities, and distinctions between finite response, continuum limits
and irreversible heat. No author scientific source was edited by this
reviewer.

## Final run status and additional checks

The final primary baseline is `baseline_basis12_001`; the compact result
is `compact_final_k1536_001`. Both retain the original `T=20/omega_dyn`
pulse. Their finite Hamiltonian minima are approximately `0.643288` and
`0.722884`. The final work divided by forcing amplitude squared is:

| Pattern ratio | Baseline | Compact endpoint |
|---:|---:|---:|
| 0.25 | 0.26996320 | 2.55780955 |
| 0.5 | 0.00286537 | 4.44069050 |
| 1 | 6.78276863 | 2.30146087 |
| 2 | 0.01779639 | 9.77967669 |
| 4 | 187.53469433 | 6.43723520 |

Each column uses its own state's dynamical frequency as specified above;
the rows do not compare identical absolute forcing histories. The
optional diffuse control's final Hamiltonian minimum is approximately
`0.655094`, and its five works are `0.32658360, 0.00412339, 6.74968575,
0.01864316, 185.42997092`. Its two reported resolutions differ by less
than one percent in each work.

`check_bare_exact.py` supplies a further actual-halo check that bypasses
Krylov: for each active harmonic it evaluates
`z_n(T)=amplitude*nu_n*b_n*pulse_integral(nu_n,T)` and directly sums
energy and angular momentum. This formula is correct for zero feedback.
The result `bare_exact_001` passes for both actual backgrounds, with
maximum comparison error approximately `2.19e-12`. It shares the
analytic pulse function, whose normalization and resonances were already
checked independently against direct integration.

The `T=40/omega_dyn` experiments have a narrower status. Baseline work is
stable under its reported 1152/1536 Krylov comparison. Its strongly
frequency-dependent change from the short pulse supports a finite-pulse
response interpretation, not a universal work-proportional-to-time law.
The longer compact pulse remains **numerically inconclusive**: the same
Krylov change moves some works substantially, including about 16% at
pattern ratio 2 when normalized by the earlier result. Excellent internal
energy conservation does not resolve that evolution error. Both versions
are retained. Late-time quadrupole observables remain unverified for
physical damping interpretation in all cases.

All listed input/output hashes for the additional final, bare-exact,
20/24-basis, long-duration and diffuse manifests were independently
recomputed and matched disk. Their process status is `completed`; this
does not override the explicitly inconclusive longer compact pulse.
The initial failed independent control remains a failed record.

| Additional artifact | SHA256 |
|---|---|
| `check_bare_exact.py` | `efcb571f065ef44020e6d325cab19a10b6adfbfa3e5fb2d46c7f08b1b5369cda` |
| `AMENDMENT_A2.md` | `969d94b92621c60167e3b63536cb354fdfb79a817d3813ec4d6ade20267eed61` |
| `bare_exact_001/result.json` | `f80c3a5d2c86d2d29f93bc8b520175c386004e098c0b400ccc099af9095e2754` |
| `compact_basis20_001/result.json` | `433b9e7c535c7bdb50c3479a70dd33dd7925590f4a92bd7655bcdeb51a39c879` |
| `compact_basis24_001/result.json` | `80283198ba2d78105ab02504c45ce5d4b2eb54c2b1575506e60cb9e490e59e23` |
| `compact_final_k1536_001/result.json` | `f7e77b48158ef6616c3f0b065c8fc88c6542ad11d3fad3c0af8a84d5d88d0cc7` |
| `baseline_long_k1152_001/result.json` | `31a6b8130fd6d1fcce42b36ace83244df430e941889f635bbd33d1933f2e4263` |
| `baseline_long_k1536_001/result.json` | `3744d446622b9ea46ad3a8aaaa12d69026d77d8be5232aff6df4cab6800b57be` |
| `compact_long_k1152_001/result.json` | `74e070e44d64007e1b5b1cf521b0a4b645c2db7b812a4605c89af8a969df69bf` |
| `compact_long_k1536_001/result.json` | `57147cfabe648195873b34fc102a277024d90e0002e704371b2029f4f88dc522` |
| `diffuse_l1_001/result.json` | `d6a90d85b1bf245f0667b39c3d6272e1212b561e65f247d2ee6861676e679cfb` |
| `diffuse_l2_001/result.json` | `abc7c45d5c58ccfd1e5ddb5ff9d2842cebdb2116a7111e9ee444fd968c147c98` |

Final verdict remains a validated finite kinetic response in the stated
fast-scalar limit and pulse domain, with the reported numerical limitations.
It does not close the finite-speed/vacuum model, infer irreversible core
heating or establish a continuum stability or damping theorem.
