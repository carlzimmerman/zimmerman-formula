# SRJ3 RESULT: the reference layout on SRJ2's cluster-regime discs

**NO VERDICT (no power) / NO VERDICT (no power) (canonical / alt), as frozen. Required twin TW-H (halo halved) does not
bite. Reading, not graded: the reference layout lies inside DD1's line on both footings (off -0.006 / -0.040 dex).**

The single R_e point RC100 gives per disc cannot tell the reference halo from half of it, nor from the law: all three sit
inside the line. Only removing the cold component altogether is excluded. So SRJ2's G2 miss is neither shown to be a mere
coverage technicality nor shown to be a physical failure. Nothing here is a pass of the theory.
TEST lane. Criteria 97cf1ef5ca (alone, before any script or number); scripts and outputs 3864669e69; no amendment.
Footings never pooled. Cold dark energy is a gravitating field component; no particle. SRF1 and SRF1R were not opened.

## Rows (DD1's class line: |off| <= 0.10 dex and |off| <= 3 se; e = 0.218 dex per disc)

| row | canonical | alt |
|---|---|---|
| n (SRJ2's cluster-regime RC100 discs) | 31 | 22 |
| off = median(Y - F), dex | -0.0061 | -0.0396 |
| se ; 3 se | 0.0392 ; 0.1175 | 0.0465 ; 0.1395 |
| line | holds | holds |
| discs with abs(d) <= 0.218 | 26 / 31 | 19 / 22 |
| X bracket z0 (59.49 / 59.50) ; z1 (55.72 / 55.73) | -0.0081 ; -0.0061, holds | -0.0416 ; -0.0396, holds |
| TW-N no cold component (must bite) | +0.1160, FAILS, bites | +0.1150, FAILS, bites |
| TW-H halo halved (must bite) | +0.0139 (moves +0.020), **no bite** | -0.0187 (moves +0.021), **no bite** |
| TW-L law restored (reported) | +0.0267 (moves +0.033), no bite | -0.0058 (moves +0.034), no bite |
| **frozen word** | **NO VERDICT (no power)** | **NO VERDICT (no power)** |

Y = log10(g_obs / g_bar), g_obs = V_c(R_e)^2 / R_e (observed), g_bar = G (M_b / 2) / R_e^2; F = log10(g_mod / g_bar),
g_mod = g_bar + G C_R(R_e) / R_e^2 with FRZ1's halo at the disc's z (M_ta = X M_b h / (1 - FB), Duffy c).

## Why each row came out as it did

- **Main.** Inside R_e (2.5 to 9.6 kpc) the reference halo (r_s 40 and 63 kpc for the two K5 discs) holds a cold mass of 0.06 to
  0.44 of the disc's baryons-plus-cold total, median f_cold 0.29 / 0.28. That adds F ~ +0.03 to +0.25 dex, and the
  observed Y has the same median. Direction of the misfit: none at the median on canonical; slightly too heavy on alt.
- **Scatter.** Per-disc d runs from -0.67 (K20 ID5, V_c 174 km/s at R_e 2.5 kpc) to +0.33 (U4 31577). Robust scatter
  0.151 / 0.137 dex, below the stated 0.218 error, so se is set by the stated errors.
- **Shape (reported).** Canonical M_b halves: +0.076 (log M_b <= 11.15) and -0.039 (above), a 0.115 dex mass trend; z
  halves +0.003 / -0.006. Alt flat: -0.040 / -0.039 by mass, -0.026 / -0.040 by z.
- **TW-H and TW-L.** Halving the halo cuts f_cold from ~0.29 to ~0.17, which moves F by only ~0.02 dex at the median,
  because baryons dominate inside R_e. The law at these g_bar (near a0) adds about as much as the reference. The line
  (0.10 dex) is wider than any of these differences. Only TW-N (no cold component at all) leaves the line.
- **Authors' f_DM (reported, never graded).** Their own decompositions give median f_DM 0.16 / 0.14 against the model's
  f_cold 0.29 / 0.28: by the authors' mass models the reference is about twice too heavy inside R_e. The inherited line
  does not see this, because Y uses only V_c and the paper's M_b, and the thin-disc M_b / 2 field is not their model.
- **Context (reported).** The 69 / 78 galaxy-regime discs under the law: off +0.107 / +0.092 (the law under-predicts;
  canonical just outside 0.10).

## Checks

- **K1** 31 / 22 cluster-regime; covered 69 / 78 at f 0.75, 1.00, 1.25; names equal srj2_rc.json's. PASS.
- **K2** SPARC reference reading 0.0640 / 0.0387 canonical, 0.0559 / 0.0332 alt. PASS. Cluster-regime with PD1 M_b:
  9 (ESO563-G021, NGC0801, NGC2955, NGC5371, NGC6195, UGC02487, UGC02885, UGC09133, UGC11455) / 2 (UGC02487, UGC02885);
  FLD1 M_b 3 / 0. Not re-graded.
- **K3** 100 rows, all primary discs finite. PASS. **K4** generalised C_R = SRH1's CR at z 0 (0 difference). PASS.
- **K5 (SI, second route)** zC 400569 (z 2.24): r_200c 121.62 vs 121.61 kpc, r_s 39.53 vs 39.53 kpc, g_mod 4.4288e-10
  vs 4.4290e-10 m/s^2; D3a 6004 (alt): 170.01 vs 169.99 kpc, 8.2774e-10 vs 8.2777e-10. PASS.

## Estimate against the outcome

Mine (frozen): off -0.10 to -0.15, P(FAILS, too heavy) 0.50, P(FITS) 0.40, NO VERDICT 0.05. **Wrong on the number**:
off is -0.006 / -0.040. The F estimate (+0.23) was right for a typical disc; Y was higher than I guessed (I read Y from
the authors' f_DM, which is where the factor-two tension actually sits). TW-L: I expected a bite; it does not.

## What this means for the regime-split joint

It is not rescued and not killed on rotation curves. One velocity at R_e cannot weigh the cold halo of a massive z ~ 2
disc to better than a factor of two. A gate that bites needs outer points (curves to 2 to 4 R_e) or the authors'
decompositions graded as data; neither was frozen here.

## What is not verified

- The observed V_c is the authors' pressure-corrected value; no errors on disk (DD1's stated 10 % used). M_b is the
  paper's (gas from scaling relations). g_bar uses DD1's M_b / 2 construction, not each disc's bulge / disc split.
- No bracket on v_stiff or c. Sample fixed at K1's in the X bracket (a smaller X would also change membership).
- Nothing was fetched; the data were on disk.

## Files

`FROZEN_CRITERIA.md` (97cf1ef5ca). `srj3.py`, `srj3.json`, `srj3.out`, `srj3_MUTATE_TWN/TWH/TWL.json / .out`
(3864669e69). SRJ2's srj2_rc.py is executed read-only from its own path; nothing is written in its folder.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.

## Dated correction (2026-11-13)

The sentence under "TW-H and TW-L" that halving the halo cuts f_cold "from ~0.29 to ~0.17" is wrong. It was a hand
figure, not a computed one. SRJ4's separate code gives a median f_cold of 0.245 / 0.238 with the halo halved: the halo
is re-solved, so the cold mass inside R_e scales about as M^(1/3). That agrees with this lane's own computed twin shift
(+0.020 dex at the median corresponds to an f_cold of roughly 0.25, not 0.17). No graded number, twin outcome or word
changes.
