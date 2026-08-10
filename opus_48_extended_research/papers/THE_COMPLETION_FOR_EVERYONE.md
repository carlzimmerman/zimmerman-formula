# The Completion, For Everyone

**The whole theory in plain words: one number from the edge of the universe, and the field theory built to carry it**

Zimmerman, Carl P. — Briar Creek Tech

Version 1, 2026-08-09.

*This is the plain-language companion to a technical paper called **The Completion** (DOI
10.5281/zenodo.21863521). Nothing in this document is new. Every claim here is the readable version
of a claim made precisely there, and every load-bearing number traces back to a named computer
script, committed to a public repository, that re-derives the number from scratch and refuses to
run — exits with an error — if the number stops being true. Where this document simplifies, the
technical paper governs.*

---

## 1. The whole story in one page

Galaxies do not spin the way gravity says they should. The stars at their outer edges move far too
fast for the visible matter to hold them, and they have been doing so in every galaxy we have ever
measured, for fifty years of measurements. Physics has two standard explanations. The first says
there is invisible extra matter — *dark matter* — five times more of it than everything we can see,
made of a particle nobody has ever detected. The second, called MOND, says there is no extra matter:
gravity itself works differently when it gets extremely weak, below a particular threshold
acceleration called **a₀** — a threshold about one hundred-billionth of the pull you feel standing
on Earth.

MOND's threshold number was always measured from galaxy data and never explained. This program
starts from an observation about that number: **it is almost exactly what you get by combining the
speed of light with the density of dark energy** — the mysterious ingredient that is pushing the
universe's expansion to speed up. Written as a formula: a₀ = κ·c·√(G·ρ_Λ), where c is the speed of
light, G is Newton's gravitational constant, ρ_Λ is the dark-energy density, and κ is a plain number
close to one-half. In other words: **the threshold where galaxies stop obeying Newton appears to be
set by the same ingredient that dominates the universe as a whole.** Either that is a coincidence,
or it is a clue about what gravity actually is.

A clue is not a theory. A one-line formula cannot tell you how light bends, what the early universe
looked like, or whether the idea even makes internal sense. For that you need a *field theory* — the
full mathematical machine, the same kind of object Einstein's general relativity is. This document
describes that machine: what it is made of, what it gets right, what it costs, how it was
stress-tested, and — most importantly — **exactly what is and is not being claimed**, including the
things that were claimed earlier in this program, turned out to be wrong, and were publicly
withdrawn.

The short version of the result: the machine exists, it is written down in one box, and it has
passed every safety and consistency test run on it so far — with two flags still open and several
named tests still owed (Sections 11 and 15). It reproduces galaxies, the bending of light, the
detailed pattern of the universe's oldest light, and the solar system, and it contains a live —
explicitly unconfirmed — candidate mechanism for galaxy clusters, the one place this kind of theory
has always struggled — and one sharp open problem: whether the field's own cosmic dust stays out of
galaxy interiors, where the rotation-curve data leave no room for it (Section 9). It does this with
five dark-sector numbers where the standard picture uses two, so it is not a simpler theory; its
claim is different: that dark energy, the dark matter phenomenon, and the galaxy-scale anomaly are
**three faces of one field** rather than three separate mysteries. And it makes predictions sharp
enough to kill it.

That is the story. The rest of this document earns it.

---

## 2. The problem: galaxies spin wrong

Take the solar system. Mercury, close to the Sun, orbits fast; Neptune, far out, orbits slowly.
That falloff is Newton's law doing its job: gravity weakens with distance, so distant things orbit
lazily. Every planet obeys it to exquisite precision.

Now zoom out to a spiral galaxy — a hundred billion stars in a disk. The same rule should apply:
stars near the bright center should orbit fast, stars at the dim outskirts slowly. Astronomers
first checked this properly in the 1970s, and the answer has been replicated thousands of times
since: **the outer stars do not slow down.** The orbital speed rises from the center and then goes
flat, staying flat as far out as anyone can measure — often far beyond the last visible star, traced
by cold hydrogen gas that radio telescopes can see. If Newton's law and the visible matter were the
whole story, those outer stars would be flung off into space. They are not.

Something is wrong with either the matter inventory or the law.

**Option one — more matter.** Wrap every galaxy in a huge invisible halo of new particles that feel
gravity but do not emit light, and the fast outer orbits are explained: the stars are responding to
mass we cannot see. This is dark matter, and it grew into the backbone of modern cosmology. In the
standard model of the universe, called ΛCDM (Λ is the symbol for dark energy, CDM stands for cold
dark matter), about 27% of the universe is this cold dark matter, about 68% is dark energy, and
everything we have ever seen — stars, planets, gas, people — is the remaining 5%.

**Option two — a different law.** In 1983 the physicist Mordehai Milgrom noticed something the halo
picture has never explained naturally: the anomaly does not switch on at a particular *distance* or
a particular *mass*, but at a particular *acceleration*. Wherever gravity's pull drops below about
10⁻¹⁰ meters per second per second — one part in a hundred billion of Earth's surface gravity —
the anomaly appears, in every galaxy, big or small, dense or diffuse. Above that threshold, Newton
holds. Below it, the effective pull is stronger than Newton predicts, in a specific mathematical
way. Milgrom called the idea MOND (MOdified Newtonian Dynamics), and the threshold acceleration a₀.

Here is why option two refuses to die, forty years on. If you plot, for thousands of measured points
in hundreds of galaxies, the gravity you *observe* against the gravity the *visible matter alone*
would produce, the points collapse onto a single tight curve — the same curve for every galaxy. This
plot is called the **radial acceleration relation**, and it is one of the tightest empirical laws in
extragalactic astronomy. In the halo picture there is no obvious reason a messy, history-dependent
process — every galaxy with its own accidents of formation, collision, and gas flow — should conspire
to put every galaxy on one universal curve keyed to one universal acceleration. In MOND, that curve
*is the law*, so its universality is automatic.

And yet MOND, as Milgrom wrote it, has two famous holes. It is a rule for slow-moving matter only —
it says nothing about light, or the early universe, or the cosmos as a whole. And it under-predicts
the mass of galaxy *clusters*, the largest bound structures in the universe: even with MOND's boost,
clusters come up short by roughly a factor of two, so MOND traditionally needs some dark matter
after all, exactly where its slogan says there should be none.

Both camps, then, live with an embarrassment. The dark-matter camp cannot explain why galaxies obey
one universal acceleration law. The modified-gravity camp cannot cover clusters or cosmology. This
program is an attempt to build the theory that has neither embarrassment — anchored to one specific
idea about where a₀ comes from.

---

## 3. The coincidence at the center of everything

