# CFG628: FRB foreground-halo gas vs the census placement R4. NON-DIAGNOSTIC on both footings, and the MUTATE control is NOT detected (the test has no teeth at FLIMFLAM DR1 power)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (2f6846261), before any script or prediction.
- **Scripts:** `cfg628_transcribe.py` (LaTeX to CSV, spot checks: `cfg628_transcribe.out`); `cfg628_partition.py`
  (`.out`, `.json`); `CFG628_MUTATE=1` gives `cfg628_partition_MUTATE.out/.json`. One process, about 40 s, 0.37 GB peak, nice 10.
- **Settings:** κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are scored separately, never pooled. Cold energy mass is
  still required (no particle). This is not "theory closed", and nothing here says the data favour the framework. No ΛCDM or
  standard-MOND quantity is a yardstick in the verdict.

## Bottom line

| | canonical | alt |
|---|---|---|
| measured f_halo (rebuilt FLIMFLAM DR1 likelihood, flat priors) | 0.615 (−0.287 / +0.240) | same data |
| **power gate** σ(f_halo) | **0.264 > 0.25 → NON-DIAGNOSTIC** (published σ 0.275, also above) | same |
| framework interval P (census f_ret) | [0.000, 0.824] | [0.000, 0.824] |
| Z_near / Z_far | 0.00 / +2.14 → "CONSISTENT (interval-limited)" bin, **no statement** | same |
| MUTATE P (f_ret = 1) | [0.853, 2.150]; Z_near +0.99 | same |
| **MUTATE tooth** (needs \|Z\| ≥ 3) | **NOT DETECTED: the test has no teeth** | same |
| f_IGM (context only) | P_IGM [0.60, 0.95] vs 0.674 (−0.18/+0.18): Z_near 0 | same |

**Verdict: NON-DIAGNOSTIC on both footings.** Eight sightlines cannot separate "galaxies keep about 10% of their catchment
baryons" from "they keep all of them". The f_ret = 1 control sits only 1σ from the measurement (Pr(f_gas ≥ 0.853) = 0.17). The
footings agree to three decimals because they enter only the E2 geometry, and E2 never sets an edge of P.

The **primary Spec A statistic is NOT EVALUABLE.** It is the per-halo framework DM along each sightline, and none of the approved
sources contains a per-halo foreground catalogue (see "Data that would make the primary evaluable").

## Data transcribed (parser `cfg628_transcribe.py`; every row names its table)

- `flimflam_dr1_sightlines.csv`: Khrykin+24 (arXiv:2402.00505) Table 1 + Table 3. 8 sightlines: RA, Dec, z, DM_FRB,
  DM_igm^argo ± σ (f_igm = 1), DM_halos ± σ (f_gas = 1, mNFW to r200), DM_host^halo ± σ, ⟨log M_host^halo⟩, DM_MW.
- `flimflam_dr1_published_posteriors.csv`: Khrykin+24 Table 5. Four prior sets × (f_igm, f_gas, DM_host^unk, ⟨DM_host⟩).
- `connor25_frbs.csv`: Connor+25 (arXiv:2409.16952), both FRB tables. 68 rows: DM_obs, DM_ex, z (photometric flag), DM_MW,
  survey.
- `craft_ics_frbs.csv`: Shannon+24 (arXiv:2408.02083) tab:frb_discoveries. 43 rows: ν_c, DM, DM_MW (NE2001), z or flag.
- **C3 checks:**
  - Table 1 and Table 3 agree exactly. CRAFT and Connor agree on DM to within 1 pc cm⁻³ and on z to within 0.001 for 7 of the
    8 sightlines. The exception is FRB 20211212A: Connor gives DM 209.0 against 206.0 elsewhere (flagged, not corrected).
  - Naming: Khrykin+24's 20190608A / 20211127A are written 20190608B / 20211127I elsewhere, and Connor writes 20180924A for
    20180924B.
  - Connor's DM_ex = DM_obs − DM_MW holds on all 68 rows. A hand spot-check of three Table 3 cells passes.
- Not used: Caleb+26 (FRB 20240304B). Its numbers in CFG627 are WebFetch read-outs, not transcribed tables, and it has no
  foreground catalogue.

## What was computed

**Measurement (no framework input).**
- Khrykin+24's Gaussian DM likelihood with its Table 3 per-sightline inputs, the log-normal host (s* = 1.23) and σ_MW = 15.
  Priors are flat: f_igm, f_gas ∈ (0, 1], ln μ ∈ [0, 6].
- Their f_d prior is dropped. It converts f_gas to f_cgm through the Aemulus ΛCDM halo mass function, which is inherited.

**Framework, in the measurement's f_gas units, per halo mass 10¹¹–10¹³ M☉.**
- f_ret comes from CFG416/CFG515 `fret_of` (imported read-only), with M_ta = M_h or 2 M_h.
- Retained baryons are M_b,now = f_ret · 0.157 · M_ta.
- Ionized gas is taken two ways: B-lo = M_b,now − M* (Moster+13 M*), and B-hi = M_b,now.
- The gas is isothermal at σ² = V_f²/2, hydrostatic in g_N ν_mono(g_N/a₀), out to the census edge.
- It is converted to f_gas two ways: E1 counts all of it; E2 counts only the part projected inside r200.
- At the census floor (M_ta < 10^12.5 h⁻¹) a galaxy halo keeps at most f_eq = 0.108 (B-hi).
- From 10^11.5 to 10^12.5 the census retains **fewer baryons than Moster's stars** (M*/(f_b M_h) up to 0.22 against f_ret 0.10),
  so B-lo gives zero hot gas. This is an internal tension between two inputs (the census floor and the inherited SHMR), not a
  measurement.
