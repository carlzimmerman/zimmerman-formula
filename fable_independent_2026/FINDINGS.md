# fable_independent_2026 — findings

Opened 2026-09-08, parallel to the lead agent's IC-series. Every number below comes
from a script in this directory with checks that can fail. Nothing here is committed
as a win that a check did not survive.

## L2 — the cluster inverse problem: what clusters need is not a kernel

`L2_cluster_inverse.py` (6 FAIL of 10; the FAILs are the finding).

Inverting the static law on the corrected X-COP profiles gives the boost that would
reproduce the observed cluster masses from the baryons exactly. It exists and is
well behaved: single-valued to 0.147 dex, monotone, so the stiffness stays positive.
It is **Δ_req ≈ 5.5 s^0.81**, i.e. J_Y ≈ 0.13–0.18 nearly constant, i.e. **g_obs ≈ 6.9 g_N**.

- Its log-slope, 0.81 ± 0.08, sits **3.9σ above the 1/2** that caps any kernel with a
  deep-MOND limit. A slope near 1 means gravity rescaled by a constant, i.e. extra
  mass tracing the baryons — not an interpolation function.
- It exceeds the widest bounded-boost ceiling of the kernel family by 2.9×.
- **The impossibility:** at the *same* accelerations, s = 0.09–0.65, clusters require
  **2.2–5.1× the boost galaxies are measured to have**; worst |z| = 13. The ratio is
  identical on both footings because a₀ cancels from a ratio of measured accelerations.
- Escapes priced and closed: nonthermal support needs σ₁D = 857 km/s, **5.2× Hitomi's**
  Perseus measurement; the minimal continuation to Solar-System accelerations puts
  2.75e-10 m/s² at Saturn, **3.9e4× the residual bound**.
- Controls: a synthetic set built from the carried kernel round-trips to 1.1e-16, and
  the carried kernel reproduces the known ~2× shortfall at 0.8 R500.

**No single-valued Δ(s) can serve galaxies and clusters.**

## L3 — the coefficient's last door: a split-degeneracy theorem

`L3_flux_quantisation.py` (5 FAIL of 10).

k04 reduced κ = ½ to one coupling ratio in the four-form promotion. Flux quantisation
cannot fix it, and the obstruction is structural.

- **Theorem.** The map β → μβ, Z → Z + 2bβ²(1−μ²) leaves invariant Z̃ = Z + 2bβ², the
  quantised flux q_n = ne/Z̃, the level spacing, ε, Λ, L_dS, the Brown–Teitelboim
  junction radius, the four-form boundary term and the Brown–York horizon energy —
  and sends κ → μκ. Quantisation constrains the **sum**; κ needs the **split**.
  Positivity of Z bounds κ only by b^(-1/2) = 7.45, a factor-15 window.
- Reason: quantisation constrains couplings to the potential (topological); β multiplies
  the field strength inside a nonlinear term, and a 2-brane in D = 4 has no magnetic
  partner to pair β with e.
- **The "8" is footing-dependent:** Z/β² = 2/κ² − 2b is 7.96 canonical, 5.48 alt (a 31%
  move), 9.39 for the horizon coefficient. Any principle returning exactly 8 would be
  reading one footing. *(This corrects how this result was stated on 2026-09-06.)*
- No integer works: implied flux number is 5e-62 at the Planck charge, 7e-4 at the
  neutrino scale; a Planckian charge overshoots ρ_Λ by 4.4e122 — the 10^120 appears as
  the Bousso–Polchinski problem, not as a derivation.
- Controls against published results: Duff–van Nieuwenhuizen sign, Bousso–Polchinski
  spectrum and shell count (J ≈ 100), Brown–Teitelboim junction condition.
- One genuine positive: the four-form boundary term **independently re-derives k04's
  Legendre sign fix**.
- Untested adjacent door, not claimed closed: a membrane whose charge or tension itself
  depends on a₀.

## L5 — can the cluster residual be a long-range force?

