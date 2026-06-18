# Chapter 21: The Mechanism: De Sitter–Unruh Modified Inertia

> *"The pull was never missing. What was missing was the right idea of how heavy a thing becomes when almost nothing is pushing on it."*

In the last chapter we did something audacious. We took a number measured in the slow, dim outskirts of galaxies — the acceleration scale $a_0 \approx 1.2 \times 10^{-10}$ meters per second per second, the speed at which Milgrom's "new physics" switches on — and we wrote it down in terms of the cosmological constant $\Lambda$, the same $\Lambda$ that runs the accelerating expansion of the entire universe:

$$a_0 = c^2 \sqrt{\frac{\Lambda}{32\pi}}.$$

We checked that the number comes out right. We admired the coincidence. And then, if you were paying attention, you probably felt a little cheated — because a formula that gets a number right is not yet *physics*. It is a clue. A good detective does not stop at "the butler's fingerprints are on the glass." She wants the story: who reached for the glass, and when, and why.

This chapter is the story. It is the engine room of the whole framework. By the end of it you should be able to say, in plain words, *why* a galaxy on the edge of weighing almost nothing should suddenly behave as though it weighed more — and to say it without ever once invoking an invisible particle. The answer, and it is a strange and beautiful one, is that **the missing pull was never a pull at all. It was a change in how hard things are to push.**

Let me be honest with you up front, the way I will try to be honest at every turn in this book: the *form* of what follows is on firm ground, and the *mechanism* I am about to describe is built out of real, published, conservative physics that almost no one disputes in isolation. But the full chain — from "empty space has a temperature" all the way to "galaxies rotate the way they do" — has a genuine gap in it that I will show you in daylight, not hide. This is not a theory of everything yet, as frustrating as it may be. It is, I think, a real mechanism with a real wall still standing in front of it. Let's go meet both.

## The two ways to fake gravity

Newton's law of motion, the one you met in school, is usually written

$$F = m\,a.$$

Force equals mass times acceleration. There are three characters in that little sentence, and it is worth slowing down to notice that there are *three* of them, because almost everyone glides past it.

There is $F$, the **force** — the push or pull, gravity in our case.

There is $a$, the **acceleration** — how fast the object's motion is changing, which is what we actually *see* when we watch a star swing around a galaxy.

And there is $m$, the **inertial mass** — the object's reluctance to be pushed. Inertia is not weight. Inertia is sluggishness. It is the reason a parked truck is hard to get rolling even on level ice where it has no weight to fight, and the reason that same truck, once rolling, is hard to stop. Inertia is the "how much does this thing resist being accelerated" number, and Newton, with a kind of quiet confidence that turned out to be one of the deepest assumptions in all of physics, simply set it equal to a fixed property of the object: a brick has a certain $m$, here, there, today, forever.

Now. When astronomers look at the edge of a galaxy and find the stars moving faster than Newton's law allows for the visible matter, they are staring at an equation that has gone wrong. The left side and the right side don't balance. Something must give. And here is the fork in the road — the same fork from Chapter 5, but now we can see it with new eyes:

**You can add force.** Pile invisible matter — dark matter — into the galaxy until the extra gravity on the left side, the bigger $F$, accounts for the motion you see. This is the road the mainstream took, and most of the field is still on it. We spent Chapter 6 watching fifty patient years of searching for the particle that would make this road real, and we watched the searches come up empty. The road is not refuted. But it is long, and the destination has not appeared.

**Or you can change the rule.** Leave the visible matter as the only matter, and admit instead that the equation $F = ma$ itself is not quite right out here — that in this strange regime of near-weightlessness, the relationship between push and motion is different from what Newton assumed.

That second road is Milgrom's road, MOND, which we met in Chapter 17. And here is the subtlety that this entire chapter turns on, a subtlety that even many professional physicists blur: *changing the rule* is itself a fork. You can change the **force** side — invent a new law of gravity, so that gravity gets stronger than Newtonian at low accelerations. Or you can change the **inertia** side — keep gravity exactly as Einstein and Newton left it, and instead change the $m$, the sluggishness, so that objects become *harder to budge* when they are barely being budged at all.

Those two are not the same idea wearing different clothes. They make different predictions, they have different escape hatches, and — this is the punch line of the whole framework — only the second one, **modified inertia**, gives you a clean reason why the Solar System is safe. Let me say the term plainly, because it is the heart of everything that follows.

> **Modified inertia** means: the force law and the gravity stay Newtonian/Einsteinian, but an object's *resistance to acceleration* — its effective inertial mass — is no longer a fixed constant. It grows in a particular way when the object's acceleration falls below the scale $a_0$. The galaxy edge looks like extra gravity, but the books are actually being balanced on the *other* side of the equation: things out there are simply harder to push than Newton thought.

Hold that distinction. We are going to earn it.

## Why "harder to push" — where would that even come from?

Here is the question that should be nagging you. Inertia is the most taken-for-granted quantity in physics. A brick resists being pushed; that's just what bricks do. Where on Earth would a brick get *extra* reluctance, and why only when it's barely accelerating, and why at one特 special acceleration $a_0$ tied to the cosmological constant of all things?