Milgrom himself noticed, already in 1983, that his measured threshold a₀ is numerically close to
quantities built from the universe's expansion rate. In modern terms, the sharpest version goes
through dark energy.

Dark energy is the ingredient, discovered through supernova surveys in 1998, that makes the
universe's expansion accelerate. Its density, ρ_Λ, is measured. Take that density, combine it with
Newton's constant G and the speed of light c — the only combination with the units of an
acceleration is c·√(G·ρ_Λ) — and you get a number in the same neighborhood as the measured a₀. The
relation this program is built on is:

**a₀ = κ · c · √(G · ρ_Λ)**, with κ a pure number, measured from galaxy data to be **0.551 ± 0.043**
— consistent with exactly one-half.

An equivalent way to write the same statement: a₀ = c·H_Λ / Z, where H_Λ is the expansion rate the
universe is heading toward as dark energy takes over completely, and Z = 2√(8π/3) ≈ 5.79. Both forms
are the same claim wearing different clothes. Numerically, the canonical value used throughout this
program is a₀ = 9.36 × 10⁻¹¹ m/s². (Readers comparing with the MOND literature will see a₀ quoted
there as about 1.2 × 10⁻¹⁰ — a fitted value roughly 28% higher. The two sit well within the spread
of published a₀ measurements, and which one the data actually prefer is one of the measurement
questions this program works on; Section 13 returns to it.)

Two honesty notes, immediately, because this is where a program like this can start lying to itself.

**First: the *form* of the relation is forced; the *number* κ is not.** There is a small uniqueness
theorem in the technical corpus: if a₀ is built from G, c, and a density, the combination c·√(G·ρ)
is the *only* one dimensionally possible — the arithmetic of matching units has exactly one
solution. So the shape of the formula is mathematics. But the pure number κ in front is **measured,
not derived**. Years of attempts to derive κ = ½ from first principles are documented in this
program's repository, and every one failed or turned out to be circular — a fact the technical
papers state in bold type. The measured value 0.551 ± 0.043 is consistent with ½, but it is also
consistent with 1/√3 and other simple candidates. The honest statement is "κ is measured, and ½ sits
comfortably inside the error bar" — nothing stronger. Section 15 returns to this.

**Second: a coincidence of numbers is cheap; the question is what follows.** Plenty of numerical
coincidences in physics turned out to mean nothing. The only way to find out whether this one means
something is to take it seriously as a foundation, build the full theory that carries it, and let
that theory make predictions that can fail. That is what "the Completion" means: not a new slogan,
but the completed machine.

Why might dark energy plausibly set a galaxy-scale threshold at all? Here is the intuition, offered
as intuition only. Dark energy gives the universe a *horizon* — a farthest distance from which light
can ever reach us, because beyond it, accelerating expansion carries space away too fast. A horizon
is not nothing: in modern physics horizons carry temperature and entropy, as Hawking and others
showed for black holes. And there is a curious fact about gentle acceleration: the more gently a
body accelerates, the larger the region of spacetime that matters to its motion — until, below
roughly c times the horizon's expansion rate, that region grows as large as the horizon itself. It
is not absurd that dynamics should change there; the threshold acceleration at which a falling body
starts to "feel the edge of the universe" is, up to a pure number, exactly c·√(G·ρ_Λ). The technical
corpus contains a derivation in this spirit that produces the precise *shape* of MOND's transition
function — the mathematical bridge describing how gravity crosses over from Newton above a₀ to the
modified law below it (it turns out to reproduce, exactly, a formula Milgrom published in 1999) —
while *failing* to produce the measured coefficient, predicting one about twelve times too large,
which the galaxy data rule out at 15.6 sigma. That split result — the shape derivable, the
coefficient stubbornly not — is one of the cleanest honest findings of the whole program, and it is
why κ is treated as a measured quantity.

---

## 4. Why a formula is not enough: what a field theory is

Everything so far could be written on an index card. Why do the technical papers run to hundreds of
pages of derivations and scripts?

Because an index card cannot answer questions like these:

- **How does light bend?** MOND's rule covers slow-moving matter. Light is not slow. Galaxies and
  clusters bend light measurably (gravitational lensing), and any theory that gets lensing wrong is
  dead on arrival. An earlier arm of this very program — a version where the modification lived in
  the *inertia* of matter rather than in gravity — was killed by exactly this test: it predicted
  that the mass a galaxy shows through lensing should differ from the mass it shows through orbits
  by a factor of about six, and observation says the two agree. That arm was excluded at 21 sigma —
  a statistical death sentence — and the program said so publicly and moved to the arm this document
  describes. Theories are supposed to be killable. That one was killed.
- **What happened in the early universe?** The cosmic microwave background (the CMB) — the
  universe's oldest light, released 380,000 years after the Big Bang — carries a pattern of hot and
  cold spots whose detailed statistics are measured to a fraction of a percent. The standard model
  fits that pattern using cold dark matter. Any replacement theory must reproduce it or die.
- **Is the theory even self-consistent?** Field theories can hide fatal diseases — "ghosts,"
  instabilities, faster-than-light signals. A formula cannot be checked for these; a full theory can
  and must be. Section 11 is entirely about this.

