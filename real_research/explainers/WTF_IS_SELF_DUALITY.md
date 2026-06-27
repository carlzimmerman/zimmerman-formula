# WTF is self-duality? — and what Koide's 2/3 secretly is

*A plain-language explainer, written for Carl Zimmerman, June 2026. The point: "self-duality" is the hidden shape behind Koide's 2/3, and the de Sitter–Unruh framework is full of self-dualities too — so this note explains the idea, then states honestly whether the framework's self-dualities and Koide's are the same thing or just rhyme.*

---

## The idea in one line

> **A self-duality is a transformation that is its own undo button** — do it twice and you're back where you started. The special configurations that *don't move at all* under it are the **self-dual points**, and they're always the perfectly *balanced* ones.

A transformation that is its own inverse is called an **involution**. The classic example:

- Take the swap **(x, y) → (y, x)** (reflect across the diagonal). Do it twice — back to start. It's an involution.
- Which points *don't move?* The ones with **x = y** — the **45° line.** That's the self-dual set: the perfectly balanced configurations where the two things being swapped are equal.

That's the whole concept. **Self-dual = sits exactly on the fence between two things being swapped.** 45°. Equal parts. The balance point.

## Why physicists care

Self-duality keeps showing up at the deepest points in physics, because "balanced under a swap" is often where something special happens:

- **Electromagnetism:** swapping electric ↔ magnetic fields (E → B, B → −E) is a duality; self-dual field configurations (instantons) are the lowest-energy, most stable ones.
- **The Ising model** (magnets): Kramers–Wannier duality swaps high temperature ↔ low temperature; the self-dual point is *exactly* the critical temperature where the magnet transitions.
- **String theory / S-duality:** swaps strong coupling ↔ weak coupling; the self-dual point is where a theory is its own mirror.

The pattern: **the self-dual point is where the interesting transition lives.** Find the involution, find its fixed point, and you've often found the physics.

## Koide's 2/3 is secretly a self-duality

Here's the part that connects to your lepton work. Write the three charged-lepton masses as a vector of their square-roots: **(√mₑ, √m_μ, √m_τ)**. Now split that vector into two pieces:

- its **"democratic" part** — how much it points along (1,1,1), the all-equal direction;
- its **"perpendicular" part** — everything left over (the spread between generations).

**Koide's Q = 2/3 is *exactly* the statement that these two parts are equal** — the √-mass vector sits at **45°** to the democratic axis. It's a self-dual point. In fact Q = 2/3 is the fixed point of a specific involution on Q itself (Q → Q/(3Q − 1), the "swap the singlet and the doublet" map).

So "why is Koide 2/3?" is really asking: **"why does the lepton √-mass vector sit exactly on its 45° self-dual fence?"**

## The catch that kills easy answers (the circularity trap)

Here's why "it's self-dual!" doesn't, by itself, explain anything — and this is the trap I have to keep myself out of. There's an exact identity (verified in this repo, `reviews/koide_circularity_INDEP_verify.py`):

$$Q = \frac{1}{3} + \frac{r^2}{6}$$

where **r** is the amplitude of the √-mass vector's spread. So **Q = 2/3 ⟺ r = √2**, *exactly and always.* That means:

> Saying "force r = √2" and saying "assume Q = 2/3" are the **same statement.** And the 45° self-dual point is the *universal* balance point of *any* vector in *any* dimension — it carries **zero** information about leptons specifically.

So self-duality tells you the *shape* of the answer (45°, √2) but **not why leptons land there.** Anyone who "derives" √2 by fitting the masses has just smuggled 2/3 back in. A real derivation has to make √2 *emerge* from a structure that never mentions √2, 45°, or 2/3. That's a brutally high bar — and it's the bar we hold every swing to.

## The framework is full of self-dualities too

The de Sitter–Unruh framework has its *own* self-dual structures — we catalogued **seven** of them (`reviews/selfduality_constant_catalog.py`). They sort by which constant they carry:

| framework self-duality | its constant |
|---|---|
| μ_fw constitutive law, balance at x=1 (**at the MOND scale a₀**) | **golden φ** (1/φ = 0.618) |
| dS-Unruh quadrature T(a)=√(a²+a_dS²), channel balance | **√2** |
| the memory-kernel θ(0) (DC weight) | **√2** |
| Koide's singlet/doublet involution | **√2** |
| inverted-black-hole UV/IR radius | **√Z** (= 2.406) |
| dimension d=3, seesaw 3/2 | integer/rational |

So your theory genuinely lives in "self-dual land," and **three** of its self-dualities carry the same √2 Koide does. That's the seduction. Here's where it bottoms out — honestly, with a correction to something *I* got wrong.

## The honest answer *(computed — including a √2 I mislabeled)*

The most seductive one is the **dS-Unruh quadrature**: T(a) = √(a² + a_dS²) is a real two-channel balance, and where the channels are equal you get a genuine native **√2**. That part is real — it's a fourth √2 in your spine, not numerology.

**But I'd placed it at the wrong scale, and the computation caught me.** The channel balance sits at **a = a_dS = cH_Λ = Z·a₀ ≈ 5.79 a₀** — the *horizon floor* scale — **not at a₀, the MOND scale.** At a₀ itself the ratio is only √(1 + 1/Z²) = 1.0148, *not* √2; and your framework's *own* special value at a₀ is the **golden φ**, not √2. So the catchy "√2 sitting right at the MOND scale!" was a conflation, **wrong by a factor of Z.** (This is the discipline working: I planted a seductive claim, and the script refuted it.)

And even granting the real √2 it *does* have, it doesn't reach Koide — for a clean structural reason:

> Your framework's √2's are **1+1 channel-balances** living on the **1-D acceleration axis** (a simple "swap the two channels" symmetry). Koide's √2 is a **1+2 doublet-split** living in **3-D generation space** (the S₃ symmetry of three families). The "2" means *two channels* in one and *the dimension of a doublet* in the other. **Same number, completely different worlds** — and the only bridge your spine has between them (the inertia response μ_fw) is flavor-blind, so it provably can't carry one into the other.

**The verdict:** the seduction bottoms out — fully mapped, not hand-waved. Your self-dualities are real and beautiful (φ at the MOND scale, √2 at the horizon scale, √Z in the black-hole duality), but none of them is *Koide's* √2. The missing piece is a **lepton-selective family symmetry** (Sumino-class) that lives *outside* the gravity spine — the open 45-year problem itself.

## So what *is* self-duality, in one line?

**The "balanced under a swap" point — 45°, equal parts, the fence between two things** — and it's the hidden shape of Koide's 2/3, of phase transitions, and of the deepest dualities in physics. Your framework has its own self-dual points; whether any of them is *Koide's* self-dual point is exactly the question we keep swinging at — with the rule that √2 has to *earn* its way out, not get fitted in.

---

*Related reading in this repo: `WTF_IS_A_LEPTON.md`, and the computed results in `reviews/koide_circularity_INDEP_verify.py`, `reviews/koide_two_sqrt2.py`, `reviews/framework_selfdualities.py`, and `reviews/koide_quadrature_sqrt2.py`.*
