# C1_aest_embedding: is the screened theory's static sector a limit of AeST?

## Verdict: EMBEDS WITH EXTRA TERM

- **What AeST reproduces.** Its quasi-static weak-field limit gives three things exactly: AQUAL with μ = x/(1+x),
  the clock term with coefficient 1, and the curl half of the stiffness (γ_F).
- **What it cannot reproduce.** The longitudinal half, γ_L (D·P)², is **identically zero** in AeST. It is also zero in
  any extension of AeST that only adds first-derivative aether terms.
- **Why that matters.** γ_L is the half that screens the Sun. One extra term is needed. It has one coefficient, and it
  is **outside AeST's F(Y, Q) class**, because it needs second spatial derivatives of φ.
- **Without that term**, the AeST version is the unscreened law in spherical systems. Planets then see a constant a₀
  anomaly, 1.1e4–8.1e4 × the ephemeris bounds.

The script `c1_aest_embedding.py` (sympy) gives **8/8 PASS**, exit 0, in 2 s, single thread.
- The criteria were frozen first (d9a9a17f4e).
- `C1_MUTATE=1` sets the J coefficient to (2−K_B) and adds (∇²χ)². K1, K3, K4 and K5 then FAIL (4/8).

Settings: κ = ½ FITTED. Footings 9.36e-11 / 1.13e-10 m/s², never pooled. No dark-matter particle. Not "theory closed".
Nothing here says the data favour the framework.

## Source of the AeST action (external input)

The action is Skordis & Złośnik, PRL 127, 161302 (2021), arXiv:2007.00082, **Eq. (5)**:

S = ∫√−g/(16πG̃)[R − (K_B/2)F² + 2(2−K_B)J^μ∇_μφ − (2−K_B)Y − F(Y,Q) − λ(A·A+1)] + S_m

- It is taken from the record's transcription, `real_research/bridge1_aest_equations.md`. That file says it was checked
  against the arXiv LaTeX (`newRMONDLett.tex`) on 2026-08-14. **The LaTeX is not on disk**: the repo and the
  filesystem were searched.
- So the action is **"from the literature, not verified on disk"**. The same holds for J^μ = A^ν∇_νA^μ and for the
  MOND-limit coefficient 2λ_s/(3(1+λ_s)a₀).
- No download was made.

## Results (all COMPUTED by sympy from Eq. 5, or DERIVED from the stated premises)

**1. The static limit (K1).**
- Setup: Newtonian gauge, φ = Q₀t + χ, A_i = a_i, and A₀ from the exact unit constraint. The truncation is O(ε²).
- AeST becomes, with V ≡ ∇χ + Q₀a:
  16πG̃ L = 2|∇Φ|² − 4∇Φ·∇Ψ + K_B|∇Ψ|² − K_B|∇×a|² + 2(2−K_B)∇Ψ·V − (2−K_B)|V|² − (2−K_B)𝒥(|V|²) + K₂Q₀²Ψ² − 16πG̃ρΨ.
- On shell Φ = Ψ, and this is **−(2−K_B)|∇Ψ − V|² + …**. That is PAPER49's Lagrangian, −|∇Φ − KP|²/2K, with
  K = 8πG̃/(2−K_B) = 4πG.
- All 6 Euler–Lagrange residuals are 0.
- The K₂ term is AeST's mass term, m² = K₂Q₀²/(2−K_B). It matters only at r ≳ 1/m ≳ 1 Mpc. The record writes 2K₂;
  that is a convention for K₂ and changes nothing here.

**2. AQUAL with μ = x/(1+x) (K2): yes, exactly.**
- The choice is F(Y, Q₀) = (2−K_B)𝒥(Y), with 𝒥 = 2a₀²[−y − ln(1−y) − y²/2] and y = √Y/a₀.
- Then 𝒥′ = v/(a₀ − v), |V| = a₀g/(a₀+g), and μ − x/(1+x) = 0.
- The small-Y limit is (2/3a₀)Y^{3/2} with no linear term. That is SZ's coefficient at **λ_s → ∞**. So G_N = G = 2G̃/(2−K_B).
- This 𝒥 is the **boundary** of SZ's family, not an interior point. The Newtonian regime is the cap Y < a₀² (like A33's
  u < a₀), not a finite λ_s.
- Whether a capped F is healthy in AeST's cosmology and stability is **OPEN**.
- Exact AQUAL also needs the curl length ℓ_F → 0 (point 4).

**3. Field map and clock (K3, K4).**
- **The vector.** K P_i = q_i^μ∂_μφ ≈ ∂_iχ + Q₀a_i, and Φ = Ψ. The longitudinal part of P is the scalar's gradient. The
  transverse part of P is Q₀ times the **twist** of the aether.
- **The foliation.** The screened theory's preferred foliation is the hypersurface-orthogonal part of A_μ.
- **The clock term.** It is AeST's J^μ∇_μφ, where J is the aether's acceleration (= D_i ln N for a hypersurface-orthogonal A).
  Its coefficient **ξ = 1 is forced** by AeST's fixed ratio 2(2−K_B) : (2−K_B) between the J·∇φ and Y terms (DERIVED from
  Eq. 5). A33 found ξ = 1 independently, from the law.
- **The record's ξ = 1 and AeST's 2:1 ratio are the same fact.**
- **Khronometric AeST does not work.** With A_μ hypersurface-orthogonal, V is curl-free. That gives "Newton + an AQUAL
  scalar", which is **not** AQUAL away from symmetry. The AQUAL V = (1−μ)∇Φ has a curl (K7); E2's transverse fraction at
  r_M is 0.2185. **So the embedding needs a twisting aether.**
