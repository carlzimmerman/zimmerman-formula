# mi_closure_pin — Lane consequences of the off-circular pullback + the Ostrogradsky fix

**Date:** 2026-07-16. **Framework:** de Sitter–Unruh **MODIFIED INERTIA** (Carl Zimmerman), judged on
its own terms: own interpolation ν(y)=√(1+1/y), μ(x)=(√(1+4x²)−1)/(2x)=K(x²), horizon-derived
a₀=cH_Λ/Z. **Both footings carried:** canonical a₀=9.36×10⁻¹¹ (ρ_DE, cH_Λ/Z), alt a₀=1.13×10⁻¹⁰
(ρ_tot/cH₀). Sign s=−1 and a₀'s value remain **POSTULATES** (untouched by this lane).

**Scripts (all exit 0, no hard-coded verdict booleans; reproduce with `python3 <name>.py`):**

| script | checks | verdict |
|---|---|---|
| `ostro_nonlocal_verify.py` | 13/13 | nonlocal disformal B is **ghost-free** (genuinely; controls fire) |
| `rider_a_offcircular.py` | 8/8 | off-circular dynamics offset **STILL A BRACKET** (sign free; anisotropy slope forced) |
| `rider_b_lensing.py` | 6/6 | off-spherical lensing **BRACKETED** (inherits Gap A through B[K]) |
| `rider_c_planetary.py` | 8/8 | clean a₀/2 solar-system evasion **NOT FORCED** — tension SURVIVES |

---

## 0. The pullback input (established upstream, this lane's premise)

The off-circular dS-Unruh Wightman pole **stays at/above κ=H_Λ** for every eccentricity, every
anisotropy, and — the decisive crux — **every reduction weighting**: κ_eff=√(H_Λ²+(a/c)²) ≥ H_Λ, with
equality only in the a→0 geodesic/deep-MOND limit. Orbital AC content is a comb at n·ω_orbit ≫ H_Λ, so
nothing lands in the (0,H_Λ) amplitude-MOND band. Because the pole is ≥ H_Λ for **all** weightings, the
pullback **cannot select one** → the reduction-weighting function **η(β) is NOT pinned. FREEDOM STANDS**
(the SPEC's honest prior "likely stays free" is confirmed by direct computation, reported straight as a
NULL — verified as rigorously as a win). κ_eff/H_Λ = 1.01481 at a=a₀ identically, footing-independent.

Everything below is the **downstream** status of the three riders given this NULL, plus the
load-bearing Ostrogradsky fix.

---

## 1. Rider (a) — off-circular dynamics: STILL A BRACKET (not a forced number)

**Verdict: the dSph / dispersion RAR offset is a BRACKET, its overall sign FREE; only the anisotropy
derivative is forced.** `rider_a_offcircular.py`, built on the validated rb3 Plummer machinery.

- **Lower endpoint — closure A** (instantaneous |a|): dispersion systems sit **exactly** on the
  rotation RAR, offset **0.000 dex** (pointwise inversion to 5×10⁻¹⁴ over 6 decades). Identical to
  MG-with-same-ν in spherical symmetry.
- **Sign is NOT pinned by the pullback.** Two admissible orbit-shape populations of the *identical*
  |a| history give **opposite-sign** offsets: apocentre-dominated **tangential** orbits sit **below**
  the RAR (negative), pericentre-dominated **radial/plunging** orbits run **above** it (positive — the
  kinetic pump; sign flip confirmed at e≈0.62). The concave-RAR Jensen gap is weighting-dependent, and
  that weighting **is** the free η(β). → the offset is a bracket spanning 0.
- **What IS forced (pullback-independent):** d(offset)/d(radial-anisotropy) **> 0** — radially-biased
  systems run hotter (Spearman ρ(e, offset)=+0.86, monotone). **MG-with-same-ν gives exactly 0 AND
  zero anisotropy dependence** for an isolated spherical system → this differential is **MG-impossible**
  (the clean discriminator).
- **Bracket magnitude, both footings:** isotropic-ensemble deep-regime mean ≈ **−0.024 dex**
  (canonical) / **−0.025 dex** (alt), 16–84% ≈ [−0.05, 0.00] dex, footing-stable (spread ~few % at
  N=500), with a positive radial tail. *(Deep-regime toy magnitudes are illustrative; the signed
  pattern and the forced anisotropy slope are the physics, not the exact dex.)*

**Honest ceiling:** off-circular predictivity carries **one free reduction-weighting function η(β)** on
the 2-D (eccentricity × anisotropy) orbit-shape space — overall-offset **sign free**, magnitude
bracketed [0 … closure-B pattern], **only the anisotropy slope forced**.

---

## 2. Rider (b) — off-spherical lensing: BRACKETED (inherits Gap A through B[K])

**Verdict: off-spherical lensing is a BRACKET of the same origin and O(10%) width as the dynamics —
it inherits Gap A; it adds no new gap.** `rider_b_lensing.py`.

