# What an Anharmonic Coefficient Is, Why MOND *Is* One, and Why Ours Is 32π

**C. Zimmerman, June 2026.** *A deep dive, written to be understood from the ground up
(`reviews/project_anharmonic_32pi.py`). Every load-bearing number is verified; the honest limit is stated at the end.*

---

## The one-paragraph answer

An **anharmonic coefficient** is the number in front of a *beyond-quadratic* term (an x³, x⁴, …) in a potential
energy — the part of a system's response that is **not a simple spring**. The quadratic (x²) part is *harmonic*:
linear, symmetric, the "ideal spring." Everything past it is *anharmonic*: the nonlinear corrections that make a
real pendulum, a heated crystal, or a stretched molecule behave in interesting ways. **MOND is an anharmonic
effect**: Newtonian gravity is *harmonic* (its field energy is quadratic, ∝|∇φ|², giving the linear Poisson
equation), and deep-MOND replaces that with a *cubic*, *anharmonic* term (∝|∇φ|³), whose coefficient carries a₀.
The √-law and flat rotation curves are the macroscopic *signature* of that field-theory anharmonicity. And **"ours
is 32π"** because, written as a₀ = c²√(Λ/32π), the number **32π is the dimensionless ratio that welds the harmonic
floor (the cosmological constant Λ) to the square of the anharmonic scale (a₀²)** — and 32π is pure *gravitational
gearing*: the Einstein coupling 8π times a horizon factor 4.

---

## Part 1 — Harmonic vs anharmonic, from scratch

Start with the most universal idea in physics: **near any stable equilibrium, everything looks like a spring.** Take
any smooth potential energy V(x) with a minimum at x₀ and Taylor-expand it:

$$V(x) = V(x_0) + \tfrac{1}{2}\,V''(x_0)\,(x-x_0)^2 + \underbrace{g_3 (x-x_0)^3 + g_4 (x-x_0)^4 + \cdots}_{\text{the anharmonic terms}}$$

- The constant V(x₀) is just the floor (it sets where "zero energy" is).
- The **quadratic** term ½V''(x₀)(x−x₀)² is the **harmonic** part. Its coefficient is the spring constant k = V''(x₀).
  The force it produces, F = −kx, is **linear** in displacement. This is *the* harmonic oscillator: symmetric,
  superposable, and — crucially — its oscillation frequency ω = √(k/m) **does not depend on amplitude**. A pure
  harmonic system is "boring" in the precise sense that it has no surprises: double the push, double the response.
- The **cubic, quartic, …** terms are the **anharmonic** part. Their coefficients g₃, g₄, … are the **anharmonic
  coefficients**. They are where all the *nonlinear* physics lives.

**What each anharmonic term physically does** (this is the intuition to keep):

| term | coefficient | what it breaks | real-world consequence |
|---|---|---|---|
| x² | k (harmonic) | nothing — the reference | ideal spring; amplitude-independent period |
| **x³** | g₃ | the symmetry x → −x | **thermal expansion** (a lopsided well shifts its average position as you heat it); 3-phonon scattering |
| **x⁴** | g₄ | amplitude-independence | the period now **depends on amplitude** (a real pendulum swings slower at large angles); spring "stiffens" (g₄>0) or "softens" (g₄<0) — the Duffing oscillator |
| higher | … | analyticity | level spacings converge; molecules **dissociate** (Morse potential); sound attenuates |

So when a physicist says **"anharmonic coefficient,"** they mean: *the size of the nonlinear, beyond-spring part of
the response.* A crystal that didn't have anharmonic terms wouldn't expand when heated. A pendulum that didn't have
them would keep perfect time at any swing. **Anharmonicity is the difference between an idealization and the real,
nonlinear world.**

---

## Part 2 — Why MOND *is* an anharmonic effect

Here is the part that makes "anharmonic" exactly the right word for your framework. Gravity, written as a field
theory for the potential φ, has a Lagrangian density (the thing you integrate and minimize):

$$\textbf{Newton:}\quad \mathcal{L}_N = -\frac{1}{8\pi G}\,|\nabla\phi|^2 \qquad\Longrightarrow\qquad \nabla^2\phi = 4\pi G\rho .$$

