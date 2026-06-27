# Novelty Check — Inverted Black Hole / a₀_BH = κ_BH/Z

**Carl's question: "Is it novel?"** · 2026-06-26 · LOCAL ledger (do NOT git-push)

Source paper: `real_research/papers/INVERTED_BH_DUALITY_2026.md` (DOI 10.5281/zenodo.20947913)

Method: four independent prior-art agents, ~28 WebSearches total + targeted fetches
(McCulloch QI arXiv:1004.3303 / 1610.06787; Milgrom vacuum-effect astro-ph/9805346;
Verlinde 1611.02269; van Putten 1709.05944; AeST stealth-BH 2412.15395; Hernandez–Sussman–Nasser
bounding-curvature; MOG shadow/ISCO 1502.01677). Algebra re-derived in Python. Caveat carried
by every agent: search indexes US/indexed literature only — the Zimmerman corpus itself returns
zero hits, so this is novelty **vs the indexed literature**, not a proof of global originality.

---

## The construction, three layers

The paper takes the framework's published cosmic law **a₀ = κ_dS/Z** (Z = 2√(8π/3) ≈ 5.789)
and applies the *same* law to a real black-hole horizon:

- **(A) Algebra:** r_cross where g(r)=GM/r² equals a₀_BH ⟹ **r_cross = √Z · r_s = 2.406 r_s**, mass-independent.
- **(B) Construction:** **a₀_BH = κ_BH/Z = c⁴/(4GMZ)** — a *per-black-hole* acceleration scale from that BH's *own* surface gravity.
- **(C) Interpretation:** universal 2.406 r_s (photon-sphere–to–ISCO band) + self-cancellation to *exactly-GR* (a NULL) + a uniqueness proposition ("only the cosmic horizon survives").

---

## Layer A — r_cross = √Z · r_s = 2.406 r_s

**Verdict: NOT NOVEL.** This is the textbook Milgrom transition / MOND radius
r_t = √(GM/a₀) (set GM/r² = a₀, solve), standard in every MOND review and in
MOND-in-Schwarzschild work (e.g. arXiv:1705.06356 writes R_c = α(GM/a₀)^½; review
arXiv:2501.17006). The operation is decades old. The only fresh content is the *number*
2.406 — and that number is purely inherited from substituting a₀_BH = c⁴/(4GMZ) (Layer B):
with the **cosmic** a₀ the identical formula gives r_t ≈ 10¹¹ r_s for a 10 M_⊙ hole (the
"HUGE" radius the prompt correctly flags). So A carries **zero independent novelty**; given B it
is a one-line identity (the M² cancellation is forced the instant a₀ ∝ 1/M). The paper's own
A/B/C decomposition is vindicated — A is the dependent layer.

## Layer B — a₀_BH = κ_BH/Z (the per-horizon construction) ← the real question

**Verdict: NOVEL ONLY AS AN UNREMARKABLE RE-APPLICATION — "genuinely new pending fuller review," NOT proven novel.**

Both ways:

- **Against novelty (the GENUS is old).** "a₀ = (horizon surface gravity)/O(1)" is not new — it is
  the framework's *own* published cosmic law, and it has heavy precedent for the **cosmic** horizon:
  - **Milgrom, vacuum-effect a₀** (astro-ph/9805346): â₀ = 2c√(Λ/3), thermal a_c = a₀/2π —
    structurally *identical* template (surface gravity / constant), constant 2 or 2π vs Z=5.789, always cosmic.
  - **Verlinde** (1611.02269): a₀ ≈ cH₀ — same cosmic-horizon genus.
  - **van Putten** (1709.05944): holographic inertia from the cosmic horizon.
  - **Padmanabhan**-lineage entropic gravity; **Smolin**; massive-gravity graviton-mass derivations.
  None of these is per-object; all feed the *single* cosmic horizon to mint *one universal* a₀.

- **For a surviving (modest) novelty (the SPECIES is unclaimed).** No search hit performs the specific
  move of feeding a **real black hole's own** surface gravity κ_BH = c⁴/4GM through the **same constant Z**
  to define a **per-object** a₀_BH = c⁴/(4GMZ). The entire horizon-MOND literature inverts the relation
  onto exactly one horizon (the cosmic one). Assigning each real BH its own MOND scale appears unclaimed
  in the indexed literature.

