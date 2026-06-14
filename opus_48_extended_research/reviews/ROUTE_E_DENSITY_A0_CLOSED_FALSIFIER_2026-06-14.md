# Route E (ADVERSARIAL / null_steelman): does the dS-Unruh FOUNDATION license a local-density a0, and what scale does it pick out? — VERDICT: CLOSED FALSIFIER (2026-06-14)

**Grade: CLOSED-FALSIFIER. The foundation does NOT license a local-matter-density floor; every framework-native
length is cosmological (Gpc), CMB-pinned (1 Mpc), or system-tracking (kills the RAR / self-normalizes), with a
2.2–660× gap to the 300–450 kpc cluster-core window; the equivalence principle structurally forbids a local-matter
floor; the SPARC environment null (10.5σ) already excludes the per-galaxy coupling.**

Code: `route_E_foundational_scale_enumeration.py` + `/tmp/route_E_additive_check.py`. Builds on the five banked nulls
(ELL_DESITTER_UNRUH_HORIZON, DENSITY_A0_RDE_CROSSOVER, DENSITY_A0_ELL_1MPC, cluster_dsunruh_floor_MI, the SPARC env
test). Literature re-fetched from primary sources (Luo 2026 arXiv:2602.14515; Milgrom 1999 astro-ph/9805346).

---

## The question (a DERIVATION question, not a candidate-ell scan)

The banked work established that the density-law `a0=(c/2)√(Gρ_local)` lands Tian 2020's ~17× cluster RAR scale to order
and flattens the raw deficit [1.55,7.66]→[0.75,1.30] with zero parameters (right-signed) — but only if a smoothing scale
ell makes the relevant ρ the cluster-MEAN (~Mpc) and NOT the galaxy-disk-local (~10⁵–10⁶ ρ_DE, which would erase the
0.13-dex SPARC RAR). Five DERIVED ells were tested and ALL fail. Route E goes to the FOUNDATION and asks the structural
question the ell-scan cannot: **does `T_eff=(ℏ/2πck_B)√(a²+(cH)²)`, with `a0↔Λ`, license ANY local-matter scale — and
if so what length does the foundation PICK OUT?** Route E is the adversarial both-ways guard: steelman the NEGATIVE.

## The derivation — the foundation references NO local-matter scale

**(1) The floor is the cosmological constant, uniform in space.** In `T_eff=(ℏ/2πck_B)√(a²+(cH)²)` the second argument
is `(cH)²` — a CURVATURE / horizon-acceleration scale, not a matter density. The literature is explicit and unanimous:
`a0=√(Λ/3)` (Milgrom 1999); Luo 2026 derives `a_bg=c²√(Λ/48)` "from uniform cosmological background acceleration, **not
local structures**," with the modified-inertia structure **additive**: `a_T = a_pr + a_bg` (his eq. 19), where `a_pr` is
the particle's OWN proper acceleration and `a_bg` is fixed by Λ. **The floor `a_bg` is the SAME number for a galaxy and a
cluster core** — verified numerically (`a_bg=1.355e-10`, uniform). The only thing that differs between environments is
`a_pr` (the local field strength), which sets WHERE on the interpolation a system sits — not the floor. So the
foundation gives the SHARED-MOND cluster deficit, NOT a density-driven boost.

**(2) The local hook exists ONLY via the Friedmann substitution — and it is curvature-illegitimate sub-horizon.** The
density reading arises by substituting `H²=(8πG/3)ρ` into the floor. Covariant test (sympy/numpy): the dS-Unruh floor is
the ISOTROPIC de Sitter Ricci `R_dS=4Λ` (a property of the vacuum). A local matter clump sources a TIDAL / Weyl /
Newtonian curvature. The ratio `R_matter/R_dS = 8πGρ/(4Λc²·...)` is ~0.37 at the cosmic mean (substitution legitimate →
`a0=(c/2)√(Gρ_crit)=1.13e-10`, the ρ_total footing), but **~700 in a cluster core and ~10⁵–10⁶ in a galaxy disk**. In
those regimes the local curvature is tidal/anisotropic and DWARFS the isotropic-dS floor — using `a0=(c/2)√(Gρ_core)`
substitutes the WRONG curvature object. The substitution is curvature-legitimate ONLY near `ρ~ρ_DE`, i.e. at `r_DE`,
which self-normalizes (banked).

