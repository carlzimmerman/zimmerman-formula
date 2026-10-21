# CFG948 FROZEN CRITERIA: the derived no-capture criterion (CFG939) confronted with the Coma UDGs and the NGC 1052 dwarfs

Written 2026-10-21 and committed ALONE, before any script of this lane exists and before any number of this lane is computed.
Block 940–949 (CFG948 row reserved in the LEDGER at 14ce57aef).

κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 m/s² are scored separately and never pooled. Raw data and
framework-native quantities only. The extra mass is cold energy, not a particle. Not "theory closed".

## 0. Status and disclosure (NOT blind with respect to the record)

**Seen before this file was written:**
- CFG933's README and `cfg933_results.json`: the 9 admitted Coma UDGs at ⟨E_obs⟩ = +0.760 / +0.669 ln over the isolated
  law (sealed estimator), se_obs 0.262 (canonical); the per-galaxy table; DF2 / DF4 at E_obs −1.709 / −2.170; the Coma −
  group residual difference +2.67 ± 0.55 (4.9σ); the S-set shifts (M* ±0.2 dex, σ ±15%, distance ±5%).
- CFG936's README: the 6 Lelli+15 tidal dwarfs at −0.690 / −0.728 dex; TDGs and DF2/DF4 consistent with Newton
  (+0.055 ± 0.114 dex; +0.021 ± 0.539 ln).
- CFG939's README, DERIVATION and `cfg939.py`: the no-capture criterion v_rel > V_esc,b (V_esc,b = √(2|Φ_b(r½)|), the
  `v_in_kms` of its N5 table: TDGs 21–53 km/s, DF2/DF4 22.9 / 22.1 km/s); f_crit(x) (2/3 deep); the flat frozen
  potential (co-moving binding −(2/3)GM_b/r); the statement that a conservative tether settles by expelling and never holds a
  surplus; the N4 sudden-loss runs (unbound at t = 0+ for f 0.5–0.9: 0, 0, 0.942, 1, 1). N4 did NOT record the enclosed
  medium relative to the post-loss law; nobody has computed it.
- THEORY_CANONICAL 2026-10-14 / 10-16 / 10-18 (S3 "surpluses are expelled (CFG776)"; S4 and its working rule H-EX;
  CFG941's theorem D-T "no gravity between tethered components; satellites would show an EFE-like hover").
- L23's Coma β-model constants (Freundlich+2022's X-ray hydrostatic model: kT 8.6 keV, r_c 276 kpc, β 0.71, μ 0.6) and the
  Coma table columns `d_kpc` (projected) and `dmean_kpc` (mean 3-D distance).
- The Leisman+2017 HI-bearing UDG table on disk (`real_research/data/alfalfa_huds_leisman2017.tsv`): column list and rows
  (logMHI ~8.5–9.4, gMAG −14 to −17).

**Hand estimates made from what was seen (disclosed; they shaped the A-grid and are NOT test results):**
- A = R_e / r_M (r_M = √(G M*/a0), current stellar mass) for the 9 admitted Coma UDGs: about 5.1–8.3 (canonical) and
  5.6–9.2 (alt). The engine grid A ∈ {5, 7, 9.5} was chosen to cover it.
- Coma UDGs: V_esc,b ≈ 13–19 km/s; g_bar/a0 ≈ 0.003–0.02, so the Newtonian floor E_N ≈ −2 to −2.5 ln.
- Single-stream, point-mass, deep-regime algebra (not run): after a sudden loss f < 2/3 each shell oscillates between its
  start r0 (inner turning point) and x r0, x = [ε + √(4ε − 3ε²)]/(2(1 − ε)), ε = 1/(3(1 − f)). The orbit spends more time
  outside the new equilibrium radius r0/√(1 − f) than inside, so the phase-mixed enclosed medium is expected at or BELOW the
  post-loss law. E(0+) = −½ ln(1 − f) > 0 is a transient.

**Expectations formed from what was seen (disclosed, not tested):**
- X1. The derived ceiling is the law (E_ceil = 0): the engine's phase-mixed W1 average ≤ 0 for every (A, f).
- X2. The in-situ / no-capture Newtonian reading (P-b) is EXCLUDED for the Coma UDGs at ≥ 5σ after systematics.
- X3. Against the ceiling, z_stat ≈ 2.9 / 2.5 and z_sys ≈ 1.7 / 1.5: not CONTRADICTED. The declared coherent
  systematics (σ_sys ≈ 0.36 ln) exceed the statistical error, so the MUTATE plus04 plant (+0.921 ln) reaches only
  z_sys ≈ 2.1. The main class is therefore expected to be **NOT DIAGNOSTIC (CONTROL-LIMITED: systematics, not N)**.
