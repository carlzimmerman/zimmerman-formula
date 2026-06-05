# Deep-MOND Scale Invariance Is Broken *Explicitly*, Not Spontaneously: There Is No MOND Dilaton

**C. Zimmerman, June 2026.**
*A short note. Scope is deliberately narrow and the priors are attributed throughout: the only claim of novelty is
the crisp statement of one corollary (Section 3) and its observational reading (Section 4). Everything else is
Milgrom (1984, 2009), the extended-metric-MOND literature, and Singh (2026).*

---

## Abstract

The deep-MOND limit possesses an exact conformal (scale) symmetry — in three spatial dimensions a ten-parameter
group isomorphic to **SO(4,1), the de Sitter group** (Milgrom 2009) — with the acceleration scale a₀ playing the
role of the symmetry-breaking parameter. We note a simple but, to our knowledge, unstated corollary: because the
symmetry is broken **explicitly** — a₀ is a dimensionful coefficient of a non-invariant operator in the action, not
the order parameter of a non-invariant vacuum — **Goldstone's theorem does not apply, and there is no light scalar
(dilaton or pseudo-Goldstone boson) associated with deep-MOND scale invariance.** Consequently, AQUAL-type MOND
predicts no new long-range fifth force or extra gravitational-wave polarization *of this symmetry origin*. This
distinguishes it sharply from frameworks in which scale invariance is realized *with* a dynamical scalar
(Weyl/Scale-Invariant-Vacuum) or broken *spontaneously* (dilaton-as-pNGB). A corollary for experiment: a "MOND
dilaton" search motivated by the scale symmetry is looking for a particle the symmetry structure forbids.

## 1. The symmetry and what breaks it (attribution)

Milgrom (2009, arXiv:0810.4065) showed that the deep-MOND limit follows from invariance of the dynamics under the
spacetime dilatation (t, **r**) → (λt, λ**r**), and that the resulting potential theory (AQUAL, Bekenstein–Milgrom
1984) has, in d = 3 spatial dimensions, a full conformal symmetry group **SO(4,1)** — the isometry group of
four-dimensional de Sitter space, a coincidence Milgrom himself flagged as "perhaps pointing to another connection
of MOND with cosmology." Singh (2026, arXiv:2601.04290) develops this into a relativistic MOND in which the single
scale a₀ is fixed by a dynamically selected de Sitter radius, a₀ = c²/(ξ ℓ_dS).

A precise point of framing, due to Milgrom: the scale-invariant theory is the **a₀ → ∞ limit** (equivalently, the
regime of accelerations far below a₀), and what *obstructs* the scaling symmetry is the surviving Newtonian/rest-mass
structure. In the language of the AQUAL action, the deep-MOND cubic term ∝ ∫d³x |∇φ|³/a₀ is scale-invariant, while
the Newtonian quadratic term ∝ ∫d³x |∇φ|² scales as λ¹; a₀ is the acceleration at which the non-invariant (Newtonian)
term takes over from the invariant (deep-MOND) one. (We verified the λ-scaling explicitly in
`reviews/project_symmetry_breaking.py`.) That a₀ "breaks the scale invariance of the gravitational interaction" is
the standard reading of the extended-metric-MOND line (e.g. arXiv:1108.5588, 1202.3629).

## 2. Explicit vs. spontaneous breaking

The distinction that matters for what follows is elementary but consequential:

- **Spontaneous** breaking: the action is invariant, the **vacuum** is not. Goldstone's theorem then guarantees a
  massless boson for each broken generator of a continuous *internal* symmetry (and a dilaton — a *pseudo*-Goldstone
  — for spontaneously broken scale invariance, since scale symmetry is typically anomalous).
- **Explicit** breaking: the **action itself** is not invariant — it contains a dimensionful parameter or a
  non-invariant operator. There is no associated Goldstone boson; the would-be Goldstone is removed (or lifted to
  arbitrary mass) by the explicit term. The textbook analogue is the quark mass term m q̄q, which breaks chiral
  symmetry *explicitly*: the pion is a *pseudo*-Goldstone precisely because chiral symmetry is *also* broken
  spontaneously by ⟨q̄q⟩, and it acquires mass from the explicit m.

