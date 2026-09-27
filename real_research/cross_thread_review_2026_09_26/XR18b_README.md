# XR18b — is FP19's repaired separator H_K1 well posed, stable and causal? (before a particle-mesh run)

Review lane of `cross_thread_review_2026_09_26`, 2026-09-27. An adversarial re-audit of FP19's H_K1 (commit 0c18c582f), the
separator that replaced FP13's ill-posed H_S (XR18, 53854a459). H_K1 reads the state only through the leaf average ⟨K⟩_h:

* χ = (S_ξ − S_B)φ, B = L²/2, L = L_Λ · 3Λ/⟨K⟩_h² (L_Λ = 2.9 Mpc, n = 2);
* J_Y = J_P2 + 2 y_th √Y, y_th = max(0, 1 + Ω_r − 9Λ/⟨K⟩_h²)·(⟨K⟩_h²/3 − Λ)·L/α (c_y = 2, chosen after scoring; the q = 0 ramp).

Four scripts, each with a pre-declared hypothesis block, controls that reproduce committed numbers exactly, and a MUTATE run
that must fail. Both a₀ footings throughout (canonical 9.3603e-11, alt 1.1312e-10 m/s²). κ = ½ is FITTED (Z = 5.7888);
nothing here derives it, and nothing here closes the theory. Causality is judged by the record's criterion B, as XR18 used it.

## Bottom line

**H_K1 is linearly well posed and causal at FP19's cell. Its ⟨K⟩_h channel is real but (v/c)²-small. FRW growth across the
q = 0 kink is well posed. A particle-mesh (PM) run can proceed, with conditions (listed below).** The obstruction that stopped
H_S is gone: no Newtonian-order state read, no R_B term, and no sign change of the ψ-symbol at any k.

What does not go away, and now reaches further:

* **Cold matter at yield surfaces.** Its linear growth rate depends on resolution, Γ ∝ d_min^(−1/4), and is capped only at ξ.
  This is XR18's H_Y liability, unchanged: 190–374 H at ξ.
* **Cold matter at the zeros of the band-passed field.** Below z_q0 = 0.635, H_K1 has no yield, so every zero of the
  band-passed field (halo centres, saddles of the web) is unplugged. The same d^(−1/4) growth appears there. H_Y plugged
  those points.
* **λ.** It must be *declared* ≤ ~0.03 for the MOND-regime observables not to depend on it. Left free, it is a knob.

## 1. The linear symbols (`XR18b_symbol_channel.py`, 12/12 main, rc = 0)

* **FP19's "+0.995" is 1 − eps_K by construction.** R_B = κ = 0 because the read is ⟨K⟩_h, and eps_K = 4.96e-3 is subtracted.
  FP19's own code reproduces it exactly (K2).
* **The real ⟨K⟩_h read is not "k = 0 only".** For a plane wave the first variation of ⟨K⟩_h vanishes, but the second does
  not. The action depends on ⟨K⟩_h through the whole leaf, so (dS/d⟨K⟩_h)·δ²⟨K⟩_h is a **local operator at every k** with a
  leaf-averaged coefficient C. The exact second-order ADM expansion (sympy, unitary gauge about FRW, verified) gives
  C a³[3H A² − 9H Aζ − 3A ζ̇ + 9ζζ̇ + a⁻²A∇²β].
  * FP19 H4's lattice read makes B a *linear* function of the leaf mean of ψ, so δ²B = 0 by construction. The real ⟨K⟩_h does
    not behave that way.
  * FP19's ledger entry R19e ("a mean-field term at k = 0 only") should read: *a local term at every k, with a
    (v/c)²-small coefficient.*
* **The constrained block is untouched (S2).** Take the lapse, shift and Brown–Kuchar dust multiplier, plus the CMC multiplier
  at c₂ = ∞. The block determinant with the channel equals the one without it **identically**. This holds at finite c₂ and at
  c₂ = ∞, and for both leaf weightings (√h and N√h).
  * The channel's entries are ε_C times GR's entries of the same structure. The factors are −2ε_C (A²), −ε_C (A∇²β) and
    −ε_C (Aζ̇).
  * The Aζ entry is −9ε_C(aH/k)² times GR's A∇²ζ entry.
  * Here ε_C = ρ_extra/(2ρ_crit).
* **Size on the real state (S3).** ρ_extra = 3HC = −∂e_M/∂ln⟨K⟩_h, from two channels:
  * through B: the chassis's MOND-binding rate I(L) (FP19 A2's envelope identity);
  * through y_th: a₀²⟨x⟩/(4πG).

  |ρ_extra|/ρ̄ ≤ 2.6e-5 and |ε_C| ≤ 9.1e-6 at every z = 0–2.5, on both footings, in every reading of the web:
  * per-mode, rms and halo I(L);
  * Gaussian ⟨x⟩, and the reading-free Jensen bound ⟨x⟩ ≤ y_rms^½.
