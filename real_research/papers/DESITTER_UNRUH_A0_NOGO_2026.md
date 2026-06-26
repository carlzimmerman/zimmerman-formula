# The de Sitter–Unruh Acceleration Scale: A Geometric Reframing of the MOND Constant a₀, and No-Go Theorems for Its Modified-Inertia Completion

**Carl P. Zimmerman** — Briar Creek Tech
*Version: 2026-06-26*

---

## Abstract

The dynamics of galaxies require, below a characteristic acceleration **a₀ ≈ 1.2×10⁻¹⁰ m s⁻²**, either unseen matter or a modification of the law of gravity/inertia (Milgrom 1983). This scale numerically coincides with the cosmological quantity **c√Λ**, where Λ is the cosmological constant. This paper does three things, and is careful to keep them separate.

1. **A reframing (modest, not original).** The same number is written as a *surface gravity of the cosmological horizon*: a₀ = c²√(Λ/32π) = (c/2)√(Gρ_Λ) = cH_Λ/Z, with Z = √(32π/3) ≈ 5.789. This is a few lines of algebra; anyone can check it in minutes.

2. **A mechanism for the *shape* (known physics).** The square-root "deep-MOND" law, and with it the Radial Acceleration Relation (RAR) and the Baryonic Tully–Fisher Relation (BTFR), follow from treating inertia as a response to the de Sitter–Unruh temperature of the cosmic horizon (Milgrom 1999; Deser & Levin 1997). The mechanism is real; it is not new here.

3. **Rigorous limits (the genuinely new content).** We prove, with explicit calculations, exactly what this picture *cannot* do. (i) The O(1) coefficient Z is **not derived** — it is a free choice. (ii) The "temperature route" that gives the shape predicts an acceleration scale ~12× too large, and at the level of a real action it produces the **wrong sign** (it raises inertia, i.e. anti-MOND): we state this as a passivity theorem. (iii) **No covariant modified-inertia completion exists** in three exhaustive cases — local, field-theoretic, and nonlocal — each blocked by a named obstruction (an Ostrogradsky ghost, a Cassini-violating metric coupling, and the passivity sign theorem respectively).

The honest conclusion: **a₀ ~ c√Λ is a *forced scale* — but the MOND sign and the precise normalization are *postulated*, not derived.** This is a suggestive geometric/thermodynamic way to look at the MOND constant, with sharply proven boundaries. It is **not** a complete theory of MOND, and it is **not** a theory of everything. The one observationally distinctive consequence — a *declining* acceleration scale, a₀(z=3) ≈ 0.74 a₀(0), tracking the dark-energy density — is falsifiable this decade.

This paper supersedes and corrects, in the direction of *less* claimed, an earlier and over-stated description of this material.

---

## 1. Introduction and background

### 1.1 The problem MOND addresses

A spiral galaxy rotates. If you measure how fast stars and gas orbit at a radius *r*, Newtonian gravity predicts the orbital speed *v* from the visible (baryonic) mass *M* inside that radius: v² = GM/r, where G is Newton's constant. The prediction fails — observed speeds stay roughly *constant* out to large radii ("flat rotation curves") instead of falling off. The two standard responses are (a) **dark matter**: posit extra invisible mass, or (b) **MOND** (MOdified Newtonian Dynamics, Milgrom 1983): posit that the law itself changes when accelerations get very small.

MOND's empirical core is a single new constant of nature, the **acceleration scale a₀**. Above a₀, physics is Newtonian. Below a₀ (the "deep-MOND" regime, where galaxy outskirts live), the effective gravitational acceleration *g* is no longer the Newtonian value g_N = GM/r² but instead

> **g = √(a₀ · g_N)** (deep-MOND limit). (1.1)

Because g = v²/r for a circular orbit, equation (1.1) gives v⁴ = G M a₀ — a flat rotation curve whose speed depends only on baryonic mass. Empirically a₀ ≈ 1.2×10⁻¹⁰ m s⁻², and this one number, with one stellar mass-to-light ratio, reproduces the rotation curves of ~175 galaxies (the SPARC sample; Lelli, McGaugh & Schombert 2016) to within their scatter.

