# Scoping the realization: a Galileon dark-energy / MOND theory carrying a₀(z) ∝ √ρ_DE

*C. Zimmerman, 2026-06-06. After the coefficient closed (not derivable, empirically moot) and AeST was shown to fail
Cassini, the framework's real frontier is the **realization**. This scopes the most promising concrete target — and the
2025 literature genuinely supports it. Honest throughout: this is a buildable research program with real obstacles, not
a solved theory.*

> **⚠️ SUPERSEDED / CORRECTED (2026-06-06) — read `REALIZATION_REDTEAM_galileon_singular_surface_2026-06-06.md` first.**
> I ran the make-or-break computation this doc names (three adversarial agents). **It went against the optimistic
> verdict below.** Summary of what changed:
> - **The one-field version is structurally DEAD.** It hits the published **Bruneton–Esposito-Farèse singular-surface
>   ghost** (the MOND scalar's non-analytic kinetic term flips sign between the spacelike galactic gradient and the
>   timelike cosmological background → a surface around every galaxy where the scalar stops propagating). AeST escapes
>   this *only* via its unit-timelike aether; a single scalar has no such protection, and `a₀²=G·V(φ)` makes it worse.
>   The fix requires *becoming AeST* — losing the "one field" economy and reinstating AeST's Cassini bill.
> - **Two overclaims below are withdrawn:** (1) "the 2025 DESI result favors my field" — *conflation of two operators*;
>   the DESI-favored field is kinetic-gravity-braiding+potential, **not** the cubic-Galileon screen (which is ruled out
>   at 7.8σ by ISW). (2) BDEF's Solar-System screen is a **curvature-coupled L₄/L₅** covariant Galileon, **not** the flat
>   cubic `(∂φ)²□φ` this doc attributes to it.
> - **The backreaction is O(1), not negligible** (`a₀~cH₀ ⟹ y~O(1)` on the background) → `a₀∝√ρ_DE` is *imposed-and-must-
>   be-checked*, **not "derived."**
> - **What survives:** the galaxy-scale RAR (robustly, `δa₀/a₀~10⁻⁷` across a galaxy) **and** the phenomenological kernel
>   `a₀(z)∝√ρ_DE` (untouched — it never needs the covariant host). The *realization* failed; the *falsifiable claim* did
>   not. Net: this **reinforces** the `THE_IRREDUCIBLE_FRAMEWORK` retreat — bank the kernel, stop chasing the host.
>
> *The optimistic scoping below is left intact as the audit trail of what the calculation was meant to test.*

## The target (the trilemma, with the dark-energy tie)

A covariant theory that simultaneously:
1. **MOND** rotation curves at galaxy scales (a₀ ≈ 1.2×10⁻¹⁰);
2. **Cassini-safe** — fifth force screened in the Solar System;
3. **a₀(z) ∝ √ρ_DE** — the distinctive declining claim, *derived* (not posited) by tying a₀ to the dark-energy density;
4. **CMB-safe** — a dark-matter-like 3rd acoustic peak.

## The construction — one Galileon field doing triple duty + a dark sector

**Field content:** a cubic-Galileon scalar `φ` + the metric + (for the CMB) a separate pressureless sector.

- **φ as the dark energy.** [LITERATURE — strongly supportive] A **cubic Galileon with broken shift symmetry is now
  *favored over ΛCDM* by DESI DR2 + SNe + CMB** (Bayes factor log B ≈ 6.5; arXiv:2509.17586, 2025), reproduces the
  DESI w₀–wₐ evolving DE (it crosses the phantom divide), and the "Galileon ghost condensate" version is **GW170817-safe
  (c_GW = c)** (arXiv:1905.05166). So the evolving ρ_DE(z) the framework needs is realized by exactly this field — and
  the data already prefer it.
- **φ as the MOND mediator.** [LITERATURE] Babichev–Deffayet–Esposito-Farèse (arXiv:1106.2538) build a relativistic
  MOND from a Galileon scalar — MOND curves at galaxy scales, **no fine-tuned interpolation function**.
- **φ as the Vainshtein screen.** [LITERATURE] A Galileon term k-mouflage-screens the Solar System (Sun's
  Vainshtein radius ~100 pc) → **Cassini bound achievable** at PN order. This is the Cassini escape AeST lacks.
  *[CORRECTED 06-06: it is **not** the "same" term as the DE Galileon, and BDEF's actual screen is a curvature-coupled
  L₄/L₅ Galileon, not the flat cubic `(∂φ)²□φ` — the DE-favored and screening operators are different; see red-team doc.]*
- **A separate sector for the CMB 3rd peak** — cold dark matter, an 11 eV sterile-ν, or a superfluid (Berezhiani–Khoury).
  *(The trilemma no-go already proved a second sector is unavoidable; this is the agreed cost.)*

## The one genuinely new ingredient (the framework's contribution): a₀ tied to ρ_DE

