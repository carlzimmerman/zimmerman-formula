# X26_cold_sector_map: which sound-speed laws for the cold sector survive the record's constraints?

Criteria: `FROZEN_CRITERIA.md` (b10263968f, committed alone, before any script or number). `AMENDMENT_A1.md` holds A1
(implementation: a NaN in the cluster-table interpolation; RUN1 was killed before any graded number), A2 (post-result check
K5: direct re-grading of the allowed points) and A3 (post-result, reported only: MGAS500 terciles and a fine universal scan).
κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy is gravitating field mass, never a particle.
The map is exhaustive, not a fit: no best-fit point is reported. Not "theory closed". Nothing here says the data favour the
framework. Every number is from `x26_cold_sector_map.out` / `_results.json` / `x26_pass_masks.npz` or `x26_derive.out`.

## The family

    c_s²(system, z) = c_*² (σ/100 km/s)^{2r} (ρ_b/10⁻³ M☉ pc⁻³)^q a^{2p−1}

Here σ and ρ_b are each system's own velocity scale and mean baryon density (X19's conventions). The cosmic medium is X22's
forest half-mode perturbation, so its sound speed scales as c_s,cos ∝ a^{p_eff−½} with **p_eff = p − r/2 − 3q/2** (derived,
D1). The grid has 55 539 points per footing: c_* = 1 to 10⁴ km/s in 0.125-dex steps, r from −1 to 3, q from −1 to 1 (steps of
0.125), and p ∈ {3, 4, 6}.

Retention uses the record's own machinery:
- SPARC: X22's d2 line;
- groups, the MW disc and the 74 dwarfs: the peer lane's flat-well predictor;
- the 106 KT clusters: X23_late_heated_cold's hydrostatic model in the C\* potential (cold self-mass sources AQUAL and
  lenses);
- the forest and σ₈: X22's linear ODE.

## Verdict (frozen classes): **ALLOWED ONLY WITH SEPARATE c₀**, both footings

- **The family alone (scenario A) is EMPTY.** C-dwarfs fails at every one of the 18 513 (c_*, r, q) points, on both
  footings. The family cannot reproduce X24's mass-driven dwarf extra.
  - The smallest family χ² anywhere on the grid is 449 (canonical) / 436 (alt). X24's floor gives 287 / 278 on the same 74
    dwarfs, and the law alone gives 734 / 658.
  - The "closing pairs" are therefore C-dwarfs paired with any other constraint. C-dwarfs is empty on its own.
- **With the dwarf extra assigned to a separate c₀ (scenario B), an allowed region exists:** 45 grid points (canonical) and 37
  (alt), 8e-4 / 7e-4 of the grid.
  - In (c_*, r, q) these are 19 points (canonical) and 16 points (alt), listed with their margins in the `.out` A2 block.
  - C-dwarfs-c₀ never binds: scenario B equals "no dwarf constraint at all" on both footings.

### The allowed region (scenario B)

| | canonical | alt |
|---|---|---|
| log₁₀ c_* (km/s) | 2.375 – 4.0 (grid edge) | 2.625 – 4.0 (grid edge) |
| r | −0.625 – +0.375 | −0.625 – +0.25 |
| q | −0.125 – +0.875 | −0.125 – +0.875 |
| p | 3, 4, 6 (p = 3: 10 of 19 (c_*, r, q); p = 6: all 19) | 3, 4, 6 (8 / 13 / 16) |
| c_s at the KT-cluster median (σ 517 km/s) | 556 – 736 km/s | 595 – 761 km/s |
| c_s at the SPARC median (σ 70.5 km/s) | 209 – 12 014 km/s | 386 – 11 794 km/s |

**Shape: a thin sheet, not a volume.** The KT terciles and the slope pin the clusters' cold sector to c_s ≈ 550–770 km/s,
about 1.1–1.5 × σ_KT. They also allow only a weak dependence across the cluster σ range (|r| ≲ 0.6).
- **On the sheet the margins are comfortable.** A2 re-graded every allowed point and its c_* ± 1 neighbours directly, with
  no table: 0 grade flips (K5), and every |Z| < 2 (`.out` A2 lines).
- **Across the sheet the window is narrower than the grid step.** The cluster window is about 0.05 dex wide; the grid step
  is 0.125 dex. The grid therefore samples the sheet sparsely, and the true region is larger than the 45 / 37 points.
  - Evidence: on the canonical footing, universal heating (r = q = 0) passes the KT terciles and slope at **634–714 km/s**,
    yet no grid node lands there (A3 fine scan). On alt the window is **673–773 km/s**, and the node at 750 km/s is allowed.