* **The ψ-symbol (S1).** Take FP19's symbol with eps_K *not* subtracted, and subtract the channel's bound
  2|ε_C| + 9|ε_C|(aH/k)²(1 + |dln C/dln a + 3|).
  * Sub-horizon k (10 aH/c to 1e3 h/Mpc): min S = **+0.999982**.
  * k = 1e-4 h/Mpc: the bound is 4.7e-3, and the exact statement there is S2.
  * **No sign change anywhere.**
* **eps_K (S4).** It does not measure any term, and subtracting it hides none.
  * eps_K is XR18 C1's proxy a₀²⟨x⟩³/(6πG), evaluated with the halo reading's ⟨x⟩ at z = 0.25.
  * That ⟨x⟩ is 0.294 at M_min = 1e8. It violates the Jensen bound, 0.091, by ×3.2, and grows ×2.3 per decade of M_min: the
    dilute-halo sum adds overlapping deep-MOND fields as scalars.
  * The quantity the variation actually needs, I_halo, converges (1e7 vs 1e8: 1.0002).
  * The derived channel is 5e-3 of eps_K. FP19's subtraction was conservative, and structurally misplaced: a homogeneous
    density does not enter the Newtonian symbol.
* **The φ-symbol (S5).** Write FP7's committed block as a quadratic in U = ω²/k².
  * Its discriminant is (A − B)² + S² + 2S(A + B) ≥ 0, with A = C_φα_c(3c₂ + 2), B = λc₂(2 − α_c), S = σ²(2 − α_c)(3c₂ + 2).
  * So for every C_φ ≥ 0 all roots are real and ≥ 0, at finite c₂ and at c₂ = ∞.
  * C_φ = 0 at zero field below z_q0 is a degenerate symbol, not a negative one.

## 2. Nonlocality through ⟨K⟩_h (same script)

* **Conservation (B1).**
  * Vary the full action through ⟨K⟩_h. The reparametrisation Noether identity N dE_N/dt − ȧE_a = 0 then holds
    identically. It was checked with four explicit test functions, one of them H_K1's ramp × (⟨K⟩²/3 − Λ) × L(⟨K⟩), smoothed.
  * Freeze the read instead (L and y_th prescribed in time, as scoring or a PM does). The identity then fails, and the
    Friedmann constraint drifts at |3Ḣ C|/(3Hρ̄) ≤ 9.1e-6.
  * A read of the scale factor, L(a) and y_th(a), satisfies the identity identically. This is XR21's PM form, and it is a
    leaf-volume read.
* **Translation invariance (B2).** On periodic 16³ and 32³ leaves, the channel's leaf-uniform coefficient exerts no net force
  on a random density field (≤ 2.6e-17). A position-weighted coefficient does (5e-3).
* **Global terms.** Derived: ≤ 2.6e-5 of ρ̄. XR18 C1's formula on H_K1 gives 1.9e-5 (Gaussian). The same (v/c)² order as H_Y's
  1.6e-5.

## 3. The q = 0 kink and λ (`XR18b_ramp_lambda.py`, 12/12 main, rc = 0)

* **The ramp is a kink, not a jump (R1).** y_th is continuous at z_q0 and vanishes exactly there (offset 1.6e-10). This differs
  from FP13's table, whose zero sat 0.010 lower. Its one-sided ⟨K⟩-derivative is 2(1 + Ω_r)(⟨K⟩²/3 − Λ)L/α = 1.25e-2
  (canonical).
* **FRW growth across z_q0 is well posed (R2).**
  * With the ramp smoothed, σ₈ converges monotonically: |dσ₈| = 4.2e-4 / 1.8e-5 / 1.0e-6 at eps = 0.05 / 0.01 / 0.002.
  * Every σ₈ mode crosses the yield at most once.
  * Within 0.02 of z_q0 the chord's largest step shrinks ×9.95 under 10× refinement.
* **The background (R3).** The Friedmann function F(H) jumps *up* by ΔF/ρ̄ ≤ 1.4e-5 at H(z_q0). So H(ρ) stays continuous: a
  Filippov sliding segment pins H for H·Δt ≤ 4.6e-6. Well posed.
* **λ at the switch-off (R4).**
  * At c₂ = ∞, zero field and a closed band-pass, every coefficient of the root polynomial is ∝ λ, so φ has no equation at
    λ = 0.
  * With structure, φ un-freezes at ≥ 59 H for every sub-L σ₈ mode, for λ ∈ [0, 274.4].
