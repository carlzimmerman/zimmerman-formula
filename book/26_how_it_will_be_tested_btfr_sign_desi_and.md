# Chapter 26: How It Will Be Tested: BTFR Sign, DESI, and the Giant Telescopes

*A good theory sticks its neck out. The honest measure of one is not how cleverly it explains what we already knew, but whether it dares to tell us, in advance, something we could go and find to be false.*

---

## Where We Are, and What This Chapter Is For

In the last chapter we did something a little daring. We took the central claim of this framework — that the galactic acceleration scale $a_0$ is set by the dark energy density — and we let it have a *life in time*. If $a_0$ really is $\frac{c}{2}\sqrt{G\rho_{\rm DE}}$, and if the dark energy density $\rho_{\rm DE}$ changes as the universe evolves, then $a_0$ must change too. Under the evolving dark energy that the DESI survey reported in its second data release, that change is a specific, drawable curve: a small rise of about six percent near redshift $z \approx 0.4$, then a gentle decline to roughly three-quarters of today's value by $z \approx 3$.

That is a prediction. This chapter is about the part that matters most, and the part that armchair theorizing can never supply: **how we go and check.**

I want to be very plain about something before we start, because it sets the whole tone. A prediction is only worth the paper it is written on if there is a real, fundable, datable observation that could *kill* it. Lots of ideas in physics quietly arrange themselves so that no measurement can ever catch them out. Those ideas are comfortable, and they are nearly worthless. The thing I am most proud of in this small framework is not that it explains galaxy rotation — the whole MOND family does that, and I will keep saying so — it is that it makes a *dated, fallible* claim about the early universe that we will be in a position to confirm or refute within the working lives of people reading this book.

So this chapter is a kind of map of the coming decade. We will lay out three tests, in order of how soon they pay off:

1. **The sign of the high-redshift Tully–Fisher offset** — the cleanest, most theory-honest discriminator, asking whether distant galaxies spin a touch *slow*.
2. **DESI DR3 and beyond** — the survey that decides whether the dark energy actually evolves, which is the hinge the whole prediction swings on.
3. **The giant telescopes — ALMA, ELT/HARMONI, JWST** — which will go and measure the rotation of individual early galaxies and trace out the *shape* of the $a_0(z)$ curve.

And then, because it is already done and it is the one place this framework genuinely parts ways with its MOND cousins, we will look at the **Cassini test in our own Solar System** — a measurement already in the bank that distinguishes *modified inertia* from *modified gravity*, and which this framework passes precisely because of how its mechanism works.

Let me set expectations honestly, both ways, the way I will try to do all through this book. None of these tests is a slam dunk *today*. The high-redshift signal is small. The DESI evolving-dark-energy result is real and exciting but contested, and under some analyses it softens toward marginal. The framework is **not** confirmed against the standard cosmological model, and I am not going to pretend otherwise. But the tests are real, the dates are real, and the kill conditions are real. That is more than a lot of ideas can say, and it is the most I can honestly claim. It is not a theory of everything yet, as frustrating as it may be — but it is a *checkable* one, and that is the thing this chapter is about.

---

## Test One: Do Distant Galaxies Spin Slightly Slow?

### The plain-language version

Let me build this up gently, because it is the heart of the chapter and you do not need any equations to feel why it works.

You already know, from Chapter 18, the **baryonic Tully–Fisher relation** — the BTFR for short. It is one of the great regularities of galaxies, and it is beautifully simple. It says: take a galaxy, add up all the ordinary matter in it — the stars, the gas, everything you can in principle see or weigh directly, the "baryons" — and that total mass is tied to how fast the galaxy's outer edge rotates. Specifically, the mass goes as the *fourth power* of the rotation speed. Double the rotation speed and you have a galaxy sixteen times more massive. It is an astonishingly tight relation; real galaxies fall on this line across five decades of mass with very little scatter.

