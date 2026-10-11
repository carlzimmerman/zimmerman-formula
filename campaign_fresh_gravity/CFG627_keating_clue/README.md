# CFG627: the "Keating clue". Four new radio results mapped onto the framework

**Lane type.** Read and think only. There are no simulations and nothing was downloaded. The only script is `cfg627_numbers.py`
(< 1 s, one process; `.out`, `.json`, plus a `CFG627_MUTATE=1` control that passes). The 1024³ CFG596 job was not touched.

**Prompt.** A public post (about 2026-10-11) pointed to four results:
1. FRB 20240304B, the farthest localized FRB (Science 2026);
2. NASA's Webb release on the same burst;
3. CHIME's standalone 21 cm auto-power detection;
4. a MeerKAT HI intensity-mapping result (ApJL 2026).

**Bottom line (read this first).** None of the four results is a decisive test of the framework.
- The framework's distinctive prediction (a₀ tracks ρ_DE, so a₀(z) is FLAT if Λ is constant, against the rival a₀ ∝ H(z)) is not
  reachable from any of them. The FRB host is a ~10⁷ M☉ dwarf with no kinematics, and its predicted dispersion is far below any
  JWST resolution floor. None of the HI results measures BAO.
- The FRB dispersion-measure (DM)–z relation tests a baryon budget and background. Those are the same in the framework as in any
  standard budget, because it uses the same Ω_b, Ω_c/Ω_b = 5.364 and a constant ρ_DE.
- The CHIME auto-power is the only lensing-free probe here of the small-scale clustering behind the growth tension. But its amplitude is
  degenerate with Ω_HI b_HI, and the framework's own predicted k-shape changes sign between our engines, so it cannot be frozen until
  CFG596 settles which engine is used.
- **Ranked first by decisiveness × feasibility:** an FRB baryon-partition check of the census placement R4 (feasible now, low
  decisiveness).
- **Ranked second:** a CHIME shape test, gated on CFG596's z = 1 gravitating P(k).

κ = ½ is fitted. The footings are 9.36e-11 (canonical) and 1.13e-10 (alt), never pooled. Cold energy mass is required. This is not
"theory closed", and nothing here says the data favour the framework.

---

## 1. What each result measures (sources read 2026-10-11)

**Provenance rule.** These are WebFetch/WebSearch read-outs. A number marked **[abs]** was read from abstract text. One marked
**[tab]** is reported by the fetch summariser as coming from a paper table. Everything else is **[PROVISIONAL]**: it came from a
summariser or press text, not from a table read here. Treat every number as provisional until it is checked against the PDF.

### R1. FRB 20240304B (Caleb et al. 2026, Science; arXiv:2508.01648)
- **Redshift:** z = 2.148 ± 0.001 **[abs]**. This is a JWST NIRSpec spectroscopic redshift of the host.
- **DM:** 2458.20 ± 0.01 pc cm⁻³ after scattering correction **[tab]** (2462.48 as detected).
- **Milky Way terms:** DM_MW,ISM = 28.1 (NE2001) and 20.8 (YMW16) **[tab]**; DM_MW,halo = 40 **[tab]**, with a systematic of
  "a few tens".
- **DM_cosmic + DM_host/(1+z):** ≈ 2330 pc cm⁻³ **[PROVISIONAL]**. The host term is not separated. The excess above the median
  cosmic DM at this z is ≈ 550 **[PROVISIONAL]**.
- **Foreground structures:** the sightline passes ~1.1 Mpc from the Virgo centre, with DM_Virgo ≈ 235 **[tab]**. This is a model
  estimate from X-ray data, not a measurement. A z = 0.311 group at 240 kpc adds ≈ 33 ± 13 **[tab]**.
- **Redshift from the Macquart relation alone:** 2.8 (+0.6/−1.2), with a 95% range of 1.63–3.40 **[PROVISIONAL]**. The measured z
  falls inside it.
- **Magnetic and scattering terms:**
  - RM is −55.6 ± 0.5 rad m⁻² **[tab]** (about −550 in the rest frame);
  - the mean line-of-sight B is about 28 nG in magnitude **[PROVISIONAL]**;
  - τ(1 GHz) = 5.6 ± 0.3 ms **[tab]**.