To answer that we have to revisit three ideas you already met in Part III, because the mechanism is built entirely out of them. I'll restate each in one breath:

**First, the Unruh effect (Chapter 14).** Accelerate through empty space — truly empty space, the quantum vacuum — and you do not find it empty. You find it *warm*. An accelerating thermometer reads a temperature

$$T_{\text{Unruh}} = \frac{\hbar\, a}{2\pi c\, k_B},$$

proportional to your acceleration $a$. Stand still (or coast in a straight line) and you read zero. Push harder and the vacuum glows hotter. This is not science fiction; it is a direct consequence of combining quantum field theory with relativity, derived independently by Fulling, Davies, and Unruh in the 1970s, and it is about as mainstream as physics gets. The vacuum has a temperature *that depends on how you move through it.*

**Second, de Sitter space and the temperature floor (Chapter 15).** Our universe is not empty in the way the textbook vacuum is empty. It has dark energy — a cosmological constant $\Lambda$ — driving it to accelerate apart. Such a universe (a "de Sitter" universe, after Willem de Sitter) has a cosmic horizon, a far-off surface beyond which things recede faster than light and from which we can never get information. And just as a black hole's horizon has a temperature (Hawking's great result), so does the cosmic horizon. The whole universe sits bathed in an unimaginably faint warmth radiating in from that horizon, the **Gibbons–Hawking temperature**:

$$T_{\Lambda} = \frac{\hbar H_\Lambda}{2\pi k_B} = \frac{\hbar c}{2\pi k_B}\sqrt{\frac{\Lambda}{3}},$$

where $H_\Lambda$ is the expansion rate set by dark energy. Plug in the numbers and $T_\Lambda$ is about $3 \times 10^{-30}$ kelvin — colder than anything you can imagine, thirty zeros below a degree. But here is the word that matters: it is a **floor**. In our universe you cannot get colder than $T_\Lambda$ by coasting, because even a perfectly free-falling observer, accelerating relative to nothing, still finds the vacuum glowing at this faint dark-energy warmth. This is the **de Sitter–Unruh temperature floor** — the unremovable minimum temperature of the vacuum in a universe with dark energy. Empty space, in our cosmos, is never perfectly cold.

**Third — and this is the idea that ties inertia to temperature — the conjecture, going back to Milgrom in 1999 and resting on the Deser–Levin analysis of Unruh radiation in de Sitter space, that *inertia itself is a response to the vacuum the object swims through.*** This is the daring leap, and I want to flag it clearly as a leap, not a theorem. The thought is: maybe an object's reluctance to be accelerated is not a primitive, free-standing property like the color of a marble. Maybe it is the object's reaction to the warm vacuum it sees when it accelerates — a kind of drag against the Unruh radiation it stirs up. If that is true, then inertia *knows about* the temperature of the vacuum. And the temperature of the vacuum, in our universe, has a floor.

Now watch what those three ideas do when you put them in a row.

## The pieces click: an inertia that knows about dark energy

Picture a star far out at the edge of a galaxy, where gravity is gentle and the star's acceleration is tiny — far below $a_0$, drifting along in something very close to free fall.

When an object accelerates *hard* (you in a car, a planet near the Sun), its own Unruh temperature $T_{\text{Unruh}} \propto a$ is enormous compared to the cosmic floor $T_\Lambda$. The floor is utterly negligible. The object's "vacuum experience" is dominated by its own acceleration, and inertia behaves exactly as Newton said. Nothing new happens. Cars and planets and cannonballs are unaffected.

But when an object accelerates *very gently* — when its $a$ is so small that its own Unruh temperature $T_{\text{Unruh}} \propto a$ drops *below* the cosmic floor $T_\Lambda$ — something has to give. The object cannot experience a vacuum colder than the floor. Its "vacuum experience" can no longer keep shrinking in lockstep with its acceleration, because the floor is in the way. And if inertia is the response to that vacuum experience, then inertia can no longer shrink in lockstep either. **The object's effective inertia stops falling the way Newton's bookkeeping assumed. It stays "propped up" by the floor.** Relative to what a naive force balance expects, the object is *harder to push than it should be* — it carries a little extra sluggishness, donated by the dark-energy warmth of the vacuum.

And the crossover — the acceleration at which the object's own Unruh temperature equals the cosmic floor, the dividing line between "Newton is fine" and "something new" — is set by equating

$$T_{\text{Unruh}}(a) \sim T_\Lambda \quad\Longrightarrow\quad \frac{\hbar a}{2\pi c k_B} \sim \frac{\hbar H_\Lambda}{2\pi k_B} \quad\Longrightarrow\quad a \sim c\,H_\Lambda.$$

That crossover acceleration is, up to a pure number, exactly $a_0$. The scale at which inertia starts misbehaving is the scale at which an object's self-made vacuum warmth dips below the warmth that dark energy paints on the whole sky. *That* is why $a_0$ is tied to $\Lambda$. Not numerology — a temperature crossover.

