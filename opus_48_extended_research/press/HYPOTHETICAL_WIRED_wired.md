> **HYPOTHETICAL FEATURE — written in the style of *Wired*.**
> This is **not** an actual *Wired* article. It was not commissioned, written, reviewed, or endorsed by *Wired* or anyone affiliated with it. It is a stylistic illustration — how this publication *might* cover the de Sitter–MOND framework, pitched at its typical audience and technical level. Every scientific claim reflects the framework's honest, both-ways standing: a falsifiable one-parameter theory of gravity and the dark sector — not a confirmed result, and **not a theory of everything**.
>
> *Subject: the de Sitter–MOND framework of Carl P. Zimmerman (Briar Creek Tech). Drafted June 2026.*

---

# The Man Who Bet Dark Matter on a Single Number

### An independent researcher says the cosmos has been hiding a coincidence in plain sight for fifty years. The telescopes that could vindicate him—or end his idea for good—are already pointed at the sky.

There is a number that has haunted physics since 1983, and almost nobody outside a small circle has ever heard of it. It is about 1.2 × 10⁻¹⁰ meters per second squared—an acceleration so faint it is roughly the speed a snail would pick up if it had ten billion years to get going. Below that threshold, something strange happens. Stars at the edges of galaxies, drifting through that whisper-quiet regime, refuse to slow down the way Newton and Einstein say they should. The galaxies spin too fast for the matter we can see. For ninety years, the mainstream answer has been dark matter: invisible particles, five times more abundant than everything we can touch, holding the cosmos together with gravity we cannot otherwise account for.

Carl Zimmerman thinks the answer was sitting in a different equation the whole time.

Zimmerman is not a tenured astrophysicist. He runs Briar Creek Tech, a small software shop that builds CRMs and lead-generation tools for clients around Charlotte, North Carolina. He writes Flutter apps for a living. And in his off hours, across 2026, he published three papers to Zenodo—the open-access repository CERN helped build—arguing that the famous galaxy-rotation number isn't a fundamental constant of nature at all. It's an echo. An echo of dark energy, the mysterious pressure that is blowing the universe apart.

His claim fits on a single line: **a₀ = c²√(Λ/32π)**.

In words: the acceleration scale where galaxies go haywire is set by the cosmological constant Λ—the same quantity that drives cosmic acceleration. Plug in the measured value of dark energy and the formula spits out 9.36 × 10⁻¹¹ m/s², sitting comfortably inside the empirical spread. The galaxy problem and the dark-energy problem, in this telling, are not two mysteries. They are one mystery, seen from two directions.

If that sounds too tidy to be true, you are in good company. Most cosmologists would tell you exactly that.

---

The coincidence itself is real, and it is old. Physicists have noticed for decades that the MOND acceleration scale—MOND stands for Modified Newtonian Dynamics, the heretic's alternative to dark matter—lands suspiciously close to the acceleration you'd compute from the cosmological constant. Roughly, a₀ ≈ cH₀, the speed of light times the expansion rate of the universe. It's the kind of thing that makes a certain personality type sit up at 2 a.m. Either it means something, or the universe is playing a cruel joke.

The mainstream has mostly filed it under "joke," or at least "intriguing but unexplained." Zimmerman filed it under "causal."

To make the coincidence into a mechanism, he reaches for a piece of physics most people have never heard of: the de Sitter–Unruh effect. The Unruh effect, predicted in 1976, says that if you accelerate through empty space, the vacuum stops looking empty—it glows with a faint thermal warmth, a temperature proportional to your acceleration. Now add dark energy. A universe with a cosmological constant has its own irreducible temperature floor, a baseline warmth to the vacuum that never goes away. Building on work by the Israeli physicist Mordehai Milgrom—MOND's founder—and on the 1997 Deser–Levin analysis of acceleration temperatures, Zimmerman argues that a star drifting in a galaxy's outskirts, barely accelerating at all, feels that cosmic temperature floor as a kind of drag. It resists being pushed. From the outside, that extra resistance looks exactly like extra gravity—like dark matter that isn't there.

The crucial word is *inertia*. Zimmerman's framework doesn't add a new force. It modifies how hard it is to accelerate things in the first place, and only in the regime where accelerations are vanishingly small. Crank the acceleration up—say, to anything you'd find in the Solar System—and the effect switches off automatically. That's not a bug fix bolted on after the fact. It's baked into the structure, which is why the framework is, in the jargon, "Cassini-safe": it doesn't violate the exquisitely precise tracking of NASA's Saturn probe, the measurement that has strangled so many alternative-gravity theories in their cribs.

