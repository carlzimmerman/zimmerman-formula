# P4_v3_galaxy_tiles — FROZEN CRITERIA (committed alone, before any script or number of this lane)

Lane `rebuild_2026_10_22/P4_v3_galaxy_tiles/`. Written 2026-10-23. Rules: `rebuild_2026_10_22/BRIEF.md`,
`doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) and
1.1312e-10 m/s² (alt; FP0 full precision, `CFG4_common.A0`), scored separately, never pooled. No dark-matter particle.
Never "theory closed"; never "the data favour the framework".

## 0. The owner's rule and what is computed

Every galaxy-column tile is recomputed for **v3** (`covariant_push_2026_10_22/THEORY_V3_DRAFT.md`) in its static weak-field
limit, on **baryons only**:

- field equation: AQUAL, ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b, **μ(x) = x/(1+x) exactly** (E2, C4). Not ν_RAR, ν_mono, ν_e or QUMOND;
- **external field solved, not added**: a uniform field g_e imposed as the boundary condition (Φ → g_e z + the linearised
  far field), the full nonlinear equation solved inside;
- **screening**: the C4-literal stiffened form (γ_F = 0, the D10 equations): ∇²Φ = 4πGρ_b + ∇·p, χ = Φ + (L★²/2)∇·p(∇χ),
  p(v) = v/(1+|v|) (a₀ = 1 units). L★ = **24 and 90 pc** (bracket; D10 floor 21.7 / 22.9 pc). L★ = 0 (plain AQUAL) is
  reported as the unscreened limit;
- **no settling, supply, catchment, census-edge, ownership, capture or round rules**; no cold-energy halo. v3's BS dust is
  taken to contribute nothing inside galaxies (NOT DERIVED; F1). **Not included: BS24 Eq. 35's μ_K²ψ term** (N0 audit
  item 2; batch R6 owns it). This is stated on every tile.

Solver (written in this lane, `p4_solver.py`): axisymmetric finite volume on (ln r, θ), uniform g_e along the axis, Newton with
the exact sparse Jacobian (one field Φ at L★ = 0; two fields Φ, χ at L★ > 0). Outer boundary (Dirichlet): with g_e > 0,
Φ_b = g_e z − GM/(μ_e√(1+L_e)) / √(r_⊥² + z²/(1+L_e)), L_e = dlnμ/dlnx at x_e = 1/(1+x_e), at r_out ≥ 300 max(r_data, r_e),
r_e = √(GMa₀)/g_e; with g_e = 0, the spherical law's potential for the total mass. Inner boundary zero flux at r_in, with
M(<r_in) added to the innermost ring. External field from an environment's Newtonian field g_Ne: g_e μ(g_e/a₀) = g_Ne (the
environment's own AQUAL field taken spherical: declared approximation). Rotation/RAR observables use the **orientation
average** (sphere average) of −∂Φ/∂r; brackets: the ring perpendicular to ê (θ = π/2) and the great circle containing ê.

## 1. Checks (script `p4_v3_galaxy_tiles.py`; one line per check, `K# PASS value threshold`; exit 0 iff all pass)

| id | check | pass line |
|---|---|---|
| K1 | isolated Plummer, L★ = 0: sphere-averaged g vs the exact spherical law ν₁(g_N/a₀)g_N, ν₁ = ½ + √(¼ + 1/y), r = 0.1–30 a, y = GM/(a²a₀) ∈ {0.03, 1, 30} | max rel. dev ≤ 0.5 % |
| K2 | linear EFE (y = 1e-4 point-like Plummer in x_e = 0.3): field along / across ê vs 1/μ_e and 1/(μ_e√(1+L_e)) | ≤ 1.5 % |
| K3 | grid convergence: production grid vs (1.5× nper, 1.5× N_θ) on 5 SPARC EFE galaxies, the 6 TDGs and DF2/DF4 at L★ = 0 and 90 pc | max |Δ log g| ≤ 0.003 dex |
| K4 | cross-check against the record's independent screened solver (D10 `d10_solver.Solver2D`, read-only import): Plummer y = 0.5, x_e = 0.1, Λ = 0 and Λ = 0.2 a, monopole g at r = 0.5, 1, 2, 4 a | ≤ 1 % |
| K5 | data identity: own SPARC loader == `CFG4_common.load_sparc` arrays (bit-for-bit); CFG695 S2 reproduced (0.1009 @ 0.60 / 0.0994 @ 0.55) | |Δrms| ≤ 1e-4, Υ equal |
| K6 | MeerKAT: 47 survivors; CFG301 pooled s★ (ν_mono, k = 1) 1.117 and CFG309 REST a₀ 1.311e-10 (k = 0); CC2 SPARC closure 1.304 | rel. ≤ 2e-3 |
| K7 | groups: CFG540's law-without-edge class means (ν_mono, rounded footings 9.36e-11 / 1.13e-10) +0.010 / −0.010 | ≤ 0.002 dex |
| K8 | MW: grid baryon mass of McMillan17 vs direct integral ≤ 2 %; Newtonian K_z(R₀, 1.1)/2πG vs direct column ≤ 3 %; AQUAL disc far field (v_c at 40–60 kpc) vs spherical law ≤ 2 %; own NFW comparator χ²(K_z) within ±2 of CFG514's 43.7 | as stated |
| K9 | TDG / DF2-DF4 data: CFG936's law residual means with ν_e (−0.690 / −0.728 dex) and CFG933's E_obs (DF2 −1.709, DF4 −2.170) | ≤ 1e-3 |
| K10 | Chae 2021 environment names all found in SPARC; count reported | 100 % matched |
| K11 | peak RSS | < 1 GB |

