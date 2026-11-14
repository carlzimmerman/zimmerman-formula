# EUC17R: COMPARISON WITH THE LEAD (EUC17)

2026-11-14. Written after this re-grade's own result was committed (`RESULT_BLIND.md`, 2c8361f51b). Only then were
the lead's `RESULT.md` and `AMENDMENT_A2.md` opened, plus, to explain the differences below, the lines of `euc17.py`
that order the EUC10 lenses and call `stats`, the K0 line of `euc17.out`, and the numbers in `euc17_A2_results.json`.
κ = ½ FITTED. Adopts nothing.

## 1. Labels: the same in every row and footing

| Row | Lead (under its A2) | This re-grade (as frozen) |
|---|---|---|
| R1 | CEILING HOLDS / CEILING HOLDS, CHANGED, ROBUST | CEILING HOLDS / CEILING HOLDS, CHANGED, ROBUST |
| R2 | WIDE LENSES BREAK THE CEILING / same, UNCHANGED, ROBUST | WIDE LENSES BREAK THE CEILING / same, UNCHANGED, ROBUST |
| R3 | NO VERDICT / NO VERDICT, UNCHANGED, ROBUST | NO VERDICT / NO VERDICT, UNCHANGED, ROBUST |

Both files say the same about what the labels mean. R1's CHANGED is a hit, not a pass. It holds only with every source
at infinity; at z_s ≈ 2 the would-be word is still CEILING BROKEN. S1's median correction of 0.071 dex sits above
EUC12's 0.05 dex agreement, which is a reason to doubt the extrapolated wings. Both files rest the premise on one lens.

## 2. Where they differ

**(a) The as-frozen word.** The lead's run as frozen is **NOT EVALUABLE**: K0 failed on the upper bound of f₂₅ for
the EUC10 reading (0.818 against the committed 0.909, both footings). This re-grade's K0 **passes as frozen** (24 of 24
items). On that reading it reproduces 0.909 with a bound difference of 4.8e-5.

The cause is lens order, not tolerance and not stream position. EUC10 and EUC16 call `stats` with a fresh generator
on lenses in key-catalogue row order, and with 11 lenses the bootstrap bounds of a fraction depend on that order. The
lead rebuilt the reading in the order of `euc10_per_lens.csv`, which is sorted by identifier. This re-grade put the
lenses in key-catalogue order (READING.md §3, fixed before any number). The frozen text names neither order. A2's
diagnosis is right that a 0.01 tolerance cannot survive a change of order on 11 lenses. With the source lane's own
order, though, the frozen check holds unchanged, and A2's wider tolerance of max(0.01, 1/N) is not needed.

Disclosure: READING.md §3 was written after the memory-index line that said the lead's run "voided itself as frozen"
because "bootstrap bounds of a fraction step by 1/N". The order choice serves the purpose of a harness, which is to
repeat the source computation, but the leak came first. The re-grade does not claim the choice was naive.

My judgment: K0 asks for the committed statistics to be reproduced, and the source lane's own order is part of that
computation. So the frozen criteria are evaluable as written, and the as-frozen labels are the ones in §1. The lead's
post hoc A2 reaches the same labels. The difference changes no word. If the lead wants the record to say that a
blind reading found the lane evaluable as frozen, that is a dated note for the lead to add; this session edits no
lead file.

**(b) Bracket F5 and the 5 % no-mask rule.** The lead's as-frozen script counted F5's deliberate drop of n > 9.5
lenses (8.6 % of P) as "no mask", so every row printed FRAGILE (F5). A2 §2 calls this a script error and counts only
lenses without a mask record. This re-grade did that from the start (READING.md §1 and §5: the share counts lenses
without a usable mask among the lenses F5 keeps), and every row is ROBUST. That is independent support for A2 §2
being a script correction rather than a change of criteria.

**(c) Bounds of EUC1's conditional readings (reported, would-be words only).** Point values are identical (0.1488,
0.2719). The bounds differ by at most 0.001: z_s = 3 is [0.1363, 0.1613] for the lead and [0.1366, 0.1607] here;
z_s ≈ 2 is [0.2566, 0.2873] for the lead and [0.2566, 0.2882] here. The lead gives these readings a fresh generator.
This re-grade continues EUC1's shared stream (READING.md §3). The would-be words are the same (NO VERDICT and CEILING
BROKEN).

**(d) K4 convention.** Both get +1.10 % for (a) and 1.266 × for (b), and both note that a major-axis radius would give
1.03 × and fail (b). The lead rejects the major-axis reading on the geometric share and the released library's
convention. This re-grade rejects it with a rule written before the run: the convention whose model best matches the
released map inside the mask (0.976 against 0.808). The lead also checked that the map is zero outside the mask and
compared seven more bands; this re-grade did neither.

## 3. Where they agree to every printed digit

R1, R2 and R3 point values and bounds (for example R1 f₂₅ 0.0602 [0.0520, 0.0683] / 0.0498 [0.0426, 0.0576]; R2
0.4435 [0.3548, 0.5244] / 0.3790 [0.2984, 0.4599]; R3 b_med +0.1920 [+0.0786, +0.3376] / +0.1735 [+0.0612, +0.3218]).
Also law B, the EUC10 reading (+0.3368 [+0.0790, +0.5759] / +0.3201 [+0.0625, +0.5601]), every bracket in the lead's
§2 table, S1 by θ_E class, and K0b (5.0e-5), K1 (2.9e-7; 5.6e-17), K2 (1.8e-14), K3 (no mask smaller than θ_E) and
K5 (0.822, 0.637). Both find EUC4's secondary and complement bins not evaluable: 4 of 292 and 23 of 2,045 lenses have
a mask. Both find no lens of R1, R2 or R3 without a mask.

## 4. Not covered by this re-grade

The lead's post hoc reading T (A2 §3, wings beyond the mask removed) was not recomputed. The lead's extra K4 checks
are listed in (d).