Let me say the whole thing once more in a single, plain sentence, the sentence I'd want a sixteen-year-old to carry out of this chapter:

> Because space in our universe is never perfectly cold, an object drifting almost weightlessly feels a faint extra sluggishness — and that sluggishness, in the gentle gravity at a galaxy's edge, looks exactly like the missing pull. No dark matter. Just inertia that knows about dark energy.

There is no new substance anywhere in that story. There is no fifth force. There is only the oldest quantity in mechanics — inertia — turning out to be a little more interesting, and a little more cosmic, than Newton had any way of knowing.

> **Deeper Dive: From the temperature floor to the inertia law via Deser–Levin quadrature.**
>
> The qualitative "crossover" argument above is suggestive but loose. The quantitative content comes from asking: *what is the effective Unruh-type temperature seen by an observer who accelerates with proper acceleration $a$ while immersed in de Sitter space?* This is precisely the question Deser and Levin (1997, 1998) answered, extending earlier work by Narnhofer, Peter, and Thirring. An observer with proper acceleration $a$ in a de Sitter background of Hubble scale $H_\Lambda$ does not see the simple flat-space Unruh temperature. Instead the two scales **add in quadrature**:
> $$T_{\text{eff}} = \frac{\hbar}{2\pi c k_B}\sqrt{a^2 + a_{\rm dS}^2}, \qquad a_{\rm dS} \equiv c\,H_\Lambda.$$
> This is the central technical fact. Notice its limits. For $a \gg a_{\rm dS}$ it reduces to ordinary Unruh, $T_{\rm eff}\to \hbar a / 2\pi c k_B$. For $a \to 0$ it does **not** vanish; it floors out at $T_{\rm eff}\to \hbar a_{\rm dS}/2\pi c k_B = T_\Lambda$. The floor is built into the geometry of de Sitter space, not added by hand.
>
> Now follow Milgrom's (1999) proposal that the *inertial* contribution available to a body is what the vacuum delivers *over and above the cosmic floor* — the object responds to the temperature **excess** $T_{\rm eff}(a) - T_{\rm eff}(0)$, since the floor is the ambient state it cannot escape and cannot extract work from. Define a dimensionless interpolating function $\mu_{\rm fw}$ by writing the modified law of motion as
> $$\mu_{\rm fw}\!\left(\frac{|a|}{a_0}\right)\, m\, a = F,$$
> where $m$ is the ordinary (Newtonian) inertial mass and $\mu_{\rm fw}$ encodes the extra sluggishness. Requiring the effective inertia to track the temperature *excess* over the floor, one is led to
> $$\mu_{\rm fw}(x) = \frac{T_{\rm eff}(a) - T_{\rm eff}(0)}{(\text{ordinary Unruh at } a)} = \frac{\sqrt{x^2+1}-1}{x},\qquad x \equiv \frac{|a|}{a_0},$$
> after fixing the crossover constant. (The subscript "fw" is for "framework," to distinguish this specific interpolation from the menagerie of $\mu$-functions used elsewhere in the MOND literature; they differ in detail but share the two required limits.) Check the limits: as $x\to\infty$, $\mu_{\rm fw}\to 1$ and you recover $ma=F$ exactly — full Newtonian inertia, Solar System safe. As $x\to 0$, $\mu_{\rm fw}\to x/2$, so $\tfrac12 (a^2/a_0)\,m = F$, i.e. $a = \sqrt{2 a_0 F/m}$ — the deep-MOND square-root law that produces flat rotation curves. The single constant $a_0$ that sets the crossover is, in this picture, $a_0 = \kappa\, c\,H_\Lambda$ with a pure number $\kappa$ that the next two chapters dissect. **Be careful what I am and am not claiming here:** the Deser–Levin quadrature is solid, established physics. The *step from a temperature excess to an inertia* is Milgrom's heuristic, and converting it into the exact $\mu_{\rm fw}$ above requires modeling choices. The form is forced; the precise functional shape and the value of $\kappa$ are not handed to us for free. I will keep flagging that seam.

![Semi-log plot of the framework interpolation function mu_fw versus acceleration in units of a0, rising from the deep-MOND line toward 1.](figures/ch21_mu_fw_interpolation.png)

***Figure 21.2 — "Harder to push" made quantitative.*** Computed from the framework's equation $\mu_{\rm fw}(x)=(\sqrt{x^2+1}-1)/x$, read off the de Sitter-Unruh temperature *excess* over the floor. The factor $\mu_{\rm fw}$ multiplies $m\,a$ in $\mu_{\rm fw}\,m\,a=F$, so $\mu_{\rm fw}<1$ means an object delivers *less* response per unit force — it behaves as if harder to push. For $x\gg1$ (Solar System) $\mu_{\rm fw}\to1$ and Newton is recovered exactly; for $x\ll1$ (galaxy edge) $\mu_{\rm fw}\to x/2$, the deep-MOND square-root law that flattens rotation curves. The single scale $a_0$ marks the handoff.

