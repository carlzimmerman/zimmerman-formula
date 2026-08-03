# WTF Is the Ephemeris Problem?

### A plain-English explainer for the hardest open liability in the framework

*Companion to `reviews/mi_vdep_ephemeris_verdict_2026.py` and `real_research/reviews/mi_alpha2_sun_reflex_2026.py`. One equation, right at the end.*

---

## 1. The short version

Your theory says inertia gets weaker when acceleration gets very small. Galaxies have very small accelerations, so galaxies are where you see the effect — that's the whole point, and it works.

But "very small" isn't a wall. It's a slope. And a slope means the effect **never fully switches off** — it just gets tiny. So there's a whisper of it in the solar system too.

The solar system is the most precisely measured thing in physics. We know where Mars is to about **a metre and a half.**

The whisper is louder than a metre and a half.

That's the ephemeris problem.

---

## 2. What "ephemeris" even means

An **ephemeris** is a table of where the planets are. Modern ones (JPL's DE440, the French INPOP series) are built by taking every measurement humanity has — radar bounced off Mars, radio ranging to the Cassini spacecraft at Saturn, decades of optical astrometry — and fitting one gigantic model of the solar system to all of it at once.

The fit has hundreds of free knobs: every planet's mass, every starting position and velocity, the asteroid belt's total mass, relativistic corrections. They turn all the knobs until the model reproduces every observation.

What's left over — the part the knobs *can't* absorb — is the residual. **And the residual is tiny.** For Mars ranging it's about **1.5 metres** over decades of tracking.

That number is your problem. Anything your theory predicts that's bigger than the residual, and which the knobs can't absorb, is already ruled out.

---

## 3. Why your theory leaks into the solar system at all

Your law says the *observed* acceleration and the *Newtonian* acceleration aren't equal:

- Where gravity is strong (a planet), they're nearly the same.
- Where gravity is weak (a galaxy's edge), the observed one is much bigger.

"Nearly the same" is the problem. **How** nearly?

Your framework has had two versions of the answer, and this is the crux of the whole thing:

**Version α=1** — the exact, beautiful one, g_obs² = g_bar² + g_bar·a₀. This turns out to leave behind a **constant** leftover acceleration of a₀/2, pointed at the Sun, everywhere, forever. Constant. It doesn't shrink as you move to stronger gravity. That's **1279× larger** than the ephemeris allows.

**Version α=2** — the softer one, adopted in July precisely to fix that. Here the leftover *does* shrink: it goes like a₀²/(2g). Stronger gravity, smaller leftover. Much better.

---

## 4. The twist: it's the Sun's problem, not the planets'

Here's the part that's easy to miss, and the corpus missed it for seven weeks.

If the leftover shrinks as gravity gets stronger — goes like **1/g** — then to find the worst offender, you look for the object feeling the *weakest* gravity in the system.

That's not Neptune. **It's the Sun.**

The Sun barely accelerates at all. It gets tugged around a little by Jupiter — it wobbles about the solar system's balance point at roughly 12 metres per second, a slow shuffle. Its acceleration from that tug is about 2×10⁻⁷ m/s², which sounds small but is the key number: **it's about 2,200 times a₀**, whereas Earth's acceleration is about **60 million** times a₀.

So the Sun sits *thirty thousand times closer* to your theory's transition than Earth does. On a 1/g tail, that means the Sun's leftover is **thirty thousand times bigger**.

And it matters observationally, because the Sun's wobble is what sets the origin of the whole coordinate system. Get the Sun's response to Jupiter wrong and every planet's predicted position drifts.

Run through the full ephemeris fit — letting the fit absorb what it can into the Sun's mass, Jupiter's mass, and all 36 starting conditions — and the leftover Mars residual is:

> **12.7 metres, against a 1.5 metre budget. 8.5× too big.**
> (12.4× on the alternative a₀ footing. 6.2× even with every absorption trick allowed.)

Better than 1279×. Still failing.

---

## 5. Why you can't just absorb it

The obvious objection: if it's a constant pull toward the Sun, can't you just pretend the Sun is slightly heavier and call it a day?

Partly, and the fit does exactly that. But not fully, for two reasons:

**It has the wrong shape.** A change in the Sun's mass produces an effect that falls off as 1/r². Your leftover doesn't. So the two disagree at different planets, and with Mercury, Venus, Earth, Mars, Jupiter and Saturn all measured at once, the fit can't satisfy them simultaneously — absorbing it at Mars breaks it at Saturn.

**It bends orbits in a way mass can't.** A constant extra pull makes orbits precess — the ellipse slowly rotates. Mass doesn't do that. And precession is exactly what centuries of astronomy measure best. (It's how Mercury caught Einstein's attention.)

There was a hope that the Galaxy's own gravitational field pulling on the whole solar system would cancel it. **It doesn't** — and this one's pretty: the Galactic pull points in one fixed direction in space, while your leftover always points at the Sun and therefore *rotates* as the planet goes round. Average over one orbit and the fixed-direction piece averages to **exactly zero**. It can't cancel something that spins relative to it.

---

## 6. The thing we tried tonight, and why it didn't work

We built a new version where the modification depends on **velocity** instead of acceleration. It's a genuinely nice construction: it's ghost-free, it needs no acceleration in the action, and it reproduces every rotation curve exactly.

The hope was that planets move slowly compared to light, so maybe the effect would switch itself off in the solar system for free.

It doesn't, and the reason is a single line of algebra. Compare the two versions' arguments — the thing fed into the modification:

$$\frac{z}{a_N/a_0} \;=\; 2 - \frac{r}{A} \;=\; \begin{cases} 1+e & \text{at perihelion}\\ 1 & \text{on a circle}\\ 1-e & \text{at aphelion}\end{cases}$$

The two versions differ **only** by that factor, and it's bounded by the orbit's eccentricity e. Mars's is 0.09. The Sun's wobble is 0.05. **So the new version changes the answer by a few percent, not by the factor of 12 we'd need.** On a perfect circle the two are *identical*.

Worth knowing: an AI agent claimed this construction *did* cure the problem. It was wrong, and one line of algebra was enough to show it. That's why load-bearing numbers get computed rather than relayed.

---

## 7. What would actually fix it

Three routes. Two work, one doesn't, and the prices are known.

**Route A — make the switch-off faster. This is the cheapest and it works.** Instead of a leftover that shrinks like 1/g (a power law), use one that shrinks *exponentially* — like e^(−√(g/a₀)). At the Sun that suppresses it by **7×10¹⁶**. Every bound clears by many orders of magnitude, and it's already the template your own whitepaper adopted.

The price used to look steep: you'd give up the de Sitter–Unruh *derivation* of the law's shape. But two results from today cut that price, and this is the genuinely new part:

- Milgrom's admissibility condition on nonlocal theories excludes **every** interpolating function in use — his own, McGaugh's, all of them. So switching to the exponential loses no standing you had.
- The de Sitter–Unruh derivation only works for **straight-line** acceleration. On an orbit the worldline is a helix, and rotating detectors aren't thermal. So the shape you'd be "giving up" was never derived for orbits in the first place.

**You'd be trading a postulate for a postulate, and getting a working solar system.**

**Route B — make a₀ depend on orbital frequency.** a₀ effectively shrinks for fast orbits. Planets orbit ~10¹⁵ times faster than a galaxy rotates, so the effect vanishes there. Works, and the velocity-dependent construction gives it a natural home rather than bolting it on. Price: a fifth constant in the theory.

**Route C — use the radial-velocity sector.** There's a beautiful fact here: circular orbits are **provably blind** to the part of the Lagrangian that depends on ṙ. So you could put anything there and every rotation curve, the whole radial acceleration relation, and the κ=½ measurement would stay *exactly* unchanged.

But it can't fix this. A ṙ-dependent term vanishes when ṙ = 0 — and the Sun's wobble is nearly circular. It can move eccentric planets and not the one body that binds.

**Its value is the opposite direction: it's a free prediction sector.** Invisible to every rotation curve, but it produces eccentricity-dependent effects — which is exactly the wide-binary test, done properly this time from a real Lagrangian.

---

## 8. Where this actually leaves you

**It is not a killer.** It rules out a *shape* — the power-law approach to Newton — not the framework. Your central claim, a₀ = ½c√(Gρ_Λ), never enters this argument: the ephemeris constrains how the law switches off, not what the acceleration scale is.

**It is the sharpest open item you have**, and it's been mis-stated in your own corpus twice today in *both* directions: once by claiming the Galaxy's field relieves it (it doesn't — post-relief equals no-relief exactly), and once by claiming the α=2 switch discharged it (it doesn't — the Sun binds at 8.5×, and your own published whitepaper said so seven weeks before the switch).

**And it has a known fix with a known price.** That's an unusually good position for an open problem. Most open problems don't come with a working solution attached and a receipt for what it costs.

---

### The one equation

$$\delta a \;\simeq\; \frac{a_0^2}{2g}$$

The leftover acceleration your theory predicts, in terms of the local Newtonian gravity g. It's small when g is big. The Sun's g is tiny — about 2,200 a₀ — so its leftover is 30,000 times Earth's, and that's the whole problem in one line.

Route A replaces the 1/g with e^(−√(g/a₀)), and 7×10¹⁶ is the size of the improvement.
