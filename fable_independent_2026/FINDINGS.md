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

## L7 — the decisive diagnostic: the cluster residual IS the cosmic dark-to-baryon share

`L7_cosmic_ratio.py` (3 FAIL of 6). With every mechanism closed (L2, L5, L6 and the
2026-09-06/07 dark-sector no-go), one question becomes decisive and had not been asked in
this form: is the required source quantitatively the *cosmic* ratio? It is.

At the outermost audited radius (1000 kpc, 0.80 R500), across all twelve X-COP clusters:

| quantity | measured | expectation |
|---|---|---|
| baryon fraction f_bar | **0.149** [0.115, 0.160] | cosmic Ω_b/Ω_m = 0.156 |
| Newtonian M_dark/M_bar | **5.73 ± 0.68 (12% scatter)** | cosmic Ω_dm/Ω_b = **5.43** |
| framework M_resid/M_bar | 2.76 (alt) / 3.09 (canonical) | framework predicts **0** |

- **R1 PASS, R2 PASS.** The Newtonian reading matches the cosmic ratio to 5% and is
  universal across clusters to 12%. Clusters retain essentially the cosmic baryon fraction.
- **R3 FAIL.** The framework's residual after its own kernel is 2.8–3.1 baryonic masses,
  **13–15σ from the zero it predicts**.
- **R4 FAIL.** That residual *decreases* with radius at −1.9 per dex, which is what
  "constant cosmic dark ratio minus a kernel boost that grows outward" looks like — the
  signature of a kernel adding spurious support, not of a missing mass.
- Control R0: the reconstructed baryon fraction lands in the observed cluster range.

**Reading it honestly.** This does not measure dark matter and does not touch the galaxy
evidence, where baryons plus the kernel work at 0.108 dex and a cosmic-share halo would
overshoot badly (g04k: 2.6 M_b inside 10 kpc against the 0.25 M_b the RAR tolerates). What
it shows is that the number clusters ask for is one ΛCDM fixes independently, from the CMB
and BBN, rather than fits — while the framework must supply it from a mechanism that six
independent lanes have now failed to find.

## The programme's central problem, stated as sharply as the data allow

- **Clusters** say: cosmic dark-to-baryon share, universal to 12%, exactly the ΛCDM number.
- **Galaxies** say: baryons plus the kernel, with no room for that share — a cosmic halo
  overshoots the rotation curves by an order of magnitude.

Both cannot be simply true, and this is the classical MOND-plus-halos tension, not a defect
peculiar to this action. What survives either resolution is the programme's distinctive and
independently testable content: the tie a₀ = κ c√(Gρ_Λ) with κ fitted, and the two
pre-registered measurements (Gaia DR4's two arms, the deep-MOND Tully–Fisher zero point at
z ≈ 2.5).

## L1 — the caustics lane: my own load-bearing number, corrected

`L1_caustics_and_cap.py` (3 FAIL of 12). This lane attacked the number every other verdict
rests on, using the two best objections to it: g04k's dust self-gravity was a **monopole**,
which is radial by construction and smooths over exactly the caustics cold collisionless
infall forms; and its MOND multiplier **lost the acceleration cap** where the internal and
external fields cancel (a criticism the lead agent raised independently).

**The number falls by a factor of two, and the conclusion survives.**

| run | <10 kpc | <30 kpc | <100 kpc |
|---|---|---|---|
| monopole + g04k rule (anchor, reproduces g04k's 2.58) | 2.69 | 9.38 | 27.5 |
| multipole + repaired, σ = 20 km/s, canonical | **1.43** | 9.32 | 28.7 |
| multipole + repaired, σ = 60 km/s, canonical | **0.92** | 7.79 | 27.5 |
| multipole + repaired, σ = 20, alt footing | **1.45** | 9.37 | 29.1 |
| direct O(N²), independent solver | 1.09 | 8.83 | 29.0 |
| Newtonian control | 0.39 | 1.05 | 2.0 |

Caustics account for essentially the whole change (−49%); the cap repair costs 2%. Against
the 0.25 M_b the radial acceleration relation tolerates, the delivered mass is still **4–6×
over**, on both footings, both dispersions and two independent force solvers. The resolution
trend *rises* with N (1.24 at N = 4000 → 1.43 at 8000) and the coarse timestep biases *down*,
so the converged value is at or above these.

Solver validation: the multipole reproduces the monopole in spherical symmetry to 0.007%, and
reproduces the analytic interior field of an oblate spheroid to 5.9% where the monopole is
wrong by 38%. The final state is genuinely non-radial (median |a_tan|/|a_rad| = 0.372).

**A third defect, named by neither critique, and it matters for future work.** The algebraic
multiplier ν(|g|)g has **nonzero curl** the moment the field stops being radial: it does net
work around a closed loop (5.7e-3 of the path integral for the g04k rule, against 1.3e-9 for
the Newtonian field), and with the non-radial solver switched on it pumps energy and unbinds
the entire system within 1 Gyr, at any timestep. g04k never saw this because a monopole force
is radial by construction. **Any future non-radial MOND infall calculation in this programme
needs a genuine QUMOND field solve, not a per-particle multiplier.** The L1 runs above use a
conservative scheme, verified not to move the answer on its own (2.82 vs 2.69 with the monopole).

## L10 — the khronon gate: one design parameter, and a target region

`L10_khronon_gate.py` (5 FAIL of 10). L4 found the lead's construction propagates a healthy
khronon-type scalar with c_s² = 1/3. This lane put that mode through the preferred-frame and
stability gates this repository already established for a khronon in this action class.

**Controls.** An independent symbolic derivation reproduces g03v's closed form for α₂ (and
identifies a 3c₁₄²/4 term omitted there), its exact zero c₂\* = c₁₄/(1−2c₁₄), both published
numbers, and g03w's two tachyon rates.

