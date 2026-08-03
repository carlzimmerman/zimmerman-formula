# What in the World Is a Dimensionless O(1) Prefactor?

### And why it's the only part of your claim that's actually yours

*Plain English. No equations you can't skip.*

---

## 1. Start with the two words

**Dimensionless** means the number has no units attached. Not metres, not seconds, not kilograms — just a
number. If you measure a doorway in feet and I measure it in metres, we get different numbers. But if we both
measure the *ratio* of its height to its width, we get the *same* number. That ratio is dimensionless. It's
real, it's a fact about the doorway, and it doesn't care what ruler you used.

**O(1)** — read "order one," or "order unity" — means the number is somewhere in the neighbourhood of 1.
Maybe 0.5, maybe 2, maybe 1/(2π) ≈ 0.16. Not 10⁶. Not 10⁻⁴³. Physicists say "O(1)" when they know a number is
*mundane in size* but don't know its exact value.

Put them together and a **dimensionless O(1) prefactor** is: *a plain number, near 1, sitting in front of an
equation, whose exact value nobody has derived.*

---

## 2. Why there's a hole there in the first place

Here's the thing that trips everyone up. **Dimensional analysis is enormously powerful and it always stops
one step short.**

Suppose you want to know how long a pendulum takes to swing. You have a length L and gravity g. You ask: what
combination of L and g gives me a *time*? There's essentially only one answer: √(L/g). So you know, without
solving anything, that the period is proportional to √(L/g). That's a huge amount of information for free.

But the actual answer is **2π**√(L/g). Dimensional analysis cannot give you the 2π. It never can. The 2π comes
from actually solving the equation of motion — from the real dynamics, not from bookkeeping the units.

That gap is where the prefactor lives. **Units tell you the shape of the answer. Only the theory tells you the
number.**

---

## 3. Your case, in one line

You want to know the acceleration scale a₀ where gravity starts behaving strangely in galaxies. You have the
speed of light c, Newton's constant G, and the density of dark energy ρ_Λ. You ask: what combination gives an
*acceleration*?

The answer is c√(Gρ_Λ). There's basically nothing else it could be. So:

> a₀ = **κ** · c√(Gρ_Λ)

and the **κ** is your dimensionless O(1) prefactor. You say it's **½**.

That c√(Gρ_Λ) part? **That isn't yours.** Milgrom wrote essentially that in 1994, and wrote a whole paper
called *"The a₀–cosmology connection in MOND"* in 2020. Dimensional analysis is public property — anyone who
lines up c, G and ρ_Λ gets the same form.

**The κ = ½ is yours.** That's not a small thing, and it's not a large thing. It's exactly one thing.

---

## 4. Why prefactors are not trivia

It's tempting to think "it's just a number out front, who cares." The history of physics says otherwise. The
prefactor is routinely where the entire content lives:

- **Black hole entropy.** Bekenstein worked out that a black hole's entropy is proportional to its horizon
  area. Enormous insight. But the coefficient — that it's exactly **¼** of the area in Planck units — took
  Hawking's full quantum calculation. That ¼ is now a benchmark every candidate theory of quantum gravity has
  to reproduce. Whole research programmes are judged by whether they get one fraction right.
- **Unruh temperature.** An accelerating observer sees a warm vacuum, at temperature proportional to their
  acceleration. The coefficient is **1/2π**. That 2π is not decoration — it's the signature that the effect is
  really thermal, tied to a periodicity in imaginary time. Get a different number and you've got a different
  physical mechanism.
- **The Chandrasekhar mass.** Roughly (ℏc/G)^(3/2)/m_p², which gets you into the right ballpark for a white
  dwarf. But the actual limit involves solving a specific stellar structure equation, and the resulting number
  is what tells you which stars explode.

In every case: the scaling tells you *what kind of thing is going on*. The prefactor tells you *which specific
theory is right*.

So a derived κ would be a serious result. **A fitted κ is a serious claim.** Those are different, and the
difference is the whole ballgame.

---

## 5. Why yours is genuinely hard

Your κ = ½ can be written a couple of other ways, and it's worth seeing them because they show where the
difficulty sits:

> a₀ = cH_Λ / Z, with **Z = 2√(8π/3) = 5.78881**

