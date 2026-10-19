# CFG861 FROZEN CRITERIA: do unresolved binaries make the CLASSICAL dwarfs' excess? (before any script)

**Why.** CFG860 (NOT GAS) and CFG843 leave two readings for the faint-dwarf excess (+0.3 to +0.5 dex in g at g_bar < 10⁻¹² m/s²):
something real in every faint pressure-supported dwarf, or a measurement systematic they share. Binary stars inflate
single-epoch velocity dispersions. The ultra-faints were checked (CFG29, 46, 51, 78, 93, 259: binaries trim the excess, do not
remove it). The classical dSphs were never cleaned: CFG51's reducer listed them (Draco, Ursa Minor, Sextans, Carina, CVn I,
Leo II, Crater 2, Antlia 2, Fornax, Sculptor, Leo I) but did not analyse them. Walker+2023's per-epoch catalogue is on disk
(`real_research/data/walker2023/`).

## Reduction (reuse, do not re-invent)
Use CFG51's reducer (`campaign_fresh_gravity/CFG51_walker_multiepoch/reduce_walker.py`) unchanged: quality cut, membership v2
(logg, fixed velocity window with σ_seed = max(LVD σ, 3 km/s), Gaia PM, parallax; one recentring), Gaussian likelihood with
known errors, epochs pooled across instruments by Gaia id. Classical = LVD-matched and M_V ≤ −7.7 (CFG51's rule).

**Like-for-like binary shift.** For each classical system, take the members with ≥ 2 quality epochs (the multi-epoch set M):
- σ_single(M): first quality epoch of each star in M.
- σ_clean(M): drop stars in M whose epoch velocities give χ² about their weighted mean with p < 0.01 (CFG51's rule), then use
  the all-epoch mean velocities of the rest.
- δ = 2 log10(σ_clean(M)/σ_single(M)) (dex in g_obs; negative = binaries inflated the dispersion).
Same stars, same footprint, so δ isolates binaries from membership and radial-coverage differences. **Informative** if
|M| ≥ 30. CFG51's full-sample estimators (single / allmean / clean / paperflag) are reported for every system.

**Δ.** Δ_LVD = CFG860's Δ (CFG852's `delta_ups2`: Υ_V = 2, Wolf at r_1/2 = 4/3 r_h, ν_e, canonical a0 = 9.3603e-11 graded,
alt 1.1312e-10 reported). Δ_clean = Δ_LVD + δ.

## Graded sample and classes
Graded: informative classical systems with log10 g_bar < −11.9 (where the excess lives, CFG828). m = mean Δ_clean over them,
s = its standard error (std/√N); mean δ and its standard error reported.
1. **NOT DIAGNOSTIC** if fewer than 4 graded systems.
2. **BINARIES EXPLAIN** if m < +0.10 dex and m < 2s (cleaned excess consistent with the law).
3. **BINARIES MINOR** if |mean δ| < 0.05 dex and m > 3s (cleaning barely moves it; the excess stands).
4. **PARTIAL** otherwise (binaries remove a measurable piece, or the result is in between).

**Reported, not graded:** alt footing; every classical system (including those at higher g_bar) with |M|, multi-epoch
fraction, n removed, σ_single(M), σ_clean(M), δ, Δ_LVD, Δ_clean; Υ_SFH Δ from CFG828 where present; the binary dispersion each
system would need to make its whole excess, σ_bin = σ_LVD √(1 − 10^(−Δ_LVD)), against the ~4.5 km/s single-epoch bound
(McConnachie & Côté 2010, as used in CFG29); a variant with |M| ≥ 15; a variant using CFG51's paper-flag cleaning; the UFD
results of CFG51/CFG93 quoted (not re-run) for the combined picture.

**Declared limitations.** Binaries with periods much longer than the epoch baselines (or tiny amplitudes) escape the χ² test;
δ is a lower bound on the binary effect for the multi-epoch set. Single-epoch stars are not used in δ. Crater 2 and Antlia 2
are tidally disturbed; tides are already on the record (CFG838/839) and not re-tested here. No epoch zero-point offset is
modelled (CFG51's choice).

## Controls
- **K1:** the reused reducer reproduces CFG51's committed UFD dispersions (`walker_reduced_dispersions.tsv`) for Boötes I and
  Tucana II (single and clean) to 1e-6 km/s.
- **K2:** for Draco, Δ_LVD equals CFG860's Draco Δ (`cfg860_results.json`) to 1e-9.
- **MUTATE** (separate outputs, `CFG861_MUTATE=1`, seed 861): in every graded system, add an independent per-epoch velocity
  offset drawn from N(0, 10 km/s) to every epoch of a random 50% of the stars in M. Must hold: (a) the cleaning removes ≥ 70% of
  the injected stars across the graded systems; (b) mean δ ≤ −0.10 dex (the injection inflates σ² by ~50 km²/s², i.e.
  +0.18 to +0.26 dex for σ = 6–10 km/s). Either failing means the cleaning has no teeth here.

## Resources
A 1024³ run (NCS0) is live. One process, numpy/scipy only, no downloads, well under 1 GB; single-thread BLAS environment.

κ = ½ fitted; cold energy mass required; not theory closed.
