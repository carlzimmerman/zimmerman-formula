# PREDECLARED principles, closures and success criterion (written BEFORE any script of this lane was run)

Lane S: quasi-local energy and gravitational field-energy budgets.  Units c = 1, G explicit where it matters.

## Conventions (fixed now)
- rho := rho_Lambda (energy density), p = -rho.  Friedmann for the vacuum: H^2 = 8 pi G rho/3, L = 1/H.
- xi := a0^2/(G rho c^{-2}...) i.e. xi = a0^2/(G rho) (c = 1).  The puzzle says xi = 1/4.  Z = H/a0, Z^2 = (8 pi/3)/xi.  xi is NOT used until the last step of each script.
- Working units for every scan: a0 = G = c = 1, so G rho = 1/xi, H^2 = 8 pi/(3 xi), L = sqrt(3 xi/(8 pi)); every quantity is then a function of the single unknown xi.
- Length scales derived from a0 alone: R_a = 1/a0 (Rindler length), r_sa = 1/(2 a0) (Schwarzschild radius of the black hole whose surface gravity is a0).  Masses: M_a = 1/(G a0), M_s = 1/(4 G a0) (that black hole), M_dS = L/(2G) (Misner-Sharp mass of the dS horizon = E_vac(L)).
- MOND radius r_M(M) = sqrt(G M/a0); Schwarzschild radius r_s(M) = 2 G M.
- E_vac(R) := (4 pi/3) rho R^3.  Deep-MOND point-mass field g(r) = sqrt(G M a0)/r for r >= r_M.

Disclosure of what I already knew before declaring (not part of the criterion): the puzzle target xi = 1/4; the record's principle-free 'forced kernel' a0 = H (xi = 8 pi/3); by hand I expect (a) every local density equality u(a0) = rho gives xi in pi x Q (kappa about 5), (b) the deep-MOND field energy of a point mass diverges logarithmically at both ends, (c) with r_in = r_M and R = L the ratio E/M is bounded by a0 L/(3e).  None of (a)-(c) is used to choose or reject a principle; each principle is decided by its script.

## Field-energy density conventions (magnitudes; the SIGN question is a separate check in s02)
- D0: w0(g) = g^2/(8 pi G)      (Poisson-normalised Newtonian form applied to the field strength g)
- D1: w1(g) = g^3/(12 pi G a0)  (AQUAL F-term, F = (2/3) y^{3/2}: the deep-MOND form of the same gradient term)
- D2: w2(g) = g^3/(6 pi G a0)   (AQUAL on-shell localisation |F - 2 y mu| = (4/3) y^{3/2} (a0^2/8 pi G))
Shell energy E_k(R; r_in) = int_{r_in}^{R} 4 pi r^2 w_k(g(r)) dr with the point-mass field above.

## Principle families (each is a physical statement + a formal equation for xi)

