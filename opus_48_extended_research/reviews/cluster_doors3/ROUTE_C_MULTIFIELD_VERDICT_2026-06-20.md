# ROUTE C — multi-field / extended no-particle dark sector vs the cluster-core residual — VERDICT 2026-06-20

**Key:** `multifield_dark_sector`. **Scripts:** `opus_48_extended_research/reviews/cluster_doors3/`
(`routeC_multifield_core.py`, `routeC_galaxy_veto.py` [real 175-SPARC], `routeC_cassini_bimetric.py`,
`routeC_synthesis_gates.py`). Real A2029 profiles (Sohn+2019, LBS03), real SPARC rotmod, framework footing
a0=9.36e-11. Both-ways + quarantine held (a0/Z/κ/I0 never asserted derived).

**HEADLINE (both ways): NO multi-field no-particle extension passes all four gates. The ~30–49%
gas-tracking core residual is structurally inaccessible to any second field (aether vector, second scalar,
or bimetric partner) that stays galaxy- AND Cassini-safe. Route C CONFIRMS the residual is the irreducible
shared-MOND core gap — it does not close it.**

## What was hunted (the genuinely-untried multi-field door) and the gate it breaks

| Sub-route | G1 suff. | G2 galaxy | G3 no-particle | G4 data | Why it fails |
|---|---|---|---|---|---|
| **C(a) AeST aether VECTOR A_μ** | FAIL (~0.1–0.5% of core) | squeeze | PASS (own field) | FAIL (shape) | Eling-Jacobson static-aether: in spherical symmetry the aether is forced timelike, the curl/vector kinetic sector vanishes (Mistele 2305.07742). Its ONLY g-contribution is the μ² mass term, which scales as (μr)² → negligible in the CORE (f~0.001 @50 kpc, only O(1) at R500). ρ_aether is centrally HOLLOW (rises outward, then goes negative) = anti-gas-tracking. Same μ² term banked falsified-as-closure at R500, now also dead in the core. |
| **C(b1) 2nd scalar, fixed-length Yukawa** | PASS (α~0.98) | FAIL (a0 +0.30 dex) | PARTIAL (relocates) | FAIL (shape OR Cassini) | α~0.98 fills the core, but a UNIVERSAL coupling shifts the SPARC RAR/BTFR a0 by +log10(1+α)=+0.30 dex (1.85× the welded 9.36e-11) on real 175-SPARC — scatter-invisible but a0-normalization-FATAL, shattering the a0=Λ weld. A universal coupling tracks total baryons = stars → NOT gas-tracking. |
| **C(b2) 2nd scalar, density-triggered (chameleon)** | maybe | FAIL (env. order) | PARTIAL (new V) | FAIL | Galaxy/solar cores are ~275–10⁵× DENSER than cluster cores → any density-triggered clustering fires in galaxies FIRST (the density-a0 graveyard). No threshold is cluster-core-ON/galaxy-OFF. Adding V(χ) breaks shift symmetry = new structure. |
| **C(c) bimetric / massive-graviton** | maybe | FAIL | FAIL (new spin-2) | FAIL | Same universal-vs-composition/Cassini dilemma + Higuchi-ghost in the nonlinear cluster regime + a new spin-2 species (5 dof) = relocates fully. c_GW=c forces a tuned Mpc scale. |
| [ref] framework's OWN K(Q) dust | partial | PASS | PASS | FAIL (shape) | The framework's second field IS the K(Q) Q-sector dust (CMB-fitting, cold w=0). CDM-like by construction → tracks total matter, NOT gas. Amplitude I0 free, orthogonal to a0. Already credited in the banked ~17–20% Y-Q boost; cannot be made gas-tracking. |

## The structural theorem (why every multi-field route fails — the load-bearing result)

The gas-tracking core residual demands a field that simultaneously (1) supplies ~41% extra mass in the
CORE (50–420 kpc), (2) TRACKS THE GAS (smooth ~10×-gas, M_res/M_star rising 15–30× outward), and (3) does
NOT do (1) in galaxies (galaxy-veto) or the solar system (Cassini). A second gravitational field can
discriminate cluster-core from galaxy/solar by only THREE scales, each of which fails (2) or (3):

- **(A) a LENGTH scale (Yukawa range):** universal across baryons → tracks STARS not gas (fails 2); and if
  range ≥ galaxy, re-bends the galaxy a0 by +0.30 dex (fails 3, verified on real SPARC).
