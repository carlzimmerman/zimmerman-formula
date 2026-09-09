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

**CORRECTED 2026-09-08 by L18 (below): the "matches the cosmic ratio to 5%" headline is partly an
artefact of ignoring the hydrostatic mass bias and is withdrawn.** Correcting for the measured
(positive) bias moves the Newtonian ratio from 5.73 up to 9.04 across b in [0, 0.33]. What survives,
and strengthens, is the 13-15 sigma residual against the framework's predicted zero and the 12%
cluster-to-cluster universality. The cosmic *reading* of the cluster data is if anything better
motivated with the bias included; the *five per cent agreement* is not a real number.

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

> **⚠ PARTLY WITHDRAWN 2026-09-08 by L19.** The Cherenkov arm below is wrong in two places and its
> conclusion "σ = 1 within 4e-15" does not stand. The bound 2e-15 applies to a mode that couples to
> the emitter's T⁰⁰ ~ E²; on the IC10 η = 1 plateau the clock reaches matter only through the
> conformal factor, so the vertex is T^μ_μ and the bound loosens by 7.2e5× to 1 − c_s ≤ 1.4e-9.
> Larger: the exponential wall was evaluated along the ambient Galactic path where |a| ~ a₀, when the
> radiation is generated in the cosmic ray's own near field where |a|/a₀ = 8.8e38. **Cherenkov does
> not force σ = 1.** The PPN arm (K6) and the target-region table are untouched. See L19.


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

## L14 — the global parameter sweep: no admissible point, and the obstruction is two gates deep

`L14_parameter_sweep.py` (2 FAIL of 24). Individual pincers were known; the simultaneous
admissible region had never been computed. Ten gates, each rebuilt from its source script and
each reproducing that script's published verdict as a control, swept over 120,065,220 grid points
per footing in (K_B, c₂, c₁₄, |K₂|, Q₀, ξ).

| gate | canonical | alt |
|---|---|---|
| G1a PPN α₁ | 0.369 | 0.358 |
| G1b PPN α₂ | 0.278 | 0.278 |
| G2 clock tachyon | 0.091 | 0.091 |
| G2b condensate ε₀ | 0.274 | 0.274 |
| G3 linear growth | 0.800 | 0.800 |
| G4 dark-sector window | 0.172 | 0.138 |
| G5 Solar-System ξ | 0.529 | 0.471 |
| G6 BBN | 0.599 | 0.599 |
| G7 tensor + G_N > 0 | 0.808 | 0.808 |
| G8 Cherenkov | 0.386 | 0.386 |
| **intersection** | **0 points** | **0 points** |

**The obstruction is exactly two gates deep, not ten.** Minimal incompatible subsets, identical on
both footings: **{G1a, G2}**, **{G1b, G2}**, **{G2, G7}**, and {G2, G4, G8}. Every one contains G2.
The condensate's background makes the clock tachyonic at a rate needing c₁₄ ≥ 3Ω_d/Ω_m = 2.533,
while a positive Newton constant needs c₁₄ < 2 and PPN α₁ needs c₁₄ ≤ 2.5e-5 — a five-order
shortfall that closes only if one tolerates a k-independent mode growing ~300 e-folds per Hubble time.

**Drop G2 and the other nine open a real region** — 299,547 canonical / 221,544 alt points —
containing the programme's own fiducial corner: K_B ≤ 0.25, c₂ ≈ c₂\*(c₁₄), c₁₄ ≤ 1.18e-5,
|K₂| ∈ [5e4, 5e5], Q₀ ≤ 1 H₀, ξ ≥ 0.10/0.15 pc. Two cross-checks worth noting: that region
predicts **γ_v ∈ (1.0000, 1.0450] canonical / (1.0000, 1.0300] alt**, i.e. exactly Amendment 11's
registered Arm B ceilings; and its c₁₄ ≤ 1.18e-5 is consistent with L10's independently derived
target region c₁₄ ≤ 2.5e-5. Two lanes, different machinery, same corner.

**Two costs the individual pincers did not show.** G3 and G4 together cap S_eff at 0.185/0.153, so
every survivor sits on the fast-clock branch with the action's linear scalar source screened off
(T3 FAIL). And the obvious escape from the tachyon — freeing the dust amplitude — caps the
condensate's dark fraction at 2.6e-6, **1e5× too small to be the dark sector G4 exists to supply** (T4).

