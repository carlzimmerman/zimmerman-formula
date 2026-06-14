# Route A — does a local potential / curvature modify the dS-Unruh (cH)² temperature FLOOR → a shifted a0_local? VERDICT (2026-06-14)

**Grade: CLOSED-FALSIFIER (the foundation licenses the dependence but DERIVES the wrong SCALE — a Tolman c²
redshift, ~1e-5 in any bound system, ~4-5 orders of magnitude short of the 2-25x clusters need). Sign is RIGHT;
magnitude is fatally small; the only large reading collapses to the BANKED density-a0 null.**
Code: `/tmp/dsunruh_tolman.py`, `/tmp/dsunruh_curvature.py`, `/tmp/sign_and_scale.py` (sympy/numpy).

## The foundation (Milgrom's own vacuum-effect derivation, web-confirmed)
T_eff = (ħ/2πckB)√(a² + (cH)²); the floor (cH)² is the **Gibbons-Hawking de Sitter horizon temperature** set by the
**COSMOLOGICAL Λ**: an inertial observer in dS sees T = αc√(Λ/3); an accelerated one sees T = α√(a²+c²Λ/3). a0 is the
break where a² meets the c²Λ/3 floor. **The floor is a property of the VACUUM (the global dS horizon), not of local
matter.** (Milgrom astro-ph/9805346; the search confirms the floor tracks the cosmological Λ, and the a0 break is where
the Unruh wavelength reaches the dS horizon.) This is the load-bearing fact: to shift a0_local you must shift the
floor, i.e. change the LOCAL VACUUM — and there are only two ways to do that.

## Route A sub-route (i): TOLMAN REDSHIFT of the floor temperature — DERIVED, RIGHT-SIGN, but ~1e-5
Tolman's law (a THEOREM of static-GR equilibrium thermodynamics, zero tuned input): T(r)√(-g00) = const, so a test mass
in a well sees the dS bath **blueshifted**: T_local = T_∞/√(1+2Φ/c²). Since a0 ∝ T_floor LINEARLY
(a0_eff = (2πckB/ħ)T_floor), **a0_local = a0/√(1+2Φ/c²)**.
- **SIGN: RIGHT.** Φ<0 ⇒ √(1+2Φ/c²)<1 ⇒ a0_local>a0. Deep wells BOOST a0. This is the correct direction for clusters.
- **MAGNITUDE: FATAL.** The factor is set by Φ/c², the relativistic scale. Bound systems are non-relativistic:
  - galaxy disk Φ ≈ −(200 km/s)² ⇒ 2Φ/c² = −8.9e-7 ⇒ a0_local/a0 = **1.0000005** (SPARC-safe — but trivially, nothing happens)
  - cluster core Φ ≈ −(1500 km/s)² ⇒ 2Φ/c² = −5.0e-5 ⇒ a0_local/a0 = **1.000025** (NEED 2-25x; got 0.0025%)
  - to BOOST a0 by 2x needs 2Φ/c² = −0.75, i.e. |Φ| = 0.375c², an **escape velocity ~0.87c** — a black-hole horizon,
    not a cluster. Clusters fall short by a factor ~1.5e4.
- **DERIVED, not tuned** — the scale c² is FORCED by the theorem. But c² is the WRONG scale (off by 4-5 dex). This is a
  scale-mismatch failure of exactly the same species as the banked ELL_DESITTER null (the derived horizon was Gpc, also
  the wrong scale by the same physics — non-relativistic bound systems are tiny perturbations on the cosmic dS bath).

## Route A sub-route (ii): LOCAL CURVATURE replaces/augments the floor's Λ — COLLAPSES TO THE BANKED DENSITY NULL
If the floor tracks a LOCAL Ricci scalar instead of the background Λ: for matter, R_m = 8πGρ/c², so Λ_eff = (R_m+R_dS)/4
and a0_local = c²√(Λ_eff/32π) = (c/2)√(G(ρ+ρ_DE)) — **this IS the density law a0=(c/2)√(Gρ).** It boosts cluster-core
(~1e3 ρ_DE) by ~32x AND galaxy disk (~1e6 ρ_DE) by ~1000x → **breaks the 0.13-dex SPARC RAR.** This is the banked
DENSITY_A0 null R1, not a new escape. Worse: a POINTWISE curvature has NO smoothing scale, so it reads the highest local
ρ — the galaxy disk — even more aggressively than the density-ball. The Weyl/tidal (mean-interior-density) reading is
**wrong-differential**: MW mean-interior density (<8 kpc, ~3e5 ρ_DE) EXCEEDS cluster mean-interior (<R500, ~3e3 ρ_DE) by
~100x, so a tidal floor would boost galaxies MORE than clusters. No reading threads.

## Why no amplification rescues it
a0 ∝ T_floor LINEARLY — there is no power-law that amplifies the tiny Tolman factor. The local matter enters T_eff only
through 'a' (= g_bar), which is ALREADY counted in the Newtonian field; to move the FLOOR you must change the vacuum,
and the only two vacuum-change routes are (i) Tolman (~1e-5, derived but tiny) and (ii) local-Λ/curvature (= the density
null). The foundation closes both doors itself.

## Verdict (both ways — held to the 10x-harder bar for a "works" claim)
**CLOSED-FALSIFIER for the local-potential route.** The dS-Unruh foundation DOES license a local-potential dependence of
a0 (Tolman redshift of the floor, right-signed, zero new input) — so the answer to "does the foundation license ANY
dependence" is YES, honestly. But it DERIVES the scale as c² (relativistic), which makes the effect ~1e-5 in every bound
system: galaxies are safe trivially (nothing happens) and clusters get nothing (1.000025x vs the needed 2-25x). The only
way to get a large boost is to read the floor off local curvature/density — which IS the banked density-a0 null and
breaks SPARC. **No DERIVED in-window SPARC-safe scale exists on this route.** This is the sixth banked null on the
density/local-a0 front, and the cleanest: the foundation's own scale (c² for redshift, or the cosmic dS horizon for the
floor) is structurally too large/relativistic to single out the ~300-450 kpc cluster-core window.

*No manufactured cure: the right-sign Tolman effect is credited honestly, then shown to be 4-5 dex too small — DERIVED
but on the wrong scale, not tuned away. No high-priest dismissal: the route was given its full hearing (sign, magnitude,
amplification, both sub-routes, the tidal differential, the literature). Quarantine held: a0/Z never asserted derived;
the c² Tolman scale flagged DERIVED-but-wrong-magnitude, the density reading flagged = the banked tuned-scale null.*

## Source
Milgrom, "The modified dynamics as a vacuum effect," astro-ph/9805346 (Phys. Lett. A 253, 273) — the dS-Unruh
T=α√(a²+c²Λ/3), floor set by cosmological Λ, â₀=2c√(Λ/3), the a0 break = Unruh wavelength reaching the dS horizon.
