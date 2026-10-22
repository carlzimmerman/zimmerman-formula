# C4_khronon_parent: is the Blanchet–Skordis Khronon theory a covariant parent of the screened theory?

## Verdict: EMBEDS WITH EXTRA TERM

- **The L★ → 0 sector embeds exactly, with no addition.** The Khronon's static limit is AQUAL. Choosing
  J = J_x gives μ = x/(1+x) exactly. A33's P sector at γ = η = 0 is the Legendre dual of J_x, and its clock term is
  the Legendre coupling P·A.
  - So A33/PAPER49 at L★ = 0 **is** a Khronon theory: the foliation is τ, and D_i ln N is the khronon acceleration A_i.
- **C1's khronometric obstruction does not arise.** The foliation is hypersurface-orthogonal, yet the law is AQUAL off
  symmetry, identically. The curl-free constraint acts on A_i = ∂_i ln N, which is curl-free in AQUAL as well. The
  auxiliary P* = (1−μ)∇Φ/K is not constrained, and it has a curl.
- **The Khronon cannot screen the Sun on its own.** Its only length is μ⁻¹ ≥ 100 kpc.
  - With J_x, planets see the full a₀: 1.08e4–8.07e4 × the ephemeris bounds.
  - With a turn-off J (which BS require anyway), Q₂ under AQUAL still fails at every y_t: 2.44× (canonical) and 2.85×
    (alt) the Hees 2σ line at best.
- **What the screened theory needs on top of the Khronon:**
  - P is promoted from an auxiliary to an independent spatial covector (n·P = 0, 3 components);
  - one term −(γ_L/2)(D_iP^i)², with 1 constant (L★).
  - The result is A33 written covariantly with τ.
- **Cosmology.** The dust abundance is again an initial condition, as in AeST (C2): I₀ is the khronon's shift charge,
  so Ω_K is **FITTED**. Y ≡ 0 on FRW, so a₀ is absent from the background.
- **A new matching (DERIVED, under one literature premise).** Take BS25's normalisation J(∞) = 0. Then the action gives
  an identity: Λc⁴/a₀² = 2∫₀^∞(y − y_N)dy = **2F(y_t)**.
  - This is twice the record's closure, F(y_t) = Λc⁴/a₀².
  - So y_t = **33.94** (canonical), **23.70** (alt) and **33.98** (κ = ½), not 66.30 / 46.01 / 66.38.
  - This applies only to the turn-off branch, which fails Q₂ anyway.

The script `c4_khronon_parent.py` (sympy + scipy) gives **8/8 PASS**, exit 0, in 1.4 s, 0.12 GB RSS, single thread.
- The criteria were frozen first (b0ea16ecf1).
- `C4_MUTATE=1` makes K1 (f = 1 − J′), K3 (ξ = 2) and K8 (no factor 2) FAIL (5/8). Outputs are in `*_MUTATE.*`.

Settings: κ = ½ FITTED. Footings 9.36e-11 / 1.13e-10 m/s², never pooled. No dark-matter particle. Not "theory closed".
Nothing here says the data favour the framework.

## Source of the Khronon equations (external, PROVISIONAL)

- BS24 = arXiv:2404.06584v2 (JCAP 11 (2024) 040) and BS25 = arXiv:2507.00912v1 were **read via WebFetch** of the arXiv
  HTML on 2026-10-22. They are **not verified on disk**. No download was made.
- The record's earlier transcription (`fable_independent_2026/KHRONON_2404.06584_COMPARISON.md`) agrees on Eqs. (1)–(7).
- Used:
  - S = (c³/16πG)∫√−g[R − 2J(Y) + 2K(Q)] (BS24 Eq. 6, BS25 Eq. 1);
  - Q, n_μ, A_μ = c²n^ν∇_νn_μ = −c²q_μ^ν∇_ν ln Q, and Y = A·A/c⁴ (Eqs. 1–5);
  - K = μ²(Q−1)² (Eq. 7);
  - Eq. 24 (φ = ψ), Eq. 35 (∇·[(1+J_Y)∇φ] + μ²φ = 4πGρ), and Eq. 37 (deep-MOND J);
  - Eq. 40 (J → Λ∞ at strong field), Eq. 39 (μ⁻¹ ≫ 100 kpc), and Eqs. 47/53/57 (FRW);
  - BS25 Eq. 4a (J = 0 at Y ≫ a₀²/c⁴), Eq. 4b (J(0) = Λ, the measured one) and Eq. 17 (ρ̄_K).