* **Gates (R5).** At c₂ = ∞, σ₈ spreads by 3.6e-7 for λ ≤ 0.03 and by 1.7e-4 up to 274.4, and the forest stays at 0. FP19
  scored at the c₂ floor, where XR25 L2 finds no λ window at all. At c₂ = ∞ its σ₈ moves by ≤ 4e-6.
* **The MOND regime fixes the window (R6).** Relative to λ → 0, the tracking speed at C^Q = 100 and the galaxy α₂v² (620 km/s)
  drift by 1% at λ = 0.061 and 0.030 respectively. Across (0, 274.4] they change ×9.6 and ×93.
* **Strong coupling in real backgrounds (R7).** It is not absent, but it is sub-ξ.
  * Every zero of the band-passed field below z_q0 carries a strongly coupled core: 46–900 m in the metric-visible sector,
    ≤ 7.2 km in the sub-ξ sector. This was checked for web zeros and for cored centres at 10²–10⁶ ρ̄.
  * H_K1's yield layers above z_q0 carry 0.2–5 km layers.
  * All of these are far below ξ = 7.5e14 m, for every λ ∈ [1e-9, 0.03].
  * The metric-visible length at the ξ scale is ≤ 0.17 m.
  * λ barely controls any of this (ℓ ∝ λ_eff^(−1/8)). The flattest zero's sub-ξ core reaches ξ only at λ ~ 1e-125.

**The λ answer, plainly.**
* λ must be ≤ ~0.03 (λ ≪ 3, the khronon's own inertia at c₂ = ∞) for the MOND-regime observables to be λ-independent.
* Within (0, 0.03] λ is a regulator: the limit λ → 0⁺ is smooth for everything computed here.
* No datum in the record selects a value inside (0, 274.4]. The only data bound is tracking, from above.
* So the chain must **declare** λ ≤ 0.03. Left free, λ is a knob, because the MOND regime reads it.
* FP19's F-table row ("regulator, any value ≲ 100") is wrong at c₂ = ∞ and should be corrected.

## 4. Cold matter (`XR18b_yield_surfaces.py`, 7/7 main, rc = 0)

* **At H_K1's yield surfaces (B4b).** 30 hosts at z = 0.7–4, with r_Y = 39–1289 kpc.
  * The isolated surface mode scales as d_min^(−p), with p = 0.249–0.250.
  * It saturates between ξ/3 and ξ/10 (within 0.2%).
  * Γ is 20–37 H at 1 kpc and **190–374 H at ξ/10**, against XR18's H_Y 204–451 H.
  * It is resolution-dependent below ξ. B4, XR18's whole-domain version, is reported only: p = 0.151–0.250, because it mixes in
    interior modes, as XR18 found.
* **At the unplugged zeros below z_q0 (Z1).** The test is the exact l = 0 sector about a Gaussian-cored centre (10²–10⁶ ρ̄,
  σ = 1 kpc).
  * p = 0.229–0.240, saturating at ξ (≤ 0.02%).
  * At ξ/10, Γ is 6.4–75 times the Newtonian rate.
  * At the web's zeros at mean density (the 1-D local form), Γ ≈ 6.6 H at a 50 kpc cell and 17.5 H at 1 kpc, rising to 249 H
    at ξ.
  * **This is new relative to H_Y.**

## 5. Criterion B and the DE12-type second variation

* **Criterion B (A1).** 0 violations in 3,438,864 root evaluations on H_K1's backgrounds:
  * z = 0.7–4 with yield (approach to d/r_Y = 1e-12, plug, zero field);
  * z = 0.25 without yield (the whole profile to 50 Mpc);
  * c₂ ∈ {7.29e-3, 0.1, ∞}, λ down to 1e-9, both α_c ends.

  S5 is the proof for any C_φ ≥ 0.
* **Exponents (A2).** At the surfaces, C_L ~ d^(0.5000–0.5001) and C_T ~ d^(−0.5000 to −0.4999). At a zero-field centre, both
  go as r^(0.5001–0.5002): a degenerate point.
* **No k⁰ term (`XR18b_second_variation.py` B1).** Run XR18's WKB engine on its own extracted text, with the channel's
  operator added. The only k⁰ term is the gas's c_s²/(2ρ); the channel is O(k⁻⁴).
* **B2 fails as run.** This was pre-declared, and expected from the exploratory run: DE12's convention on the *isolated* hosts
  gives Γ(1/kpc) up to **1.43e5 H at z = 0.25**, at r = 13.6 Mpc.
  * There the host's band-passed field is 1e-24–1e-22 a₀: the Gaussian band-pass has removed the monopole.
  * H_K1 has no yield below z_q0, so nothing plugs that region.
  * Embedded in the web's own band-passed field (B2w), the growth is **0** for 1e6 K gas on all 24 hosts.
  * At the web's zeros and at cored centres, 1e6 K gas does not grow at 1/kpc (B2z). For 1e5 K gas at the densest centre,
    MOND amplification gives 270 H where Newton gives 0: ordinary central-MOND physics that H_Y had plugged.
* **The gas radial sector (B3).** Around H_K1's yield surfaces it is bounded (≤ 16 H) and converged (0.0% grid change, 0.2%
  eps change), and the yield lifts it over plain P2 by at most ×1.48.
  * B3r (reported): at z = 0.25, embedded in the web, 1.1–31 H. The largest (30–31 H, the 1e12 hosts) is an inner,
    host-dominated mode, the same whether the host is isolated or embedded.
  * Isolated over the whole profile it reaches 4e4–1.3e5 H.

