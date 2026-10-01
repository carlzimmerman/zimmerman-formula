# AS240-r1 — Gravitational-wave amplitude transport (seed AS240, Tier-0b)

**Run id:** `AS240-r1-20260928T202950Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 via OpenRouter, platform=subagent, worker
id `dsv4f-hermes` (Hermes agent, host macOS 26.5.2)
**Task sha256:** `76a9573a0df9a3b08abccc8f452ab568dd590637d827bcb1c2e8b353213caad5` (verified on disk)
**Branch:** CA5-GNC-R physical-metric branch (filtered nu_mono gate, causality criterion B
are the operative target text; **no branch translation used** — the tensor sector of the
pinned action is used directly). Q / RAR / MU2 / EXP / MONO laws are never used here.
**Status:** derived, scoped claim; acceptance_state = unreviewed.

---

## 0. Sources and conventions (step 1: pin the action)

Pinned and hash-verified against SOURCE_MANIFEST.json:

| Source | SHA-256 (on disk, verified) |
|---|---|
| `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` | `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` |
| `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` | `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` |
| `real_research/common_action_2026_09_26/transport/HOMOGENEOUS_FRW.md` | `ecc93b07a62d7ea531abcf4ca8ed8cbe7b9f73c8cb60f931dc8fcb6e9e685c1d` (context, not load-bearing) |
| `STANDING.md` | `660462ebe8f98844c418e173a1dada90b9df3800c4d445fd5a0556eb9476bf63` |

Action cell (CA4-GNC/CA5-GNC-R, FINAL_ACTION §§1–7): one physical metric `g`, `M_P^2 =
(8πG_bare)^{-1}`, matter and photons coupled only through `S_b[g]`, five real carrier
fields with the projected clock, C4 convex gate, heat filter `S_h = e^{bΔ_h}`,
compensator `c_N ℓ a·DW_b`; `G_N = G_bare/c_N` with `c_N = 1 − α/2` (derived in the
action), `G_cosm/G_N = c_N` (FINAL_ACTION eq. 18). Homogeneous inactive FRW branch
(§7): `f = G = 0`, `z = 0`, `a = DU = DZ = 0`, `Q_K = 0`, Friedmann
`3M_P^2H^2 = M_P^2Λ + ρ_b + ρ_d`; tensor sector is Einstein's
`(M_P^2/8) a^3[ḣ_ij² − a^{-2}(∂h_ij)²]` in cosmic time (speed one), with the *constant*
tensor normalization `M_P^2 = 1/(8πG_bare)`.

Framework inputs: `a0 = κ c √(G ρ_Lambda)`, **κ = 1/2 ADOPTED** (campaign mandate; not
derived here; an independent κ-derivation is not supplied by this task). Numerics:
`G=6.67430e-11`, `c=299792458`, `M_sun=1.98847e30`, `pc=3.085677581491367e16` (SI).
`G_N`, `G_bare`, `G_cosmo` kept as separate symbols throughout (FINAL_ACTION: `G_N =
G_bare/c_N`, `G_cosm/G_N = c_N`).

**Mode/boundary conditions (step 1 target):** flat compact box `x³ ∈ [0, 2π)`,
conformal time η, single TT tensor mode `h_ij = e_ij h(η,x³)` with comoving wavenumber
`k = 2πm/L` integer (`m ∈ ℕ`), geometric-optics regime `ω/H ≫ 1`, WKB ansatz
`h = A(η) exp(iθ/ε)`, `θ = −ωη + kx³`, envelope `A` slowly varying, initial data:
outgoing WKB branch to first order, `h(η0) = A0 sin(kx)`, `h'(η0) = −A0(k cos(kx) +
ℋ0 sin(kx))`, periodic boundaries, `ℋ = a'/a`.

**Upstream dependencies recorded:** `results/AS238/` (tensor dispersion, sibling) and
`results/AS239/` (inhomogeneous carrier propagation, sibling) are **not present** in
`deepseek_push/astra_spawn_ideas/results/` at execution time. The tensor operator used
here is therefore derived **directly from the pinned action** (D1 below) as a
stand-in, and the c_T = 1 tensor-dispersion content is covered by the direct action
check + the wave-code phase-speed control (N1-B5). `results/AS658/` (vacuum DOF, zero
bulk modes; fluctuation gate open) and `results/AS215/` (time-orientation certificate)
were read; both are consistent with and unaffected by this result.