**Source:** Figure generated by [`book/figures/ch21_mu_fw_interpolation.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch21_mu_fw_interpolation.py). Framework interpolation and modified-inertia law: [Zenodo 10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540); heuristic origin Milgrom 1999 with Deser & Levin 1997, Class. Quantum Grav. 14, L163.


![Log-log plot of effective vacuum temperature versus acceleration, showing the ordinary Unruh line bending into a constant floor.](figures/ch21_desitter_unruh_temperature_floor.png)

***Figure 21.1 — The temperature floor that sets $a_0$.*** Computed from the framework's equations. The ordinary flat-space Unruh temperature (grey dashed) falls in lockstep with acceleration all the way to zero. The Deser-Levin quadrature $T_{\rm eff}=\frac{\hbar}{2\pi c k_B}\sqrt{a^2+(cH_\Lambda)^2}$ (purple) tracks it at high acceleration but **floors out** at $T_\Lambda\approx2.2\times10^{-30}\,$K (red dotted) — the unremovable warmth dark energy paints on the vacuum. The crossover, where an object's self-made warmth dips below the floor, sits at $a\sim cH_\Lambda$, which is the framework's $a_0$ up to a pure number $\kappa$ — no galaxy data used.

**Source:** Figure generated by [`book/figures/ch21_desitter_unruh_temperature_floor.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch21_desitter_unruh_temperature_floor.py). Quadrature: Deser & Levin 1997, Class. Quantum Grav. 14, L163; Unruh 1976, PRD 14, 870. Framework scale $a_0=c^2\sqrt{\Lambda/32\pi}$: [Zenodo 10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540).


## Why this is Solar-System-safe — and why that is not a lucky accident

Here is where modified inertia earns its keep, and where it pulls decisively ahead of the "modify gravity" cousin.

If you modify *gravity* — make the gravitational force itself stronger at low accelerations — then you have a problem in your own backyard. The outer Solar System has regions where the *gravitational* acceleration from the Sun is small. Pluto, the Voyager probes, the far reaches of the Oort cloud: out there the Sun's pull is weak. A modified-*gravity* MOND would predict extra pull on those bodies, and we have flown spacecraft through exactly those regions. The Cassini probe, in particular, tracked Saturn's distance to exquisite precision for years and would have screamed if there were an extra MOND-strength tug. There wasn't. Modified-gravity theories have to wriggle out of this with extra machinery.

