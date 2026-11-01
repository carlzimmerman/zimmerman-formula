# Argon reply, 2026-11-01: revised stop seal and D2's inner-mass prediction (recorded on receipt)

Committed before any VB1 measurement. VB1's runs finished 2026-11-01 00:29 and no f_out or f_in existed in the lane when this was written. ZN4's runs had finished and its readouts existed, unread by this record; Argon's message cites no ZN4 number.

κ = ½ FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.

## 1. D2 predictions, as Argon sent them

All are for a sphere at **2.25 q_M** against 1.50 q_M, one 1e14 seed, z = 0.

| quantity | Argon |
|---|---|
| ΔM(< 0.7 R500) | +1.8 % ± 1.2 %, range +0.5 % to +3.2 % |
| ΔM(< R200) | +5.5 % ± 2.0 % |
| ΔΣ(2.18–3.17 R500) | +21 % ± 5 %, range +16 % to +26 % |
| G-OUT-M3 on the measured gas scale | about +3.8 to about +2.4 |
| class | inner gate passes; outer gate below 28 %, so partial relief |

**Mismatch with VB1.** VB1 runs RS **2.0**, the IC grid's ceiling (`VB1_vacuum_boundary/FROZEN_CRITERIA.md`, disclosed there). Argon's numbers are stated at 2.25, and its message does not mention 2.0. They are recorded as given and must not be scored as hits at 2.0 without saying so. By Argon's own shell argument, RS 2.0 should give a smaller outer gain than 2.25, so a low f_out at 2.0 does not refute the 2.25 figure, and the 2.0 run cannot confirm it directly. The criteria file's earlier Argon line, f_out 1.18–1.24, was likewise given for 2.25. This session's line there stays as frozen.

**Scale of the error bars.** The new outer range, 1.16–1.26, is wider than the earlier 1.18–1.24.

## 2. Revised stop seal, as Argon sent it

**Cluster half, on ZN4 + RF3's grader.** ZN4 at ng 80 fails X-COP (rms > 0.100 or |mean Δ| > 0.050), or G-IN-Mall Z < −2.0, or G-OUT-M3 Z > +2.0 on one gas scale, and stays above +2.0 after D2's boundary test.

**Galaxy half, on X80 + ND1 + 1e12 ng 80.** Either:
1. ND1 fails LITTLE THINGS (+0.138, 200 of 200 draws) and the three SPARC dwarf bins miss ET1's 69 / 103 / 143 once η_conv(1e12, ng 80) ≥ 25.0; or
2. the ng 80-anchored η(M) drops N1's SPARC median Υ below 0.50, or leaves at least 2 of 3 ET1 bins outside at 95 % CI.

## 3. Points raised on receipt

1. **The galaxy half is not a forward test.** Argon itself says it has already fired unless η(1e12) falls more than 20 % at ng 80. Branch 1 restates ND1's known result, so the seal's only open content is the cluster half and that η line. It should be read that way.
2. **"And" became "or".** The earlier seal required the cluster and galaxy halves together. If both halves are still required, only the cluster half decides. Which halves must fire is not stated explicitly and needs Argon's answer.
3. **"Outside [69, 103, 143] at 95 % CI"** is not a defined interval. These are three central values, and no tolerance is given.
4. **The D2 clause is open.** The cluster half depends on a boundary test at 2.25 that VB1 cannot run on this grid.
5. **Group estimate: the inputs conflict.** The message gives M200 = 1e13 with M_b ≈ 6e11, a ratio of 16.7, and also M200/M_b ≈ 2.38. With the first pair, fair share (6.27 M_b = 3.8e12) would **lower** M200, the opposite of the claimed × 2.63. The Z −2.8 to −3.4 is therefore not a result. It also scales σ as if the halo alone set it. The number asked for in section 4 item 2 of `ARGON_REPLY_2026-10-31_EVENING_SCORED.md` remains to be read from the grader.
6. **D4's scoring is partial.** X80's README also scores Argon's converged ratios, 1.251–1.254 and 1.126 against measured 1.128 and 0.938: HIT at 1e10 (−10 %), MISS at 1e11 (−17 %). The message reports only the 0.96 and 0.92 lines.

## 4. Confirmed against the record

BA2's X71 +3.20 / +2.98 and X73 PRIMARY +1.04; X80's ρ₁₀ 1.128 and ρ₁₁ 0.938; ND1's +0.138 in all 200 draws; RF4's two-halo UNSEPARABLE; AE1's FAIL and its criteria commit b0334ac907. The other items in the message were not rechecked here.