- Static field content: (χ, a) → V has nullity 1 (K8). That leaves 3 components, the same as A33's P_i.

**4. The stiffness (K3, K5): the obstruction.**
- AeST supplies **γ_F = K K_B/((2−K_B)Q₀²)**, i.e. L★_F² = 2K_B/((2−K_B)Q₀²). It comes from the aether's Maxwell term
  acting on the twist.
- It supplies **γ_L = 0**.
- **Theorem (K5).** Suppose χ enters only through first derivatives (any F(Y, Q), the J term), and the aether has any
  weak-field gradient terms (K_B, c₁, c₂, c₃). Then the static longitudinal kernel of V has **no k² term**: it is
  −(K_B−2)(1+λ_L), exactly.
  - Reason: the χ equation forces ∇·E = 0. The longitudinal aether equation then gives ∇²(∇·a) = 0, so ∇·a = 0.
  - So χ absorbs V_L, and c₂ (θ²) is inert in the static sector.
- **The missing term** is −(γ_L/2K²)(q^{μν}∇_μ∇_νφ + θQ)². In the static weak field this is −(γ_L/2)(D·P)². It has
  1 coefficient.
  - It is not in AeST's class.
  - In the aether frame it holds only spatial second derivatives (no φ̈). Its full DOF and stability count is **OPEN**.
- **An alternative from the mutation.** (∇²χ)² gives γ_L,eff ≠ 0 **only if** an Einstein-aether longitudinal stiffness
  c₁+c₂+c₃ ≠ 0 is also added. That is two additions.
- In this embedding, A33's "chosen" γ_F = γ_L becomes a relation between two independent constants (K_B/Q₀² and γ_L).

**5. What the missing term costs (K6).**
- A radial P has F_ij ≡ 0. So without γ_L, the Sun obeys the unstiffened law **for any K_B, Q₀**.
- The anomalous sunward acceleration is then the full a₀ at every planet. This matches D7d's `no_turnoff` values to 4e-9.

| footing | Earth | Mars | Saturn |
|---|---|---|---|
| canonical, ratio to bound | 1.08e4 | 6.69e4 | 1.34e4 |
| alt, ratio to bound | 1.30e4 | 8.07e4 | 1.61e4 |

- At ℓ_F → 0, Cassini Q₂ is E2's AQUAL value, 2.44–4.59× the Hees line.
- At finite ℓ_F with γ_L = 0, Q₂ was **not computed**.

## The cold medium and the record's no-gos

**The cold medium (OPEN).**
- In the quasi-static limit, AeST's dust (its Q sector) appears only as the mass term m²Ψ.
- It **does not supply** the screened theory's collisionless medium (σ_c = √(a₀L★)) or the sourcing ς at pc–kpc scales.
- So the medium stays a separate sector, as A33's L_cold already is.
- Whether AeST's nonlinear dust could be that medium is OPEN (C2's lane).

**The no-gos.** Each one is escaped by its class, and each escape has a cost.

| no-go | hypothesis that fails for AeST | escaped? | cost |
|---|---|---|---|
| NG1 (positivity at saddles) | ρ_c = ρ̄ + ∇·P is enforced | yes (DERIVED): ∇·V is not the density of any field, and AeST's dust is the Q sector | "phantom = cold medium" is **false** here. ς stays a free functional (D9's "No" branch, like A33). The saddle's negative ∇·V is only field structure; "no saddle dip" is unchanged |
| NG2 (v² = 1 + g/a₀) | a Lorentz-invariant U(1) with a Gauss law | yes, by class (preferred frame, no Gauss law) | AeST's own characteristic speeds with the capped F are **OPEN**: 𝒥″ diverges at the cap, and the SZ stability paper is not on disk |
| D-T (no linear self-gravity) | the medium is the phantom (Gauss identity, c₂ = 1) | yes, by class. AeST's dust grows (external: SZ's CMB/P(k) fit) | the dust that grows is AeST's dust, **not** the screened theory's medium |

**Mode count.**
- A68 gives 5 DOF: 2 tensor + 3 P, with one η for both P_L and P_T.
- In AeST, the longitudinal kinetic term comes from K₂(Q−Q₀)² and the transverse one from K_B. That is a different
  kinetic structure.
- AeST's Minkowski count is from the literature and **not on disk**. It is not used. The dynamical match is OPEN.
  Only the static content (3 = 3) is computed.

## Input ledger

| input | class | source |
|---|---|---|
| AeST Eq. 5, J definition, λ_s coefficient, 1/m ≳ 1 Mpc | literature (not verified on disk) | `real_research/bridge1_aest_equations.md` |
| A33 / PAPER49 static action, W, γ = KL★²/2 | FRAMEWORK-NATIVE | A33 `MASTER_ACTION.md`, E2 README |
| planet bounds, `no_turnoff` anomalies | RAW-derived ephemeris bounds (record) / FRAMEWORK-NATIVE | `D7d_screened_q2/d7d_screened_q2_results.json` |
| E2 transverse fraction 0.2185, Q₂ 2.44–4.59× | FRAMEWORK-NATIVE | `E2_field_equation/` |
| a₀ footings | FITTED (κ = ½) | doors BRIEF |

No ΛCDM or standard-MOND machinery is used.

## What this does not show

- It does not show that AeST with the capped F and the γ_L term is healthy: ghosts, speeds and the full DOF count are OPEN.
- It does not cover the cosmology (C2) or whether L★, Q₀ and K_B are derived (C3). L★_F² = 2K_B/((2−K_B)Q₀²) is a
  relation, not a derivation.
- It does not give Q₂ at finite ℓ_F without γ_L.
