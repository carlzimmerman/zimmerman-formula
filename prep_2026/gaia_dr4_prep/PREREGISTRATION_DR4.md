# GAIA DR4 PRE-REGISTRATION FREEZE
## de Sitter-Unruh modified-inertia program — the two banked DR4 pipelines
**Frozen: 2026-07-16. Confrontation target: Gaia DR4 (~Dec 2026).**

---

### Purpose and freeze mechanism

Gaia DR4 will be confronted by exactly two pre-built pipelines in this directory.
Every analysis choice either pipeline makes — cuts, estimator, binning, error
model, statistic, decision bands — is frozen in this document BEFORE the data
exist. Nothing in the tables below may be changed after DR4 lands. The freeze is
enforced by SHA-256 hashes of the pipeline files (this directory is not a git
repository; the hashes are the mechanism). Any change after this date must be
recorded as a dated, clearly-labeled **POST-HOC AMENDMENT** appendix at the
bottom of this file — the original frozen choice is never edited, and any
post-hoc amendment must state what the frozen analysis returned first.

**Framework statement (own terms, not the standard-MOND lens):** modified
INERTIA with horizon-derived a0 = cH_Lambda/Z and the framework's own
dS-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar*a0), i.e.
nu(y) = sqrt(1 + 1/y). Both a0 footings are carried everywhere a0 enters
(working-rule 4): **canonical a0 = 9.36e-11 m/s^2** (rho_DE / cH_Lambda) and
**alt a0 = 1.13e-10 m/s^2** (rho_total / cH0).

**Honesty rules binding on the confrontation write-up:** no
"validates/proves/confirms" language — outcomes are stated as
consistent/disfavored-at-k-sigma/killed per the pre-declared bands below; the
gamma = 1.137 value is the modified-GRAVITY number and is never presented as
the framework-MI target (which is ~1.09, band 1.05–1.10); the s^TX margin is
~1.5x (the "~9.6x" figure is a superseded looser-bound corner and must not be
cited); s^TX outcomes are preferred-frame/Lorentz-violation verdicts,
MOND-family-shared, never MI-vs-MG verdicts.

### Freeze manifest (SHA-256)

| file | role | sha256 |
|---|---|---|
| `prep_2026/gaia_dr4_prep/wide_binary_pipeline.py` | FROZEN analysis pipeline, Door 4A | `669fecc4b42b0f0a23c263715d45c3a56cca112af70fccdc4ed95696d53bb4ff` |
| `prep_2026/gaia_dr4_prep/stx_dipole_template.py` | FROZEN analysis pipeline, Door 4B | `09cf51aef657292412ba0d647744b4470a0dcf58e6e192ba92475fe9930d506b` |
| `zimmerman-formula/real_research/reviews/wb_dr4_prereg_framework_curve.py` | banked theory-target script (read-only, frozen repo) | `6b8fad626067e076219f56309144b7d56c1050f129601b2d73f3286911ac3798` |
| `zimmerman-formula/real_research/reviews/stx_target.py` | banked s^TX prediction (read-only, frozen repo) | `1451b7810e48674f3d8759c484aee3bfd7b874836ca0e810de56d289bfab6987` |
| `zimmerman-formula/real_research/reviews/stx_inpop_recipe.py` | banked s^TX physics + kill ledger (read-only, frozen repo) | `8227bea52b9aa070769b767070cbd0146709c8cafab42432448d4cacd7b7aab1` |

Reproduction commands (both must exit 0):
`python3 wide_binary_pipeline.py --dry-run` and `python3 stx_dipole_template.py`.
Frozen RNG seed for both: **20261216**.

---

## SECTION 1 — Wide-binary gamma test (Door 4A)

### 1.1 Hypotheses and frozen theory targets

The observable is **gamma_v**, the deep-regime velocity-boost asymptote
(v_rms / v_rms,Newton). **Convention warning (frozen):** Chae-style
gravity-boost gamma = G_eff/G_N is the SQUARE of gamma_v. Published
force-boost numbers must be square-rooted before comparison
(e.g. Chae et al. 2026, arXiv:2601.21728: force gamma 1.600 (+0.171/−0.141)
= velocity gamma_v ≈ 1.26). All targets below are gamma_v.