### TYPE I -- local density equalities (no closure needed)
- I1: w0(a0) = rho     (u_g of the a0-field equals the vacuum energy density)
- I2: w1(a0) = rho
- I3: w2(a0) = rho
- I4: (task wording: 'a0-field energy density equals the vacuum energy at the radius where the two accelerations match') at the zero-gravity radius r* of a point mass, defined by g_MOND(r*) = g_Lambda(r*) = H^2 r* (the vacuum's own repulsive field strength H^2 r, from rho + 3p = -2 rho), require w_k(g(r*)) = rho for k = 0, 1, 2.  This contains M; it is decided only after an M-tie of TYPE III (M in {M_a, M_s, M_dS}).
- I5: 'strength-H field' Friedmann reading: w0(H) = rho/3 (identity, used as a bookkeeping check, not a principle).

### TYPE II -- surface / column budgets (closure: a length ell)
Brown-York (membrane) surface pressure of an acceleration horizon with acceleration a: s_BY = a/(8 pi G) (derived in s01; equals T_U x sigma_BH with T_U = a/2 pi, sigma_BH = 1/(4G)).
- II1: s_BY(a0) = rho * ell   for ell in { R_a, r_sa, L }
- II2: T_dS sigma_BH = H/(8 pi G) versus rho * ell for ell in { L, R_a, r_sa } (H/(8 pi G) = rho L/3 is an identity; the other two are principles)
- II3: the puzzle read as 'column vacuum energy over the Rindler length = 32 pi times (T_U sigma_BH)': declared as a RESTATEMENT (planted control, must be flagged as such).

### TYPE III -- integrated point-mass field-energy budgets (a grid; 3 x 3 x 3 x 5 x 3)
Unknown xi.  Grid axes, each fixed here:
- density convention D in {D0, D1, D2}
- inner cut r_in in {0 (D0 only), r_M(M), r_s(M)}
- outer radius R in {L, R_a, r_sa}
- mass tie M in { M_a, M_s, M_dS, E_vac(R), M with r_M(M) = R (i.e. M = a0 R^2/G) }
- target T in { M (rest energy), E_vac(R), R/(2G) (the mass that would make R a horizon) }
Equation: E_D(R; r_in, M) = T.  Entries with r_in >= R are 'empty'.  Entries whose equation contains no rho (R in {R_a, r_sa}, M-tie not using rho, T not E_vac) are classified 'rho-free': identity (scale-free) or inconsistent; they fix nothing.  Entries with rho are solved for xi > 0.
- III-bound (analytic, declared): sup over M of E_D(L; r_in = r_M(M))/M for D1, D2 (scale-free upper bound in terms of a0 L).

### TYPE IV -- vacuum-ball self-energy budgets
- IV1: Newtonian self-energy of a uniform ball of vacuum energy E_vac(R): |U| = (3/5) G E_vac^2 / R.  Principle: |U| = E_vac(R) (compactness / 'zero-energy' budget) with R in {R_a, r_sa} (R = L carries no a0).
- IV2: same with the deep-MOND-corrected self-energy: skip (no principled definition); recorded as not done.
- IV3: Brown-York energy of the dS tube, E_BY(R) = (R/G)(1 - sqrt(1 - R^2/L^2)), versus E_vac(R): the ratio is a function of R/L only; principle: E_BY(R) = 2 E_vac(R) picks R = L (no a0).  Recorded as a scale-free identity check.

### TYPE V -- quasi-local horizon quantities of the a0-black-hole versus the vacuum
- V1: E_BY(r_sa) = r_sa/G = E_vac(R) for R in {R_a, r_sa}.
- V2: horizon thermodynamic energy T S = M_s/2 (Smarr) equals E_vac(R) for R in {R_a, r_sa}.
- V3: horizon area times vacuum density: G rho A(r_sa) = 4 pi (the record's K_Sigma = G rho identity) -- declared RESTATEMENT (planted control).

### TYPE VI -- the factor-4 chain (item 4 of the lane task)
rho/u_g(a0) = 32 pi = 8 pi x 4.  Candidate quasi-local readings of the '4', each stated with its d-dependence BEFORE computing:
- Q1 trace count: -T^mu_mu(vacuum)/rho = d + 1.
- Q2 Schwarzschild: 4 = (1/(kappa r_s))^2 with kappa = (d-2)/(2 r_s) -> (2/(d-2))^2.
- Q3 area/disc: Omega_{d-1}/V_{d-1} (area of S^{d-1} over volume of B^{d-1}).
- Q4 Bekenstein-Hawking quarter: 1/(1/4) = 4 (d-independent).
- Q5 Brown-York/Komar factor: E_BY(horizon)/M_Komar = 2, squared.
- Q6 thermodynamic decomposition of the Poisson 8 pi: 8 pi = 2 pi (Unruh) x 4 (quarter), so 32 pi = 2 pi x 16 = 2 pi x 4 x 4.
For each: is it EQUAL to 4 at d = 3 for a structural reason, does the corresponding principle (stated as a budget equation) actually produce xi = 1/4, or is it a restatement.

## Success criterion (fixed now)
A principle SUCCEEDS iff (a) it is stated without Z, a0's value, 32 pi or any target (the closures above are the only inputs and were declared here, not tuned); (b) its solution xi equals 1/4 (i.e. Z^2 = 32 pi/3) EXACTLY (sympy equality, or 1e-12 relative for numerical roots) and the coefficient is produced by the principle, not inserted; (c) the hit is not reproduced at comparable frequency by decoy targets.
A principle whose closure carries the puzzle's own coefficient (a length equal to r_sa or R with the factor 2 built into the definition, or an equation of the form G rho r^2 = 1) is a RESTATEMENT, not a success.  Planted controls: II3 and V3 must be detected as hits (script sanity), and mutating E_vac's 4 pi/3 -> 4 pi must change the pi-classification.
Decoy calibration: the identical grid is re-solved with decoy targets xi_d in {1/2, 1/3, 1/6, 1/8, 1/5, 2/3, 3/4, 1/16, 2/3pi, 2 pi/27, 1/(4 pi)} and the number of exact hits is compared with the number at xi = 1/4.
Classification requested (item 3): for every solved entry, the pi-class of xi (Q, Q x pi, other) and of Z^2 = (8 pi/3)/xi; and the same classification if Lambda (not G rho) is the fixed variable: a0^2/Lambda = xi/(8 pi).
