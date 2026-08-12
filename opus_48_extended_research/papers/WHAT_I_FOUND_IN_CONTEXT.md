# What I Found, In Context

### A plain-language account of one idea, what came before it, and what is still broken

**Carl P. Zimmerman** — Briar Creek Tech
12 August 2026. ORCID 0009-0008-3508-7982.

*Companion orientation piece to* THE_COMPLETION *(v9, DOI 10.5281/zenodo.21895046).*

---

## What this document is

This is an honest orientation piece about a single idea and where it sits in a literature that is
forty years old. It is deliberately *not* a claim of discovery. It says what
came before, what I added, what that buys, and what remains broken — including one thing that is
broken in a way I cannot currently fix.

I have overclaimed in public once before, in June 2026, and had to retract it in front of about
forty physicists. This document is written the way I should have written that one.

---

## 1. The problem, in one paragraph

Galaxies rotate faster than the matter we can see should allow. Stars at the edge of a spiral
galaxy orbit at speeds that would fling them off if gravity were only responding to the visible
gas and stars. There are two ways out. Either there is a great deal of invisible matter — dark
matter — arranged just so around every galaxy. Or gravity itself behaves differently when the pull
gets very weak. The second option is called MOND, proposed by Mordehai Milgrom in 1983.

## 2. The suspicious number

MOND works, empirically, extremely well for galaxies. Give it the visible matter and it predicts
the rotation curve, across galaxies spanning five decades in mass. But it contains one dial: an
acceleration, written $a_0$, about $1.2 \times 10^{-10}$ m/s². Above that acceleration gravity is
Newtonian. Below it, the law changes. Nobody knew why that particular value.

And here is the thing people noticed almost immediately. That number is close to the acceleration
you would naively build out of the universe as a whole — roughly the speed of light times the
expansion rate, $c H_0$, or equivalently $c\sqrt{G \rho_\Lambda}$ using the density of dark energy.
Milgrom pointed this out. Everybody repeated it. It has been described as one of the more
provocative coincidences in physics.

But it stayed a coincidence. You could write it on a napkin. You could not derive it. In every
working version of the theory, $a_0$ remained a number you fit to galaxy data, and the resemblance
to cosmology sat there unexplained.

## 3. What made a real theory possible

For a long time MOND had no relativistic version that survived contact with cosmology. The best
attempt, Bekenstein's TeVeS (2004), eventually failed the cosmic microwave background — the
snapshot of the universe at 380,000 years old, which is the single most constraining dataset in
cosmology.

In 2021 Constantinos Skordis and Tom Złośnik published **AeST** — Aether Scalar Tensor
(*Phys. Rev. Lett.* **127**, 161302). It does MOND in galaxies *and* it passes the CMB. That was
the breakthrough, and it is theirs, not mine. Everything below is built on their theory.

AeST contains what is usually called a "dark sector": a field with an energy density and a
pressure. In their formulation, $a_0$ is still put in by hand as a constant of the theory.

## 4. The move

My contribution is one line. Instead of inserting $a_0$ as a constant, I set it equal to the dark
sector's own pressure:

$$a_0^2(Q) = \kappa^2 G \left(-K(Q)\right)$$

where $K(Q)$ is the function that already sets that pressure in AeST, and $\kappa$ is a
dimensionless coefficient.

In words: **the MOND scale is not a separate number. It is the pressure of the dark sector,
expressed as an acceleration.** The coincidence becomes an identity.

## 5. What that buys, that I did not put in

Two things follow that I could not adjust after the fact.

**First, $a_0$ stops being a dial.** Because the dark sector's pressure is what drives cosmic
acceleration, tying $a_0$ to it means $a_0$ is fixed by the dark energy density — a quantity
measured by completely independent means. The prediction is $a_0 = \kappa c \sqrt{G \rho_\Lambda}
= 9.4 \times 10^{-11}$ m/s². The leftover coefficient $\kappa$ comes out of the galaxy data at
$0.551 \pm 0.043$. I want to be precise about this: $\kappa$ is **measured, not derived.** Four
different candidate values sit within two standard deviations of each other, and the data do not
single out any one of them. Anyone who tells you the coefficient is derived — including me on a
bad day — is overstating it.

**Second, and more interestingly, $a_0$ must change over cosmic history.** The dark sector's
pressure evolves. So $a_0$ evolves with it, in a way fixed by the same equation, with nothing left
to tune. And the direction it comes out is:

> **$a_0$ was essentially zero in the early universe and is at its maximum today.**
> Concretely, at recombination $a_0$ was 0.6% of its present value.

That is not something I arranged. And it is exactly what the theory needs, because it means MOND
was *switched off* when the CMB was imprinted. The CMB is the test that killed the previous
generation of these theories. Here, passing it stops being a struggle and becomes a consequence.

## 6. Now the honest part: what came before

