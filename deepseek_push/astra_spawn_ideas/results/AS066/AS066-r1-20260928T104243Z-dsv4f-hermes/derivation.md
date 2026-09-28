# AS066 — Horizon coefficient comparison without a theorem leap

**Run:** `AS066-r1-20260928T104243Z-dsv4f-hermes` — worker `deepseek/deepseek-v4-flash-0731 (openrouter)` via Hermes focused subagent.
**Task sha256:** `880e86983dae32c7c76cbaba78f3854088724ee8c8c8975b47d5d559f6b394a5` (verified against the pinned value before execution).
**Sources verified pinned:** `PD01_polarization_count.py` = `37e39d1a…c2e74d`, `PD08_particle_free_derivation.py` = `83f6054c…f0cfb`, `k01_zero_mode_theorem_and_lambda_free_vacuum.py` = `8df5a3ab…35b25c` (byte-exact vs the AS066 seed and SOURCE_MANIFEST.json pins).
**Bounds enforced:** wall-time ≤ 120 s (`signal.alarm`), 1 thread (single process), memory: `setrlimit(RLIMIT_AS)` not enforceable on this macOS host (recorded honestly); observed wall 0.316 s, peak RSS 64 MB (61.4 MiB, `/usr/bin/time -l`). mpmath 80 dps.

---

## 1. Task, claim, symbols, boundary conditions, assumptions (seed step 1)

**Precise claim under test (the "named claim" of the seed):** compare, without importing an observational preference, the horizon coefficient
κ_h = √(8π/3)/(2π) — the coefficient that a0 = cH/(2π) with H² = 8πGρ_Λ/3 (Gibbons–Hawking/Unruh horizon form, k03) implies for a0 = κ c√(Gρ_Λ) — with the adopted framework coefficient κ_Z = 1/2, and identify exactly which of the proposed premises of the OR-channel program (channel integrality, unit slope, OR composition) exclude κ_h.

**Symbol dictionary** (all dimensionless positive finite parameters except where units are given):
- s = c√(Gρ_Λ) — vacuum rate (m/s²); Y = g/s (total acceleration in vacuum units); y = g_N/s (baryonic Newtonian acceleration in vacuum units); x = g/a0 (framework total-acceleration ratio); y_B = B/a0 = g_N/a0 (framework baryonic ratio; y_B = 2y under κ_Z).
- μ_n(Y) = 1 − (1+Y)^{−n}, n ≥ 1 — the MU_n response family on the declared branch (CORE coefficient; conditional MU_n statistical response). MU2 is the framework's registered member at n = 2: μ2(x) = 1 − (1+x/2)^{−2}, x = g/a0, y_B = g_N/a0, exactly as in FRAMEWORK_CONTRACT.
- OR-composed response over n equal independent channels with per-channel engagement p_λ, p_λ(0)=0, p_λ(∞)=1: μ(Y) = 1 − (1 − p_λ(Y))^n; λ = p_λ'(0) is the per-channel linear coefficient ("slope").
- κ ≡ a0/s is the framework coefficient; κ_Z = 1/2 adopted (framework input, NOT derived here); κ_h = √(8π/3)/(2π) the horizon comparison value.
- G_N, G_bare, G_cosmo kept separate: the horizon reading uses the same-G Einstein-frame formula H² = 8πGρ/3; the G-ratio variant is recorded (§7).

**Boundary conditions / domain:** Y ≥ 0, y ≥ 0, n ≥ 1 symbolic or n ∈ ℕ when integrality is invoked; p_λ(0) = 0 (frozen vacuum, zero drive → zero engagement, PD08 step 1), p_λ(∞) = 1 (saturation, μ(∞) = 1, L230 normalisation, PD08 step 2); deep-MOND spherical matching μ(g/s)·g = g_N (algebraic form of the weak-field Poisson law in the deep cell); Newtonian limit y → ∞: μ → 1, g → g_N.
**Framework inputs vs conclusions:** INPUTS — a0 = κ c√(Gρ_Λ) with κ = 1/2 adopted; G, c, M_sun, pc; both footings a0 = 9.3619e-11 and 1.1279e-10 m/s²; the MU_n branch and its OR reading as in the contract; the heat filter and MONO are NOT exercised (the object is the CORE coefficient cell). CONCLUSIONS to be established — the exact ratio κ_Z/κ_h, the conditional exclusion statement, and the matching-λ control values.

---

## 2. Exact ratio and which premises exclude κ_h (seed step 2)