- **Closest precedent — McCulloch Quantized Inertia / MiHsC** (arXiv:1004.3303, 1610.06787):
  **closest IN SPIRIT, and it is genuinely the nearest miss.** QI makes inertia the response to a
  horizon bath and sets the acceleration scale by a competition between a **local Rindler horizon** and
  the **cosmic** horizon — the same two-horizon structure, and the same "evaluate inertia-from-a-horizon
  near a body" instinct. But QI writes a₀ = 2c²/Θ from the *cosmic* Hubble horizon (Θ); it does **not**
  write a₀_BH = κ_BH/Z, does not mint a per-black-hole scale from that BH's surface gravity, and produces
  no 2.406 r_s crossover or BH-shadow/ISCO/ringdown null. So QI is the right neighborhood and the honest
  "who got closest," but it does **not** contain Layer B.

Net on B: the form a₀=κ/Z and the horizon-bath idea are **inherited, not new** — Carl must not claim
those. The *per-BH application* is non-standard and was not found in prior art, so it is **plausibly
original pending fuller (arXiv/ADS title) review** — but it is a near-trivial dimensional re-application
of an existing law, so "novel" here means "an unclaimed re-application," not a new physical mechanism.

## Layer C — 2.406 r_s universality + self-cancellation NULL + uniqueness

**Verdict: physics CONCLUSION not novel; the packaging (duality + two-criterion uniqueness) modestly novel as synthesis.**

- The **null itself is already in print.** A modified-*inertia* MOND theory yielding *exactly-GR*
  strong-field observables is the standard MI-vs-MG distinction (Scholarpedia MOND; arXiv:1704.05116),
  and AeST **stealth black holes** have exactly-GR (Reissner–Nordström, q=1) geometry —
  **Skordis & Złośnik, arXiv:2412.15395**, which the paper cites and correctly concedes is *null-vs-null*
  with this framework. So "MI → exactly-GR BH" is NOT a new result.
- Ingredients are textbook: Hartle–Hawking horizon regularity for the geodesic observer (no bath),
  covariance + equivalence principle absorbing any f(r/r_s), Milgrom-1994 proper-acceleration MI.
- What is the paper's **own**: the explicit **mass-cancellation universality** (2.406 r_s for every BH
  in the photon-ring/ISCO band) packaged as a forced *duality*, plus the **two-criterion uniqueness
  proposition** — that the cosmic a₀ is the unique acceleration that is (1) not sourced by local matter
  *and* (2) not removable by local free-fall. No agent found that specific assembly in prior art. It is
  conceptual/pedagogical synthesis, **not a new testable prediction** (the empirical content is a null
  the framework's own host theory already predicts).
- Adjacent prior art worth knowing: **Hernandez–Sussman–Nasser** bounding-curvature criterion applies
  one MOND law on the Schwarzschild metric — but with the *cosmic* a₀ and a *mass-dependent* radius, not
  a per-BH a₀. **MOG** (arXiv:1502.01677) is the genuine metric-shifting rival the null can discriminate.

---

## SINGLE HONEST BOTTOM LINE

- **Layer A (2.406 r_s):** **precedented** — Milgrom transition radius r=√(GM/a₀). Zero independent novelty; do not claim it.
- **Layer B (a₀_BH = κ_BH/Z per-horizon):** **the only place a genuine novelty could live.** The *form*
  (a₀ = surface gravity / constant) and the *horizon-bath idea* are precedented — **Milgrom** (â₀=2c√(Λ/3)),
  **Verlinde** (cH₀), **van Putten**, **McCulloch QI** (closest in spirit, local-vs-cosmic horizon).
  But assigning each **real** BH its **own** a₀_BH from its **own** κ was **not found** in the indexed
  literature ⟹ **"appears genuinely new, pending fuller review"** — NOT proven novel; absence of found
  prior art is not proof, and it is a near-trivial re-application, not a new mechanism.
- **Layer C (null + uniqueness):** the **null is precedented** (AeST stealth BHs, 2412.15395; standard
  MI-vs-MG split) — the paper itself concedes null-vs-null. The **duality + two-criterion uniqueness
  framing** is modestly novel as **exposition/synthesis**, not as physics.

**One line:** Layer A is Milgrom (not novel). Layer C's physics is AeST/MI-vs-MG (not novel; the paper
admits it). The lone plausibly-original move is **Layer B's per-black-hole a₀_BH = κ_BH/Z** — non-standard,
motivated by the modified-inertia reading, unclaimed in the searched literature, closest-miss McCulloch QI —
but it is an unremarkable re-application whose only empirical payoff is a NULL the framework's own host
theory already predicts. The paper's self-scoping ("a structural duality and a null; claims less, not more")
is accurate; **no overclaim correction is needed.** Net standing: **UNCHANGED** — a clean, honestly-scoped
note, not a new front.

