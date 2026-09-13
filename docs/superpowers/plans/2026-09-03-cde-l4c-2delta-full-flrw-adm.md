# CDE-L4C-2Delta Full FLRW ADM Audit Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` to execute this plan task by task, with specification and quality review at each checkpoint.

**Goal:** Derive—not promote or insert—the complete scalar quadratic ADM action of the frozen CDE-L4C-2Delta theory on its explicit expanding flat-FLRW vacuum solution, then close the finite- and zero-wave-number Dirac chains far enough to decide whether the candidate has a hidden scalar.

**Architecture:** Add one focused symbolic module beside the existing CDE scripts. It will construct the ADM geometry from an explicit real Fourier-mode metric ansatz, expand every term of the same frozen covariant action through second order, impose only equations actually derived by the existing minisuperspace variation, and pass the generated Lagrangian to a general time-dependent Dirac routine. A separate test module will recompute identities from exposed expressions and include mutation controls; the existing principal-family scripts remain as scoped regressions rather than being silently rewritten.

**Tech stack:** Python 3, SymPy exact algebra, the repository's plain-Python test style, Git.

**Authoritative specification:** `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` and the frozen `ACTION` in `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_action_gate_2026.py`.

---

## Task 1: Freeze conventions and build failing geometry tests

**Files:**

- Create: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/test_cde_l4c_2delta_full_flrw_adm_2026.py`
- Create: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_full_flrw_adm_2026.py`

- [x] Write tests first for a real mode with
  \(N=1+\epsilon\Phi\cos(kx)\),
  \(h_{ij}=a^2e^{-2\epsilon\Psi\cos(kx)}\delta_{ij}\), and
  \(N_i=-\epsilon kB\sin(kx)\delta_{ix}\).
- [x] Require the implementation to expose the exact spatial metric, inverse, determinant, acceleration, three-curvature, extrinsic curvature, and both Laplacians before expansion.
- [x] Test identities rather than stored coefficients: `h * h_inverse = I`, the conformal-curvature formula, direct trace versus matrix trace, and the homogeneous limits `R3=a_i=D2_C=D2_K=0`.
- [x] Add a convention mutation control that flips the shift sign and must change the mixed \(B\dot\Psi\) coefficient.
- [x] Run the new test and record the expected import/API failure.
- [x] Implement `series_coefficient`, exact real-mode averaging, and `derive_full_flrw_adm_geometry()` just far enough to make the geometry tests pass.
- [x] Re-run the new test and preserve the exact command/output in the final audit record.

## Task 2: Generate the complete quadratic action from ADM ingredients

**Files:**

- Modify: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_full_flrw_adm_2026.py`
- Modify: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/test_cde_l4c_2delta_full_flrw_adm_2026.py`

- [x] Add failing tests requiring independently exposed second-order contributions from:
  `N sqrt(h) (R3 + Kij Kij - K^2 - 2 Lambda)`,
  the exact exponential correction at \(y=0\),
  `N sqrt(h) lambda_s D2(R3 - 4 D_i a^i)`,
  `N sqrt(h) lambda_K D2 K`,
  the unitary-gauge cuscuton, and `-N sqrt(h) V(T)`.
- [x] Expand \(\lambda_A=\bar\lambda_A(t)+\epsilon\delta\lambda_A\cos(kx)\) directly inside the action; do not replace it by an asserted effective multiplier.
- [x] Verify by differentiation that the quadratic MOND contribution comes from the exact primitive's Hessian and that the omitted remainder begins at cubic order in the zero-field perturbation amplitude.
- [x] Derive the vacuum background substitutions from the existing Euler equations:
  \(V=M_{\rm Pl}^2(3H^2-\Lambda)\) and
  \(M_c^2=-2M_{\rm Pl}^2\dot H\), then show all first-order tadpoles vanish before using the quadratic action.
- [x] Compare the simultaneous \(H\to0\), \(\bar\lambda_s\to0\), \(\bar\lambda_K\to0\), \(M_c^2\to0\), \(V+M_{\rm Pl}^2\Lambda\to0\) limit coefficient-by-coefficient with the already ADM-generated Minkowski Lagrangian. The comparison is computed, not asserted.
- [x] Derive the on-shell time-integration-by-parts remainder explicitly, including \(\dot A=3HA\), and verify that it cancels against the cuscuton term only after the Raychaudhuri equation is imposed. State the temporal and spatial boundary assumptions.
- [x] Add a missing-term mutation (remove the cuscuton or multiplier-background contribution) and require at least one action or constraint identity to fail.
- [x] Run tests red, implement `derive_full_quadratic_action()`, and run them green.

## Task 3: Derive the complete time-dependent Dirac chain for finite \(k\)

**Files:**

- Modify: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_full_flrw_adm_2026.py`
- Modify: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/test_cde_l4c_2delta_full_flrw_adm_2026.py`

