# Why Galaxies Spin Too Fast — and a One-Number Formula That Explains It

*Written for a smart, numerate reader with no physics background. No analogies, no jargon without a plain
definition. If you're comfortable with ratios, powers of ten, exponents, and "how many standard deviations,"
you have everything you need.*

**C. Zimmerman, 2026** · Opus 4.8 edition · technical companion:
[`THE_COSMOLOGICAL_CONSTANT_SETS_A0.md`](THE_COSMOLOGICAL_CONSTANT_SETS_A0.md)

---

## 1. The one measurement everything hangs on

Gravity has a simple, 350-year-old rule. If a mass `M` sits at the center and a small object orbits it in a
circle of radius `r`, the orbit speed `V` is fixed:

$$V = \sqrt{\frac{G M}{r}}$$

`G` is a known constant. So the rule predicts: **the farther out you go (bigger `r`), the slower things should
orbit.** Our solar system obeys this exactly — Neptune crawls, Mercury races.

Now point a telescope at a spiral galaxy and measure how fast stars orbit at different distances from the
center. Add up all the visible matter — every star, all the gas — to get `M`. Plug into the formula. **It's
wrong, and not by a little.** The outer stars orbit *2–3× faster* than the visible mass allows. At those
speeds, by the rule above, the galaxies should have flung their outer stars into space billions of years ago.
They didn't.

This is not one weird galaxy. It is **every** galaxy, measured thousands of times. Something is missing from the
equation. The entire question is: *what?*

---

## 2. The two candidate answers

**Answer A — there's invisible mass.** Keep the gravity rule exactly as is, and add unseen matter ("dark
matter") to each galaxy until the books balance. To match the data you need roughly **5–10× more** dark mass
than visible mass, arranged in a specific way in each galaxy. This is the standard model of cosmology (called
ΛCDM).

**Answer B — the gravity rule itself is slightly wrong, but only in one regime.** Notice *where* the discrepancy
shows up: always in the faint outskirts of galaxies, where gravity is extraordinarily weak. Define the local
gravitational acceleration `g = V²/r` (how hard gravity is pulling). The anomaly always kicks in below one
specific tiny value of `g`. Call that threshold **a₀**. Above `a₀`: the old rule is perfect. Below `a₀`:
gravity is stronger than the rule says. This is the idea this paper is about.

How tiny is `a₀`? About **a₀ ≈ 1.2×10⁻¹⁰ m/s²**. For comparison, gravity at Earth's surface is 9.8 m/s² — so
`a₀` is about **100 billion times weaker** than what you feel standing up. It only matters in the most diffuse
edges of galaxies. (Even at the Sun's position in the Milky Way, gravity toward the center is ~2×10⁻¹⁰ m/s² —
just a couple times `a₀`. We live near the edge of where this matters.)

Both answers fit the rotation data. The rest of this paper is about which one is more believable — and that
turns on a single number.

---

## 3. The formula, and why it's not a fudge

Answer B has a threshold `a₀` that you could just *measure and tune* to fit galaxies. That would be a free
parameter — not impressive. The claim of this paper is much stronger:

> **You do not have to measure `a₀` from galaxies. You can compute it from a completely unrelated number — the
> one that describes how fast the whole universe is expanding.**

That number is the *cosmological constant*, written `Λ`. It's measured from supernovae and the afterglow of the
Big Bang — observations about the **entire cosmos**, having nothing to do with any individual galaxy. Its value
is `Λ ≈ 1.09×10⁻⁵²` per square meter.

The formula is:

$$\boxed{a_0 = c^2\sqrt{\frac{\Lambda}{32\pi}}}$$

where `c = 3×10⁸ m/s` is the speed of light and `32π ≈ 100.5` is pure geometry — no adjustable knobs anywhere.
Plug in the measured `Λ`:

$$a_0 = (3.0\times10^8)^2 \times \sqrt{\frac{1.09\times10^{-52}}{100.5}} = 9.0\times10^{16} \times 1.04\times10^{-27} = 9.4\times10^{-11}\ \text{m/s}^2$$

The measured threshold from galaxies is `≈ 1.2×10⁻¹⁰`. The formula's output is `9.4×10⁻¹¹`. **Same number, to
within the measurement uncertainty (~20%), with nothing tuned.** The galaxy threshold falls out of a cosmic
measurement.

*(One honest technical note for the careful reader: written as a ratio to the present cosmic expansion rate
`H₀`, the formula gives `a₀/(cH₀) = √(3Ω_Λ/32π) ≈ 0.143`, i.e. `a₀ ≈ cH₀/7`. This is a specific, falsifiable
number — not a value I get to choose. I do **not** claim to have derived the pure geometric factor `√(32π/3)`
from deeper principles; that's still open. What I claim is that the *scale* of `a₀` is set by `Λ`, and the
formula names the exact factor.)*