- **The sheet reaches the c_* = 10⁴ grid edge** at r ≈ −0.6, q ≈ +0.75–0.9, so it is open there.

**The tightest constraints** (B leave-one-out: how many points each opens when dropped; alt in brackets):
- C-T3: 45 → 60 (37 → 65);
- C-σ₈: → 54 (→ 62);
- C-KTb: → 55 (→ 46);
- C-forest: → 49 (→ 40);
- C-T1: → 48 (→ 40).

Single-constraint pass fractions (canonical; alt in the `.out`):

| constraint | pass fraction |
|---|---|
| C-T2 | 0.038 |
| C-T3 | 0.017 |
| C-KTb | 0.036 |
| C-SPARC | 0.365 |
| C-groups | 0.518 |
| C-MW | 0.504 |
| C-forest | 0.878 |
| C-σ₈ | 0.805 |
| C-CMB | 1.000 |

### Reported (A3, post-result): the MGAS500 terciles cut most of the sheet

X7's MGAS500 terciles (X23 A1's C-T1..T3) are not graded here: σ needs KT, so only the 106 KT clusters are graded (frozen
§3). Where r = 0, every cluster can be scored.
- **Universal heating (r = q = 0, 500–1000 km/s): the MGAS500 terciles fail everywhere on both footings.** The KT window
  above is real, but no universal c_s passes both slicings. X23 A1's "INTERSECTION EMPTY" was partly a node-spacing effect
  on the KT rows (its nodes were c_s,need × 3 and × 4). It still holds once the MGAS500 terciles are included.
- **Density-keyed r = 0 points (q > 0) also mostly fail.** Of the seven r = 0 allowed points, two pass all MGAS500
  terciles in both h cells:
  - canonical c_* 10^3.125, q +0.375;
  - alt c_* 10^3.25, q +0.5.

  The rest fail T2 (Z up to +2.40) or T3 (Z down to −5.07).

## Special cases

- **Universal late heating (r = q = 0, X23):** on the grid it is allowed on alt only (c_* = 750 km/s, p = 4 and 6). Off the
  grid, A3 finds the KT windows above, and the MGAS500 terciles exclude it on both footings.
- **Virial heating (r = 1, q = 0): EXCLUDED** on both footings at every c_*. C-KTb fails along the whole r = 1, q = 0 line;
  on canonical C-T3 fails too.
  - At c_* = 100 km/s (c_s = σ) it fails C-SPARC, C-T1, C-T2, C-T3 (canonical only), C-KTb and C-dwarfs-c₀.
  - A cold-sector temperature proportional to the cluster's own temperature reverses the KT slope, as X23's σ_KT bracket
    showed.
- **Density-keyed (q ≠ 0):** the region extends to q = −0.125 … +0.875. It needs q ≥ −0.125, so heating that grows toward
  low density (q < 0, VHC-like) is excluded except for a sliver.
- **X24b's VHC (r = 0, q = −1, p = 2):** marked EXCLUDED, citing `X24b_vacuum_heated_cold` JSON `verdict` = "NO EPS WINDOW"
  (3492bcbeb4). q = −1 is also the FP1 edge, and p = 2 is below X22's forest band.
  - Caveat from X24b D3: for q ≠ 0 the perturbations are non-barotropic, and the forest's Jeans suppression is 3.6 × weaker
    than X22's barotropic form used here. The C-forest cut is therefore conservative for q ≠ 0: it can only over-exclude.
- **Dwarf floor: no (c_*, r, q) reproduces it** (C-dwarfs empty; minimum χ² above). FP3 gives the reason below.

## First-principles cuts (`x26_derive.py`, sympy, 7/7)

