# S3_v3_mw_seals FROZEN CRITERIA: batch R3 of N0_board_audit for v3 (AQUAL discs, μ = x/(1+x), EFE solved, screening)

Written 2026-10-23 and committed alone (with `ASSUMPTION_LEDGER.md`), before any script of this lane exists and before any
number of this lane is computed. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` and
`BRIEF_E_AUDIT.md`. κ = ½ is FITTED. Footings canonical a₀ = 9.3603e-11 and alt 1.1312e-10 m/s², computed and reported
separately, never pooled. No dark-matter particle. Never "theory closed"; never "the data favour the framework". Every run:
`OMP_NUM_THREADS=1 nice -n 15`, single thread, < 1 GB RSS, minutes per script. No downloads (data on disk only).

**Scope.** R3 of `rebuild_2026_10_22/N0_board_audit/AUDIT.md` (tiles 25, 43, 45, 47), MINUS lane P4's items (SPARC RAR,
tile 15; MW vertical force vs Bovy & Rix, tile 24's v3 counterpart). No P4 output exists on disk at freezing time
(`find . -name "P4*"` empty). This lane computes K_z(R, z) only as a sealed DR4 prediction (Part C); it does NOT score the
Bovy & Rix K_z data. It solves AQUAL only on the 12 + 46 galaxies of CFG493's κ routes (Part B), not the SPARC RAR set.
CFG960 and every running job are untouched. Never edited: CFG553's files, AG4e's `SEALED_N1.json`/`PREDICTIONS_HASH.txt`,
CFG571/CFG806/CFG809 files, any other lane.

**v3 (the yardstick).** `covariant_push_2026_10_22/THEORY_V3_DRAFT.md` §1–3 and N0: static limit = AQUAL
∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b with μ(x) = x/(1+x) (E2, C4), i.e. ν₁(y) = (1 + √(1 + 4/y))/2 in spherical symmetry; an
external-field effect (EFE) everywhere; screening L★ ≥ 21.7 / 22.9 pc (up to ~90 pc); BS dust with a fitted abundance and
its static μ_K²ψ term (BS24 Eq. 35; owned by batch R6). No settling, supply, ownership, round (RM) or additive-phantom rule.

## 0. Read before freezing (disclosed)

CFG532/532b/533 READMEs and `cfg532b_results.json` (RM-v / RM-φ / ALG ν_mono cells; primary Ou+Jiao RM-v canonical
Δ −0.164 ± 0.045, Z −3.63; law slopes −0.10 to −0.19; data slopes Ou −0.325, Jiao −0.319, Wang −0.356, Zhou −0.186,
Feng −0.026); CFG516 README (QUMOND in-plane force 20 % → 0.3 % below ALG at 1 → 30 kpc on a near-Kuzmin disc; fitted a₀
moves with the law definition); CFG553 criteria/README (P1–P5; NFW on Ou+24 χ² 9.872); CFG493 README and code (P1
−10.015, P2 −10.081, P3 −10.302, combined −10.107 ± 0.099, κ_Λ 0.417 ± 0.095, κ_crit 0.345 ± 0.078); AG4e README/code
and the first entries of `SEALED_N1.json`; CFG571's `predict`; addendum E (ffb14e40bc); CFG809 §3–4 (σ_Δv ≥ 0.2-dex
systematics); E2 README and `aqual_axi.py` / `aqual_fft.py`; hunt h81 output (MW external field e_N = 0.01273 canonical /
0.01054 alt, Newtonian, toward (l, b) = (268.5°, +33.0°), angle to the disc normal γ = 57.0°; QUMOND azimuthal asymmetry
0.3–1.4 % at 15–25 kpc); `gext_vectors_2026/data/gext_vectors.csv` (SPARC e_N in 1.2e-10 units) and
`prep_2026/wallaby_firing/gext_wallaby_237.csv` (WALLABY e_N per footing). No v3 MW, κ or ALMA AQUAL-disc number exists in
the record to my knowledge (N0: "no v3 run exists").

## 1. The AQUAL disc solver (one code for every part; `s3_aqual.py`)

- **Axisymmetric (R, z) finite volume**, full z range (no mirror assumption), geometric cell growth from the axis and the
  midplane (a cell is centred on z = 0), outer boundary ≥ 300 r_M. Equation: Σ_faces A_f μ(|∇Φ|_f/a₀) ΔΦ/d = 4πGρV; |∇Φ|_f
  from the normal difference ⊕ the averaged tangential central differences. Solved by Kačanov iteration (μ frozen per
  step, sparse LU) with Anderson acceleration; started from the algebraic total field. Converged when the relative
  nonlinear residual ≤ 1e-8.
- **Boundary (Dirichlet at the outer faces):** isolated: the exact spherical AQUAL potential of the total mass (deep-MOND
  quadrupole decays as r^−√3, < 1e-4 at the boundary). EFE along the disc axis (γ = 0, axisymmetric): Φ_b = g_e z +
  the linearised AQUAL far field −GM/(μ_e √(1+L₀) R̃), R̃ = r √(sin²θ + cos²θ/(1+L₀)), L₀ = dlnμ/dlnx at x_e (E2's
  form); g_e = ν₁(e_N) e_N a₀ (total external field).
- **Correction-factor convention:** every AQUAL result is used as C = g_AQUAL / [ν₁(g_N/a₀) g_N] with g_N from the SAME
  grid (μ = 1 solve), applied to the exact/record Newtonian field. Discretisation errors largely cancel in C.
- **3-D EFE at an arbitrary angle (MW only):** periodic FFT grid, g = g_N + g_e ê + δ, δ = P_L[(1 − μ(|g|))g − (1 − μ_e)g_e ê]
  (E2 `aqual_fft.py`'s fixed point, re-implemented), g_N interpolated from the fine axisymmetric Newtonian solve. Used only
  as the ratio C₃(R, φ; γ = 57°) / C₃,mean(R; γ = 0) applied to the fine axisymmetric γ = 0 solve. Internal relative
  acceleration = g − g_e ê (the centre falls with the external field).
- **Screening:** v3's stiffness acts below l_g = L★²/(2 r_M). It is computed for every object (L★ = 21.7, 22.9, 24, 90 pc)
  and the solve is unscreened when l_g < 1 % of the smallest radius used (expected: l_g ≲ 0.5 pc for the MW, ≲ 10 pc for
  the dwarfs). Stated, not solved.
- **μ_K² term:** not in any verdict (batch R6 owns it; its zero point is a per-object constant in H2/Mistele). Part A
  reports a first-order bound only: δρ = μ_K²|ψ_int|/(4πG) with μ_K = 14.8 h/Mpc (h = 0.674), ψ_int from the EFE solve
  (zero at infinity), its shell-enclosed mass added to V², and the resulting slope shift.

## 2. Part A — the Milky Way's outer rotation slope (tile 25)

- **Data (CFG532/532b, re-parsed by my own loader, same files, line ranges and error models):** Ou+24 (stat ⊕ 3 % inner /
  15 % R > 22 kpc), Eilers+19 (stat ⊕ 3 %), Wang+23 (stat ⊕ 3 %), Jiao+23 (published), Zhou+23 (stat ⊕ 3 %), Feng+26
  Cepheids (stat ⊕ 3 %), SL23 DR3+ (reported only, never combined). Radii as published (no R₀ rescale, CFG532 primary).
- **Baryons:** B1 McMillan17 (thin, thick, bulge, HI, H₂; my own transcription of CFG514's Table 3 formulae), census held
  (stars 5.43 ± 0.57e10; s* post hoc as CFG532). Variants B2 / B2b / B3 (CFG516's definitions, executed read-only):
  reported only.
- **The path, one ingredient at a time (each on both footings):**
  0. OLD: CFG532b's RM-v and RM-φ (ν_mono) cells, read from `cfg532b_results.json` (no recompute).
  1. ALG ν_mono on my Newtonian field (reproduction control A3 against CFG532b's ALG cells).
  2. KERNEL: ALG ν₁.
  3. GEOMETRY: AQUAL ν₁ disc, isolated.
  4. EFE (**the v3 cell**): AQUAL ν₁ + uniform external field, γ = 57°, e_N = h81 (0.01273 canonical / 0.01054 alt).
     Primary azimuth: the anticentre wedge (galactocentric azimuth within ±30° of the Sun–anticentre line, where the
     15–27.5 kpc tracers sit); the azimuthal mean and the exact axisymmetric γ = 0 solve are reported. e_N variants
     (reported): 0 (isolated) and 2 × h81.
  5. SCREENING: l_g numbers (no change expected).
  6. μ_K²: the first-order bound (reported only).
- **Statistics and labels (CFG532/532b frozen rules, unchanged):** per curve: χ²/N and p at census, s* and M*_need,
  slope dlnV/dlnR by CFG532's weighted estimator over 15–27.5 kpc (Cepheids 10–R_max), Δσ, verdict CONSISTENT /
  NOT DIAGNOSTIC / NEEDS-HEAVY-DISC / EXCLUDED by CFG532 §4's code path. Combined RGB/LIM slope test: one curve per group
  (APOGEE-RGB = {Ou, Eilers, Zhou} × LIM = {Jiao, Wang}), GLS of Δ = b_data − b_law at ρ = 0 and 0.5; **primary = Ou+Jiao,
  ρ = 0**; labels: NOT DIAGNOSTIC if σ̄ > |b_law + 0.5|/2, else SHAPE CONSISTENT |Z| ≤ 2, SHAPE TENSION 2 < |Z| ≤ 3,
  SHAPE EXCLUDED |Z| > 3. Cepheid class (Feng alone) the same.
- **Tile-25 reading for v3 (per footing):** the primary combined label at step 4. It is called ROBUST only if steps 4 at
  ρ = 0.5, the azimuthal mean, γ = 0 and e_N ∈ {0, 2 × h81} all give the same label; otherwise "depends on <named input>".
- **Hand expectation (before any number):** v3's 15–27.5 kpc slope −0.13 to −0.17; AQUAL moves V by ≤ 2 % there; the EFE
  steepens the slope by 0.005–0.02; primary Z −3 to −4 → SHAPE EXCLUDED on both footings, as the record (the steep DR3
  decline is not cured by v3); Cepheids SHAPE CONSISTENT or TENSION.

## 3. Part B — κ re-fit under v3's AQUAL disc law (tile 47)

- **Machinery:** CFG493's code executed read-only up to its combination section (its loaders, `arrays`, `fit1`, `boot1`,
  `build`, `gas_points`, levers, error terms); my own ν₁ versions of `fit1`/`fit3`; its GLS `combine`, `cov`, `verdict`
  and shared priors SH unchanged.
- **Steps, each reported per route and combined:** K (kernel ν_mono → ν₁) → A (AQUAL disc, isolated: the per-point
  correction C applied as g_model = C(R; a₀) ν₁(g_bar/a₀) g_bar) → E (EFE, γ = 0 axisymmetric, reported only).
  - **P1 (12 SPARC, ladder distances):** mass model per galaxy: Σ★ = Υ SBdisk (rotmod), exponential beyond the last
    point; bulge spherical from V_bul; Σ_gas from a non-negative least-squares inversion of rotmod V_gas² on hat
    functions at the rotmod radii (+ two outer nodes at 1.5 and 2 R_last, zero beyond). Thickness: primary stars
    exponential z_d = 0.1 R_disk, gas sech² z₀ = 0.1 kpc; variant razor-thin (all).
  - **P3 (46 WALLABY):** Σ_gas = CFG493's profile (1.33 He, flux correction) with its exponential tail; stars CFG493's
    exponential (M★, R_d); same thickness rule.
  - **P2 (MIGHTEE widths, committed numbers only):** kernel shift bounded on y ≤ 0.084 (N0): δL₂ = −log₁₀(ν₁/ν_mono)²
    at y = 0.084 halved, ± the same (uniform-in-y proxy); AQUAL-disc shift from C at R = 3, 4, 5 R_d of a declared
    reference deep disc (stars exponential, gas exponential R_g = 2 R_d, M_gas = 3 M★, y(3R_d) ≈ 0.05): shift = mean,
    error = half-range. Both added as P2 unique terms.
  - C(R; a₀) is computed at a₀ ∈ {4.0, 6.5, 10.5, 17.0} × 1e-11 m/s² per galaxy and interpolated linearly in log a₀
    (clamped). Galaxies, point masks and weights are CFG493's at nominal.
  - **New unique term "AQUAL geometry"** per route = |L(primary thickness) − L(razor-thin)| / 2. All other terms are
    CFG493's, with "statistics" re-bootstrapped under each step (same seeds, same resample counts).
  - **EFE step (reported, not the verdict):** P1 e_N from `gext_vectors.csv` (×1.2e-10/a₀ to each footing's units),
    P3 from `gext_wallaby_237.csv` (galaxies present there only, others listed), both brackets noclu / maxclu, C computed
    at the step-A fitted a₀; Δ log a₀ by refit; geometry γ = 0 (orientation dependence quoted from Part A's 3-D ratio).
- **Verdict:** CFG493's rule at step A on both footings (INCONSISTENT WITH ½ if the ½ pull ≥ 2; DISCRIMINATING if every
  other candidate ≥ 2; else CONSISTENT BUT NOT DISCRIMINATING). Report κ_Λ ± σ and κ_crit ± σ. "AQUAL moves κ" if
  |ΔL_combined(K→A)| ≥ 0.02 dex (≈ 0.2σ), else "AQUAL does not move κ materially".
- **Hand expectation:** kernel shift −0.03 to 0.00 dex per route (ν₁ ≥ ν_mono); AQUAL shift within ±0.03 dex; κ_Λ in
  0.37–0.46; CONSISTENT BUT NOT DISCRIMINATING on the canonical footing.

## 4. Part C — sealed Gaia DR4 Milky Way predictions for v3 (tile 45), committed before 2026-12-02

- New files only, in this lane: `SEALED_V3_MW_DR4.json` (deterministic: no timestamps or run times),
  `PREDICTIONS_V3_HASH.txt` (its SHA-256), `PREDICTIONS_V3.md` (tables from the JSON). Labelled "v3" throughout. CFG553 is
  never edited; it stays the record's sealed old-model set.
- **Models:** v3 = AQUAL ν₁ on B1 census baryons with the EFE of §2 step 4 (primary, e_N = h81, γ = 57°), and the
  isolated v3 (e_N = 0) as a sealed variant. Census band: stars × s, s ∈ {s−, (s− + 1)/2, 1, (1 + s+)/2, s+},
  s± = 1 ± 0.57/5.43, gas held (CFG553 §2). B2 / B2b / B3 reported as an envelope only. Rival: B1 Newtonian + a spherical
  NFW fitted to Ou+24 (CFG553's NFW, refitted by my code; footing-independent). CFG553's sealed rows are quoted, not
  recomputed.
- **Predictions (both footings, every s):** P1 K_z(R, |z|)/(2πG) at R = 5, …, 16 kpc × |z| = 0.5, 1.1, 2.0 kpc and the
  midplane ν_z² (CFG553 convention); P2 V_c(R) at R = 5, …, 27 kpc (anticentre wedge, azimuthal mean, γ = 0) and the
  15–22 and 15–27.5 kpc slopes (CFG553's even-grid estimator); P3 at R₀ = 8.122 kpc: the dynamical-minus-baryon
  ("phantom") density at (R₀, 0) and its shell average, K_z(R₀, 1.1)/(2πG), the true column Σ(|z| < 1.1) = ∫∇²Φ/(4πG) dz,
  the Oort limit; P4 σ_z(R, 0) for isothermal exponential tracers h = 0.30 and 0.90 kpc (σ_z² = ∫₀^∞ e^(−z/h) K_z dz);
  P5 V_c at 30, 40, 50, 60 kpc and the 30–60 kpc mean (in-plane azimuthal mean, anticentre wedge, and the spherical
  equivalent √(GM_dyn(<r)/r) from Gauss flux); **P6 (new, v3-specific):** the EFE azimuthal asymmetry of V_c in the
  plane, A(R) = 2(V_max − V_min)/(V_max + V_min) over azimuth, and the azimuths of V_max / V_min, at R = 15, 20, 25,
  30, 40, 50, 60 kpc (isolated v3 predicts A = 0 exactly).
- **Decision rules after DR4: CFG553 §4–§5 adopted verbatim** with "framework band F" = the v3 census band (primary EFE),
  rival R = the NFW census band; scalar and vector rules, robustness requirements, required precisions and systematics
  propagation as there. P6 is scored as a scalar per radius (F = the v3 band, rival = 0).
- The JSON also carries the inputs' identifiers (e_N, γ, R₀, grid, code commit is added in the README, not in the JSON).

## 5. Part D — ALMA U4_27928 (2026-11-06) and GS4_24110 (2026-11-28) disc reading for v3 (tile 43), committed before 2026-11-06

- **Algebraic reading (AG4e = CFG571's head with ν₁):** reproduced by my own implementation (control D1).
- **AQUAL-disc reading:** the same discs (razor-thin Freeman stars M★, R_d; razor-thin exponential gas M_gas, R_g ∈ {R_d,
  1.5 R_d}), the same radius (GS4 R_e = 7.39 kpc, V_c 206; U4 R = 2 R_e, the sealed V_c grid 150…300), the same a₀(z)
  branch ratios (read from `SEALED_N1.json`), both footings. The requirement M_gas,req,AQ solves C(R; M_gas) ν₁(g_N/a₀) g_N =
  V_c²/R with exact Bessel g_N, iterating C to |Δ log M_gas| ≤ 0.002. FLOOR if stars alone give AQUAL V_c ≥ V_c. Reported:
  log M_gas,req,AQ, log V²_bar,req,AQ R/G (Newtonian in-plane of the required configuration, the plan's Δ_v convention),
  and Δ vs AG4e per cell. Variant (reported only): both discs sech² with z₀ = 0.15 R_d. EFE: no external field estimate
  for these discs is on disk → isolated (stated). Screening: l_g computed (no effect).
- **Decision (frozen):** "AG4e IS v3's ALMA reading" iff, on the razor-thin primary, every non-FLOOR cell has
  |Δ log V²_bar,req| ≤ 0.01 dex and |Δ log M_gas,req| ≤ 0.03 dex and no FLOOR flag flips. Otherwise "v3 NEEDS ADDENDUM F":
  `ADDENDUM_F_DRAFT.md` is written in this lane only (scoring the AQUAL-disc requirement as a labelled parallel reading by
  addendum E's rules), for the coordinator to file with owner approval. In both cases the AQUAL-disc reading is sealed
  here: `SEALED_V3_ALMA_AQUAL.json` + `ALMA_V3_HASH.txt`, committed before 2026-11-06.
- **Hand expectation:** AQUAL moves g at R ≈ 1.7–3.4 R_d by 1–4 %, so log M_gas,req by 0.02–0.10 dex in non-FLOOR cells →
  likely "NEEDS ADDENDUM F"; FLOOR flags unchanged.

## 6. Checks (each script prints one line per check; the lane script aggregates; exit 0 iff all pass)

- **A1** data: row counts (Ou 37, Eilers 38, Wang 19, Jiao 18, Zhou 34, Feng 12, SL23 45) and every data slope equal to
  `cfg532b_results.json` to 1e-9.
- **A2** Newtonian: (i) razor-thin Freeman disc on the solver grid vs the Bessel formula, max |ΔV²|/V² ≤ 0.5 % on
  R ∈ [0.5, 15] R_d; (ii) my B1 in-plane Newtonian V vs CFG532's `v_model("N")` (executed read-only) ≤ 1 % on 5–27.5 kpc.
- **A3** reproduction: my ALG ν_mono census law slope per curve within 0.003 of CFG532b's ALG cell, χ² within 3 %.
- **A4** AQUAL solver: (i) Plummer sphere: AQUAL = ν₁ algebraic ≤ 0.3 % on 0.3–30 b; (ii) Kuzmin disc: in-plane AQUAL =
  ν₁(g_N)g_N ≤ 0.5 % on R ∈ [0.3, 20] a (Brada–Milgrom identity); (iii) EFE along z: Plummer b = 0.01 r_M at y_e = 0.1
  vs E2's `aqual_axi` point mass, equatorial g_R at r = 0.5, 1, 2, 4 r_M agree ≤ 1 %; (iv) MW grid refinement changes
  V(15–27.5 kpc) by ≤ 0.3 % and the slope by ≤ 0.003; (v) residual ≤ 1e-8.
- **A5** 3-D: (i) N = 128 vs 160 (same box) ratio change ≤ 0.5 % on 15–60 kpc; (ii) 3-D γ = 0 azimuthal mean vs the
  axisymmetric γ = 0 solve ≤ 3 % on 15–60 kpc; (iii) γ = 0 azimuthal variation ≤ 0.3 %.
- **A6** slope estimator: Kepler −0.5 and flat 0 exactly (1e-6).
- **A7** law on: v3 V(20 kpc) ≥ 170 km/s on both footings (Newton gives ~120).
- **B1** CFG493 reproduced with ν_mono: L1, L2, L3, combined L and σ to 1e-6 dex.
- **B2** P1 gas inversion: rotmod V_gas² reproduced at P1's points with rms ≤ 3 % of V_bar²; my Newtonian V_bar² vs
  rotmod's, median |Δ| ≤ 5 %.
- **B3** P3 Newtonian: my grid V_gas² vs CFG493's `v2_disc`, median |Δ| ≤ 2 % at the gas points.
- **B4** C interpolation in a₀: direct vs interpolated at the fitted a₀ ≤ 0.3 % (5 galaxies per route).
- **B5** GLS weights sum to 1 (1e-12).
- **C1** two independent runs of the seal script give byte-identical JSON (checked by re-running; the second run's hash
  is printed).
- **C2** my NFW fit to Ou+24 on my B1 Newtonian field: χ² within 3 % of 9.872 (CFG553).
- **C3** Jeans integrator: uniform K_z → σ² = K h to 0.1 %.
- **C4** the seal's P2 V_c(20 kpc) and slopes equal Part A's v3 cell exactly.
- **D1** my algebraic ν₁ implementation reproduces every `SEALED_N1.json` logVbar2R_G and logMgas (≤ 1e-6 dex) and every
  FLOOR flag.
- **D2** razor-thin Freeman on the ALMA grid ≤ 0.3 % on R ∈ [0.5, 5] R_d. **D3** Kuzmin AQUAL identity on the ALMA grid
  ≤ 0.5 %. **D4** requirement iterations converged (≤ 0.002 dex). **D5** grid refinement moves a representative
  log M_gas,req,AQ by ≤ 0.005 dex.
- **MUTATE** (`S3_MUTATE=1` or `--mutate`; outputs `*_MUTATE.out`, `*_results_MUTATE.json`; nothing is sealed): μ ≡ 1
  (Newton) inside the AQUAL solver. A7 must FAIL (V(20) ≈ 120 km/s); D's AQUAL requirement must leave the algebraic ν₁
  requirement by > 0.3 dex (check D6, which must FAIL under mutate). Also, as CFG532b M3: a Keplerian tail injected beyond
  15 kpc must give primary |Z| > 3 at the v3 cell (DETECTED line, not a check).

## 7. What would change the reading

A failure of A2–A5 or D1–D3 stops the dependent part (disclosed; no number from it is used). A post-result change of any
rule is an append-only AMENDMENT, marked pre- or post-result. A fail is checked as hard as a pass: if v3 cures the MW slope,
the cure must be traced to a named ingredient (kernel, geometry or EFE) with its size; if it does not, the tension is
reported as v3's own.

## AMENDMENT A1 (2026-10-23, PRE-RESULT: solver development only; no MW, κ, seal or ALMA number of this lane exists yet)

**A4(ii) and D3 were mis-specified.** The Brada–Milgrom Kuzmin identity is not "in-plane AQUAL = ν₁(g_N,R) g_N,R". Above a
Kuzmin disc the Newtonian field is a point mass's at (0, 0, −a), so AQUAL's exact solution is that point mass's spherical
AQUAL field, and in the plane g_R(R, 0) = ν₁(|g_N(R, 0⁺)|/a₀) g_N,R(R, 0) with |g_N(0⁺)| = GM/(R² + a²), the FULL field
magnitude just off the plane (it includes the vertical 2πGΣ-type component). Corrected checks (same tolerances):
- **A4(ii)/D3:** in-plane AQUAL vs ν₁(GM/(R² + a²)/a₀) · GMR/(R² + a²)^{3/2} ≤ 0.5 % on R ∈ [0.3, 20] a, AND the off-plane field
  magnitude at z = 0.5 a vs the point-mass AQUAL value ≤ 0.5 %.
- Reported alongside (not a check): the in-plane AQUAL / in-plane-algebraic ratio on the Kuzmin disc (it is −11.7 % at
  R = 0.3 a for y ≈ 4 at that radius), which is the size of the "geometry" ingredient this lane measures.
- Solver default tolerance set to the frozen 1e-8 relative residual (a round-off floor near 4e-9 makes 1e-9 unreachable).
Nothing else changes.

## AMENDMENT A2 (2026-10-23, PRE-RESULT: solver and bookkeeping only; still no MW, κ, seal or ALMA number of this lane)

1. **Round-off floor.** With a large dynamic range (cells 0.0005–3000 kpc) or a uniform external flux the relative residual
   stalls near 1e-8–5e-8 (round-off). A solve is converged when the residual ≤ 1e-8, OR it has stalled for 10 iterations at
   ≤ 1e-7 (flagged "floor" and counted in A4(v)).
2. **EFE numerics.** The uniform external field is carried analytically: Φ = φ + g_e z, with g_e added to every z-gradient
   used in μ and the uniform part's flux added per cell. Same equation and boundary physics as §1; only the round-off
   changes. E2 cross-check (A4(iii)) unchanged.
3. **3-D stop rule.** Plain fixed point (Anderson raised RSS to 0.8 GB for no gain), float32 storage; stop when the in-plane
   radial fields at 15, 27.5 and 60 kpc (8 azimuths) change by < 2e-6 (relative) for 5 consecutive iterations.
   The 3-D ratio is also tabulated at 5–12.5 kpc so the χ² over each whole curve uses the EFE model (W → 1 inside).
4. **Bookkeeping.** B2 / B2b / B3 densities are transcribed from CFG516 (checked identical to CFG516's functions by
   evaluation, A2(ii)) instead of executed. C(R; s) is tabulated on s ∈ {0.25, 0.5, 0.75, s±, (s± + 1)/2, 1, 1.3, 1.6, 2, 3, 4}
   and interpolated linearly in ln s; the 3-D ratio W is computed at s = 1 and applied at every s (s* only). The e_N = 2 × h81
   variant uses its own solve at s = 1 (census) and h81's C for s* (reported variant only). Solver controls A4(i)–(iii) run
   with the true μ in both modes (they validate the code, not the mutate). A4(i)'s Plummer grid resolves b by 20 cells.

## AMENDMENT A3 (2026-10-23, POST-RESULT for Part A; PRE-RESULT for Parts B, C, D)

Seen before writing this: Part A's development run (13/14 checks; A5iii FAILED, 3-D γ = 0 azimuthal variation 0.63 % > 0.3 %,
largest at 5–12.5 kpc and 0.59 % at 17.5 kpc; every step SHAPE EXCLUDED, v3 Z −4.37 / −4.61; that run's parent RSS peaked at
1.74 GB because the fine-grid solves ran in-process before the child-process presolve was wired — disclosed; numerics unaffected).

1. **As frozen (§7), A5iii's failure removes the γ = 57° 3-D cells (AQ_v3, AQ_v3_mean, AQ_v3_2x) from Part A's reading.** The
   EFE cell of the reading becomes the exact axisymmetric γ = 0 solve (AQ_gamma0); its robustness set is {ρ = 0.5, isolated,
   e_N = 2 × h81 at γ = 0}. The 3-D cells stay in the output, labelled "A5iii failed".
2. **Post-result diagnostic (reported):** a Plummer sphere (M 6.6e10, b 3 kpc) in the record's field tilted 57° from the grid
   axis has an exact solution (my axisymmetric solver about the field axis). Its in-plane radial field varies with azimuth by
   4.3 / 9.7 / 15.8 % (peak-to-peak / mean) at 15 / 27.5 / 60 kpc, and the 3-D solver reproduces this (4.5 / 9.6 / 15.3 %, N 160,
   box 640 kpc). The large m = 1 pattern is physical AQUAL, not a grid artifact; the record's QUMOND linear-response estimate
   (hunt h81: |A| 0.3–1.4 % at 15–25 kpc) is several times smaller.
3. **Part C's 3-D estimator (decided before any Part C number):** pointwise ratio V²(R, φ) = V²_axi,γ0(R) × F₃(R, φ; 57°) /
   F₃(R, φ; 0) (N 160, box 640 kpc; cancels the grid's azimuthal artifact present in both runs). New check **C5:** on the tilted
   Plummer reference the pointwise estimator reproduces the exact 57° in-plane F_R to ≤ 1 % at every sampled (R, φ) on
   15–60 kpc and its peak-to-peak variation to ≤ 0.5 % absolute. If C5 fails, the seal's primary is the exact γ = 0 solve and
   the 3-D numbers (anticentre wedge, P6) are sealed as "unvalidated".
4. **RSS:** every AQUAL solve now runs in a short-lived child process (parent and child peaks are reported in each results JSON).

## AMENDMENT A4 (2026-10-23, PRE-RESULT for κ: no κ, route or combined number of Part B computed yet; per-galaxy C diagnostics seen)

1. **Gas inversion basis (§3 P1).** The frozen node set (rotmod radii + free nodes at 1.5 and 2 R_last) is degenerate: mass in the
   unconstrained outer nodes barely changes V² inside, so NNLS did not converge and a bounded solve put 4.7e9 M☉ of gas into
   NGC3109's outer nodes (SPARC M_HI ≈ 5e8). Replaced by one hat per rotmod radius, flat inside R_1, the last hat declining
   linearly to zero at 1.5 R_last; bounded-variable least squares with a 1e-6 relative ridge (minimum-norm among equal fits).
   NGC3109 then has 4.6e8 M☉. The inversion gas mass / (1.33 M_HI,SPARC f²) is reported per galaxy.
2. **New unique error term "outer gas extent"** per route (P1, P3) = |L(gas to 1.5 R_last) − L(gas to 2 R_last)| / 2 (P1: the
   last hat reaches zero at 2 R_last; P3: CFG493's exponential tail cut at 2 instead of 1.5 r_last). Reason: the development
   diagnostics showed C at the outermost points moving by up to ~10 % with the outer gas (NGC3741, UGC05829), the size of the
   effect being measured. Primary stays 1.5 (CFG493's own P3 tail).
3. B2's tolerances unchanged. Nothing else changes.
