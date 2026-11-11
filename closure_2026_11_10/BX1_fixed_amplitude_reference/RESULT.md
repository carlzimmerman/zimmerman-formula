# BX1 RESULT: KL1 Part C's gate with a fixed-amplitude, paired 200 Mpc/h S0 splice (one full-size pair)

**AS FROZEN (21e1c07e9a): NO VERDICT (canonical) / NO VERDICT (alt).** KA3 fails and MUTATE MB2 does not bite. Both were seen at
256^3 and recorded in AMENDMENT A1 before any 512^3 or gate number existed.

**UNDER AMENDMENT A1 (post hoc, 4af7a4b905): A1's graded label is PENDING.** That label is the mean of the 512^3 pairs A and B,
and 512^3 pair B had not finished. **INTERIM reading on 512^3 pair A** (A1's fallback rule, applied while pair B runs):
**AMPLITUDE CONSISTENT (canonical) / AMPLITUDE CONSISTENT (alt). DES Y3 sits 0.15 to 0.17 widths under the line, inside its own
splice noise.** KiDS-Legacy and DES Y3 both read CONSISTENT on both footings. KiDS-1000 (reported) reads GAP STAYS.

The withheld frozen gate on pair A gives the same numbers and the same per-survey readings. This label rests on **one full-size
pair**. 512^3 pair B (seed 7102 and twin) and the extra 256^3 runs (pairs C and D, random R6..R10) had not finished at landing.
They may follow in a later addendum.

**No survey crossed the two-width line relative to the 256^3 numbers.** Legacy went from 1.35-1.66 at 256^3 to 1.51 / 1.72 at
512^3 pair A. DES Y3 (polished scan) went from 1.72-1.86 to 1.85 / 1.83.

TEST lane: relabels nothing, adopts nothing, not registered. **kappa = 1/2 FITTED; not theory closed.** Footings canonical (a0
9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a gravitating field component,
never a particle.

## 1. The gate (KL1 Part C: C0 splice + C2 slow-loss response, covariance at the model)

g = (target sigma8 - survey best sigma8) / width. The targets are the neutrino-floor sigma8, 0.8121 (canonical) and 0.8120 (alt).
Legacy and KiDS-1000 use KL1's frozen scan. DES Y3 uses AMENDMENT C3's polished scan.

| row (splice below k 0.5) | KiDS-Legacy can / alt | DES Y3 polished can / alt | KiDS-1000 can / alt |
|---|---|---|---|
| **GATE_BX1 (512^3 pair A, graded)** | **+1.51 / +1.72** (p 0.26 / 0.25) | **+1.85 / +1.83** (p 0.30 / 0.31) | **+3.59 / +3.72** (p 0.068 / 0.065) |
| C3b_BX1 (Legacy's own mass-dependent NLA) | +1.40 / +1.66 | - | - |
| KA4: GATE_R2 (CFG411 splice, KL1's row) | +1.17 / +1.36 | +1.28 / +1.33 (REP_R2) | +3.37 / +3.53 |
| KL1 Part C gate (R1, the 100 Mpc/h box) | +1.71 / +1.88 | +2.18 / +2.23 | +3.72 / +3.85 |
| KL1 R2b (CFG424 seed 360, single random run) | +1.92 / +2.09 | 3.49 / 3.43 (frozen scan) | - |
| REP_A256 / REP_B256 (256^3 pairs) | +1.45 / +1.66, +1.35 / +1.53 | +1.75 / +1.86, +1.72 / +1.58 | +3.56 / +3.69, +3.49 / +3.62 |
| REP_Asingle (512^3 run A alone, no twin) | +1.29 / +1.48 | +1.39 / +1.40 | +3.46 / +3.59 |
| MB1_x09 (pair A x 0.9 below k 0.5) | +0.74 / +0.93 | +0.55 / +0.53 | +3.11 / +3.25 |

- DES Y3 on KL1's frozen scan (reported): pair A +1.86 / +1.75. The 256^3 pairs read +1.84 / +1.80 (A) and +2.21 / +1.58 (B).
- ln det gaps (frozen scans, reported, not graded): Legacy +1.89 / +2.06, DES +2.27 / +2.18, KiDS-1000 +3.99 / +4.12. **With the
  ln det term, DES is above 2 on both footings and alt Legacy is just above 2.** The gate as KL1 froze it does not use this term.
- Every p at the target is >= 0.05 for Legacy and DES. No POOR FIT.

## 2. Residual realisation noise, in widths

**Measured (the frozen sigma_g):** sigma_g = |g_A256 - g_B256| / sqrt(2), from the two 256^3 pairs used as splices:

| | Legacy | DES Y3 (polished) | KiDS-1000 |
|---|---|---|---|
| canonical | 0.07 | 0.02 | 0.05 |
| alt | 0.09 | 0.20 | 0.05 |

- [INSIDE SPLICE NOISE] (|g - 2| < 2 sigma_g) applies to DES Y3 alt (0.17 < 0.40). The tag does not change a label.
- **The canonical DES value 0.02 is a single draw of a difference and is almost certainly too small.** The same two pairs on
  KL1's frozen scan differ by 0.37 canonical (sigma 0.26) and 0.22 alt (sigma 0.16).
- A linear-response cross-check (reported): the 256^3 pairs' band powers (k <= 0.5) differ by 1.2 / 1.9 / 3.1 % at z 1 / 0.5 /
  0. MB1 gives 0.77 widths (Legacy) and 1.30 widths (DES) per 10 % of power. So a single pair carries about 0.1 to 0.17 widths of
  noise on Legacy and 0.2 to 0.3 on DES.
- **My reading:** a single pair's residual noise is about 0.1 width on Legacy and about 0.2 width on DES, on both footings.
  - Legacy is under the line by 0.49 / 0.28 widths: about 3 to 5 sigma.
  - DES is under the line by 0.15 / 0.17 widths: **under 1 sigma**.
  - **So DES Y3's CONSISTENT is not resolved from 2 by one pair.**
- The single fixed run without its twin (REP_Asingle) reads DES 0.43 to 0.46 widths lower than the pair. That is the size of the odd,
  second-order mode coupling that pairing cancels at 200 Mpc/h.
- Fixed pairs against random runs (256^3, A1's KA3 (a')): the pairs' band average is above the mean of the five random runs by
  +1.7 % / +3.2 % / +5.7 % (t +0.79 / +1.23 / +1.88; not significant). If that offset were real, the pair would overstate power,
  and the true gaps would be **lower**, further inside CONSISTENT. It cannot push a reading over 2.

## 3. Known answers and MUTATE

| check | result |
|---|---|
| KA1: option-off copy vs CFG530 S0_L100_N256 (1e-5) | PASS, 3.9e-8 (bit for bit against CFG596's VLs) |
| KA2 (a): fixed IC power / input | PASS, 2.1e-15 |
| KA2 (b): z_i r / r_bin, 256^3 | PASS, max 0.0031, rms 0.0020 against 0.102 for random runs |
| KA2 on production pA / pAi | PASS, max 0.0055 / 0.0074, rms 0.0029 / 0.0032 |
| **KA3 (a) frozen chi^2** | **FAIL**, chi^2 44.8 / 70.9 / 177.9 on 15 bins (z 1 / 0.5 / 0) |
| KA3 (b) frozen quiet | x9 / x6 / x4 against the line of x5: fails at z 0 |
| KA3 (a') A1, band Welch t | PASS, t +0.79 / +1.23 / +1.88 |
| KA4: KL1's GATE_R2 rows | PASS, exact (d = 0) on Legacy, DES and KiDS-1000, both footings |
| KA5: splice writer | PASS, bit for bit |
| polished-scan replay of KL1 C3 (R1) | 2.1779 / 2.2305, identical |
| MB1 (x 0.9 must drop the gap >= 0.3) | bites: Legacy 0.77 / 0.78, DES 1.30 / 1.30 |
| **MB2 frozen (single / pair >= 1.5 at z 0)** | **does not bite**: 1.8 / 1.5 / 1.2 |
| MB2' A1 (>= 1.1 at every z, post hoc) | bites: 1.78 / 1.50 / 1.23 |

## 4. The pair against the record (reported; L100 box bins below k 0.5)

The table gives pair A (512^3) divided by each record. err = |A - B| / (sqrt 2 mean) from the 256^3 pairs.

| z 0, k | 0.080 | 0.140 | 0.197 | 0.255 | 0.320 | 0.385 | 0.444 |
|---|---|---|---|---|---|---|---|
| / CFG411 (R2) | 1.057 | 1.012 | 1.117 | 0.997 | 0.986 | 1.101 | 1.025 |
| / CFG424 (R2b) | 1.007 | 0.969 | 0.926 | 0.896 | 0.930 | 0.966 | 0.949 |
| / L100 box raw | 1.239 | 0.953 | 0.749 | 0.852 | 0.862 | 0.919 | 0.958 |
| / L100 R1-corrected | 0.987 | 0.983 | 1.107 | 0.860 | 0.908 | 0.892 | 0.988 |
| err | 0.013 | 0.020 | 0.025 | 0.003 | 0.033 | 0.043 | 0.014 |

At z 1 and z 0.5 the pattern is the same (`bx1_compare.out`). The pair sits between the two single random runs: -1 to +12 %
against CFG411 and 3 to 10 % below CFG424 at k 0.2 to 0.45. It is below the R1-corrected box at k 0.25 to 0.4 and below the raw box at
k 0.2 to 0.4. So the R1 splice carried more power than the pair at those scales, and that is why the gate falls from KL1's
1.71 / 2.18 to 1.51 / 1.85.

CFG411's slower growth after z_i (disclosed in the frozen criteria at k 0.5 to 1) does not show as a uniform offset below k 0.5.
Against the pair, CFG411 is low mainly in the bins at k 0.2 and 0.38 (by 10 to 12 %).

**Resolution (reported).** P_512 / P_256 for pair A (shared modes, L 200) is 1.000 at k 0.04 and rises to 1.021-1.025 at
k 0.47, at every z. Gap shift from A256 to pair A: Legacy +0.06, DES +0.10 / -0.03.

## 5. Limits

- **One full-size pair.** 512^3 pair B, the A + B mean that A1 grades, and the extra runs were not finished at landing.
- **The frozen premise failed.** At 200 Mpc/h a fixed pair is 4 to 9 times quieter than one random run, not noise-free. Its
  residual (about 0.1 width Legacy, 0.2 width DES) is the same size as DES's margin under 2.
- The 200 Mpc/h run is used only below k 0.5. The 100 Mpc/h box's own draw above k 0.5 remains (R1's correction is not applied
  there, as in R2).
- 512^3 at 200 Mpc/h is coarser than the 100 Mpc/h box. P_512 / P_256 shows 2 % at k 0.47, so 512 to infinity is plausibly 1 to
  2 % more at the splice edge (not measured).
- **DES Y3 is not DES's newest release.** The year-6 analysis exists and is not on disk (no download).
- One gravity-only dynamics (S0) for the splice. The response alpha(k) stays the S0 L100 run's.
- Inherited: the EH IC spectrum, the flat w = -1 background and the massless-neutrino S0 run. The neutrino floor enters only
  through the target sigma8, as in KL1.
- The ln det gaps put DES above 2. The gate as frozen by KL1 does not use them.
- KiDS-1000 stays at 3.6 to 3.7 widths whatever the splice. Its gap is not a long-mode question.
- sigma_g from two pairs is a one-draw estimate (section 2).

## 6. Hand estimate (frozen section 12, A1 section 6) against the outcome

| item | estimate | outcome |
|---|---|---|
| KA3 | passes with large margins | **FAILED** (the main miss: second-order mode coupling at 200 Mpc/h) |
| pair vs CFG424 / CFG411 at k 0.25-0.5 | near CFG424, ~10 % above CFG411 | 3-10 % below CFG424, -1 to +12 % against CFG411 |
| Legacy | 1.6-2.0 / 1.8-2.2 | 1.51 / 1.72 (below) |
| DES polished | 2.2-3.0 | 1.85 / 1.83 (below) |
| KiDS-1000 | 3.6-3.9 | 3.59 / 3.72 (on) |
| overall | GAP STAYS by DES 65 %, AMPLITUDE CONSISTENT 30 % | AMPLITUDE CONSISTENT (interim, the 30 % branch); frozen NO VERDICT |
| sigma_g | Legacy < 0.1 (A1: 0.1-0.3); DES 0.1-0.3 (A1: 0.2-0.6) | Legacy 0.07 / 0.09; DES 0.02 / 0.20 (about 0.2 by cross-check) |
| MB1 | Legacy 0.5-0.8, DES 1-2 | 0.77 / 0.78, 1.30 / 1.30 |

## 7. What this means for the lensing row

- With KL1's own long-mode reference replaced by a fixed pair, form B's amplitude reads CONSISTENT with KiDS-Legacy (1.5 / 1.7
  widths) and with DES Y3 (1.85 / 1.83). The DES reading is inside one pair's residual noise of the line.
- KL1's "GAP STAYS (DES 2.2)" reading moves under 2 on this pair. It is not cleared beyond the noise.
- KiDS-1000 stays GAP STAYS (3.6 / 3.7).
- The frozen label is NO VERDICT.
- Nothing is relabelled. PAPER72 should cite the frozen NO VERDICT first, then the interim pair-A reading with its noise. The
  A + B mean is due in a later addendum.

## 8. Commits

| what | local | origin |
|---|---|---|
| FROZEN_CRITERIA.md (alone) | 21e1c07e9a | (filled after push) |
| AMENDMENT_A1.md (alone, post hoc) | 4af7a4b905 | (filled after push) |
| landing: scripts, outputs, this RESULT | (filled after commit) | (filled after push) |

## 9. Files

- `bx1_pm.py`: a copy of CFG596's engine (sha256 of the source 1c207fa5fd1d...) with FIXAMP / INVERT / NOSAVE / ICCHECK.
- `bx1_run.py`: the serial launcher with its watchdog.
- `bx1_ka.py`: known answers and MUTATE, written to `bx1_ka.json` / `.out`.
- `bx1_splice.py`: the splices in KL1's layout (`bx1_splice_*.json`), plus `bx1_compare.json` / `.out`.
- `bx1_regrade.py`: KL1's scripts executed unchanged, with BX1 splices added (`parts/bx1_<footing>_<group>.json` / `.out`).
- `bx1_grade.py`: labels, written to `bx1.json` / `.out`.
- Run products (engine JSONs, logs) are in `../_external_data/bx1_work/` (outside git).
- `parts/run_*.log` are not committed (they carry machine paths in warnings).

kappa = 1/2 FITTED; not theory closed.
