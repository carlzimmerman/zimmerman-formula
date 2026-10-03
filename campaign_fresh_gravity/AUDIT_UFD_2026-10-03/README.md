# AUDIT_UFD 2026-10-03: is the Milky Way ultra-faint failure real, and was it computed by the framework's own rules?

> κ = ½ is FITTED and stays fixed. Both footings are used: a₀ = 9.36e-11 and 1.13e-10 m s⁻². The cold component's mass is still required, and no dark-matter particle is added. This is an audit, not a frozen lane. No frozen result is changed, nothing was downloaded, and nothing is committed by this folder.

- **Script:** `audit_ufd.py`, about 20 s. It writes `audit_ufd.out` and `audit_ufd_results.json`, and exits 0 when its three reproduction checks pass (they do).
- **Method:** the script reads the Local Volume Database MW table on disk (`real_research/data/dsph/lvd_dwarf_mw.csv`, Pace 2024) directly. It re-implements the estimator, the Kaplan–Meier median with upper limits, the bootstrap and the Υ floor from scratch. The only record function it imports is `nu_mono`, for the kernel check. It then changes one declared input at a time. There is no fitting and no scan.

## The claim

CFG313's bare-law row: MW ultra-faints at +0.325 dex, 3.77σ (canonical) and +0.304 dex, 3.55σ (alt). This is the same number as CFG28, CFG42/45 reading L, CFG259 DV0, and CFG286 at full stripping. CFG313 did not compute it anew; it reproduces the law row from CFG45's harness.

## Verdict table

| # | item | what was done in the record | framework-correct? | effect on the offset (canonical; dex, then z) |
|---|---|---|---|---|
| 1 | Raw data provenance | LVD (Pace 2024), as downloaded on 2026-09-03 (PROVENANCE.md). σ_los, the circularised r_half (`rhalf_sph_physical`), M_V, distance. The 9 upper limits come from `vlos_sigma_ul`. No HI in any UFD. | **Y.** Published compilation values. The law row uses no halo-model, abundance-matched or ΛCDM-SFH mass. Spot check of 5 (Boo I, UMa I, Seg 1, Tuc II, Com Ber): 2 L_V equals the LVD's own `mass_stellar` to ≤ 0.005 dex over all 40, and r_sph = r_maj √(1−e) to rounding. σ matches the file. | none. Independent reproduction: +0.3245 ± 0.0860, z +3.77 / +0.3045, z +3.55 (exact). |
| 1b | Older-catalogue cross-check | — | info | McConnachie 2012 differs for some systems: Boo I 2.4 then vs 4.0 now; Boo II 10.5 ± 7.4 vs 1.92; Herc 3.7 vs 2.25. The current LVD values are mostly 2023–26 multi-epoch or DEIMOS. CFG259 showed that swapping between sources moves the median by ≤ 0.005. |
| 2 | Stellar mass / M/L | Υ_V = 2 for every system (the LVD convention). The Υ_V 1–4 range is used as a systematic floor (±0.077 dex), which is the largest error term. | **Partial-Y.** Υ_V = 2 is a stellar-population value, not ΛCDM. It is not computed from an SPS model on disk. Recalled SPS values for ancient, metal-poor populations are about 1.5–2 (Kroupa/Chabrier) and about 2.6–3 (Salpeter). Recalled UFD IMF measurements lean bottom-light, i.e. lower Υ. | Υ 1.5: +0.356 (4.15σ). Υ 3.0: +0.279 (3.25σ). Υ 1.0: +0.401. The law needs Υ_V ≈ 7.8 (6.6 alt) to reach 2σ and ≈ 35 (29 alt) to reach zero. No SPS model allows either. |
| 3 | Prediction formula | σ² = g(r) r/3 at r = (4/3) r_half, with half the mass inside. g = ν(g_N/a₀) g_N, kernel `hunt_lib.nu_s`, which is the exponential RAR kernel, not ν_mono. | **Y in effect.** The UFDs sit at y = 7e-5 to 3e-3. There ν_mono equals the exponential kernel to 5e-9, and the median is unchanged to 1e-4. The estimator predicts slightly more than the deep-MOND (4/81) G M a₀ formula, so it leans in the law's favour. | ν_mono: 0.000. With (4/81): +0.342 (+0.018 dex, 4.06σ). The r_half choice (major-axis vs circularised) changes nothing (deep regime: σ is independent of r). |
| 3b | External field effect | Not applied. Under FG001 ownership (candidate B), an accreted satellite follows the **isolated** law of its own baryons. The EFE version is the *rival* reading. | **Y.** This is B's own rule, and it is the choice most favourable to the law. | EFE rival (the record's algebraic a_int, MW 6e10 M☉ at D_gc): **+0.764 dex (+0.44 worse), 4.6σ** (the Υ floor doubles in the quasi-Newtonian regime). With the LMC field for the 7 LMC systems: the same. An EFE can only make it worse. |
| 4 | Equilibrium / tides | No tidal cut in the law row. CFG28's distance test. CFG286 tested only the *rule's* NFW collapse cores being stripped at pericentre. That is inert because r_t/r_ev ≈ 34, and it says nothing about the bare law or about tidal heating of the stars. | **Partial.** Tidal heating under the framework is not modelled anywhere. The empirical checks say tides are not the driver. | D_gc > 80 kpc: +0.325 (3.90σ). ≤ 80 kpc: +0.322 (2.54σ, fewer objects). Dropping six disturbed systems (Tuc III, Boo III, Her, Wil 1, Seg 2, Tuc V; a list recalled from the literature, not in the file): **+0.355 (3.85σ), larger.** The disturbed systems sit low (Boo III −0.12, Her 0.00). Dropping the LMC-hosted 7: +0.322. |
| 5 | Binary inflation | The LVD values are mostly multi-epoch or DEIMOS 2023–26. CFG259 re-scored with Arroyo-Polonio+26 binary corrections (8 systems) and Geha+26 DEIMOS. 9 upper limits enter the Kaplan–Meier median as censored values. | **Y.** The censoring is handled correctly. Phoenix II's 21.2 km/s limit carries no information, and KM handles that correctly too. | CFG259: −0.003 to +0.005 dex, 3.5–3.9σ. A mean statistic would shift by about −0.02 (CFG259's hand estimate). The binary floor needed is about 3.4 km/s in every system. Eri II and UMa I sit above the single-epoch binary ceiling (CFG29). |
| 6 | The statistic | Kaplan–Meier median of 31 + 9 log(σ_obs/σ_pred). Error = bootstrap (1000, seed 42) ⊕ half the Υ 1–4 shift. Collapse floor = 0 for the law. Sample = all LVD MW systems with M_V > −7.7 (a standard cut, independent of the framework). | **Y, and conservative.** My script recomputes it exactly. | Inverse-variance mean (31 resolved): +0.378 ± 0.017 ⊕ floor, **4.8σ**, χ²/dof 19 about zero. SPS-range floor (Υ 1.5–3): **6.0σ**. Best-measured 13 (error ≤ 25%): +0.432, 4.05σ. The 3.8σ headline is the *most lenient* of these statistics. |
| 7 | ΛCDM contamination | The law row (reading L) calls no halo_mass, NFW or f_b. The collapse-mass floor is zero for L. CFG313's ΛCDM content (Moster/Mandelbaum, Dutton–Macciò NFW, Planck f_b) enters only the *rule* rows, which are inert on native mass. | **Y.** The law row is clean. | none |