The 8π in there is Einstein's (it's the 8π in the field equations). The 3 is Friedmann's (from the expansion
equation). And here's the thing — **they cancel.** They appear on both sides of the conversion between ρ_Λ and
H_Λ and drop out. What's left over is the **2** — which is just 1/κ wearing a different hat.

You can even write it as Z² = 4·(8π/3), which makes it look like the whole mystery is a single factor of 4.
That framing is appealing, and I should be straight with you: **it isn't progress, it's rephrasing.** Saying
"Z² = 4·(8π/3)" and saying "κ = ½" are the *same statement*. Neither one explains the other. It's a nicer way
to display the puzzle, not a step toward solving it.

Three specific routes to deriving κ have been tried and closed:

1. **Forcing it from quantum consistency** — no ghosts, unitarity, holographic bounds. These constrain the
   *shape* of the modification, not its *normalisation*. Wrong tool for the job.
2. **The κ-linear family.** There's a natural class of constructions you'd hope would pin κ. It turns out
   every member scales as κ^n identically — so the whole family is a *relabelling* of κ, not a determination
   of it. That's a theorem, not another near miss.
3. **The CKN degrees-of-freedom bridge.** There's a tempting constant, (3/8π)^(1/4) = 0.5878, that looks like
   it might be the missing link. It satisfies (3/8π)^(1/4) = √(2/Z) **exactly**. Which means it's an algebraic
   rewriting of Z — the same information in a costume. No new content.

The pattern in all three: **you cannot get a number out of an argument that never had that number in it.** To
derive κ you need a theory that actually computes the normalisation — the equivalent of Hawking's calculation,
not Bekenstein's scaling argument.

---

## 6. So could we just *measure* it?

That's the obvious move, and it's where the current honest answer is uncomfortable.

The competing value in the literature is κ = 1/2π (Milgrom 2020). The difference between that and your ½ is
**7.87%** in a₀. Small — but a 7.87% measurement of a₀ doesn't sound impossible. Galaxy rotation curves are the
natural instrument.

It doesn't work yet, and the reason is specific. To get a₀ out of a rotation curve you have to assume a
**transition shape** — how gravity hands over from Newtonian to modified as acceleration drops. Nobody knows
that shape. And when you try five plausible shapes, each one prefers a *different* a₀:

| assumed shape | prefers a₀ of |
|---|---|
| x/(1+x⁴)^(1/4) | 1.244 |
| x/√(1+x²) | 1.192 |
| √(1+1/y) | 1.154 |
| deep limit only | 1.059 |
| exponential | 0.938 |

That's a **30.6% spread** — nearly four times the 7.87% you're trying to measure. **The uncertainty in the
shape is bigger than the thing being measured.** Four of the five lean your way and none reaches 3σ, so the
data likes κ=½ but cannot confirm it.

And a trap worth knowing: the relation g_obs² − g_bar² = a₀·g_bar, which looks like a clean one-number
extraction of a₀, is *secretly one of those shapes* — it's the √(1+1/y) kernel written as a straight line. It
gives a₀ exactly right on data that follows that kernel and is off by 10% or 84% on data that doesn't. It feels
shape-free. It isn't.

---

## 7. What this means for you, honestly

- The **form** a₀ ∝ c√(Gρ_Λ) is public property. Dimensional analysis gives it to anyone.
- The **κ = ½** is your distinctive claim. Narrow, specific, and falsifiable — which is what makes it a real
  claim rather than a vibe.
- It is **fitted, not derived**, and three routes to deriving it are closed for structural reasons rather than
  from lack of effort.
- Present data **leans** your way (1.5σ–2.7σ depending on shape) but **cannot resolve** κ, because the shape
  systematic is four times the signal.
- Fixing it needs an a₀ measurement good to ~3% that *doesn't* assume a shape. The only regime that's naturally
  shape-free is the deep-MOND limit — where every candidate shape agrees — and that's also where the data is
  thinnest.

The honest version of your claim is a good one: *here is a specific number, here is why nobody can derive it
yet, and here is exactly what observation would settle it.* That's a normal, respectable position in physics.
Pretending the number is derived would be the only way to make it a bad one.

---

### The one-sentence version

A dimensionless O(1) prefactor is the plain number that dimensional analysis can never give you and only a
complete theory can — which is why it's simultaneously the smallest-looking part of your equation and the only
part that's actually yours.
