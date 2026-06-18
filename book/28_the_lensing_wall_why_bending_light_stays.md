# Chapter 28: The Lensing Wall: Why Bending Light Stays Phenomenological

> *Light is the one messenger that travels across the whole universe without a clock or a scale of its own. It just goes where spacetime tells it to. And it is exactly here, in the bending of starlight, that our framework hits its hardest wall.*

---

## A confession at the start

I want to begin this chapter the way an honest mechanic begins when you bring in a car that mostly runs beautifully. "The engine's strong, the transmission's smooth — but I have to be straight with you about the brakes." This is the brakes chapter.

Everything we have built so far has a certain pleasing tightness to it. The acceleration scale $a_0$ comes out tied to dark energy. The form of the law is forced by several independent arguments. The single free number $\kappa=\tfrac12$ turns out to be pure geometry. When you put it all together, you get a one-parameter theory of gravity and the dark sector that does a genuinely good job on the rotation of galaxies.

And then you ask it a simple question — *how much does this galaxy bend the light passing behind it?* — and the tightness vanishes. The framework, in its current form, cannot answer that question from first principles. It has to be *told* the answer, fit from the data, and then it reproduces it. That is not a prediction. That is a curve we drew through points someone else measured.

This is the deepest crack in the whole edifice, and I am not going to paper over it. By the end of the chapter I want you to understand three things: what gravitational lensing is and why it matters so much; *why* a theory like this one runs into a brick wall when it tries to bend light honestly — a wall that turns out to be a genuine mathematical theorem, not just a failure of effort; and exactly which pieces the framework wins, which pieces it concedes, and which are still being argued over. As frustrating as it may be, this is not a theory of everything yet, and the lensing wall is the single clearest reason why.

Let me build it up slowly.

---

## What lensing is, and why it is such a good scale

Start with the thing itself. **Gravitational lensing** is the bending of light by gravity. A massive object — a galaxy, a cluster of galaxies — sits between you and some more distant source of light, and as that light passes near the mass, its path is deflected. The intervening mass acts like a lens: it can magnify the distant source, smear it into arcs, even produce multiple images of the same object. Einstein predicted it; the 1919 eclipse expedition that made him world-famous measured starlight bending around the edge of the Sun. Today it is one of the most powerful tools in astronomy.

Here is *why* it matters so much for our story. Almost everything else we have talked about — rotation curves, the velocities of galaxies in a cluster — measures how *matter* moves. Matter moving is matter responding to gravity, and gravity, in this framework, is a force on massive bodies that has been modified at low accelerations. So you might worry that when galaxies seem too heavy, we are really just seeing matter pushed around by a modified law, with no actual extra mass there at all.

Light is the independent check. Light has no rest mass. It does not "feel" a Newtonian gravitational force in the ordinary sense. In Einstein's picture, light simply follows the straightest available path through curved spacetime. So when light bends *more* than the visible matter can account for, that is a second, independent witness telling you something is off — and crucially, it is a witness that responds to a *different aspect of gravity* than orbiting stars do. Matter in orbit cares about one part of the spacetime geometry. Light cares about the sum of two parts. Getting both to agree, with one consistent law, is the real test.

Let me make that "two parts" precise, because the whole chapter turns on it.

