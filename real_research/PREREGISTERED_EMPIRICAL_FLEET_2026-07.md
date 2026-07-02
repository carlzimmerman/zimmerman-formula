# PRE-REGISTERED EMPIRICAL FLEET — 2026-07
## Six confrontations of the dS-Unruh modified-inertia framework, verdicts locked before the data

**Framework footing (its own terms, fixed for every test below):** de Sitter–Unruh **modified inertia**; a₀ = c²√(Λ/32π) = cH_Λ/Z = **9.36×10⁻¹¹ m/s²**, Z = √(32π/3); interpolation g_obs = √(g_bar² + g_bar·a₀), i.e. ν(y) = √(1 + 1/y) — the framework's own ν, not McGaugh's. This is a **one-parameter reframing of a₀** (the TOE/SM overclaims were publicly retracted 2026-06-23 and are not reasserted here). Footing forks are disclosed where they bite: canonical a₀ from ρ_DE/cH_Λ (9.36e-11) vs the ρ_total/cH₀ variant (1.13e-10); redshift evolution a₀(z) ∝ √ρ_DE(z) (canonical, can bump/decline) vs cH(z)E(z)/Z (always rising). This document pre-registers, dated **2026-07-02**, the prediction AND the kill condition for six empirical tests, ordered by how soon each crunches. Every load-bearing number carries its source. The kill conditions are stated as prominently as the detection conditions, and the author accepts them as written.

**Verification scripts:** committed — `reviews/stx_target.py` (s^TX = 8.68e-10), `reviews/cassini_quadrupole_framework.py` (Q₂ inheritance), `real_research/rar_framework_a0_mlfit.py` (RAR 0.108 dex @ Υ=0.70, convention-compatibility baseline). Session scripts (scratchpad, exit 0, pending author vetting + commit): `stx_inpop_recipe.py`, `wb_dr4_prereg_framework_curve.py`, `desi_dr3_decision_matrix.py`, `eta_beta_first_crude_CLASHVLT.py`, `sigma_spread_survey_forecast.py`.

---

## Test 1 — s^TX Lorentz-violation dipole: dedicated INPOP/JPL fixed-direction fit

**The pre-registered prediction.** The framework's preferred frame induces an SME gravity-sector background with a single boost component: **|s^TX| = 8.68×10⁻¹⁰**, CPT-even only, sign negative (same sign as the Hees+ 2015 central value −2.9e-9), with the direction **FIXED at the CMB dipole apex** (l,b) = (264.021°, 48.253°) → (RA, Dec) = (167.94°, −6.94°) in the Sun-centered frame; β_apex = 1.2336×10⁻³ (Planck dipole 369.82 km/s). Component ratios locked: s^TY/s^TX = −0.2136, s^TZ/s^TX = +0.1245. Source: `reviews/stx_target.py`; validated this session against Hees+ 2015 (PRD 92, 064049) Eq. (3)/(7a,b) to 0.01%.

