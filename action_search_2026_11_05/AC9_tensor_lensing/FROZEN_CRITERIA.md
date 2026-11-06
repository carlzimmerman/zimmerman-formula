# AC9 frozen criteria: AC2q's tensor speed and lensing slip on its own terms

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED;
not theory closed. Adopts nothing. No dark-matter particle.

## Why

AC2q (AC7, d063cd6e5f) owes "lensing and tensor regrades on its own equations".
Relative to v3s at mu_K = 0 (whose tensor speed and lensing passed in V3W W4a / W3),
AC2q changes two things in the gravitational sector:

1. the stiffness becomes -(gamma/2){[max(D.P + 2X, 0)]^2 - (2X)^2}: on-region
   v3s's -(gamma/2)(D.P)^2 plus T_on = -2 gamma X D.P; off-region T_off = +2 gamma X^2;
2. the clock is the canonical dark-energy scalar (X - V), with no dust.

Item 2 is a canonical scalar: in unitary gauge (phi = phi(t), sigma = 0 in statics,
AC8) it is a barotropic perfect fluid with no anisotropic stress, and it does not
change the tensor principal part (standard). So only T_on and T_off are graded.
Unitary gauge: X = s^2/(2 N^2), s^2 = phidot^2 <= 2 rho_DE (framework-native).

## Tests

T1 (tensor, sympy, method of V3W W4a). TT modes h_+, h_x(t, z) on a frozen
background: lapse N = 1 + A.x, P_j = P0_j + G_jk x_k (constant gradients), with
T_on (and separately T_off) multiplied by N sqrt(h). Graded:
- T1a: no (dh)(dh) term at O(h^2), and every h*dh term is a total derivative
  (folded into the mass): the principal part is GR's, c_T = c exactly.
- T1b: mass term m^2 of the new pieces, numerically on V3W W4a's grid (galactic
  g = a0 and Earth-surface g; Lstar 21.7/24/90 pc canonical, 22.9/24/90 alt;
  |p|/a0 in [0.03, 0.99]; 13 directions; hedgehog gradients at the solar surface)
  with s^2 = 2 rho_DE (bound) per footing. dv/c at 100 Hz must lie inside the
  GW170817 band [-3e-15, 7e-16].

T2 (lensing slip, sympy). Static metric N = 1 + Phi(x), h_ij = (1 - 2 Psi) delta_ij
+ chi_ij (chi traceless), general P_i(x). Derive, from T_on: the Psi source S_Psi and
the anisotropic stress Pi_ij = dT/dchi_ij at chi = 0. In the reduced static GR action
L = (1/8 pi)[(grad Psi)^2 - 2 grad Phi . grad Psi] - rho Phi, the Psi equation is
del^2(Phi - Psi) = -4 pi S_Psi, so slip relative to the dynamical source is
|S_Psi| / rho_tot (likewise |Pi| / rho_tot for the traceless part).
- T2a: S_Psi and Pi_ij vanish identically at s = 0 and at grad Phi = 0, i.e. they are
  O(s^2 * grad Phi * P): beyond O(GM), so v3s's W1 statement "the Psi equation has no
  source at O(GM)" carries to AC2q.
- T2b: bound |S_Psi|, |Pi| / rho_tot <= gamma s^2 a0 r for a deep-MOND profile
  (g = sqrt(G M a0)/r, rho_tot = g/(4 pi G r), |P| <= a0/K), at r = 30/100/310 kpc,
  both footings, Lstar up to 90 pc. Line: < 1e-6, far below W3's v3s bound 6.5e-5
  and the KiDS amplitude error (about 0.2).
- T_off has no P and depends on N only: its Psi source is an isotropic pressure term
  2 gamma X^2 ~ gamma s^4, and Pi = 0. Reported with T2b's numbers.

## Known answers and controls (separate outputs)

- K1: s = 0 gives zero new mass, zero S_Psi, zero Pi (AC2q = v3s at mu_K = 0).
- K2: a planted vector-kinetic test term c P_i P_j h^{ij} N sqrt(h) must return the
  known anisotropic stress Pi_ij = -c (P_i P_j)^TF (method sees anisotropic stress).
- MUTATE (T1): a planted term c P^2 (d_z h_+)^2 N sqrt(h) must make T1a fail.
  If it does not, T1a has no power and no verdict stands.

## Lines

- PASS (tensor) if T1a holds and T1b's dv/c lies in the band on both footings.
- PASS (lensing) if T2a holds and T2b's bound is < 1e-6 on both footings.
- FAIL if T1a fails without the plant, or any graded number leaves its line.
- Either label is scoped: frozen backgrounds, linear in h / first order in chi,
  no nonlinear or Solar-interior solve, no new data graded.
