# ST1: does the hot/cold step have several causes? IN PART. The IMF explains the early types; the dSph and UDG steps survive their own systematics

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter particle is adopted; HC1's fermion is graded only
as the record's test object. Footings graded separately, never pooled.

- Criteria: FROZEN_CRITERIA.md (3622fad837), committed alone before any script.
- Script: st1.py. It execs GB1's loaders and gates read-only, uses the plain law throughout and keeps GB1's lines.
  One thread, about 1 s, well under 1 GB. A rerun gives a byte-identical st1.json.
- Outputs: st1.json / st1.out (main) and st1_MUTATE.json / st1_MUTATE.out (twins).

**Label: MULTI-CAUSE IN PART.**
- X-ray ellipticals and the KiDS early/late split are explained by IMF variation, on both footings.
- The dSph satellites (bright M31) and the Coma UDGs still sit above the law after their own measured systematics,
  on both footings.
- So it is not "clusters and groups only". The reduced target has four rows: clusters, groups, bright M31 dSphs and
  Coma UDGs.
- HC1's fermion and QX12 iter_3's sea both fail the reduced battery. They also fail the conditional battery that
  drops the dSphs and UDGs, because neither passes X-COP or the groups.

## Class x footing (plain law; GB1 lines unchanged)

| Class (gate) | Systematic applied (size, source) | canonical: raw -> residual | alt: raw -> residual | Cell (canon / alt) | Class label |
|---|---|---|---|---|---|
| X-ray ellipticals (G4, \|mean\| <= 0.15) | IMF, Posacki+2015 (QX26), per-galaxy sigma_e | +0.210 -> **+0.093** | +0.189 -> **+0.074** | PASS / PASS | **EXPLAINED** (sigma x0.9: +0.107 / +0.088; x1.1: +0.081 / +0.062) |
| KiDS early/late split (G7, \|R\| < 2 sigma_tot = 0.128) | IMF, early sigma {130, 170, 210}, late 60 km/s (QX26) | R +0.158 (2.46 sigma) -> **+0.121 / +0.098 / +0.080** (1.89 / 1.53 / 1.24 sigma) | +0.158 -> **+0.122 / +0.098 / +0.080** | PASS / PASS (all three) | **EXPLAINED** (thin: 0.007 dex inside the line at 130 km/s) |
| dSph satellites (G6, each class's 95 % CI contains 0) | equilibrium cut, tau = R_e/r_J < 0.375 (QX24 estimator, Z2 C1 line); keeps bright M31 21/25, MW classical 8/8 | bright M31 +0.199 [+0.079, +0.393] -> **+0.214 [+0.101, +0.445]**; MW classical +0.217 -> +0.217 [-0.049, +0.544]; LG field +0.019 (untouched) | bright M31 +0.188 -> **+0.201 [+0.089, +0.433]**; MW classical +0.207 [-0.057, +0.532]; LG field +0.007 | FAIL / FAIL | **NOT EXPLAINED**. The cut raises the step |
| Coma UDGs (G5, \|mean\| <= 2 sigma) | CFG948 recipe on v3 (S1): M_* +-0.2 dex, sigma +-15 %, D +-5 %. Q = quadrature (GB1); L = all three at the favourable edge, linear sum (0.353 dex) | +1.121 -> Q **+4.28 sigma_U**; L **+0.768** (+6.75 sigma_stat) | +1.078 -> Q **+4.11 sigma_U**; L **+0.724** (+6.37 sigma_stat) | FAIL / FAIL (both readings) | **NOT EXPLAINED** (residual 0.68 / 0.67 of raw; the 2/3 line sits 0.02 / 0.006 below, so PARTLY would read the same FAIL) |
| X-COP (G2) | none in this lane | +0.468 (rms 0.476) | +0.435 (0.444) | FAIL / FAIL | remains |
| groups (G3, >= 16 of 20) | none in this lane | 0 / 0 of 20 (median +0.367 / +0.205 at f* 0 / 1) | 0 / 0 (+0.328 / +0.168) | FAIL / FAIL | remains |
| SPARC (G1), Solar System (G8) | none | Z +0.027, rms 0.136; SS 0.211 | Z -0.001, rms 0.133; SS 0.190 | PASS / PASS | no step |

**Reported only.**
- IMF on the hot systems (GB1's L1 bracket): X-COP +0.451 to +0.445 (canonical) and +0.418 to +0.412 (alt); groups
  pass 0-1 of 20.
- Lensing masses are at least the hydrostatic ones (QX21 T3). QX30's cluster data-assumption audit is ROBUST.
- None of this lowers the cluster or group row.

## Verifying the two non-IMF FAILs

**dSph satellites.**
1. **The cut runs the wrong way.** The four satellites dropped (And I, XVII, XIX, XXV) are the most tidally exposed,
   and they sit lowest. Removing them lifts bright M31 from +0.199 to +0.214 (canonical).
2. **The T3b direction confirms it.** Over the 33 graded satellites, Spearman(offset, log tau) is -0.33 (p 0.06) and
   the slope is -0.43 dex per dex, on both footings. The line at tau = 0.375 still reads +0.094 / +0.082 above the
   anchor.
3. **Tidal inflation would need the opposite sign.** It would make the most exposed systems sit highest.
4. **The pericentre reading** (tau x 2.08) keeps 15/25 of bright M31 and reads +0.305 / +0.292, still FAIL.
5. **The strict line** tau < 0.05 leaves 1/25 and 0/8: NO VERDICT, no power, as QX24 found.
6. **The CI is not a power artefact.** Bright M31's CI excludes zero at N = 21. The MW classical class still contains
   0 only because N = 8.
7. **The record agrees.** X20 (Spearman(E, log tau) about 0; equilibrium subset EXTRA at 5.4-5.8 sd) and Z2 ("tides
   are not implicated for any flavor") reached the same answer by other estimators.

**Coma UDGs.**
1. **Every data systematic at once is not enough.** With all three at their full favourable edge, summed linearly
   (more generous than the record's quadrature), the residual is +0.77 / +0.72 dex. That is 6.4-6.8 statistical sigma.
2. **S1's host-field variants all stay above 3.3 sigma_sys:** field / 2 gives +0.944 / +0.887 (z_sys 3.60 / 3.38);
   dproj gives +1.215 / +1.182.
3. **The one reading that would pass drops the EFE entirely.** The isolated AQUAL solve gives +0.325 / +0.285 dex
   (z_sys 1.64 / 1.45). That is a change of field equation, not a mass systematic: the v3s / AC2q static sector has the
   EFE. It is reported here, not graded.

## What the record leaves: the target

The remaining set is X-COP, groups, bright M31 dSph satellites and Coma UDGs, on both footings. An ingredient has to
fill these and stay out of the SPARC discs and the LG field dwarfs. Ellipticals and KiDS early types need nothing
beyond the IMF.

The uniform extra baryon factor f that nulls each remaining row (GB1's L0 convention: b = 1 + f, F = 1, class
statistic set to 0) is a target statement, not a candidate:

| Row | f canonical | f alt | Compare (KD1) |
|---|---|---|---|
| SPARC discs (must stay out) | <= 0.33 | <= 0.19 | KD1 |
| X-COP | 4.18 | 3.78 | 4.2 / 3.8 |
| groups (median residual, f* 0 / 1) | 3.70 / 1.35 | 3.05 / 1.03 | 1.2-3.5 / 0.9-2.9 |
| bright M31 dSphs (equilibrium subset) | 1.64 | 1.50 | ~1.7 / 1.3 |
| Coma UDGs (all systematics at the favourable edge / raw) | 23.6 / 86.4 | 20.2 / 77.7 | ~80 (raw) |
| LG field dwarfs, ellipticals after IMF, KiDS after IMF | 0 (no step left) | 0 | |

So exit 1 relaxes the target only at the early-type rung. The dSph rung (f about 1.5-1.6 in satellites but 0 in field
dwarfs of similar mass) and the UDG rung (f >= 20 even at the most generous systematics) stand. The reduced target of
the brief ("clusters and groups only, with discs, dSphs and UDGs excluded") is **not** what the record leaves. It is
graded below only as the conditional reading.

## Reduced battery: the two record test objects

Each corrected row is read from the object's committed record cell minus the L0 shift that the ST1 systematic makes
on that class (first-order, as frozen). Rows G1, G2, G3 and G8 are the record cells unchanged. G9 (CMB) is as the
record has it: HC1 fails it with chi^2 166-194; QX12 iter_3 was not CMB-graded.

| Object | Footing | G1 | G2 X-COP | G3 groups | G4 (IMF) | G5 (Q / L) | G6 (cut) | G7 (IMF) | G8 | Reduced battery | Conditional (G5, G6 dropped) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HC1 fermion, 11.14 eV | canonical | PASS | FAIL +0.392 | FAIL 0, 3 of 20 | PASS +0.091 | FAIL +1.120 / +0.767 | FAIL bright M31 +0.229 [+0.109, +0.423] | PASS +0.118 / +0.095 / +0.076 | PASS | **FAILS (G2, G3, G5, G6)** | **FAILS (G2, G3)** |
| HC1 fermion | alt | PASS | FAIL +0.360 | FAIL 0, 3 of 20 | PASS +0.070 | FAIL +1.077 / +0.723 | FAIL +0.219 [+0.099, +0.413] | PASS +0.118 / +0.095 / +0.077 | PASS | **FAILS (G2, G3, G5, G6)** | **FAILS (G2, G3)** |
| QX12 iter_3 sea | canonical | | no c_s0 of 60 passes X-COP; best rms 0.463 at 1135 km/s (mean +0.450); c_min over-fills at -0.713 | no c_s0 passes X-COP and the groups | | | | | | **FAILS (G2, G3)** at every c_s0 | **FAILS (G2, G3)** |
| QX12 iter_3 sea | alt | | none of 60; best rms 0.436 at 1216 km/s (+0.423); c_min -0.724 | none | | | | | | **FAILS (G2, G3)** | **FAILS (G2, G3)** |

Dropping the dSph and UDG constraints frees QX12's c_s0, which those galaxy gates had fixed. But no value on its whole
100-6000 km/s scan passes X-COP. HC1's mass was fixed by the CMB abundance, not by the dSphs or UDGs, so dropping
them does not move it. Both objects fail the cluster and group rows they would have to carry alone.

## Known answers and twins

| Check | canonical | alt | line |
|---|---|---|---|
| KA1 GB1 L0, 23 graded numbers (G1-G8) | 0 | 0 | 1e-9 |
| KA2 S-E vs QX26 D_imf | 2.5e-7 | 3.2e-7 | 1e-6 |
| KA3 S-K vs QX26 KiDS R (as frozen) | **FAIL 3.4e-4** | **FAIL 3.1e-4** | 1e-4 |
| KA3' QX26's linearised formula replayed (post-freeze) | 5.0e-9 | 5.4e-9 | 1e-8 |
| KA4 QX24 tau p10/p50/p90 (0.0641 / 0.1396 / 0.3842) | 0 | 0 | 1e-9 |
| KA5 sigma_U from S1's se and sigma_sys | 0 | 0 | 1e-12 |
| KA6 HC1 / QX12 record cells read back | max 4.0e-4 | | 5e-4 |
| M1 Newton on the corrected battery | FAIL G1 (Z +0.431, rms 0.514) | FAIL G1 | must fail: BITES |
| M2 IMF inverted (b = 1/f_IMF) on G4 | FAIL +0.322 | FAIL +0.299 | must fail: BITES |
| M3 no cut reproduces GB1's G6; zero line gives NO VERDICT | PASS | PASS | must hold |

## Disclosed (post-freeze)

1. **KA3 tolerance was mis-set.**
   - What differs: QX26 linearises the KiDS IMF shift (slope dlog g_law / dlog g_N x log10 f_IMF). GB1's L1, which
     ST1 uses as frozen, applies the exact law. The two differ by 0.7-3.4e-4 in R.
   - Not a loader fault: replaying QX26's linear formula reproduces its R to 5e-9. That is finite-difference roundoff
     at h = 1e-4, so the replay line was set to 1e-8.
   - Effect on the cell: none. The tightest bracket value sits 0.007 dex inside the line. Grading proceeded on that
     basis; st1.json carries both KA_all_as_frozen (false) and KA_all (true).
2. **The UDG class label rests on a 2/3 rule that sits near its boundary.**
   - The residual / raw ratio is 0.685 / 0.672 against the 2/3 line, so the label reads NOT EXPLAINED rather than
     PARTLY.
   - The cell is FAIL either way, and so is the lane label.
3. **The reduced-battery rows for the test objects are first-order.** Each corrected row is the object's record cell
   minus L0's systematic shift. This is exact for data-side shifts (UDG edges, the dSph subset median applied to the
   class number). For the IMF it is approximate: HC1's fermion share depends on the baryon mass, and that was not
   re-solved. None of these rows decides an object's label. Both objects fail G2 and G3, which carry no correction.
4. **In the MUTATE output, M2's "raw" figure is Newton's.** M2 itself is the inverted IMF on the plain law, as frozen.

Kappa = 1/2 FITTED; not theory closed.