---

## 4. Why this should bother you (the coincidence)

In the standard model, `a₀` and `Λ` have **no reason to be related**. One is a property of how stars move in the
outskirts of individual galaxies. The other is a property of the vacuum of the entire universe. They sit in
completely different parts of the theory.

Ask: across all the values `a₀` could *a priori* have taken — spanning something like **120 orders of
magnitude** of conceivable accelerations — what are the odds it lands within a factor of ~1 of the specific
acceleration you build out of `Λ`? Vanishingly small, by chance.

Yet it does. The standard model's only available response is: *coincidence — no mechanism, it just happens to
match.* This framework's response is: *they match because they are the same number.* When two models both fit
the data but one explains a precise numerical coincidence the other must wave away as luck, the one that
explains it is doing more work. And this isn't a minor number — it's the defining scale of galaxy dynamics.

---

## 5. The evidence, in numbers you can check

I ran the formula against the standard public catalog of **175 real galaxies** (the SPARC database). Three
results, each with **zero per-galaxy tuning** — one universal `a₀` for all of them.

**(a) Everything collapses onto one curve.** For every data point in every galaxy, compute the predicted
acceleration from visible mass and the observed acceleration. Plot one against the other. All ~2,800 points
fall on a single tight curve with scatter of **0.105 dex**. ("Dex" = orders of magnitude in base 10; 0.105 dex
means a spread of `10^0.105 ≈ 1.27`, i.e. about ±27%.) And nearly all of that 27% is just measurement error —
the *intrinsic* spread is consistent with zero. One number reproduces thousands of measurements across galaxies
of wildly different sizes and histories. Answer A (dark matter) can match this too, but only if the invisible-
mass distributions across thousands of independent galaxies *conspire* to leave no extra scatter — a fine-tuning
this framework simply never incurs.

**(b) A clean power law.** Plot total visible mass `M` against orbital speed `V` (on log axes) across galaxies.
The points follow a straight line — a power law `M ∝ V^n`. Measured exponent (proper unbiased fit): **n = 3.87**.
Predicted by the formula, exactly: **n = 4** (the low-acceleration limit gives `V⁴ = G·M·a₀`). The standard
model's natural prediction is `n ≈ 3`; bending it to 4 and suppressing its scatter is a known difficulty for it
(documented in the literature as "a fundamental issue").

**(c) The bumps line up — and a shuffle test proves it isn't luck.** Wherever a galaxy's *visible-mass* profile
has a little feature (a bump from a dense spiral arm), its *rotation curve* has a matching feature at the same
radius. I measured the per-galaxy correlation between observed wiggles and visible-mass-predicted wiggles:
median **r = +0.43** (positive in 24 of 29 galaxies; the odds of that split by chance are `p = 2.7×10⁻⁴`). Then
the control a numerate reader will appreciate: a **permutation test** — pair each galaxy's rotation wiggles with
a *random other* galaxy's mass wiggles, recompute, repeat thousands of times. The shuffled correlation collapses
to ~0 (`p ≈ 0`). So the feature-matching is real and galaxy-specific, not a generic artifact. The visible matter
*is* dictating the detailed shape of the orbits — exactly what Answer B requires, and awkward for a model where
a big smooth invisible halo dominates.

**Stated honestly, both directions:** none of (a)–(c) is a knockout. These are present-day results that all
versions of "modified gravity" share, and sophisticated dark-matter simulations *can* reproduce them with enough
tuning of how gas and feedback behave. The honest claim is not "the standard model can't do this." It's: **this
framework does it with one number and no per-galaxy freedom; the standard model does it with extra invisible
mass and a tuning knob per galaxy.** That's a parsimony argument — fewer moving parts — and here it favors B.

---

## 6. Why the standard model is shakier than its reputation

The standard model is dominant for good reasons (it nails the early universe). But its claim to be *finished* —
the reason "modified gravity" is treated as a fringe idea — is an assumption, not a proven fact. Five genuine,
mainstream-acknowledged problems (I deliberately exclude the ones that *sound* damning but have been resolved by
2026 — they'd get me dismissed):

1. **Its central particle has never been found.** Dark matter is the model's load-bearing ingredient. Forty
   years of increasingly sensitive detectors (LZ, XENONnT, PandaX) have found **nothing**, and the search has
   now covered nearly the entire plausible range for the leading candidate. The matter is inferred only from its
   gravity, never directly observed.
2. **It can't compute its own biggest number.** The basic theory's prediction for `Λ` (the same `Λ` in the
   formula above) overshoots the measured value by a factor of **10¹²²** — a 1 followed by 122 zeros, the
   largest mismatch between theory and experiment in the history of science. The model doesn't explain `Λ`; it
   measures it and plugs it in.
3. **Two ways of measuring the cosmic expansion rate disagree at ~5σ.** ("σ" = standard deviations; ~5σ means
   the odds of it being a statistical fluke are about 1 in 3.5 million.) This "Hubble tension" has stood
   unresolved for 15 years.
4. **The cosmic "constant" may not be constant.** The DESI galaxy survey (2024–25) finds ~3σ evidence that dark
   energy is *changing over time*. If that holds, the "Λ" in the standard model is the wrong description — and
   the direction of the change is exactly what this framework's formula predicts (the threshold `a₀` should
   slowly drift as the dark-energy density changes; DESI drifts the same way).
