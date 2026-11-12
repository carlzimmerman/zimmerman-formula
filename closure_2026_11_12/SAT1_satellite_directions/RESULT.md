# SAT1 RESULT: the satellites' actual directions LOWER the field reading's apparent mass beyond 150 kpc

2026-11-12. Criteria `FROZEN_CRITERIA.md` (sha256 in `FREEZE_STAMP.txt`, frozen 20:26:56 UTC before
the satellite table was downloaded or any script written). One amendment (`AMENDMENT_A1.md`, KA1's
Monte Carlo draw count; written after run 1 stopped at KA1 and before any label). TEST lane. Adopts
nothing. Relabels no other lane. Satellite positions are a web download and are PROVISIONAL.

## Labels (bin B2, 150 to 300 kpc, primary statistic R_mean; headline = census baryons, primary sample)

| case | canonical | alt |
|---|---|---|
| **census, G239 formula (headline)** | **ANISOTROPY LOWERS IT, NOT ENOUGH** | **ANISOTROPY LOWERS IT, NOT ENOUGH** |
| census, REL variant | ANISOTROPY LOWERS IT, NOT ENOUGH | ANISOTROPY LOWERS IT, NOT ENOUGH |
| MB15 hot gas, G239 formula | ANISOTROPY LOWERS IT, NOT ENOUGH | ANISOTROPY LOWERS IT, NOT ENOUGH |
| MB15 hot gas, REL variant | ANISOTROPY LOWERS IT, STILL ENOUGH | ANISOTROPY LOWERS IT, STILL ENOUGH |

Bin B1 (100 to 150 kpc), direction only: G239 formula LOWERS (both footings, both baryon variants);
REL variant RAISES, FRAGILE (census) / RAISES (hot gas), by 2 to 4 per cent.

No case raises the B2 reading. The direction does not depend on the footing: the ratios agree to
0.002 between canonical and alt.

## Numbers

Sample: Local Volume Database `dwarf_mw.csv`, host Milky Way, confirmed galaxies, Galactocentric
50 to 300 kpc: 35 objects; 13 in B1, 9 in B2 (Hydra II, Leo IV, Canes Venatici II, Leo V, Pisces II,
Columba I, Canes Venatici I, Leo II, Pegasus III, Leo I). All 35 have proper motions, so V-PM equals
the primary sample. In B2 the mean cos(psi) to the direction the field points toward is +0.28: the
satellites sit preferentially on that side (Leo I, Leo II, Leo IV, Leo V, Hydra II at cos(psi) 0.71
to 0.94).

Required factor F (line must rise by F for the median class-S plateau pull to reach -2):
census 1.258 (canonical) / 1.152 (alt); MB15 hot gas 0.821 / 0.751 (the angle average already
passes).

| B2, census | mean M_app | mean M_avg | R_mean | LOO range | bootstrap 16-84 | R_med |
|---|---|---|---|---|---|---|
| G239, canonical | -3.95 | 5.26 | -0.75 | -1.76 to 0.10 | -2.20 to 0.77 | -1.51 |
| G239, alt | -4.33 | 5.75 | -0.75 | -1.76 to 0.10 | -2.20 to 0.77 | -1.51 |
| REL, canonical | 4.81 | 5.26 | 0.914 | 0.882 to 0.950 | 0.846 to 0.982 | 0.863 |
| REL, alt | 5.25 | 5.75 | 0.914 | 0.881 to 0.950 | 0.845 to 0.982 | 0.862 |

(10^11 Msun.) With MB15 hot gas, REL: R_mean 0.934 / 0.933 against F 0.821 / 0.751. Variant V-ALL
(11 in B2): REL 0.940 / 0.940 census, 0.960 / 0.959 hot gas; the hot-gas V-ALL case is labelled FRAGILE because
its leave-one-out range (0.937 to 0.995) crosses 0.98 (LOWERS vs NO CHANGE); it stays above F.

## What it says

