# AC17 frozen criteria: relativistic UV sign of the khronon scalar in every direction

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. Reads AZ36 (astra_goal_2026_11_05/AZ36_pn_sign) and
V3X W4c (rebuild_2026_10_22/V3X_v3s_close_undecided); edits neither.

## What is open, and the scoped claim settled here

AZ36 proved exactly that, on a static spherical background, the radial high-frequency mode has
c_rad^2 = gamma B_tau / [(1 + gamma s)^2 + gamma mu^2/(K N^2)], B_tau = s + gamma s^2 + mu^2 (1-N)/(K N^2),
so PN corrections cannot flip its sign. It left open arbitrary propagation directions, nonspherical
backgrounds (the Galactic external field) and metric mixing (NO VERDICT). V3X's PN symbol is
Omega^2 = gamma Theta rho_tau |xi|^2 in every direction; V3X *asserted* that O(GM/c^2 r) corrections do
not flip it.

Claim graded here (AC17-UV): on ANY static background with conformally flat spatial metric
(ds^2 = -N^2 dt^2 + Psi^4 dx^2, exact, no PN expansion; this covers every static spherical background,
and the Sun + uniform external field at the order of the background used by V3X), with arbitrary
background polarization P0^i(x) on the switched-on branch s > 0, the UV principal symbol of the
khronon/polarization scalar sector, in every propagation direction k, has real positive omega^2 and a
positive kinetic coefficient, i.e. the relativistic corrections do not flip the PN sign. Graded on
the Solar-System background, both footings.

Not claimed: the finite-wavelength (non-WKB) spectrum's relativistic corrections, the switch
interface, moving/rotating sources, nonlinear well-posedness (AC16), causality (AC18).

## Method (Stueckelberg khronon, sympy, exact)

tau = t + sigma(t, x). u_mu = -N_tau d_mu tau, N_tau = Xt^(-1/2), Xt = -g^{mu nu} d_mu tau d_nu tau.
P^mu orthogonal to u (P^t fixed by P^mu d_mu tau = 0). a_mu = h_mu^nu d_nu ln N_tau, so P^mu a_mu =
P^nu d_nu ln N_tau. s = D_mu P^mu = (1/sqrt(-g)) d_mu(sqrt(-g) P^mu) - P^mu a_mu. Q = 1/N_tau.
v3s on-region density (AZ36 normalization):
  L = sqrt(-g) [ P^mu a_mu - W(K|P|) - (gamma/2) s^2 + mu^2 (Q - 1)^2 / (2K) ].
AC2q on-region: the clock is the dark-energy scalar, phi = phidot0 tau, X = (phidot0^2/2) Xt; add
sqrt(-g)(X - V) and replace s by s + 2X in the stiffness, minus the -(gamma/2)(2X)^2 off-term (AC7).
Perturb sigma, P^i -> P0^i + p^i, and the lapse N -> N + n (the gravitational coupling of n kept at
the PN order V3X used, -|grad n|^2 Psi^2 .../(2K) form, stated in the script). Second-order
Lagrangian, Euler-Lagrange equations (variational derivative, so integrations by parts are exact),
then the UV principal symbol: omega ~ |k| -> infinity with background coefficients frozen at the point,
keeping in each equation the highest total derivative order that survives. Background derivatives
(d P0, d N, d Psi) that multiply principal terms are kept as point values. W enters through W1 = W'(x0),
W2 = W''(x0), x0 = K|P0|, with W1 > 0, W2 > 0 (H >= K, V3X) as hypotheses.

## Gates

G1 (exact, symbolic): the principal omega^2 roots are written as positive factor x B(k_hat), and B
is reported in closed form. Third-derivative terms in the EL equations must cancel exactly (else the
UV counting is wrong and the label is NO VERDICT).
G2 (Solar background, numerical, mpmath 50 digits): nodes r = 1, 3, 10, 30, 100, 300, 1000 AU, both
footings (canonical a0 9.3603e-11, Lstar 21.68 pc; alt 1.1312e-10, 22.85 pc), N and Psi of the Sun +
Galactic external potential (g_ext = 1.9e-10 m/s^2 with 2.3e-10 also run), background P0 = Sun hedgehog
(V3X K4: D.P0 = M/(2 pi Lstar^2 r) inside 1e-3 Lstar) plus a uniform external part |P_ext| taken at its
UNSCREENED bound g_ext/(K c^2) (conservative), 13 directions of P_ext relative to r_hat, 400 directions
of k. B(k_hat) > 0 and omega^2 > 0 at every node, direction and footing; the minimum of
B(k_hat)/B_PN (B_PN = the V3X value rho_tau = D.P0) is reported.

## Lines

- PASS if G1 holds with B(k_hat) > 0 under stated hypotheses or numerically at every G2 point, both
  footings, both actions, K1-K3 pass and MUTATE bites.
- FAIL if any G2 point has B < 0 or omega^2 < 0 (confirmed at 50 digits): a direction in which the
  relativistic correction flips the PN sign. The direction and node are reported.
- NO VERDICT only if G1's third-derivative cancellation fails, a known answer fails, or MUTATE does not bite.

## Known answers and controls (separate outputs)

- K1: spherical background, P0 radial, k radial: B equals AZ36's B_tau times a positive factor, using
  the background P equation (symbolic residual 0). If the decoupled calculation does not reproduce
  AZ36's sign factor, that is reported as a failed known answer.
- K2: PN limit (N, Psi -> 1, |P0| -> 0 at fixed D.P0): omega^2 -> gamma rho_tau |k|^2 (V3X W4c (c)).
- K3: P0 = 0, mu = 0, gamma = 0: the sigma sector is empty (sigma pure gauge, GR).
- MUTATE (AC17_MUTATE=1): gamma -> -gamma. omega^2 < 0 must appear at every G2 point; else no power.
