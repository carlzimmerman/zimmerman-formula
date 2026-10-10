# CFG543: the group supply gap. Frozen labels MECHANISM FOUND (progenitor containment), plus a NOT DIAGNOSTIC trigger on the hot-gas route. In substance the outcome turns on the groups' hot gas, which is not on disk

κ = ½ is fitted. The footings (9.36e-11 / 1.13e-10, written can / alt) are never pooled. The cold energy's mass is still
required. No dark-matter particle. This is not a closed theory. Every number below is read from `cfg543_results.json`,
`cfg543_results_MUTATE.json` or `cfg543_postfreeze_results.json`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (4db846853).
- **Scripts:** `cfg543_group_supply.py` (primary; about 4 s; `CFG543_MUTATE=1` writes the `_MUTATE` outputs) and
  `cfg543_postfreeze.py` (diagnostics written after the primary was seen; no verdict weight). Run with
  `OMP_NUM_THREADS=2 nice -n 10`.
- **Imports, read-only:** CFG540 (`cfg540_bfjr`: data reader, ν, grid) and CFG515 (`cfg515_lib`: fret_census, fret_of).
- **Data:** CFG540's local VizieR file. Also on-disk `real_research/data/lovisari2015_groups.tsv` and `kt2017_*.tsv`.
  Nothing was downloaded.

## The gap
CFG540/541 put the 63 Tian+2026 groups at Δ̄ = +0.118 / +0.105 with the class-A edge. The law with no edge gives +0.010 / −0.010.

## 1. Data re-check

- **Column definitions.** The VizieR header is the only definition on disk:
  - M_bar is "log10(baryonic mass)", with no composition stated;
  - Re is "Effective radius/mean radius";
  - σ is "log10(velocity dispersion)".
  - No ReadMe or paper text is on disk.
- **D1, hot gas: EXCLUDED, at least for NGC 4936.**
  - NGC 4936 is the only overlap with the on-disk X-ray table.
  - Tian's M_bar is 9.82e11. Lovisari+2015 measure Mgas,500 = 1.69e12 (h70), so the hot gas inside R500 alone is 1.72 × M_bar.
  - Descriptive check: Tian M_bar over the KT2017 group K-band luminosity has a median of 1.57 (46 non-Virgo groups, crude
    coordinate match). That is a stars-plus-cold-gas level, not stars plus a group atmosphere.
- **D2, Re.** Re / KT "projected virial radius" has a median of 1.05. So Re is a group-scale projected size estimator, not a
  measured half-mass radius.
- **D3, σ.** σ_Tian / σ_KT has a median of 0.75. The memberships differ; this is descriptive only.
- **Checks: all pass.**
  - K1: C0 reproduces CFG540's cap and no-edge means (|diff| 0.0000).
  - K2: the deep-MOND 4/81 limit (0.0000 dex).
  - K3: the Monte-Carlo Hernquist projected pairwise harmonic radius is 1.046 ± 0.008 R_e (analytic 1.052).
  - K4: the β-model matches the Lovisari median Mgas,2500/Mgas,500 exactly, with r_c/R500 = 0.234 derived from the table.

## 2. Results (class mean Δ̄, Z = Δ̄/σ_tot with CFG540's statistics; can / alt)

| config | what it is | can | alt |
|---|---|---|---|
| C0 | CFG540/541: M_cat, supply 5.364 M_cat / fret_census(M_cat) | +0.118 (Z +3.44) ABOVE | +0.105 (Z +3.04) ABOVE |
| **(a) P1** | census-internal hot gas (M_hot = M_cat (f_ret/0.10 − 1), median 3.99 M_cat) in the law + consistent supply | **−0.111 (Z −2.63) BELOW** | **−0.124 (Z −2.90) BELOW** |
| P1, f_cond 0.07 / 0.13 | brackets | −0.167 / −0.064 (CLOSES at 0.13) | −0.180 / −0.077 (CLOSES at 0.13) |
| P1, G2 (gas out to 2 R500) | geometry | −0.090 BELOW | −0.102 BELOW |
| (a) P3 | hot gas 1.72 M_cat (NGC 4936 anchor) + census on the total | −0.049 (Z −1.48) CLOSES | −0.062 (Z −1.87) CLOSES |
| **(i) P2** | progenitor-containment supply 5.364 M_cat / 0.10, M_bar taken as complete | **+0.060 (Z +1.65) CLOSES** | **+0.043 (Z +1.20) CLOSES** |
| P2, f_cond 0.07 / 0.13 | brackets | +0.047 / +0.071 CLOSE | +0.030 / +0.056 CLOSE |
| P2h | half of M_cat in one progenitor at its own census | +0.072 (Z +2.02) ABOVE | +0.056 (Z +1.57) CLOSES |
| (b) C0, Re/1.052 / Re/2.104 / Re/3.305 | Re definition brackets R2 / R3 / R4 | +0.114 / **+0.067 (Z 1.98)** / **+0.044** | +0.101 / **+0.052** / **+0.028** |
| max-concentration bound | all supply at the centre | C0 −0.223, P2 −0.445 | same |

