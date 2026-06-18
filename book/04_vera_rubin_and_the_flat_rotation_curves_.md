# Chapter 4: Vera Rubin and the Flat Rotation Curves (1970s)

> *In the 1930s, a heavy cluster of galaxies whispered that something was missing. In the 1970s, a careful woman with a spectrograph and a great deal of patience made the universe say it out loud.*

## Where We Are in the Story

Let me catch us up, because Chapter 4 is the moment the whole book turns.

In Chapter 2 we learned how to weigh the heavens. Kepler noticed that planets farther from the Sun move more slowly, and Newton explained exactly why: gravity reaches out across empty space, and an orbit is a balance between a body's tendency to fly off in a straight line and the inward pull holding it in a circle. From that balance comes one of the most useful equations in all of astronomy — a way to read the *speed* of an orbiting object and deduce the *mass* of whatever it is orbiting. We weigh the Sun by watching the Earth go around it. We can weigh a galaxy, in principle, by watching its stars go around its center.

In Chapter 3 we met Fritz Zwicky, who in 1933 pointed that logic at the Coma cluster — a swarm of galaxies, each one orbiting the common center of the swarm — and found something alarming. The galaxies were moving far too fast for the visible matter to hold them together. By the virial theorem, the theorem that ties a system's motion to its mass, Coma needed something like a hundred times more gravitating mass than its glowing galaxies could supply. Zwicky called the missing ingredient *dunkle Materie* — dark matter. And then, for the most part, the world filed his result under "interesting, probably some mistake in the assumptions" and moved on for forty years.

This chapter is about why the world stopped being able to move on.

The trouble with Zwicky's clusters was that they were *complicated*. A cluster is a loose, messy crowd of galaxies, and to apply the virial theorem you have to assume the crowd is settled, relaxed, and behaving itself statistically. There were honest places to hide. Maybe Coma wasn't relaxed. Maybe the distances were off. Maybe there was ordinary gas no one had counted. A skeptic in 1940 had room to breathe.

What was needed was something cleaner. A single galaxy is a far simpler object than a cluster: a flattened, rotating disk of stars and gas, turning like a vast slow pinwheel. If you could measure how fast that pinwheel turns at different distances from its center — its *rotation curve* — you would have an almost embarrassingly direct weighing of the galaxy, point by point, using nothing more than Newton's two-hundred-year-old equation. No statistical assumptions about a relaxed crowd. Just a spinning disk and the law of orbits.

That measurement is what Vera Rubin made. And what she found did not match what the visible stars predicted — not by a little, but by a factor of ten, and not in a way you could blame on a messy crowd. It was the cleanest possible measurement giving the most stubborn possible answer. After Rubin, the missing mass was no longer a curiosity at the edge of the field. It was a crisis at its center.

Let me build up to what she saw, slowly, starting with what we *expected* to see.

## What a Spinning Disk Should Do

Picture our Solar System from far above. The planets orbit the Sun in nearly circular paths, and they obey Kepler's rule: the farther out you go, the slower you move. Mercury, hugging the Sun, races around at about 48 kilometers per second. Earth ambles at 30. Distant Neptune crawls at barely 5. Plot orbital speed against distance from the Sun, and you get a curve that *falls* as you go outward — steadily, predictably, dropping off.

Why does it fall? Because almost all the mass of the Solar System — about 99.8 percent of it — is concentrated in the Sun at the center. Once you are outside the Sun, going farther out doesn't enclose any *more* mass; the Sun is all there is. The pull of gravity weakens with distance, so the speed needed to balance it weakens too. Specifically, the orbital speed falls off as one over the square root of the distance. Double your distance from the Sun and your orbital speed drops by a factor of about 1.4. This declining pattern is called **Keplerian falloff**, and it is the signature of a system whose mass sits in the middle.

> **Deeper Dive: The orbital speed equation, and where Keplerian falloff comes from**
>
> For a body on a circular orbit of radius $r$ around an enclosed mass $M(r)$, set the gravitational force equal to the centripetal force required for circular motion:
>
> $$\frac{GM(r)\,m}{r^2} = \frac{m\,v^2}{r}$$
>
> The orbiting mass $m$ cancels — a wonderful fact, the same fact behind the equivalence principle we'll meet in Chapter 7 — leaving the **circular-velocity equation**:
>
> $$v(r) = \sqrt{\frac{GM(r)}{r}}$$
>
> Here $G$ is Newton's gravitational constant, $r$ is the orbital radius, and crucially $M(r)$ is the mass enclosed *within* radius $r$. The shell theorem (also Newton's) guarantees that for a spherically symmetric mass distribution, only the mass interior to the orbit matters, and it acts as if concentrated at the center. (For a thin disk the geometry is messier — a correction factor of order unity — but the scaling logic survives, and the conclusion is the same.)
>
> Now consider two limits.
>
> **Point mass (the Solar System).** Outside the central mass, $M(r) = M$ is constant. Then
> $$v(r) = \sqrt{\frac{GM}{r}} \propto r^{-1/2}.$$
> Speed falls as the inverse square root of radius. This is Keplerian falloff.
>
> **What the visible disk of a galaxy *should* give.** A galaxy's light is concentrated toward the center and fades exponentially outward; essentially all the starlight is contained within a few "scale lengths." So once you are beyond the bright stellar disk, you have enclosed essentially all the *visible* mass, $M(r) \to M_{\text{vis}} = \text{const}$, and the prediction is again
> $$v(r) \propto r^{-1/2}.$$
> Beyond the glowing edge of a galaxy, the rotation speed should drop off in the same Keplerian way the planets do. *That* is the prediction Rubin set out to test.