A *field theory* answers such questions because it specifies everything, everywhere. A field is a
quantity with a value at every point of space and time — the temperature map on a weather chart is a
field; so is the electromagnetic field carrying this document to your screen. Einstein's general
relativity is a field theory in which the field is the geometry of spacetime itself. To complete
this program, one must write down the *action* — the single master expression from which, by a
standard mathematical procedure (the same handle Einstein's theory turns), every equation of motion
for every situation follows. Once the action is fixed, there is no more room to make things up: the
theory says what it says in every regime, and either survives the data or does not.

**The action of this theory fits in one box.** Here it is, described in words; the technical paper
gives the symbols. Spacetime geometry appears exactly as in Einstein's theory. Matter — stars, gas,
light, you — appears exactly as in Einstein's theory, and couples to geometry exactly as in
Einstein's theory (this single choice is why light-bending comes out right, as Section 7 explains).
To this, add **two new fields and one function**, described next.

---

## 5. The machine: three fields, one new function

The theory is called **AeST** — Aether-Scalar-Tensor — a framework published in 2021 by Constantinos
Skordis and Tom Złośnik, who proved something remarkable: theirs is the only known relativistic
MOND-type theory able to reproduce the cosmic microwave background. Honesty first, as always: **the
AeST framework is theirs, not this program's.** What is this program's own is the *choice of the
free function* inside it — the part Skordis and Złośnik deliberately left open — plus the coefficient
that anchors it to dark energy, and the theorems and mechanisms of Sections 8–11. Think of AeST as
an engine block that its designers shipped with the fuel map unspecified — the fuel map being the
table that tells an engine exactly how much fuel to deliver in every condition. This program's claim
is a particular fuel map, and everything that follows from it.

The three ingredients:

**The metric (the "tensor").** Spacetime geometry, exactly as in general relativity. Nothing
modified here.

**The aether (the vector field, written A^μ).** Despite the antique name, this is a modern, precise
object: at every point of spacetime, an arrow of fixed unit length pointing into the future. A field
of compass needles for time, defining at each point a natural notion of "at rest." Einstein's
relativity famously abolished any *built-in* preferred rest frame; here one returns, but as a
dynamical field with its own equations — free to tilt and respond — rather than as rigid scaffolding.
This is a real conceptual price. Some of the observational tests it raises are passed cleanly —
light-bending and the speed of gravitational waves, as Sections 7 and 11 explain; the precision
"preferred-frame" tests from the solar system and pulsars have not yet been computed for this
theory, as Section 15 discloses.

**The khronon (the scalar field, written φ).** A single number at every point — from the Greek
*chronos*, time, because it behaves like a universal clock-reading field. This field is the workhorse
of the theory: its behavior in different environments *is* dark energy, *is* the dark-matter
phenomenon, *is* the MOND effect, depending on where you look.

From the aether and the khronon's rate of change, the theory builds two basic quantities: one
(called Q) measuring how fast the khronon ticks along the time direction, and one (called Y)
measuring how steeply it varies across space. The entire content of the theory — everything this
program claims as its own — is one function 𝓕(Y, Q) telling spacetime how much energy the khronon's
configuration carries. That function is the fuel map. It has three pieces, and each piece is one of
the theory's three jobs:

```
𝓕  =  (galaxy piece — depends on Y)          ← the MOND kernel, Section 6
    + (cosmology piece — depends on Q)        ← dark energy and the cosmic dust, Section 8
    + (cluster piece — couples Y and Q)       ← the environment response, Section 10
```

(The technical paper writes the third piece as A·B(Y/a₀²)·(Q−Q₀)², where Q₀ is the khronon's natural
resting ticking rate, B is a bell-shaped curve, and A is an amplitude — all of it Section 10's
subject.) Sections 6, 8, and 10 take the three pieces in turn. Section 7 explains why light behaves.
Section 9 answers the question every reader of this program eventually asks — *so is there dark
matter in this theory or not?* — with the exact, honest answer.

---

## 6. Job one: galaxies — the MOND kernel

The first piece of the function depends only on Y — on how steeply the khronon varies across space —
and it is built to do exactly one thing: reproduce, in the regime of galaxies, the framework's own
MOND-type law with the dark-energy-anchored a₀ in it.

The specific transition curve the program uses — its *kernel*, this program's word for the chosen
interpolation between the Newtonian and modified regimes, fixed in advance and registered (more on
registration in Section 13) — has three properties worth stating in words:

- **Above the threshold, Newton — overwhelmingly.** Where gravity is strong compared to a₀, the
  correction dies off *exponentially*. At Earth's orbit around the Sun, the predicted deviation
  carries a suppression factor of about 10⁻³⁴⁵⁷ — a decimal point followed by three and a half
  thousand zeros. The theory does not "approximately" recover the solar system; it recovers it with
  astronomical overkill. Planetary position tables (ephemerides), spacecraft tracking, lunar laser
  ranging: untouched.
- **Below the threshold, the boost** — precisely the behavior that makes rotation curves flat and
  gives galaxies the observed tight relation between visible mass and rotation speed (the baryonic
  Tully–Fisher relation), which in this theory is a theorem, not a fit.
- **In between, one smooth curve** — and this is where the theory faces its most granular test.

That test is the radial acceleration relation of Section 2: thousands of measured points from the
SPARC sample of 175 galaxies, each point a direct comparison of observed gravity against
visible-matter gravity. Fit with the dark-energy-anchored a₀, the scatter of the data around the
predicted curve is **0.108 dex** — dex is the astronomers' unit of "factors of ten," and 0.108 dex
means the typical point sits within about 28% of the curve, over data spanning factors of
thousands — at a stellar mass-to-light ratio of 0.70, comfortably inside the range stellar
population models allow. (Two fine-print notes, for the reader who checks: that fit uses the
framework's original transition curve, whose difference from the completion's kernel is smaller
everywhere than the scatter itself; and the RAR *alone* cannot pick between the anchored a₀ and
the traditional fitted value — the mass-to-light ratio can absorb the difference. The honest
statement is not "anchoring fits better" but "anchoring costs nothing": tying a₀ to an
independently measured cosmological number, instead of fitting it to the very galaxies being
explained, gives an equally good account of the data.)

One more galaxy-scale number, because later sections lean on it: the theory's third term (the
cluster mechanism of Section 10) also technically operates inside galaxies, so one must check it
does not spoil this agreement. It contributes 0.034% of a typical galaxy's visible mass in the
interior — shifting the radial acceleration relation by 0.0004 dex, roughly 270 times smaller than
the observed scatter. Galaxies do not notice it.

---

## 7. Light: the test that kills theories like this

Gravitational lensing deserves its own short section, because it is the single most efficient
executioner of modified-gravity theories — it personally killed the previous arm of this program —
and because the way this theory passes is clean enough to state exactly.

When light from a distant galaxy passes a massive object, its path bends; astronomers measure the
mass of the deflector from the bending. Separately, they can measure the same object's mass from
the orbits of things moving around or within it. In general relativity plus dark matter, both
measurements see the same total mass, so they agree — and observationally, **they do agree**, across
galaxies and clusters. Any theory in which the "orbit mass" and the "lensing mass" differ is dead.

In this theory they agree *identically*, for a structural reason. The khronon and aether do their
work by shaping the same spacetime geometry that matter and light both respond to; light couples to
that geometry exactly as in Einstein's theory, with nothing extra. In the technical language, the
two gravitational potentials that govern slow matter and light are forced equal — the
parametrized-post-Newtonian parameter γ equals 1 exactly — so whatever total gravity the theory
produces, orbits and lensing see the same thing, automatically. The 21-sigma execution that ended
the modified-inertia arm becomes, in this arm, a 0.6-sigma pass — statistical agreement.

The physical picture is worth one sentence: in this theory the dark field genuinely *gravitates* —
it is a real source of spacetime curvature where it accumulates — rather than being a bookkeeping
correction to matter's response, and that is precisely why light cannot tell the difference between
this universe and a dark-matter one at the lensing level.

---

## 8. Job two: the universe — dark energy and "dust" from one function

The second piece of the function, K(Q), depends only on how fast the khronon ticks. It has to
manage the entire cosmological side of the ledger, and it does three jobs with three features of one
curve.

