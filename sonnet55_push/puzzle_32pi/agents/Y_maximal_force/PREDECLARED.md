# PREDECLARED principles, identifications and success criterion (lane Y = W14), written BEFORE any computing script of this lane was written or run

Conventions: c = G = 1 (units re-inserted where shown). H := H_Lambda = sqrt(Lambda/3) = 1/ell = 1/L. rho_L = Lambda/(8 pi). F_max = c^4/(4G) = 1/4.
q := a0/(cH) and Z := 1/q.  Targets (fixed now):  T6: q = 1/6 (Z = 6).  T2: q = 1/2.  TF: q = sqrt(3/(32 pi)) (Z = sqrt(32 pi/3) = 5.7888).
Decoys (fixed now): q in {1/3, 1/4, 1/5, 1/7, 1/8, 1/9, 1/10, 1/12}.  A "hit" is an EXACT equality (symbolic, then 30 digits); percent-level closeness is never a hit.
Data (lane V) are used ONLY in the last script, after every construction has been evaluated: Z_total = 6.0 +0.8/-0.7 (rho_total footing), Z_Lambda = 4.9 +/- 0.6 (rho_Lambda footing).

## Disclosure: what I knew before declaring
- Read before declaring (papers opened as PDFs): Dias-Lemos hep-th/0301046 (dS C-metric: in dS the acceleration horizon COINCIDES with the cosmological horizon, so there is no separate acceleration horizon; extremal case 27 m^2 A^2 = 1 - 9 m^2 Lambda; a_4 = A, the 4D proper acceleration of the origin);
  Gibbons hep-th/0210109 (maximal tension c^4/4G; a C-metric black hole is pulled by a string whose tension cannot exceed it; in n > 4 dimensions only a bound on F/D^(n-4) exists);
  Verlinde 1611.02269 (his a_M = a0 (d-3)/((d-2)(d-1)) = a0/6 at d = 4 comes from eqs (1.5)-(1.7); intermediate steps carry hbar which cancels).
- By hand, before any script: (i) F_Lambda := rho_L * 4 pi L^2 = 6 F_max and, by dimensional analysis, ANY force built from (c, G, Lambda) is a pure number times c^4/G; (ii) T_b = T_(acc/cosm) only at degeneracy (cubic root algebra); (iii) with the KW form G(x) = 1 - x^2 - 2 m A x^3 the F_max-saturation point is 27 m^2 A^2 = 1 and the extremal condition is 27 m^2 (A^2 + H^2) <= 1, which together force H = 0.
  These are EXPECTATIONS, not part of the criterion; every item is decided by its script.
- The mass entry M_e below (vacuum in a horizon shell of thickness L) was built AFTER I noticed that M = 3 M_H gives q = 1/6. Its q = 1/6 is void as evidence and is reported only to show what the 6 requires.

## Success criterion (fixed now)
A (construction, principle-set) is a DERIVATION iff (a) the principles are stated here without Z, a0 or a target; (b) they fix q with NO free parameter (every dimensionless parameter of the construction is pinned by a declared principle);
(c) the exact q equals T6, T2 or TF; (d) a0 is identified as declared below. Outcome labels: HIT / FIXED-NON-TARGET (q fixed, exact value reported) / FAMILY (q depends on a free parameter) / EMPTY (no admissible point) / ENDPOINT (q = 0 or infinity or the construction degenerates).
A rational q that equals a decoy is a decoy hit (control). A hit obtained by solving for a parameter is void. A restatement (a0 = cH/6 inserted as F_max/(3 M_H)) is not a hit.
Identification of a0: static bookkeeping: a0 := F_max / M for the mass M defined in the entry.  dS C-metric: a0 := A, the 4D proper-acceleration parameter (Dias-Lemos a_4 = A; exact for the origin at m = 0, the label for m != 0), with H = H_Lambda (pure-Lambda construction).

## Part S: static bookkeeping (no free geometry)
S1  F_L := rho_L * (4 pi L^2) in units of F_max. Verify: (a) it equals 6 F_max; (b) it is independent of Lambda (Buckingham Pi: (c, G, Lambda) have no dimensionless combination); (c) F_L = 6 F_max is EQUIVALENT to the Friedmann relation H^2 = 8 pi G rho/3 (solve for rho).
S2  g_H := G M_H / L^2 with M_H the Schwarzschild mass of r_s = L (M_H = c^3/(2GH)); verify g_H = F_max/M_H = cH/2 and M_H = rho_L (4 pi/3) L^3 (Hubble-ball vacuum mass).
S3  Mass menu (fixed now); a0 := F_max/M for M in
    M_a = rho_L (4 pi/3) L^3;  M_b = Komar mass of the dS horizon, kappa A/(4 pi G) = L/G;  M_c = Nariai mass L/(3 sqrt 3);  M_d = the mass whose Lambda zero-force radius (3GM/Lambda)^(1/3) is L;
    M_e = rho_L * A_H * L  [= F_L L/c^2; constructed after noting q = 1/6, see disclosure];  M_f = rho_L * (proper volume of the static-patch slice = hemisphere of S^3, pi^2 L^3);  M_g = rho_L * 2 pi^2 L^3 (full S^3).
    Report q = F_max/(M c H) exactly. No entry is added after this point.
