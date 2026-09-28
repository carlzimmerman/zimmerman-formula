# AS008 — Deep temperature as a velocity scale — derivation

**Group:** A01 · **Priority:** P0 · **Branch:** CORE scale identities
**Run:** `AS008-r1-20260927T200612-8f9004` (worker sa-7-b5e2ed7b, completed by orchestrator)
**Task SHA-256:** see `result.json` (computed at dispatch)

## 1. Exact claim

Given the task-declared **conditional deep-equilibrium inputs** σ² = C/2, ρ_ph = C/(4πG r²),
P = σ²ρ_ph (C = √(GM_b a0)) and adopted κ = 1/2 (a0 = κc√(Gρ_Λ)), the temperature–velocity map is:

- **k_B T = m σ²** ⟹ **T = m C / (2 k_B)** — the deep velocity scale maps linearly onto a
  temperature scale per mass; T/m = C/(2 k_B) is mass-independent.
- The map (m, T) → (λm, λT) leaves σ² = k_B T/m **exactly invariant**: a measured σ determines
  only the ratio T/m, never m (mass degeneracy).
- **Hydrostatic balance holds identically**: with P = σ²ρ_ph, dP/dr = −ρ_ph g for every r ≠ 0,
  where the phantom density is ρ_ph(r) = C/(4πG r²) and g(r) = C/r.
- The hydrostatic ODE dσ²/dr = (2σ² − C)/r has general solution σ²(r) = (C + K r²)/2;
  the bounded solution K = 0 is selected by boundedness at r → ∞ (classical argument, not certified).
- SIS pairing: v_flat² = 2σ².

**Negative control (live):** the wrong normalization σ² = C (instead of C/2) breaks hydrostatic
balance identically — the cleared residual C·(C/4πG)·(−2)/r³ ≠ −(C/4πG)(1/r²)(C/r) (Lean T5);
Python lane additionally records the wrong-normalization ODE inconsistency (`mutation_independent_T`
check: σ(T=10⁶ K, m_p) differs from the deep σ by 41903.2 m/s, recorded, flagged as expected).

## 2. Numerical witnesses (both footings, 50-digit mpmath; see as008_probe_raw.json, 27/27 checks)

| Quantity (M_b = 10¹¹ M☉) | canonical a0 = 9.3619e-11 | alternative a0 = 1.1279e-10 |
|---|---|---|
| C [m²/s²] | 3.524880e10 | 3.868991e10 |
| σ [km/s] | 132.757 | 139.086 |
| v_flat [km/s] | 187.747 | 196.698 |
| T_proton [K] | 2.13515e6 | 2.34359e6 |
| T_electron [K] | 1162.84 | 1276.36 |
| r_M [kpc] | 12.202 | 11.117 |

- Hydrostatic residual dP/dr + ρ_ph·g ≡ 0 exactly (sympy 0.0; mpmath 60-dps residuals 0.0 at
  r/r_M ∈ {0.5, 1, 3, 10, 100}, both footings).
- Branch correction table: leading corrections to g = C/r at r = r_M are
  Q: y/2, RAR: u/2 with u = √y etc. — recorded in `branch_correction_acceleration`,
  verifying the deep-limit approach per branch (compare-only; no branch law adopted here).
- Degeneracy scan: (m2, T2) = (λm, λT) gives σ(m2) − σ(m1) = 0.0 at 50 dps. ✓

## 3. Framework inputs vs derived results

- **Adopted inputs:** κ = 1/2; a0 footings (both); σ² = C/2, ρ_ph = C/(4πG r²), P = σ²ρ_ph
  (task-declared conditional deep-equilibrium targets — NOT derived, per FRAMEWORK_CONTRACT).
- **Derived (exact algebra, Lean-certified):** temperature scale law T = mC/(2k_B);
  mass-degeneracy invariance; hydrostatic identity; ODE general solution family; SIS pairing;
  wrong-normalization failure (factor-1/2 discrimination).
- **Not established:** equilibrium *formation* (why σ² = C/2 dynamically), finite-boundary
  treatment, logarithmic-well double-counting, no action-level derivation; no branch law used.

## 4. Bounds enforced

Wall 21.38 s (probe; cap 120 s) · peak RSS 63.9 MB (cap 512 MB; macOS refuses RLIMIT_AS —
recorded verbatim) · 1 thread · no grids (scalar symbolic + 50-dps mpmath).

## 5. Next unresolved implication

Deriving σ² = C/2 and ρ_ph = C/(4πG r²) from the operative dynamics (equilibrium formation,
finite boundaries, normalization, log-well double counting). Nearest catalog continuations:
AS087/AS097 (equilibrium/statistical group); the child spec `AS008.C01` is NOT dispatched
(no spawn mechanism in the worker); orchestrator may dispatch.

## 6. Lean certificate

`AS008_deep_temperature_certificates.lean` — 9 theorems, exit 0, zero sorry,
`#print axioms` = exactly [propext, Classical.choice, Quot.sound] for all 9
(compile log `lean_compile2.out`).

## 7. Limitations

Conditional equilibrium-input result only: no dynamics/kernel/action content, κ and the
equilibrium relations remain adopted inputs, no observations fitted, no closure claim.