- **Spherical/circular: the bracket CLOSES.** curl(ν g_bar)=0 identically (sympy, exact) → a local
  disformal B is an exact lensing potential → **dynamics-RAR = lensing-RAR exactly**. Forced there.
- **Off-spherical: local B fails.** For a binary, curl(ν g_bar) is **order-unity nonzero** (ratio
  0.13 to the field) → the lensing B must be the **nonlocal AQUAL (curl-free) potential**, which is a
  *different* reduction of the same operator than the algebraic first-moment (dynamical) field.
- **The bracket, quantified:** a scalar lensing potential (closure B) sources **zero** lensing
  B-mode/curl by construction; the algebraic closure-A field carries a **transverse (B-mode) fraction
  ≈ 8%** of the field for a 2:1 flattened mass (both footings). That transverse part **is** the
  inherited Gap-A ambiguity — it decreases monotonically toward the grid floor as the config becomes
  spherical (11.2% at q=0.4 → ~3% floor at q=1). The B-mode is itself MG-impossible for a pure scalar
  potential.

**Honest ceiling:** since the pullback left η(β) free, the off-spherical lensing prediction is a
**bracket of the same O(10%) width** as the dynamics, closable only by the same undone pin (or an
empirical proxy). c_T=1 (graviton on g) is untouched — the disformal B u u has no TT part.

---

## 3. Rider (c) — the planetary a₀/2 tension: clean evasion NOT FORCED (tension SURVIVES)

**Verdict: with the corner forced to a₀ (field-theory lane) and η(β) free (pullback), the clean
solar-system a₀/2 evasion is NOT forced — it still requires a free choice. Reported straight as the
honest finding.** `rider_c_planetary.py`.

**[1] Reading A (the reduction that carries the galactic RAR) reproduces the a₀/2 tail at full
strength** — a constant sunward a₀/2 = 4.68×10⁻¹¹ (canon) / 5.65×10⁻¹¹ (alt) m/s² at every planet.
Recomputed exclusion vs the cited INPOP/EPM per-planet δg bounds:

| planet | δg bound [m/s²] | excl (canon) | excl (alt) |
|---|---|---|---|
| Mercury | 4.6×10⁻¹⁴ | 1017× | 1228× |
| Venus | 8.0×10⁻¹⁴ | 585× | 706× |
| Earth | 8.7×10⁻¹⁵ | 5379× | 6494× |
| **Mars** | **1.4×10⁻¹⁵** | **33429×** | **40357×** |
| Jupiter | 5.6×10⁻¹³ | 84× | 101× |
| Saturn | 7.0×10⁻¹⁵ | 6686× | 8071× |

The tail is **not absorbable into a GM rescaling** (nonzero linear-in-A perihelion precession; ref
`vfy_kernel_planets.py` V2). So the RAR-carrying reduction is dead at planets by 10²–10⁴×, both footings.

**[2] The action forces the corner to the wrong place.** CLOSURE_MAP item (d): descent from S forces
the memory corner to the **action scale**, ω_c=a₀/2c = 1.56×10⁻¹⁹ rad/s, τ_mem=2c/a₀ = **203 Gyr**
(canon) / 168 Gyr (alt). The Reading-C planetary window (reactive + drift + RAR-floor,
KERNEL_PLANETS §6) is ω_c ∈ [9×10⁻¹⁵, 2.2×10⁻¹⁴] rad/s = **~Myr**. The action-forced corner is
**10⁴·⁸ (≈5 orders) below** the window.

**[3] One Lorentzian memory gate cannot sit at the action scale AND thread the planets.** A viable
corner must satisfy ω_gal ≪ ω_c ≪ ω_planet. At the **action-forced corner** the galactic MOND boost
retained is L_c(ω_gal/ω_c) = **2.9×10⁻⁸** → **RAR-dead at galaxies** (it suppresses the tail but also
kills the rotation curves). Only the **free ~Myr corner** threads both: galactic retained 0.996 (RAR
OK) and planetary tail suppressed ~10¹¹× (clears every per-planet bound, both footings).

**[4] Therefore the clean evasion is NOT forced.** The action's own corner is RAR-dead; the
planet-threading corner is a **free ~Myr choice** that neither the action's corner-forcing (which
points at 203 Gyr) nor the pullback (η free) supplies. The RAR-preserving survivor remains the **gated
Reading C with a free corner** — a falsifiable, two-sided-open **conditional** pass, **not** a forced
suppression. **The a₀/2 tension SURVIVES** in exactly this sense.

**Honest ceiling:** at planetary accelerations (10⁴–10⁸ a₀) GR and healthy MOND-family theories both
predict ≈0; these numbers discriminate **among the framework's own doors only, never vs ΛCDM**.

---

## 4. The load-bearing Ostrogradsky fix (was tautological at `unification.py:161`)

`unification.py:161` guarded the nonlocal-B Ostrogradsky-freedom with `True is (a_proxy.has(Derivative))`
— tautological (a_proxy was *defined* as a Derivative), verifying nothing; it was removed and left
ASSERTED. **`ostro_nonlocal_verify.py` does the check for real** (13/13, no hard-coded pass booleans;
every verdict read off a Hessian / a sign / a numerically-computed spectral density).

