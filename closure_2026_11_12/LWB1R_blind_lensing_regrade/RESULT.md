# LWB1R RESULT: blind re-grade of LWB1 (DESI DR1 Lensing Without Borders, Delta Sigma + wp amplitude)

## Blind label (unchanged from RESULT_BLIND.md, 449a97c992)

**J (KiDS-1000 + DES Y3 + HSC Y3): AMPLITUDE CONSISTENT / AMPLITUDE CONSISTENT (canonical / alt), FRAGILE.** sigma8
0.7862 / 0.7871 +- 0.0285, gap +0.91 / +0.87 widths below form B's 0.8121 / 0.8120. Per survey: KiDS NO POWER, DES
TENSION (+3.49 / +3.47), HSC-Y3 AMPLITUDE CONSISTENT (-1.28 / -1.32), K+D TENSION (+3.12 / +3.09). My code passes every
gating known answer as frozen, so this is the frozen reading; no amendment was needed.

A consistency check, not independent evidence (KiDS-1000 and DES Y3 are sources already tested). CONSISTENT is not a pass
for the theory; nothing here says the data favour the framework. Cold dark energy; footings never pooled.

## COMPARISON with LWB1's RESULT.md: AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL

| row (canonical) | LWB1 | LWB1R (mine) | difference |
|---|---|---|---|
| J sigma8, gap, chi2/dof | 0.7864 +- 0.0285, +0.90, 126.2/105 | 0.7862 +- 0.0285, +0.91, 126.2/105 | 0.0002 |
| KiDS | 0.7596 +- 0.0508, +1.03 | 0.7590 +- 0.0509, +1.04 | 0.0006 |
| DES | 0.6470 +- 0.0474, +3.48 | 0.6466 +- 0.0474, +3.49 | 0.0004 |
| HSC-Y3 | 0.8580 +- 0.0355, -1.29 | 0.8575 +- 0.0353, -1.28 | 0.0005 |
| K+D | 0.6990 +- 0.0364, +3.11 | 0.6988 +- 0.0363, +3.12 | 0.0002 |
| Planck18 reference on K+D, S8 | 0.713 +- 0.037 | 0.710 +- 0.037 | 0.003 |
| point-mass bracket on J | 0.6809, +2.62 GAP STAYS | 0.6800, +2.64 (width 0.0500: NO POWER line) | label wording, see below |
| R_min 12 on J | 0.7306, +2.33 | 0.7300, +2.33 | 0.0006 |
| N = 1 on J | 0.8732, -1.92 | 0.8733, -1.93 | 0.0001 |
| MU1 J ratio | 0.857 | 0.8565 | 0.0005 |

Alt agrees the same way (largest sigma8 difference 0.0002). Every graded label is the same on both footings.

**Differences and their causes (none moves a graded label):**
1. **As-frozen reading.** LWB1 as frozen is NO VERDICT because its KA1 check truncated the power-law line of sight at
   pi = 3000. My power-law check (xi to 2e5, finite-interval plus Fourier quadrature) passes as frozen: wp within 0.10 %,
   Delta Sigma within 0.01 %. This independently supports AMENDMENT A1's diagnosis that the fault was in the check, not
   in the pipeline. So the graded label stands without the amendment.
2. **Point-mass bracket wording.** Both find sigma8 0.680-0.681 with width 0.0500, g +2.62 / +2.64. LWB1 calls it GAP
   STAYS; my grader applies NO POWER (width > 0.05) first, and the width is at the line (0.05001 canonical, 0.05005 alt). A reported bracket, not
   graded; both readings say the same thing: J's consistency does not survive a free enclosed-mass term.
3. **Blinding slope (KA4).** LWB1: KiDS +0.010 +- 0.028, HSC +0.010 +- 0.025. Mine (diagonal errors, DES points with S/N > 2,
   R_max the smaller of the pair): pooled c 0.028 +- 0.012, 2.46 sigma, under the 3-sigma line but closer to it. Method
   difference (weighting and point selection), not a different file; it passes in both.
4. **Reference-spectrum framing.** Both pipelines read the Planck spectrum low on K+D (S8 0.710 / 0.713 against the
   PROVISIONAL 0.794). LWB1 states it as 2.2 of its own widths; I state it as -1.92 combined widths and add an
   offset-shifted row: with each vector's Planck offset removed, form B's gaps are +0.55 to +1.05 everywhere. Both read the
   DES / K+D TENSION as carried mostly by the method on these vectors, not by form B.
5. **pi_max infinity.** LWB1 used 300 (0.7690, +1.58); I used the full line of sight (0.7673, +1.64). Both p ~ 0.01.

The near-identical numbers are expected: both lanes use the same data vectors, covariances and stored spectra (BX1 N(k),
CO1 R_tot, KL1 targets) under the same frozen model. They confirm the arithmetic (transforms, projections, Kaiser wp, fit),
not the model's inputs, and they are not two measurements.

**Blindness caveat (from READING.md).** I had seen LWB1's canonical first-run rows in its AMENDMENT_A1 and its result
commit subject before writing any code. I did not open its scripts, outputs or RESULT.md until RESULT_BLIND.md was
committed. My code was written from the frozen criteria; the agreement to <= 0.0006 in sigma8 is a result of the same
inputs, but a fully blind re-grade it is not.

## Not checked by either lane

Lange+'s 0.794 (not on disk); the BGS-LRG and wp-Delta Sigma cross-covariances (zero); nonlinear or stochastic bias;
projection over the lens n(z); the realisation noise of BX1 pair A; whether `blindA` hides a common offset.

Commits: READING 55b7a264a6; code and run 434df4e462; graded rows ee6f51a542; RESULT_BLIND 449a97c992; this file next.
Not pushed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