> ### ⚠️ AMENDMENT 1 — 2026-07-27, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **The original table below had a scoring defect: it listed γ_v = 1.000 as the *Newtonian rival* only.
> On the framework's own committed action, 1.000 in the 2–30 kAU window is ALSO the framework's
> prediction.** As frozen, a Newtonian DR4 result would have been recorded as a kill of the framework
> when it may be a confirmation — and could not have been claimed afterwards without being post-hoc.
> This amendment fixes that, and it is entered *before* DR4 rather than after.
>
> **Why.** The framework carries a response gate `G(ω) = 1/(1 + iω/ω_c)` with
> ω_c ∈ [1.782, 2.211]×10⁻¹⁴ rad/s. A wide binary's *orbital* frequency at 10 kAU is
> Ω = 2.44×10⁻¹³ rad/s — **11× above the entire committed ω_c window** — so the gate is SHUT and the
> boost is suppressed by Re G ≈ 0.005–0.008.
> The question of whether the kernel senses the acceleration *magnitude* (constant on a circular orbit
> → gate open → 1.09 stands) or the orbital *frequency* (→ gate shut → 1.000) is now **SETTLED from the
> committed action**, not left open: `S_matter = −½∫√−g ρ_m [s uᵘ K(□_u/a₀²) u_μ]` with
> `□_u f = uᵃ∇_a(uᵇ∇_b f)`, and on a circular orbit **□_u u_μ = −Ω² u_μ identically** (sympy residual
> zero, `real_research/reviews/mi_dcac_branch_settled_2026.py`, 5/5). So K's argument is
> z = −(Ωc/a₀)² — a frequency. The acceleration magnitude, though genuinely constant, never enters the
> operator. **The gated (AC) branch is the framework's branch.**
>
> | amended hypothesis | γ_v target, 2–30 kAU | basis |
> |---|---|---|
> | Newtonian | 1.000 exactly | — |
> | **framework-MI, GATED (the framework's prediction)** | **1.0004–1.0006**, i.e. <0.04σ from Newton | `mi_wb_gate_fork_2026.py` (11/11), all four footing × ω_c-edge combinations |
> | framework-MI, ungated (superseded — retained for the record) | band 1.05–1.10, point 1.09 | the original row below |
>
> **So a Newtonian DR4 result in 2–30 kAU CONFIRMS the framework's gated branch and does NOT falsify
> it.** Conversely, a detection of γ_v ≈ 1.09 in that window would falsify the gated branch and revive
> the ungated one. Both outcomes are informative; neither is a free pass.
>
> **Where the framework IS falsifiable — the discriminating window moves outward.** The gate opens at
> r_gate = (GM/ω_c²)^(1/3), which exceeds the MOND radius r_M = √(GM/a₀) for every mass (ratio
> 4.54–7.76). Between them is a **dead zone**: sub-a₀ but gate-shut, hence Newtonian, running ~10 → ~50–60
> kAU for 1.5 M☉. Beyond r_gate the boost switches on as
> **γ_v − 1 ≃ ½[ν(y_ext) − 1](ω_c²/GM)s³** — exponent **exactly 3**, derived not fitted, amplitude fixed
> by ω_c, the measured pair mass and the Galactic field, with **zero free parameters**
> (`mi_wb_cubic_rise_2026.py`, 10/10). An n-pole gate would give s^(3n), so the measured log-slope
> returns the pole count as n = p/3 (`mi_wb_exponent_pipeline_2026.py`, 6/6). Every published
> contaminant channel rises as s^(1/2) instead. **FROZEN PREDICTION: p = 3.**
>
> **Pre-registered falsifiers of the gated branch**, any one of which kills it: (i) no excess beyond
> ~50 kAU in a contamination-controlled sample; (ii) an excess whose log-slope is inconsistent with 3;
> (iii) a knee that does not move as M^(1/3); (iv) an amplitude inconsistent with ω_c²/GM on both
> footings and both window edges; (v) γ_v ≈ 1.09 detected *inside* 30 kAU.
>
> **Power, and the honest limitation.** The shape test needs ~2000 clean pairs per separation bin for
> ~5σ separation of p = 3 from p = 0.5 (~400 gives only ~2.3σ). El-Badry, Rix & Heintz 2021 has, at
> d < 200 pc, only 436/270/155/60/24/3 clean pairs across the 30→236 kAU bins — **364 total beyond 50
> kAU**. So **this test cannot be run on DR3**; it requires DR4's astrometry and sample
> (`mi_wb_dr3_feasibility_2026.py`, 5/5). That is precisely why this amendment is entered now.
>
> **Unchanged by this amendment:** the a₀-degeneracy flag below still holds in full — DR4 γ_v constrains
> the ν+EFE+gate prescription, **not** the value a₀ = 9.36×10⁻¹¹, and no outcome may be reported as
> measuring a₀ or Z. a₀'s value, Z, s = −1 and ω_c remain POSTULATED. ω_c in particular is anchored by
> no independent argument and is the framework's most exposed quantity.
>
> **Still open, and newly sharpened:** on the frequency axis |K| = 1 exactly, so K contributes pure
> phase there and the entire magnitude suppression rests on the separate gate. Giving the gate the same
> frequency argument as K is now *consistent* rather than assumed — but the K/gate division of labour is
> underived. This amendment does not close that.

| hypothesis | frozen gamma_v target | source |
|---|---|---|
| Newtonian | 1.000 exactly | — |
| **framework-MI** (per-star MI-EFE prescription) | **band 1.05–1.10, point target 1.09** (dynamical asymptote 1.1015, observable-diluted edge 1.0508) — ⚠️ **SUPERSEDED for 2–30 kAU by Amendment 1: this is the UNGATED number** | banked `wb_dr4_prereg_framework_curve.py` (asserts 1.095 < asy < 1.105), rerun 2026-07-16, exit 0 |
| framework-as-MG (AQUAL-EFE point-field, framework nu) | 1.137 (computed 1.1389) | same banked script (asserts \|asy − 1.137\| < 0.005) |
| conventional-MOND benchmark | 1.33 (dynamic-range injection only; Milgrom a0 + literature-scale EFE asymptote — NOT a framework number) | pipeline injection ladder |

Frozen flags carried with the targets:
- **Prescription flag** (banked, verbatim honored): the per-star MI-EFE law is
  a prescription, not a completion — the band 1.05–1.10 is a
  prescription+observable bracket, not a theorem.
- **a0-degeneracy** (computed in the banked script): Milgrom-a0 MI asymptote
  1.134 ≈ framework-a0 MG 1.139. A 22% a0 shift moves gamma_v by 3.3%.
  **DR4 gamma_v constrains the nu+EFE prescription, NOT the value
  a0 = 9.36e-11.** No outcome below may be reported as measuring a0.
- **External field (frozen both ways):** primary g_ext,obs = 1.778e-10 m/s^2
  (= 1.9 a0_can, McMillan-2017-class solar neighborhood; the value the banked
  targets are computed at). Alt convention g_ext = Vc^2/R0 = 2.078e-10
  (Vc = 229 km/s, R0 = 8.178 kpc, per the repo Saad-Ting confrontation
  script). Higher g_ext → more EFE Newtonization → LOWER MI and MG asymptotes.
  Both g_ext values are frozen now; targets are quoted at the primary and the
  alt is reported alongside by mechanically rerunning the banked script — no
  new freedom at confrontation time.
- **Both a0 footings:** binning and y_extN run both ways always
  (canonical y_extN = 1.4647; alt y_extN = 1.1513). Gate-measured recovery
  spread between footings ≤ 0.005 in gamma — the footing is non-diagnostic
  here; canonical decides, alt is always reported.

### 1.2 Frozen DR4 cut list

The DR4 catalog fed to the pipeline (`--catalog`, columns
`sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc`) MUST be built with exactly
these cuts. This table is mirrored in the code (`FROZEN_DR4_CUTS`).

| # | cut | frozen value | a-priori ground |
|---|---|---|---|
| 1 | Galactic latitude | \|b\| > 15 deg | Banik et al. 2024 (MNRAS 527, 4573) §2.1 — crowding/extinction |
| 2 | magnitude | G < 17 both components | Banik+24 §2.1; astrometric error model validity; MS mass calibration |
| 3 | distance | d < 250 pc (parallax > 4 mas) | Banik+24 §2.1 |
| 4 | parallax S/N | ≥ 40 both components | distance error < 2.5% → vtilde error < 4%, subdominant to the 5% mass error; non-binding for most of the G<17, d<250 pc DR4 sample (guards tails only) |
| 5 | parallax consistency | \|d1 − d2\| < min(4 sigma, 8 pc) | Banik+24 §2.1 |
| 6 | projected separation | 2 < s < 30 kAU | Banik+24; the MOND radius r_M(1 Msun) ≈ 7 kAU sits inside the window (deep-regime leverage); > 30 kAU = chance-alignment + Galactic-tide regime |
| 7 | RUWE | < 1.4 both | Gaia DPAC single-star threshold (Lindegren 2018 TN; Lindegren+21); RUWE inflation traces unresolved companions (Belokurov+20, MNRAS 496, 1922) — a direct contamination screen |
| 8 | ipd_frac_multi_peak | ≤ 2 both | Banik+24 §2.4.3 — resolved blends |
| 9 | extinction | A_V < 0.5 | Banik+24 §2.4.1 |
| 10 | total mass | 0.464 < M_tot < 4.31 Msun | validity range of the Banik+24 eq.6 cubic M_G→M (M_G in [0.6, 11.1]); outside it the inversion is non-physical |
| 11 | RV consistency | reject \|dRV\| > max(3 sigma_dRV, 3 v_c(s_proj)) where both components carry DR4 RVs | Banik+24 §2.4.5 (his own screen; ~3.5% loss at DR3) — hierarchical triples induce km/s-scale dRV vs ≤ ~1.4 km/s orbital ceiling at s ≥ 2 kAU, M_tot ≤ 4.31 |
| 12 | **NSS screen (NEW, DR4-enabled)** | reject pairs where either component has ANY DR4 non-single-star solution (astrometric orbit, acceleration, or spectroscopic orbit) | DR4's 66-month epoch astrometry is the designed detector for exactly the undetected inner companions that inflate gamma — the direct cut on the contamination axis that DR3 lacked |
| 13 | resolved-triple search | no co-moving third Gaia source (parallax within 3 sigma, PM within 5 sigma of the pair) with G < 20 within projected 30 kAU of either component | Banik+24 faint-companion search analog (his m_G < 20 depth) |
| 14 | chance alignment | R_chance_align < 0.01 (El-Badry-style statistic recomputed on DR4) | El-Badry, Rix & Heintz 2021 (MNRAS 506, 2269): the > 99%-bound-probability subsample threshold (their own highest-confidence class); Chae 2023 (ApJ 952, 128) §2.1 uses the same value |
| 15 | vtilde error | sigma(vtilde) ≤ 0.1 max(1, vtilde/2) | Banik+24 eq.10 — bounds deep-bin noise inflation (D1-type diagnostic) |
| 16 | vtilde cap | **NONE at catalog level**; the estimator's symmetric cap vtilde < 6.0 applies identically to data and forward model | symmetry between data and model MC (Banik's catalog-level vtilde ≤ 5 is NOT adopted for DR4; it appears only in the DR3-era dry-run transcription, and an asymmetric catalog cap the model does not share would bias the medians) |