- **Host galaxy:**
  - log M*/M☉ = 6.89 (+0.06/−0.01) from FAST++ **[tab]** (6.98 from Prospector);
  - SFR 0.15 M☉/yr **[tab]**;
  - Z ≈ 0.1–0.2 Z☉;
  - L_opt = 1.9e9 L☉;
  - Hα flux 4.2e-18 cgs **[tab]**.
- **Not reported:** the host size or half-light radius, any line width, any velocity dispersion, and any dynamical mass. Line widths
  were left free between 500 and 5000 km/s in the fit **[PROVISIONAL]**.
- **Cosmology adopted:** not stated in the text the fetch read.
- **Headline claim:** the burst doubles the redshift reach of localized FRBs and probes ionized baryons over ~80% of cosmic history
  **[abs]**.

### R2. NASA/Webb release (2026-10-08)
- It restates R1 and adds no new numbers. It describes the host as a small, star-forming, metal-poor dwarf, with the redshift from
  oxygen and nitrogen lines.
- It reads the host as pointing to a young magnetar. That is the authors' interpretation, not a measurement.
- Nothing in it bears on the framework beyond R1.

### R3. CHIME 21 cm auto-power
**Detection paper:** CHIME Collaboration, arXiv:2511.19620.
- The auto-power spectrum is detected at **12.5σ** over 608.2–707.8 MHz, i.e. **z 1.01–1.34** (mean z ≈ 1.16), at
  **0.4 ≲ k ≲ 1.5 h Mpc⁻¹** **[abs]**.
- Two sub-bands give 8.7σ (z ~ 1.08) and 9.2σ (z ~ 1.24) **[abs]**.
- It uses 94 nights.
- No BAO is measured: the k range lies above the BAO scale.

**Interpretation paper:** arXiv:2603.25680.
- The amplitude is A²_HI ≡ 10⁶ Ω_HI² (b_HI² + ⟨fμ²⟩)² **[abs]**, with A²_HI = 3.55 (+0.96/−1.32) stat ± 0.61 sys **[PROVISIONAL]**.
- With a b_HI prior of 1.56 ± 20%: 10³ Ω_HI = 0.79 (+0.20/−0.16) **[PROVISIONAL]**.
- With an Ω_HI prior of 6.3e-4 ± 25%: b_HI = 1.99 (+1.22/−0.74) **[PROVISIONAL]**.
- The fiducial cosmology is Planck 2018 **[PROVISIONAL]**.
- The data disagree with IllustrisTNG HI at **3.1σ (TNG100) and 4.0σ (TNG300)** **[abs]**. TNG has less power: the rescale factors
  are 2.38 ± 0.18 ± 0.40 and 3.97 ± 0.30 ± 0.67 **[PROVISIONAL]**.
- The paper says the mismatch is mostly in amplitude, "as opposed to scale-dependence", and that rescaled TNG curves fit the shape
  **[PROVISIONAL]**. It attributes the gap to weaker nonlinear redshift-space HI clustering in the simulations, not to the HI
  abundance **[abs]**.
- The finger-of-god (FoG) damping is a phenomenological shape parameter (σ_FoG,fid ≈ 1.93 h⁻¹ Mpc at z = 1, times a free α_FoG).
- **Public band powers and covariance:** NOT confirmed. No data-availability statement was found in the parts that were read.

**Press release:** the ASU news item itself was not found. A UBC release gives S/N 12.4 at mean z 1.16 **[PROVISIONAL]**.

### R4. MeerKAT HI intensity mapping
**ApJL paper:** Paul, Chen, Santos & Wolz 2026, ApJL 1005, L56 (doi 10.3847/2041-8213/ae808f; arXiv:2301.11943).
- Interferometric foreground-avoidance detection of the HI power spectrum on **Mpc scales at z ≈ 0.32 and 0.44**, from about 96 h of
  data.
- The current arXiv abstract gives 3.2σ / 3.5σ with conservative flagging and 5.9σ / 9.18σ with power-spectrum-based flagging
  **[abs]**.
