# Independent audit: exact two-image shear elimination

**Primary verdict: proved as written.** The universal algebra in the frozen `TwoImageShear.lean` is correct. Its existence theorem together with `unique_shear` establishes the intended unique unrestricted trace-free shear. This is nuisance elimination and an identifiability limitation of two point positions; it is not a gravity-law, physical-environment or empirical-fit certificate.

## Claim card and independent derivation

Objects are real positions theta_A=(xa,ya), theta_B=(xb,yb), supplied real reduced deflections alpha_A,alpha_B, a real fixed t=1−kappa, and an arbitrary real shear center c. Let d=theta_A−theta_B and D=dx²+dy². Hypothesis D!=0 means the positions are distinct. There is a unique real pair (g1,g2), without a magnitude prior, such that the two source vectors

    b_i = t theta_i − alpha_i − Gamma (theta_i−c),
    Gamma = [[g1,g2],[g2,−g1]],

are equal. With v=t d−(alpha_A−alpha_B), the pair difference equation is

    [[dx,dy],[-dy,dx]] [g1,g2]^T = [vx,vy]^T.

The determinant is D, and direct matrix inversion gives

    g1=(dx vx−dy vy)/D,
    g2=(dy vx+dx vy)/D,
    g1²+g2²=(vx²+vy²)/D.

This freshly reconstructed derivation matches both Lean definitions, the inverse-component lemma, uniqueness lemma and norm lemma. The arbitrary center cancels from the difference. The proof does not require spherical symmetry, an SIE or any other field law. It does require two distinct positions and permits arbitrary real shear magnitude and t. If d=0, unequal supplied deflections cannot be absorbed by shear, and equal supplied deflections give non-uniqueness; the denominator hypothesis correctly excludes both exceptional cases.

Dependency graph: real field cancellation + polynomial ring identities -> inverse components/norm; nonzero D + two linear equations -> uniqueness; inverse components + expanded pair difference -> common source; positivity of nonzero real squares -> distinct-pair denominator. All leaves are internal Lean/mathlib algebra. No external physical theorem or numerical PDE enters.

## Implementation and coordinate dictionary

`host_control/fit_host.py::Host.rays` lines 26–32 uses A and C for the two quasar positions, `d=A−C`, `v=d−(pure(A)−pure(C))` and exactly the two inverse formulas above. It is the theorem's t=1 (zero external convergence) case. `pure` is the already geometry-reduced deflection, in arcseconds. `lens_models.py::sie_deflection` adds `(g1 X+g2 N, g2 X−g1 N)` about the sky origin: therefore instantiate the theorem with c=(0,0), not with the SIE mass center. The independent SIE mass-center parameters affect only `pure`; the theorem allows arbitrary supplied deflections and remains applicable.

Both Python coordinate components are X west and N north, with consistent angular units. No east/west sign change is needed within this dictionary. Under an external change to an east-positive convention the off-diagonal shear convention must also be transformed; the certificate does not silently convert sky bases or position angles. The host source center is subsequently set to A−total(A), and the continuous inversion subtracts that same center from its lens equation. This correctly centers the common point source. The same formulas remain in the inspected `fit_host_v4.py` and `arbitrary_field_adapter.py`, though the recorded source-hash contract specifically covers the originally requested `fit_host.py` and `lens_models.py`.

For a finite imposed shear bound gamma_max, the exact norm identity implies a two-position feasibility condition `|t d−Delta alpha| <= gamma_max |d|`; unlimited shear is essential to the unconditional existence conclusion. The certificate does not show that a fitted shear satisfies an environmental prior. It also does not constrain image parities, local magnifications, additional images, an extended source, or flux consistency. Independent quasar amplitudes in the host control cannot turn the point-position elimination itself into a flux-ratio test.

## Obligations and evidence

| Obligation | Outcome |
| --- | --- |
| Quantifiers, real domain and denominator | Passed; D!=0 is explicit |
| Matrix inverse, signs, common center | Passed by independent derivation |
| Existence and uniqueness | Passed; existence and uniqueness are separate proved lemmas |
| Norm identity and axis-aligned/zero-v limits | Passed; dx!=0,dy=0 reduces to g1=vx/dx,g2=vy/dx; v=0 gives zero shear |
| Python rays/coordinate convention | Passed at the frozen source hashes |
| Unchanged original Lean compilation | Passed, exit0 |
| All five lemma axiom dependencies | Passed; only propext, Classical.choice, Quot.sound |
| False arithmetic mutation rejection | Passed; actual unsolved norm goal, not missing file/import |
| Observations, field error, physical priors, full image fit | Out of scope |

`result.json` records all commands, SHA256 inputs before/after, compiler and log hashes. The accepted frozen source SHA256 is `e289fd0fa38c939e1a1d24e667b0623cb93006c80044f1ee50a003acecbee954`. The independently invoked compiler was Lean 4.34.0-rc2, commit 6a10ac8c22beadecabdbb0919c2b50214762f91d. It compiled the unchanged absolute original file, then an owned copy with all five `#print axioms` commands. Neither accepted source contains sorry/admit or introduces custom axioms.

The owned negative control multiplies the norm theorem's right-hand side by 2, leaving its proof unchanged. It is false already at dx=1,dy=0,vx=1,vy=0 (1=2). `mutation_compile.log` reports an unsolved polynomial goal at `TwoImageShear_FALSE.lean:25:51`, exit1; the verifier affirmatively requires a proof-failure diagnostic and rejects missing-file/import errors. The failed mutation's printed `sorryAx` is Lean's diagnostic placeholder after the failed proof, not an accepted certificate. The positive axiom logs contain no sorryAx.

Reproduce from repository root:

    python3 euclid_for_j0332_followup_2026_11_13/l017819_quasar/formal/independent_review/verify.py

This writes only the review directory and uses the existing read-only `fable_independent_2026/lean_2026` environment. Each compiler subprocess has a 90-second cap. The first attempted verifier invocation had an incorrect local repository-root path and stopped before launching Lean; it was corrected before the recorded successful run and was never counted as a negative control. The canonical source/project were not edited. No gap remains in the scoped algebraic statement; any extension to physically bounded nuisance priors or observational adequacy is a separate task. No novelty or breakthrough claim is made.
