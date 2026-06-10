# Does a₀ track the large-scale cosmic web? — the missing environmental fork test

**Date:** 2026-06-05 · **Script:** [`reviews/project_sparc_a0_vs_cosmicweb.py`](project_sparc_a0_vs_cosmicweb.py) · **Figure:** [`figures/a0_vs_cosmicweb.png`](../figures/a0_vs_cosmicweb.png) · **Table:** [`data/sparc_a0_environment_table.csv`](../data/sparc_a0_environment_table.csv)

**GRADE: UNIVERSALITY EVIDENCE (category ii).** Per-galaxy a₀ shows **no** correlation with large-scale
ambient density across **three independent external density fields**; the strong environmental fork
(a₀ ∝ √ρ_local, slope +0.5) is excluded, and the result is consistent with the framework's uniform
rho_Λ reading. This is a NULL, and the null is the valuable result.

---

## The fork

The framework a₀ = (c/2)√(G ρ) has three readings for *which* ρ sets a₀:
1. **ρ_Λ** (cosmic, uniform) → a₀ universal, the same everywhere.
2. **ρ_total/ρ_crit** → a₀(z), evolves (tested elsewhere).
3. **ρ_local** (ambient matter) → a₀ rises with environment, slope d log a₀ / d log(1+δ) = **+0.5**.

Fork 3 has an *internal* version (a₀ vs a galaxy's own surface density — already disfavoured: the
residual is an M/L artifact, see [`project_sparc_a0_vs_density_direct.py`](project_sparc_a0_vs_density_direct.py),
and the RAR scatter bounds σ(ln ρ_source) < ~32%, see [`project_rar_bounds_rho_uniformity.py`](project_rar_bounds_rho_uniformity.py))
and a **large-scale-environment** version — does a₀ track the *cosmic-web* density (void vs filament vs
cluster) at a galaxy's location? SPARC has no environment column, so this needed an **external cross-match**.
Both prior scripts flagged it as the genuinely-missing test. This supplies it.

## Method

- **a₀ per galaxy** — fit from the deep-MOND points of `data/sparc_data/*_rotmod.dat` exactly as the
  direct-density script does: M/L = 0.5 disk / 0.7 bulge; deep-MOND cut g_bar < a₀/3; log₁₀ a₀ =
  2 log₁₀ g_obs − log₁₀ g_bar; median over deep points. (165 galaxies fit.)
- **Position/distance** — RA/Dec/cz from `data/sparc_ned_positions.json` (NED, 122 galaxies); measured
  distance D from `data/SPARC_Lelli2016c.mrt`.
- **Three external density axes**, each a different catalogue, scale, and systematic:

| | Field | Source | Density axis | Geometry | N |
|---|---|---|---|---|---|
| 5a | 2MRS counts-in-cylinders | Huchra+2012 (J/ApJS/199/26) | volume-limited galaxy counts, 2 Mpc | redshift-space | 90 |
| 5b | Tully group halo mass | Kourkchi&Tully 2017 (J/ApJ/843/16) | host group log M_halo + cluster/field | group dynamics | 103 |
| 5c | 2M++ density field | Carrick+2015 | reconstructed δ, 4 Mpc/h | **real-space** | 122 |

## Results (all computed on real data)

**5a — 2MRS counts-in-cylinders** (the primary):
- Spearman a₀ vs (1+δ): **r = +0.12 (p = 0.24)** — no rank correlation.
- Slope d log a₀ / d log(1+δ) = **+0.052 ± 0.043** — 1.2σ from 0, **10.5σ from +0.5**.
- Binary fork: dense and void thirds differ by 1.22 dex in density but only **+0.07 dex in a₀** (p = 0.17);
  fork-3 predicts +0.61 dex → observed is **9× too small**.
- Normalization validated by Monte-Carlo: random sky positions give median 1+δ ≈ 0.6 vs SPARC's ≈ 4.8;
  the excess is genuine galaxy-clustering bias (rank/slope invariant).

**5b — Tully group halo mass** (independent catalogue + systematic):
- a₀ vs log M_halo: Spearman **r = +0.15 (p = 0.13)**; slope +0.036 ± 0.030.
- All-sky cluster-vs-field binary (the Ursa-Major test generalized): **−0.002 dex (p = 0.60)**, where the
  strong fork needs +0.5…+1.0 dex (cluster cores ~10–100× denser than the field). Excluded.