- Press and a review quote 8.0σ / 11.5σ **[PROVISIONAL]**; the numbers differ between versions.
- The rms fluctuation is ~0.44 / 0.63 mK at 1 Mpc **[PROVISIONAL]**.
- The paper probes the parameters of the HI mass function and HI halo model; the abstract gives no numerical Ω_HI or bias.

**Companion single-dish paper (posted 2026-10-08):** MeerKLASS, arXiv:2610.12158.
- Auto-spectrum at **z = 0.42**, 0.095 < k < 0.245 h Mpc⁻¹, **S/N 6.2** **[abs]**.
- 10³ Ω_HI b_HI = 1.271 (+1.080/−0.598) **[abs]**.
- The subset auto-spectra carry excess power from unresolved systematics; the result rests on cross-spectra **[abs]**.

**Record context.** Earlier FRB baryon work is already in `citations/works`: Macquart+20 (the DM–z census), Khrykin+24 FLIMFLAM DR1
(f_igm = 0.59 (+0.11/−0.10), f_gas(10¹⁰–10¹³) = 0.55 (+0.26/−0.29), as used in `fable_independent_2026/L45_cgm_baryons.py`) and
Prochaska & Zheng 2019. New since then is Connor+25 (arXiv:2409.16952, Nature Astronomy): DSA-110, 39 FRBs with host redshifts, about
76% of baryons in the IGM, Ω_b h₇₀ = 0.049 ± 0.003 **[PROVISIONAL]**.

**Record check.** There is no FRB or HI intensity-mapping lane in `campaign_fresh_gravity/`. The old
`ai_slop/research/frb_analysis/` scripts are Z²-numerology era and are not cited.

---

## 2. Mapping each result onto the framework

Numbers below come from `cfg627_numbers.out`.

### R1 + R2. FRB 20240304B

**(a) The mean DM–z (Macquart) relation tests the baryon budget, not the law.**
- ⟨DM_cosmic⟩ = (3cH₀Ω_b / 8πG m_p) ∫ f_d(z) f_e (1+z)/E(z) dz.
- In the framework, every term is the same as a standard budget:
  - Ω_b is an input, and so is Ω_c/Ω_b = 5.364;
  - cold energy dilutes as a⁻³ in the background;
  - ρ_DE is constant up to the CFG549 trickle of ~1e-7.
- So the framework predicts NOTHING different for the mean. N3 gives ⟨DM_cosmic⟩(2.148) ≈ 1900 pc cm⁻³ at f_d = 0.84 (inherited
  background), against the measured ≈ 2330 including the host term. The difference sits inside the host and sightline scatter.
- f_d is the fraction of baryons that are ionized and diffuse, meaning not in stars or neutral or cold ISM. It does not depend on
  whether hot gas sits in halos or in the IGM, because halo hot gas also adds DM. So even the census placement R4 does not enter the
  MEAN.
- **Cleanliness:** clean as a budget check; zero diagnostic power for the law.

**(b) The DM PDF and foreground-halo partition (FLIMFLAM-style) tests where the ionized gas sits.**
- This depends on how much gas each halo retains, which is R4's f_ret (about 0.1 for galaxies, 0.86–0.90 for clusters), and on the
  gas profile in the law's potential.
- This is the one framework-relevant FRB statistic. R4 is data-forced, so a failure would point at the census sources, not at the
  law (low decisiveness).

**(c) H(z) or ρ_DE(z) from DM–z.**
- It is degenerate with Ω_b h f_d. With one localized FRB above z 1.5, it is not competitive with DESI, which already pins
  a₀(z)/a₀(0) to ±0.04 dex (CFG512/549).

**(d) a₀ at z = 2.15 from the host.**
- The flat-vs-rival gap is a₀ ratio 1 vs **3.24** (0.51 dex; N1). The prompt's "~3×" is right; CFG571 uses 3.03 at z = 2.0.
- Even granting the inherited deep-MOND estimator σ⁴ = (4/81) G M a₀, the host gives **σ ≈ 8–16 km/s (FLAT) vs 11–21 km/s
  (∝ H)** for M_bar = 1–10 × M* on either footing (N2). The separation is only ×1.34 in σ.
