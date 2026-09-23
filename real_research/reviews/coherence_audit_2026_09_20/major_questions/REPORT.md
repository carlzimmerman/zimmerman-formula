# Major-question audit, September 20, 2026

**Primary verdict: refuted, with a valid manufactured counterexample.** The
examined Navier–Stokes campaign's implemented nonlinear operator is not
`(u·∇)u`. Eight scripts use its transposed-Jacobian contraction instead. This
invalidates their interpretation as numerical evidence for the stated NSE
systems. It does not disprove the separate conditional window theorem, the
external Lean development, or any regularity conjecture.

Base repository revision: `3aaed026d55f65b38733316cb63c432290a339e1`, dirty
workspace. The surveyed source revisions and SHA-256 hashes are recorded in
`source_inventory.json`. Only files in this audit directory were written.

## Exact claim and decisive witness

On the 2π-periodic three-torus, define the Jacobian by
`D[i,j] = ∂_j u_i`. True advection is `A_i = Σ_j u_j D[i,j]`.
The code uses `B_i = Σ_j u_j D[j,i] = ∂_i(|u|²/2)`.
For the usual Leray projector `P`, `PB=0`, whereas `PA` need not vanish.

Take the smooth, divergence-free, mean-zero field

```
u(x,y,z) = (sin y, 0, sin x).
A = (0, 0, sin y cos x),       PA = A.
B = (sin x cos x, sin y cos y, 0),       PB = 0.
```

The true projected nonlinearity has spatial RMS exactly `1/2`.
The source implementations with a correct projector return less than
`3.3e-32` RMS for this fixture. Every product mode is at wave number at most
2, below the audit's cutoff 4 and Nyquist 6: aliasing cannot explain the
discrepancy. An independent symbolic Jacobian calculation verifies the
continuum identities exactly. The test extracts actual function ASTs and
executes their unchanged bodies; it does not import scripts and accidentally
launch their large top-level experiments.

The exact locator exemplifying the defect is
`deepseek_push/navier_stokes_attempt/N04c_equilibrium_long.py:109–123`.
Its own diagnostic at lines 125–136 repeats the index reversal even though
the docstring explicitly defines `derivs[i][j]=∂_j u_i`.

| Source | Exact effect of the audited code |
|---|---|
| `N03_supbarrier.py:78`, `N03b_beta_family.py:50` | Transposed contraction; correct projection removes it |
| `N04_galerkin.py:59`, `N04b_equilibrium.py:89`, `N04c_equilibrium_long.py:109` | Same; classical no-drag branch reduces to forced Stokes in resolved Galerkin arithmetic |
| `N09_twofluid_galerkin.py:148` | Same missing fluid advection; separate gravity term is unprojected in its RHS |
| `N05_window_theorem.py:333` | Also differentiates the outer initial `uh`, not the current argument; later evolution is a frozen-Jacobian system, so it must not simply be called Stokes |
| `N12_selfseeding.py:106` | Also has an incorrect projector: `INVK[1:]=1/Ksq[1:]` zeros the entire `k_x=0` plane, allowing a longitudinal gradient through |

The N05 closure defect is directly tested: doubling the current velocity
while keeping its captured initial state fixed doubles its purported
quadratic nonlinearity, rather than multiplying it by four. The real-space
RMS difference from quadratic scaling is exactly 1 for the chosen fixture
up to floating error. In N12 the surviving gradient is
`(0,sin y cos y,0)`; its divergence is `cos(2y)`, with measured maximum 1.
These are two further source-level errors, distinct from the transpose.

## The useful exact theorem: energy tests are blind to this error

For every real velocity vector and every real matrix,

```
u · (D u) = u · (Dᵀ u).
```

Thus an energy-contraction test cannot distinguish the correct and incorrect
nonlinearities. For smooth divergence-free periodic fields both also give
zero integrated nonlinear energy input. This explains how the campaign's
energy-identity checks can pass while the dynamics is wrong; additional
energy checks alone would not repair the evidence.

`AdvectionBridge.lean` proves six precise algebraic statements: the
half-square derivative polynomial, this energy blindness, annihilation of
gradient Fourier polarizations by the projector, the exact local witness,
its zero transposed contraction, and its nonzero surviving transverse
polarization. Fresh compilation prints only `propext`, `Classical.choice`
and `Quot.sound`. Calculus, FFT semantics, and continuum PDE existence are
not formalized by these six lemmas. No mathematical novelty is claimed for
these classical identities; their value here is locating the exact failed
implementation-to-equation implication.

## Constructive repair and bounded comparison

`run_final/corrected_galerkin.py` is an isolated, runnable copy of the
original N04c `galerkin` function with three scientific edits:

1. Contract velocity with the derivative direction, giving `Σ_j u_j ∂_j u_i`.
2. Subtract its projection in the evolution RHS. The original adds it;
   this sign was hidden by its zero projected value.
3. Correct the matching diagnostic contraction.

The returned state, initial state, forcing and wave-number array are added
only for audit diagnostics. The original source files are unchanged.
The comparison uses `n=12`, `ν=.05`, `A=1`, no drag, `T=2`, NumPy seed 7,
RK4 steps `.004` and `.002`, and exactly the source forcing and initial-state
normalization. It is not a repeat of the campaign's `n=32,T=200` run.

| Endpoint/invariant | Original | Corrected, dt=.004 |
|---|---:|---:|
| RMS difference from the exact forced Stokes solution | `2.74e-15` | `0.124103236` |
| Maximum divergence | `6.76e-17` | `1.11e-16` |
| Absolute nonlinear energy contraction | `1.03e-18` | `1.03e-18` |
| Integrated energy residual | `5.09e-8` | `6.75e-8` |
| Final speed supremum | `1.36549316` | `1.36593144` |

