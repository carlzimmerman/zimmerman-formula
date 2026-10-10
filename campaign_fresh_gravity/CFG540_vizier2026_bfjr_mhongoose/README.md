# CFG540: the baryonic Faber–Jackson relation (Tian+2026) under the law, plus MHONGOOSE ultra-deep HI

κ = ½ is fitted. The footings (9.36e-11 / 1.13e-10, written can / alt) are never pooled. The cold energy's mass is still required. No
dark-matter particle. This is not a closed theory. All numbers below are read from the committed JSON.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (3241b65ad).
- **Data:** VizieR ASU-TSV, owner-approved (`FETCH_LOG.md`, sha256 listed). Stored outside git in `_external_data/vizier2026/`.
  Nothing more was fetched.
- **Scripts:** run with `nice -n 10` on 2 threads or fewer.
  - `cfg540_bfjr.py`: Part A. Writes `.out` and `_results.json` in about 3 min. `CFG540_MUTATE=1` writes `_MUTATE.*`.
  - `cfg540_mhongoose.py`: Part B.
  - `cfg540_postfreeze.py`: post-freeze diagnostics, written after the primary was seen. They carry no verdict weight.
- **TDCOSMO SL2S (J/A+A/705/A13):** the catalogue is a list of spectrum files with no tabulated σ, so it is **not usable**.

