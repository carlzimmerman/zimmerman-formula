# Chapter 25: The Signature Prediction: a₀ Tracks Dark Energy Through Time

*Every honest theory must, at some point, stick out its neck. This is where ours does.*

---

## A Promise We Have Not Yet Cashed

We have spent the last several chapters building something. In Chapter 20 we met the central claim — that the galactic acceleration scale a₀ can be written in terms of the cosmological constant Λ, the same Λ that drives the accelerating expansion of the universe. In Chapter 21 we met the *mechanism* that might stand behind that claim: de Sitter–Unruh modified inertia, the idea that empty space in a Λ-universe carries a faint temperature floor, and that matter drifting in near-free-fall feels that floor as a little extra resistance to being pushed — extra inertia that, from the outside, looks like extra gravity. In Chapters 22 and 23 we sorted carefully through what is *forced* by the structure and what is *chosen*: the form a₀ ∝ c²√Λ and the √(8π/3) kernel are forced; the single number κ = ½ is a geometric posit, the one free knob. And in Chapter 24 we tallied the score: one knob, against ΛCDM's six parameters and an as-yet-undetected particle.

All of that has been, in a sense, *retrospective*. We have been explaining a number — a₀ ≈ 9.36 × 10⁻¹¹ m/s² — that was already measured before the framework was written down. A skeptic is entitled to fold their arms at this point and say: *Fine. You have a pretty story that reproduces a number we already knew. So does MOND, with a number it also fit after the fact. Tell me something I do not already know. Tell me something that could be* **wrong**.

That is a completely fair demand. It is, in fact, *the* demand — the one that separates a piece of physics from a piece of philosophy. A theory earns its keep not by explaining the past but by sticking out its neck about the future, in a way precise enough that nature could snap it off.

This chapter is the framework sticking out its neck.

And here is the thing that makes it genuinely interesting, rather than just another adjustable curve: the prediction we are about to make has **nothing left to tune**. Every knob has already been spent. The one free number, κ = ½, sets the *present-day* value of a₀ — and once that present-day value is fixed, the framework has no remaining freedom to say how a₀ behaves at *other* times. The shape of a₀ through cosmic history is dictated entirely by the cosmology, by how dark energy itself evolves. We do not get a vote. We hand the steering wheel to the universe and watch where it drives.

If a₀ is really *made of* dark energy, then when dark energy changes, a₀ must change too — on a curve we are not allowed to bend.

That is the bet. Let us see exactly what it says.

---

## The Core Idea, in Plain Words

Start from the one sentence that this whole book has been circling: **the galactic acceleration scale is set by dark energy.**

If you take that sentence literally — not as a slogan but as a statement about the actual contents of the universe — then it has an immediate, almost unavoidable consequence. Dark energy is not guaranteed to be a constant. For most of the past quarter-century, physicists *assumed* it was constant; that constant even has a name, Λ, the cosmological constant, and a constant energy density that never dilutes as the universe expands. But "assumed constant" is not the same as "known constant." Dark energy could, in principle, have been a little denser in the past, or a little thinner, and slowly drifted to the value we see today.

Now follow the logic. If a₀ is built out of the dark-energy density — if, as Chapter 20 had it, a₀ = (c/2)√(G ρ_DE), so that a₀ is essentially the square root of how much dark energy there is — then **a changing dark-energy density forces a changing a₀.** When there was more dark energy, the acceleration scale was higher. When there was less, it was lower. The galactic ruler we use to weigh the cosmos would itself have been a slightly different length at different epochs of cosmic history.

Let us name this carefully, because the whole chapter turns on it.

**a₀(z) evolution** is the claim that the acceleration scale a₀ is not a fixed constant of nature but a slowly changing quantity that depends on *when* in cosmic history you measure it. The little "(z)" is the standard astronomer's way of labeling cosmic time. The letter **z** stands for *redshift*: light from a distant galaxy is stretched to longer, redder wavelengths by the expansion of the universe during its long journey to us, and the amount of stretch tells us how long ago the light left. Redshift z = 0 means *here and now*. Larger z means *longer ago and farther away*. Redshift z = 1 is light that left when the universe was about half its present age; z = 3 reaches back to when the cosmos was only about two billion years old. So "a₀(z)" is shorthand for "the value the acceleration scale had at the cosmic epoch labeled by redshift z."