1. **G239's formula, taken literally, gives negative apparent masses for 7 of the 9 B2 satellites.**
   Beyond about 150 kpc the record's field (0.0127 a0) exceeds the Galaxy's own Newtonian pull
   (0.008 a0 at 200 kpc), and the code's g_r includes the external field's own uniform acceleration.
   On the side the field points to, the net acceleration is outward. That is the "parallel diverges"
   behaviour G239 reported, seen from the other side. As a satellite-mass reading it is not usable:
   it says how the uniform field enters, not what a tracer analysis would infer.
2. **The REL variant (frozen in advance) is the physical reading.** A satellite's motion is measured
   relative to the Galaxy, which is itself accelerated by the field; subtracting that uniform part
   leaves an apparent mass 9 per cent BELOW the angle average in B2 (bootstrap 0.85 to 0.98), on
   both footings. In B1 it is 2 per cent above, within the noise.
3. **So the satellites' placement does not rescue PLT1's plateau rows.** The census line had to rise
   by a factor 1.26 / 1.15; the satellites' actual directions move it by 0.91 (REL) or turn it
   negative (G239). With MB15 hot gas counted the angle-average line already clears the rows
   (F < 1), and the 7 per cent drop from the directions leaves it clear (0.93 vs 0.82 / 0.75).
4. The hand expectation (LOWERS IT, low confidence) was right in sign.

## Checks

KA1 to KA6 pass on run 2 (run 1 stopped at KA1, see the amendment; output kept):
- KA1 isotropic mean over 2e7 draws 5.2678 +- 0.0041 vs quadrature 5.2642 and G239's 5.264 (0.07 per cent).
- KA2 at 80 kpc: parallel +0.576, perpendicular +0.014 (G239: +58, +1 per cent; tolerance 1 point).
- KA3 geometry: Sun to centre 0.021 kpc; NGP b = 90.0000; along the field mu = -1 gives -28.6 (below
  the 5.26 average), opposite gives +35.2 (above).
- KA4 SI recomputation with scipy quad: 5.26421 vs 5.26421.
- KA5 LMC 49.6 kpc; Leo I r 262.0 kpc; 35 primary rows. KA6 F reproduces median -2.0000.
- Hand check in SI for Leo I (r 262 kpc, mu -0.805, canonical): M_app -39.75 (script -39.75), REL
  4.542 (script 4.539; the hand value uses M_b at 0.9995 of the census total).
Mutations (`sat1_mut.out`): M1 bites (90 deg rotation about the z axis moves B2 R_mean from -0.75 to
+0.76; over the pole to -0.59); M2 bites (sign flip to +2.50); M3 e_N = 0 gives R = 1 to 1e-12.

## Limits

- **This is the direction of the bias, not a recomputed mass.** Published satellite masses come from
  velocities through an estimator (tracer mass estimators, distribution functions), not from the
  radial acceleration at each satellite's present position. A satellite's speed reflects the
  potential along its orbit; a position-weighted acceleration is a proxy.
- B2 has only 9 satellites (11 in V-ALL); the leave-one-out and bootstrap ranges are wide for the
  G239 reading and about +-0.05 for REL.
- REL subtracts nu(e_N) e_N mu, the QUMOND acceleration of a test body far from the Galaxy; the
  Galaxy's own centre-of-mass acceleration in QUMOND is not exactly this. It is a frozen variant, not
  G239's code.
- QUMOND kernel; uniform static field; LMC's field and the LMC-hosted satellites (host 'lmc', 9 rows,
  excluded by the frozen selection) not included; sky coverage of the ultra-faint surveys biases the
  directions toward the north, and that bias is part of what a real satellite sample carries.
- PLT1's literature rows mix globular clusters and satellites; this lane uses satellite positions only.

## Files

`FROZEN_CRITERIA.md`, `FREEZE_STAMP.txt`, `AMENDMENT_A1.md`; `lvdb/dwarf_mw.csv` and
`lvdb/SOURCE.txt` (URL https://raw.githubusercontent.com/apace7/local_volume_database/main/data/dwarf_mw.csv,
46509 bytes, sha256 8e80a917658c150474f80c8541d36a119eb5b255531dae5def5a85866a4ff021, PROVISIONAL);
`sat1.py` (run with `python3 -I sat1.py`); `sat1.out`; `sat1_results.json`; `sat1_mut.out`;
`sat1_run1_KA1_failed.out`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
