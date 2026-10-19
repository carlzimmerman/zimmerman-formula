# CFG852 — does the dwarf excess track gas loss (metallicity deficit at fixed stellar mass)?

Criteria: `FROZEN_CRITERIA.md` (9f77f4463, before the script). Run: `python3 cfg852.py` (MUTATE `CFG852_MUTATE=1`). Seconds.

## Result — CLASS: **NO SIGNAL** (the test had power; the effect is absent)
- Primary (22 CFG828 dwarfs with metallicities, SFH-based M/L): MZR slope 0.51; partial Spearman of the excess Δ with the
  metallicity residual δZ at fixed g_bar = −0.108 (p 0.32). Right sign, no significance.
- Secondary (67 LVD pressure-supported dwarfs, Υ = 2): MZR slope 0.34 (K1: the literature range); partial ρ = −0.024 (p 0.43).
- Power: an injected Δ = −0.5 δZ is recovered at ρ −0.71 (p 1e-4) and −0.68 (p < 1e-4); shuffled δZ gives nothing. So a gas-loss
  dependence of that size would have been seen.
- **Reading:** dwarfs that lost more gas through outflows (more metal-poor than their mass implies) do not carry more excess.
  Free cold energy tied to each dwarf's actual gas loss is not supported by this independent, chemistry-based proxy. Together
  with CFG822/823/838/839/842/844/845/848, every framework mechanism examined for the satellite-dwarf excess now fails a hard test.
- Declared confound: δZ partly tracks star-formation duration; this does not rescue the hypothesis (a gas-loss signal would
  still have to appear at the injected size).

κ = ½ fitted; cold energy mass required; not theory closed.