And the specific form of the dependence is what we will call **√ρ_DE(z) scaling**: a₀ at any epoch is proportional to the *square root* of the dark-energy density at that epoch. The square root is not a free choice we sprinkled on for taste. It is already sitting inside the central formula — a₀ goes as √(G ρ_DE), so √ρ_DE is simply what the formula says. Double the dark energy and a₀ goes up not by a factor of two but by a factor of √2, about 1.41. The square root softens everything; it means a₀ is a fairly *lazy* tracker of dark energy, moving only half as fast (in fractional terms) as the density it follows.

So the headline, in one breath: **a₀ should ride up and down with the square root of the dark-energy density across cosmic time, on a curve that the cosmology fixes and the framework is not permitted to adjust.**

> **Margin aside.** Why does a square root tame the motion? Because for small changes, a fractional change in √x is *half* the fractional change in x. A 12% rise in ρ_DE becomes only a ~6% rise in a₀. We will see that 6% again very soon — it is not a coincidence.

---

## Why Dark Matter Cannot Make This Prediction

Before we work out the curve, it is worth dwelling on *why* this is the framework's signature — the one prediction that genuinely belongs to it and not to its rivals. The reason is almost embarrassingly simple, and it is the most honest selling point the framework has.

**Dark matter has no acceleration scale to evolve.**

Think about what a dark-matter particle *is*, in the standard picture (Chapters 5 and 6). It is matter — cold, slow, invisible matter — that clumps under gravity exactly the way ordinary matter does, just without giving off light. There is nothing in that picture that singles out a special acceleration. A galaxy's rotation curve, in the dark-matter account, is whatever it is because of how much invisible matter happened to settle into that galaxy's halo and how it is distributed. Different galaxies, different halos, different curves. There is no universal number a₀ baked into the laws; the apparent regularities (which we will meet again in a moment) are, in the dark-matter view, emergent accidents of how galaxies form. And because there is no fundamental acceleration scale in the theory at all, there is certainly no *cosmic clock* attached to one. Dark matter cannot predict that the acceleration scale was 6% higher at redshift 0.4, because in its world there is no such scale to be higher or lower.

Plain MOND (Chapter 17) is a more interesting case, and we must be fair about it. MOND *does* have an acceleration scale a₀ — that is its whole point. But in Milgrom's original formulation, a₀ is simply a new constant of nature, like the speed of light or the charge of the electron. A constant. There is no reason within MOND for it to change over cosmic time, and most MOND practitioners have treated it as fixed. Some have noticed the numerical coincidence that a₀ is close to cH₀ (the speed of light times the Hubble rate) and to c²√Λ, and have *speculated* that it might therefore evolve — but speculation is not the same as a forced, parameter-free curve, and MOND as a framework does not require it.

Our framework does require it. That is the difference. The framework does not merely *permit* a₀ to evolve; it *insists* on it, because it claims a₀ is not a fundamental constant at all but a *derived quantity* — a thing built out of the dark-energy density, the way a wave's speed is built out of the properties of the medium it travels through. If the medium changes, the wave speed changes; you do not get to hold it fixed. So the framework is structurally committed to a₀(z) evolution in a way that neither dark matter nor textbook MOND is.

This is the cleanest statement of what the framework risks. **If a₀ turns out to be a genuine, unchanging constant of nature, the framework is wrong** — or at least its central physical claim is wrong — *even if every galaxy rotation curve it ever touched came out perfectly.* The rotation curves are shared territory (we will be honest about that throughout). The *evolution* is the framework's own neck.

> **Margin aside.** Notice the asymmetry of the bet. Confirming the curve would be strong evidence *for* a dark-energy origin of a₀. But the framework is most exposed on the downside: a flatly *constant* a₀ across redshift, well-measured, would be very hard for it to survive. A theory you can kill is a theory worth having.

---

## What Sets the Curve: How Dark Energy Itself Changes

So the shape of a₀(z) is inherited, wholesale, from the shape of ρ_DE(z) — the dark-energy density as a function of cosmic time. To know what a₀ does, we need to know what dark energy does. And here we hand the question over to the observers, because this is *their* measurement, not the framework's.

For a long time the default answer was the simplest one imaginable: dark energy is a true constant, ρ_DE never changes, the "cosmological constant" deserves its name. In that world a₀(z) would be flat — the same value at every redshift — and the framework's signature prediction would collapse into "a₀ is constant," indistinguishable from textbook MOND, and impossible to use as a discriminator. If the universe had handed us a genuinely constant dark energy, this chapter would be very short and rather disappointing.

But over the past few years, that default has been shaken. We need to introduce the instrument and the language astronomers use, because the rest of the chapter lives inside them.

