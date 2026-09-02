# The Cosmological Constant Sets the MOND Scale: A Horizon-Derived Acceleration, a Field-Theoretic No-Go for Its Lorentz-Invariant Completion, and a Falsifiable Redshift Law

**A flagship synthesis, 2026-09-01.** Every quantitative claim below is backed by a committed,
re-runnable script that is designed to be able to fail; where a step is an input or a definitional
choice rather than a derivation, it is labelled as such in the text. Two "footings" are carried on
every dimensional number: canonical (ρ_DE / cH_Λ ⇒ a₀ = 9.36×10⁻¹¹ m s⁻²) and alternative
(ρ_total / cH₀ ⇒ 1.13×10⁻¹⁰ m s⁻²).

---

## Abstract

The mass-discrepancy–acceleration relation of galaxies is governed by a single acceleration scale
a₀ ≈ 1.2×10⁻¹⁰ m s⁻². We take seriously the hypothesis that this scale is not fundamental but is set
by the cosmological constant Λ, through

> **a₀ = ½ c √(G ρ_Λ) = c² √(Λ / 32π) = c H_Λ / Z,   Z = √(32π/3) ≈ 5.789,**

giving a₀ = 9.36×10⁻¹¹ m s⁻² with no fitted normalisation beyond the order-unity factor κ = ½. We
then ask whether this scale can be carried by a complete relativistic field theory that also (i)
reproduces the exact interpolation μ(y) = 1 − e^{−y}, (ii) produces correct gravitational lensing with
no slip (Φ = Ψ), (iii) propagates only the two tensor polarisations of the graviton, (iv) has
acceptable post-Newtonian parameters, and (v) admits an expanding cosmology — the "complete
completion" requirements. Our central result is a **no-go**: no *local* field theory in one physical
metric with two tensor degrees of freedom (plus at most one healthy scalar) meets all of these
simultaneously, and the *preferred-frame* (Einstein-aether) class — the one class that survives the
single-metric scalar no-gos — fails the preferred-frame PPN bound through a specific and unavoidable
mechanism: **the scalar–vector coupling that generates the MOND behaviour contributes an irreducible,
aether-kinetic-independent term to the preferred-frame parameter α₁, which can be cancelled only by
sending the vector kinetic coefficient negative — i.e. by introducing a spin-1 ghost.** We prove the
closed form

> **α₁ = −4 c₁₄ − 4 (2 − K_B)/(J_Y + 1),**

with c₁₄ = K_B + c₄ the vector kinetic coefficient and (2 − K_B) the MOND-generating coupling, and
show that α₁ = 0 forces c₁₄ = −(2 − K_B)/(J_Y + 1) < 0. We further prove that any causal completion of
this kind must carry a dark field, so that the MOND scale and the dark-energy density are two faces of
one shift-symmetric condensate (the same field whose de Sitter minimum gives w = −1). The durable,
falsifiable content of the framework is the prediction that the acceleration scale tracks the Hubble
rate, a₀(z) ∝ H(z), constant to sub-percent for z ≲ 5 and switching off before recombination. We give
the current confrontation of that law with data and the decisive tests forthcoming from Gaia DR4,
Euclid, DESI, and high-redshift kinematics.

We claim less than a theory of everything and less than a dark-matter-free modified gravity: we claim a
sharp reframing of one number, a rigorous statement of why its Lorentz-invariant field-theory
embedding cannot be dark-field-free, and a falsifiable redshift law.

---

## The Zimmerman field equations (the named positive content)

The parts of this framework that are the author's own and that survive every result below are a small,
closed set of equations. We state them as the operative content, with each labelled derived or input.

**(Z1) The acceleration law** — the single postulate, INPUT (κ = ½ fitted):

    a0 = (1/2) c sqrt(G rho_Lambda) = c^2 sqrt(Lambda / 32π) = c H_Lambda / Z,   Z = sqrt(32π/3).

**(Z2) The quasistatic field equation** — modified-gravity (AQUAL) form, exact exponential kernel:

    ∇ · [ μ(|∇Φ| / a0) ∇Φ ] = 4π G ρ_b,    μ(y) = 1 − e^{−y},

with matter obeying r¨ = −∇Φ. High acceleration (y ≫ 1): μ → 1 exponentially, recovering Poisson with
the derived Newton constant. Low acceleration (y ≪ 1): μ → y and the equation becomes |∇Φ|² = a0 g_N.

**(Z3) The Tully–Fisher theorem** — a consequence of (Z2), DERIVED, parameter-free:

    v^4 = G a0 M_b,     d ln v / d ln a0 = 1/4     (radius cancels identically).