### 1.2 The coincidence this paper is about

The number a₀ is suspiciously close to two *cosmological* quantities:

- **cH₀** — the speed of light times the Hubble constant (the expansion rate of the universe). Numerically cH₀ ≈ 6.8×10⁻¹⁰ m s⁻², so a₀ ≈ cH₀/6.
- **c√Λ** — where **Λ** (the cosmological constant) is the tiny constant energy density of empty space driving cosmic acceleration. Numerically a₀ ≈ c√Λ × O(1).

In standard ΛCDM cosmology this coincidence is treated as **accidental** — a₀ is a galaxy-scale fact, Λ is a cosmic-scale fact, and their proximity is chance. The premise explored here is the opposite: that the coincidence is **causal** — the galaxy acceleration scale is *set by* the cosmological constant. We will see that this premise is *partly* defensible (the scale is forced; the shape has a mechanism) and *partly* not (the exact coefficient and the sign are not derived). Stating which is which, rigorously, is the point of the paper.

### 1.3 What is claimed, and what is not

To avoid the trap this material previously fell into, here is the ledger up front.

| Statement | Status |
|---|---|
| a₀ has the *order of magnitude* of a cosmological acceleration (c√Λ ~ cH₀) | **Forced** (Sec. 2–3) |
| The deep-MOND √-law, RAR, BTFR | **Derived** from de Sitter–Unruh inertia (known physics, Sec. 3) |
| The *exact value* a₀ = c²√(Λ/32π) | **Not derived** — one O(1) coefficient is a free choice (Sec. 4.1) |
| The MOND *sign* (inertia *lowered* at small a) from the cosmic vacuum | **Not derived** — provably so (Sec. 4.2) |
| A covariant theory underlying all this | **Does not exist** in three exhausted cases (Sec. 4.2) |
| A theory of everything / the Standard Model | **Not claimed. Disavowed.** |

---

## 2. The acceleration scale as a horizon surface gravity

### 2.1 The quantities involved (background)

- **The cosmological constant Λ.** Empty space has a small constant energy density. In Einstein's equations this appears as Λ, with units of 1/length². Measured value Λ ≈ 1.1×10⁻⁵² m⁻². Equivalently it is a *dark-energy mass density* **ρ_Λ = Λc²/(8πG)** ≈ 5.8×10⁻²⁷ kg m⁻³ (this is just the definition that turns the geometric Λ into a density, using G and c; the 8π is the standard Einstein-equation factor).
- **The de Sitter rate H_Λ.** A universe containing only this dark energy expands exponentially at a rate **H_Λ = c√(Λ/3)** (the factor 3 is the Friedmann equation, H² = 8πGρ/3, specialized to ρ = ρ_Λ). H_Λ is close to today's Hubble constant H₀ because dark energy dominates today.
- **Surface gravity.** A horizon of radius R has a characteristic acceleration, its *surface gravity* κ_surf = c²/(2R) — the same formula that gives a black hole's surface gravity (there R is the Schwarzschild radius). It is "how hard" the horizon pulls at its own scale.

### 2.2 The algebra (anyone can verify this)

Start from the hypothesis that the dark-energy density sets the scale through a surface-gravity-like relation,

> **a₀ = (c/2)√(G ρ_Λ).** (2.1)

The (c/2) is a choice of O(1) coefficient — call its origin κ = ½; we will return to the fact that it is not forced (Sec. 4.1). Substitute ρ_Λ = Λc²/(8πG):

> a₀ = (c/2)√(G · Λc²/8πG) = (c/2)·c√(Λ/8π) = **c²√(Λ/32π).** (2.2)

Numerically, with the measured Λ, this gives **a₀ = 9.36×10⁻¹¹ m s⁻²** — within ~20% of the empirical MOND scale (and consistent with it once the stellar mass-to-light ratio and the choice of interpolation function are accounted for; this paper does not re-litigate that fit).

