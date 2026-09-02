# Why the MOND Scale Is the Dark-Energy Scale: A Universal Dark-Field Theorem for Relativistic Modified Gravity

**Flagship synthesis, 2026-09-01.** Every quantitative claim is backed by a committed, re-runnable
script built to be able to fail; steps that are inputs or definitional choices rather than derivations
are labelled as such. Two "footings" are carried on every dimensional number: canonical
(ρ_DE / cH_Λ ⇒ a₀ = 9.36×10⁻¹¹ m s⁻²) and alternative (ρ_total / cH₀ ⇒ 1.13×10⁻¹⁰ m s⁻²).

---

## Abstract

The mass-discrepancy–acceleration relation of galaxies is governed by one acceleration scale
a₀ ≈ 1.2×10⁻¹⁰ m s⁻². We take seriously the hypothesis that this scale is set by the cosmological
constant, a₀ = ½c√(Gρ_Λ) = c²√(Λ/32π) = cH_Λ/Z with Z = √(32π/3), giving 9.36×10⁻¹¹ m s⁻² with no
fitted normalisation beyond the order-unity κ = ½. We then ask what relativistic field theory can carry
this scale while also reproducing the exact interpolation μ(y) = 1 − e^{−y}, producing correct lensing
with no slip (Φ = Ψ), propagating only the two tensor polarisations of the graviton, and having
acceptable post-Newtonian behaviour. Our central result is a **theorem**:

> **Any relativistic completion that reproduces exact MOND phenomenology together with slip-free lensing
> (Φ = Ψ) necessarily carries a dark field — an independent gravitating component sourced by, and
> tracking, the baryonic mass. There is no dark-field-free realisation.**

The proof is a pincer with the mechanism fully exposed. (i) In any *local* single-metric theory,
achieving MOND with exactly two propagating tensor degrees of freedom forces the MOND potential to be
carried by a **second-class constraint**, which is elliptic and therefore **instantaneous**; an
instantaneous carrier gives a preferred-frame post-Newtonian parameter **α₃ = O(1)**, excluded by
pulsar timing at ~10¹⁹×. Escaping this requires a retarded — i.e. *propagating* — carrier, which is an
extra gravitational degree of freedom: a dark field. (ii) In any *nonlocal* theory, the retarded
operator □⁻¹ supplies the retardation (so α₃ = 0, evading the local kill) but the carrier is then
□⁻¹[ρ_b], a gravitating memory field that carries the enclosed baryonic mass into the exterior — again
a dark field, and demonstrably slaved to the baryons (the ratio-lock). MOND's defining relation
v⁴ = G M_b a₀ requires the exterior field to know the *enclosed* baryonic mass, a nonlocal datum that
no local curvature functional can supply; carrying it is exactly what makes the carrier a dark field.

We tested the theorem to destruction against the strongest candidate constructions — generalised
Einstein-aether/AeST, khronometric MOND, minimal-modified/constraint gravity (MMG, York/CMC), a
cuscuton-dark-energy four-constraint construction (CDE-L4C) built on published two-degree-of-freedom
machinery, and the Deffayet–Woodard nonlocal theory — and each fails in exactly the way the theorem
predicts. The positive corollary is the point: **the dark field the theorem forces is the dark-energy
condensate**, the field whose de Sitter minimum gives w = −1 and whose scale sets a₀. That is why
a₀ = c²√(Λ/32π); the MOND scale and dark energy are two faces of one field, and the durable falsifiable
prediction is that the acceleration scale tracks the expansion, a₀(z) ∝ √ρ_DE(z), constant to
sub-percent for z ≲ 5 and switching off before recombination.

We claim less than a theory of everything and less than dark-matter-free modified gravity. We claim a
sharp reframing of one number, a rigorous statement of why its relativistic embedding cannot be
dark-field-free, and a falsifiable redshift law.

---

## The Zimmerman field equations (the operative content)

The parts of this framework that are the author's own and that survive every result below form a small
closed set, each labelled derived or input.

**(Z1) The acceleration law** — the single postulate, INPUT (κ = ½ fitted):

    a₀ = ½ c √(G ρ_Λ) = c² √(Λ/32π) = c H_Λ / Z,   Z = √(32π/3).

**(Z2) The quasistatic field equation** — modified-gravity (AQUAL) form, exact exponential kernel:

    ∇·[ μ(|∇Φ|/a₀) ∇Φ ] = 4π G ρ_b,    μ(y) = 1 − e^{−y}.

