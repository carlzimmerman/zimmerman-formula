# Chapter 13: What Is Inertia, Really?

> *Push an empty shopping cart in the parking lot and it rolls easily. Push a full one and it fights back. Now imagine you and the cart are floating in deep space, far from any planet, with nothing holding the cart down. Push it. It still fights back. Why?*

---

## A question hiding in plain sight

We are about to begin the part of this book where the new physics lives. Parts 1 and 2 were the long, honest setup: how we weigh galaxies, how we discovered that the weighing doesn't add up, and the two great roads out of that discovery — a new particle or a new law. We spent a lot of pages on General Relativity and the expanding universe so that when the framework finally arrives, you'll have the vocabulary to judge it on its own terms.

This chapter, and the three after it, are the foundation stones. The framework at the heart of this book proposes to modify a single quantity — **inertia** — and it proposes to do so using **temperature**, of all things, drawn from the geometry of an expanding, accelerating universe. Before any of that can make sense, we have to look hard at the thing being modified. And here is the uncomfortable, wonderful truth I want you to sit with for a whole chapter:

**Nobody fully knows what inertia is, or where it comes from.**

That is not a rhetorical flourish. It is the honest state of physics in 2026. We can *measure* inertia to exquisite precision. We have an equation for it that is more than three centuries old and works fabulously well. We use it to fly spacecraft and design bridges. But the question of *why* matter resists being pushed — what physical mechanism, what part of the universe, actually does the resisting — remains genuinely open. Some of the greatest minds in the history of science chewed on it and walked away unsatisfied. Einstein chewed on it for years; it helped him build General Relativity, and then it quietly defeated him.

So if you finish this chapter feeling that inertia is stranger than you thought, that's not a failure of the chapter. That's the point. You can't appreciate a proposal to modify inertia until you've felt how mysterious the ordinary thing already is.

Let's start with the shopping cart.

---

## Inertia: the resistance to a change in motion

Here is the first definition, and it's worth saying slowly.

**Inertia** is the tendency of an object to keep doing what it's already doing — to keep sitting still if it's sitting still, or to keep moving in a straight line at a steady speed if it's already moving — and its *resistance* to any change in that state of motion.

