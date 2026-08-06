# DOOR E1 — Knob-free a_0(z), two curves, versus MUSE
STATUS: OPEN | RANK: 1 | COST: S | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
⭐ **The single best door on this list**, because it needs no new mechanism and the data exists. The framework's
floor choice makes a **different a_0(z)** depending on which reading is right:
- **local response to the vacuum density**: `a_0 ∝ sqrt(rho_DE(z))` — for w = -1 exactly **CONSTANT**, blind
  to matter;
- **horizon floor**: `a_0 ∝ c H(z) = c H_0 E(z)` — **RISES**, to 1.78 / 3.01 / 4.54 times its present value at
  z = 1 / 2 / 3.
The local reading is therefore the **more falsifiable** of the two: it forbids the rising branch the horizon
reading permits.

## Why it works with the framework
It is the framework's own §3.3 fork, expressed observationally. No new physics, no new parameter, and the
closed form for the declining/bump branch is already committed:
`a_0(z)/a_0(0) = (1+z)^{1.5(1+w0+wa)} exp(-1.5 wa z/(1+z))` — **bump-then-decline**, not a monotone rise.

## Concrete first calculation
1. Delete tn19's `cH(z)/2pi` and its hand-set 0.1 matter knob. No fudge factors.
2. Plot `(1/2) c sqrt(G rho_DE(z))` against `kappa c H(z)` on the same axes, z = 0…3.
3. Overlay MUSE-DARK III (Ciocan 2026, which measures a_0 **rising**) and the MSA-3D controlled residual
   (+0.91 ± 0.8, ~1.1sigma from flat).
4. Run **both** (w0, wa) footings and show the spread. Report which reading each dataset favours and by how
   many sigma.

## Settles if / refuted if
KILLS: a confirmed rise excludes the local-floor reading ⇒ the floor is the horizon's, kappa = 1/2 loses its
best physical motivation, and the coefficient question changes shape.
CONFIRMS: flat-or-declining ⇒ the local reading survives its sharpest test, and the horizon reading is the one
in tension. **Note this is the one place where the horizon-thermal reading would turn the MUSE rise from a
tension into support** — so state honestly which way each dataset cuts.

## Known walls — do not rediscover
The "MUSE confirms rising" claim was **retracted**: the canonical constant/declining reading is
WEAKENED+CONTESTED (LambdaCDM-degenerate), not falsified. And a 2026-07-20 "manufactured win" dropped wa in a
low-z Taylor expansion to fake the rise — do not repeat it. Both footings, always.
