# Conditional AQUAL and resolved-image scaling certificate

**Verdict: proved as written for the 13 explicitly conditional algebraic identities.** This is author self-review, Lean kernel checking, and a separate exact-rational countercheck—not an independent physical or empirical certification. `run_02` is the authoritative completed evidence record. No novelty, dark-energy measurement, full-theory fit or astrophysical pass/fail is claimed.

The exact claim card is `HYPOTHESES.md`. The frozen compiled source is `ConditionalScaling_v1.lean`; the convenience copy `ConditionalScaling.lean` is byte-identical. No existing Lean project or Git state was changed.

## What the certificate establishes

For **a>0 and λ>0**, at fixed geometry and profile, the joint transformation

\[
(M,a,g)\longmapsto(\lambda M,\lambda a,\lambda g)
\]

preserves the dimensionless argument \(\lVert g\rVert/a\) and multiplies \(\mu(\lVert g\rVert/a)g\) by λ. This holds for any fixed μ, not only the simple interpolation function. With supplied linear divergence, compatible scaled boundary data and a supplied fixed-geometry linear deflection projection, the corresponding source equation and projected deflection scale. For the usual positive source-sign convention take g=∇Φ; if g denotes physical acceleration −∇Φ, include that minus sign in the source/operator convention. Homogeneity is unchanged.

For the lens map

\[
\beta(\theta)=(1-\kappa)\theta-\alpha(\theta)-\Gamma\theta,
\]

the explicit transformation

\[
\alpha'=\lambda\alpha,\qquad
\Gamma'=\lambda\Gamma,\qquad
\kappa'=\lambda\kappa+1-\lambda
\]

gives \(\beta'=\lambda\beta\). Defining \(S'(b)=S(b/\lambda)\) preserves the complete surface-brightness image at every position. Continuous sources remain continuous. Any fixed deterministic observation operator, including fixed PSF convolution and pixel integration, preserves equality of those image functions. This extends beyond the earlier two-point shear elimination, but remains a known mass-sheet application.

The additional postulate

\[
a^2=(c^2G/4)\rho_{\rm DE}
\]

