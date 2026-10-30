# X77_direct_core_surface_density: FROZEN CRITERIA (committed alone, before any script or number)

**Idea.** Route E's grader uses only ρ₀r₀ = η Σ_coll (r₀ is then solved from the halo mass). c_f enters only through
X43's map η = (4/(3B(1))) c_f^{5/4}, which assumes the infall law M ∝ r^{0.75} inside r_f. The zooms' c_f (an r₋₂
crossing or an NFW fit) is pushed through that map. Both steps are assumptions. The native object is the zoom halo
itself. So measure the quantity the grader uses directly: fit the grader's own shape to each native halo and read off
ρ₀r₀. No c_f and no infall law.

**Measurement (per finished X48 snapshot, all grids and masses on disk; no A4 run is read until it finishes):**
- Centre, r_vir (18π² ρ_m(z_f)), r_conv and the fit range [r_conv, r_vir]: X48's `measure()` unchanged.
- Objective: X48's NFW-fit objective unchanged (squared log residual of M(<r)/M(<r_vir)), with the smooth-core shape
  M_S(<r) ∝ asinh(x) − x/√(1+x²), x = r/r₀, in place of NFW. One parameter a = r_vir/r₀, grid 0.5–60 (2001 log steps).
- **η_native ≡ ρ₀r₀ / (Δ ρ_m(z_f) r_vir) = (4/3) a² / B_S(a)**, with B_S(x) = 4[asinh x − x/√(1+x²)] and Δ = 18π².
  This is exact given the fit, because ρ₀ is set by M(<r_vir).
- Burkert is also reported, with its own B(x) and X43's 14.83 as the comparison value.

**Reference values (from committed lanes, not tuned here):**
- X73 / X74 pass at c_f = 4, which is η_S = 10.82.
- The pre-read brackets put the pass limit at c_f ≈ 7 at 1e12, so η_S ≈ 21.2 (SPARC Υ floor).
- The probe put it at c_f ≈ 5 at clusters, so η_S ≈ 14.3 (G-IN-Mall).

**Grade (smooth core, per mass; nine-seed median, 68 % bootstrap with 10 000 resamples, seed 20261026):**
- **NATIVE INSIDE WINDOW:**
  - at 1e12, the median η_native ≤ 21.2;
  - at each cluster mass, the median is ≤ 14.3.
- **NATIVE OVER:** a median above its limit. Say by what factor.
- **Resolution:** at 1e12, compare ng 48 against ng 64. A shift above 20 % carries [RESOLUTION-DEPENDENT].
  - 1e13 and 1e14 exist only at ng 48 until A4 finishes, so they carry [ng 48].

**Checks:**
- **K1:** the synthetic NFW with c = 4 from X48's K3 is fitted, and η_native is printed. A synthetic smooth core with
  a = 6 must be recovered within 5 %.
- **K2:** the formula η_native(a) matches direct numerical integration of ρ₀r₀ to 1e-10.
- **MUTATE:** shrink every radius inside r_vir/4 by a factor of 0.8 (a more concentrated core). η_native must rise.

**Reported only:**
- η_native computed with the rule's r_f (from M_f) in place of the measured r_vir;
- what an "η-equivalent c_f" would be, i.e. solving 10.82 (c/4)^{1.25} = η_native.

κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating
field component, never a particle. The zooms are collisionless cold collapse of an isolated constrained peak. The
floor physics is not in them, so this tests the collapse branch only.
