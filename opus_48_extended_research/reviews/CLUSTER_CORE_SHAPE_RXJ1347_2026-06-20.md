# CLUSTER CORE-SHAPE — first-pass data confrontation on RX J1347 — verdict: GAS-TRACKING (2026-06-20)

**Workflow:** `cluster-core-shape-firstpass` (wao0tzzq3; 6 agents, pull→build→confront→synthesis; ~449k tokens;
REAL published profiles). Builds the framework-footing core residual M_res(r) = M_lens − M_MOND(a0=9.36e-11)
for RX J1347.5−1145 from archival data and reads whether it is gas-tracking (shared gap) or galaxy-tracking
(IGIMF remnants → ~half closure). This is the decisive observable from CLUSTER_STACK_AND_DECISIVE_TEST.

**HEADLINE (both ways — the framework-UNFAVORABLE outcome, reported straight): GAS-TRACKING. The first-pass
archival data says the core residual is a smooth ~10×-gas diffuse component, NOT stellar remnants — closing the
IGIMF escape by SHAPE and landing the no-particle stack at the LOWER (~45%) end, not the favorable ~54-65%.
The residual is the shared MOND cluster gap.** ROBUST to every systematic pushed framework-favorable; held
back from "final" only by RX J1347 being a merger (the relaxed cross-check needs a single matched cluster).

## The real profiles (recovered + cite-checked)
- **M_lens(r):** Umetsu+2016 (ApJ 821, 116; CLASH SL+WL) NFW M200c=34.2e14 M☉, c=3.09. **Caught a unit trap**
  (the Table-2 "h⁻¹" header does NOT apply as written — using it would have inflated M_lens 1.43× and
  manufactured a larger residual). M(<100kpc)=3.0e13, M(<300)=2.1e14, M(<500)=4.7e14 M☉.
- **M_gas(r):** Gitti+2007 (A&A 472, 383; XMM double-β) validated 3 ways. M_gas(<420kpc)=4.69e13 M☉.
- **M_star(r):** BCG+ICL de Vaucouleurs 1.5e12 M☉, Re=40 kpc (generous; the least-constrained component).
- **M_HSE(r):** flagged NOT recoverable below ~250 kpc (XMM bins give spurious negative core mass).

## The framework-footing residual (M_res = M_lens − M_MOND, a0=9.36e-11)
| r (kpc) | M_lens | M_MOND | M_res | M_res/M_gas | M_res/M_star |
|---:|---:|---:|---:|---:|---:|
| 50 | 8.1e12 | 1.7e12 | 6.4e12 | 33.8 | 7.6 |
| 100 | 3.0e13 | 4.7e12 | 2.5e13 | 19.3 | 22.6 |
| 200 | 1.05e14 | 1.9e13 | 8.6e13 | 10.0 | 64.7 |
| 300 | 2.09e14 | 4.6e13 | 1.6e14 | 7.1 | 116 |
| 500 | 4.68e14 | 1.2e14 | 3.4e14 | 5.3 | 235 |

**Inner log-slope d ln M_res/d ln r = 1.81 — almost identical to M_lens (1.82), far from the flat M_star
(0.29).** The decisive discriminator: **M_res/M_star RISES ~30× outward (8 → 235)** — the residual is
ANTI-correlated with the cuspy stellar light, the OPPOSITE of the Bullet/galaxy-tracking signature. M_res/M_gas
stays smooth O(5–30). **The residual is a ~10×-gas diffuse halo, not remnants → GAS-TRACKING (FPS shape).**

## Robustness — SOLID, does not flip
Every dominant systematic pushed framework-FAVORABLE and the read held: (1) deflating M_lens by the documented
2× WL-vs-HSE/merger ratio keeps M_res positive + gas-like, M_res/M_star still rises ~27×; (2) the merger boost
and non-thermal HSE bias both INFLATE the residual (true could only be smaller, not differently-shaped); (3)
single-NFW UNDER-predicts the SL core M_2D by ~2–3.4× inside 120 kpc → inner M_res is a LOWER bound,
reinforcing gas-tracking; (4) **the IGIMF-remnant escape is CLOSED** — sourcing M_res from remnants needs a
stellar M/L rising 5× (50 kpc) → 165× (500 kpc), impossible for any light-tracking population; boosting the BCG
M/L can't help because the residual is centrally DEFICIENT relative to the stellar cusp. The convention-
independent slope match (1.81 vs 1.82) is the robust core.

