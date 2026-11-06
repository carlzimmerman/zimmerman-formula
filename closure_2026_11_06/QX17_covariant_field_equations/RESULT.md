# QX17: the full field equations of v3s (2026-11-06)

**Label: CERTIFIED** (criteria d6c0fe3a0c; script `qx17.py`, output `qx17.out` / `qx17.json`; MUTATE twin `qx17_MUTATE.*`).
Adopts nothing. kappa = 1/2 FITTED. Not theory closed. Units c = 1, K = 4 pi G (restore c: K -> 4 pi G/c^2, see §6).

Until today the record had only the **limits** of the action: the static AQUAL equation, the weak-field PN system and
the FRW reduction (EQUATIONS_IN_ORDER.md §2-3). This file gives the **complete covariant Euler-Lagrange set**: the
metric, khronon, P and multiplier equations, with every stress tensor written out. Each one is checked against a direct
sympy variation of the Lagrangian density (§5).

## 0. Which action

PAPER68 (and EQUATIONS_IN_ORDER §1) print

    S = (1/4K) Int sqrt(-g) [R - 2J(Y) + 2K(Q)] - (gamma_L/2) Int sqrt(-g) [max(D.P, 0)]^2 + S_m .

**Read literally, that has a misprint.** P appears only in the stiffness, so its own equation forces D.P to be constant and P
decouples from gravity. The form every lane has actually solved (C4 K3, C6, H4, V3W, X3, AC15) puts J(Y) in
**Legendre form**:

    S = Int sqrt(-g) { [R - 2 Lambda + 2 mu_K^2 (Q-1)^2]/(4K) + P^m A_m - W(K|P|) - gamma_L F(Pi) + lambda n^m P_m } + S_m      (A)

    W(p) = (a0^2/K)[-p/a0 - ln(1 - p/a0)],   F(Pi) = [max(Pi,0)]^2 / 2,   Pi = D_m P^m,   gamma_L = K Lstar^2/2 .

**K0 (sympy, exact).** Maximizing over P gives back the printed J:
max_P [P.A - W(K|P|)] = (a0^2/K)[u - ln(1+u)] with u = |A|/a0, attained at K|P| = a0 u/(1+u). So at gamma_L = 0,
(A) is exactly -J_x(Y)/(2K). With gamma_L > 0, P is a genuinely independent field and (A) is the theory.
**PAPER68 should carry (A).** That is an erratum on the printed form only; no number changes.

## 1. Definitions (all covariant; tau = the khronon)

| symbol | definition |
|---|---|
| Q | sqrt(-g^{mn} d_m tau d_n tau)  (= 1/N in unitary gauge tau = t) |
| n_m | -d_m tau / Q  (unit, future, hypersurface-orthogonal) |
| h_mn | g_mn + n_m n_n  (projector onto the leaves) |
| l | ln Q |
| A_m | n^n nabla_n n_m = -h_m^n d_n l  (= d_i ln N in unitary gauge) |
| D_m f | h_m^n d_n f  (leaf gradient) |
| Pi | D_m P^m = nabla_m P^m - P^m A_m = (Q sqrt(-g))^{-1} d_m (Q sqrt(-g) P^m)   (= D_i P^i, since Q sqrt(-g) = sqrt(gamma)) |
| Pi_+ | max(Pi, 0);  F = Pi_+^2/2,  F' = Pi_+  (F is C^1, so every equation below is defined) |
| P-hat | P/|P|,  |P| = sqrt(g^{mn} P_m P_n) |
| curly D_m | d_m Pi_+ - Pi_+ d_m l  =  Q d_m (Pi_+/Q) |

## 2. The field equations

**(E1) Multiplier.**

    n^m P_m = 0 .

**(E2) P equation** (vary P_m), full and then split along n and along the leaves:

    -d^m l - K W'(K|P|) Phat^m + gamma_L (d^m Pi_+ - Pi_+ d^m l) + lambda n^m = 0

    leaves:   (1 + gamma_L Pi_+) A_m + gamma_L D_m Pi_+ = K W'(K|P|) Phat_m          [the screened constitutive law]
    normal:   lambda = (1 + gamma_L Pi_+) n^m d_m ln N + gamma_L n^m d_m Pi_+            (fixes the multiplier)