## 6. Verdict and the particle-mesh run

H_K1 at FP19's cell is **linearly well posed** (items 1–2), **causal** in criterion B's sense (item 5), and **stable in the DE12
sense** (no k⁰ mode; the gas is bounded). Its FRW background and growth are well posed across the kink (item 3).

It is **not** Hadamard-stable for cold matter as ξ → 0: at yield surfaces, and now at every zero of the band-passed field below
z_q0. The rate is capped by ξ, but a PM run that does not resolve ξ is capped only by its cell. The nonlinear free-boundary and
zero-field (Hölder-½) Cauchy problems stay open, as XR18 left them for H_Y.

**A PM run of H_K1 should proceed, on these conditions:**
1. Prescribe L(a) and y_th(a) from the box's scale factor. XR21's form is itself an action, and the dropped ⟨K⟩_h channel is
   ≤ 3e-5 of ρ̄.
2. Implement the ramp analytically, switching off exactly at z_q0.
3. Declare λ ≤ 0.03. The quasi-static QUMOND solve is its λ → 0⁺ limit.
4. Run at least two cell sizes and show that σ₈, the forest and P(k) converge. Alternatively, give the carrier a physical
   width. The d^(−1/4) law predicts roughly ×1.5 in the local rate per ×5 in resolution at zeros and surfaces.
5. Monitor the minimum band-passed field. Low-field regions carry an unbounded susceptibility below z_q0.

Outside this audit, and still open:
* FP19's KiDS numbers are pre-FP20; use FP20's exact projector.
* The baryons-only reading (FP22).
* The per-mode versus real-space yardstick (XR21).

## Controls and MUTATE

| Script | Control | Reproduces | Result |
|---|---|---|---|
| symbol_channel | K1: FP19's code exec'd read-only | FP19 H1 (σ₈ ×4, forest ×4, flagships ×4, SPARC ×2, KiDS ×6 *pre-FP20*), L(z), y_th(z) | max dev 0 (35 numbers); closed forms 0 |
| symbol_channel | K2: FP19's symbol_table + K_channel | FP19 H3 (headline 1 − eps_K; H_S band) | 0 |
| symbol_channel | K3: **XR18's own functions** (text extracted) | XR18 N3: R_B 6.92–7.47 / 7.62–8.13 at z ≤ 0.635, band 0.12–1.62 h/Mpc | 0 |
| symbol_channel | K4: sympy ADM expansion | the Friedmann pair; the hand-derived channel operator | exact |
| ramp_lambda | K1, K2 | XR18 Q1 (smoothed-ramp σ₈) and Q2 (ω_r) on H_S | 0 |
| ramp_lambda | K3, K4 | XR25 L2/L4 (λ_max 274.39; tracking, α₂v²); FP7 B6's 12 strong-coupling rows | 0 |
| yield_surfaces | K1: **XR18's own radial functions** | XR18 B4b, 202 rates on 24 hosts | 0 |
| yield_surfaces | K2: XR18_yield_surface's own host_profile | XR18 A2 slopes | 0 |
| second_variation | K1: XR18's WKB engine (extracted) | DE12's S identically; DE12's c_gate on 24 layers | 4.4e-16 |
| second_variation | K2: XR18's radial functions | XR18 B2 (24 hosts) and B3 base rates | 0 |