## Escape routes the frozen B does not contain (reported only; none is a fix)

| route | framework basis | result | why it is not a fix |
|---|---|---|---|
| Infall gas below the calibrated mass range | FG001 class A (keep the infall baryons); CFG18's nearest-neighbour draw | +0.224 (CFG18), about 2.6σ; FG001 H8: +0.209 | It extrapolates field-dwarf gas fractions down to M★ ~ 1e3–1e5, where none are measured. CFG18 itself declared the UFDs reionisation fossils with no infall gas. It still fails. |
| Law on the *initial* baryons, M_init = R_ind M_now (CFG35's conservation read literally; R_ind from CFG317's leaky box, per object) | conserved cold component of the original baryons | UFDs **−0.208** (yield −0.5: −0.123; +0.1: −0.298), so it overshoots. MW classicals: **+0.100 → −0.271** (stars only, n 12) | It swaps the failure. It over-predicts the UFDs and breaks the classicals, which pass today. CFG317 tested R only through the rule's edge switch, where it is inert. It never tested this reading. |

## Bottom line

**The +3.8σ is a genuine, framework-native failure, and the record states it fairly. It is not an analysis error.** The raw LVD values are transcribed correctly. The chain uses no ΛCDM input. The prediction is B's own isolated law with the adopted ν_mono (identical to the kernel used in this regime). Stellar mass uses a stellar-population M/L. Upper limits and binaries are handled correctly.

Every check that could break the failure leaves the offset at +0.28 to +0.43 dex:
- the external field, which B does not apply, would make it worse by 0.44 dex;
- the deep-MOND formula, by 0.02 dex;
- an old-population Υ_V of 1.5, by 0.03 dex;
- dropping the tidally disturbed systems, by 0.03 dex;
- Salpeter Υ_V = 3 is the only standard choice that lowers it (by 0.045 dex, to 3.25σ).

The **size** of the offset is robust. The **significance** of 3.8σ is the lenient end: a mean statistic or an SPS-width Υ floor gives about 5–6σ. The failure needs a mass about 30× the stars (Υ_V ≈ 30–35) or about 3.4 km/s of binary inflation in every system. Neither is available.

**Framework-native corrections that would each need a new frozen lane (none may be applied to CFG313):**
1. The conserved cold component of the *initial* baryons fed to the law, rather than through the rule's switch. The pre-flight above predicts it overshoots the UFDs and breaks the classicals.
2. Tidal heating under ownership, at the measured pericentres. The distance and disturbed-system tests above predict no help.
3. A per-system Υ_V from an SPS model with each system's own [Fe/H] and age. This needs an SPS table that is not on disk (e.g. the BaSTI or MIST V-band M/L grids). The expected effect is ≤ 0.05 dex.

Nothing here says the theory is closed or that the data favour any framework.