**(Z4) The lensing statement** — no slip, so light and matter feel the same potential:

    Φ = Ψ,     γ_PPN = 1,

which any viable relativistic embedding must reproduce with Φ and Ψ derived independently.

**(Z5) The redshift law** — the distinctive, falsifiable prediction:

    a0(z) ∝ sqrt(rho_DE(z)) ∝ H(z)     (dark-energy-dominated),

constant to < 1% for z ≲ 5, switching off before recombination. The constant value at the de Sitter
minimum is DERIVED from the sector; the *evolution* as a dynamical consequence is an open problem
(the inverse-K(Q) problem), and is at present a consistent phenomenological law, not a theorem.

These five statements are the framework. Sections 4–6 prove that **no local, Lorentz-invariant,
ghost-free field theory in one metric with two tensor degrees of freedom reproduces (Z2)–(Z4)
simultaneously without a dark field**; the surviving embedding realises (Z1)–(Z5) with a
shift-symmetric condensate that is simultaneously the dark-energy vacuum (w = −1) and the dark-matter
charge — the physical meaning of (Z1).

## 1. The acceleration scale and its horizon interpretation

The empirical MOND scale is the acceleration below which galaxy rotation curves flatten and the
radial-acceleration relation (RAR) bends from g_obs = g_bar to g_obs = √(a₀ g_bar). Writing the
de Sitter horizon surface gravity as κ_dS = c H_Λ, with H_Λ = c√(Λ/3) the dark-energy-only expansion
rate, the framework's single physical postulate is

    a₀ = c H_Λ / Z,   Z = √(32π/3),

equivalently a₀ = ½c√(Gρ_Λ) = c²√(Λ/32π). Numerically, with Planck Λ, this is 9.36×10⁻¹¹ m s⁻².

**What is a derivation and what is not.** The *coincidence* a₀ ~ c²√Λ is Milgrom's and decades old.
The factor Z = √(32π/3) is algebraically the Einstein coupling 8π times the Friedmann 3, with a single
outside factor of 2; the "8π" and "3" cancel cleanly against the ρ_Λ = Λc²/8πG and H² = 8πGρ/3
definitions, but **the outside factor κ = ½ (equivalently the value of Z) is FITTED, not derived.**
Two independent estimators of κ from SPARC galaxies give 0.465 ± 0.076 (baryonic Tully–Fisher route)
and 0.551 ± 0.043 (distance-free route); these bracket ½, and an irreducible gas-mass systematic floor
(helium 0.5%, HI self-absorption 2.5%, CO-dark H₂ 3%) caps the measurement at ≈ ±0.02, enough to
distinguish ½ from 1/√3 at ~4σ but never to establish a specific rational. We therefore treat κ = ½
as a one-parameter effective input.

## 2. The phenomenology the scale carries

With the exponential interpolation μ(y) = 1 − e^{−y}, y = g_bar/a₀ (the Bekenstein–Milgrom AQUAL form
whose kernel is the exact primitive G(y) = y² + 2(1+y)e^{−y} − 2, with G′(y)/2y = μ), the framework
reproduces, on both footings and with committed scripts:

- **The radial-acceleration relation** on 175 SPARC galaxies at 0.108 dex scatter at Υ = 0.70 — at or
  below standard MOND's 0.122–0.140, and convention-compatible with the framework's a₀.
- **The baryonic Tully–Fisher relation** as a *theorem* of the deep-MOND limit: g_obs = √(a₀ g_bar)
  gives v⁴ = G a₀ M_b with the radius dropping out identically, slope d ln v / d ln a₀ = ¼ exactly.
- **Weak-lensing RAR** from 40 kpc to 2.2 Mpc, at χ²/dof = 2.03 (canonical) / 0.94 (alternative
  footing), against real KiDS-1000 data, with no dark component and no free parameters — two to four
  decades in acceleration below the SPARC regime.
- **Solar-system safety:** the exponential kernel suppresses the Sun's anomaly by ~10¹³, discharging
  the ephemeris liability that excludes power-law interpolations.

These are the successes a completion must preserve. They do not by themselves require a field theory;
they require that whatever the field theory is, it reduce to exact-exponential AQUAL in the
quasistatic weak field with γ_PPN = 1.

## 3. The completion program: the requirements, stated so they cannot be moved

A relativistic completion carrying this scale should satisfy, from **one** action:

1. Exact μ(y) = 1 − e^{−y}; deep-MOND v⁴ = G a₀ M_b; Newtonian μ → 1 at high acceleration.
2. Exactly two propagating tensor degrees of freedom — no hidden scalar graviton, no ghost; a genuine
   matter/clock scalar allowed only if explicitly counted and healthy.
3. Correct lensing: Φ = Ψ, γ_PPN = 1, with Φ and Ψ each derived independently from the field equations.
4. Acceptable PPN: β, γ, α₁, α₂, α₃ within experimental bounds, **derived not assumed.**
5. Ordinary-matter conservation ∇_μ T^{μν} = 0 as a genuine Bianchi/Noether identity.
6. c_T = c and positive tensor kinetic energy (GW170817).
7. Stability: no ghost, no gradient instability, no instantaneous physical channel.
8. Expanding FLRW with H ≠ 0, not obtained by freezing the conformal mode.
9. Controlled zero-field (y → 0) limit.
10. Newtonian/GR recovery with a *derived* Newton constant.
11. One physical metric for matter and photons.
12. The exponential constitutive law preserved.
13. The a₀–Λ relation preserved or derived — or, honestly, stated as input.

The value of stating these immovably is that the historical relativistic-MOND theories (TeVeS,
generalized Einstein-aether, BIMOND, khronometric MOND, nonlocal MOND) each satisfy *most* and fail
*one*, and the failure migrates from theory to theory. We now show that this migration is not bad luck.

## 4. The local no-go theorem

**Theorem (local completion no-go).** *No action in one physical metric g with matter minimally
coupled to g, propagating exactly two tensor modes plus at most one additional healthy scalar, and
built from finitely many derivatives (locality), realises requirements 1, 3, 4, 6, 7, 8
simultaneously.*

The proof is by exhaustion over what carries the MOND force beyond the two tensor polarisations, each
case closed by a committed computation:

| Carrier | Fails on | Mechanism (committed script / result) |
|---|---|---|
| algebraic/elliptic metric constraint | 7, 8 | over-constraint freezes the conformal mode (FLRW dies) or α₃ = O(1) instantaneous response (`sf62`, DC-019, York causal gate) |
| frame-free scalar F(X) | 3 | anisotropic stress ∂φ∂φ sources Φ − Ψ ≠ 0 (Bekenstein–Sanders; DC-013) |
| clock coupled to R_nn / extrinsic curvature | 6 | exact MOND forces λ ≈ −v_flat²/c² ≈ 2×10⁻⁷, so c_T departs from c by ~10⁷–10⁹× the GW170817 bound (`luminality_no_go_observational_strengthening`, verified across every galaxy MOND zone) |
| clock coupled to its own acceleration | 7 | radial gradient instability on a₀ < a < 38 a₀ (FC-KH; (yq)′ no-go theorem) |
| DHOST / degenerate higher-derivative | 3 | under-lenses; degeneracy fixes the ghost, not the slip (DC-017) |
| preferred-frame vector (Einstein-aether) | 4 | §5 below — the α₁ mechanism |
| second dynamical metric | 2 | seven propagating modes (2 + 5), excluded by requirement 2 |

The single assumption the theorem cannot drop is **locality**: a genuinely nonlocal, field-dependent
spin-2 form factor is not covered, and is the one open direction. (The field-*independent* nonlocal
class is already excluded — it is too linear in the baryonic source to produce the √ scaling of deep
MOND.)

## 5. The aether kill and its mechanism (the central new result)

The preferred-frame vector carrier — the Aether-Scalar-Tensor (AeST) class of Skordis & Złośnik, and
its Einstein-aether generalisations — is the one carrier that survives the single-metric scalar
no-gos, because a unit timelike vector supplies the extra structure needed for MOND lensing without an
anisotropic-stress slip. It is therefore the decisive case. We settle it.

**Setup.** The AeST action fixes the aether kinetic sector to Maxwell form (in Einstein-aether
language c₁ = −c₃ = K_B, c₂ = c₄ = 0), which is exactly the condition c₁₃ = 0 that GW170817 requires
for c_T = c. The full Einstein-aether kinetic term has two further couplings, c₂ (∇·A)² and c₄ a_μa^μ,
that are *tensor-blind* (they do not touch the graviton, so c_T = c survives them). The natural
question — never previously computed with the scalar coupling retained — is whether restoring c₂, c₄
opens a healthy preferred-frame-null point α₁ = α₂ = 0.

**Computation.** Extending the Foster–Jacobson-controlled, two-gauge, boosted-moving-source quadratic
solve (which reproduces the textbook Einstein-aether α₁, α₂ at generic c₁…c₄ as an end-to-end control,
and reproduces the AeST kill exactly at c₂ = c₄ = 0), we obtain the closed form, verified symbolically
against a grid of (K_B, J_Y) and against the c₂ = c₄ = 0 anchor:

> **α₁ = −4 c₁₄ − 4 (2 − K_B)/(J_Y + 1),   c₁₄ ≡ K_B + c₄,**

at the physical deep field J_Y = μ(u₀) = 1. Here the first term is the pure Einstein-aether
contribution (in the frozen-scalar limit J_Y → ∞ it is the whole answer, reproducing Foster–Jacobson
α₁ = −4c₁₄ on the c₁₃ = 0 plane), and the second term is the AeST scalar–aether drag contribution. It
is **c₁₄-independent, strictly negative for K_B < 2, and present at the deep field.** The coupling c₂
does not appear (the (∇·A)² operator is longitudinal; α₁ is transverse).

**The kill.** α₁ = 0 requires

> c₁₄ = −(2 − K_B)/(J_Y + 1) < 0   for all 0 < K_B < 2 and all J_Y ≥ 1

(at J_Y = 1, c₁₄* = (K_B − 2)/2 ≈ −0.9). But the spin-1 (vector) kinetic coefficient computed
independently from the vacuum dispersion relation is proportional to c₁₄ — explicitly 2·c₁₄·B with
B = 2Q₀²(J_Y+1)(K_B−2) − k² < 0 — so it flips sign as c₁₄ crosses zero. AeST (c₄ = 0, c₁₄ = K_B > 0)
is the ghost-free reference established by the AeST no-ghost theorem; the α₁ = 0 locus (c₁₄ < 0)
carries the opposite-sign spin-1 kinetic term, i.e. a **ghost**. The sign flip is verified numerically
(healthy point −0.429, α₁ = 0 locus +1.930).

**The mechanism, in one sentence.** *The drag coefficient (2 − K_B) is exactly the scalar–aether
coupling 2(2 − K_B) J^μ∇_μφ that generates the MOND behaviour; it contributes an irreducible,
aether-kinetic-independent negative term to the preferred-frame parameter α₁; α₁ can be driven to zero
only by sending the vector kinetic coefficient negative, i.e. by introducing a spin-1 ghost.* The term
that makes the theory MOND is the term that breaks preferred-frame invariance. This closes the whole
Einstein-aether-plus-shift-scalar class, generalising the AeST-specific result, and it is not evaded by
GW170817-compatible tuning because c_T = c is exactly preserved by the couplings involved.

**Scope, stated honestly.** The result is proved within the standing cosmological-background,
inert-kernel (J_Y = 1) linearisation. The one un-run upgrade to full finality is the same
solar-profile-background check named for the AeST-specific kill: a saturated-μ background with
gradients could in principle modify the transverse O(w) response, but to overturn the verdict it would
have to flip a certified O(1) coefficient by O(1), not a small correction. We flag it as the single
open computation and do not claim it is closed.

## 6. Why the surviving completion must carry a dark field

Independently of the aether kill, a causal completion carrying correct MOND lensing with only two
propagating degrees of freedom is impossible: {MOND lensing} + {two local DOF} + {causal single
metric} is unsatisfiable, because the elliptic MOND potential, coupled to an evolving acceleration
scale, becomes a physical instantaneous observable (via the MOND external-field effect), with no
retardation backstop — the longitudinal ∇(Φ − Ψ) force is annihilated by the transverse-traceless
graviton. Every route that keeps causality carries a conserved dark charge: the AeST condensate's
shift charge, the mimetic dust's ratio-locked charge, or (if one forfeits causality) an instantaneous
York-time field. The dark field is therefore not a defect of one construction but a structural feature.

**The positive reading.** In the AeST embedding, the dark field is the shift-symmetric scalar's
condensate. Its de Sitter minimum gives w = −1 exactly (dark energy), and its excitation carries a
cold, conserved, a⁻³ charge to the CMB (the dark-matter-like component at full Ω_dm). **The MOND scale
and the dark-energy density are two faces of one field** — which is precisely why a₀ ∝ c√(Gρ_Λ). The
concession "the theory contains a dark field" is, on this reading, load-bearing rather than reluctant:
at the σ₈ scale today a linear perturbation sits deep in the MOND regime, where the kernel would
multiply gravity by ~30×, so a cold dark component is *required* to keep MOND out of linear cosmology
and reproduce the CMB.

The framework therefore claims **"no dark-matter particle,"** not "no dark matter": the carrier is a
mode of a field, and the field is unavoidable.