- X4. The sign verdict is expected to read "group sign predicted, difference sign allowed, Coma's above-law sign forbidden by
  the derived dynamics but not significantly contradicted".
- The rule "≥ 3σ after declared systematics" (quadrature) is the task's wording. It was adopted knowing X3. The statistics-
  only class and the per-variant z are committed as reported rows (R1) so the reader sees what a looser rule would give.

## 1. Question

CFG939 derived from the single-medium action (S2 + S3) that a system captures no cold energy iff it moves through the settled
medium faster than its own baryonic escape speed. Coma UDGs move through Coma's medium at v_rel ≥ 100 km/s (CFG939's declared
lower bound; Coma's dispersion is ~10× larger) against V_esc,b of tens of km/s, yet CFG933 found them ABOVE the isolated law,
while the NGC 1052 dwarfs and the tidal dwarfs sit at Newton. Two questions, one class each per footing:
- **Q1 (class):** is the Coma UDG sample inside the framework's derived allowed range (Newton floor to ceiling)?
  **CONSISTENT / CONTRADICTED / NOT DIAGNOSTIC** (section 4).
- **Q2 (verdict):** does the framework, with the derived criterion, predict the observed SIGN difference (Coma above the law,
  NGC 1052 group below it)? **PREDICTED / NOT PREDICTED, NOT EXCLUDED / CONTRADICTED** (section 5).

## 2. What the derived criterion predicts (the framework's allowed range)

### 2.1 The three histories
- **(P-c) DF2/DF4 and the tidal dwarfs: Newton.** Debris born moving through a settled medium at v_rel ≥ 100 km/s > V_esc,b
  captures nothing (CFG939 N5). Reproduced in K2 with CFG939's own code. Predicted E = E_N,i (per galaxy).
- **(P-b) Coma UDG born in the cluster** (from material orbiting the cluster: debris of cluster galaxies or stripped gas,
  moving at ~σ_cl ≫ V_esc,b): no capture → **Newton**, E = E_N,i. A system condensing at rest relative to the settled
  cluster medium (|v_rel| < V_esc,b ≈ 15–20 km/s) could capture, but then sits at most on the law; this does not raise the
  ceiling.
- **(P-a) Coma UDG born in the field, then infall.** In the field it moves with its local medium (v_rel small), captures and
  settles onto the law (CFG747/748). On infall:
  - *Ram pressure* acts on the gas, not on cold energy. Cold energy is collisionless. Its only couplings to Coma's
    flowing medium are the mass-rank tether (P, a functional of the total enclosed density, smooth over the UDG) and the
    stiffness force γ∇ρ_c. Coma's medium streams through at v_rel ≫ V_esc,b and is not captured (CFG939). The stiffness
    "ram" acceleration is bounded in R8 and must be ≪ the UDG's binding acceleration.
  - *Gas stripping* is a baryon-potential change (CFG939 §4.5(b)). A sudden loss (faster than the medium's radial period
    T_q) of fraction f unbinds the medium where f > f_crit(x) (2/3 deep) → the medium leaves → **Newton**. A loss with
    f < f_crit leaves the medium bound. A slow loss (≫ T_q) is adiabatic: each shell keeps zero radial action and tracks
    the moving equilibrium, i.e. the law of the current baryons.
  - *Tides* remove medium beyond the Jacobi radius r_J (the record's King/Jacobi treatment with law effective masses,
    CFG916). This can only lower the medium inside r½.
  - The only candidate surplus in S2 + S3 is the bound medium left after a sub-threshold sudden loss. Whether it is a
    surplus over the CURRENT baryons' law once phase-mixed is computed by the engine (2.3).

### 2.2 The ceiling
- The framework's allowed range for each Coma UDG is **[E_N,i, E_ceil]**, with E_N,i = −ln ν_e(g_bar,i/a0) (Newton in the
  same estimator) and **E_ceil = max(0, C_dyn)**. C_dyn is the engine's largest phase-mixed surplus (2.3).
  - E_ceil ≥ 0 because the f = 0 / adiabatic history gives exactly the law.
- The ceiling uses the **isolated, EFE-free law**, as CFG933 and the record's galaxy tests do. Two things only LOWER it:
  - the framework's external-field response;
  - the strict D-T reading (the medium hovers off the infalling baryons, R5).
  So a CONTRADICTED verdict against this ceiling would hold a fortiori. A CONSISTENT verdict would not certify the
  EFE-on case.