- NIRSpec's instrumental σ is about **47 km/s (R 2700) to 127 km/s (R 1000)**.
- The size is unresolved and the gas mass unknown. **Infeasible. Kill.**

**(e) Open tensions.**
- **Cluster mass shortfall (CFG624/625):** the Virgo DM of 235 on this sightline is an X-ray-model estimate. It cannot be used to
  check missing cluster baryons, because it presumes the gas model. Undetected ionized cluster gas can be closed by arithmetic
  instead. The Bullet core shortfall is 3–6× the total mass, while gas is only ~10–15% of cluster mass, so the missing mass would have
  to be roughly 20–40× the gas. That is excluded by X-ray and SZ gas masses. An FRB-based check would add little. (Estimate only; not a
  committed calculation.)
- **Halo concentration and growth:** FRB DM scatter tracks how the gas clusters (feedback), not the cold-energy profile. There is no
  framework-native route without a gas model in our PM. Not addressed.

### R3. CHIME 21 cm auto-power (z ≈ 1.16, k 0.4–1.5 h/Mpc)

**(a) BAO / H(z), then ρ_DE(z), then a₀(z) via CFG549.**
- No BAO is in this result; CHIME's full band (400–800 MHz, z 0.78–2.55) might deliver it in future. The channel is already open
  through CFG549 with DESI.
- More important, a ρ_DE(z) uncertainty of ≲ 0.04 dex is tiny next to the flat-vs-rival a₀ gap: 0.29 dex at z 1.16, 0.51 at 2.15
  and 0.58 at 2.5 (N1).
- A radio BAO matters only for F-DESI vs F-flat (≈ 0.06 dex at z 2). Under CFG549 R2 that needs about 97 discs per bin at 0.1 dex.
- The fork test is limited by galaxy a₀(z) (CFG535, CFG571), not by ρ_DE. A radio BAO would be independent of DESI's systematics, but
  it is **not decisive**.

**(b) Amplitude and shape of the nonlinear HI power: a growth probe that does not use lensing.**
- This is the only result of the four that touches the open growth/concentration tension (CFG555/556/590–596).
- The framework predicts more matter power at some k ~ 1 on the gravitating field. But the CHIME amplitude is A²_HI ∝ Ω_HI² b_HI²,
  so it absorbs any amplitude excess unless Ω_HI(z~1) and b_HI are fixed independently. b_HI needs an HI–halo model, which the
  framework does not have. Any such model is inherited.
- That leaves the **k-shape** over 0.4–1.5 h/Mpc. The framework's own shape prediction is **not stable across engines**. From
  `CFG555/cfg555_results.json`, z = 0, gravitating P/P_S0:

  | engine | k = 0.5 | k = 1.0 | k = 2.0 |
  |---|---|---|---|
  | bookkeeping, 512³ (425/439/460/518) | 1.10–1.16 | 0.80–0.87 | 0.63–0.68 |
  | LR, L200 256³ (527) | 1.34–1.41 | 1.29–1.36 | — |
  | 256³ zero-knob runs | 1.06–1.07 | 0.93–0.97 | — |

  So the sign of the k = 0.5 → 1 change depends on the engine, and these are z = 0 values. A frozen shape prediction must wait for one
  declared engine at z ≈ 1. CFG596 (1024³, running) stores gravitating P(k) at z = 1, which is the needed input.
- The FoG nuisance (α_FoG free) is itself a shape parameter and will absorb much of any 10–40% shape signal.
- **Context only (a ΛCDM yardstick, no verdict weight):** CHIME has 2.4–4× more nonlinear HI power than TNG, with the same shape.
  The sign matches the framework's "more small-scale clustering" only in amplitude, which is the degenerate direction. It is not a
  clue for the framework.

**(c) The cluster shortfall** is not addressed.

### R4. MeerKAT HI (z 0.32/0.44 on Mpc scales; z 0.42 on large scales)
- The z = 0.42 large-scale result gives 10³ Ω_HI b_HI = 1.27 (+1.08/−0.60). That is an 85% amplitude error, with no growth or
  shape leverage and no BAO.
