# The cluster closing calculation — VERDICT: FALSIFIED-AS-CLOSURE (2026-06-14)

*The decisive calc Carl asked for: solve the FULL nonlinear AeST scalar mass-term model for clusters with the
physical boundary condition and ONE CMB-pinned 1/μ held across galaxies AND clusters, and decide whether it
closes the eRASS1 η~2.15 cluster deficit. Three independent solvers (shooting + envelope-min BC; BVP/IVP
collocation; standing-wave Green's function) + a hostile referee who recomputed from scratch. Scripts:
`cluster_aest_shooting_solver.py`, `cluster_aest_massterm_BVP_implB.py`, `aest_single_mu_gauntlet.py` (+ the
three `*_2026-06-14.md` derivations).*

---

## VERDICT: **FALSIFIED-AS-CLOSURE**

> With one CMB-pinned 1/μ = 1 Mpc, the physical boundary condition, and **zero per-cluster tuning**, the
> full-nonlinear AeST scalar mass term gives **η(R500) = O(1) and *below* MOND (a deficit, ~0.3–0.96), never
> the eRASS1 ~2.15 boost.** The AeST mass term — the framework's one intrinsic cluster candidate — does **not**
> close the cluster deficit from first principles. It *predicts a deficit, not a cure.*

Three solvers, the same verdict: η(R500) = {0.85, 0.63, 0.46, 0.33} for M500 = {1, 3, 5, 10}×10¹⁴ M⊙
(shooting/envelope-min); ~0.9–0.96 (standing-wave); deficit (BVP). Galaxies stay MOND-pure to <0.2% at 10–30
kpc **with the same μ**. The verdict is robust; the implementations differ only on the *precise* sub-unity
number (0.3 vs 0.95), for a reason that is itself the proof — see below.

## The decisive physics (a genuine insight, worth keeping)

**+μ²Φ is a positive-sign *Helmholtz* operator, not a Yukawa operator.** A Yukawa mass term (−μ²) gives an
exponentially *decaying* short-range field; the AeST mass term enters with the *opposite sign*, so the
homogeneous solutions are **oscillatory** — [A cos(μr) + B sin(μr)]/r — both decaying as 1/r. Consequences:

1. **The boundary condition Φ(∞)→0 is NON-SELECTIVE (degenerate).** Every member of the homogeneous family
   already satisfies Φ(∞)→0, so that condition does *not* pin the solution. Adding a homogeneous standing wave
   swings η(R500) across 0.38 → 4.74 while Φ(∞)→0 holds throughout. This is exactly why the *first* pass found
   η=2.15: it was reachable **only** by sliding the free Helmholtz boundary constant (Verwayen's χ̂_out)
   **per cluster** — a tune, not a prediction. Remove that per-cluster freedom (any fixed physical
   prescription) and you get a deficit.
2. **The "boost" is at the wrong radius.** The shallow phantom-mass peak (only ~+9%) sits at ~4 Mpc ≫ R500,
   followed by a *negative-phantom dip* near R500 — the Durakovic–Skordis peak-then-dip signature, but parked
   beyond the cluster and far too weak.
3. **One μ cannot thread both scales (Mistele tension, reproduced end-to-end).** At 1/μ = 1 Mpc galaxies are
   MOND-pure ((μr)²~10⁻⁴, term OFF) but clusters get η~0.92–0.96 (term ON but only the shallow misplaced peak).
   Shrinking 1/μ to chase 2.15 makes η *oscillate* (never cleanly reaching 2.15) and **breaks galaxies first**
   (deviation crosses 1% by 1/μ~0.2 Mpc). No single CMB-pinned μ delivers the boost while keeping galaxies safe.

The full nonlinearity is genuinely solved (exact M(x)=(√(1+4x)−1)/(√(1+4x)+1); at R500, (μR500)²~0.5–2.3 = O(1)
so the (μR)² expansion is invalid and was *not* used; g_bar/a₀~0.07 = deep-MOND; μ→0 reproduces analytic MOND
to 0.2%). The one delicate point (the oscillatory Helmholtz tail) was diagnosed and handled with an
r_max-independent envelope-minimization BC.

## What Carl CAN say / must NOT say

- **CAN:** "AeST's scalar mass term is a genuine intrinsic mechanism at the right *scale* — OFF in galaxies
  (MOND-pure to <0.2% at one CMB-pinned 1/μ~1 Mpc), ON at clusters — and, solved fully and honestly, it
  *predicts* clusters stay essentially MOND at R500 (η~O(1), a mild deficit), with a falsifiable peak-then-dip
  η(M500) signature."
- **MUST NOT:** "first principles close the eRASS1 ~2× cluster deficit" — that requires a per-cluster boundary
  tune of the degenerate Helmholtz constant. **The ~2× cluster deficit remains MOND's shared, inherited,
  UNSOLVED liability.**

## The surviving (falsifiable) prediction — opposite to closure

At the CMB-pinned 1/μ = 1 Mpc the AeST mass term predicts: (1) clusters **stay ~MOND at R500**, η(R500)~0.8–1.1,
a mild *deficit* of the same sign as MOND's known shortfall — **not** a 2× excess; (2) a **peak-then-dip** radial
RAR (shallow +9% phantom bump at ~4 Mpc, negative-phantom dip near R500); (3) η(M500) **declining steeply**
(dη/dlog₁₀M500 ~ −0.5), wrong-signed and far too steep vs eRASS1's flat ~2.15. A measured sustained 2.15× out
to R500, a *rising* η(M500), or a peak located *at* R500 each **falsifies** the term as written.

## Where this leaves clusters

**No framework channel supplies the 2× as a forced first-principles result.** The mass term — AeST's one
intrinsic candidate — predicts a deficit, robustly across three solvers + two referee rebuilds. **Clusters are
a permanent shared-MOND liability requiring a SECOND component** (the textbook MOND cluster problem, reproduced
on real eRASS1 data, robust to interpolation function 2.15–2.40 and stellar fraction 1.9–2.4; conventionally
patched by ~2 eV sterile/active neutrinos or additional dark baryons — NOT by the AeST mass term).

*This SUPERSEDES the cluster line in `CLUSTERS_AND_WIDE_BINARIES_FIRST_PRINCIPLES_2026-06-14.md`: the AeST mass
term is downgraded from CANDIDATE-UNPROVEN to FALSIFIED-AS-CLOSURE (predicts a deficit, not a cure). No
manufactured cure; the #1 rule held — this is a clean, decisive negative, three independent ways, with a real
physics reason (the Helmholtz BC degeneracy). Quarantine held: a₀/Z never asserted derived; μ flagged a free
CMB-pinned constant, identical galaxies↔clusters.*