The corrected field changes by only `2.59e-13` RMS when the time step is
halved, while the original-to-corrected difference is `0.1241` RMS. The
integrated energy residual improves by a factor of four, as expected for
the trapezoidal quadrature used in that diagnostic. The original matches
the independently evaluated exact Stokes solution

```
u_hat(t,k) = exp(-ν|k|²t) u_hat(0,k)
           + (1-exp(-ν|k|²t))/(ν|k|²) f_hat(k).
```

The near agreement of the two speed maxima therefore also fails to validate
the vector evolution. The distinguishing observable is the actual field or
a projected nonlinear mode. This bounded repair provides a usable starting
point; it certifies neither spatial convergence nor long-time behavior.

## Other major questions inspected

**Riemann hypothesis.** Read `RH16_zeta_rar.py`, `lean/RH16L_zeta_rar.lean`,
`lean/RH13L_doubled.lean`, and the September 17 `RH19_ATTRIBUTION_FIX.md`.
The certificate's polynomial factor identities are genuine algebra; it
explicitly excludes the infinite-product convergence and global zero
criterion. The doubled completion explicitly admits an off-axis-root
counterexample. RH19 already retracts the novelty framing of RH16–18.
No new completed implication to RH was found in this bounded source survey.
The missing positive route remains a property of the actual completed zeta
that controls every zero, rather than reflection symmetry or a finite grid.
The historical attributions in RH19 were not independently authenticated
here and are not used to establish this audit's new result.

**Yang–Mills.** Read the final conclusion, `lean/YM05_lattice_gap.lean`,
`YM06_capped_gap.py`, and `lean/YM06_capped_gap.lean`. The previous audit's
YM07 failure was not rerun. A distinct source-to-target gap remains in YM06:
it assigns `ω₁=π c_s/(2L)` and proves that number positive, but provides no
self-adjoint physical fluctuation operator or domain that identifies it as
the lowest mode of the capped halo. Its tested `sin(πx/(2L))` solves a
one-dimensional mixed-boundary problem. Positivity of that assigned number
does not prove a three-dimensional halo gap. Constant Neumann modes and
coupling to an exterior region illustrate why a finite radius alone cannot
supply the missing coercivity hypothesis. The source itself leaves the
boundary identification as follow-up. A constructive next theorem would be
an energy/coercivity inequality for an explicitly defined radial fluctuation
operator, including its weight, center condition, cap condition and exterior
matching. This is separate from an SU(3) continuum mass-gap theorem.

**External NS formalization.** The authorized local source copy is
`openai/NavierStokesAndEuler`, revision
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. Its actual definition in
`NavierStokes/ProblemStatement.lean:59–64` applies the spatial Fréchet
derivative to the velocity, agreeing with `D u`, not `Dᵀ u`.
That local primary-source definition was read directly; this audit does
not revalidate its full proof or infer current external referee status.
Also, the campaign's N14 prose says its R3 candidate is spatially periodic,
whereas the actual R3 `CandidateProperties` has no periodicity hypothesis
and its module states that explicitly. This is a transcription error, not
evidence against the external theorem.

## Dependency and obligation ledger

```
source derivative indices -> implemented B=Dᵀu -> gradient/projection kill
                                                -> incorrect NSE surrogate
mathematical A=Du -> manufactured transverse mode -> decisive discrimination
                                  -> isolated repaired evolution
```

| Obligation | Status |
|---|---|
| Test field is smooth, periodic, divergence-free and resolved | Passed, exact symbolic derivation |
| Source functions implement true advection | Failed, eight source locators |
| Original N04c evolves NSE in the classical no-drag case | Failed; exact Stokes control reproduced |
| Energy identity can authenticate the nonlinear contraction | Failed, universal Lean identity |
| Repaired finite run obeys projection/energy invariants | Passed at the stated finite bound |
| Repaired results converge as grid size grows | Not addressed |
| Window theorem's continuation source hypotheses | Conditional; not reauthenticated in this pass |
| YM06 cap selects the claimed fluctuation operator and domain | Not addressed by source certificate |
| RH kernel algebra controls all actual zeta zeros | Incomplete in examined sources |

The strongest safe continuation is to validate each lane's differential
operator against a manufactured non-gradient mode before rerunning its
physical or regularity experiments. For NS the remaining task is the full
corrected campaign, including N05 closure and N12 projector repairs, before
using those numerical results as evidence. For RH and YM, the missing
operator/function-domain implication must be stated before more scalar
arithmetic or theorem counts are treated as progress on the major problem.

## Provenance and reproduction

`run_final/manifest.json` records the successful computation with actual
argv, eight source hashes before/after, result hashes, seed, software and
resource bounds. `run_lean/manifest.json` separately pins the Lean file and
Mathlib host manifest and records fresh compilation. Both are version 2
mathbox manifests validated with the repository root.

The earlier `run/` is a failed audit-harness attempt (missing extraction
global `INVK`), preserved transparently. `run_verified/` succeeded but its
contract's summary sentence was overly broad about N12; `run_final/`
supersedes it using the corrected explicit contract. No lane-source data
were changed between these runs.

To reproduce use `check_advection.py OUTPUT_JSON`, with a pre-existing
output directory, or execute the exact argv in the checked manifest after
choosing a fresh output directory. `check_lean.py OUTPUT_JSON` runs the
existing repository Lean host. The isolated corrected function can be
imported directly from `run_final/corrected_galerkin.py`.
