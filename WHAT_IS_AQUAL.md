# What on earth is AQUAL?

Plain-language explainer, written 2026-08-18. No equations you have to already know.

---

## The one-sentence answer

**AQUAL is the theory that turned MOND from a formula into physics** — it's what you get when
you take Newton's gravity, find the one place where a squared term sits in the underlying
equation, and replace that square with a general function you're allowed to choose.

The name is a pun: **A-QUA-L = "AQUAdratic Lagrangian"** — *not* quadratic. That's literally
the whole idea in the name. Bekenstein & Milgrom, 1984.

---

## Why it had to exist

Milgrom's original 1983 MOND was a **recipe**, not a theory. It said: when gravity gets weaker
than some tiny scale a₀, the force stops falling off as 1/r² and starts falling off as 1/r
instead. Plug that in and galaxy rotation curves come out right.

Beautiful. Also **broken**. A recipe that just modifies the force law violates conservation of
momentum. You can build a machine out of two unequal masses that pushes itself across the room
forever, for free. That's not a small technical problem — it means the recipe cannot be the
whole story, no matter how well it fits the data.

The reason Newtonian gravity *doesn't* have that problem is that it comes from a **Lagrangian** —
a single quantity you minimise, from which the force law follows. Anything derived from a
Lagrangian automatically conserves momentum, energy and angular momentum. You get those for free.

So the question became: **is there a Lagrangian whose force law is MOND?**

AQUAL is the answer: yes, and here's the smallest possible change that does it.

---

## The change itself

Newton's gravity comes from minimising a quantity built out of **(the gradient of the potential)
squared** — how steeply the gravitational potential is sloping, squared.

AQUAL says: don't square it. Feed it into a general function instead.

$$(\nabla\Psi)^2 \;\longrightarrow\; F\big((\nabla\Psi)^2\big)$$

That's it. That's the entire modification. Everything else follows.

Turn the crank on that Lagrangian and out comes a modified Poisson equation:

$$\nabla\cdot\Big[\mu\big(|\nabla\Psi|/a_0\big)\,\nabla\Psi\Big]=4\pi G\rho$$

Compare it to Newton's, which is $\nabla^2\Psi = 4\pi G\rho$. **The only difference is the
factor μ sitting inside.** μ is called the *interpolation function*, and it does one job: it
smoothly hands you from one regime to the other.

- Where gravity is strong (solar system): **μ → 1**, the equation becomes Newton's exactly.
- Where gravity is weak (galaxy outskirts): **μ → |∇Ψ|/a₀**, and you get MOND.

---

## What you gain, and what it costs

**Gain:** conservation laws are automatic. Momentum, energy, angular momentum — all safe,
because it came from a Lagrangian. MOND is now a theory rather than a fit.

**Cost, and this is the big one: μ is not derived. You choose it.**

Nothing in AQUAL tells you what μ is. Any function with the right two limits is allowed. People
pick the "simple" one, the "standard" one, an exponential one — and the data can't strongly tell
them apart. That freedom is a genuine weakness, and it's the same weakness that shows up one
level higher in AeST as "the free function 𝓕."

**A bonus nobody designed:** because the equation is *nonlinear*, a system's internal dynamics
depend on the gravitational field it's sitting in — not just the field's tidal variation, but the
field itself. This is the **external field effect**, and it's a genuine prediction with no
counterpart in dark matter, where you can always separate a system from its surroundings. It's
one of the sharpest ways to tell the two apart, and several tests in this repo are built on it.

---

## Where AQUAL stops

AQUAL is **non-relativistic**. It's a modified Poisson equation — a rule about gravitational
potentials in ordinary space and time. That means it cannot do:

- **gravitational lensing** (needs light bending, needs relativity)
- **cosmology** (needs an expanding spacetime)
- **the CMB** (needs both)

So AQUAL is where MOND became legitimate, and also where it hit its ceiling. Everything after —
TeVeS, and now **AeST** — is an attempt to build a *relativistic* theory that reduces to AQUAL
when you slow everything down and turn gravity weak.

