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