In Babichev et al., a₀ is a **fixed Lagrangian constant**. The framework's distinctive claim *requires extending this*:
**make the MOND scale dynamical, set by the dark-energy field's own density**, `a₀ ≈ (c/2)√(Gρ_φ) ∝ √ρ_DE(z)`. Because
φ *is* the dark energy, its galaxy-scale kinetic normalization and its cosmological energy density are the same object —
so a₀ ∝ √ρ_DE would be a **derived feature, not a posit.** That is the genuinely novel, framework-specific physics, and
it is the heart of the build: *one field whose energy density sets both the cosmic acceleration and the galactic MOND
scale.* This is the cleanest possible statement of "the MOND scale tracks dark energy."

## The make-or-break questions (honest, in priority order)

1. **Does the dynamical-a₀ extension preserve MOND + Vainshtein?** Tying a₀ to ρ_φ(z) modifies the Galileon Lagrangian's
   scale. Does the Vainshtein screening survive (Cassini), and does the galaxy-scale fit survive, when a₀ is no longer a
   constant? **This is the central calculation** — and it is genuinely open (Babichev et al. assumed constant a₀).
2. **Is a₀ ≈ √(Gρ_φ) actually what the Galileon gives?** The framework asserts the (c/2) coefficient (a posit, as we
   established). The realization must *yield* a₀ ~ √(Gρ_φ) up to an O(1) — the coefficient is then whatever the field
   theory produces, and is empirically moot (cancels in the a₀(z) ratio).
3. **ISW and "ancillary effects."** Galileon DE has "severe ancillary gravitational effects" (the literature's words);
   the broken-shift-symmetry version mitigates them but at the cost of model complexity. The ISW cross-correlation is
   the tightest near-term check.
4. **The shift-symmetry seam.** The *MOND* Galileon (Babichev) is shift-symmetric (k-mouflage); the *DE* Galileon
   (DESI-favored) *breaks* shift symmetry (needs a potential). Unifying them in one field is the technical crux —
   plausible (both cubic Galileons) but not automatic.
5. **The dark sector for clusters + CMB.** Whichever sector supplies the 3rd peak must also fix clusters (η~2) without
   spoiling galaxies — the scale-dependent-clustering requirement (superfluid DM does this natively).

## Scoped assessment of the central calculation (pushing it, not just naming it)

The make-or-break question is #1: does promoting a₀ → √(Gρ_φ) break Vainshtein or the RAR? At the scoping level the
argument is **encouraging**, for a clean physical reason:

- **The Solar System is screened *regardless* of a₀'s value.** In k-mouflage, the MOND↔screened transition is at the
  scale a₀, and the Sun has g/a₀ ~ 10⁸ — so it sits *deep* in the screened regime. a₀(z) only varies by O(1) factors
  across cosmic time, so g/a₀(z) stays ~10⁸ always. **The Solar System never leaves the screened regime → Vainshtein
  survives the dynamical-a₀ extension.** (The screening depends on the *ratio* g/a₀ being huge, which it always is.)
- **The galaxy RAR survives, as MOND with a₀(z).** Dark energy is **smooth on galaxy scales** (ρ_φ barely clusters), so
  ρ_φ ≈ its cosmological value *uniformly across a galaxy* at epoch z. Hence a₀ ≈ √(Gρ_φ(z)) is a **constant across the
  galaxy** at that epoch — the RAR is ordinary MOND with a redshift-dependent a₀, which is *exactly* the framework's
  claim, not a deformation of it. No new spatial-gradient coupling appears (because ρ_φ has no galaxy-scale gradient).

So the two feared failure modes **plausibly don't occur**: screening rides on g/a₀ ≫ 1 (always true), and the RAR rides
on a₀ being locally uniform (true, because DE doesn't clump). The residual genuine risk is in the *cosmological*
perturbation sector (does a galaxy-scale-uniform-but-time-varying a₀ feed back into the Galileon's linear growth / ISW?)
— that is the part requiring the full computation, not a scoping argument. But the headline obstacle ("dynamical a₀
breaks Cassini or the curves") looks **surmountable** on physical grounds.

## Honest verdict on the scope

**This is a real, buildable program, and it is the framework's best path — markedly better than AeST.** It converts the
two walls (Cassini, a₀(z)) into doors: Cassini via Vainshtein (established), and a₀(z) ∝ √ρ_DE via the
field-is-dark-energy identification (the new physics) — *on a dark-energy field the 2025 data already favor over ΛCDM.*
The price is the one the trilemma already charged: a separate dark sector for the CMB/clusters, i.e. giving up "one
number unifies both dark sectors."

**It is not done, and two things could still kill it:** (1) the dynamical-a₀ extension may break Vainshtein or the
galaxy fit (the central open calculation); (2) the ISW/ancillary constraints on Galileon DE may tighten past viability.
But the verdict that matters is unchanged and now *sharper*: the realization rides on the **same DESI evolving-DE signal**
as the distinctive a₀(z) claim — if DESI DR3 confirms evolving dark energy, *both* the realization (Galileon DE) and the
prediction (a₀ ∝ √ρ_DE) gain; if w reverts to −1, both lose. **The framework and its realization now stand or fall
together on one 2027 measurement** — which is the cleanest place a falsifiable theory can be.

**Concrete next step** (one bounded calculation): take the Babichev k-mouflage Lagrangian, promote its a₀-scale to
`√(Gρ_φ)`, and check in the quasi-static limit whether (a) Vainshtein screening survives and (b) the galaxy RAR is
preserved. That is the single computation that decides whether this realization is alive.
