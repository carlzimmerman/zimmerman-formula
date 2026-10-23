# X2_cluster_outskirts: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. Map: `X0_explanation_map/MAP.md`
§1.A (items 1–3) and §3 (first bullet). Inputs and classes: `ASSUMPTION_LEDGER.md`.
κ = ½ FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻², reported side by side, never pooled. No dark-matter
particle. No new fitted constant as a cure. Never "theory closed". Never "the data favour the framework".

## 0. Question

F1 (f1803b0256) finds the eRASS1 × KiDS cluster cores at A_MID = 1.68–1.85 (canonical) / 1.54–1.70 (alt) times the law on
baryons (0.46–1.42 Mpc, bins 3–5), with A_OUTER ≈ 0.87–1.00 (1.42–3 Mpc, bins 6–7), and writes that "any added cold profile
that fixes MID overshoots the outskirts". Does that survive (a) the measured outskirt gas slope, (b) mass terciles, (c) the
external field, (d) the reduced-shear term, (e) the cross-shear and random-minus-random null offsets? On the corrected
baseline, does any fixed-form published component, with no constant fitted here, pass?

**Seen before freezing (disclosed).** READMEs, criteria and ledgers of F1, H2, S4; F1's `f1_cluster_cores.py` (full), its
`.out` and JSON row names; H2's `chi2_prof` code and its printed law χ² (33.4 / 27.3 at h 0.672, 41.8 / 34.9 at h 0.686);
F1's MUTATE JSON rows (cross shear, PRIMARY h0672 MID 0.209 / 0.192); READMEs or LEDGER rows of CFG687, CFG688, CFG814
(+ criteria and `cfg814.py` gas lines), CFG949 (+ criteria §1–5, `cfg949.py` structure and the R930 code block), CFG727,
CFG922; T1 and F2 field definitions (Chae+21 noclu / maxclu medians, P2 catalogue medians); FPS 2410.02612 Eq. 17 and
its mean parameters (web lookup, §3); Milgrom 2008 abstract (web lookup). **No number of this lane exists.**

## 1. Data, statistic, cells

- **Data.** F1's own per-cluster KiDS measurement (326 eRASS1 clusters, F1's estimator, F1's random positions), REPLAYED
  here from F1's KiDS column cache with F1's `esd()` / `gather()` / random loop verbatim, extended only to also return
  (i) the cross shear, (ii) each random's ESD separately, (iii) the source moments m_k = Σ w·Σ_crit⁻ᵏ, k = 2…5, per bin
  and per h. The replay must reproduce F1's cache `f1_meas.pkl` (sha256 961ea4fc…e720) exactly (check R1) and F1's
  MUTATE cache (cross shear) exactly (R2). The per-cluster products are committed as `x2_replay_percluster.npz`.
- **Statistic.** F1's: A_band = Σ_i Σ_j W_ij D_ij B_j / Σ_i Σ_j W_ij P_ij (W = 1/E², B = F1's data boost, applied as in
  F1's frozen PRIMARY), bands MID = bins 3–5, OUTER = bins 6–7 (INNER reported, never graded); jackknife over F1's 30
  equal-count RA patches. Z_band = (A_band − 1)/σ_band.