**Exact ratio.** κ_h = √(8π/3)/(2π). Squaring: κ_h² = (8π/3)/(4π²) = 2/(3π), hence exactly

    κ_h = √(2/(3π)) = 0.4606588659617806390…   (80-dps value)
    1/κ_h = √(3π/2) = 2.1708037636748029781…  
    κ_Z/κ_h = (1/2)·√(3π/2) = √(3π/8) = 1.0854018818374014890…

All four identities verified exactly by sympy (`simplify` → 0) and at 80 dps; the square identity, the ratio, and the irrationality statements are Lean-certified (below). κ_Z/κ_h = √(3π/8) is transcendental (π transcendental ⇒ its positive square root is), in particular ≠ 1: the coefficients are not equal by an exact irrational factor 1.0854, i.e. 8.54 % (0.036 dex) — matching k03's separated 8.5 % separation.

**Premise analysis.** In the OR-composed family μ = 1−(1−p_λ)^n the deep matching gives exactly (μ ≈ nλ·Y near 0)

    nλ g²/s = g_N   ⇒   g² = a0 g_N with a0 = s/(nλ)   ⇒   κ = 1/(nλ).

Three proposed premises, evaluated one at a time (fixed: OR composition; μ(∞)=1; p(0)=0):

| premise set | κ attainable | κ_h attainable? |
|---|---|---|
| OR + unit slope (λ = 1), n ∈ ℝ | κ = 1/n, any real n | YES at n = √(3π/2) = 2.1708 |
| OR + channel integrality (n ∈ ℕ), λ free | κ = 1/(nλ) | YES: n = 2, λ = √(3π/8) = 1.0854 |
| OR + unit slope + integrality | κ ∈ {1, 1/2, 1/3, …} | **NO** (1/κ_h = 2.1708 ∉ ℕ) |
| no premise (general μ, slope m) | κ = 1/m, m ∈ ℝ⁺ | YES (trivially) |

So: **OR composition alone does not exclude κ_h; unit slope alone does not; channel integrality alone does not; the conjunction (unit slope ∧ integrality) does.** The weakest conditional exclusion, stated precisely:

> **Weakest conditional exclusion (proved, Lean H + sympy/numerics):** within the OR-composed response class with per-channel unit slope (λ = 1), the deep-MOND coefficient takes exactly the reciprocal-channel values κ = 1/n, n ∈ ℕ; the horizon coefficient is excluded exactly because 1/κ_h = √(3π/2) is not a natural number — indeed not rational (π irrational ⇒ 3π/2 is not a rational square; Lean G, H). Removing either conjunct admits κ_h: at fixed n = 2 a free per-channel slope λ = √(3π/8) reproduces it (negative control NC1); at fixed λ = 1 a real channel count n = √(3π/2) reproduces it (NC2).

This is exactly the structural statement PD01 carries as a consequence ("under κ = 1/n it would need n = √(3π/2) = 2.1708 — not a channel count"), now proved as a certificate with its scope and its two failure modes made explicit — the "theorem leap" the seed forbids (a universal exclusion would be false; the conditional one is true).

**Diagnostics at λ = 1/2, 1, 2** (n = 2, λ the per-channel linear coefficient): κ(λ) = 1/(2λ) = **1, 1/2, 1/4** — the values 1 and 1/2 are PD01's binary {1/2, 1} (which the two computed Poisson channels allow), 1/4 lies below both footings, and the matching λ* = 1.0854 lies between the λ = 1 and λ = 2 diagnostics; κ_h = 0.4607 sits between κ(λ=1) = 1/2 and κ(λ … ) = 1/3... (distances to the reciprocal lattice 1/n, n = 1..20 recorded in raw_output.json S2: nearest neighbour 1/2 at distance 0.0393, next 1/3 at 0.1273).

**Shape-parameter reading (unit slope kept).** With the completion p_λ(Y) = Y/(1+λY) (unit slope for every λ), μ'(0) = 2 for λ ∈ {1/2, 1, 2} — sympy `limit` gives exactly 2 in all three cases — so κ = 1/2 for every shape: within the unit-slope OR family the coefficient is completion-independent (the content of PD08 step 4, re-derived here), and κ_h is unreachable. This is the correct "universal within the unit-slope class" statement; it is false as a claim over all λ (NC1).

---

## 3. Intermediate algebra, scale factors, signs, units (seed step 3)