> **Deeper Dive: The two potentials, and gravitational slip**
>
> In the weak-field, slowly-varying regime appropriate to galaxies and clusters, the spacetime around a mass is described to good approximation by a metric of the form
> $$ ds^2 = -\left(1 + \frac{2\Phi}{c^2}\right)c^2\,dt^2 + \left(1 - \frac{2\Psi}{c^2}\right)\delta_{ij}\,dx^i dx^j .$$
> There are **two** potentials here, not one. $\Phi$ is the *time–time* potential: it governs the rate at which clocks run and, through that, the acceleration of slow-moving matter. A star orbiting a galaxy responds to $\Phi$ alone — to leading order its equation of motion is $\ddot{\mathbf{x}} = -\nabla\Phi$.
>
> $\Psi$ is the *space–space* potential: it describes how much space itself is curved. Light, being relativistic, is deflected by the *sum* of the two. The bending angle of a ray works out proportional to $\nabla(\Phi+\Psi)$. So:
> - **Dynamics** (orbits, dispersions) probes $\Phi$.
> - **Lensing** probes $\Phi+\Psi$.
>
> In ordinary General Relativity with no exotic stress, the two potentials are *equal*: $\Phi=\Psi$. The difference between them,
> $$ \eta_{\text{slip}} \equiv \frac{\Psi}{\Phi} \quad\text{or}\quad \Phi - \Psi , $$
> is called the **gravitational slip**. A nonzero slip means space is curved by a different amount than clocks are slowed — and that is exactly the kind of thing that a modified-gravity theory, or an unusual matter field, can produce. The slip is the hinge on which relativistic MOND-like theories live or die: it is the one extra knob that lets lensing differ from dynamics. We will see that this framework's natural relativistic home has *no* slip at all, $\Phi=\Psi$, and that this is both a blessing and the source of the wall.

So now you can see the shape of the problem. In standard physics with dark matter, the extra invisible mass curves *both* potentials by the same amount, and everything is consistent: light and orbits agree because there is real extra stuff there. In a MOND-like theory, there is *no* extra stuff. The same visible matter has to somehow curve spacetime *enough to match what dark matter would have done* — both for orbits and for light — using only a modification of the law. And here is the trap: the modification that fixes the orbits does not automatically fix the light by the right amount. You have to engineer the slip on purpose. And when you try to engineer it honestly, a theorem stops you.

Let me explain that theorem, because it is the heart of the chapter.

---

## The wall: a no-go theorem

A **no-go theorem** is a proof that something you might want is impossible under a stated set of assumptions. It is one of the most useful — and most humbling — kinds of result in physics. It does not say "we couldn't find it." It says "stop looking, here is why it cannot exist, given what you've asked for." A famous example is the proof that you cannot comb a hairy ball flat without leaving a cowlick; another is the proof that no theory can simultaneously be a local, deterministic hidden-variable theory and reproduce all of quantum mechanics. No-go theorems are the guardrails of theoretical physics. They tell you which roads are closed so you stop driving into them.

The no-go theorem we care about closes the road to honest MOND lensing. Informally, it says this:

> *You cannot build a relativistic MOND-like theory that (a) is generally covariant, (b) propagates gravitational waves at the speed of light, (c) is free of ghosts, and (d) bends light by the extra amount needed to mimic dark matter while still switching off safely in the Solar System — all at once.*

Each of those four requirements is something we are not willing to give up cheaply. Let me say what each one means in plain language, because the plainness is the point.

**(a) General covariance** — also called **diffeomorphism invariance** — is the principle that the laws of physics do not depend on the coordinate grid you draw on spacetime. There is no special graph paper that the universe comes printed on. This is the founding principle of General Relativity, and abandoning it means abandoning the relativity in relativity.

**(b) Gravitational waves travel at the speed of light**, $c_T = c$. We *measured* this. In 2017, the neutron-star merger GW170817 sent both gravitational waves and a gamma-ray flash across 130 million light-years, and they arrived within about two seconds of each other. That tiny gap, over that enormous distance, pins the speed of gravitational waves to the speed of light to roughly one part in $10^{15}$. A whole generation of MOND-like and dark-energy theories died on the morning that result came out, because they had quietly relied on gravity propagating at a different speed. Ours must respect it.

**(c) Ghost-freedom** is the requirement that the theory not contain a "ghost" — a field whose energy runs off to minus infinity, so that the vacuum can lower its energy forever by spitting out more and more excitations. A theory with a ghost is not just ugly; it is *sick*. It has no stable ground state. It predicts that empty space should instantly boil. We cannot accept a ghost.