- **Every equation used is re-derived from the quoted action.**
  - K1 checks Eqs. 3, 24 and 35.
  - K7 checks Eqs. 47, 53, 57 and BS25 17.
  - All residuals are 0, so the transcription is self-consistent.
- The WebFetch summary also reported a "c²/a₀" coefficient in BS24 §3.1, against the 2/3 of Eq. 37.
  - Eq. 37 is the one consistent with f → y in deep MOND (K2).
  - The §3.1 text was not seen directly.

## Results (COMPUTED by sympy from the quoted action, or DERIVED from stated premises)

**1. The static limit (K1): AQUAL, not QUMOND.**
- Setup: static metric with ψ (lapse) and ϕ (spatial), no symmetry, τ = t.
- A_i computed from n_μ equals ∂_i ln N exactly. Y = ε²|∇ψ|² + O(ε³).
- The O(ε) Lagrangian is a total derivative.
- The Euler–Lagrange equations give **ϕ = ψ** and **∇·[(1 + J′(Y))∇ψ] + μ²ψ = 4πGρ**, with residuals 0.
- The interpolating freedom is the whole function J: μ(x) = 1 + J′(Y).
- Lensing sees the same potential as dynamics (ϕ = ψ).

**2. μ = x/(1+x) (K2): yes, exactly.**
- J_x = Λ − 2a₀²[y − ln(1+y)], with y = √Y/a₀.
- Then 1 + J_x′ = y/(1+y) exactly, and the small-Y series is Eq. 37 term by term.
- But J_x/√Y → −2a₀ at large Y. So x/(1+x)-exact lies **outside BS's admissible class** (Eq. 40 / 4a), which demands
  J → const. That is the a₀ planetary tail again, in Khronon language.

**3. The clock term (K3): the Legendre coupling; ξ is not forced.**
- A33's static γ = η = 0 Lagrangian is −|∇Φ|²/2K + ξP·∇Φ − W(K|P|). Eliminating P algebraically gives BS's static
  Lagrangian with J = J_x **at ξ = 1** (residual 0).
- For general ξ, μ_ξ = (a₀(1−ξ²) + ξg)/(a₀ + ξg). At ξ = 2 it reproduces A33 K5: −0.550 a₀ at g = a₀/3.
- So in the Khronon parent, ξ = 1 is the statement "J = J_x, given W". It is a representation choice, not an
  independent fact.
- **This is weaker than AeST**, where the 2:1 ratio forces ξ = 1 (C1 K4).
- The covariant clock P^μA_μ (n^μP_μ = 0) reduces to P^i∂_i ln N exactly (K6).

**4. Curl structure (K4): AQUAL off symmetry; the obstruction is AeST-specific.**
- C1 showed that a hypersurface-orthogonal AeST aether makes V = ∇χ + Q₀a curl-free. That is "Newton + an AQUAL scalar",
  off by E2's transverse fraction 0.2185.
- The Khronon's nonlinearity acts on the lapse itself, so the field equation is Bekenstein–Milgrom AQUAL for any
  distribution: Khronon − AQUAL ≡ 0.
- For a non-symmetric test field (two masses), the auxiliary P* = (1−μ)∇Φ/K has |∇×P*|/|∇P*| = 0.126, while ∇×∇Φ = 0.
- So the curl that AQUAL needs lives in an unconstrained auxiliary, not in the foliation.
- The obstruction belongs to **how AeST builds V from the aether**, not to having a preferred foliation.

**5. Screening (K5, K6): the pure Khronon cannot do it.**