---

## 1. Step 2 — WKB amplitude-order equation (derived, exact)

### 1.1 Tensor operator directly from the action (D1)

Metric `ds² = a²(η)(−dη² + dx²) + a²h_ij dx^i dx^j` with the `+` polarization
`h_11 = −h_22 = q(η,x³)` (TT: trace 0, `∂_i h_ij = 0`). Sympy expands `√(−g) R` to
second order in the perturbation and applies the exact Euler–Lagrange operator
(including the `q″q`, `q_xx q` total-derivative pairings). Result, exact:

```
EOM  =  κ(η) · [q″ + 2ℋ q′ − ∂₃² q]  =  0,        κ(η) = −a(η)²
canonical quadratic action density  =  (M_P²/2)·(a²/2)·[q′² − (∂₃q)²]
```

- Friction coefficient `+2ℋ` exactly (`friction/κ − 2a′/a ≡ 0`);
- speed² = 1 exactly (`−c_spa/c_kin − 1 ≡ 0` with `c_kin = +a²/2 > 0`);
- positive canonical tensor kinetic energy (`c_kin = +a²/2`), requirement 6;
- EL residual after exact coefficient extraction `≡ 0`.

So on the homogeneous inactive branch the TT tensor sector is exactly the Einstein one
with **constant** `M_P` — the c₂Q_K², |a−DZ|², gate, heat and carrier terms have no
quadratic TT piece: `K^(1) = 0` for pure-TT modes (D2), and scalar/tensor decouple at
quadratic order on the homogeneous isotropic background.

### 1.2 WKB collector (D3)

With `L = ∂_η² + 2ℋ∂_η − ∂_x²` applied to `A(η)e^{i(θ/ε)}`, `θ = −ωη + kx³`:

```
ε^{-2} (eikonal):   (k² − ω²)A = 0          → ω = +|k|        (null, c_T = 1)
ε^{-1} (transport): −2i[ω(A′ + ℋA) + kA_x] = 0  →  plane envelope:  A′ + ℋA = 0
ε^{0}  (subleading): A″ + 2ℋA′ = −A0a0·a″/a²  ≠ 0   (relative order (ℋ/ω)²)
```

Substitution residual of `A(η) = A0·a0/a(η)` into the transport equation:
**exactly 0** (sympy). **Amplitude transport law (the derived object):**

```
A(η) = A0 · a0 / a(η)          (per comoving mode; leading WKB order)
```

with relative error `O((ℋ/ω)²)`, quantified numerically in N2. The equation of motion
this satisfies is `h″ + 2ℋh′ − ∂₃²h = 0`, i.e. `γ = A exp(iθ/ε)` with `k_μ = ∂_μθ` as
displayed in the seed's mathematics line, and transport at the next WKB order as
required.

**Lean-certified** (substitution identity, derivative form):
`deriv (fun t => A0*a0/a t) η + (deriv a η / a η)·(A0*a0/a η) = 0` — theorem
`transport_law`, axioms = {propext, Classical.choice, Quot.sound}, zero sorry.

### 1.3 Step 3 — GW luminosity distance equals the EM one (D4)

Flux bookkeeping on the same background (all exact, sympy):

- source-frame luminosity `L = 4π(a_em r)²·κ ω_e² A_em²` (emission sphere, comoving
  radius `r`);
- transport + redshift: `A_obs = A_em·a_em/a_0`, `ω_obs = ω_e·a_em/a_0`;
- observed flux `F_obs = κ ω_obs² A_obs²` dilutes as `a^{-4}` (verified: `F_obs = F_e
  (a_em/a_0)⁴`);
- `4π D_L² F_obs = L` solved for the strain-implied distance:

```
D_L^GW = a_0 r (1+z)  =  D_L^EM        (flat FRW, D_L = (1+z)²D_A = (1+z)D_M)
D_L^GW / D_L^EM − 1 ≡ 0                (exact, constant M_P)
```