**Load-bearing fork (disclosed, both readings run).** Reading **U** (universal s^TX — what every published bound constrains, and what the headline comparison uses) vs reading **P** (per-body, s^Tj ∝ a₀/2g_orb, the ledger's own formula). Under **P**, drift rates are ≤0.012 mas/cy — 30–1000× below current σ, and even a dedicated fit gives S/N 0.26–0.44: **planetary ephemerides cannot currently test reading P.** This front is a **reading-U test only**, and the "crunchiest in-hand" claim is scoped accordingly.

**The kill condition.** A dedicated 1-parameter INPOP fit (direction fixed at the apex, amplitude A the only new parameter) returning **|A| < 2σ with σ_A ≤ 4.3×10⁻¹⁰ excludes the prediction at ≥2σ**; at the idealized Mars-dominated floor (σ_A ≈ 4.3×10⁻¹¹) the exclusion power is 8–20σ. This is decidable with **existing** MESSENGER + Mars archives — no new mission required.

**The data + date.** MESSENGER ranging 2011–15, Mars orbiters (MGS/MEX/MRO) 2005–20 (the workhorse: idealized S/N 21–40), Cassini 623 normal points 2004–17 (Di Ruscio+ 2020, A&A 640, A7), Juno 2016–26. Archives in hand now; requires an INPOP/JPL-side run (raw residual products are not publicly fetchable — verified this session). Realistic date: whenever an ephemeris group runs it; the analysis is a one-parameter addition.

**The analysis recipe.** Add the Hees+ 2015 Eq. (3) boost term δa⃗ = (2GM/cr³)[(s⃗·v⃗)r⃗ − (r⃗·v⃗)s⃗] to each planet's EOM with s⃗ = A·n̂, n̂ fixed as above; s̄^jk = 0; no change to light-time/Shapiro. Fit A jointly with ICs, GM_sun, asteroid ring. Run variants U and P, report both. The fixed direction collapses Hees+ 2015's 8-parameter 0.99-correlated fit (marginal σ = 8.3e-9) to a ~100× tighter 1-parameter fit — that is the entire leverage.

**Status: crunchiest in-hand test, genuinely on the edge.** DIY 1-parameter fit on the published secular-advance tables (Hees+ 2015 Table I; INPOP15a updates from Fienga+ 2016, arXiv:1601.00947): **A = (−2.5 ± 5.9)×10⁻¹⁰** [10a] / (−0.9 ± 6.4)×10⁻¹⁰ [15a-updated]; 95% bound |A| < 1.2e-9. The prediction sits at 1.4–1.5σ: **not excluded, not detected, central-value sign matches.** Already ~2× tighter than the banked combined bound 1.3e-9 (Hees+ 2016, arXiv:1610.04682, Table 9).

---

## Test 2 — Gaia DR4 wide binaries: the MI-EFE plateau

**The pre-registered prediction.** Velocity-ratio plateau at projected separation s ≥ 7 kAU (fiducial M_tot = 1.5 M_⊙, g_ext = 1.9a₀ = 1.778×10⁻¹⁰ m/s², McMillan-2017-class): **framework MI band γ_v = 1.05–1.10** (upper edge 1.1015 = per-star algebraic MI-EFE with the framework's own ν; lower edge = Banik-style ×0.5 observable dilution — a bracket, not a derivation). Distinct from **MG/AQUAL 1.137–1.139** and **Newton 1.000**. The MI-distinctive signature is the ν′ cross-term suppression below the MG value. Pre-declared: **s = 3–6 kAU is NON-discriminating between MI and MG** (the curves cross near 6–7 kAU); the test lives on the plateau. **a₀-degeneracy stated up front:** a 22% move in a₀ shifts the MI plateau only 1.102 → 1.134, so DR4 tests the ν+EFE prescription, **not** the value 9.36e-11. Deepest caveat, not softened: the per-star law is a prescription — the framework's MI completion is unwritten (trichotomy: local = ghost, field = Cassini/Q₂, nonlocal = anti-MOND sign); the band is a prescription+observable bracket, not a theorem.

Curve table (framework's own ν; full table in `wb_dr4_prereg_framework_curve.py`):

| s [kAU] | Newton | MI lower | MI upper | MG/AQUAL |
|---|---|---|---|---|
| 3 | 1.000 | 1.022 | 1.043 | 1.023 |
| 7 | 1.000 | 1.050 | 1.100 | 1.107 |
| 10 | 1.000 | 1.051 | 1.101 | 1.137 |
| 20 | 1.000 | 1.051 | 1.101 | 1.139 |
| 30 | 1.000 | 1.051 | 1.102 | 1.139 |

**The kill conditions.**
- **Newtonian null** (plateau 1.00 ± 0.03, triple-vetted): framework MI-EFE **dead at wide-binary scales** (≥1.7σ against the band's own lower edge, 3.3σ against the upper). Only σ ≲ 5% makes the null decisive; at σ = 15% it is not a kill. Pre-declared meaning of the null: the sole escape is an unwritten nonlocal MI completion — invoking it post hoc is a declared **retreat** demoting the reframing to galaxy-scale-only phenomenology.
- **Clean MG value** (1.13–1.15 at σ ≲ 4%): framework MI disfavored; survival only as the AeST/MG realization, which **inherits the Cassini Q₂ 3–15σ tension** (Desmond–Hees–Famaey 2024, MNRAS 530, 1781; Park+ 2026, arXiv:2602.17884; `reviews/cassini_quadrupole_framework.py`) — survival in worse shape, and it may not be reframed as a win.
- **≥1.20** (Chae-2023-like boost): kills the framework's ν as written and standard AQUAL-EFE alike.
- **Pre-declared ambiguous zones:** [1.00–1.05] at σ ≥ 5%; [1.10–1.14] at σ ≥ 4%.

**The data + date.** Gaia DR4, release ~Dec 2026; Banik-style plateau sensitivity σ_γ ~ 3–15%; realistic verdict 2027+. Current landscape is contested — Banik+ 2024 (MNRAS 527, 4573; DR3) report Newton, excluding pure-AQUAL at ~16σ, while Chae (2023 ApJ 952, 128; 2024 ApJ 972, 186) claims a boost on overlapping data; the flip hinges on hidden-triple treatment, exactly what DR4 settles. **Most likely failure mode: the Newtonian null.**

**The analysis recipe.** Banik-style ṽ = v_p/v_c statistic with resolved-triple vetting; fit the plateau γ_v on s ≥ 7 kAU only; compare against the four pre-registered levels above. Curves + banked-number reproduction: `wb_dr4_prereg_framework_curve.py` (reproduces 1.05–1.10, MG 1.139, y_ext,N = 1.4647).

**Status:** pre-registered before DR4; verdict pending.

---

## Test 3 — DESI DR3: the a₀(z) decision matrix (Front B geometry gate)

**Canonical footing:** a₀(z) = a₀·√(ρ_DE(z)/ρ_DE(0)), CPL parametrization. The fork a₀(z) = cH(z)E(z)/Z (always rising, w(z)-insensitive, **no bump in any cell**) is disclosed per row and claimed as salvage in none.

**THE PRE-REGISTERED KILL, stated first:** **if DR3 recovers w = −1, a₀(z) = const identically. The bump, the a₀(z=3) suppression, and the growing-ν CMB offset ALL dissolve; Front B dies.** The framework degenerates to constant-a₀ phenomenology with a derived value. No salvage via the cH(z) fork is claimed.

| DR3 outcome | (w₀, wₐ) | a₀(z) bump | z_peak | a₀(z=3)/a₀ | Σ_eff (CMB offset)† | **VERDICT (pre-committed)** |
|---|---|---|---|---|---|---|
| Strong evolving (DESY5-like; DESI DR1+CMB+DESY5, arXiv:2404.03002) | (−0.727, −1.05) | **+6.0%** | 0.351 | 0.648 | +0.032…+0.042 eV | **DISTINCTIVE-ALIVE** |
| Mild evolving (DESI DR2+CMB+Pantheon+, arXiv:2503.14738) | (−0.838, −0.62) | **+3.6%** | 0.354 | 0.775 | +0.021…+0.028 eV | **DISTINCTIVE-ALIVE** (weaker; bump at banked floor) |
| **Null: w = −1** | (−1.0, 0) | none | — | 1.000 | 0 | **DISSOLVED — pre-registered kill** |
| Phantom-only (repr. −1.10, −0.20) | — | none (monotonic declining) | — | 0.671 | +0.030…+0.039 eV | **DEGENERATE** — no bump, no fit-specific signature; worst case for MUSE direction |
| Quintessence-only (repr. −0.90, +0.10) | — | none (monotonic rising) | — | 1.354 | **−0.034…−0.044 eV (sign flips)** | **DEGENERATE** — only cell easing MUSE-rising, but bump gone; Σ_eff sign flip is a testable difference |

† Lensing-kernel-weighted proxy normalized to the banked strong-evolving case, NOT a Boltzmann run (flagged in-script). Negative = lensing excess mimicking negative Σm_ν.

**The distinctive signature is the BUMP** (peak sits exactly at the phantom crossing z_x = (1+w₀)/(−wₐ−(1+w₀))), and only the two crossing scenarios have it. Consistency check (in-script assert): +6.0% / +3.6% at z_peak ≈ 0.35, inside the banked +3.6–8.9% @ z ~ 0.35–0.44 band.

**What DR3 cannot decide (any cell):** (1) the MUSE-DARK III direct-datum tension (Ciocan et al. 2026; read as a₀ RISING — contested/ΛCDM-degenerate per standing) — geometry vs dynamics, independent, survives every row; (2) the √ρ_DE-vs-cH(z)E(z) footing fork; (3) **detection ≠ confirmation: DR3 is an asymmetric test — it can KILL or PERMIT, never confirm** (evolving w(z) is equally evolving-DE ΛCDM); (4) every other front in this document — none touch w(z).

**The data + date.** DESI DR3 BAO+SN+CMB joint fits; expected 2026–27. Script: `desi_dr3_decision_matrix.py`.

**Status:** matrix pre-committed; awaiting DR3.

---

## Test 4 — η(β): cluster anisotropy slide (MI-distinctive, MG/ΛCDM-flat)

**The pre-registered prediction.** Under MI, the empirical η̂ = G·M_bar·a₀/σ⁴ **slides UP with radial anisotropy β**: dln(η̂)/dβ = **+0.75** deep-MOND-normalized (crude ×0.5 dilution → ~+0.4; sign mapping derived in-script: the Newtonian-inferred M_dyn/M_bar counter-slides at −0.56/β). **MG (Milgrom 2014, PRD 89, 024016 virial universality) and ΛCDM: both FLAT.** Source: DOI 10.5281/zenodo.21104820 (η 2.15 iso → 2.8–3.0 at β 0.3–0.5); `eta_beta_first_crude_CLASHVLT.py`.

**The kill condition.** Measured η̂ slope **≤ 0 at 3σ**, with the power stated below, kills the MI η(β) slide. Detection: +0.5…+1.0 at 3σ is MG/ΛCDM-impossible.

**The data + date.** In hand: Biviano et al. 2026 CLASH-VLT (arXiv:2508.05195 + arXiv:2602.15934 stack) — 9 clusters, 0.19 ≤ z ≤ 0.45, per-cluster β_sym(r200) + MAMPOSSt M200; baryons from Donahue+ 2014 (ApJ 794, 136). Decisive: **4MOST CHANCES**, 150 clusters, >1000 members each to 5r200 (arXiv:2411.13655; first light 2025-10-18, ESO ann25007; ops Q1 2026) — verdict ~2029–2031. Power (attenuation included): today's β errors (±0.3) need ~160 clusters (deep slope) / ~560 (diluted); CHANCES-quality (±0.12) needs ~42 / ~145 — **decisive with CHANCES iff the diluted slope is ≳0.4**.

**Status: first real data point BANKED, and it leans against.** Monte-Carlo over all stated errors on the 9 CLASH-VLT clusters: **dln(η̂)/dβ = −0.09 ± 0.20** (and dln(M_dyn,N/M_bar)/dβ = +0.03 ± 0.14). **FLAT** — consistent with MG/ΛCDM at <0.5σ; nominally 4.3σ/4.1σ from the deep-MOND-normalized MI slide and ~2.4σ from the ×0.5-diluted slide. NOT banked as a kill, both ways: (a) r200 sits at g ~ 0.3–1·a₀ and the **intermediate-regime dilution on the framework's own ν is UNCOMPUTED — now the single load-bearing theory number** (if ~×0.2, today's data cannot see the slide at all); (b) σ⁴ was proxied by (M200·E(z))^{4/3}, making the projections algebraically related; (c) MAMPOSSt mass–anisotropy degeneracy; (d) β–M200 correlation (Spearman +0.75) with f_gas–mass trends as a mimic/mask channel. Equally honest: **both projections lean anti-MI, so a straight deep-MOND reading of the slide is already mildly disfavored.** Next steps, in order: compute the ν-dilution; replace the σ proxy with published per-cluster σ_los; pull real M200 posteriors (25% was assumed).

---

## Test 5 — σ-spread: non-adiabatic infall-phase dispersion excess (the MG-impossible discriminator)

**The pre-registered prediction.** MI predicts a **6–13% velocity-dispersion excess for infall-phase (non-virialized) cluster members** in the low-g outskirts; **MG predicts exactly 0** (MG-impossible observable); ΛCDM's tidal-heating confound is separable by **opposite radial trend + hysteresis**: tidal excess grows toward pericenter and persists after passage; the MI excess grows OUTWARD into the low-g zone and vanishes at virialization. Source: banked (cluster-standing ledger); `sigma_spread_survey_forecast.py`.

**The kill condition.** A null (excess consistent with 0) in a phase-binned stack with N/bin ≥ the requirement below kills the MI σ-spread at the corresponding band edge. Honest power correction (supersedes the earlier ~300–1000/bin figure): N/bin = (3/(f·p))²; at phase-classification purity p ~ 0.6, 3σ needs **~1,500/bin (13% edge) to ~6,900/bin (6% edge)**. A detected excess with the tidal radial trend (inward-growing, hysteretic) is NOT a detection — pre-declared.

**The data + date.** Archival NOW: HeCS (Rines+ 2013, ApJ 767, 15) — 58 clusters, ~22k redshifts incl. infall regions; a stacked pilot already exceeds 3σ-N for the 9–13% band (2026, systematics-limited). WEAVE WWFCS (16–20 clusters to ~5R200, on-sky): ~2027–2029. **Decisive: 4MOST CHANCES ~2028–2031** (~300,000 spectra; statistics overpowered, verdict set by systematics). MUSE/LEWIS: wrong tool (cores only) — central-bin control only.

**The analysis recipe.** Caustic phase classification (CIRS-style, Diaferio caustics) → two-bin infall-vs-virialized dispersion difference at fixed radius → radial-trend + hysteresis cut against the CDM tidal mimic. **Prerequisite before any pilot claim (pre-declared): an N-body tidal-heating mock quantifying the residual mimic after the radial-trend cut.**

**Status:** pilot possible now; mock is the gating item; decisive window 2028–2031.

---

## Test 6 — a₀(z) bump, direct dynamical detection (below-floor, long-horizon — stated honestly)

**The pre-registered prediction.** If DR3 lands in a crossing cell (Test 3 rows 1–2), the canonical a₀(z) has a **+3.6–8.9% bump at z ~ 0.35–0.44** (fit-dependent; +6.0%/+3.6% at z_peak ≈ 0.35 for the two 2026 fits), then declines to a₀(z=3)/a₀ = 0.65–0.78.

**The kill conditions.** (1) **w = −1 at DR3: the bump dissolves before it is ever hunted** — this test dies with Test 3's kill row and no dynamical search is then warranted. (2) Conditional on a crossing cell: a dynamical a₀(z) measurement flat or declining through z ≈ 0.35 at <2% precision kills the bump. (3) The MUSE-DARK III direction (a₀ RISING with z, Ciocan et al. 2026) already stands against the canonical declining tail — contested/ΛCDM-degenerate per standing, but it is the current direct datum and it does not favor this prediction.

**The data + date — the honest part.** **No existing survey measures a₀ dynamically to <4% at z ≈ 0.35.** The bump amplitude (3.6–8.9%) sits below the current per-epoch measurement floor (MUSE-class studies carry ~tens-of-% a₀ systematics from M/L and interpolation choices). Plausible carriers — z ~ 0.3–0.5 rotation-curve samples, M-σ evolution, CHANCES-era cluster kinematics vs z — put a realistic first confrontation **>2030, contingent on DR3 permitting**. This test is listed last because it is the least in-hand; it is pre-registered anyway so the prediction cannot be retrofitted.

**Status:** dormant pending Test 3; below current floor; long-horizon.

---

## Integrity clause

The verdicts above are pre-committed as of **2026-07-02, before the data**: before any dedicated INPOP fixed-direction fit, before Gaia DR4, before DESI DR3, before CHANCES/WWFCS cluster spectroscopy, and before any dynamical a₀(z) campaign. Each kill condition was written with the same care and prominence as its detection condition, and **the author accepts the kills as written**: a dedicated ephemeris null at σ_A ≤ 4.3×10⁻¹⁰ kills the s^TX dipole (reading U — the only testable reading); a triple-vetted Newtonian wide-binary plateau at σ ≲ 5% kills the MI-EFE at wide-binary scales, with the nonlocal-completion escape pre-declared as a retreat; w = −1 at DR3 dissolves Front B entirely; an η̂(β) slope ≤ 0 at 3σ with CHANCES-grade power kills the η(β) slide (whose first real data point, banked above, already leans flat-to-anti-MI); a phase-binned σ-spread null at the stated N kills the MG-impossible discriminator; and the a₀(z) bump dies with w = −1 without appeal to the cH(z) fork. No outcome in any table may be reframed after the fact: ambiguous zones are pre-declared ambiguous, MG-collapse outcomes carry the inherited Cassini Q₂ 3–15σ tension and are pre-declared survival-in-worse-shape, and a hit inside any band confirms the prescription tested — not more. Detection claims will not be advanced from tests this document marks DEGENERATE, non-diagnostic, or below-floor.