# Paper I — An explicit aether-scalar-tensor realization of an evolving MOND scale

> **⚠️ COEFFICIENT-FOOTING CORRECTION (2026-06-13):** Any "a₀ = cH₀/Z", "1/Z = 0.173 against cH₀", or "1/Z bracketed by Milgrom 1/2π / Verlinde 1/6" below uses the **superseded footing**. Canonical: a₀ = c²√(Λ/32π) = cH_Λ/Z = 9.36×10⁻¹¹ (ρ_DE; cH_Λ = √Ω_Λ·cH₀ = 0.83·cH₀). The coefficient 1/Z = 0.173 is against **cH_Λ**; against cH₀ it is **0.143**. Milgrom (0.159) and Verlinde (0.167) use cH₀, so the apt comparison is 0.143 — the **low outlier**, NOT bracketed. cH₀/Z = 1.13×10⁻¹⁰ is the ρ_total reading (+20%). See [THE_A0_COEFFICIENT_CONVENTION.md](THE_A0_COEFFICIENT_CONVENTION.md) + [THE_A0_COEFFICIENT_AUDIT_2026-06-13.md](THE_A0_COEFFICIENT_AUDIT_2026-06-13.md).


**Carl Zimmerman** · June 2026 · *full pedagogical write-up · companion to Paper II (the CMB-safety theorem)*

---

## Abstract

Modified Newtonian Dynamics (MOND) replaces dark matter at galaxy scales with a single
acceleration constant, a₀ ≈ 1.2×10⁻¹⁰ m s⁻². For forty years it has been noticed that this
scale is numerically close to the cosmic acceleration cH₀, and Milgrom (2014) suggested that if
the connection is physical, a₀ should *evolve* with cosmic time. This paper writes that idea down
explicitly as a covariant field theory. We take the Aether–Scalar–Tensor theory (AeST) of
Skordis & Złošnik (2021) — the one relativistic version of MOND that fits the microwave
background — and promote its fixed acceleration constant to a *dynamical function of the aether's
expansion*, a₀ → a₀(θ) = cθ/(3Z), where θ = ∇·A. On a cosmological background θ = 3H exactly, so
a₀(z) = cH(z)/Z = a₀(0)E(z) emerges as a field equation rather than an assumption. Inside a
galaxy the same θ stays ≈ 3H(z), so the local dynamics recover standard MOND with the
epoch-appropriate scale. The construction is honest about its boundaries: the coefficient Z is a
chosen O(1) number, the physical idea is Milgrom's, and the host theory is Skordis & Złošnik's.
What is new is the explicit, minimal coupling that turns "a₀ evolves" into a definite Lagrangian.

---

## 1. Introduction — the problem this paper solves

### 1.1 MOND and its one number
Spiral galaxies rotate too fast at their edges for the gravity of their visible matter. The
standard fix is invisible **dark matter**. MOND takes a different route: it says that *below a
critical acceleration* a₀, Newton's law is modified, so that the gravitational acceleration g felt
by a star is larger than GM/r² would predict. Empirically, in the "deep-MOND" regime (g ≪ a₀) the
observed acceleration is g = √(g_N a₀), where g_N = GM/r² is the Newtonian value. This one rule,
with one constant a₀, reproduces the rotation curves of 175 galaxies (the SPARC sample) with
remarkable accuracy.

### 1.2 The cosmic coincidence
The number a₀ ≈ 1.2×10⁻¹⁰ m s⁻² is suspiciously close to the **cosmic acceleration** cH₀ ≈
6.5×10⁻¹⁰ m s⁻² (the speed of light times the Hubble expansion rate). Specifically a₀ ≈ cH₀/6.
Milgrom noted this in 1983. If it is not an accident, then a₀ — a *galaxy-scale* quantity — is set
by the *whole universe's* expansion rate. That is a deep, Machian-sounding idea: local dynamics
fixed by global cosmology.

