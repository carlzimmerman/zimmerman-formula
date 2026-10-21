# CFG957 — the owner's idea (2026-10-21): a0(z) oscillates like a wave. Physical models, and every observable other than the expansion bound (FROZEN, before any script or number from this lane)

Block CFG950–959; the id was reserved in the LEDGER (436f62cea2). **The oscillating-a0(z) hypothesis, including its refined form
(the wave is larger early and shrinks over time, and today a0 is on the way down from a recent peak), is the owner's idea
(2026-10-21).** The owner's blue sketch was a rough illustration only; the hypothesis is the general family.

**Split with CFG956.** CFG956 (criteria 707cdf4cb4, amendment A1 8debb62336) computes the expansion-data bound on the wave
(CFG689's BAO + Pantheon+ likelihood, plain and damped families, the sketch). This lane does not recompute that bound. It does:
Part 1, the physical models the framework offers for a wave in ρ_DE; Part 2, every other observable a wave touches. Where a CFG956
number is needed, it is read from CFG956's committed files if they exist when this lane's MAIN run starts; otherwise the README
says "CFG956 pending" and uses only CFG956's frozen statements (e.g. its K5: no expansion datum constrains z > 2.5).

## 0. Read before freezing (not blind)
- THEORY_CANONICAL_2026-10-18.md and the 2026-10-21 DRAFT (§3.8: CFG689's native band; §0 item 7 and obligation 10: three
  dark-energy readings in use).
- CFG689: README, cfg689_summary.md, cfg689.json (read only; its script is never imported or run).
- CFG956 FROZEN_CRITERIA.md and A1, and its uncommitted K output (seen; not used for any number here).
- CFG935 (energy sink; the R-d dark-energy partner, Δρ_DE/ρ_DE ≈ 1e-6), CFG630 (settling feeds ρ_DE: one-sided Q ≥ 0, phantom-side
  trickle 0.8–1.25e-6 since z = 1; the canonical partner φ̈ + 3Hφ̇ + V′ = Q/φ̇ is singular at φ̇ = 0), CFG542 (partner φ coherent,
  canonical, V unspecified), CFG131 (interacting vacuum, Q = ξ…, flat a0 only for |ξ| < 0.0275), CFG253 (dark energy → cold mass,
  ≤ 3% after recombination), CFG360_cold_fluid_from_dark_energy (C1 Q = Γρ_Λ; C2 a field whose minimum moves, residual
  oscillation (π mT/2)/sinh(π mT/2)), CFG288 (one field V = ρ_Λ + m²|Φ|², complex, m ≥ 2e-20 eV, amount free), CFG911 (readings ε,
  V = (ε−p)/2, −p, trace, active; the record uses three as one), CFG245 (the record's three declared vacuum rates H_Λ, a0/c,
  √(Gρ_Λ)), CFG223 (implied-a0 estimator; baryon lever d log s*/d(baryon dex) = −2.5 to −4.8), CFG926 R4 (fossil a0), CFG740
  (sealed wide-binary envelope has no a0 in it), CFG820 (L* ≥ 24 pc), CFG932 Q4 (the CFG650/654 engine is one-sided: instant
  deficit fill, no surplus removal). The DE1–DE13 lanes (memory index) are a vacuum GATE on where the law acts; none of them makes
  ρ_DE dynamical, so none is a candidate here.
- Numbers seen before freezing: the panel-(d) points and CFG689 quantiles in
  FIGURE_SUMMARY_2026-10-21/plotted_numbers.json; cfg689.json's P1/P6 quantiles (2.5/16/50/84/97.5%) and node posterior; the
  KiDS Δχ² of T1x −7.70, T2x −7.18, NC1x −10.08, NC2x −9.39 (robust −5.69 to −12.85).

## 1. The law and its readings
- a0 = κ c √(G F_DE), κ = ½ FITTED. A wave in a0 is a wave in F_DE.
- **Readings of F_DE (CFG911).** Primary three, each reported separately and never merged:
  - ε, the energy density (canonical S1);
  - −p, minus the pressure (stage-17);
  - V = (ε − p)/2, the potential (R16).
  - Trace (ε − 3p)/4 and active mass −(ε + 3p)/2 (both normalised to ε at w = −1): report only.
- **Expansion always sees ε.** H(z) and every distance depend on ε, whatever a0 reads. So CFG956's bound applies to an a0 wave only
  in the ε reading. Under −p or V it bounds the ε that accompanies the wave, not the a0 wave itself. This is a statement of the
  setup, written here before any number.
- Footings 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), never pooled. Ratios a0(z)/a0(0) do not depend on the footing.
  Absolute values and the committed points are given per footing (s* × 9.3603e-11 / a0_footing, as panel (d)).

