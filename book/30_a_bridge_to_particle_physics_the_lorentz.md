# Chapter 30: A Bridge to Particle Physics: The Lorentz-Violation Interface

> *Sometimes the most interesting door in a house is the one you didn't build on purpose — the gap under the stairs you only notice because a draft keeps coming through it.*

For twenty-nine chapters we have been talking about gravity and the large, slow universe: spinning galaxies, the weight of clusters, the temperature of empty space, the acceleration scale a₀. We have been very careful, all along, to keep one promise: this framework does **not** touch the Standard Model of particle physics. It says nothing about why the electron weighs what it weighs, nothing about quarks or the Higgs, nothing about the masses of the fundamental particles. We have walled that off, deliberately and repeatedly, and we will keep walling it off in the chapters that remain.

So it may come as a surprise — it certainly surprised me — that there is exactly **one** place where the framework cannot help but leave a fingerprint in the world of particle physics. Not because we reached over the wall and meddled. We didn't. The fingerprint is forced on us by something we already admitted the theory does: it quietly picks out a **preferred frame** in the universe, a special state of rest. And once you have a preferred frame, the rest of physics is obligated to notice. There is a draft coming through that gap under the stairs whether we like it or not.

This chapter is about that draft. It is a genuinely lovely piece of physics, and it is also a place where I have to be more careful with my words than almost anywhere else in the book. Because the temptation here — the temptation that would make this framework look far more powerful than it is — would be to say that the theory *explains* or *predicts* something deep about particle physics. It does not. What it does is much humbler, and I want to get the verb exactly right: it **induces** a small, computable effect, with a size **inherited** from a number (a₀) we already had. It does not *derive* anything new about particles. Hold onto that distinction; it is the whole moral of the chapter, and I will repeat it more times than is strictly polite.

Let me build up to it slowly.

## A preferred frame, and why it matters

Start with a word we have used loosely and now need to pin down: **frame**, short for *reference frame*. A reference frame is just a point of view from which you measure things — a particular choice of "what counts as standing still" and "what counts as moving." If you are reading this on a train, the seat across from you is at rest *in your frame*, even though a cow in a field watches the whole train hurtle past *in its frame*. Both points of view are legitimate. That, in one sentence, is the heart of Einstein's relativity: the laws of physics look the same in every frame moving at a steady velocity. There is no experiment you can do inside a sealed, smoothly-moving train car to tell whether you are moving or standing still. No frame is special. This deep democracy of viewpoints is called **Lorentz symmetry** (after Hendrik Lorentz, whose equations describe how measurements of space and time translate from one frame to another), and it is one of the most thoroughly tested principles in all of science.

Now here is the uncomfortable thing about our framework, which we have actually known since the lensing chapters. The de Sitter–Unruh mechanism leans on a particular special state: the state of *being at rest with respect to the cosmic horizon*, the same rest frame in which the cosmic microwave background looks uniform in every direction, the average rest frame of the universe itself. The acceleration that feeds the whole mechanism is acceleration *relative to that frame*. The theory, in other words, has a **preferred frame**: a specific state of motion that it treats as genuinely special, not just one democratic viewpoint among equals.

A preferred frame breaks the perfect democracy. It is as if the universe, very gently, painted one seat on the train gold. Most of the time you would never notice — the effect, as we will see, is staggeringly tiny. But "you would never notice" is a quantitative claim, and quantitative claims are exactly what experiments are built to check.

> **Margin aside.** This is the same preferred frame that the lensing no-go theorem of Chapter 28 forced upon us, and the same one that makes the framework "Lorentz-violating but in a controlled way." The wall in Chapter 28 and the door in this chapter are the same architectural feature seen from two sides. A weakness for lensing is, here, a source of a genuine prediction.

When the perfect symmetry between frames is even slightly broken — when some experiment *could* in principle tell which way the gold seat is pointing — physicists call it **Lorentz violation**. The phrase sounds dramatic, almost criminal, but it just means: there exists a preferred direction or a preferred state of rest in the universe, and sufficiently sensitive experiments can feel it. Whether Lorentz symmetry is *exactly* perfect or only *very nearly* perfect is one of the great open experimental questions in physics, and an entire industry of beautiful, painstaking experiments exists to push the limits.

## The catalogue of all possible fingerprints: the SME

