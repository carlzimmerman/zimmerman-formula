# DUST TASKS — open problem 2d, the framework's #1 open problem

**Read `dust_filters.py --explain` FIRST, every session.** Five free filters, three of them
parameter-free, each fatal alone. Any candidate mechanism gets screened before it gets a
session. `python dust_filters.py --screen spec.json` — exit 0 = screened, exit 2 = dead.

**The problem, stated exactly.** The dark sector is a shift-symmetric condensate whose
excitation is pressureless dust with ρ = Q₀n identically. Halos capture it, nothing found so
far stops it collapsing, and the endpoint is a black hole falsified 5.8×10⁵× against Sgr A*.
The property that makes w = −1 exact is the property that makes the excitation dust — so the
dark-energy success and this problem are the same feature of the same field.

**Standing rules.** Everything in `PROTOCOL.md` applies (small-context mode; script in
`runs/`; run via `harness.py`; one ledger row; end the session). Two extra, specific to this
front: (1) a candidate that passes the screen is **SCREENED, never VIABLE** — say so in the
ledger; (2) verify an adverse result as rigorously as a favourable one. A wrong kill here is
as costly as a wrong rescue, because it closes a door that was open.

**D001 — Filter calibration against the four known corpses.** Hypothesis: `dust_filters.py`
reproduces the committed verdicts for all four candidates in
`real_research/reviews/second_field_catalog_2026.py` (second k-essence; ungated Proca in the
contact and long-range limits; promotion-only field; the fixed-bare-Λ-gated Proca). Method:
write a spec JSON per candidate from the review's own descriptions, screen each, compare with
the review's verdict and killing leg. PASS: 4/4 agreement, or a named disagreement — which
would mean the filter is wrong and must be fixed before any other D-task runs.

**D002 — Non-charge-built pressure: enumerate and screen.** Hypothesis: F1 (ρ = Q₀n makes any
charge-built pressure a local P(ρ)) can be evaded only by a pressure source that is not
built from the conserved charge, and the list of such sources is short and enumerable.
Method: enumerate candidate sources (a second condensate with its own charge; a gauge field;
a fermion degeneracy sector; vorticity/turbulent stress; a non-local/gradient-energy term;
finite-temperature radiation of the sector), and for each state exactly which conserved
quantity carries the pressure and screen it. PASS: the table, with the killing filter named
per row, and any row that survives escalated to ESCALATE.md.

**D003 — Non-monotone gates: does a falling-outward scalar exist?** Hypothesis: F5 kills any
gate monotone in a quantity that rises outward, so the escape needs a scalar of the theory
that FALLS outward in a self-gravitating dust cloud. Method: list the theory's available
local scalars (Q, Y, |∇φ|, ρ, ρ_baryon, curvature invariants, Q−Q₀, the DBI wall distance)
and compute the radial gradient sign of each in the committed support profile. PASS: the
sign table. A scalar that falls outward is a REAL finding — escalate it.

**D004 — Is 0.194 ever order unity?** Hypothesis: the crossover r_×/R_supp =
[M_bar/((π²/3)M_dust)]^(1/3) is parameter-free but not universal — it depends on the
baryon-to-dust ratio, which varies across galaxy classes. Method: compute it across the
SPARC range of M_bar/M_dyn (use `real_research/` SPARC data already in the repo), including
the most baryon-dominated systems. PASS: the crossover as a function of the mass ratio, and
whether any real galaxy class reaches r_×/R_supp ≳ 0.5. If one does, F5's 99.27% is not
universal and the gated route reopens for that class.

**D005 — Is the dust forced to be irrotational?** Hypothesis: the corpus states the dust is
an irrotational potential flow (no angular momentum, no shell crossing, no substructure).
If that is an artifact of the initial conditions rather than forced by the action, then
centrifugal support evades F1–F4 entirely — it is not a pressure. Method: check whether the
shift symmetry plus the equation of motion forbid vorticity identically, or only for
initially-irrotational data; state which, with the derivation. PASS: forced-or-not, with the
proof. **This is the highest-value task on this list** — a "not forced" answer opens a
support channel none of the five filters touch.

**D006 — Which input dominates the 5.8×10⁵× Sgr A* falsification?** Hypothesis: the
falsification is robust, but its margin is dominated by one or two inputs. Method: locate the
committed calculation in `nbody_2026/`, re-derive it, and do a sensitivity sweep over its
inputs (captured mass, halo class, collapse efficiency, the black-hole mass used, formation
time). PASS: the sensitivity table and the identity of the dominant input. A halo class where
the margin drops below ~10× is a finding.

**D007 — Two-component split: how much charge can be dust?** Hypothesis: a fraction f of the
charge is dust and (1−f) is something else; the CMB fixes a minimum clustering component,
so there is a maximum f that avoids the collapse and a minimum f that keeps the CMB. Method:
use the committed CLASS pass to bound the clustering component from below, and D006's
sensitivity to bound the collapsing fraction from above. PASS: the interval, or the
demonstration that it is empty. An empty interval is a strong negative worth recording.

**D008 — Transport with the framework's own enhanced gravity.** Hypothesis: the committed
690 Gyr transport timescale was computed Newtonianly; the framework's own kernel gives
ν(y) = 9–45 at the relevant scales, which shortens it. Method: recompute the transport time
with g = ν(y)g_bar and the derived a₀(z), using the same geometry as the committed
calculation. PASS: the corrected timescale. If it drops below a Hubble time the transport
escape reopens; if not, the closure is strengthened. **Report the direction honestly either
way** — this is a case where the framework's own machinery could cut against it.

**D009 — Find the a₀-gate escape corner.** Hypothesis: the review proved the gate
amplification equals the barotropic factor only in the restricted regime ν₀·r_supp ≥ 10, and
flagged an unpriced deep-support corner (separation 3.46×10² > 1) closed on a different leg
(the RAR/lensing mass budget at 9.0–9.9×). Method: map where the restriction fails and
recompute the corner on its own terms. PASS: whether the corner is genuinely closed or only
closed by the budget argument. If the latter, it is a live escape with a stated price.

**D010 — The maximum tolerable lensing pile-up.** Hypothesis: candidate 4 died partly on
piling 55–61% of the framework's own lensing mass at r_× = 653 kpc, inside the range already
fitted. Method: using the committed KiDS weak-lensing fit (`stage12`, real Mistele+2024
data), compute the maximum mass excess at 0.3–1 Mpc that the fit tolerates at 2σ. PASS: the
tolerance curve. This converts a qualitative kill into a quantitative budget every future
candidate can be screened against — add it to `dust_filters.py` as F6 if it works.

**D011 — Observable signature short of a black hole.** Hypothesis: if the dust collapses but
has not yet reached the endpoint, there is a halo-scale signature testable with existing
data. Method: compute the intermediate-state density profile and ask what it does to rotation
curves, lensing, or stellar kinematics at 0.1–10 kpc. PASS: a named observable with a
magnitude, or a demonstration that the intermediate state is unobservable — which would
itself be worth knowing, because it means the problem is purely theoretical.

**D012 — Literature: has anyone solved this?** Hypothesis: dust retention in a
shift-symmetric condensate is a known problem with known attempted solutions. Method: search
the ghost-condensate, khronon, Galileon, superfluid-dark-matter and BEC-dark-matter
literature for support mechanisms in a sector with a conserved shift charge. Report what was
tried and what killed it. PASS: the annotated list. **Cite nothing you have not read** — mark
anything second-hand as UNVERIFIED, and never invent an equation number, quote or DOI.