- **Profile χ²** (H2's A1 line, used by S4 and named "F1's line" in the brief): residual stack
  s_j = Σ_i W_ij (D_ij B_j − P_ij)/Σ_i W_ij over bins 3–7, jackknife covariance (30 patches), Hartlap (30 − 5 − 2)/29;
  pass line χ² ≤ 11.07.
- **Cells.** 2 footings × 2 native h (0.672, 0.686) = 4 cells. Every graded statement must hold in all 4 cells; footing or
  h splits are reported as SPLIT.
- **Boost convention.** Graded on F1's frozen PRIMARY convention (measured boost B < 1 applied). Every graded row is also
  reported with F1's A1 convention (boost clipped at 1). If a class differs between the two, it carries the qualifier
  BOOST-DEPENDENT.

## 2. Baseline C0 (step 0) and the changes (step 1)

**C0 = F1 PRIMARY:** spherical AQUAL μ = x/(1+x); native h; eRASS1 Mgas500 × q^{5/2}, R500 × q; β-model β = 2/3,
r_c = 0.15 R500, normalised to Mgas500, cut at 3 Mpc; stars f* = 0.20 × gas; catalogue miscentring; data boost.
Implemented by exec'ing F1's own functions from `F1_cluster_cores/f1_cluster_cores.py` (sha256 recorded) read-only.

Changes, each applied ALONE to C0, then all primaries together (C*):

- **(a1) PRIMARY measured outskirt slope (CFG814's prescription):** gas = C0's β-model inside r200m ≡ 2.2 R500, then
  ρ ∝ r⁻³ beyond (continuous), still cut at 3 Mpc; normalisation at R500 unchanged. Source: CFG814, which takes ≈ −3 at
  r200m from the SRG/eROSITA stack arXiv:2509.25317 (abstract value, PROVISIONAL) and r200m = 2.2 R500 (PROVISIONAL
  conversion). Brackets, reported, never in a class name: **(a2)** CFG814's bracket F (r⁻³ to 2 r200m, then r⁻²);
  **(a3)** ρ ∝ r⁻³ from R500 outward (the steepest reading; not the record's prescription).
- **(b) Terciles:** catalogue MGAS500 (unrescaled, as CFG687/CFG949) terciles of the 326; every quantity per tercile at
  C0 and at C* (jackknife with F1's patch labels restricted to the tercile).
- **(c1) PRIMARY external field:** uniform Newtonian y_e = Chae+21 "noclu" median (F2's primary, "the weakest on-disk
  empirical estimate"), y_e = 10^(median log e_N) × 1.2e-10 / a₀ per footing, median recomputed from
  `real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv` and required to equal F2's −3.215 to ±0.005.
  Brackets, reported: **(c2)** Chae+21 "maxclu" median (F2's upper, −2.30); **(c3)** P2's catalogue median y_e = 6.56e-5 /
  5.43e-5 (galaxies' baryons only, a lower bound). None of these is a field measured at eRASS1 clusters (stated).
  **Solver:** F2's exact axisymmetric AQUAL solve of a point mass in a uniform field (`F2_outer_lensing/f2_aqual.py`,
  imported read-only, default resolution), giving C(s; y_e) = M_EFE(<s)/M_iso(<s), s = r/r_M. **Primary transplant
  (F2's):** g(r) = g_iso(r) × C(r/r_M) with r_M = √(G M_src,tot/a₀), M_src,tot = all sourcing mass inside 3 Mpc.
  **Bracket (c1-loc):** r_M(<r) from the enclosed mass (local). Newtonian-added components get no EFE.
- **(d) Reduced shear:** the model is forward-modelled into the estimator: P_red,ij = P_ij Σ_{k=0..3} Σ_ij^k m_{k+2,ij}/m_{2,ij}
  (the expansion of Σ w Σ_crit⁻² · ΔΣ/(1 − Σ_crit⁻¹Σ) / Σ w Σ_crit⁻² to 4th order), with Σ_ij the model's own
  (miscentred) surface density at bin centres. Each model (law or law + component) uses its own Σ.
- **(e) Systematics propagated:** null stacks from the replay: cross shear D× (cluster − mean random, as F1's MUTATE) and
  random-minus-random D_RR = mean(randoms 1–3) − mean(randoms 4–n) (CFG687's M2 definition), both × B. Band offsets
  A_×,band = Σ W D× / Σ W P and A_RR,band likewise; σ_band,sys² = σ_jk² + A_×,band² + A_RR,band²; the χ² covariance adds
  the rank-1 templates s_× s_×ᵀ + s_RR s_RRᵀ (s from the residual-stack formula with D → D×, D_RR, P → 0). Conservative
  (the null stacks carry shape noise). Z is reported with and without (e).
- **C\* (corrected baseline)** = C0 + (a1) + (c1) + (d) + (e). C* is the baseline for step 2.

Reported for C0, every single change, every bracket, C*, per cell and per boost convention: A_INNER, A_MID ± σ, A_OUTER ± σ,
Z_MID, Z_OUT, profile χ², the gas share beyond R500 inside 3 Mpc, and the overshoot diagnostic (§2.1).

### 2.1 Overshoot diagnostic (operational form of F1's sentence; a shape test, never a pass)

- **PN (graded):** a central point mass per cluster, M_pt,i = λ × (rescaled Mgas500_i), added Newtonian to the
  configuration's model (ΔΣ = M_pt/πR² for R > the cluster's miscentring offset, 0 inside; Σ = 0 at R > offset). λ is
  solved so that A_MID = 1 (the "needed" amount, as F1 solved its needed dust). Then A_OUTER, Z_OUT and χ² are reported.
  **Why PN:** for any added component with a non-increasing ρ(r) ≥ 0 added Newtonian, πR²ΔΣ is non-decreasing in R, so
  ΔΣ(R_out)/ΔΣ(R_mid) ≥ (R_mid/R_out)², with equality for a point mass. Per cluster, PN therefore adds the LEAST outer signal
  of any such component for a given MID gain: if PN overshoots, every monotone added component overshoots at least as much
  (under the same per-cluster scaling). A component that sources the AQUAL field adds phantom mass and is argued, not
  proven, to overshoot more (PS reported).
- **Reported, not graded:** PS (the same point mass sourcing AQUAL) and GS (F1's own shape: dust tracing the gas, sourcing
  AQUAL; F1's "needed dust") at C0 and C*.
- If λ_needed ≤ 0 (A_MID ≤ 1 already), the overshoot is "not applicable" (counts as no overshoot).
- **Status per configuration:** OVER if Z_OUT(PN) ≤ −2 in all 4 cells; NONE if Z_OUT(PN) > −2 in all 4; SPLIT otherwise.

## 3. Step 2: fixed-form components on C* (NO constant fitted here)

Each is added to C*'s baryons with every C* ingredient (gas (a1), EFE (c1) for sourcing mass, reduced shear with the
model's own Σ, systematics). Graded in all 4 cells.

- **K-DEB-rule (CFG949's committed debris, its own reading B0):** lensing mass = baryons (C* gas × 1.2) + the CFG949
  primary-corner debris, all Newtonian, no law (footing-independent): (1 − f_b) M_ta in a truncated NFW with CFG930's rule
  (C = 3000, r_ta boundary, native EPS z_c, cluster's own z), M_ta from CFG949's S-cen supply on the C* gas
  (M_ret = 1.2 M_gas(< 3 Mpc), census f_ret). Code: CFG949's R930 block exec'd read-only (sha256 recorded).
- **K-DEB-committed:** as K-DEB-rule, but the supply computed from F1's C0 gas (β = 2/3 to 3 Mpc), i.e. the debris amount
  CFG949's rule assigns with the gas budget it was committed with; lensing baryons stay C*'s.
- **K-DEB+law:** C*'s law on the baryons plus K-DEB-rule's debris added Newtonian (the "added to the corrected law"
  reading; CFG930's N-B double count).
- **K-FPS (LITERATURE-INPUT, PROVISIONAL):** FPS (Famaey, Pizzuti & Saltas, arXiv:2410.02612) Eq. 17,
  ρ_δM(r) = η ρ_gas(r) exp(−r/r_c), with their weighted means log η = 0.93 (η = 8.511) and r_c = r₀/λ = 0.43 Mpc (physical),
  ρ_gas = C*'s gas; the missing mass sources the AQUAL field with the baryons (FPS's QUMOND with ν simple = this AQUAL in
  spherical symmetry). Fitted by FPS on 16 CLASH clusters (gas masses 0.8–5.3e14 M☉); applied unchanged here (no rescaling
  with mass, no use of their scatter). Source: web lookup of the arXiv HTML (PROVISIONAL; the paper is not on disk).
- **Milgrom 2008 (arXiv:0712.4203) CBDM: NOT TESTED** — the abstract (web lookup, PROVISIONAL) gives only "similar to the
  hot-gas mass, more centrally concentrated", not a fixed form.
- **Pass line (per component):** profile χ² ≤ 11.07 AND |Z_MID| ≤ 2 AND |Z_OUT| ≤ 2, with (e), in all 4 cells.
  Also reported without (e) and with the clipped boost.
- No amplitude, concentration, η, r_c or supply is adjusted; no scan. A component that fails is reported as failing.

## 4. Frozen verdict classes (all four reported)

**V1 overshoot (F1's sentence):**
- **OVERSHOOT ROBUST:** status OVER at C0, after each primary single change ((a1), (c1), (d), (e)) and at C*.
- **OVERSHOOT REMOVED BY ⟨X⟩:** OVER at C0 and NONE at C*; ⟨X⟩ = the primary single changes whose status is NONE alone;
  if none alone, "REMOVED ONLY IN COMBINATION".
- **OVERSHOOT WEAKENED BY ⟨X⟩:** OVER at C0, not ROBUST and not REMOVED (C* SPLIT, or C* OVER with some single change not
  OVER); ⟨X⟩ named as above.
- **OVERSHOOT NOT ESTABLISHED AT F1's BASELINE:** C0 status is not OVER (then F1's sentence held only for its specific
  shapes; GS reported).
- Qualifiers (reported, never change the class): per-tercile statuses at C0 and C* ("HOLDS IN EVERY TERCILE" / names); the
  brackets (a2), (a3), (c2), (c3), (c1-loc); BOOST-DEPENDENT.

**V2 component:** **A FIXED-FORM COMPONENT PASSES (name)** if any of K-DEB-rule, K-DEB-committed, K-DEB+law, K-FPS meets
§3's pass line in all 4 cells; else **NONE PASSES** (with the reason per component: MID, OUTER or shape/χ²).

**V3 core excess (the law on baryons at C\*, with all systematics):** **SURVIVES** if Z_MID ≥ 3 in all 4 cells;
**NOT SIGNIFICANT** if Z_MID < 2 in all 4; **WEAKENED** otherwise. Also reported without (e).

**V4 outskirts anchor:** A_OUTER of the law at C* and per tercile, reported with Z_OUT (no class name beyond the numbers).

## 5. Checks (scripts print `K# PASS|FAIL value threshold`; exit 0 iff all pass)

Replay `x2_replay.py <F1 KiDS cache dir> <F1 meas dir>` (writes `x2_replay.out`, `x2_replay_results.json`, the npz):
- R1: 326 clusters; per cluster and h, D, E, den, den_r equal F1's `f1_meas.pkl` (max |Δ| ≤ 1e-9 × max|D|, names identical).
- R2: cross-shear D equals F1's `f1_meas_MUTATE.pkl` the same way.
- R3: the 4th-order reduced-shear series equals the exact Σ w Σ_crit⁻²/(1 − Σ_crit⁻¹Σ_t) average over the actual sources to
  ≤ 1e-6 relative, for 3 clusters × all bins at Σ_t = 300 M☉ pc⁻².
- R4: peak RSS < 1 GB.
- `--mutate`: the first 20 clusters only, with e2's sign flipped; R1 must FAIL.

Analysis `x2_cluster_outskirts.py [--mutate]`:
- K0: C0 reproduces F1's PRIMARY A_MID and A_OUTER (F1 JSON, 4 cells) to ≤ 1e-4, and the law χ² reproduces H2's printed
  33.4 / 27.3 / 41.8 / 34.9 to ≤ 0.5 (H2 used its own signed projector, which differs from F1's by ~2e-3 per bin; S4's
  third projector gave 33.6 / 27.6). This lane's χ² always uses F1's projector.
- K1: replay npz sha256 recorded; F1 source sha256 recorded; CFG949 source sha256 recorded.
- K2: the truncation-aware projector (log ρ floored at 1e-300 in every cell) equals F1's projector to ≤ 1e-12 relative for a
  positive profile, and gives a truncated uniform sphere's analytic ΔΣ to ≤ 1 % in bins 3–7.
- K3: (a1) gas equals C0's inside 2.2 R500 (≤ 1e-12), has log-slope −3 beyond (±1e-3), and keeps M_gas(< R500) = Mgas500.
- K4: EFE: (i) F2's own isolated-limit check: C(s) at y_e = 1e-6 equals 1 to ≤ 1e-3 at s = 0.1, 0.3, 1, 3, 10; (ii) C(s) ≤ 1 + 2e-3 for every s at every used y_e;
  (iii) the noclu median equals F2's −3.215 (±0.005).
- K5: reduced shear: the factor is ≥ 1 everywhere and the median Σ_crit⁻¹Σ in MID is < 0.1 (perturbative).
- K6: CFG949 reproduction: its R930 debris + CFG687's own inputs (318 clusters, `cfg687_percluster.npz`, β-model gas,
  h 0.70, Newtonian, truncation-aware projector) give B0 A_MID 1.011 and A_OUTER 1.047 to ≤ 0.02.
- K7: FPS implementation: for a uniform test gas the missing mass inside r equals the analytic η ρ₀ 8π r_c³ [1 − e^{−x}(1 +
  x + x²/2)], x = r/r_c, to ≤ 1e-4.
- K8: the cross-shear band offset at C0, h 0.672, reproduces F1's MUTATE PRIMARY h0672 A_MID 0.209 / 0.192 to ≤ 0.002.
- K9: peak RSS < 1 GB.
- `--mutate` (outputs `*_MUTATE.*`): the cross shear replaces the tangential data (K0 must FAIL), the EFE ratio is
  inverted (K4(ii) must FAIL) and the reduced-shear correction flips sign (K5 must FAIL).

Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, ≤ 30 min each; none while free memory is low (`compute_queue/heavyq.py
status`); compute_queue/ and other lanes untouched.

## 6. Stop rule

No knob scans; no component amplitude fitted; the needed-λ of §2.1 is a diagnostic only. Brackets are reported, never used
to name a class. If R1/R2 or K0 fail, nothing downstream is graded (UNDECIDED, missing input named).

## AMENDMENTS (append-only; each labelled PRE-RESULT or POST-RESULT)

- **A1 (PRE-RESULT, implementation; written before any script had run and before any number of this lane existed):** the
  4th-order reduced-shear series of §2(d) cannot meet R3's frozen 1e-6 at Σ_t = 300 M☉ pc⁻² (κ ≈ 0.07 there, so the
  truncation error is ≈ κ⁵ ≈ 2e-6). The replay stores m_k for k = 2…8 and the series is taken to 6th order,
  P_red = P Σ_{k=0..6} Σ^k m_{k+2}/m_2, in both R3 and (d). R3's threshold is unchanged.
- **A2 (POST-RESULT for R4 only; memory handling, no physics or statistic change):** the first full replay (kept as
  `x2_replay_RUN1_rss.out`, `x2_replay_results_RUN1_rss.json`) reproduced F1's caches exactly (R1, R2: max |Δ| = 0) and
  passed R3, but FAILED R4 at 1.126 GB macOS ru_maxrss (the touched pages of the memory-mapped KiDS columns count there).
  The replay now re-opens the memory maps every 15 tried clusters, which unmaps the touched pages. R1–R4 are re-run and
  must pass again; R4's threshold is unchanged. No number of the analysis script existed when this was written.
- **A3 (written after a development run had printed C0 and the (a1)/(a2) rows, and BEFORE any (c) row was seen; solver
  setting only):** with F2's default iteration cap (300) the Kacanov iteration stops before its 1e-9 tolerance at the
  weak fields (last relative change 1.1e-8 / 2.3e-8 for noclu, 4.2e-6 / 5.3e-6 for the P2 catalogue field). All EFE solves
  (and the K4(i) solve) now use `maxit = 3000` with F2's resolution and tolerance unchanged; the reached tolerance is
  reported per solve. The development run's outputs are overwritten by the final run.