## The honest caveat (why it's "leaning-preliminary," not final)
RX J1347 is a known MERGER, and a clean RELAXED cross-check could not be done on a SINGLE matched cluster (the
recovered relaxed data were A383 lensing + A2029 gas — *different* objects). So the headline rests on the
merger target. The slope diagnostic is convention-independent, but the dedicated confirmation is to run the
SAME matched pipeline on a genuinely relaxed, XRISM-pinned target (A2029) — exactly what the banked
CLASH_XRISM_SHAPE_PROPOSAL delivers (XRISM kills the η~2 HSE branch + pins inner T(r)).

## Standing
The first real data confrontation lands GAS-TRACKING: in the core, baryons+MOND source only **16–31%** of
M_lens; the rest is an irreducible smooth ~10×-gas residual = the **shared MOND cluster-core gap** (the classic
factor-~2 residual MOND leaves in rich cores), NOT framework-specific, NOT closed by IGIMF remnants. The
no-particle stack sits at the ~45% (lower) end. **The favorable galaxy-tracking / ~half-closure scenario is
NOT supported by this preliminary archival pass.** NEXT: the matched relaxed (A2029/XRISM) read to confirm
it's not a merger artifact. Quarantine held (a0=9.36e-11 input, never asserted derived). Both ways: gas-
tracking reported straight at full weight; the lone merger caveat flagged honestly; no reflexive dismissal of
the unfavorable result, no manufactured galaxy-tracking.

---

# Core-Shape Data Confrontation — RX J1347.5-1145: First-Pass Verdict

## 1. Real profiles recovered (and what was/was not publicly recoverable)

All three mass components for the PRIMARY target **RX J1347.5-1145** (z=0.451) were recovered from published profiles:

- **M_lens(r)** — Umetsu+2016 (ApJ 821, 116; CLASH joint SL+WL+magnification). Deprojected NFW M200c=34.2e14 Msun (physical), c=3.09. Verified self-consistent against Table 3 overdensity masses; **caught and corrected a unit-convention trap** (the Table-2 "h^-1" header does NOT apply to RXJ1347's number as written — using it as h^-1 would have inflated M_lens by 1.43x and manufactured a larger residual). M_lens(<100kpc)=3.0e13, M(<300kpc)=2.1e14, M(<500kpc)=4.7e14 Msun.
- **M_gas(r)** — Gitti+2007 (A&A 472, 383; XMM double-beta DDg1 density + deprojected T). Validated against three independent SZ/X-ray gas masses (Pointecouteau, Schindler). M_gas(<420kpc)=4.69e13 Msun.
- **M_star(r)** — BCG+ICL de Vaucouleurs profile, total 1.5e12 Msun, Re=40 kpc (Postman+2012-class CLASH HST photometry, generous normalization). **This is the least-constrained component** — recovered as a reasonable profile, not a tabulated CLASH fit; bounded both ways below.
- **M_HSE(r)** — Gitti+2007 NFW-anchored; flagged that the RXJ1347 core HSE below ~250 kpc is genuinely NOT recoverable from XMM bins (gives spurious negative core mass; Gitti impose a 5th-order T polynomial to avoid it).

**Not recoverable as a single matched cluster:** a clean RELAXED comparison with matched gas+lens+star from ONE object. The recovered relaxed data were A383 (lensing, Umetsu+2016) and A2029 (gas, Lewis-Buote-Stocke 2003) — DIFFERENT clusters — so the relaxed cross-check could not anchor the headline. **The headline rests on the merger target RXJ1347.**

## 2. Framework-footing residual M_res(r) and its SHAPE

On the framework footing (a0=9.36e-11, dS-Unruh nu g_obs=sqrt(g_bar^2+g_bar*a0)), M_bar=M_gas+M_star, M_MOND from M_bar, **M_res = M_lens - M_MOND**:

| r (kpc) | M_lens | M_MOND | M_res | M_res/M_gas | M_res/M_star |
|--------:|-------:|-------:|------:|------------:|-------------:|
| 50  | 8.1e12 | 1.7e12 | 6.4e12 | 33.8 | 7.6 |
| 100 | 3.0e13 | 4.7e12 | 2.5e13 | 19.3 | 22.6 |
| 200 | 1.05e14| 1.9e13 | 8.6e13 | 10.0 | 64.7 |
| 300 | 2.09e14| 4.6e13 | 1.6e14 | 7.1 | 116 |
| 500 | 4.68e14| 1.2e14 | 3.4e14 | 5.3 | 235 |

**Inner log-slopes (50-300 kpc):** d ln M_res/d ln r = **1.81**, almost identical to d ln M_lens/d ln r = 1.82, vs d ln M_gas = 2.69 and the nearly-flat d ln M_star = **0.29**.

**SHAPE = GAS-TRACKING (FPS shape).** The residual is a smooth, extended component of order **~5-30x the gas mass**. The decisive discriminator: **M_res/M_star RISES ~30x outward (8 -> 235)** — the residual is anti-correlated with the cuspy stellar light, the OPPOSITE of the Bullet/galaxy-tracking signature. M_res/M_gas instead stays O(5-30) and varies smoothly. The residual looks like a ~10x-gas diffuse halo, not stellar remnants.

## 3. Systematic robustness — SOLID, does not flip

Every dominant systematic was pushed in the framework-favorable direction and the read held:
- **WL-vs-HSE / merger bias:** deflating M_lens by up to 2x (the documented Bradac SL+WL-vs-HSE ratio 2.07-2.45) keeps M_res positive everywhere and still gas-like (M_res/M_gas spans only ~7x), while M_res/M_star still rises ~27x. No flip to star-tracking.
- **Merger boost + non-thermal HSE bias** both INFLATE the residual — true residual could only be smaller, not differently-shaped.
- **Strong-lensing core excess:** single-NFW under-predicts observed M_2D by ~2-3.4x inside ~120 kpc, so the inner M_lens (hence inner M_res) is a LOWER bound — reinforces gas-tracking.
- **IGIMF-remnant escape CLOSED:** sourcing M_res from stellar remnants would require a M/L rising from ~5x (50 kpc) to ~165x (500 kpc) — impossible for any light-tracking population. Boosting the BCG M/L cannot help because the residual is centrally DEFICIENT relative to the stellar cusp.

The convention-independent slope match (M_res slope 1.81 vs M_lens 1.82, far from flat stars) is the robust core of the verdict.

## 4. Implication for no-particle closure

Gas-tracking lands the stack at the **LOWER (~45% gas) end**, NOT the favorable ~54-65% galaxy-tracking end. In the core, baryons+MOND source only **M_MOND/M_lens = 0.16-0.31** (30-500 kpc); the remainder is the irreducible ~10x-gas smooth residual = the classic SHARED MOND rich-cluster gap, not closed by remnants and not framework-specific.

## 5. Honest verdict + next step

**This preliminary archival pass favors GAS-TRACKING** — the shared irreducible-gap reading, framework-UNfavorable relative to the half-closure hope. I did not manufacture galaxy-tracking; the data simply do not show the residual following the stellar light, and the IGIMF escape is closed by the rising-M/L test. **Caveat that keeps this preliminary, not final:** the matched read sits on the MERGER cluster RXJ1347; a single-cluster RELAXED confirmation could not be assembled from the recovered tables.

**Single next step:** run the identical matched pipeline on **A2029** (relaxed, XRISM-pinned non-thermal pressure <=2%, X-ray/lensing c-concordance) with its own lensing+gas+star — i.e. execute the banked CLASH/XRISM core-shape proposal, which removes the dominant core-HSE systematic the merger target leaves open. Until then: gas-tracking-leaning-preliminary. (Quarantine held: a0/Z/kappa used as inputs, never asserted derived; reported the shape the data show, both ways.)