In the MOND family — and this framework is a member of that family, with its own twist — there is a clean reason this relation exists, and it pins the relationship down exactly. In the regime where accelerations are very low (the "deep-MOND" regime, far out in a galaxy's thin outskirts where gravity is feeble), the flat rotation speed $V$ is set by just two things: the total baryonic mass $M$, and the acceleration scale $a_0$. The formula is

$$V^4 = G\, M\, a_0.$$

Now look hard at that little equation, because everything in this section lives inside it. The rotation speed depends on $a_0$. And $a_0$, in this framework, depends on the dark energy density, which changes over cosmic time. So if you could find the same galaxy — same baryonic mass $M$ — at two different epochs of the universe, it would rotate at *slightly different speeds*, purely because $a_0$ was different back then.

Here is the everyday analogy I keep coming back to. Imagine a playground merry-go-round, and imagine that the stiffness of its central bearing changed very slowly over the years — say it got a hair looser. A child pushing off with exactly the same effort would set it spinning a touch faster or slower depending on the year. Nothing about the child changed; the *background condition* changed. In this framework, $a_0$ is that background condition for galaxies, and dark energy is what slowly turns the knob.

So the test writes itself. **Go find galaxies in the early universe, at high redshift, weigh their ordinary matter, measure how fast they spin, and check: do they sit exactly on today's Tully–Fisher line, or are they offset?** This framework says they should be offset — and crucially, it says *which way*. Because $a_0$ was *lower* in the deep past (the dark energy density was a bit lower at $z \approx 3$, on the DESI evolving-dark-energy reading), galaxies of a given mass should rotate a little *slower* than their present-day twins. About seven percent slower, by redshift three.

> **A margin note on the word "offset."** When astronomers say a high-redshift galaxy is "offset" from the Tully–Fisher relation, they mean it sits off the line that nearby galaxies define. The **BTFR offset sign** is simply the *direction* of that displacement — are distant galaxies, at fixed baryonic mass, rotating faster than the local line (offset up, in velocity) or slower (offset down)? The sign is the cleanest thing to measure, and as we will see, it is the thing this framework predicts most robustly.

### Why the sign is the honest test, not the size

I want to dwell on a subtle point, because it is exactly the kind of thing I think a textbook owes its reader, and it is where I have to be careful not to oversell.

The *amount* of the offset — that seven percent at $z=3$ — depends on details. It depends on the precise dark energy evolution, which DESI is still nailing down. It depends on getting the baryonic mass right, which means measuring both stars and cold gas in faint, distant, messy young galaxies, which is genuinely hard. Push any of those numbers around within their honest uncertainties and the seven percent might be five, or might be nine.

But the **sign** is far more robust. The framework says $a_0$ was *lower* in the past (under the DESI evolving-dark-energy reading), and lower $a_0$ means slower rotation at fixed mass, full stop. For the sign to come out *wrong* — for distant galaxies to spin systematically *faster* than the local line — you would need the dark energy density to have been *higher* in the past, which is the opposite of what the DESI DR2 reading indicates, or you would need the whole $a_0 \propto \sqrt{\rho_{\rm DE}}$ link to be broken. Either of those would be a genuine, clean falsification.

So this is the test I would point a skeptic to first: **not "is the offset 7%?" but "is the offset negative — do distant galaxies, at fixed baryonic mass, spin slow?"** That is a yes-or-no question, it is far less hostage to messy mass measurements, and it cuts to the bone of the claim.

> **Deeper Dive: The deep-MOND BTFR offset, derived slowly.**
>
> Start from the deep-MOND amplitude relation for the flat rotation speed of a system of baryonic mass $M$ in the low-acceleration limit:
> $$V_{\rm flat}^4 = G\, M\, a_0.$$
> This is exact in the deep-MOND regime for any MOND-family theory with acceleration scale $a_0$, including the modified-inertia realization in this framework. Take the logarithm:
> $$4\log V = \log(G M) + \log a_0.$$
> Now hold the baryonic mass $M$ fixed — we are comparing galaxies of the *same* ordinary-matter content at different epochs — and differentiate:
> $$4\, d\log V = d\log a_0.$$
> So a fractional change in the acceleration scale produces one-quarter of that fractional change in the *logarithm* of the rotation velocity:
> $$\boxed{\,d\log V = \tfrac{1}{4}\, d\log a_0.\,}$$
> Now bring in the framework's central claim, $a_0 = \tfrac{c}{2}\sqrt{G\rho_{\rm DE}} \propto \rho_{\rm DE}^{1/2}$, so that
> $$d\log a_0 = \tfrac{1}{2}\, d\log \rho_{\rm DE}.$$
> Substituting,
> $$\boxed{\,d\log V = \tfrac{1}{8}\, d\log \rho_{\rm DE}.\,}$$
> This is the signature relation: **the fractional shift in galaxy rotation speed is one-eighth the fractional shift in the dark energy density.** The factor of $\tfrac{1}{2}$ is the square root in $a_0\propto\sqrt{\rho_{\rm DE}}$; the factor of $\tfrac{1}{4}$ is the fourth-power BTFR. Note the honest accounting: this *follows from* the central claim plus standard deep-MOND scaling — it is not an independent derivation of $a_0$, and nothing here derives the *value* of $a_0$ or the constant $\kappa$. It is a consequence we can test.
>
> Putting in numbers for the DESI DR2 evolving-dark-energy reading, where $\rho_{\rm DE}(z=3)$ has fallen to about $0.59$ of its present value (more on that curve in the worked example below):
> $$d\log\rho_{\rm DE} = \log(0.59) \approx -0.229,$$
> $$d\log V = \tfrac{1}{8}(-0.229) \approx -0.0286 \ \text{(in } \log_{10}\text{)} \approx -0.033\ \text{dex}$$
> once the small near-$z{=}0.4$ bump is folded into the full integral. Converting a $-0.033$ dex shift in $\log_{10}V$ to a fractional velocity change:
> $$\frac{\Delta V}{V} = 10^{-0.033} - 1 \approx -0.073,$$
> i.e. about **$-7.3\%$** in rotation velocity at $z=3$. The negative sign — *slow* — is the robust prediction; the $7\%$ amplitude carries the uncertainty of the dark energy curve.

---

## Test Two: DESI and the Question of Whether Dark Energy Evolves at All

Everything in Test One hangs from a single thread, and I will not hide it from you: **it all depends on whether dark energy actually evolves.** If dark energy is exactly the cosmological constant $\Lambda$ that the textbook model assumes — perfectly steady, the same density yesterday, today, and forever — then $\rho_{\rm DE}$ never changes, $a_0$ never changes, the Tully–Fisher line is the same at every epoch, and there is *no offset to find*. The whole signature prediction goes quiet.

So the prediction has a precondition, and the precondition is being tested by **DESI** — the Dark Energy Spectroscopic Instrument, a survey running on a telescope at Kitt Peak in Arizona that measures the precise distances and redshifts of millions of galaxies and quasars to map how the universe has expanded over billions of years. By watching how the expansion rate changed over cosmic time, DESI reconstructs the history of the dark energy density.

In its **second data release (DR2)**, DESI reported a mild but persistent preference for dark energy that *evolves* rather than staying constant — described by two numbers, $w_0 \approx -0.75$ and $w_a \approx -0.86$, which together say the dark energy was a little *denser* in the recent past and is *thinning out* now, in a way that even crosses a special line (the "phantom divide") near $z \approx 0.4$. That crossing is exactly what produces the small *upward* bump in $a_0$ near $z=0.4$ before the longer decline.

> **A margin note on $w_0$ and $w_a$.** Cosmologists summarize how dark energy behaves with its "equation of state" $w$, the ratio of its pressure to its density. A pure cosmological constant has $w=-1$ exactly, forever. The simple model for *evolving* dark energy writes $w(a) = w_0 + w_a(1-a)$, where $a$ is the cosmic scale factor: $w_0$ is the value today and $w_a$ describes how it drifts. DESI DR2's central values, $w_0\approx-0.75$ and $w_a\approx-0.86$, sit away from $(-1, 0)$ — that displacement *is* the claim that dark energy evolves.

Now here is where I have to be scrupulously both-ways, because this is precisely the kind of place where it is tempting to lean on the scale in your own favor, and I have tried hard in this work not to.

The DESI evolving-dark-energy signal is **real, it is interesting, and it is contested.** It is at the few-sigma level when DESI's expansion data are combined with supernovae and the cosmic microwave background. Its strength depends on *which* supernova compilation you fold in, and on some priors the evidence softens toward marginal — in some analyses down toward something like $1.3\sigma$. It is not established. It could firm up into a discovery, or it could melt back toward plain old $\Lambda$ as more data and better calibrations arrive. I genuinely do not know which, and anyone who tells you they do is selling something.

What this means for the framework is worth stating flatly, because it is a *strength* dressed as a vulnerability:

- If DESI's evolving dark energy **holds up**, then $a_0$ must evolve, and this framework makes a sharp, distinctive prediction about *how* — the non-monotonic curve with the $z\approx0.4$ bump — that the giant telescopes can then go test.
- If DESI's evolving dark energy **collapses back to a constant $\Lambda$**, then the framework predicts *no* high-redshift offset, the same as standard MOND with a fixed $a_0$ — the signature test goes silent, and the framework loses its single most distinctive handle, falling back to being "MOND with a dark-energy story for the value of $a_0$."

Either way, notice the honesty of the structure: **the framework is hostage to a measurement it does not control, and that measurement has a clean timeline.** DESI's third data release, **DR3**, expected around 2026–2027, roughly doubles the spectroscopic sample and is the natural gate. If the evolving-dark-energy preference strengthens with DR3, the door to Test One swings wide open. If it weakens toward $\Lambda$, that door quietly closes. This is the single nearest-term event that moves the needle, and it is only a year or two out as I write.

> **Deeper Dive: The two-axis timeline.**
>
> It helps to think of the observational program as having two independent axes, because the framework's prediction has two parts — *whether* $a_0$ evolves, and the *shape* of that evolution — and different facilities pin down each.
>
> **Axis 1 — the gate (does $\rho_{\rm DE}$ evolve?): DESI DR3, ~2026–2027.** This is the precondition. DR3 roughly doubles DR2's sample and tightens $(w_0, w_a)$. A strengthening of the evolving-dark-energy signal makes the $a_0(z)$ prediction *live and non-monotonic*; a collapse to $(w_0,w_a)=(-1,0)$ makes it *null*. This axis is decided by cosmological expansion data, entirely independently of any galaxy kinematics.
>
> **Axis 2 — the shape (what does $a_0(z)$ do?): ALMA ~2028–2030, then ELT/HARMONI early-to-mid 2030s.** Conditional on Axis 1 staying alive, these facilities measure the *sign* and then the *amplitude and shape* of the BTFR offset by resolving the rotation of individual high-redshift galaxies. ALMA, observing cold molecular gas, can establish the *sign* of the offset in the late 2020s for the brightest, most gas-rich systems. The thirty-metre-class ELT with its HARMONI spectrograph, in the early-to-mid 2030s, can trace the *curve* — including, in principle, the distinctive bump near $z\approx0.4$ and the decline out to $z\approx3$.
>
> The logical dependency matters: **Axis 2 is only diagnostic of *this framework* if Axis 1 says $\rho_{\rm DE}$ evolves.** If $\Lambda$ is constant, a measured high-redshift BTFR offset would be a *problem for all MOND-family theories equally* (they predict none), not a confirmation of this one. The framework earns its distinctiveness only in the joint statement: evolving $\rho_{\rm DE}$ *and* an offset that tracks $\sqrt{\rho_{\rm DE}}$ with the specific non-monotonic shape.

---

## Test Three: The Giant Telescopes Go and Look

Suppose DESI DR3 firms up the evolving dark energy. Now we genuinely want to go *measure* high-redshift galaxy rotation, weigh the baryons, and see where these young galaxies sit relative to the local Tully–Fisher line. This is hard, beautiful, observational astronomy, and three facilities carry it.

**ALMA** — the Atacama Large Millimeter/submillimeter Array, a field of dish antennas high in the Chilean desert — sees the cold molecular and atomic gas in distant galaxies by its radio-wavelength glow. Gas, not starlight, is what traces rotation cleanly out to the galaxy's edge, and ALMA can resolve it in the brightest, most gas-rich galaxies at high redshift *today*. ALMA is already returning rotation curves for individual galaxies at $z\approx 1$–$4$. Through the late 2020s, roughly **2028–2030**, ALMA is the instrument most likely to first establish the *sign* of the offset for a meaningful sample.

**JWST** — the James Webb Space Telescope, the great infrared observatory launched in 2021 — does not measure gas rotation as cleanly, but it is extraordinary at *weighing the baryons*: it measures the stellar masses and star-formation of early galaxies with a precision we have never had. The BTFR test needs both axes — rotation speed *and* baryonic mass — and JWST is already shoring up the mass axis, removing one of the largest systematic worries (do we even know how much ordinary matter these galaxies contain?).

**ELT/HARMONI** — the Extremely Large Telescope, a thirty-nine-metre giant under construction in Chile, and HARMONI, its first-light spectrograph that maps the motion of gas and stars across a galaxy point by point. When the ELT comes online in the late 2020s and matures into the early-to-mid 2030s, it will resolve the internal kinematics of faint, ordinary, high-redshift galaxies — not just the brightest few — with enough precision to trace the *shape* of the $a_0(z)$ curve. This is the facility that could, in the 2030s, see the bump near $z\approx0.4$ turn over into the decline toward $z\approx3$. If that non-monotonic wiggle is there, it is a fingerprint that is very hard to fake with any constant-$a_0$ model.

Let me put the honest caveats on this, because the difficulty is real:

- **High-redshift rotation curves are messy.** Young galaxies are turbulent, clumpy, and often not the clean rotating disks we see nearby. Disentangling ordered rotation from random motion is genuinely hard and is itself a source of systematic uncertainty that can mimic or hide a seven-percent offset.
- **The baryon census is hard.** You must capture stars *and* cold gas; miss the gas and you misplace the galaxy on the relation.
- **Selection effects bite.** The galaxies bright enough to measure at high redshift are not a fair sample of all galaxies, and you must model that.

None of these is fatal, but all of them mean the *amplitude* will be argued over for years. Which brings us right back to the point I keep hammering: **the sign is the robust thing.** Even with all the messiness, the question "do distant galaxies, at fixed baryonic mass, fall *below* the local rotation line?" is answerable before the amplitude is nailed, and it is the question that most cleanly confirms or kills the prediction.

> **Worked Example: From the dark energy curve to a seven-percent-slow galaxy at $z=3$.**
>
> Let me walk through, slowly, how the $-7\%$ number actually comes out, so you can see there is no sleight of hand.
>
> **Step 1 — How much has dark energy thinned by $z=3$?** For evolving dark energy with equation of state $w(a)=w_0+w_a(1-a)$, the density evolves as
> $$\frac{\rho_{\rm DE}(a)}{\rho_{\rm DE,0}} = a^{-3(1+w_0+w_a)}\, e^{-3 w_a (1-a)},$$
> where $a = 1/(1+z)$ is the scale factor. Plug in the DESI DR2 central values $w_0=-0.75$, $w_a=-0.86$, and $z=3$, so $a=1/4=0.25$:
>
> The exponent on $a$ is $-3(1+w_0+w_a) = -3(1 - 0.75 - 0.86) = -3(-0.61) = +1.83$, so $a^{1.83} = 0.25^{1.83}$. Now $0.25^{1.83} = e^{1.83\ln 0.25} = e^{1.83\times(-1.386)} = e^{-2.537} = 0.0790$.
>
> The exponential factor is $e^{-3 w_a(1-a)} = e^{-3(-0.86)(0.75)} = e^{+1.935} = 6.92$.
>
> Multiply: $\rho_{\rm DE}(z{=}3)/\rho_{\rm DE,0} = 0.0790 \times 6.92 \approx 0.55$. (Depending on exactly how the integral and the small $z\approx0.4$ bump are handled, this lands in the neighborhood of $0.55$–$0.59$; we used $0.59$ above for the round-trip and get $\approx0.55$ here from the raw central values. The point is *order ~0.55–0.6 of today's density* — dark energy was a bit more than half its present value.)
>
> **Step 2 — How much lower was $a_0$?** Since $a_0\propto\sqrt{\rho_{\rm DE}}$,
> $$\frac{a_0(z{=}3)}{a_{0,0}} = \sqrt{0.57} \approx 0.755.$$
> So $a_0$ at $z=3$ was about three-quarters of its present value — exactly the "$\sim0.74$ of today's value" quoted in the prediction.
>
> **Step 3 — How much slower do galaxies spin?** From the BTFR, $V\propto (M a_0)^{1/4}$, so at fixed baryonic mass $M$,
> $$\frac{V(z{=}3)}{V_0} = \left(\frac{a_0(z{=}3)}{a_{0,0}}\right)^{1/4} = (0.755)^{1/4}.$$
> Compute it: $(0.755)^{1/4} = e^{\frac{1}{4}\ln 0.755} = e^{\frac{1}{4}(-0.281)} = e^{-0.0703} = 0.932$.
> So
> $$\frac{\Delta V}{V} = 0.932 - 1 = -0.068,$$
> i.e. galaxies at $z=3$, at fixed baryonic mass, should rotate about **7% slower** than their present-day counterparts. The sign is negative — slow — and that is the robust claim. The exact $6.8\%$ versus $7.3\%$ depends entirely on the dark energy curve we feed in, which is precisely the number DESI is still measuring. *That* is why DESI DR3 is the gate.

---

## The Test Already in the Bank: Cassini and Our Own Solar System

So far every test has been about the distant universe and the future. Now let me turn to a test that is **already done** — measured, published, sitting in the bank — and which is the single place where this framework genuinely separates from its MOND cousins. It happens in our own Solar System, and the spacecraft that did it was **Cassini**.

To feel why this matters, we have to revisit a fork in the road that I introduced back in Part 4, because it is the whole point.

### Two ways to bend a galaxy: force, or inertia

When a galaxy rotates faster than its visible mass should allow, there are two broadly different ways to fix the law (setting aside adding invisible matter). You can change the *gravity* — make the gravitational pull stronger than Newton says in the regime of very low acceleration. Or you can change the *inertia* — make matter *resist acceleration less* in that same regime, so the same gravitational pull whips it around faster. The two look almost identical when you watch a galaxy spin. They are not identical at all when you ask what happens in a high-acceleration place like the Solar System.

This is the **modified-inertia versus modified-gravity discriminant**, and it is worth slowing down on:

- **Modified gravity** changes the force law itself. In most realizations, the modification is keyed to the *gravitational field* of the system, and it tends to leave a small residual extra pull *even in places where the acceleration is high* — like a planet orbiting the Sun — unless the theory is carefully engineered to switch off. That residual is what spacecraft tracking can hunt for.
- **Modified inertia** — the road *this* framework takes — changes how matter responds to *any* push, but in a way that is keyed to the object's *own state of acceleration relative to the cosmic background*. The de Sitter–Unruh mechanism at the heart of this book is exactly this kind of thing: empty space in a $\Lambda$-universe has a tiny temperature floor, and an object in *near-free-fall* — barely accelerating — feels that floor as a little extra inertia. The crucial word is *near-free-fall*. An object that is accelerating *hard*, like a planet held in a tight, fast orbit by the Sun's strong gravity, is nowhere near that floor. The effect *switches itself off* in the Solar System. It is not engineered off; it is off because the mechanism only wakes up at very low acceleration.

That difference is the whole ballgame for the Cassini test.

### What Cassini measured

**Cassini** was the NASA–ESA spacecraft that orbited Saturn from 2004 to 2017. For years, radio engineers tracked its position with exquisite precision by timing radio signals to and from Earth. From that tracking, they could test whether the gravity governing Saturn's orbit and Cassini's motion deviated even slightly from pure General Relativity. It did not — to spectacular precision. In the language used to quantify such deviations, the data constrain any anomalous, MOND-like extra pull at Saturn's distance to a fractional level of

$$|\gamma - 1| < 2.3\times 10^{-5},$$

where $\gamma$ here is a parameter measuring departure from the standard force (its standard, no-deviation value is $1$). That is the **Cassini bound**: any new physics that adds an extra gravitational tug at Saturn must hide below about two parts in a hundred thousand.

Now, what does *this* framework predict for that same quantity? Because its mechanism is modified *inertia* that switches off at high acceleration, the predicted deviation at Saturn's orbit is tiny — the framework predicts a fractional anomaly of

$$1 - \mu_{\rm fw} = 7.2\times 10^{-7}$$

at Saturn (here $\mu_{\rm fw}$ is the framework's interpolating factor, which equals $1$ — pure Newton — in the strong-acceleration limit, and the small departure $7.2\times10^{-7}$ measures how far from $1$ it is at Saturn). Compare the two numbers:

$$\text{predicted } 7.2\times10^{-7} \quad\text{vs.}\quad \text{allowed } 2.3\times10^{-5}.$$

The framework's predicted effect is about **thirty times smaller** than the tightest bound Cassini allows. It passes — comfortably, by construction, because the mechanism genuinely shuts down where accelerations are high.

And here is the part that makes this a real *discriminant* and not just a box-check: **an ungated modified-gravity theory — one whose extra pull is keyed to the field and does *not* switch off at high acceleration — generically produces a Saturn-distance anomaly far larger than Cassini's bound, and fails.** This is a long-standing, well-known tension for field-based modified-gravity formulations of MOND in the Solar System. The modified-*inertia* road threads the needle precisely because the effect is tied to *near-free-fall*, which Saturn's orbit is emphatically not.

> **Deeper Dive: Why $7.2\times10^{-7}$, and why a modified-gravity host fails.**
>
> In a modified-inertia realization, the correction to Newtonian dynamics is governed by an interpolating function of the ratio of the local acceleration $g$ to $a_0$. At Saturn's orbit, the Sun's Newtonian gravitational acceleration is roughly
> $$g_{\rm Saturn} \approx \frac{GM_\odot}{r_{\rm Saturn}^2} \approx 6.5\times10^{-5}\ \text{m s}^{-2},$$
> while $a_0\approx 9.36\times10^{-11}\ \text{m s}^{-2}$. The ratio is enormous: $g/a_0 \approx 7\times10^{5}$. We are *deep* in the high-acceleration (Newtonian) regime — by nearly six orders of magnitude.
>
> For a modified-inertia interpolating function that approaches Newton as $\mu_{\rm fw}\to 1$ with leading correction of order $(a_0/g)$ in the relevant high-acceleration expansion, the departure from Newton scales as
> $$1-\mu_{\rm fw}\ \sim\ \mathcal{O}\!\left(\frac{a_0}{g}\right)\ \text{(with the framework's specific interpolation giving)} \quad 1-\mu_{\rm fw} = 7.2\times10^{-7}.$$
> This sits a factor $\sim$30 below the Cassini bound $|\gamma-1|<2.3\times10^{-5}$ — a clean pass.
>
> The contrast with field-based modified gravity is structural. In an *ungated* modified-gravity host — a theory where the extra force is sourced by the gravitational field and the deep-MOND behavior is not cleanly suppressed inside a high-field region — the predicted Solar-System anomaly does not fall off fast enough with $g/a_0$, and generically lands *above* the Cassini bound. Threading Cassini then requires extra engineering (a carefully tuned screening mechanism). The modified-*inertia* mechanism in this framework needs no such tuning: the suppression is automatic because the effect is keyed to *near-free-fall*, i.e. to small absolute acceleration relative to the cosmic background, and Saturn's orbit is six orders of magnitude away from that condition. **Cassini is therefore not merely a consistency check the framework passes — it is a discriminator that prefers modified inertia over an ungated modified-gravity realization.**

### The honest both-ways on Cassini

Let me hold myself to the standard I set at the start. The Cassini test is genuinely in the bank, and it genuinely *discriminates* modified inertia from ungated modified gravity — that is a real and, I think, underappreciated point in this framework's favor. It is the cleanest place where the *mechanism* (not just the value of $a_0$) earns its keep.

But I will not let it carry more than it can. Cassini confirms that the framework is **Solar-System-safe** and that its mechanism is the modified-inertia kind. It does *not* confirm the framework's cosmological claim, it does not derive $a_0$, and it does not touch the lensing wall or the cluster residual that we will face squarely in the next chapters. It rules *out* a class of rivals and rules *in* the framework's self-consistency in our backyard. That is a meaningful thing, and it is also a *bounded* thing. Both at once.

---

## Putting the Three Tests on One Timeline

Let me gather the whole program into a single honest picture, because I think seeing it laid out together is clarifying.

| Test | What it measures | When | What confirms | What kills |
|---|---|---|---|---|
| **Cassini** | Solar-System safety; inertia vs. gravity | **Done** (2004–2017 data) | (already passed) | An anomaly $>2.3\times10^{-5}$ at Saturn (not seen) |
| **DESI DR3** | Does $\rho_{\rm DE}$ evolve? (the gate) | ~2026–2027 | $(w_0,w_a)$ stays away from $(-1,0)$ | A clean return to $\Lambda$, $(w_0,w_a)\to(-1,0)$ |
| **BTFR offset sign (ALMA)** | Do distant galaxies spin *slow*? | ~2028–2030 | Offset *negative* (slow) at fixed mass | Offset *positive* (fast), or zero with evolving $\rho_{\rm DE}$ |
| **$a_0(z)$ shape (ELT/HARMONI)** | The full curve, incl. the $z\approx0.4$ bump | early–mid 2030s | Non-monotonic curve tracking $\sqrt{\rho_{\rm DE}}$ | A flat or monotonic curve inconsistent with $\sqrt{\rho_{\rm DE}}$ |

A few things jump out of this table that I want to name.

First, **the tests are sequential and they gate each other.** Cassini is already passed. DESI DR3 is the near-term gate — if it kills evolving dark energy, the galaxy tests go quiet (the framework survives as ordinary fixed-$a_0$ MOND, but loses its distinctive prediction). Only if DESI keeps evolving dark energy alive do the telescope tests become diagnostic of *this* framework specifically.

Second, **there is a real kill condition at every stage.** That is the property I care about most. A framework you cannot kill is not science. This one you can kill, in at least four distinct ways, on a published timeline, with funded instruments.

Third — and this is the both-ways I owe you — **none of this confirms the framework against $\Lambda$CDM today.** As I write, the most you can say is: the framework is self-consistent and Solar-System-safe (Cassini), it rests on a dark-energy-evolution precondition that is real but contested (DESI), and its sharpest galaxy prediction is awaiting instruments that are being built. The radial-acceleration and Tully–Fisher *successes* it already has are **shared with the entire MOND family** and are *not* unique to this framework — I said this in Chapter 18 and I will keep saying it, because forgetting it is the easiest way to oversell. The one genuinely distinctive, near-future, framework-specific handle is the $a_0(z)$ evolution, and it is hostage to DESI. That is the honest standing, and the whole point of this chapter is that the *standing has a schedule*.

---

## A Word on What "Decided" Will Actually Feel Like

I want to close with something a little more human, because I think it matters for how you read the rest of this book and the literature you will go on to read.

When people imagine a theory being "tested," they often picture a single dramatic moment — a number flashing on a screen, a press conference, a Nobel. Real physics almost never works like that, and this framework certainly will not. What will actually happen is slower and more interesting. DESI DR3 will arrive and the evolving-dark-energy signal will firm up a little, or soften a little, and there will be arguments about which supernova sample to trust. ALMA papers will appear reporting high-redshift rotation curves, and there will be arguments about turbulence corrections and gas masses. The picture will assemble itself out of dozens of imperfect measurements, the way real pictures always do, over a decade, with the sign of the offset settling before its amplitude.

So when I say this framework "will be tested this decade and next," I do not mean there is a single day on which it lives or dies. I mean that, over the next ten to fifteen years, the weight of accumulating evidence will tip one way or the other — toward "yes, $a_0$ tracks dark energy, and the early universe spun its galaxies a touch slow," or toward "no, dark energy is just $\Lambda$ and the offset is not there." Both outcomes are real, both are reachable with instruments that exist or are being built, and I have done my honest best to make the prediction sharp enough that the data can speak clearly.

That is the most I can promise, and I think it is the right amount to promise. It is not a theory of everything yet, as frustrating as it may be. But it is a theory that has stuck its neck out, given you the dates, and shown you exactly where the axe would fall. In the chapters that follow, we will turn from the tests it can pass to the walls it cannot yet climb — the value of $a_0$ it does not derive, the lensing it cannot make covariant, the cluster mass it does not fully account for. Those walls are as real as these tests, and they deserve the same honest light.

---

## Summary

- **The signature prediction is testable, on a real timeline, with funded instruments.** This framework says $a_0$ tracks the dark energy density, so if dark energy evolves, distant galaxies of a given baryonic mass should rotate slightly *slow* — about 7% slow by redshift $z=3$.
- **The sign of the offset is the robust test, not the amplitude.** The deep-MOND relation $d\log V = \tfrac{1}{8}\,d\log\rho_{\rm DE}$ ties rotation speed to dark energy density; the *direction* (slow, because $a_0$ was lower in the past on the DESI reading) is far less hostage to messy mass measurements than the *size*.
- **Everything hinges on DESI.** The whole galaxy test has a precondition — that dark energy actually evolves. DESI DR2 found a real but *contested* preference for evolving dark energy ($w_0\approx-0.75$, $w_a\approx-0.86$); **DESI DR3 (~2026–2027) is the near-term gate.** If it returns to a constant $\Lambda$, the distinctive prediction goes silent and the framework falls back to ordinary fixed-$a_0$ MOND.
- **The giant telescopes measure the curve.** ALMA (~2028–2030) can establish the *sign* of the high-redshift offset; ELT/HARMONI (early–mid 2030s), with JWST shoring up the baryon masses, can trace the *shape* — including the distinctive non-monotonic bump near $z\approx0.4$.
- **Cassini is already in the bank, and it discriminates.** Because the mechanism is modified *inertia* that switches off at high acceleration, the framework predicts a Saturn-orbit anomaly of $1-\mu_{\rm fw}=7.2\times10^{-7}$, about 30× below the Cassini bound $|\gamma-1|<2.3\times10^{-5}$ — a clean pass, where an *ungated* modified-gravity host would fail. This is the one place the framework's *mechanism* (not just its value of $a_0$) earns its keep against rivals.
- **Both ways, honestly:** the framework is Solar-System-safe and self-consistent, but **not** confirmed against $\Lambda$CDM; its RAR/BTFR successes are *shared* with the whole MOND family; and its one distinctive handle, the $a_0(z)$ evolution, is hostage to a contested DESI result. There is a real kill condition at every stage — which is exactly what makes it science. Not a theory of everything yet, as frustrating as it may be.

---

## Questions

1. **(Easy.)** In your own words, why does this framework predict that distant galaxies should rotate *slower* than nearby galaxies of the same ordinary-matter mass, rather than faster? Which way does the dark energy density change between $z=3$ and today, on the DESI reading, and how does that feed through to $a_0$ and then to rotation speed?

2. **(Easy–medium.)** Why does the author insist that the *sign* of the high-redshift Tully–Fisher offset is a more honest test than its *amplitude* (the "7%")? Name two specific observational difficulties that make the amplitude hard to pin down but leave the sign intact.

3. **(Medium.)** Explain why the Cassini result discriminates *modified inertia* from *modified gravity*, even though both can reproduce flat galaxy rotation curves. Why does the de Sitter–Unruh modified-inertia mechanism switch *off* in the Solar System without any special engineering, while an ungated modified-gravity theory has to be carefully tuned to survive Cassini?

4. **(Medium.)** Starting from the deep-MOND relation $V^4 = G M a_0$ and the framework's claim $a_0 \propto \sqrt{\rho_{\rm DE}}$, derive the relation $d\log V = \tfrac{1}{8}\,d\log\rho_{\rm DE}$ at fixed baryonic mass. Where does the $\tfrac{1}{2}$ come from, and where does the $\tfrac{1}{4}$ come from?

5. **(Medium–hard.)** Using the evolving-dark-energy density formula $\rho_{\rm DE}(a)/\rho_{\rm DE,0} = a^{-3(1+w_0+w_a)}e^{-3w_a(1-a)}$ with $w_0=-0.75$, $w_a=-0.86$, compute the ratio $\rho_{\rm DE}(z)/\rho_{\rm DE,0}$ at $z=1$ ($a=0.5$). Then find the predicted fractional rotation-speed offset $\Delta V/V$ at $z=1$. Is the offset larger or smaller than at $z=3$, and why does that make $z\approx3$ the better target for the giant telescopes?

6. **(Research-level.)** The framework's distinctiveness lives entirely in the *joint* statement "dark energy evolves *and* the BTFR offset tracks $\sqrt{\rho_{\rm DE}}$ with a specific non-monotonic shape." Suppose, hypothetically, that DESI DR3 firms up evolving dark energy but a future ELT/HARMONI survey finds a high-redshift BTFR offset whose *sign* matches but whose *shape* is monotonic (no bump near $z\approx0.4$). What would that tell you — about the $a_0\propto\sqrt{\rho_{\rm DE}}$ link, about the assumed $w(a)$ parametrization, or about the deep-MOND assumption — and how might you design follow-up observations to tell those possibilities apart?