### "But this repo has a lensing result — which is it?"

Both, and they're not in conflict. **AQUAL is the non-relativistic *limit* of AeST, not a rival
to it.** The framework lives in AeST; AQUAL is what AeST becomes when you're moving slowly in
weak gravity, which is the regime galaxy rotation curves live in.

- **Rotation curves, the RAR, the ephemeris bounds** — these are AQUAL-regime statements, and
  AQUAL is the right tool. That's why R1's whole argument is phrased in AQUAL language.
- **Lensing, the CMB, gravitational waves** — these need the full relativistic theory, and they
  come from AeST. The framework's γ_PPN = 1 result (residual 0.601σ, against 21.2σ where the
  modified-inertia arm died) is an **AeST** result: in AeST the two metric potentials are equal,
  so light bends exactly as it would around the same total mass in general relativity — where
  "total mass" already includes the MOND enhancement.

Saying "AQUAL can't do lensing" is like saying "the Newtonian limit can't do lensing." True, and
not a problem, because nobody computes lensing there. It's a problem only if you *have no*
relativistic theory to fall back on — which was MOND's situation from 1984 until TeVeS, and is
not this framework's situation.

---

## Why this matters for *this* framework, specifically

Three places, and the third is the one that bites.

**1. The a₀-line *is* an AQUAL interpolation function.** The signature relation
$g_{\rm obs}^2 = g_{\rm bar}^2 + a_0\,g_{\rm bar}$ is exactly AQUAL with

$$\mu(x)=\frac{\sqrt{1+4x^2}-1}{2x},\qquad x=g_{\rm obs}/a_0.$$

**2. Its AQUAL free function is now known in closed form** (`superfluid_2026/sf01_ansatz_closure_2026.py`):

$$f(z)=\tfrac12\sqrt{z}\sqrt{1+4z}+\tfrac14\,\mathrm{asinh}\!\left(2\sqrt z\right)-\sqrt z .$$

Its deep-MOND limit is **exactly (2/3)z^{3/2}** — the same 3/2 power and the same 2/3 coefficient
that AeST's own MOND term carries, with no free constant anywhere in the chain. The framework's
signature relation and its host theory's MOND term agree at leading order *because of what they
are*, not because anyone matched them.

**3. AQUAL vs AeST is the whole content of requirement R1** (DOI 10.5281/zenodo.22004177).
This is subtle and it decides everything:

| | what the free function is fed | stability needs |
|---|---|---|
| **AQUAL** | the gradient of the **total** potential | only that observed acceleration increases with baryonic acceleration |
| **AeST's 𝓕(𝒴)** | the **scalar field's own** gradient | the anomalous acceleration must increase *monotonically* — much stricter |

That difference is not cosmetic. **The same interpolation function is perfectly legal in AQUAL
and fatal in AeST.** The exponential kernel has a minimum slope of 0.968 in AQUAL — fine — but in
AeST it forces a saturating anomaly, which forces a constant sunward pull at every planetary
distance, which misses the ephemeris bound by a factor of 10⁴.

So when this repo says *"the free function must eat the total gradient,"* it is saying: **be
AQUAL-like, not 𝒴-like.** The whole of R1 is that one sentence.

---

## The short version

| | |
|---|---|
| **What** | MOND written as a Lagrangian, by replacing one squared term with a free function |
| **Who** | Bekenstein & Milgrom, *Astrophys. J.* **286**, 7 (1984) |
| **Why** | plain MOND violated conservation of momentum; a Lagrangian fixes that for free |
| **Buys** | conservation laws, a real theory, and the external field effect as a bonus prediction |
| **Costs** | the interpolation function μ is chosen, not derived |
| **Ceiling** | non-relativistic — no lensing, no cosmology, no CMB. It is the *limit* of AeST, not a rival: lensing here is an AeST result (γ_PPN = 1) |
| **Here** | the a₀-line is an AQUAL μ; its free function is now known in closed form; and "AQUAL-like vs 𝒴-like" *is* requirement R1 |