At gamma_L = 0 the leaf part is |A| = K W'(K|P|), so K|P| = a0 x/(1+x) with x = |A|/a0: the Legendre map of K0.
With K W' = a0 p/(a0 - p) it inverts to K|P| = a0 |E|/(a0 + |E|), with E_m = (1 + gamma_L Pi_+) A_m + gamma_L D_m Pi_+.

**(E3) Khronon equation** (vary tau): a conserved khronon current,

    nabla_m [ n^m rho_Q  -  lambda P^m / Q ] = 0 ,
    rho_Q = J_P / Q + mu_K^2 (Q - 1)/K ,      J_P = nabla_m [ (1 + gamma_L Pi_+) P^m ] .

So the khronon dust is the charge rho_Q carried along n, with a leafwise flux lambda P/Q. In unitary gauge (tau = t, lapse N,
shift N^i, spatial metric gamma_ij):

    d_t (sqrt(gamma) rho_Q) - d_i [ sqrt(gamma) ( N^i rho_Q + lambda N^2 P^i ) ] = 0 ,
    rho_Q = N { D_i[(1 + gamma_L Pi_+) P^i] + (1 + gamma_L Pi_+) P^i A_i } + mu_K^2 (1/N - 1)/K .

To leading order rho_Q = D.P + mu_K^2 (Q - 1)/K. That is the record's rho_tau (BS24 hold equation, H4).

**(E4) Metric equation** (vary g^{mn} at fixed tau, P_m, lambda):

    G_mn + Lambda g_mn = 2K ( T^m_mn + T^Q_mn + T^W_mn + T^P_mn )          (2K = 8 pi G)

with T_mn = -(2/sqrt(-g)) delta(sqrt(-g) L)/delta g^{mn}:

    T^Q_mn = g_mn L_K + (mu_K^2/K) Q (Q - 1) n_m n_n ,          L_K = mu_K^2 (Q-1)^2/(2K)

    T^W_mn = -g_mn W(K|P|) + K W'(K|P|) P_m P_n / |P|

    T^P_mn = g_mn (P.A) + 2 P_(m d_n) l + (nabla.P) n_m n_n  -  2 lambda n_(m P_n)
             + gamma_L [ -g_mn F + 2F h_mn + h_mn P^r curlyD_r - 2 P_(m curlyD_n) ] .

Energy density seen by the foliation (n^m n^n T_mn) of the non-GR sector:

    rho = (mu_K^2/2K)(Q^2 - 1)  +  W(K|P|)  +  Pi  +  gamma_L F(Pi)          (K5)

In the weak field W ~ |grad Phi|^2/K is post-Newtonian, so rho -> D.P + mu_K^2 (Q-1)/K: Poisson for all mass, as in the record.

**(E5) Matter.** S_m is minimally coupled to g, so nabla^m T^m_mn = 0 (baryons fall on geodesics of g).

**(E6) Consistency (Noether; not checked numerically).** (A) is diffeomorphism invariant and the constraint is carried by a
multiplier. So on shell of (E1)-(E3), nabla^m (T^Q + T^W + T^P)_mn = 0 and the Bianchi identity is respected. Conversely,
(E4) plus matter conservation imply the khronon equation (E3) wherever d tau is non-zero, as in every khronometric theory.

**The switch.** Pi_+ is continuous, but d Pi_+ jumps where Pi crosses 0. So (E2)-(E4) hold in the weak (distributional)
sense across the switch surface. Inside Pi < 0 lobes every gamma_L term is zero and the equations are the unscreened
Khronon's. X3/AC15 solved exactly this system.

## 3. Reductions (each one is the record's)

| limit | from (E1)-(E4) | record |
|---|---|---|
| FRW, P = 0 | (E3): a^3 mu_K^2 (Q-1)/K = const, so Qbar = 1 + I0/(2 mu_K^2 a^3); rho = I0(1 + w0/a^3)/(8 pi G a^3), w = w0/(w0 + a^3), w0 = I0/(4 mu_K^2); J, a0 and gamma_L absent (Y = 0, Pi = 0) | C4 K7 (K4 here) |
| static, weak, gamma_L = 0 | (E2) gives K P = (1 - mu) grad Phi; (E4)_00 gives Poisson with rho_b + D.P; together div[mu(|grad Phi|/a0) grad Phi] + mu_K^2 Phi = 4 pi G rho_b, phi = psi | C4 K1 / BS24 Eq. 3.21 |
| static, weak, gamma_L > 0 | (1 + gamma_L Pi_+) grad Phi + gamma_L grad Pi_+ = K W' Phat (the record keeps the linear version grad Phi + gamma_L grad(div P)); the Cassini hedgehog inside Lstar | C6 / C6P / X3 |
| spherical static, mu_K = 0 | g^2 = g_N (g + a0) (law S) | LEAN QX1.balance_iff_lawS |