**DESI** is the Dark Energy Spectroscopic Instrument — a survey on a telescope in Arizona that has measured the three-dimensional positions of tens of millions of galaxies and quasars, mapping the cosmic web across billions of years of cosmic history. By tracking a faint, fossil-sound-wave pattern in how galaxies cluster (a ruler called the *baryon acoustic oscillation*, laid down in the infant universe and stretched by expansion ever since), DESI can reconstruct how fast the universe was expanding at many different epochs — and from the expansion history, infer how the dark-energy density has behaved over time. **DESI DR2** is the second major data release from this survey, the one whose dark-energy results we will use as our working numbers.

To describe a dark energy that might *change*, cosmologists need a compact way to write down "how constant is it, and if it is changing, which way?" The standard shorthand is the **CPL parametrization** — named for the physicists Chevallier, Polarski, and Linder who introduced it. It describes dark energy with just two numbers:

- **w₀** (read "w-naught") is the dark-energy *equation-of-state parameter* today. The equation-of-state parameter w is the ratio of a substance's pressure to its energy density, and it controls how the substance's density changes as the universe expands. A true cosmological constant has w exactly −1: its density never dilutes. If w₀ is a little *above* −1 (say −0.9), dark energy thins out as the universe grows; if w₀ is *below* −1 (say −1.1), it is in the exotic regime physicists call "phantom," where the density would actually *grow* with expansion.

- **wₐ** (read "w-a") describes how w itself drifts with cosmic time. If wₐ is zero, w never changes and we are back to a fixed equation of state. If wₐ is non-zero, the dark energy was a different kind of stuff in the past than it is today.

The headline from DESI DR2, taken at face value, is that dark energy appears **not** to be a simple constant. The best-fit numbers come out near **w₀ ≈ −0.75** and **wₐ ≈ −0.86**. Read those together and they tell a specific little story: today w₀ ≈ −0.75 sits *above* −1, but a negative wₐ means w was *more* negative in the past — below −1, in the phantom regime, at earlier times. Somewhere in between, the equation of state must have passed *through* the special value w = −1.

That crossing has a name, and it matters enormously for our curve.

The **phantom-divide crossing** is the cosmic moment when the dark-energy equation of state passes through w = −1 — the dividing line between ordinary, diluting dark energy (w > −1) and the exotic "phantom" regime (w < −1). At that crossing, the dark-energy density is doing something special: it stops growing and begins to decline (or vice versa). In other words, the density ρ_DE reaches a *turning point* — a maximum — right at the phantom-divide crossing. And since a₀ rides on √ρ_DE, **a₀ reaches its own maximum at the same moment.** The crossing is the peak of our curve. Under the DESI DR2 numbers, that peak lands at a redshift of about **z ≈ 0.4** — light that left roughly four billion years ago.

Let me be very honest, and this is a both-ways moment we will return to with force at the end of the chapter: **none of this is settled.** The DESI DR2 preference for evolving dark energy is real and it is interesting, but it is not a discovery on the scale of, say, the 1998 acceleration result. Different choices of which datasets to combine, and different prior assumptions, can pull the significance up or down, and under some reasonable analyses the evidence for any evolution at all softens toward the level where it could still be a statistical fluctuation. We are building our signature prediction on top of *somebody else's* contested measurement. That is a genuine vulnerability, and we will own it. But it is also, for the moment, the best estimate the field has of how dark energy behaves — so it is the honest input to use. If those numbers move, our curve moves with them, automatically and without any new freedom. That is exactly the point.

