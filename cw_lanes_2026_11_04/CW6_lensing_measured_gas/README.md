# CW6_lensing_measured_gas: GAP UNCHANGED on both footings. The measured kSZ gas leaves the red and blue amplitudes where they were and worsens A30. Gas held inside R_vir narrows red, and at Zhang's X-ray level it pushes blue over

Criteria `FROZEN_CRITERIA.md` (7ac475d533), committed alone before any script or number. Script `cw6.py`. Outputs `cw6_<mode>.{json,out}`; MUTATE twins `cw6_<mode>_MUTATE.{json,out}`.

**Not blind.** LE1's gap, GH10 and GH11's kSZ amplitudes, GH2's X53 result and S2's gas ladder were known before freezing (see the criteria). No CW6 number existed. The F1 and F2 fits to the DR2 points are new.

κ = ½ FITTED and held fixed. The cold sector stays retired; nothing here adds a particle or a cold component. Not theory closed. Nothing here says the data favour the framework. No downloads. No grader was edited: each runs from a copy or an exec of the record's text, and the hot-gas term is the only swap.

## How to run
```
cd cw_lanes_2026_11_04/CW6_lensing_measured_gas
export OMP_NUM_THREADS=1 PYTHONHASHSEED=0
nice -n 10 python3 -I cw6.py ksz                  # K2, F1 and F2 fits on the DR2 points
nice -n 10 python3 -I cw6.py gas                  # K3, profile table
nice -n 10 python3 -I cw6.py le1     [--mutate]   # H1: A30, A1, G3 on B21 Fig-3 (LE1's harness)
nice -n 10 python3 -I cw6.py b21c    [--mutate]   # H2: B21 Fig-8 colour bins (S2's forward model, L4 row)
nice -n 10 python3 -I cw6.py si2 <p2_work_dir> [--mutate]   # H3: SI2's clean lenses S1, S3 by colour
nice -n 10 python3 -I cw6.py verdict [--mutate]   # frozen labels; --mutate is printed, not graded
```
- `<p2_work_dir>` holds P2's phase-A outputs (`p2_phaseA.json`, and `p2_meas_d8787042a095deef.npz`, sha256 def6b9284d02…) and P2's table caches. It is not committed. P2 phase A rebuilds it from F1's KiDS reader cache.
- Peak RSS is 0.08-0.72 GB per mode, and the whole run takes about 4 minutes.

## Checks (all pass)
| Check | Result |
|---|---|
| K1 H1, the fixed term against `le1_real.json` | \|d\| 0: A30 +9.27 / +6.52, no two-halo +9.19 / +6.17, A1 +0.0887 / +0.0500, G3 +5.01 / +3.32 |
| K1 H2, S2's L4 row | \|d\| 0 for blue, red and all, both footings |
| K1 H3, SI2 at R0 (S1, S3; all, red, blue) | \|d\| 0. The own-lens table and neighbour term are identical to P2's |
| K2, GH11's A through this lane's copy | sharp(1.8) 0.54167 and no-miscentring 0.44796, \|d\| 0; narrow F2 off by 5.2e-4 (line 0.02) |
| K3, profile normalisation | 2e-16; sharp total against quadrature 1e-6; narrow F2 4e-5 |
| K4, G3 hook fed CX1's own baryons | 2e-15 |
| MUTATE (gas zeroed) | bites in every harness, sample and footing |

Reported, not frozen: the gas-zeroed twin in H2 reproduces S2's L3 row (no hot gas) exactly, so the swap reaches S2's grader. The label code run on the twin reads GAP WIDENED (red +3.6σ on B21c).