**Deep matching with all factors.** Spherical static source, weak-field law div(μ(|∇φ|/s) ∇φ) = 4πGρ_b; for a point mass the algebraic content is μ(g/s)·g = g_N with g_N = GM_b/r² (Newtonian baryonic field, positive outward radial). At Y → 0: μ_n(Y) = nY − n(n+1)Y²/2 + n(n+1)(n+2)Y³/6 − … (binomial, radius of convergence |Y| < 1), so with μ = nλY + …:

    nλ g²/s = g_N  ⇒  g² = (s/(nλ))·g_N,   a0 ≡ s/(nλ),   κ ≡ a0/s = 1/(nλ).   [sign: positive for all positive parameters; units: s in m s⁻², hence a0 in m s⁻²]

**Horizon coefficient provenance (same-G):** H² = 8πGρ_Λ/3 (de Sitter critical formula) and the adopted coincidence a0 = cH/(2π) give, symbolically (sympy, G a free symbol):

    κ = a0/(c√(Gρ_Λ)) = (cH/(2π)) / (c√(G·3H²/(8πG))) = √(2G/(3π)) = √(8π/3)/(2π) at G → 1.

i.e. κ_h is the coefficient *implied by* the horizon normalisation; the normalisation itself (cH/2π) is an adopted number, not derived — the seed's "adopted normalization useful only with its physical identification separately justified": the identification is the Unruh/Gibbons–Hawking horizon read, recorded as input, not derived here. With G_N ≠ G_cosmo the coefficient generalises to √(8π G_cosmo/(3 G_N))/(2π) (§7).

**Limiting regimes of the MU_n branch (n = 2 numerically, n symbolic in sympy), with leading neglected terms:**

- Deep (Y → 0): y = Y·μ_2(Y) = 2Y² − 3Y³ + 4Y⁴ − …; **leading neglected term −3Y³** (series domain |Y| < 1). Verified: at Y = 1e−6, (y − 2Y²)/Y³ = −2.99999600000… = −3 + 4Y − 5Y² + … (next term 4Y = 4e−6 confirmed to 1e−10).
- Newtonian (Y → ∞): y = Y − u/(1+u)², u = 1/Y ⇒ y = Y − 1/Y + 2/Y² − 3/Y³ + …; **leading neglected term −1/Y, next +2/Y²**. Verified at Y = 1e8: (Y−y)·Y = 0.99999998 (→1), ((Y−y) − 1/Y)·Y² = −1.99999997 (→ −2).
- Boundary/normalisation: μ_2(0) = 0 (zero field, zero response), μ_2(1) = 3/4 exactly (1 − 2⁻²), μ_2(∞) → 1 (normalisation; at Y = 1e8: 1 − 1e−16). The deep limit of MU2 in framework units is x = √y_B (g = √(a0 g_N)): the **shared deep a0-line**; the finite laws differ (below). Q and MU2 are distinct branches: at y_B = 0.1, x_MU2/x_Q = 1.0767 (>7.6 % deviation); at y_B = 1e−3, x_MU2 = √y_B·(1 + (3/8)√y_B + (13/128)y_B + O(y_B^{3/2})) with the two leading terms verified (residual 4.93e−7 vs O(y^{1.5})). RAR/EXP/MONO were not used for any conclusion (branch discipline; comparison-only in §4 table where Q is needed).

---

## 4. Independent check, different representation, actual residuals (seed step 4)

Representation switch: instead of the series, invert the implicit relation y = Y·μ_2(Y) by bisection at 80 dps over y = 10^k, k = −8..8 step 0.25 (65 points; bracket doubling, relative width 1e−70) and evaluate three independent objects:

1. **Forward residual:** max |μ_2(Y_sol)·Y_sol − y|/y = **8.82e−71** over the 65-point grid (tolerance 1e−60). Actual residual, not a Boolean.
2. **Deep a0-line approach in the solved inverse:** q ≡ g²/(a0 g_N) = 2Y²/y: at y = 1e−8, q − 1 = 1.0607e−4 with (q−1)/√y = 1.060729 vs 3/√8 = 1.060660 (leading term 3·2^{−3/2}√y; scaling confirmed at y = 10^{−7.75}). The a0-line is exact only in the y → 0 limit.
3. **MU2 x-representation:** solving x·μ2(x) = y_B (bisection, same precision; y_B = B/a0 = 2y under κ_Z) confirms the branch table below and the deep two-term expansion (above).

**Branch distinctness table (y_B = B/a0; comparison only):**

