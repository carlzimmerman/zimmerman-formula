# The master map — the settled-state corpus, certified end to end

**File: `lean_certs/cert_master_settled_state.lean`** — 14 theorems,
compiles RC 0, **every theorem audited**: axioms =
{propext, Classical.choice, Quot.sound}, zero sorry, zero sorryAx.

This is the framework's closed algebra, in one file. It does not say the
theory is closed — it says exactly what IS closed, what is fitted, and
what is still open, so the honest boundary is machine-readable.

## The closed chain (certified, in dependency order)

| theorem | content | from |
|---|---|---|
| `kernel_occupancy_identity` | 1/(e^s−1) = e^{−s}/(1−e^{−s}) | T9 |
| `m_ph_closed_form` | M_ph(<r) = M_b/(e^s−1) | T9 |
| `deficit_stable_form` | (s/2)e^s/(e^s−1) = (s/2)/(1−e^{−s}) | T9 |
| `elasticity_annihilates_at_root` | s·e^s = 2(e^s−1) ⇒ ε(s) = 0 | T9 |
| `half_mass_at_log3` | M_ph/M_b = ½ at s = ln 3 | T9 |
| `kernel_half_coth` **(new)** | 1/(e^s−1) = ½(coth(s/2) − 1) — the ½-triple's exact algebraic face | master |
| `mu_ph_is_constant` | r²ρ_ph = √(GMa₀)/4πG uniform | T10 |
| `v4_from_uniform_mu` | v² = 4πGμ ⇒ v⁴ = GMa₀ | T10 |
| `supply_mass_exact` | M_ph = 5.36 M_b at s = ln(1+1/5.36) | T10 |
| `assembly_ratio_from_law` | t_c/t_g = ln(1−f_c)/ln(1−f_g) (Γ cancels) | T11 |
| `epoch_elasticity_closed` | ε(f) = (1−f)(−ln(1−f))/f | T12 |
| `sound_speed_fourth_power` | c² = v²/2 ⇒ c⁴ = GMa₀/4 | T13 |
| `sound_speed_sqrt` | √(GMa₀/4) = √(GMa₀)/2 | T13 |
| `jeans_square` | λ_J² = 2π²r² (λ_J = √2·π·r) | T13 |

The chains they weld into:

1. **The mass law is exact.** Deep phantom ρ ∝ 1/r² with the kernel
   (T5/T7) has zero flux leak; M_ph(<r) is the closed form; half-mass at
   ln 3·r_t; the ½-triple (κ = ε(0) = kernel-half) is a declared
   observation, its algebra now certified.
2. **The settled state is the uniform-μ state, and flat rotation is
   μ-constancy.** v⁴ = GMa₀ at the flat level; 5.36 M_b inside the
   supply radius (P3 machinery).
3. **The clock is a pure ratio.** Completeness ratios cancel Γ; the
   elasticity of completeness is a function of f alone.
4. **The phantom is barotropic, silent at 132.8/139.2 km/s, and
   Jeans-stable at every radius** — no phantom substructure, ever.

## The boundary (what the certificate does NOT claim)

- **κ = ½ is fitted**, not derived. The a₀ = κ·c·√(Gρ_Λ) scale and the
  ½ appear as a declared unification (kernel-half = ε(0) = κ), NOT as a
  theorem. The record's own rule: "κ = ½ stays fitted unless every step
  is forced with no inserted rational."
- **λ is convention-dependent** (sibling audit 983addaac accepted in
  T12's addendum): the three-clock λ agreement holds only under mixed
  definitions; one-definition b = 0 flooring shows factor 2.37
  divergence. λ universality is NOT currently forced.
- **No dark-matter particle.** The cold fluid is a separate component;
  its mass is still required. The no-substructure theorem covers the
  phantom only.
- **Limits ride the lanes.** ε(s) → ½ at s → 0 and all derivative /
  variance / statistical steps are computed in the lane scripts (the
  house pattern: calculus carries in the lane, algebra is certified).

## The master falsifier suite (everything above that is killable)

1. Any measured σ_ph ≠ (GMa₀)^{1/4}/√2 (MW satellites: ~110–125 vs
   132.8/139.2 km/s — live near-boundary test).
2. ~~Any pure-dark substructure observation.~~ **WITHDRAWN (2026-10-07):
   CFG344 requires the cold fluid to clump like CDM — dark subhalos are
   expected (cold-fluid structure); a detection constrains the cold
   fluid, not the phantom. The phantom-only statement stands.**
3. Any completeness sample whose σ(f)/[f·ε(f)] leaves 0.4–0.5 by >2σ,
   or whose σ(0.60)/σ(0.43) breaks the 1.146 fork (vs 1.0 null).
4. A flat-level galaxy whose v⁴ ≠ GMa₀ outside the systematics
   (the mass-law face). [T13's sound-speed item is NOT
   framework-distinguishing: c = (GM_b a₀)^{1/4}/√2 is the textbook-SIS
   value at the TF normalization — audit accepted.]
5. A λ measurement at one fixed assembly definition that forces a
   common λ across clocks — currently open, correctly so.
6. (falsifier of the BOOKKEEPING, not the framework) a completeness
   sample whose σ(f)/[f·ε(f)] leaves 0.4–0.5 by >2σ — same content
   as #3; numerics provisional until the level bias of the 0.43/0.60
   floor values is resolved.
5. A λ measurement at one fixed assembly definition that forces a
   common λ across clocks — currently open, correctly so.

## How to read the verdict

The framework's settled-state algebra — mass law, uniform-μ settling,
v⁴ = GMa₀, supply 5.36, clock ratios, elasticities, sound speed,
Jeans stability — is now a single machine-checked corpus: 14 theorems,
one file, zero sorry, three axioms, reproducing the per-lane
certificates (T9–T13) exactly. The theory's OUTER layer (κ, λ, the cold
fluid) remains honestly open, with its fitted/convention-bound status
printed in the same file's docstring.
## Addendum (2026-10-07): the cold profile is measured

The radial application of cert #14–16 to the published MW halo anchors
(T18) re-derived the knife-edge radially (|M_cold(30)|/M_b = 0.13,
V=188) and measured the cold component's profile: x_cold(100) = 0.28 →
x_cold(217) = 0.46, shape = the un-settled reservoir. Falsifier suite
extension: a cusping ρ_cold inside 50 kpc, or the 30-kpc cold
exceeding 0.3 M_b under V=188-consistent data, kills the inner
closure.
