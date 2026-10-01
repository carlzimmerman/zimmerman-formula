# AS238 — Tensor dispersion on homogeneous occupied FLRW — derivation

**Run:** `AS238-r1-20260928T212251Z-dsv4f-hermes`
**Task pin:** sha256 `30e0632f796a0d6ab53607f7e857630647933190e33d6a0798dc276bab89e269` (verified before and after execution)
**Worker:** deepseek-v4-flash-0731 via Hermes Agent (openrouter)
**Started/finished (UTC):** 2026-09-28T21:22:51Z / 2026-09-29T00:13:29Z
**Status:** completed · **Outcome:** supports_scoped_claim (Tier-0b, un-reviewed)

---

## 1. Cell, conventions and pinned premises

- **Action cell:** CA5-GNC-R (FINAL_ACTION.md sha `b8c04d4e…`, occupied/RESULT.md sha `6091291f…`, FRIED_CHICKEN_SPEC.md sha `98d9149f…` — all re-verified 2026-09-28). Physical metric g, signature (−,+,+,+); flat compact FRW leaf with scale factor a(t) and Hubble H = ȧ/a; bare Einstein–Hilbert coefficient M = M_P²; **occupied branch**: Λ = 0, gate inactive (Y_h = −θ < 0), background Z = U = 0, z = 0, t_c = 1; the five real carrier fields occupy the homogeneous background with
  3MH² = T + V + V0,  MḢ = −T,  P_d = T − V − V0,  T = ½Σv_A²,  V = V_mix ≥ 0,  V0 > 0
  (occupied Friedmann pair; M, T, V, V0 constant; no Λ-term survives the occupation, i.e. MΛ + ρ_d with Λ = 0).
- **Mandatory input adopted (not re-derived):** κ = 1/2 in a0 = κc√(Gρ_Λ). Dimensional footings reported **separately**: canonical a0 = 9.3619e-11 m/s² at κ = 1/2 ⇒ ρ_Λ = 4a0²/(Gc²) = 5.8444e-27 kg/m³; alternative a0 = 1.1279e-10 m/s² (same formula ⇒ ρ_Λ′ = 8.4831e-27 kg/m³; conversion κ_eff = 0.60239 at fixed ρ_Λ). No footing shares both a fixed density and a fixed κ.
- **Constants (SI, only in the numeric layer):** G = 6.67430e-11, c = 299792458, M_☉ = 1.98847e30, pc = 3.085677581491367e16.
- G_N/G_bare/G_cosmo are kept distinct: the derivation only uses the Einstein coefficient M = M_P² of the same action; no independent G enters the tensor sector at this order (c_T = c is a0-free).
- **Target (from the task):** S_T = (M_P²/8)∫a³[γ̇_ij² − a⁻²(Dγ_ij)²] if “no extra terms survive” — the task demands deriving (or refuting) this and the resulting dispersion, with a capable-of-failing negative control.

## 2. Perturbation setup

Tensor TT mode at finite non-zero comoving wave vector k = (kx, ky, kz):

  g_ij = a²(δ_ij + ε q(t) e_ij C(x)),  C = cos(k·x),  S = sin(k·x),
  e_ij symmetric, trace-free, transverse: k^i e_ij = 0, e_ii = 0.

The **exact TT family** is imposed by solving the four linear conditions (k·e rows + trace) for (e13, e23, e33, e12) with parameters (e11, e22) — valid for generic k with kx, ky, kz ≠ 0; `e2 := e_ij e_ij` is computed symbolically (printed in `derive_raw.out`; for a single +-polarization mode e2 = 2). A 3-parameter family was tried first and rejected because it left a residual transversality defect (see failed_attempts).

## 3. Quadratic variation of the whole action, not the Einstein form

Every term of the CA5-GNC-R action relevant at the homogeneous occupied background is proportional to √−g times a metric-independent coefficient; the five carriers are frozen at their homogeneous VEVs, so at O(ε²) the full second variation is

  δ²S = δ²[(M/2)∫√−g (R − 2Λ)] + δ²[∫√−g (T − V − V0)]