- The interferometric Mpc-scale result is deep in the 1-halo HI regime. It needs an HI halo model (inherited), and its significance
  depends on the flagging.
- Neither addresses a₀(z) or the cluster shortfall. Both are amplitude-only and too weak. Not useful now.

### Inherited assumptions any of these tests would need
- **ΛCDM-inherited:**
  - Ω_b h² (Planck CMB; BBN D/H is an acceptable non-ΛCDM substitute) and h;
  - the background E(z) with Ω_m from the CMB (the framework shares it but does not derive it);
  - the host-DM log-normal and the cosmic-DM PDF shape (the Macquart F parameter, calibrated on ΛCDM hydrosims);
  - FLIMFLAM foreground halo masses (abundance matching) and halo gas profiles;
  - the halo mass function, if R4 is integrated over a population (our PM's supply is itself borrowed; CFG594);
  - the Virgo X-ray gas model;
  - the HI–halo connection and b_HI(k), and the fiducial Planck 2018 cosmology in the CHIME and MeerKAT k conversion;
  - TNG (context only).
- **Standard-MOND-inherited:** the σ⁴ = (4/81) G M a₀ isothermal estimator (N2, used only for size); a ν-function for any host
  rotation model; the EFE convention, which the framework does not have (R7).
- **Data-forced but external:** stellar mass density f_*(z), neutral gas Ω_HI(z) (also needed to break the CHIME degeneracy), and
  the MW ISM and halo DM models (NE2001 / YMW16 / a halo model).

---

## 3. Ranking of candidate "Keating clue" lanes

Each lane is scored on decisiveness for the framework (D, 0–5) and feasibility with public data (F, 0–5). The score is D × F.

| # | lane | D | F | D×F | why |
|---|---|---|---|---|---|
| 1 | **K2: FRB foreground-halo partition vs census R4** (FLIMFLAM / Connor / CRAFT sightlines) | 1.5 | 4 | **6** | Feasible now from small published tables. Tests the global consistency of R4's retained fractions. A failure points at the census sources, not the law |
| 2 | **K1: CHIME nonlinear HI k-shape vs our own PM gravitating P(k, z≈1)** | 2 | 2 | **4** | The only lensing-free probe of the growth tension here. Blocked until one engine is declared (CFG596 z = 1 output); band powers are not confirmed public; FoG absorbs shape |
| 3 | K3: FRB sightlines through clusters as missing cluster baryons for CFG624/625 | 1 | 2 | 2 | Arithmetic already closes it (20–40× the gas mass needed; excluded by X-ray and SZ). Not worth a lane |
| 4 | K6: FRB DM–z as an H(z) / ρ_DE(z) probe | 1 | 2 | 2 | Degenerate with Ω_b h f_d; 1 FRB above z 1.5; DESI already gives ±0.04 dex |
| 5 | K7: MeerKAT Ω_HI b_HI amplitude (z 0.32–0.44) | 0.5 | 3 | 1.5 | Amplitude only, 85% error, needs an HI model |
| 6 | K4: radio BAO → ρ_DE(z) → a₀(z), sealed | 1 | 1 | 1 | ρ_DE error ≪ the 0.3–0.6 dex fork gap; no HI BAO yet; CFG549 already holds the mapping. Freezing a conversion table costs nothing, but the bottleneck is galaxy a₀(z) (CFG571) |
| 7 | K5: a₀(z = 2.15) from the FRB host | 4 | 0 | 0 | σ 8–21 km/s against an instrumental σ of 47–127 km/s, unresolved, no gas mass. Infeasible |

**Honest verdict.** No lane is decisive. The distinctive prediction (flat a₀(z)) is still tested only through z ≈ 1.4–2 disc
kinematics (CFG571 sealed: U4_27928 on 2026-11-06, GS4_24110 on 2026-11-28). The growth tension is still tested only through the
framework-native shear test CFG592/596. The Keating results add an independent check of the baryon budget and a possible lensing-free
growth check later. Neither is a clue for or against the law today.

---

## 4. Frozen-criteria-ready specs (for the owner's go; not frozen here)

### Spec A (top): CFG628 candidate. FRB foreground-halo partition vs the census placement R4

- **Question.** Do the framework's retained gas fractions predict the measured excess DM of FRB sightlines that pass near cataloged
  foreground halos?
- **Inputs:**
  - per-sightline DM, z_FRB, and the foreground-galaxy catalogue with impact parameters and stellar masses, from published tables:
    Khrykin+24 FLIMFLAM DR1 (8 sightlines), Connor+25 (39 hosts), CRAFT/ICS localizations (Shannon+24) and Caleb+26 (1);
  - each foreground system's baryonic mass from its stellar mass plus scaling (data);
  - **f_ret(M_bar) from the frozen census table (CFG515)**;
  - the halo gas profile in hydrostatic balance in the law's potential (baryons + phantom + settled cold energy, out to the census edge
    r_edge = r_M / ln(1 + f_ret f_b/(1 − f_b))), with T at the law's virial value.