**Frozen strictness ladder** (each run alongside the primary, never substituted
for it): RUWE 1.4 → 1.2; R_chance 0.01 → 0.001; separation 2–30 → 3–20 kAU;
RV-screened subsample only; NSS screen OFF (as a contamination probe — the
off/on shift measures the contamination the screen removes).

### 1.3 Frozen estimator and statistic (exactly as coded)

- Observable per pair: vtilde = v_perp / sqrt(G M_tot / s_proj).
- Binning: median(vtilde) in 8 bins of log10(y_proj), y_proj = g_N(s_proj)/a0,
  frozen edges **[−1.5, −1.1, −0.8, −0.5, −0.2, 0.1, 0.5, 1.0, 2.2]**;
  bins with < 80 pairs dropped; symmetric outlier cap vtilde < 6.0;
  per-bin errors: 200-resample bootstrap of the median.
- Forward model: Newtonian Kepler population MC (3,000,000-pair master, sized
  so its finite-MC error is subdominant; that error is bootstrapped at a
  reference gamma and propagated — ignoring it produces a ±1–2% pseudo-bias,
  found and fixed at the gate), thermal f(e) = 2e primary, DR4 noise
  (§1.4), 5% Gaussian mass scatter, masses via the Banik+24 eq.6 cubic.