| y_B | x_MU2 | x_Q = √(y_B²+y_B) | x_MU2/x_Q |
|---|---|---|---|
| 1e−3 | 3.20010039e−2 | 3.16385840e−2 | 1.01145 |
| 1e−2 | 0.103853111 | 0.100498756 | 1.03338 |
| 0.1 | 0.357090196 | 0.331662479 | **1.07667** |
| 1 | 1.489288572 | 1.414213562 | 1.05309 |
| 10 | 10.272810580 | 10.488088482 | 0.97947 |

(Full 80-dps values in raw_output.json S4.) Shared deep limit (both → √y_B), finite disagreement up to ~7.7 %: an identical deep limit is not an identical finite law — the reason no Q/MU2 identification is made anywhere in this result.

**Exact vs finite consistency distinguished:** the identities κ_h² = 2/(3π), κ_Z/κ_h = √(3π/8), the reciprocal-square identity and 1/κ_h ∉ ℚ are exact (sympy and Lean); every deep/Newtonian "limit" statement above is a finite-Y consistency check with its leading term and domain stated.

---

## 5. Negative controls (capable of failing) and strongest surviving statement (seed step 5)

**NC1 — "the exclusion is universal while allowing λ in p_λ" (seed-mandated control): FAILS as a universal claim.** Take the two-channel OR family with p_λ'(0) = λ free (n = 2 fixed). The excluded value is reproduced exactly: λ* = √(3π/8) = 1.0854018818374014890…, because 1/(2λ*) = κ_h identically (residual 0.00e+00 at 80 dps; μ'(0; λ*) = 2λ* = √(3π/2) = 1/κ_h; Lean K). Diagnostics at λ ∈ {1/2, 1, 2} bracket the match: κ = 1, 1/2, 1/4. **The exclusion is conditional on the unit-slope premise (λ = 1); it is not universal in λ.**

**NC1b — unit-slope shape family p_λ = Y/(1+λY): the exclusion survives.** λ ∈ {1/2, 1, 2} all give μ'(0) = 2 exactly (sympy), κ = 1/2 for every shape; κ_h is unreachable inside the unit-slope OR class. The control is capable of failing (any λ* would be exhibited — none exists by the identity μ'(0) = n).

**NC2 — channel integrality: the exclusion is conditional there too.** κ_h = 1/n requires n = 2.1708 ∉ ℕ (distances to 1/n, n ≤ 20, in raw_output S2). The conditional statement is certified by Lean G/H (1/κ_h not rational, not natural). Relaxing integrality admits κ_h at n = √(3π/2).

**NC3 — limiting-regime control:** deep and Newtonian regimes both exist for MU_n and are checked with leading neglected terms (§3); boundary and normalisation checked (§3); the a0-line at finite y is NOT exact (q ≡ g²/(a0 g_N) = 1.41452201092 at g_N/s = 0.1): exact-identity vs finite-consistency distinguished.

**Strongest surviving statement:**