`L5_long_range_G.py` (3 FAIL of 5). The constructive reading of L2: a constant rescaling
of G at large radii and none at small radii is what a finite-range (Yukawa) force gives.

- **Shape passes.** A single (α, λ) reproduces the corrected enhancement over 40–1000 kpc
  to **0.064 dex rms**. The residual really does have the shape of a finite-range force.
- **But the fit wants λ = 14 kpc**, which is *inside* galaxies, and α = −0.891.
- **Galaxies kill it:** predicted RAR offsets of +0.36 dex at 10 kpc and **+0.96 dex at
  100 kpc**, against the relation's observed 0.11 dex scatter.
- **BBN kills it independently:** the same parameter that sets the cluster enhancement is
  the cosmological Newton constant, G_cosmo/G_local = R(∞) = **9.2**, raising the expansion
  rate at nucleosynthesis by 3.0× — **41× the conservative bound**. The two cannot be
  decoupled within a single fixed-strength force.
- Control: the fitter recovers injected (α, λ) exactly.
- Untested adjacent door, not claimed closed: a **screened/chameleon** force whose strength
  depends on local density or potential, where the cosmological and cluster values are
  decoupled by construction. That is a different model with a new free function.

## Standing after these three

The cluster residual is not a kernel (L2), not a fixed-strength long-range force (L5), and
the coefficient is not fixed by the geometric or boundary sector (L3). Combined with the
2026-09-06/07 dark-sector no-go and its 3D confirmation, what clusters demand — about seven
baryonic masses tracing the baryons — has no mechanism in or adjacent to this action, and
the one structure that reproduces its radial shape is excluded twice over.

## L4 — independent verification of the lead's IC7

`L4_verify_ic7.py` + `L4_VERIFICATION.md` (1 FAIL of 24). The lane rebuilt the lead's
Hamiltonian and curvature coefficient by hand from IC4/IC5/TENSOR_BALANCE and
differentiated independently — no import, no reuse of its algebra.

**Everything the lead computed reproduces.** The boxed obstruction
S₄′(1) = −e^{5/6}(5T−27)(8T−27)(8T+27)/(18T²(4T−27)) = **−11.1407711251147987**, matching
to 18 digits; det(M\*) = −4T²h₀²/81; c₇(j=1.007) = 0.00235189114143216; the 18-digit
sheared state; the constraint-algebra matrices K and Ω₁₂ and the Dirac singular values;
IC7's own leftover S4₁₁ + 32c₇ = 0.0151964888331. No contradiction anywhere. IC7's claim
that c₇ is built from action derivatives alone — "neither measured eigenvalues nor a
desired wave speed define it" — is **confirmed as written**, and the cutoff correctly
excludes det M = 0 (the singular point is exactly the static branch ρ = 0, where θ = 0).
Controls: the same machinery returns the GR DeWitt supermetric λ = 1, c_T² = 1 for ADM
GR, and a DOF count of 2 for ADM GR.

**Three things the files understate.**
1. **The degree-of-freedom count is 3, not 2.** In unitary clock gauge: 8 canonical pairs
   (6 barred-metric + ξ + u) = 16, minus 4 second-class auxiliary constraints, minus 2×3
   first-class spatial-momentum constraints, giving (16−4−6)/2 = **3**: two tensor
   polarisations plus one propagating scalar. The lapse carries a second-class constraint
   rather than acting as a Lagrange multiplier, so there is no local first-class
   Hamiltonian constraint. The scalar is **healthy** — reduced kinetic Hessian A₀ = 0.46 > 0,
   no ghost, c_s² = 1/3 — and DeWitt λ = 1 identifies it as a khronon-type mode, not a
   Hořava λ-mode. IC7 does not change the count: c₇R̄² carries no time derivative.
2. **The repair window is narrow.** The θ ≡ 1 plateau ends at j = 1.0736 and closes at
   j = 1.1316, where the unrepaired S₄ = −0.734 returns in full while η is still 1. The
   repair covers |j−1| < 0.074 of the isotropic family, not the family.
