# CFG762 FROZEN CRITERIA: is there ONE c_P that lets P radiation export infall energy in every SPARC galaxy?

Date: 2026-10-13. Block CFG760–769. Committed ALONE before any CFG762 script or number. Written after CFG760/761, whose scaling
(c_P,max ∝ V/√s₀, c_P,min ∝ r) makes a CLOSED outcome expected; that expectation is stated here so the result is not read as a
surprise. κ = ½ FITTED; both footings, never pooled; the cold energy's mass is required; not "theory closed".

## Inputs (raw SPARC via CFG4_common, read-only; CFG760's CFG691_copy loader)
For each galaxy, its last measured radius R. Baryonic V_bar² at the CFG691 best Υ per footing (0.46 canonical / 0.42 alt);
M_b = V_bar²R/G (CFG691's convention). r_M = √(GM_b/a₀), y = (GM_b/R²)/a₀. Included iff y ≤ 1 (cubic-W regime, as CFG760);
the excluded count is reported.

## Quantities (most favourable to an open door)
- ℓ_γ = L*²/(2r_M), L* = 5.754 pc; s₀ = R/ℓ_γ; ω_g from CFG760's profile.
- Infall speed V = 2·V_obs(R); threshold x_e = 0.71 (CFG761's smallest measured value).
- c_P,max = V/(x_e ω_g(s₀) s₀) (export possible); c_P,min = R/13.8 Gyr (one crossing in a Hubble time).

## Test
- **D1. OPEN iff max over included galaxies of c_P,min ≤ min over included galaxies of c_P,max, for both footings**
  (a single c_P serves all). CLOSED otherwise.
- Reported: the number of galaxies whose own window [c_P,min, c_P,max] is non-empty; the gap factor max c_min/min c_max.

**MUTATE** (`CFG762_MUTATE=1`): no vacuum curvature, so ω_g → 0 and c_P,max = ∞. D1 must then be OPEN. Exit 1 iff it bites.

## Not tested
Non-spherical geometry, the region y > 1, export channels other than P radiation.