That's it. Inertia is "resistance to a change in motion." Notice what it is *not*. It is not friction. Friction is a force from rubbing — the cart's wheels against the ground, air against your hand. We can imagine turning friction off entirely (that's what deep space gives us, near enough), and inertia is still there. It is not gravity either, though we'll see in a moment that the two are tangled together in one of the deepest puzzles in all of physics.

Inertia is the thing that makes a full cart harder to get going than an empty one. It's why a loaded truck takes longer to speed up and longer to stop than a bicycle. It's why, when your car brakes hard, your body keeps lurching forward — your body was moving, and it "wants" to keep moving, and the seatbelt is what finally changes its mind.

The quantity that measures how much inertia an object has is its **mass**. More mass, more inertia, more resistance. This is the mass in the most famous equation in introductory physics, Newton's second law:

$$ F = m\,a $$

In words: the force $F$ you apply equals the object's mass $m$ times the acceleration $a$ you produce. Rearrange it — $a = F/m$ — and you can read inertia right off the page. For a given push $F$, a bigger $m$ gives a smaller $a$. The object accelerates *less* for the same shove. That "less" is inertia, written in algebra.

Now here's the thing the shopping-cart thought experiment is designed to surface. In deep space, with no ground, no air, no gravity to speak of, the cart *still* has mass, and so it still resists. The resistance isn't coming from the floor. It isn't coming from the Earth pulling down. It is somehow intrinsic to the cart — or so it seems. Newton's equation tells you *how much* the cart resists. It is completely silent on *why* it resists at all, or *what* it is pushing back against.

Read that last sentence again, because it is the hinge of the whole chapter. $F = ma$ is a spectacularly accurate description. It is not an explanation. It tells you the price of accelerating a mass; it does not tell you who is collecting the payment.

> **Margin aside.** Galileo got to the doorway of inertia before Newton walked through it. He realized that a ball rolling on a perfectly smooth, level surface would, absent friction, just keep rolling forever. Aristotle had taught for two thousand years that motion needs a continuous cause — that things stop because stopping is their natural state. Galileo saw that stopping is caused (by friction), and that *steady motion needs no cause at all*. That single inversion is the seed of the entire concept of inertia.

---

## Two kinds of mass that have no business being equal

Now I have to complicate the word "mass," because it's secretly doing two completely different jobs, and the fact that it can do both is one of the most astonishing coincidences — if it is a coincidence — in physics.

**Job one: inertial mass.** This is the mass we just met. **Inertial mass** is the measure of an object's resistance to being accelerated by *any* force whatsoever. Push it with your hand, a magnet, a rocket — inertial mass is what sets how much it speeds up. It lives in $F = ma$, where it answers the question "how hard is this to get moving?"

**Job two: gravitational mass.** This is something else entirely. **Gravitational mass** is the measure of how strongly an object participates in gravity — both how hard it pulls on other things and how hard it gets pulled. It lives in Newton's law of gravity:

$$ F = \frac{G\, M\, m}{r^2} $$

Here $m$ is gravitational mass: the "gravitational charge" of the object, the thing that couples it to the gravity of a mass $M$ a distance $r$ away, with $G$ being Newton's gravitational constant. Just as electric charge measures how strongly something responds to electricity, gravitational mass measures how strongly something responds to gravity.

Stop and notice how unrelated these two ideas are. Inertial mass is about resistance to *every* push. Gravitational mass is about your particular *coupling to gravity*, one specific force among many. There is no obvious reason on Earth or in heaven why a thing's reluctance to be accelerated by a rocket engine should have anything to do with how strongly it feels the Earth's pull. Electric charge and inertial mass are clearly different numbers — a heavy object can carry tiny charge, a light object huge charge. Why should *gravitational* charge be any different?

And yet. When you drop two objects of different mass in a vacuum — a feather and a hammer, famously demonstrated on the Moon by astronaut David Scott in 1971 — they fall *together*. They hit the ground at the same instant. Galileo argued this (the leaning-tower story may be apocryphal, but the reasoning is his), and it has been confirmed ever since to staggering precision.

Why does this require the two masses to be equal? Watch the algebra. The force of gravity on a falling object near Earth is $F = m_{\text{grav}}\, g$, where $g$ is the gravitational field and $m_{\text{grav}}$ is the object's *gravitational* mass. The acceleration that force produces is, by Newton's second law, $a = F / m_{\text{inert}}$, where $m_{\text{inert}}$ is its *inertial* mass. Put them together:

$$ a = \frac{m_{\text{grav}}}{m_{\text{inert}}}\, g $$

For every object to fall with the *same* acceleration $a$ — for the feather and the hammer to land together — the ratio $m_{\text{grav}} / m_{\text{inert}}$ must be the *same* for all of them. Choose your units so that ratio is exactly 1, and you get the rule everyone learns in school: all objects fall at the same rate $g$, regardless of mass. But look at what was smuggled in to make that work. The "resistance to a rocket" number and the "coupling to gravity" number cancel. They are, as far as anyone can measure, **identical**.

This equality has a name — the **weak equivalence principle**, or the *universality of free fall* — and it is not a small thing. It is the experimental seed from which Einstein grew General Relativity, as we saw in Chapter 7. But notice that General Relativity *assumes* the equality; it builds a magnificent geometric cathedral on top of it. It does not *explain* why the two masses are equal in the first place. It promotes the coincidence to a principle and gets on with the work. That is a perfectly respectable thing for a theory to do. But the coincidence is still sitting there, unexplained, at the bottom of everything.

> **Deeper Dive: How well do we actually know $m_{\text{grav}} = m_{\text{inert}}$?**
>
> The equality of inertial and gravitational mass is one of the most precisely tested statements in all of physics. The standard figure of merit is the **Eötvös parameter**, defined for two test bodies $A$ and $B$ as
> $$ \eta = 2\,\frac{(m_{\text{grav}}/m_{\text{inert}})_A - (m_{\text{grav}}/m_{\text{inert}})_B}{(m_{\text{grav}}/m_{\text{inert}})_A + (m_{\text{grav}}/m_{\text{inert}})_B}. $$
> If the two masses are identical for both bodies, $\eta = 0$ exactly. Any difference — any object that falls even infinitesimally faster than another in the same gravitational field — shows up as a nonzero $\eta$.
>
> The history is a ladder of ever-tighter null results:
> - **Loránd Eötvös** (Baron Roland von Eötvös, Hungarian, ~1885–1909) used a torsion balance — essentially a horizontal beam hung from a fine fiber, with different materials on each end — and constrained $\eta \lesssim 10^{-9}$. The Sun's and Earth's gravity, plus the Earth's rotation, would twist the fiber if the materials responded differently. They didn't.
> - The **Eöt-Wash group** at the University of Washington pushed torsion-balance tests to $\eta \lesssim 10^{-13}$ over decades.
> - The **MICROSCOPE** satellite (CNES, French space agency), with final results published in 2022, tested platinum against titanium in free fall in orbit — the cleanest "drop tower" imaginable, falling around the Earth for years — and found $\eta = (-1.5 \pm 2.3_{\text{stat}} \pm 1.5_{\text{syst}}) \times 10^{-15}$. Consistent with zero at the level of **one part in $10^{15}$**.
>
> To feel that number: it is like comparing the weights of two cargo ships and finding they agree to within the mass of a single grain of sand. Whatever makes inertial and gravitational mass equal, it holds to fifteen decimal places. A modified-inertia program of the kind this book will develop must respect this — it must not break the universality of free fall in any regime we have tested, which is one reason (as we'll see in Chapter 21) the framework's modification is engineered to switch *off* in the high-acceleration Solar-System regime where these experiments live.

![Bar chart of Eotvos-parameter upper limits from Newton to MICROSCOPE, shrinking by twelve orders of magnitude](figures/ch13_eotvos_ladder.png)

***Figure 13.1 — The ladder of ever-tighter null tests of $m_{\text{grav}}=m_{\text{inert}}$.*** Each bar is the published upper limit on the Eötvös parameter $\eta$ reached by a landmark experiment; a shorter bar is a tighter test. From Newton's pendulums to the MICROSCOPE satellite the bound has fallen by twelve orders of magnitude, to $|\eta|\le 2.3\times10^{-15}$ — agreement to fifteen decimal places. The dashed line marks the present floor that any modified-inertia theory must respect. These are the published figures of merit, not raw data.

**Source:** Figure generated by [`book/figures/ch13_eotvos_ladder.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch13_eotvos_ladder.py). Bounds from the equivalence-principle literature: the MICROSCOPE final result $\eta=(-1.5\pm2.3_{\text{stat}}\pm1.5_{\text{syst}})\times10^{-15}$ (CNES, 2022), the Eöt-Wash torsion-balance program (University of Washington, $\sim10^{-13}$), and Eötvös's original torsion-balance limit ($\sim10^{-9}$, ~1885–1909).


> **Worked Example: Reading inertia and gravity off the same falling rock.**
>
> Let's make the two masses concrete with a single object and slow numbers.
>
> Take a rock with mass $m = 2.0\ \text{kg}$. We'll use this one number in both roles and watch it do two different jobs.
>
> **As gravitational mass — how hard does Earth pull it?**
> Near Earth's surface the gravitational field is $g \approx 9.8\ \text{m/s}^2$ (more carefully, $g = GM_\oplus/R_\oplus^2$, but $9.8$ will do). The downward pull is
> $$ F = m_{\text{grav}}\, g = (2.0\ \text{kg})(9.8\ \text{m/s}^2) = 19.6\ \text{N}. $$
> So Earth tugs on the rock with about 19.6 newtons. Here the "2.0 kg" is acting as a gravitational charge — its coupling to Earth's field.
>
> **As inertial mass — how much does that pull accelerate it?**
> Now release the rock and ask how fast it speeds up. Newton's second law uses the *inertial* mass:
> $$ a = \frac{F}{m_{\text{inert}}} = \frac{19.6\ \text{N}}{2.0\ \text{kg}} = 9.8\ \text{m/s}^2. $$
> The rock accelerates downward at $9.8\ \text{m/s}^2$. Here the "2.0 kg" is acting as resistance to acceleration.
>
> **The magic.** The acceleration came out to exactly $g$ — the same $9.8\ \text{m/s}^2$ we put in. That happened *only because the gravitational 2.0 kg and the inertial 2.0 kg are the same number.* Symbolically:
> $$ a = \frac{m_{\text{grav}}\, g}{m_{\text{inert}}} = \frac{m_{\text{grav}}}{m_{\text{inert}}}\, g = (1)\,g = g. $$
> If gravitational mass had been, say, $2.0\ \text{kg}$ but inertial mass had been $2.2\ \text{kg}$ — a 10% mismatch — the rock would have fallen at $a = (2.0/2.2)(9.8) \approx 8.9\ \text{m/s}^2$, noticeably slower than a rock with matched masses dropped beside it. We'd see heavy things fall at different rates depending on their internal makeup. We have looked for exactly this, with platinum and titanium, to fifteen decimal places. We have never seen it. The cancellation is, as far as we can measure, perfect.
>
> The lesson to carry forward: $F=ma$ governs how the rock *responds*; $F = m_{\text{grav}}\,g$ governs how gravity *pulls*. They are different physics that happen to share a number. The framework in this book lives entirely on the *first* equation — it asks whether the $m$ in $F=ma$, the inertial $m$, might be subtly different from what Newton assumed when accelerations get fantastically small.

---

## Newton's bucket: is motion *relative to something*?

We've established that inertia exists, that it's measured by mass, and that this mass coincides mysteriously with gravitational charge. Now comes the deeper question, the one that haunted Einstein: **motion relative to what?**

When I say the cart "resists a change in motion," I've assumed I know what "motion" means. But motion is relative. Sitting in a train, you can read a book without spilling your coffee even though, relative to the ground, you're hurtling along at a hundred miles an hour. As far as the coffee is concerned, the train carriage is "at rest." Velocity is always *relative to something* — there is no experiment you can do inside a smoothly gliding train, windows shaded, to tell whether you're moving or parked. Galileo knew this; it's called the principle of relativity, and it's centuries older than Einstein.

But *acceleration* feels different. When the train suddenly brakes, your coffee sloshes. When it rounds a curve, you lean. You can *feel* acceleration from the inside, with no window needed. And inertia — the resistance we care about — is resistance to *acceleration* specifically. So acceleration seems to be absolute in a way velocity is not. Acceleration relative to *what*, though? What is the cosmic referee that decides you're accelerating and the coffee should slosh?

Newton had an answer, and he built a famous thought experiment — really an actual experiment you can do at home — to defend it. It's called **Newton's bucket**.

Here it is. Take a bucket of water and hang it from a long, twisted rope. Let it go, and the rope unwinds, spinning the bucket. Watch the water's surface, and you'll see four stages:

1. **At first**, the bucket spins but the water hasn't caught up — the water sits still while the bucket walls slide past it. The water's surface is **flat**.
2. **Then** friction drags the water into spinning along with the bucket. Now the water is rotating, and its surface climbs the walls and dips in the center — it forms a curved, concave shape, like the inside of a bowl. (This is the centrifugal effect; the spinning water is flung outward and piles up at the rim.)
3. **Now grab the bucket and stop it.** The water keeps spinning for a while. The bucket is still relative to you, but the water's surface is *still curved*.
4. Eventually the water slows and the surface goes **flat** again.

Newton's killer observation: in stage 1 the water and bucket are *at rest relative to each other* (both still, surface flat), and in stage 3 they are *also at rest relative to each other* (the spinning water inside a now-stopped bucket — well, moving relative to it, but the point sharpens if you compare the surface shapes). The decisive comparison is between stage 1 and stage 2. In stage 1, water and bucket *agree* in motion and the surface is flat. In stage 2, water and bucket *agree* in motion again (both spinning together) — and yet the surface is curved.

So the curving of the surface — the centrifugal effect, a real, visible, measurable consequence of inertia — does **not** depend on the water's motion *relative to the bucket*. The bucket can't be what the water is "accelerating relative to." Newton concluded: the water's surface curves because the water is rotating relative to **space itself** — relative to an absolute, fixed, invisible stage on which all motion plays out. He called it **absolute space**. Inertia, for Newton, is your resistance to accelerating with respect to this absolute stage.

It's a clean answer. It's also deeply unsatisfying to a lot of physicists, then and now, for one reason: absolute space *acts but cannot be acted upon*. It pushes the water up the walls, but nothing you do affects it. It has no other properties — no temperature, no substance, no way to detect it except through the very inertia it's supposed to explain. It's an invisible referee who decides the game but never shows up in any other photograph. Many found that too convenient, a name for the mystery rather than a solution to it.

> **Deeper Dive: The absolute-versus-relational debate, stated carefully.**
>
> The dispute Newton's bucket dramatizes is one of the oldest in physics, and it has two camps.
>
> **The absolutist (Newton, broadly).** Space — or in the modern, post-Einstein version, *spacetime* — is a real entity with its own existence, independent of the matter in it. Accelerated motion is motion relative to this entity, and inertia is the resistance such motion meets. The clinching argument is precisely the bucket: inertial effects (the curved surface, the felt "g-forces") appear whenever there is acceleration relative to space, *even when there is no relative acceleration between the test object and any nearby matter*. Newton's contemporary correspondent and rival **Gottfried Leibniz** argued the opposite — that space is nothing but the set of relations between bodies, with no independent existence — and the **Leibniz–Clarke correspondence** (1715–16, Samuel Clarke writing for Newton) is the classic statement of the two positions.
>
> **The relationist (Leibniz, Berkeley, later Mach).** There is no absolute space. All motion is motion *relative to other matter*. Berkeley objected to Newton directly: in a truly empty universe, he said, the bucket argument collapses, because "rotation" relative to nothing is meaningless. If the water's surface curves, it must be curving relative to *something physical* — and the only candidate left is the rest of the matter in the universe: the fixed stars.
>
> The stakes are not merely philosophical. They are this: **what physical system supplies the standard of non-acceleration?** What defines the frames — the *inertial frames* — in which Newton's first law holds and a free particle moves in a straight line? Newton says: absolute space defines them, full stop. The relationist says: the matter of the universe defines them, and if you could somehow change that matter, you would change the inertial frames themselves. That second possibility is testable in principle, and it is the doorway to Mach.
>
> General Relativity, it's worth noting, sits awkwardly between the camps. Its spacetime is dynamical — matter shapes it, so it is *not* Newton's rigid absolute stage — yet spacetime still has independent reality and still carries energy and inertia of its own (gravitational waves exist in otherwise empty space). Einstein hoped GR would be fully relational, fully Machian. It is not, quite. That unfinished hope is the next section.

---

## Mach's principle: do the distant stars give you your inertia?

Now we reach the idea I find genuinely haunting, the one that gives this chapter its weight.

**Ernst Mach** was an Austrian physicist and philosopher of the late 1800s — the same Mach whose name we attach to supersonic speeds ("Mach 2"). He was a fierce critic of anything in physics he thought was unobservable metaphysics, and Newton's absolute space was exactly his sort of target. You can't see it, you can't touch it, you can only infer it from inertia itself — so, said Mach, it explains nothing. It's a circular ghost.

Mach offered a radical alternative. He took the bucket and added a twist that you cannot do in a laboratory but can absolutely do in your head. Newton imagined the water rotating relative to absolute space. Mach asked: how do we *know* it's rotating relative to space, and not relative to *the rest of the universe*? When the water's surface curves, the water is, after all, also spinning relative to the **fixed stars** — relative to the great mass of all the distant galaxies. In every real bucket experiment, those two things — "rotating relative to space" and "rotating relative to the distant stars" — happen together. We have never been able to pull them apart, because we cannot remove the stars.

So Mach made a daring leap: maybe it's the stars. Maybe the curved water surface is the water responding to its rotation *relative to all the other matter in the universe*, not relative to any invisible absolute stage. Maybe inertia is not a property an object has all by itself, intrinsically, but a *relationship* between that object and everything else there is.

This is **Mach's principle**: the proposal that the inertia of any body — its resistance to acceleration, the very mass in $F = ma$ — is not intrinsic to the body but is somehow *determined by, and generated by, the rest of the matter in the universe*, chiefly the distant masses that dominate the cosmic budget.

Let that sink in, because the consequences are wild. If Mach is right:

- In a truly empty universe — one single object, nothing else — that object would have **no inertia at all**. There'd be nothing to be accelerated relative to, so a feather-light shove would send it to infinite speed. Inertia would be meaningless. (Berkeley's intuition, made into a physical claim.)
- The reason you feel a jolt when the train brakes is, ultimately, *the distant galaxies*. Your body is accelerating relative to the bulk of the universe's mass, and that relationship is what shoves you into the seatbelt. The seatbelt is local; the resistance it overcomes is cosmic.
- Inertia becomes a kind of gravity-like influence reaching across billions of light-years. The far-off matter, faint and uncaring, would be silently setting the terms of every push you've ever made.

I called it haunting and I mean it. There is something vertiginous about the thought that the resistance of your morning coffee mug is underwritten by the Andromeda galaxy and a hundred billion others. Einstein loved it. He found Mach's principle so compelling that he made it one of the guiding stars while building General Relativity, and he coined the very name "Mach's principle." He wanted his new theory of gravity to *contain* Mach's idea — to make inertia genuinely arise from cosmic matter.

And here is the honest, slightly melancholy ending of that story. **General Relativity does not fully deliver Mach's principle.** It captures pieces of it — there are real "frame-dragging" effects, measured by the Gravity Probe B satellite and others, in which a spinning mass really does drag the local standard of non-rotation around with it, exactly as a Machian would hope. That's a genuine, confirmed Machian whisper. But GR also permits solutions that Mach would hate: you can write down a perfectly valid GR universe that is completely empty *except* for a single rotating object, and that object still has inertia, still feels centrifugal effects, still has something to rotate "relative to." In an empty GR universe, spacetime itself plays the role of Newton's absolute stage. Einstein eventually, reluctantly, conceded that GR is not fully Machian. The principle that helped him build the theory survived only in part inside it.

So Mach's principle today is not a law of physics. It is a *hypothesis* — a beautiful, partly-confirmed, partly-frustrated hypothesis about where inertia comes from. It has never been turned into a complete, predictive theory that everyone accepts. It hovers, suggestive and unfinished, over the foundations of mechanics. Generations of physicists have tried to make it precise — Sciama, Brans and Dicke, Barbour, and others built theories reaching toward it — and each captured a facet without nailing the whole. (We'll meet the Brans–Dicke attempt again in passing when we discuss scalar fields.)

I dwell on this because it sets up the entire posture of this book. We are about to consider a framework that modifies inertia. The very fact that *inertia's origin is an open question* — that the smartest people who ever lived left it open — is what makes such a modification *thinkable* rather than crankish. You can't responsibly modify something you fully understand. But inertia we do not fully understand. There is room here. The room is real.

> **Deeper Dive: Mach's principle, frame-dragging, and why it never closed.**
>
> "Mach's principle" is notoriously not a single statement — the physicist Hermann Bondi and others catalogued at least half a dozen distinct versions. The strongest, most testable form is the claim that **local inertial frames are entirely determined by the distribution and motion of matter in the universe**, so that there is no inertia in the absence of matter and the inertial mass of a body could in principle depend on its cosmic surroundings.
>
> *What GR does deliver (the Machian whispers):*
> - **Frame dragging (the Lense–Thirring effect).** A rotating mass twists the spacetime around it, dragging the local non-rotating frame — the frame in which a gyroscope holds steady — around with it. **Gravity Probe B** (NASA, results 2011) measured the Earth's frame-dragging on orbiting gyroscopes at the predicted level (about 37 milliarcseconds per year), confirming the effect. This is genuinely Machian in spirit: the local standard of "not rotating" is *set by nearby matter's motion*, not by an aloof absolute space.
> - **Thirring's interior calculation.** A rotating massive shell drags the inertial frames in its interior — exactly the qualitative effect Mach's principle predicts, with the surrounding matter "imposing" its rotation on the inertia inside.
>
> *What GR refuses to deliver (the anti-Machian solutions):*
> - **Gödel's rotating universe** and, more simply, **Minkowski space** (the empty, flat spacetime of special relativity) contain perfectly good inertial frames *with no matter at all to define them*. In vacuum GR, the metric itself supplies the inertial structure. Mach's principle, in its strong form, is therefore *not* a theorem of General Relativity; it is at best an optional feature of particular matter-filled solutions.
> - GR's spacetime carries energy, momentum, and inertia of its own (gravitational waves propagate through vacuum). A fully relational theory would have no such free-standing inertial substrate.
>
> *The relevance here.* The framework this book develops is, in spirit, a **modified-inertia** program: it proposes that the effective inertial mass in $F = ma$ departs from its Newtonian value when an object's acceleration falls below a tiny cosmic scale $a_0$. Whether one calls that "Machian" depends on the version of Mach one means — but the *family resemblance* is direct. In the framework (Chapters 20–22), the modification of inertia is tied to a cosmic quantity: the temperature floor of de Sitter space, which is itself set by the dark-energy density of the *whole universe*. So the resistance a galaxy's stars feel in their slow orbits ends up depending on a property of the entire cosmos — a thoroughly Machian-flavored statement, even though the mechanism is thermodynamic and geometric rather than a direct sum over distant masses. I want to be careful and honest here: the framework does **not** derive Mach's principle, and it does not claim to have solved the centuries-old origin-of-inertia problem. It claims something narrower and, I think, more defensible — that *if* you let a known cosmic temperature scale modify inertia in the deep low-acceleration regime, you reproduce the observed dynamics of galaxies with the right scale. That is a real claim, and it is not a theory of everything yet, as frustrating as it may be.

---

## Modified inertia versus modified gravity: which thing are we changing?

There's a fork buried in everything we've said, and it pays to make it explicit now, because the whole back half of this book lives on one side of it.

Recall the two equations that share the word "mass":

$$ F = m\,a \qquad \text{(inertia — how it responds)} $$
$$ F = \frac{G M m}{r^2} \qquad \text{(gravity — how it's pulled)} $$

Now suppose — as Parts 1 and 4 of this book argue at length — that something is genuinely wrong with our predictions for galaxies: the stars in the outskirts move faster than the visible matter can explain. If you don't want to add an invisible particle (dark matter), you have to change one of these two equations. Which one?

**Modified gravity.** You can change the *right-hand side of the gravity equation* — say that the force of gravity itself is stronger than $GMm/r^2$ when gravity gets very weak. The pull is bigger than Newton said, so the stars orbit faster, no dark matter needed. Most of the well-known alternatives to dark matter take this road. Milgrom's original MOND can be read this way; the relativistic theory AeST (which we'll meet in Chapter 28) is squarely a modified-gravity theory.

**Modified inertia.** Or — and this is the road this book takes — you can leave gravity alone and change the *left-hand side of the inertia equation*. Say that when an object's acceleration $a$ becomes extraordinarily small, smaller than a threshold $a_0$, its inertial mass is no longer simply $m$. The *resistance to acceleration* itself weakens. Then, for the same gravitational pull, the star accelerates *more* than Newton predicted — and again it orbits faster, again with no dark matter. But the mechanism is utterly different: gravity is untouched; what changed is how matter *responds*.

![Left: a galaxy rotation curve where Newton falls off but the modified curve stays flat. Right: a fork showing modified gravity versus modified inertia](figures/ch13_mi_vs_mg_fork.png)

***Figure 13.3 — One flat rotation curve, two different equations you could change.*** Left: for a schematic disk galaxy the Newtonian (baryons-only) speed rises then falls, while both roads out of dark matter produce the same flat outer curve; the shaded gap is the 'missing' speed. Right: the fork the chapter draws. Modified gravity changes the right side of the gravity law ($F=GMm/r^2$); modified inertia — the road this book takes — changes the left side of $F=ma$ only when $a<a_0$, leaving gravity untouched and switching off in the Solar System. A schematic illustrating the chapter's central conceptual choice, not a fit to data.

**Source:** Figure generated by [`book/figures/ch13_mi_vs_mg_fork.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch13_mi_vs_mg_fork.py). The two-road framing and the framework's modified-inertia stance follow the main result paper, [doi.org/10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540), building on Milgrom (1983) MOND and the relativistic modified-gravity theory AeST, Skordis & Zlosnik (2021, PRL 127, 161302).


These two roads can look identical in a simple galaxy rotation curve — both can be tuned to fit the same flat curve. But they are *not* physically equivalent, and they make different predictions elsewhere. Modified inertia, because it changes $F = ma$ only at fantastically small accelerations, naturally leaves the Solar System untouched (planets accelerate briskly, far above $a_0$) — which, as we'll see, lets it sail past the stringent Cassini spacecraft tests that constrain modified-gravity theories. That "switch-off at high acceleration" is not a patch bolted on; it falls out of the structure. It's one of the framework's quieter strengths.

Milgrom himself — the originator of MOND, whom we'll properly meet in Chapter 17 — has long emphasized that a *modified-inertia* reading of MOND is possible and in some ways more natural, and he wrote foundational papers on it in 1994 and 1999. The framework in this book builds directly on that modified-inertia tradition, marries it to the de Sitter temperature we'll develop in Chapters 14–15, and finds the acceleration scale $a_0$ emerging with the right magnitude.

I'll say plainly, as I'll keep saying: modified inertia is a **minority** position. The mainstream overwhelmingly favors a dark-matter particle, and has good reasons (the cosmic microwave background and galaxy clusters chief among them, which we covered in Part 2 and will revisit in Part 6). A responsible reader should hold the modified-inertia road as *one live possibility among several*, attractive for specific reasons, burdened with specific unsolved problems — not as established fact. But it is a respectable road, traveled by serious physicists, and it is the road we're on. Knowing *that inertia's origin is open* is what makes the road passable at all.

> **Margin aside.** A subtle point worth flagging now and developing later: a modified-inertia theory has to be careful about the equivalence principle — the fifteen-decimal-place equality of inertial and gravitational mass from the MICROSCOPE satellite. If you change inertia, you risk breaking that equality and predicting that different materials fall at different rates. The framework dodges this because its modification depends only on *acceleration*, not on what an object is made of, and switches off entirely in the high-acceleration regime where every equivalence-principle test has ever been run. The tests live where the modification sleeps. We'll return to this in Chapter 21.

---

## Where this leaves us

Let me gather the threads, because we covered a lot of ground and the next chapters depend on it.

Inertia is the resistance of matter to a change in its motion, measured by mass, and quantified by Newton's $F = ma$. That equation is one of the most successful in science — and it is a *description*, not an *explanation*. It tells us the price of acceleration without telling us who collects it.

The mass in that equation, the **inertial mass**, coincides to fifteen decimal places with **gravitational mass**, the entirely different quantity that governs how strongly an object feels gravity. Nobody knows why. General Relativity assumes the equality and builds on it; it does not derive it.

When we ask "acceleration relative to *what*?", Newton answered "absolute space" — an invisible, unaffectable stage — and defended it with the spinning bucket. Many found that an empty name for the mystery. **Mach** proposed instead that inertia comes from the rest of the matter in the universe, the distant stars and galaxies; that in an empty cosmos there would be no inertia at all. Einstein found Mach's principle so beautiful he built it into the foundations of General Relativity — and then found, to his lasting discomfort, that GR contains Mach's idea only in part. Mach's principle remains a hypothesis: partly confirmed (frame-dragging is real and measured), partly refused (empty-universe solutions have inertia anyway), never closed.

So the origin of inertia is, in 2026, a genuinely open question. That openness is the room in which this book's framework lives. The framework is a **modified-inertia** proposal: it leaves gravity alone and changes how matter resists acceleration, but only at accelerations far below anything in the Solar System — and it ties that change to a temperature drawn from the geometry of our accelerating universe. Whether it's right is a matter for the later chapters and, ultimately, for telescopes. What I hope you carry out of *this* chapter is the felt sense that inertia was never the simple, settled thing it pretends to be. The mystery was always there, hiding in the shopping cart. We are about to propose one possible thread out of the labyrinth — not the only thread, not a proven thread, and not a theory of everything yet, as frustrating as it may be. But a thread worth following.

Next, in Chapter 14, we pick up the strangest ingredient: the discovery that *acceleration itself produces a temperature* — the Unruh effect — which will turn out to be the physical heart of how this framework modifies the very inertia we've just spent a chapter learning to respect.

---


![Curve of effective inertia ratio versus acceleration, rising from near zero below a0 to one above it](figures/ch13_inertia_switchoff.png)

***Figure 13.2 — Where the modification sleeps and where it wakes.*** The purple curve is the framework's effective inertia ratio $m_{\rm eff}/m=\mu_{\rm fw}(a/a_0)$ as a function of an object's acceleration. Far above the cosmic scale $a_0$ — in the Solar System, where every equivalence-principle test (MICROSCOPE, Eöt-Wash) and the Cassini bound live — the ratio is indistinguishable from Newton's value of $1$, so the modification is invisible. Only in galaxy outskirts, where accelerations fall to a fraction of $a_0$, does inertia weaken. Computed from the framework's own interpolation function; the value $a_0=9.36\times10^{-11}$ m/s$^2$ is an input, not a derived number.

**Source:** Figure generated by [`book/figures/ch13_inertia_switchoff.py`](https://github.com/carlzimmerman/zimmerman-formula/blob/main/book/figures/ch13_inertia_switchoff.py). Framework interpolation $\mu_{\rm fw}(x)=(\sqrt{1+4x^2}-1)/(2x)$ and scale $a_0$ from the main result paper, [doi.org/10.5281/zenodo.20721540](https://doi.org/10.5281/zenodo.20721540); the modified-inertia tradition follows Milgrom (1994; 1999).

## Summary

- **Inertia** is the resistance of an object to any change in its state of motion. Its measure is **mass**, and the relationship is Newton's second law, $F = ma$. The equation describes inertia superbly but does not explain its origin — it says *how much* matter resists, never *why* or *against what*.
- **Inertial mass** (resistance to being accelerated by any force) and **gravitational mass** (the "charge" that couples an object to gravity) are conceptually unrelated, yet measured to be equal to about one part in $10^{15}$ (MICROSCOPE satellite, 2022). This **equivalence** is the seed of General Relativity, which assumes it rather than deriving it.
- **Newton's bucket** argues that inertial effects (the curving water surface) depend on rotation relative to *space itself*, not relative to nearby matter — Newton's case for **absolute space**, an invisible, unaffectable stage. Leibniz, Berkeley, and later Mach rejected it as an unobservable name for the mystery.
- **Mach's principle** is the hypothesis that inertia is not intrinsic but is generated by the rest of the matter in the universe — the distant stars. In a truly empty universe, there would be no inertia at all. Einstein built it into General Relativity's foundations, but GR delivers it only partially: frame-dragging (measured by Gravity Probe B) is a genuine Machian effect, while empty-universe solutions retain inertia, against Mach.
- A **modified-inertia** program changes the left side of $F = ma$ at very low accelerations, rather than changing gravity. It is a respectable minority response to galaxy dynamics, naturally Solar-System-safe (the modification switches off at high acceleration), and the road this book takes — building on Milgrom's 1994/1999 modified-inertia work. It does **not** derive or solve Mach's principle; it claims only that a known cosmic temperature scale, allowed to modify inertia in the deep low-acceleration regime, reproduces galactic dynamics with the right scale. Not a theory of everything yet, as frustrating as it may be.

---

## Questions

1. **(Easy.)** In your own words, explain why a fully loaded shopping cart is harder to start moving than an empty one *even on a perfectly frictionless surface, even in deep space*. Which quantity is responsible, and which of Newton's equations describes it?

2. **(Easy–medium.)** Inertial mass and gravitational mass are conceptually different ideas. State what each one measures, and describe one everyday observation (such as dropping two different objects) that would look strange if the two masses were *not* equal.

3. **(Medium.)** Walk through Newton's bucket experiment stage by stage and explain why Newton concluded that the curving of the water's surface cannot be caused by the water's motion *relative to the bucket*. What did he say it was caused by instead, and what was Mach's objection to that answer?

4. **(Medium–hard.)** The MICROSCOPE satellite measured the Eötvös parameter to be consistent with zero at the level of $\sim 10^{-15}$. Explain in words what a *nonzero* result would have meant physically — what would we observe in a falling-bodies experiment? — and why a modified-inertia theory of galaxy dynamics must take this constraint seriously. (Hint: think about where, in acceleration, these tests are performed versus where the modification is supposed to act.)

5. **(Hard / discussion.)** "Mach's principle is not a theorem of General Relativity." Defend this statement using *both* a confirmed Machian effect that GR predicts *and* a GR solution that violates Mach's principle. Why might Einstein have found this outcome disappointing, given his original motivations?

6. **(Research-level.)** The framework in this book is a *modified-inertia* program in which the change to inertia is tied to a cosmic temperature scale set by dark energy. Sketch how such a proposal might be considered "Machian in spirit," and then articulate the strongest reason it would be *wrong* to call it a derivation or solution of Mach's principle. In your answer, distinguish clearly between (a) reproducing the correct acceleration scale for galaxy dynamics and (b) explaining the microphysical origin of inertia itself — and identify which of these the framework can honestly claim.