## 2. Part 1 — physical models (declared; nothing else is tried)

### M1. A light canonical scalar dark-energy field oscillating in its potential
- **Model:** one real canonical scalar, minimally coupled, V(φ) = V0 + ½ m² φ², V0 > 0. ρ_DE = ε_φ = V0 + ½φ̇² + ½m²φ².
  - Frozen start (the attractor): φ̇ = 0 at a_i = 1e-3, field value set by r_i ≡ ½ m² φ_i² / V0.
  - New constants: m and r_i (two). V0 is today's dark energy, already an input.
- **Background (CFG689 primary best fit, cfg689.json BAO+SN.P2.pbest):** ω_b 0.0223601, ω_c 0.1201954, ω_k 0.0038916,
  ω_r = 2.4728e-5 (1 + 0.2271 × 3.044), today's dark energy W0 = w(0) = 0.3116063. h² = ω_m + ω_r + ω_k + W0.
  - V0 is solved (brentq) so that V0 + ρ_φ(a = 1) = W0; H0 is then CFG689's.
  - ρ_φ is fed back into H (self-consistent).
- **Equations.** In N = ln a, with H in units of 100 km/s/Mpc, μ = m/(100 km/s/Mpc):
  φ_NN = −(3 + H_N/H) φ_N − μ² φ / H², with (H²)_N = −3ω_m a⁻³ − 4ω_r a⁻⁴ − 2ω_k a⁻² − 3 H² φ_N².
  - scipy solve_ivp, DOP853, rtol 1e-10, atol 1e-13, from a_i to a = 1. The future, to a = 100, is used only to count future
    extrema.
- **Masses, declared now:**
  - (R) the record's own rates (CFG245): H_Λ = H0 √Ω_Λ; a0/c (both footings: 2a0/c is √(Gρ) of the footing's reading, a0/c itself
    is the rate); √(Gρ_DE) (both footings);
  - (X) illustrative masses outside the record: m/H0 ∈ {3, 5, 10, 20, 40}. A map of the family's predictions, never fitted and
    never selected by any datum. Every quoted (X) result carries "two new constants (m, r_i)".
- **Largest allowed r_i per (m, reading), r_max:**
  - (B) band check (ε, all readings): √X(z) = √(ε(z)/ε(0)) inside CFG689's 2.5–97.5% quantiles at z = 1.0, 1.2, 1.5, 2.33 (P1) and
    2.0 (P6). This is a band check, not a likelihood; CFG956 holds the likelihood.
  - (P) −p reading only: −p(t) ≥ 0 for all a ≤ 1 (else a0² < 0).
  - V is always ≥ V0 > 0 and ε > 0, so (P) does not apply to them.
  - Search: r_i on the grid 10^(−4 … 3) in 0.25-dex steps. r_max is the largest passing grid value below the first failure,
    refined by 30 bisections in log r_i up to the next grid value.
