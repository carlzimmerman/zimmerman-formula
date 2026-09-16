# G129 — THE tSZ OBSERVING PROPOSAL

**The wave-6 prediction as a real, pre-registered measurement** — G113's zero-parameter
Compton-y profile of the 12 X-COP clusters, with targets, prediction, instrument,
exposure/SNR, falsifiers, controls, pipeline, and verdicts.

**Filed 2026-09-15. Lane G129 (wave 9).**
**Deliverable: this file + `G129_tsz_proposal.py` / `.out` / `G129_results.json` (committed and pushed).**

> **STATUS: READY TO RUN — no telescope time required.** All inputs are public today
> (Planck HFI maps + y-maps; ACT DR5/DR6 maps and the Coulton+24 arcminute y-map; SO maps
> as they land; X-COP profiles committed in this repo and public on Vizier). The decision
> rules (F1/F2, the band windows, the χ² convention) are fixed here, **before the maps are read**.

**Built on (all committed):** G113 `G113_tsz_prediction.py/.out/.json` (P7, the y-profile,
11/11), G095 (the T-ratio closed form), the X-COP ingests `real_research/data/xcop/`
(G050/G057 loaders; Ettori+19 `xcop_r500_ettori2019.json`), G105 (T(r) md5-verified vs the
official release), KEPLER_GRADE_CLUSTER_PREDICTIONS.md (P1–P7), WAVEBOARD.md (wave 6 landing,
wave 9 dispatch). Every per-cluster number below is reproduced by `G129_tsz_proposal.py`
(gated digit-for-digit against G113's own build, 5/5 checks PASS).

**Constants (G113's, verbatim):** canonical a0 = 9.3619e-11 m/s², μ = 0.6, X = 0.76 (μ_e =
2/(1+X)), σ_T = 6.6524587e-29 m², m_e c² = 8.1871058e-14 J, T_CMB = 2.7255 K, flat LCDM
H0 = 67.4, Ωm = 0.315; kpc/arcmin from D_A(z).

---

## 1. THE TARGETS — the 12 X-COP clusters

Sky positions **read from the committed X-COP release FITS headers**
(`real_research/data/xcop/<name>/*_hydro_mass.fits`, HDU 1: RA/DEC) — the same files
G050/G057/G095/G113 load. Redshifts from the committed Ettori+19 ingest (`z` per G113).
R500/M500 from the same ingest; r_M, θ_M, θ_500, y0 from G113's build (re-computed here,
bit-identical to G113's own build).

| cluster | RA (J2000) [deg] | Dec (J2000) [deg] | z | R500 | M500 | r_M | θ_M | θ_500 | y0 (pred.) | ACT band |
|---|---|---|---|---|---|---|---|---|---|---|
| A1644 | 194.3015 | −17.4097 | 0.0473 | 1054 kpc | 3.48e14 | 273 kpc | 4.73′ | 18.24′ | 1.90e-05 | in |
| A1795 | 207.2196 | +26.5896 | 0.0622 | 1153 | 4.63e14 | 342 | 4.58′ | 15.45′ | 7.57e-05 | out |
| A2029 | 227.7342 | +5.7444 | 0.0773 | 1423 | 8.82e14 | 521 | 5.72′ | 15.62′ | 2.31e-04 | in |
| A2142 | 239.5862 | +27.2294 | 0.0909 | 1424 | 8.95e14 | 568 | 5.39′ | 13.50′ | 1.89e-04 | out |
| A2255 | 258.2160 | +64.0631 | 0.0809 | 1196 | 5.26e14 | 398 | 4.19′ | 12.59′ | 3.91e-05 | out |
| A2319 | 290.3028 | +43.9450 | 0.0557 | 1346 | 7.31e14 | 580 | 8.61′ | 19.98′ | 1.66e-04 | out |
| A3158 | 55.7180 | −53.6277 | 0.0597 | 1123 | 4.26e14 | 333 | 4.63′ | 15.63′ | 4.38e-05 | in |
| A3266 | 67.8434 | −61.4297 | 0.0589 | 1430 | 8.80e14 | 448 | 6.32′ | 20.15′ | 8.41e-05 | in (edge) |
| A644 | 124.3574 | −7.5087 | 0.0704 | 1230 | 5.66e14 | 388 | 4.64′ | 14.70′ | 9.65e-05 | in |
| A85 | 10.4594 | −9.3029 | 0.0555 | 1235 | 5.65e14 | 406 | 6.05′ | 18.40′ | 7.97e-05 | in |
| RXC1825 | 276.3355 | +30.4367 | 0.0650 | 1105 | 4.08e14 | 312 | 4.01′ | 14.21′ | 4.05e-05 | out |
| ZW1215 | 184.4219 | +3.6557 | 0.0766 | 1358 | 7.66e14 | 405 | 4.48′ | 15.03′ | 6.14e-05 | in |
| **median** | — | — | 0.0622 | 1230 | 5.66e14 | 402 | **4.7′** | **15.5′** | **7.77e-05** | 7/12 |

*ACT band column*: planning assignment for the arcminute-resolved inner profile, using the
publicly released ACT coadd coverage (DR5 note: dec ∈ (−63°, +23°); A3266 sits at the south
edge). Clusters marked "out" get their inner profile from Planck 5–10′ beams alone (their
θ_M = 4.0–8.6′ is near or above the Planck beam — the r_M crossing is only partially resolved
for them) and from SO where its 40%-sky footprint lands. The exact per-cluster ACT/SO hit
count is to be confirmed from the public maps' noise/hit maps at run time; nothing in the
decision rules depends on it (Planck covers all 12 for the phantom zone).

## 2. THE PREDICTION TO TEST — G113's y-profile

The thermal SZ parameter projects the electron pressure: y(b) = (σ_T/m_e c²) ∫ n_e k_B T_e dl.
The framework fixes **both** factors from the committed cluster structure, zero free parameters:

- **density**: n_e = ρ_gas/(μ_e m_p) from the committed X-COP cumulative gas mass;
- **temperature**: the **G095 closed form per radius** — T_vir(r) = μ m_p G M_HSE(<r)/(2 k_B r),
  the virial temperature of the *total* enclosed mass (the per-radius extension of the
  registered G095 identity, median hse = 0.99, 0.053-dex scatter) — **the G095 T-extension
  outside R500 is exactly what the outer profile tests**;
- the μ/μ_e cancellation gives the closed-form pressure P_e = (μ/2μ_e) ρ_gas G M_HSE(<r)/r —
  **no temperature input at all**;
- beyond the data: gas envelope ρ ~ r^−q (q measured per cluster; P2 band 2.0–2.5) and the
  total mass continued by the deep-regime phantom ρ_ph = A/r² (A = √(G M_b a0)/(4πG)), so
  T_vir → T_inf = 2 T_floor = 3.6 keV-class (median 3.63 keV; the G130 outer asymptote).

**The committed numbers (G113, 11/11):**

| quantity | prediction | classic cluster reading |
|---|---|---|
| central Compton parameter y0 | median **7.77e-05** (range 1.90e-05–2.31e-04); 1.62× the baryon floor (pressure-weighted G095 factor); core-dominated (88% within 1.05 R500) | (amplitude = consistency, see §8) |
| inner dimensionless profile | beta-FORM, **β_eff = 0.42** (10/12 well-constrained; median fit RMS 0.008 dex; A1644/A2255 flat cores under-constrained) | β ∈ [0.5, 0.8], β = 2/3 typical |
| outer slope at 2 R500 | **−1.44** (band from the P2 q-band: −1.5…−1.0; per cluster slope = −(q−1) ± 0.4, 9/12) | −(6β−1) ≈ −3 |
| **phantom-zone pressure signature** | **y/y(classic β=2/3, r_c=0.15 R500) = 40× at R500, 105× at 2 R500** (per cluster 2.6–474×); window-average +1.50 dex over [r_M, 2R500]; slope gain +1.56/decade vs −3 | isothermal collapse |
| outer thermal pressure | held up by the still-growing total mass: T_vir → T_inf = 2 T_floor; falloff = the gas envelope alone, y ~ b^−(q−1) | — |

The physics in one sentence: **the dark sector's mass keeps growing beyond R500
(phantom ρ ~ r^−2 + dust envelope), so the virial temperature the gas feels stays at the
T_inf isotherm and the outer Compton pressure falls no faster than the gas envelope —
the SZ channel sees the phantom through the temperature it imposes on the gas.**

What is NOT predicted (by honesty, G113 V3): y0 from first principles (the free-dust
normalization is open); the EFE cap's exact line (an active cap would *steepen* the outer
profile back toward the beta family — the measurement discriminates capped vs uncapped,
G108's window); any per-cluster power law.

## 3. THE INSTRUMENT — which survey measures which scale

The angular map of the prediction (median cluster): θ_M = 4.7′ (the deep-regime crossing,
start of the phantom zone), θ_500 = 15.5′, 2θ_500 = 31′. G113's window: y(1′)/y0 = 0.97,
y(5′)/y0 = 0.66, y(10′)/y0 = 0.35.

| survey | channels | beam (FWHM) | noise floor | role in this proposal |
|---|---|---|---|---|
| **ACT DR6** | f090, f150, f220 | 2.2′ / **1.4′** / 1.0′ | ~10 μK·arcmin median combined depth (19,000 deg²; deep fields lower) | the **inner profile**: θ < θ_M = 4.7′ resolved, the r_M crossing, the β-form core out to ~18′; bin SNR 18–34 (median, per-channel) |
| **SO LAT** | 93 / 145 GHz | 1.4′ | ~6 μK·arcmin white noise (40% sky, Science-Goals baseline) | same inner role with ~1.7× the ACT S/N where the footprint lands |
| **SO deep** (SAT-class) | 93 / 145 GHz | 1.4′ | **~1.6 μK·arcmin class** (the deep fields) | the high-S/N inner branch: central SNR 54–529 (per cluster, per-channel) |
| **Planck HFI** | 100 / 143 / 217 / 353 GHz | 9.7′ / **7.2′** / 4.9′ / 4.9′ | 77.4 / 33 / 46.8 / 154 μK·arcmin (2018 I Table 4) | the **phantom zone**: [θ_M, 2θ_500] = [4.7′, 31′] median, all 12 clusters (all-sky); 217 GHz = the tSZ-null control; 353 GHz = dust |
| the y-maps | — | — | — | ACT component-separated y-map over ~13,000 deg² (Coulton et al. 2024, public); Planck MILCA/NILC y-maps (public) |

**The resolution needed.** To resolve the r_M crossing (4.7′) and the core radius of the
β-form (r_c ≈ 0.37 θ_500 ≈ 5.8′ median): beam ≲ 1.4′ — ACT/SO. To *integrate the phantom
zone* with maximum S/N per bin: 5–10′ beams (Planck) — the big beams average more sky per
noise element. The two surveys are complementary; their bin sets overlap in 3–8′ for the
joint-fit consistency control (§6).

**The y → ΔT_CMB conversion** (ΔT = T_CMB·y·g(x), x = hν/kT_CMB, g = x coth(x/2) − 4):

| channel | g(x) | ΔT per 1e-6 of y | σ per beam |
|---|---|---|---|
| 93 GHz (SO) | −1.572 | −4.28 μK | 1.52 (deep 1.6) / 5.69 (LAT 6) μK |
| 98 GHz (ACT f090) | −1.527 | −4.16 μK | 6.04 μK |
| 100 GHz (Planck) | −1.508 | −4.11 μK | 10.64 μK |
| 143 GHz (Planck) | −1.040 | −2.84 μK | 6.07 μK |
| 150 GHz (ACT f150) | −0.953 | −2.60 μK | 9.49 μK |
| 217 GHz (Planck) | −0.008 | −0.02 μK | 12.69 μK (the null control) |

*(This is the "−2 μK-class per 1e-6 y" conversion quoted in the dispatch, stated exactly:
−2.6 to −2.8 μK per 1e-6 y at 143–150 GHz; −4.1 to −4.3 at 93–100 GHz. Relativistic SZ
corrections at kT ≈ 5–9 keV are O(5–10%) on the amplitude — a stated systematic on the
consistency test, negligible for the shape/decision channels.)*

**Exposure statement.** ACT and Planck are at **end-of-survey depth — the data already
exist**
(Planck HFI full mission public since 2013/2015/2018; ACT DR5 since 2020, DR6 since 2025).
SO reaches the quoted floors at its advertised survey end state. **No new observing time is
requested**; the "exposure" is the archived map depth, and the per-bin S/N below is what the
full maps deliver. For SO the same thresholds apply verbatim at whatever depth the public
maps carry at run time (all S/Ns scale linearly with σ_noise).

## 4. EXPOSURE / SNR — the forecast (per cluster and per radial bin)

Per-channel (no component-separation penalty; the ~1.4× ILC penalty stated as the
assumption — all S/Ns scale linearly).

**Central beam-averaged S/N per cluster:**

| cluster | ACT f150 | Planck 143 | SO LAT (6) | SO deep (1.6) |
|---|---|---|---|---|
| A1644 | 5.2 (in band) | 8.8 | 14.4 | 54.0 |
| A1795 | (out of band) | 20.2 | 52 | 196 |
| A2029 | 51.3 (in band) | 49.6 | 138 | 529 |
| A2142 | (out) | 48.3 | 123 | 460 |
| A2255 | (out) | 17.4 | 30 | 112 |
| A2319 | (out) | 64.4 | 125 | 462 |
| A3158 | 11.8 (in band) | 15.6 | 33 | 121 |
| A3266 | 23.3 (in band) | 35.3 | 66 | 241 |
| A644 | 25.2 (in band) | 28.9 | 70 | 259 |
| A85 | 21.0 (in band) | 26.9 | 59 | 217 |
| RXC1825 | (out) | 14.7 | 30 | 112 |
| ZW1215 | 17.1 (in band) | 22.6 | 48 | 176 |
| **median** | **20.0 (7 in-band)** | **24.8** | **60** | **206** |

**Per radial bin (sample-median S/N; Planck over all 12, ACT over the 7 in-band):**
ACT bins (arcmin):
0–1′: 20.5 · 1–2′: 22.5 · 2–3′: 25.9 · 3–4.5′: 33.6 · 4.5–6′: 32.4 · 6–8′: 30.5 ·
8–10.5′: 23.5 · 10.5–14′: 20.9 · 14–18′: 18.5.

Planck 143 bins (arcmin):
0–4′: 22.6 · 4–8′: 15.7 · **8–12′: 10.2 · 12–17′: 9.3 · 17–23′: 7.8 · 23–31′: 6.6 ·
31–40′: 5.4** — the phantom-zone window [θ_M, 2θ_500] sits at bin S/N 6.6–15.7 with bright
clusters to 30–60 (A2029: 43.97/29.2/19.0/14.3/10.8/10.2/8.1; A2142 similar; weakest
cluster A1644 still 8.5/7.7/7.2/7.6/6.7/6.2/5.8 — its profile is *flat*, q = 2.28).

**The decision power this buys.** The outer log-slope over [θ_500, 2θ_500] from the two
endpoint bins has σ_s ≈ 0.32 per cluster (conservative 2-bin; a multi-bin fit over the four
outer bins ~0.15), i.e. **0.09 pooled over the 12** → the F1 line (−2 vs the predicted
−1.44, Δ = 0.56) separates at ~2σ per cluster and **~6σ pooled**; the F2 line (the flat
edge, band half-width 0.4) at ~1.5σ per cluster, **~5σ pooled** (see §5). The full-shape
separation at the forecast noise: **median combined χ² = 3087 vs the classic β = 2/3 profile**
(3197 vs β = 0.7; common-y0 normalization; 12/12 clusters > 25 = 5σ-class). Caveats
registered: A644 (steepest envelope, q = 3.8) carries only ~2.6× hold-up — its outer
Planck bins are dim (17–23′: S/N 1.2, 23–31′: 0.27); its constraining power sits in the
inner/ACT bins and in the χ² fit over the full curve, and the sample-median statements do
the heavy lifting, exactly as G113 registered.

**Assumptions box (all stated, all linear in σ_noise):** per-channel noise floors as listed;
ILC component-separation penalty 1.4×; Gaussian beams; no residual CMB contamination term
(controls below); the χ² convention (common y0 normalization, shape-only); slope errors are
2-bin conservative; bin-to-bin noise uncorrelated.

## 5. THE FALSIFIERS (pre-declared; decision rules fixed before the maps are read)

- **F1 — kills the G095 T-extension.** The measured log-slope over θ ∈ [θ_500, 2θ_500] is
  **steeper than −2.0 at ≥ 3σ** (per cluster; the pooled 0.09 error makes the sample-level
  line ~6σ): the extension of the G095 identification (T = the virial temperature of the
  total mass, per radius) *outside R500* is killed, and the framework at cluster scale
  reduces to G095's averaging-aperture statement (G113 V3's decision line, made quantitative
  here: the separable Δ = 0.56 in slope).