**The PPN arm genuinely passes, by an enormous margin.** The construction's own exponential
screening puts Cassini at 5.78e5 a₀, some 3.7e4× above the PPN threshold of 15.4 a₀, so the
preferred-frame coupling there is e^(−5.8e5) — zero for any practical purpose, on both footings.
That is a real win. Its recorded cost: c₁₄ → 0 is also the strong-coupling limit, since the
mode's kinetic normalisation is proportional to c₁₄. That is exactly the recipe's P7 wound.

**What fires is gravitational Cherenkov, and it is one design parameter deep.** A subluminal
gravitational-sector mode radiates Cherenkov gravitons off ultra-high-energy cosmic rays; the
bound is 1 − c_s ≤ 2e-15 (Moore & Nelson 2001; Elliott, Moore & Stoica 2005), the same gate this
repository already imposes on its own khronon in `g03v_k2_pincer_closure` V6. With c_s² = 1/3,
1 − c_s = 0.4226 — **excluded by 2.1e14×**; IC7's own 0.3886 fails by 1.9e14×. The exponential
wall cannot rescue it, because the wall is a function of |a|/a₀ while the Cherenkov bound is read
exactly where |a| ~ a₀: suppressing it along a 10 kpc Galactic path would need |a| ≥ 33 a₀, which
a 220 km/s Galaxy reaches only within 0.5 kpc of the centre, 20× short.

**The actionable part.** c_s² appears to be σ, a free construction choice in IC-4 over (0, 1].
Cherenkov collapses that interval to **σ = 1 within 4e-15** — the mode must be marginally
luminal, not 1/3. Moving σ shifts p_R, A_R, B_R and F, so the IC6 obstruction, the IC7
counterterm and the tensor balance all need re-verifying at the new value. Nothing here
contradicts a claim the lead has made: IC-4 states σ is a choice, and no IC file claims a
Cherenkov, PPN or causality pass.

**The target region, for any clock construction in this class:**

| c₁₄ | c₂ range | binding constraint | Ω_off max |
|---|---|---|---|
| 1e-8 | ≥ 1.000e-8 (open above) | Cherenkov | 3.3e-9 |
| 4e-7 | ≥ 4.000e-7 (open above) | Cherenkov | 1.3e-7 |
| 1e-6 | 1.000e-6 – 5.000e-6 | Cherenkov | 3.3e-7 |
| 1e-5 | 1.000e-5 – 1.087e-5 | Cherenkov | 3.3e-6 |
| 2.5e-5 | 2.500e-5 – 2.583e-5 | Cherenkov | 8.3e-6 |

c₁₄ ≤ 2.5e-5 from α₁; c₂ in a thin collar just above c₁₄ about c₂\* = c₁₄/(1−2c₁₄); and
M ≡ |K₂|Q₀²ε₀/H₀² ≤ c₁₄. **The lower edge is always Cherenkov, never α₂, so a successful
construction is pinned to a marginally superluminal khronon.** The region is nonempty — and
becomes empty only if the clock sector must itself carry Ω_d = 0.266, where it is short by 3.2e4×.

**Honest limitation (K4 FAIL).** The mapping from the lead's variables to (c₁₄, c₂, |K₂|Q₀²) is
not determined by its published files: c₁₃ = 0 is clean, but c₂ = −FY/(a₀²K₆) vanishes at the
witness where the mode was measured (so the scalar's gradient energy comes from the auxiliary
sector, not c₂), c₁₄ has three inconsistent readings spanning 0.073–1.333, and |K₂|Q₀² has no
counterpart because there is no condensate in the IC action. Missing inputs named: the PPN
weak-field expansion of the IC action with the auxiliary constraint solved, and the O(k⁰) mass
term of the reduced scalar system.
