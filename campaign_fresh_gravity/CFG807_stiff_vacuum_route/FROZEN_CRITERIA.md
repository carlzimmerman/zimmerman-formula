# CFG807 FROZEN CRITERIA: does the stiffened action revive the "dark energy = the a0-field's vacuum energy" route?

Written and committed ALONE before any script exists. Block: CFG807 (this lane only).

## Question
PAPER42 (with PAPER41's turn-off) reads the observed Lambda as the zero-field energy of the MOND field:
Lambda c^4/a0^2 = int_0^inf y (nu - 1) dy (BIMOND alpha = 1 normalisation), finite only with a strong-field turn-off y_t
(k = 2: (pi/4) y_t - (1/8) ln(4 y_t) + 1/16; y_t = 128.9 on the kappa = 1/2 footing; p45). The record then found
(sonnet55_push/puzzle_32pi p56/p57/p58) that this class fails Cassini Q2 (kappa < 0.17) and that a y_t ~ 129 turn-off
dominates extreme-TNO precession (43/90 objects) and over-fills the detached disk (p57, occupancy 0.69 vs Newton 0.07).

The frozen canonical action (THEORY_CANONICAL_2026-10-14 S2):
L = -|grad Phi - K P|^2/2K - rho Phi - W_rem(u) - (gamma/2)|grad P|^2, K = 4 pi G, u = K|P|, K W_rem' = u^2/(a0 - u),
gamma = K L*^2/2, L* in [5.75 pc, >~ 1 kpc]. CFG770: this action passes Cassini by stiffness screening.

Target dictionary (D_kappa, THEORY_PUSH_2026-10-14): S2 vacuum energy eps = (a0^2/K) C; kappa = 1/2 <=> C = 16 pi
<=> rho_DE c^2 = 4 a0^2/G <=> Lambda c^4/a0^2 = 32 pi.

## Script 1 (cfg807_solar.py): solar-system objections inside the stiffened action
- S1 Cassini: Q2 from the CFG770 linear-response machinery (copied, not imported), with the background response
  (A_par = dg_N/du, A_perp = g_N/u at the Galactic field) computed from the law WITH a k = 2 turn-off on the phantom,
  u_t(y) = u(y)/(1 + (y/y_t)^2), y = g_N/a0, for y_t in {32, 64, 128.9, 1000} and without one; 3 Galactic fields x 2
  footings; L* = 5.75 pc. PASS iff worst |Q2| < 5.2e-27 s^-2 (Park+2026 2 sigma, as CFG770) for every y_t.
- S2 TNO: anomalous radial acceleration of the stiff action at 30-20000 AU (CFG770 a_anom, canonical footing, middle
  Galactic field), orbit-averaged Gauss apsidal rate for the 90 SBDB objects (a > 150 AU, q > 30 AU; file sha256
  ba561f97...), versus the giant-planet quadrupole rate (p56's formula). PASS iff |w_anom/w_pl| < 0.1 for all 90 objects
  AND the anomaly's apsidal period exceeds 4.5 Gyr for at least 80/90. Report p56's turn-off count (43/90) beside it.
- S3 (reported): the turn-off radius r_t = sqrt(GM_sun/(y_t a0)) versus the stiffness length; whether the turn-off can
  change the Sun's response at all (|u_sun|/a0 at 1-2000 AU).
- MUTATE (CFG807_MUTATE=M1): stiffness off (unscreened simple-mu phantom of the Sun, EFE neglected as in p56):
  S2 must FAIL.

## Script 2 (cfg807_vacuum.py): is the P-sector vacuum energy well-defined, and does the action fix it?
- V0 (sympy): the S2 Euler-Lagrange equations are independent of an additive constant in W_rem, and K W_rem''(0) = 0
  holds for every such constant (criticality, Theorem B of D_kappa).
- V1: evaluate the PAPER42 premise "no vacuum constant in the strong-field state" in BOTH normalisations available in
  the S2 action: (a) the potential form, eps_W = W_rem(0) - W_rem(u_strong); (b) the Legendre/QUMOND-dual form,
  eps_Q = (1/K) int_0^inf u dg_N. Report sign and finiteness of each for the frozen W_rem.
  "Well-defined" = finite AND positive (de Sitter sign) in at least one normalisation WITHOUT an added constant.
- V2: can a strong-field turn-off (the device that makes the PAPER41/42 integral finite) be written as a single-valued
  W_rem(u)? Test: is u_t(g_N) monotone (then R = K W_rem' is single-valued)? Controls: frozen S2 law (monotone ->
  representable), exponential RAR (record finite 12.99, p21) and the k = 2 turn-off. Also test the general statement
  numerically: for continuous R(u) with R(0) = 0 onto [0, inf), eps_Q grows without bound with the upper limit.
- V3: does any element of the action fix y_t or C? Candidates: (i) L* (the only stiffness scale): the stiff screening
  cut-off of a point mass, y_t(M) = (r_M/L*)^2 (mass-dependent?), and c^2/(a0 L*); (ii) gamma = K L*^2/2 (enters only
  gradients: uniform-state energy unchanged?); (iii) K = 4 pi G (fixes only the unit a0^2/K). MUTATE-style tooth:
  vary L* x2 and M x10 -> if the candidate y_t moves, it is not a universal vacuum number.
- V4 (reported): coefficient C(y_t) for a hand-set k = 2, 3, 4 turn-off in the QUMOND-dual form; the y_t that gives
  C = 16 pi. Also Lambda c^4/a0^2 = 2C in single-field units (no BIMOND factor 1/(1+alpha)).
- MUTATE (CFG807_MUTATE=M2): monotonicity detector restricted to y <= 1 (below every turn-off maximum): the RAR and
  turn-off controls must then be mis-reported -> the control check FAILS.

## Verdict classes (decided by the checks above, nothing else)
- ROUTE REVIVED: S1 and S2 PASS, AND V1 well-defined, AND V3 finds an action element that fixes C with no hand-set
  number, with C in [33.0, 128.3] (D_kappa PASS-DATA; PASS-EXACT iff C = 16 pi).
- ROUTE UNBLOCKED: S1 and S2 PASS, AND V1 well-defined (or V2 representable with a finite positive eps), but C rests
  on a hand-set number (y_t or the additive constant).
- STILL BLOCKED: S1 or S2 FAIL (label BLOCKED-SOLAR), or S1 and S2 PASS but the vacuum energy is not well-defined in the
  stiffened action and no single-valued W_rem hosts a finite turn-off (label BLOCKED-STRUCTURAL).
- A y_t or C chosen to match Lambda is NEVER a derivation. kappa = 1/2 stays FITTED unless REVIVED-EXACT.

## Standing
No dark matter particle species; cold energy mass still required; never "theory closed". Machine rule: pgrep for
1024^3 runs before every computation. Scripts: numpy/scipy/sympy, seconds, one process, nice.