**(3) The equivalence-principle obstruction (the deepest negative, literature-confirmed).** The dS-Unruh heat is felt by
a particle ACCELERATED relative to the cosmic vacuum. A star in a galaxy/cluster is in FREE FALL in the local field — by
the EP its frame is locally inertial and it feels NO local Unruh heat from local matter. The ONLY bath it cannot
free-fall out of is the cosmological de Sitter horizon (Λ is global; no frame removes it). **This is precisely WHY
`a0↔Λ` and not `a0↔ρ_local`:** local matter curvature is removable (no floor shift); dS/Λ curvature is irreducible (sets
the universal floor). Luo 2026 confirms: local gravity and the cosmological background are separate additive terms with
"no feedback from local mass to the floor," and "the known effects of deSitter background expansion on local
gravitational systems like galaxies seem negligible." **The foundation structurally forbids a local-matter floor.**

## The implied a0_local — the magnitudes (both ways)

| environment | ρ/ρ_DE | curvature R_m/R_dS | a0_local/a0 IF density-read | foundation licenses it? |
|---|---|---|---|---|
| galaxy disk (local) | 1e5–1e6 | 2.5e4–2.5e5 | **316×** (would kill RAR) | NO (EP-removed; tidal not dS) |
| cluster core (local) | 730 | 182 | **27×** (right magnitude for Tian 17×) | NO (EP-removed; tidal not dS) |
| cluster Mpc-ambient (tuned ell) | 30 | 7.5 | 5.5× | only at TUNED ~Mpc–10 Mpc ell |
| cosmic mean | 1 (ρ_crit) | 0.37 | 1.21× (UNIFORM, ρ_total footing) | YES — but uniform, no differential boost |
| dark-energy floor | — (ρ_DE) | 0.25 | 1.00× (the spine) | YES — the canonical a0 |

