# Local Winding Clock MOND Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the first executable action-derived gate for the local cumulative-winding clock MOND candidate defined in `docs/superpowers/specs/2026-09-09-local-winding-clock-design.md`.

**Architecture:** Build a focused package under `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/`. The IC1 exponential MOND sector is imported only through its explicit primitive and static equations; the new (Q,lambda) memory sector and canonical massive cold scalar are varied independently. Each gate returns derived expressions, residuals, matrices, and a scoped status so a passing computation cannot be mistaken for full-theory closure.

**Tech Stack:** Python 3, SymPy exact algebra, NumPy/SciPy numerical checks, JSON manifests, and a noncompiled Lean-ready statement file because no Lean executable or lake project is present.

**Spec:** `docs/superpowers/specs/2026-09-09-local-winding-clock-design.md`

## Global Constraints

- Keep the primary winding rate signed: \\(\mathcal W(\Theta)=\Theta\\); test the smooth absolute-value rate only as a negative control.
- Preserve the exact constitutive law \\(\mu(y)=1-e^{-y}\\) on the baryon-only static branch.
- Couple baryons and the cold scalar to the same physical metric (g_{\mu\nu}); derive the baryon Ward identity independently.
- Compute ranks, determinants, constraint classes, and degree counts from generated matrices; do not enter target values as assertions.
- Treat (k=0), (k\ne0), (Q=0), and the \\(\varepsilon_w\\to0^+\\) control as separate sectors.
- Label the local winding calibration as a bounded empirical/assembly diagnostic, not as a cosmological derivation.
- Do not claim full PPN, nonlinear stability, or complete theory closure until their gates are actually implemented.

### Task 1: Derive the single action and exact static identities

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/action_variation.py`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/test_action_variation.py`

**Interfaces:**
- `derive_action() -> dict` returns the displayed IC1 potential, the exponential primitive residual, the (Q)- and (lambda)-Euler derivatives, the canonical cold-scalar Euler derivative, and all simplification residuals.
- `static_branch() -> dict` returns independent lapse/conformal static equations, the baryon-only MOND residual, and the high-acceleration measured-(G) expression.

- [ ] **Step 1: Write failing tests** for exact primitive differentiation, (E_\lambda=n^\mu\nabla_\mu Q-\Theta), (E_Q), (E_{\chi_c}), and the baryon-only static residual.
- [ ] **Step 2: Run the focused test** with `python3 -B -m unittest -v qwen_claude_field_theory/closure_2026/local_winding_clock_2026/test_action_variation.py`; confirm failure because the module is absent.
- [ ] **Step 3: Implement exact SymPy variation**. Use (U(c)=(1-c)[\ln^2(1-c)-2\ln(1-c)+2]-2), (w=(u-1)\ln N), and (mathcal L_c=X_c-m_c^2\chi_c^2/2). For the static branch vary (Phi,Psi) independently before imposing (Phi=\Psi).
- [ ] **Step 4: Run the focused test** and require every returned residual to simplify to zero; report the actual expressions in JSON-compatible strings.
- [ ] **Step 5: Commit** the two files with `git add .../action_variation.py .../test_action_variation.py && git commit -m "derive local winding action identities"`.

### Task 2: Compute the memory-sector Dirac chain

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/dirac_gate.py`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/test_dirac_gate.py`

**Interfaces:**
- `dirac_report(mode: str) -> dict` accepts `"k_nonzero"` or `"k_zero"` and returns the velocity Hessian, primary/secondary constraints, actual Poisson matrix, computed rank, first-/second-class nullities, preservation residuals, and memory phase-space count.
- The homogeneous test uses the ADM memory term (a^3\lambda(\dot Q-N\Theta)), with \\(\Theta=\dot a/(Na)\\), plus the canonical cold scalar term (a^3e^{-\beta Q}[\dot\chi_c^2/(2N)-Nm_c^2\chi_c^2/2]). The absolute-value \\(\mathcal W_{\rm abs}\\) block is evaluated separately and never merged into the primary result.

- [ ] **Step 1: Write failing tests** that require the generated constraint list to contain the momenta returned by differentiating the Lagrangian, require the Poisson matrix to be antisymmetric, and require preservation residuals to vanish after solving actual multiplier equations.
- [ ] **Step 2: Run the focused test** and record the expected missing-module failure.
- [ ] **Step 3: Implement the Legendre map** for (a,Q,\lambda,N,\chi_c). Derive (p_\lambda) and the (p_Q)-λ relation from the velocity definitions, then derive secondary constraints by Poisson brackets with the unmodified Hamiltonian.
- [ ] **Step 4: Build separate (k\ne0) and (k=0) blocks**. Use a symbolic spatial wave number in the nonzero block and substitute it to zero only after constructing the full matrix. Solve multiplier preservation from the actual matrix and report singular cases instead of assigning a rank.
- [ ] **Step 5: Run the focused test** and inspect the matrix, determinant factors, and residuals. A one-pair clock result is accepted only if it is produced by the calculated rank/nullity.
- [ ] **Step 6: Commit** with `git add .../dirac_gate.py .../test_dirac_gate.py && git commit -m "derive local winding memory Dirac chain"`.

### Task 3: Derive weak-field potentials and Ward identities

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/weak_field_ward_gate.py`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/test_weak_field_ward_gate.py`