is algebraically preserved by \(\rho_{\rm DE}'=\lambda^2\rho_{\rm DE}\). Positive density changes for λ>0, λ≠1. **All distances were held fixed**: this is not a self-consistent cosmological family in which changing dark-energy density is shown to leave the background geometry unchanged.

| Formal obligation | What is checked | Status |
|---|---|---|
| Dimensionless argument and pointwise/field flux | Norm scaling, a>0, λ>0, real division | Proved |
| Source equation | A supplied linear divergence and fixed unit-mass source | Proved conditionally |
| Boundary transformation | A supplied linear boundary map with scaled data | Proved conditionally |
| Deflection projection | A supplied linear map containing fixed distance factors | Proved conditionally |
| Lens/source/observed image | Explicit κ and shear scaling; inverse source-coordinate scaling | Proved |
| Continuous source | Continuity preserved under fixed scalar coordinate map | Proved |
| Density-squared relation | Polynomial identity and nontrivial positive density change | Proved |
| Squared velocity moment | A supplied fixed-tracer linear force functional | Proved conditionally |

## Essential physical limits

The linear operators are assumptions encoded in their types. No analytic divergence domain, gradient/potential construction, PDE solution, regularity, uniqueness, isolated asymptotic boundary theorem or numerical convergence was formalized. A pre-existing analytic solution would additionally need its function space and boundary conditions to remain admissible under the scaling.

The external κ and Γ are phenomenological lens-plane terms. **The proof does not construct a physical mass sheet whose field may be superposed in nonlinear AQUAL.** A fixed external field, a fixed nonzero boundary condition, positivity/domain constraints or an environment prior can prevent some transformed parameters from belonging to the allowed model family. Therefore the imaging non-identifiability conclusion applies only when that family is actually allowed.

No source-size/absolute-flux calibration, time delay, absolute mass/M/L or independent dynamical constraint is assumed. Such information can restrict the family. A fixed source grid or regularization prior need not be closed under source rescaling; fixing κ=0 also removes most of the algebraic family. Those restrictions define a conditional model and cannot themselves be promoted into new observational dark-energy evidence.

The optional second-moment theorem only states Q(λg)=λQ(g) for a supplied linear functional Q. If a fixed-tracer, fixed-anisotropy, compatible-boundary Jeans/aperture construction supplies that functional, its squared dispersion scales and dynamics can constrain λ. The real-galaxy construction and its uncertainty are not certified here. The newly audited DESI spectrum remains empirical evidence with the separate limitations recorded in `../dynamics_audit/README.md`.

## Verification and genuine negative control

The compile command, run from the existing read-only dependency workspace, was:

```text
cwd: /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/euclid_for_j0332_followup_2026_11_13/l017819_quasar/identifiability_scaling/ConditionalScaling_v1.lean
```

Lean **4.34.0-rc2**, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d`, returned exit 0. All 13 printed theorem dependencies contain only `propext`, `Classical.choice`, and `Quot.sound`. There are no `sorry`, admitted declarations or new axioms in the positive source. One harmless linter suggestion prefers `simp` to `simpa`; the frozen successful source was not changed for style. Mathlib was clean at commit `85e3a25e006c35636f0e53b0e9296caca2685bc0`.

The negative control replaces the first transformed convergence term by \(\lambda\kappa+1-2\lambda\). The actual file exists and compiles far enough to produce the expected **proof error at line 80**, with the false residual equation `k * 2 - k * kappa = k - k * kappa`. Its exit code is 1; there is no missing-file, import or dependency failure. Downstream errors/`sorryAx` in the failed mutated compilation are expected diagnostic artifacts and are not part of the accepted proof.

The separately implemented Python `Fraction` calculation passed **48 flux cases, 96 lens/source-brightness cases and 12 density cases** using exact rational arithmetic. It also checks that keeping a fixed while doubling g does not produce the required simple-μ flux scaling: at a=g=1, F(2g)=4/3 whereas 2F(g)=1. The false convergence example with θ=(1,0), α=Γ=κ=0 and λ=2 yields β'=(4,0), rather than the correct (2,0). These finite examples supplement rather than replace the universal Lean proof.

`run_02_command.txt` records the full bounded computation-audit command; `contract_02.json` gives the exact declared input closure and bounds. The runner used a 300-second cap and one numerical-library thread. Both input/output hashes and the completed status validate. Installed Lean/Mathlib compiled dependencies remain trusted external library artifacts; toolchain, lock files and direct import sources are hashed, not every transitive compiled artifact.

`run_01` is preserved as a valid **failed** evidence record: its preflight text scanner incorrectly matched the English word “admit” inside a comment, so Lean was never launched in that run. The corrected scanner in `verify_scaling_v2.py` removes comments before the textual check and still requires the kernel axiom audit. Do not cite run_01 as a successful compile or as a mathematical counterexample.

## Primary-source scope and provenance

Bekenstein & Milgrom's 1984 paper gives the modified Poisson equation and isolated boundary convention in equation (3), printed page 8. The field homogeneity here is directly re-derived algebra from that form. [Primary paper](https://articles.adsabs.harvard.edu/pdf/1984ApJ...286....7B).

Schneider & Sluse 2013 §2.1, equation (1), states the standard mass-sheet transformation and source-coordinate scaling; §2.2 discusses information that can break it. This certificate is a conditional application of that known lensing algebra, not a newly discovered invariance. [Primary paper](https://orbi.uliege.be/bitstream/2268/175963/1/2013_AA_559_A37_MST_Schneider_sluse.pdf).

Both PDFs, extracted text and retrieval metadata/SHA-256 files are retained under `inputs/`. The earlier project `AqualScaling.lean` already certified related flux/mass-sheet algebra. This file makes the explicit shear/convergence model, arbitrary μ, continuous-source observation operator and squared-density scope local to the current identifiability audit.

| Artifact | SHA-256 |
|---|---|
| ConditionalScaling_v1.lean | `ad4524d3f24929571f39b96971165c74695608555473fd22024c32a060bda3e6` |
| HYPOTHESES.md | `8fcb721e8e05bf8ce3b5067d394eedc2b462ea9633c49bdea1f803caff3ae632` |
| run_02/manifest.json | `581a611328a1619f8b23024a93fd9267bce158a109bc601f41cacba20d3334ca` |
| run_02/result.json | `b26f5e1273cacbf55106fb6551d90bd978ffb4cba0f3389ed092a49b4a9c3170` |

Terminal state: compilation session **3776** returned exit 0; public-source fetch session **74839** returned exit 0. No process remains live from this formal task. No external author was contacted.
