# XSTRAT_SPEC — x-Stratified Matched Filter for the Directional-EFE Test (Lane W3)

**Banked 2026-07-16, BEFORE any WALLABY per-side data touches the filter.**
Companion code: `xstrat_filter.py` (this directory; exit 0, smoke-tested).
Banked inputs (all FROZEN / read-only): `zimmerman-formula/real_research/reviews/directional_efe_2026/laneA_predictions_results.json` (the signed BVP A-map), `prep_2026/aligned_firing/fire_aligned_n16.py` (predictor + stack + permutation null, imported verbatim — no re-implementation, no convention drift).

> **FIREWALL (top of every output, per the ground rules):** At WALLABY scale
> (N~237 per-side-capable galaxies) the achieved sensitivity at AQUAL amplitude
> is ~1–1.5 σ (n=16 gave 0.32 σ; √(237/16)=3.85×). **Neither pre-registered
> kill condition** (3-σ AQUAL-vs-Branch-B separation; N~1157 canonical footing
> / ~1424 alt footing) **can trigger** at N~237. Kill-condition language in this
> lane appears only as "cannot trigger". Everything below is bank-the-method;
> any number produced at N~237 is EXPLORATORY.

---

## 1. The frozen strata

Stratification variable: **r = x/e = g_bar/g_ext** — the ratio of the outer-rotation-curve internal acceleration to the environmental field. r is **a0-footing-independent** (a0 cancels), so stratum membership does not move between the canonical (9.36e-11) and alt (1.13e-10) footings. It **does** move between the Chae max-clustering and no-clustering e_N brackets (e changes), so both brackets are always run.

| Stratum | Frozen boundary | Banked-map sign |
|---|---|---|
| **DEEP** | r < 1.0 | **REVERSED**: attractor side **SLOWER** |
| **TRANSITION** | 1.0 ≤ r < 5.0 | positive, crossing-adjacent suppression + the map's amplitude peak (peak at r ≈ 2) |
| **OUTER** | r ≥ 5.0 | clean positive: attractor side **FASTER**, amplitude monotone-declining in r |

**Where the boundaries come from (computed, not assumed).** The lane brief proposed deep: x < 2e. The banked signed map `A_fw_gamma0_pct` actually crosses zero at **x*/e = 0.72–0.97** — six independent crossings on the banked grid, computed by `xstrat_filter.py` at import time with the same interpolation rules as the banked interpolator (linear in e along x-rows; linear in log x down e-columns):

| direction | at | x*/e |
|---|---|---|
| along e | x=0.05 | 0.745 |
| along e | x=0.10 | 0.720 |
| along e | x=0.20 | 0.807 |
| along log x | e=0.10 | 0.785 |
| along log x | e=0.20 | 0.764 |
| along log x | e=0.30 | 0.969 |

A deep boundary at 2e would therefore **mix both predicted signs inside "deep"** (galaxies with 0.8e < x < 2e are on the positive side of the crossing). **Adjusted and frozen: R_DEEP = 1.0**, the conservative outer envelope of the banked crossings. The transition/outer edge stays at **R_OUTER = 5.0**: by r ≈ 5 the map is past its r ≈ 2 amplitude peak and sign-clean. The banked verbal statement "attractor side faster for x ≳ 2e" is the same map — 2e sits inside TRANSITION, already positive. The script **asserts at runtime** that every banked crossing lies in the frozen bracket (0.70, 1.00) and refuses to run otherwise.

## 2. The stratified statistic

Identical to the pre-registered stack, computed separately per stratum S:

    Ahat_S = Σ_{i∈S} (A_i p_i / s²) / Σ_{i∈S} (p_i² / s²)

with the banked predictor p_i = A_map(x_i, e_i)·G(γ_i)·cos(ψ_i) (the **signed** map — the reversal is inside p_i, not inside the stratification). Errors: bootstrap over galaxies + the banked isotropic-direction permutation null (ψ and γ recomputed per draw), reused verbatim from `fire_aligned_n16.py`. Strata with n < 2 are reported EMPTY/UNDERSIZED — no number fabricated.

## 3. Sign predictions per stratum per theory

Because the signed map carries the reversal, **E[Ahat_S] is stratum-uniform per theory** — the stratification tests whether the *data's sign flips where the map's does*:

| Theory | DEEP (r<1) | TRANSITION | OUTER (r≥5) |
|---|---|---|---|
| **AQUAL/QUMOND-class MG** | **+1** — data must show attractor side **slower** | +1 (suppressed raw amplitude) | +1 — attractor side faster |
| **Branch B (elastic medium)** | **+0.304** (natural w; 0.24 Cassini-max) — **same reversal**, w-suppressed | +0.304 / 0.24 | +0.304 / 0.24 |
| **Pure MI** | **0** | **0** | **0** |