(Λ = 0 on the occupied branch; the σ_ij σ^ij-type sectors are included in δ²R — nothing is assumed a priori; the carrier *fields’* own quadratic modes decouple from the tensor at O(ε²) because the background solves the carrier stationarity conditions, see Limitations).

Implemented symmetrically in `as238_derive.py` (sympy):
1. exact h_ij, h^ij (with the ε² inverse-metric correction), Christoffels (all components, 4+3+3+6 independent families, closed form),
2. Ricci scalar R = g^{μν}R_{μν} from R_00, R_{0i} (g^{0i} = 0, so R_{0i} never enters) and R_ij with the full ΓΓ contraction,
3. ε-expansion of L = √−g[(M/2)(R−2Λ)+(T−V−V0)] to order ε² — including δ²√−g·(background R) and δ²√−g·(T−V−V0) — box average (⟨C²⟩ = ⟨S²⟩ = 1/2, ⟨CS⟩ = 0) with the exact TT family substituted,
4. integration by parts in time (kinetic part), collecting S2 = A q̇² + D q² + (linear) q,
5. substitution of ȧ = Ha, ä = Ḣa + H²a **before** the Friedmann pair is applied.

**Extracted coefficients (symbolic, exact):**

  A / [(M/8)a³]  > 0  (the full polarization-polynomial printed in derive_raw.out; A = A_canon·(e2/2) with A_canon = (M/8)a³, verified: A/A_canon = 1 with the e2-normalized family),
  linear piece in q: **0** (exact TT transversality), 
  D / [(M/8)a³] = −k²·… − a²·[(6MH²+4MḢ−2MΛ+2T−2V−2V0)/4]·(pol)/(k²-e2-normalization)
  ⇒ mass coefficient per [a³·e2/2]:
  **mass = −(3MH² + 2MḢ − MΛ + T − V − V0)/4**  (pre-Friedmann; Λ = 0 held symbolic),
  **mass after the occupied Friedmann pair (3MH² = T+V+V0, MḢ = −T, Λ = 0): exactly 0.**

The mass-cancellation identity

  −(3MH² + 2MḢ − MΛ + T − V − V0)/4 = 0 under 3MH² = MΛ+T+V+V0, MḢ = −T

is certified in Lean (theorem `mass_cancel`, below).

## 4. Resulting tensor sector

Per polarization (using the e2/2 normalization of the box average):

  **S_T = (M/8) ∫ a³ [ γ̇_ij² − a⁻² (Dγ_ij)² ] d³x dt ,**
  **EOM:  q̈ + 3H q̇ + (k²/a²) q = 0** (per polarization; exactly the coefficient ratios 1 : 3H : k²/a² against (M/4)a³),
  **dispersion: w² = k²/a², phase speed c_T = 1** (c in SI units) — no mass term, no a0-term, no κ-term survives; Hubble friction 3H present; positive kinetic coefficient (M/8)a³ > 0 ⇒ positive-energy sector at the quadratic level.

Verification by substitution (algebra control, task step 4): with q ~ e^{+iwt} the frozen-coefficient symbol is
  (3iHw a² + k² − w²a²)/a²,
the roots w = 3iH/2 ± √(4k²−9H²a²)/(2a) substitute back to **residual 0 for each root**; the extracted coefficients satisfy the EOM with **residual 0**.

## 5. Negative control (must be capable of failing) — FIRES

Add the diagnostic shear-squared operator (κ/2)∫a³σ_ijσ^ij:
  kinetic coefficient A_κ = (M+κ)/8 [symbolically: (M+κ) times the same polarization polynomial],
  speed² ratio = M/(M+κ) (κ = 0 ⇒ 1),
  the **pure-Einstein extraction w² = k²/a² substituted into the modified EOM leaves the residual −κk²/(8a²) ≠ 0** (fires for any κ ≠ 0).

