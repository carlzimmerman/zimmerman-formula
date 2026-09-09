# Localized V4 Clock–York Action Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and falsifiably test a local constrained representation of the surviving V3 exponential clock action, preserving its exact static MOND branch while deriving the auxiliary Euler–Lagrange equations and the nonzero-​k / homogeneous Dirac mode counts.

**Architecture:** Replace each spatial pseudoinverse by an elliptic auxiliary field and multiplier: a scalar χ for the trace/Hodge inverse, a co-closed one-form (A_i) for the transverse Hodge inverse, and a transverse-traceless tensor (Q_{ij}) for the York inverse. The prototype will use a first-order ADM quadratic reduction for the constraint audit, while a separate symbolic module records the covariant localized action and its formal variations. Eliminating the auxiliaries algebraically must reproduce the V3 response at fixed metric; the Dirac engine must then determine whether the localization adds zero propagating modes.

**Tech Stack:** Python 3.9, SymPy exact algebra, NumPy/SciPy only for numerical rank controls, existing `construct.canonical_constraints`, JSON manifests, optional Lean-ready exported polynomial identities (no Lean dependency assumed).

**Spec:** `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/PATTERN_SYNTHESIS_2026-09-09.md` and `PARAMETER_FAMILY_GATE.md`.

## Global Constraints

- Preserve the exact constitutive law μ(y)=1−exp(−y) and the measured coupling (G_N=2G_b/C).
- Do not assign PPN parameters or DOF counts; derive them from the varied equations and actual Poisson-bracket matrix.
- Treat (k=0) and (k\ne0) separately; never infer the homogeneous rank by taking a limit of a nonzero Fourier mode.
- Keep the clock scalar explicitly counted; localization fields must be shown auxiliary or the candidate remains open.
- Preserve unrelated dirty worktree changes and stage only this new directory plus the plan.
- A zero exit code is execution evidence only; the final report must list non-claims and unresolved gates.

---

### Task 1: Freeze the localized action contract and write the failing controls

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/contract.json`
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/test_localized_v4.py`
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/README.md`

**Interfaces:**
- `test_localized_v4.py` imports `localized_action.action_data()` and
  `localized_dirac.flat_scalar_blocks()`.
- `action_data()` returns the action terms, coefficient witness, kernel
  conventions, and a list of explicit non-claims.
- `flat_scalar_blocks()` returns symbolic quadratic Lagrangians for the
  physical scalar `(z,n,B)`, trace localizer `(chi,lambda_chi)`, transverse
  localizer `(A_T,lambda_A)`, and TT localizer `(Q_+,Q_x,lambda_Q)`.

- [ ] **Step 1: Write the failing tests first.**

```python
def test_localizer_equations_are_present():
    data = action_data()
    assert "Delta_h chi - D_iD_j K^ij" in data["constraints"]
    assert "H1 A - P_T div K" in data["constraints"]
    assert "H_TT Q - P_TT(3Ric)" in data["constraints"]

def test_nonzero_and_zero_mode_cases_are_not_merged():
    blocks = flat_scalar_blocks()
    assert blocks["k_nonzero"]["kernel_dimension"] != blocks["k_zero"]["kernel_dimension"]

def test_elimination_identity_is_not_assumed():
    result = eliminate_localizers()
    assert result["scalar_identity"] is True
    assert result["vector_identity"] is True
    assert result["tt_identity"] is True
```

- [ ] **Step 2: Run the test to verify it fails for the expected missing-module reason.**

Run from the new directory:

```bash
python3 -m unittest -v test_localized_v4.py
```

Expected: import failure because `localized_action.py` and `localized_dirac.py` do not yet exist.

- [ ] **Step 3: Add only the contract and README text.** Document the localized action:

\[
S_{\rm loc}=S_{\rm EH}+S_f-\ell\theta^2+\eta_U U^2+
\eta_XU\chi+\eta_V(2A\cdot J-A\cdot{\cal H}_1A)+
\eta_{TT}(K_{TT}^2+2Q\cdot R_{TT}-Q\cdot{\cal H}_{TT}Q)
+\lambda_\chi(\Delta_h\chi-D_iD_jK^{ij})
+\lambda_A^i(D_iA^i)+\lambda_Q^{ij}(D^kQ_{ki},Q^i{}_i).
\]

State that (J_i=D^mK_{im}), (U=K-\langle K\rangle-\chi), and that the
multiplier form is a local representation of the V3 pseudoinverse only after
the auxiliary equations and kernel conditions are solved.

- [ ] **Step 4: Re-run the test and record the new failure location.**

Expected: failure moves from missing files to missing functions, confirming the tests exercise the intended API.

---

### Task 2: Implement the exact flat-sector localization and elimination identities

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/localized_action.py`
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/eliminate_localizers.py`
- Modify: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/test_localized_v4.py`

**Interfaces:**
- `action_data() -> dict` exposes exact coefficients `C=5/3`, `ell=1/100`, `eta_U=1/12`, `eta_X=1/3`, `eta_V=-1/3`, `eta_TT=-1/6` and the symbolic action terms.
- `eliminate_localizers() -> dict` solves the χ, A, Q, and multiplier equations for a nonzero flat Fourier mode and returns exact equality checks against the V3 pseudoinverse terms.
- `localized_static_variation() -> dict` returns independent Φ/Ψ Euler equations and the exponential μ equation.