- Fit: 1-parameter profile chi2 for the deep asymptote gamma_inf over the
  frozen grid **0.90 to 1.50, step 0.0025**, with the EFE-saturated transition
  shape gamma(y) = 1 + (gamma_inf − 1) · y_extN/(y_extN + y),
  y_extN = framework-inverted external field (primary g_ext §1.1).
- Nuisance: one multiplicative kappa (eccentricity-calibration mismatch),
  **anchored** as a Gaussian prior on the high-acceleration bins
  (log10 y ≥ 0.5, boost ≈ 1 for every gamma on the grid) and profiled
  analytically over the deep bins. (A fully-free kappa is degenerate with
  gamma and biases it low by ~0.01–0.05 — found and fixed at the gate.)
  **Frozen kappa acceptance window: [0.95, 1.05].** kappa outside the window
  = eccentricity/anchor calibration mismatch → the verdict is downgraded to
  "systematic-limited" (§1.5), never re-tuned.
- 1-sigma from delta-chi2 ≤ 1; the quoted sigma(gamma) is
  **max(profile sigma, independent-realization rms)** (the pipeline's own
  conservative rule).
- Shape caveat (frozen): injection and recovery share the transition shape by
  construction — the gate certifies ASYMPTOTE RECOVERY, not shape
  discrimination. The confrontation must also overlay the banked exact
  framework curve (`wb_dr4_prereg_framework_curve.py`); shape
  mis-specification is a flagged systematic, not a tunable.