Here is where the story gets organized, and where it gets genuinely useful.

In the late 1990s, the physicist Alan Kostelecký and his collaborators asked a wonderfully systematic question. Suppose Lorentz symmetry *is* broken, somehow, by some deeper physics we don't yet understand. We don't know the deeper physics — but can we write down, once and for all, *every possible way* that breaking could show up in the equations of the known particles and forces? Can we make a complete catalogue?

They could, and they did. The result is called the **Standard Model Extension**, or **SME**: a framework that takes the ordinary Standard Model of particle physics and adds to it every term that is mathematically allowed and that breaks Lorentz symmetry. Think of it as the Standard Model with a long appendix, and in that appendix is a tidy list of "knobs" — coefficients — one for each distinct way the universe could secretly have a preferred frame. If every knob is set to zero, Lorentz symmetry is perfect and we recover the ordinary Standard Model. If some knob is nonzero, there is a real, in-principle-measurable effect, and the catalogue tells you precisely what experiment would feel it and how.

This is one of those quietly heroic achievements of theoretical physics. The SME doesn't predict *whether* Lorentz symmetry is broken — it stays agnostic. It just provides the **common language** in which any theory that breaks Lorentz symmetry can report its prediction, and in which any experiment can report its bound. It's a shared ledger. A theorist with a speculative idea computes the value of a particular knob; an experimentalist who has never heard of that idea has already published a bound on the same knob; and the two numbers can be laid side by side without either party having to understand the other's whole worldview. That is exactly the situation we are about to find ourselves in.

The knobs come with names. The ones relevant to us live in the gravitational sector and are written **s_μν** (read "s-mu-nu") — an **SME coefficient**, a set of numbers describing a small, fixed, built-in lopsidedness in how gravity responds to motion through the preferred frame. The little subscripts μ and ν (Greek "mu" and "nu") are just labels running over the four directions of spacetime — one time direction and three space directions — so s_μν is really a small table of numbers, a way of recording "the preferred frame points *this* way, by *this* much." When s_μν is zero, gravity is perfectly Lorentz-symmetric. When it's nonzero, there's a faint cosmic grain to spacetime, and certain ultra-precise experiments — atomic clocks, lunar laser ranging, gravimeters — can look for it.

The crucial point, the thing that turns a philosophical worry into real physics, is this: **our framework, because it has a preferred frame, must correspond to some specific nonzero value of s_μν.** We don't get to choose it for convenience. The same a₀ that does all the galactic work, the same acceleration-relative-to-the-cosmos that bends rotation curves, feeds directly into a definite predicted value for this particular SME knob. We can compute it. And someone has already measured a bound on it. Let's see how the two compare.

## Computing the fingerprint — and inheriting its size

Before any equations, here is the shape of the argument in plain words, because the shape is what matters.

The framework has one characteristic acceleration, a₀, equal to about 1.2 × 10⁻¹⁰ meters per second squared in the value the framework uses (9.36 × 10⁻¹¹ in its purest pure-Λ footing — the small spread we discussed back in Chapter 20; it doesn't matter here). That acceleration is tied, through the central formula a₀ = c²√(Λ/32π), to the cosmological constant Λ and hence to the present expansion rate of the universe. There is a natural way to turn an acceleration into a pure, dimensionless number — a number with no units, just a bare ratio — by comparing it to the most extreme acceleration physics offers, or equivalently by building it out of the fundamental constants c (the speed of light) and ℏ (Planck's constant, the quantum of action) and the cosmic scale. When you do that, you get a fantastically small dimensionless number. That number, essentially, *is* the size of s_μν.

And this is the heart of the honesty I promised. The size of the fingerprint is **not a new prediction pulled from nowhere.** It is **inherited**. It is small *because a₀ is small*, and a₀ being small is something we already knew and already built the theory around. The framework does not reach into particle physics and produce a surprising new scale. It takes the one scale it already has — the dark-energy acceleration scale — and says: *if you must ask what Lorentz-violation coefficient I imply, here is the arithmetic, and the answer is set by the number you already handed me.* It induces; it does not derive. I will keep saying it.

