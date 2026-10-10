# CFG585 FROZEN CRITERIA — do OLDER early types carry more excess at fixed mass? (cold-energy settling over time)

(owner chat 10-09/10, "yes run the age test"). Committed alone before any lensing number for these subsamples.

Hypothesis (owner's "clumps change over time"; framework-native but with NO settling mechanism on record): if cold
energy settles inward with time, older systems carry more central excess. Prediction: at fixed M* and type,
older (redder) early types show a LARGER inner deficit ε than younger (bluer) ones: D = ε_old − ε_young > 0.
Prior record: CFG115 (within-class colour contrast, older environment, p 0.20, non-discriminating); CFG531 (early +0.83,
late −0.31). This lane uses CFG529's validated f30 environment and CFG531's estimator.

Pre-flight (counts and colours only, no lensing): u−r from KiDS_DR4_brightsample_LePhare (MAG_ABS_u − MAG_ABS_r),
exact RA/Dec match for all 181,477 lenses (reproduces every typ label). f30 early types: 26,572. Age proxy = colour
residual at fixed mass (u−r minus the median in five log M* quintile bins). OLD = top residual tertile, YOUNG = bottom;
separation 0.254 mag; median log M* 10.80 / 10.80.
POWER FORECAST (declared now): σ_D ≈ 0.31 (CFG531 early σ(K-in) 0.127 × √3 per tertile, in quadrature). If ε scales with
colour like the early–late contrast (≈ 1.76 per mag), D ≈ +0.45 → Z ≈ 1.45, P(Z ≥ 2) ≈ 0.29; with CFG115's gradient
(0.34 dex/mag) D ≈ +0.22 → Z ≈ 0.7. → LOW POWER (P < 0.5): a null cannot exclude settling.

Statistic: ε in bands K-in (primary) and K9 from CFG531's machinery (executed unedited up to its own analysis: esd_loo,
comps, all_bands), for masks f30 & early & OLD and f30 & early & YOUNG; constructions A and B; both footings.
D = ε_old − ε_young with the larger of the leave-one-patch-out jackknife and quadrature errors (CFG531's rule).
Verdict: CONFIRMED iff D > 0 with Z ≥ 2 in K-in for both constructions on both footings; CONTRADICTED iff D < 0 with
Z ≤ −2 likewise; else NOT CONFIRMED [LOW POWER].
Controls: C1 the two tertiles' median log M* agree within 0.05 dex; C2 CFG531's full-early ε(K-in, A, canonical)
reproduced to 0.005 by the executed functions.
MUTATE (CFG585_MUTATE=1): swap the OLD/YOUNG labels at random within mass quintiles (keeping counts); D must be
consistent with 0 (|Z| < 2 in all four cells).
κ = ½ fitted; footings never pooled; colour also tracks M/L, dust and metallicity, so a positive D would be a lead,
not proof of settling; cold energy's mass required; not theory closed.
