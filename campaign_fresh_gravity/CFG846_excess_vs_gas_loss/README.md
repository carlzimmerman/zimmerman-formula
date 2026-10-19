# CFG846 — does the excess over the law track gas-poorness at matched g_bar? (H-EX's own prediction)

Criteria: `FROZEN_CRITERIA.md` (a575dcd09, before the script). Run: `python3 cfg846.py` (MUTATE `CFG846_MUTATE=1`). Seconds.
Note: CFG583 (10-09) already found SPARC underpowered for a 0.1–0.2 dex gas-fraction effect; this test was frozen before that
row was re-read (disclosed) and differs in using matched g_bar on the low-acceleration half.

## Result — CLASS (Test 1, within SPARC): **NO PATTERN** (stable at Υ_disk 0.4 / 0.5 / 0.6)
- 138 SPARC galaxies, points with g_bar < 10^−10.5: partial Spearman of the residual with gas-poorness s = M★/(M★ + 1.33 M_HI)
  at fixed g_bar = −0.000 (p 0.50); gas-poor minus gas-rich tercile −0.024 dex. Same at Υ 0.4 (+0.010) and 0.6 (−0.012).
  K1 PASS (median +0.031). MUTATE (shuffle) NO PATTERN.
- Within SPARC's reach (g_bar ≳ 10⁻¹²) gas content does not change the residual — consistent with CFG583.

## Test 2 (reported, the positive pattern): at g_bar < 10⁻¹² m/s², matched in g_bar
| sample | gas content | excess over the law |
|---|---|---|
| satellite dSphs / UFDs (CFG828, N 20) | gas-free | **+0.44 dex** |
| red isolated lenses (CFG829) | gas-poor | **+0.20 dex** (A 1.59 ± 0.08) |
| blue isolated lenses (CFG829) | gas-rich | +0.01 dex (A 1.02 ± 0.09) |
| SPARC discs | gas-rich | do not reach this regime (lowest bin +0.07 at ~1e-12) |
The red–blue split at identical g_bar is ~5σ (ΔA = 0.57 ± 0.12; CFG840's variants move blue between 0.90 and 1.31, so the split
stays ≥ 2.5σ in every variant).

## Reading
The empirical rule the record now supports: **the excess appears only in gas-poor systems, and only at g_bar ≲ 10⁻¹² m/s².**
Gas-rich systems obey the law at every acceleration tested. This is the qualitative signature of canonical H-EX (free cold
energy = cold share of expelled baryons, which matters only where the law's own cold mass is small), but H-EX's census version
(CFG822: free share spread to r_ta) is too weak in dSphs and H-PRIM's universal concentrated core (CFG844/845) over-predicts
gas-rich dwarfs. A version tied to each system's ACTUAL gas removal is the open candidate; it needs an independent measure of
removed gas before it can be frozen.

κ = ½ fitted; cold energy mass required; not theory closed.