- **(b) Re conversion.** It closes CFG540's gap on its own only if Re is the N²/Σ_{i<j} 1/R_ij convention (R3; Z 1.98 on can,
  right at the edge) or the 3D gravitational radius (R4). If Re is the pairwise harmonic radius (R2), it does nothing.
  P1 and P2 keep their labels under R2–R4, so the result is **not Re-dependent**.
- **(iii) f_ret.**
  - CFG540 applied the census f_ret (median 0.291, range 0.109–0.595) to the catalogue M_bar.
  - That census counts gas plus stars (CFG416's declared text, R4), and D1 says M_bar does not hold the hot gas.
  - The result: in 63 of 63 groups the inferred M_ta is smaller than the sum of the group's own galaxy-floor progenitor
    catchments.
  - Consistent supply is 2.91× CFG540's (median; range 1.09–5.95). That is the size CFG541 said was needed (×3 alt, ×5 can).
- **(i) Merger history.**
  - Class A has no return, and every progenitor catchment sits inside the z = 0 turnaround sphere. So the cumulative supply
    can never exceed the z = 0 catchment (bound ×1.00). It also cannot be smaller than the sum of the progenitor catchments.
  - With condensed baryons assembled at the 0.10 floor, this gives P2.
  - The partition matters: P2h, with half the baryons in one progenitor, is ABOVE on can (Z 2.02).
- **(ii) Catchment growth.** The z = 0 catchment is the largest so far. EdS self-similar growth gives 0.50 / 0.33 of it at
  z = 1 / 2. Factor ≤ 1, so growth cannot raise the supply.
- **MUTATE: all bite.**
  - M1, supply × 0.3: P1 rises +0.112 / +0.117, P2 rises +0.072 / +0.076.
  - M2, σ shuffle: the P2 rms grows in 200 of 200 shuffles.
  - M3, Newtonian: P1 +0.391, P2 +0.810, both ABOVE.
  - Disclosure: P1 at supply × 0.3 sits at +0.000 / −0.007. With hot gas in the law, roughly CFG540's own supply level closes
    it, as P3 does.

## 3. Verdict (frozen rule, both footings agree)
- **MECHANISM FOUND (progenitor containment).** P2 closes.
- **NOT DIAGNOSTIC trigger:** P1 closes only inside the f_cond = 0.13 bracket.
- No Re-dependence.
- The DATA-ISSUE label does not apply as frozen. D1 = HOT GAS EXCLUDED, but P1 over-corrects instead of closing.

## 4. Plain reading (post-freeze, `cfg543_postfreeze.out`, no verdict weight)

1. **The +0.12 gap is an assumption error in how the supply was set.**
   - CFG540 fed a stars-plus-cold-gas M_bar to a census f_ret that counts hot gas too.
   - That makes each group's catchment smaller than the sum of its own progenitors' catchments.
   - With the supply set consistently, the gap is gone if M_bar is the whole dynamical baryon budget (P2).
2. **The hot gas decides the outcome, and it is not on disk.** D1 says real groups do have hot gas.
   - With the consistent (containment) supply, the class mean crosses zero at only h = M_hot/M_cat ≈ 0.39 (can) / 0.24 (alt).
   - At NGC 4936's measured 1.72, it over-corrects: −0.073 (Z −2.07) / −0.087 (Z −2.43).
   - At the census-internal amount (median 3.99) it over-corrects further: P1 Z −2.63 / −2.90.
   - So the census's group retention (0.3–0.6) implies more hot gas than the group σ allow when the supply is consistent.
     CFG515 flagged the same thing: "group retention slightly too high".
3. **The sign has flipped.** The group test is no longer "framework too low".
   - It is now bracketed: P2 sits at +0.06 / +0.04, and any realistic hot gas gives −0.05 to −0.12.
   - Where it lands depends on how much hot gas lies inside the members' orbits.
4. **A mass trend remains in every configuration:** dΔ/dlog M is +0.10 (P2), +0.13 (P3) and +0.15 (C0). The massive groups
   stay relatively high.
5. **Inherited inputs:** f_cond = 0.10 as the condensed retention (the census floor), the β = 2/3 geometry, and the
   progenitor partition.

## 5. Fetch list for the owner's go (not fetched)
- The Tian+2026 letter, A&A 710, L39 (PDF, about 1–3 MB, estimated). It would settle what M_bar contains for groups and how
  Re is defined.
- Group X-ray gas masses for the Tian groups, for example a ROSAT/eROSITA group gas-mass table (VizieR TSV, under 1 MB,
  estimated). With it, h could be measured per group instead of the single NGC 4936 anchor.

Dated 2026-10-09.

## Addendum (dated 2026-10-09, post-freeze; the frozen verdict above is unchanged)

**Source.** The coordinating session fetched the public arXiv source of Tian+26 (2605.26965) on the owner's approval. It is
stored outside git in `_external_data/vizier2026/tian26/src/BFJR.tex`. I checked the statements below against that text.
`cfg543_addendum.py` writes `.out` and `_results.json`.

**What the paper says**
- **Group M_bar = member stars + observed X-ray hot gas.** Stars come from K-band magnitudes (Cappellari 2013, Kroupa IMF).
  For ellipticals and groups the paper puts the median gas-to-baryon fraction at "about 8%" (ST2024). Unobserved warm-hot gas
  is excluded. The 63 groups are 13 from ST2024 and 50 from Milgrom 2019, mainly built on the MK2011 catalogue.
- **Re for groups** is the average projected radius of all member galaxies.
- **σ** is the biweight line-of-sight dispersion of the members inside that radius.

**D1 is superseded.**
- M_bar does contain the observed hot gas, at about 8%.
- The NGC 4936 comparison used Lovisari's gas out to R500, which reaches beyond the member region Tian counts. So "HOT GAS
  EXCLUDED" was a wrong reading of that comparison. The ratio of 1.72 is a gas amount out to R500, not gas missing from M_bar.
- This settles the frozen pair of readings in favour of **P2**: consistent containment supply with M_bar complete.
  - P2 gives +0.060 (Z 1.65) / +0.043 (Z 1.20) and CLOSES.
  - P1 and P3 add hot gas that M_bar already counts, or gas lying beyond the members. Their over-corrections do not apply.

**What this means for the census group f_ret**
- Read as the stars + cold-gas retention, the census floor (0.10) and its group values (0.3–0.6) imply hot gas of about
  3.99 × M_bar (median). The paper reports about 0.08 of M_bar as observed X-ray gas.
- So the census group f_ret overpredicts the baryons in these groups, inside the member radius, by about 50×.
- The census group values come from X-ray-selected groups and clusters, with gas measured out to R500. They do not describe
  the baryons of these optically selected groups inside the member radius.
- This is also why CFG540's supply was too small. Its census f_ret divided a nearly complete M_bar by a retention that
  assumes a large atmosphere the members do not hold.
- With M_bar complete, containment puts these groups' retention at the galaxy floor, not at 0.3–0.6. Whether the extra
  Lovisari-type gas beyond R_mean should enter the supply is left open. It would raise the supply.

**Mean-projected-radius conversion for the Hernquist tracer (derived)**
- ⟨R⟩ = (π/4)⟨r⟩ for isotropic projection.
- ⟨r⟩ diverges logarithmically for an untruncated Hernquist, so the conversion depends on where the members are truncated,
  r_t = c a.
- k = ⟨R⟩/R_e is 1.126 (c = 10), 1.563 (c = 20), 2.224 (c = 50) and 2.767 (c = 100).
- So the frozen R2 value (1.052, the pairwise harmonic radius) is not the paper's definition. The true R_e is Re/k, with
  k ≈ 1.1–2.8.

| | c = 10 | c = 20 | c = 50 | c = 100 |
|---|---|---|---|---|
| C0, can / alt | +0.109 / +0.096 (ABOVE) | +0.086 / +0.071 (ABOVE) | +0.064 / +0.049 (CLOSES) | +0.053 / +0.037 (CLOSES) |
| P2, can / alt | +0.054 / +0.038 | +0.042 / +0.025 | +0.031 / +0.013 | +0.025 / +0.007 (all CLOSE) |

**Aperture**
- The paper measures σ within R < Re, not over the whole system as the frozen setup assumed.
- P2 with that aperture gives +0.030 / +0.011 ± 0.021 (SE only) at k = 1, and +0.021 / +0.002 at k = 1.563.
- P2 closes under every conversion and both apertures.

**Plain reading after the addendum**
- The CFG540/541 group excess came from an assumption error. The supply was set with a gas-plus-stars census retention
  applied to a nearly complete stellar-plus-observed-gas M_bar.
- With the supply set consistently by progenitor containment (inherited input: the 0.10 galaxy floor; the progenitor
  partition is still an assumption, and P2h is marginal on can), the groups sit on the law within +0.00 to +0.06 dex.
- The mass trend (+0.10 dex per dex in P2) remains.
- κ is fitted, and the cold energy's mass is still required.