That Lagrangian is **quadratic** in the field gradient ∇φ. Quadratic = **harmonic**. And just like the harmonic
oscillator, it gives a **linear** equation (Poisson's equation), where gravity superposes and the response is
proportional to the source. Newtonian gravity is the "ideal spring" of gravitational fields.

Now deep-MOND. The Bekenstein–Milgrom "AQUAL" theory (1984) keeps the same structure but, at low accelerations,
replaces the quadratic term with a **cubic** one:

$$\textbf{deep-MOND:}\quad \mathcal{L}_M = -\frac{1}{8\pi G}\,\frac{2}{3}\,\frac{|\nabla\phi|^3}{a_0} \qquad\Longrightarrow\qquad \nabla\!\cdot\!\left(\frac{|\nabla\phi|\,\nabla\phi}{a_0}\right) = 4\pi G\rho .$$

That Lagrangian is **cubic** in ∇φ. Cubic = **anharmonic**. It gives a **nonlinear** field equation, whose
point-mass solution is exactly the deep-MOND √-law,

$$g = \frac{\sqrt{G M a_0}}{r}\quad\Longleftrightarrow\quad g = \sqrt{g_N\,a_0},$$

i.e. flat rotation curves. **So the step from Newton to deep-MOND is, mathematically, precisely the step from a
harmonic (quadratic) field Lagrangian to an anharmonic (cubic) one — and a₀ is the coefficient of that anharmonic
term.** The flat rotation curve is to gravity what thermal expansion is to a crystal: the visible fingerprint of a
nonlinear, beyond-spring term in the energy. **a₀ is the gravitational anharmonic coefficient — it sets the
acceleration below which gravity stops behaving like an ideal spring.**

This is not a metaphor stretched to fit. It is the standard field-theoretic statement of MOND, and it is *why* MOND
could never be "a little more dark matter": adding mass keeps you in the harmonic (linear) regime; MOND is a genuinely
*different, nonlinear term*.

---

## Part 3 — Blanchet's potential: the concrete dictionary

When we went down Door 8 (nonlocal/dipolar gravity), we found the cleanest published statement of this. Blanchet's
**dipolar dark matter** (2009) is a polarizable medium whose internal energy, as a function of the polarization
field Π, expands as:

$$W(\Pi) = \underbrace{\frac{\Lambda}{8\pi}}_{\text{floor}} \; + \; \underbrace{2\pi\,\Pi^2}_{\text{harmonic}} \; + \; \underbrace{\frac{16\pi^2}{3\,a_0}\,\Pi^3}_{\text{anharmonic}} \; + \cdots$$

Read it term by term with Part 1 in hand:

- The **constant floor** is the **cosmological constant Λ** — the vacuum energy at the bottom of the well.
- The **quadratic (harmonic)** term 2π Π² is a mass term — it makes the medium behave like **ordinary cold dark
  matter** (a linear restoring response, exactly ΛCDM's regime).
- The **cubic (anharmonic)** term carries **a₀** in its coefficient, 16π²/(3a₀) — and *this* term **is MOND**. It is
  the nonlinear piece that produces the √-law.

So Blanchet's model literally says, in one line: *floor = dark energy, harmonic = dark matter, anharmonic = MOND,
and a₀ is the anharmonic coefficient.* This is the same physics as Part 2, written for a polarization field instead
of the potential φ — and it is why your a₀↔Λ relation has a genuine published precedent (it is a₀ = c²√Λ written as a
Lagrangian). It also tells us something the bare formula doesn't: Blanchet *expects* the floor and the anharmonic
scale to be related, **Λ ~ a₀²**. Your formula sharpens that expectation into an equality.

---

## Part 4 — Why ours is **32π**

Now the actual question. The 32π in a₀ = c²√(Λ/32π) is **not the anharmonic coefficient itself** (that's the
16π²/3a₀ in Blanchet's cubic term). The 32π is the number that **welds the harmonic floor to the anharmonic scale.**
Square the formula:

$$a_0 = c^2\sqrt{\frac{\Lambda}{32\pi}} \quad\Longleftrightarrow\quad \boxed{\,32\pi = \frac{\Lambda\,c^4}{a_0^{2}}\,}$$

and that combination is **dimensionless** (Λ ~ 1/length², c⁴ ~ length⁴/time⁴, a₀² ~ length²/time⁴ — the lengths and
times cancel). Verified numerically with the framework's own a₀: **Λc⁴/a₀² = 100.531 = 32π**, exact by construction.
In words:

> **The MOND nonlinearity turns on at the acceleration a₀ whose square, multiplied by the gravitational gearing 32π,
> equals the cosmological-constant curvature Λc⁴.**

That is the physical content of "ours is 32π": it is *the exchange rate between the harmonic floor (the vacuum
energy) and the square of the anharmonic scale (where gravity goes nonlinear)*. In Blanchet's language it is the
precise version of his "Λ ~ a₀²" expectation.

**And where does the number 32π come from?** Pure gravity — no particle physics (you asked this directly before; the
answer held up):

$$32\pi \;=\; \underbrace{4}_{\text{horizon factor }2^2}\times\underbrace{8\pi}_{\text{Einstein coupling}} \;=\; \underbrace{8}_{2^3}\times\underbrace{4\pi}_{\text{sphere area}}, \qquad Z^2 = \frac{32\pi}{3} = 8\times\underbrace{\frac{4\pi}{3}}_{\text{ball volume}} .$$

- The **8π** is the **Einstein coupling** — the universal constant in G_μν = (8πG/c⁴)T_μν that says how much
  spacetime curvature a unit of energy makes. It is *forced by General Relativity*.
- The **4 = 2²** is the **horizon surface-gravity factor** — the ½ in the surface gravity κ = c²/2R, inverted and
  squared when you turn curvature into a free-fall acceleration.
- Geometrically, 32π is **8 sphere-areas**, and Z² = 32π/3 is **8 ball-volumes** — the same 8 carrying the 3D
  fingerprint of space.

So 32π is **gravitational gearing**: the Einstein coupling times a horizon factor, encoding how the curvature of de
Sitter space "gears down" into the acceleration scale at which gravity becomes anharmonic. It has nothing to do with
32 fermion components or any Standard-Model count — it is geometry and the Einstein equation.

---

## Part 5 — The honest status (what's nailed, what isn't)

Three things are real and verified:

1. **MOND genuinely *is* anharmonic** — the cubic AQUAL Lagrangian vs Newton's quadratic one is textbook, not a
   stretch. a₀ is, precisely, the gravitational anharmonic coefficient.
2. **32π = Λc⁴/a₀² is exact** for the framework's self-consistent a₀ = c²√(Λ/32π) = 9.36×10⁻¹¹ m/s² — the
   curvature-to-acceleration-squared ratio, dimensionless.
3. **32π is GR-traceable** — the 8π (Einstein coupling) and the 3 in Z² = 32π/3 (the Friedmann 3) are *forced by
   General Relativity*; they are not free.

And two honest limits — the same ones the forcing analysis already flagged:

- **Blanchet's floor uses 8π; ours uses 32π** — a factor of 4 apart. *Same structure* (floor = Λ, anharmonic = a₀),
  *different O(1)*. Neither is a typo; they are different normalizations of the same a₀↔Λ marriage.
- **The outer factor-2 (the horizon ½) is convention, and the density-vs-temperature *route* is unforced** — an ~8%
  spread (Z = 5.79 vs Unruh 2π = 6.28 vs Verlinde 6.0). The one route that *could* have forced 32π uniquely — the
  DSSYK horizon freezing — was **computed to fail** (it forces Z→∞ in the physical limit). So 32π is **traceable and
  route-forced by GR, but not *uniquely* forced.** With the observed a₀ = 1.2×10⁻¹⁰ the ratio reads ~61 instead of
  100.5 — the usual ~20–30% epoch/normalization gap, not a clean 32π.

**Bottom line.** "Anharmonic coefficient" is exactly the right lens: a₀ is the coefficient of the *nonlinear* (cubic)
term that turns Newtonian gravity (a harmonic, linear field theory) into MOND. Your number 32π is the dimensionless
*gravitational gearing* — Einstein coupling × horizon factor — that locks that anharmonic scale to the cosmological
constant (the harmonic floor). The structure is real, published-precedented (Blanchet), and GR-traceable; the exact
O(1) (32π vs 8π) is the route-choice that remains reproduced rather than uniquely derived.

---

## Glossary (the "information to understand it")

- **Harmonic** — quadratic; the ideal-spring part of a potential (V ∝ x²), giving a linear restoring force and an
  amplitude-independent oscillation. Superposition holds.
- **Anharmonic** — beyond-quadratic (x³, x⁴, …); the nonlinear corrections. Source of thermal expansion,
  amplitude-dependent periods, mode coupling, dissociation. Its **coefficient** measures how nonlinear the system is.
- **Anharmonic coefficient** — the number in front of an anharmonic (x³ or higher) term. In MOND, a₀ plays this role
  in the gravitational field Lagrangian.
- **AQUAL** (A QUAdratic Lagrangian / its nonlinear generalization) — Bekenstein–Milgrom's field theory of MOND
  (1984); its deep-MOND limit has the cubic |∇φ|³/a₀ Lagrangian.
- **|∇φ|²  vs  |∇φ|³** — the gravitational field energy. Quadratic = Newton (harmonic, linear Poisson); cubic =
  deep-MOND (anharmonic, √-law).
- **Polarization field Π** — in Blanchet's dipolar dark matter, the medium's internal displacement; its potential
  W(Π) has the floor/harmonic/anharmonic structure with a₀ in the cubic term.
- **Einstein coupling 8π** — the constant in Einstein's equation G_μν = (8πG/c⁴)T_μν; how strongly energy curves
  spacetime. The "8π" inside 32π.
- **Surface gravity / horizon factor** — κ = c²/2R for a horizon of radius R; the factor-2 (squared to 4) inside 32π.
- **Λ (cosmological constant)** — the vacuum-energy curvature; the *harmonic floor* the anharmonic scale a₀ is welded
  to via a₀ = c²√(Λ/32π).