So here is the clean, falsifiable expectation, stated in plain words. A galaxy's light is bunched toward its center. Out past the bright part, where there are hardly any more stars to add weight, the orbital speed of whatever you can still see out there should be *falling* — the same gentle decline the planets show, for exactly the same reason. The center holds the mass; the edge feels a weakening pull.

If galaxies behaved like the Solar System writ large, that is what we would measure. Hold that picture. It is wrong, and the way it is wrong is the entire subject of this book.

## How You Measure the Speed of a Star You Cannot Visit

Before we get to the answer, we need to be honest about the question: how on Earth do you measure how fast a star is moving when it is tens of thousands of light-years away and appears, even through a great telescope, as a dimensionless point or a faint smear of light? You cannot watch it move across the sky; at those distances the sideways motion over a human lifetime is far too small to see. What you *can* measure, with exquisite precision, is the part of its motion that is *toward you or away from you*. And the tool that lets you do it is one of the most beautiful gifts physics ever handed astronomy: the **Doppler shift**.

You already know the Doppler effect with your ears. A fire truck races toward you and its siren sounds high-pitched; it passes and races away and the pitch drops. The siren itself never changes. What changes is that the approaching truck crowds its sound waves together — squeezing them to a shorter wavelength, a higher pitch — while the receding truck stretches them out to a longer wavelength, a lower pitch. Motion toward you shortens waves; motion away lengthens them.

Light does exactly the same thing. An object moving toward you has its light shifted to shorter wavelengths — toward the blue end of the spectrum, a **blueshift**. An object moving away has its light stretched to longer wavelengths — toward the red end, a **redshift**. Measure the shift, and you have measured the speed along your line of sight. The faster the motion, the bigger the shift.

But this raises a sharp question. To know that a wavelength has been *shifted*, you have to know what it was *supposed* to be. If I hand you a single color of light, you cannot tell me whether it has been reddened or not — reddened *from what*? You need a reference, a known marker, a "this line should be exactly *here*." Nature, generously, provides these markers, and they come from the inner lives of atoms.

### The Fingerprints of Atoms

Every chemical element absorbs and emits light only at certain sharply defined wavelengths — its own private set, fixed by the quantum structure of its atoms. Hydrogen has its set, calcium has another, oxygen another still. When you spread a star's light into a spectrum, you see these as bright or dark **spectral lines**: narrow features at precise, lab-measured wavelengths. They are, quite literally, atomic fingerprints, and they appear at the same wavelengths in a galaxy ten million light-years away as they do in a flame on a laboratory bench, because hydrogen is hydrogen everywhere.

This is the astronomer's reference. You find a known line — say a particular glow of hydrogen whose true wavelength you have measured in the lab — and you see where it actually lands in the galaxy's spectrum. The gap between where it *should* be and where it *is* tells you the line-of-sight speed of the gas that emitted it. Do this for the gas on one side of a spinning galaxy and it is moving toward you (blueshifted); do it for the other side and it is moving away (redshifted), because the disk is turning. The difference between the two sides, after accounting for the galaxy's overall motion through space and the tilt at which we view the disk, *is* the rotation speed.

This technique — reading motion from the Doppler shift of spectral lines — is called **Doppler spectroscopy**, and it is the workhorse behind everything in this chapter.

> **Deeper Dive: From a measured shift to a velocity, and the lines Rubin used**
>
> For speeds small compared to the speed of light $c$ (true for galaxy rotation, which is hundreds of km/s against $c \approx 300{,}000$ km/s), the nonrelativistic Doppler relation is
>
> $$\frac{\Delta\lambda}{\lambda_0} = \frac{v_{\text{los}}}{c},$$
>
> where $\lambda_0$ is the rest (laboratory) wavelength of the line, $\Delta\lambda = \lambda_{\text{obs}} - \lambda_0$ is the measured shift, and $v_{\text{los}}$ is the line-of-sight velocity (positive for recession). A redshift ($\Delta\lambda > 0$) means motion away; a blueshift, motion toward.
>
> To turn this into a *rotation* speed, three corrections enter. First, subtract the galaxy's systemic velocity — its bulk motion through space, mostly the cosmic expansion (Chapter 9). Second, divide by $\sin i$, where $i$ is the disk's inclination: a disk seen perfectly face-on ($i=0$) shows no rotational Doppler shift at all, because the spin is entirely across your line of sight; a disk seen edge-on ($i=90°$) shows the full effect. Third, account for the line's measured position along the disk.
>
> Rubin and Ford worked in the *optical*, using emission lines from glowing clouds of ionized gas called **HII regions** ("H-two regions") — nurseries of hot young stars where ultraviolet starlight has stripped electrons from hydrogen. Their workhorse was the H$\alpha$ line of hydrogen at a rest wavelength of $\lambda_0 = 656.3$ nm (deep red) and the bright forbidden lines of doubly-ionized oxygen, [OIII]. These HII regions are bright, sharp, and scattered across a galaxy's disk — perfect tracers of where the gas is and how fast it turns. The radio astronomers, as we'll see, used a different and even more powerful tracer: the 21-cm line of *neutral* hydrogen, which reaches much farther out.