- **The record's surplus mechanisms, and their status:**
  - S3: surpluses are expelled (CFG776). CFG939: a conservative tether settles by expelling and never holds a surplus.
  - S4's free population and its working rule H-EX (the cold share of expelled baryons is free): NOT DERIVABLE from the
    single medium (CFG939). The gas trigger is not supported (CFG860), and free cold energy lands too far out for dwarfs
    (CFG822).
  - H-EX is therefore NOT used for the ceiling. It is quantified as reported row R4 (its frozen-profile maximum, and the
    f needed to reach the observed excess).

### 2.3 The engine: sudden sub-threshold loss in the exact S2 + S3 Lagrangian shell dynamics (derives C_dyn)
- **Units and kernel.**
  - G = a0 = 1, and the CURRENT baryonic mass M_b′ = 1, so r_M = 1 is the observed galaxy's current r_M.
  - The kernel (W_rem difference, Gant, Hpot, f_crit) is CFG939's, exec'd read-only from the text of `cfg939.py`. γ = 0,
    as in CFG939 N4. CFG939's N5 gives Mach ≥ 1.7 at r½ for DF2/DF4-like systems, so stiffness does not suppress crossing
    there.
- **Baryons.** Plummer, scale a = A (projected half-light radius R_e = A). Before the loss M_b = 1/(1 − f), with the same
  shape. At t = 0 M_b → 1 everywhere: sudden and uniform in radius.