**Feature one: the floor.** The function K has a constant offset: a fixed energy floor of exactly
the dark-energy density. A constant energy density filling space, unchanging as the universe
expands, pushing outward with a pressure exactly equal and opposite to its energy density (the
relation cosmologists write as w = −1): that *is* dark energy, by definition. In this theory it is
not added as a separate ingredient; it is the resting value of the khronon's own energy function —
the value the field's energy takes when it sits at its natural minimum. At that minimum, w = −1
holds *exactly*, proved, not tuned.

**Feature two: the wiggle.** Displace the khronon's ticking rate slightly off its natural value and
the energy rises — and, crucially, this excitation energy *dilutes as the universe expands exactly
the way ordinary matter does*, with zero pressure. Cosmologists call anything with that behavior
"dust." The universe's dark matter, as far as cosmological measurements are concerned, is dust —
and here, the dust is not a substance added to the theory: it is the *same field*, slightly
excited. How much excitation the universe carries is set by initial conditions (one number, playing
the role ΛCDM's dark-matter density plays), and Section 9 is honest about what that does and does
not buy.

**Feature three: the cap — and the theorem.** The obvious, simplest choice for K — a plain
parabola, energy rising as the square of the displacement — was already studied by others, including
by Skordis's own collaborators, and in 2024 Blanchet and Skordis published what amounted to a no-go:
with the parabola, matching cosmology and matching galaxies impose requirements on one of the
theory's mass scales that conflict by a factor of 455. The natural conclusion was that this class of
theories cannot do both jobs. This program's response was first to prove a small theorem: for *any*
power-law K — quadratic, quartic, sextic, anything — the early universe comes out wrong in a
specific calculable way. As you run the universe backward and the khronon's displacement grows, a
power-law energy function makes the field's pressure blow up: the early cosmos fills with a stiff,
honey-like medium that is flatly ruled out by the observed abundances of the lightest elements
(hydrogen, helium) forged in the universe's first minutes, and by the microwave background. The
exponent only changes how badly. **No power law can work. What works is boundedness**: give the
energy function a hard cap — a maximum displacement it can never exceed, approached with a
square-root shape exactly like the one special relativity uses to cap velocities at the speed of
light (the technical name is a DBI form, borrowed from string theory's toolbox). With the cap in
place, run the universe backward and the pressure stays finite; the early-time behavior turns back
into harmless dust. And the 455× conflict does not merely shrink: the two requirements stop
conflicting and start pointing the same way, with a 226-fold margin to spare. The published no-go,
under this program's choice of function, dissolves.

**The receipt.** Words like these are cheap; the test is numerical. The theory was run through
CLASS — one of the two standard precision codes every working cosmologist uses to compute the
microwave background — with the capped K in place. Result: the acoustic peak pattern of the CMB
agrees with the standard model's to **0.069%**, far inside measurement error, and the matter
distribution at the representative measured scale to 1.7%. On the universe's oldest light, this
theory and ΛCDM are indistinguishable. Two disclosed caveats accompany that pass, and Sections 11
and 15 state them (they concern the *later* growth history, verified only in part, and a parameter
window tightened by the health checks of Section 11 — tightened, notably, by this program's own
hand against its own earlier choice).

---

## 9. So is there dark matter in this theory or not?

This question deserves a section with no hedging, because it is the question, and because the
answer's honesty is the program's credibility.

Start with what "dark matter exists" actually asserts: that the universe's inventory contains an
undiscovered *substance* — a new species of particle, sitting in halos, waiting in the dark. That is
the picture the words smuggle in, and the picture direct-detection experiments have spent forty
years failing to confirm.

In this theory that picture is replaced, not merely relabeled. ΛCDM adds two unrelated dark
ingredients to the universe: a constant (dark energy) and a material (cold dark matter, a particle
species). This theory adds no new species of matter. It adds one dynamical field — the khronon, with
its aether companion — and that single field's three behaviors *are* the three dark phenomena: its
resting energy is dark energy, its gentle excitation does the cosmological job dark matter was
invented for, and its spatial response is the MOND law.

Now the exact statements, each with its precise status:

**There is no dark matter particle.** Nothing in this theory is a new species of matter. No WIMP, no
axion, nothing for an underground detector to catch or a collider to make. Four decades of null
results are, in this theory, exactly what should have been found: there is nothing of that kind to
find.

**The CMB never detected a substance in the first place.** A theorem in this program's corpus makes
this precise: the microwave background constrains a *behavior*, not an identity. It demands
something that gravitates, exerts no pressure, and dilutes like matter — and it cannot distinguish,
even in principle, whether that something is a particle fluid or a field excitation: the two differ
by exactly zero sigma in the CMB's eyes. "Dark matter," in cosmology, is a job description, not an
identified employee. ΛCDM fills the job with a hypothetical particle. This theory fills it with the
field that is already on the payroll for dark energy and MOND. The job itself is real and
non-negotiable: delete the pressureless component and the ratio of the CMB's third to first acoustic
peak shifts by 54%, a catastrophe no refitting of other parameters can absorb. So the flat sentence
"there is no dark matter" is not available to this theory or to any theory that matches the CMB, and
this document will not use it.

**And in galaxies — the honest status is: open, and sharply posed.** The galaxy data themselves are
unambiguous: rotation curves are fit by visible matter plus the modified law alone, to 0.108 dex,
with no dark contribution needed or wanted. For the theory to be right, then, its own cosmic dust —
the field excitation of Section 8, which certainly exists at cosmological scales — must largely
*stay out* of the inner regions of galaxies where those curves are measured. Does it? This program
had a mechanism that guaranteed it, and killed that mechanism itself this week (Section 10 tells the
story). What remains are two computable branches: in one, the settled field inside a galaxy's halo
relaxes to a flat, centrally-evacuated profile — a configuration this theory's own equations prefer
in equilibrium — and galaxies are safe by orders of magnitude; in the other, the dust piles up the
way cold particles would, and the theory *overshoots* its own best data. Which branch nature's
version of this theory takes is a hard nonlinear calculation — the kind nobody, in any group, has
yet performed for this class of theory — and it is now the sharpest open problem on the program's
list, stated in Section 15 and scheduled as the next calculation.

So the defensible summary — the one this program will defend in any referee report — is:

> **Dark matter is not a thing in this theory: no particle, no new substance — one field doing three
> jobs. The cosmological job that ΛCDM assigns to a particle is done here by the same field that
> supplies dark energy and the galaxy law. Whether that field's dust stays out of galaxy interiors,
> as the data demand, is the theory's sharpest open problem — with both branches computable and the
> calculation scheduled.**

Whether nature agrees is Section 13's business.

---

## 10. Job three: clusters — the thorn, the failures, and the live candidate

Galaxy clusters — swarms of hundreds of galaxies in halos of hot gas, the largest bound objects in
existence — have been MOND's thorn for forty years, and this program spent its hardest weeks on
them. This section tells the story as it happened, including the dead bodies, because the dead
bodies are why the surviving candidate deserves attention.

**The problem.** Even with MOND's boost, clusters come up short: the gravity needed to hold the hot
gas and the galaxies exceeds what the visible matter plus the modified law can produce, by around a
factor of two. Milgrom's rule, which clears every galaxy, hits a wall at the next scale up.

**The failures, in the open.** This program tried, and killed, three mechanisms in sequence — each
kill executed by the program's own scripts, each published, each now on a formal do-not-cite list:

1. *A geometric lever* based on how the field's response scales with the size of the system. Killed:
   its required mass scale conflicts with independent galaxy-lensing bounds published by Mistele,
   McGaugh and Hossenfelder — it satisfies neither of the two bounds it needed to.
2. *A primordial route*: clusters sit where the early universe was clumpiest — perhaps the dark
   field remembers that. Killed three independent ways, the third decisive: a smoothness theorem.
   Any suppression mechanism of the proposed kind removes *fluctuations*, not the *mean*, and a
   collapsing region captures all the cold material in its basin regardless — so the proposed
   difference between clusters and galaxies provably cannot arise from initial conditions of that
   class. The route's own published write-up was amended to say so. (This kill is also what reopened
   the galaxy question of Section 9: the same theorem says the field's dust falls into *every*
   collapsing basin, galaxies included, unless the settled field arranges itself away from their
   centers — the open calculation described there.)
3. *A potential-depth response*: let the field respond to how deep a gravitational well it sits in —
   clusters are the deepest wells, so target them by depth. Killed by a scale-freeness check the
   program's own specification had missed: gravitational potentials in the cosmos are nearly the
   same depth everywhere on large scales (about one part in a hundred thousand), so a response steep
   enough to single out clusters floods the whole universe with twenty times too much energy. Written
   down, checked, dead within a day.

**The survivor.** The third failure taught the lesson that built the candidate. Depth alone cannot
select clusters; scale alone cannot either (the second failure); but there is one property clusters
uniquely combine. Recall a₀, the threshold acceleration. Galaxy interiors sit *above* it; the cosmic
web at large sits *far below* it; but the bodies of galaxy clusters — at the radius where their
masses are actually measured — sit at 0.33 to 0.58 times a₀. **Clusters are the cosmic objects that
live at the MOND transition itself.** They are the unique environments that are simultaneously deep
and *at the threshold*.

So the third piece of the function is a *resonance at the transition*. It couples the khronon's
ticking to its spatial variation through a bell-shaped profile B that peaks exactly where local
gravity equals a₀ and dies off on both sides. Like a wine glass that answers only to its own note,
the dark sector's extra response answers only to environments near a₀ — which is to say, clusters.
The elegance one should insist on: **the location of the peak costs nothing.** The theory's
Y-variable is already naturally measured in units of a₀² — the peak position is inherited from the
framework's central number, not tuned. What is genuinely new and fitted is one amplitude, called A,
calibrated so clusters get their missing gravity.

Any such mechanism must then survive everywhere else, and this one was marched through five
environments: **clusters** (calibration — that one is free); **galaxy interiors** (contributes
0.034% of the visible mass; the radial acceleration relation moves by 0.0004 dex — unnoticeable);
**galaxy outskirts** at about three million light-years (1.2% extra effective mass, versus a
measured lensing tolerance of 5.9% — inside bounds by a factor of about five); **the smooth
universe** (0.6% of the mean matter density — harmless, and the term vanishes identically in exact
cosmological symmetry, so the CMB results of Section 8 are untouched *by construction*); **the solar
system** (a correction of order 10⁻¹⁹ — nineteen zeros — of nothing).

And it evades both earlier executioners by design: it is a *response*, not a transported substance,
so the smoothness theorem does not apply (nothing is being carried in from the early universe); and
it couples to the environment directly, so it needs no primordial selection.

**Status, stated coldly: a candidate, not a result.** It has passed the environment matrix above, a
dedicated stability audit, and — as of this document's date — the full perturbation analysis of
Section 11. But it has not been fit to real cluster mass profiles at all — by this program or
anyone; the amplitude is calibrated on a single summary number, and a real cluster model is owed.
Its amplitude also sits in tension with a separate published cluster analysis by Mistele and
collaborators (not the lensing bounds of failure 1) at that analysis's demanding end — Section 11
turns exactly this into a kill test. And this program has been wrong about clusters three times
this month. The reader should hold it accordingly. But it is the first cluster mechanism this
program has produced that *survived its own execution squad* — and its slogan states a genuinely new
idea, whatever its fate: *the dark sector's response is resonant at the MOND transition, and
clusters are the objects that live at a₀.*

---

## 11. Could the whole thing be sick? The safety inspection

A field theory can fit every observation and still be fatally diseased. This section explains the
diseases, in plain terms, and reports the inspection — because "we checked whether our own theory is
sick, using tests that could have killed it" is precisely what separates a theory from a wish. All
of this is recent work: an isolated-term health check first, then the full analysis with every
interaction included, completed the day of this document.

**Ghosts.** The gravest disease. A "ghost" is a field configuration carrying *negative* kinetic
energy. If a theory has one, the vacuum itself is unstable: empty space can spontaneously erupt into
pairs of positive- and negative-energy excitations, endlessly, everywhere — the theory predicts that
the universe should instantly self-destruct, which is a strong prediction and a wrong one.
Historically, ghost diseases have killed more modified-gravity proposals than any observation has.
The base AeST framework was proven healthy by its authors. The question was whether this program's
additions — above all the new cluster term — poison it. The answer is a theorem: the cluster term's
contribution to the theory's kinetic structure is *provably incapable of subtraction* — it can add
stability but never remove it, in any environment, for any field values. Healthy plus non-negative
is healthy. **The bump cannot create a ghost — ever.** Proved symbolically in closed form, then
verified numerically on two hundred randomized configurations.

**The speed of gravitational waves.** In 2017, two neutron stars collided 130 million light-years
away. The ripple in spacetime and the flash of light arrived within two seconds of each other —
after 130 million years in transit. Gravitational waves therefore travel at the speed of light to
about one part in a quadrillion, and that single measurement annihilated whole families of
modified-gravity theories the week it was announced. In this theory, the new terms touch the
relevant part of the geometry only algebraically — not through the derivatives that set a wave's
speed — and the wave speed works out to exactly the speed of light: not approximately,
*identically*, as a structural fact. **This theory could not have failed the 2017 test even in
principle.**

**Gradient stability, and a bound with teeth.** Beyond ghosts there are subtler instabilities, where
small spatial ripples of the field amplify instead of oscillating. Here the inspection *bit*, twice
— and the bites are the best evidence of its sincerity. First: on the smooth cosmological
background, health of the cluster term demands that the cap parameter of Section 8 be small —
quantitatively, at most about 10⁻⁶ in the theory's own units — which *overrules a value this program
itself had previously used* (10⁻²). The theory's own consistency disciplined its author; the allowed
window remains 3.7 orders of magnitude wide, and nothing previously verified is disturbed, but the
old fiducial number is dead, by the program's own hand. Second: inside cluster-like environments,
the stability analysis caps the cluster term's amplitude A from above. With every field interaction
included, the cap lands between roughly 2.7 and 7.4 times the calibrated value (the residual range
awaits one coefficient from Skordis and Złośnik's published supplemental material — a literature
lookup, not a new calculation). Meanwhile the separate cluster analysis by Mistele and collaborators
mentioned in Section 10 would demand, at its far end, an amplitude 34 times the calibrated value.
**Stability forbids that end outright** — it exceeds the cap several times over — while the near end
of the same analysis, 4 times calibrated, sits at the boundary: alive or dead by a coefficient. The
theory is thus *pinched from two sides*: observation demands the amplitude be big enough, internal
health forbids it from being too big, and the window between is narrow and closing. A theory that
arranges its own execution window is doing falsifiability properly.

**Loose ends, disclosed.** Two flags remain open and are stated wherever the results are: a
possible mild instability in the aether (vector) sector deep inside galaxies — suppressed by a small
coupling, flagged for a dedicated analysis rather than resolved; and one known curiosity of the
base AeST framework (a formal unboundedness below a certain wavelength, known to its authors) which,
at this program's parameter values, migrates to the scale of the entire observable universe — an
amusing and possibly meaningful relocation, noted, not celebrated.

The inspection's summary: **no ghosts, by theorem; gravitational waves exactly at light speed, by
construction; stability bounds that bite the theory's own parameters, accepted and published; two
flags open and labeled.**

---

## 12. What it costs: the price tag, read aloud

No honest sales pitch omits the invoice.

**Parameters.** ΛCDM's dark sector runs on two numbers: how much dark energy, how much dark matter.
This theory runs on five: the vacuum scale (dark energy's density), the amount of khronon
excitation (the dust's abundance — an initial condition, not explained), the field's mass scale, the
cap scale of Section 8, and the cluster amplitude of Section 10. Five against two. **This is not a
simpler theory, and this document will not pretend otherwise.** What is bought for the extra three:
one function replaces three unrelated sectors; the galaxy-scale acceleration a₀ is not an
*additional* dial on top of those five — it is re-expressed through the field's own condensate mass,
a re-expression that checks out arithmetically to 0.076% but is a relabelling, not an independent
derivation (Section 15, item 1); and the theory acquires kill-tests that ΛCDM, with its flexibility,
does not offer.

**A preferred frame.** The aether restores a dynamical version of the notion of absolute rest that
special relativity abolished. The observational cost is confined by the same structure that saves
lensing, but precision solar-system and pulsar bounds on preferred-frame effects exist, and Section
15 lists what has not yet been computed against them.

**An inherited tension.** The Cassini spacecraft's radio-link measurements constrain one
post-Newtonian quantity at a level in 3-to-15-sigma tension with this class of kernels. Inherited,
disclosed, unresolved. It sits on the worry list, neither hidden nor fatal at current precision of
the theory-side calculation.

**Things given up.** Earlier arms of this program claimed more: a derivation of a₀'s coefficient
from first principles (failed — κ is measured); a laboratory-testable modified-inertia effect (that
arm is dead); a theory-of-everything ambition (publicly retracted in June 2026, and the retraction
stands — Section 15). The surviving theory is narrower than the program's earliest hopes, and better
for it.

---

## 13. How it dies: the predictions

A theory is only as good as the experiments that could kill it. This one maintains a registered
kill-list. The word "registered" is doing real work in that sentence: the galaxy-survey predictions
below were *frozen before the data arrive* — written into a public preregistration document whose
cryptographic hash (a digital fingerprint that changes if a single character is edited) is committed
publicly, so the targets cannot be quietly moved after the fact. Nine amendments to that document
exist; each is itself hash-stamped; the analysis pipeline is committed alongside. When the data
land, the confrontation is automatic and the escape hatches are welded shut.

**One: wide binary stars (the sharpest, and it is imminent).** Pairs of stars orbiting each other at
great separations — thousands of times the Earth–Sun distance — have mutual gravity right at a₀.
They are the cleanest MOND laboratory in the sky, free of the messy gas dynamics of galaxies. The
European Gaia satellite's fourth data release will provide orbital statistics for enormous numbers
of them. This theory's registered prediction: orbital velocities boosted over Newton by a factor of
1.2139. (A stated alternative, 1.2592, corresponds to the other of two defensible conventions for
anchoring the dark-energy density — both were frozen in the registration, so a result matching
neither kills the theory regardless of convention.) The dead modified-inertia arm predicted 1.1582 —
separated from the live target at about 2.7 sigma by the survey's expected precision: enough for
DR4 to distinguish the arms. The numbers are frozen in public, by design.

**Two: a directional signature (already flickering).** Because the aether picks out a frame and the
external galactic field matters in this theory (the "external field effect," a MOND signature with
no ΛCDM counterpart), binaries oriented differently with respect to the galaxy should behave
measurably differently, at the 1-to-4% level, with a definite sign. The dead arm predicted exactly
zero such effect. A first statistical test on existing data gives a positive signal with the
predicted sign at p = 0.029 — suggestive, not decisive (about one-in-thirty odds of arising by
chance, and one such firing is not a discovery). It is listed because it was predicted *before* it
was seen, and DR4 will settle it.

**Three: clusters, from three sides (the candidate's own gallows).** The Section 10 mechanism must
produce anisotropic stress in clusters — a specific mismatch, of order tens of percent, between
cluster masses inferred from lensing and from hot-gas pressure profiles. Both measurement types
exist and are improving; a dedicated confrontation is a data-analysis project, not a new theory. The
mechanism also predicts *cluster-to-cluster variety* in the dark residual — different clusters sit
at different distances from the a₀ resonance — where mechanisms tied to a fixed geometric scale
predict uniformity; existing cluster samples can already test this. And the amplitude is pinched
between an observational floor and a stability ceiling (Section 11), with the gap at the level of
one pending coefficient. Any of the three jaws can close.

**Four: the redshift evolution of a₀.** If a₀ is truly anchored to dark energy, it must track the
dark-energy density through cosmic time — a specific, gentle evolution law, published by this
program, distinct both from a constant a₀ and from naive expansion-rate scaling. High-redshift
rotation measurements are near the required precision now, and current claims in the literature cut
both ways; the program's assessment of its own standing here is "contested, being watched," and the
prediction is on record.

**Five: two smaller flags on the record.** The aether sector implies a specific, computable pattern
of tiny Lorentz-violation effects in precision laboratory experiments (the g−2 family of tests) — a
computable prediction, not yet registered; a related Lorentz-violation channel (Gaia asteroid
astrometry) is among the hash-stamped gates. And a modified-gravity universe forms massive structures
*earlier* than ΛCDM expects — a long-standing MOND expectation that the James Webb Space
Telescope's surprisingly mature early galaxies currently favor, noted with the caution that early
JWST results are still being digested by everyone.

**Six: no particle, ever.** Every future direct-detection experiment continues to find nothing. An
unfalsifiable-sounding prediction with real content: a single confirmed dark-matter particle
detection kills this theory outright. Forty years of null results are, so far, forty years of this
prediction coming true.

---

## 14. Why should anyone trust this? The receipts

This program is one person with computers, working outside the academy, in a field with a long
tradition of confident outsiders being wrong. That context earns extra skepticism, and the program's
answer to it is procedural, not rhetorical. Four procedures:

**Every claim has a script.** Every load-bearing number in this document — every sigma, every dex,
every bound — is computed by a named script in the public repository, runnable by anyone, that
re-derives the number from scratch and *exits with an error* if any of its internal checks fail. The
technical paper's results table names the script for every row; scripts carry negative controls
(deliberate wrong inputs that must fail, proving the test can fail). The repository currently runs
to hundreds of such checks, green.

**Predictions are frozen before data.** The preregistration-and-hash discipline of Section 13: the
sharpest predictions are cryptographically time-stamped in public before the deciding dataset
exists. Whatever DR4 says, the record of what was predicted cannot be edited afterward.

**Errors are published louder than results.** The program maintains a formal do-not-cite list of its
own withdrawn claims — currently more than a dozen entries, including the three dead cluster
mechanisms of Section 10, a wrongly-claimed statistical exclusion (an error in the program's own
kernel arithmetic, found by the program, announced by the program), and a retracted
theory-of-everything overclaim (Section 15). Several corrections ran *against* the program's
interest; at least one ran in its favor and was published with exactly the same prominence. The
week's work log recorded in the technical corpus includes roughly a dozen near-misses — moments
where an exciting wrong number nearly got reported — caught by the standing rule that every
important quantity be computed a second, independent way.

**The competition is credited by name.** The base framework is Skordis and Złośnik's. The
transition curves are borrowed too: the shape this program derived from de Sitter space is
Milgrom's 1999 formula, and the completion kernel's functional form is the empirical fitting
function of McGaugh, Lelli and Schombert (2016). The data are the SPARC team's. The sharpest published objections — the ones
this program spent weeks answering — are Blanchet and Skordis's no-go and the Mistele–McGaugh–
Hossenfelder lensing bounds, and both are cited as the serious challenges they are. The claim
defended as original is narrow and stated in the technical paper's final section: the dark-energy
anchor and its coefficient, the choice and factorization of the function 𝓕, the boundedness theorem
and the dissolution of the 455× no-go, the cluster resonance mechanism, and the health-and-matrix
theorems of Section 11.

None of this makes the theory *right*. It makes the theory *checkable*, which is the only coin
science accepts.

---

## 15. What is NOT claimed

The technical paper's most important section is its list of non-claims. Reproduced here in plain
words, it is the fence past which no honest summary of this work may step:

1. **κ = ½ is not derived.** The coefficient linking a₀ to dark energy is *measured*: 0.551 ± 0.043
   (and ± 0.063 if the current tension in measurements of the universe's expansion rate is carried
   as an additional systematic — the coefficient is hostage to that dispute, since it scales
   one-for-one with it). One-half sits comfortably inside the error bar; so do other simple
   candidates, including 1/√3. Every attempted first-principles derivation either failed or
   collapsed into circularity, and the technical corpus proves several *cannot* work. One
   well-posed open problem remains (Section 16).
2. **"Zero dark matter" is not claimed.** Section 9 is the claim: no particle, no new substance, one
   field — but the cosmological pressureless job is real and filled at full strength.
2b. **"No dark matter in galaxies" is currently an open problem, not a result.** The mechanism this
   program had for keeping the field's dust out of galaxy interiors was withdrawn this week, by the
   program's own theorem. The favorable branch (the field's settled configuration is centrally
   evacuated) and the fatal branch (it piles up like cold particles and overshoots the galaxy data)
   are both computable; the nonlinear calculation that decides between them has never been done for
   this class of theory, by anyone, and is the program's next scheduled work.
3. **The cluster mechanism is a candidate, not a result.** It has survived this program's own
   execution attempts — environment matrix, health check, full perturbation analysis — and no
   external scrutiny. It has not been fit to real cluster mass profiles by anyone, and its
   amplitude tension with a published cluster analysis is live and could kill it.
4. **The late-universe growth history is only partly verified.** The CMB acoustic-peak pass is a
   real CLASS-code result; the subsequent growth of cosmic structure needs a dedicated evolving-
   sound-speed treatment that is owed, not done. One initial-condition confrontation (with
   intergalactic-hydrogen absorption data) is likewise owed.
5. **Solar-system preferred-frame parameters are not yet computed** for this specific function
   choice, against lunar-ranging and pulsar bounds; and the Cassini tension of Section 12 is
   inherited, disclosed, and unresolved.
6. **The wide-binary prediction is the idealized asymptote.** The registered 1.2139 is the clean
   point-source limit; the full nonlinear treatment is owed before DR4 lands.
7. **This is not a theory of everything.** It contains no explanation of particle physics, no
   quantum gravity, no unification. An earlier overclaim in that direction was publicly retracted on
   2026-06-23, and the retraction stands. This is a proposed field theory of the dark sector,
   anchored to one measured coincidence — nothing more, and the program regards "nothing more" as
   already ambitious enough.

---

## 16. The one open problem of the coefficient

Strip away everything settled and one question about the *number* remains, and it can now be stated
in a single line — which is itself progress, because for most of this program's life the question
was a fog.

A calculation in the technical corpus treats a body accelerating through the bath of gravitational-
wave fluctuations that a dark-energy-dominated universe must contain — must, because the horizon of
Section 3 carries a temperature, and a temperature means the universe is filled with a faint thermal
jitter, including a jitter of spacetime itself. Two remarkable things happen in the calculation.
First, an apparently hopeless suppression — effects of this kind are normally crushed by the Planck
scale, quantum gravity's remoteness, to the tune of hundreds of orders of magnitude — is *exactly
cancelled* by the enormous entropy of the cosmic horizon: the product of the horizon's entropy and
its curvature is π, identically, not approximately. What survives the cancellation is a formula of
exactly the right form: a₀ equals c times the horizon expansion rate times a pure number. Second,
the pure number — and with it κ — reduces to one well-posed question: **κ² = 8π × ε_tot, where
ε_tot is the fraction of the horizon's fluctuation modes that act on a slowly accelerating body.**
If ε_tot could be computed and came out to 1/(32π), then κ = ½ exactly, and the last measured number
in the theory would become a derived one.

It has not been computed. Five defensible ways of setting up the count give answers spanning a
factor of about 160, one of them lands exactly on ½, and that one was checked and found to rest on
an invalid step — a near-miss the program documented rather than published. The question is stated,
sharp, and open. It is either this framework's Rosetta stone or its tombstone inscription, and the
program genuinely does not know which.

---

## 17. Where this stands

As of 2026-08-09, the theory described here is, to this program's knowledge, the only proposal in
the literature that simultaneously: anchors MOND's acceleration scale to the measured dark-energy
density; embeds it in a relativistic field theory that passes gravitational lensing with exact
equality of dynamical and lensing mass; reproduces the CMB acoustic peaks in a real Boltzmann-code
run; recovers the solar system with exponential overkill; fits the radial acceleration relation as
well as fitted-a₀ MOND while taking its scale from cosmology instead; carries a stability-vetted candidate
for clusters resonant at its own threshold; and holds a certificate that its additions cannot
introduce ghosts, with gravitational waves at exactly light speed.

It is five parameters against ΛCDM's two. It is one outsider's program against a standard model
with tens of thousands of person-years behind it. It has been wrong, in public, more than a dozen
times this year, and says so — and its two sharpest open problems (the dust-in-galaxies calculation
of Section 9; the mode-count of Section 16) are stated in print, with the failure branches spelled
out. And it is now, in the only sense that matters, *finished as a construction*: the action is
written, the safety certificate is signed, and everything that remains is calculation and
confrontation — confrontations it has pre-committed to losing publicly if it loses.

The universe's oldest light, its strangest galaxies, and its emptiest places may yet converge on the
same verdict they have always given Newton and Einstein: *close, but the truth was stranger*. This
theory's wager is narrow and specific: that the strangeness begins at one hundred-billionth of a g —
at the acceleration where a falling body starts to feel the edge of the universe — and that the
number written on that edge is, within a hair's measurement, one-half.

---

## 18. Credit

The intellectual lineage, so no reader mistakes what is borrowed for what is claimed: MOND is
Milgrom's (1983), and the transition function this program derived from de Sitter space turns out to
be exactly Milgrom's own 1999 formula. The classical field-theoretic MOND is Bekenstein and
Milgrom's (1984). The relativistic framework AeST is Skordis and Złośnik's (2021), including its CMB
success; the ghost-condensate technology traces to Arkani-Hamed, Cheng, Luty and Mukohyama (2004).
The galaxy data are the SPARC compilation of Lelli, McGaugh and Schombert. The published challenges
answered here are Blanchet and Skordis's (2024) and Mistele, McGaugh and Hossenfelder's (2023). The
DBI functional form is borrowed from string theory's standard toolkit.

Original to this program: the coefficient relation a₀ = κc√(Gρ_Λ) as an anchor with κ measured at
0.551 ± 0.043; the factorized function 𝓕 and its offset-DBI Q-sector; the boundedness theorem and
the dissolution of the 455× no-go; the CLASS confrontation of that sector; the a₀-bump cluster
mechanism and its five-environment, health, and full-matrix results; the preregistered wide-binary
program with its hash-stamped amendments; and the open problems of Sections 9 and 16.

---

## Glossary

- **a₀** — the threshold acceleration, 9.36 × 10⁻¹¹ m/s², below which gravity departs from Newton.
  About one hundred-billionth of Earth's surface gravity.
- **Acoustic peaks** — the characteristic pattern of spot sizes in the cosmic microwave background,
  left by sound waves in the primordial plasma; measured exquisitely, and the sharpest test of any
  cosmological theory.
- **Action** — the single master formula defining a physical theory; all equations of motion follow
  from it by a standard procedure.
- **AeST** — Aether-Scalar-Tensor theory (Skordis & Złośnik 2021), the relativistic framework this
  theory lives in.
- **Aether** — here, a field of unit arrows pointing into the future at every point of spacetime,
  defining a local standard of rest; dynamical, not rigid.
- **CLASS** — one of the two standard precision codes for computing cosmic-microwave-background
  predictions; used here to test this theory, not a simulation of it.
- **Dark energy** — the smooth ingredient accelerating the universe's expansion; about 68% of the
  cosmic energy budget; in this theory, the resting energy of the khronon field.
- **DBI form** — an energy function with a hard cap approached via a square root, mathematically
  parallel to how special relativity caps speeds at c.
- **dex** — astronomers' unit for factors of ten; 0.1 dex ≈ 26%.
- **Ghost** — a field excitation with negative kinetic energy; fatal, because it makes empty space
  unstable. This theory carries a proof it has none.
- **Kernel** — this program's word for the chosen transition curve between the Newtonian and
  modified regimes.
- **Khronon** — the scalar field at the theory's heart, behaving like a universal clock-reading;
  its states supply dark energy, the cosmic dust, and the MOND effect.
- **ΛCDM** — the standard model of cosmology: general relativity plus dark energy (Λ) plus cold
  dark matter (CDM).
- **Lensing** — the bending of light by mass; measures gravity with light instead of orbits.
- **MOND** — Modified Newtonian Dynamics (Milgrom 1983): the hypothesis that the galaxy anomaly
  reflects a change in the law below a₀ rather than unseen matter.
- **Parsec** — astronomers' distance unit, about 3.26 light-years.
- **Preregistration** — publicly freezing a prediction, with a cryptographic fingerprint, before
  the deciding data exist.
- **Radial acceleration relation (RAR)** — the observed tight universal curve linking total gravity
  to visible-matter gravity across all galaxies; this theory fits it to 0.108 dex.
- **Sigma (σ)** — a measure of statistical confidence; 5σ (about one-in-3.5-million odds of chance)
  is physics' conventional discovery threshold, and 21σ — the lensing kill of this program's earlier
  arm — is beyond-argument territory.
- **SPARC** — the reference sample of 175 galaxies with precision rotation curves and photometry,
  compiled by Lelli, McGaugh and Schombert.
- **Wide binaries** — star pairs separated so widely their mutual gravity sits near a₀; the
  cleanest test environment for MOND-type laws, and the subject of this program's registered Gaia
  DR4 prediction.