| pure-Khronon option | result | source |
|---|---|---|
| J_x (μ = x/(1+x) exactly) | planet anomaly = a₀: Earth/Mars/Saturn 1.08e4 / 6.69e4 / 1.34e4 × bound (canonical), 1.30e4 / 8.07e4 / 1.61e4 × (alt) | C1 json (= D7d no_turnoff) |
| any turn-off J obeying Eq. 40/4a | AQUAL Q₂ / Hees 2σ ≥ 2.44 (canonical), ≥ 2.85 (alt) at every y_t row; Q₂ is set by the law near y ≈ 1 | E2 json, D7b |
| the K(Q) mass term | μ²r² = 1.2e-13 at 7000 AU (μ⁻¹ = 100 kpc): inert | BS24 Eq. 39 |

- The screened theory's stiffness is non-perturbative where it acts: (L★/r)² = 2.5e13 (24 pc) to 3.4e14 (90 pc) at 1 AU.
- So P cannot be integrated out into a local lapse operator. To O(γ) it would be the Hořava-type operator
  (γ_L/2K²)(D_i[(1−f)A^i])², but that expansion fails in the Solar System.
- **P must be an independent field.**

**6. Cosmology (K7): the abundance is an initial condition.**
- On FRW, Y ≡ 0, so J contributes only J(0) = Λ. a₀ is absent from the background, as C2 found for AeST.
- The minisuperspace action gives:
  - K_Q = I₀/a³, with I₀ the conserved shift charge of τ;
  - Q̄ = 1 + I₀/2μ²a³;
  - ρ̄_K = I₀(1 + w̃₀/a³)/(8πGa³);
  - w = w̃₀/(w̃₀ + a³).
  All residuals are 0.
- **I₀ is an integration constant, so Ω_K is FITTED.** BS25 put Ω_K,0 ≈ 0.26 by hand.
- The quadratic K is stiff early (w → 1). BS25's DBI K that cures this adds a second constant, λ_D.
- The Khronon does not derive A33's medium abundance (5.3643 ρ_b) either.

**7. Closure identity (K8): DERIVED under the premise J(∞) = 0.**
- Λ = J(0) − J(∞) = ∫(1 − f)dY = (2a₀²/c⁴)∫₀^∞(y − y_N)dy.
- Integration by parts gives ∫D dy = ∫D dy_N, with D = y − y_N, because the boundary term D²/2 vanishes at both ends.
  It is checked numerically to 4e-16 on the record's turn-off law, and y(y_N) is monotone (min dy/dy_N = 0.987).
- So the Khronon form of the record's closure is **2F(y_t) = Λc⁴/a₀² = 8π/κ²**.
- y_t (Khronon) is 33.94 / 23.70 / 33.98 (canonical Λ / alt Λ / 32π), against the record's 66.30 / 46.01 / 66.38.
- This does **not** select κ: y_t stays a relabelling of κ (D7).
- It holds only if Λ∞ = 0. Under BS24's general Eq. 40 (Λ∞ free) there is no closure at all.
- Consequences of the halved y_t for wide binaries: **not computed** (OPEN).

## Which parent needs fewer additions? (C1 vs C4)