### 1.3 The sharp consequence: a₀ must evolve
The Hubble rate is not constant — it was larger in the past, when the universe was denser. So if
a₀ tracks cH, then **a₀ was larger in the past too**. Writing it through the matter and dark-energy
content (the function E(z) ≡ √(Ω_m(1+z)³ + Ω_Λ), where z is redshift),

> **a₀(z) = a₀(0)·E(z).**

This is Milgrom's 2014 proposal. It is the one distinctive, falsifiable consequence of taking the
coincidence literally. By z = 6 (when the universe was ~1 Gyr old), a₀ would be ten times its
present value.

### 1.4 What is missing — and what this paper supplies
The relation a₀(z) = cH(z)/Z is, so far, just a rule about a number. To be physics it must come
from an **action** — a covariant Lagrangian whose field equations *produce* an evolving a₀, that
is consistent with the cosmic microwave background (CMB), and that reduces to ordinary MOND inside
galaxies. **This paper provides exactly that:** the minimal modification of an existing,
CMB-tested relativistic-MOND theory that makes a₀ evolve. Paper II then proves the construction
does not spoil the CMB.

---

## 2. Background — the host theory (AeST), explained

### 2.1 Why a plain scalar field is not enough
The natural way to make MOND relativistic is to add a scalar field φ whose gradient supplies the
extra "MOND" acceleration. Early theories (e.g. TeVeS) did this but failed: they either made
gravitational waves travel at the wrong speed (ruled out by the 2017 neutron-star merger
GW170817) or got the third peak of the CMB wrong.

### 2.2 The AeST fields
Skordis & Złošnik (2021) solved this with three ingredients:
- the **metric** g_μν (ordinary gravity);
- a **scalar** φ (supplies the MOND gradient);
- a **unit-timelike vector** A_μ — the "aether" — constrained so that A^μA_μ = −1 everywhere.

The aether is the key new object. Physically it picks out, at every point, a preferred
"time direction" — the local cosmic rest frame. On the cosmological background it simply points
along cosmic time.

### 2.3 The action and where a₀ lives
The AeST action (their Eq. 5) is, schematically,

$$
S = \int d^4x \frac{\sqrt{-g}}{16\pi\tilde G}\Big[R - \tfrac{K_B}{2}F^{\mu\nu}F_{\mu\nu}
 + 2(2-K_B)J^\mu\nabla_\mu\phi - (2-K_B)\mathcal Y - \mathcal F(\mathcal Y,\mathcal Q)
 - \lambda(A^\mu A_\mu + 1)\Big] + S_m[g],
$$

where R is the usual curvature, F_μν = 2∇_[μA_ν] is the aether's "field strength," λ is a
Lagrange multiplier enforcing the unit constraint, and 𝓕 is a **free function** of two scalars:

- **𝒴 = q^{μν}∇_μφ∇_νφ**, with q_{μν} = g_{μν} + A_μA_ν — this projects out the time direction and
  keeps only the **spatial** gradient of φ. *This is the MOND/galaxy sector.*
- **𝒬 = A^μ∇_μφ** — the part of φ's gradient **along** the aether (its time-derivative). *This is
  the cosmological/dark-matter-mimicking sector.*

The acceleration constant a₀ appears in the MOND sector. As the spatial gradient gets small, the
free function approaches

$$\mathcal F \to \frac{2\lambda_s}{(1+\lambda_s)\,a_0}\,\mathcal Y^{3/2},$$

i.e. **a₀ is the coefficient of the 𝒴^{3/2} term.** Meanwhile the cosmological sector is governed
by a separate function 𝒦(𝒬) = −2Λ + 𝒦₂(𝒬−𝒬₀)² + …, which makes φ's energy density behave like
cold dark matter (∝ a⁻³) and supplies the cosmological constant Λ. Crucially, **𝒦(𝒬) contains no
a₀.** The galaxy scale and the cosmological dust mode live in *different arguments of the free
function.* (This separation is what Paper II exploits.)

---

## 3. The construction — promoting a₀ to the aether expansion