**5c — 2M++ real-space field** (removes the redshift-space caveat; validated: Virgo +8.3, Coma +12.8):
- Spearman a₀ vs (1+δ): **r = −0.08 (p = 0.38)**; slope **−0.046 ± 0.081** — 0.6σ from 0, **6.8σ from +0.5**.
- Partial Spearman controlling distance: r = −0.09 (p = 0.31). Void-vs-dense binary: −0.094 dex (p = 0.32).
- Better void coverage (20 underdense galaxies) and the full SPARC distance range.

**Confound control (the flagged Local-Volume risk):**
- (1+δ) anticorrelates with distance (r = −0.375) — the genuine Local-Volume signature — **but** a₀ does
  **not** correlate with distance (r = −0.07, p = 0.51), and the a₀–δ null survives partial-correlation
  and a fixed 10–35 Mpc distance slice. The distance confound is not masking a signal.

**Proxy validity + look-elsewhere (§5d):**
- The external fields **agree on which galaxies are dense** — 2MRS vs 2M++ Spearman **r = +0.58 (p ≈ 3×10⁻⁹)**,
  Tully vs 2M++ r = +0.21 — so the convergent null is *informative*, not the result of junk proxies.
- Family-wise permutation over the **three environment proxies**: most-extreme |r| = 0.15, **global p = 0.32** →
  no environment coupling survives look-elsewhere.
- Independently red-teamed: an agent reconstructed every pipeline from scratch and confirmed all numbers
  (per-galaxy a₀ to 4 dp, the 2M++ convention via Virgo/Coma, the KT2017 matches), found **no bug producing
  a false null**, and judged the grade fair (full audit reproduced 2M++ −0.08, +0.5 excluded at 6.8σ/10.5σ).

**Power (injection-recovery):** the 3σ minimum detectable slope is **~0.15**. An injected +0.5 fork is
recovered at ~12σ (100% detection) — we *would* have seen it. A weak/hybrid coupling with |slope| < ~0.15
is **not** excludable.

## Honest caveats (kept loud)

- **Local-Volume-biased sample** (median cz ~770 km/s): modest cosmic-web dynamic range, little void
  coverage → bounds the *strong* fork far better than a weak one.
- **Power floor ~0.15**: decisive against the strong fork, but a hybrid `√(ρ_Λ + local matter)` coupling
  (which dilutes the contrast, since ρ_Λ ≈ 2 ρ_mean) below |slope| 0.15 is not reached.
- **The strongest correlation is real — and it is NOT the environment.** a₀ vs Hubble-T is r = −0.263
  (p = 0.003, N = 122) and *does* survive look-elsewhere. But T is **internal** morphology: a₀–T stays
  r = −0.27 after controlling for the 2M++ density (internal, not environment-mediated), and T barely tracks
  environment here (T vs 2M++ r = −0.11). It is the internal M/L+coverage artifact dissected in the
  direct-density script (T tracks SBdisk, whose a₀-trend collapses in gas-dominated galaxies); my own
  M/L-free T-subset is underpowered (N ≈ 29), so the clean proof is that script's, not an overclaim here.
  Crucially, the **three large-scale-environment proxies stay null under look-elsewhere (family-wise p = 0.32)**.
- **Necessary, not sufficient**: environment-independence is *required* by √(ρ_Λ) but does not *prove* ρ_Λ
  causes a₀ — that is the a₀(z) evolution test (category iii).

## Convergence

Seven density axes now agree on **no a₀–environment coupling** and all exclude +0.5: internal Spitzer SB
and the RAR-scatter bound (direct/`_rar_bounds_`); the SPARC-self kNN density and the Ursa-Major split
([`sparc_environment_a0_REAL.py`](sparc_environment_a0_REAL.py)); and the three external fields here
(2MRS, Tully, 2M++) spanning redshift-space and real-space, 2 Mpc to 4 Mpc/h scales. The breadth of the
convergence is the strength of the case.

## Provenance / reproduce

```
# external catalogues (downloaded to data/; regen commands in the script docstrings):
#   2mrs_huchra2012.tsv        VizieR J/ApJS/199/26   (2MRS, Huchra+2012)
#   kt2017_galaxies.tsv        VizieR J/ApJ/843/16/table3
#   kt2017_groups.tsv          VizieR J/ApJ/843/16/table2
#   twompp_density.npy         https://cosmicflows.iap.fr/assets/data/twompp_density.npy
python3 reviews/project_sparc_a0_vs_cosmicweb.py
```
