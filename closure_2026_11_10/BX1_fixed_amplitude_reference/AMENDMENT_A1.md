# BX1 AMENDMENT A1 (POST HOC): KA3 and MB2 fail as frozen; an amended reading beside the frozen one

Committed alone, after the 256^3 known-answer runs were graded and before any 512^3 production number or any BX1 gate number
exists. **Post hoc**: the numbers below were seen. TEST lane; relabels nothing, adopts nothing. **kappa = 1/2 FITTED; not theory
closed.** Footings graded separately, never pooled. The frozen criteria (21e1c07e9a) are not edited.

## 1. What was seen (bx1_ka.py on the 256^3 runs)

- KA1 PASS: the option-off copy matches CFG530 S0_L100_N256 to 3.9e-8 (sigma8 3.7e-9) and CFG596's own VLs run bit for bit.
- KA2 PASS: the fixed run's IC power equals the input to 2.1e-15; at z_i, r / r_bin is within 0.003 of 1 below k 0.5 (rms 0.002
  against 0.10 for the random runs).
- KA4 PASS and KA5 PASS: KL1's stored GATE_R2 rows reproduced exactly (difference 0) on Legacy, DES, KiDS-1000, both footings;
  the splice writer is bit-exact.
- **KA3 FAILS.** (a) pair A against the random mean: chi^2 44.8 / 70.9 / 177.9 on 15 bins at z 1 / 0.5 / 0 (pair B: p 0.56 /
  0.26 / 0.000). (b) pair-to-pair rms at k <= 0.3: 2.2 % / 3.2 % / 4.6 %, against 19.5 % / 19.9 % / 20.4 % for two random runs,
  so x9 / x6 / x4 (the line was x5: fails at z 0).
- **MB2 does not bite:** single fixed runs A / B differ by 4.4 % / 5.2 % / 5.8 % rms (k <= 0.5), the true pairs by 2.5 % /
  3.5 % / 4.7 %: ratios 1.8 / 1.5 / 1.2 (the line was 1.5 at z 0).
- Per run (P / (D^2 P_lin) by bin): single fixed runs start exact and move by 5 to 15 % per bin at k 0.1 to 0.5 by z 1, each
  inverted twin the opposite way; the pair means move by 2 to 5 %. sigma8 at z 0: fixed 0.880 / 0.911 / 0.895 / 0.875, random
  0.837 / 0.881 / 0.836 / 0.876 / 0.892 (the fixed runs' sigma8 growth from z_i is 2.4 % higher, about 2.3 sigma with 5 runs).

## 2. The frozen reading stands first

By the frozen rule (a failed KA, a MUTATE arm that does not bite), **BX1's frozen label is NO VERDICT on both footings, whatever
the gate reads.** It leads RESULT.md.

## 3. What the failure says

The frozen premise was that a fixed pair has almost none of the low-k noise. At 200 Mpc/h that is false. Mode coupling moves
single fixed runs by 5 to 15 % per bin by z 1. Most of that coupling is odd in the initial field, and pairing cancels it, but 2 to
5 % per bin is left (even terms). The pair is 4 to 9 times quieter than one random run, not noise-free. KA3 (a) treated the pair as
noise-free and the bins as independent, and both are wrong. The z 0 bins are strongly correlated: one draw moves every bin
together, as the sigma8 spread shows.

## 4. The amended reading (A1), reported beside the frozen one

- **KA3 (a') unbiased, robust to bin correlation.** At each z in {1, 0.5, 0}: per run, the equal-weight mean over the bins with
  k <= 0.5 of P / (D^2 P_lin(k_bin)); pair values are the means of their two twins. Welch t of the mean of pairs {A, B} against
  the mean of R1..R5 (sample variances, ddof 1): PASS if |t| <= 3 at every z. The band k <= 0.3 is reported.
- **KA3 (b)** is reported (x9 / x6 / x4) and no longer gates. In its place, **the label carries its measured noise:**
  - The graded splice becomes **the mean of the 512^3 pairs A and B** (splice `BX1_AB`). Pair B is now required, not optional.
  - sigma_g of that mean = max(|g_A - g_B| / 2 at 512^3, |g_A256 - g_B256| / 2 at 256^3), per survey and footing.
  - If the 512^3 pair B cannot complete: the graded splice is pair A, with sigma_g = |g_A256 - g_B256| / sqrt(2).
  - The [INSIDE SPLICE NOISE] tag rule is unchanged, with this sigma_g.
- **MB2' (post hoc line).** A twin replaced by a copy gives a pair equal to the single run, so its ratio is exactly 1. MB2'
  bites if the single / pair rms ratio is >= 1.1 at every z. The frozen 1.5 was my estimate of the pairing gain. The observed
  gain is 1.8 / 1.5 / 1.2. The gate with pair A's run alone (`REP_Asingle`) against pair A is reported beside it.
- **MB1** (x 0.9 on pair A's splice, >= 0.3 widths) is unchanged.
- **KA2 on every 512^3 run** is unchanged, and so are KA4 and KA5.
- **Overall labels** use the frozen gate and C3b rule on the graded splice above.

## 5. More runs, if time allows after the production pairs (reported only)

At 256^3, L 200, NSEED 512: random R6..R10 (seeds 7206..7210) and fixed pairs C (7103) and D (7104). KA3 (a') is re-read on the
extended set and reported beside the graded one. The scatter of the four 256^3 pairs' gaps, used as splices, is a second estimate
of sigma_g.

## 6. Hand estimate for the amended reading (before any production number)

- KA3 (a') passes (|t| about 1 to 2.5 at z 0).
- sigma_g of the A + B mean: Legacy 0.1 to 0.3 widths, DES 0.2 to 0.6.
- The gate as in FROZEN_CRITERIA section 12: GAP STAYS driven by DES Y3 is most likely, and a DES reading inside its own splice
  noise is likely.