This is the part that genuinely impresses people who look closely. The *form* of Zimmerman's equation—a₀ scaling as c² times the square root of Λ—is what physicists call over-determined. Several independent lines of reasoning force that same shape. The funny-looking factor buried inside it, a square root of 8π/3 with its awkward half-integer power of π, isn't a fudge; it falls out of the 8π in Einstein's field equations and the factor of 3 in the Friedmann equation that governs cosmic expansion. The geometry leaves little room to wiggle.

And then there is the number Zimmerman is proudest of: **one**. As in, one free parameter.

---

The standard model of cosmology—ΛCDM, the reigning champion—runs on six adjustable parameters plus an undetected particle that decades of increasingly sensitive experiments have failed to catch. Zimmerman's framework, he argues, runs on a single knob, which he calls κ = 1/2. And in his third 2026 paper, he tried to prove that the knob isn't even really adjustable—that it's pure geometry.

His argument: κ = 1/2 is what you get from the single-degree-of-freedom limit of a known bound in quantum gravity (the Cohen–Kaplan–Nelson relation between a system's size and its energy), and from an exact arithmetic identity—the 3/8π in the equation is just the Schwarzschild ½ divided by the volume of a ball, 4π/3. Run the numbers and the two expressions are identical to the last decimal. He further claims the value can't be shifted by demanding the theory stay free of ghosts, stay unitary, respect holography, or match the Standard Model's degree-of-freedom count. One knob, locked by geometry, versus six parameters and a particle nobody has found.

It is, as physics goes, an aesthetically gorgeous pitch. Which is precisely why Zimmerman is so careful—almost compulsively careful—about what it does *not* do.

"It's not a theory of everything yet," he says, "as frustrating as it may be."

He means it literally. The framework is a theory of gravity and the dark sector, and nothing else. It says nothing about why the proton weighs 1,836 times what the electron does—that ratio still reduces to a free Yukawa coupling and the strong force, untouched. It doesn't derive the masses of any particles, doesn't explain the Koide relation among the lepton masses, doesn't produce the Standard Model's gauge group. All of that remains walled off, exactly as it is for every other theory of gravity on the market, string theory included. Zimmerman is unusually loud about this for someone selling a big idea. He will tell you, unprompted, that his equation does not even derive the *value* of a₀—that κ = 1/2 is a geometric *posit*, an assumption, which makes the theory one-parameter, not the zero-parameter holy grail. He'd rather say it himself than have a referee say it for him.

There is a discipline to how this was built that is worth pausing on, because it's where the tech-culture story and the physics story fuse. Zimmerman didn't develop the framework alone in the romantic-genius sense. He developed it adversarially—running the math through AI systems instructed not to cheerlead but to attack. To find the convention that makes the equation look good and then deliberately swap in the convention that makes it look bad. To check whether a claimed "win" against the data survives when you change the assumed mass-to-light ratio of a galaxy, or the interpolation function, or the weighting of the fit—and to report it honestly when a result turns out to be an artifact rather than a triumph. It is, in a way, the open-source ethos applied to one's own pet theory: assume your code has bugs, write the test that tries hardest to break it, and publish the failures alongside the passes. The papers went up on Zenodo, free for anyone to tear apart, rather than into the slow grind of a journal—or worse, into a drawer.

---

So what would it take to know if he's right?

This is the part that elevates the whole enterprise from numerology to science, and it is genuinely on a clock. Zimmerman's framework makes a prediction that ordinary dark matter does not, and that even most of the MOND family does not: if a₀ is set by dark energy, and dark energy *changes over cosmic time*, then a₀ must change too. The acceleration scale in distant, ancient galaxies should differ from the one in our cosmic backyard, tracking the square root of the dark-energy density at that epoch.

And here the bet gets specific—dangerously specific. The DESI survey's second data release has reported hints that dark energy isn't a constant after all, but is evolving (in the parameters cosmologists write as w₀ ≈ −0.75, wₐ ≈ −0.86). Run that evolution through Zimmerman's formula and you don't get a boring straight line. You get a curve with character: a roughly 6 percent *bump* in a₀ near redshift 0.4—right where dark energy crosses a threshold cosmologists call the phantom divide—followed by a decline to about three-quarters of today's value by redshift 3. A rival reading of the same physics predicts a₀ *rising* into the past instead; at redshift 3 the two forecasts differ by a factor of around seven and a half. Plain-vanilla ΛCDM predicts a flat line. Three distinguishable curves. One sky to check them against.

The cleanest test is almost charmingly concrete. It's the *sign* of a tiny offset in how fast distant galaxies rotate. If Zimmerman is right, galaxies at redshift 3 should spin about 7 percent slow relative to the local relation between mass and rotation speed—a fingerprint in the baryonic Tully-Fisher relation, the empirical law connecting a galaxy's visible mass to how fast it turns. DESI's third data release, expected around 2026–27, could begin to see it. High-redshift kinematics from the Extremely Large Telescope, JWST, and ALMA—the back half of this decade and into the 2030s—could nail it.

Which means Zimmerman has done the bravest and most uncomfortable thing an idea-maker can do. He has written down the conditions for his own funeral.

If the DESI evolving-dark-energy signal holds and the high-redshift Tully-Fisher offset shows up with the right sign and size, he has something extraordinary: the first direct evidence that the galaxy-rotation scale breathes with the cosmos. If the signal reverts to a plain, unchanging cosmological constant—and he is the first to flag that recent reanalyses, sensitive to the statistical priors you choose, have softened that DESI signal toward something like 1.3 sigma, a level no one would bet a career on—then his framework's distinctive content simply dissolves. It collapses back into ordinary MOND, an interesting curiosity with the same baggage MOND has always carried. The a₀(z) prediction, as he puts it, is a hostage.

He does not flinch from the rest of the baggage either. The galaxy relations his framework reproduces—the radial-acceleration relation, the Tully-Fisher law—are not unique to it; they are shared by the entire MOND family, and reproducing them proves the framework is *consistent*, not that it is *correct*. Galaxy clusters remain a sore spot: they retain a residual mass discrepancy that his framework, like every MOND-style theory, does not fully cure. And gravitational lensing—the bending of light by mass, one of the sharpest tools cosmologists own—is a genuine weak point. One of Zimmerman's own 2026 results is a *no-go theorem*: a proof that you cannot build a covariant, Solar-System-safe MOND lensing in the obvious way. The framework's lensing therefore remains an un-derived free function, the same unfinished business that AeST—the leading relativistic MOND theory, built by serious academics—has never closed either. He proved his own idea has a hole, and published the proof.

There's one more twist, and it's the kind of thing that could make a Standard Model physicist look up from their detector. Because Zimmerman's framework picks out a preferred frame of reference—it quietly violates the strict Lorentz symmetry that special relativity holds sacred—it is, technically, what particle physicists call a Standard Model Extension background. That's not a hand-wave; it's a specific, mature framework for cataloging Lorentz violation. And it means the same a₀ that bends galaxy rotation curves should induce a tiny, computable Lorentz-violation coefficient measurable in a lab, along with a falsifiable theorem: the violation should break Lorentz symmetry while *preserving* the deeper CPT symmetry. The induced lab signal already sits within about a factor of two of the tightest current bound. Another tripwire. Another way to die.

---

Step back, and the honest shape of the thing comes into focus—neither the breakthrough some would want to crown nor the crankery a tired reviewer might wave away.

What Zimmerman has is a brave, economical, falsifiable idea: a fifty-year-old coincidence promoted to a cause, a single geometric knob in place of six parameters and a missing particle, a mechanism stitched from real and respectable physics, and—crucially—a set of predictions sharp enough to be wrong. What he does not have is confirmation. The mainstream overwhelmingly favors particle dark matter and ΛCDM, for good and well-earned reasons; the evidence for invisible matter is broad and cross-checked, and MOND-family theories have stumbled on clusters and lensing for decades. This is one independent researcher's proposal, not peer-reviewed orthodoxy, and it should be read as exactly that.

But the test is not a thought experiment scheduled for some hazy future. The telescopes are already operating. The data releases have dates. Somewhere between now and roughly 2032, the universe is going to render a verdict on whether the galaxy-rotation number breathes with the dark energy that is tearing space apart—or whether it sits there, flat and indifferent, and Carl Zimmerman's beautiful single line goes quietly into the archive of ideas that were elegant and wrong.

He seems to find that prospect less frightening than most people would. He built the thing to be killable. The only failure he appears to fear is the one that can't be tested at all.

The snail keeps accelerating. The telescopes keep watching. And for once, we won't have to wait fifty more years to find out.