There is a poetry to this worth pausing on. We will never send a probe to another galaxy. We will never touch one of its stars or sample one of its gas clouds. And yet, by catching the light that left it millions of years ago and measuring — to a fraction of a nanometer — how the wavelengths of hydrogen and oxygen have been nudged by motion, we can clock the spin of a pinwheel of a hundred billion suns. The whole crisis of dark matter is built on this single, delicate, trustworthy thread. It is worth trusting; the Doppler shift is among the best-tested ideas in physics.

## Vera Rubin, and the Virtue of Patience

Vera Rubin (1928–2016) was an American astronomer who came to this problem with two qualities that turned out to matter enormously: a gift for careful, undramatic measurement, and a temperament suited to long unglamorous work that many of her contemporaries found beneath them.

That second point deserves a word, because the history is part of the science. Rubin worked in an era when American astronomy was, to put it gently, not built to include women. She was, for a time, barred from observing at certain major telescopes. When she had earlier touched controversial questions — the large-scale streaming of galaxies — she had met enough hostility that she made a deliberate decision: she would find a problem so solid, so based on clean measurement, that no one could argue with the data. Galaxy rotation curves looked, in the late 1960s, like exactly such a problem — careful, somewhat tedious, and as she put it, a place where she "could observe and study and learn and nobody would bother me." The irony is total and historic. The quiet, uncontroversial problem she chose precisely *because* it seemed safe became one of the great upheavals of twentieth-century physics.

Working at the Carnegie Institution in Washington with her longtime collaborator **Kent Ford** — an instrumentalist whose new, extraordinarily sensitive image-tube spectrograph was the other hero of this story — Rubin set out to do something almost mundane. She would take the nearest large spiral galaxy, Andromeda (also called M31), and measure its rotation curve properly: not just near the bright center, where others had looked, but point by point, HII region by HII region, as far out into the disk as Ford's spectrograph could reach.

Ford's instrument was the enabling technology. Earlier astronomers had been limited by the patience of photographic film, which drinks in light so slowly that the faint outer regions of a galaxy could take all night — many nights — to register. Ford's image tube electronically amplified the incoming light, so that exposures that once took unworkably long became feasible. This is a recurring lesson in observational science: a discovery often waits not for a new idea but for a new instrument sensitive enough to make the old question answerable. The missing mass had been hiding in plain sight, in the outer disks of galaxies, waiting for a spectrograph good enough to clock the gas out there.

So Rubin and Ford measured Andromeda, and then galaxy after galaxy after galaxy — dozens of spirals, of every size and brightness, across the 1970s. Night after patient night, they recorded the Doppler shift of HII regions marching outward from each galaxy's center, converting shift to speed, building the rotation curve point by point. They expected — everyone expected — to watch the curves climb in the dense inner regions and then *bend over and fall* in the Keplerian way once they passed the bright stellar disk, tracing out the declining signature of a galaxy whose mass lived in its middle.

That is not what the curves did.

## The Curves That Would Not Fall

The rotation curves rose in the center, as expected — and then they leveled off. And then they kept going. Out past the bright stellar disk, out where the starlight had faded to almost nothing, out where the Keplerian decline should have set in long ago, the orbital speed simply... stayed flat. The gas at the visible edge of a galaxy was moving just as fast as the gas well inside it. Sometimes the curve even crept slightly *upward*. It refused, stubbornly, to fall.

This is the **flat rotation curve**, and it is the central observational fact of this book. Let me state it carefully, because everything downstream depends on it. A flat rotation curve means that the orbital speed of stars and gas, plotted against distance from the galaxy's center, becomes roughly constant out to the largest radii we can measure — instead of declining as Kepler's law demands for any object orbiting a centrally-concentrated mass. Galaxy after galaxy showed it. Big galaxies, small galaxies, bright ones, faint ones: flat, flat, flat.

Now feel the force of this through the orbital equation. We measure the speed $v$, and we measure the radius $r$, and Newton's law tells us flatly what mass must be enclosed: $M(r) = v^2 r / G$. If $v$ stays constant while $r$ keeps growing, then $M(r)$ must *keep growing in direct proportion to $r$* — the enclosed mass goes up and up as you move outward, even into regions where there is essentially no light. The galaxy keeps getting heavier the farther out you look, long after it has stopped getting brighter.