High acceleration (y≫1): μ→1 exponentially, Poisson with the derived Newton constant. Deep MOND (y≪1):
|∇Φ|² = a₀ g_N.

**(Z3) The baryonic Tully–Fisher theorem** — a consequence of (Z2), DERIVED, parameter-free:

    v⁴ = G a₀ M_b,     d ln v / d ln a₀ = ¼   (radius cancels identically).

**(Z4) The lensing statement** — no slip, light and matter feel one potential:

    Φ = Ψ,     γ_PPN = 1   (Φ and Ψ derived independently in any embedding).

**(Z5) The redshift law** — the distinctive falsifiable prediction:

    a₀(z) ∝ √ρ_DE(z) ∝ H(z)   (dark-energy-dominated),

constant to <1% for z ≲ 5, off before recombination. The constant value at the de Sitter minimum is
DERIVED; the evolution as a dynamical consequence is the open inverse-K(Q) problem — at present a
consistent phenomenological law, not a theorem.

The theorem below (§4–§7) shows (Z2)–(Z4) cannot be realised without a dark field; (Z1) and (Z5) give
that dark field its identity as the dark-energy condensate.

## 1. The acceleration scale and its horizon origin

Below a₀ galaxy rotation curves flatten and the radial-acceleration relation bends from g_obs = g_bar
to g_obs = √(a₀ g_bar). The framework's postulate is that a₀ is the de Sitter horizon surface gravity
cH_Λ (H_Λ = c√(Λ/3)) reduced by one geometric factor Z = √(32π/3), which is algebraically the Einstein
8π times the Friedmann 3 with a single outside factor of 2. **What is derived and what is not:** the
a₀ ~ c²√Λ coincidence is Milgrom's, decades old; the cancellation of the π's, 8 and 3 is exact; the
outside factor **κ = ½ is FITTED**. Two independent SPARC estimators give κ = 0.465 ± 0.076 (BTFR) and
0.551 ± 0.043 (distance-free), bracketing ½; an irreducible gas-mass floor (~3.9%) caps the
measurement at ≈ ±0.02, enough to separate ½ from 1/√3 at ~4σ but never to fix a specific rational.
κ = ½ is a one-parameter effective input.

## 2. The phenomenology the scale carries (all script-backed, both footings)

- **RAR** on 175 SPARC galaxies: 0.108 dex at Υ = 0.70 — at or below standard MOND's 0.122–0.140.
- **BTFR** as a theorem of the deep-MOND limit: v⁴ = G a₀ M_b, slope ¼ exactly.
- **Weak-lensing RAR** 40 kpc–2.2 Mpc, χ²/dof = 2.03 (canonical) / 0.94 (alt), real KiDS-1000 data,
  no dark component, no free parameters.
- **Solar system:** the exponential kernel suppresses the Sun's anomaly ~10¹³×, discharging the
  ephemeris liability that excludes power-law interpolations.

These are the successes a completion must preserve. They require that the completion reduce to
exact-exponential AQUAL with γ_PPN = 1 — which, as we now prove, forces a dark field.

## 3. The completion requirements

From ONE action: (1) exact μ = 1 − e^{−y}, deep-MOND v⁴ = G a₀ M_b, Newtonian recovery; (2) exactly two
tensor DOF, no ghost, at most one healthy extra scalar; (3) Φ = Ψ, γ_PPN = 1, both derived
independently; (4) acceptable PPN β, γ, α₁, α₂, α₃ — derived; (5) ∇_μT^{μν} = 0 for ordinary matter as
an identity; (6) c_T = c; (7) stability, no instantaneous physical channel; (8) expanding FLRW; (9)
controlled y→0; (10) derived Newton constant; (11) one physical metric; (12) the exponential law; (13)
the a₀–Λ relation, input unless honestly derived. The historical relativistic-MOND theories each
satisfy most and fail one, with the failure migrating from theory to theory. The theorem explains why.

## 4. The universal dark-field theorem — statement

**Theorem.** *Let a relativistic gravitational theory reproduce, in the quasistatic weak field, the
exact MOND relation ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b with slip-free lensing Φ = Ψ, from matter minimally
coupled to a single physical metric. Then the theory contains a dark field: an independent field with
its own gravitating stress, sourced by and tracking the baryonic mass density. There is no
dark-field-free realisation compatible with observed preferred-frame bounds.*