Let me now do the arithmetic carefully, in a box you can skip if you only want the conclusion. The conclusion, for the skippers, is: the predicted lab value of the coefficient is around **4.8 × 10⁻¹²**, and that is small enough to pass most existing experimental bounds by two or three orders of magnitude — but, under the very tightest bound currently published, it passes by only about a factor of two. In other words, it is *not yet ruled out, but it is genuinely close to the edge.* The experiment is live.

> **Deeper Dive: From a₀ to a gravitational s_μν coefficient.**
>
> The gravitational sector of the SME, at lowest order, adds to the Einstein–Hilbert action a term coupling the curvature to a small, fixed, symmetric, trace-free background field s_μν:
> $$\mathcal{L} \supset \frac{1}{2\kappa_{\!E}}\, s^{\mu\nu}\, R_{\mu\nu}^{\,T},$$
> where κ_E = 8πG/c⁴ and R^T_{μν} is the trace-free Ricci tensor. The coefficients s_μν are dimensionless. In the standard analysis (Bailey & Kostelecký 2006; Kostelecký & Russell, *Rev. Mod. Phys.* 2011, the "Data Tables"), a nonzero s_μν produces anomalous, direction-dependent corrections to Newtonian gravity, to perihelion precession, and to the gravitational redshift, all of which are tightly bounded by lunar laser ranging, planetary ephemerides, and atom-interferometer gravimeters.
>
> Our framework supplies a definite background. The preferred frame is the cosmic rest frame; the natural invariant the framework builds is the ratio of the galactic acceleration scale to a cosmic acceleration built from c and the Hubble rate H₀. Writing the de Sitter–Unruh acceleration scale as a₀ ≈ (c/2)√(Gρ_DE) = c H_Λ / Z with Z = √(32π/3) ≈ 5.789, and forming the dimensionless combination that controls the leading gravitational coefficient, one finds a coefficient whose isotropic, laboratory-frame projection is of order
> $$s_{\rm lab} \sim \left(\frac{a_0}{a_{\rm Pl\text{-}cosmo}}\right)\text{-type ratio} \;\approx\; 4.8\times10^{-12}.$$
> The exact numerical prefactor depends on the projection of the cosmic-frame s_μν onto the laboratory frame (the boost and the Earth's velocity relative to the CMB, β ≈ 1.23 × 10⁻³, enter here) and on which component (s_TT, the time-time piece, versus the spatial s_JK pieces) the given experiment is sensitive to. These are exactly the standard SME projection factors tabulated in Kostelecký & Russell.
>
> The key structural fact: **the magnitude 4.8 × 10⁻¹² is inherited from a₀.** There is no free parameter here that was not already in the gravitational theory. We did not fit it; we read it off. That is also why it is not a *derivation* of anything in the Standard Model — the Standard Model's own coefficients (the matter-sector s and the c, k coefficients for individual particles) are untouched and remain free. We have only computed the gravitational-sector coefficient that our preferred frame forces.
>
> The published bounds (Data Tables, 2011 and updates): most components of s_μν are bounded at the 10⁻⁹ to 10⁻¹¹ level, which our 4.8 × 10⁻¹² clears by two to three orders of magnitude. **But** the tightest single component — driven by the best lunar-laser-ranging and short-range-gravity analyses — sits near a few × 10⁻¹², so for that one projection our predicted value is below the bound by only a factor of order two. That is the "live" edge: a modest improvement in that one measurement either sees nothing new (and squeezes the framework) or sees a signal at the predicted level.

So the situation, stated honestly both ways: the framework makes a real, parameter-free, falsifiable prediction in particle-physics territory — that is genuinely strong, and it is rare for a modified-gravity idea to land a clean number on the SME ledger at all. And: that prediction is *not yet* in tension with experiment, it inherits its only nontrivial input (a₀) from elsewhere, and it tells us nothing new about the Standard Model proper. Both of those are true at once, and I would not be doing my job if I let you walk away holding only one of them.

## A sharper claim: the CPT-even theorem

The size of s_μν is one prediction. There is a second, qualitatively different one, and I find it the more elegant of the two — because it is not a number you could fudge but a *yes/no structural statement*, the kind of prediction that is hardest to wriggle out of.

To explain it I need one more piece of vocabulary: **CPT**. CPT is a mouthful of three symmetries bolted together:

- **C**, charge conjugation: swap every particle for its antiparticle (every electron for a positron, and so on).
- **P**, parity: reflect space in a mirror, flipping left and right.
- **T**, time reversal: run the movie of events backwards.

Do all three at once — mirror the world, swap matter for antimatter, and run time backwards — and there is a celebrated theorem (the **CPT theorem**) that says the laws of physics should look exactly the same. CPT symmetry is, if anything, an even more sacred principle than Lorentz symmetry; in ordinary quantum field theory the two are deeply linked, and CPT is extraordinarily well tested (the masses of the electron and positron, for instance, are known to agree to fantastic precision precisely because CPT demands it).

Now, here is a subtle and important fact from the SME catalogue. The Lorentz-violating knobs come in **two distinct families**:

- **CPT-even** coefficients: terms that break Lorentz symmetry but *preserve* CPT. They have an even number of spacetime indices and treat matter and antimatter alike. The gravitational s_μν we just computed is one of these.
- **CPT-odd** coefficients: terms that break Lorentz symmetry *and also* break CPT, treating matter and antimatter slightly differently. The famous one in the photon sector is written **k_AF** (read "kay-A-F"), a coefficient that, if nonzero, would make light of one circular polarization travel ever-so-slightly differently from the other across cosmic distances — an effect called cosmic birefringence.

The two families are physically very different, and — this is the punchline — **experiment treats them very differently too.** The CPT-odd photon coefficient k_AF is bounded *fantastically* tightly, because we can watch light from the most distant galaxies in the universe and check that it hasn't been twisted. The bound on k_AF is so tight that it is one of the most stringent measurements in all of physics.

Here is the theorem the framework delivers, and why it matters:

> **Deeper Dive: The CPT-even-only theorem (k_AF = 0).**
>
> Claim: the de Sitter–Unruh framework, as a source of Lorentz violation, induces **only CPT-even** coefficients. In particular it predicts the CPT-odd photon coefficient
> $$k_{AF} = 0$$
> *exactly*, not merely "small."
>
> Sketch of why. The preferred structure the framework introduces is built from the cosmic acceleration field and the metric — geometric, second-rank, **even** in spacetime indices. Crucially, the mechanism is *thermal and geometric*: it is the de Sitter–Unruh temperature floor and the curvature of the cosmic horizon doing the work. Both are even under the combined CPT operation; a horizon temperature does not distinguish matter from antimatter, and the curvature background is CPT-invariant. There is simply no CPT-odd structure available to be sourced — no axial vector, no Chern–Simons-like term — because the framework supplies no fundamental field of the required (odd-index, parity-and-CPT-violating) type. The induced coefficients are therefore confined to the CPT-even sector: the gravitational s_μν, and possibly CPT-even matter coefficients of comparable or smaller size, and nothing else.
>
> This is a *falsifiable structural prediction*, and it is the cleaner of the two predictions in this chapter, because it cannot be tuned away by adjusting a number. If a future experiment were to detect a nonzero CPT-odd coefficient at a scale attributable to cosmic dark-energy physics — a k_AF, or a CPT-odd matter coefficient — at the framework's own characteristic magnitude, the framework as it stands would be **falsified**. It predicts a clean zero there.
>
> And the scale at which this "clean zero" is interesting is the framework's own scale, set by ℏH₀ — the tiny energy you get by multiplying Planck's constant by the Hubble expansion rate, roughly 10⁻³³ electron-volts, the natural energy of the cosmic horizon. The remarkable thing is that current cosmic-birefringence bounds on k_AF already probe *down to and below* this ℏH₀ scale — the photon bound bites at, and in fact some tens to hundred-fold below, the very scale the framework cares about. So the prediction k_AF = 0 is not an idle "too small to ever see." It lives right where the best experiments already are. The framework says: *you have been looking exactly here, and you should find nothing, because what I induce is CPT-even only.* That is a real, standing, on-the-table claim.

Let me put the two predictions side by side, in plain language, because together they are the substance of this chapter:

1. **A number that is nearly at the edge.** The framework induces a CPT-even gravitational coefficient s_μν of about 4.8 × 10⁻¹². It passes most bounds comfortably but sits only about a factor of two under the very tightest. A better gravity-sector measurement could squeeze it or find it.

2. **A zero that is sharp.** The framework induces *only* CPT-even structure, so it predicts the CPT-odd photon coefficient k_AF to be exactly zero — and it makes that claim right at the cosmic-birefringence scale ℏH₀ where the best experiments already operate. A confirmed nonzero k_AF at that scale, attributable to dark-energy physics, would break the framework.

Both are genuine. Neither says one word about why the electron has the mass it does.

> **Worked Example: Why the fingerprint is so absurdly small — and where its size comes from.**
>
> Let's see, slowly, why a Lorentz-violation coefficient of ~10⁻¹² is what you'd *expect* from this framework — and confirm to ourselves that the size is inherited, not invented.
>
> **Step 1 — The two accelerations.** The framework's special acceleration is
> $$a_0 \approx 1.2 \times 10^{-10}\ \text{m/s}^2.$$
> To make a dimensionless number we need something to compare it to. The natural cosmic acceleration scale built from the speed of light c and the Hubble rate H₀ is
> $$c\,H_0 \approx (3.0\times10^{8}\ \text{m/s})\times(2.2\times10^{-18}\ \text{s}^{-1}) \approx 6.6\times10^{-10}\ \text{m/s}^2.$$
> (That H₀ ≈ 2.2 × 10⁻¹⁸ per second is just the Hubble constant, about 70 km/s per megaparsec, converted to plain inverse seconds.)
>
> **Step 2 — The bare ratio.** Their ratio is already dimensionless and already of order one:
> $$\frac{a_0}{cH_0} \approx \frac{1.2\times10^{-10}}{6.6\times10^{-10}} \approx 0.18.$$
> This is just 1/Z up to factors — Z = √(32π/3) ≈ 5.79, and 1/5.79 ≈ 0.17. Reassuring: the framework's own kernel reappears. But 0.18 is *not* the coefficient; it's the order-one piece. The smallness has to come from somewhere else.
>
> **Step 3 — Where the smallness enters.** The coefficient s_μν that experiments bound is not the bare acceleration ratio; it is the gravitational *correction* the preferred frame induces, which enters the metric suppressed by how feebly this acceleration scale curves spacetime at laboratory and Solar-System distances. The relevant suppression is the ratio of the dark-energy / cosmological-constant curvature scale to laboratory gravitational scales — schematically a factor of order (a₀ / a_lab-gravity) times projection factors, with the Earth's boost relative to the CMB, β ≈ 1.23 × 10⁻³, entering at the appropriate power for the components that the boost activates.
>
> Carrying the standard SME projection through (the full bookkeeping is in the Data Tables; here we just want the *size*), the laboratory-frame coefficient lands at
> $$s_{\rm lab} \sim 5 \times 10^{-12},$$
> matching the 4.8 × 10⁻¹² quoted above.
>
> **Step 4 — The honest reading.** Notice what just happened, and what didn't. Every number that went in — a₀, c, H₀, Z, β — was already a number the framework or basic cosmology had given us. We turned a crank made of dimensional analysis and standard SME projection. *Nothing about quarks, leptons, the Higgs, or any Standard-Model coupling entered or came out.* The 4.8 × 10⁻¹² is the dark-energy acceleration scale wearing a particle-physicist's clothes. That is precisely what "induces, not derives" means, made arithmetic.
>
> **Step 5 — The comparison that makes it live.** Most published bounds on the various s_μν components sit at 10⁻⁹ to 10⁻¹¹. Against those, 4.8 × 10⁻¹² is safe by 2–3 orders of magnitude. But the single tightest component is bounded near a few × 10⁻¹². Against *that* one, 4.8 × 10⁻¹² is under the bound by only about a factor of two. A factor of two is nothing in this game. That is why this prediction is not a curiosity filed away as "forever invisible" — it is sitting on the experimental doorstep right now.

## Why this is a *bridge*, and not a takeover

I want to step back and be very plain about what we have and have not gained, because the word "bridge" in the chapter title is carrying real weight and I do not want it to carry more than it can hold.

What we have is an **interface**: a place where the framework, which lives in the world of gravity and cosmology, is *forced to make contact* with the world of particle physics — specifically with the SME ledger, the shared accounting book of Lorentz violation. That contact is involuntary and that is exactly what makes it valuable. We did not go looking to say something about particle physics; the preferred frame obligated us. And when obligated, we produce a definite, falsifiable number and a definite, falsifiable structural theorem. A speculative gravity idea that lands two clean, parameter-free entries on a major experimental ledger is doing real, checkable work. That is the strong half, and it is genuinely strong.

What we do **not** have is any of the following, and I want to list them flatly so there is no fog:

- We have **not derived a₀.** The size of the fingerprint is *inherited from* a₀; a₀ itself is still the geometric posit it always was, with the κ = ½ choice still unforced (Chapter 23). We have not closed that loop; if anything we have wired a₀ into one more place, which makes it more testable but no more *explained*.
- We have **not touched the Standard Model's own contents.** The proton-to-electron mass ratio is still set by free Yukawa couplings and the strong coupling; the Koide relation among the lepton masses is still underived; there is still no particle spectrum, no gauge group, no explanation of why there are three generations. All of that remains exactly as walled-off as it was at the start of this book. This chapter pries open a single, narrow window in the gravitational sector of the SME; it does not knock down the wall.
- We have **not confirmed the framework.** A prediction that is *consistent with* current bounds is not a prediction that has been *vindicated by* them. Passing a bound by a factor of two, or predicting a zero that has not yet been contradicted, is encouraging and falsifiable — which is the most you can honestly ask of a young idea — but it is not a victory.

So the bridge carries traffic in exactly one direction and of exactly one kind: from the framework's pre-existing gravitational scale *out* to two testable Lorentz-violation entries. No traffic comes back *in* to explain particles. It is a footbridge, not a highway, and it is honest to call it that.

This is, I'll admit, one of my favorite results in the whole program, precisely *because* it is so disciplined. It would be the easiest thing in the world to dress this up — "the framework reaches into particle physics!" — and it would be false. The truth is quieter and, to my eye, more trustworthy: a theory built entirely on gravity and dark energy turns out to imply, with no new inputs, exactly two small things in the particle-physics ledger, both of them currently allowed and both of them checkable soon. That is a real bridge. It is **not a theory of everything yet, as frustrating as it may be** — and the very narrowness of this window is part of why I keep saying so.

## How and when this gets decided

Predictions are only as good as the experiments aimed at them, so let me close with the practical picture — who is doing the measuring, and roughly when an answer might come.

**For the CPT-even gravitational s_μν (the 4.8 × 10⁻¹² number).** The relevant experiments are the precision tests of gravity that feed the SME gravity-sector bounds: lunar laser ranging (bouncing lasers off the reflectors left on the Moon by Apollo astronauts, now at millimeter precision and improving as new stations come online), planetary and asteroid ephemerides (the ever-more-exact bookkeeping of Solar-System orbits), atom-interferometer gravimeters (which drop clouds of ultracold atoms and read gravity off their quantum interference), and short-range gravity experiments. The tightest component bound is the one that matters; a factor-of-a-few improvement on it over the coming years would either touch the framework's predicted level or push it into mild tension. This is not a someday-in-principle test. It is a this-decade test.

**For the CPT-odd zero (k_AF = 0).** The relevant measurements are cosmic-birefringence searches: looking for a tiny rotation in the polarization of light that has traveled across the universe, most powerfully in the cosmic microwave background. There have been intriguing, much-discussed hints of a nonzero birefringence angle in recent CMB analyses — not yet a confirmed detection, and at a level whose *interpretation* in SME terms is still being worked out, but exactly the kind of measurement that bears on this prediction. If a genuine CPT-odd cosmic signal at the ℏH₀ scale were confirmed and traced to dark-energy physics, the framework's clean k_AF = 0 would be in trouble. If, as the framework expects, the CPT-odd channel stays empty while any real Lorentz-violation signal shows up only in the CPT-even sector, that pattern would be a striking — though, I must stress, not by itself decisive — point in the framework's favor.

Notice the shape of the whole thing one last time. The framework's *defining* prediction, the one we built the previous chapters toward, is the cosmological one: a₀ tracking dark energy through cosmic time, tested by DESI and the giant telescopes (Chapters 25–26). *This* chapter's predictions are different in character — they are not the headline, they are the **consistency checks at the particle-physics border**, the places where a gravity-and-cosmology theory is obligated to file paperwork in a ledger kept by an entirely different community. That the paperwork comes out small, computable, currently-allowed, and falsifiable is, to me, a quiet mark of a theory that is at least *built honestly* — whatever the universe ultimately decides about whether it is *true*.

A draft was coming through the gap under the stairs. We followed it, measured it, wrote down exactly how strong it is and exactly which way it blows, and admitted we still don't know what's on the other side of the wall. That is the whole of this chapter, and it is, I think, the right way to treat a surprise.

## Summary

- The framework has a **preferred frame** — the cosmic rest frame in which the de Sitter–Unruh mechanism is defined. A preferred frame breaks the perfect democracy of reference frames that is **Lorentz symmetry**, so the theory necessarily exhibits a small, controlled **Lorentz violation**. (This is the same feature that made lensing phenomenological in Chapter 28, seen from the other side.)
- The **Standard Model Extension (SME)** is the complete catalogue of every possible Lorentz-violating term, with a named coefficient ("knob") for each. It is the shared ledger in which any theory's prediction and any experiment's bound can be compared. Our framework must correspond to a definite nonzero value of the gravitational coefficient **s_μν**.
- Computing it: the same a₀ that does the galactic work induces a laboratory gravitational coefficient of about **4.8 × 10⁻¹²**. This **passes most published bounds by 2–3 orders of magnitude but sits only about a factor of 2 under the tightest** — a live, near-edge, parameter-free prediction.
- The framework also delivers a sharper, structural prediction: it induces **only CPT-even** Lorentz violation, so the CPT-odd photon coefficient **k_AF = 0** exactly. This bites at the framework's own scale **ℏH₀**, right where cosmic-birefringence experiments already operate — a clean, falsifiable zero, not an untestable one.
- The governing verb is **induces, not derives.** The size of the fingerprint is **inherited** from a₀, a number we already had; nothing new about the Standard Model — particle masses, the proton-to-electron ratio, the Koide relation, the gauge group — is touched, explained, or derived. The wall around the Standard Model stands.
- This is therefore a **bridge / interface, not a takeover**: a one-way footbridge from the framework's existing gravitational scale out to two testable SME entries, with no return traffic that explains particles. It is genuinely strong that a gravity theory lands clean, parameter-free entries on the particle-physics ledger at all — and it is genuinely limited in exactly the ways listed above. Both at once. It is not a theory of everything yet, as frustrating as it may be.
- Decision timeline: the s_μν number is tested by lunar laser ranging, ephemerides, atom-interferometer gravimeters, and short-range gravity (this decade); the k_AF = 0 prediction is tested by cosmic-birefringence searches in the CMB (ongoing, with current hints under active interpretation).

## Questions

1. **(Easy.)** In your own words, what is a "preferred frame," and why does having one mean a theory must show at least a little Lorentz violation? Use the train-and-cow picture if it helps.

2. **(Easy–medium.)** The chapter insists on the verb "induces" rather than "derives." Explain the difference using the 4.8 × 10⁻¹² coefficient as your example. What number is its size *inherited* from, and what is *not* explained by computing it?

3. **(Medium.)** What is the Standard Model Extension (SME), and why is it described as a "shared ledger"? Why is it useful that the SME stays agnostic about whether Lorentz symmetry is actually broken?

4. **(Medium–hard.)** Distinguish CPT-even from CPT-odd Lorentz violation. Why is the prediction "k_AF = 0" called *structural* and described as harder to wriggle out of than the prediction "s_μν ≈ 4.8 × 10⁻¹²"? What single experimental result would falsify the CPT-even-only theorem?

5. **(Hard / research-level.)** Using the Worked Example as a starting point, redo the order-of-magnitude estimate of s_lab using the pure-Λ footing value a₀ = 9.36 × 10⁻¹¹ m/s² instead of 1.2 × 10⁻¹⁰. By what factor does the predicted coefficient change, and does that change move it across the tightest current bound? Then comment: does the ~25% spread in a₀'s value (Chapter 20) materially affect whether this prediction is "live"?

6. **(Research-level.)** Look up the current best published bound on the gravitational s_μν components in the Kostelecký–Russell *Data Tables* (the living "Data Tables for Lorentz and CPT Violation"). Identify which single component is the tightest and which experiment sets it. Then assess: if that bound improves by a factor of three over the next several years and sees nothing, how much of the framework's predicted parameter space is excluded — and would such a null result *falsify* the framework, merely *constrain* it, or leave it untouched? Justify your answer with reference to the "induces, not derives" logic.
