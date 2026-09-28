# AS127 — Derive reciprocal lapse density directly (CA5-GNC-R)

**Run:** `AS127-r1-20260928T151134Z-dsv4f-hermes`
**Branches:** CA5-GNC-R (host CA4-GNC); conclusion branch only CA5-GNC-R. Q, RAR, MU2, EXP, MONO are untouched comparison branches (this task does not involve any of the five constitutive laws; the heat filter's `nu_mono` appears only via the unchanged host gate).
**Outcome classification:** **derived** (scoped candidate result, not gravity closure).

---

## 1. Pinned action and conventions (step 1)

Sources (hashes verified at execution; match pins in the task and `SOURCE_MANIFEST.json`):

| Source | SHA-256 |
|---|---|
| `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` (CA4-GNC host) | `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` |
| `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md` (CA5-GNC-R reciprocal barrier) | `290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d` |

Conventions (FINAL_ACTION §1): `c=1`, signature `−+++`, `M_P^2 = (8π G_bare)^{-1}`; foliation
`n_μ = −τ_μ/√X_τ`, `N = X_τ^{-1/2}`, `h = g + n⊗n`, `a_μ = D_μ ln N`; leaves compact, connected,
closed, spacelike; mean `⟨A⟩_h = (∫√h A)/(∫√h)` — **not lapse-weighted** (FINAL_ACTION §1 and eq. (9)):
`δ_h⟨Z⟩_h = ½⟨z h^{ij}δh_ij⟩_h`. The h-mean has no N factor, so at fixed `h` the centered variable
`z = Z − ⟨Z⟩_h` and `t = 1 + z` are **N-independent**. No spatial boundary terms (FINAL_ACTION §2).
`G_N = G_bare/c_N` (FINAL_ACTION §5) — G_N, G_bare, G_cosmo kept separate.

CA5-GNC-R dark sector (vacuum ACTION R1): with the five real carrier fields `φ_A`,
`K_d = ½ Σ_A n(φ_A)^2`, `W_exc = ½ Σ_A |Dφ_A|^2 + Vmix` (positive masses/interactions, `Vmix > 0`),
`F(t) = 1 + (t + 1/t − 2)^2`, `V_0 > 0` constant, the replaced dark Lagrangian is

```
L_d = t K_d − W_exc/t − V_0 F(t),        t = 1 + Z − ⟨Z⟩_h > 0 .        (R1)
```

**Target** (task math): the physical lapse density

```
ρ_R = −(N√h)^{−1} δS_R/δ ln N ,   S_R = ∫ dt d³x N√h L_d ,
n(φ_A) = (φ̇_A − N^i D_i φ_A)/N ,                                        (T)
```

varied at **fixed h, Z, shift N^i, coordinate velocities φ̇_A** — δ ln N an arbitrary smooth
function on the compact leaf (δN^i = 0, δφ_A = 0, δ(Dφ_A) = 0, δZ = 0), before any field
elimination. `t_c > 0` (positive barrier coordinate), arbitrary fixed spatial gradients, no
homogeneous specialization, five fields, `V_0 > 0`; the coefficient of the inverse square is
identically one (R1). Criterion B / MONO / heat filter `S = exp((ξ²/2)Δ_h)` play no role in
this identity: `Y_h`, `f`, `J` are N-independent at fixed `h, U` (FINAL_ACTION §4, eq. (12)),
so their lapse variation is the already-pinned host piece `c_N[G(Y_h) − ℓΔ_h W_b]`.

## 2. Variation of ln N (step 2)

1. **Measure:** `δ(N√h)/δ ln N = N√h` pointwise (`h` fixed).
2. **Normal derivative:** from (T), `δ n(φ_A) = −n(φ_A) δ ln N` (velocities and shift fixed).
   Hence `δK_d = Σ_A n_A δn_A = −Σ_A n_A² δ ln N = −2 K_d δ ln N` — *exactly* (the identity is
   linear-quadratic; no expansion).
3. **Reciprocal pieces:** `t`, `W_exc`, `F(t)` are N-independent at fixed `(h, Z)` (Item 1 of
   the averaging-measure control below; `W_exc` depends on `h, φ_A` only).
4. **Assemble:**

```
δS_R = ∫ N√h [ L_d + t·(−2K_d) ] δ ln N
     = ∫ N√h [ −t K_d − W_exc/t − V_0 F(t) ] δ ln N .
```

δ ln N is arbitrary and local, so the density is pointwise:

```
ρ_R := −(N√h)^{−1} δS_R/δ ln N = t K_d + W_exc/t + V_0 F(t).        (★)
```

**Result (★) reproduces the pinned source formula (R3) exactly.** Substitution-back control:
reinsert (★) into `δS_R = ∫N√h(−ρ_R)δlnN` and re-differentiate assemble → symmetric residual 0
(check A, below), plus finite-difference verification B1 (rel. residual 4.7e-11).

## 3. Reduction and Hamiltonian lapse coefficient (step 3)

- **Kinetic piece** `t K_d`: carrier-normal kinetic energy with *reciprocal* weight `t`
  (positive for `t>0`; the barrier coordinate multiplies kinetic and divides gradient).
- **Gradient + potential piece** `W_exc/t`: reciprocal gradient weight `1/t`.
- **Vacuum (reciprocal-barrier) piece** `V_0 F(t) ≥ V_0` (F ≥ 1, min at t=1).
- **Hamiltonian comparison:** canonical momentum `π_A = ∂L_d/∂φ̇_A = (t/N) n_A`;
  Legendre transform at fixed `(t, h)` gives
  `H = Σ_A π_A φ̇_A − L_d = N ρ_R + N^i Σ_A π_A D_i φ_A`, so the shift-free Hamiltonian lapse
  coefficient is exactly `ρ_R = tK_d + W_exc/t + V_0 F(t)` — the lapse density is the true
  energy density of the reciprocal sector. Sign convention check against the standard scalar
  result (`ρ = ½n² + ½|Dφ|² + V`, kinetic coefficient **+1**) and against the CA4 host
  `ρ_d = e^z K_d + e^{−z} W_d` (FINAL_ACTION eq. (2), `ρ_d = ∂_z L_d`): (★) is the structural
  image of `ρ_d` under the reciprocal replacement `(e^z, e^{−z}) → (t, 1/t)` plus the barrier
  `V_0 F(t)`. Kinetic coefficients: `t` (correct) vs `−t` (negative control, §4).
- **Clock sector of the same candidate:** with the action-family convention
  (`ρ_d = ∂_z L_d` enters **with a plus sign**, FINAL_ACTION eq. (2)/(7); CA5 R4),
  `σ_R = +∂L_d/∂t = K_d + W_exc/t² − V_0 F′(t)` — reproduces R3's second formula exactly
  (check D, symbolic residual 0, finite-difference rel. residual 8.6e-11). The full Z equation
  (R4) carries the mean projector `−⟨Nσ_R⟩_h/N` (√h-only mean).
- **Limiting case** `t → 1` (z → 0, mean-normalized state): `ρ_R → K_d + W_exc + V_0`,
  which is the CA4 density at `z = 0` plus the vacuum tension `V_0`; `F(1)=1`, `F′(1)=0`
  (vacuum source and linear susceptibility vanish at `t=1`, vacuum ACTION R2–R3). Vacuum
  piece `ρ_v = V_0 F(t)` matches R3's `ρ_v`.

## 4. Controls that must be capable of failing (step 4)

| Control | Method | Result |
|---|---|---|
| **Signs** | Legendre + limiting standard scalar comparison (above) | kinetic coefficient +t>0 correct; control variant −t<0 detected as wrong |
| **Dimensions** | `[ρ_R] = energy density` (natural units c=1); measure `N√h`; target formula (T) adimensional in `a0` | consistent; a0 enters only through host gate scales, not through (★) |
| **Averaging measure** | `⟨Z⟩_h` uses pure `√h` (FINAL_ACTION §1, eq. (9)); verified `t` is N-independent at fixed h,Z | pass — without this, `δ ln N` would drag `δt` and (★) would fail |
| **Limiting case** | t→1 reduces to CA4 z=0 density + V₀; F(1)=1, F′(1)=0 | pass |
| **Substitution back (algebra)** | sympy: reinsert (★) into the varied action, simplify residual | residual `0` (exact) |
| **Substitution back (numerics, refined)** | 2-cell × 5-field central finite difference ε=1e-6 in ln N on cell 1; velocities & gradients frozen; recompute n(φ_A) with new N | dS/dlnN = −5.53984831297 vs −N√h·ρ_R = −5.53984831323; **rel. residual 4.7e-11 < 1e-6 (PASS)** |
| **Negative control** | Hold `n(φ_A)` fixed during the ln N variation (only the measure moves) | wrong density `−tK_d + W_exc/t + V_0F`: **kinetic coefficient −1.17 < 0 (wrong sign)**; wrong density −2.5329 < 0 (can be negative — unphysical for positive kinetic energy); residual vs correct = 6.9261... = 2tK_d exactly (symbolic `n²t`, numeric equality to 1e-12); finite-difference rel. residual 1.8e-11 vs its own prediction, so the control *does* change the answer — it fails as designed and is demonstrably capable of failing |
| **Clock-source cross-check** | σ_R = +∂L_d/∂t at fixed N,h,n (R3 second formula) | symbolic residual 0; numeric rel. residual 8.6e-11 (PASS) |

All numeric residuals are actual measured values from `compute_as127.py` (raw_output.json),
not booleans; the negative control **failed exactly as required** (wrong sign exhibited).

## 5. Footings (framework contract)

(★) is a0-free and dimensionless in structure: it holds identically on **both** footings with
no change. Numerical scales (G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30,
pc = 3.085677581491367e16; same-G convention for ρ_Lambda, G_N = G_bare/c_N recorded):

| Quantity (M_b = M_sun) | canonical a0 = 9.3619e-11 m/s² | alternative a0 = 1.1279e-10 m/s² |
|---|---|---|
| ρ_Lambda = 4a0²/(Gc²) | 5.8444e-27 kg/m³ | 8.4831e-27 kg/m³ |
| r_M = √(GM/a0) | 1.1906e15 m = 0.038586 pc | 1.0847e15 m = 0.035154 pc |
| v_flat = (GMa0)^{1/4} | 333.87 m/s | 349.78 m/s |
| B(r_M) | 9.3619e-11 m/s² (B = a0, self-check 1.4e-16) | 1.1279e-10 m/s² (self-check 1.1e-16) |

Footing separation (contract rule “never share both fixed ρ_Lambda and fixed κ”):
`a0_alt/a0_can = 1.2047768`; **if ρ_Lambda fixed** at the canonical value, the alternative
footing means effective κ = 0.6023884 (= ½·1.2047768) ≠ ½; **if κ = ½ fixed**, ρ_Lambda must
rise by factor 1.4514872. κ = 1/2 itself is an adopted input, not derived here.

## 6. Branch fidelity and closure implication

- Branches Q / RAR / MU2 / EXP / MONO are **not** touched, compared, or identified: (★) is an
  action-level identity of CA5-GNC-R's dark sector; the constitutive law resides in the
  unchanged heat gate `J, ν_mono` (MOND branch MONO remains the operative comparison target of
  the campaign, with criterion B — not concluded on here).
- **Closure implication (named gate):** the lapse/clock input of the single common action
  CA5-GNC-R. (★) supplies `ρ_R` for the unitary lapse equation — the CA4 host eq. (13) with
  `ρ_d → ρ_R` (vacuum ACTION: “the lapse sees ρ_b + ρ_R”) — and `σ_R` for the projected Z
  equation (R4), both from one variation of one fixed action before field elimination. This is
  a *derived* physical lapse density suitable for insertion into the common constraint;
  transfer to the operative filtered-MONO target remains gated (below). It does **not**
  promote anything to complete gravity closure.
- **Missing upstream results:** `results/AS131/`, `results/AS145/`, `results/AS133/` do not
  exist at dispatch (heat-field metric stress, gate contribution to the lapse equation,
  terminal heat BC) — recorded as unavailable dependencies; (★) was cross-checked directly
  against the pinned source formulas (R3) instead.

## 7. Lean certificate

`AS127_lapse_density.lean` — 9 theorems, zero `sorry`, compile exit 0,
`#print axioms` = `[propext, Classical.choice, Quot.sound]` for every theorem (hard bar met):
(a) `lapse_density_correct` (main identity, measure + kinetic variation),
(b) `kinetic_variation` (δK = −2K), (c) `control_wrong_density` (wrong sign when n frozen),
(d) `control_residual` (= 2tK), (e) `wrong_kinetic_sign` (−t < 0 for t>0),
(f) `correct_kinetic_positive`, (g) `F_identity` ((t+1/t−2)² = (t−1)⁴/t²),
(h) `F_lower_bound` (F ≥ 1), (i) `vacuum_piece_bound` (V ≤ V·F). Compiled host-side with
`lake env lean <abs path>` from `fable_independent_2026/lean_2026`; no files written into the
Lean tree.

## 8. Failed attempts (preserved)

1. First Lean proof of `vacuum_piece_bound` produced `V*1 ≤ V*F` vs `V ≤ V*F` mismatch —
   fixed with `simpa` (commit in the file history of this run).
2. First clock-source check used the wrong sign convention (−∂L/∂z instead of the
   action-family convention +∂L/∂z pinned by FINAL_ACTION eq. (2) and CA5 R4); corrected and
   re-verified (the failed form is preserved as the first raw_output.json in this run's
   `failed_attempts` record — note in raw output D_clock_source residual_nonzero).
3. sympy “Can't calculate derivative wrt z+1” — replaced ∂/∂t by ∂/∂z (dt/dz = 1).

## 9. Limitations and next unresolved implication

Does **not** establish: coupled global existence/positivity of `(N, Z, U, W_b, φ_A)` for
CA5-GNC-R; the joint lapse–Z problem (ρ_R and σ_R depend on Z through t, so the lapse eq.
and R4 are nonlinearly coupled); heat-gate interplay (`f = G′(Y_h)`, MONO splice) inside the
full equations; PPN/no-slip; tensor/GW sector; criterion-B Cauchy well-posedness; the
homogeneous `k = 0` and deep-MOND `y → 0` limits; V_0's magnitude or the κ = 1/2 normalization
(both remain inputs). Numerical verification is a 2-cell × 5-field frozen-gradient prototype
(finite evidence, not a theorem).

**Next unresolved implication:** the first missing mathematical bridge is the joint
lapse/Z solvability of the coupled system for CA5-GNC-R at fixed carrier/gate data —
whether a positive lapse `N` solving eq. (13) with `ρ_R(t(Z))` and the projected Z-equation
(R4) with `σ_R(t(Z))` exists on the compact leaf (BARRIER_PROOF.md covers Z alone at fixed
data and does not cover the coupled pair). This is the smallest step past the pinned
fixed-data Z theorem that still uses (★) as input.

**Suggested follow-up (child spec):** `branches/AS127/AS127.C01.md` — prove existence of a
positive smooth lapse for the 2-cell/compact-leaf model of eq. (13)+R4 with ρ_R, σ_R from (★),
fixed carrier data and `t ∈ (0, T)`, with the negative control “ρ_R replaced by the
measure-only (wrong) density ⇒ kinetic sign −t ⇒ positive-solution existence fails”.

## 10. Artifacts

- `derivation.md` (this file), `result.json`, `compute_as127.py`, `raw_output.json`,
  `raw_output.stderr`, `AS127_lapse_density.lean`, `AS127_lapse_density_axioms.lean`,
  `lean_compile_out.txt`, `lean_axioms_out.txt` — all in this run directory; hashes in
  `result.json` `artifacts_sha256`.