> **Deeper Dive: A flat curve *demands* enclosed mass rising linearly with radius**
>
> Start again from the circular-velocity relation and solve for the enclosed mass:
>
> $$v(r) = \sqrt{\frac{GM(r)}{r}} \quad\Longrightarrow\quad M(r) = \frac{v(r)^2\,r}{G}.$$
>
> If the rotation curve is flat, $v(r) = v_{\text{flat}} = \text{const}$, then
>
> $$\boxed{\,M(r) = \frac{v_{\text{flat}}^2}{G}\,r \propto r.\,}$$
>
> The enclosed mass grows *linearly* with radius, without bound, out as far as the flat curve persists. Meanwhile the *light* stops: the surface brightness of a stellar disk falls off exponentially, so the enclosed *luminous* mass approaches a constant. The two diverge dramatically. At the optical edge of a typical bright spiral, the dynamically-required mass already exceeds the stellar-plus-gas mass by a factor of several; trace the flat curve out to where the neutral-hydrogen gas finally fades, often several times farther than the starlight, and the discrepancy grows to a factor of roughly **ten**.
>
> Equivalently, in terms of *density*: a mass profile $M(r) \propto r$ requires a density profile
>
> $$\rho(r) = \frac{1}{4\pi r^2}\frac{dM}{dr} = \frac{v_{\text{flat}}^2}{4\pi G}\,\frac{1}{r^2} \propto r^{-2}.$$
>
> An inverse-square density falloff is exactly the profile of an **isothermal sphere** — a self-gravitating ball of particles whose velocity distribution is the same at every radius, like the molecules of an isothermal (constant-temperature) gas in its own gravity. We'll return to why that particular profile keeps showing up. For now, note the chain: *flat curve* $\Rightarrow$ *mass* $\propto r$ $\Rightarrow$ *density* $\propto r^{-2}$ $\Rightarrow$ *isothermal sphere*. Each link is just algebra on Newton's law plus the measured fact that $v$ is constant.

Let me put the size of the problem in homely terms. Imagine you weigh a city by counting its lit windows at night, and your tally comes to a million people. Then you weigh the *same city* by measuring how its outskirts move — and the motion insists there are ten million people there, nine million of whom show no light at all, living in a vast dark suburb extending far beyond the glowing downtown. You would not conclude the suburb is empty. You would conclude that most of the city is dark. That is precisely the conclusion the rotation curves forced.

## The Halo: A Galaxy's Hidden Bulk

To make a flat rotation curve, then, a galaxy needs a great deal of unseen mass, and it needs that mass arranged in a particular way — spread out far beyond the visible disk, growing with radius, enclosing the bright pinwheel inside a much larger, rounder, invisible cloud. Astronomers call this hypothesized cloud the **dark-matter halo**: a roughly spherical envelope of unseen matter, several to ten times the mass of all the stars and gas, extending well past the glowing disk, whose gravity holds the outer gas in its fast, flat orbit.

The word "halo" is apt. A spiral galaxy, in this picture, is a bright flat disk of stars embedded near the center of a vast, dim, ball-shaped reservoir of something we cannot see. The disk is the part that shines; the halo is the part that weighs. By the time you reach the outer rotation curve, the halo is calling the gravitational tune — the stars are a minority partner in their own galaxy.

> **Deeper Dive: The pseudo-isothermal halo and the density profile $\rho \propto r^{-2}$**
>
> The simplest halo model that produces a flat outer rotation curve is the **pseudo-isothermal sphere**, with density
>
> $$\rho(r) = \frac{\rho_0}{1 + (r/r_c)^2},$$
>
> where $\rho_0$ is the central density and $r_c$ is a "core radius." Near the center ($r \ll r_c$) the density is roughly constant; far out ($r \gg r_c$) it tends to $\rho \propto r^{-2}$, exactly the isothermal falloff derived above. The enclosed mass then grows as $M(r) \propto r$ at large radius, and the rotation curve flattens to a constant
>
> $$v_{\text{flat}} = \sqrt{4\pi G \rho_0 r_c^2}.$$
>
> This was the phenomenological halo of the late 1970s and 1980s. Later, cosmological N-body simulations of cold dark matter (Chapter 6 and 12) produced a different, theoretically-motivated profile — the **Navarro–Frenk–White (NFW) profile**,
> $$\rho(r) = \frac{\rho_s}{(r/r_s)\,(1 + r/r_s)^2},$$
> which falls as $r^{-1}$ in the center and $r^{-3}$ far out, and which fits the *cosmological* expectation for how dark matter should clump. The mismatch between the cored isothermal halos that rotation curves seem to *prefer* and the cuspy NFW halos that simulations *predict* became known as the **core–cusp problem**, one of the small-scale tensions of the standard cosmological model we'll weigh honestly in Chapter 12. I flag it here only so you can see, even at this early stage, that "add a dark-matter halo" is not a single clean idea but a family of choices, each with its own fit and its own frictions. We will be careful, throughout this book, to keep that honesty in view.