### 1.4 Frozen error model

DR3 per-star sigma_pm, sigma_plx vs G interpolated from Lindegren et al. 2021
(A&A 649, A2) grid as tabulated in the code; DR4 scaling frozen at
**sigma_pm × (66/34)^−1.5 = 0.372** and **sigma_plx × (66/34)^−0.5 = 0.718**
(nominal mission scaling; flagged APPROX). Mass calibration error: 5% Gaussian
per pair (Banik+24 quote ~5.5%, §2.3.3). If DR4's published per-source errors
differ from this model, the pipeline uses the PUBLISHED DR4 errors and the
model-MC noise is regenerated from them — that is a mechanical substitution,
not a re-tune, and is recorded in the amendment appendix.

### 1.5 Pre-declared decision bands

Let gamma_hat, sigma_fit be the pipeline output on the frozen-cut DR4 catalog
(canonical footing decides; alt footing reported). Frozen total error:

- **sigma_sys = 0.02** (frozen allowance), covering: eccentricity-model
  mismatch ±0.015 (gate-measured flat-vs-thermal shift −0.015; the
  Hwang+22-preferred SUPERTHERMAL population lies beyond thermal on the same
  axis and is covered at the same magnitude with opposite sign — flagged),
  a0-footing spread ≤ 0.005, residual shape/g_ext dependence.
- **sigma_tot = sqrt(sigma_fit^2 + 0.02^2)**.

Verdict rule (frozen): z_H = (gamma_hat − gamma_H)/sigma_tot for each
hypothesis H in {1.00, 1.09 [band 1.05–1.10], 1.137, 1.33}.
"**Consistent with H**" requires |z_H| < 2; "**H disfavored**" requires
|z_H| > 3; "**supports H over H'**" requires BOTH |z_H| < 2 AND |z_H'| > 3.

Expected DR4 numbers (from the gate, N = 30,000 assumed; if DR4 yields a
different N after the frozen cuts, sigma_fit scales as sqrt(30000/N) —
mechanical, no freedom): sigma_fit ≈ 0.019, sigma_tot ≈ 0.028. Illustrative
band edges at sigma_tot = 0.028:

| gamma_hat lands in | pre-declared reading |
|---|---|
| ≤ 1.007 | supports Newtonian over framework-MI (MI disfavored > 3 sigma); a Newton-side verdict is contamination-ROBUST (contamination only pushes gamma UP) |
| 1.007 – 1.083 | no hypothesis separation at the frozen thresholds — report as undecided with the z-table |
| 1.083 – 1.145 | non-Newtonian at ≥ 3 sigma AND framework-MI-compatible; **MI-vs-MG is NOT decided in this zone** (1.137 lies inside it); requires the ladder-stability + kappa-window + contamination tests to pass, else "systematic-limited" |
| 1.145 – 1.20 | MG-side; MI disfavored per z; same ladder requirements |
| > 1.20 | **contamination-guard zone**: above every EFE-saturated target, approaching the no-EFE benchmark — pre-declared reading is "contamination-dominated or EFE-shape failure", NO hypothesis verdict permitted (this is where the DR3 dry run landed, §1.6) |

Separation forecasts (frozen, statistical at N = 30k): Newton vs MI 1.09 at
3 sigma needs N ≳ 12,200 — expected DECIDABLE. MI 1.09 vs MG 1.137 at 3 sigma
needs N ≈ 45,000 statistically AND sigma_sys < 0.01 — pre-declared as
**likely UNDECIDABLE in DR4 at the frozen allowances**; no post-hoc shrinking
of sigma_sys may be used to claim it. MOND benchmark 1.33 separates from all
others at > 7 sigma.

Stability requirements for any non-Newtonian verdict (frozen): every
strictness-ladder variant (§1.2) must shift gamma_hat by < 1 sigma_fit; kappa
within [0.95, 1.05]; the NSS-off contamination probe must move gamma_hat
TOWARD the verdict value when the screen is turned ON. Any failure →
"systematic-limited, no verdict" — that outcome is reported, not repaired.

### 1.6 Contamination axis: mitigation plan and the DR3 dry run read honestly

**The axis:** undetected close companions (hierarchical triples) add orbital
velocity to v_perp and inflate gamma — contamination biases HIGH, mimicking a
boost, never a deficit. This is the known interpretation axis of the entire
wide-binary literature (Chae 2023 models hidden companions probabilistically;
Banik+24 rejects them by screens; their opposite conclusions — force-boost
detection vs Newtonian at 19 sigma — trace to exactly these choices).

**How the frozen cuts bound it:** four independent screens attack it — RUWE
< 1.4 (astrometric-wobble tracer, Belokurov+20), the DR4 NSS screen (direct
66-month orbit/acceleration detection — the qualitatively new DR4 handle),
the RV screen (km/s-scale dRV from inner companions vs ≤ 1.4 km/s orbital
ceiling), and the resolved-triple search to G < 20. The NSS-off ladder rung
measures removed contamination directly, and the asymmetric verdict rule
(§1.5) makes the Newton-side reading contamination-robust while holding any
boost-side reading to the stability tests.

**DR3 dry run (2026-07-16, El-Badry+21 eDR3 catalog, Banik-like cuts,
10,624 pairs): gamma = 1.205 ± 0.035 (canonical), 1.2025 ± 0.0337 (alt).**
Honest reading, frozen: this value lands in the pre-declared
contamination-guard zone (> 1.20) and is **consistent-with-contamination**:
the dry-run sample is LOOSER than Banik's 8,611 (three of his screens are not
implementable from the eDR3-era catalog: the chi2/nu cut beyond the RUWE
substitute, the faint-companion search, and the RV triple screen — each
removes triples, so their absence biases gamma HIGH by construction). The
repo's own banked audits quantify the degeneracy: a Newtonian population
needs f_triple ≈ 0.19–0.20 to absorb the deep-bin excess
(`wb_threshold_audit`), and the deep-bin medians sit ~2–3 sigma above the
calibrated Newtonian MC while the MOND upper bound overshoots them by 6–22
sigma (`wb_deprojection_mc`). **The dry run is a pipeline shakeout — machine
works, real data in, plausible-magnitude output — and is NOT evidence for any
hypothesis, including the framework's.** It is also not evidence against:
1.205 with no triple screens is exactly what either a Newtonian or an MI
population plus known contamination would produce. The DR4 run with cuts
11–13 active is what adjudicates.

