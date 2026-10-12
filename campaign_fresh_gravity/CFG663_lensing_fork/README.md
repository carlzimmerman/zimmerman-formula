# CFG663: the response sector has to lens

**Label (primary, blue isolated lenses, both footings): H-NL EXCLUDED.** In the two-sector picture (collisionless cold matter +
a response field that makes the law), a response that does not lens is excluded by raw lensing plus raw rotation curves.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (93c6e29ce), 2026-10-12. Block CFG660–669.
- **Settings:** κ = ½ FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed";
  nothing here says the data favour the framework. Raw data only: Brouwer et al. 2021 KiDS-1000 isolated lensing RAR (release tar
  on disk, extracted to a fresh temp directory, read with `python3 -I`) and SPARC rotmod (CFG4 harness, Υ = 0.61). No ΛCDM or MOND
  model enters a prediction.
- **Script:** `cfg663.py`, one process, about a minute, exit 0 → `cfg663.out`, `cfg663_results.json`. MUTATE runs:
  `CFG663_MUTATE=1 CFG663_M=M1` and `CFG663_M=M2`, each exits 1 when its tooth bites (both do) → `cfg663_MUTATEM1/M2.*`.

## The logic

Dynamics in the two-sector picture is law + cold matter, g_dyn = F(g_bar) + g_cold. If the response does not lens, lensing sees
only Newtonian mass, g_lens = g_bar + g_cold, so the raw lensing **fixes** the cold matter: g_cold,req = g_lens,obs − g_bar. The
same population of baryons must then show dynamics F(g_bar) + g_cold,req. Cold matter cannot hide: it enters both probes.

## Results (overlap g_bar 4.04e-13 to 3.92e-12: 324 SPARC points in 59 galaxies)

| lensing file | footing | rms H-L (law) | rms H-NL | Δ | KiDS draws with Δ ≥ 0.03 | median g_cold,req/F | class |
|---|---|---|---|---|---|---|---|
| **blue (primary)** | canonical | 0.1115 | 0.2665 | **+0.155** | 2000/2000 (5th pct +0.101) | 0.62 | **H-NL EXCLUDED** |
| **blue (primary)** | alt | 0.1307 | 0.2888 | **+0.158** | 2000/2000 (5th pct +0.105) | 0.57 | **H-NL EXCLUDED** |
| all isolated | canonical | 0.1115 | 0.3326 | +0.221 | 2000/2000 | 0.88 | H-NL EXCLUDED |
| all isolated | alt | 0.1307 | 0.3522 | +0.222 | 2000/2000 | 0.81 | H-NL EXCLUDED |

- Mean signed residual log(g_obs/g_pred) on the overlap: H-L −0.043 / −0.081, H-NL −0.245 / −0.269 (blue). H-NL over-predicts the
  rotation curves by a factor of about 1.8.
- Context only: KiDS blue lensing vs the law, χ² 21.7 / 25.7 for 15 bins (can / alt); all isolated, 194 / 133 (the red half carries
  the early-type excess the record already knows: CFG585, CFG700).
- MUTATE: M1 (g_cold,req = 0) gives Δ = 0 exactly; M2 (Newtonian lensing) gives NOT DIAGNOSTIC.

## Reading

1. **The response sector must lens like mass**, at the accelerations where lensing and rotation curves overlap. A response that acts
   on matter but not on light (for example a conformally coupled scalar, as in the stable construction of astra's
   STABLE_SOURCED_RESPONSE) is excluded as the source of the law, whatever collisionless cold matter accompanies it.
2. This sharpens the lensing ⇄ stability fork of MECHANISM_JOINT_2026-10-12.md into a requirement: the response must couple to the
   metric (lens), and a metric-coupled polarization medium is the class with the growing mode (astra POLARIZATION_REPAIR_GATE;
   CFG660 S5). A completion has to be stable **and** lens: for example a disformal coupling, or a stiff sector whose energy
   gravitates. That is now the single sharpest open requirement for the mechanism.
3. **Limits, stated once:** different populations (KiDS isolated lenses vs SPARC discs; the blue bin narrows but does not remove
   this); B21's g_bar recipe vs SPARC rotmod; the SIS ESD → g_obs conversion; KiDS covariance only (SPARC errors enter through the
   harness weights). The excluded gap (0.16 dex, a factor of 1.8) is large compared with each of these.

## Disclosures (2026-10-12)

- The criteria quoted 179 SPARC points for [3e-13, 3e-12]; the frozen procedure's overlap is [lowest KiDS centre ≥ 3e-13,
  highest centre] = [4.04e-13, 3.92e-12], which holds 324 points. The procedure, not the quoted count, was frozen.
- After the first run: a tar extraction filter (`filter="data"`) and a cleaner covariance-diagonal check were added, and the
  MUTATE exit codes were wired as frozen. All numbers are identical before and after.
