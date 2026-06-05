# Empirical predictions of the a₀ ↔ Λ framework — four independent channels

**C. Zimmerman, June 2026.** Reproducible, independently-testable predictions worked *inside* the framework, taking
its two premises as given and computing what they imply across four observational channels. Every script runs
standalone on a laptop (`python doorN_*.py`), uses real public data where data exists, and prints an honest
scorecard — successes, inherited tensions, and non-wins alike.

## The premises (taken as given here; argued elsewhere in the repo)

1. **The scale:** `a₀ = c²·√(Λ/32π) = (c/2)·√(G ρ_Λ) ≈ 9.4×10⁻¹¹ m/s²` — the MOND acceleration scale *is* the
   cosmological constant. (The 32π coefficient is route-forced and does **not** enter any test below.)
2. **The evolution:** `a₀(z) = a₀(0)·√(ρ_DE(z)/ρ_DE0)` — the scale tracks the **dark-energy density** history.
   Under DESI DR2 (w₀=−0.752, wₐ=−0.86) this is **non-monotonic**: a₀ rises ~6% to a peak near z≈0.4, then declines.

**The through-line.** All four doors test the *same* law, and the prediction is **coefficient-free**: in every
channel the observable ratio reduces to `(ρ_DE(z)/ρ_DE0)^(1/4 or 1/2)`, so the un-derivable 32π and the `c²√G`
prefactor cancel. The dark-energy history that DESI measures fixes all four predictions at once.

## The four doors

| # | Channel | z=0 status (real data) | Distinctive prediction | Script |
|---|---------|------------------------|------------------------|--------|
| **4** | **MDAR** (master relation) | reproduces SPARC mass-discrepancy relation, **0.195 dex** (175 galaxies, 3389 pts) | deep-MOND missing-mass factor **~12% smaller at z=3** at fixed g_bar | `door4_mdar_evolution.py` |
| **2** | **Dwarf spheroidals** | **5/8** classical dSphs within ~40% (median 24%), **no dark matter**, EFE included | fixed-mass dwarf **~7% colder at z=3** (σ∝a₀^¼) | `door2_dwarf_spheroidals.py` |
| **1** | **Gravitational lensing** | reproduces KiDS lensing RAR (Brouwer+2021, z~0.3) | **saturated deflection** α∞=2π√(GMa₀)/c² (b-independent — no halo mimics it); amplitude **non-monotonic** (peak z~0.4) | `door1_gravitational_lensing.py` |
| **3** | **Early galaxies** (JWST/ALMA) | high-z discs sit ~on the z=0 BTFR within errors | discs **~11–16% below** the z=0 BTFR at z=4–6 — a **sign test** that excludes the rising √ρ_total reading | `door3_early_galaxies.py` |

## Honest scorecard (the whole truth, not the highlight reel)

- **Genuine successes inherited from MOND:** the z=0 MDAR/RAR (0.195 dex), most dwarf dispersions, and the lensing
  RAR are all reproduced by the *single* scale a₀ with no dark matter and no per-galaxy fitting.
- **Tensions inherited from MOND, reported not hidden:** Draco, Ursa Minor (and, under our EFE coefficient, Sextans)
  are over-dispersed vs the prediction — the long-known dSph problems. Clusters and the bullet cluster (elsewhere in
  the repo) still need a separate dark component. The framework is MOND at galaxy scales and carries MOND's baggage.
- **An honest non-win:** the *declining* a₀ works mildly *against* JWST's "too massive too early" galaxies — a
  constant/rising a₀ would help more there. The framework's distinctive feature is a liability for that puzzle.
- **What's genuinely new and falsifiable:** the **evolution**. The same coefficient-free √ρ_DE law predicts a
  specific, correlated shift across all four channels. The cleanest single test is the **high-z BTFR offset** (Door
  3): its *sign* already excludes the rising reading, and its *magnitude* (~11% at z≈4) is the make-or-break
  deep-MOND disc measurement (JWST/ALMA kinematics; forecast in `../reviews/z3_bridge_forecast_mc.py`).

## What kills it, what confirms it

- **Confirms:** DESI DR3 (~2027) cements dynamical dark energy **and** high-z discs land ~11% below the z=0 BTFR with
  the predicted √ρ_DE shape, correlated across the four channels.
- **Kills:** DESI reverts to constant Λ (removes all distinctive content → ordinary MOND); or the high-z BTFR offset
  comes back flat-or-positive when DESI says dynamical (direct falsification); or a direct dark-matter detection
  (kills MOND and the framework together).

## Reproducing

```bash
cd real_research/predictions
python door4_mdar_evolution.py      # needs ../data/sparc_data/  (included)
python door2_dwarf_spheroidals.py
python door1_gravitational_lensing.py
python door3_early_galaxies.py
```
Each writes a figure to `../figures/doorN_*.png` and prints its full numeric table + verdict. Dependencies: `numpy`
(+ `matplotlib` for figures). No network, no fitting, no hidden parameters — the only inputs are the published a₀
anchor, the DESI w₀-wₐ dark-energy law, and the real galaxy data in `../data/`.