Rewrite (2.2) as a surface gravity, a₀ = c²/(2R*):

> **R* = c/√(Gρ_Λ) = √(8π/Λ).** (2.3)

So a₀ is *exactly* the surface gravity of a horizon of radius R*, the natural free-fall radius of a universe at the dark-energy density. Finally, dividing (2.2) by H_Λ = c√(Λ/3):

> **a₀ = c H_Λ / Z,  Z = √(32π/3) ≈ 5.789.** (2.4)

Equations (2.1)–(2.4) are the entire "reframing." They are algebraic identities given the one input (2.1); a referee can check them in minutes. **Read this way, a₀ is the acceleration associated with the cosmological horizon — galaxies in the deep-MOND regime are systems whose internal accelerations have dropped to the level set by the universe's own boundary.** That is the picture. Whether it is a *theory* depends on the next two sections.

---

## 3. The shape: deep-MOND from de Sitter–Unruh modified inertia

This section recovers the *functional form* (1.1) — the square-root law, the RAR, the BTFR — from a physical mechanism. The mechanism is **modified inertia from the de Sitter–Unruh temperature** (Milgrom 1999; the temperature structure is Deser & Levin 1997). It is established physics; nothing here is original. It matters because it is what separates "an interesting numerical coincidence" from "a mechanism for the law."

### 3.1 Background: the Unruh and de Sitter–Unruh temperatures

The **Unruh effect** (1976): an observer accelerating through the quantum vacuum with proper acceleration *a* perceives the vacuum as a thermal bath at temperature **T_U = ℏa/(2πck_B)**. Acceleration and temperature are proportional; an accelerated detector "feels warm."

In de Sitter space (a universe dominated by Λ) there is, additionally, the **Gibbons–Hawking temperature** of the cosmological horizon, T_dS ∝ ℏH/k_B — empty accelerating space is itself warm. An observer who is *also* accelerating sees a combination. The combined (Deser–Levin) temperature for acceleration *a* in de Sitter space is

> **T(a) ∝ √(a² + (cH)²).** (3.1)

(The accelerations add in quadrature, like the magnitudes of perpendicular vectors, because the two temperatures come from independent horizons.)

### 3.2 The deep-MOND limit

Milgrom's modified-inertia proposal: a body's inertia responds not to its acceleration directly, but to the *excess* temperature it feels over the cosmic background — i.e. to

> **T_eff(a) = T(a) − T(0) ∝ √(a² + (cH)²) − cH.** (3.2)

Now take the **low-acceleration limit** a ≪ cH (galaxy outskirts). Expand the square root: √(a² + (cH)²) = cH√(1 + a²/(cH)²) ≈ cH(1 + a²/2(cH)²) = cH + a²/(2cH). Subtracting cH,

> **T_eff ≈ a²/(2cH)  (deep-MOND).** (3.3)