The (1 + gamma_L Pi_+) A and gamma_L Pi_+ d l pieces are **new**: they come from D.P = nabla.P - P.A in the covariant form.
The weak-field record drops them. **Size (ARGUED, not a re-solve)**, with the record's Solar-System values:
- gamma_L Pi_+ = 2 pi G rho_tau Lstar^2/c^2. At rho_tau = 0.045 Msun/pc^3 that is 6.4e-12 / 7.1e-12 (Lstar 21.7 / 22.9 pc)
  and 1.1e-10 at 90 pc (AC7 Q3's number). So (1 + gamma_L Pi_+) moves the constitutive law by <= 1.1e-10.
- P.A in Pi = nabla.P - P.A, and Pi_+ d l next to d Pi_+, are relative corrections of size |A| r/c^2 ~ U = GM/(c^2 r):
  2.6e-8 at Mercury, 9.9e-9 at 1 AU, 9.9e-10 at 10 AU (2.1e-6 at the solar surface). These are 1PN corrections to the
  stiffness that sets the hedgehog.
- The smallest Cassini margin on record is 4.8e7 (C6P). A relative change <= 2.6e-8 in the anomaly cannot move any C6P
  label. A full PDE re-solve with these terms has **not** been done.

## 4. What this does not cover

- **AC2q** (candidate, not adopted): replace Pi_+ by max(Pi + 2X, 0), drop K(Q), make phi the clock. Its equations follow by
  the same steps; they are not written or checked here.
- The GR part (R, Lambda) is standard and not re-derived.
- Well-posedness, PN sign and causality are separate lanes (AC16-AC18).

## 5. Checks

| check | what | result |
|---|---|---|
| K0 | Legendre: max_P[P.A - W] = (a0^2/K)[u - ln(1+u)] | PASS, sympy exact (residual 0) |
| K1 | (E2) P equation, 3 components | PASS, max rel 3.8e-41 |
| K2 | (E3) khronon equation | PASS, max rel 1.8e-41 |
| K3 | (E4) full non-GR stress tensor, all 6 components in 2+1 | PASS, max rel 1.2e-40 |
| K4 | FRW: Qbar, rho, w equal to C4 K7 | PASS, sympy exact |
| K5 | n.n T = rho_Q-sector + W + Pi + gamma_L F | PASS, max rel 6.9e-41 |

Method: the Lagrangian density (A) minus R, Lambda is built on jet symbols. Euler-Lagrange derivatives are taken against
g_ab, tau (to second order), P_a and lambda, and evaluated (mpmath, 40 digits) on 3 random polynomial configurations in
2+1 dimensions (seeds 11/22/33, Pi = 0.59/1.01/0.92 > 0 branch, n.P = 0 imposed by P = h.V). 2+1 is the smallest dimension
where h_mn differs from P_m P_n/|P|^2. The equations are written without dimension-specific identities, so they hold in 3+1.
W is a generic test polynomial in K1-K3, so the equations hold for any W; the physical W enters only through K0.
Runtime 1715 s, 0.5 GB RSS, one thread.

**MUTATE** (`QX17_MUTATE=1`): flips the sign of Pi_+ d l inside curlyD in (E4) and of the lambda flux in (E3).
K2 then fails at 0.17-0.78 and K3 at 0.010-0.33 (worst component per seed) on all 3 seeds, as it must (`qx17_MUTATE.out`, 1757 s). K1 still passes because it was not mutated.

First run: crashed before any number on a script bug (`sp.diff(tau, c)` instead of `X[c]`). Fixed and rerun; no graded
number came from the crashed run.

## 6. Restoring c

With x^0 = c t: K = 4 pi G/c^2 multiplies the matter-like pieces. The prefactor of R is c^4/(16 pi G). A_m carries 1/c^2
(Y = A.A/c^4). a0 -> a0/c^2 inside W (a_geo).
