# TH1_turnaround_basins: flow-defined basins reproduce BS1 in the Local Volume; the Milky Way's halo hinges on M31's baryon mass

Criteria: `FROZEN_CRITERIA.md` (4322b7a2a4, committed alone, before any script or number); no amendment.
Machinery: BS1's committed UNGC frame, select and line-fit block, executed read-only.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **FLOW BASINS REPRODUCE BS1** (T 12.3 and CL3's 12.236)

**Method.**
- The 67 SPARC galaxies with a UNGC counterpart are re-flagged with basins defined by the **measured zero crossing of
  the radial-velocity field** around each galaxy's main disturber.
- That is the turned-around region, θ < 0: the candidate field equation's own variable (e03863663b).
- **Result:** no galaxy changes branch, and all 67 stay on the law under both rules.

**Determinable flow basins** (N ≥ 8 accurate distances in 0.2–3 Mpc, H > 0, R0 in the window): 13 of the 45 centres.

| centre | R0 (kpc) | H (km/s/Mpc) | log M_basin |
|---|---|---|---|
| M31 | 903 ± 78 | 109 | 11.80 (see below) |
| DDO 44 / NGC 2403 field | 1062 ± 90 | 168 | 12.15 |
| NGC 2403 | 821 ± 107 | 114 | 11.06 |
| IC 342 | 589 ± 166 | 103 | 11.66 |
| NGC 253 | 364 ± 212 | 108 | 11.99 |
| Antlia | 844 ± 151 | 89 | 9.88 |

The M81, M101, NGC 4258, NGC 4736 and NGC 5194 groups give no positive-slope zero crossing within 0.2–3 Mpc with
UNGC's accurate distances, so they are **not determinable**. They keep BS1's flags, which are also below T.

**Check K0:** the same block reproduces BS1's LG R0 = 794.7 kpc exactly.

## What this does and does not test

- **It is a weak test of the flags themselves.** Every Local Volume SPARC galaxy sits in a basin below T on either
  definition, so agreement is easy.
- BS1's 13 switched galaxies (mostly Ursa Major, about 18 Mpc) lie **outside** UNGC's volume and are **not** tested
  here. That needs Cosmicflows-4 distances, a download for which the owner's approval is needed.
- **The flow criterion is operational where the data allow.** Zero crossings exist for 13 centres, with turnaround
  radii of 0.3–1.1 Mpc, the expected scale.

## A finding on the data (reported, not graded): the Milky Way's switch depends on M31's baryon mass

- Centred on M31, the flow basin's mass from UNGC's own K-band light (Υ_K 0.6) is only **log M 11.80**, below T.
  - UNGC's 2MASS light gives M31 log L_K 10.73, i.e. M★ ≈ 3×10¹⁰ M☉.
  - The Milky Way has no UNGC K luminosity.
- BS1 used CFG522's record baryons: MW 6×10¹⁰, M31 1.2×10¹¹, M33 8×10⁹ and the LMC 3×10⁹ M☉. That gives
  log M_basin 12.39.
- **2MASS is known to miss the extended light of very large nearby galaxies.** Published M31 stellar masses are about
  1×10¹¹ M☉, so the record's value is the better one. Still, the Milky Way's halo in the basin picture **rests on
  M31 + MW baryons ≳ 1.5×10¹¹ M☉**. If they are lower, the Local Group falls below the switch.

## Checks: 4/4

- **K0:** the LG R0 is reproduced.
- **K1:** every determinable R0 lies inside the window.
- **K2:** peak RSS 0.05 GB.
- **K3:** at least one group H lies within ×3 of the LG's.
- **Rerun:** byte-identical (`4a9d493d…dfef`).

**MUTATE twin** (centre velocity sign flipped): **it did not fail its designed check.** K3 still passed and the run
exited 0, so the twin's teeth did not bite as frozen (disclosed). The twin does change the outcome: 9 galaxies change
branch. So the projection matters, but K3 is too loose to register it.