## Estimator (derived, declared)
- Each system is treated as a spherical, self-consistent baryonic body (mass follows light), with no rotation and no dark component.
- The field is g = ν(g_N/a0) g_N, with ν_mono, the round rule, no EFE, and the CFG515 census edge (primary).
- Profiles: Hernquist for ellipticals and groups (R_e = 1.8153 a). Plummer for dwarfs.
- Constant-β Jeans: β = 0 is primary, with ±0.3 as sensitivity.
- Aperture: σ_e is the light-weighted value inside Re (the catalogue's σ is σ_e, since logFPmass = log 5Reσ²/G reproduces to 0.0002 dex).
  For groups the aperture is the whole system, which is exactly Milgrom's σ⁴ = (4/81) G M a0 in the deep limit (K1 0.0015 dex).
- Checks: K1, K2 and K3 all pass. Clarification of the frozen text: K2's "σ² = GM/(6a)" means the 3D mean square. The line-of-sight value is GM/(18a). The check is implemented that way.

## Part A results (β = 0 primary; class mean Δ = log σ_obs − log σ_law; σ_tot includes the declared 0.10 dex mass-scale floor)

| class | N | can: Δ̄ ± SE (Z) | alt: Δ̄ ± SE (Z) | β −0.3 / +0.3 (can) | verdict can / alt |
|---|---|---|---|---|---|
| GROUPS (census edge) | 63 | +0.153 ± 0.021 (Z 4.3) | +0.145 ± 0.021 (Z 4.1) | β-independent (aperture ∞) | **ABOVE LAW / ABOVE LAW** |
| GROUPS, law without edge | 63 | +0.010 (Z 0.3) | −0.010 (Z −0.3) | — | (CONSISTENT) |
| ELLIPTICALS | 1244 | +0.100 ± 0.003 (Z 2.4) | +0.092 ± 0.003 (Z 2.3) | +0.108 / +0.089 | **ABOVE LAW / ABOVE LAW** |
| … MaNGA | 1218 | +0.102 ± 0.003 | +0.095 ± 0.003 | | |
| … ATLAS3D | 26 | **−0.015 ± 0.014** | −0.019 ± 0.014 | | |
| DWARFS | 93 | +0.055 ± 0.013 (Z 1.7) | +0.038 ± 0.013 (Z 1.2) | +0.069 (Z 2.2) / +0.036 | **β-DEPENDENT / CONSISTENT** |
| … Fornax, Virgo, LG | 31, 34, 28 | +0.041, +0.062, +0.061 | +0.024, +0.046, +0.042 | | |

- **Massive-system tension (frozen rule): REPLICATES** for ellipticals and for groups, on both footings and at every β.
  - The size matches the record: SLUGGS +0.07, and KiDS early types about +0.04 to +0.09 dex in σ.
  - **Caveat 1, ellipticals.** The class result is MaNGA's: 1218 of the 1244 systems. The 26 ATLAS3D ellipticals sit on the law (−0.015 ± 0.014), so the two surveys differ by +0.12 dex.
    - Within MaNGA the offset is flat in mass: dΔ/dlog M_b is +0.011, and the mass bins run +0.08 to +0.105 from 10^9.5 to 10^12.5.
    - So it is not a massive-end effect.
    - Nulling it needs a baryonic mass-scale shift of +0.24 / +0.23 dex (post-freeze). That is the size of a Chabrier → Salpeter change.
    - Inside the Re of ellipticals the law is close to Newtonian. The Newtonian MUTATE is only 0.05 dex higher.
    - So this residual is mostly the familiar stellar-vs-dynamical mass offset, and an IMF or M/L choice can absorb it.
    - The paper's IMF and its MaNGA σ_e/Re definitions are not on disk.
  - **Caveat 2, groups.** The law alone fits groups (+0.01 / −0.01). The whole group excess comes from the **census edge**.
    - The census f_ret is 0.11–0.60 (median 0.29), which puts r_edge at about 1.0–1.1 Re (range 0.6–2.8).
    - So the supply cap truncates the settled cold energy inside the members' orbits.
    - Post-freeze check, an edge-placement variant: freezing the phantom where its own mass reaches the supply cap, instead of at the point-mass r_edge, moves the edge out ×1.36.
    - That leaves +0.118 / +0.105 ± 0.021. The excess survives the check, somewhat reduced.
    - The bracket f_ret = 0.07 gives +0.051 / +0.035; f_ret = 0.18 gives +0.108 / +0.097; f_ret = 1 gives +0.364 / +0.367.
    - Massive, high-f_ret groups are above the law even without the edge (+0.14 / +0.12 for f_ret ≥ 0.4; dΔ/dlog M +0.12).
    - Not known from the files on disk: whether the groups' M_bar includes hot intragroup gas, and whether "Re" is a mean member radius rather than a half-mass radius. The groups verdict is conditional on both.
- **Edge relevance:** for ellipticals the edge is irrelevant (min r_edge/Re 17.8 / 16.2; shift < 1e-6 dex). For dwarfs the mean shift is 0.0005 dex; only And XIX (+0.033 / +0.043) and CVn I (+0.006 / +0.008) move. For groups it **matters** (+0.143 / +0.155 dex).
- **Trend with g_bar (frozen rule): DOES NOT TRACK** on both footings, because some bins lie outside ±0.10 dex.
  - The overall slope is small: −0.015 ± 0.004 (can) and −0.013 ± 0.004 (alt) dex per dex, over 7 dex in g_bar/a0 (−3.9 to +3.1).
  - On the catalogue g_bar axis, every bin with log g/a0 < 2 is positive, between +0.02 and +0.17. So the law follows the BFJR's slope across the whole range, but with a positive offset of about +0.1 dex.
  - Inside the ellipticals there is a tilt: the residual falls with g_bar (−0.08 dex per dex, post-freeze). Compact high-g ellipticals reach −0.05 on the catalogue axis and −0.09 on the GM/2Re² axis.
- **No-EFE readout (descriptive):** cluster dwarfs (Fornax + Virgo) minus Local Group dwarfs is −0.008 ± 0.031 (can) and −0.006 ± 0.031 (alt). There is no EFE-like deficit in cluster fields, which reads with R7. Weight is low: tides and the dwarfs' M_bar composition are not modelled.

## MUTATE: PASS on both footings, as frozen
- **M1, Newtonian.** Groups are +0.81, dwarfs +0.40 and ellipticals +0.15. The frozen labels are "NOT DIAGNOSTIC" because the 0.05 floor exceeds 0.045, not CONSISTENT, so the tooth passes. Disclosure: it passes through the floor rule, while the offsets themselves are huge.
- **M2, a0 × 4.** Dwarfs are BELOW LAW (−0.075 / −0.093). Groups stay ABOVE (+0.11), because the edge moves inward as a0 grows; with the edge on, groups are only weakly sensitive to a0.
- **M3, within-sub-sample σ shuffle.** For ellipticals and dwarfs the rms grows in 200/200 shuffles, so the law tracks individual systems, not only class means.

## Part B: MHONGOOSE (descriptive; Veronese+2026, 16 galaxies)
- **The catalogue contains no rotation curves.** So no RAR or outer-slope test is possible from it.
- Integrating the stacked face-on profiles reproduces table1's M_HI to +0.08 dex (median; range +0.02 to +0.23).
- **Gas beyond N_HI = 1e20 cm⁻²:** median 6.7% of the HI (mean 7.4%, max 25.4% for UGCA 307), using the outermost crossing.
  - The frozen literal "first drop" picks up NGC 1371's central HI hole (99.9%). Both are reported; the variant is disclosed.
- **Gas beyond 1e19 cm⁻²:** median 0.2%, max 5.1%.
- At those radii the gas-only g_bar is already 10^−1.6 to 10^−2.9 a0.
- So curves and gas models that stop at 1e19 miss under 1% of the gas in most of these systems. Models that stop at about 1e20 miss about 7% (up to 25%), all of it at g_bar ≲ 0.01 a0.
- This matters only for the lowest-acceleration RAR points and for outer slopes beyond the classic HI edge. It does not touch the inner regions that carry the record's tensions.

## Bottom line
- On 1400 pressure-supported systems spanning 7 dex in g_bar, the law reproduces the baryonic Faber–Jackson relation to a level offset of about +0.1 dex in σ.
- Dwarfs and ATLAS3D ellipticals are on the law.
- MaNGA ellipticals sit +0.10 / +0.09 above it, flat in mass. This replicates the record's massive-system sign and size, but it is degenerate with a Salpeter-like mass scale.
- Groups are on the law alone. They sit +0.15 above the framework once the census edge truncates the cold energy at about 1 Re (+0.11 with the supply-cap placement).
- This is a new pressure point on R2/R4 at group scale, conditional on the groups' baryon census.
- Dated 2026-10-09.