> **Theorem (conditional, on the declared CORE cell with κ = 1/2 adopted and the OR-channel reading of MU_n):** Let μ(Y) = 1 − (1 − p(Y))^n, n ∈ ℕ, p(0) = 0, p'(0) = 1, p(∞) = 1 (unit-slope OR composition). Then the deep-MOND coefficient of the spherical matching is exactly κ = 1/n; with n = 2 (the metric's two static Poisson channels, PD01 part 2) κ = 1/2 exactly. The horizon coefficient κ_h = √(8π/3)/(2π) = √(2/(3π)) = 0.4606588659… satisfies **none** of these: 1/κ_h = √(3π/2) ∉ ℚ (Lean), κ_Z/κ_h = √(3π/8) (Lean), κ_h ≠ 1/2 (Lean). The exclusion is exactly the conjunction (unit slope ∧ integrality): dropping either premise admits a matching parameter (NC1, NC2). **First additional implication to transfer to the full theory:** the unit-slope fraction identity p'(0) = 1 must be derived from the varied action (the one-scale structure supporting it is k01's zero-mode/outcome-3 theorem for the kernel class and PD08 step 3; it is currently a stated L230 principle, not a proved action consequence), and the two-channel count must be extended from the linearised static sector to the full action (PD01 part 2's scope). No other branch (RAR, EXP, MONO, Q) was imported to obtain this statement.

---

## 6. Dimensional footings (both, separately)

Framework: ρ_Λ = 4a0²/(Gc²). c√(Gρ_Λ) = 2a0 at κ = 1/2.

| quantity | canonical footing | alternative footing |
|---|---|---|
| a0 (κ = 1/2) | 9.3619e−11 m/s² | 1.1279e−10 m/s² |
| ρ_Λ | 5.8444124540e−27 kg/m³ | 8.4830896196e−27 kg/m³ |
| c√(Gρ_Λ) | 1.87238e−10 m/s² | 2.25580e−10 m/s² |
| **a0 at κ_h (same density)** | **8.6252844745e−11 m/s²** | **1.0391542698e−10 m/s²** |
| effective κ of alt footing at fixed canonical density | — | 0.6023884041 (= a0_alt/(c√(Gρ_can))) |
| a0_alt/a0_can (fixed κ) | 1.2047768081 | — |
| ρ_alt/ρ_can (fixed κ) | 1.4514871574 = (a0_alt/a0_can)² | — |

(Fixed densities with changed κ and fixed κ with changed densities are kept separate; the two footings never share both fixed ρ_Λ and fixed κ.) Derived radii (M_b = 1e11 M_sun): r_M = 12.2019668076 kpc (κ_Z, can), 11.1167167432 kpc (κ_Z, alt), 12.7123290093 kpc (κ_h at canonical density); v_flat = (GM a0)^{1/4} = 187.7466476786, 196.6975003381, 183.9393081413 km/s respectively (full 1e9 and 1e11 tables in raw_output.json S6; these are framework kinematics, not measurements).

---

## 7. G_N/G_bare/G_cosmo separation and the H0-degeneracy note

The horizon identification assumes the same G in H² = 8πGρ/3 and in a0 = κ c√(Gρ). Keeping them separate: κ_h(G_N, G_cosmo) = √(8π G_cosmo/(3 G_N))/(2π); the ratio becomes κ_Z/κ_h = √(3π G_N/(8 G_cosmo)), which equals 1 exactly when **G_cosmo/G_N = 3π/8 = 1.17810** — i.e. an exact same-G assumption is baked into the 8.54 % gap; a measured G-ratio of 1.18 would close the coefficient gap without any channel argument. This is recorded as an open dependency (no framework-level G_cosmo/G_N measurement is brought in here), and it parallels k03's P2 (the coefficient question is degenerate with the H0 tension at fixed Ω_Λ: κ = 1/2 at Planck H0 = 67.4 and κ_h at SH0ES H0 = 73.0 predict the same a0 to <1 % — reproduced as k03's own output, which the run dir re-execution confirmed unchanged).

---

## 8. Pinned-source evidence (re-executed this run, outputs in run dir)

- `k01_zero_mode_theorem_and_lambda_free_vacuum.py` — exit 0; K1, K2 PASS (statics invariance J → J+C; Λ_eff = Λ + (2−K_B)J(0)/2 + K(Q0)/2 with Λ free ⇒ outcome 3); K3–K5 FAIL as recorded (negative Lambda-free vacuum; size factor; QUMOND reading at η = 0.984/3.5); K6 PASS guard. Historical constants G = 6.674e−11, c = 2.998e8 (its own header) — difference vs framework numerics quantified: <0.06 % in G, <0.07 % in c; no conclusion here depends on them.
- `PD01_polarization_count.py` — exit 0; **17/17 PASS**; the two static Poisson channels of the linearised metric; κ = 1/n with n = 2; the 2π-horizon form dies structurally (n = √(3π/2) ∉ ℕ) — the statement this run certifies.
- `PD08_particle_free_derivation.py` — exit 0; **7/7 PASS**; steps 1–5 of the particle-free derivation; p'(0) = 1 stated via the one-scale fraction identity (L230), flagged here as the load-bearing unproved premise (limitations).
- k03 (source of κ_h, `kappa_closure/k03_half_vs_two_pi_precision.py`) read as evidence: κ_2π = √(8π/3)/(2π) = 0.4607; data separation impossible at the 8.5 % level (BTFR mass-budget floor 9.47 %, DR4 21 %, |ln LR| < 1 σ undecided); H0-degeneracy. Not re-executed (not pinned by this seed; its numbers are reproduced by quoting + my independent computation of the same 8.54 %/0.036-dex gap).

## 9. Execution bounds and reproducibility

Declared: ≤120 s wall, ≤512 MB, 1 thread. Enforced: `signal.alarm(120)` (compute 0.316 s); single-threaded single process; memory: RLIMIT_AS rejection recorded (macOS host; observed peak RSS 64 MB). All outputs in `raw_output.json` + `raw_output.stderr`; hashes in result.json. The Lean certificate compiles clean (`lake env lean`, exit 0, empty log) and the axioms file prints the unfiltered axiom set for all 12 theorems: exactly `[propext, Classical.choice, Quot.sound]`, zero `sorry` (verified by grep and by `#print axioms`).