I want to be scrupulously fair here, because this is the fork in the road, and the rest of the book lives at this fork. The flat rotation curve is an *observation* — solid, repeatable, beyond serious dispute. The dark-matter *halo* is an *interpretation* of that observation, and it is a very natural one: if Newton's gravity is exactly right and the curves are flat, then there *must* be unseen mass arranged just so. That interpretation has been the mainstream answer for fifty years, and it is a strong one. But notice that it is an interpretation, not a measurement. Rubin measured speeds. The halo is what you *add* to Newton's law to explain those speeds. In Chapter 5 we will meet the other road from this same fork — the suggestion that maybe it is the *law* that needs adjusting, not the *mass* that needs adding — and the entire framework this book is building toward lives on that second road. For now, simply hold both possibilities open. The data are the data; what they *mean* is the argument.

## Then Radio Confirmed It, and Made It Undeniable

Rubin and Ford worked in visible light, tracing HII regions. But visible starlight, and the glowing gas clouds that go with it, fade out at the optical edge of a galaxy. To really nail the flat curve, you wanted to measure rotation *even farther out*, in regions with no appreciable starlight at all — out where the only thing left to clock is cold, dark, neutral hydrogen gas. And here radio astronomy delivered a tracer that, frankly, seems almost designed for the job: the **21-centimeter line**.

Hydrogen is the most common substance in the universe, and most of it, out in the calm spaces of a galaxy, is *neutral* — a single proton with a single electron bound to it, cold and quiet, emitting no visible light. But neutral hydrogen has a subtle trick. The proton and the electron each behave like a tiny spinning magnet, and these two magnets can be aligned either the same way or opposite ways. Very, very occasionally — once in millions of years for any given atom — an atom flips from the slightly-higher-energy aligned state to the slightly-lower-energy opposite state, and in doing so it emits a single photon of radio light with a wavelength of about 21 centimeters. For any one atom this is absurdly rare. But a galaxy holds so many billions upon billions of hydrogen atoms that the faint 21-cm glow adds up into a signal radio telescopes can map in beautiful detail.

This is the **21-cm line of neutral hydrogen**, often written as the "HI line" (pronounced "H-one," meaning neutral atomic hydrogen). And it is the perfect rotation tracer for two reasons. First, neutral hydrogen extends *much* farther out than the starlight — often two, three, even four times beyond the visible disk — so it lets you measure the rotation curve in regions that are essentially dark. Second, like any spectral line it Doppler-shifts with motion, so you read the gas's speed exactly as Rubin read the speed of her HII regions, just at radio wavelengths instead of optical ones.

In the Netherlands, the radio astronomer **Albert Bosma** made this his doctoral thesis. Through the 1970s, using the Westerbork radio array, Bosma mapped the 21-cm rotation curves of two dozen spiral galaxies, pushing far beyond the optical edges Rubin's HII regions could reach. The radio curves told exactly the same story, and pushed it home: flat, flat, flat — out and out, well past the starlight, into regions where the only thing turning was invisible gas held by invisible mass. Bosma's flat curves, appearing essentially alongside Rubin and Ford's, are why the result became impossible to wave away. Two completely independent techniques — optical spectroscopy of glowing gas clouds and radio mapping of cold neutral hydrogen — using different instruments, different wavelengths, different tracers, in different countries, converged on the same stubborn, unexpected flatness. When two unrelated methods give you the same answer, you stop blaming the method.

> **Deeper Dive: Why the 21-cm line exists, and why it reaches so far**
>
> The 21-cm line is the **hyperfine transition** of the hydrogen ground state. The proton and electron each carry an intrinsic spin and an associated magnetic moment; the magnetic interaction between them splits the otherwise-single ground state into two sublevels — a triplet (spins parallel, slightly higher energy) and a singlet (spins antiparallel, slightly lower energy). The energy splitting is tiny, $\Delta E \approx 5.9 \times 10^{-6}$ eV, corresponding to a photon of frequency
> $$\nu = 1420.4\ \text{MHz}, \qquad \lambda = \frac{c}{\nu} \approx 21.1\ \text{cm}.$$
> The spontaneous transition is forbidden to leading order (it is a magnetic-dipole transition), giving it an enormous mean lifetime — on the order of $10^7$ years per atom. That extreme rarity is exactly *why* the line is so useful: it makes the gas optically thin, so the radio signal you receive is directly proportional to the *amount* of hydrogen along the line of sight, and the line traces cold neutral gas wherever it lives — including the vast outer reaches of a galaxy where there are no stars at all.
>
> Operationally, a radio array like Westerbork builds a "data cube": at each position on the sky it records the 21-cm intensity as a function of Doppler-shifted frequency, i.e. as a function of line-of-sight velocity. From this cube one extracts the velocity field across the whole HI disk and fits a **tilted-ring model** — a stack of concentric rings, each with its own rotation speed and orientation — to recover $v(r)$ out to the edge of the gas. Because the HI commonly extends to $2$–$4$ optical scale lengths beyond the last bright stars, these radio curves probe the halo-dominated regime directly, where the discrepancy with the luminous mass is largest. This is the regime where the enclosed mass-to-light ratio climbs to $\sim 10$ and beyond.

