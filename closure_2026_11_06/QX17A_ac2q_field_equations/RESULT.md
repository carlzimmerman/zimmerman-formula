# QX17A: the full field equations of the AC2q candidate (2026-11-06)

**Label: CERTIFIED** (criteria 1b39bcb871, renamed from QX18 in 100b4d4924; script `qx17a.py`, outputs `qx17a.*`,
MUTATE `qx17a_MUTATE.*`). AC2q is a candidate, **not adopted**. Adopts nothing. kappa = 1/2 FITTED. Not theory closed.
Units c = 1, K = 4 pi G. Definitions as in QX17 §1 (Q, n, h, l = ln Q, A, D, Pi = D.P, P-hat, F = [max(.,0)]^2/2).

## Action (AC7)

    L/sqrt(-g) = R/(4K) + X - V(phi) + P.A - W(K|P|) - gamma { F(Pi + 2X) - (2X)^2/2 } + lambda n.P ,    X = Q^2/2

The dark-energy scalar phi is the clock (tau = phi, Q = |d phi|). There is no K(Q) dust. Write

    Sigma = Pi + Q^2 = D.P + 2X   (the khronon charge),   Sigma_+ = max(Sigma, 0),   curlyD_m = d_m Sigma_+ - Sigma_+ d_m l .

## Field equations

**(F1)** n.P = 0.

**(F2) P equation.** This is v3s's with Pi_+ -> Sigma_+:

    -d^m l - K W'(K|P|) Phat^m + gamma (d^m Sigma_+ - Sigma_+ d^m l) + lambda n^m = 0
    leaves:  (1 + gamma Sigma_+) A_m + gamma D_m Sigma_+ = K W'(K|P|) Phat_m
    normal:  lambda = (1 + gamma Sigma_+) n.d ln N + gamma n.d Sigma_+

**(F3) Clock (phi) equation.** The khronon current, now sourced by the potential:

    nabla_m [ n^m rho_phi - lambda P^m / Q ] = -V'(phi) ,
    rho_phi = J_P / Q + Q [ 1 - 2 gamma (Sigma_+ - Q^2) ] ,      J_P = nabla_m [ (1 + gamma Sigma_+) P^m ] .

At P = 0 and gamma = 0, n rho_phi = -grad phi, so this is box phi = V'(phi), the canonical scalar.

**(F4) Metric equation.** G_mn = 8 pi G (T^m + T^phi + T^W + T^P)_mn, with

    T^phi_mn = d_m phi d_n phi + g_mn (X - V)            ( = Q^2 n_m n_n + g_mn (Q^2/2 - V) )
    T^W_mn   = -g_mn W + K W' P_m P_n / |P|                                   (as v3s)
    T^P_mn   = g_mn (P.A) + 2 P_(m d_n) l + (nabla.P) n_m n_n - 2 lambda n_(m P_n)
               + gamma [ -g_mn F(Sigma) + Pi Sigma_+ h_mn + h_mn P^r curlyD_r - 2 P_(m curlyD_n)
                         - 2 Q^2 Sigma_+ n_m n_n + (1/2) g_mn Q^4 + 2 Q^4 n_m n_n ] .

There is no separate Lambda: V(phi) is the dark energy.

**Foliation energy density** of the P + stiffness sector (K5):

    n.n T^P = Pi (1 - gamma Q^2) + gamma Pi^2/2      (on-region)

In unitary gauge Q^2 = s^2 = phidot^2/N^2. So the -gamma Q^2 Pi piece is exactly the record's T_on = -2 gamma X D.P
(LEAN QX1.ac2q_on), on top of v3s's gamma F.
**Off-region** (Sigma < 0): every Sigma_+ term drops, and n.n T^P = Pi - gamma Q^4/2 + 2 gamma Q^4 = Pi + (3/2) gamma Q^4. The
gamma Q^4 pieces are the record's T_off = +2 gamma X^2 sector. Off-branch is **argued** term by term: those pieces are the same
on both branches and are checked on-branch. No off-branch configuration was evaluated.

**FRW (K4).** At P = 0: Pi = 0 and Sigma = Q^2. The stiffness stress tensor is then identically zero (its g and nn
coefficients cancel), and rho_phi = Q, so box phi = V'. The background is exactly the canonical scalar's, matching
LEAN QX1.ac2q_frw_background.

**Consistency (E6 of QX17 applies unchanged).** Diffeomorphism invariance plus the multiplier give
nabla^m (T^phi + T^W + T^P) = 0 on shell. The clock equation follows from the metric equation wherever d phi is non-zero.

## Checks

| check | what | result |
|---|---|---|
| K1 | (F2) P equation, 3 components | PASS, max rel 6.4e-41 |
| K2 | (F3) clock equation including -V'(phi) | PASS, max rel 7.8e-41 |
| K3 | (F4) full stress tensor (phi + W + P + stiffness), all 6 components in 2+1 | PASS, max rel 4.7e-40 |
| K4 | FRW: stiffness stress zero, rho_phi = Q (box phi = V') | PASS, sympy exact |
| K5 | n.n T^P = Pi (1 - gamma Q^2) + gamma Pi^2/2 | PASS, max rel 1.8e-40 |

Same method as QX17 (jet variation, mpmath 40 digits, seeds 11/22/33, Pi = 0.59/1.01/0.92 so Sigma > 0, generic test W and
V = (2/5) phi - (3/7) phi^2). Runtime 2720 s, one thread.

**MUTATE** (`QX17A_MUTATE=1`) drops the -2 gamma Q^2 Sigma_+ n n term from (F4) and the -2 gamma (Sigma_+ - Q^2) piece from rho_phi.
- K2 fails at 0.23 / 0.39 / 7.3e-3 (seeds 11/22/33; order corrected after 48bc781928) and K3 at worst-component 0.55 / 0.65 / 0.67, as they must.
- K5 also fails (0.81-0.84). That is expected, because the dropped nn term enters it; the criteria did not declare it.
- K1 still passes, because it was not mutated.