- The upper end of P (0.824) is set by 10¹³ groups with M_ta = 2 M_h (f_ret 0.38).
- Reported only, post freeze: with M_ta = M_h alone, P1 = [0, 0.267], Z_near −1.21.

## Disclosures (verify a fail as hard as a win)

1. **The interval is wide by construction.** The DR1 halo-mass weights are not public, so P spans the whole grid and every
   variant. A gate-passing sample would still need the per-halo catalogue to give a sharp test.
2. **K1 FAILS at its frozen tolerance.** ν_mono differs from the exponential form by 4.8e-5 (absolute) for y < 1, against the
   frozen 1e-6. The relative difference is 4.9e-9: the engine's own table and trapezoid resolution, copied verbatim. The tolerance
   was not changed, and the difference has no effect on any number here.
3. **C2 FAILS (over-coverage).** The 68% coverage is 0.95, not in [0.55, 0.81]. The recovered medians scatter by 0.157, but the
   quoted σ is 0.30. So the f_gas posterior is prior-dominated: the flat prior bounded at 1 sets the width, and there is no bias
   (mean recovered 0.506 against a truth of 0.5). This supports the gate reading.
   - With the truth at the prior's centre, the scatter of the medians is itself shrunk, so 0.157 is not a usable frequentist σ.
4. **C1 is only partial.**
   - The f_igm / f_gas medians are within 0.10 of the published values, so they count as "reproduced" by the frozen rule: 0.674 /
     0.615 rebuilt against 0.59 / 0.55 published.
   - ⟨DM_host^unk⟩ is NOT reproduced. The rebuilt values are 24 (with the ln σ term) and 161 (without it), against 69 published.
   - The paper's exact normalisation and its HMF-based f_d prior cannot be recovered from the text.
5. **The frozen gas profile is degenerate (found after the run).** An isothermal gas around a point mass piles up at the inner cut,
   because ρ ∝ exp(G M/σ² r) in the Newtonian core. So E2 collapses onto E1. P does not depend on the profile, because its edges
   are the B-lo minimum and the E1 B-hi maximum.
   - A post-freeze diagnostic E2′ puts the gas only between r_M and r_edge. It gives cylinder fractions of 0.89–1.00 and a range
     of [0, 0.70] / [0, 0.74] (canonical / alt). No verdict weight.
6. **f_IGM is context only.** The measured f_igm rests on ARGO (ΛCDM N-body) reconstructions. The framework's cosmic halo fraction
   is a declared bracket [0, 0.15], because a halo mass function would be inherited. Under MUTATE, f_IGM is not evaluable.
7. **The N forecasts are optimistic.** They scale σ as N^-1/2 from a prior-bounded posterior: about 9 sightlines to reach the gate,
   and about 73 to exclude f_ret = 1 at 3σ. No verdict weight.
8. **The census-vs-measured-gas clause of Spec A is NOT EVALUABLE.** No source gives per-system gas masses.

## Inherited ingredients (flagged; none is a yardstick)

- **Halo masses:** CIGALE M* → Moster+13 SHMR (ΛCDM abundance matching). The Moster parameters were recalled, not verified against
  the paper, so they are PROVISIONAL.
- **Halo radius and background:** M200c / r200 with the Planck-like background (h 0.673, Ω_m 0.315, z̄ 0.20).
- **The measurement's template:** mNFW gas with r_max = r200 and Ω_b/Ω_m = 0.046/0.315. It is inside Table 3's DM_halos and
  DM_host^halo.
- **The IGM term:** ARGO density reconstructions (ΛCDM, calibrated on hydro sims) in DM_igm^argo, plus the +15 for the first
  50 h⁻¹ Mpc.
- **Milky Way terms:** NE2001 and the 40 ± 15 MW halo DM.
- **The host model:** log-normal with s* = 1.23 (James+22a).
- **The baryon budget:** the f_d range [0.75, 0.95] (Madau–Dickinson stellar mass density; Khrykin+24's prior).
- **Halo mass function:** a declared f_halo,cos bracket is used in place of one.
- **Connor+25's f_IGM = 0.76:** calibrated on IllustrisTNG300. CONTEXT only; not used.

## Data that would make the primary evaluable (NOT downloaded; for the owner's decision)

| item | source | size |
|---|---|---|
| FLIMFLAM DR1 foreground galaxy and group catalogue (per-galaxy RA, Dec, z, CIGALE M*, FoF group membership) for the 8 sightlines | Huang+24 / Khrykin+24. Per 2408.12864 it is "released on Zenodo after refereeing"; the DOI and release status were not checked | unknown (catalogue-sized, likely < 10 MB) |
| Per-field foreground tables from the earlier single-sightline papers (for example Simha+2020 on FRB 20190608B, ApJ 901, 134) | arXiv LaTeX sources; IDs not verified here | unknown (tables ~KB) |

With per-halo b⊥, z and M*, the Spec A statistic becomes buildable: a framework column per halo from the edge-bounded profile
(after fixing the profile's inner boundary, disclosure 5). Even then, the power gate at N = 8 would very likely still trip
(disclosures 3 and 7).

## Run

```
nice -n 10 python3 -I campaign_fresh_gravity/CFG628_frb_halo_partition/cfg628_transcribe.py
nice -n 10 python3 -I campaign_fresh_gravity/CFG628_frb_halo_partition/cfg628_partition.py
CFG628_MUTATE=1 nice -n 10 python3 -I campaign_fresh_gravity/CFG628_frb_halo_partition/cfg628_partition.py
```

The data path defaults to `<repo parent>/_external_data/frb_tables/`; override it with `CFG628_DATA`.