> **Worked Example: Weighing a galaxy's hidden mass from a flat curve**
>
> Let's do a real galaxy-scale calculation slowly, the way Rubin's data invite us to. Take a typical bright spiral with a flat rotation speed of
> $$v_{\text{flat}} = 200\ \text{km/s} = 2.0\times10^{5}\ \text{m/s},$$
> and suppose its 21-cm gas lets us trace that flat curve out to a radius of
> $$r = 30\ \text{kpc}.$$
> A kiloparsec is about $3.086\times10^{19}$ m, so
> $$r = 30 \times 3.086\times10^{19}\ \text{m} = 9.26\times10^{20}\ \text{m}.$$
>
> **Step 1 — Total mass enclosed within $r$, from dynamics.** Using $M(r) = v^2 r / G$ with $G = 6.674\times10^{-11}\ \text{m}^3\,\text{kg}^{-1}\,\text{s}^{-2}$:
> $$M(r) = \frac{(2.0\times10^5)^2 \,(9.26\times10^{20})}{6.674\times10^{-11}}.$$
> The numerator is $(4.0\times10^{10})\times(9.26\times10^{20}) = 3.70\times10^{31}$. Dividing:
> $$M(r) = \frac{3.70\times10^{31}}{6.674\times10^{-11}} = 5.55\times10^{41}\ \text{kg}.$$
> In solar masses ($M_\odot = 1.989\times10^{30}$ kg):
> $$M(r) = \frac{5.55\times10^{41}}{1.989\times10^{30}} \approx 2.8\times10^{11}\,M_\odot.$$
> So the dynamics demand roughly **280 billion solar masses** within 30 kpc.
>
> **Step 2 — Compare to the visible matter.** A galaxy like this has a stellar-plus-gas mass of, very roughly, $5$–$6\times10^{10}\,M_\odot$ — call it $5.5\times10^{10}\,M_\odot$, most of it well inside 30 kpc.
>
> **Step 3 — The discrepancy.**
> $$\frac{M_{\text{dynamical}}}{M_{\text{visible}}} \approx \frac{2.8\times10^{11}}{5.5\times10^{10}} \approx 5.$$
> Already a factor of five at this radius — and it *keeps climbing* if the flat curve continues past the gas, because $M(r)\propto r$ while the light has long since run out. Trace such curves to their limits and the ratio reaches of order ten. Five-sixths or more of the gravitating mass, on this accounting, is dark.
>
> Notice what we did and did not assume. We used only the measured flat speed, the measured radius, and Newton's circular-orbit law. *If* that law is exactly right, the missing mass is real and large. The entire alternative road of this book is the proposal that the last "if" is where to push. We measured a discrepancy; whether it is missing *mass* or a missing piece of the *law* is the open question. Hold the number — a factor of several to ten — and hold the honesty about what it does and does not prove.

## The Quiet Regularity Hiding Inside the Crisis

Most accounts of this history stop at the crisis: galaxies are mostly dark, here is your missing mass, on to the particle hunt. But there is a second, subtler thing buried in Rubin's and Bosma's curves, and it is the thread this whole book is really about. So let me draw it out gently, even though its full weight will not land until Part IV and Part V.

The first surprise was that the curves are *flat* rather than declining. The second surprise — quieter, and slower to be appreciated — is how *regular* the whole business is. Galaxies are wildly diverse objects: they span a factor of thousands in mass, brightness, and size; some are gas-rich, some gas-poor; some are placid, some disturbed. And yet the way the unseen mass arranges itself relative to the seen mass is not a free-for-all. There is a striking *conspiracy* between the visible disk and the invisible halo.

Here is the conspiracy, stated plainly. In the inner parts of a galaxy, the stars dominate the gravity, and the rotation curve is shaped by them. In the outer parts, the halo dominates, and the curve is shaped by it. For the curve to come out *flat* — for it to neither dip nor bump at the handoff — the falling contribution of the stellar disk and the rising contribution of the halo have to fit together with remarkable precision, right where one takes over from the other. They have to be tuned to each other. There is no obvious reason, in the dark-matter-halo picture, why a galaxy's *visible* stuff and its *invisible* stuff should know about each other so intimately as to produce a featureless flat line across the transition. They are supposed to be two different substances — ordinary matter that shines, and exotic matter that doesn't — that merely happen to share a galaxy. Why should their gravitational contributions interlock so neatly?