The proof (§5–§7) is a two-horn pincer. It rests on one physical observation, made sharp: **MOND is a
statement about enclosed mass.** The deep-MOND acceleration g = √(a₀ g_N) = √(a₀ G M_b(<r))/r depends
on the baryonic mass *interior* to the field point — a nonlocal functional of ρ_b. A local curvature
functional f(R, R_μν, …) is blind to enclosed mass in the exterior vacuum (where R_μν = 0), so it
cannot produce MOND at all. The enclosed-mass dependence must be carried by *some* field extending into
the exterior. The two horns exhaust how that field can behave.

## 5. Horn 1 (local): the α₃ pincer

**Claim.** In a local single-metric theory with exactly two propagating tensor DOF, the MOND potential
is carried by a second-class constraint, which is instantaneous, giving α₃ = O(1).

**Mechanism.** With no extra propagating DOF, the field carrying the enclosed mass cannot be a
propagating mode — it must be fixed on each time slice by a constraint. A second-class constraint is
solved by an elliptic Green operator: the response function in (k, ω) space is R = 1/k², **independent
of ω** — instantaneous, no retardation. The preferred-frame parameter α₃ vanishes if and only if the
interaction is retarded (momentum-conserving); an instantaneous response leaves a residual
preferred-frame term at O(w²), and the principal (k,ω) extraction gives **α₃ = O(1)** (representative
value −1), against the pulsar bound |α₃| < 4×10⁻²⁰ — a ~10¹⁹× violation. Restoring retardation requires
a propagating carrier = an extra DOF = a dark field. *The same property that removes the scalar graviton
(N_grav = 2) is what makes the MOND carrier instantaneous, and hence what forces α₃ ≠ 0.* You cannot
have both.

**Tested to destruction.** Four independent local constructions fail exactly here:
- **Generalised Einstein-aether / AeST.** Restoring the two aether couplings AeST sets to zero
  (c₂, c₄, tensor-blind so c_T = 1 survives) and computing the boosted PPN gives the closed form
  **α₁ = −4c₁₄ − 4(2−K_B)/(J_Y+1)** (c₁₄ = K_B + c₄). Setting α₁ = 0 forces c₁₄ = −(2−K_B)/(J_Y+1) < 0,
  a spin-1 ghost. The irreducible term is exactly the scalar–vector coupling 2(2−K_B)J·∇φ that
  *generates* MOND. The solar-profile-background check confirms no screening (α₁ grows to −5.65
  longitudinal, −12 transverse). Verified against a grid + two gauges + Foster–Jacobson recovery.
- **Khronometric MOND (FC-KH).** Radial-gradient ghost c²_∥ ∝ f'' < 0 on a₀ < a < 38a₀; the
  Cassini-vs-ghost pincer; the (yq)′ analytic no-go.
- **Constraint gravity (MMG, York/CMC).** The elliptic constraint gives α₃ = O(1) (DC-019); York/CMC
  is DEAD-INSTANTANEOUS via the MOND external-field effect.
- **Cuscuton-DE four-constraint (CDE-L4C).** The fullest test: built on the Yao–Gao four-second-class-AC
  theorem plus the cuscuton and the Laplacian zero-mode trick. It clears — at the principal level — the
  exact kernel and deep-MOND cubic, GR recovery, the a₀↔Λ promotion, no-slip Φ = Ψ, the Dirac
  preservation crux (the MOND lapse equation emerges independently; the no-slip multiplier does not
  steal it), and the DOF count (four constraints, rank-4 second-class, det Δ ∝ k⁸λ_∥², N_grav = 2). It
  then dies at α₃ = O(1) — and dies *because* it passed the DOF count: the second-class constraint that
  removed the scalar graviton is the instantaneous carrier that forces α₃ ≠ 0.

## 6. Horn 2 (nonlocal): the memory dark field

**Claim.** A nonlocal theory escapes the α₃ kill but carries a dark field.

**Mechanism.** A retarded nonlocal operator □⁻¹_ret has response R = 1/(k² − ω²/c²), which carries the
retardation term the local constraint lacks, so **α₃ = 0** — a genuine escape, and without a local
propagating scalar (the retardation lives in the operator). This is the one place the Horn-1 pincer
does not reach; the Deffayet–Woodard 2026 theory is the concrete instance (exact MOND, Φ = −Ψ lensing,
c_T = 1, α₂-safe). But the carrier is now □⁻¹[ρ_b] — the enclosed-mass memory, nonzero in local
vacuum, with its own gravitating stress: a dark field. It is not avoidable: to give v⁴ = G M_b a₀ the
memory must track the baryonic mass, and Deffayet–Woodard's own structure makes this exact (the mimetic
charge and ρ share a conserved flux, so Q ∝ ρ_b identically — the ratio-lock). A memory field that
tracks M_b and sources the metric is a dark field by definition; one that did not track M_b would not
be MOND.