3. **A new liability, quantified.** On any background with barred spatial curvature
   R̄₀ ≠ 0, the IC7 term detunes the tensor cone exactly: **c_T² = 1 − 4c₇R̄₀/c**, with
   4c₇/c = 0.00857 per unit R̄₀. IC6's exact tensor luminality was a cancellation that
   IC7 breaks off flat backgrounds; the lead notes the non-transfer qualitatively, this
   is its size.

**How to read the count fairly.** The lead's own requirement allows a genuine clock mode
provided it is separately identified, counted and shown healthy. This mode is all three.
So the honest statement is not that IC7 is wrong but that the chassis propagates a khronon,
and the programme must now either accept it as the allowed clock mode or remove it.
If accepted, the next gate is its preferred-frame phenomenology — and this repository
already has a pincer there: g03v's α₂ = −c₁₄/2 + c₁₄²/(2c₂) with |α₂| < 4×10⁻⁷, and
g03w's clock-tachyon pincer between PPN (c₁₄ ≲ 10⁻⁵) and stability (c₁₄ ~ 1). That is the
connection worth handing to the lead.

## L6 — the screened-force door: closed

`L6_screened_force.py` (5 FAIL of 6). L5 left this door open explicitly: a chameleon,
symmetron or Vainshtein-type force whose strength depends on a local variable, so that the
cluster and cosmological values are decoupled by construction. It is the last structural
candidate for the cluster residual. A screening mechanism is operationally a monotone
function S(X) of one local variable, so it dies two ways.

**Overlap.** Where clusters and SPARC galaxies occupy the same X but need different
enhancement, no single-valued S(X) exists. Enhancement here is what a screened force must
add *on top of* the framework's kernel, E = g_obs/[g_bar + a₀Δ(g_bar/a₀)].

| screening variable X | cluster/galaxy overlap | worst z |
|---|---|---|
| acceleration g_bar (control — this *is* a kernel, must fail) | 100% | 25.0 |
| potential Φ_loc = g_bar·r (chameleon, symmetron) | 47% | 17.7 |
| baryon density ρ_b (density-dependent coupling) | **100%** | 12.8 |
| enclosed mass M_b(<r) (Vainshtein-like) | 11% | 7.9 |

The density row is the decisive one: clusters and galaxies overlap **completely** in baryon
density and require enhancements differing at 12.8σ. The spherical-equivalent density used
for SPARC understates a disc's true density, so correcting it separates the populations
further and cannot merge them.

**The cosmological ordering — independent of which variable is screened, and of overlap.**
The homogeneous background lies beyond cluster outskirts in every candidate variable:
baryon density 1057× lower, and both the local potential and the acceleration go to zero
by homogeneity. So any monotone S that unscreens clusters relative to galaxies unscreens
the *background* at least as much, forcing G_cosmo/G_local ≥ E(cluster outskirts) = 1.82,
which is 4× the conservative BBN bound. This reaches L5's kill without assuming a range.

Control: the machinery reproduces L2's kill in acceleration bins at |z| = 25.

**Untested, stated rather than closed:** (i) a *time-dependent* transition — a field that
rolls late — evades the ordering argument because the background value at nucleosynthesis
and today differ; that is a cosmological history rather than screening, and it must then
face the CMB and the growth of structure. (ii) A non-monotone S, or S of two variables at
once, is a fitted function rather than a screening mechanism.

## Standing after L2, L3, L5, L6

For the cluster residual — about seven baryonic masses tracing the baryons — the following
are now closed on this programme's own gates: an interpolation kernel (L2), a fixed-strength
finite-range force (L5), and a screened force in potential, density or mass (L6). Together
with the 2026-09-06/07 dark-sector no-go and its 3D confirmation, no mechanism in or adjacent
to this action supplies it. The coefficient's geometric/boundary door is closed too (L3).