Modified *inertia* gates differently, and the difference is everything. In a modified-inertia theory, what matters is not whether the *gravitational field* is weak — it's whether the *object's total acceleration* is small. And here is the saving subtlety: an object in the Solar System, even way out past Pluto where the Sun's pull is feeble, is **still being accelerated** — it's whipping around the Sun (or around the galactic center, or feeling the Sun's gravity as it falls) at an acceleration vastly larger than $a_0$. Its own Unruh temperature towers over the cosmic floor. So $\mu_{\rm fw} \approx 1$, inertia is exactly Newtonian, and nothing anomalous happens. The modification *switches itself off* wherever the actual acceleration is large — which is everywhere we have ever sent a probe.

> **Deeper Dive: The gating, made precise.**
>
> The distinction is which quantity sits inside the interpolating function. In modified *gravity* (e.g. AQUAL, the aquadratic Lagrangian theory, or the relativistic theory AeST), the field equation reads schematically $\nabla\!\cdot\!\big[\mu(|\nabla\Phi|/a_0)\,\nabla\Phi\big] = 4\pi G\rho$, so the modification is controlled by the *gravitational field strength* $|\nabla\Phi| = g_N$. In modified *inertia*, the modification is controlled by the *kinematic acceleration* $|a|$ of the test body itself:
> $$\mu_{\rm fw}\!\left(\frac{|a|}{a_0}\right) m\,a = -m\,\nabla\Phi_N.$$
> In the deep Solar System these two quantities part ways. Consider Saturn: its heliocentric gravitational acceleration is $g_N \approx 6\times 10^{-5}\,\text{m/s}^2$, comfortably above $a_0\approx 1.2\times10^{-10}$. Both theories are safe at Saturn. But consider a body at the Sun–galaxy saddle, or an object whose *Newtonian* field has nearly cancelled — there, $g_N$ can dip below $a_0$ while the body's *actual* acceleration (dominated by the galaxy, or by orbital motion about a companion) stays large. A modified-gravity theory predicts an anomaly in such low-field pockets; a modified-inertia theory predicts none, because $|a|$ is what gates, and $|a|\gg a_0$. Conversely, on a circular galactic orbit $g_N \approx |a|$ and the two frameworks agree to leading order on rotation curves — which is exactly why MOND's galaxy successes are *shared* across the whole family and are **not** unique to this picture (a point I will hammer again in Chapter 26). The Cassini bound on an anomalous Saturn-range acceleration, of order $10^{-14}\,\text{m/s}^2$, is passed *automatically* by modified inertia and only *with effort* by modified gravity. This Solar-System safety is, to my mind, the single strongest structural argument for the inertia interpretation — it is not a fudge bolted on afterward; it falls out of which variable lives inside $\mu_{\rm fw}$.

So: same flat rotation curves out where galaxies live, automatic silence in the Solar System where we can check most precisely. That is a real, structural virtue, and I want you to enjoy it. But now I owe you the wall.

## The wall: the wrong-sign problem, and an honest accounting

If the story I just told were the *whole* story — "object feels a warm bath, bath adds drag, drag looks like inertia" — then a careful physicist would catch it out within an afternoon, and would be right to. The naive version of the mechanism has a fatal flaw, and intellectual honesty demands I show it to you rather than usher you past it.

The flaw is this. If you model the extra inertia as a *passive* drag — the object plowing through a warm vacuum and feeling resistance, like a spoon through honey — and you work out the sign of that resistance using ordinary linear-response physics (the fluctuation–dissipation theorem, the same machinery that governs Brownian motion and Johnson noise in a resistor), **the force comes out with the wrong sign, or with the wrong velocity-dependence, to be inertia at all.** A genuine drag depends on *velocity* and opposes motion; it makes things slow down and stop. Inertia depends on *acceleration* and resists *changes* in motion; it does not drain energy. You cannot get the second by naively summing up the first. Several authors have pointed this out, and they are correct: the cartoon of "Unruh radiation as a frictional bath" simply does not reduce to a clean modified-inertia law. If you've read popular accounts that breezily say "the vacuum pushes back and that's the missing gravity," you have read the cartoon, and the cartoon is broken.

This is not a small embarrassment to be swept under the rug. It is *the* central theoretical problem of any modified-inertia program, and it has a name attached to its deepest form.

> **Deeper Dive: The Milgrom 1994 no-go, and why the resolution must be a time-nonlocal action.**
>
> Milgrom himself proved the sharpest version of the obstruction in 1994. The result, which I'll call the **Milgrom 1994 no-go**, states roughly: *any modified-inertia theory that (i) is derived from an action, (ii) is Galilean-invariant, and (iii) gives the correct MOND limit for circular orbits, cannot be a local theory of the particle's position and its finitely many time-derivatives.* In plain terms — you cannot build honest modified inertia out of $x$, $\dot x$, $\ddot x$, and a finite stack of higher derivatives evaluated at a single instant. A local Lagrangian $L(x,\dot x, \ddot x, \dots)$ will not do it. This is a *theorem*, not a difficulty of imagination, and any serious proposal must obey it.
>
> The no-go also tells you the *only* door left open. If finitely-many-derivatives-at-one-instant is forbidden, the action must depend on the **entire history of the trajectory** — it must be a **time-nonlocal action**, one whose Lagrangian at time $t$ depends on $x(t')$ for a range of other times $t'$, weighted by some memory kernel. This is not exotic hand-waving; nonlocal-in-time effective actions are completely standard in physics whenever you "integrate out" a bath or a field with its own dynamics (the influence functional of Feynman and Vernon, the radiation-reaction of an accelerated charge, the Caldeira–Leggett model of quantum dissipation all live here). The vacuum *is* such a field. So the structurally correct object is
> $$S[x(\cdot)] = \int dt\,dt'\; x(t)\, \mathcal{K}\!\big(t-t';\,a_0\big)\, x(t') + \cdots,$$
> with a memory kernel $\mathcal K$ that carries the scale $a_0$ and is engineered so that (a) for high-frequency / high-acceleration motion it collapses to the ordinary local $\tfrac12 m\dot x^2$ kinetic term (Newton, Solar-System safe), and (b) for slow, sustained, low-acceleration motion it reproduces the deep-MOND $\mu_{\rm fw}\to x/2$ behavior. Crucially, a properly constructed kernel can give a contribution that depends on the sustained *acceleration* (inertia-like) rather than the instantaneous *velocity* (drag-like) — which is exactly how the wrong-sign problem is *resolved rather than evaded*. The sign problem of the naive passive bath is an artifact of forcing a local, velocity-coupled, dissipative response onto a phenomenon that is intrinsically nonlocal-in-time and acceleration-coupled.
>
> **Now the honesty, in full.** What I have described is the *shape* of the correct answer: a time-nonlocal worldline action that obeys Milgrom's no-go instead of falling foul of it. That such a structure *can* encode the MOND limit and *can* avoid the sign problem is established. What does **not** yet exist — not in my work, not in anyone's — is a *first-principles derivation* of the specific kernel $\mathcal K$ from the de Sitter–Unruh vacuum, with no free functions, that produces $\mu_{\rm fw}$ on the nose. The mechanism is, at this level, *consistent and well-motivated* but not *closed*. The temperature floor is real (Deser–Levin). The need for a nonlocal action is real (Milgrom 1994). The marriage of the two into a unique, derived kernel is the open frontier. I will not dress that gap up as anything other than what it is. This is the most important caveat in the chapter, and it is the most important caveat in the whole framework: **the form $a_0 \sim c^2\sqrt\Lambda$ is forced, the mechanism is the right *kind* of mechanism, but the mechanism is not derived end-to-end.** Not a theory of everything yet — as frustrating as it may be.

I want to dwell on that for a moment, because how you feel about it tells you what kind of reader you are. A hostile reader sees the gap and says, "Then you have nothing — just a coincidence dressed in physics vocabulary." A credulous reader skips the gap and says, "He's solved dark matter." Both are wrong, and both are wrong in the same lazy way: they refuse to hold two true things at once. The honest position — the only one I'll defend — is that we have a *forced functional form*, a *Solar-System-safe gating mechanism*, and a *concrete, theorem-respecting program* for closing the derivation, with the closure not yet achieved. That is more than a coincidence and less than a proof. Real science usually lives in exactly that uncomfortable middle for a long time before it resolves one way or the other.

## A second honesty: what "looks like extra gravity" really means

Let me clear up one thing that trips people up, because it matters for later chapters.

When I say the extra inertia "looks exactly like the missing pull," I mean it in a precise and limited way. On a circular orbit — a star going round a galaxy at steady speed — the only acceleration is the centripetal one, pointing inward, and a body that is *harder to accelerate inward* will settle into the same orbit that a body of normal inertia would settle into under a *stronger inward pull*. The two are observationally identical for that motion. That's the magic, and it's why rotation curves come out right.

But "looks like extra gravity for circular orbits" is not the same as "is extra gravity for everything." Light does not orbit; it streaks past on nearly straight lines, barely accelerating in the relevant sense. So a theory that fixes rotation curves by fattening the *inertia* of slow-moving stars does not automatically bend *light* by the right amount — and gravitational lensing, the bending of light by mass, becomes a separate and genuinely unsolved problem. I am telling you this now so that Chapter 28, "The Lensing Wall," does not feel like a betrayal. It is a real weakness, it is shared with the leading relativistic MOND theory (AeST), and a no-go theorem stands in the way of curing it covariantly without breaking the Solar-System safety we worked so hard to win. The same modified-inertia logic that makes the Solar System safe is part of *why* lensing stays hard. The virtues and the wounds come from the same root. That is usually how it goes with real physical ideas.

## Worked Example

> **Worked Example: From the temperature floor to a flat rotation curve.**
>
> Let us walk, slowly, from "the vacuum has a temperature floor" to "the star's orbital speed stops falling off with distance" — the flat rotation curve that started this whole mystery in Chapter 1. We will use only the pieces assembled above. Take it one line at a time; no step is hard, there are just several of them.
>
> **Step 1 — the floor temperature.** The de Sitter–Unruh floor is $T_\Lambda = \hbar H_\Lambda / 2\pi k_B$. With $H_\Lambda \approx 1.8\times 10^{-18}\,\text{s}^{-1}$ (the dark-energy expansion rate),
> $$T_\Lambda = \frac{(1.05\times10^{-34})(1.8\times10^{-18})}{2\pi(1.38\times10^{-23})}\ \text{K} \approx 2.2\times 10^{-30}\ \text{K}.$$
> Thirty zeros below a degree. Hold onto it as the ambient warmth of empty space.
>
> **Step 2 — the crossover acceleration.** An object's own Unruh temperature equals this floor when $\hbar a /2\pi c k_B = T_\Lambda$, i.e. when $a = cH_\Lambda$. Numerically $a = (3\times10^8)(1.8\times10^{-18}) \approx 5.4\times10^{-10}\,\text{m/s}^2$. The framework's full bookkeeping (the $\kappa=\tfrac12$ and the $\sqrt{8\pi/3}$ kernel of Chapters 22–23) sharpens this to $a_0 = 9.36\times10^{-11}\,\text{m/s}^2$, of the same order. The crossover scale is *automatically* of order $cH_\Lambda \sim 10^{-10}\,\text{m/s}^2$ — within a factor of a few of the measured $a_0$ with **no galaxy data used at all.** That order-of-magnitude inevitability is the heart of the claim.
>
> **Step 3 — the deep-MOND inertia law.** Far out in a galaxy a star's acceleration is tiny, $x=|a|/a_0 \ll 1$, so $\mu_{\rm fw}(x)\to x/2$ and the law $\mu_{\rm fw}\,m a = F$ becomes
> $$\frac{1}{2}\frac{a}{a_0}\, m\, a = F \quad\Longrightarrow\quad a^2 = \frac{2a_0 F}{m}.$$
> The gravitational force from the galaxy's visible mass $M$ at radius $r$ is the ordinary Newtonian one, $F = GMm/r^2$ (we did **not** touch gravity), so
> $$a^2 = \frac{2a_0\, GM}{r^2}\quad\Longrightarrow\quad a = \frac{\sqrt{2 a_0 G M}}{r}.$$
>
> **Step 4 — impose circular motion.** For a circular orbit the acceleration is $a = v^2/r$. Set the two expressions equal:
> $$\frac{v^2}{r} = \frac{\sqrt{2 a_0 G M}}{r}\quad\Longrightarrow\quad v^2 = \sqrt{2 a_0 G M}\quad\Longrightarrow\quad v^4 = 2\,a_0\,G\,M.$$
> Look hard at that last line. **The radius $r$ has cancelled out completely.** The orbital speed $v$ no longer depends on how far out you are. That is a *flat rotation curve* — the very thing Vera Rubin found in the 1970s and the thing dark matter was invented to explain. Here it has dropped out of an inertia that knows about the temperature floor of a dark-energy universe, with the only "force" being plain Newtonian gravity from the stars and gas you can actually see.
>
> **Step 5 — sanity check on a real galaxy.** Take the Milky Way's baryonic mass, $M \approx 6\times10^{10}\,M_\odot \approx 1.2\times10^{41}\,\text{kg}$, and $a_0 = 9.36\times10^{-11}$:
> $$v^4 = 2(9.36\times10^{-11})(6.67\times10^{-11})(1.2\times10^{41}) \approx 1.50\times10^{21}\ \text{m}^4/\text{s}^4,$$
> $$v \approx (1.50\times10^{21})^{1/4} \approx 1.97\times10^{5}\ \text{m/s} \approx 197\ \text{km/s}.$$
> The Milky Way's outer rotation speed is observed to be roughly $200\,\text{km/s}$. We landed within a few percent — *and notice we also just re-derived the baryonic Tully–Fisher relation* $v^4 \propto M$ of Chapter 18, with the proportionality constant fixed by $a_0$, and through $a_0$ by the cosmological constant. **One honest caveat, carried as always:** this success — flat curves and the $v^4\propto M$ law — is *shared by the entire MOND family*, modified-gravity and modified-inertia alike. It is a triumph of the *form*, which is forced; it is not, by itself, evidence for *this* mechanism over the other MOND cousins. The mechanism's distinctive fingerprint lives elsewhere — in the time-evolution $a_0(z)$ of the next chapters — not in the rotation curve we just nailed.

![Rotation speed versus radius: the Newtonian curve falls off while the modified-inertia curve flattens to a constant near 200 km per second.](figures/ch21_flat_rotation_curve.png)

***Figure 21.3 — The worked example, drawn.*** Computed from the framework's equations for a Milky-Way-mass disk ($M_b\approx6\times10^{10}\,M_\odot$). With only ordinary Newtonian gravity from the visible mass, the speed falls as $\sqrt{GM/r}$ (grey dashed). Solving the modified-inertia law $\mu_{\rm fw}(|a|/a_0)\,m\,a=GMm/r^2$ at each radius (purple) makes the curve **flatten**, settling onto the deep-MOND value $v=(2a_0GM)^{1/4}\approx197\,$km/s where the radius cancels entirely — landing in the observed $\sim200\,$km/s band (red). This success is real but shared by the whole MOND family; the distinctive test lives in $a_0(z)$.

**Source:** Figure generated by [`book/figures/ch21_flat_rotation_curve.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch21_flat_rotation_curve.py). Framework law and $v^4=2a_0GM$: [Zenodo 10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540). Flat curves first measured by Rubin & Ford 1970, ApJ 159, 379; baryonic Tully-Fisher: McGaugh 2012, AJ 143, 40.


## Stepping back

So here is the engine room, with the lights on and nothing hidden in the corners.

The fuel is dark energy — the cosmological constant $\Lambda$ — which gives our universe a faint, unremovable temperature floor in the vacuum, the de Sitter–Unruh temperature $T_\Lambda$. The moving part is inertia, reconceived (following Milgrom and Deser–Levin) not as a frozen property of matter but as matter's response to the vacuum it accelerates through. When an object accelerates hard, its self-made vacuum warmth swamps the floor and inertia is ordinary Newton — so cars, planets, and Cassini are untouched. When an object barely accelerates at all, the floor props its inertia up, it grows reluctant to be pushed, and at the edge of a galaxy that extra reluctance mimics, to the eye, exactly the missing gravitational pull. The crossover sits at an acceleration of order $cH_\Lambda$ — which is to say, at $a_0$ — because that is where an object's own Unruh warmth dips below the warmth dark energy paints across the sky.

That is a genuine mechanism, built from genuine physics, and its Solar-System safety is a structural gift rather than a patch. And it has a real, unhealed wound: the naive passive-bath version gets the sign wrong, the cure must be a time-nonlocal action that respects Milgrom's 1994 no-go, and the *specific* memory kernel that would derive $\mu_{\rm fw}$ from the vacuum with no free functions does not yet exist. The form is forced. The mechanism is the right *kind* of mechanism. The end-to-end derivation is unfinished. All three of those are true at once, and a reader who can hold all three is reading this book exactly as I hoped it would be read.

Not a theory of everything yet — as frustrating as it may be. But a clear, honest, and rather beautiful idea about why the spin of galaxies remembers the dark energy filling the sky.

## Summary

- **The fork inside the fork.** "Missing mass" can be patched by *adding force* (dark-matter particles) or by *changing the law*. Changing the law itself splits into **modified gravity** (strengthen the force at low acceleration) and **modified inertia** (keep gravity Newtonian, make objects harder to push at low acceleration). This framework is modified *inertia*.

- **The three borrowed ideas.** (1) The **Unruh effect**: an accelerating observer sees a warm vacuum, $T_{\rm Unruh}\propto a$. (2) The **de Sitter–Unruh temperature floor** $T_\Lambda = \hbar H_\Lambda/2\pi k_B$: in a dark-energy universe the vacuum has a minimum temperature you cannot coast below. (3) Milgrom's conjecture that **inertia is a response to that vacuum** — so inertia inherits the floor.

- **Why $a_0$ tracks $\Lambda$.** The new physics switches on where an object's own Unruh temperature drops below the cosmic floor, i.e. where $a \sim cH_\Lambda$. That crossover *is* the acceleration scale $a_0$, tying the galactic scale to dark energy with no galaxy data used.

- **The Deser–Levin quadrature** $T_{\rm eff}=\frac{\hbar}{2\pi ck_B}\sqrt{a^2 + (cH_\Lambda)^2}$ supplies the floor rigorously; reading the inertia from the temperature *excess* over the floor yields the framework interpolation $\mu_{\rm fw}(x)=(\sqrt{x^2+1}-1)/x$, which is Newtonian ($\mu_{\rm fw}\to1$) for $x\gg1$ and deep-MOND ($\mu_{\rm fw}\to x/2$) for $x\ll1$.

- **Solar-System safety is structural.** Because $\mu_{\rm fw}$ gates on the body's *actual acceleration* $|a|$, not on the gravitational field strength, the modification switches off everywhere a probe actually flies (orbital accelerations $\gg a_0$). Cassini's bound is passed automatically — a virtue of modifying inertia rather than gravity.

- **The open wall, stated plainly.** A naive "passive warm-bath drag" gives the **wrong sign** for inertia. The **Milgrom 1994 no-go** proves modified inertia cannot come from a local, finite-derivative action; the cure must be a **time-nonlocal action** with a memory kernel — standard physics in form, and it resolves (not evades) the sign problem. But the *specific* kernel that would derive $\mu_{\rm fw}$ from the de Sitter–Unruh vacuum with no free functions **does not yet exist**. The form is forced; the mechanism is unfinished.

- **Shared, not unique.** The flat rotation curves and the baryonic Tully–Fisher law $v^4=2a_0GM$ that fall out of this mechanism are real successes — but they are *shared with the whole MOND family*, not fingerprints of this mechanism in particular. The distinctive test lives in $a_0(z)$ (Chapters 25–26), and lensing remains a genuine open problem (Chapter 28).

## Questions

1. **(Easy.)** In your own words, explain the difference between "modified gravity" and "modified inertia," and give the everyday reason — using the idea of a probe like Cassini still being strongly accelerated — why modified inertia leaves the Solar System untouched.

2. **(Easy–medium.)** The Unruh temperature is $T_{\rm Unruh}=\hbar a/2\pi c k_B$. Roughly what acceleration $a$ would you need to feel a vacuum as warm as room temperature ($\approx 300\,$K)? Compare that to $a_0\approx 10^{-10}\,\text{m/s}^2$ and to the de Sitter floor temperature $T_\Lambda\approx 2\times10^{-30}\,$K. What does the enormous gap tell you about why the effect is invisible in everyday life but relevant at a galaxy's edge?

3. **(Medium.)** Using the deep-MOND inertia law $\tfrac12(a/a_0)\,m\,a = GMm/r^2$ and the circular-orbit condition $a=v^2/r$, re-derive $v^4 = 2a_0 GM$ yourself, showing each cancellation. Then estimate the flat rotation speed of a dwarf galaxy with baryonic mass $M = 10^{9}\,M_\odot$. Is it faster or slower than the Milky Way's, and why does that make sense?

4. **(Medium–hard.)** The text claims the rotation-curve and Tully–Fisher successes are "shared with the whole MOND family" and therefore do *not* select this mechanism over modified-gravity MOND. Explain carefully why a circular orbit cannot distinguish "harder to push inward" (modified inertia) from "pulled harder inward" (modified gravity). Then propose, in words, a kind of motion or observation that *could* in principle tell them apart.

5. **(Hard / research-level.)** State the Milgrom 1994 no-go theorem in your own words, and explain why it forces any honest modified-inertia theory to be *time-nonlocal* (history-dependent) rather than built from finitely many time-derivatives at a single instant. Why does a passive, velocity-coupled "drag" model give the wrong sign for inertia, and how does an acceleration-coupled, nonlocal memory kernel resolve the problem *while obeying* the no-go?

6. **(Research-level / open.)** The chapter is explicit that no first-principles derivation yet exists of the specific memory kernel $\mathcal{K}(t-t';a_0)$ that would yield $\mu_{\rm fw}$ from the de Sitter–Unruh vacuum with no free functions. Sketch what such a derivation would have to accomplish: which limits it must reproduce, which symmetries it must respect, and what would count as success versus what would merely be a fit. If you could prove one auxiliary result that would most advance the program, what would it be — and would proving it derive the *value* of $a_0$, or only its *form*? (Quarantine check: be careful to distinguish deriving the form from deriving the number.)