| Script | MUTATE (pre-declared) | Must fail | Outcome |
|---|---|---|---|
| symbol_channel | FP13's variance-fixed B restored (tied yield kept) | S1 | S1 FAIL (min S = −8.90, band 0.11–1.82 h/Mpc), rc = 1 |
| ramp_lambda | hard step at q = 0 | R2 | R2 FAIL (chord step shrink ×1.00), rc = 1 |
| yield_surfaces | yield sign flipped (J_P2 − 2y_th√Y) | A1 | A1 FAIL (16,587 of 4,309,704 roots violate criterion B), A2 FAIL, rc = 1 |
| second_variation | DE12's local density-read gate | B1, B2w, B3 | B1, B2, B2w, B3 FAIL (B3: 613.8% grid change; B2w up to 4.9e4 H), rc = 1 |

Main runs: symbol_channel, ramp_lambda and yield_surfaces have rc = 0. **second_variation has rc = 1** because of B2, a
load-bearing failure that was pre-declared, expected and is kept as run. Its reading is in section 5.

## Disclosures

* **Exploratory runs before any script was written** (scratch, not in the repository):
  * a read-only reload of FP19's machinery, which reproduced its H1/H3 exactly;
  * a sizing of I(L), I_halo and ⟨x⟩ on H_K1's grown state (ρ_extra ~ 1e-5);
  * sympy prototypes of the ADM expansion, the constrained block and the minisuperspace Noether identity. The first form of
    that identity, written with an undefined sympy function, gave a spurious nonzero residual (a `Subs` artefact); the scripts
    use explicit test functions;
  * XR18's B4b recipe on H_K1's hosts (190–374 H at ξ/10);
  * DE12's convention on H_K1's isolated hosts (4e4–1.4e5 H at z = 0.25, in the far field). B2's hypothesis was written knowing
    this, and says so.
* **Fixes after first runs.** All runs were MUTATE first and main last.
  * symbol_channel:
    * The first MUTATE run failed S2's ratio test on a bookkeeping mismatch: a(t)³ against the Fourier block's a₀³. It was fixed
      and MUTATE re-run.
    * After the first main run, the verdict text misstated S1's k-range (it is sub-horizon). The text was fixed and MUTATE and
      main re-run.
    * Before the first run, S1's bound was given its dln C/dln a term (the ζζ̇ mass term).
  * yield_surfaces:
    * The first MUTATE run failed the K2 control at 1.3e-7. The two XR18 scripts use different M_sun (FP6's 1.98847e30 versus
      DE12's 1.98892e30). K2 now uses XR18_yield_surface's own host code, and matches exactly.
    * The second MUTATE run returned nan in A2's centre clause: FP6's `gfrac_smooth` cancels catastrophically below x ~ 1e-6.
      For the cored centre only, it was replaced by the regularised incomplete gamma P(3/2, x²/2), checked against
      `gfrac_smooth` to < 1e-9 where both are accurate. Z1's numbers did not change.
    * MUTATE was run three times, then main once.
  * ramp_lambda and second_variation: no fixes after their first runs.
* **Threads.** At most 2 (BLAS/OpenMP = 2), one script at a time. Each script runs in under 40 s.
* **Side effect.** Importing the shared modules writes gitignored bytecode into the folder's `__pycache__`: `XR18b_common`, and
  possibly a refresh of `XR25_common`'s. No tracked file outside `XR18b_*` was written.
* **Not done:**
  * a nonlinear (free-boundary or zero-field) Cauchy problem;
  * a PM run;
  * the baryons-only reading;
  * any KiDS verdict (FP20's projector was not needed here).

## Files (all in `real_research/cross_thread_review_2026_09_26/`)

| File | Content |
|---|---|
| `XR18b_common.py` | Lane helper; read-only loaders of FP19 (slices of its main()), FP9, DE12; text extraction of XR18's functions; H_K1's closed forms; FP7 B6's ℓ_sc |
| `XR18b_symbol_channel.py` (+ `.out`, `_MUTATE.out`, `_results.json`, `_results_MUTATE.json`) | items 1–2: symbols, the ⟨K⟩_h channel, eps_K, Bianchi, translation |
| `XR18b_ramp_lambda.py` (+ outputs) | item 3: the kink, FRW growth, the background, λ, strong coupling |
| `XR18b_yield_surfaces.py` (+ outputs) | items 4–5: criterion B, exponents, cold matter at surfaces and zeros |
| `XR18b_second_variation.py` (+ outputs) | item 5: WKB count, DE12's convention (isolated, embedded, zeros), the gas radial sector |
| `XR18b_README.md` | this file |

Run any script from the repository root, e.g. `python3 real_research/cross_thread_review_2026_09_26/XR18b_symbol_channel.py`.
Set `MUTATE=1` for the control run. It writes `*_MUTATE.out` and `*_results_MUTATE.json` and never touches the main outputs.