### 1.7 Gate and dry-run record (rerun after the freeze edits, 2026-07-16)

`python3 wide_binary_pipeline.py --dry-run` → **exit 0, GATE VERDICT: PASS.**
Synthetic-injection gate (N = 30,000, DR4 noise, no hard-coded passes):
inject 1.00 → recover 0.9850 ± 0.0137 (canonical) / 0.9900 ± 0.0125 (alt);
inject 1.09 → 1.0950 ± 0.0137 / 1.0925 ± 0.0150;
inject 1.33 → 1.3450 ± 0.0212 / 1.3375 ± 0.0212 — all within
max(2 sigma, 0.02). Spread check (8 catalogs @ 1.09): mean 1.0881,
rms 0.0191. Eccentricity bracket: flat-e truth under thermal-e model shifts
gamma by −0.0150 (flagged systematic, §1.5). DR3 dry run: §1.6 numbers,
802 deep pairs (y < 0.3, canonical).

---

## SECTION 2 — s^TX SME boost-dipole template (Door 4B, Front A)

### 2.1 Frozen prediction, direction convention, and current standing

- Prediction (banked, not re-derived): per-body
  s^{Tj} = (a0 / 2|g_orb|) gamma^2 beta_cmb n_hat_j; Saturn channel
  **|s^TX| = 8.68e-10 (canonical a0)**; a0 enters linearly →
  **alt footing 8.68e-10 × (1.13/0.936) = 1.048e-9**.
- **Frozen direction convention:** n_hat = the Planck 2018 CMB dipole apex,
  galactic (l, b) = (264.021°, 48.253°) = equatorial (J2000)
  RA 167.94°, Dec −6.94°. Locked equatorial component ratios
  **s^TY : s^TX : s^TZ = 0.208 : −0.971 : −0.120** (code-asserted against the
  IAU rotation to < 5e-3). The predicted **s^TX is NEGATIVE** (n_X < 0 with a
  positive per-body amplitude). Template sign frozen: alpha > 0 IS the
  framework sign; there is no post-hoc sign freedom.