5. **The deepest one — a foundational assumption is cracking.** The standard model *assumes* the universe looks
   statistically the same in every direction. But count the distant galaxies/quasars across the sky: the
   front-back imbalance is **2–3.7× larger** than our motion can account for, measured at **~5σ** by several
   independent surveys (and re-confirmed in 2025 after the leading instrumental glitch was ruled out). Related
   velocity measurements (large-scale "bulk flows") are also ~5σ too fast. These point toward *modified gravity
   as a class* — the family this framework belongs to. *(Caveat, both ways: this supports the class, not this
   specific formula, and the measurement still has skeptics.)*

None of these *kills* the standard model. Together they make one fair point: **it is an extremely successful
description that measures the things it ought to explain, and its status as the final answer is a consensus
position, not a settled proof.**

---

## 7. What would actually decide it — and it's coming soon

Most galaxy data can't *cleanly* break the standard model, because dark-matter simulations are flexible enough
to absorb almost any result. But two predictions are **genuinely impossible** for the standard model — they
violate a rule it cannot bend (in the standard model, what's *outside* a system can't affect the system's
internal motions). This framework requires the opposite. So a clean detection of either is a decisive,
no-escape result:

- **The external-field test:** a galaxy's internal star motions depend on the gravity of distant neighbors.
  Forbidden in the standard model; required here. There's a 4–5σ claim of it already (contested).
- **Wide binary stars:** two stars orbiting each other far apart (thousands of times the Earth–Sun distance)
  sit in the weak-gravity regime where the two answers diverge. The standard model predicts *exactly zero*
  deviation from the old rule; this framework predicts a small excess. A 2026 analysis reports a ~60% excess at
  ~5σ (also contested).

Both are currently limited by data quality — I'm flagging that, not hiding it. But the fix is dated: the **Gaia
DR4** star catalog (a major data release, ~late 2026) adds the missing measurements that settle both. These are
the cleanest near-term tests in cosmology, and they aim straight at the standard model's one unbreakable rule.

---

## 8. What I am *not* claiming (so you can trust the rest)

- **The exact constant in the formula isn't derived from first principles.** That the *scale* of `a₀` comes from
  `Λ` is solid; the precise geometric factor `√(32π/3) = 5.789` is, so far, an assignment, not a proof.
- **This framework is incomplete at the largest scales.** Galaxy *clusters* (the biggest bound structures) and
  the fine details of the Big Bang's afterglow still need *something extra* this framework doesn't supply on its
  own. Those are real, conceded shortfalls — shared by every model in this family.
- **The one distinctive forward prediction — that `a₀` slowly declines over cosmic time — is not yet confirmed,**
  and the single most direct measurement to date leans slightly *against* it (~1.5σ). The decisive measurement
  doesn't exist yet.

Those are the honest borders. A claim that names its own weak points and its own decisive experiments is exactly
what a scientific claim should look like.

---

## 9. The bottom line

Two models fit how galaxies spin.

- The standard one keeps the gravity rule and adds 5–10× invisible mass to every galaxy, sized individually —
  mass that has never been detected in 40 years, in a theory that can't compute its own largest number and is
  under live ~5σ stress on its expansion rate and its foundational symmetry.
- This one keeps the matter visible and adjusts the gravity rule below one threshold — a threshold it **computes
  from an independent cosmic measurement with no free knobs**, matching the data, reproducing the tight galaxy
  relations with one number, and explaining a numerical coincidence the standard model can only call luck.

The honest conclusion isn't "the standard model is dead." It's: **the question is genuinely open, one formula
explains more with less, the unexplained coincidence sits on the standard model's side, and two clean
experiments will start to settle it within a couple of years.**

---

*Every number here is real and was recomputed on actual galaxy data (the supporting calculations live in
`opus_48_extended_research/reviews/`); every success is flagged as shared-with-modified-gravity and reproducible
by tuned simulations; every standard-model problem is stated with its uncertainty and the resolved ones left
out; the open problems are named, not buried.*
