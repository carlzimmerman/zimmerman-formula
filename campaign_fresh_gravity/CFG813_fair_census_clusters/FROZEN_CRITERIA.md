# CFG813 FROZEN CRITERIA: fair test of the expelled-gas rule (H-EX) in clusters, using richness-based stellar masses (committed before any script)

**Why.** CFG812 found that in eRASS1 and ACCEPT, the catchment retention f_ret was pinned at 0.60 by the condensed-fraction
floor. The harness fixed condensed = 0.20 M_gas, so the census never acted (CFG727/808/809). This lane removes the fixed
0.20 for the clusters that have an independent stellar-mass handle.

**Sample.** The 76 eRASS1 clusters (CFG687) matched to redMaPPer λ ≥ 20 (CFG688/CFG726 match, `cfg726_work/lambda.json`).

**Condensed mass (declared, observation-based, provisional).**
- M_cond = λ × 10^10.7 M☉. Here λ counts red members above 0.2 L*, at a mean stellar mass of ≈ 10^10.7 M☉ per member
  (an order-of-magnitude literature value, quoted from memory). The BCG is included in the count.
- **Brackets:** ×0.5 and ×2.
- No ΛCDM halo-mass calibration is used.
- Per cluster, fs = M_cond / M_gas,tot replaces the fixed 0.20. The stellar placement is unchanged (BCG = half, members
  r^−2.5).

**Rule.** CFG809's H-EX split, unchanged (census catchment fixed point; retained baryons tether their own share; the expelled
share is free; Method A placement). With fs ≈ 0.05–0.1 the condensed floor no longer binds, so f_ret(M_ta) acts.

**Comparison on the SAME 76 clusters, read from the stored work files:**
- (i) the plain law (CFG687 PL);
- (ii) CFG809 H-EX with fs = 0.20 (`cfg809_work/erass.npy`).

## Pass rule (primary: ν_s, canonical; alt reported)
- MID and OUTER band A within 2σ (jackknife, 15 RA patches), AND both gas-mass halves |Z_MID| < 3.
- Classes:
  - **FAIR PASS** if the primary passes AND it beats (ii) in Σ Z² over MID, OUTER and the two halves;
  - **IMPROVES** if it beats (ii) but does not pass;
  - **NO GAIN** otherwise.
- **Brackets:** ×0.5 and ×2 are reported. The verdict is stated as robust only if both brackets keep the same class.

**Scope (stated).** ACCEPT has no λ, so it is not fair-tested here. eFEDS already uses measured catalogue condensed masses
(CFG809: PASS, p 0.044/0.087).

## Controls
- K1: the fs = 0.20 rerun of 5 clusters reproduces their CFG809 stored rows within 1e-6.
- K2: the median f_ret over the sample is < 0.60, i.e. the floor no longer binds; the median is reported.

κ = ½ fitted; cold energy mass required; not theory closed.