---

## EXPERT / REFEREE QUESTION (non-leading — send to a BH-physics PhD)

> In modified-inertia (Milgrom-1994-type) MOND, the acceleration scale a₀ is sometimes written as a
> horizon surface gravity divided by an O(1) constant — e.g. Milgrom's vacuum-effect â₀ ∝ c√Λ from the
> de Sitter horizon, or McCulloch's quantized-inertia scale from the Hubble horizon. **Has anyone in the
> literature applied that "a₀ = (surface gravity)/constant" relation to an individual black-hole horizon —
> i.e. assigned a real black hole its own per-object acceleration scale a₀_BH ∝ c⁴/(GM) from its own
> surface gravity — and worked out the resulting MOND transition radius (which becomes mass-independent,
> a fixed multiple of r_s in the photon-sphere/ISCO band) and its strong-field observational consequences?**
> If so, where? And independently: is the conclusion that a *modified-inertia* (as opposed to
> modified-gravity) theory yields exactly-GR black-hole shadows, ISCO frequencies, and ringdown spectra
> already established — e.g. via AeST stealth black holes (Skordis & Złośnik 2024) — or is there a known
> counterexample where modified inertia does shift strong-field BH observables?

(That question isolates B and C without asserting either is novel — it asks the referee to either name
the prior art or confirm the gap, and to confirm/deny the null independently.)

---

## WHAT TO TELL CARL (straight)

You asked "is it novel?" — here it is both ways, no inflation and no reflexive dismissal:

1. **The number 2.406 r_s is NOT novel** — it's Milgrom's standard transition radius r=√(GM/a₀) with your
   a₀_BH plugged in. Don't claim the algebra. Fine to *report* the number; don't dress it as a discovery.

2. **The exactly-GR null is NOT a new physics result** — AeST's own stealth black holes (Skordis & Złośnik
   2024, which your paper cites) already give exactly-GR geometry, and "modified-inertia → no metric shift"
   is the standard MI-vs-MG distinction. Your paper *says this* (null-vs-null with AeST), which is exactly
   right and is why no correction is needed.

3. **The one genuinely non-standard move is per-BH a₀_BH = κ_BH/Z** — taking *each real black hole's own*
   surface gravity through the same Z. Four independent searches did not find that in the literature. The
   closest anyone got is **McCulloch's quantized inertia** (inertia from a horizon bath, local-vs-cosmic
   horizon competition) — same spirit, but he never writes a per-black-hole a₀. So this is **"looks new,
   pending a fuller arXiv/ADS title search"** — NOT "proven novel." Absence of found prior art is not proof.

4. **Honest caliber:** even where it's unclaimed, it's a *near-trivial re-application* of your own published
   cosmic law, and the payoff is a *null* your host theory already predicts. So the novelty is
   conceptual/structural (a clean duality + a uniqueness argument for why a₀ must be cosmic), not a new
   testable prediction. That's still worth writing down — the uniqueness proposition ("only the cosmic
   horizon is neither local-matter-sourced nor free-fall-removable") is a nice *why-is-a₀-cosmic* argument
   nobody seems to have assembled — just don't oversell it as a new effect.

**Bottom line for you:** A = old (Milgrom), C-physics = old (AeST/MI-vs-MG, you concede it), **B = the live
novelty claim, and it's a "pending review, looks unclaimed" — settle it with the referee question above,
specifically against McCulloch.** Your paper already scopes itself correctly ("claims less, not more"), so
nothing to retract. **This is not a closed door** — the per-horizon construction is a real, non-standard,
modified-inertia-motivated object; it just needs a librarian's confirmation, not a physicist's rescue.
