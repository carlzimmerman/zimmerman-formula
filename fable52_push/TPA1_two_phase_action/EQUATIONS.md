# The two-phase action and its field equations

TPA1, 2026-11-09 (criteria b81c28d00c). TEST lane: this file states equations and their limits; it adopts nothing and
relabels nothing. Every equation below was checked against a direct sympy variation of the action (RESULT.md gives the
checks and their residuals). kappa = 1/2 FITTED; not theory closed.

## 1. Conventions

Units c = 1 and K = 4 pi G; signature (-, +, +, +). Restoring c: K -> 4 pi G/c^2, the prefactor of R is c^4/(16 pi G), and
a0 -> a0/c^2 inside W. Two footings are carried and never pooled: canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 m/s^2,
with a0 = kappa c sqrt(G rho_DE) and kappa = 1/2 fitted.

Definitions (PAPER70). tau is the clock (khronon); Q = sqrt(-g^{mn} d_m tau d_n tau) (= 1/N in unitary gauge);
n_m = -d_m tau / Q; h_mn = g_mn + n_m n_n; l = ln Q; A_m = n^n nabla_n n_m = -h_m^n d_n l; D_m = h_m^n d_n;
Pi = D_m P^m = nabla_m P^m - P^m A_m; Phat = P/|P|. As in QX17, P^m A_m is written -P^m d_m l and Pi = nabla.P + P^m d_m l;
the two forms differ by terms proportional to n.P, which the multiplier absorbs.

## 2. The action

    L/sqrt(-g) = [R - 2 Lambda]/(4K) + L_K(Q) + S(n_d) Lam_law + lambda n^m P_m + L_m                         (A_S)

    L_K(Q)  = mu_K^2 (Q - 1)^2 / (2K)
    Lam_law = P^m A_m - W(K|P|) - gamma_L F(Pi)
    W(p)    = (a0^2/K) [ -p/a0 - ln(1 - p/a0) ],     gamma_L = K Lstar^2 / 2,
    F       = the adopted Pi^6 blend, F(Pi) = b^2 f(Pi/b), b = rho_DE (F = Pi^2/2 for Pi >= b; F ~ Pi^6 near 0).

L_m is minimally coupled matter. This is PAPER70's action (A) with one change: the law's whole Lagrangian Lam_law is
multiplied by the switch S.

**The density the switch reads.** n_d = mu_K^2 (Q - 1)/K = L_K'(Q). It is the charge density of the clock current when the
law sector is absent (the "rho" of the clock charge N = rho + Pi), and a function of Q alone. Write

    S_Q = dS/dQ = (mu_K^2/K) S'(n_d),     S_QQ = (mu_K^2/K)^2 S''(n_d).

**The switch.** S is C^2, non-increasing, S = 1 for n_d <= n_1 and S = 0 for n_d >= n_2 (0 < n_1 < n_* < n_2).

**Where S sits (reading R1).** S multiplies the Legendre pair P.A - W and the stiffness together; the constraint does not
carry S. The equations below are written with two switches, S_L on the pair and S_F on the stiffness: R1 is S_F = S_L = S;
the form with the stiffness outside the switch (V0) is S_F = 1. Putting S on the constraint as well is equivalent on shell
wherever S > 0 (lambda -> S lambda).

## 3. Field equations

**(E1) Multiplier.**

    n^m P_m = 0 .

**(E2) P equation** (vary P_m):

    S_L ( -d^m l - K W'(K|P|) Phat^m ) + gamma_L [ d^m (S_F F') - S_F F' d^m l ] + lambda n^m = 0 .

Leaf part:

    S_L ( A_m - K W'(K|P|) Phat_m ) + gamma_L [ D_m (S_F F') + S_F F' A_m ] = 0 .

Normal part (fixes the multiplier), with ln N = -l:

    lambda = ( S_L + gamma_L S_F F' ) n.d ln N + gamma_L n.d (S_F F') .