This is the **disk–halo conspiracy**, and it was noticed early — the very smoothness of the curves was itself a puzzle. The deeper you look, the more it sharpens. It is not just that individual curves are flat; it is that across the whole population of galaxies, the *visible* matter alone turns out to predict an astonishing amount about the *total* gravity, including the part attributed to the dark halo. Knowing where the stars and gas are, you can predict the rotation curve — dark matter and all — with a precision that, on the face of it, the dark-matter-halo picture does not obviously require.

> **Deeper Dive: The conspiracy that becomes the radial-acceleration relation**
>
> Decompose a galaxy's rotation curve into the contributions that add in quadrature:
> $$v_{\text{obs}}^2(r) = v_{\text{disk}}^2(r) + v_{\text{gas}}^2(r) + v_{\text{halo}}^2(r).$$
> The first two terms come straight from the observed light and gas (with a stellar mass-to-light ratio as the one significant fudge factor); the third is the inferred dark halo. The empirical fact — sharpened over decades since Rubin — is that $v_{\text{halo}}$ is not free. The amplitude and shape of the dark contribution are tightly correlated with the baryonic contribution, in such a way that the *total* curve is flat and, more remarkably, that the *acceleration* you actually measure at each radius is a tight, one-to-one function of the *acceleration* you would have predicted from the visible matter alone.
>
> Write the observed centripetal acceleration $g_{\text{obs}} = v_{\text{obs}}^2/r$ and the acceleration expected from the baryons alone $g_{\text{bar}} = v_{\text{bar}}^2/r$. The data of the last decade (the SPARC sample of $\sim$175 galaxies, McGaugh, Lelli, and Schombert 2016) show that $g_{\text{obs}}$ is an extremely tight function of $g_{\text{bar}}$ — the **radial-acceleration relation (RAR)** — with a characteristic transition near an acceleration scale
> $$a_0 \approx 1.2\times10^{-10}\ \text{m/s}^2.$$
> Above $a_0$, $g_{\text{obs}} \approx g_{\text{bar}}$ (ordinary Newtonian gravity, no dark matter needed). Below $a_0$, $g_{\text{obs}} \approx \sqrt{g_{\text{bar}}\,a_0}$ (the regime where the missing mass appears). The scatter about this relation is remarkably small — close to the observational error itself.
>
> This is the deep regularity that the flatness first hinted at. It is genuinely surprising in a pure dark-matter-halo picture: there is no compelling reason that the exotic halo's gravity should be *dictated*, radius by radius, by the visible matter through a single universal acceleration scale. The standard model accommodates the RAR — with enough care about how baryons settle into halos and how feedback redistributes gas, simulations can reproduce much of it — but it was not *predicted* by it. The relation, and that scale $a_0$, are exactly what Part IV (Milgrom's MOND) and Part V (this book's framework) take as the *primary clue*, the thing crying out to be explained rather than fitted.
>
> A crucial honesty, carried from the first page to the last: that the RAR is real and tight is not in dispute. *What it means* very much is. And I will say plainly, here and throughout, that the framework this book builds reproduces the RAR's *form* and ties its *scale* $a_0$ to the dark-energy density of the cosmos — but it shares those rotation-curve and Tully–Fisher successes with the *entire* MOND family; they are not unique to it, and they do not by themselves single it out. The framework is not a theory of everything yet, as frustrating as it may be. What this chapter establishes is only that the clue exists, that it is buried in the flatness Rubin found, and that it is begging for an explanation. The rest of the book is the attempt to give it one — honestly, both ways, with the open questions kept always in view.

So the flat rotation curve gives us two gifts at once. The loud one is the crisis: galaxies are gravitationally dominated by something we cannot see, by a factor of several to ten. The quiet one is the clue: that "something," whatever it is, is governed by a single acceleration scale and locked to the visible matter with a tightness that asks to be understood. Most of physics, for fifty years, has chased the loud gift — *what is the dark stuff?* This book is mostly about taking the quiet gift seriously — *why is there a special acceleration, and why does it equal what it equals?* Keep both in your pocket. We will need them both.

## A Word on Why This Settled the Matter

It is worth asking why Rubin's curves convinced the community when Zwicky's clusters, forty years earlier, had not. The answer is instructive about how science actually moves.

Zwicky's argument was statistical and depended on a chain of assumptions about a complicated, possibly-unsettled crowd of galaxies. Each link in that chain was a place a reasonable skeptic could push. Rubin's argument was almost brutally direct: here is a single galaxy; here is its measured rotation speed at each radius; here is Newton's two-century-old law; the mass simply does not add up. There was no relaxed-crowd assumption to question, no virial average to distrust. And then Bosma's radio curves, using a wholly different tracer at a wholly different wavelength, gave the identical result and extended it farther out than starlight could go. A clean measurement, repeated independently, in a simple system, against a law no one doubted. That combination is about as persuasive as observational astronomy gets.

It is also a useful reminder, as we go forward, of what *kind* of fact a flat rotation curve is. It is not a theory. It is not an interpretation. It is a measured relationship between speed and radius in real galaxies, as solid as anything in extragalactic astronomy. Everything we build in the coming chapters — the dark-matter halo, Milgrom's modified dynamics, this book's de Sitter–Unruh framework — is an attempt to *explain* this fact. The fact itself is not up for grabs. Where the honest argument lives is in the explanations, and I will try, at every step, to give you both the strengths and the weaknesses of each, in the same breath, so that you can judge for yourself.

## Summary

- **The expectation.** A galaxy's light is concentrated toward its center. By Newton's law of orbits, $v(r)=\sqrt{GM(r)/r}$, the rotation speed of gas beyond the bright disk *should* decline with radius (Keplerian falloff, $v\propto r^{-1/2}$), just as the planets slow down with distance from the Sun.

- **The measurement.** Vera Rubin and Kent Ford, using a sensitive image-tube spectrograph and Doppler spectroscopy of HII regions (notably the H$\alpha$ line), measured the rotation curves of dozens of spiral galaxies in the 1970s, far out into their disks.

- **The surprise.** The curves did not fall. They rose, leveled off, and stayed **flat** out to the largest radii measured — the central observational fact of this book. The visible edge of a galaxy turns just as fast as its interior.

- **What flatness demands.** $v=\text{const}$ forces the enclosed mass to grow linearly with radius, $M(r)\propto r$, and the density to fall as $\rho\propto r^{-2}$ (an isothermal sphere) — even where there is no light. Galaxies need roughly **ten times** more gravitating mass than their stars and gas supply, arranged in an extended, roughly spherical **dark-matter halo**.

- **Radio confirmation.** Albert Bosma mapped the **21-cm line of neutral hydrogen**, which reaches far beyond the starlight, and found the same flatness even farther out. Two independent techniques (optical and radio) converging made the missing mass undeniable.

- **Crisis and clue.** The loud lesson is the crisis: galaxies are dominated by unseen mass. The quiet lesson — the thread of this whole book — is the *regularity*: the dark and visible contributions conspire to make flat curves and obey a tight **radial-acceleration relation** with a universal scale $a_0\approx1.2\times10^{-10}\ \text{m/s}^2$. That clue, not the crisis, is what Parts IV and V try to explain.

- **The honest standing, stated early.** That the curves are flat and the RAR is tight is *measured fact*, beyond dispute. Whether the explanation is unseen *mass* or a modified *law* is the open fork we take up in Chapter 5 — and even the framework this book builds, which reproduces the RAR's form and ties $a_0$ to dark energy, shares those galaxy-scale successes with the whole MOND family and is not, as frustrating as it may be, a theory of everything yet.

## Questions

1. **(Easy.)** In our Solar System, why does Neptune orbit so much more slowly than Earth? Using the idea behind the orbital-speed equation in words (no algebra needed), explain why we *expected* a galaxy's rotation curve to decline at large radius, and state in one sentence what Rubin actually found instead.

2. **(Easy–medium.)** Explain in your own words how a Doppler shift lets us measure the speed of gas in a distant galaxy we can never visit. Why do we need known spectral lines (atomic "fingerprints") to do it — what goes wrong if we only have a single, unlabeled color of light?

3. **(Medium, calculation.)** A spiral galaxy has a flat rotation speed of $v_{\text{flat}}=150$ km/s, and its 21-cm gas traces the flat curve out to $r=25$ kpc. Using $M(r)=v^2 r/G$, estimate the total mass enclosed within 25 kpc (in solar masses). If the visible mass is about $3\times10^{10}\,M_\odot$, what is the ratio of dynamical to visible mass? (Useful: $1\,\text{kpc}=3.086\times10^{19}$ m; $G=6.674\times10^{-11}$ SI; $M_\odot=1.989\times10^{30}$ kg.)

4. **(Medium.)** Show, starting from a flat rotation curve ($v=\text{const}$), that the required mass profile is $M(r)\propto r$ and the density profile is $\rho(r)\propto r^{-2}$. Why is the $r^{-2}$ profile called "isothermal," and what does that name borrow from the physics of ordinary gases?

5. **(Medium–hard, conceptual.)** State the "disk–halo conspiracy" in your own words. Why is it *surprising* in a picture where ordinary matter and dark matter are two completely different substances that merely share a galaxy? What feature of the data (introduced in the final Deeper Dive box) sharpens the conspiracy into a quantitative regularity, and what is the characteristic acceleration scale involved?

6. **(Research-level.)** The radial-acceleration relation has remarkably small scatter — close to the observational uncertainties. Sketch how a cold-dark-matter cosmology might *accommodate* this relation (think: how baryons settle into halos, mass-to-light ratios, feedback) versus how a modified-dynamics view would *predict* it from a single acceleration scale. What kinds of observations could, in principle, distinguish "the RAR is an emergent coincidence of galaxy formation" from "the RAR reflects a fundamental law"? In your answer, be explicit about which galaxy-scale successes would be *shared* by any MOND-family theory and therefore could *not*, by themselves, single out one specific framework over another.