Deep-MOND scale invariance is of the **explicit** type. The dimensionful a₀ (and, in Milgrom's framing, rest mass)
sits in the Lagrangian; the scale symmetry is a property of a *limit* of the theory, not a spontaneously broken
symmetry of the full action with a non-invariant ground state. There is no order parameter, no ⟨·⟩ that breaks it.

## 3. The corollary: no Goldstone, no MOND dilaton

It follows immediately that **deep-MOND scale invariance has no Goldstone boson.** There is no light scalar — neither
an exact Goldstone nor a pseudo-Goldstone dilaton — *protected by, or arising from,* the deep-MOND conformal
symmetry. The symmetry is explicitly broken at the level of the action, so the one structural mechanism that would
*guarantee* a light scalar (spontaneous breaking + Goldstone's theorem) is simply absent.

We have not found this stated in the MOND literature, despite the scale invariance (Milgrom 2009) and its de Sitter
/ a₀-from-Λ connection (Singh 2026) being well known. It is a one-line consequence once the breaking is identified as
explicit — but it has a non-trivial observational reading, and it corrects a natural but wrong intuition (that a
scale-invariant modified gravity "should" come with a dilaton).

## 4. Observational reading

If there is no Goldstone scalar of deep-MOND origin, then **this symmetry contributes no new long-range fifth force
and no extra (scalar) gravitational-wave polarization.** A near-massless dilaton with universal derivative couplings
is exactly the kind of object that fifth-force and equivalence-principle experiments (Eöt-Wash torsion balances,
MICROSCOPE, lunar laser ranging, Cassini) are sensitive to, and exactly the kind of extra polarization that
multi-messenger GW astronomy (GW170817, with c_GW = c to ~10⁻¹⁵) constrains. The no-Goldstone result says the deep-
MOND conformal symmetry predicts **none of these** — consistent with all current null results, and, importantly, it
says so as a *structural* statement rather than a tuning.

The practical corollary: **a "MOND dilaton" search motivated by the scale symmetry is the wrong experiment.** The
absence of such a scalar is not a failure of MOND to be detected; it is what the (explicitly broken) symmetry
predicts.

## 5. Contrast with scalar-realized and spontaneous-dilaton frameworks

The corollary's content is sharpest by contrast:

- **Weyl / Scale-Invariant-Vacuum (SIV)** (Maeder & Gueorguiev, e.g. arXiv:2001.04978): realizes scale invariance
  *dynamically*, via a scalar gauge field of Weyl integrable geometry. Here a scalar degree of freedom **is** the
  mechanism — the opposite structural choice from AQUAL-MOND.
- **Spontaneous-dilaton models** (e.g. arXiv:2601.01938): a dilaton arises as a pseudo-Goldstone boson of
  *spontaneously* broken scale symmetry, and carries observable couplings.

AQUAL-type MOND sits in neither class: its scale symmetry is *explicitly* broken and carries no scalar of Goldstone
origin. Whether a given relativistic completion of MOND carries a scalar is therefore a question about that
completion's construction, **not** a consequence of the deep-MOND symmetry.

## 6. Honest caveats

1. **Covariant MOND theories *do* contain extra fields.** AeST (Skordis–Złošnik 2021), TeVeS, RAQUAL, etc. introduce
   a scalar and/or a unit-timelike vector — but these are the **carriers of the MOND modification**, inserted by the
   covariant construction, not Goldstone bosons of the deep-MOND conformal symmetry. Their masses, couplings,
   screening, and c_GW = c are fixed by the construction (and tuned to pass GW170817 and solar-system tests), *not*
   protected by a broken symmetry. The claim here is narrow and specific: the conformal symmetry contributes **no
   additional, symmetry-protected light scalar** beyond whatever fields a model puts in by hand.
2. **This is a corollary, not a theory.** Its two ingredients — Milgrom's explicit-breaking framing and textbook
   Goldstone logic — are individually standard; the only new content is stating their conjunction crisply, with the
   observational reading and the SIV/dilaton contrast. A referee could reasonably call it obvious. We think it is
   nonetheless worth recording, because the intuition it corrects ("scale-invariant gravity ⇒ a dilaton") is common
   and the structural answer is clean.
3. **Same root as the un-forced coefficient.** That a₀ is an *explicit*-breaking parameter is also why its value (and
   the dimensionless coefficient relating a₀ to √Λ) **cannot be fixed by the symmetry** — symmetries fix the *form*
   of the deep-MOND term (the cubic, hence the √-law) but never the *scale* that breaks them. The no-Goldstone
   corollary and the route-forced-not-uniquely-forced status of the coefficient are two faces of the same fact.

## References

- Bekenstein & Milgrom 1984, ApJ 286, 7 (AQUAL).
- Milgrom 1984, ApJ 287, 571 (isothermal spheres; deep-MOND Faber–Jackson).
- **Milgrom 2009, ApJ 698, 1630, arXiv:0810.4065** — the MOND limit from spacetime scale invariance; SO(4,1) = de
  Sitter group.
- Recovering-MOND-from-extended-metric line: arXiv:1108.5588; arXiv:1202.3629 (a₀ as explicit breaker of
  gravitational scale invariance).
- **Singh 2026, arXiv:2601.04290** — relativistic MOND; a₀ from a dynamically selected de Sitter radius.
- Maeder & Gueorguiev, arXiv:2001.04978 (Scale-Invariant Vacuum / Weyl geometry — scalar-realized scale invariance).
- arXiv:2601.01938 (dilaton as spontaneous-scale-breaking pseudo-Goldstone — the contrast case).
- Skordis & Złošnik 2021, PRL 127, 161302, arXiv:2007.00082 (AeST — a covariant MOND with explicit scalar+vector).
- Supporting verification in this repository: `reviews/project_symmetry_breaking.py` (the λ-scaling and crossover);
  `SYMMETRY_BREAKING_PHYSICS.md` (the fuller treatment and the novelty/priority audit).