- [ ] Add failing tests requiring momenta to be obtained by differentiating the generated quadratic Lagrangian with respect to every velocity.
- [ ] Restore the scalar spatial metric mode \(E\) before the Legendre transform, either by a second direct ADM expansion or by a separately verified linear spatial-diffeomorphism identity, and require the generated action to depend on the gauge-invariant shear \(B-a^2\dot E\). Do not count a gauge-fixed second-class pair as physical constraint removal.
- [ ] Let the velocity Hessian determine the primary constraints. Do not provide an expected primary count to the derivation routine.
- [ ] Construct the canonical Hamiltonian and total Hamiltonian from those momenta and primaries.
- [ ] Preserve every constraint with
  \(dC/dt=\partial_t C+\{C,H_T\}\), including derivatives of \(a,H,\dot H,\bar\lambda_s,\bar\lambda_K\) and any coefficients inherited from the on-shell witness.
- [ ] Iterate preservation until the rank stops changing and every remaining equation either fixes a multiplier or adds a genuinely independent constraint, with independence tested by the full phase-space Jacobian.
- [ ] Construct the actual Poisson-bracket matrix of the final independent set, its determinant/minors, symbolic rank where tractable, and sampled exact/numerical ranks away from declared singular surfaces as a cross-check.
- [ ] Compute first- and second-class counts from the null space and closure relations; derive the reduced symplectic form and phase-space dimension. Never encode an expected rank or DOF.
- [ ] Verify the scalar spatial-diffeomorphism generator from the first-class chain and show that gauge fixing \(E=0\) reproduces the existing gauge-fixed constraint system.
- [ ] Add mutation controls that delete one multiplier coupling and perturb one coefficient; require the derived chain or rank to change.
- [ ] Run tests red, implement `derive_finite_k_dirac_chain()`, and run them green.

## Task 4: Restart the homogeneous and zero-field sectors

**Files:**

- Modify: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_full_flrw_adm_2026.py`
- Modify: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/test_cde_l4c_2delta_full_flrw_adm_2026.py`

- [ ] Derive a fresh covariant \(k=0\) minisuperspace Hamiltonian in variables \((a,T,N,\lambda_s^{(0)},\lambda_K^{(0)})\) before identifying constraints; do not substitute \(k=0\) into the finite-\(k\) bracket matrix and call that the homogeneous chain.
- [ ] Expose both the substituted finite-\(k\) matrix and the restarted homogeneous chain so their difference is executable.
- [ ] Repeat the finite-\(k\) rank calculation for generic \(\bar\lambda_s,\bar\lambda_K\), for the zero-multiplier branch, and along the explicit expanding witness.
- [ ] Record every coefficient surface where rank changes. Treat the exact \(y=0\) theory separately from the \(y\to0^+\) longitudinal constitutive Hessian.
- [ ] Compute the homogeneous cuscuton constraint bracket for general \(V''(T)\), then evaluate it on the explicit quadratic-potential witness. If the witness lies on a rank-changing surface, close that special chain separately and report the irregular points.
- [ ] If a scalar pair survives, derive its reduced quadratic Hamiltonian or dispersion polynomial and test kinetic/gradient signs. If no pair survives, identify the extra independent constraint and prove its preservation.
- [ ] Add a rank-surface mutation/control and run all new tests.

## Task 5: Produce a scoped falsification/construction report

**Files:**

- Create: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/CDE_L4C_2DELTA_FULL_FLRW_ADM_AUDIT_2026-09-03.md`
- Create: `qwen_claude_field_theory/closure_2026/cde_l4c_2delta_2026/cde_l4c_2delta_full_flrw_adm_2026.out`
- Create or update: a focused manifest in the same directory containing SHA-256 hashes, Python/SymPy versions, exact commands, return codes, assumptions, and computed scope.
- Modify only if needed for truthful routing: `hunt_2026/FRIED_CHICKEN_HANDOFF_BRIEF.md`
- Modify only if needed for truthful routing: `qwen_claude_field_theory/closure_2026/one_shot_final/ONE_SHOT_COMMANDS.md`

- [ ] Make the script's `main()` print numbered checks that can fail and return nonzero on a failed derivation identity.
- [ ] State the frozen action, perturbation/gauge conventions, full generated Lagrangian, background equations, complete constraint chain, bracket matrix or a machine-readable exact representation, sector split, stability result, and precise theorem scope.
- [ ] Classify only this frozen action as `DEAD`, `OPEN`, or `ACTUALLY_CLOSED`; do not resurrect the withdrawn universal local no-go.
- [ ] If this action is dead, name the first exact gate and obstruction. If it remains open, name the single next unavoidable calculation.
- [ ] Capture a fresh `.out`, rerun, and byte-compare it.
- [ ] Hash only files actually included in this focused audit and validate every hash.

## Task 6: Regression, adversarial review, and publication checkpoint

**Files:**

- Verify only; stage only the explicit files produced by this plan.

- [ ] Run the new test module with warnings promoted to errors.
- [ ] Run its executable report and compare fresh output byte-for-byte with the committed `.out`.
- [ ] Run the existing CDE action and FLRW tests and reports.
- [ ] Run the relevant elliptic-projector, MMG/York, exact-kernel, and closure tests listed in the current handoff/one-shot command file.
- [ ] Run `python3 -m py_compile` over every new/modified Python file and `git diff --check`.
- [ ] Request an independent specification review and code-quality review; incorporate only verified findings.
- [ ] Inspect `git diff` and `git status`, explicitly excluding all unrelated dirty/untracked files.
- [ ] Commit with a scoped scientific message and push only after every reported command/status has been rechecked.