Numeric layer (numpy, 4th-order FD lattices, `as238_numeric.py`), controls N1–N8, all residuals below:

| check | statement | measured | tolerance (pre-set) | result |
|---|---|---|---|---|
| N1 | discrete action → exact discrete EL (periodic time chain, 4 cells, ε = 1e-6 FD derivative) | max|err| = 4.03e-6 | 1e-4 | PASS |
| N1b | same operator on off-shell random data (capable-of-failing sensitivity) | max|q̈+3Hq̇+a⁻²Lap q| = 968.9 ≫ 0 | > 1 | PASS (non-vacuous) |
| N2 | discrete EOM identity on TT superpositions, occupied rad-like & de Sitter | ~4.3e-19 | 1e-12 | PASS |
| N3 | k = 0 long-wavelength freeze: q̇a³ = const | max rel 3.7e-14 | 1e-9 | PASS |
| N4 | **shear negative control**: extraction must find w² = M/(M+κ)·k²/a²; wrong (pure-Einstein) extraction residual | N=17: w² = 0.053276, residual −0.039957 fires**; N=33: w² = 0.014257, residual −0.010693 fires | fires ≠ 0 | PASS (fires) |
| N5 | refinement 17 → 33 → 65: w²a²/k² → 1 | 1.0000 at all three | 1e-6 | PASS |
| N6 | both footings: canonical ρ_Λ = 5.8444e-27 (a0 = 9.3619e-11, κ = 1/2); alt foot ρ_Λ′ = 8.4831e-27 (a0 = 1.1279e-10); c_T = 299792458 m/s in both (sector is a0-free: gate inactive) | as listed | — | PASS |
| N7 | SI dimension bookkeeping of S_T and EOM | [q̈]=s⁻², [3Hq̇]=s⁻², [(c/a)²Lap q]=s⁻² | — | PASS |
| N8 | second variation of the **exact nonlinear action** (numerical Christoffels/Ricci on the full metric, no linearization) vs the derived quadratic form + carrier measure, static a = 1.3, H = 0, P_d = −0.0363, e = diag(1,−1,0), k = (0,0,1), quartic window probe (q = q̇ = 0 at the edges, q̈ ≠ 0 inside so the raw density genuinely differs from the canonical form) | c_fit = 0.0575177 vs canonical 0.0575297 (rel 2.08e-4); raw-density expectation 0.0575273 (rel 1.67e-4); IBP identity ⟨q̈q⟩ = −⟨q̇²⟩ to 2.2e-6 | 1e-2 | PASS |

The N8 check is run on the same lattice that measures the discrete gradient operators L1sq = L2d = 0.9309 ≠ 1 (k·dx = π/3), which are inserted into the expectation, so lattice bias is removed explicitly rather than hidden.

## 6. Lean certificate (zero sorry, allowed axioms only)