**Lean certificates (run-dir `AS066_horizon_coefficient.lean`, 12 theorems):**
`kappa_h_sq` (κ_h² = 2/(3π)), `kappa_h_pos`, `kappa_h_ne_zero`, `inv_kappa_h_sq` ((1/κ_h)² = 3π/2), `kappa_ratio_sq` ((κ_Z/κ_h)² = 3π/8), `kappa_ratio` (κ_Z/κ_h = √(3π/8)), `kappa_h_ne_half` (κ_h ≠ 1/2), `inv_kappa_h_not_rational` (¬∃q:ℚ, q = 1/κ_h), `inv_kappa_h_not_nat` (¬∃n:ℕ, n = 1/κ_h), `or2_expansion` (1−(1−λY)² = 2λY − λ²Y²), `or2_deep_ratio` (μ(Y)/Y = 2λ − λ²Y for Y ≠ 0), `matching_lambda_coefficient` (κ_h = 1/(2·(1/(2κ_h)))). House traps handled: `field_simp` never trailed, `mul_left_cancel₀` avoided, sqrt identities via `Real.sq_sqrt` + positivity, `eq_div_iff` with explicit nonzero, `irrational_pi` (this build's name).

## 10. Closure implication and child proposal

- **Gate/implication (CORE coefficient cell, group A03):** the coefficient κ = 1/2 is an INPUT of the amended thirteen-item target (a0–vacuum relation retained as input). This result pins the exact numerical relationship to the only surviving principle-shaped alternative (κ_h, the 2π-horizon form): ratio √(3π/8) = 1.0854, exclusion conditional on (unit slope ∧ channel integrality), both failure modes exhibited, data-side separation impossible at 8.5 % (k03). Branch compatibility: the result lives on the declared CORE/MU_n cell; filtered MONO + criterion B (operative gate) is untouched; no Q/RAR/EXP/MONO identification was made.
- **Child AS066.C01 (ready spec, NOT dispatched — no spawn mechanism on this worker):** *"Deep coefficient of the operative MONO cell through the heat filter"* — derive the actual deep slope μ'(0) at the operative weak-field cell (∇²u = 4πGρ_b; ∇²Φ = 4πGρ_b + S*∇·[(ν_mono−1)∇Su], S = exp((ξ²/2)Δ), FRIED_CHICKEN_SPEC requirement 1) in units of s = c√(Gρ_Λ): is the coefficient still exactly 1/2 (κ = 1/2), or does the filter shift it by a computable O(ξ²-scale) term? Controls: ξ → 0 limit returns κ = 1/2 exactly; Newtonian cell unchanged; filter-width sweep must move the shift (capable of failing); forward-law residual grid. Duplicate check: AS/MY manifests + FGF queue scanned — A03 neighbours (AS051 general deep-slope matching, AS052 unequal channel slopes, AS053 slope freedom in a one-scale action, AS060 PD08 quadratic OR expansion, AS063 identifiability of n and per-channel slope, AS074 robustness under kernel deformations) do not exercise the heat filter on the coefficient; no registered task matches this fingerprint (action cell, MONO+filter, deep coefficient, κ-shift).

## 11. Limitations

- κ = 1/2 remains adopted; the one-scale "fraction identity" p'(0) = 1 remains a stated principle (L230/PD08 step 3, k01 outcome-3 support), not a proved consequence of the varied action — the exclusion of κ_h is conditional on it (NC1).
- The two-channel count is a linearised-static-sector computation (PD01 part 2); its full-action extension is open.
- The horizon normalisation a0 = cH/(2π) is itself adopted (Unruh/GH identification), and the same-G assumption hides a G_cosmo/G_N = 3π/8 exact-degeneracy (§7); no measurement is invoked in this structure-only result (data-side separation is a k03 result, quoted with its scope).
- The a0-line g² = a0 g_N is a deep limit, not an exact finite law of MU2 (NC3); limiting-regime checks are finite consistency with stated leading terms, not exact identities (the exact identities are the sympy/Lean ones).
- No dynamics, stability, lensing, PPN, or filter content; no operative-branch (MONO/criterion B) conclusion; no empirical claim. This is a coefficient-cell comparison; a completed task is not closure of gravity.

*All numerical values quoted appear in `raw_output.json` (sections S0–S7) with 80-dps precision; hashes of every artifact in `result.json`.*