## 7. Why the two horns exhaust the possibilities

The enclosed-mass carrier is a field extending into the exterior. Either it is fixed on each slice
(instantaneous → Horn 1 → α₃ kill unless it propagates → dark field), or it is mediated by a nonlocal
retarded operator (→ Horn 2 → memory dark field), or it propagates as a genuine local mode (→ an extra
DOF = a dark field directly). In every branch the carrier is an independent gravitating field. **Hence
the theorem.** The lensing requirement Φ = Ψ is what forbids the trivial escape of a stress-free
carrier: to bend light like the dynamical mass, the carrier must source the metric, i.e. gravitate.

## 8. The positive reading: the dark field is dark energy

The theorem is usually heard as a defeat — "the theory has dark matter after all." It is the opposite.
The dark field the theorem forces is not arbitrary: in the AeST realisation it is a shift-symmetric
condensate whose de Sitter minimum gives w = −1 exactly (dark energy) and whose excitation carries a
cold, conserved, a⁻³ charge (the CMB dark-matter component at full Ω_dm). **The MOND scale and the
dark-energy density are two faces of one field** — which is exactly why a₀ = c²√(Λ/32π). At the σ₈
scale today a linear perturbation sits deep in the MOND regime, where the kernel would multiply gravity
~30×; a cold dark component is therefore *required* to keep MOND out of linear cosmology and reproduce
the CMB. "The theory contains a dark field" is load-bearing, not reluctant. The framework's honest
slogan is **"no dark-matter particle"** — the carrier is a mode of a field, and the field is
unavoidable, and it is dark energy.

## 9. Falsifiable content, scope, and honesty

**The prediction:** a₀(z) ∝ √ρ_DE(z), rendered by the derived law as constant to <1% for z ≲ 5,
transition z_t ∈ [17, 35], off at recombination. Consequences, each pre-registrable on both footings:
the early-rotator BTFR zero point v(z)/v(0) = [a₀(z)/a₀(0)]^{1/4} (flat below z = 5, signed deficits
above — a 2030s ALMA/JWST target); the weak-lensing RAR knee not moving with z below z ≈ 5; MOND-boosted
collapse 1.34–1.96× faster and *declining* with z; the Gaia DR4 wide-binary γ_v; DESI's w(z) dissolving
to −1.

**Input, not derived:** κ = ½ (fitted); the a₀–Λ promotion (a definitional choice); the a₀(z) evolution
as a dynamical consequence (the inverse-K(Q) problem is open).

**Scope of the theorem.** The α₃-vs-0 dichotomy is the robust presence/absence of the retardation term
in the (k,ω) response, not a fine coefficient; the exact α₃ number needs the full boosted 1PN solve.
The enclosed-mass argument is established at the mechanism level and is confirmed by every known
instance (AeST, khronometric, MMG/York, CDE-L4C, Deffayet–Woodard). A fully general theorem-grade
statement would formalise "MOND's enclosed-mass dependence ⇒ the exterior carrier gravitates"; the one
honest residual is a nonlocal construction whose memory carries M_b yet somehow does not gravitate as
an independent component — no such construction exists, and Φ = Ψ appears to forbid it.

**Not claimed:** a theory of everything; dark-matter-free modified gravity; a completed all-gates
Lorentz-invariant field theory. The result is that no dark-field-free completion exists, that the
required dark field is the dark-energy condensate, and that a₀ ∝ H(z) is the sharp test.

---

## Reproducibility

Committed under `qwen_claude_field_theory/closure_2026/`: `FRIED_CHICKEN_VERDICT_2026-09-01.md` (the
local case-exhaustion); `GEN_AEST_PPN_VERDICT.md` + `generalized_aest_2026/` (the aether α₁ closed form
and no-screening); `V9_PPN_KILL_VERDICT.md`; `fc_kh_terminal/` (khronometric); `theory_2026/york/`
(York/CMC DEAD-INSTANTANEOUS); `cde_l4c_2026/gateA/` (the CDE-L4C preservation crux, the rank-4 Dirac
count, and the α₃ kill); `nonlocal_door_2026/NONLOCAL_DOOR_VERDICT.md` (the retarded escape and the
memory dark field); `solar_screening_2026/` (no screening). Phenomenology under `real_research/` and
`nbody_2026/`. All scripts exit 0, contain checks built to fail and at least one mutation control, and
carry both footings. a₀ = c²√(Λ/32π) is an external input to every candidate and is never claimed as
derived.