### 3.1 The idea
We want a₀ to become a *field* that equals cH(z)/Z on the background. The aether already carries a
natural candidate: its **expansion scalar**

$$\theta \equiv \nabla_\mu A^\mu,$$

the rate at which the aether congruence spreads apart — exactly analogous to how a gas of
free-falling particles expands. We therefore replace the constant a₀ by

> **a₀ → a₀(θ) = cθ/(3Z),  Z = 2√(8π/3) ≈ 5.789.**

This is the *entire* modification. No new field is introduced — θ is built from A_μ, which is
already in the action. It is the minimal covariant way to make a₀ dynamical.

### 3.2 Why this is the right object
θ is a *local* scalar, but on cosmological scales it knows about the *global* expansion (we show
θ = 3H next). So coupling a₀ to θ realizes the Machian idea — local dynamics fixed by the global
state — through a genuinely local field. There is no action at a distance.

---

## 4. The cosmological limit — the evolution falls out

On a Friedmann–Robertson–Walker (FRW) background, the aether points along cosmic time,
A^μ = (1,0,0,0), and its expansion is computed from

$$\theta = \frac{1}{\sqrt{-g}}\,\partial_\mu(\sqrt{-g}\,A^\mu) = \frac{1}{a^3}\,\partial_t(a^3) = 3\frac{\dot a}{a} = 3H.$$

This is **exact** — no approximation. (We verified it symbolically; see `theta_3H_coupling.py`.)
Substituting into the coupling,

> **a₀(z) = c·θ/(3Z) = cH(z)/Z = a₀(0)·E(z).**

So the evolving scale is not assumed — it is the value the field a₀(θ) takes when the field
equations are solved on the cosmological background. This is the central payoff of the
construction: **"a₀ evolves as E(z)" has become a theorem about a Lagrangian.**

---

## 5. The galaxy limit — does a galaxy see 3H?

A subtlety could ruin everything. Inside a galaxy the gas is bound, not expanding. If the aether
were dragged into the galaxy's static rest frame, its local expansion θ would drop to ≈ 0, and
then a₀ = cθ/3Z would vanish — no MOND at all. So we must check what θ a galaxy actually sees.

We compute θ to first order in the weak gravitational field (longitudinal gauge, with potentials
Ψ and Φ, and a small aether peculiar flow **B**). The result (derived in full in
`theta_3H_coupling.py`) is

$$\theta = 3H \;-\;3H\Psi \;-\;3\dot\Phi \;+\;\nabla\!\cdot\!\mathbf{B}.$$

The leading term is the **background** 3H — it comes from the expansion of the cosmic background
the galaxy is embedded in, *not* from any local motion. The corrections are tiny:
- −3HΨ: Ψ is the Newtonian potential, ~10⁻⁶ in a galaxy, so this term is ~10⁻⁶ × 3H — negligible;
- −3Φ̇: zero for a static (non-evolving) galaxy;
- ∇·**B**: the divergence of the aether's peculiar flow, ≈ 0 for a virialized, non-expanding system.

So a galaxy at epoch z sees **θ ≈ 3H(z) to about one part in a million.** The cosmic expansion
threads right through the bound system; it is *not* screened. The coupling therefore delivers
a₀ ≈ cH(z)/Z exactly where rotation curves are measured, and the φ-sector reduces to the standard
Bekenstein–Milgrom equation with the epoch-appropriate scale:

$$\nabla\!\cdot\!\big[\mu(|\nabla\phi|/a_0(z))\,\nabla\phi\big] = 4\pi G\rho_b,\qquad v^4 = G M\,a_0(z).$$

*(The leftover ∇·**B** term is small here, but it is exactly where the External Field Effect lives
— a system embedded in a coherent large-scale flow feels an environmental correction. That is a
genuine, separate prediction; see §6.)*

---

## 6. What the construction predicts

Because every deep-MOND relation scales with a₀(z) = a₀(0)E(z), the model makes a coherent set of
predictions for high-redshift galaxies:

| quantity | scaling | by z = 6 |
|---|---|---|
| dynamical-to-baryonic mass ratio | ∝ √E(z) | ×3.2 |
| rotation/dispersion velocities | ∝ E(z)¼ | +80% |
| baryonic Tully–Fisher zero-point | ∝ −log E(z) | −1.0 dex |
| MOND/characteristic radius | ∝ 1/√E(z) | ÷3.2 |
| critical surface density | ∝ E(z) | ×10 |

**One genuinely distinctive prediction.** The standard MOND External Field Effect — a system in an
external field g_ext has its deep-MOND behaviour suppressed by the ratio η = g_ext/a₀ — now
*weakens with redshift*, because a₀(z) grows: η ∝ 1/E(z). So high-z galaxies in dense environments
should behave more like *isolated* deep-MOND systems. This differs from both ΛCDM (no host effect
on internal dynamics) and constant-a₀ MOND (constant effect). It is the model's clearest
falsifiable signature.

---

## 7. Honest status and boundaries

Stating the limits is what keeps the result trustworthy:
- **The physics is Milgrom's.** a₀ ≈ cH₀ (1983) and the evolving a₀ ∝ cH (2014) are his ideas;
  this paper supplies a covariant *realization*, not a new physical principle.
- **The coefficient Z is a posit.** The factor of 2 in Z = 2√(8π/3) is a chosen O(1) number; it is
  not derived (a companion analysis shows it sits in the de Sitter cluster ~6 but is not pinned by
  any horizon/entropy argument). The falsifiable prediction is *Z-independent*, so this costs the
  testable content nothing.
- **The data are suggestive, not conclusive.** Fitting a₀(z) ∝ E(z)^p to current measurements gives
  p = 0.80 ± 0.17; constant a₀ is disfavoured at ~2σ once inter-method systematics are folded in.
  A hint, not a detection.
- **The amplitude is degenerate with ΛCDM.** Hydrodynamic simulations reproduce a rising
  *apparent* a₀, so the amplitude alone does not discriminate; the distinguishing test is the EFE
  evolution (§6) on extended high-z galaxies.
- **The CMB is the crucial consistency check** — addressed in Paper II, which proves the running a₀
  leaves the *linear* CMB exactly invariant (the second-order effect is estimated small but
  remains open).

---

## 8. Conclusion

We have written the evolving MOND scale as an explicit covariant field theory: AeST with its
acceleration constant promoted to the aether expansion, a₀ = cθ/3Z. On the cosmological background
this yields a₀(z) = cH(z)/Z = a₀(0)E(z) as a field equation; inside galaxies the same θ stays
≈ 3H(z), recovering standard MOND with the epoch-appropriate scale; and the construction makes a
coherent set of high-redshift predictions, one of which (the redshift-weakening External Field
Effect) is genuinely distinctive. The idea is Milgrom's and the host theory is Skordis &
Złošnik's; the contribution here is the minimal, explicit coupling that turns the words "a₀
evolves" into a definite Lagrangian — and a thing one can test.

---

### References
- Milgrom, M. 1983, ApJ 270, 365 (MOND).
- Milgrom, M. 2014, Phys. Rev. D 91, 044009; arXiv:1412.4344 (cosmological variation of a₀).
- Skordis, C. & Złošnik, T. 2021, Phys. Rev. Lett. 127, 161302; arXiv:2007.00082 (AeST).
- McGaugh, Lelli & Schombert 2016, PRL 117, 201101 (SPARC).
- Famaey, B. & McGaugh, S. 2012, Living Rev. Relativity 15, 10 (MOND review; External Field Effect).

*Reproducibility:* `reviews/theta_3H_coupling.py` (θ = 3H on FRW; the galaxy anti-screening),
`reviews/GEOMETRIC_ACTION_theta_coupling.md` (the action and its limits). Companion: **Paper II**
(the δq⁰⁰ = 0 linear-CMB-safety theorem).
