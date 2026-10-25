# DW1_dwarf_core_flattening — FROZEN CRITERIA (committed alone, before any script or graded number)

Written 2026-10-25 at the owner's request: "Test whether the core law can flatten below ~20 km/s for a stated physical
reason (e.g. the self-interaction rate saturating, rate x age >> 1) without breaking OS1's SPARC + cluster result."
κ = ½ FITTED. Footings canonical / alt, scored separately, never pooled. Cold dark energy (not matter, never a particle).
Nothing here says the data favour the framework or ΛCDM. Not "theory closed".

## 0. Starting point

OS1 (71873e76d3): Σ_i = Σ_a0 (σ_i/σ_ref)^q, with q_f = 0.892 / 0.748 calibrated on SPARC alone and σ_ref = 70.50 km/s.
This passes SPARC and 14/15 cluster cells, but dwarfs EXCLUDE (65% / 48%). The coupling is fully fixed by the anchor:
from LN1 T7, the self-interaction rate per density is s·v = K σ^(1−n), with K = 9 σ_ref^(1+n) / (4πG t Σ_a0²),
n = 2q − 1 and t = 13.8 Gyr.

## 1. Mechanisms screened analytically (reported as derived screens; no data enter)

**M1, rate saturation through the short-mean-free-path regime.** Heat conduction switches from ∝ s (long mean free
path) to ∝ 1/s (short mean free path) when the Knudsen number Kn = λ/H < 1, with λ = 1/(ρ s) and H = σ/√(4πGρ). At the
core law's own core (Γt = 1), using v = (4/√π) σ:

  Kn² = (16 / 9π) (2 a₀ t)² σ^(n−1) / σ_ref^(1+n),  i.e.  Kn = Kn_ref (σ/σ_ref)^(q−1),  Kn_ref = (4 / (3√π)) · 2a₀t / σ_ref.

Pre-computed before freezing (disclosed): Kn_ref ≈ 870 (canonical) / 1051 (alt). The script reports Kn at σ = 5 km/s
and 1000 km/s. **Rule:** M1 can flatten dwarfs only if Kn < 1 at dwarf σ.

**M2, gravothermal core collapse** (rate × age ≫ 1). In the core law, every core sits at Γt = 1 by construction, so the
collapse parameter is the same for every system, and nothing singles out σ < 20 km/s. This is reported as a structural
statement: RULED OUT within this law. A collapse lane would need a different core condition, which is a new law.

## 2. The graded test: M3, the law's σ is the halo's own dispersion

SPARC uses V_last/√2 (flat-part rotation) and clusters use √(kT/0.6 m_p). Both are halo-scale dispersions. OS1 gave
dwarfs their **stellar** σ, measured deep inside the core. M3 applies the law's own variable consistently, with no new
constant. For each dwarf:

- the halo is a Burkert at Σ(σ_h) = Σ_a0 (σ_h/σ_ref)^q_f with core radius r₀;
- σ_h = V_max/√2 of that halo, where V_max² = π G Σ r₀ · m₁ and m₁ = max_x Bk(x)/x = 0.860619;
- so σ_h solves σ_h^(2−q) = π G Σ_a0 σ_ref^(−q) r₀ m₁ / 2 (unique for q < 2).

The dwarf's halo-consistent cap is g_cap,i = max over r₀ of π G Σ(σ_h(r₀)) Bk(r₁₂/r₀) (r₀/r₁₂)², over r₀ from 1 pc to
1 Mpc on a log grid (4001 points) with a local refine. S_i and z_i are then computed exactly as in CD1/OS1, using X1's
binary-corrected Δ[Newton], g_h,req = g_obs − g_N, and sd_h.

| class (per footing; the verdict needs both footings to agree, else UNDECIDED) | rule |
|---|---|
| M3 RESCUES DWARFS | CONSISTENT: < 5% of dwarfs at z ≥ 2 and median S ≤ 1 |
| M3 PARTIAL | not CONSISTENT and < 25% at z ≥ 2 |
| M3 FAILS | ≥ 25% at z ≥ 2 |

**SPARC and clusters are unchanged by construction** (M3 only changes how dwarf σ is defined), so OS1's results stand.
This is stated, not regraded.

Reported only:
- grades by X1 class;
- σ_h/σ★ at the maximising r₀;
- the maximising r₀ and its halo V_max;
- whether that r₀ is physically plausible (r₀ ≥ r₁₂/3 and the halo mass M(<10 r₀) ≤ 10¹¹ M☉).

## 3. Checks

- **K0** With σ_h replaced by the stellar σ (OS1's rule), the dwarf class and fractions equal OS1's (65.2% / 48.3%) to 0.001.
- **K1** m₁ from a grid equals the brentq root of d/dx(Bk/x) = 0 to 1e-6.
- **K2** The σ_h solve returns V_max/√2 of its own halo to 1e-8.
- **MUTATE=1** (separate outputs): replace σ_h by σ_ref for every dwarf (Σ = Σ_a0, i.e. CD1's ceiling). The result must
  equal CD1's (fraction 0.011, median S 0.53 / 0.44), because a fixed Σ_a0 halo's cap is CD1's. Exit 1 if so.

## 4. Disclosed

- **Hand estimate.** A dwarf needs σ_h/σ★ ≈ S^(1/q) to clear its OS1 shortfall, about 5.8 (canonical) / 3.8 (alt) at the
  median, so σ_h ≈ 30–50 km/s. Larger r₀ raise σ_h but lower the pull at r₁₂, so the maximum may still fall short.
  FAILS or PARTIAL is a plausible outcome.
- SPARC's V_last/√2 includes baryons. The dwarfs' σ_h is halo-only. This small definitional mismatch is disclosed.
- The inner cluster over-prediction (OS1 INNER M-all) is not addressed here.
