# CFG961 DERIVATION: CFG938's parent on FRW, its tensor speed and its cosmic clock (independent check of WT-02 / WT-05)

**Rules and records.**
- Criteria: `FROZEN_CRITERIA.md` (83b04219e), committed alone first. Amendment A1 (f3cbd85e5) is post hoc relative to scratch
  development runs and was committed alone before the graded run.
- Every number below is printed by `cfg961.py` in `cfg961.out` / `cfg961_results.json` (MUTATE: `cfg961_MUTATE.*`).
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Cold energy is gravitating mass; no particle species.
  Not "theory closed". Nothing here says the data favour the framework.
- No WT-02, WT-05, WT-07/08/09 or CFG938 code was imported, copied or run. The derivations start from CFG938's action as printed
  in its DERIVATION §3.4.

## 0. The action and the reading used

  S = ∫√−g [c⁴R/16πG − mc²n − W_full(u) − (3γ/4K²) τ_μν τ^μν + λ(D_μD^μχ − Kmn)] + S_b

**Definitions.**
- D_μD_νχ = h_μ^α h_ν^β ∇_α∇_βχ and D²χ = h^{μν}∇_μ∇_νχ.
- u² = h^{μν}∂_μχ∂_νχ, h^{μν} = g^{μν} + u^μu^ν; τ is the traceless part of DDχ.
- W_full = [−a₀u − a₀² ln(1 − u/a₀)]/K, γ = KL*²/2, K = 4πG.
- This is CFG938's own reading: its cfg938.py builds DD = h·∇∇χ·h, and its S1d uses D²χ̄ = −3Hχ̄̇ on FRW.

**The identity behind everything in (a)** (verified symbolically in `cfg961.out`, "linear D² χ"):

  h^{μν}∇_μ∇_νχ = ³Δχ − θ u^μ∂_μχ,  θ = ∇_μu^μ.

- On FRW, θ = 3H/c. The term −θ u·∂χ is how S1d makes χ̄(t) absorb ρ̄: −3Hχ̄̇/c² = Kρ̄_c, so χ̄̇ = −Kρ̄_c c²/(3H).
- At linear order the tilt of the medium's slices cancels between ³Δ and −θu·∂χ. The perturbed constraint contains no medium
  velocity (`cfg961.out`: D²χ = ∂_x²δχ/a² − 3Hδχ̇/c² with gravity off).

## 1. Claim (a): the linearised system on flat FRW

### 1.1 Construction (own sympy, `frw_system`)