- **T1 — photon sector.** g~=η+B u u: computed det g~=B−1 and the electric Hessian H=1/√(1−B). For
  the physical 0≤B<1 window g~ is Lorentzian and the Hessian positive-definite → **photon not a ghost**.
  The causal bound **B<1 emerges from the Hessian** (at B≥1 the signature/kinetic is lost), not assumed.
- **T2 — nonlocal frame sector (the real question).** Represented (1−K)(□_u) by its **exact Herglotz
  spectral form** ∫dμ(t)/(|t|+□_u). Computed the density ρ(t)=+(1/π)Im K(−t+i0) numerically on **both
  cut regions** (region A t∈(0,¼) from the √z cut; region B t>¼): **ρ(t) ≥ 0 everywhere** (measure
  positive), **sum rule ∫dμ/|t| = 1.00000** = region A 0.363 + region B 2/π=0.637, and ρ→0 as t→0
  (no massless pole). The auxiliary Lagrangian's **Ostrogradsky Hessian ∂²L/∂χ̈² = 0** (χ̈ enters
  linearly → no nondegenerate higher-derivative momentum) and its **kinetic Hessian = 2 dμ(t) > 0**
  with mass²=t a₀² > 0. → a tower of **healthy massive scalars, NOT an Ostrogradsky ghost**.
- **T3 — controls proving the test is not vacuous.** The same machinery **flags** the textbook
  L=½q̈² ghost (Hessian=1≠0) and a Herglotz-violating **negative-measure** kernel (kinetic coeff<0),
  and **passes** a healthy Klein–Gordon field. So the T2 positivity check is load-bearing, not
  decorative.

**Verdict: the nonlocal disformal photon coupling S_photon[g~=g+B(a)uu], with B carrying the nonlocal
K(□_u/a₀²), is GHOST-FREE — genuinely, machine-checked, not asserted.**

**Honest caveat (stated, not hidden):** the auxiliary modes are healthy but their spectral weight peaks
at mass ~ a₀ (Compton/memory time ~c/a₀ ≈ 84–101 Gyr, super-Hubble); on all sub-Hubble scales they
reduce to the elliptic (spatial ∇⁻²) AQUAL constraint, consistent with the passive-frame "0 accessible
propagating dof" picture. Ghost-freedom is the machine-checked claim here; c_T=1 (graviton on g) is
untouched.

---

## 5. Ledger — what this lane changed

| # | Statement | Status |
|---|---|---|
| K-1 | Off-circular pole ≥ H_Λ for all weightings → η(β) free | **NULL, confirmed** (input) |
| A-1 | dSph/dispersion offset is a **bracket** (sign free), closure A = 0 dex | **DERIVED** |
| A-2 | d(offset)/d(radial-anisotropy) > 0 — **MG-impossible** discriminator | **DERIVED, forced** |
| B-1 | Off-spherical lensing **inherits Gap A** through B[K]; ~8% B-mode bracket | **DERIVED, bracketed** |
| B-2 | Spherical: dynamics-RAR = lensing-RAR exactly (curl=0) | **DERIVED, forced** |
| C-1 | Reading A reproduces a₀/2 tail; excluded 10²–10⁴× per planet, both footings | **DERIVED** |
| C-2 | Action-forced corner (a₀/2c, ~200 Gyr) is RAR-dead at galaxies | **DERIVED** |
| C-3 | Clean a₀/2 evasion **NOT forced** — needs a free ~Myr corner; tension survives | **DERIVED, NULL** |
| O-1 | Nonlocal disformal B is **ghost-free** (Herglotz-positive auxiliary tower) | **DERIVED, machine-checked** |
| P-1 | s=−1, a₀'s value | **POSTULATE** (untouched) |

**Bottom line.** The pullback NULL propagates cleanly: the off-circular **dynamics offset stays a
bracket** (sign free, anisotropy-slope forced and MG-impossible), the **off-spherical lensing inherits
that same bracket**, and the **planetary a₀/2 evasion is not forced** — the RAR-preserving survivor is
still the gated Reading C with a free corner that neither the action nor the pullback pins. The one
load-bearing hard-coded check (nonlocal-B Ostrogradsky-freedom) is now a genuine, discriminating
verification: **ghost-free**. This lane discriminates only among the framework's own closures; it
prefers neither the framework nor ΛCDM and introduces no new number. Both footings throughout; s=−1 and
a₀'s value remain postulates; c_T=1 and Cassini respected; no "theory complete/closed/proved" language.

*Sources read (frozen read-only repo cited file:line where load-bearing): `prep_2026/mi_field_theory/`
CLOSURE_MAP.md, UNIFICATION.md, `unification.py:139-169` (the fixed tautology); `prep_2026/mi_fingerprint/`
rb3_eccentric_offset.py; `prep_2026/planetary_doors/` KERNEL_PLANETS.md §6, BOUNDS.md §1.2 (per-planet
δg). All new work in `prep_2026/mi_closure_pin/` only; the frozen repo was not modified.*
