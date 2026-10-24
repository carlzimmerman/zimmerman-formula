# X18_beta_growth_forest: does nonlinear saturation rescue C1's small-scale growth, or does the forest close C1's window? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md`) before any lane script exists and before any number is computed by
code. Rules: `rebuild_2026_10_22/BRIEF.md`. κ = ½ is FITTED. Footings canonical a₀ = 9.3603e-11 m/s² and alt
a₀ = 1.1312e-10 m/s², never pooled. No dark-matter particle. No new fitted knob: β is used only inside X14's window
(set by caustics and H₀, not by data). Never "theory closed"; nothing here says the data favour the framework. Small jobs
only: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes; `compute_queue/` and every other lane
untouched (X17's script is run only as a patched copy in a temporary directory, outputs there); no downloads.

**C1 cannot be tuned to ΛCDM-like growth.** β is not a growth knob. If some β passes the forest, that is reported as a
surviving window inside X14's caustic/H₀ window, never as a fit, and never as "β measured".

**The question.** X17 found that C1 (the khronon K² term, B = β/(2+3β); window β ∈ [β_min = 2.0e-6 canonical /
2.2e-6 alt, β_max = 1.0e-5] at μ_K = 0.1 Mpc⁻¹, up to 1.12e-4 at μ_K = 0.03) has c_A = 0 on FRW. It also multiplies the
khronon's response to baryon wells by F = 1 + Bk_p²/(Kρ̄_τ). In X4's linear ODE every window cell overshoots the dust
reference at k ≳ 1–3 h/Mpc. X17 did not compute nonlinear saturation: the perturbations' own law-field gradient
x = |∇Ξ|/a₀ > 0 switches on c_A² = Bc²(M_θ − 1). Does that saturation stop the overshoot? Does the record's Lyman-α
forest gate then close C1's window, or does some β in the window pass?

## 0. What was read, and the not-blind statement

Read before freezing: `covariant_push_2026_10_22/V3_FULL_PICTURE.md` §4.2 and §6 (caustics row, X14–X17 bullets);
X17 README (all) and `x17_beta_sound_selector.py` (header, constants, S0-1/S0-2/S0-3/S0-5, Part G: `khr_drive`,
`growth_C1`, G-DISP, the growth table); X17 JSON growth cells; X4 FROZEN_CRITERIA §F, ASSUMPTION_LEDGER A14/A15,
README F rows; `x4_dbi_door.py` F0a/F0b blocks (L473–519) and its gate function (L525–555); X4 JSON F0a/F0b; the
rebuild BRIEF rule lines; the record's standing a₀(z) statement (a₀(z) = κc√(Gρ_DE(z)); constant when w = −1).

**Not blind.** Before freezing I reasoned on paper (no script, no code-computed number):
- **The saturated kernel is the record's own kernel.** X14's khronon dispersion with general M_θ is
  ω² = −(Kρ̄_τ + Bk²)·s_M, s_M = (Mμ² − (M − 1)k²)/(k² + Mμ²). This is the record's M1 kernel s(k; f₀) at
  f₀ = 1 − 1/M (§4.2). At M = 1 it is X4's J_x kernel μ²/(k² + μ²). The mode is pressure-supported (s_M < 0) once
  (M − 1)k² > Mμ², i.e. for M = 1 + x once x > μ²/(k² − μ²), which is X17's "x > s(k)".
- **Onset is expected early at forest scales.** Paper estimate: the per-ln-k khronon acceleration at k = 1 h/Mpc,
  z = 3 is y ~ 1e-3 × Δ_τ × (1+z)² ~ 1e-3. The threshold there is (aμ_K/k)² ~ 3e-4. So onset is expected before
  z = 3 on forest scales.
- **Saturation is not expected to Jeans-suppress the total.** With baryons, the coupled FRW mode keeps
  D = −Kρ_b(Kρ_τ + Bk²)(1 − s_M) < 0 for every M ≥ 1, so a growing root always exists. As k → ∞ the root tends to
  λ₊ → Kρ_b·M/(M − 1): a stiff khronon settles into the static sub-phantom charge δρ_b/(M − 1) (H-RESP's k → 0 limit),
  which is MOND-like boosted baryon growth. For x ≪ Ω_b/Ω_m this is faster than dust growth. The changeover from C1's
  √(Kρ_b Bk²) rate needs x²Bk² ≳ Kρ_b, which I expect only at x ≳ 0.1. **Expected verdict: C1 WINDOW CLOSED BY THE
  FOREST, through overshoot on L346's band.** The thresholds below are the record's own forest lines and X4's
  pre-declared [0.5, 2] margin. None is tuned to these expectations.

## 1. The saturation model (derived from the action; nothing posited)

- **Kernel (check Q-KER, sympy).** X14's `disp` (as copied in X17), with the C1 transport term Bk²/K, at general M_θ
  (Θ = 0) gives ω² + (Kρ̄_τ + Bk²)s_M ≡ 0 with s_M as in §0. M_θ: transverse (k ⊥ ∇Ξ) M_T = 1 + x; longitudinal
  (k ∥ ∇Ξ) M_L = (1 + x)². These are the record's M_θ ∈ [1 + x, (1 + x)²] (X14/X15/X17); both are graded as a bracket.
- **Coupled system (check Q-DISP, sympy).** X17's G-DISP determinant (khronon + dynamical baryon fluid), redone at
  M_L = M_T = M, equals (λ² − Tλ + D)·(k² + Mμ²)·(λ-free factor) with T = Kρ_b + (Kρ_τ + Bk²)s_M and
  D = −Kρ_b(Kρ_τ + Bk²)(1 − s_M). So the saturated growth ODE is X17's `growth_C1` with s → s_M. Nothing else changes:
  baryons feel the Newtonian φ of the total charge; F = 1 + Bk_p²/(Kρ̄_τ) is unchanged.
- **Asymptote (check Q-ASY, sympy).** lim_{k→∞} λ₊ = Kρ_b·M/(M − 1). So the saturated system has no Jeans cut-off in
  the total. The khronon's own Jeans wavenumber (pressure beats the hold) is k_J,p = μ_K√(M/(M − 1)).
- **The perturbation's own acceleration (from the khronon's Gauss law).** The linear khronon charge δρ_τ at
  wavenumber k has a law-field gradient whose Newtonian-from-charge part, per ln k, is
  y_k(a) = Kρ̄_τ(a)·Δ_τ(k, a)·k_p/(k_p² + μ_K²)/a₀, with K = 4πG, ρ̄_τ = Ω_τρ_crit a⁻³ (Ω_τ = Ω_m − Ω_b, X4/X17)
  and k_p = k/a. The nonlinear Gauss law ∇·[∇Ξ/(1 + |∇Ξ|/a₀)] = Kρ_τ is inverted with X14's cap identity
  (𝒰(y) = a₀y/(a₀ − |y|)): **x = y/(1 − y)**. If y ≥ 1, the record's hold-flux cap is reached. The quasi-linear model is
  then invalid for that mode (flag CAP).
- **Normalisation.** Δ_τ(k, a) = Δ_A(k)·δ_τ^ODE(k, a)/D_dust^ODE(a = 1). Δ_A(k) = √(k³P_A(k)/2π²) is the z = 0 linear
  dust spectrum of background A (CLASS, C2b refit parameters, exactly as X17's `PkA`). D_dust^ODE is X17's dust run.
- **Which x a mode sees (two brackets, both graded).**
  - **S (self):** each mode's M comes from its own y_k.
  - **E (environment, WKB):** each mode's M comes from the cumulative rms over all scales at least as large,
    y_E(k)² = ∫_{k' ≤ k} y_k'² d ln k' (trapezoid on the lane grid). This is the external field that larger scales
    impose, plus the mode itself.
  - Both are solved self-consistently inside the ODE: M is recomputed from the current δ_τ at every right-hand-side
    call.
- **a₀(z).** The record's standing statement is a₀(z) = κc√(Gρ_DE(z)). The ODE background (X4/X17) has constant Λ, so
  a₀ is constant, used as written per footing.
- **Onset.** For each graded k, a_on(k) is the first a at which s_M ≤ 0, i.e. the c_A pressure beats the hold. Also
  reported: the first a at which x ≥ s(k) = μ²/(k_p² + μ²) (X17's stated proxy), and k_J at z = 3, 2 and 0.
- **Check Q-LIM.** The saturated ODE with x forced to 0 equals X17's `growth_C1` (max relative difference ≤ 1e-10 on
  every graded output).

## 2. Step 0 (stop rule: any failure ⇒ verdict UNDECIDED, nothing further scored)

| id | reproduction | pass line |
|---|---|---|
| S0-1 | X17's own script (sha256 frozen at its committed state) run as a patched copy in a temporary directory (only HERE and ROOT rebound) | exit 0; 13/13 PASS; verdict "WRONG SIGN"; 0 differing JSON leaves vs the committed JSON, apart from timing/RSS fields and timing substrings ("… s)") |
| S0-2 | this lane's verbatim copy of X17's `make_E`, `khr_drive`, `growth_C1`, background A and `sig8_from_T` reproduces X17's growth cells: R_β, R_0 and T² (z = 0, z = 3) at k = 0.1/0.3/1/3/10 h/Mpc, both footings, both μ_K, β_min and β_max, a_i = 1e-3 | max relative difference ≤ 1e-6 |
| S0-3 | X4's β = 0 row: F3/X4's ODE copy (`growth_ratio_x4`) σ₈ ratio at μ_K 0.1 / 0.03 (a_i 1e-3, 1e-4) vs X4 JSON `ode`; X17's `T2_beta0` cells | ≤ 1e-4 (X4); ≤ 1e-6 (X17) |
| S0-4 | forest gate numbers: L346's six bins and the sw5_canon / sw5_alt / never_on bands from `real_research/g03_audit_2026/L346_switch_forest_gate_results.json` equal X4's `F0a` and L346's stored F2; L319's T²_5.3keV(k5) by L319's formula (`real_research/dark_sector_2026/L319_lambda_triggered_kicked_decay.py` L169–171, L184–185; h 0.6736) equals X4's `F0b` 0.99519 | ≤ 1e-9; band verdict FAIL as L346; never_on exactly 1; \|T²_5.3keV − 0.995\| ≤ 5e-4 |

## 3. Required checks (all must pass in the main run)

S0-1 … S0-4; Q-KER; Q-DISP; Q-ASY; Q-LIM; **Q-CONV**. Q-CONV: the gate classes F and the σ₈ class are unchanged
between a_i = 1e-3 and 1e-4 and between rtol 1e-7 and 1e-9, in every graded cell. It is evaluated on the (β_min, β_max)
cells of each μ_K and footing, both models, both orientations. If Q-CONV fails, the verdict is UNDECIDED.

## 4. The graded cells

- Footings: canonical and alt, separately.
- μ_K = 0.1 Mpc⁻¹: β ∈ geomspace(β_min(foot), β_max(0.1), 5).
- μ_K = 0.03 Mpc⁻¹: β ∈ geomspace(β_min(foot), β_max(0.03), 7).
- β = 0 at each μ_K is computed as the v3s reference (reported, not graded).
- Brackets: x-model {S, E} × orientation {⊥ (M = 1 + x), ∥ (M = (1 + x)²)}.
- ODE: X17's `growth_C1` with s → s_M; a_i = 1e-3 primary, DOP853, rtol 1e-7.
- k grid: X17's KT (36 points, 1e-3–3 h/Mpc) ∪ {0.1, 0.3, 1, 3, 10} ∪ L346's six bins ∪ {k5} ∪ geomspace(3, 50, 20)
  h/Mpc.
- Outputs at z = 3, 2 and 0.

## 5. The forest gate (the record's lines; X4's F rule verbatim)

- **Reference.** As X4/X17: T²(k, z) = (δ_m/δ_m,dust)² in the same ODE, with δ_m = (Ω_bδ_b + Ω_τδ_τ)/Ω_m. The dust run
  is ΛCDM-like growth (X4 F0c: DUST = ΛCDM).
- **F_L346** (L346 F2; X4 ledger A14): T² at L346's six bins (1.10–3.56 h/Mpc), at z = 3 **and** z = 2, in
  **[0.8, 1.2]**.
- **F_L319** (L319; X4 ledger A15): T²(k5 = 4.6199 h/Mpc) ≥ T²_5.3keV = 0.99519 (strict), ≥ 0.9 (loose), at z = 3 and
  z = 2.
- **F = FAIL** if F_L319 loose fails at z = 3 or z = 2, **or** the worst L346 bin at z = 3 or z = 2 lies outside
  [0.5, 2.0]. This is X4's pre-declared margin, so that no linear-only failure is one that nonlinear refill could
  plausibly erase.
- **F = PASS** if F_L346 passes and F_L319 strict passes.
- **F = UNDECIDED** otherwise.
- **CAP flag.** If y ≥ 1 for any mode with k ≤ 5.1 h/Mpc at any a ≤ 1/3, the cell is CAP and its F is UNDECIDED (the
  quasi-linear model is invalid there). A cell whose worst bin has Δ_m > 1 at z = 3 is also labelled FORMAL
  (reported; F unchanged).
- All gate lines are LITERATURE-INPUT, ΛCDM-PROCESSED (forest bounds come from ΛCDM-calibrated hydro). Both are
  applied to linear (here quasi-linear) 3D P(k), not to the flux power, exactly as X4 did.
- **Reported only:** the 1D ratio P1D/P1D,dust at k_∥ = the L346 bins, with P1D(k) = (1/2π)∫_k^{50} P(q) q dq on the
  lane grid.

## 6. Verdict classes (per footing; footings never pooled)

For one footing, a graded β (on its μ_K grid) is:
- **robust FAIL** if F = FAIL in all four brackets;
- **robust PASS** if F = PASS in all four brackets;
- **mixed** otherwise.

Verdicts:
- **C1 WINDOW CLOSED BY THE FOREST**: every graded β, on both μ_K grids, is robust FAIL on this footing.
- **WINDOW NARROWED TO [β range] (μ_K …)**: at least one β is robust FAIL, none is robust PASS. The surviving range is
  the contiguous set of non-robust-FAIL grid β, stated per μ_K. A surviving range is a window, not a fit.
- **SATURATION RESCUES (forest passes for β in …)**: at least one β is robust PASS. The robust-PASS range is reported per
  μ_K as a window, never a fit, together with its σ₈.
- **UNDECIDED**: step 0 fails, a required check fails, or no β is robust FAIL or robust PASS.

The overall line states both footings. If they differ, both are stated and neither is pooled.

**Reported only (no verdict weight).**
- σ₈/σ₈,dust at z = 0 after saturation (X17's `sig8_from_T` convention), per cell.
- Whether it lies in [0.95, 1.05]. This lane's convention; the record's own growth line is R ≥ 0.95 (X4).
- Whether any β has both σ₈ and the forest within lines. That would be stated as a window.
- a_on(k), k_J(z), y and x at z = 3, 2, 0.
- The coupled growth rate √λ₊/H at k = 1, 3, 10 h/Mpc, saturated against x = 0.
- The β = 0 (v3s) reference with saturation.
- What a Boltzmann / N-body run would need. C1 is not in Q6's CLASS patch.

## 7. MUTATE twin (`X18_MUTATE=1`, separate outputs `_MUTATE`)

MUTATE runs step 0, the symbolic checks, Q-LIM and one reduced cell (canonical, μ_K 0.1, β_min; S⊥ only; Q-CONV on
that cell). The required failures are exactly these:

| mutation | change | must fail |
|---|---|---|
| m1 | X17 copy run with `X17_MUTATE=1` | S0-1 |
| m2 | the S0-2 copy of `khr_drive` returns 1/F | S0-2 |
| m3 | the S0-3 copy uses kernel s = 1 | S0-3 |
| m4 | L319 line evaluated at 3.0 keV | S0-4 |
| m5 | s_M's (M − 1)k² term with the wrong sign | Q-KER |
| m6 | the target D uses (1 + s_M) | Q-DISP |
| m7 | the asymptote target Kρ_b·M (no 1/(M − 1)) | Q-ASY |
| m8 | Q-LIM's x = 0 run uses 2B | Q-LIM |

Q-CONV is not mutated. The MUTATE verdict line is the control's output, not physics.

## 8. What this lane cannot show

- The saturation is quasi-linear: WKB modes on a background x from the perturbations themselves, self-consistent in
  the ODE. It is not an N-body or Boltzmann solution, and not L1's question in full. Mode coupling beyond the
  M-feedback, shell crossing and baryon pressure are absent, and the forest is graded on (quasi-)linear 3D power.
- The literal K(Q) background (radiation-like khronon to z ≈ 35–78) is not modelled, as in X4/X17's ODE.
- Orientation averaging is bracketed (⊥, ∥), not computed.