**Answer to step 3: yes** — for constant `M_P² = 1/(8πG_bare)` the GW luminosity
distance evolution equals the electromagnetic one in this sector, to WKB order (with
the O((H/ω)²) correction quantified in N2). The physical reasons, all pinned to the
action: (i) matter/photons couple to the single physical metric `g` (`S_b[g]`), so EM
and GW rays are null geodesics of the same metric with the same redshift; (ii) the
tensor kinetic normalization `M_P` is exactly constant (no varying-M_* channel: in the
action, `G_bare` is a constant parameter and `G_cosm/G_N = c_N` is z-independent);
(iii) no scalar/tensor mixing at linear order on the homogeneous background (D2). For
comparison, a hypothetical (NOT the framework's) z-dependent tensor coupling
`G_*(z)` would give `D_L^GW/D_L^EM = √(G_*(z)/G_*(0))` (derived in D5) — the
framework's constant `G_bare` makes that ratio identically 1.

Numerically N3 verifies on a matter+Λ background (z ∈ [0.02, 2], 401 points):
`S(z) := h_obs(z)·D_L(z)/(1+z)` constant to `4.4e-16` and `max|D_L^GW/D_L^EM − 1| =
3.3e-16`.

---

## 2. Step 4 — negative control (capable of failing): G_N calibration vs propagation friction

**Setup (NC-1/NC-2/NC-3, z ∈ [0.02, 2], 257 points, noise σ = 1e-3, seed 20260928).**
True strain of equal-luminosity standard sirens through the derived transport:
`h(z) = C(1+z)/D_L(z)` (from 1.3). Friction model family: `h = C(1+z)/D_L·exp(−γz)`
(in log space, linear least squares). All thresholds set before evaluation.

- **NC-1 planted friction (γ_p = 0.12):** the γ = 0 model leaves residuals with
  `max|resid| = 1.20e-1 ≫ σ` and monotone slope `−0.120/unit z` — **control fires**
  (a genuine friction cannot be absorbed into the amplitude calibration); the γ-fit
  recovers `γ̂ = 0.11987 ± 5.4e-5` ✓.
- **NC-2 G_N miscalibration:** strain rescaled by `√c_N`, `c_N = 1 − α/2 = 0.75`,
  α = 0.5 (misuse of the *measured* Newton constant in the flux→strain calibration
  instead of the tensor normalization): the strain ratio to the true law is
  **z-independent** (`max|ratio − mean|/mean = 2.6e-16 < 1e-13`) and the friction fit
  returns `γ̂ = −1.3e-4 ± 5.4e-5 ≈ 0` — **a constant G-normalization is a pure
  amplitude calibration and cannot masquerade as a friction term** (distinction
  checked; symbolic counterpart D5: `d/dz ln(h_cal/h) ≡ 0` vs `d/dz ln(h_fric/h) =
  −γ φ'(z) ≠ 0`).
- **NC-3 equal-luminosity exponent:** fit `h ∝ (1+z)^{1+δ}/D_L` on true data:
  `δ̂ = +2.7e-4 ± 8.7e-5 ≈ 0` ✓; planted `δ_p = 0.08` recovered:
  `δ̂ = 0.08027` — **the discriminator can fail and detect a wrong transport law.**

**Dimensional / sign / measure / limiting-case checks (mandated control list):**
- dimensions: all ω, k in units 1/η; h dimensionless; the operator and WKB orders
  dimensionally consistent as built from `θ = −ωη + kx` (checked per term);
- signs: expanding branch (`ℋ > 0`) **damps** the amplitude (`A′ = −ℋA < 0`,
  numerically B1–B3: A·a = const with a growing); contracting branch (B4, ℋ < 0)
  **grows** the amplitude (A·a = const with a decreasing) — sign control;
- averaging measure: sin/cos projections on the box are exactly orthonormal for box
  harmonics: `<sin²> = <cos²> = 1.000000000000000` (discrete measure);
- limiting case: `ℋ ≡ 0` (B5, flat space) reproduces the flat wave equation with
  constant envelope (residual `2.2e-11`) and phase speed `c_T = 1.0000000000`;
- substitution back into the original equation: symbolic transport-equation residual
  = 0 (D3) and Lean `transport_law`; EOM direct-from-action (D1).

---

## 3. Numerical evidence (as240_numeric.py, all residuals actual)

| ID | Check | Observed (coarse → refined grid 2400 → 9600 steps) | Threshold | PASS |
|---|---|---|---|---|
| N1-B1 | matter era `a=(η/4)²`, k=30: `A·a = const` | 6.9e-5 → 6.9e-5 | 1e-3 (WKB O((H/ω)²) bound) | ✓ |
| N1-B2 | radiation `a=η`, k=60 | 7.2e-9 → 4.0e-11 | 1e-3 | ✓ |
| N1-B3 | de Sitter `a=1/(1−0.05η)`, k=10 | 6.1e-5 → 6.1e-5 | 1e-3 | ✓ |
| N1-B4 | contracting (sign control) | 4.2e-5 → 4.2e-5, A grows ∝ 1/a | 1e-3 | ✓ |
| N1-B5 | flat `ℋ=0` (limiting case) | 2.3e-8 → 2.2e-11 | 1e-6 | ✓ |
| N1-B5s | phase speed c_T | 1.0000000000 | \|c_T−1\| < 1e-6 | ✓ |
| N2 | WKB order: err = C₁(H/ω)² + C₂(H/ω)⁴, ω/H ∈ {6,9,24,60} | C₁ = 0.52, leading slope −1.973 | −2.00±0.05 | ✓ |
| N3 | `D_L^GW = D_L^EM` (matter+Λ, 401 z) | S constancy 4.4e-16; max ratio dev 3.3e-16 | 1e-10 | ✓ |
| NC-1 | planted friction 0.12 fired & recovered | resid 0.12 ≫ σ; γ̂ = 0.11987 | fires + recovers | ✓ |
| NC-2 | G_N miscalibration: z-independent, γ̂ ≈ 0 | 2.6e-16; γ̂ = −1.3e-4 | 1e-13; γ̂ ≈ 0 | ✓ |
| NC-3 | exponent δ̂ ≈ 0; planted 0.08 recovered | +2.7e-4; 0.08027 | δ̂ ≈ 0; recovery | ✓ |

Refinement: one mandated refinement executed (2400 → 9600 time steps) and reported per
case; N3 additionally evaluated the fine z-grid; residuals converge with the grid
(B2: 7.2e-9 → 4.0e-11; B5: 2.3e-8 → 2.2e-11; the B1/B3/B4 plateaus at ~6e-5 are the
physical O((H/ω)²) WKB correction, not numerics — confirmed by the N2 slope test).

---

## 4. Footings (both, separate)

The derived law is **dimensionless** (`A ∝ 1/a` and `D_L^GW/D_L^EM = 1` contain no a0);
it applies identically to both footings — the propagation-only tensor sector never
involves a0, which lives in the static/gate sector of the action:

- canonical `a0 = 9.3619e-11 m/s²`, κ = 1/2 (adopted): `ρ_Λ = 5.844412454e-27 kg/m³`,
  `ε_Λ = 5.252695960e-10 J/m³`;
- alternative `a0 = 1.1279e-10 m/s²`: at fixed `ρ_Λ` (canonical density) `κ_eff =
  0.6023884041 ≠ 1/2`; at fixed κ = 1/2 `ρ_Λ′ = 8.483089620e-27 kg/m³`, `ε_Λ′ =
  7.624220727e-10 J/m³`.
- Cross-consistency with AS658/AS215 footing constants: |diff| < 1e-4 relative. ✓

---

## 5. Main result (exact claim)

Let (g, M_P² = 1/(8πG_bare), S_b[g], carrier/gate sector of FINAL_ACTION §1–7) be the
CA5-GNC-R action on the homogeneous expanding inactive FRW branch
(3M_P²H² = M_P²Λ + ρ_b + ρ_d, f = G = 0, z = 0), with a TT tensor mode of comoving
wavenumber k, ω = |k| ≫ H, and WKB initial data as in §0. Then, on the periodic box
[0,2π), η ∈ [η0, η1]:

1. **Amplitude transport (derived):** the envelope obeys `A′ + ℋA = 0`, i.e.
   `A(η) = A0·a0/a(η)`, with relative error O((H/ω)²) (C₁ = 0.52 in
   `err = C₁(H/ω)² + C₂(H/ω)⁴`, slope −1.973 ± 0.05); substitution residual exactly 0
   (sympy + Lean).
2. **Luminosity distance (derived):** `D_L^GW(z) = D_L^EM(z)` identically in this
   sector for constant M_P; numerically 3.3e-16 over z ∈ [0.02, 2] (matter+Λ
   background).
3. **Negative control (passed, capable of failing):** a changed G-normalization
   (`G_N` instead of `G_bare`, √c_N factor) is a z-independent calibration —
   `max|ratio(z) − mean|/mean = 2.6e-16`, fitted friction exponent γ̂ ≈ 0 —
   and is **distinguished from** a propagation-friction term, which produces
   z-monotone residuals of O(γ) that the calibration model cannot absorb (NC-1).

Target classification: **derived** (scoped, propagation-only, no binary emission
model imported). It does **not** promote to complete gravity closure (see §7).

---

## 6. Lean certificate

`AS240_transport.lean` (self-contained, house build `fable_independent_2026/lean_2026`,
compiled with `lake env lean` from the compile host; **no files written into the
compile host**):

| Theorem | Statement | Compile | Axioms |
|---|---|---|---|
| `transport_law` | `deriv (fun t => A0*a0/a t) η + (deriv a η / a η)·(A0*a0/a η) = 0` (WKB amplitude law satisfies the transport equation) | exit 0, zero sorry | {propext, Classical.choice, Quot.sound} |
| `flux_scaling` | `(ω0a0/a)²(A0a0/a)²a⁴ = ω0²A0²a0⁴` (flux ∝ ω²A² dilutes as a^{-4}) | exit 0, zero sorry | {propext, Classical.choice, Quot.sound} |

`AS240_axioms_check.lean` re-verifies both via `#print axioms` (unfiltered). Outputs:
`lean_raw.out` (silent, warnings only), `lean_axioms.out`.

---

## 7. Limitations and next unresolved implication

**Limitations (not established):**
- WKB/geometric-optics order: `A ∝ 1/a` is the leading-order law with a quantified
  O((H/ω)²) correction; the ε⁰ transport equation is not solved to next order
  (not needed for the distance equality at this order).
- The tensor operator was derived directly from the pinned action because sibling
  **AS238 (tensor dispersion) is not landed**; the direct action check (D1) and the
  c_T = 1 phase-speed control substitute for it at this level, but the sibling's full
  dispersion/dof content remains formally open.
- Propagation-only: no binary emission model imported, so no absolute strain
  prediction for specific sources; the observed radiation reaction in matter
  (matter-era drag comes only from the background) is out of scope.
- Constant `M_P` assumed per the action's parameters: `G_bare` const, `c_N` const;
  the varying-M_* comparison (D5) is derived as a diagnostic, not a framework branch.
- κ = 1/2 remains adopted (campaign mandate); the footings are separate as required.
- No empirical data fits; numerics are double precision on the declared finite
  domain; the phase-speed check covers one mode family on one background.

**next_unresolved_implication:** the emission-side bridge — the standard-siren /
binary-model link between the propagation-only law `A ∝ 1/a` (and `D_L^GW = D_L^EM`)
and an observable strain for a compact binary in the common action, which requires
the tensor two-point source coupling (Newtonian-order emission amplitude with G_N) of
the CA5-GNC-R action; sibling AS238's full dispersion analysis; and the
GW170817-type bound on c_T (exact 1 here at WKB order) at finite H/ω.

**suggested_followup (child, ready spec in result.json):** AS240.C01 — "Tensor
two-point emission amplitude and standard-siren strain from the CA5-GNC-R action":
linearized TT source term `(M_P²/2)∫√−g h_ij T_{b}^{ij}` with the S_b[g] matter
coupling, quadrupole amplitude with `G_N` vs `G_bare` bookkeeping, and a
GW170817-consistent c_T bound statement; discriminating control: the √c_N
calibration shift of this seed's NC-2 must appear as the emission-side counter-term.

## 8. Assets

`derivation.md` (this file), `as240_derive.py` + `derive_raw.out`, `time_mem_derive.txt`,
`as240_numeric.py` + `numeric_raw.out`, `time_mem_numeric.txt`, `AS240_transport.lean`,
`AS240_axioms_check.lean`, `lean_raw.out`, `lean_axioms.out`, `result.json`.
All SHA-256 in result.json (artifacts_sha256).