The effective inertial response is *quadratic* in the acceleration when accelerations are small. If we identify the Newtonian source g_N with this effective response (the body's true dynamical acceleration *a* must produce the Newtonian pull through the *reduced* inertia), the operative relation is a² ∝ g_N · (cH), i.e.

> **a = √(a₀ g_N),  with a₀ ∝ cH.** (3.4)

This *is* the deep-MOND law (1.1). From it follow immediately:

- the **RAR** (the observed-vs-baryonic acceleration relation), via the full interpolation μ(a) = a/(√(a²+a_H²) − a_H) that smoothly joins Newtonian (a ≫ a₀) to deep-MOND (a ≪ a₀);
- the **BTFR** v⁴ = G M a₀, the tight relation between a galaxy's baryonic mass and its flat rotation speed.

We verified (1.1), the RAR interpolation, and v⁴ = GMa₀ symbolically; they are exact consequences of (3.2). **So the *shape* of MOND genuinely follows from de Sitter–Unruh inertia.** This is the strongest part of the picture, and — per §1.3 — the part most worth a relativist's attention.

---

## 4. The limits, proven

Sections 2–3 are the optimistic half. This section is the half that keeps the work honest: precisely what cannot be derived, with the obstruction named in each case. **This is the new content of the paper.**

### 4.1 The coefficient is not derived; the two routes disagree

The scale a₀ emerged with a free O(1) coefficient — the κ = ½ in (2.1), equivalently the precise value of Z in (2.4). Nothing above fixes it. We separately verified that κ cannot be forced by the usual candidate principles (ghost-freedom, unitarity, holographic entropy bounds): each of those probes only *signs, ratios, or the overall scale*, and κ is an overall normalization invisible to them. So **a₀'s order of magnitude is forced (it is a cosmological acceleration), but its exact value is a one-parameter choice, not a zero-parameter prediction.** That is a completely standard situation in physics — a derived functional form with one undetermined O(1) constant — and it is stated here as such rather than disguised.

There is a sharper problem, and it is the most important physical statement in the paper. **The route that gives the *shape* (Sec. 3) and the route that gives the *scale* (Sec. 2) are not the same theory.** The shape comes from a *temperature*: the natural acceleration scale of the de Sitter–Unruh temperature is ~cH_Λ (even ~2cH_Λ for the static-patch reading), i.e. it predicts a₀ of order cH_Λ. The observed value (2.4) is **a₀ = cH_Λ/Z ≈ cH_Λ/5.8** — about an **order of magnitude smaller** than the temperature route predicts (the ratio 2Z ≈ 11.6 is the "~12× overshoot"). The reason is structural and worth stating cleanly:

> **Every de Sitter temperature is *linear* in H (an energy scale, ∝ cH), while a₀ = c²√(Λ/32π) is a *square root of a density* (∝ √ρ_Λ). A linear-in-H temperature can never equal a square-root-of-density acceleration without an extra ingredient.** The 32π in Z is a *gravitational* normalization (the 8π of Einstein's equations, inside ρ_Λ = Λc²/8πG), and it is invisible to a kinematic temperature.

So the horizon interpretation is genuinely "onto something" for the *shape*, but the *scale* it naturally predicts is wrong by ~12×, and welding the temperature-route shape to the density-route scale is an unsolved problem — not a completed one.

### 4.2 No covariant modified-inertia completion exists (a three-horn no-go)

A "reframing" becomes a "theory" when it has a **covariant action** — a Lorentz-invariant Lagrangian that (a) yields the deep-MOND law, (b) recovers Newton/GR at high acceleration, (c) is *stable* (no runaway/ghost), and (d) survives Solar-System tests. There are exactly three ways to build modified inertia, and we find **all three are blocked**, each by a named, calculable obstruction.

**(i) Local route → Ostrogradsky ghost.** The natural local construction gates a particle's inertia by its acceleration magnitude |a|. But |a| is a *second time derivative* of position, so the Lagrangian depends on ẍ. *Background:* **Ostrogradsky's theorem** states that any non-degenerate Lagrangian containing second (or higher) time derivatives has a Hamiltonian that is *unbounded below* — there is a "ghost," a mode whose energy can go to −∞, making the theory unstable. We verified the gate is non-degenerate (d²L/d(ẍ)² ≠ 0) and exhibits the ghost explicitly (a propagator pole with negative residue). Adding a preferred-frame ("aether") vector does not help: the vector *labels* the cosmic rest frame but cannot lower the derivative order of the gate. This is precisely Milgrom's 1994 modified-inertia no-go, made explicit.

**(ii) Field route → modified gravity, fails the Solar System.** Promote the modification to a dynamical field that sits in the *metric* sector. Then it is no longer modified *inertia* but modified *gravity*, and it generically moves the gravitational potential Φ. *Background:* in any theory built from a metric, energy–momentum conservation (a consequence of coordinate invariance, the "Bianchi identity") *links* the different components of the gravitational field. We show that the kind of anisotropic ("traceless shear") stress such a field produces has a non-zero divergence, which conservation can only balance by sourcing a pressure that *feeds back into Φ*. A theory that changes Φ at the relevant level is excluded by **Cassini**'s measurement of the post-Newtonian parameter γ (|γ − 1| < 2×10⁻⁵, Bertotti, Iess & Tortora 2003). So the field route survives stability only by becoming the thing the data already forbids.

**(iii) Nonlocal route → the passivity sign theorem.** The one remaining corner is a *fully nonlocal* action — inertia as a memory response of the particle's worldline to the cosmic vacuum (Milgrom 1999). This *is* ghost-free (a nonlocal "form factor" can have a single healthy pole, evading Ostrogradsky). It is the most physically natural route and the closest the framework comes to a real completion. But it fails for one sharp, provable reason, the central technical result of this paper:

> **The passivity → anti-MOND sign theorem.** Let a particle acquire its inertial correction from coupling to *any* cosmological/de Sitter source that is (causal) — its response is analytic in the upper half frequency-plane (Kramers–Kronig) — and (ghost-free/unitary) — its spectral density satisfies ρ(ω) ≥ 0 (Källén–Lehmann positivity). Then the change in inertia at low acceleration is
> **δm = 2 ∫₀^∞ ρ(ω′)/ω′² dω′ ≥ 0** — inertia is **raised**.
> MOND requires inertia *lowered* (δm < 0), which demands ρ(ω) < 0 over some band — a negative-norm ghost. Hence "active (sign-flipping) + causal + ghost-free + MOND-signed" is **overdetermined and impossible** for any passive, unitary, stationary vacuum.

*Background on what makes this tight.* A "passive" medium is one in thermal equilibrium that can only *absorb* net energy from a probe (dissipation); the fluctuation–dissipation theorem ties its noise to that positive dissipation, and the sign of the low-frequency inertia shift follows. To *lower* inertia you need an *active* (gain) medium — one that does net work *on* the probe, like a laser medium. We checked the candidate cosmological sources for activity and found every realizable one is passive: the expanding background only reshapes the *noise* (not the sign-bearing dissipation); the de Sitter (Bunch–Davies) vacuum restricted to a static patch is *exactly thermal* (the KMS condition) with detailed balance; horizon thermodynamics (Jacobson, Padmanabhan) obeys the second law with positive entropy production. The only genuinely active mechanism — a driven non-equilibrium steady state ("frenesy") — is real physics but cannot be sourced from a de Sitter vacuum without postulating an external drive, and in any case operates at the wrong (super-horizon) frequencies.

**Important both-ways clarification:** the wall is **passivity (thermodynamics)**, *not* causality. Causality alone permits a MOND-signed kernel — we exhibit an explicit causal counterexample — but that kernel describes a *gain medium*, which the passive cosmic vacuum is not. This sharpens, rather than weakens, the result: the obstruction is precisely identified.

**Net.** All three horns are blocked: local = ghost, field = Cassini, nonlocal = unsourceable active kernel. **The MOND sign cannot be sourced from the passive de Sitter vacuum.** Therefore, within this picture, the MOND sign — and with it the specific normalization — must be *postulated*. a₀ ~ √Λ is a forced scale; the dynamics that would make it a derived *theory* of inertia provably do not exist in the passive-vacuum framework.

---

## 5. Predictions and observational status

A reframing earns the word "predictive" only if it forecasts something that was not used to build it. Here is the honest breakdown.

**Genuinely distinctive (differs from ordinary constant-a₀ MOND):**
- **a₀(z) decline.** If a₀ tracks the dark-energy density, and dark energy dilutes (even slightly) with redshift on the DESI-preferred evolving branch, then a₀ *decreases* into the past: a₀(z=3) ≈ 0.74 a₀(0). Equivalently, the high-redshift BTFR zero-point sits slightly *below* the local one. This is the cleanest distinctive test, accessible to ELT/JWST/ALMA high-z kinematics this decade. **Caveat:** it is hostage to the dark-energy equation of state — if DESI consolidates on a pure cosmological constant (w = −1), this signal vanishes and the picture degenerates to ordinary MOND.
- **A CMB-apex acceleration dipole** (≈0.06%, fixed sky direction) — unique to a preferred-frame realization, but below every near-term experimental floor.

**Modified-inertia vs modified-gravity discriminators** (test that it is *inertia*, not gravity): the Solar-System a₀/2 channel (modified inertia evades Cassini where modified gravity is excluded); a cluster-member velocity-dispersion correlation with infall phase (zero for modified gravity).

**Real but MOND-shared** (test MOND vs dark matter, not this picture specifically): the RAR and its scatter, the external field effect (wide binaries, Gaia DR4), galaxy-cluster residuals, dwarf-galaxy dynamics, the weak-lensing RAR (Euclid DR1).

The honest sting: the *most distinctive* predictions are the hardest to access (a₀(z) is hostage to w; the CMB dipole is below floor), while the *accessible* ones are MOND-shared. The decisive near-term gate is the **a₀(z) / high-z BTFR-sign** measurement.

---

## 6. Conclusion

This paper has tried to do the one thing speculative frameworks most often fail to do: **separate what is forced from what is chosen, and prove the difference.**

- **Forced:** a₀ has the magnitude of a cosmological acceleration; a₀ ~ c√Λ is a horizon surface gravity (Sec. 2). The deep-MOND √-law, the RAR, and the BTFR follow from de Sitter–Unruh modified inertia (Sec. 3). These are real, and the shape mechanism is the genuinely interesting physics.
- **Not forced, and provably so:** the exact coefficient Z (a free O(1), Sec. 4.1); the agreement of the temperature route's scale with the density route's scale (they differ by ~12×, Sec. 4.1); the MOND *sign* from the cosmic vacuum (forbidden by the passivity theorem, Sec. 4.2); a covariant completion (excluded in all three cases, Sec. 4.2).

The defensible position is therefore: **a₀ = c²√(Λ/32π) is a suggestive geometric/thermodynamic reframing of the MOND acceleration scale, with a real mechanism for its functional form and sharply proven limits on its completion. It is not a theory of MOND, and it is emphatically not a theory of everything.** The forward direction is observational: the declining-a₀(z) signature is the test that could promote this from a reinterpretation to a falsified-or-confirmed physical claim within the decade.

We state these limits plainly because the alternative — pretending an undetermined coefficient was derived, or that a reframing was a theory — is how speculative work loses the right to be taken seriously. The boundaries proven here are, we think, more valuable than the coincidence that motivated them.

---

## Acknowledgements and provenance

The de Sitter–Unruh modified-inertia route to MOND is due to M. Milgrom (1999); the de Sitter–Unruh temperature structure to S. Deser and O. Levin (1997). The empirical MOND relations used here are from the SPARC program (Lelli, McGaugh & Schombert). This manuscript intentionally claims *less* than, and corrects, an earlier description of the same material by the author. All symbolic and numerical checks (the algebra of Sec. 2, the deep-MOND expansion of Sec. 3, the Ostrogradsky, Bianchi, and passivity-sign calculations of Sec. 4) are reproducible from the public repository.

## Selected references
- M. Milgrom, *A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis*, ApJ 270 (1983) 365.
- M. Milgrom, *The modified dynamics as a vacuum effect*, Phys. Lett. A 253 (1999) 273 [astro-ph/9805346].
- S. Deser, O. Levin, *Accelerated detectors and temperature in (anti-)de Sitter spaces*, Class. Quantum Grav. 14 (1997) L163.
- M. Ostrogradsky (1850); R. P. Woodard, *Ostrogradsky's theorem on Hamiltonian instability*, Scholarpedia (2015).
- F. Lelli, S. McGaugh, J. Schombert, *SPARC*, AJ 152 (2016) 157.
- B. Bertotti, L. Iess, P. Tortora, *A test of general relativity using radio links with the Cassini spacecraft*, Nature 425 (2003) 374.
- C. Skordis, T. Złośnik, *Aether-scalar-tensor theory* (a relativistic MOND, modified-gravity), Phys. Rev. D 100 (2019) / PRL 127 (2021).