| cut | inequality on (r, q) | effect on the map |
|---|---|---|
| FP1 thermodynamic stability | q > −1 (dP/dρ = (1+q)P/ρ > 0). Schwarzschild: a per-system isothermal profile is stable for γ > 1; the barotropic reading is stable iff q < γ − 1 (γ = 5/3 ⇒ q < 2/3; γ = 4/3 ⇒ q < 1/3), conditional on γ | the hard cut removes only q = −1 and never binds the region. The conditional γ = 5/3 cut would remove the allowed points with q ≥ 0.75 (`.out` A2 list) |
| FP2 causality | asymptotically: r ≥ 0 (σ → 0) and q = 0 (ρ → 0 and ρ → ∞), else a cutoff is needed. The computed cut is c_s < c in every graded system and in the cosmic medium to z = 1100 | the computed cut never binds the region (leave-one-out unchanged). Asymptotically, every allowed point with r < 0 or q ≠ 0 needs a cutoff |
| FP3 virial bound | a fluid bound with no external confinement has β ≥ 3 ⇔ c_s ≤ √(2/3) σ. log(c_s/σ) = log c_* + (r − 1) log σ + (q/2) log ρ is linear in (log σ, log ρ), so retained and expelled classes must be linearly separable | class medians: clusters T2/T3 bound with SPARC, groups, T1 and the MW unbound is possible (r −1 … 0.875, q −0.5 … 1). **Adding the dwarfs as bound is IMPOSSIBLE on both footings**: the first-principles reason C-dwarfs is empty |
| FP4 μ-pincer Part F | r = 0: the background passes through each well's state at (1+z)³ = δ_well; only the time factor escapes it. The forest needs p_eff = p − r/2 − 3q/2 above its threshold, which gives q ≤ (2/3)(p − r/2 − p_min) | graded through the p_eff threshold table (`.out`): the forest allows c_s,cos(today) ≤ 10^2.77 at p_eff = 3 and 10^3.35 at p_eff = 4. The σ₈ limit is 10^2.80 / 10^2.94 |

## Energy (reported; over the scenario-B allowed set)

| system | (3/2) Ω_c c_s²/(Ω_Λ c²) | per baryon |
|---|---|---|
| KT-cluster median | 2.0e-6 – 3.5e-6 (canonical); 2.3e-6 – 3.7e-6 (alt) | 26 – 46 keV (canonical); 30 – 49 keV (alt) |
| SPARC median | 2.8e-7 – 9.3e-4 (canonical); 9.6e-7 – 9.0e-4 (alt) | 3.7 keV – 12 MeV |

- The cluster row is about 10× X23's 3 keV at c_s,need.
- The top of the SPARC range comes from the r < 0, q > 0 end of the sheet.
- No action supplies this energy. The record's status is unchanged from X23: X6, X19 step 2, CFG944 Theorem G, CFG741 and
  CFG643.

## Step 0 and checks (11/11 PASS; MUTATE exit 1 as required)

| check | result |
|---|---|
| K0a X21 KT terciles + slope | 8.9e-16 |
| K0b X23 A1 KT A_pred at its 13 nodes | 0 |
| K0c X22 c_s,need by this lane's SPARC code at r = q = 0 | 190.014 / 201.315 (exact) |
| K0d X22 R_σ₈ and forest classes, p 3/4/6 | 0 deviation, identical |
| K0e peer groups/MW E_pred; X24 χ²_floor H 217.005 / 194.825, field 70.023 / 82.878 | 0 |
| K0f X24b verdict | "NO EPS WINDOW" |
| K1 table interpolation | 9.8e-3 ≤ 1 % (5 zero-weight KT clusters per cell interpolated linearly, A1) |
| K2 SPARC monotone in c_* | PASS |
| K3 sympy | 7/7 |
| K4 RSS | 0.60 GB |
| K5 direct re-grade of the allowed points (A2) | 0 flips |

- **MUTATE** (`X26_MUTATE=1`: m1 measured KT terciles T1 ↔ T3, m2 β factor 2 dropped): **K0a FAILS** (1.06), **K0c FAILS**
  (c_s,need 134.4 / 142.4), and K0e fails as well. The verdict is UNDECIDED (step 0), exit 1.
- `x26_derive.py` MUTATE (ρ ∝ a⁻²): D1 fails, exit 1.

## What this does not show

- **It is a grid.** The sheet is thinner than the c_* step, so the listed points sample it and do not bound it. The c_* = 10⁴
  edge is open.
- **The machinery is the record's:** isothermal statics in every system, a linear cosmic medium, and a barotropic forest
  (conservative for q ≠ 0). There are no assembly histories (X24b has them for VHC).
- **The MGAS500 terciles are reported, not graded,** and they remove most r = 0 points. A successor test should grade them
  with σ for all 326 clusters.
- **No action exists for any point,** and the energy at the cluster sheet is 26–49 keV per baryon. The allowed region is a
  target for an action, not a result about one.

## Run

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X26_cold_sector_map/x26_derive.py                         # exit 0, 7/7
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X26_cold_sector_map/x26_cold_sector_map.py                # exit 0, ~12 min, 0.60 GB
PYTHONHASHSEED=0 X26_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X26_cold_sector_map/x26_cold_sector_map.py   # exit 1 by design
```

Read-only inputs:
- X2's source (exec'd);
- X7's npz and JSON;
- the eRASS1 FITS and the SPARC rotmods;
- L346's JSON;
- X1's per-system CSV and the CFG257 Arroyo-Polonio table;
- the X19, X21, X22, X23 (both lanes), X24 and X24b JSONs.