**Why DEEP is the discriminator:** any isotropic systematic averages to Ahat = 0 in every stratum (the permutation null enforces this). A *directional* contaminant that mimics "attractor side faster" (tidal lopsidedness, ram pressure toward an attractor, etc.) produces Ahat > 0 in OUTER but **Ahat < 0 in DEEP** — it cannot know to flip sign at the map's crossing. A positive Ahat_DEEP together with positive Ahat_OUTER is an **MG fingerprint no isotropic (or rigid-directional) systematic can fake**. Branch B shows the same fingerprint at w-suppressed amplitude; pure MI shows nothing anywhere. (Amplitude separation AQUAL-vs-Branch-B remains out of reach at N~237 — see FIREWALL — but the *sign pattern* is a qualitative check that comes free.)

## 4. Joint 2-parameter (amplitude, reversal-depth) fit

    A_i = α · p_i(β),   p_i(β) = A_map(x_i, β·e_i)/100 · G(γ_i) · cos(ψ_i)

β rescales the effective external field, sliding the crossing to x* ≈ 0.8·β·e. χ²(α,β) = Σ(A_i − α p_i(β))²/s²; α profiled analytically; β on the **frozen** log grid [0.25, 4.0], 33 points. Targets: **AQUAL (α=1, β=1)**; **Branch B (α=0.304 natural / 0.24 Cassini-max, β=1)** — Branch B suppresses amplitude, not depth; **pure MI (α=0, β unidentified)**. β is identifiable only with DEEP+TRANSITION coverage; on an outer-dominated sample the β profile is flat (reported as such, expected).

## 5. THE SIGN TRAP (flagged in every lane)

Pre-registered convention: **A_i = 2(v_rec − v_appr)/(v_rec + v_appr)** — receding side first — paired with ψ measured from the **receding-side** kinematic major axis, so p_i > 0 predicts attractor-side-FASTER for r ≳ 2. **`perside_extractor.py`'s pilot printout used the OPPOSITE ordering** A = 2(v_app − v_rec)/(v_app + v_rec). Every WALLABY feed into this filter MUST convert (A_prereg = −A_extractor) **and the conversion must be verified by hand on at least one galaxy from the raw mom1 map** before any stratified number is quoted. A silent flip inverts the DEEP-stratum physics conclusion exactly — it would turn the MG fingerprint into its own refutation. The n=16 smoke-test sample is WHISP-derived and already convention-correct (recomputed from v_rec, v_appr inside `fire_aligned_n16.py`).

## 6. Smoke test result (n=16, banked aligned-firing sample)

As expected, the n=16 sample is **outer-dominated — that is fine and is the point**: r = x/e spans 4.6–38.7, so DEEP is empty in every config and TRANSITION holds at most one galaxy (UGC05721, r=4.6, maxclu bracket only). WALLABY's N~237 is what populates DEEP/TRANSITION. All four config combinations run (both a0 footings × both clustering brackets):

| Config | DEEP | TRANSITION | OUTER |
|---|---|---|---|
| canonical, maxclu | EMPTY | n=1 UNDERSIZED | n=15: Ahat = +2.59 ± 3.69 (Z=+0.70, p2=0.153) |
| canonical, noclu | EMPTY | EMPTY | n=16: Ahat = +23.7 ± 24.9 (Z=+0.96, p2=0.050) |
| alt, maxclu | EMPTY | n=1 UNDERSIZED | n=15: Ahat = +2.82 ± 4.15 (Z=+0.68, p2=0.160) |
| alt, noclu | EMPTY | EMPTY | n=16: Ahat = +26.5 ± 28.5 (Z=+0.93, p2=0.053) |

Consistent with the banked full-sample firing (Ahat = +2.95, p2 = 0.061, EXPLORATORY); the noclu rows have near-zero predictors (huge σ) — a bracket statement, not a signal. The joint (α,β) fit runs and the β profile is **flat in every config (span Δχ² ≤ 0.4)** — exactly the advertised behavior on an outer-dominated sample; α_hat is wild with σ-sized errors at n=16, reported straight, EXPLORATORY. **None of these numbers can touch the kill conditions (cannot trigger — see FIREWALL).**

Machine-readable results: `xstrat_filter_results.json` (carries FIREWALL + SIGN_TRAP strings, frozen constants, banked crossings, per-stratum stacks, β profiles).