- **Reported per m:**
  - **Wave or not.** The number of local extrema of a0(z) in each reading over z ∈ [0, 5]; also over z ∈ [0, 10], and in the future
    to a = 100. "WAVE" means ≥ 2 extrema in z ∈ [0, 5] (a peak and a trough).
  - **Natural period.** In cosmic time, T_a0 = π/m (Gyr) for −p and V; the ε ripple shares it. In e-folds,
    P_ln(z) = π H(z)/m at z = 0, 1, 2.33 (a chirp, set against CFG956's fixed-P grid).
  - **Onset.** z_osc, where H(z_osc) = m.
  - **Damping.** β_ρ = the slope of ln ρ_φ against ln(1+z), fitted over z ∈ [0, z_osc/2] (m with z_osc ≥ 2 only). The a0 wave's
    relative amplitude in −p (V) is ρ_φ/(2V0) (ρ_φ/(4V0)) for small r, so β = β_ρ. In ε the ripple is (3H/4m)(ρ_φ/V0) by D6, so
    β_ε = β_ρ + ⟨d ln H/d ln(1+z)⟩ over the same window.
  - **Phase today.** The sign of d a0/dt at a = 1, per reading.
  - **"On the way down" natural or chosen.** On 400 log-spaced masses in [3, 40] H0 at r_i = 0.01, the fraction with d a0/dt < 0
    today, per reading. NATURAL if ≥ 0.9; CHOSEN (a selection on m) if < 0.9; THEOREM if it follows for every m.
- **Sub-variant (derivation only):** a complex field on a circular orbit (CFG288's form) has p_osc ≡ 0.

### M2. The record's own dynamical dark-energy partner (CFG542 Pb, CFG630, CFG935 R-d)
- φ̈ + 3Hφ̇ + V′(φ) = Q/φ̇, with Q ≥ 0 (CFG630 class A, one-sided). V is not specified by the record.
- **Derivation (D7):** u = ½φ̇² obeys du/dt = −6Hu − V′φ̇ + Q, so du/dt = Q > 0 at u = 0. φ̇ can never change sign: the partner
  cannot turn, and so cannot oscillate, while it is the settling sink.
- **Amplitude ceiling:** any rise of ε is ≤ ∫Q dt. CFG630's total since z = 8 is ≤ 3.8e-6 ρ_DE, so ≤ 8.3e-7 dex in a0.
- **Numeric toy (MUTATE M-d):** V0 + ½m²φ², m = 10 H0, the ΛCDM background of §2 (no feedback), Q = q · 3H W0 with q = 1e-6.
  Start: φ̇ > 0 small at a_i = 1e-3. Radau, rtol 1e-9, with an event at φ̇ = 0.

### M3. Exchange between cold energy and dark energy (CFG131, CFG253, CFG360-DE C1, CFG630)
- **Vacuum continuity (D8):** for a w = −1 component, ρ̇_DE = −Q exactly (no Hubble term). So ρ_DE is monotone over any interval
  where Q keeps one sign. A wave needs a Q that changes sign periodically. Every record Q is one-signed: CFG630 Q ≥ 0; CFG253 and
  CFG360-DE C1 run dark energy → cold; CFG131's ξ is a constant.
- **Linear two-fluid relaxation (D8):** Q = Γ(ρ_c − R ρ_DE) gives det = −3HΓR < 0, a saddle with no oscillation. The general
  linearisation Q = q_c ρ_c + q_d ρ_DE is also derived. Complex eigenvalues are possible only around the ρ_c = 0 fixed point, so
  they would need ρ_c < 0. The only fixed point with ρ_c ≥ 0 is ρ_c = 0, so no physical oscillation exists about an equilibrium.

### Physical-model classes (per model)
- **WAVE FROM FRAMEWORK SCALES:** "WAVE" (≥ 2 extrema of a0 in z ∈ [0, 5]) with the record's own scales and zero new constants.
- **WAVE ONLY WITH NEW CONSTANTS:** "WAVE" only with constants not in the record; they are counted.
- **NO WAVE:** the model cannot oscillate (theorem or numerics).
- **Overall physical axis:** NO PHYSICAL MODEL IN THE FRAMEWORK iff no model is in the first class.
- **Energy and stability, reported per model:**
  - NEC (ε + p ≥ 0) and dε/dt = −3Hφ̇² ≤ 0 (D5). So in the ε reading a canonical scalar can never give a0 a local peak in time.
  - No ghost, c_s² = 1, m² > 0.
  - −p ≥ 0 (D10); the coherent-partner requirement of CFG542.
  - The DESI-type phantom crossing, impossible for a canonical field.

## 3. Part 2 — observables

### (a) Galaxy dynamics over time
- **Predictions.** log10[a0(z)/a0(0)] at z ∈ {0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5}, per reading, for every (X) mass at r_max of that
  reading. The required per-point error for a 3σ separation from flat is |Δ|/3. The gap to the rival a0 ∝ H(z) (CFG223 curve) is
  also given.
- **Windows and testability.** W_low = {0.5, 1, 1.5, 2}, W_high = {2.5, 3, 3.5, 4, 4.5, 5}.
  - TESTABLE in a window iff |Δ| ≥ 0.15 dex at ≥ 2 of its redshifts. That is a required error ≥ 0.05 dex, half of CFG689 P6's
    decisive 0.10 dex.
  - Otherwise UNTESTABLE NOW.
- **The committed points** (read only from plotted_numbers.json; K1 re-reads them from their sources):
  - MeerKAT HI (z 0.067); RC100 route B Q1, Q2, Q3; ALESS 122.1; ALPINE 6 pooled; CRISTAL R_out (primary). CRISTAL R_e is a
    variant, not added: both CRISTAL routes use the same galaxies.
  - RC100 Q4 (upper bound) is listed only.
  - y_i = log10 s*_i; σ_i = ½[log10 hi68 − log10 lo68] (CFG956 §6).
  - The alt footing shifts every y_i by the same constant. With a free offset c that changes nothing, so the statistics below are
    footing-independent.
- **Model vs points.** For each (X) curve at r_max (each reading): Δχ² = χ²(curve + c) − χ²(flat + c), c profiled. Statistical
  errors only, and with a systematic floor σ_sys = 0.375 dex added in quadrature (CFG223's smallest baryon lever, 2.5, times the
  record's 0.15-dex baryon floor).
- **Galaxy-side wave statistic T (a detection statistic; its best template is never adopted as a model).**
  - Bank: templates T_k(z) = (1+z)^β cos(2 m t(z) + φ), with m/H0 ∈ {3, 5, 10, 20, 40}, β ∈ {0, 3} and φ = jπ/8 (j = 0…7):
    80 templates. t(z) is cosmic time in the §2 background with ρ_φ ≡ 0.
  - Model y = c + A T_k; A has free sign; c and A by weighted least squares.
  - T = min_c χ²(flat) − min_{k,A,c} χ².
  - Null: 4000 Gaussian mocks y_i ~ N(0, σ_i), seed 9571. p = (1 + #{T_null ≥ T_obs})/4001. T_3σ = the 99.73% quantile.
  - Systematic variant: σ_i → √(σ_i² + 0.375²), with its own null (seed 9573).
  - **Labels** (reported; the phenomenology classes do not rest on them):
    - NO WAVE SIGNAL: p_stat ≥ 0.05;
    - PATTERN IN STATISTICAL ERRORS ONLY: p_stat < 0.05 and p_sys ≥ 0.05;
    - WAVE-LIKE PATTERN, NOT A DETECTION: p_stat < 0.003 and p_sys < 0.05.
  - Every label carries the selection caveat: the 53 no-root galaxies at z ≈ 2–5 are not in the points, which biases them high,
    and baryon masses move s* by factors of 2–10 (CFG223).
- **Galaxy response (reported).**
  - T_a0 = π/m against orbital times of 0.3–1.2 Gyr. Adiabatic iff T_a0 ≫ t_orb.
  - In deep MOND, v⁴ = G M a0 with j = r v conserved gives r ∝ a0^(−1/4).
  - Bin averaging: the amplitude factor |sinc| for a bin of Δ ln(1+z) = 0.2 at the local P_ln(z).

### (b) Today's d a0/dt
- (1/a0) d a0/dt at a = 1, in units of H0 and per year, per reading, for every (X) curve at r_max.
- The CFG956 damped family's value is −H0 d ln a0/d ln(1+z)|₀ = −H0 ε0 (β sin φ + (2π/P) cos φ)/(1 + ε0 sin φ). It is evaluated
  only if CFG956's committed ε0_95 exist; otherwise the formula alone is given.
- **Local constraints in the record:** the Solar System is Newtonian through the stiffness term (CFG770); the sealed wide-binary
  envelope has no a0 in it (CFG740); the outer globulars are screened (CFG820). No pulsar, LLR or laboratory a0 limit is in the
  record. Class: ALLOWED BUT UNTESTABLE NOW, unless such a constraint turns up in the record.

### (c) Structure growth
- **Ratchet.** The CFG650/654 engine fills deficits instantly and never removes a surplus (CFG932 Q4). So its settled cold energy
  follows the running MAXIMUM of the phantom target, not the instantaneous a0.
  - Effective shift Δln a0_eff = max over z ∈ [0, 3] (also [0, 10]) of ½ ln[F(z)/F(0)], per reading. The two-sided (time-average)
    figure is also given.
- **Lever from the record.** dΔχ²_KiDS/d ln a0 = (Δχ²_alt − Δχ²_can)/ln(1.1312e-10/9.3603e-11): native (NC2x − NC1x) and inherited
  (T2x − T1x).
  - Predicted ΔΔχ² = lever × Δln a0_eff, compared with NC2x's robustness span and with the class line (TENSION at Δχ² ≥ 4).
  - Order of magnitude only: the footings differ in more than a0.
- **Fossil.** The deep-MOND fossil excess is E_σ = ¼ ln F_max^(a0), against the dwarfs' +0.38 (CFG827) and CFG926 R4.

### (d) CMB: distance to last scattering and ISW (reading-independent: both depend on ε only)
- **Distance.** δD_M(z*)/D_M, z* = 1089.9, for every (X) curve at r_max(ε). The comparison background has ρ_φ ≡ 0 and V0 = W0 (same
  H0 and ω's). The shift is set against CFG689 A2.1's datum error (100θ* = 1.04109 ± 0.00030, 0.029%).
  - Reported only, with no nuisance refit (ω_k and h can absorb part).
  - **The record's native θ* treatment is blocked:** CFG689's θ* rows are held back because its K9 failed as frozen. So no class
    rests on this item.
- **ISW proxy.** Linear growth D(a) (ρ_φ smooth; c/m ≥ 0.1 Gpc for m ≤ 40 H0) in the model and comparison backgrounds. The
  fractional change in I = ∫ |d(D/a)/d ln a| d ln a over z ∈ [0, 3] is set against a declared 20% (an ISW detection at ~5σ).

### (e) BAO and SNe
- CFG956 only.

### (f) The distinctive signature
- **Extrema.** The number of extrema of a0(z) in z ∈ [0, 5] per reading. Flat, the ΛCDM emergent proxy and a0 ∝ H(z) have none
  (monotone).
- **Mismatch.** The kinematic-vs-expansion mismatch M = max over z ∈ [2.5, 5] of |log10 a0_reading(z) − log10 √(ε(z)/ε(0))|.
- **The ε-reading theorem (D5).**
- The cleanest smoking gun and the epoch when data could see it are stated in the README from these numbers.

## 4. Classes

### Phenomenology axis
Per sub-hypothesis:
- **H1:** a wave at z ≤ 2.33;
- **H2:** a wave at 2.5 ≤ z ≤ 5, larger early;
- **H3:** a0 on the way down today;
- **H4:** large low-z excursions like the illustrative sketch.

Class labels:
- **ALLOWED AND TESTABLE:** allowed by every committed constraint, and TESTABLE by §3(a)'s rule in its window. The window and the
  measurement are stated.
- **ALLOWED BUT UNTESTABLE NOW:** allowed, but not TESTABLE, or no probe exists.
- **EXCLUDED:** only by a committed likelihood (CFG956) or a theorem, with its significance. This lane's band checks alone can only
  say "OUTSIDE CFG689's 95% BAND (marginal per node)".

### Physical-model axis
As in §2.

### Both axes
Both axes are reported for each sub-hypothesis. A phenomenologically allowed wave can still have NO PHYSICAL MODEL IN THE
FRAMEWORK.

## 5. Controls

### K (overall PASS needs K1–K5; if any fails, the main numbers are reported as unverified)
- **K1:** the 8 points (and Q4) re-read from CFG303, CFG309, CFG301 and the chart CSV, equal to plotted_numbers.json to 1e-9 relative.
- **K2:** cfg689.json's P1 (1.0, 1.2, 1.5, 2.33) and P6 (2.0) quantiles, read here, equal plotted_numbers.json's q16/q50/q84 to
  1e-9. h from pbest within 0.005 of P3's median H0/100.
- **K3:** the KG solver.
  - (a) r_i = 0 gives every reading ratio ≡ 1 to 1e-10.
  - (b) EdS (ω_m only, H = 2/(3t)): φ/φ_i equals sin(mt)/(mt) to 1e-6 over mt ∈ [0.1, 30].
  - (c) |dε/dN + 3(ε + p)| / ε ≤ 1e-6 along an (X) run.
  - (d) Pure de Sitter, m = 1.2 H (< 3H/2): φ never crosses zero to N = 20; m = 2 H crosses (analytic roots).
- **K4:** β_ρ at m = 40 H0 over z ∈ [0.3, 3] lies in 3 ± 0.1.
- **K5:** the rival a0 ∝ H(z) at z 1–5 from cfg223_results.json equals plotted_numbers.json to 1e-9.

### MUTATE (separate _MUTATE outputs; frozen pass rules)
- **M-a, planted wave.** Template m = 7 H0 (off-grid), β = 3, φ = 1.0 rad. Amplitude chosen so that RMS_i(A_p T(z_i)/σ_i) = 3 over
  the 7 points (the planted wave is 3× the real errors). 500 realisations with N(0, σ_i) noise, seed 9574.
  - PASS if T ≥ T_3σ (stat null) in ≥ 90% of them.
- **M-b, null calibration.** 4000 fresh null mocks, seed 9572.
  - PASS if the false-positive rate at T_3σ is ≤ 0.01.
- **M-c, friction teeth.** The KG run with the Hubble friction reversed (−3Hφ̇ → +3Hφ̇), m = 40 H0.
  - PASS if β_ρ(reversed) < 0 while K4's β_ρ is in 3 ± 0.1.
- **M-d, partner teeth.** The M2 toy.
  - PASS if Q = 0 gives ≥ 2 sign changes of φ̇ by a = 1, and Q > 0 gives none (no φ̇ = 0 event, and min φ̇ > 0).

## 6. Derivations (sympy, cfg957_derivations.py; each check PASS/FAIL)
- **D1:** de Sitter roots λ = −3H/2 ± √(9H²/4 − m²). Underdamped iff m > 3H_Λ/2.
- **D2:** EdS: sin(mt)/(mt) solves φ̈ + (2/t)φ̇ + m²φ = 0. u = a^(3/2)φ obeys ü + (m² − 9H²/4 − 3Ḣ/2)u = 0.
- **D3:** WKB (two-timescale average): amplitude ∝ a^(−3/2), ρ_osc ∝ a⁻³.
- **D4:** for φ = A cos θ: ε = V0 + ρ_osc; −p = V0 + ρ_osc cos 2θ; V = V0 + ρ_osc(1 + cos 2θ)/2; trace and active. A complex
  circular orbit gives p_osc = 0.
- **D5:** dε/dt = −3H(ε + p) = −3Hφ̇² ≤ 0.
- **D6:** the ε ripple: δε = (3H/2m) ρ_osc sin 2θ to first order in H/m.
- **D7:** the M2 no-turning lemma.
- **D8:** M3: vacuum continuity; the 2×2 linear system (trace, det, discriminant); relaxation det = −3HΓR.
- **D9:** the lever's ln(1.1312/0.93603).
- **D10:** −p ≥ 0 ⇔ ρ_osc ≤ V0 (real field).

## 7. Hand estimates (made before any code; no weight)
- **Record rates.** H_Λ ≈ 0.83 H0; a0/c ≈ 0.14 / 0.17 H0; √(Gρ) ≈ 0.29 / 0.34 H0. All lie below 3H_Λ/2 ≈ 1.24 H0, so they are
  overdamped. No extremum before today, and none in the future: NO WAVE FROM FRAMEWORK SCALES.
- **m = 10 H0.** Onset z ≈ 5–6; about 3 a0 cycles to today; T_a0 ≈ 4.5 Gyr. Under −p, positivity gives r_i ≲ 1, so today's wave
  is ≲ 0.2%, ≲ 6% at z 2.33 and ≲ 30% at z 4.
  - "Larger early" (β ≈ 3) follows from Hubble friction alone.
  - The phase today is set by m: down for about half of all masses (CHOSEN).
- **ε reading.** A monotone staircase, ripple ≈ (3H/4m) r. a0 is always on the way down, with no recent peak possible (THEOREM).
- **M2, M3.** NO WAVE.
- **Today's rate.** (1/a0) d a0/dt ≲ r0 m ≈ 0.03 H0 ≈ 2e-12 yr⁻¹. Untestable locally.
- **Shear.** |ΔΔχ²| ≲ 3.6 × 0.35 ≈ 1.3: no class change.
- **θ*.** δD_M/D_M ~ 1e-3 to 1e-2 at m 3–10 H0 and r_max. Larger than θ*'s 0.03%, so a working native θ* would constrain it; it is
  blocked by K9.
- **Points.** No allowed curve moves any z ≤ 2.3 point by more than its 68% error. At z 4.5–5.3 the −p envelope may reach
  0.1–0.3 dex for m 5–10 H0, still at or below ALPINE's and CRISTAL's errors.
- **Statistic.** M-a detects in ≈ 100%. The real-data T may come out large in statistical errors alone (ALESS and ALPINE sit
  ≈ 3σ above MeerKAT's level), and not in the systematic variant.

## 8. Compute, outputs, wording
- **Compute.** One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, < 1 GB. Wall cap 1 h per mode; an amendment is
  needed before any rerun past the cap.
- **Outputs.**
  - cfg957_derivations.py → cfg957_derivations.{out,json};
  - cfg957.py, modes K / MAIN / MUTATE → cfg957_K.{out,json}, cfg957.{out,json}, cfg957_MUTATE.{out,json};
  - cfg957_figure.py → cfg957_a0z_envelopes.png (the panel-(d) layout, the predicted envelopes, the high-z prediction window);
  - README.md, leading with a plain-language summary for the owner.
- **Wording.**
  - "The owner's idea (2026-10-21)" in every file. No personal names or home paths.
  - κ = ½ FITTED; footings never pooled; not theory closed; never "the data favour the framework".
  - EXCLUDED is reported as plainly as ALLOWED. A bound on a wave is not evidence for a wave.
  - Any post-hoc change is a dated, labelled amendment.