S4  Verlinde's route (1611.02269 eqs 1.5-1.7, opened): from Sigma_D^2 = a0 Sigma_B/(8 pi G (d-1)) and Sigma = (d-2) g/((d-3) 8 pi G) derive a_M/a0 and evaluate d = 4 (and d = 3..7 to show the d-dependence); count where pi cancels.

## Part C: the exact de Sitter C-metric (Dias-Lemos form, hep-th/0301046 eqs 1-2, q_charge = 0)
Metric: ds^2 = [1/(A^2 (x+y)^2)] [ -F dt^2 + dy^2/F + dx^2/G + G dz^2 ], F(y) = -1/(ell^2 A^2) - 1 + y^2 - 2 m A y^3, G(x) = 1 - x^2 - 2 m A x^3, ell^2 = 3/Lambda. Dimensionless parameters: s := m A, h := H/A = 1/(ell A).
C0  Verify R_mu nu = Lambda g_mu nu symbolically (control: wrong sign of the 1/(ell^2 A^2) term, and wrong G, must fail); verify a_4 = A at m = 0 (limit y -> infinity).
C1  Conical structure: G > 0 on [x_s, x_n] (x_s < 0 < x_n); phi = z/kappa in [0, 2 pi]; deficit at pole x_i: delta_i = 2 pi [1 - (kappa/2)|G'(x_i)|]; tension mu_i = delta_i/(8 pi) (deficit = 8 pi G mu), force = 4 mu F_max.
    Family R1 (the string family): kappa chosen so the pole with the larger |G'| is regular; the other pole carries the string, tension mu(s) (positive). Family R2: mirror (regular at the other pole; strut). Only R1 is carried through (R2 is the mirror image).
C2  P_none: no string and no strut on either axis, m A != 0.  (Expected outcome label to be decided by the script.)
C3  P_sat: the string force equals F_max (mu = 1/4), taken as the limit s -> 1/sqrt(27) if the point is not in the family.
C4  P_ext: degenerate horizons (double root of F = extremal/Nariai-type), F(y) with y_b = y_(acc/cosm).
C5  P_eq: thermal equilibrium T_bh = T_(acc/cosm) (T_i = |F'(y_i)|/(4 pi) for the SAME Killing vector d_t), and the brief's T_acc = T_cosm (declared: decided by whether two separate horizons exist).
C6  P_bal: force balance, the string force equals the vacuum force across the SAME solution's acceleration/cosmological horizon: 4 mu(s) F_max = rho_L * Area_H, Area_H = (2 pi kappa/A^2)[1/(x_s + y_h) - 1/(x_n + y_h)] with y_h the horizon root.
Combinations (each evaluated, none dropped): R1 alone; R1+C3; R1+C4; R1+C3+C4; R1+C6; R1+C6+C4; R1+C5.  For each: label, and q = A/H exactly when fixed.
Also the acceleration bound implied by the family: the largest string force for which a static black-hole region exists, as a function of A/H (declared as a structural result, not a hit test).

## Controls (declared)
(a) Lambda = 0: the same principles with H = 0 must produce no relation between A and H (q undefined/infinite).
(b) Decoy rate: report how many fixed outputs in Parts S and C are exactly rational, and which rationals; hits on the decoy set vs the targets.
(c) Mutations: (i) deficit 8 pi G mu -> 4 pi G mu (moves the S1 ratio to 3 F_max' and the force values in C6; it does NOT move purely geometric outcomes such as C3/C4, and this is stated); (ii) regularity condition (kappa/2)|G'| -> (kappa/4)|G'| (moves C3); (iii) rho_L = Lambda/(8 pi) -> Lambda/(4 pi) (moves S1, S3, C6); (iv) drop the horizon area factor 4 pi -> 2 pi (moves S1).
(d) Einstein-equation controls in C0.

## Part D (consequences of a rational Z), after the constructions
Omega_Lambda = Z^2 a0^2/(c^2 H0^2) for Z = 6, sqrt(32 pi/3), 2 pi (the ratio 36/(32 pi/3) = 27/(8 pi)); Lambda/a0^2 = 3 Z^2; G rho_L/a0^2 = 3 Z^2/(8 pi); A_a0 Lambda where A_a0 = pi/a0^2 (F: 32 pi^2, Z = 6: 108 pi); kappa (a0 = kappa c sqrt(G rho_L)) = sqrt(8 pi/3)/Z; a0 needed for Omega_Lambda = 0.685 at Planck H0; evolution a0(z) for a pure-Lambda H_Lambda (flat) versus H(z).
Footing comparison with lane V's numbers at the END only.