- **Framework-native prediction.** DM_halo,i = ∫ n_e dl per foreground system from that profile. DM_IGM follows from
  f_d,IGM = f_d − Σ retained. Both footings, never pooled.
- **Statistic.** Fit the two FLIMFLAM-style partition parameters (f_IGM, f_halo) to the sightline DMs, with a host-DM nuisance
  (log-normal, INHERITED and declared). Report Z = (f_halo,pred − f_halo,meas)/σ and the same for f_IGM.
- **Pass/fail rule (to be frozen).**
  - CONSISTENT if |Z| < 2 for both;
  - TENSION if 2 ≤ |Z| < 3;
  - EXCLUDED if |Z| ≥ 3 in either.
  - Power gate: if σ(f_halo) > 0.25 (FLIMFLAM DR1 gives about +0.26/−0.29), label NON-DIAGNOSTIC and make no statement.
  - A failure is attributed to the census, not to the law, unless it survives replacing f_ret with each system's own measured gas.
- **MUTATE control.** Set f_ret = 1 for every system, so all catchment baryons are retained. The predicted f_halo must rise to the
  cosmic share and be detected as EXCLUDED by FLIMFLAM. If it is not, the lane has no power.
- **Controls.** C1: reproduce FLIMFLAM's published (f_IGM, f_gas) with their own inherited halo model (identity check, context).
  C2: a synthetic recovery test.
- **Expected outcome (stated before any run).** Probably NON-DIAGNOSTIC at DR1 power. R4's galaxy f_ret ≈ 0.1 goes in the same
  direction as the "gas-rich IGM" findings, so a clash is not expected.
- **Data files.** All are table-sized, but none was fetched and **sizes are not checked**:

  | file | source | size |
  |---|---|---|
  | FLIMFLAM DR1 sightline + foreground table | ApJ 973, 151 (doi 10.3847/1538-4357/ad6567; arXiv number to look up) | tables ~KB; source tarball ~5–20 MB (unverified) |
  | Connor+25 FRB / host table | arXiv:2409.16952 | ~KB table; tarball ~10–30 MB (unverified) |
  | CRAFT localized FRB sample | Shannon+24, arXiv:2408.02083 | ~KB table (unverified) |
  | Caleb+26 Table 1/2 | arXiv:2508.01648 | already read |

### Spec B (second; gated on CFG596): CFG629 candidate. CHIME nonlinear HI k-shape vs our own gravitating P(k, z ≈ 1)

- **Precondition (hard gate).** The owner declares one engine. CFG596 must deliver gravitating P(k) at z = 1 for S0 and the framework
  model, both footings, with k ≤ 1.5 h/Mpc resolved (k_hi = πN/4L). No freeze before that.
- **Inputs:**
  - CHIME band powers and covariance at z 1.01–1.34 (2511.19620 / 2603.25680). Request them, or digitise the figures (flagged
    PROVISIONAL);
  - the CHIME window and transfer function;
  - CFG596 z = 1 gravitating P_F(k) and P_S0(k), interpolated to z = 1.16 by the engine's own extra snapshot.