## The gas
**The kSZ fits** (GH11's machinery, b = 0, 13 θ, primary miscentring):
- **New:** F1(1.8) gives A 0.635 ± 0.137 (χ² 15.5/12, p 0.22); F2(1.8) gives A 0.589 ± 0.132 (χ² 17.2/12, p 0.14).
- **On record (GH11):** sharp(1) 0.745, sharp(1.8) 0.542, sharp(3) 0.605.

**M_hot(< r)/M★ at log M★ 10.75** (R_vir 210 kpc):

| Profile | 50 kpc | 100 | 200 | 300 | 500 | total |
|---|---|---|---|---|---|---|
| fixed term (record) | 0.06 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| **P1** sharp(1.8), A 0.542 | 0.08 | 0.28 | 0.92 | 1.84 | 2.73 | 2.73 |
| P2 sharp(1), A 0.745 | 0.11 | 0.38 | 1.26 | 1.37 | 1.37 | 1.37 |
| P3 sharp(3), A 0.605 | 0.09 | 0.31 | 1.02 | 2.05 | 4.93 | 7.32 |
| P4 F1(1.8), A 0.635 | 0.10 | 0.34 | 1.08 | 2.01 | 3.83 | 5.90 |
| P5 F2(1.8), A 0.589 | 0.09 | 0.30 | 1.00 | 1.90 | 3.10 | 3.41 |
| P6 sharp(1), X-ray A = 1 | 0.15 | 0.51 | 1.69 | 1.84 | 1.84 | 1.84 |

- At log M★ ≥ 10.75, every kSZ-normalised profile holds less gas inside 100 kpc than the fixed term. P6 holds about the same.
- Every profile holds more than the fixed term beyond 200 kpc.
- At log M★ 11 (R_vir 295 kpc), P1 holds 0.15 M★ inside 100 kpc. At 10.5, P2 and P6 hold 0.51 and 0.68 there. The full table is in `cw6_gas.out`.

## Result: the frozen colour lines, P1 against the fixed term
A = data/model. z = (A − 1)/σ. m = the move in units of the fixed-term σ.
- B21c is S2's window amplitude on B21's Fig-8 colour bins.
- S1 and S3 are SI2's A_in at 0.03-0.31 Mpc.

| Footing | Sample | Colour | Fixed term | P1 | z after | m |
|---|---|---|---|---|---|---|
| canonical | B21c | red | 1.313 ± 0.063 (+4.96) | 1.306 ± 0.063 | +4.87 | −0.12 |
| canonical | B21c | blue | 0.878 ± 0.074 (−1.65) | 0.861 ± 0.073 | −1.92 | −0.24 |
| canonical | S1 | red | 1.290 ± 0.147 (+1.97) | 1.209 ± 0.135 | +1.55 | −0.55 |
| canonical | S1 | blue | 1.301 ± 0.553 (+0.54) | 1.138 ± 0.509 | +0.27 | −0.30 |
| canonical | S3 | red | 1.762 ± 0.330 (+2.31) | 1.698 ± 0.319 | +2.19 | −0.19 |
| canonical | S3 | blue | 2.108 ± 1.005 (+1.10) | 1.875 ± 0.970 | +0.90 | −0.23 |
| alt | B21c | red | 1.200 ± 0.058 (+3.46) | 1.193 ± 0.057 | +3.36 | −0.13 |
| alt | B21c | blue | 0.802 ± 0.067 (−2.94) | 0.786 ± 0.066 | −3.23 | −0.24 |
| alt | S1 | red | 1.181 ± 0.135 (+1.35) | 1.107 ± 0.124 | +0.87 | −0.55 |
| alt | S1 | blue | 1.187 ± 0.505 (+0.37) | 1.038 ± 0.465 | +0.08 | −0.30 |
| alt | S3 | red | 1.615 ± 0.302 (+2.04) | 1.557 ± 0.292 | +1.90 | −0.19 |
| alt | S3 | blue | 1.926 ± 0.920 (+1.01) | 1.712 ± 0.889 | +0.80 | −0.23 |

**Label per footing: GAP UNCHANGED** (canonical and alt).
- No colour moved by 1σ.
- B21c red stays 4.9σ (canonical) and 3.4σ (alt) above 1.
- Alt blue was already 2.9σ below 1 with the fixed term, and it stays there (−3.2σ).
- **A30 flag: WORSENS.** A30 goes from +9.27 to +10.45 (canonical) and from +6.52 to +13.97 (alt).
- **PROFILE-DEPENDENT:** P2 reads GAP NARROWED and P6 reads OVERSHOOTS (blue). P3, P4 and P5 read GAP UNCHANGED.
- **Brackets:** B2 (extreme miscentring, A 0.851) reads OVERSHOOTS (blue). B1, B3, B4 and B5 read GAP UNCHANGED.

## The other graders (H1, B21 Fig-3, all colours)
| Profile | A30 Z can / alt | A30, no two-halo | A1 dex can / alt (z) | A1 by bin, canonical | G3 z on G1's inventory |
|---|---|---|---|---|---|
| fixed | +9.27 / +6.52 | +9.19 / +6.17 | +0.0887 (6.69) / +0.0500 (3.78) | +0.085 +0.102 +0.071 +0.094 | +2.82 / +1.13 |
| **P1** | **+10.45 / +13.97** | +9.73 / +13.13 | **+0.0852 (6.43) / +0.0467 (3.52)** | +0.067 +0.070 +0.063 +0.111 | +2.16 / +0.48 |
| P2 | +5.94 / +5.91 | +5.41 / +5.34 | +0.0649 (4.90) / +0.0263 (1.99) | +0.051 +0.056 +0.043 +0.086 | +1.61 / −0.07 |
| P3 | +42.22 / +58.23 | +40.42 / +55.89 | +0.0871 / +0.0485 | | +1.90 / +0.22 |
| P4 | +26.73 / +37.63 | +25.46 / +35.99 | +0.0787 / +0.0401 | | +1.73 / +0.05 |
| P5 | +13.01 / +18.18 | +12.20 / +17.20 | +0.0814 / +0.0428 | | +1.98 / +0.30 |
| P6 | +5.92 / +8.01 | +5.36 / +7.37 | +0.0462 (3.48) / +0.0077 (0.58) | +0.034 +0.033 +0.023 +0.070 | +0.73 / −0.95 |

G3 with CX1's own point-mass baryons stays +5.01 / +3.32. Brackets are in `cw6_le1.out` and `cw6_verdict.out`.

## In plain words
1. **The gas the kSZ measures does not close the gap.**
   - Every kSZ-normalised shape (P1, P3, P4, P5) moves B21c red by 0.5σ or less, and A1 by 0.01 dex or less.
   - The gas sits mostly at 200-500 kpc. Inside 100 kpc it is about the same as the fixed term, or lighter.
   - The inner projected signal hardly changes, and the outer signal overshoots. A30 worsens on both footings, and SI2's S1 A_O1 falls from 0.88 to 0.59 (canonical).
2. **Gas inside R_vir is what helps.**
   - P2 (the kSZ amplitude at 1 R_vir, 0.745) narrows B21c red by 1.4σ, 1.313 → 1.227 canonical. A30 improves, +9.27 → +5.94.
   - At Zhang's X-ray value (P6, A = 1), red reaches 1.152 (+2.7σ) canonical and 1.052 (+1.0σ) alt. Blue drops to 0.774 (−3.5σ) and 0.707 (−5.0σ).
   - On B21's colour bins, one gas rule cannot bring red within 2σ without pushing blue over.
3. **On SI2's clean lenses every profile moves the amplitudes by under 1.3σ.**
   - S1 red is within 2σ under every profile; S3 red sits near +2σ under every profile.
   - Blue is too noisy to bind (σ 0.5-1.0).
4. **G3 moves more than A1** (P1: +2.82 → +2.16 canonical). G3 compares the local g at R and does not project, so gas beyond R does not lower it. G3's own baryon convention (CX1's point mass, +5.01) still moves it more than any gas swap.
5. **This agrees with GH2 on X53's harness:** a cut at R_vir helps the law, and a cut at 1.5 R_vir or beyond hurts it.