The general move — let $a_0$ depend on the dark-sector field, so that $a_0$ evolves — **is not
new, and it is older than I realised.**

- **Bekenstein and Sagi, 2008**, *"Do Newton's G and Milgrom's $a_0$ vary with cosmological
  epoch?"* (arXiv:0802.1526). They compute exactly this in TeVeS: how $a_0$ depends on the
  cosmological value of the scalar field at the epoch a system formed. They find $a_0$ varies as
  the exponential of that field.
- **Famaey and McGaugh's Living Review (2012)** states it as established background: $a_0$ for a
  quasi-static system depends on the cosmological scalar-field value at the time that system
  collapsed, so different systems could in principle show different $a_0$.
- The $a_0 \simeq c^2\sqrt{\Lambda}$ resemblance is likewise decades old.

So the *family* of ideas is well-trodden. I should not, and will not, present the concept as mine.

**What does appear to be specific to my version, as far as I have checked:**

1. **The identification with pressure specifically.** Bekenstein–Sagi have $a_0$ going as an
   exponential of the field. Mine has $a_0^2$ *equal to* the dark sector pressure. That is a much
   tighter statement — there is no new function to choose, because $K(Q)$ is already in the theory
   doing another job.
2. **The direction of the evolution is opposite.** Theirs decreases with time. Mine rises to a
   maximum today. That is a genuine, testable difference, and it is the one that makes the CMB
   work rather than hurt.
3. **It is done inside AeST**, the version that actually passes the CMB, rather than inside TeVeS,
   which does not.

**And a caveat on my own caveat:** I have run three literature searches, not a priority search. A
real one means a full-text arXiv search on the pressure identification and reading Bekenstein–Sagi
carefully to see how close their construction already gets. Until that is done, the defensible
framing is not *"a new idea"* but:

> **a known idea, implemented in a specific way that fixes the coefficient and reverses the sign
> of the evolution.**

That is a narrower claim. It is also the kind that survives a referee.

## 7. What works

Taking the theory as it stands — AeST plus the pressure identification — the following hold, each
backed by a script in the public repository rather than by assertion:

- Gravitational waves travel at exactly the speed of light (required since 2017).
- No ghosts — the theory is not secretly unstable.
- Light bending matches general relativity's prediction in the solar system.
- The cosmic microwave background fits, computed with the standard CLASS code.
- Galaxy rotation curves: 0.108 dex scatter across the SPARC sample.
- The baryonic Tully–Fisher relation comes out as a *theorem*, not a fit.
- Solar system dynamics are untouched.
- Weak gravitational lensing works from 40 kpc out to 2.2 Mpc.

## 8. What does not work

**Galaxy clusters.** Fix the gravity law on galaxies — which the rotation curves do, tightly — and
clusters come out roughly a factor of two short. The extra pull is really there and the law does
not supply it.

This is not a flaw peculiar to my version. It is MOND's forty-year-old open wound. TeVeS does not
solve clusters. AeST as published by Skordis and Złośnik does not solve clusters. Milgrom's own
suggested resolution is undetected ordinary matter or massive neutrinos sitting in clusters.

What I *can* now say precisely is why my own equation cannot patch it. The reason is almost
funny. Fixing clusters needs the theory to distinguish a cluster from a galaxy at the same
acceleration, which requires the local dark-sector charge. But the amplitude of that effect turns
out to be a simple ratio: the local charge density divided by the dark energy density. And even if
that charge were *the entire dark matter content of the universe*, the term is still a hundred to
a thousand times too small. The knob exists. It is nowhere near big enough.

**Two other things are open, and I would rather list them than be asked about them:**

- $\kappa$ is measured, not derived. See above.
- The dark sector needs a pressureless component to make the CMB work, and that component gets
  captured by galaxies and should collapse. Followed honestly, the endpoint is black holes that
  are not observed. This is unresolved and it is as serious as clusters.

## 9. Where this leaves things

I have a relativistic theory — mostly other people's — with one line added that turns a famous
coincidence into an equation, fixes an otherwise free parameter to an independently measured
quantity, and forces the MOND scale to have been switched off in the early universe, which is
precisely what the hardest dataset requires.

It works on eight fronts and fails on one, and the one it fails on has defeated everyone who has
tried for forty years.

"Without a doubt" is not on offer here, and it is not on offer for the standard model of cosmology
either. What is on offer is a framework with no referee-proof kill and a short, honest list of
what is open. The next step is not another mechanism. It is writing this up properly and putting
it in front of people qualified to break it.

---

*The full technical version is* THE_COMPLETION *(v9, DOI 10.5281/zenodo.21895046). Every claim
above is backed by a runnable committed script in the accompanying repository. Where a claim was
withdrawn — and several were, including two of my own during the week this was written — the
withdrawal is recorded in the repository rather than quietly removed.*