- **Frozen reading fork:** primary = P (per-body, amplitude ∝ 1/g_orb — the
  ledger's own formula); U (universal single s^TX) always cross-fit. The
  noise-free P-signal-vs-U-template overlap in this channel is alpha_U =
  +0.0047 — the readings are nearly orthogonal; verdicts are quoted per
  reading, never mixed.
- **Current standing (frozen, correct margin):** tightest published bound =
  the COMBINED multi-planet fit s^TX = (−0.2 ± 1.3)e-9 (Hees et al. 2016,
  arXiv:1610.04682 Table 9; Kostelecky–Russell Data Tables v19 Table D50).
  The canonical prediction sits **0.67 sigma INSIDE the bar with the
  predicted negative sign** — margin **1.50x canonical / 1.24x alt**. LIVE:
  neither comfortably safe nor excluded, and the sign agreement is not a
  detection. **The "~9.6x margin" figure is superseded** (it was the
  Saturn-amplitude vs INPOP-only 8.3e-9 looser-bound corner; banked
  correction 2026-06-21) and must not be cited.
- **Interpretation guard (frozen):** any preferred-frame MG host
  (AeST/khronometric-class) induces a comparable s^TX. Every outcome below is
  a preferred-frame/Lorentz-violation verdict, MOND-family-SHARED — **never**
  an MI-vs-MG verdict.

### 2.2 Frozen statistic

GLS amplitude fit of the locked-direction template:
alpha_hat = ⟨T_perp, d⟩ / ⟨T_perp, T_perp⟩, sigma_a = sigma_NP/sqrt(⟨T_perp,T_perp⟩),
where T is the Earth–Saturn range perturbation from numerical integration
(DOP853, rtol 3e-12) of BOTH bodies carrying their per-body s (H15 eq. 3
boost term; Hees, Bailey et al., PRD 92, 064049 (2015)), and T_perp, d are
projected orthogonal to the frozen absorption basis: 6 Saturn ICs + 6 EMB ICs
+ GM_sun + range bias + linear drift (finite-difference partials; the banked
"conservative" level — a real INPOP/DE global refit absorbs more, so all
sensitivities quoted here are upper limits AT THIS ABSORPTION LEVEL, flagged).
Template linearity is gate-verified (two independent scalings, < 1%
required). Normalization: **alpha = 1 ⟺ |s^TX| = 8.68e-10 (canonical)**;
**alpha = 1.207 ⟺ |s^TX| = 1.048e-9 (alt footing)**.

### 2.3 Pre-declared decision bands (mirrored verbatim in the code output)

| outcome | frozen condition |
|---|---|
| DETECT (canonical) | alpha_hat ≥ 3 sigma_a AND \|alpha_hat − 1\| ≤ 2 sigma_a |
| DETECT (alt) | alpha_hat ≥ 3 sigma_a AND \|alpha_hat − 1.207\| ≤ 2 sigma_a |
| KILL (canonical) | \|alpha_hat\| < 2 sigma_a with sigma_a ≤ 0.50, i.e. sigma(s^TX) ≤ 4.34e-10; 3-sigma kill at sigma_a ≤ 0.33 (sigma(s^TX) ≤ 2.89e-10) |
| KILL (alt) | \|alpha_hat\| < 2 sigma_a with sigma_a ≤ 0.604 (sigma(s^TX) ≤ 5.24e-10) |
| WRONG-SIGN KILL | alpha_hat ≤ −3 sigma_a (direction- and sign-locked template) |
| NO VERDICT | any sigma_a too large to exclude either 0 or the prediction — the present standing |

A detection claim additionally requires the U-reading cross-fit to be
reported and the P/U discrimination stated; a canonical-vs-alt footing
discrimination requires the two DETECT windows to be disjoint at the achieved
sigma_a (they overlap for sigma_a > ~0.05 — pre-declared as unlikely to be
separable; the footings differ by 0.207 in alpha).

### 2.4 Honest sensitivity statement (frozen — no sensitivity claims beyond it)

This single Cassini–Saturn direct-range channel (623 normal points,
2004.0–2017.7, Di Ruscio et al. 2020, A&A 640, A7; sigma_NP = 6 m mid value,
3/15 m sensitivity rows, flagged approx) reaches sigma(s^TX) ≈ 1.5e-7 at the
conservative absorption level — **~2 orders short of the prediction**
(detection significance ~0.006 sigma; prediction-vs-bound separation ~0.003
sigma). It cannot alone detect 8.68e-10, nor separate it from a
bound-saturating 1.3e-9. This matches the banked recipe (Saturn sigma_A =
4.5e-8; the strong per-body channel is Mars, sigma_A = 3.44e-9; the published
1.3e-9 bound is the combined multi-planet secular fit). **The frozen
deliverable is the gated fixed-direction template machinery** — locked
direction, locked ratios, locked statistic, locked bands — ready to ingest
DR4-era ephemeris residual series (INPOP/DE refits absorbing Gaia DR4
asteroid/SSO astrometry) via `fit_amplitude()`. The decision, when it comes,
lives in the multi-planet combined fit evaluated against §2.3 exactly as
frozen.

### 2.5 Gate record (rerun after the freeze edits, 2026-07-16)

`python3 stx_dipole_template.py` → **exit 0, GATE VERDICT: PASS** (linearity
7.4e-5 rel. dev.; injection alpha = 1, null, and high-S/N alpha = 2000
recovered within tolerance at sigma_NP = 3/6/15 m over 500 noise
realizations each; empirical/analytic sigma ratios 1.057/0.985/1.002).
Template raw p2p 6.770e-2 m per unit alpha; after conservative absorption RMS
1.390e-3 m per unit alpha (94.3% absorbed). Locked ratios verified against
the Planck-apex rotation to 1.1e-3.

---

## Amendment protocol

Nothing above changes. Post-DR4, the only permitted additions are dated
**POST-HOC AMENDMENT** entries below this line, each stating (a) what the
frozen analysis returned first, (b) what is being added and why, (c) that the
addition is exploratory and carries no pre-registered evidential weight.

*(no amendments)*