**The synthesis, and it is actionable.** The condensate was introduced to be the dark sector. It
cannot be, by five orders of magnitude. And its background is precisely what makes the clock
tachyonic, which is the single gate blocking every other one. So removing the condensate costs
nothing that was ever going to work and cures the one fatal conflict — and the lead agent's IC-series
has already removed it (L10's K4 records that the IC action has no condensate counterpart at all).
**A cure for the tachyon is necessary and sufficient for this action to have a home.**

## L11 — does the IC-series give MOND? Yes, at the framework's own a₀

`L11_galactic_limit.py` (3 FAIL of 22). The lead agent's own status file lists "galactic matching"
as open. It is not open any more, and the answer is a genuine positive.

**The derived limit.** The published static branch reduces exactly to

    div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G_N rho_b,   mu(y) = 1 - e^(-y),   G_N = 1/(8 pi m)

with Φ = Ψ. Every load-bearing feature checks out:
- **A MOND limit exists**: g → √(g_N a_scale) as g_N → 0, on both footings.
- **The scale is exactly the action's own a₀**, coefficient 1.000000 — no stray 2, ½ or 2π — so
  setting the action's a₀ to 9.3619e-11 or 1.1279e-10 reproduces the programme's scale exactly.
- **No slip**: ∇²(Φ − Ψ) = 0 survives the clock terms, so lensing and dynamics share one potential
  to better than 1e-4 out to 1 Mpc. That is the framework's lensing requirement, met structurally.
- **The Newtonian limit uses the same G** that normalises the tensor sector, so G_dyn = G_lens = G_tensor.
- The mechanism is exact, not perturbative: U′(c) = −ln²(1−c) gives u² = 1 − exp(−|a|/a₀) exactly on
  the static branch, and static GR's lapse-gradient square cancels, leaving μ = u².
- Every clock/vacuum term the limit drops is ≤ 1.9e-5 of the retained ones out to 1 Mpc.
- Control: the same machinery returns the Newtonian Poisson equation for GR plus a minimal source.

**Three things scored separately rather than hidden in the verdict.**

1. **It produces the exponential carrier, not ν_RAR (B2b FAIL).** μ = 1 − e^(−y) is the kernel this
   programme swapped *away from* on 2026-09-06. They differ by up to 0.073 dex, and on the bulgeless
   SPARC control the exponential ceiling is exceeded 5× more often (16.3%/10.5% against 3.1%/1.8%;
   the programme's own controlled count in g03w gives the same ordering at 7.3%/3.5% vs 1.2%/0.6%).
   Disfavouring, not exclusion — f25/g03l find exponential-vs-RAR undecided once a₀ and Υ are profiled.
   **Note a documentation conflict this exposes:** the recipe's frozen ingredient I1 names
   μ(y) = 1 − e^(−y) as *the* kernel, while THE_ACTION §3 carries ν_RAR. The lead is following the
   recipe correctly; the two documents disagree and one of them needs amending.

2. **The far-field boundary condition on u is not determined by the published files (B5 FAIL)**, and
   this is the one that matters. The η = 0 static branch gives u → 0 (isolated MOND); the η = 1
   plateau gives u = 0.49–0.67. Matching them needs the varied η-transition, which IC10's own "What
   remains" lists as undone. **Stakes:** if u must approach the cosmological value, the static law
   reads it as a universal external field of 0.28–0.59 a₀, and 27%/38% of bulgeless SPARC points
   beyond 2 kpc sit below even the smallest of those — precisely where flat rotation curves live.

3. The verdict PASSES on the reduction itself: the IC-series is a candidate host for this framework's
   galaxy phenomenology.

## L16 — the hybrid rescue: not available, but something real survives

`L16_hybrid_inverse.py` (5 FAIL of 11). This lane went looking for the rescue: if cold dark matter
exists at the abundance ΛCDM predicts, does the galaxy data still *require* an acceleration scale?

**No, and it is bounded rather than merely unfitted.** Granting each SPARC galaxy the halo ΛCDM
actually predicts for it (Moster+2013 abundance matching, Dutton & Macciò 2014 concentrations — the
relation already in this repository):

| | no halo | with the ΛCDM halo |
|---|---|---|
| variance in the residual explained by acceleration | **74.0%** | **−3.5%** |
| median within-galaxy slope | −0.324 | +0.020 (6% retained) |
| fitted acceleration scale | a₀ to 0.002 dex | **< 3.3e-13 m/s², i.e. 3.4 dex below a₀** |

The controls make the null real rather than a failure of sensitivity: an injected a₀ is recovered to
0.100 dex, the detection floor reaches a₀/3.2, and the verdict is identical across all eleven halo
rows spanning **twice** the abundance-matching and concentration uncertainties. a₀ returns only for a
halo 63× smaller than ΛCDM predicts, 6σ below it.

**What survives, and it is not nothing.** With zero free parameters on each side, the framework's
kernel at fixed a₀ still describes these rotation curves **more tightly than the granted halo does**:

| description | scatter |
|---|---|
| fixed-a₀ kernel (no free parameters) | **0.142 dex** |
| abundance-matched ΛCDM halo (no free parameters) | 0.171 dex |
| the same halo once its own M₂₀₀ and concentration scatter is switched on | **0.198 dex** |

That last row is the known halo-population-scatter problem (Desmond 2017, and this repository's own
`rar_origin_detector_2026.py` V2), and it is where an acceleration scale keeps content even though
the data do not *require* one. Baryons plus an NFW halo with no boost also miss the inner curves at
0.167 dex, 1.5× the relation the kernel achieves.

**The synthesis with L7.** Dark matter accounts for clusters (L7) *and* suffices for galaxies (here).
The kernel accounts for galaxies and cannot account for clusters (L2, L5, L6). So the hybrid in which
each does half the job is not available in the direction the framework needed. What the programme
keeps is narrower, real, and quantified: the **tightness** of the relation and the **value** of a₀
tied to ρ_Λ — neither of which rotation curves settle, and both of which the two pre-registered
measurements were built to test.

## L9 — the late-time transition: buys the cosmology, not the mechanism

`L9_late_transition.py` (1 FAIL of 9). L6 closed screened forces on two horns and explicitly left one
escape: a field that rolls late, so the coupling at nucleosynthesis and today differ. This tests it.

**It genuinely defeats L6's cosmological horn (T6 PASS).** With g(z_BBN) = 1 exactly and g(0) = F, a
narrow region survives nucleosynthesis, the microwave background, structure growth AND the full
expansion history including the absolute BAO ruler, while still delivering the enhancement at the
X-COP redshifts. This is the **first mechanism in the programme to reach the cluster residual without
being excluded by the gate it was proposed against.**

| footing | surviving region | construction |
|---|---|---|
| canonical | z_t ∈ [0.0033, 0.374], W ∈ [0.376, 0.565] — 146/3721 | h refitted to the acoustic scale |
| alt | z_t ∈ [0.0033, 0.441], W ∈ [0.336, 0.604] — 269/3721 | same, plus 6 at measured H₀ |

It makes a **sharp falsifiable prediction**: σ₈ = 0.845–0.861 with H₀ = 68–72, Ω_m = 0.27–0.31,
t₀ = 13.7 Gyr. Every survivor sits at the top of the growth gate; tightening that gate from 3σ to 2σ
empties the canonical footing entirely.

**But T8 is the decisive half, and it fails.** L6 killed the screened force on *two* horns, and the
roll addresses only the first. The second is the spatial contrast: clusters and galaxies overlap
**100% in baryon density** while requiring enhancements 12.8σ apart. Those two populations are
observed at z = 0.0037 and z = 0.090 — essentially the same epoch — so a spatially uniform g(z)
supplies a factor of **0.97, in the wrong direction**, against a required 2.2–5.1. The roll therefore
buys the cosmology and not the mechanism: the model still needs exactly the density-dependent
screening L6 excluded at 12.8σ, and weakens that exclusion by nothing.

**Two corrections the lane made by computing rather than assuming, one of them to my own framing.**
First, in a consistent scalar-tensor model the factor g **cancels exactly** from the growth source,
4πG_eff ρ_m/H² = (3/2)ρ_m/ρ_tot, so my premise that a 2–7× boost in G would "drive growth hard" was
wrong; growth moves only through the closure-forced Ω_Λ, and the two consistent normalisations push
σ₈ in opposite directions. Second, the roll's own d ln g/d ln a term in H(z) partly mimics dark
energy, which is why a universe that is ~50% matter still reproduces the distances — this is why the
lane added the absolute BAO ruler, since supernovae marginalise their zero point and the acoustic
scale is one number a refit can always hit. A bisection bug in the h-refitter was caught by the F = 1
control and fixed.

## L18 — the hydrostatic bias: not an escape, and it corrects one of my own numbers

`L18_hse_bias.py` (7 FAIL of 10). Every cluster result tonight rests on hydrostatic X-ray masses,
which carry a known systematic: M_HSE = (1 - b) M_true, with b measured in [0.00, 0.42] over the
literature and [0.03, 0.17] for X-COP itself. Nobody had propagated it. This lane exists to attack
this lane's own strongest claims.

**Controls pass**: at b = 0 it reproduces L7 exactly (f_bar = 0.149, ratio 5.73, 12% scatter) and L2
exactly (A = 5.47, p = 0.811, ratios 2.2-5.1).

**The direction is confirmed and it runs against the framework (H2).** At b = 0.20 the framework's
residual moves 3.09 -> 4.85 M_bar, the maximum required boost 2.94 -> 3.80, and the slope 0.811 ->
0.818, i.e. further from the 1/2 that caps any kernel. All three move away.

**The b that would rescue the framework is on the other side of zero:**

| to rescue | required b | measured |
|---|---|---|
| L7's residual to zero at 0.80 R500 | **-0.82** canonical / -0.68 alt (all twelve clusters negative, -1.25 to -0.52) | [0.00, +0.42] |
| L2's cluster/galaxy agreement | **-2.07** (bins -2.21 to -0.95, identical on both footings) | X-COP's own [0.03, +0.17] |
| L2's slope down to 1/2 | ≈ -6.8 | |

**And it is not physically available (H8).** A negative b means sigma^2 < 0 in twelve of twelve
clusters — not turbulence but a demand that the measured thermal pressure gradient be overstated by
1.82x. Even the *allowed* b = 0.20 already needs sigma_1D = 559 km/s, 3.4x Hitomi, and that
correction hurts the framework rather than helping.

**What this corrects in my own record (H6).** L7's headline "5.73 against cosmic 5.43, agrees to 5%"
is partly an artefact of ignoring the bias, and is withdrawn above. The ratio runs to 9.04 by
b = 0.33, leaving L7's own 30% depletion allowance (baryon retention 96% -> 64%). The 13-15 sigma
residual and the 12% universality (H9) survive the whole range and strengthen.

**Two items handed back.** (i) The L7 phrasing, corrected above. (ii) `hunt_2026/u13_mass_efe_and_domain.py`
line 334 carries the bias sign backwards relative to `u02:565`, and its C3 prose is wrong; no published
number moves because C7 overwrites B = 0.0 immediately after. Flagged, not edited.

## L15 — the obstruction at σ = 1: does not vanish, and a theorem says nothing in range removes it

`L15_sigma_one.py` (1 designed FAIL of 30). L10 showed Cherenkov forces the clock's speed parameter
σ from 1/3 to 1. Every downstream result was derived at the wrong value, so this lane redid them.
Mandatory control passed first: S₄′(1)|σ=1/3 = −11.1407711251147987, reproducing the lead's boxed
identity exactly.

**The obstruction survives and grows.** S₄′(1)|σ=1 = **−20.194205022906776**, same sign, **1.81×**
the published magnitude. IC7's counterterm is not only still required but required 1.78× more
strongly (c₇ ×1.785), on a window **half as wide** (|j−1| < 0.074 → 0.050), with its tensor detuning
2.6× larger. The construction does not simplify.

**The theorem, and it is the useful part.** σ's role is nowhere stated in the published files, so the
lane determined it: σ reaches everything through one channel, p_R = 8/3 + 4a\*σ, which makes
h|_{τ=0} exactly σ-free. That yields a new closed form, verified against the lead's identity at
σ = 1/3 and against the numeric derivative at six values of σ to better than 1.7e-40:

    S_4'(1;sigma) = e^{5/6} (p_R T - 9)(3 p_R + 4)(3 p_R - 44) / (216 (4T - 27)),   p_R = 8/3 + 4 a_* sigma

It has **exactly one zero**, at **σ\* = 4T/(4T−27) = 1.679** — a mode 29.6% superluminal — and that
lies above 1 for *every* T in the frozen domain. So **no σ in IC-4's own admissible interval (0, 1]
would ever have removed the obstruction**, and Cherenkov happens to select the point where it is
strongest (argmax at σ = 0.9807).

**The positive half is real.** σ = 1 is a regular point with nothing degenerate. c_T² = 1 survives as
a σ-**identity** rather than a tuning; the degree-of-freedom count stays 2 tensors + 1 clock; and the
scalar kinetic normalisations (a\* = 1.786, A₀ = 0.4615) are exactly σ-independent. The healthy clock
and the luminal tensor sector are robust to this entire class of parameter motion.

**A conditional worth stating precisely, because it is now the whole game.** The obstruction vanishes
only at σ\* = 1.679, i.e. a 29.6% superluminal clock. That is excluded *if* the gravitational-Cherenkov
bound applies to this mode. L19 is testing exactly that, on the grounds that L8 showed the mode is no
longer a gravitational khronon but a separately counted k-essence clock in an exactly Einstein metric
sector. **If L19 finds the bound does not apply, σ\* = 1.679 becomes reachable and IC7 becomes
unnecessary.** If it does apply, σ = 1 is forced and IC7 is required more strongly than published.

**Corrections and handbacks.** A premise of the lane's own brief was wrong: the branch does not end at
J_T = 0 but at a σ-independent **fold** of the auxiliary constraint surface at j = 1.216488, with J_T
positive to it and its margin collapsing 0.727 → 0.390. Named missing input: S4₁₁(σ=1), the sheared
reduced quartic, requires re-running the lead's anisotropic two-mode reduction with the new p_R.
Also flagged: `IC10_LOCAL_CLOCK.md` and `OPTICAL_ALIGNMENT.md` reuse the symbol σ for an unrelated
quantity (−1/4), which is worth renaming before it causes an error. Handoff challenge **B1 is discharged**.

## L12 — the constraint-first route (recipe A1): count confirmed, foliation kills it

`L12_constraint_first.py` (13 FAIL of 25). A1 is the one "acceptable protein" in the frozen recipe
claiming exactly two gravitational degrees of freedom — no khronon — via a constraint
`C_M = D_i[mu(y) D^i q] − S ≈ 0` with `q = −(1/6) ln det γ`. Its three open checks (foliation, matter,
cosmology) had never been run. They have now, and all three fail for one shared reason.

**The count is right, and so is the phenomenology.** C_M is momentum-free, so the constraint matrix
has rank 2, giving one second-class pair and (12 − 2 − 6)/2 = **2** — control returns 2 for ADM GR
by the same rule. The removed mode is genuinely the conformal one (the coefficients of a″, b″, c″ in
δC_M are symbolically identical). The static weak-field limit is **exactly Milgrom's equation** with
the recipe's frozen kernel μ = 1 − e^(−y), reproducing v⁴ = GMa₀ on both footings; screening is by a
local acceleration per I4 (y > 1e5 out to Neptune); recovery is exponential with no 1/y per I5.

**And then it dies, on the cleanest possible test.** Vacuum Schwarzschild in Painlevé–Gullstrand
slicing has exactly flat spatial metric, so q ≡ 0 and the MOND field is **exactly zero** — while the
static slice of the *same spacetime* gives g_Newton. The field is a property of the slice, not of the
geometry.

It is worse than non-covariant slicing. Taken literally q is not a spatial scalar at all (anomaly
δ_ξq = ξ·∂q − ⅓∂·ξ), so **empty flat space in spherical coordinates demands −1.6×10³ kg/m³ of
fictitious matter at 1 AU**. The standard fiducial repair restores scalarity but not uniqueness: the
areal fiducial gives g_N/3 and the isotropic one g_N, a factor 3 in the field and **9 in a₀**, with
nothing in A1 selecting between them.

- **Matter (M1 FAIL):** general relativity's own Hamiltonian constraint already gives ∇²q = 4πGρ/c²,
  so imposing C_M as well leaves div[e^(−y)∇q] = 0, and since max g·e^(−g/a₀) = a₀/e no nonzero flux
  survives r → 0. **g ≡ 0 for any matter.** The two constraints want accelerations differing by
  2.87× (canonical) / 3.12× (alt) at 10 kpc. Matter conservation itself is fine (M3 PASS).
- **Cosmology (K1, K2 FAIL):** on FLRW, D_i q = 0, so μ(0) = 0 and C_M reduces to −S, **forcing
  ρ = 0**. At linear order the operator starts at second order (measured slope 2.0000), so it
  constrains δρ rather than the metric and removes no mode.
- **F4 FAIL, the P7 pattern again:** the lapse-fixing coefficient is ∝ μK, and |K|/ω = 3×10⁻¹¹ in the
  Solar System — the second-class pairing that buys the count is nearly degenerate exactly where the
  theory must work.

**Verdict: A1 as written is dead as a route to N_grav = 2 without a preferred foliation.** The
surviving obligation is to find a scalar, foliation-independent quantity to put in q's place; this
lane found none. That is an open construction problem, not a closed door — but the recipe's A1 entry
should be amended to record that its three open checks have now been run and failed.

## L21 — binary galaxies: the regime between a galaxy and a cluster

`L21_binary_galaxies.py` + `L21_BINARY_GALAXIES.md` (16 checks, 7 FAIL; every control passes). This lane
CHECKS AND EXTENDS existing work rather than opening a front: `hunt_2026/h48_h69_binary_galaxies.py`,
`h48_h69b_relative_isolation.py` and `h47_dwarf_pairs.py` already measured these samples, and
`closure_2026/g02c_two_body_force.py` already verified Milgrom's deep-MOND two-body force by an independent
QUMOND field solve. What is new: the CARRIED saturated kernel instead of the pure deep-MOND limit, the
external field COMPUTED from 2M++ (e_N = 0.01240/0.01027) with an orientation-averaged anisotropic EFE, the
cosmic-share curve L7 implies, and a forecast on an axis immune to the stellar M/L.

On 1900 isolated 2MRS major pairs (rebuilt independently; N and σ reproduce h48_h69b to 4% and 0.3%):

| law | A (canonical) | A (alt) | σ from 1 |
|---|---|---|---|
| framework, isolated deep-MOND (its **best case**) | 1.802 ± 0.041 | 1.731 | 19.6 |
| framework, carried with the EFE | 2.311 ± 0.053 | 2.219 | 24.9 |
| **cosmic share (5.43 M_b), point mass / NFW** | **2.222 / 2.319** | — | 22 / 25 |
| **framework kernel + cosmic share** | **1.141 ± 0.028** | **1.099** | 5.0 |
| ΛCDM abundance-matched | 0.967 ± 0.024 | — | 1.4 |

- **The cosmic share does not extend downward.** A Newtonian reading of the pairs needs M_dark/M_bar =
  **30.9 ± 1.6 within the pair separation**, against 5.73 ± 0.68 at 0.80 R500 — a factor 5.7, 16σ. The
  ladder is not monotone; there is no radius at which "the cosmic share turns on".
- **A cosmic-share halo alone is worse than the kernel** here (2.22–2.32 against 1.80), against expectation.
- **The two together very nearly work and neither does alone**: A = 1.10–1.14, and its separation slope is
  the closest of any law to the measured −0.170 ± 0.029 (1.9σ). The amount the framework is short at pair
  separations is, to ~10% in velocity, the amount the cluster residual is — four decades apart in mass.
- **Structural degeneracy (S0 FAIL).** Beyond ~200 kpc the framework's EFE branch and a cosmic-share halo
  are the SAME law: ν̄(e_N) = 7.99 against 1 + 5.43 = 6.43, identical in shape, **11.5% apart in velocity**.
  All discriminating power lives on the isolated branch. The curves cross at r_p ≈ 70 kpc (0.049 a₀); the
  maximum divergence over 30–1000 kpc is 0.546 dex at 1000 kpc.
- **The deficit grows with mass** (M0 FAIL, 3.9σ over 0.56 dex), which a kernel with no scale in it forbids;
  ΛCDM's abundance-matched halos move the other way.
- **The galaxy-side gate bites on shape and mass scale, not amount** (S6 FAIL, computed here not reused):
  the carried kernel tolerates 0.41 M_b inside 10 kpc at L\* and 0.59 at a dwarf; an NFW cosmic share puts
  0.34 M_b (admissible) and 1.90 M_b (excluded, 3.2×). L1/g04k's exclusion is of a *concentrated* component.
- **Forecast, pre-registerable.** Parameter-free: σ_los = 0.60679 (G m a₀)^{1/4} = 107.7 / 112.9 km/s for
  two 8e10 M_⊙ galaxies at ANY separation. 3σ separation from a cosmic-share halo needs **384 pairs at
  40 km/s, 122 at 10 km/s**, or **65 pairs on the shape axis** — all far below the 1900 in hand.
  **Statistics are not the limitation; isolation depth is** (2MRS sees only companions above ~23% of the
  pair's mass, and the amplitude falls 1.99 → 1.51 as the isolation deepens, so every A here is an
  UPPER limit). The unresolved cross-scale tension with ALFALFA's dwarf pairs (1.12 ± 0.29) stands.

## L13 — the strong-coupling wound (recipe P7): does not fire, but the design principle does

`L13_strong_coupling.py` + `L13_STRONG_COUPLING.md` (22 PASS, 4 FAIL; all 13 controls pass).

The recipe's P7 says the khronon's kinetic normalisation is proportional to c₁₄, so the exponential
screening that buys the PPN pass also drives the mode to strong coupling exactly where the theory
must work. This lane computed the kinetic Hessian directly rather than arguing from the normalisation.

- **P7 does not fire.** The Hessian is diag(2M²c₁₄k², 2M²|K₂|) at *every* value of the screening
  variable. The AeST-type mixing 2(2−K_B)J^μ∂_μφ carries one time derivative, is antisymmetric, and
  drops out of the symmetric part entirely. c₁₄_eff/c₁₄ = 1.190 at Saturn, 1.0018 at 1 AU,
  1.0000001 at Cassini conjunction. The screening does **not** feed back on the normalisation.
- **The strong-coupling scale is astronomically safe:** Λ_sc = 2M_pl√c₁₄ = 1.54e16 GeV = 1.28e−32 m,
  10⁴³× shorter than 1 AU. P7 would need c₁₄ < 7.3e−92 to bite.
- **But A3's design principle is violated as an identity.** α₁ = −4c₁₄ exactly, and the khronon
  kinetic term is 2M²c₁₄k², so the ratio is identically −4 for every (K_B, c₂, c₁₄) — the two cannot
  be separated by choosing parameters. The recipe's α_PF ∝ e^(−y) is refuted outright: α₁ and α₂
  contain no screening variable at all. Whatever buys the PPN pass, it is not a screened α₁.
- **Two costs, quantified and new.** The MOND scalar's own cone is c_s ≥ 19c at 1 AU and 2522c at
  Cassini conjunction, forced by J_Y = s/Δ with Δ bounded (this is L33's lane). And on the saturated
  branch Δ′ = 0 exactly, so Σ_∥ = 1/Δ′ is infinite and the scalar's cubic action **cannot be written**
  — the action as published is not twice differentiable at the Solar-System background (L30's lane).

## L19 — does the Cherenkov bound apply to the clock? Partly not, and L10 is corrected

`L19_cherenkov_applicability.py` + `L19_CHERENKOV.md` (13 checks, 6 FAIL; every control passes,
including an independent re-derivation of Moore & Nelson's coefficient and the published 2e-15 bound).

L10 excluded c_s² = 1/3 by gravitational Cherenkov and concluded the clock must be luminal to 4e-15.
This lane asked the question L10 assumed: **does that bound apply to this mode?** It largely does not.

- **The bound constrains the coupling, not the speed.** Moore & Nelson's 2e-15 is for a mode coupling
  to the emitter's T⁰⁰ ~ E². On IC10's η = 1 plateau the clock never appears in S_m and reaches matter
  **only through the conformal factor**, so ∂S_m/∂w = −√(−g)T^μ_μ exactly and the vertex is the trace.
  That loosens the bound by **7.2e5×, to 1 − c_s ≤ 1.4e-9**.
- **That alone does not save c_s² = 1/3** (still fails by 2.9e8×). What saves it is L10's second and
  larger error: the exponential wall was evaluated along the ambient 10 kpc Galactic path where
  |a| ~ a₀, when the radiation is generated **in the cosmic ray's own near field**, where
  |a|/a₀ = 8.8e38. Applying Milgrom's own high-acceleration GR limit (arXiv:1102.1818) there gives
  D_loss = 4.5 ℓ_M — 1.4e7× the path length and **33 Hubble distances** — for any subluminal speed,
  on both footings and at full tensor coupling. **L10's "the exp wall cannot rescue this gate" is
  withdrawn**, and with it "σ = 1 within 4e-15".
- **A three-tier conditional, with the deciding input named.** Y1, a gravitational-sector mode with
  preferred-frame mixing (IC5/6/7, and IC10 off the η = 1 plateau where L8 found λ ≠ 1): vertex ~E²,
  bound 2e-15, L10 stands. Y2, a k-essence clock in an exactly Einstein sector with conformal coupling
  only (IC10 at η = 1 as published): bound 1.4e-9. Y3, Y2 plus the high-acceleration limit holding in
  the emitter's near field: **no bound at all**. The deciding computation is IC10's own open item 3 —
  expand P_w + e^{4w}T^μ_μ = 0 on the static branch and evaluate ∂w/∂X̃ as |a|/a₀ → ∞.
- **One correction cutting the other way (C5 FAIL).** "Conformal scalars decouple from radiation" is
  **false** at Cherenkov kinematics: the emitted quantum is spacelike (2p·k = k²), and for a spin-0
  primary the trace coupling reproduces the tensor bound to four digits. The protection here is
  entirely the Dirac structure ⟨T^μ_μ⟩ = M ū(p′)u(p), not conformal invariance.
- **Confirmed in L10:** the PPN arm (K6) is untouched, the speed is the invariant that matters, and
  without screening c_s² = 1/3 does fail. **Consequence for the handoff:** A5 becomes a conditional,
  A6 is scoped to Y1, and L15's σ* = 1.679 obstruction drops off the critical path.
- Causality control (C9): the subluminal clock cone lies inside the metric null cone, so no closed
  causal curve can form. No photon, neutrino, graviton, binary-pulsar or CMB channel binds it.

## L17 — the nonlocal elliptic door (recipe A5): a seasoning, not a protein

`L17_elliptic_nonlocal.py` + `L17_ELLIPTIC.md` (32 checks, 17 FAIL; all 7 controls pass, both footings).

A5 proposes a spatially nonlocal elliptic operator f(−D²/a₀²) — nonlocal enough to change the force
law, elliptic so it adds no initial data. This lane tested it in both placements: as the **mechanism**
that produces MOND, and as a **filter** inside an already-MOND term (PAPER4's ξ²|∇⊥V|²).

- **A5's own central claim is TRUE, and this lane confirms it independently.** The localisation
  L = λ[(1−ℓ²Δ)w − u] adds **exactly zero** degrees of freedom (four second-class constraints). The
  same localisation with a *temporal* operator adds 2, with kinetic eigenvalues −2/+2 — a ghost pair,
  which is the recipe's P6 reproduced from the same machinery. At a zero of the symbol the quartet
  collapses to 2 first class, so **ellipticity is load-bearing**, not the word "auxiliary". Controls:
  the Dirac counter returns 1, 0, 2, 3, **2 for linearised GR**, and 5 for massive Fierz–Pauli.
- **As the mechanism it dies on linearity, and the argument is generic.** A filter is a linear
  operator, so superposition forces g ∝ M for every symbol and every length:
  **d ln g/d ln M = 1.000000** against MOND's required 0.5, re-verified on an arbitrary 200×200 dense
  nonlocal positive-definite operator to 1e-11. μ(y) = 1 − e^(−y) is unreachable in principle —
  A5-L's μ_eff = 1/(1 + 2r/πℓ) depends on r alone and is identical to six digits for two galaxies
  whose required μ differ by 8.6×.
- **A5's own caveat fires exactly, and is quantified.** g_A5L/g_MOND = (2/π)(v_flat/c)² = **2.50e-7**
  (canonical) / 2.74e-7 (alt), r-independent — short by ~4e6. Under a density rescaling the extra
  force is O(ε^1.000000) while the frozen kernel's phantom is O(ε^0.498), non-analytic and dominant.
  The momentum scaling really *is* changed, 1/r² → 1/r (O1 PASS), so the recipe's note is confirmed
  in both halves: the mechanism works and the amplitude is six orders short.
- **Root cause, and the deliverable.** The only length a₀ and c admit is ℓ₀ = c²/a₀ = 31.11 / 25.82
  Gpc, and ℓ₀/r_M = (c/v_flat)² ≈ 8e5–8e7. In PAPER4's filtered placement that length annihilates
  MOND from either side — smoothing suppresses the argument by 1.4e19 (Gaussian) / 4.8e12 (Helmholtz)
  at 20 kpc, sharpening saturates it at y = 6.9e15. Both give Newton. **A nonlocal operator is
  triggered by a length; MOND is triggered by an acceleration**, and the only dictionary between them
  is r_M = |Φ|/a₀ — the potential, which the recipe's I4 forbids by name, which is not a local
  invariant, and which is mass-dependent and therefore not an operator at all.
- **The price A5 does not pay.** There is no covariant elliptic operator on a Lorentzian manifold, so
  the filter needs a foliation; the A5 term is built from γ_ij with N only in the measure, so its
  khronon kinetic matrix is **exactly zero**. Either the host supplies c₁₄ ≠ 0 (and the count is 3)
  or nothing does and the foliation scalar is strongly coupled — the recipe's P7, verbatim.
- **Verdict: admissible as a seasoning, excluded as a protein.** The Solar-System gate passes (S2),
  and the DOF result and the elliptic-vs-temporal contrast are worth keeping. Both failures rest on
  two independent legs — linearity, which involves no cosmological number at all, and the dimensional
  uniqueness of c²/a₀ — so they are generic to the class, not artefacts of a filter choice.