> **Deeper Dive: The parameter-free evolution law.**
>
> The framework's prediction is a *ratio*, and the ratio is where the magic — and the honesty — lives. Start from the central relation,
>
> $$a_0(z) = \frac{c}{2}\sqrt{G\,\rho_{\rm DE}(z)},$$
>
> where every epoch's a₀ is built from that epoch's dark-energy density. Now divide the value at redshift z by the present-day value:
>
> $$\boxed{\;\frac{a_0(z)}{a_0(0)} = \sqrt{\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)}}\;}$$
>
> Look at what dropped out. The factor c/2 cancelled. The Newton constant G cancelled. The geometric kernel √(8π/3) cancelled. The one free number κ = ½ — which entered only through the *normalization* of a₀ — **cancelled.** Even the choice of interpolation function (the detail of how the modified-inertia transition is shaped, which differs across MOND-family theories) drops out of the ratio, because it affects today and the past identically. *Nothing tunable survives.* The shape of a₀(z)/a₀(0) is a pure function of the dark-energy density history, and that history is an input from cosmology, not a parameter of the framework. This is why we keep calling the prediction parameter-free: it is not a figure of speech. The single knob the framework owns sets the overall *height* of the a₀ curve, and the height divides out of the shape.
>
> To get a number we need ρ_DE(z) explicitly. Under the CPL parametrization, integrating the dark-energy conservation equation with w(a) = w₀ + wₐ(1 − a), where a = 1/(1+z) is the cosmic scale factor, gives the standard closed form:
>
> $$\frac{\rho_{\rm DE}(z)}{\rho_{\rm DE}(0)} = (1+z)^{\,3(1+w_0+w_a)}\,\exp\!\left(\frac{-3\,w_a\,z}{1+z}\right).$$
>
> Combine the two boxed results and you have the framework's complete, parameter-free signature curve:
>
> $$\frac{a_0(z)}{a_0(0)} = (1+z)^{\,\tfrac{3}{2}(1+w_0+w_a)}\,\exp\!\left(\frac{-3\,w_a\,z}{2(1+z)}\right).$$
>
> Everything on the right-hand side is cosmology. The framework contributes only the *claim that this equals the acceleration-scale ratio* — and that claim has no free parameters left in it.

---

## Reading the Curve: A Bump, Then a Long Decline

Now let us actually *walk along* the curve, in words, from here-and-now back into the deep past, so you can picture its shape before we compute a single point.

Start at redshift zero — today. By construction, a₀(0)/a₀(0) = 1. The ruler is its present length.

Step back to modest redshifts, z of a few tenths. Because dark energy was in its phantom phase in the recent past (w below −1), its density was actually *higher* back then than it is today — phantom dark energy grows denser as you go backward toward the present, which is the same as saying it was denser just behind us. So a₀ was *higher* in the recent past. The curve climbs as we step back from z = 0. It is a gentle climb, softened by the square root.

Keep stepping back and you reach the turning point — the phantom-divide crossing, near **z ≈ 0.4**. Here the dark-energy density hits its maximum, and so a₀ reaches its peak. Under the DESI DR2 numbers, that peak sits about **6% above** today's value. A small bump — but a bump with a definite location and a definite height, both fixed by the cosmology, neither adjustable. Galaxies at this epoch would, if the framework is right, feel an acceleration scale a few percent larger than the one we measure locally.

![The CPL equation of state w(z) crossing minus one while the dark-energy density reaches its maximum at the same redshift near 0.4](figures/ch25_phantom_divide_mechanism.png)

***Figure 25.3 — The mechanism behind the bump: where w crosses −1, ρ_DE peaks.*** Both curves are framework-computed from the DESI DR2 CPL parameters (w₀ = −0.75, wₐ = −0.86). The equation of state (red, left axis) sits above −1 today but was in the "phantom" regime (w < −1) in the past, so it must cross the phantom divide w = −1 — here near z ≈ 0.41. At exactly that crossing the dark-energy density (purple, right axis) reaches its maximum and turns over. Because a₀ ∝ √ρ_DE, the acceleration scale inherits its peak at the same redshift — fixing the location of the curve's bump with no freedom left to the framework.