`AS238_tensor_dispersion.lean` (self-contained, compiled host-only with `lake env lean`, Lean 4.34.0-rc2, mathlib) certifies four algebraic identities:
1. `mass_cancel` — the occupied-Friedmann-pair mass cancellation  (…)/4 = 0;
2. `kinetic_coeff` — IBP coefficient rule −(3/4)A − C = (1/4)A for C = −A (raw → canonical kinetic);
3. `shear_disp` — (M+κ)w² = Mk²/a² ⇒ w² = (M/(M+κ))k²/a² (negative control's algebra);
4. `onshell_substitution` — −ω² + k²/a² = 0 for on-shell modes.

`#print axioms` for all four: **[propext, Classical.choice, Quot.sound]** — exactly the allowed set; zero `sorry`.

## 7. Both footings

- Canonical: a0 = 9.3619e-11 m/s², κ = 1/2 ⇒ ρ_Λ = 5.8444e-27 kg/m³ (N6).
- Alternative: a0 = 1.1279e-10 m/s², κ = 1/2 ⇒ ρ_Λ′ = 8.4831e-27 kg/m³; or κ_eff = 0.60239 at fixed ρ_Λ (reported as conversion only).
- The tensor sector itself is a0-free: c_T = c in both footings; the FRW leaf evolution in this sector is the same in both (the dispersion is scale-invariant: w² = k²/a²).

## 8. Bounds actually enforced

- Symbolic run: wall 30.00 s (self-reported sympy 29.8 s), peak RSS 89.6 MB (measured 83.4 MB footprint), 1 thread (env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1).
- Numeric run: wall 3.5 s, peak RSS **503.8 MB (≤ 512 MB cap)**, 1 thread (same env), grids N4/N5: 17, 33, 65; N8: (6,6,6,151) with the 512 MB cap honored after trimming from (24,24,24,41 → rejected 1.9 GB estimate) via (10,10,10,161 → 1.50 GB actual) and (8,8,8,81/161 → 578/530 MB) to (6,6,6,151 → 503.8 MB).

## 9. Failed attempts (preserved in the run dir)

- `as238_derive.py` history: 3-parameter TT family left a transversality defect (linear piece ≠ 0) → replaced by the exact 4-condition TT solution; a placeholder Christoffel contraction bug (`l0 := None` dead line, missing −Γ^l_ik Γ^k_jl double loop); the spatial chain rule ∂_k f = k_k(C ∂_S f − S ∂_C f) was required for products mixing C and S (an S²-only version left a spurious k² mass term).
- `as238_numeric.py` history: projector shape bug; metric-block assembly; de Sitter meshgrid; N1 sign/broadcast errors; N3 Euler→exact exponential step; N8 probes: sin²(πu) (4th-order boundary stencils inaccurate for its high q̈ at the edges → 1.1% edge contamination at Nt=41), closed-form window averages (factor-1/T² and sign slips → false 3.4× mismatch), sub-window restriction (destroys the IBP identity) — resolved by the quartic probe u²(1−u)² on which all 4th-order stencils are exact, full-window means, and lattice-measured gradient operators. Diagnostic scripts kept: `debug_curvature.py`, `pin_R_bug.py`, `compare_R.py`, `diag_n8*.py`.

## 10. Limitations

- Derivation is **linearized** (quadratic action, TT sector) around the homogeneous occupied background; non-linear tensor self-interactions and tensor×carrier-fluctuation couplings (the five carriers’ own O(δφ²) sectors) are not computed here — the claim covers the free tensor sector only.
- `kappa = 1/2` is an adopted input, not derived; the two footings are reported separately as the framework requires.
- Generic-k exact TT family requires kx, ky, kz ≠ 0; axis-aligned modes (e.g. k ∥ ẑ) are limits of the same expressions (the numeric layer uses k = (0,0,1) with e = diag(1,−1,0) and matches).
- Numerics: finite-difference 4th-order on compact tori; sampled domain listed in §5; residual levels 1e-4–1e-3 in N8 (edge-slice stencil contamination), 1e-14–1e-19 in N3/N2, negative control fires at O(κk²/a²).
- No claim about closure of gravity; the occupied-branch implication is limited to the statement in §4.

## 11. Next unresolved implication

The back-reaction of the tensor wave on the occupied Friedmann evolution (energy-momentum of the wave, ρ_gw ∝ (M/8)γ̇², and its effect on the Friedmann pair) — i.e., the sector's second-order closure — is the first missing bridge; the free dispersion alone does not establish the energy exchange between the tensor sector and the five-carrier occupation.

## 12. Suggested follow-up (child)

**AS238.C01 — tensor-wave stress-energy and back-reaction on the occupied branch**: derive ⟨T_μν^{(2)}⟩ for the TT mode from the same CA5-GNC-R action (Noether/definition), verify ρ_gw = (M_P²/8)⟨γ̇²⟩ (c = 1; SI factor (c²/8πG)), and check the energy exchange against the Friedmann pair (3MH² = T+V+V0 with ρ_d → ρ_d + ρ_gw). Controls: exact symbolics + conservation ∇^μT_{μν} = 0 residual, both footings, shear negative control switched off.