- [ ] **Step 1: Add the scalar localizer test.** Assert that varying λχ gives χ=`Delta` inverse of `D_iD_jK^ij`, and varying χ gives the local equation used in elimination.
- [ ] **Step 2: Run only that test and confirm it fails before implementation.**
- [ ] **Step 3: Implement exact SymPy expressions.** Use a nonzero Fourier symbol (K=k^2), retain the sign of the negative Laplacian explicitly, and solve rather than substitute the desired inverse.
- [ ] **Step 4: Add vector and TT elimination tests.** Use a transverse vector and two TT polarizations; require the resulting quadratic forms to equal (V\,H_1^\dagger V) and (R_{TT}H_{TT}^\dagger R_{TT}).
- [ ] **Step 5: Add independent static variation.** Vary Φ and Ψ separately from the localized action with (K_{ij}=0), checking Δ(Ψ−Φ)=0 and ∇·[μ∇Φ]=4πG_Nρ.
- [ ] **Step 6: Run the focused tests and preserve exact expressions in JSON.**

---

### Task 3: Derive the localized ADM Dirac structure

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/localized_dirac.py`
- Modify: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/test_localized_v4.py`

**Interfaces:**
- `flat_scalar_blocks() -> dict` returns the (k\ne0) and (k=0) quadratic Lagrangians with variables, velocities, and primary candidates.
- `dirac_report(mode: str) -> dict` computes the actual Hessian nullspace, primary constraints, every preservation equation through closure, the Poisson-bracket matrix, rank, and first/second-class counts.
- `constraint_matrix(block) -> SymPy Matrix` exposes the unrounded matrix for audit.

- [ ] **Step 1: Write tests for controls before the localized system.** Reuse the existing GR and one-scalar controls, requiring their known counts to be regenerated by the same engine rather than copied.
- [ ] **Step 2: Run controls and confirm the new module fails to import.**
- [ ] **Step 3: Implement the nonzero-mode block.** Include (n,B,\chi,\lambda_\chi,A_T,\lambda_A,Q_+,Q_\times,\lambda_Q), with no time derivatives assigned to localizer fields or multipliers unless they arise from the explicitly retained (K_{ij}) constraint term.
- [ ] **Step 4: Iterate preservation until closure.** A missing preservation equation or inconsistent rank must raise an error rather than be reported as a count.
- [ ] **Step 5: Implement a distinct (k=0) minisuperspace block.** Remove inverse-Laplacian divisions and compute the homogeneous rank independently.
- [ ] **Step 6: Assert only derived structural properties.** The tests may require that all localizer variables are eliminated in the healthy witness, but they must inspect the returned matrix and derive its rank; no rank/determinant literal may be embedded as the computation’s input.
- [ ] **Step 7: Run the focused Dirac tests and save the full matrices.**

---

### Task 4: Add the nonlinear-variation and causal-residue gate

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/metric_variation_gate.py`
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/causal_response_gate.py`
- Modify: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/test_localized_v4.py`

**Interfaces:**
- `metric_variation_gate() -> dict` differentiates the localizer equations with respect to lapse, shift, and spatial metric, including the variation of the mean projector and the kernel constraints.
- `causal_response_gate() -> dict` evaluates all six conserved source seeds and returns denominator factorization, spatial-pole count, and tensor/clock cone factors.

- [ ] **Step 1: Add a failing finite-difference test for the moving metric weights and projectors.** The test must compare action directional derivatives against direct finite differences on the same periodic cochain discretization used in `operator_variation.py`.
- [ ] **Step 2: Run it and confirm the new gate is missing.**
- [ ] **Step 3: Implement the Fréchet variations.** Include δ(A^{-1})=−(A^{-1})(δA)(A^{-1}), moving mean projector, Hodge/York constraint variations, lapse weight, and δ(K_{ij}).
- [ ] **Step 4: Add the six-source causal check.** Require the localized action to reproduce the existing V3 response after auxiliary elimination, then inspect whether any unpaired (k^2) denominator or instantaneous branch remains.
- [ ] **Step 5: Run numerical derivative and exact Fourier checks.** Record tolerances and raw output in a run manifest.

---

### Task 5: Optional Lean-ready algebra export and research report

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/lean_ready_identities.json`
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/REPORT.md`
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/manifest_contract.json`
- Create: `qwen_claude_field_theory/closure_2026/localized_v4_action_2026/run_localized_v4.py`

**Interfaces:**
- `lean_ready_identities.json` contains exact polynomial/rational identities with variable domains and no floating targets; it is an export, not a proof.
- `run_localized_v4.py` writes a JSON result below `run_001/` for the computation-audit runner.

- [ ] **Step 1: Export only identities independently verified by SymPy.** Include the static μ identity, the three elimination identities, and the response denominator factorization.
- [ ] **Step 2: Write the report with a requirement-by-requirement status table.** Distinguish derived, finite-verified, conditional, and still open; explicitly include PPN α₁/α₂/α₃, FLRW perturbations, y→0, empirical fits, and Lean availability.
- [ ] **Step 3: Run the bounded computation runner with pinned inputs and validate its manifest.**
- [ ] **Step 4: Run the complete localized package test suite and existing clock-construction regression tests.**
- [ ] **Step 5: Run `git diff --check`, inspect the exact diff, and commit only the plan and localized package if staging is authorized.**

## Self-review checklist

- [ ] The plan has a single subsystem and does not silently claim the full ten-gate theory.
- [ ] Every new production function has a test written before its implementation.
- [ ] (k=0) and (k\ne0) are separate code paths and separate reports.
- [ ] No expected determinant, rank, PPN number, or DOF count is hard-coded as an input.
- [ ] A failure of the localized action remains a useful constructive obstruction, not a relabelled completion.
