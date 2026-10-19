# CFG828 — the uniform dwarf excess: law shape at low acceleration, or pressure-supported systems?

Criteria: `FROZEN_CRITERIA.md` (dbbfeedff, before the script). Run: `python3 cfg828.py` (MUTATE `CFG828_MUTATE=1`). Seconds.

## Result — CLASS (canonical, primary ν): **MIXED** (neither frozen class; the result is a location in acceleration)
- **Where SPARC and the dwarfs overlap (g_bar ≥ ~10⁻¹² m/s², N = 8: Leo I, Leo II, Sculptor, Fornax, And VII, NGC 147/185/205),
  pressure-supported dwarfs sit where rotating discs do:** D = Δ_dwarf − Δ_SPARC = +0.05 ± 0.07 dex (z +0.7), identical on
  both ν kernels and both footings. So the excess is NOT a property of dispersion-supported systems as such.
- **The excess lives below SPARC's floor.** 21 of 29 dwarfs have g_bar < 10^−11.9 (SPARC's lowest point is 8e-13 and its
  lowest bin holds 36 points); they average Δ = +0.44 dex (canonical; +0.40 alt). SPARC itself is flat at +0.02–0.07 dex
  down to its floor (K1 PASS, overall median +0.031).
- LAW-SHAPE was not declared because SPARC's in-range median (+0.04) is below the +0.10 bar: discs give no sign of the law
  failing where they reach.
- **Exploratory (post-hoc, not scored):** across all 29 dwarfs Δ anticorrelates with g_bar (ρ = −0.47, p = 0.011); the
  dwarfs' log g_obs–log g_bar slope is 0.34 against the law's deep-regime 0.5 (median g_obs = 0.19 a0, scatter 0.35 dex).
  The faintest systems sit above the law as if g_obs flattened toward a floor.
- **Reading:** the dwarf problem is an ultra-low-acceleration problem (g_bar ≲ 10⁻¹² m/s², y ≲ 0.01). There, either the
  law's deep regime is too steep (a law-shape failure discs cannot probe), or the faintest systems are inflated by things
  that act only there (Galactic tides / external field, binaries, non-equilibrium). A rotation or lensing probe at
  g_bar < 10⁻¹² is what separates the two.

## Controls
- K1 PASS (SPARC median +0.031 dex). MUTATE bites: σ/1.45 moves mean D by −0.32 dex (to −0.27, z −3.7), as required.

κ = ½ fitted; cold energy mass required; not theory closed.
