# EW2 iter_1 frozen criteria: the record's best AeST form, stated exactly

Kappa = 1/2 FITTED; not theory closed. Committed with ../FROZEN_CRITERIA.md before any script or number. No gate is
graded here; the file fixes what iter_2..iter_4 test.

## Which form

The record's AeST forms: AX1/AeST (plain AeST, AQUAL static limit; FAIL Cassini Q2 2.44-5.15x), v4 (AeST + C1's capped
F + gamma_L; I1, M1, C7, N0), SZ21's own finite-lambda_s family (H1: fails SPARC once BBN's lambda_s >= 24.7). The best
form for the owner's "works everywhere" is v4, the only one whose static sector is the canonical law AND screens the
Sun (C1: AeST reproduces AQUAL, the clock term and gamma_F; gamma_L must be added). It is the form graded below.

## The action (record transcription; SZ21 eq. 5 + C1 + I1)

S = Int sqrt(-g)/(16 pi G~) [ R - (K_B/2) F_{mu nu}F^{mu nu} + 2(2-K_B) J^mu D_mu phi - (2-K_B) Y - F(Y, Q)
      - lambda (A.A + 1) - (gamma_L/K^2) (q^{mu nu} D_mu D_nu phi + theta Q)^2 ] + S_m[g]

with J^mu = A^nu D_nu A^mu, q^{mu nu} = g^{mu nu} + A^mu A^nu, Q = A^mu D_mu phi, Y = q^{mu nu} D_mu phi D_nu phi,
theta = D_mu A^mu, K = 8 pi G~/(2 - K_B) = 4 pi G, G = 2 G~/(2 - K_B).

Free functions (exact, from the record):
- F(Y, Q): its Y-dependence at Q = Q0 is F(Y, Q0) = (2 - K_B) Jcal(Y) (C1 K2), and its Q-dependence at Y = 0 is K(Q)
  (SZ21 L300 / L396: 8 pi G~ rho = Q K' - K on FRW). The Y-part sets the static law, the Q-part the FRW dust.
- Jcal(Y) = 2 a0^2 [ -y - ln(1 - y) - y^2/2 ], y = sqrt(Y)/a0 (C1 K2; capped: Newtonian regime is Y -> a0^2;
  small-Y limit (2/(3 a0)) Y^{3/2}, i.e. SZ's lambda_s -> infinity, F_Y(0) = 0).
- K(Q) = -2 Lambda + K2 (Q - Q0)^2 (SZ21 L300; quadratic Higgs-phase K as in AN1/H2).

Constants: K_B <= 0.078 (BBN, C2 K6); gamma_L via L* in {24, 50, 90} pc (FITTED window, D10/C3; beta_L =
(2-K_B) L*^2/2); mu = sqrt(2 K2/(2 - K_B)) Q0 (the dust/mass scale); I0 = a^3 K'(Q) (the dust charge, an initial
datum: Omega_aest is FITTED, C2 K2); Delta (the static zero point of Phi, a per-object integration constant, VSZ).
Declared mu values in the record (no new value is introduced): AN1 list {0.0156, 0.1, 1, 10, 56.6, 2.04e4, 1.24e8}
Mpc^-1, H2 grids {0.1, 0.3, 0.5, 0.7, 1.0} (allowed by SZ21 / VSZ "mu^-1 >~ 1 Mpc") and {1.58, 2.0, 3.0} (probes),
C7's Q0 = 0.1 Mpc^-1.

## Static (quasi-static, weak-field) equations used by iter_2..iter_4 (H2's exact spherical form; VSZ / SZ21)

  lap Phi~ + mu^2 Phi = 4 pi G rho_b ,  div[Jcal' grad chi] = lap Phi~ ,  Phi = Phi~ + chi ,  Psi = Phi.

Spherical: M_eff(r) = M_b(r) - (mu^2/G) Int_0^r Phi r'^2 dr',  Phi'(r) = sgn(M_eff) g_AQUAL(G |M_eff|/r^2, a0),
g_AQUAL(gN) = gN/2 + sqrt(gN^2/4 + a0 gN). Zero point: VSZ's Delta (H2's phi_c_for: lambda = lambda_max + Delta,
lambda_max = (2/3)(1 - ln(3 sqrt2/(mu r_M))), imposed on the mu = 0 solution at R_ref = 3 Mpc); primary Delta = 0.
gamma_L enters only inside L* of each mass (v3s screening; C3, C6, C6P) and is not in this form at r >> L*.

Hydrostatic (static-branch) dust density: delta rho_d = -mu^2 Phi/(4 pi G) (H2, from SZ21 L396, L300, L361, L379).

Linear FRW (C2 K1, C7 D1-D2): Y = 0 at orders eps^0 and eps^1, so Jcal drops out of the linear equations; the scalar is
pressureless dust for k < a mu (comoving) and has the Jeans-type band k > a mu, unbounded for F_Y(0) = 0 (H1; with
gamma_L the band ends at k_c ~ 242 Mpc^-1 physical at mu^-1 = 1 Mpc, L* = 24 pc).

## Known-answer checks (iter_1)

- KA1: replay C1's sympy script (covariant_push_2026_10_22/C1_aest_embedding/c1_aest_embedding.py, read-only copy run
  in scratch, outputs saved here as ew2_c1_replay.out): 8/8 PASS, exit 0 (static limit, AQUAL mu = x/(1+x) exact, Phi =
  Psi, clock xi = 1, gamma_L identically absent from AeST).
- KM1 (MUTATE): the same script with C1_MUTATE=1 must fail (C1 recorded 4/8): saved as ew2_c1_replay_MUTATE.out.
- If KA1 fails, iter_2..iter_4 are NOT EVALUABLE.