**Interfaces:**
- `weak_field_report() -> dict` returns separately varied \\(\Phi\\)- and \\(\Psi\\)-equations, the baryon-only MOND residual, the cold-source term, and the measured high-acceleration Newton constant.
- `ward_report() -> dict` returns the baryon Noether residual, the cold-sector exchange residual, and the (Q)-equation source term.

- [ ] **Step 1: Write failing tests** for independent potential equations, exact baryon conservation on its scalar equation of motion, and a nonzero but explicitly accounted cold/Q exchange term when \\(\beta\\ne0\\).
- [ ] **Step 2: Run the focused test** and confirm it fails before implementation.
- [ ] **Step 3: Implement the weak-field variation** from the same static density used in Task 1. Keep the cold stress symbolic and set \\(\chi_c=0\\) only for the baryon-only branch.
- [ ] **Step 4: Derive Ward identities by varying the metric and matter fields**, then simplify the divergence on each matter equation. Do not label the cold stress separately conserved when the (Q)-dependent prefactor exchanges energy.
- [ ] **Step 5: Run tests** and require all identities explicitly marked exact to reduce to zero; leave \\(\Phi=\Psi\\), PPN, and causal status as computed outputs rather than assumptions.
- [ ] **Step 6: Commit** with `git add .../weak_field_ward_gate.py .../test_weak_field_ward_gate.py && git commit -m "derive winding-clock weak-field and Ward gates"`.

### Task 4: Derive FLRW winding and calibrate the assembly-history gate

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/flrw_winding_gate.py`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/test_flrw_winding_gate.py`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/winding_calibration.py`

**Interfaces:**
- `flrw_report() -> dict` returns the lapse, scale-factor, cold-scalar, and memory equations, an expanding solution family with (H\ne0), and the residual of (Q-\ln(a/a_{\rm ref})).
- `calibration_report() -> dict` computes the L75 representative (Q_{\rm rec}=0), (Q_{\rm gal}=\ln3), (Q_{\rm cl}=\ln1.7), the derived \\(\eta=e^{-\beta Q}\\), and the interval of \\(\beta\\) satisfying a declared galaxy ceiling.

- [ ] **Step 1: Write failing tests** for an expanding branch, exact homogeneous memory equation, positive cold kinetic coefficient, and the derived ordering \\(\eta_{\rm cl}>\eta_{\rm gal}\\) for \\(\beta>0\\).
- [ ] **Step 2: Run the focused test** and record the missing-module failure.
- [ ] **Step 3: Derive the homogeneous equations** before setting (N=1), solve the (Q) equation exactly, and verify the Friedmann residual with the cold scalar stress retained.
- [ ] **Step 4: Implement the calibration** using the numerical ceiling and assembly values recorded by L75; report the resulting \\(\beta\\)-interval and do not invent a cluster lower bound.
- [ ] **Step 5: Run tests** and separately report any failure of the expanding solution, cold kinetic sign, or ordering.
- [ ] **Step 6: Commit** with `git add .../flrw_winding_gate.py .../test_flrw_winding_gate.py .../winding_calibration.py && git commit -m "derive FLRW winding and assembly calibration"`.

### Task 5: Export exact identities, build the runner, and audit the first checkpoint

**Files:**
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/lean_ready_identities.json`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/lean_ready_identities.lean`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/run_local_winding.py`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/test_local_winding.py`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/contract.json`
- Create: `qwen_claude_field_theory/closure_2026/local_winding_clock_2026/REPORT.md`

**Interfaces:**
- `run_local_winding.py --output-dir NAME` writes `local_winding_results.json` containing Tasks 1–4 and a `status` field that remains `OPEN` unless all implemented gates actually pass.
- The JSON and `.lean` files contain exact expressions and theorem-shaped declarations only; because Lean is unavailable, the `.lean` file must state `-- NOT COMPILED` and contain no claim of a checked proof.

- [ ] **Step 1: Write the integration test** that calls every gate, checks all declared exact residuals, verifies both mode keys, and asserts that the report does not claim full closure while PPN/stability are absent.
- [ ] **Step 2: Run the integration test** and capture the expected import failures for missing gate modules.
- [ ] **Step 3: Implement the runner and deterministic export**. Convert SymPy objects to strings, preserve booleans as booleans, and include source hashes in the report.
- [ ] **Step 4: Add the computation contract** with the exact input list, bounds, software versions, and explicit non-claims. Do not include unrelated dirty files.
- [ ] **Step 5: Run the complete local package tests** with `python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/local_winding_clock_2026 -p 'test_*.py' -v`.
- [ ] **Step 6: Run the Mathbox provenance command** from the package contract, write a fresh `run_001/manifest.json`, and validate it with `validate_manifest.py --root`.
- [ ] **Step 7: Run relevant existing gates**: the IC1 package tests and the fresh `fable_independent_2026/L75_clock_winding_transmission.py` diagnostic.
- [ ] **Step 8: Write `REPORT.md`** with exact equations, command exit statuses, the first failure or open gate, and a requirement table. State `OPEN` unless every target requirement is actually derived and verified.
- [ ] **Step 9: Run `git diff --check`, inspect the staged diff, commit the package, and push only the scoped files.

## Verification standard

The first checkpoint is successful only if the exact action variation, actual
Dirac matrix, Ward identities, expanding FLRW branch, and calibration all
reproduce from the recorded manifest.  Even then, the full gravity objective
remains OPEN until the same action has passed the remaining PPN, causal,
nonlinear stability, and empirical gates.