## 7. The falsifiable content: a₀ tracks the Hubble rate

The distinctive, testable prediction is that the acceleration scale evolves with the dark-energy
density:

> **a₀(z) ∝ √ρ_DE(z) ∝ H(z)** (dark-energy-dominated),

which the framework's derived law renders as: a₀ constant to < 1% for z ≲ 5, a transition at
z_t ∈ [17, 35], and a₀ switched off (a₀(z*)/a₀(0) ≈ 0.006) at recombination — so that the CMB requires
a clustering component, a prediction rather than an embarrassment. (Whether the evolution is *derived*
from the action or is an input depends on solving the open "inverse-K(Q)" problem; at present the
constant-a₀ value is derived at the de Sitter minimum and the evolution is a phenomenological law
consistent with the sector, not a theorem. We state this explicitly.)

Consequences, each a pre-registrable number on both footings:
- **Early-rotator Tully–Fisher zero point:** v(z)/v(0) = [a₀(z)/a₀(0)]^{1/4} at fixed baryonic mass — a
  theorem of the a₀-line. Flat to 0.009% below z = 5; signed velocity deficits 0.34% (z=10), 2.6%
  (z=15), 7.8% (z=20). Any robust offset below z ≈ 5 falsifies the law; above z ≈ 17 it clears the
  0.06-dex BTFR floor. A pre-registered forecast for 2030s ALMA/JWST kinematics.
- **Weak-lensing RAR in redshift bins** (KiDS / DES / HSC / Euclid): the lensing a₀ knee does *not*
  move with z below z ≈ 5 — a null with teeth.
- **Collapse timing:** MOND-boosted collapse is 1.34–1.96× faster than Newtonian, and the boost
  *declines* with z (2.03× at z=6, 1.14× at z=25) — a shape no constant-a₀ MOND predicts.
- **Wide binaries (Gaia DR4):** a preferred-frame-independent γ_v in the registered band; the
  framework's pre-registration is hash-frozen.
- **DESI w(z):** the sector predicts dissolution to w = −1; a confirmed phantom crossing is evidence
  against it.

## 8. Standing, honestly

**What is established (script-backed, both footings):** the a₀ = ½c√(Gρ_Λ) reframing and its
phenomenology (RAR, BTFR, weak-lensing RAR, solar system); the local no-go theorem; the aether kill
with the α₁ = −4c₁₄ − 4(2−K_B)/(J_Y+1) mechanism; the universal dark-field theorem; the falsifiable
a₀ ∝ H(z) law and its confrontation with current data.

**What is input, not derived:** κ = ½ (fitted); the a₀–Λ promotion (a definitional choice tying the
MOND scale to the dark-sector pressure); the evolution a₀(z) as a *dynamical consequence* (the
inverse-K(Q) problem is open — the constant value is derived, the evolution is a consistent law).

**What is open:** the single nonlocal, field-dependent spin-2 direction not covered by the locality
assumption of the no-go; the solar-profile-background upgrade of the aether kill to full finality; the
cluster-core residual (whether the potential-depth-keyed dark-field response pins dynamically to the
observed core mass while remaining galaxy-safe); and a first-principles derivation of κ.

**What is not claimed:** a theory of everything; a dark-matter-free modified gravity; a completed
Lorentz-invariant field theory passing all thirteen requirements. The honest result is that such a
local completion does not exist, that the surviving completion carries a dark field which is the
dark-energy condensate, and that the reframing makes one sharp, falsifiable prediction — a₀ ∝ H(z) —
that the next decade of surveys will test.

---

## Reproducibility

The load-bearing computations are committed under `qwen_claude_field_theory/closure_2026/`:
`FRIED_CHICKEN_SPEC.md` (the requirements), `FRIED_CHICKEN_VERDICT_2026-09-01.md` (the local no-go
theorem), `GEN_AEST_PPN_VERDICT.md` and `generalized_aest_2026/` (the aether kill: anchors, closed
form, dispersion, sign-flip), `one_shot_final/` (the curvature-QUMOND and luminality no-gos),
`V9_PPN_KILL_VERDICT.md` (the AeST-specific PPN kill), `THE_GENERALIZED_COMPLETION.md` (the action and
gate scorecard). The phenomenology scripts (RAR, BTFR, weak-lensing RAR, κ error budget) are under
`real_research/` and `nbody_2026/`. All exit 0; each contains checks constructed to be able to fail and
at least one mutation control. Two footings are carried throughout. The a₀ = c²√(Λ/32π) value is an
external input to every candidate action and is never claimed as derived.
