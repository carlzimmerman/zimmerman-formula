# A1/A2 branch corroboration from a SECOND route (2026-08-22)

Goal: independently confirm (or flag discrepancies in) the A1/A2 coefficient
functions and the "no 2-DOF for nonlinear lapse derivatives" statement used by
the SCG+auxiliary-MOND program, and pin down (i) whether H_i is first-class and
(ii) whether the scalar is removed by a second-class pair or a kinetic-matrix
degeneracy. Verbatim quotes with equation numbers; INCOMPLETE where a claim is
not verifiable against a fetched primary source.

## Sources fetched
- S1 (primary, cited by repo): arXiv:2604.14490v1 (HTML) — "Spatially covariant
  gravity with two degrees of freedom: A perturbative analysis up to cubic order".
- S2 (SECOND route, independent): arXiv:2403.15355 (HTML) = Chin. Phys. C,
  10.1088/1674-1137/ad47a9 — "Spatial covariant gravity with two DOF in the
  presence of an auxiliary scalar field: perturbation analysis".
- S3: arXiv:1910.13995 (abs) = PRD 101 (2020) 064018 — "SCG theories with two
  tensorial DOF: the formalism".
- S4: arXiv:1806.02811 (abs) = JCAP 05 (2019) 024 — "SCG with velocity of the
  lapse function: the Hamiltonian analysis".
- S5: arXiv:1409.6708 — "Hamiltonian analysis of spatially covariant gravity"
  (PDF unreadable via fetch → used for cross-reference only, not quoted).

## A1/A2 coefficient functions — CONFIRMED (S1, verbatim)
Case I (f3 = f̃3 = 0). The two GR-limit-admitting 2-DOF branches:

Solution A1 (Eqs. 87-88, Action 106):
    C4 ≠ 0,  ω2 = C1 N/(C5 − 2 C2 N),
    ω3 = (2 C1 C2 C5 D3 − 3 C4 C6) N² / [3 C4 (1 + C2 N)(C5 − 2 C2 N)²],
    b3 = 0,  J3 = D3,
    c1^(1,1,0) = [−6 C4 C6 + 2 C1 C2 D3 (C5 + 2 C2 N)] / [C1 C2 (C5 − 2 C2 N)].

Solution A2 (Eqs. 90-91, Action 107):
    C4 ≠ 0,  ω2 = C1 N/(C5 − 2 C2 N),  C5 ≠ 0,
    ω3 = D1 N² / [(1 + C2 N)(C5 − 2 C2 N)] ≠ 0,
    b3 ≠ 0,  J3 = D3,  c1^(1,1,0) = −2 D3.

KEY STRUCTURAL FACT (corroborates the no-go): Actions S^A1 (106) and S^A2 (107)
are built ONLY from K̂_ij, K, ³R, ³R_ij combinations — they contain NO lapse-
acceleration (a_i = D_i ln N) terms at all. The admissible 2-DOF cubic branches
are acceleration-free.

## "No 2-DOF for nonlinear lapse derivatives" — CONFIRMED (S1, verbatim, §III.2)
- "no 2-DOF theory can be constructed in this branch because the required
  constraints are mutually inconsistent" (Case II, f3 ≠ 0).
- "This result indicates that the cubic terms containing the acceleration, i.e.,
  spatial derivatives of the lapse function, inevitably reintroduce an additional
  scalar degree of freedom beyond the two tensor modes."
- Solution C (the branch that DOES carry acceleration terms) "lack[s] a proper
  GR limit" (§III.3).
⇒ Independent of the repo's own derivation, the literature says: you cannot put a
  nonlinear function of the lapse-acceleration into the gravitational sector and
  keep 2 DOF + a GR limit. The MOND F(a²/a0²) must live OUTSIDE this sector.

## Quadratic degeneracy d2² = 4 c4 d1 — CONFIRMED from the SECOND route (S2)
S2's concrete d=2 Lagrangian gives the degeneracy condition verbatim:
    Eq. (89):  d2² − 4 c4 d1 = 0   (with the companion Eq. (90): 2bb′ − 2b′² + bb″ = 0).
This is EXACTLY the repo's established "d2^2 = 4 c4 d1" for the quadratic
lapse-acceleration sector c4 a_i a^i + d2 a_i D^i φ + d1 D_i φ D^i φ.
Closure `verify_lapse_kinetic_degeneracy.py` (run, PASS): Eq.(89) ⇔ det M = 0 for
the symmetric kinetic form M = [[c4, d2/2],[d2/2, d1]] (rank 2→1). So the
degeneracy is literally a rank drop of the (a_i, D_i φ) kinetic matrix.

## Mechanism: kinetic-matrix degeneracy → SECOND-CLASS pair (S2,S3,S4)
- S3 (abstract): three DOF generically (2 tensor + 1 scalar); TWO necessary-and-
  sufficient conditions remove the scalar — (1) "the lapse function-extrinsic
  curvature sector must be degenerate" and (2) the phase-space dimension "at each
  spacetime point is even".
- S4 (abstract, verbatim): with lapse velocity present, "the condition requiring
  the kinetic terms to be degenerate is not sufficient... because the primary
  constraint due to the degeneracy condition does not necessarily induce a
  secondary constraint, if the mixing terms between temporal and spatial
  derivatives are present. In this case the ... consistency condition must be
  imposed in order to ensure the existence of the secondary constraint and thus
  to remove the unwanted mode."
- Search corroboration (S3-context): "the primary and secondary constraints
  associated with the lapse function become second class, as long as the lapse
  function enters the Hamiltonian nonlinearly."

ANSWER (mechanism): the scalar is removed by a KINETIC-MATRIX DEGENERACY that
GENERATES a primary constraint, supplemented (when temporal-spatial mixing is
present) by a consistency/even-phase-space condition guaranteeing a secondary
constraint; the resulting primary+secondary pair is SECOND-CLASS (because the
lapse enters nonlinearly). It is NOT an extra first-class gauge symmetry. Both
descriptions in the task ("second-class pair" and "kinetic degeneracy") are the
SAME mechanism: the degeneracy is what produces the second-class pair.

## H_i (spatial diffeomorphism / momentum constraint) — first-class by construction
All papers build the action manifestly invariant under spatial diffeomorphisms
(the defining "spatially covariant" property); the momentum constraint H_i is
therefore first-class and untouched — only the lapse (Hamiltonian-constraint /
scalar) sector is modified. INCOMPLETE: no fetched source stated the Dirac
bracket {H_i, H_j} ≈ 0 verbatim; the first-class status is inferred from the
construction (spatial covariance), which is standard and not in dispute.

## Discrepancies / cautions
- None found between the repo's established statements and S1/S2. The repo's
  "d2^2 = 4 c4 d1" matches S2 Eq.(89) exactly, and the "Case II has no 2-DOF"
  and "acceleration reintroduces the scalar" claims match S1 §III.2 verbatim.
- S4 sharpens the mechanism: degeneracy ALONE is insufficient when temporal-
  spatial mixing terms are present — a consistency condition is also required.
  This does not weaken the no-go (it makes the acceleration sector harder, not
  easier, to keep at 2 DOF), but it should be cited alongside the degeneracy
  condition rather than the degeneracy condition alone.
- INCOMPLETE: exact identification of A1/A2's C_i, B_i, D_i as functions of
  (h_ij, ³R, N) beyond the relations above was not extracted; the actions 106/107
  are reproduced structurally. Any downstream embedding must re-fetch S1 for the
  full definitions of C1..C6, B1,B2, D1,D3, b, ω_i before quoting coefficients.