- **Framework-native prediction.** The template T(k) = P_F(k, z)/P_S0(k, z). The HI power is modelled as
  A² T(k) P_S0(k) × D_FoG(k; α_FoG) × (1 + β μ²)² averaged over μ, with A and α_FoG free. S0 is the same-pipeline comparison, as in
  CFG592; no ΛCDM yardstick enters the verdict.
- **Statistic.** Δχ² between the framework template and the S0 template (T ≡ 1) after marginalising A and α_FoG. Also a power-gate
  forecast first: Z_eff from mocks with the CHIME covariance and the FoG prior range.
- **Pass/fail rule.**
  - If Z_eff < 3 in the forecast: NON-DIAGNOSTIC, no run.
  - Otherwise: framework EXCLUDED if Δχ² ≥ 9 against it; DISFAVOURED for 4–9; CONSISTENT below 4.
  - S0 is reported identically.
  - Footings are never pooled; both engines are reported if the owner does not choose one.
- **MUTATE control.** Use CFG555's no-compensation run (424/518 MUTATE: k = 0.5 → 1.49/1.44, i.e. 40–50% excess) as T(k). The gate
  must detect it as excluded or disfavoured, or else report zero power.
- **Inherited and declared:**
  - the HI–halo bias b_HI and its scale dependence, assumed constant over 0.4–1.5 here (a declared simplification);
  - the FoG form;
  - the linear RSD β;
  - the Planck 2018 fiducial in the k conversion.
- **Expected outcome (stated before any run).** NON-DIAGNOSTIC. The framework's shape change across 0.4–1.5 is ~10–40% depending on
  the engine, the FoG absorbs shape, and CHIME's per-bin errors are tens of percent at 12.5σ total.
- **Data needed:**

  | item | source | size |
  |---|---|---|
  | CHIME band powers + covariance | not confirmed public; request from the collaboration | — |
  | 2511.19620 PDF (figure digitisation) | arXiv | ~5–15 MB (unverified) |
  | 2603.25680 PDF | arXiv | ~5–15 MB (unverified) |
  | CFG596 z = 1 JSON | local; produced by the running job | — |

  No heavy compute is needed beyond reading CFG596's output.

**Not specced:**
- K4: a sealed radio-BAO → a₀(z) conversion table. It can be added to CFG549 as a two-line appendix when an HI BAO is published. The
  fork's decision stays with CFG571.
- K5: the FRB host kinematics. Infeasible.

---

## 5. Files
- `cfg627_numbers.py`, `cfg627_numbers.out`, `cfg627_numbers.json`: N1 a₀ ratios, N2 host σ against the NIRSpec floor, N3
  ⟨DM_cosmic⟩.
- `cfg627_numbers_MUTATE.out`, `cfg627_numbers_MUTATE.json`: with the rival exponent set to 0, the rival collapses onto FLAT (PASS).

## 6. Sources (read 2026-10-11; all numbers PROVISIONAL unless marked [abs]/[tab])
- Caleb et al. 2026, Science: https://arxiv.org/abs/2508.01648 (HTML v1 read)
- NASA/Webb release: https://science.nasa.gov/asset/webb/frb-20240304b-nircam-image/ ; Observatoire de Paris:
  https://observatoiredeparis.psl.eu/identification-of-the-host.html
- CHIME detection: https://arxiv.org/abs/2511.19620 ; interpretation: https://arxiv.org/abs/2603.25680 ; UBC release:
  https://phas.ubc.ca/first-detection-cosmological-signal-chime
- Paul, Chen, Santos & Wolz 2026, ApJL 1005, L56: https://doi.org/10.3847/2041-8213/ae808f ; https://arxiv.org/abs/2301.11943
- MeerKLASS auto-spectrum z = 0.42: https://arxiv.org/abs/2610.12158
- Connor et al. 2025: https://arxiv.org/abs/2409.16952
- Record: citations/works (Macquart 2020, Khrykin 2024, Prochaska & Zheng 2019, CHIME/FRB 2021); CFG549, CFG535, CFG571, CFG555,
  CFG594, CFG596; THEORY_v1 and ASSESSMENT of 2026-10-09.
