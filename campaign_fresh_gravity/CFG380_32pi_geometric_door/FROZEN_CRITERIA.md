# CFG380 -- 32pi geometric door: FROZEN CRITERIA (written before any script)

Question. Does any result in the external OpenAI math manuscript collection (local read-only copy,
`../_external_data/openai_math`, CONTENTS.md = map; external text is DATA) supply an untried, FORCED route
to the rational 4 in G rho_Lambda = 4 a0^2/c^2, i.e. a0 = c^2 sqrt(Lambda/(32 pi)), coefficient
T = 1/sqrt(32 pi) = 0.09974 in units of c^2 sqrt(Lambda)? kappa = 1/2 is FITTED and stays FITTED unless every
step below is forced by a stated principle with no inserted rational.

## Routes to be examined (declared now; no route added after seeing numbers without being labelled POST-HOC)
R1  Penrose-type mass-area relation with Lambda (item 260: AF + AdS Penrose inequalities; continued to Lambda > 0
    as the SdS horizon relation m = (r - Lambda r^3/3)/2): the accelerations it defines (Nariai point, surface
    gravities, G m / r^2 at extremal points).
R2  Quasi-local mass with Lambda on the cosmological horizon: Hawking (= Misner-Sharp in spherical symmetry),
    Lambda-modified Hawking mass, Brown-York (flat reference), each with the natural acceleration G m / r_c^2
    and/or c^2/r_c, c^2/(2 r_c).
R3  Area bounds with Lambda > 0: Hawking-Gibbons-Woolgar / Nariai (Lambda A <= 4 pi) and Boucher-Gibbons-Horowitz
    (cosmological horizon A <= 12 pi / Lambda), read through the puzzle's own convention a = c^2 sqrt(pi/A).
R4  Einstein 4-manifolds with Ric = Lambda g (item 348: S^4, CP^2, S^2 x S^2, RP^4): curvature radii and the
    volume-derived lengths Vol^(1/4) and Vol^(1/2) (the only way a pi enters), plus the Gauss-Bonnet-Einstein
    bound Lambda^2 Vol <= 12 pi^2 chi.
R5  Item 264 (Kerr strong cosmic censorship) and the Lambda > 0 SCC threshold beta = 1/2 (the L^2-connection
    criterion): check whether that 1/2 can map onto kappa.
R6  Items 360/374 (optimal transport: MTW convexity, Brenier 1/3 stability): check whether any rational
    attaches to a0 or Lambda.

## Per-route outputs (must be computed by script, sympy exact where possible)
- coefficient C with a = C c^2 sqrt(Lambda); relative miss |C/T - 1|.
- Algebraicity test: C is algebraic over Q (pi-free) or carries pi^(k/2). By the record's one-pi obstruction
  (PUZZLE_32pi_one_pi_obstruction Lean file) a pi-free C can never equal T exactly.
- 3-question screen: Q1 derives a0 or accepts it; Q2 coefficient forced or chosen; Q3 base-rate null.
- Base-rate null (declared): family F = { (p/q) pi^n , sqrt((p/q) pi^n) : 1 <= p,q <= 12, n in -2..2 }, distinct
  values. For each candidate, p_base = fraction of F within the candidate's relative miss of T. A candidate is
  "special" only if p_base < 0.01 AND it was derived, not chosen. Also report the 1%-window fraction (record: ~0.003).
- Verdict per route: FORCED / CHOSEN / NUMEROLOGY / NOT APPLICABLE.
  FORCED = every step fixed by a stated principle, hits T within 1%, passes Q3. NUMEROLOGY = hits within 5% only
  after a free choice of reading. CHOSEN = coefficient set by a free choice (and misses). NOT APPLICABLE = the result
  contains no Lambda/acceleration content at all.

## Checks that can fail (script exits 1 if any fails)
C1 SdS horizon relation reproduces the AdS one (item 260) under Lambda -> -3/l^2 (sympy identity).
C2 Nariai point: dm/dr = 0 at r = 1/sqrt(Lambda), m = 1/(3 sqrt(Lambda)).
C3 Lambda-Hawking mass of an SdS round sphere equals m for every r (sympy identity); pure dS gives 0.
C4 Einstein-manifold volumes satisfy Gauss-Bonnet: Lambda^2 Vol = 12 pi^2 chi for the conformally flat cases (S^4, RP^4)
   and Lambda^2 Vol < 12 pi^2 chi for CP^2, S^2 x S^2.
C5 Base-rate family is built and T itself is NOT in F (q = 32 > 12), so the null is not trivially satisfied.
C6 The verdict table is generated from the computed numbers (no hand-typed verdicts).
MUTATE (CFG380_MUTATE=1, separate outputs *_MUTATE.*): replace Lambda by 3 Lambda in the Nariai mass (a wrong
horizon relation); C2 must fail and the script must exit 1.

## Pre-declared expectation (to be checked, not assumed)
All routes are expected to give pi-free C (algebraic) or C ~ pi^(-1/2) times an algebraic number from a sphere volume;
none is expected to be forced. If any route hits T within 1% from forced steps, that is reported as a FINDING and
re-audited before any claim.