## As hard as a fail
1. **The kSZ samples aren't isolated** (satellite fraction about 0.28). Host gas and two-halo signal are not subtracted. They are matched in mass only roughly: a CIGALE bin read on Chen's scale through GH9, while the lenses use their own catalogue scale. B3 (lens masses +0.19 dex) leaves the label unchanged.
2. **Inside about 250 kpc (the 1′ aperture) the shape is Zhang's β-model, assumed.** A more concentrated profile would put more gas inside 100 kpc and could move the inner amplitude. No measurement exists there for quiescent galaxies at log M★ 10.5-11 (CFG836). This is the main way the label could be wrong.
3. **The same gas goes on both colours.** The hot gas of blue lenses is not measured. If blue lenses held less gas, P6-like gas could close red without pushing blue over. A colour-split kSZ or X-ray profile would decide it; none is on record.
4. **The points are not native.** A scales as 300 km/s / σ_true, and r 0.64 carries 10 %. The brackets cover A from 0.41 to 0.85 and close nothing. B2 (A 0.85) narrows red by 1.8σ and pushes blue over.
5. **P2's NARROWED reading leaves blue at −2.7σ on B21c canonical.** Blue moved 0.8σ, under the frozen 1σ overshoot rule, so the frozen label is NARROWED. Read plainly, blue also crosses the line under P2.
6. **One A serves every lens mass.** Bins 1-2 (below log M★ 10.5) are an extrapolation. Under P1 the A1 rows of bins 1-3 drop and bin 4 rises (+0.094 → +0.111): at log M★ near 11, the large R_vir leaves even less gas inside 100 kpc.
7. **A30's two-halo template carries the inherited Planck-era spectrum.** Without the two-halo term the picture is the same: P1 +9.73 / +13.13 against +9.19 / +6.17.
8. **In H3, neighbour gas is a point mass.** The own-only rows move A_in by 0.04 or less (P1 S1 red 1.209 against 1.237 canonical).
9. **NV2's external field is available for no lens sample.** It is not applied.
10. **The label rests on B21c,** the only colour sample with small errors. SI2's clean lenses can't separate the readings.

## Departures, all disclosed
1. **The first `si2` run peaked at 1.46 GB.** A per-mass cache of profile tables for the neighbour totals caused it. Those values are no longer cached. The rerun peaked at 0.67 GB and gave identical numbers (max |d| 0). All modes were then rerun with the final script.
2. **Unrounded values.** A values are read unrounded from GH11's JSON; the criteria table rounds them to 4 digits. B3's offset is GH9's median 0.1884 (criteria: +0.19), and e = 0.13588.
3. **S2's output writer is disabled in the exec copy.** S2's `finish()` call would be reached only if S2's K0a failed, and it writes S2's own outputs. In this lane's copy it is replaced by a SystemExit, so S2's files can't be overwritten. K0a passed.
4. **P2's measurement cache** is read from a local scratch copy (sha256 above).

κ = ½ FITTED; not theory closed.