- **F2 — kills the phantom-zone pressure profile.** The measured slope is **flatter than
  the registered per-cluster band [−(q−1)−0.4, −(q−1)+0.4] at ≥ 3σ** (i.e. slope >
  −(q−1)+0.4): the T_inf = 2 T_floor isotherm × gas-envelope reading — the phantom-zone
  pressure *as predicted* — is killed (the outer pressure would exceed what the envelope +
  isotherm allow: a different hold-up mechanism, or a rising T_vir).
- **PASS window.** Sample-median slope in (−1.7, −0.9) (G113 V2a's registered band) with
  per-cluster values inside their bands at ≤ 2σ; window-average y/y(classic) over
  [r_M, 2R500] consistent with the predicted +1.5 dex and the 40×/105× ratios (the ratios'
  model-convention nature is stated in §8).
- **Amplitude (consistency, non-decisive by construction).** y0 measured vs predicted within
  the ~0.05-dex HSE budget (G113 V1e); a violation indicts the X-COP gas/calibration, not
  the framework.
- **Capped-vs-uncapped register.** A profile in the pass window discriminates the uncapped
  reading from the EFE-capped one (which steepens back toward the beta family); a separate
  attribution of *which* dark mechanism holds the pressure up is not claimed (§8).

## 6. THE CONTROLS

1. **Beta-model fit comparison.** Fit the free family y = y0b (1+(θ/θ_c)²)^(1/2−3β) over
   b ∈ (0.05, 0.8) R500 (G113's recipe): the framework predicts β_eff = 0.42 (median,
   10/12 well-constrained) vs the classic 0.5–0.8 band; the β-fit's *extrapolation* to
   2R500 vs the measured outer bins is the model-independent closure (a fitted inner beta
   that extrapolates into the measured outer bins is the most forgiving competing model —
   the honest alternative to the β = 2/3 reference).
2. **Cluster subtraction for the Planck beams.** The 5–10′ beams see neighbouring clusters
   and LSS: point-source masks (PSZ2/ACT catalogs), iterated subtraction of neighboring
   clusters from the y-map before profiling, local-background annuli at 2.5–3.5 θ_500 for
   the zero level; the 217-GHz null map monitors CIB/dust leakage; 353 GHz dust templates
   and CO masks enter the ILC (§7).
3. **Survey jackknives.** Planck half-mission maps; ACT day/night and array splits;
   pipeline cross-checks MILCA vs NILC vs matched filter (NEMO-class); 100 noise
   realizations for the bin covariance and the Δχ² distribution.
4. **Resolution-overlap joint fit.** ACT/SO bins (1–8′) and Planck bins (3–40′) overlap in
   3–8′; the joint fit enforces cross-survey consistency and bounds the beam-transfer
   systematic.
5. **The 217-GHz tSZ-null channel.** g(217) ≈ −0.008: the null map must show zero signal at
   the cluster position at the cluster's own scale — a null check on the y estimate itself.

## 7. THE FULL PIPELINE

1. **Data products needed.** Planck HFI PR4 100/143/217/353 GHz maps + masks and masks for
   y; ACT DR5/DR6 f090/f150/f220 maps + inverse-variance maps (LAMBDA); the Coulton et al.
   2024 arcminute y-map (~13,000 deg²) and 1.4′ y-map noise levels; SO survey maps (when public);
   PSZ2/ACT cluster catalogs for point-source and neighbor subtraction; the X-COP gas +
   hydrostatic-mass profiles (committed ingests in this repo); this file's target table.
2. **y-map extraction per survey.** Per survey: ILC/NILC component separation over its
   frequency set (CMB, dust, synchrotron, CO; 217 GHz null monitor; 353 GHz dust templates),
   producing y maps + per-pixel noise maps + masks; cross-check with map-space matched
   filtering (Melin-class NEMO) — a pipeline cross-validation, not a choice.
3. **Radial profile.** Inverse-noise-weighted annular means at the cluster position, bins
   as in §4; each model profile convolved by the survey beam transfer function; bin
   covariance from the noise maps; 100 noise realizations for the covariance/Δχ².
4. **Model comparison (χ² per prediction).** Per cluster, per bin set: **M1** = the G113
   zero-parameter curve (this file's numbers — no fitted parameters); **M2** = classic
   β = 2/3, r_c = 0.15 R500, common y0; **M3** = the free β-family self-fit over
   (0.05, 0.8) R500 extrapolated. Report χ², Δχ², BIC per cluster and pooled; apply the
   F1/F2 decision lines and the pass window to the M1 residuals; register the verdict
   text in this repo's ledger format (per-cluster table + sample-median rows + verdicts).
5. **Decision record.** Any F1/F2 firing is a kill exactly as pre-declared; no post-hoc
   rescue, no amplitude rescues (the amplitude channel is registered non-decisive).

## 8. VERDICTS

**V1 — the proposal is complete.** TARGETS (12/12 with sky positions from the committed
FITS headers, z from the Ettori+19 ingest), PREDICTION (y0 7.77e-5 median; slope −1.44 at
2R500; 40×/105× at R500/2R500 vs classic β = 2/3; the G095 T-extension as the object of the
outer-slope test), INSTRUMENT (ACT/SO ~1.4′ inside θ_M — 4.0–8.6′ per cluster, median 4.7′; Planck 5–10′ on the
phantom zone; per-cluster footprint check), EXPOSURE/SNR (per-cluster central S/N tables,
per-bin S/N tables, slope decision power 0.09 pooled, χ² separation 3087 median), FALSIFIERS
(F1/F2 with 3σ rules), CONTROLS (β-fit comparison, Planck-beam cluster subtraction, null
channels, jackknives, overlap joint fit), PIPELINE (4 stages). Executable as written on
public data today. **5/5 checks PASS** (`G129_tsz_proposal.py`/`.out`).

**V2 — the SNR estimate: which cluster, which bin, the forecast.** The weakest and the
strongest brackets: **A1644** (y0 = 1.90e-5) — central S/N 8.8 (Planck 143), 5.2 (ACT),
54 (SO deep 1.6 μK·arcmin); Planck phantom-zone bins 8.5/7.7/7.2/7.6/6.7/6.2/5.8 across
0–40′ — measurable everywhere because its profile is flat (q = 2.28), y(23–31′)/y0 = 0.26.
**A2029** (y0 = 2.31e-4) — central 49.6 (Planck), 51 (ACT), 529 (SO deep); Planck bins
44.0/29.2/19.0/14.3/10.8/10.2/8.1. Sample-median per-bin S/N: ACT 18–34 per bin (7 in-band
clusters); Planck phantom-zone bins 6.6–15.7; bright-cluster outer bins 30–60. The decision
quantities: slope error 0.09 pooled (0.32 conservative 2-bin per cluster; ~0.15 multi-bin)
→ F1 at ~6σ, F2 at ~5σ pooled; median χ² separation vs β = 2/3 of 3087 (12/12 clusters
> 25). Scaling: all S/Ns ∝ 1/σ_noise; the 1.4× ILC penalty is the stated assumption. The
one registered weak spot: A644's outer bins (steep envelope, minimal hold-up) — its
constraining power is the full-curve fit plus the sample median, not its own outer bins.

**V3 — does this proposal, when run, DECIDE the phantom-zone pressure signature — and who
can run it?**

> **DECIDES, WITH QUALIFICATION.** (1) **What it decides cleanly:** the per-cluster outer
> Compton shape on θ ∈ [θ_500, 2θ_500] ≈ [15.5′, 31′] at Planck 143 GHz bin S/N
> 10.2/9.3/7.8/6.6 (median across the four outer bins; bright clusters 10–60), with a
> conservative 2-bin slope error of 0.32 per cluster (~0.15 multi-bin), i.e. 0.09 pooled —
> the F1 line (steeper than −2 at θ_500 → G095 extension killed) separates at ~6σ pooled;
> the F2 line (flatter than the registered [−(q−1)±0.4] band → the phantom-zone pressure
> reading as registered is killed) at ~5σ pooled; the shape-separation χ² vs the classic
> β = 2/3 profile is 3087 (median; 12/12 > 25). The inner profile (θ < θ_M = 4.7′, the
> β-form core with β_eff = 0.42 vs 0.5–0.8) is ACT/SO-resolved at central S/N ~20 (median,
> 7 in-band clusters; SO deep to ~200) and per-bin S/N 18–34. **(2) What it decides only
> partially:** (i) the 40×/105× "phantom-zone multiples" are ratios vs the *classic*
> β = 2/3, r_c = 0.15 R500 convention — the physically scored quantities are the absolute
> beam-convolved per-cluster curves and the slope, and the decision window is the
> registered band, not the ratio's magnitude; (ii) A644 (q = 3.8) has only ~2.6× hold-up —
> for it the signature is a factor, not two decades, and its outer bins are dim: the
> sample-median statement does the work, as registered; (iii) a pass-window profile
> confirms the *outer pressure hold-up* but does not by itself prove the phantom density
> profile ρ = A/r² or identify the holding mechanism (phantom vs dust envelope vs EFE-cap
> boundary) — the measurement discriminates the capped from the uncapped reading (G108's
> window) and leaves the amplitude as a consistency test within the ~0.05-dex HSE budget.
> So: **it decides the existence and the quantitative form of the outer thermal-pressure
> hold-up — the phantom zone's pressure signature as defined by G113 — and it cannot, by
> itself, decide which dark mechanism provides it.** (3) **Who can run it:** any SZ
> analyst. All inputs are public today (Planck HFI maps + MILCA/NILC y-maps; ACT DR5/DR6
> maps on LAMBDA and the Coulton+24 13,000-deg² y-map; PSZ2; X-COP profiles; public tools
> healpy/NILC/fgbuster, pixell, matched-filter codes). No telescope time is requested —
> this is a pre-registered analysis whose decision rules are fixed here before the maps
> are read. Realistic cost: 2–4 weeks of postdoc-level analysis per survey; the Planck
> branch alone already closes the outer-shape decision; the ACT/SO branch adds the
> arcminute inner resolution.

---

*All numbers from the committed ingests and the committed G113 artifact, reproduced by
`G129_tsz_proposal.py` (in-process code-level gate vs G113's own build, 0.000e+00; vs the
committed JSON at the documented storage class ≤1.16e-4; 5/5 checks PASS). A FAIL would be a
finding. The committed G113 JSON's own stale-regeneration noise (max 1.16e-4 in y0 vs its
current script) is registered in the gate note of `G129_tsz_proposal.py`.*