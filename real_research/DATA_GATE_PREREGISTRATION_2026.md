# Pre-registration — the Zimmerman framework's imminent data gates

**Committed 2026-06-26, before the data.** This document fixes — in advance and unambiguously — what the
framework predicts at the next three near-term data gates, what each survey can actually measure, and the
explicit CONFIRM and KILL lines, stated symmetrically. It exists so that no verdict can be reverse-engineered
after the fact.

**Framework.** `a₀ = c²·√(Λ/32π) = cH_Λ/Z = 9.36×10⁻¹¹ m/s²` — a dS–Unruh modified-inertia MOND-class
gravity result. **a₀ is a FORCED SCALE; its O(1) coefficient is FREE** (corpus standing: the one-parameter
reading). So the thing under test at these gates is the *normalization* 9.36×10⁻¹¹, which is convention-degenerate
with ≈7.5×10⁻¹¹…1.8×10⁻¹⁰ across {interpolation × M/L} per the footing rule.

**Footing rule (judge on the framework's own terms).** a₀ = 9.36×10⁻¹¹; Υ ≈ 0.70; the framework's own
dS–Unruh interpolation `g_obs = √(g_bar² + g_bar·a₀)`; the declining √ρ_DE a₀(z) branch. Verify a "fails"
claim as rigorously as a "works" claim. Where a gate tests MOND-vs-ΛCDM rather than the framework specifically,
say so plainly.

All predicted numbers below were recomputed from scratch on 2026-06-26 (numpy); all survey specs were fetched
from primary sources (cited inline). Where a spec could not be confirmed it is flagged.

---

## GATE 1 — Euclid DR1 weak-lensing radial-acceleration relation (WL-RAR)

**Vehicle.** A Brouwer+2021-style lensing RAR built from Euclid DR1 LensMC (`DpdSheLensMcFinalCatalog`) +
Metacalibration (`DpdSheMetaCalFinalCatalog`) shear, photo-z (`DpdPhzPfOutputCatalog`), and baryonic photometry
(`DpdMerFinalCatalog`) over ~1900 deg² (~2× KiDS-1000). Benchmark: Brouwer+2021 (KiDS-1000, arXiv:2106.11677) —
~1M KiDS-bright lenses, 259,383 isolated, 15 g_bar bins from ~1e-9 down to ~1e-15 m/s², +0.10 dex added for the
ESD→RAR conversion.

### (1) Predicted signal (number + uncertainty)

Framework dS–Unruh interpolation `g_obs = √(g_bar² + g_bar·a₀)` at a₀ = 9.36×10⁻¹¹. Predicted WL-RAR curve
(log₁₀ g_obs, m/s²) at the Brouwer bins (recomputed):

| g_bar (m/s²) | log₁₀ g_obs (framework) |
|---|---|
| 1e-15 | −12.514 |
| 1e-13 | −11.514 |
| 1e-12 | −11.012 |
| 1e-11 | −10.492 |
| 1e-10 | −9.857 |
| 1e-9  | −8.981 |

- **Deep-MOND log-slope** `d(log g_obs)/d(log g_bar) = 0.5000` EXACTLY (the lensing/saturation tail
  g_obs → √(g_bar·a₀), α_∞ = 0.5). **Identical to regular MOND**; a₀ enters only as normalization.
- **The a₀ = 9.36e-11 vs regular-MOND a₀ = 1.2e-10 discriminating signal:** **0.054 dex (≈12–13%)** in g_obs
  at fixed g_bar in the deep regime (verified: −0.054 dex at g_bar=1e-15, −0.053 at 1e-12, −0.028 at the knee
  1e-10, −0.005 at 1e-9). Equivalently a **+0.108 dex (+28.2%)** shift of the knee position along the g_bar axis.
- **Uncertainty on the prediction itself:** a₀'s value is a forced scale with a free O(1), so the framework's
  honest predicted band is one-parameter, not zero — the 9.36e-11 normalization *is* the quantity under test, and
  is convention-degenerate with 7.5e-11…1.8e-10 across {interpolation × M/L} (footing rule).

### (2) Survey + date

**Survey precision (REAL, fetched).** Euclid DR1 LensMC method (arXiv:2606.20829, the official DR1 cosmic-shear
method; specs measured on the 63 deg² Q1 catalogue and carried to DR1): **n_eff = 26 arcmin⁻² at I_E < 24.5**
(75 at I_E < 27); multiplicative bias |m| < 1% (pre-launch sims; no DR1 real-data m yet); additive
**c₁ = (−2.35 ± 0.08)×10⁻³, c₂ = (1.79 ± 0.08)×10⁻³**; DES-Y3 cross-val **δm = (−5 ± 8)×10⁻²**, consistent with
no bias. DR1 area ~1900 deg² footprint (~1700 deg² conservative WL-complete). KiDS-1000 benchmark: ~1000 deg²,
n_eff ~ 8 arcmin⁻². Statistical S/N gain ≈ √((1700×26)/(1000×8)) ≈ **2.35×**, scaling the ~0.2–0.4 dex KiDS
lowest-bin RAR stat error to ~0.10–0.17 dex. **BUT the wall is not statistics:** (a) an irreducible +0.10 dex
ESD→RAR conversion floor (Brouwer adds it explicitly); (b) the **dominant systematic = baryonic/stellar mass
M\* ± 0.2 dex**, which shifts g_obs by 0.5×0.2 = **±0.10 dex** in the deep regime, is **common-mode across bins,
does NOT beat down with √N, and is area-independent**. Brouwer's own abstract: future surveys "(such as Euclid)"
distinguish MG and ΛCDM "IF systematic uncertainties in the baryonic mass distribution around galaxies are
reduced."

**Timeline (CORRECTED from the earlier ROUTINE read).** Per telescoper.blog 2026-06-16 + cosmos.esa.int Euclid
DR1-timeline: the **Nov-2026 first tranche is "DR-Foundation" = LE1/LE2 raw + calibrated IMAGES/point-source
catalogues ONLY** over ~1900 deg². **The LE3 cosmic-shear products (the calibrated shear maps/catalogs the WL-RAR
needs) do NOT ship in November** — they arrive with the **full DR1 mid-2027 (the blog says "probably June")**.
Direct quote: *"there will be no official cosmology results from Euclid DR1 until mid-2027 at the earliest."* So the
WL-RAR vehicle is a **mid-2027 product at the earliest**, and the downstream Brouwer-style VAC paper lands months
after that (realistic ~late-2027 to 2028). **The watch trigger is the first ≥1000 deg² WL-complete shear+photo-z
catalog, NOT the Nov-2026 image drop.** How much of 1900 deg² is WL-complete is gated on external ground-based
photo-z (some ice-contaminated data invalidated).

### (3) CONFIRM and KILL (symmetric)

**CONFIRM — MOND-vs-ΛCDM (the achievable test):** the DR1 WL-RAR reproduces the deep-MOND tail with
**log-slope 0.50 ± ~0.05** and lies systematically ABOVE the ΛCDM/NFW + abundance-matching (BAHAMAS-style)
prediction at g_bar < 1e-12, matching KiDS-1000 (lensing g_obs follows √(g_bar·a₀) ~2–3 decades below the knee).

**CONFIRM — framework a₀ (the hard test; only if the baryonic systematic is beaten to <0.05 dex):** the fitted
normalization is consistent with a₀ = 9.36e-11 (knee/normalization within ~±15%) AND the data prefer 9.36e-11
over 1.2e-10 — which requires total per-bin g_obs error ≪ 0.054 dex across several deep bins.

**KILL — MOND-class (stated as plainly as CONFIRM):** the deep-regime log-slope departs from 0.5 at >3σ (no
Milgromian saturation tail), OR g_obs → g_bar (tracks unity/NFW, no lensing excess) at g_bar < 1e-12. Either kills
MOND-class gravity, the framework included.

**KILL — framework a₀ VALUE (softer; only bites if baryonic systematic <~0.05 dex):** the fitted RAR
normalization is robustly inconsistent with 9.36e-11 — e.g. centered on 1.2e-10 at >3σ on the framework's own
dS–Unruh interpolation + Υ~0.70, OR intrinsic scatter so large (>0.3 dex) that no single a₀ fits.

**HONEST caveat (both ways):** a "prefers 1.2e-10" DR1 result is NOT a clean kill — 9.36e-11 sits inside the
convention spread (7.5e-11…1.8e-10), and the 0.054 dex separation is **below** the 0.10 dex baryonic-mass
systematic. So "wrong a₀ from DR1" is, by construction, most likely a convention/systematic artifact, not a real
falsification.

### (4) Distinctive / shared, and will it decide?

**MOND-shared.** **Partially decisive — and only for the shared question.** DECISIVE as MOND-vs-ΛCDM: the 2.35×
statistical gain over KiDS-1000 sharpens the 2–3-decade deep-MOND lensing tail and slope-0.5 saturation to high
significance, a genuine anti-CDM result the framework would share and be confirmed by. **INCONCLUSIVE as a
framework-a₀ test:** the discriminating signal (0.054 dex) is below the dominant baryonic-mass systematic
(0.10 dex, common-mode, √N-immune, area-independent), so DR1 alone cannot decide 9.36e-11 vs 1.2e-10. Deciding a₀
would need the CGM/baryon profile pinned to <0.05 dex (the explicit Brouwer caveat) — not in the DR1 deliverables.
**NET: expect CONFIRM on the shared front, INCONCLUSIVE (non-diagnostic) on the framework-distinctive a₀ value.**

---

## GATE 2 — Gaia DR4 wide-binary gravity test

**Vehicle.** Chae-2023 / Hernandez normalized-velocity-vs-separation methodology. Tests the framework's z=0
deep-MOND enhancement: does the relative-velocity-vs-projected-separation profile show a low-acceleration boost
above Newtonian at internal g_N ≪ a₀ (separations s ≳ 3 kAU), through the transition scale s_t = √(G·M_T/a₀)?
Statistic: dimensionless ṽ = v_2D / √(G·M_T/s_2D), binned in s_2D, vs Newtonian and MOND orbit-population models.

### (1) Predicted signal (number + uncertainty)

**Transition scale** s_t = √(G·M_T/a₀) (recomputed):

| M_T (M_sun) | s_t framework (a₀=9.36e-11) | s_t regular-MOND (1.2e-10) |
|---|---|---|
| 1.0 | 7961 AU | 7031 AU |
| 1.5 | **9750 AU** | 8611 AU |
| 2.0 | 11258 AU | 9943 AU |

The framework's s_t is **+13.2% wider** than regular MOND's (√(a₀_MOND/a₀)−1); equivalently the onset of the boost
sits at larger separation. Circular Newtonian velocity at s_t (M_T=1.5): **v_N ≈ 369 m/s**.

**The signal is EFE-SUPPRESSED, not the isolated +41%.** The Milky-Way external field at the Sun is
**g_ext ≈ 1.86 a₀ ≈ 1.74e-10 m/s²** (above a₀) → the wide binary is EFE-dominated. On the framework's own footing
(reproduced from project_wide_binary_prediction.py):
- standard/sharp μ (the framework's favored MI-EFE reading): **velocity boost +2.6%** (γ_v=1.026, γ_g=1.05);
- simple μ: **+13.4%** (γ_v=1.134, γ_g=1.29).

**PINNED BAND: +2–11% velocity boost** at the widest separations (γ_v ≈ 1.03–1.13; gravity-boost
γ_g = γ_v² ≈ 1.05–1.29). The MI-EFE most-Newtonian reading favors the **LOW end** γ_g ≈ 1.05–1.10 (velocity
~+2–5%). Absolute: at s_t (M_T=1.5), the boost is **~10 m/s (+2.6%) to ~50 m/s (+13.4%)**. Shape: γ→1 (Newtonian)
at s ≪ 3 kAU where g_int ≫ a₀; rises through s ~ 3–10 kAU; **plateaus** (not peaks) at the EFE-capped boost for
s ≫ s_t (the EFE prevents the full √2). **Uncertainty dominated by the interpolation function (factor ~5 spread,
2.6% vs 13%), NOT by a₀'s value.**

### (2) Survey + date

**Survey precision (REAL, fetched + computed).** Gaia DR4 astrometry (ESA science-performance, T_factor=0.749 for
the 5.5-yr baseline): parallax σ ≈ 9 µas at G=13, 14 at G=14, 22 at G=15; proper-motion σ_µ ≈ 0.54·σ_par. For the
nearby (d~100–200 pc) bright (G~13–15) wide-binary sample this gives **per-star transverse-velocity error
≈ 2.3–11.3 m/s** (recomputed: 2.30 / 5.38 / 11.26 m/s at G=13/14/15, d=100/150/200 pc), hence **per-pair
relative-velocity error ≈ 3.3–15.9 m/s**. This is **below the predicted per-pair boost** (~10–50 m/s at s_t) and
far below it as a population statistic: with N~1e4–1e5 cleaned pairs (Chae DR3: 26,615 within 200 pc; Banik: 8,611
within 250 pc), the astrometric stat floor on the mean boost is **~0.01–0.03% velocity** — negligible.
**CONCLUSION: Gaia DR4 is NOT astrometry-limited; it is TRIPLE-CONTAMINATION-limited.** DR4's real gain is the
**epoch-astrometry Keplerian/acceleration solutions that detect hidden third stars directly** — the systematic
that currently splits Chae (+1.4 boost) from Banik (16–19σ Newtonian). Realistic sensitivity ~3–15% on the boost
is set by residual triple modeling, not photon noise.

**Timeline.** **Gaia DR4 public release CONFIRMED 2 December 2026** (ESA Cosmos; 5.5-yr baseline, ~400 TB, includes
epoch astrometry + non-single-star/wide-binary orbital solutions). Wide-binary gravity papers are downstream VACs,
not in the release — expect first DR4-based Chae/Banik/Hernandez results **~Q1–Q3 2027**, gated on the
triple-rejection VAC, not on Dec-2026 itself.

### (3) CONFIRM and KILL (symmetric)

**CONFIRM:** a robust low-acceleration boost in ṽ vs s_2D of **+2–11% velocity** (γ_g ≈ 1.05–1.29) that (a)
**SURVIVES DR4 direct triple-rejection** (epoch-astrometry acceleration flagging), (b) appears in BOTH the
Chae-style normalized-velocity-profile AND the Banik/Pittordis ensemble-histogram pipelines on the same cleaned
sample, and (c) has onset near s ~ 3–10 kAU consistent with a₀ = 9.36e-11 (the framework's s_t is ~13% wider than
regular-MOND's). The framework-FAVORABLE outcome is the **low end** γ_g ≈ 1.05–1.10. Note: a Chae-magnitude anomaly
(γ_g ~ 1.4, +15–20% velocity) is ABOVE the framework's own EFE-suppressed central value — read as
**supportive-of-premise, not a clean central-value match.**

**KILL:** a **hard Newtonian null** — ṽ vs s_2D consistent with γ = 1.00 ± ~0.03 (boost < ~3% velocity,
γ_g < 1.05) across s > 3 kAU, in a DR4 sample where triple contamination has been **directly rejected via epoch
astrometry** (removing the Banik-vs-Chae modeling escape hatch), at the ~3–15% sensitivity the cleaned sample
affords. That excludes even the framework's LOW-end +2.6% and locally falsifies the central derived result
(z=0 deep-MOND enhancement).

**Both-ways caveat:** the current pre-DR4 field LEANS skeptical (Banik 16–19σ Newtonian, Pittordis–Sutherland,
"No evidence for MOND"), but every skeptical result is contested precisely on triple/eccentricity modeling — the
exact systematic DR4 epoch astrometry resolves. So the kill is only clean **AFTER** direct triple rejection;
a pre-rejection null is non-diagnostic in either direction.

### (4) Distinctive / shared, and will it decide?

**MOND-shared** (it tests whether local MOND is real, not MI-vs-MG — the boost is shared by modified-inertia and
modified-gravity at this footing; the MI-vs-MG distinction within a "yes" is below floor). **Partially decisive,
asymmetric.** The **KILL side is decisive:** a hard post-triple-rejection Newtonian null (<3% boost) locally
falsifies the framework's central z=0 deep-MOND enhancement — a genuine kill-door. The **CONFIRM side is weaker:**
a detected +2–11% boost confirms the MOND premise the framework shares, but the interpolation spread (2.6% vs 13%)
means it cannot pin the framework's specific central value, and a₀ = 9.36e-11 vs 1.2e-10 differ by only ~13% in
s_t — within the triple-systematic floor. So DR4 can KILL the premise cleanly but can only CONFIRM it broadly,
not pin a₀.

---

## GATE 3 — Gaia DR4 asteroid astrometry / gravity-sector SME s̄^μν (s^TX boost-dipole)

**Vehicle.** Gaia DR4 Solar-System-object (asteroid) astrometry feeding gravity-sector SME coefficient fits (with
extended INPOP/EPM planetary ephemerides). Tests the framework's **preferred-frame realization**: the same a₀/|a|
that makes it MOND induces a computable gravitational s̄^μν background; the single tightest channel is the
**s^TX boost-dipole, CMB-apex-locked**.

### (1) Predicted signal (number + uncertainty)

The framework's preferred-frame reading predicts a **CMB-apex-locked negative s^TX dipole** at
**≈ 8.7×10⁻¹⁰ at Saturn-a** (the a₀/2|a| per-body value; corpus value 8.68e-10, Saturn). Sky direction fixed at
the CMB apex (l = 264°, b = +48°). The tensor structure (component ledger w5k0n9hd0): s^TT O(1) absorbable,
s^TJ dipole O(β), s^<JK> quad O(β²), trace = 0 — **no O(1) un-β-suppressed anisotropic observable**; binding
bounds test only β-suppressed projections. **This s^TX channel is the live SME test** (it is COM/orbital, not
self-energy enhanced; it was correctly UNTIED from the α2 self-energy knob — α2 itself is ~1e-13, ~1e6× safe, NOT
the live test). Margin: currently **~1.5× the tightest published bound** (corrected from a banked 9.6×;
preferred-frame/LV, MOND-shared) — LIVE and falsifiable.

### (2) Survey + date

**Survey precision (REAL, partial confirmation).** Confirmed from primary sources (arXiv:1509.06868,
arXiv:1607.07394): Gaia observes ~360,000 asteroids at sub-mas level; a realistic covariance analysis over
~10,000 asteroids within the SME framework (Gaia scanning law) yields **SME-coefficient uncertainties better than
the current best literature estimates**, with the asteroid orbital-element variety beating planetary ephemerides
(8 near-coplanar near-circular planets). **A specific published s^TX numerical reach for Gaia DR4 could NOT be
confirmed** — the existing forecasts (Gaia-SSO papers) quantify the *improvement over current bounds* qualitatively
but do not pin a single DR4 s^TX σ; the ~10⁻¹⁰ next-gen reach is an analysis-stage estimate
(extended INPOP/Cassini + Gaia-SSO, ~2028–32), not a released number. **Flagged: spec is order-of-magnitude, not a
confirmed survey deliverable.**

**Timeline.** Gaia DR4 asteroid astrometry ships **2 December 2026**, but the s̄^μν fit is a downstream
ephemeris-analysis product combining Gaia-SSO with extended INPOP/EPM — realistic **~2028–32, analysis-limited**.
BepiColombo does NOT bind this channel.

### (3) CONFIRM and KILL (symmetric)

**CONFIRM:** a next-gen gravity-sector fit resolves a **CMB-apex-locked negative s^TX dipole consistent with
≈8.7×10⁻¹⁰ at Saturn-a** (the per-body a₀/2|a| pattern), in the fixed sky direction.

**KILL:** a next-gen s^TX fit reaching ~10⁻¹⁰ whose central value is **robustly inconsistent with 8.7×10⁻¹⁰** (or
inconsistent with the CMB-apex direction / per-body |a| scaling) → kills the preferred-frame realization.

**Both-ways caveat:** this is preferred-frame/LV physics the framework shares with any AeST-class preferred-frame
completion; a null here constrains the *realization*, and a confirmation does not uniquely select the framework
over other preferred-frame MOND theories.

### (4) Distinctive / shared, and will it decide?

**MOND-shared (preferred-frame).** **Likely INCONCLUSIVE in the near term, LIVE long-term.** Ships Dec-2026 but
the deciding s̄^μν fit is ~2028–32 and analysis-limited; the published DR4 s^TX reach is not yet a confirmed
number (flagged). The channel is genuinely live (~1.5× the tightest bound) and falsifiable, but on a slower clock
than Gates 1–2 and shared with other preferred-frame completions. It is the **more decisive near-term *gravity-side*
test** among the SME channels, but it is not framework-unique.

---

## SUMMARY

**The single most decisive gate for the framework specifically is NOT in this batch.** It is the **a₀(z) decline /
high-z (z≳3) BTFR-offset sign** — the framework's one genuinely framework-DISTINCTIVE prediction (discs ≈ −7% in V,
−0.033 dex below the z=0 BTFR; a₀(z=3) ≈ 0.74·a₀(0) tracking declining √ρ_DE). That test is **later** (JWST+ALMA
high-z kinematics; DESI DR3 gate ~2026–27, ELT/HARMONI early-mid 2030s) and is **hostage to DESI w(z)**: the whole
distinctive content dissolves to ordinary constant-a₀ MOND if w→−1. It is named here so the pre-registration is
honest about where the sharp knife lives.

**What these three near-term gates CAN settle:** Euclid DR1 (mid-2027+) and Gaia DR4 wide binaries (Dec-2026
release, ~2027 analysis) can decisively test the **MOND-vs-ΛCDM premise the framework shares** — the lensing RAR's
slope-0.5 deep-MOND tail above NFW, and the z=0 wide-binary low-acceleration boost (KILL side decisive after triple
rejection). The Gaia DR4 asteroid s^TX channel keeps the preferred-frame realization live (~1.5× the tightest
bound) toward a ~2028–32 verdict.

**What they CANNOT settle:** none of the three is framework-DISTINCTIVE. Gate 1's framework-a₀ discriminator
(0.054 dex) sits below the 0.10 dex baryonic-mass systematic, so DR1 cannot decide 9.36e-11 vs 1.2e-10 — and a
"prefers 1.2e-10" outcome is a convention/systematic artifact under the footing rule, not a kill. Gate 2's
interpolation spread (2.6%–13%) and the ~13% a₀-driven s_t difference are within the triple-systematic floor, so
DR4 can confirm the MOND premise but not pin a₀. Gate 3 is shared with all preferred-frame completions and its DR4
s^TX reach is not yet a confirmed number. **NET, both-ways: expect these gates to sharpen the MOND-vs-ΛCDM case
(which the framework rides) while leaving the framework-distinctive question — a₀'s value and its z-decline —
open and waiting on the high-z BTFR sign + DESI w(z).**

---

### Provenance
- Predicted signals recomputed 2026-06-26 (numpy): WL-RAR curve & 0.054 dex / 0.108 dex offsets; s_t = 9750 AU
  (M_T=1.5) & the +13.2% vs regular-MOND; EFE-suppressed +2–11% boost band; Gaia DR4 per-star v_T error
  2.3–11.3 m/s → per-pair 3.3–15.9 m/s.
- Euclid: arXiv:2606.20829 (LensMC method/specs); telescoper.blog 2026-06-16 + cosmos.esa.int Euclid DR1-timeline
  (Nov-2026 DR-Foundation = images only, LE3 shear mid-2027, "no cosmology results until mid-2027").
- Gaia DR4: cosmos.esa.int/web/gaia/dr4 (2 Dec 2026, epoch astrometry, non-single-star/wide-binary solutions);
  ESA science-performance model (T_factor=0.749).
- Gaia SME asteroid reach: arXiv:1509.06868, arXiv:1607.07394 (qualitative improvement confirmed; specific DR4
  s^TX σ NOT confirmed — flagged).
- Footing & standing: MEMORY.md, real_research/data_watch/ROUTINE.md, the a₀(z) paper (Zenodo 10.5281/zenodo.20737162).