**Expansion.**
- Medium labels φ¹ = x − εξ(t, x), φ² = y, φ³ = z, with u^μ from the conserved current.
- χ = χ̄(t) + εδχ, λ = εδλ (λ̄ = 0, CFG938's "no tether background").
- Every covariant piece is expanded with a truncated ε-series algebra. W_full enters as u²/2K at O(ε²).
- The O(ε) Euler–Lagrange expressions vanish once Friedmann and S1d are used (check `A_tadpoles_vanish`, all three gravity
  models).

**Three gravity models.**

| model | status | what it contains |
|---|---|---|
| **off** | frozen secondary | metric unperturbed |
| **qs** | frozen primary | quasi-static Newtonian Φ = Ψ with −a\|∂Φ\|²/2K |
| **gr** | A1 | the full scalar sector: lapse Ψ, shift B, Φ, E; EH from √−g R to O(ε²); baryons as a second dust; Λ |

In the gr model, Newtonian gauge (B = E = 0) is set after variation, so the system is 8 × 6.

**Frozen coefficients.** a = 1 at the instant, ȧ = H, Ḣ = −Kρ_m, plane waves e^{σt + ikx}.

### 1.2 The χ and λ equations (gravity off; the matter sector's principal part)

Rows of the 3 × 3 system, in the order (δχ, δλ, ξ), with X ≡ χ̄̇ and m ≡ ρ̄_c:

- **Vary λ (the χ constraint):**
  − (c²k² + 3Hσ) δχ/c + iKck m ξ = 0,
  i.e. ∇²δχ/a² − (3H/c²)∂_tδχ = Kδρ_c.
- **Vary χ (the λ equation):**
  (3Hσ − c²k² + 9H² + 3Ḣ) δλ/c − c k²(K + γk²) δχ/K² + iXkσ ξ/(Kc) = 0.
- **Vary ξ (the medium):**
  −σ[(Kc⁴m − X²)σ + …] ξ/(Kc³) − iKck m δλ + ik(Xσ + 3HX + Ẋ) δχ/(Kc) = 0.

What these rows show:
- The medium feels the force −ρ̄_c∇(Kδλ).
- Its inertia is ρ̄_c(1 − X²/Kc⁴ρ̄_c) = ρ̄_c(1 − Kρ̄_c/9H²) = ρ̄_c(1 − Ω_c/6). This is the cosmic clock acting on the medium; see §3.

**The heat-type character of each field.** Compare the coefficient of ∂_t with the coefficient of −k²:

| equation | homogeneous root | type for H > 0 |
|---|---|---|
| χ | σ = −c²k²/(3H) | FORWARD-parabolic |
| λ | σ = +c²k²/(3H) | BACKWARD-parabolic |

For H < 0 the roles swap.

**Dispersion relation.** It is quartic in σ, with leading coefficient −9H²(Kc⁴m − X²)/(Kc⁵). At leading order in k the roots
are σ = ±c²k²/(3H) exactly, plus two roots: Hubble-rate roots and the stiffness oscillation σ² ≈ −γρ̄_c k².

### 1.3 Hadamard scan

Grid: z = 0 and 10; H > 0 and H < 0; L* = 24 pc and 1 kpc; c/k from 100 Mpc to 24 pc (physical, at the frozen instant).

**gravity off and full GR (A1): ILL-POSED in all 8 backgrounds.**

| c/k | max Re σ/\|H\| (z = 0) | max Re σ/\|H\| (z = 10) |
|---|---|---|
| 1 Mpc | 6.595e6 | 1.577e4 |
| 1 kpc | 6.595e12 | 1.577e10 |
| 24 pc | 1.145e16 | 2.737e13 |

- The slope over the top decade is 2.0000.
- The ratio to c²k²/(3|H|) at the top k is 1.0000000000.

**Full-GR rank test (A1).** At each root, the equilibrated 8 × 6 matrix has s_min/s_max of:
- 8.6e-8 / 5.0e-17 (z = 0, c/k = 1 Mpc / 24 pc);
- 2.3e-5 / 1.4e-14 (z = 10);
- ≤ 6e-8 for H < 0.

At σ(1 ± 1e-3) it is ≥ 0.17. The residual is s_min ≈ 1.1–1.7 (H/ck)², which is the frozen-coefficient error. At z = 10,
c/k = 1 Mpc it exceeds A1's literal 1e-6 line; see §5.

**Quasi-static model (frozen primary).**
- The fast root is shifted by about 0.9% at kL* ≲ 1.
- At kL* ≫ 1 it is strongly distorted: top ratio 0.249 (z = 0, L* = 1 kpc) and 0.080 (z = 10, L* = 1 kpc), slopes 1.63 / 1.35
  (UNRESOLVED).
- Its leading σ⁴ coefficient keeps a term 9X²k²(K²c⁴m + Kc⁴γk²m − X²γk²)/(K³c⁸) at H = 0.
- **Why it fails (A1.1).** The fast modes evolve at σ ≈ c²k²/3H, faster than ck. The λ-sector's pressure-type source λ·3Φ̇χ̄̇/c⁴
  (extrinsic curvature × clock) belongs in GR's trace-ij equation Φ̈ + … = 4πGδp. There it is suppressed by (H/ck)². The
  quasi-static model instead routes it into an elliptic Poisson equation.
- The full-GR system removes the distortion: its fast root equals the gravity-off root to (H/ck)².

### 1.4 The H → 0 limit (K-a1)

With X = χ̄̇ held as an independent symbol (gravity off):
- The leading coefficient vanishes at H = 0, so the degree drops by two.
- The two fast roots are ±c²k²/(3H). They leave to infinity as H → 0: **the limit is singular, and a slower expansion makes the
  growth faster.**
- At H = X = 0 (c → ∞) the remaining roots are σ² = −(Kρ̄ + γρ̄k²). This is CFG938's S5a at u₀ = 0 without self-gravity: the
  tether gives +Kρ, and with gravity on that cancels −Kρ, leaving σ² = −γρ̄k² (quasi-static row).

In a general medium the operator is −θ u·∂χ with the local θ. Any region whose medium expands or contracts (θ ≠ 0) has growth
rates of order c²k²/|θ|.

### 1.5 CFG938's flat static result is reproduced (K-a2–K-a4)

- **K-a2.** Static medium with a uniform background gradient u₀ẑ (WKB, own quadratic action including W_full's Hessian):
  ω² = γρ₀k² + Kρ₀[R′(u₀)cos²θ + (R(u₀)/u₀)sin²θ], R = u²/(a₀ − u).
  - This is identical to CFG938 S5a (sympy difference 0).
  - The z-inertia is ρ₀ − D(u₀)u₀/(Kc²), as in CFG938 S5c.
- **K-a3.** Slip (W-only) on CFG847's five systems is within 0.3% of CFG938's printed values in every row (worst 5.792e-6,
  CFG938 5.79e-6).
- **K-a4.** NGC 3198, 43 radii: max |g_EL/g_law − 1| = 2.2e-16 on both footings. Also θ = 0 identically for a static medium in
  any static metric, so the −θu·∂χ term cannot reach the law (structural).

So CFG938's "linearly well-posed" statement is correct for what it computed: static media, flat space, WKB.

## 2. Multiplier or physical?

The question is whether the backward-parabolic λ is a Lagrange multiplier that could be solved as a constraint or boundary
problem without affecting the physical Cauchy problem. Four independent arguments say no.

**P1: λ stops being a multiplier on FRW.**
- The quadratic Lagrangian contains −(3a²ȧ/c) δλ ∂_tδχ, i.e. a p·q̇ term (`cfg961.out`, P1).
- In Dirac's analysis the primary constraints φ₁ = p_χ + 3a³Hδλ/c ≈ 0 and φ₂ = p_λ ≈ 0 have bracket {φ₁, φ₂} = 3a³H/c ≠ 0, so they
  are second class.
- λ is then χ's canonical momentum, and (χ, p_χ) is one propagating degree of freedom per point. Its Hamiltonian is linear in
  p_χ, so it is unbounded.
- At θ = 0 the bracket vanishes, λ is a true multiplier, and the χ/λ sector has 0 DOF. The degree-of-freedom count jumps at θ = 0.

**P2: the growing mode moves the medium and the metric.** Eigenvectors are normalised to Kδλ = 1 (z = 0, L* = 24 pc).

| model | case | σ/(c²k²/3H) | medium acceleration \|σ²ξ\| / \|k·Kδλ\| | δ_c / (k²Kδλ/σ²) |
|---|---|---|---|---|
| gravity off | c/k = 1 kpc | 1.0000000000 | 1.0461 = 1/(1 − Ω_c/6) | 1.0461 |
| full GR | c/k = 1 kpc | 1.0000000000 | 1.0492 | 1.0492 |

- **Gravity off.** The medium is accelerated by the full λ force, corrected only by the clock-modified inertia.
- **Full GR.** The Bardeen potential is |Φ| = 2.0e-14 |Kδλ| = 0.397 (H/ck)² |Kδλ|, which is Kρ̄_c/H² × (H/ck)², exactly what the
  λ-sector's energy density Kρ̄_cδλ sources. The full 8-row residual of the eigenvector is 2.7e-13.
- **Contracting media (H < 0).** The growing mode is χ-led (|δχ| = 1.9|Kδλ|), and the medium moves with χ.
- **Control MU5.** When λ is decoupled from the medium and gravity is off, the growing eigenvector is pure δλ (δ_c = 0,
  δχ = 0). The test does distinguish a multiplier-only growth from a physical one.

**Bianchi: in GR the λ equation is an Einstein equation.** Drop two rows of the 8 × 6 full-GR system and check whether the fast
root survives:
- **The λ equation (vary χ) can be dropped** together with the Euler, momentum or anisotropic row, and the fast root survives
  (ratio 1.00000000).
- **It cannot be dropped** together with the Hamiltonian constraint or the trace-ij equation (fast root lost: ratio 0).

When χ̄̇ ≠ 0, the contracted Bianchi identity makes the λ equation the time component of ∇_μT^{μν} = 0, and it follows from the
Hamiltonian constraint plus the trace-ij equation. So the backward-parabolic evolution is carried by Einstein's own equations.
λ cannot be "solved as a constraint" while the metric is evolved as an initial-value problem.

**P3: the final-data reading.**
- If λ is posed with final data, the system becomes a forward/backward two-point problem in time.
- The medium's present acceleration then depends on the future over τ_k = 3|H|/(c²k²): 0.22 yr at 10 kpc, 2.2e3 yr at 1 Mpc,
  2.2e7 yr at 100 Mpc (τ_k H₀ = 1.5e-11 … 1.5e-3).
- By the Bianchi argument, the metric would need the same final data.
- This is a different (teleological) theory, like the Abraham–Lorentz order reduction. It is not "linear well-posedness".

**Verdict: physical, not multiplier-only.**

**What removes it (MU2 = WT-02's MU3).**
- With the intrinsic slice Laplacian ³Δ, the χ and λ equations have no time derivative (elliptic). All roots are bounded
  (≤ 3.02|H| over the grid), in both the gravity-off and the full-GR system.
- But D²χ̄ = 0 then, so S1d fails. The background needs an explicit ρ̄ subtraction, which CFG938 avoided.
- WT-08 (criteria 1bf29e407, no committed result) is building that repair.

## 3. Claim (c): the cosmic clock

From §1.2, u² = |∂_xδχ/a + aχ̄̇ ∂_tξ/c²|². A medium moving at peculiar velocity v therefore sees the uniform medium-frame field

  u_v = γ_v v |χ̄̇|/c² = (Ω_c H₀/2) v = 2.888e-19 s⁻¹ × v

This is Newtonian order: c drops out.

**Size.**

| v (km/s) | u_v / a₀ (canonical) | u_v / a₀ (alt) |
|---|---|---|
| 30 | 9.26e-5 | 7.66e-5 |
| 370 | 1.142e-3 | 9.45e-4 |
| 630 | 1.94e-3 | 1.61e-3 |
| 1000 | 3.09e-3 | 2.55e-3 |

The claimed value 1.1e-3 a₀ at 370 km/s is reproduced: CONFIRMED.

**Preferred frame.** χ̄'s gradient is a timelike background vector, distinct from the medium's own frame, so it is a genuine
preferred frame. What the record's tests would see:

| test | comparison | label |
|---|---|---|
| SPARC (NGC 3198, 44.1 kpc) | u_v/u = 6.6e-3 / 5.9e-3 (dipole, cancels in the azimuthal average); (u_v/u)² ≤ 1.3e-4, vs a 26% rms | NOT VISIBLE |
| wide binaries (1.5 M☉ at 10 kAU) | u_v/g = 1.2e-3 (370) / 2.0e-3 (630), vs a few-% scale | NOT VISIBLE |
| Solar System | the whole tether pull at 1 AU is ≤ GM☉/L*² = 2.4e-16 (24 pc), ≤ 1% of an α₁ = 3.4e-5 signal (2.5e-14 m/s²) | NOT VISIBLE |
| KiDS h72 tail ends | r_×/r_end = 2.4–4.1 (370 km/s), 1.4–2.4 (630), 0.89–1.50 (1000) | UNDERDETERMINED (VISIBLE only for lenses moving ≳ 1000 km/s) |

**Where the clock already enters recorded numbers.**
- **The medium's inertia.** The factor 1 − Ω_c/6 is 0.956 at z = 0 and 0.860 at z = 10. This is the term behind CFG941's
  corrected growth exponent a^0.694.
- **The tensor speed** (§4). Through the slices' extrinsic curvature the clock sets c_T on FRW, and so the GW170817 path average.

## 4. Claim (b): tensor speed from the ττ term

**Construction (own sympy, `tensor_tau2`, `eh_avg`).**
- TT wave h_ij = (A₊e⁺ + A×e×)cos(k n·x − ωx⁰) on a locally flat background, with the medium at rest and a constant gradient
  ∂_μχ = (V₀, 0, 0, u₀).
- τ_ij at O(h) uses the Christoffels of η + h.
- ⟨τ²⟩ and ⟨√−g R⟩ are averaged over a period.
- EH normalisation: ⟨√−g R⟩ = ¼(A₊² + A×²)(ω² − k²), which is rotation invariant (K-b0).

**Result**, first order in L*², exact in angle and polarisation:

  δ(c_T²/c²) = (3/2) L*² [u₀² + 2V₀u₀ cos θ_k + V₀²] / c⁴ = (3/2) L*² [u_⊥² + (u_∥ + V₀)²] / c⁴

- **Spatial gradient (V₀ = 0).** The coefficient is exactly 3/2 for every θ_k and polarisation, so c_T/c − 1 = 0.75 L*²u²/c⁴.
  WT-02's coefficient is CONFIRMED, and so is A5's error.
- **Timelike gradient (u₀ = 0).** The same 3/2. On exact FRW, τ_ij = −(a²/2) ∂₀h_ij ∂₀χ̄. That gives the tensor kinetic
  coefficient Q_T = 1 − 3γχ̇²/K, the formula the sol61 audit derived on 2026-10-20 (`sol61_push/cold_covariant_audit_2026_10_20/
  RESULT.md`, in the repo at a67f9ed9c), before WT-02. Q_T(z = 4e8) is reproduced as −1325.41 (24 pc) / −2.30280e6 (1 kpc)
  against the audit's −1325.42 / −2.30281e6.
- **Other sectors.** W_full, λ̄ and n add only k-independent (mass-like) terms. The graviton-mass scale is ≤ a₀/c² = 1.0e-27 m⁻¹,
  against 2.1e-6 m⁻¹ at 100 Hz.

**Numbers (c_T/c − 1).**
- **Local, at the W wall (u = a₀):**

  | L* | canonical | alt |
  |---|---|---|
  | 24 pc | 4.46e-19 | 6.52e-19 |
  | 1 kpc | 7.75e-16 | 1.13e-15 |

  The wall-only limit is L* < 0.951 / 0.787 kpc.
- **Cosmic clock.** |∂₀χ̄| = cΩ_cH/2 = 8.658e-11 m/s², i.e. 0.925 a₀ (canonical) and 0.765 a₀ (alt). It does not depend on the
  footing. Along GW170817's path (z ≤ 0.0098, D_c = 43.5 Mpc), ⟨ū²⟩^½ = 8.766e-11 m/s².
- **Full path average.**
  - Clock: 3.91e-19 (24 pc) and 6.79e-16 (1 kpc).
  - Two galaxies (r ≥ 2 kpc each end): ≤ 2.3e-18.
  - Cross-term bound: ≤ 1e-17.
  - Total: 3.92e-19 – 6.82e-16. This is inside (−3e-15, 7e-16) on both footings at both L* ends.
- **L*_max** from the full path average is 1.015 kpc. WT-02's galaxy-only path model allowed 16–33 kpc.
- **Distance sensitivity (no class weight).** The 7e-16 line is 1.74 s over the conservative 26 Mpc. Over D_c = 43.5 Mpc the
  same 1.74 s gives 3.9e-16, and L*_max = 0.76 kpc.
- **Early universe (report only; sol61 audit).** If the medium exists early, Q_T = 0 at 1 + z = 1.10e7 (24 pc) / 2.65e5 (1 kpc),
  and Q_T < 0 before that. That is a negative tensor kinetic coefficient.

## 5. Classes

**(a) CFG938's parent is ill-posed off static backgrounds.**
- Frozen-rule class: **UNDERDETERMINED.** The frozen primary (quasi-static gravity) gives UNRESOLVED at L* = 1 kpc and fails
  K-a1, because it mis-models modes faster than ck (A1.1).
- A1 class, as written: **UNDERDETERMINED**, from one rank-test point (z = 10, c/k = 1 Mpc, 2.3e-5 against a 1e-6 line). The
  residual there equals 1.11 (H/ck)². The same test gives 1.4e-14 at c/k = 24 pc.
- **Substantive reading: CONFIRMED, physical.**
  - The gravity-off system (exact for the matter principal part) and the full-GR system agree to 1e-9 at the top k in all 8
    backgrounds.
  - All three P tests say physical.
  - The repair (MU2) removes it.

**(b) A5 "c_T = c (structural)" is wrong.**
- b1: CONFIRMED.
- b2: CONFIRMED (3/2, so 0.75).
- b3, "passes on the path average": CONFIRMED that it passes for L* ∈ [24 pc, 1 kpc]. NOT CONFIRMED as WT-02 argued it: the
  path model missed the FRW clock term, which dominates and puts L*_max at 1.0 kpc.
- "The local limit is at L* ≈ 1 kpc": CONFIRMED (0.95 / 0.79 kpc).

**(c) Hidden cosmic clock.** CONFIRMED. Visibility: NOT VISIBLE (SPARC, wide binaries, Solar System); UNDERDETERMINED (KiDS
tails); it enters the growth inertia (CFG941) and c_T (b3).

**WT-05 vs CFG955 / CFG958: CONSISTENT, no class change.**
- **CFG955.** WT-05's statements match CFG955's own outputs: Clausius H-theorem with a T_J bath = CFG955 L7; collapse = CFG955
  PH4's Bonnor–Ebert / Antonov instability. The isothermal thresholds 32.13 / 708.6 are reproduced.
- **CFG958.** CFG958's frozen T-S PASS rests on S1–S3 (SCT only), which WT-05 does not contest. Its V2 bracket ("class-A drift
  admissible", S5) holds only for the formal GENERIC entropy of CFG542. With the dust's Boltzmann entropy:
  - dS/dt = ∫ f ∇·v_s exactly (sympy);
  - deficit filling gives dS/dt < 0 (−0.372 in the toy).

  So the drift does exchange entropy. V2's own label ("only where no entropy is exchanged") and CFG958's class are unchanged; its
  bracket needs that qualifier.

**MUTATE** (exit 2 = not every tooth bites fully).
- MU2, MU3, MU4 and MU5 bite.
- MU1 (sign of −θu·∂χ flipped) bites only partly:
  - the forward/backward labels swap as required;
  - the system is ILL-POSED at z = 0 for both signs of H;
  - at z = 10, L* = 1 kpc it is UNRESOLVED. The flipped operator ³Δ + θu·∂χ is not a mirror image of the original: it keeps a
    medium-tilt coupling 2χ̄̇ δθ. At kL* ≫ 1 that coupling, together with the stiffness, turns the fast root oscillatory
    (σ ≈ −H ± 6.5e14 i H at c/k = 24 pc).
