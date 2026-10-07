# Session 4 calcs, FROZEN before any script exists

κ = ½ fitted; both footings. No DM particle; the cold mass is still required. On-disk data only. The point of this session: **try to break Session 3's good news.**

## C. The same supply rule on the MW classical dwarfs (can kill Session 3's reconciliation)
Session 3 found that law + q · 0.13 · (Ω_c/Ω_b) · R_ind · M_now gets the ultra-faints' level right (q = 1). The classicals pass the law alone (AUDIT_UFD: +0.10 dex, stars only). A rule that is real must not wreck them.
- Sample: LVD MW systems with M_V ≤ −7.7, resolved σ, and a CFG317 `cls` R_ind (LMC and SMC have none and are excluded and named; Sagittarius is reported but flagged as tidally disrupting). Stars only (Υ_V = 2) plus LVD HI ×1.33; AUDIT_UFD's isolated estimator; r_½ = (4/3) R_e.
- Prediction: σ² = G [M_law + q · 0.13 · (Ω_c/Ω_b) · R_ind · M_now] / (3 r_½), with q = 1 (Session 3's case) and q = 0.5.
- Error scale: bootstrap over objects (2000, seed 21) ⊕ AUDIT_UFD's Υ floor (0.077 dex) in quadrature.
- **BROKEN** if the q = 1 median offset < −3 σ_err at the nominal yield, on both footings (the rule overshoots the classicals). **CONSISTENT** if |median| < 2 σ_err. **STRAINED** otherwise.
- Reported: the q (all objects sharing one q) that would zero the classicals' median, set against the q that zeroes the UFDs' median (from the same formula). A single rule needs the two q values to agree within a factor 2.
- MUTATE (`--mutate`): f_gal = 0 (the rule switched off). The median must move up to the law-only value (+0.10 ± 0.02); the script exits 1 when it does.

## S. Does the supply limit show in SPARC? (can only fail the working model, never confirm it)
A supply limit can only push galaxies BELOW the law, so it predicts a negative skew of the residuals at low g_bar. The external-field effect predicts the same sign, so a negative skew is not specific; a positive or zero skew is evidence against any binding supply limit.
- Data: CFG4_common.load_sparc(), Q ≤ 2; ν_mono at both footings; Υ_disk = 0.50 fixed (Υ_bul 0.70; declared); residual r = log g_obs − log(ν g_bar).
- Per galaxy, the weighted mean residual in each g_bar bin (edges log g_bar = −12.5, −11.5, −11.0, −10.5, −10.0, −9.0), so each galaxy counts once per bin.
- Statistic: the sample skewness of those per-galaxy means in each bin, with bootstrap over galaxies (2000, seed 23).
- **NO SUPPLY SIGNAL** if the lowest bin's skewness is ≥ 0 or within 2σ of 0. **CONSISTENT WITH A BINDING LIMIT** if it is < 0 at > 3σ **and** more negative than the highest bin's. Otherwise INCONCLUSIVE.
- MUTATE: flip every residual's sign. The lowest-bin skew must change sign; the script exits 1 when it does.

### Results so far: C CONSISTENT on medians at the nominal yield (−0.16 ± 0.09; BROKEN at yield +0.1), but the single-rule check FAILS: q zeroing UFDs 0.76 vs classicals 0.18 (ratio 4.1; alt 5.0; required ≤ 2). S: NO SUPPLY SIGNAL (lowest bin skew −0.47 ± 0.43; every bin is negatively skewed). MUTATEs detected.

---
## ADDENDUM U (frozen before any U number exists): one universal cold-fluid density, fit on UFDs, predicting the classicals
The retained cold mass M_c = 0.13 (Ω_c/Ω_b) R_ind M_now sits in a uniform sphere of ONE density ρ_c shared by all dwarfs: r_c = (3 M_c / 4π ρ_c)^{1/3}, q = min(1, (r_½/r_c)³).
- Fit: the single ρ_c that zeroes the UFD median (resolved UFDs with R_ind, nominal yield, canonical; alt reported).
- Prediction: classical median offset with that ρ_c, no refit.
- **PASS** if |classical median| < 2 σ_err (C's error scale). **FAIL** otherwise. Also reported: the ρ_c the classicals alone would need, and the ratio of the two.
- MUTATE: ρ_c × 100 (all q → 1). The classical median must equal C's q = 1 value within 0.005; exit 1 when it does.