The density read gives the right cluster magnitude (27× vs Tian's 17×) at the local core density — but the SAME law gives
316× on a galaxy disk, and the foundation licenses NEITHER (EP-removed). The only foundation-licensed reading is the
cosmic-mean crossover, which is a UNIFORM 1.21× footing shift (applies to galaxies too) → η 2.15→~1.75, not 1.2–1.5.

## The enumeration — every framework-native length vs the 300–450 kpc window

| scale | value | lands in 300–450 kpc? |
|---|---|---|
| r_AH = c/H_local (dS apparent horizon) | ≥199 Mpc even at R500; 3.4 Gpc cosmic | NO — 440–660× too big |
| R* = c²/2a0 (free-fall length) | Gpc cosmic; 575 Mpc at R500 | NO — cosmological |
| 1/μ (AeST scalar Compton, CMB-pinned) | 1 Mpc fixed | NO — 2.2–3.3× too big; banked NULL |
| r_DE (level-set ρ̄=ρ_DE) | galaxy 275 kpc / cluster 7–26 Mpc | numerically near, but self-normalizes → 2ρ_DE, zero boost |
| Z-geometry modulus (32π/3) | dimensionless coupling | NO — sets no length |
| r_M = √(GM/a0) | galaxy ~9 kpc / cluster ~860 kpc | NO — tracks system → smooths disk → kills RAR |
| AeST kinetic scale | ~r_M, galaxy-internal 10–30 kpc | NO — galaxy-internal |

**The structural gap:** every derived scale is COSMOLOGICAL (horizon/Λ-set, Gpc), CMB-pinned (1 Mpc), or SYSTEM-tracking.
The smallest cosmic/CMB-pinned scale (1 Mpc) is 2.2–3.3× larger than the top of the cluster-core window (450 kpc), and
the horizon is ~660× larger. The only scales NEAR 300–450 kpc are system-tracking (r_M, r_DE), which either kill the RAR
(r_M smooths a galaxy over its own disk → a0 ~300× too big) or self-normalize (r_DE → 2ρ_DE universally, zero
differential boost). **Nothing in `a0↔Λ` — a cosmic vacuum property — references a local-MATTER scale at all.**

## The sign check

IF the floor responded to a shrinking local apparent horizon in an overdensity, `c/r_AH` would rise → larger floor →
LARGER a0 in clusters: **right-signed** for the cluster fix (and the local magnitude, 27× core, IS Tian's ballpark). But
(a) the foundation does not deliver this response (EP + additive structure, §3); (b) banked Route C found the
apparent-horizon local correction wrong-signed/null once the matter-era turnaround is handled correctly; (c) the
magnitude requires the LOCAL density, which the SPARC null kills. So the sign is right only in the inadmissible
local-clumpy reading — and that reading is excluded both by the foundation and by the galaxy data.

## The empirical nail

The framework's OWN SPARC environment test: `d log a0 / d log(1+δ) = +0.052 ± 0.043` vs the density-a0 prediction +0.5 →
**10.5σ exclusion** of the per-galaxy density coupling. Corroborated externally: Li et al. + 2026 A&A ("no credible
indication of variation in the critical acceleration scale"); Bilek 2026; the wrong-sign apparent horizon (Route C). The
per-galaxy local-density floor is DEAD on data, independent of the foundational argument.

## Derived vs tuned (ruthless)

Every in-window scale that "works" is SMUGGLED, not derived: the ~6–10 Mpc fixed ell that threads both (banked) is a
tuned input the dS-Unruh horizon does not supply; the 27× cluster-core boost rides the LOCAL density, which is the
inadmissible clumpy reading. The genuinely DERIVED scales (r_AH=Gpc, 1/μ=1 Mpc, r_DE=self-normalizing) all MISS the
window or produce no differential boost. **No new tuned input is hidden in this verdict — the verdict is that no derived
in-window SPARC-safe scale exists.** Quarantine held: a0/Z never asserted derived.

## Verdict — CLOSED FALSIFIER

**Density-a0 is a CLOSED FALSIFIER: a real, distinctive, falsifiable signature (a0_cluster > a0_field, right magnitude
~17–27×, right radial sign, zero-parameter raw-deficit flattening) that the framework's OWN dS-Unruh foundation does NOT
license and the SPARC data (10.5σ) already disfavors.** The foundation's floor is the irreducible cosmological-constant
curvature; the equivalence principle forbids it from responding to local matter; every framework-native length is
cosmological/CMB-pinned/system-tracking with a 2.2–660× gap to the cluster-core window; and the one curvature-legitimate
local reading (the ρ~ρ_DE crossover) self-normalizes to a uniform 1.21× footing shift that cannot differentially boost
clusters. This is the honest both-ways outcome: the distinctive density-a0 cluster lever is genuinely distinctive and
right-signed in magnitude, but it is NOT foundation-derived and is empirically excluded at the galaxy scale — so it
stands as a CLOSED, falsifiable prediction the framework does not own, not a delivered cure.

*Both ways: the right-signed zero-parameter flattening and the Tian-17×/cluster-27× magnitude coincidence are credited
at full weight (not dismissed); the EP obstruction, the curvature-character mismatch, the scale gap, and the 10.5σ SPARC
null are reported at full weight (not buried). No manufactured cure; no high-priest dismissal. Quarantine held.*

*Sources: Milgrom 1999 (astro-ph/9805346, the modified dynamics as a vacuum effect); Luo 2026 (arXiv:2602.14515, Local
Short-Time Acceleration / deSitter modified inertia, `a_bg=c²√(Λ/48)`, additive `a_T=a_pr+a_bg`, "negligible" local dS
effect); banked: ELL_DESITTER_UNRUH_HORIZON, DENSITY_A0_RDE_CROSSOVER, DENSITY_A0_ELL_1MPC, cluster_dsunruh_floor_MI,
CLUSTER_DENSITY_A0_SHAPE_RECONCILED, the SPARC A0_COSMICWEB_ENVIRONMENT null.*
