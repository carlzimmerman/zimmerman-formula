# UX1_action_class: FROZEN CRITERIA (committed alone, before any script or number)

Question: is there a covariant action for g_N = g^2/(g + a0), a0 = kappa c sqrt(G rho_DE), outside the classes that failed on record?

kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, both reported, never pooled. No dark matter particle. The cold component is cold dark energy. The cold sector stays retired: no result here reinstates it, only the owner can. Not theory closed. Nothing here says the data favour the framework.

## Not blind
Read before freezing: REQUIREMENTS_LIST.md, THEORY_V3_DRAFT.md, V3S_FINAL_VERDICT (lines 1-430), BOLTZ1 README, STANDING.md 284-300, M1_trilemma README, E2 and D7c READMEs, Z1 family scores, X0 MAP, CFG944's ledger row, aqual_axi.py's header.
I have also already worked by hand, with no script run, the BIMOND static reduction and the expectations below. Literature statements come from memory unless a fetched page is named, and are PROVISIONAL.

Expectation written now: clean negative on the four gates. The exact law's own tail g - g_N -> a0 should sink every unscreened candidate. BIMOND with twin dust may be the most interesting failure. This expectation may be wrong; it does not change a label.

## Candidates (fixed list; published work credited in the README)
- K1 BIMOND, no twin matter (Milgrom 2009).
- K2 BIMOND with a twin dust, locked branch (Milgrom 2010 for twin matter).
- K3 Ghost-free bigravity (Hassan-Rosen 2011, de Rham-Gabadadze-Tolley potential), and its decoupling-limit galileons.
- K4 Nonlocal metric MOND (Deffayet-Woodard 2011 and successors). Record lane read; own symbol check only.
- K5 Two-scale completion of the gamma_L stiffness: a second field that gives a second-order Lorentz-invariant system (this lane's construction, M1 listed it untested).
- K6 Mimetic gravity with f(box phi) (Chamseddine-Mukhanov 2013; Vagnozzi 2017 for the MOND-like limit).
- K7 Two-potential QUMOND parent with a rolled-over nu (Milgrom 2010).
- K8 Two-sector: v3s law sector plus a separate P(X) or mimetic dust.
- K9 Covariant refracted gravity (Matsakos-Diaferio; Sanna et al.).
- K10 Superfluid two-phase (Berezhiani-Khoury 2015). Record-closed; reported from the record only.

Added only by amendment, committed before its number.

## Gates (each candidate gets each label: PASS, FAIL, or NOT DECIDED with the reason)
- G1 STATIC LAW. Spherical static limit, baryons as the only source, returns g_N = g^2/(g + a0) exactly: sympy residual zero, for all g over the range the candidate is defined. A form reached only by fixing a free function is allowed and stated.
- G2 SOLAR SYSTEM. Both needed: Q2 at or below the Hees 2 sigma line that E2 used, at E2's four external fields on both footings; and the planets' anomaly at or below the bounds M1 used. A candidate with no screen inherits G2 FAIL from its own static tail unless its off-spherical equation differs, in which case Q2 is solved: K1's equation gets its own solve with E2's solver, imported read only. Passing needs a screen present in the action, with its value stated.
- G3 HEALTH. No ghost and no gradient instability, at quadratic order on a stated background, by sympy. A proof of extra degrees of freedom whose kinetic sign is negative is FAIL. An extra degree of freedom whose sign can't be fixed, or a Hessian rank change alone, is NOT DECIDED, never PASS. A published instability I don't recompute is labelled FAIL [RECORD or LIT], and PROVISIONAL if literature.
- G4 DUST TERM. A w = 0 term in the Friedmann equation of the metric light and baryons see, with delta growing as a at k -> 0 on a stated branch.
- Reported, not a gate: G5 DOUBLE COUNT. Does the dust sit in the static source, so that G1's exact law on baryons fails in galaxies? Stated with X22's capture and X57's numbers. It may qualify a verdict in words.

## General results to attempt (labels: PROVED IN STATED CLASS, or NOT PROVED)
- T-A. A linear, Lorentz-invariant kernel with positive spectral weight has k^2 D(k^2) non-decreasing in k^2. So it can't weaken an extra force toward short distance: a scale-based screen of that type needs a ghost, a broken Lorentz frame, or nonlinearity.
- T-B. A static field h = g - g_N driven by an elliptic convex functional has h non-decreasing in g_N, so it can't roll over to protect the planets. This extends M1's T2 beyond AeST, if it holds.
- T-C. A k^4 dispersion in one frame is Hadamard ill-posed in a tilted slicing unless the frame is a global time function (extends I1).
- Whether these cover every route is itself a question to answer. No claim of a universal no-go may be made: state the class.

## Verdict labels (one)
- ESCAPE: one candidate has PASS on G1 to G4.
- CONDITIONAL LEAD: no ESCAPE, and a candidate has at most one non-PASS gate, which is NOT DECIDED.
- CLEAN NEGATIVE ON THE LISTED CLASSES: otherwise. A candidate failing fewest gates may be named as closest; that isn't a pass. Also report any trilemma horn that the work finds misstated.

## Checks and twin
Script `ux1_gates.py`, sympy and numpy only, one thread, nice 15, no download, under 4 GB. Output `.out` and `.json` contain no timing, so a rerun must be byte-identical. Solver numbers: known-answer check against E2's AQUAL Q2 for the canonical law (the record's value within 2 %), before K1's value counts.
MUTATE twin `UX1_MUTATE=1` writes separate outputs and must fail: flips the sign of the difference field's coupling, uses a non-Stieltjes kernel with a positive weight claim, and drops the factor in the law reconstruction. If a mutation doesn't bite, that is reported. Every failed check is reported.

No deposit. No edits to PAPER67, the ledger, the outside summary or other lanes. No push.