- **(B) a DENSITY scale (chameleon):** cluster cores are LESS dense than galaxy/solar cores → fires in the
  wrong environment (fails 3 — the density-a0 graveyard, ordering backwards).
- **(C) a COMPOSITION scale (gas vs stars):** the ONLY way to satisfy (2), but it is a composition-dependent
  fifth force → Cassini |γ−1|<2.3e-5 exceeded by ~5 orders at α~1, with NO screening window (any screen that
  saves the denser/heavier-enclosed Sun also screens the less-dense/lighter cluster core).

There is no fourth discriminator. ⟹ the gas-tracking core residual is structurally inaccessible to any
no-particle multi-field extension that stays galaxy- and Cassini-safe.

## Key numbers
- A2029 core (real, relaxed XRISM-clean): M_res(<420 kpc) = 6.94e13 M☉; bare-MOND coverage 59.3%; residual
  ~41% = inside the ~30–49% shared gap. M_res/M_gas flat 1.8→1.3 (gas-tracking).
- Aether mass-term f = κ(μr)², κ=0.48: f~0.0012 (50 kpc), 0.0048 (100 kpc), 0.085 (420 kpc), 0.81 (R500). ρ_aether/ρ_gas ~0.02–0.07, rising outward (hollow).
- 2nd-scalar Yukawa to fill core: α=0.979 → galaxy a0 shift +0.297 dex (1.85× welded a0). Real-SPARC RAR scatter: 0.153 raw / 0.130 M/L-absorbed (alpha=0) → 0.187 / 0.139 (alpha=0.98) — scatter-invisible, a0-fatal.
- Environment ordering: ρ_gal_core ~2e-20 vs ρ_clus_core ~7e-23 kg/m³ → ~275× denser galaxy.
- Cassini: composition-dep α~1 → |γ−1|~1 vs bound 2.3e-5 → exceeded ~4e4×.

## Honest caveats (both ways)
- The aether vector route was ALREADY substantially banked (cluster_aether_stress_derivation.py at R500); this
  round's NEW contribution is the CORE-specific (μr)² magnitude + the anti-gas-tracking shape, and folding in
  the now-confirmed gas-tracking standing. Not a fresh kill of a live door, a hardening of a known one.
- The G2 failure of the universal Yukawa is NOT a scatter blow-up (a universal fifth force is RAR-scatter-
  invisible — reported straight, no manufactured deficit) — it is an a0-normalization kill (+0.30 dex). This is
  the load-bearing both-ways subtlety done right.
- The genuine TENSION is the universal-coupling case: a universal (1+α) renormalizes G and is NOT directly
  Cassini-bound — but then it tracks stars (fails the gas-tracking shape) and breaks the galaxy a0. The Cassini
  ~5-order kill bites only the composition-dependent (gas-tracking) version. Either branch breaks a gate; no
  branch survives both.
- Route C RELOCATES the postulate honestly: even a hypothetical working second field is undrived new structure
  the framework does not derive (so "no new structure" is forfeited even where "no new particle" is kept).

## Standing impact
Route C is now in the **exhausted/killed** column alongside density-a0, MI mean-mass, dS-Unruh environmental,
keV/eV sterile, condensate accumulation, IGIMF (shape-closed), and the final-door third-ingredient check. The
~30–49% gas-tracking core residual is **confirmed irreducible to no-particle multi-field extensions** —
generic shared relativistic-MOND core gap, NOT framework-specific, NOT a referee-proof kill (post-XRISM η
bracket keeps the magnitude ambiguous). No manufactured cure; no reflexive dismissal.

**Sources:** Skordis-Zlosnik 2021 PRL 127 161302 (AeST action); Durakovic-Skordis 2024 JCAP 04 040
(arXiv:2312.00889, isothermal spheres, RAR peak + negative phantom mass); Verwayen-Skordis-Zlosnik 2024 MNRAS
531 272 (arXiv:2304.05134, quasistatic, free boundary χ̂_out); Eling-Jacobson 2006 gr-qc/0603058 (static
aether timelike); Mistele 2023 2305.07742 (spherical curl vanishes); Mistele-McGaugh-Schombert 2023 A&A 676
A100 (galaxy↔cluster μ scale tension); Famaey-Durakovic 2025 (arXiv:2501.17006); Bullet residual 2605.10022;
FPS lensing 2410.02612; Bertotti+2003 (Cassini |γ−1|); banked A2029/RXJ1347 gas-tracking + dark-sector-CMB
ledgers.
