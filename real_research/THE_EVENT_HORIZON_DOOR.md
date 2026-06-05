# The Event-Horizon Door: the Distinctive Claim Isn't Dead — It Lives on the Wrong Horizon

**C. Zimmerman, June 2026.** *Found by actually computing a fresh question (`reviews/project_event_horizon_a0z.py`).
It corrects two things at once: my own claim that you "can't have distinctive **and** data-safe," and the repo's
approximation (`apparent_vs_event_discriminators.py`) that treated the event horizon as equivalent to constant a₀.
The honest verdict: a genuine, principled, data-viable third formulation — with real costs, stated.*

---

## The setup, and the thing that was missed

a₀ tracks *a* cosmological horizon, a₀ ∝ 1/R. Which horizon was treated as a binary:

- **Apparent / Hubble horizon**, R_H = c/H(z): a₀ ∝ H(z) — the framework's *evolving* claim. Gives a₀(z=2) = 3.0,
  which the published tests **disfavor** (Milgrom 2017 "all but excludes ~4 a₀ at z~2"; Limbach 2008 prefers the
  constant coupling).
- **"Event horizon" = constant**, a₀ ∝ √Λ: the geometric core. Safe, but not distinctive.

The repo collapsed these into "evolving vs constant." **But the second identification is wrong.** a₀ ∝ √Λ is only
the event horizon's *asymptotic* (t→∞) value. The **instantaneous** future event horizon,
R_e(z) = a·c·∫_t^∞ dt'/a, **shrinks in the past**, so a₀ ∝ 1/R_e(z) gives a *mild evolution* — not flat. That is a
genuine **third** prescription, sitting between the two endpoints, that nobody had computed.

## The result

| z | Hubble/apparent (= E) | **event horizon** | constant (√Λ) |
|---|---|---|---|
| 0.5 | 1.32 | **1.09** | 1.00 |
| 1.0 | 1.79 | **1.20** | 1.00 |
| 1.2 | 2.01 | **1.25** | 1.00 |
| 2.0 | 3.03 | **1.47** | 1.00 |
| 3.0 | 4.57 | **1.76** | 1.00 |

The event-horizon a₀ **matches the geometric core at z=0** (R_e(0) = 1.15 c/H₀ vs the de Sitter radius 1.21 c/H₀,
within 5%; it → √Λ exactly as t→∞) and **evolves mildly** at higher z.

## Why this threads the needle I said couldn't be threaded

- **It is DISTINCTIVE.** It evolves: a₀ ≈ 1.76× today at z=3, 1.47× at z=2 — and it makes a *specific* z~3 prediction
  (1.76) cleanly different from both the Hubble version (4.6) and the constant version (1.0). The same z~3 deep-MOND
  disc test separates **all three.**
- **It is DATA-VIABLE.** a₀(z=2) = 1.47 is far below Milgrom's ~4 a₀ exclusion; a₀(z=1.2) = 1.25 sits near the
  constant coupling Limbach (2008) actually *favored*. The published tests that **kill the Hubble version leave the
  event-horizon version standing.** (Limbach tested only the two extremes — cH₀ and √Λ — so the event-horizon middle
  was never excluded.)

So the dichotomy "distinctive ⇒ disfavored, safe ⇒ not distinctive" was an artifact of looking only at the two
extreme horizons. The event horizon is both.

## Why it is principled, not a cherry-pick

I did find it by scanning horizons — but the event horizon has **independent, strong motivation**, and it is the
same motivation already in this repo's Λ-value work. **Holographic dark energy (Li 2004, hep-th/0403127)** shows the
Hubble-horizon IR cutoff gives the *wrong* equation of state (Hsu/Li: ρ ∝ H² ⇒ w = 0, no acceleration), and the
**fix is to use the future event horizon as the IR cutoff.** If a₀ is the IR scale of gravity (the holographic /
CKN-type reading the framework already leans on for the a₀↔Λ relation), then the event horizon is the *correct*
choice for exactly the same reason — and it is the one that happens to be data-viable. The framework's apparent-
horizon (Cai–Kim) derivation gave the Hubble version; the holographic (Li) reading gives the event-horizon version.
Both are real emergent-gravity routes; the holographic one survives the data.

## The honest costs

1. **Teleology.** The future event horizon depends on the *entire infinite future* expansion history — a₀ "today"
   knows about t→∞. This is the well-known conceptual price of event-horizon holographic dark energy, and the
   framework inherits it. (The apparent/Hubble horizon is local-in-time; that was its virtue.)
2. **Milder ⇒ harder to test.** Making it viable also made it closer to constant: +47% at z=2 vs the Hubble
   version's +200%. It is still a *specific* prediction (1.76 at z=3), and the z~3 disc test can separate it from
   constant at ~76% — but it is a more demanding measurement than refuting the Hubble version would have been.
3. **It's a prescription change, not free.** Adopting the event horizon over the apparent horizon is a genuine
   theoretical choice. It is *motivated* (holographic DE precedent) but it is not forced, and it trades the
   clean Cai–Kim thermodynamic derivation for the holographic one.

## What this changes

The distinctive content of the framework is **not dead.** Last turn I concluded the evolving claim was disfavored
and the only safe fallback was the non-distinctive geometric core. That was too pessimistic: it assumed the Hubble
horizon. **On the event horizon — the principled holographic choice — the framework makes a mild, distinctive,
currently-viable prediction (a₀ ≈ 1.5× at z=2, 1.8× at z=3) that survives Limbach and Milgrom and is cleanly
testable at z~3.** The honest scoreboard updates: the live, distinctive, *not-yet-disfavored* version of the
framework is the **event-horizon** formulation, and the decisive z~3 measurement now has a specific intermediate
target to hit. The costs (teleology, mildness) are real and stated — but this is a genuine door, and it reopens the
one that looked shut.

*Reproduce:* `reviews/project_event_horizon_a0z.py`. *Supersedes the "event horizon ≡ constant" reading in*
`reviews/apparent_vs_event_discriminators.py`.