| item | AeST (C1) | Khronon (C4) |
|---|---|---|
| AQUAL μ = x/(1+x) | yes, F = (2−K_B)𝒥 at the λ_s → ∞ boundary | yes, J = J_x (outside BS's Eq. 40 class, like AeST's capped F) |
| curl structure off symmetry | needs a **twisting** aether; the khronometric version fails (0.2185) | AQUAL identically with a hypersurface-orthogonal foliation |
| clock coefficient ξ = 1 | **forced** by AeST's 2:1 ratio | a representation choice (absorbed in J) |
| curl stiffness γ_F | supplied (K_B, aether twist) | not supplied; one more term (or A33's choice γ_F = γ_L) |
| longitudinal stiffness γ_L (screens the Sun) | **1 extra term**, (q∇∇φ + θQ)², second derivatives of φ, outside F(Y, Q); DOF OPEN | **1 extra field** (P, 3 comps) **+ 1 term** −(γ_L/2)(D·P)², first derivatives only = A33's own term |
| dust abundance | Q₀I₀, I₀ free → Ω_c FITTED | I₀ free → Ω_K FITTED; quadratic K stiff early, DBI adds λ_D |
| a₀ in the FRW background | absent | absent (Y ≡ 0) |
| closure Λ ↔ (a₀, y_t) | none | 2F(y_t) = Λc⁴/a₀² if J(∞) = 0 (turn-off branch only) |

- **By count, AeST needs fewer additions:** 1 term against 1 field + 1 term. It also forces ξ = 1 and supplies γ_F.
- **The Khronon's addition is lower order:** first derivatives of a vector, which is A33's own, already-audited form
  (A68's 5-DOF count). AeST's extra term has second derivatives of φ, and its DOF count is OPEN.
- The Khronon is the more **natural** parent: A33 is already a Khronon-vector theory. It is not the more **economical**
  one.

## The record's no-gos

| no-go | hypothesis vs the Khronon parent | applies? |
|---|---|---|
| NG1 (positivity at saddles) | ρ_c = ρ̄ + ∇·P with ρ_c ≥ 0 enforced | **no**, by class. The khronon "phantom density" (BSK1) has no sign requirement. It comes back if one identifies it with a positive cold medium. The "no saddle dip" depths are unchanged (same AQUAL). |
| NG2 / D9 V2 | Lorentz-invariant U(1) with a Gauss law | **no**, by class (preferred foliation, no U(1)) |
| D9 Λ_LV (foliated U(1), criterion A) | U(1) dark field with a Gauss law | **no**, by class. The Khronon's MOND field is the lapse, uncapped (g, not A33's u). Its nonlinear characteristic speeds are **OPEN**: BS say the ω = 0 mode becomes propagating at nonlinear order. |
| D-T (no linear self-gravity) | the medium is the phantom (Gauss identity, c₂ = 1) | escaped above 1/μ: the dust is from K(Q) (BS's CMB claim, external). But record BSK1/BSK2 find khronon dust self-gravity inert below 1/μ, and a σ₈ ratio of 0.037 at BS's μ (registered tension, not adjudicated) |
| D9b (A33 + multiplier) | the identity is enforced | **no**: Khronon + P is literal A33 without the multiplier |
| E5 G1–G5, Theorem G | A33's kinetic structure | inherited unchanged by Khronon + P (it is A33) |

- The record also claims (`fable_independent_2026`, L117/L119) that sourcing MOND from the lapse acceleration frees a
  conformal ghost. The pure Khronon is exactly that class.
- That claim is **not tested here** (OPEN). BS24 report 2 tensor modes + 1 ω = 0 mode on Minkowski, and an IR-unbounded
  Hamiltonian for k ≲ μ (record quote).

## Input ledger

| input | class | source |
|---|---|---|
| BS24/BS25 Eqs. 1–7, 24, 35, 37, 39, 40, 47, 53, 57; BS25 4a, 4b, 17 | literature via WebFetch, **not on disk**, self-consistency checked (K1, K7) | arXiv HTML |
| A33 static action, W, ξ, K5 value | FRAMEWORK-NATIVE | A33 `MASTER_ACTION.md` |
| planet ratios | RAW-derived bounds (record) / FRAMEWORK-NATIVE | `C1_aest_embedding/c1_aest_embedding_results.json` K6 |
| AQUAL Q₂/Hees per y_t row; transverse fraction 0.2185 | FRAMEWORK-NATIVE | `E2_field_equation/e2_field_equation_results.json` |
| turn-off kernel, Λ = 1.0890e-52 m⁻², y_t rows | FRAMEWORK-NATIVE (P5 posit; κ fitted) | D7 |
| a₀ footings | FITTED (κ = ½) | doors BRIEF |

No ΛCDM or standard-MOND machinery carries a verdict. BS's Ω_K ≈ 0.26 is quoted, not used.

## What this does not show

- The health of Khronon + P is not shown: J_x outside BS's class, the cap, and the nonlinear khronon mode are OPEN.
- Q₂ with γ_L only (γ_F = 0) is not computed. D7d used γ_F = γ_L. The Sun's hedgehog has F = 0, so the monopole is
  unaffected.
- Whether K(Q) dust could be the screened theory's collisionless medium (σ_c = √(a₀L★)) is OPEN.
- BS's CMB fit is not re-derived.
- The factor-2 closure's effect on wide binaries is not computed.