**Source:** Figure generated by [`book/figures/ch25_phantom_divide_mechanism.png.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch25_phantom_divide_mechanism.py). CPL parametrization (Chevallier–Polarski–Linder) and evolving dark-energy values: DESI DR2 2025, arXiv:2503.14738; a₀ ∝ √ρ_DE scaling: [a₀(z) paper](https://doi.org/10.5281/zenodo.20737162).


Now push past the peak, to higher redshift, deeper into the past. Beyond the crossing, the equation of state was in the ordinary regime (w above −1) — wait, that is backwards; let me say it carefully, because the geometry of "earlier" and "denser" can twist your intuition. Going to *higher* z than the peak, we are going further back than the crossing, into the epoch where w was *below* −1... no. Here is the clean way to hold it: the density has a single maximum at the crossing. On *both* sides of that maximum the density is lower. So as we continue to higher and higher redshift past z ≈ 0.4, the dark-energy density falls, and a₀ falls with it — a long, slow decline. By **z = 3** — light from when the universe was only about two billion years old — the framework predicts a₀ has dropped to roughly **0.74** of its present value. About a quarter lower. Galaxies that early in cosmic history would have had a noticeably *smaller* acceleration scale than galaxies today.

So the full shape, in one mental image: a curve that starts at 1.0 today, rises to a gentle peak of about 1.06 near z ≈ 0.4, then bends over and declines steadily to about 0.74 by z = 3, continuing downward beyond. **A bump, then a long fall.** Non-monotonic — meaning it does not simply rise or simply fall, but does both, with a turnaround in between. That non-monotonicity is itself a fingerprint, because it is hard to fake with a generic fitting function and impossible to produce at all without a physical mechanism that ties a₀ to evolving dark energy.

![The a0(z) signature curve rising to a small bump near z=0.4 then declining, against a flat constant-MOND line and a steeply rising rival](figures/ch25_a0z_signature_curve.png)

***Figure 25.1 — The framework's signature prediction: a₀ tracks √ρ_DE through cosmic time.*** The purple curve is computed directly from the framework's parameter-free ratio a₀(z)/a₀(0) = √[ρ_DE(z)/ρ_DE(0)] using the DESI DR2 CPL fit (w₀ = −0.75, wₐ = −0.86). It rises to a gentle peak of about +6% at the phantom-divide crossing (z ≈ 0.4), then declines to ≈0.74 of today's value by z = 3 — the non-monotonic "bump then fall" fingerprint. Textbook MOND (teal, flat) holds a₀ fixed; the leading rising rival (red, a₀ ∝ cH(z)) climbs the opposite way, leaving an order-of-magnitude gap at high redshift. Curves are framework-computed; the dark-energy history is a cosmological input, not a knob.

**Source:** Figure generated by [`book/figures/ch25_a0z_signature_curve.png.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch25_a0z_signature_curve.py). Framework curve and a₀(z) scaling: [a₀(z) dark-energy-scale paper](https://doi.org/10.5281/zenodo.20737162) and [`opus_48_extended_research/papers/a0z_desi_figure.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/opus_48_extended_research/papers/a0z_desi_figure.py); evolving dark-energy input: DESI DR2 2025, arXiv:2503.14738.


> **Margin aside.** "Non-monotonic" just means the curve changes direction — up, then down. A constant a₀ would be a flat line. A rising-a₀ rival would be a line that only climbs. Ours does something neither of them does: it goes up a little, then comes down a lot. The *shape itself* carries information.

And here is the rival worth naming, because it sharpens the test. There is a competing reading — not from this framework — in which the relevant cosmic acceleration scale tracks not the *dark-energy* density but the *total* density or the Hubble expansion rate H(z). Because the total density and H(z) both *grow* with redshift (the universe was denser and expanding faster in the past), that rival predicts a₀ that **rises** with z, and keeps rising. By z = 3, that rising branch sits far above our declining one — the two predictions differ by a factor of roughly **7.5×** at z = 3. That is not a subtle disagreement you need exquisite precision to resolve; it is a chasm. The framework says galaxies at z = 3 were *slower* (smaller a₀); the rising rival says they were *much faster* (larger a₀). They could hardly be more opposed, which is exactly what makes the high-redshift regime such a clean place to look. We will return to *how* one looks, in the next chapter; here the point is only that the framework's curve is sharply distinguishable from both the constant case and the leading alternative.

> **Worked Example: Computing a₀ at three epochs, slowly.**
>
> Let us put real numbers through the formula, one careful step at a time, using the DESI DR2 values w₀ = −0.75 and wₐ = −0.86. The master equation, from the Deeper Dive above, is
>
> $$R(z) \equiv \frac{a_0(z)}{a_0(0)} = (1+z)^{\,\tfrac{3}{2}(1+w_0+w_a)}\,\exp\!\left(\frac{-3\,w_a\,z}{2(1+z)}\right).$$
>
> First, let us assemble the two recurring constants so we are not re-deriving them each time.
>
> The exponent on the (1+z) factor uses 1 + w₀ + wₐ = 1 + (−0.75) + (−0.86) = 1 − 1.61 = **−0.61**. Multiply by 3/2: the power is (3/2)(−0.61) = **−0.915**.
>
> The exponential's prefactor uses −3wₐ/2 = −3(−0.86)/2 = +2.58/2 = **+1.29**. So the exponential term is exp[1.29 · z/(1+z)].
>
> Our working formula is therefore
>
> $$R(z) = (1+z)^{-0.915}\,\exp\!\left(1.29\cdot\frac{z}{1+z}\right).$$
>
> **Epoch one: z = 0.4 (the predicted peak, ~4 billion years ago).**
> The power-law piece: (1.4)^(−0.915). Take ln(1.4) = 0.3365; multiply by −0.915 to get −0.3079; exponentiate: e^(−0.3079) = 0.735.
> The exponential piece: z/(1+z) = 0.4/1.4 = 0.2857; times 1.29 = 0.3686; e^(0.3686) = 1.446.
> Multiply: R(0.4) = 0.735 × 1.446 = **1.063.** The acceleration scale is about **6.3% above** today's value — there is our bump, landing essentially where we said it would.
>
> **Epoch two: z = 1 (universe roughly half its present age).**
> Power-law: (2)^(−0.915). ln(2) = 0.6931; times −0.915 = −0.6342; e^(−0.6342) = 0.530.
> Exponential: z/(1+z) = 1/2 = 0.5; times 1.29 = 0.645; e^(0.645) = 1.906.
> Multiply: R(1) = 0.530 × 1.906 = **1.010.** Already, by z = 1, the curve has come back down to almost exactly its present-day value — it is on its way past the peak and heading down.
>
> **Epoch three: z = 3 (universe ~2 billion years old).**
> Power-law: (4)^(−0.915). ln(4) = 1.3863; times −0.915 = −1.2685; e^(−1.2685) = 0.281.
> Exponential: z/(1+z) = 3/4 = 0.75; times 1.29 = 0.9675; e^(0.9675) = 2.631.
> Multiply: R(3) = 0.281 × 2.631 = **0.739.** The acceleration scale at z = 3 is about **0.74** of today's — roughly a quarter lower, exactly the figure quoted above.
>
> Step back and look at the three numbers in sequence: 1.063, then 1.010, then 0.739. **Up, then down.** We have just traced the non-monotonic signature by hand. Notice that no parameter of the framework appeared anywhere in this calculation — only c, G, and κ would have appeared, and all three cancelled in the ratio. Every input was a cosmological measurement (w₀, wₐ) or a choice of which epoch to evaluate. The curve is the universe's to draw; we only read it off.

---

## How Big Is 6%, Really? On Translating a₀ Into Something Observable

A reader is entitled to ask: a 6% bump in a quantity I cannot see directly — so what? How would anyone ever *catch* this? The full answer is the next chapter's job (Chapter 26 is entirely about the experimental program). But we owe a preview here, because a prediction you cannot connect to an observation is not really a prediction.

The bridge runs through the two great regularities we met in Chapter 18 — the radial-acceleration relation and the baryonic Tully–Fisher relation. Both of them have a₀ sitting inside them as the scale that separates the Newtonian regime from the modified one. The baryonic Tully–Fisher relation in particular says that a galaxy's flat rotation speed, raised to the fourth power, is proportional to its baryonic mass times a₀:

$$v_{\rm flat}^4 \approx G\,M_{\rm baryon}\,a_0.$$

Because v_flat goes as the *fourth root* of a₀, the square root that already tamed a₀'s evolution gets tamed *again*. A 6% change in a₀ becomes only a ~1.5% change in the predicted rotation speed (the fourth root of 1.06 is about 1.015). A 26% drop in a₀ at z = 3 becomes about a 7% change in rotation speed (the fourth root of 0.74 is about 0.93). So the framework's concrete, falsifiable claim at high redshift is roughly this: **a galaxy of a given baryonic mass at z = 3 should be spinning about 7% more slowly than an otherwise-identical galaxy today** — and, crucially, *slowly*, not quickly, which is the opposite of what the rising-a₀ rival predicts.

![Three nested curves showing the dark-energy density swing shrinking from 13 percent to 6 percent to 1.5 percent as two square roots are applied](figures/ch25_double_sqrt_softening.png)

***Figure 25.2 — The double-square-root cascade: from dark energy to a measurable spin.*** All three curves are framework-computed from the same CPL density history (w₀ = −0.75, wₐ = −0.86). The dark-energy density (red) swings by about +13% at its z ≈ 0.4 peak; the first square root, a₀ ∝ √ρ_DE, halves that to +6% (purple); the second, v_flat ∝ a₀^¼ through the baryonic Tully–Fisher relation v⁴ = G M a₀, halves it again to a mere +1.5% in rotation speed (teal). By z = 3 the same cascade turns a −26% density drop into only a ≈7% speed deficit — which is why the chapter leans on the robust *sign* of the offset rather than its fragile magnitude.

**Source:** Figure generated by [`book/figures/ch25_double_sqrt_softening.png.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch25_double_sqrt_softening.py). Framework scaling a₀ ∝ √ρ_DE: [a₀(z) paper](https://doi.org/10.5281/zenodo.20737162) and [spine paper](https://doi.org/10.5281/zenodo.20721540); baryonic Tully–Fisher relation: McGaugh 2012, AJ 143, 40 (slope-4 law from Tully & Fisher 1977, A&A 54, 661); CPL density input: DESI DR2 2025, arXiv:2503.14738.


That is why the next chapter will argue that the **sign** of the high-redshift Tully–Fisher offset is the single cleanest test. We do not, at first, even need to measure the 7% precisely. We need to measure which *way* the offset goes. Down (slow) supports the framework; up (fast) supports the rival and embarrasses the framework; zero (no offset, constant a₀) embarrasses both and vindicates textbook MOND and, in its own way, dark matter. The sign is the cheapest, sharpest discriminator, and it is the thing the giant telescopes of the late 2020s and 2030s — ELT, JWST, ALMA, pushing galaxy kinematics out to ever-higher redshift — are positioned to deliver.

> **Margin aside.** Two square roots in a row are why this is hard. a₀ goes as √ρ_DE (one root), and rotation speed goes as a₀^¼ (another). The observable signal is therefore a *very* gentle function of the underlying dark-energy change — which is honest to admit, and also why we lean on the robust *sign* rather than the fragile *magnitude*.

---

## The Honest Standing of the Bet

Let me now do the thing this book promises to do at every turn: state both sides in the same breath, plainly, with nothing hidden.

**What is genuinely strong here.** This is a real prediction. It is parameter-free in the strict sense demonstrated in the Deeper Dive — every knob, including the one free number κ, cancels out of the shape of the curve. It is *distinctive*: dark matter cannot make it at all (no scale to evolve), textbook MOND does not require it (a₀ a fixed constant), and the leading non-framework reading of an evolving scale predicts the *opposite sign* at high redshift, separated from ours by a factor of order 7.5× at z = 3. It is *falsifiable* in the most direct way a theory can be: a well-measured, genuinely constant a₀ across cosmic time would break the framework's central physical claim, no matter how many present-day rotation curves it fits. And it is *coming* — the data that bears on it is being collected right now and over the next decade, not in some indefinite future. A theory that can be killed, by experiments already underway, is exactly what an honest framework should put on the table.

**What is genuinely shaky, and we will not pretend otherwise.** First and largest: the *input* is contested. The whole distinctive shape — the bump, its location, the decline — rides on DESI DR2's preference for evolving dark energy, and that preference is not yet a settled fact. Under some reasonable combinations of data and priors the evidence for any evolution at all softens, drifting down toward the level (around 1.3σ in certain analyses) where it could be a fluctuation. If dark energy turns out to be a plain constant after all, our signature curve flattens into a horizontal line, the bump vanishes, and the prediction degenerates into "a₀ is constant" — true, perhaps, but no longer a discriminator, and indistinguishable from textbook MOND. The framework's most interesting bet is therefore **hostage** to a measurement it does not own and cannot control. That is worth saying twice.

Second: the signal is *gentle*. Two square roots stand between evolving dark energy and an observed rotation speed, so even the dramatic-sounding numbers — a 6% bump, a 26% decline — translate into single-digit-percent shifts in the quantities telescopes actually measure, against the formidable messiness of real high-redshift galaxies (which are clumpy, turbulent, and hard to assign clean rotation speeds to). Catching the *sign* is realistic; catching the *shape* in detail will be a long, hard observational campaign, and it may be years before the verdict is clean.

Third, and to keep ourselves honest about the larger picture: confirming a₀(z) would be a significant success, but it would *not* resolve the framework's deeper open questions. It would not derive the value of a₀ (κ remains a geometric posit, Chapter 27), would not touch the Standard Model (still walled off, Chapter 27), would not repair the lensing wall (Chapter 28), and would not cure the cluster residual (Chapter 29). It would tell us that a₀ is *made of dark energy* — a deep and beautiful thing if true — without telling us *why* the proportionality constant is what it is. This is, as we keep saying and will keep saying, **not a theory of everything yet, as frustrating as it may be.**

But within those limits, it is something rare and valuable: a single, sharp, parameter-free, falsifiable prediction that follows necessarily from the framework's central claim, that no rival makes the same way, and that the universe is in the middle of deciding. The framework has stuck out its neck. Now we wait — not passively, but with telescopes pointed at the deep past — to see whether nature snaps it off.

---

## Summary

- **The central claim has a forced consequence.** If a₀ is built from the dark-energy density — a₀ = (c/2)√(G ρ_DE) — then because dark energy can evolve, a₀ must evolve too. This is the framework's one genuinely new, parameter-free prediction.

- **The scaling is √ρ_DE(z).** The acceleration scale tracks the *square root* of the dark-energy density through cosmic time: a₀(z)/a₀(0) = √[ρ_DE(z)/ρ_DE(0)]. The square root is built into the formula, not chosen.

- **The prediction is genuinely parameter-free.** In the ratio a₀(z)/a₀(0), the coefficient c/2, the constant G, the geometric kernel √(8π/3), the one free number κ = ½, *and* the interpolation-function choice all cancel. Only the cosmological dark-energy history survives — and that is an input, not a knob.

- **DESI DR2 gives the working numbers.** Using the CPL parametrization (w₀ ≈ −0.75, wₐ ≈ −0.86 from DESI DR2's evolving-dark-energy fit), the density peaks at the *phantom-divide crossing* (where the equation of state passes through w = −1), near z ≈ 0.4.

- **The curve is non-monotonic: a bump, then a decline.** a₀ rises to about **+6%** above its present value at z ≈ 0.4, then falls to about **0.74** of today's value by z = 3 — up, then down. This shape is a fingerprint no constant-a₀ or rising-a₀ model reproduces; it differs from the leading rising rival by roughly **7.5×** at z = 3.

- **Only this framework makes it.** Dark matter has no acceleration scale to evolve; textbook MOND treats a₀ as a fixed constant. The framework is structurally *required* to predict evolution, because it claims a₀ is derived from dark energy rather than being a fundamental constant.

- **The cleanest test is a sign.** Through the baryonic Tully–Fisher relation (v⁴ ∝ G M a₀), the curve predicts that galaxies of fixed baryonic mass at z = 3 spin about **7% slower** than today's — *slower*, the opposite of the rising rival. The sign of the high-redshift Tully–Fisher offset, deliverable by DESI DR3 and ELT/JWST/ALMA, is the sharpest discriminator (Chapter 26).

- **Both ways, honestly.** Strong: parameter-free, distinctive, falsifiable, and under active test. Shaky: the prediction is *hostage* to DESI's contested evolving-dark-energy result, the observable signal is gentle (two nested square roots), and even a clean confirmation would leave a₀'s value underived, the Standard Model walled off, and lensing and clusters unsolved. **Not a theory of everything yet, as frustrating as it may be** — but a real bet, with the framework's neck on the line.

---

## Questions

1. **(Easy.)** In your own words, why must a₀ change over cosmic time *if* it is really made of dark energy — and why can a dark-matter particle not make the same prediction? What single feature of dark matter blocks it?

2. **(Easy–Medium.)** The framework predicts a₀ peaks about 6% above its present value near redshift 0.4 and falls to about 74% by redshift 3. Describe the *shape* of this curve in plain words, and explain what "non-monotonic" means and why the turnaround happens exactly at the phantom-divide crossing.

3. **(Medium.)** Using the working formula R(z) = (1+z)^(−0.915) · exp[1.29 · z/(1+z)] from the Worked Example, compute a₀(z)/a₀(0) at z = 2. Is your answer above or below the present-day value, and does it sit between the z = 1 and z = 3 results as you'd expect? Show each step.

4. **(Medium–Hard.)** Explain, with reference to the Deeper Dive, *why* the prediction is called "parameter-free." Specifically, which quantities cancel in the ratio a₀(z)/a₀(0), and why does the one free number κ = ½ drop out even though it is essential to fixing a₀'s present-day value? What, if anything, does the framework still contribute to the prediction?

5. **(Hard.)** The observable signal is doubly softened: a₀ goes as √ρ_DE, and rotation speed goes as a₀^¼ through the baryonic Tully–Fisher relation. Starting from the z = 3 ratio R(3) ≈ 0.74, work out the predicted fractional change in flat rotation speed for a galaxy of fixed baryonic mass. Then argue why the framework leans on measuring the *sign* of the offset rather than its precise *magnitude*.

6. **(Research-level.)** The chapter states that the prediction's distinctive shape is "hostage" to DESI DR2's contested evolving-dark-energy result, and that under some priors the evidence softens toward ~1.3σ. Suppose a future data release returns dark energy to a pure cosmological constant (w₀ = −1, wₐ = 0). Write down what a₀(z)/a₀(0) becomes in that case, explain why the prediction then loses its power to discriminate between this framework and textbook MOND, and propose what *other* observable — if any — could still distinguish a dark-energy origin of a₀ from a fixed-constant a₀ in that scenario. (Consider whether a₀ tied to *any* time-varying cosmological quantity leaves a residual signature.)