- **Medium.**
  - N = 2000 shells in the discrete law equilibrium for the pre-loss baryons, from RMIN = 1 to R0 = 50, at rest
    (CFG939's construction with Φ_b generalised).
  - The core inside RMIN is fixed at the pre-loss law mass, with a reflecting boundary at RMIN (CFG939 convention).
- **Integration.** Leapfrog with dt = 0.02 (if a run's |dE/E| > 1e-3, dt is halved and the run repeated, at most 3 times).
  Run to t_end = 10 T_q, sampling every 0.5 time units.
  - T_q = 2π/ω at r12 in the post-loss law state, with ω² = 4πGρ_b + (2g_N/r)·a0/(a0 − u) (CFG939's formula).
- **Measure.** At r12 = (4/3)A:

  E(t) = ln[(M_b′(<r12) + M_c(<r12, t)) / (M_b′(<r12) + M_c,law′(<r12))].

  M_c(<r12, t) = core + dm × (number of shells inside r12), as CFG939 samples it. M_c,law′ = u_law′(r12)·r12² is the law
  for the current baryons.
- **Grid.** A ∈ {5, 7, 9.5} and f ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.65, 0.7, 0.8}, plus an f = 0 control for each A.
  - If any admitted Coma UDG has A outside [5, 9.5] on either footing (K4), the nearest half-integer beyond it is added to
    the grid mechanically.
- **Outputs per (A, f).**
  - E(0+): engine value and closed form;
  - **W1 = the mean of E(t) over [T_q, 10 T_q] (PRIMARY: a population of UDGs seen at random times after stripping);**
  - W0 = the mean over [0, T_q] and max_{t ≥ T_q} E(t) (reported);
  - the fraction unbound at 0+ (co-moving E_q > 0) and the fraction escaping (r > 10 R0, moving out) at the end;
  - |dE/E|.
- **C_dyn = max over (A, f) of W1.** If C_dyn > 0, that (A, f) is named and the ceiling rises to it.
- **Reported variant TT (tides; no ceiling weight).** At A = 7, the f-grid is rerun with an absorbing boundary at r_J
  (shells beyond r_J removed at t = 0 and whenever they cross it). r_J/r_M = the median over the 9 admitted Coma UDGs
  (canonical, at `dmean_kpc`) of the Jacobi radius computed as in section 3.3.

## 3. Data, estimator and inputs

### 3.1 Estimator: CFG933's sealed estimator, executed read-only
- **Execution.** `CFG933_udg_sealed_test/cfg933.py` is exec'd from its text, read-only (writes refused, sys.exit
  trapped), up to and including its K-stage. Its own K-checks must pass. Its `evaluate` and `summ` functions are then
  exec'd from its text unchanged.
- **Membership.** CFG933's primary: **G-Coma** = the 9 admitted Coma UDGs; **G-group** = NGC 1052-DF2 and -DF4.
- **Per galaxy:**
  - E_obs,i = 2 ln(σ_obs/σ_law);
  - sE_i = 2e_i/σ_obs (Coma errors are symmetric);
  - g_bar,i = G(M*/2)/r12², r12 = (4/3)R_e;
  - E_N,i = −ln ν_e(g_bar,i/a0).
- **Footings.** CFG933's A0 values for both footings.

### 3.2 Framework-native inputs used only for reported rows (no class weight)
- **Coma's total field:** Freundlich+2022's X-ray hydrostatic β-model as coded in L23. Constants read from L23's text, K4:
  g_tot(r) = (3βkT/(μ m_p))·r/(r² + r_c²).
  - Host phantom field (the law's own inversion): u_host = g_tot·a0/(g_tot + a0), since g_N = g²/(g + a0).
- **Positions.** D = `dmean_kpc` (primary) and D = `d_kpc` (projected, the minimum 3-D distance, strongest field).
- **Leisman+2017 HUDs.**
  - M* = Υ_g · 10^(−0.4(gMAG − 5.11)), with Υ_g ∈ {0.5, 1, 2};
  - M_gas = 1.33 · 10^logMHI;
  - f_gas = M_gas/(M_gas + M*).

### 3.3 Jacobi radius (the record's tidal treatment)
- For a host with circular frequency Ω² = g_tot/D: r_J³ = G m_eff(<r_J) / (g_tot/D − dg_tot/dD). For the β-model the
  denominator is 2C D²/(D² + r_c²)².
- m_eff(<r) = g_law(r)·r²/G is the UDG's isolated-law effective mass, with Plummer M*, a = R_e.
- r_J is solved by bisection.

## 4. Statistic, systematics and the class (Q1)

- **Statistical error.** se_obs = max( std(E_obs; ddof 1)/√N , √(Σ sE_i²)/N ), CFG933's convention, on G-Coma (N = 9).
- **Upper test (the ceiling).**
  - Δ_up = ⟨E_obs⟩ − E_ceil.
  - σ_sys,up² = s_M² + s_A² + s_D² + s_T², where:
    - s_M, s_A, s_D = |⟨E_obs⟩(X+) − ⟨E_obs⟩(X−)|/2 for CFG933's S-pairs: M* × 10^(±0.2); σ_obs and its errors × 1.15^(±1);
      Coma distance × 0.95 / 1.05 with M* ∝ D², R_e ∝ D;
    - s_T = max over k ∈ {dmean, dproj} of |⟨E_obs⟩(S-T_k) − ⟨E_obs⟩(primary)|;
    - **S-T_k (cluster tidal truncation of the light):** each UDG's light is a Plummer sphere truncated at its r_J(D_k),
      with the projected half-light radius held at the observed R_e. r12 becomes (4/3)R_e × [r_h,3D/R_e](truncated) /
      [r_h,3D/R_e](untruncated); M* and σ are unchanged. Unbound-star inflation of σ is not modelled; it is covered by
      S-A−.
  - z_up = Δ_up / √(se_obs² + σ_sys,up²); z_stat,up = Δ_up / se_obs (reported).
  - The ceiling E_ceil is the same constant in every variant: the law is recomputed with the varied inputs.
- **Lower test (the Newton floor).** Δ_low = ⟨E_N⟩ − ⟨E_obs⟩, with systematics from the same variants applied to
  ⟨E_obs − E_N⟩; z_low.
- **Power.** P_ok iff 3√(se_obs² + σ_sys,up²) < 0.4 ln 10 = 0.921, i.e. an excess of +0.4 dex above the ceiling would be
  CONTRADICTED.
- **Class per footing, in this order:**
  - **CONTRADICTED (ABOVE THE CEILING)** iff z_up ≥ 3. **CONTRADICTED (BELOW THE FLOOR)** iff z_low ≥ 3.
  - **NOT DIAGNOSTIC** iff N < 5, or P_ok fails, or a MUTATE fails (label CONTROL-LIMITED, section 7).
  - **CONSISTENT** otherwise. Add "2–3σ tension" if max(z_up, z_low) ≥ 2.
- **Sub-hypothesis rows (graded words, not the lane class).**
  - **H_b** (every Coma UDG born in the cluster, P-b) and **H_a,sup** (field-born, stripped suddenly with f > f_crit):
    both predict E_N,i. They are tested with Δ_N = ⟨E_obs − E_N⟩, systematics from the variants on ⟨E_obs − E_N⟩, and
    z_N. The words are EXCLUDED iff z_N ≥ 3, else NOT EXCLUDED.
  - **P-c per galaxy:** DF2 and DF4, z_i = (E_obs,i − E_N,i)/sE_i, with e on the side toward Newton. A pair mean is
    reported.
- **Environment difference (reported with a word).**
  - D_obs = ⟨E_obs⟩_Coma − ⟨E_obs⟩_group, with se_D = √(se_Coma² + se_group²). For the group, sE_i = (e+ + e−)/σ_obs,
    symmetrised, under the section-4 se convention.
  - Framework interval: [⟨E_N⟩_Coma − ⟨E_N⟩_group, E_ceil − ⟨E_N⟩_group].
  - z_D = distance outside the interval / se_D, stat-only; a second number adds Coma's σ_sys,up in quadrature.
  - Words: ABOVE THE FRAMEWORK'S MAXIMUM iff z_D ≥ 3, else INSIDE / WITHIN 3σ.

## 5. The sign verdict (Q2)

- **Group sign (below the law)** is PREDICTED iff the P-c prediction ⟨E_N⟩_group < 0 and ⟨E_obs⟩_group < 0.
- **Coma sign (above the law).**
  - If E_ceil ≤ 0, "above the law" is FORBIDDEN by the derived dynamics.
  - If E_ceil > 0, it is ALLOWED up to E_ceil.
- **Verdict:**
  - **PREDICTED:** E_ceil > 0, ⟨E_obs⟩_Coma ≤ E_ceil within Q1's errors (z_up < 3), and the group sign is predicted.
  - **NOT PREDICTED, NOT EXCLUDED:** E_ceil ≤ 0 and Q1 is not CONTRADICTED (ABOVE).
  - **CONTRADICTED:** E_ceil ≤ 0 and Q1 is CONTRADICTED (ABOVE).
- **Required statement.** The README must say which statement of the record would have to change to predict the sign. The
  candidates are S3's "surpluses are expelled", CFG939's "never holds a surplus", and S4 / H-EX made derivable (an
  untethered bound component: CFG888's unwritten coupling). It must give R4's numbers.

## 6. Reported rows (no class weight)

- **R1 statistics-only reading:** the section-4 class with σ_sys = 0 and power on se_obs alone, plus z_stat,up for every
  single S-variant. Label FRAGILE if a single variant flips that statistics-only class.
- **R2 L23's weighting:** inverse-variance (sE⁻²) mean vs the ceiling.
- **R3 all 11 Coma UDGs** (adding DF44 and J125904.06+281422.4), upper test.
- **R4 the H-EX reading (S4 working rule, NOT DERIVABLE per CFG939).**
  - The frozen-profile surplus if the cold share of lost baryons stays in place: per galaxy,
    E_HEX(f) = ln[(M_b′ + M_c,law(M_b′/(1 − f)))/(M_b′ + M_c,law(M_b′))] at r12, with the isolated law and the enclosed
    baryons M*/2.
  - f* is the uniform f at which ⟨E_HEX⟩ = ⟨E_obs⟩. It is compared with R6.
- **R5 the strict D-T reading (CFG941; the record's open F2 problem, CFG945).**
  - Per galaxy: u_host(D)/g_N,max, where g_N,max = 2GM*/(3√3 R_e²) is the Plummer maximum. Given at D = dmean and dproj.
  - If ≫ 1 under D-T, the UDG's baryons cannot hold their medium against the host acceleration they alone feel, and the
    prediction collapses to H_b's Newton.
- **R6 HUD gas fractions** (Leisman+17, all rows, then the restrictive set R): median f_gas and the fraction above 2/3,
  for each Υ_g. This is the fraction of field gas-bearing UDGs that would cross f_crit if stripped suddenly.
- **R7 per-galaxy table:**
  - V_esc,b (CFG939's v_in, Plummer(M*, R_e) at 1.305 R_e);
  - T_c (CFG939's sys_numbers) and f_crit at r12 (current x);
  - r_J/r12 and r_J/r_M at dmean and dproj;
  - E_obs ± sE, E_N, and z against the ceiling and against Newton.
- **R8 stiffness "ram" bound.** a_γ = 2πG L*² |∇ρ_host| at D = dmean, with L* = 1 kpc (the window's upper end) and ρ_host
  the β-model's TOTAL density (an overestimate of the cold part), divided by the UDG's g_law(r12). The section-2.1 claim
  needs ≪ 1 for every galaxy.
- **R9 CFG939's own grader sides for the Coma UDGs.** P-a = `collapsed=True`; P-b = `collapsed=False` at v_rel 100 and
  50 km/s. These are compared with the observed side.

## 7. Controls

**K-tests** (any failure stops the lane with no class; a dated amendment is then required):
- **K0:** cfg933.py exec'd read-only through its K-stage, with all its K-checks passing.
- **K1, CFG933 reproduced.** Per footing, the following equal `cfg933_results.json` to ≤ 1e-12 (absolute):
  - G-Coma ⟨E_obs⟩, se_obs and z (against its P2 prediction);
  - DF2/DF4 E_obs and z;
  - H (diff, se, z).
- **K2, CFG939's classification reproduced.** CFG939's N5 functions are exec'd from the text of `cfg939.py`. Then:
  - v_in, T_c, f_crit and g_N/a0 for the 6 TDGs and DF2/DF4 equal `cfg939_results.json` to ≤ 1e-9 relative, on both
    footings;
  - the derived-reading sides ('tidal dwarfs', 'DF2/DF4' = BELOW) equal the JSON in every cell (2 footings × 4 L* ×
    v_rel 100/50).
- **K3, engine.**
  - (a) In point-mass mode the lane's law IC, accelerations, energy and shell energies equal CFG939's spherical functions
    (exec'd from its text) to ≤ 1e-12 relative.
  - (b) The point-mass t = 0+ unbound fractions for f 0.5–0.9 equal CFG939's N4 exactly.
  - (c) The Plummer law IC has |force| ≤ 1e-10 g_N.
  - (d) For every grid run, the engine's E(0+) equals the closed form within 0.01.
  - (e) The f = 0 control keeps |E(t)| ≤ 0.01 and |dE/E| ≤ 1e-6.
  - (f) Every grid run has |dE/E| ≤ 1e-3 after at most 3 dt halvings.
  - (g) "Frozen-medium tooth": E(0+) > 0 for every f > 0, so the measure can register a surplus.
- **K4, inputs.**
  - L23's β-model constants equal the lane's.
  - E_N,i equals 2 ln(σ_N/σ_law) with σ_N² = r12 g_bar/3, to ≤ 1e-12.
  - The A-grid covers every admitted Coma UDG on both footings (else the grid is extended per 2.3).
  - V_esc,b of the Coma UDGs comes from CFG939's own `plummer` and `phi_grid`.

**MUTATE** (separate outputs `_MUTATE_onlaw`, `_MUTATE_plus04`; blind to the real E):
- **Set-up:** G-Coma membership, real fractional σ errors (sE kept), σ_obs,i := σ_law,i × exp(E_plant/2), with:
  - **onlaw:** E_plant = E_ceil;
  - **plus04:** E_plant = E_ceil + 0.4 ln 10 = E_ceil + 0.921.
  - The plant's σ_sys comes from the same variants applied to the planted σ.
- **Required:**
  - onlaw → CONSISTENT on both footings;
  - plus04 → CONTRADICTED (ABOVE) on both footings.
- **If either fails:** CONSISTENT is not available to the main run. It reads NOT DIAGNOSTIC, CONTROL-LIMITED, and the README
  states whether the limit is N or the declared systematics. CONTRADICTED is arithmetic and is unaffected.

## 8. Compute, hygiene, amendments

- One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, each under 1 GB (RSS guard at 950 MB). Nothing
  downloaded. A live 1024³ job runs beside this lane.
- **Run order:**
  - `CFG948_MODE=K`;
  - `CFG948_MODE=engine` (writes `cfg948_engine.*`);
  - `CFG948_MODE=onlaw`, then `CFG948_MODE=plus04`;
  - main.
  MUTATE and main read E_ceil from `cfg948_results_engine.json`; main reads the two MUTATE JSONs.
- **Committed outputs:** `cfg948{_K,_engine,_MUTATE_onlaw,_MUTATE_plus04,}.out` and the matching `cfg948_results*.json`.
- **Read-only lanes:** CFG933, CFG936, CFG939 (and L23, the data files) are only read or exec'd read-only. LEDGER,
  THEORY_CANONICAL, sol61_push/ and campaign_fresh_gravity_astra/ are not touched.
- **Amendments.** Any change after this commit is a dated, labelled amendment (AMENDMENT_A*.md) that says whether any number
  had been seen.
- κ = ½ FITTED; footings never pooled; not theory closed. CONTRADICTED is reported as plainly as CONSISTENT. Nothing here
  says the data favour the framework.