**`--mutate`:** the solver's μ is replaced by the standard μ = x/√(1+x²); K1 and K2 (which compare with μ = x/(1+x)) must
FAIL. Runs the validation checks only; writes `p4_v3_galaxy_tiles_MUTATE.out`, `_results_MUTATE.json`; exit 1.

## 2. Tiles: old line, v3 computation, frozen line, ladder

Tile class rule (all tiles): **PASS** iff the tile line passes on both footings at both L★ = 24 and 90 pc; **FAIL** iff it
fails on both footings at both L★; otherwise **COND** (the split is named). Qualifier **FRAGILE** if a declared variant
changes the class, else **ROBUST**. L★ = 0 is reported, not scored. Each tile reports the **ladder**: the statistic after each
change, one at a time (old kernel → μ = x/(1+x) → geometry → rules removed → EFE solved → screening).

### T1 Rotation curves (SPARC RAR). Old: PASS, CFG695 (0.1009 / 0.0994 dex, global Υ, algebraic simple law) + CFG919 (ν_e)

- Data: 175 rotmod files + `SPARC_Lelli2016c.mrt`; all galaxies, all points with g_bar, g_obs > 0 (CFG695's mask).
  V_bar² = sign(V_gas)V_gas² + Υ V_disk² + 1.4 Υ V_bul² (CFG4 convention).
- **Geometry: spherical approximation** (M(<r) = rV_bar²/G; V_bar² linear in r between points, uniform core inside the first
  point, constant mass beyond the last). For isolated spherical sources AQUAL equals the algebraic law exactly.
- **One Υ per galaxy**, flat prior on [0.30, 1.20] (CFG695's declared scan range), chosen by minimising the galaxy's
  χ² (below). For EFE galaxies the solve runs at Υ nodes {0.30, 0.40, 0.50, 0.60, 0.75, 0.90, 1.05, 1.20} and log g is
  interpolated linearly in log Υ (fit grid step 0.01). Variant: CFG8/Chae lognormal prior (Υ_d 0.5, 0.1 dex).
- **EFE:** Chae 2021 Table 3 environmental Newtonian field (`real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv`),
  primary log e_N = mean of maxclu and noclu (as CFG8), g_Ne = e_N × 1.2e-10; brackets maxclu, noclu (solved at the primary
  best-fit Υ). Galaxies without an estimate: isolated (g_e = 0), counted and flagged.
- **Screening:** L★ = 24, 90 pc solved per galaxy on the same Υ node grid. Declared fallback if the budget is exceeded: hold Υ
  at the L★ = 0 fit (disclosed if used).
- Statistic 1 (old line): CFG4 weighted rms of log₁₀(g_obs/g_pred), w = (V/eV)² (eV, V clipped ≥ 1 km/s), per-galaxy Υ.
  **Line: rms ≤ 0.110 dex and median per-galaxy Υ in [0.50, 0.80], each footing.** This sets the tile class.
- Statistic 2 (χ², line frozen now from the data's errors): per galaxy χ² = rᵀC⁻¹r in log g, C = diag(σᵢ²) + s²11ᵀ,
  σᵢ = 2eVᵢ/(Vᵢ ln10), s² = (e_D/D ln10)² + (2 cot i · e_i/ln10)² (SPARC Table 1 distance and inclination errors; a common
  offset per galaxy); dof = N − 1; Υ refit by this χ². **Line: ≥ 90 % of galaxies have p ≥ 0.001 → χ² PASS; 75–90 % →
  χ² MARGINAL; < 75 % → χ² FAIL.** Reported alongside the class (it can add a caveat, not change the class). Reported: total
  χ²/dof, Δχ² against the same fit with ν_mono, Q ≤ 2 subset, SPARC small (M_b ≤ 3e9) / large mean residual at the old global Υ.
- Diagnostic D1 (no class weight): thin-disc AQUAL vs spherical approximation for exponential stellar discs spanning the
  SPARC central surface densities (log Σ₀ = 1.5–3.5 M☉/pc²): median in-plane Δ log g over R = 0.5–6 R_d.
- Ladder: CFG695 reproduction → per-galaxy Υ (isolated) → EFE solved → L★ 24 / 90.

### T2 Local a₀ from MeerKAT. Old: PASS, CFG301 1.046e-10 (OBS frame, ν_mono) / CFG309 1.311e-10 (REST)

- Data and chain exactly CFG301's (frozen cut, 47 survivors; W_c = W50/(1+z)^k; V = W_c/2 sin i; M_b = 1.33 M_HI + M★;
  R = D_HI/2 from the size relation; point mass inside R). **REST frame (k = 0) primary** (CFG309's decision); OBS (k = 1)
  reported. Estimator: CFG223's median-residual s★ (root of median log₁₀[D/ν(g_bar/a₀s)] = 0), re-implemented here, with
  **ν₁** (= v3's isolated AQUAL, exact for a point mass); bootstrap B = 4000 over galaxies (seed 4402).
- SPARC same-recipe closure under v3 (CC2's 123 galaxies: Q ≤ 2, i ≥ 30°, V_flat > 0, M_HI > 0; M_b = 1.33 M_HI + 0.5 L[3.6]).
- EFE: no environment estimate on disk for these galaxies → isolated (stated). Screening: one 1-D solve at the median
  survivor (L★ 24 / 90 pc) reports the shift in g at R.
- **Line: |log₁₀(a₀,MIGHTEE / a₀,SPARC-recipe)| ≤ 0.15 dex (CFG301's CC2 tolerance), REST frame, under v3.** Reported: a₀
  with 68 / 95 % intervals, offsets from both footings, the OBS row. (a₀ is footing-independent; the line is evaluated once and
  holds or fails for both footings alike.)
- Ladder: CFG301 / 309 reproduction → ν_mono → ν₁ (both frames) → screening.

### T3 Galaxy groups (BFJR). Old: PASS, CFG543 "consistent supply closes" (P2 +0.060 / +0.043 dex)

- Data: Tian+2026 (`_external_data/vizier2026/J_A_A_710_L39.tsv`, outside git), the 63 "Galaxy group" rows.
- v3: Hernquist baryons (catalogue Re = projected half-mass radius, R_e = 1.8153 a; CFG540 primary), mass = catalogue M_bar
  (stars + observed hot gas, CFG543 addendum), isolated AQUAL with μ = x/(1+x) (exact for a sphere), whole-system aperture
  σ² = ⟨r·g⟩/3. **No edge, no supply.**
- Statistic and **line (CFG540's frozen rule):** Δᵢ = log σ_obs − log σ_v3; class mean, SE = sd/√N, σ_sys = s̄ × 0.10 dex
  (s = dlogσ/dlogM_b), Z = Δ̄/√(SE² + σ_sys²). **PASS iff CONSISTENT (|Z| < 2, σ_tot ≤ 0.045); ABOVE / BELOW (|Z| ≥ 2) = FAIL.**
- EFE: no group environment estimate on disk → isolated primary. Reported sensitivity (no class weight): uniform g_e/a₀ =
  0.01 and 0.03 (declared round values) solved for every group (virial σ in the internal field).
- Screening: one representative group (median M_bar, Re) solved at L★ 24 / 90 pc; the shift is reported.
- Variants (FRAGILE test): aperture R < Re (β = 0 Jeans, the paper's definition) and Re → Re/k, k ∈ {1.126, 1.563, 2.224,
  2.767} (CFG543 addendum).
- Ladder: CFG540 no-edge reproduction (ν_mono) → ν₁ → EFE sensitivity → screening.

### T4 MW vertical force. Old: PASS, CFG516 "round rule beats the MOND phantom disc 32/32"

- Data: Bovy & Rix 2013 Table 3 (43 MAPs, K_z,1.1/2πG at R_tab + 0.122 kpc; σ ⊕ 5 %: CFG514's primary statistic); Eilers+19
  rotation curve (σ = stat ⊕ 2 %).
- Baryons: **B1 McMillan17 (primary)**, B2 L172 6.0e10, B2b 7.3e10, B3 short disc 2.15 kpc (CFG516's definitions).
- v3: full axisymmetric **AQUAL disc solve** (no round rule, no phantom-disc recipe), F0 (baryon amplitude A = 1) primary; FA
  (A fitted to Eilers by v3's own v_c, L★ = 0) reported. L★ 24 / 90 pc solved for F0 and FA. EFE: no MW external-field
  estimate on disk → g_e = 0 primary; reported sensitivity g_e/a₀ = 0.03 along the disc axis (declared round value).
- **Line (frozen now, from the data's errors): χ²(K_z, 43 MAPs, σ ⊕ 5 %) ≤ χ²₀.₉₉(43) on B1, F0, each footing.**
  Reported: K_z,1.1(R₀) vs 66.4 ± 2.2, the K_z scale length, χ²_RC, and Δχ² against this lane's own NFW comparator
  (Newtonian B1 + NFW fitted to Eilers; a fitted halo, not ΛCDM-calibrated; comparator only). FRAGILE if FA, B2, B2b or B3
  changes the class.
- Ladder: record's Newtonian numbers reproduced → AQUAL disc (L★ = 0) → L★ 24 / 90 → FA → other baryon models → EFE bracket.

### T5 Tidal dwarfs and NGC 1052-DF2/DF4. Old: COND, CFG936 route (i) "at Newton if they captured no cold energy"

- v3 has no capture/supply rule: the law acts on all baryons; the only route below the isolated law is the host's field.
- **Class T** (6 Lelli+15 TDGs, `real_research/data/tidal_dwarfs/lelli2015_tdg.csv`): uniform sphere of radius R_out and mass
  M_bar (keeps the record's g_bar = GM_bar/R_out²); host = point mass 0.6 L_K at D_p (CFG936): g_Ne = G M_h/D_p²; prediction
  g at R_out (sphere average); Δ = log₁₀(g_obs/g_pred); σ from V, M, R errors (numerical derivatives through the solve).
- **Class U** (DF2, DF4; `campaign_fresh_gravity/CFG657_trail_capture_rule/cfg657_capture.py` GAL/HOSTS, parsed read-only):
  Plummer sphere of stellar mass Ms with 3-D half-mass radius r½ = (4/3)Re (CFG933's estimator); hosts NGC 1052 (1e11 M☉) and
  NGC 1035 (5e9 M☉) at projected separations (D = 20 Mpc), **g_Ne = |vector sum|** of their Newtonian fields (primary);
  σ_pred² = r½⟨g_r(r½)⟩/3 (the sealed estimator's form with the solved field); E = 2 ln(σ/σ_law,iso), residual
  r = E_obs − E_pred, sE = 2e/σ_obs (CFG936 `u_point`).
- **Line (CFG936 §5.1 class rule):** stats r̄, se = max(sd/√n, √Σs²/n), χ² = Σ(r/s)², p = χ²_sf(n). **EXPLAINS** iff
  |r̄| < 2 se and p ≥ 0.05; **PARTIAL** iff |r̄| ≤ ½|r̄_law| (r̄_law: v3's isolated law, same units); else **FAILS**.
  Tile: PASS iff T and U both EXPLAIN (each footing, each L★); FAIL iff T or U FAILS on both footings at both L★; else COND.
- Variants (FRAGILE test): T: Plummer profile (a = R_out/2), orientation brackets, host mass ×½ / ×2; U: scalar-sum field
  (CFG936's generous form), host corners Mg 5e10 / 3e11, M35 3e9 / 1e10, global-virial σ.
- Ladder: CFG936 law residuals (ν_e) reproduced → ν₁ isolated → EFE solved → L★ 24 / 90.

## 3. Input ledger (verdict inputs of the old tiles and of this rebuild)

| input | class | source | used by |
|---|---|---|---|
| SPARC V_obs, eV, R; V_gas | RAW | `real_research/data/sparc_data/*_rotmod.dat` | T1 |
| SPARC V_disk, V_bul (3.6 μm decompositions), Υ range, 1.4 bulge factor | SURVEY-CALIBRATION (SPS / photometry) | rotmod; CFG4; CFG695 | T1 |
| SPARC D, e_D, i, e_i, L[3.6], M_HI, V_flat, Q | SURVEY-CALIBRATION (Hubble-flow distances at SPARC's H₀ = 73 for some) | `SPARC_Lelli2016c.mrt` | T1, T2 (CC2) |
| Chae 2021 e_N (maxclu / noclu) | SURVEY-CALIBRATION (environment baryon census, Newtonian) | `laneB_data/chae21_env.csv` | T1 EFE |
| g_e from g_Ne via the spherical law | FRAMEWORK-NATIVE (approximation: spherical environment) | this lane | T1, T5 |
| MIGHTEE W50, i, M_HI, z, flags | RAW | `data_assembly/mightee_hi_catalogue_2026-10-02/` | T2 |
| MIGHTEE M★ (BAGPIPES), D_HI size relation | SURVEY-CALIBRATION | same; CFG301 | T2 |
| MIGHTEE D_L (flat ΛCDM, H₀ = 70) | ΛCDM-PROCESSED (soft at z ≤ 0.093; CFG301's H₀ = 67.4 knob 0.036 dex; native H₀ 67.2–68.6) | catalogue | T2 |
| velocity frame (REST) | documentary decision | CFG309 | T2 |
| Tian+2026 σ (member biweight), Re (mean projected member radius) | RAW (catalogue) | `_external_data/vizier2026/` | T3 |
| Tian+2026 M_bar (K-band Kroupa M/L + X-ray gas) | SURVEY-CALIBRATION | same; CFG543 addendum | T3 |
| Hernquist / Plummer / uniform-sphere profiles, mass follows light, Jeans β | model assumption (declared) | CFG540 / CFG933 / CFG931 | T3, T5 |
| Bovy & Rix K_z,1.1 | SURVEY-CALIBRATION (dynamical model outputs of MAP fits) | `mw_kz11_bovyrix2013_table3.tsv` | T4 |
| Eilers+19 v_c | RAW + Jeans modelling | `mw_rc_eilers2019_table1.tsv` | T4 |
| McMillan17 baryons | SURVEY-CALIBRATION; **partly ΛCDM-PROCESSED** (fitted jointly with an NFW halo) | CFG514 | T4 |
| B2 / B2b / B3 baryons | SURVEY-CALIBRATION (L172 shapes; B3 recalled R_d) | CFG516 | T4 |
| NFW comparator | comparator only (fitted halo); never a verdict input | this lane | T4 |
| Lelli+15 TDG V_circ, R_out, M_bar, L_K, D_p (projected) | RAW + SURVEY-CALIBRATION | `tidal_dwarfs/lelli2015_tdg.csv` | T5 |
| DF2/DF4 σ, Ms, Re, positions, D = 20 Mpc, host masses | RAW (σ, Re, positions) + SURVEY-CALIBRATION (Ms, D, host M) | CFG655 / CFG657 GAL; CFG936 | T5 |
| a₀ (κ = ½), L★ ∈ {24, 90} pc | FITTED | FP0; D10 | all |
| v3 static field equation + stiffness | FRAMEWORK-NATIVE | E2, C4, D10 | all |
| **Old-verdict ingredients removed here** | | | |
| ν_mono, ν_e (ν_e = the exponential RAR shape) kernels | ν_mono FRAMEWORK (old); ν_e STANDARD-MOND-MACHINERY (reference shape) | CFG301, CFG540, CFG516, CFG919, CFG936 | T1–T5 old |
| algebraic law applied to discs | approximation (geometry) | CFG695 | T1 old |
| census edge, supply, containment, catchment, capture | FRAMEWORK rules not in v3 | CFG540/543/936/939 | T3, T5 old |
| round enclosed-mass rule; QUMOND phantom disc (PD) | FRAMEWORK rule not in v3; STANDARD-MOND-MACHINERY (QUMOND) | CFG516 | T4 old |
| FM12 eq. 60 / Chae eq. 6 1-D EFE formula | STANDARD-MOND-MACHINERY | CFG936 route iii, CFG8 | replaced by the solve |

## 4. Outputs and rules

`p4_solver.py`, `p4_v3_galaxy_tiles.py` → `p4_v3_galaxy_tiles.out`, `p4_v3_galaxy_tiles_results.json`; `--mutate` →
`_MUTATE.*`. README verdict first, one line per tile (old → v3, class). `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, no
downloads. Pathspec commits of this lane only; never push. Any later change: an append-only AMENDMENT section marked pre- or
post-result.