**(d) Cassini safety** is the requirement that whatever extra effect bends light around galaxies must *not* be present in the Solar System, where General Relativity has been tested exquisitely. The Cassini spacecraft, tracking radio signals as they grazed the Sun, confirmed standard light-bending to about one part in $10^5$. The framework's whole selling point is that its modification is an *inertial* effect that switches off at high accelerations — that is exactly what keeps it Cassini-safe for *dynamics*. The trouble is making the *lensing* sector switch off the same way without breaking one of (a), (b), or (c).

The theorem says: pick any three, and you can have them. Try to have all four, and you fail. Something has to give. Let me show you, at the level a curious reader can follow, *where* the conflict bites.

> **Deeper Dive: Why diffeomorphism invariance + $c_T=c$ + ghost-freedom forbid a covariant Cassini-safe slip**
>
> Here is the logic in compressed form; the references at the end of the chapter carry the full derivations, and the framework's own working notes reconstruct it three independent ways.
>
> To make lensing differ from dynamics, you need a nonzero gravitational slip $\Phi-\Psi$ that grows in the low-acceleration regime. In a covariant theory the slip is not free — it is *sourced* by something. There are essentially three places it can come from:
>
> 1. **A nonminimal coupling between an extra field and the spacetime curvature** (a disformal or "DHOST"-type coupling). These are the most general scalar–tensor couplings that avoid the Ostrogradsky ghost. But the same coupling that generates a slip generically shifts the speed of tensor (gravitational-wave) modes away from $c$. Demanding $c_T=c$ to the GW170817 precision forces the slip-generating part of the coupling to (near-)zero. The pure, ghost-free, luminal-GW corner of DHOST space has been shown to leave *no surviving covariant slip* of the MOND-needed form. (The framework's own `route1_dhost_pure_slip` analysis lands exactly here.)
>
> 2. **A shear or anisotropic-stress term from a vector or tensor field** — the strategy of the relativistic MOND theories. An anisotropic stress *can* source a slip. But to be ghost-free and luminal, the field has to be constrained (a unit-timelike vector, say), and the constraints that remove the ghost also remove the wanted slip in the regime where you need it, or they reintroduce a preferred frame (see below).
>
> 3. **A non-dynamical multiplier or "khronometric" structure.** Here you *do* get a slip — but only by introducing a preferred time-slicing, i.e. a preferred frame, which violates local Lorentz invariance.
>
> Trace the three branches and they converge on one conclusion: the only way to keep a Cassini-safe MOND-magnitude slip while respecting $c_T=c$ and ghost-freedom is to give up the *covariant, Lorentz-invariant* character of the lensing sector. The slip must live in a **preferred-frame** sector. There is no fully diffeomorphism-invariant, ghost-free, luminal theory that delivers it. This is the wall, stated as a theorem rather than a complaint.

I want to dwell on the *flavour* of that result for a moment, because it is easy to read it as a technicality and it is not one.

What the theorem is really saying is that the very features that make this framework attractive elsewhere are the ones that strangle its lensing. We *want* gravitational waves to go at $c$ — and they do, and we are proud of it. We *want* no ghosts — and there are none, and that is part of the one-parameter cleanliness. We *want* the modification to be an inertial effect tied to a real, physical, preferred cosmic rest frame (the frame in which the cosmic microwave background looks isotropic) — because that is the natural home of an Unruh-temperature mechanism, and it is what makes the dynamics Cassini-safe. But put those three honest commitments together and they leave you no room to build a *covariant* lensing law. The lensing is pushed, by force of theorem, into the preferred-frame sector — which is a polite way of saying it stops being a clean prediction of the geometry and becomes a fitted ingredient.

---

## What "preferred-frame lensing" actually means

Let me unpack that last term, because it is the crux and the concession.

A **preferred-frame** theory is one that, despite being dressed up in covariant clothing, secretly singles out one special state of motion as physically privileged. Special relativity's founding insight is that no inertial frame is privileged — the laws look the same whether you are drifting or speeding. A preferred-frame theory breaks that. It says: there *is* a frame that matters, the cosmic rest frame, and physics in that frame is special. When a theory does this, we say it exhibits **Lorentz violation** — it violates the Lorentz symmetry that special relativity is built on.

Now, a little Lorentz violation in the gravitational sector is not automatically fatal. The cosmos *does* have a natural rest frame — the one set by the CMB and the overall expansion — and there is a long, respectable tradition of theories (Einstein-aether, Hořava gravity, khronometric gravity) that lean on it. The framework in this book already lives partly here: its modified-inertia mechanism is tied to that cosmic rest frame, and being preferred-frame is, as we saw in the chapter on the particle-physics interface, what lets it connect to the Standard Model Extension and induce a bounded Lorentz-violation coefficient. So preferred-frame structure is not a foreign object smuggled in for lensing; it is already in the house.

But here is the difference, and it is everything: in the *dynamics* sector, the framework *derives* the form of its modification — the $a_0$, the kernel, the switch-off — from physics it can articulate. In the *lensing* sector, after the no-go theorem has done its work, what is left is a preferred-frame structure whose slip function we do not derive. We *choose* it, by fitting it to lensing data, so that the bending comes out right. That choice is not forced by the mechanism. It is a free function — a curve with adjustable shape — installed by hand to match observation.

That is what I mean when I say the lensing sector is **irreducibly phenomenological**. "Phenomenological," in physics, is a slightly bittersweet word. It means a description that captures the phenomena — it fits the data, it organizes the facts, it can even predict new data in the same regime — but is *not derived from underlying principle*. It describes *what* happens without explaining *why* that and not something else. A phenomenological law is a placeholder where a derivation ought to be. The framework's rotation-curve law is *not* phenomenological in this sense — it is grown from a mechanism. Its lensing law, right now, is. And "irreducibly" means we have a theorem telling us we cannot remove that placeholder without giving up something we refuse to give up. It is not a gap we expect to close with a clever afternoon. It is a wall.

> **A margin aside.** People sometimes hear "phenomenological" as an insult. It is not. Half of physics was phenomenological first and fundamental later — the periodic table, Balmer's formula for hydrogen lines, even Newton's law of gravity before Einstein explained it. A phenomenological law that fits is real knowledge. The honest point is only that it is *not yet* the deep thing, and you should never sell it as the deep thing.

---

## We did not just take this on faith — we tried to break the wall

I owe you the work, not just the verdict. When you are told "this is impossible," the responsible thing is to spend real effort trying to make it possible, and to fail honestly, in detail, before you concede. We did that. Over an extended push, the framework's research notes attacked the lensing wall from every covariant direction anyone has proposed:

- **DHOST and degenerate scalar–tensor theories** — the most general ghost-free scalar–tensor couplings. Result: in the pure $c_T=c$ corner, no surviving MOND-form slip.
- **Einstein-aether-type vector theories with a shear-absorbing coupling**, tuned to try to manufacture a slip from anisotropic stress. Result: the slip you can make either reintroduces a ghost or a superluminal mode, or it vanishes where you need it; adversarial cross-checks closed every escape.
- **Hořava / non-projectable infrared gravity**, leaning on a preferred slicing. Result: you *can* get a slip — but only by paying the preferred-frame price, exactly as the theorem says.
- **Khronometric aether with a non-dynamical multiplier.** Same verdict: slip available only in the Lorentz-violating sector.
- A handful of more exotic attempts — Finsler-geometry lensing, nonlocal slip constructions, backreaction arguments. Each either failed a consistency check or reduced to one of the above.

I am listing these not to bury you in names but to make a point about *how the concession was reached*. It was not reached by assumption. Several of these attempts looked, for a while, like they might work — one construction even produced an apparent "$\Delta\Phi=0$, it passes!" moment before a careful re-check found that a mislabeled equation had hidden a sign. When the synthesis caught that error, the escape closed. That is what honest theory work feels like from the inside: a promising door, a closer look, a quiet "no." Every covariant door we opened led back to the same hallway. The wall held in its strongest form.

So the concession in this chapter is *earned*. It is not "we gave up." It is "we proved the room has no covariant exit, and we are telling you so plainly."

---

## The relativistic-MOND home: AeST, and the company we keep

If the lensing wall were unique to this framework, it would be a private embarrassment. It is not. It is a *shared* wall — and understanding that is important both for fairness and for honesty.

The most successful relativistic completion of MOND to date is a theory called **AeST**, for *Aether–Scalar–Tensor* — built by Constantinos Skordis and Tom Złośnik and published around 2021. It was a real achievement: AeST is the first MOND-like theory that simultaneously fits galaxy rotation curves, passes the GW170817 speed-of-gravity test (its gravitational waves go at $c$), and — most impressively — reproduces the cosmic microwave background power spectrum, including the famous third acoustic peak that earlier MOND attempts could not match. For a long time the CMB was thought to be a clean kill of all of MOND; AeST showed that, with enough structure, a MOND-family theory can survive it. So AeST is the strongest relativistic MOND there is, and the natural relativistic "host" the framework in this book points to.

And AeST hits the same lensing wall. Here is the specific, honest way it does so.

> **Deeper Dive: AeST has no slip, so lensing mass equals dynamical mass**
>
> In the quasi-static, weak-field limit, AeST is constructed so that its two metric potentials are *equal*: $\Phi=\Psi$. There is **no gravitational slip**. This was a deliberate design choice — it is what keeps the theory ghost-free and its gravitational waves luminal, dodging the post-GW170817 graveyard.
>
> The consequence is exact and unforgiving. With $\Phi=\Psi$, the lensing potential $\Phi+\Psi = 2\Phi$ is just twice the *dynamical* potential. So in AeST, **the mass you infer from lensing equals the mass you infer from dynamics**, regime by regime. On galaxy scales, where the MOND boost to $\Phi$ already does the work of dark matter for the orbits, this is good news: the same boost automatically bends light by the right amount, and AeST reproduces the **galaxy–galaxy lensing radial-acceleration relation** — the observed tight relation between the lensing-inferred acceleration around isolated galaxies and the acceleration expected from their visible matter. That is a genuine pass, and the framework inherits it.
>
> On *cluster* scales, the same equality becomes a liability. Clusters of galaxies show a lensing mass that exceeds the visible (and MOND-boosted) mass by a residual factor of roughly $\eta \approx 2$–$2.3$ in the central regions. With $\Phi=\Psi$ and no slip to play with, AeST — and the framework — has no extra handle to absorb that residual. The cluster lensing mass is simply *too big* for what the theory can produce from baryons. This is conceded, not finessed.

Read that box twice, because it contains both the win and the loss in one breath, which is exactly how I want you to hold it.

The win: because lensing mass equals dynamical mass, and the dynamics are right for galaxies, the *galaxy-scale* lensing comes out right essentially for free. The radial-acceleration relation in galaxy–galaxy lensing is reproduced. The framework does not have to fudge anything to bend starlight correctly around an ordinary galaxy.

The loss: that same rigid equality means there is no spare slip to soak up the *cluster* residual. Clusters lens too strongly for the visible matter, by a factor of roughly two in the center, and neither AeST nor this framework can manufacture that missing factor from baryons alone. We will give the cluster residual its own chapter (Chapter 29), because it is a second, partly-independent wound and it deserves its own honest accounting. Here I only want you to see that it is *connected* to the lensing story through the no-slip property.

---

## The honest ledger: passes, concessions, and one contested item

Let me lay it out as plainly as I can, in three columns.

**What passes.** Galaxy-scale lensing. Because the relativistic host has $\Phi=\Psi$ and the dynamics are correct at galaxy accelerations, the galaxy–galaxy weak-lensing radial-acceleration relation is reproduced. Light bends correctly around isolated galaxies. This is real and it is not nothing — many a modified-gravity idea dies right here, and this one does not.

**What is conceded — genuinely independent losses.**

- *The cluster lensing residual, $\eta\approx 2$–$2.3$ in the center.* Clusters lens as if there is more mass than baryons-plus-MOND-boost can supply. With no slip, there is no covariant fix inside the theory. This is a real, conceded deficit. It is shared with all of MOND, and Chapter 29 treats it on its own terms (including the genuinely interesting point that a density-dependent reading of $a_0$ flattens the residual toward the right order of magnitude with zero new parameters — but flattening is not curing, and I will not oversell it).
- *The CMB third acoustic peak as an independent test.* AeST's success on the CMB is a success of *AeST's specific field content* — a particular aether-scalar structure tuned to get the peak heights right. It is *not* something this framework derives from its $a_0$–dark-energy mechanism. So while the framework can point to AeST and say "a MOND-family theory can pass the CMB," it cannot claim the CMB peak as its own prediction. It is borrowed, and borrowed is not derived. I count it as an independent item the framework does not own.

**What is contested.** For years the headline indictment of MOND lensing was the **weak-lensing morphology test** — claims, from large galaxy surveys, that the lensing signal around galaxies depends on their orientation or shape in a way MOND-family theories get wrong, at very high statistical significance. Earlier in this project I took those claims at near their stated strength. I no longer do. On a careful re-examination the most-cited version of that morphology split came down substantially in significance — from something near $8.8$–$9.2\sigma$ to roughly $6\sigma$ in the corrected reading — and the result is now genuinely *contested* in the literature rather than decisive. I flag it here as contested, not as a clean loss and not as a clean win. If it firms back up, it is a serious problem; if it dissolves, it was never the kill it was billed as. Honesty means living with that uncertainty out loud rather than picking the version that flatters my priors.

> **A margin aside.** Notice the discipline I am trying to model here. A "$9\sigma$ kill" against your own theory is *tempting* to cite — it makes you look unbiased, like you are not cherry-picking. But citing an inflated number against yourself is just as dishonest as citing an inflated number for yourself. Both ways, always. The corrected $\sim6\sigma$, contested, is the number that goes in the book.

---

## A worked example: how badly does the wall actually bite?

Let me make the cluster concession concrete with a slow calculation, so the word "$\eta\approx 2.3$" stops being abstract.

> **Worked Example: turning a lensing mass discrepancy into a number**
>
> **The setup.** Imagine a galaxy cluster. From its X-ray gas and its galaxies — all the *baryonic* matter we can see — we add up a total visible mass. Then we ask the framework: given that visible matter, and given the MOND-family boost to gravity at these low accelerations, how strongly *should* this cluster bend light? And separately, we measure how strongly it *actually* bends light, from the observed lensing arcs. The ratio of measured-to-predicted lensing mass is our residual $\eta$.
>
> **Step 1 — the dynamical prediction.** At cluster-center accelerations, the framework boosts the effective gravity over the Newtonian baryonic value. In the deep-MOND regime the boost to the inferred mass scales roughly as $\sqrt{a_0/g_N}$ relative to Newton, and across a real cluster it amounts, very roughly, to a factor of a few over the bare baryonic mass. Call the framework's predicted lensing mass $M_{\text{pred}}$. Because $\Phi=\Psi$ (no slip), this *equals* the dynamical mass the framework predicts — light and orbits agree inside the theory.
>
> **Step 2 — the measured lensing mass.** The observed strong-and-weak lensing of the cluster gives $M_{\text{lens}}$. For a representative relaxed cluster in the central region, observations find
> $$ \eta \equiv \frac{M_{\text{lens}}}{M_{\text{pred}}} \approx 2.3 . $$
>
> **Step 3 — read it honestly.** What does $\eta=2.3$ mean? It means that *after* the framework has done everything it can — boosted gravity at low acceleration, set the lensing mass equal to the dynamical mass — the cluster still bends light as if it carried about $2.3$ times more mass than the theory can supply. The light "sees" mass that the theory cannot put there.
>
> **Step 4 — the size of the missing piece.** Turn the ratio into a fraction. If $M_{\text{lens}} = 2.3\,M_{\text{pred}}$, then the *unexplained* part is
> $$ \frac{M_{\text{lens}} - M_{\text{pred}}}{M_{\text{lens}}} = 1 - \frac{1}{2.3} \approx 0.57 . $$
> So in the very center of such a cluster, more than *half* of the lensing signal is, in the framework's own bookkeeping, unaccounted for. That is not a rounding error. That is a hole.
>
> **Step 5 — the both-ways caveat, because I promised it.** Three honest mitigations keep $\eta\approx 2.3$ from being a clean execution. (i) The residual is a *central* quantity; integrated to the cluster's outer radius $R_{500}$ the true overall discrepancy is much milder, often near $\eta\sim 1.0$–$1.3$, once the most aggressive hydrostatic-mass assumptions are dropped (XRISM data have undercut the old $\eta\sim2$-everywhere reading). (ii) The residual is *shared with all of MOND* — it is not a wound unique to this framework, and it does not distinguish this framework from its family. (iii) A density-dependent reading of $a_0$ recovers the right *order of magnitude* of the cluster boost with no new parameters, flattening the residual's radial profile. None of that *cures* the central hole. But "uncured central residual, $\eta\sim2.3$, milder when integrated, MOND-shared, partly understood" is the honest sentence — not "the framework fails clusters by a factor of two, full stop," and not "it's fine."

That is the texture of the thing. A real hole; not a total collapse; bounded and shared and partly understood; conceded.

---

## Why this is a wall and not just a to-do item

I want to close the technical part by drawing the line clearly between two very different kinds of "we don't have that yet."

Some open problems are *to-do items*. They are things a theory has not done but could plausibly do with more work — a calculation no one has finished, an extension no one has written down. The framework has several of those, and I am hopeful about them.

The lensing sector is not one of those. It is a *wall*, and the difference is the theorem. A to-do item says "no one has found it." A no-go theorem says "under your own stated commitments, it does not exist." To get a covariant, Cassini-safe, first-principles MOND lensing law, the framework would have to *break one of its own load-bearing commitments*: give up general covariance, or give up $c_T=c$ (which experiment forbids), or admit a ghost (which sanity forbids), or give up Cassini safety (which is the whole point). There is no free direction. The only door the theorem leaves open is the preferred-frame door — and walking through it is exactly what makes the lensing phenomenological rather than derived.

So the lensing weakness is *structural*. It is not a sign that the framework is wrong — AeST passes the CMB with the same no-slip structure, so a no-slip MOND theory is empirically alive — but it is a sign that the framework, in its current form, *cannot claim lensing as a prediction*. It claims it as a fit. And a fit that you were forced into by a theorem, rather than one you chose for convenience, is at least an honest fit. But it is a fit.

This is, I think, the single sharpest answer to the question "what is the strongest thing wrong with your framework?" It is not the cluster residual (shared, partly understood). It is not the un-derived value of $a_0$ (a known, named geometric posit). It is *this*: bending light is not predicted, it is fitted, and a theorem says it has to be that way as long as the framework keeps its other promises. As frustrating as it may be, that is where the lensing wall stands, and I would rather you hear it from me, stated plainly, than discover it later and feel sold to.

---

## Summary

- **Gravitational lensing** is the bending of light by gravity. It is a uniquely powerful test because light responds to a *different combination of spacetime potentials* than orbiting matter does: dynamics probes the time potential $\Phi$, while lensing probes $\Phi+\Psi$. The difference between the two potentials is the **gravitational slip**.
- To make lensing differ from dynamics — as a MOND-like theory must, if it is to mimic dark matter for light as well as for orbits — you need to generate a slip in the low-acceleration regime.
- A **no-go theorem** forbids this honestly: **diffeomorphism invariance + gravitational waves at $c$ + ghost-freedom + Cassini safety cannot all hold at once** for a MOND-magnitude slip. Something must give, and the only surviving door is a **preferred-frame (Lorentz-violating)** lensing sector.
- Consequently the framework's lensing is **irreducibly phenomenological**: a free function fitted to data, not derived from the mechanism. This was *earned* as a concession — many covariant escape routes (DHOST, aether-shear, Hořava, khronometric, and more) were tried and each closed, one even after a tempting false "pass" that turned out to be a mislabeled equation.
- This wall is **shared**, not unique. The strongest relativistic MOND theory, **AeST** (Aether–Scalar–Tensor), has **no slip**: $\Phi=\Psi$, so lensing mass equals dynamical mass. That earns a genuine pass on **galaxy–galaxy lensing** (the lensing radial-acceleration relation), and a genuine concession on the **cluster residual** ($\eta\approx 2$–$2.3$ in the center) and on the **CMB third peak** (which AeST passes through its own tuned field content — borrowed, not derived).
- The once-headline **weak-lensing morphology split** is now **contested**, not decisive — the most-cited significance fell from $\sim$9σ to $\sim$6σ on correction. I report it as contested, both ways.
- The lensing wall is the framework's single sharpest weakness: not that the value of $a_0$ is a geometric posit (it is, and we say so), but that **bending light is fitted, not predicted, and a theorem says it must be** as long as covariance, luminal gravity, ghost-freedom, and Solar-System safety are all kept. Not a theory of everything yet — and this is the clearest reason why.

---

## Questions

1. **(Easy.)** In your own words, why is gravitational lensing a more independent test of a galaxy's mass than measuring how fast its stars orbit? What does light "respond to" that orbiting stars do not?

2. **(Easy–medium.)** What is gravitational slip? Write down the relationship between the two potentials $\Phi$ and $\Psi$ when there is *no* slip, and explain why, in that no-slip case, the mass inferred from lensing must equal the mass inferred from dynamics.

3. **(Medium.)** The no-go theorem rests on four requirements: general covariance, $c_T=c$, ghost-freedom, and Cassini safety. Pick the one you would be *most* willing to relax to escape the wall, and pick the one you would be *least* willing to relax. Justify both choices using what experiments have established.

4. **(Medium–hard.)** AeST passes the galaxy–galaxy lensing radial-acceleration relation "for free" because $\Phi=\Psi$ and its galaxy dynamics are correct. Explain why the *same* property ($\Phi=\Psi$) that gives the galaxy-scale win is what makes the cluster residual impossible to cure inside the theory. What extra ingredient would a theory need to fix clusters, and what does the no-go theorem say about installing it covariantly?

5. **(Hard / research-level.)** The chapter claims the framework's lensing is "irreducibly phenomenological" because of a theorem, whereas its rotation-curve law is "derived from a mechanism." Sharpen this distinction. Is it possible, in principle, for a future theory to *derive* the slip function from the same de Sitter–Unruh modified-inertia mechanism without violating the no-go theorem — for instance by accepting the preferred-frame sector as physical and deriving (rather than fitting) the preferred-frame slip from the cosmic rest frame? Sketch what such a derivation would have to accomplish, and what new prediction it would have to make to count as more than a relabeling of the current free function.

6. **(Research-level.)** The weak-lensing morphology split is described as "contested," with its significance falling from $\sim$9σ to $\sim$6σ on re-examination. Design an observational program — what data, what systematic checks, what null tests — that could decide whether this split is a genuine failure of no-slip MOND-family lensing or an artifact. What would a clean detection, and what would a clean null, each imply for the framework and for AeST?