- At gamma_L = 0 the leaf part is S (A_m - K W' Phat_m) = 0, so for every S > 0

      K|P| = a0 |A| / (a0 + |A|)      (the Legendre map; S drops out because it multiplies P.A and W together).

  With S on P.A alone the map would be K|P| = a0 S|A| / (a0 + S|A|) (Lean pa_only_distorts).
- R1 with gamma_L > 0, where S > 0:

      (1 + gamma_L F') A_m + gamma_L D_m F' + gamma_L F' D_m ln S = K W'(K|P|) Phat_m ,

  which is QX17's screened law (E2) exactly wherever S is locally constant, 0 < S < 1; the wall adds gamma_L F' D ln S.
- V0 (stiffness outside S): (S + gamma_L F') A_m + gamma_L D_m F' = S K W' Phat_m, i.e. gamma_L -> gamma_L / S.

**(E3) Clock equation** (vary tau): a conserved clock current,

    nabla_m [ n^m rho_Q - lambda P^m / Q ] = 0 ,

    rho_Q = n_d + nabla_a [ (S_L + gamma_L S_F F') P^a ] / Q + S_{L,Q} (P.A - W) - gamma_L S_{F,Q} F .

Under R1 the new term is S_Q Lam_law = (mu_K^2/K) S'(n_d) [P.A - W - gamma_L F]. At leading order the charge is
N = n_d + Pi + S_Q Lam_law: the record's N = rho + Pi plus the switch term.

**(E4) Metric equation** (vary g^{mn} at fixed tau, P_m, lambda):

    G_mn + Lambda g_mn = 2K ( T^m_mn + T^Q_mn + T^L_mn + T^lam_mn ) ,

    T^Q_mn   = g_mn L_K + (mu_K^2/K) Q (Q - 1) n_m n_n
    T^L_mn   = g_mn S_L (P.A - W) + 2 S_L P_(m d_n) l + nabla.(S_L P) n_m n_n + S_L K W'(K|P|) P_m P_n / |P|
               + gamma_L [ -g_mn S_F F + h_mn nabla.(S_F F' P) - 2 P_(m curlyD_n) ]
               + Q [ S_{L,Q} (P.A - W) - gamma_L S_{F,Q} F ] n_m n_n ,
    curlyD_n = d_n (S_F F') - S_F F' d_n l ,
    T^lam_mn = -2 lambda n_(m P_n) .

Energy density seen by the clock frame:

    n^m n^n T^L_mn = S_L (W + Pi) + P.dS_L + gamma_L S_F F + Q [ S_{L,Q} (P.A - W) - gamma_L S_{F,Q} F ] .

**(E5) Conservation.** For any fields (off shell),

    nabla^m (T^Q + T^L + T^lam)_mn = E_tau d_n tau + E_P^m (d_n P_m - d_m P_n) - P_n nabla_m E_P^m + E_lam d_n lambda ,

with E_tau = -nabla_m [n^m rho_Q - lambda P^m/Q], E_P^m the left side of (E2) and E_lam = n.P. On shell the right side
vanishes, so the contracted Bianchi identity gives nabla^m T^m_mn = 0: matter falls on geodesics of g. Since d_n tau is
along n_n, the leaf part of the identity holds on the (E1)-(E2) shell alone; the clock equation is its normal part.

**Force on a carrier.** If S's argument is held (S an external field), diffeomorphism invariance gives instead, on the P shell,

    nabla^m (T^L + T^lam)_mn = Lam_law d_n S ,

so the law sector hands whatever carries S the force density f_n = -Lam_law h_n^m d_m S. It vanishes wherever S is uniform.

## 4. Reductions

### 4.1 The S = 1 phase (n_d <= n_1)

S = 1 and S' = S'' = 0: every equation is QX17's (with the QX17D general-F stress). Static, weak, spherical, mu_K = 0:
Gauss gives u (1 - 1/(1 + u)) = y, i.e. g^2 = g_N (g + a0) (Lean static_law_phase).

### 4.2 The S = 0 phase (n_d >= n_2)

S = S' = 0: T^L = 0; the P equation reads lambda n^m = 0, so lambda = 0 and P is undetermined and carries no stress;
rho_Q = n_d. The equations are general relativity with PAPER70's dust: G_mn + Lambda g_mn = 2K (T^m + T^Q),
nabla_m (n^m n_d) = 0. a0 does not appear (the S = 0 Lagrangian contains no a0).

### 4.3 FRW

Isotropy gives A = 0, and the P equation then forces W'(K|P|) = 0 wherever S > 0, i.e. P = 0. Lam_law(P = 0) = 0, so the
background equations do not contain S at all:

    Qbar = 1 + I0 / (2 mu_K^2 a^3),   rho = I0 (1 + w0/a^3) / (8 pi G a^3),   w = w0 / (w0 + a^3),   w0 = I0 / (4 mu_K^2).

A small S = epsilon on the background changes the background by exactly zero, at every order.

### 4.4 Linear perturbations about FRW

Unitary gauge (lapse 1 + alpha, P_i first order). Because Lam_law is quadratic in perturbations about P = 0, the law sector's
quadratic Lagrangian is

    L2_law = Sbar abar [ P_i d_i alpha - (K/2) P_i P_i ] - Sbar gamma_L F''(0) (d_i P_i)^2 / (2 abar) ;

S' and S'' first enter at cubic order. With Sbar = 0 the law drops out: the linear theory is GR, the baryons and the cold
component. With Sbar = epsilon and the adopted blend (F''(0) = 0), eliminating P gives epsilon abar |d alpha|^2/(2K), so the
coefficient of alpha^2 in the cold component's quadratic action becomes

    (abar^3 / 2K) [ mu_K^2 Qbar^2 + epsilon k^2 / abar^2 ] .

Quasi-static growth (Jeans form, proper wavenumber k, first order in nbar):

    omega^2 = -K nbar [ 1 - k^2 / (mu_K^2 + epsilon k^2) ] .

epsilon = 1 gives K nbar / (1 + k^2/mu_K^2), the record's clock self-growth R f (RK04); epsilon = 0 gives the isolated-fluid
Jeans form K nbar (1 - k^2/mu_K^2). The first correction in epsilon is + epsilon K nbar (k/mu_K)^4.

### 4.5 Static weak field

Static clock tau = Q_inf t, so Q = Q_inf/N and A = grad ln N = grad Phi. With the switch's argument held (S a given field):

    div[ (1 - S/(1 + u)) grad Phi ] + mu_K^2 Phi = 4 pi G rho_b ,    u = |grad Phi|/a0 ,

SWT1's class with PAPER70's mu_K^2 term. With the argument being the static clock's own density, n_d = -mu_K^2 Phi/K
(Q_inf = 1), one more term appears:

    div[ (1 - S/(1 + u)) grad Phi ] + mu_K^2 Phi = 4 pi G rho_b + mu_K^2 S'(n_d) J(|grad Phi|) ,

J(g) = (a0^2/K)[u - ln(1 + u)]: a layer of (mu_K^2/K) S' J where S varies, zero in each phase.

**Wall pressure.** On the P shell the law's leaf stress along the field is T^L_xx = -S W(K|P|). With the Newtonian
gravitational stress, the momentum flux is Pi_xx = E^2/(2K) - S W(K|P|). Across a wall where S falls from 1 to 0 at fixed
displacement y (sources fixed; y = u^2/(1 + u)):

    Pi_in - Pi_out = (a0^2 / 4 pi G) [ u - ln(1 + u) - u^2 / (2 (1 + u)^2) ] ,    outward,

and along fixed displacement dPi/dS = J, so the carrier's force density is -J dS (the force of (E5) with Lam_law = J).
The clock gives the same number: the S' term of rho_Q is the law's partial pressure S Lam_law on the dust, and its gradient
at fixed field is the same force density. With the clock term's sign reversed the force points inward (Lean
flipped_clock_inward).

For a static clock the force is balanced identically by the weight of the switch's own energy layer Q S_Q Lam_law n n:
nabla^m (T^L + T^lam)_mx = 0 for any profile. A static configuration places the wall on an equipotential.

**Static existence.** For a static clock, n_d = mu_K^2 (Q_inf/N - 1)/K falls as N rises, so for any non-increasing S the
switch S(n_d(N)) rises with N (Lean static_clock_monotone): the law-on phase is where the potential is shallow and the dust
phase where it is deep. A static clock cannot hold a cleared region (law on) inside a dust envelope.

### 4.6 The other reading of n_d (D2)

If the switch reads the full leading charge N_2 = n_d + Pi, S depends on D.P and the P equation is no longer algebraic:

    S(N_2) ( A_m - K W'(K|P|) Phat_m ) = D_m [ S'(N_2) Lam_law ]          (static weak form),

so the Legendre map fails wherever S' is non-zero, P obeys a second-order equation in space, and the switch reads the
law's own phantom density Pi as dust. In each phase (S' = 0) D2 equals D1.

## 5. Health

Decoupling limit (metric frozen, gamma_L = 0, P eliminated by the Legendre maximum), static clock tau = Q_inf t + pi,
frozen-coefficient WKB with every coefficient's x-dependence kept. The clock Lagrangian is L_eff = N [L_K(Q) + S J(|A|)].

- No new mode: L_eff has no (d_t d_t pi)^2 term; the symbol is quadratic in omega (one clock mode), in each phase and in the
  wall. P stays non-dynamical.
- Kinetic coefficient (large k): S J''(A) k^2/Qbar^2 + mu_K^2/K + O(S_QQ W): positive throughout the grid. No ghost.
- Gradient coefficient, field along x (longitudinal) and across it (tangential), with p = |Pbar| = (a0/K) u/(1 + u):

      G_long = (N/Qbar) [ n_d - S_Q W(K p) + S p'/Qbar ] ,      G_tan = (N/Qbar) [ n_d - S_Q W(K p) + S (p' + A p)/Qbar ] .

  In the wall, -S_Q W > 0 dominates (S is non-increasing): the switch stabilises. In the S = 0 phase G = N n_d/Qbar > 0
  (the k-essence clock, c_s^2 = (Qbar - 1)/Qbar). In the S = 1 phase, G < 0 wherever n_d < -p'/Qbar: a law-on static clock
  whose own dust density is below the outward fall-off rate of the law's polarization is gradient-unstable, growing at a
  rate of order sqrt(K x phantom density). The threshold is 0.08 to 0.9 of the law's phantom density for a point mass.


kappa = 1/2 FITTED; not theory closed. Adopts nothing.
