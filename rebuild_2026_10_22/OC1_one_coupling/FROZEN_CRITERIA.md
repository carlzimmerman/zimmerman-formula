# OC1_one_coupling: FROZEN CRITERIA (committed alone, before any script or new number)

**Question.** Does one coupling fraction of baryonic dissipation supply the energy each system's core needs, from SPARC galaxies to clusters? This is the direct-coupling idea's one real claim, and it includes the overlap test proposed by Argon.

**Standing.** κ = ½ FITTED. Footings separate, never pooled. Cold dark energy, never a particle. Not "theory closed". Nothing here says the data favour the framework. RF6 is finished and stays as committed.

**Energy bookkeeping only.** No mechanism and no action. A pass here would not mean any rule passes SPARC, groups, the keys or X-COP, and no G1–G4 grade runs here. It tests the idea on its own premises, using the old core targets. Those premises aren't current: the owner removed the floor, ZN3's clusters need no coring for X-COP, and "active" below inherits the floor.

## Energies
- E_SN: BE1's, 1e51 erg per 100 M☉ of stars. E_BH: CL4's, 0.1 × 0.005 M★ c². Both provisional inputs, per M★ the same at every mass.
- Galaxy needs, per galaxy, committed files: **soften** BE1 (`be1_results.json`, η 21.2); **undo** CN1 (`cn1_energy.json`, Υ 0.50); **both** = their sum over galaxies in both files.
- Cluster need: CL4's `ereq` at 1e13, 1e14, targets 14.3, 10.82, f★ 0.034, 0.0615, with η_conv as CL4 committed **and** with A4's converged η. A4 is primary, as the governing later value.

## Two readings, never merged
- **Reading 1, one coupling proper:** ε = E_req/(E_SN + E_BH) everywhere. This is the only form that is one number.
- **Reading 2, two sources:** ε = E_req/E_SN in galaxies, E_req/E_BH in clusters. Two fractions that might coincide. Any agreement carries **[TWO SOURCES]**.

## Gates, on each reading and footing, galaxy job "both" primary
- **G-CONST:** within SPARC, rms of log₁₀ ε ≤ 0.30 dex and |Spearman(ε, M₂₀₀)| ≤ 0.30.
- **G-OVERLAP:** galaxy 16–84 % interval overlaps the cluster interval (min to max over mass and f★, A4 η, target 14.3 and 10.82).
- **G-RATIO:** median galaxy ε and cluster ε (A4 η, target 14.3, geometric mean over mass, f★) within a factor of 2.

## Classes
- **ONE COUPLING:** all three pass on Reading 1.
- **ONE COUPLING [TWO SOURCES]:** fail on 1, all three pass on 2.
- **INTERVALS OVERLAP ONLY:** G-OVERLAP passes on some reading, the full set on none. Name the reading.
- **NO ONE COUPLING:** G-OVERLAP fails on both.

## Reported, not graded
- Same with job soften alone and undo alone.
- Bands, overlap only: E_SN × 0.6–1.8, M_BH ± 0.3 dex. A wide band makes overlap easy, so it can't change a class.
- ε by M₂₀₀ bin.
- SPARC galaxies with zero need that still have E_SN > 0, a count: one coupling gives them energy they don't need.
- Dwarfs, sign only: SN1's S_min 46–64 against native S 44.2 (1e10), 79.1 (1e11).

## Checks
- **K1:** CL4's committed η_conv reproduces its worst ε_AGN 0.075 and ε_SN 6.71, ≤ 1e-3 relative. **K2:** BE1's medians, CN1's 0.094 read from the files. **K3:** a synthetic constant ε passes G-CONST and returns itself.
- **MUTATE:** E_BH × 0 must make Reading 1 equal Reading 1 with SN only and change G-RATIO's number by the expected factor.
- Any K failure: no verdict, exit 1.
