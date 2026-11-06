# AC18 frozen criteria: constraint causality of v3s and AC2q on charged backgrounds

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed.
Adopts nothing. No dark-matter particle. Astra's AZ39 files are read only, never edited.

## Why

AZ39 (b0061761eb) left full constraint causality NO VERDICT. It showed the P = 0, Q = 1 GR branch is
causal, and that C8's step from "a leaf-elliptic equation" to "a physical instantaneous signal" omits
a calculation. Its exact missing link: on an on-shell NONZERO-CHARGE background, take the response to a
conserved source with specified initial data, keep the metric's own (GR) response retarded, and test
whether a gauge-invariant local observable changes outside the source's causal future.
AC18 does that, scoped as below, and gives a label.

## Two claims, graded separately

- Criterion B (tau-ordering): every equation of the weak-field system is either an evolution forward in
  tau or an equation on a single leaf. No equation couples different leaves backward. With one preferred
  time there are no closed signal loops.
- Criterion A (light-cone causality): no conserved baryonic source changes a gauge-invariant local
  observable at an event outside its causal future.

## The system (the record's weak-field v3s system, AC15 S1 / AZ37 / H4, mu_K = 0)

L = P.grad Xi - (gamma/2)(div P)^2 - W(P),  Xi = phi - sigma_t + |grad sigma|^2/2,  v = -grad sigma,
plus GR for phi. Charge q = div P. The W Hessian at the background P is K Mt, with
Mt = (1 + x)[I + x e e] (transverse 1 + x, longitudinal (1 + x)^2, the record's M_theta bracket; C8's
Dh). Here e is the background field direction and x the background MOND ratio.

- S1 (sympy, exact): (a) the sigma equation is charge continuity q_t + div(q v) = 0; (b) neither P nor
  Xi carries a time derivative, so the P equation grad(Xi + gamma q) = K W'(P) holds on each leaf;
  (c) the gradient of Xi's definition is the Euler equation Dv/Dt = -grad phi + grad Xi. S1 settles
  criterion B: PASS if (a)-(c) hold as identities, FAIL otherwise.
- GR's part is made exactly retarded by hand: phi obeys the wave equation Box phi = 4 pi G rho. This is
  conservative. Any outside-cone effect found is then not the Newtonian limit's own instantaneous Poisson.

## The calculation (criterion A)

Background: frozen local coefficients (charge Pi, x, e uniform over the region considered). This is
valid for observer distances r much smaller than the background's scale, |grad Xi|/(K Pi) (kpc). The
r used below is far below it, and the correction is O(r / that scale).
Source: a test mass m at y, at rest for t < 0, displaced as d(t) = v_s t e_s for t >= 0. Conserved.

Leading order in G and in t:
1. delta phi_b: the exact retarded solution. It is supported in |x - y| <= c t (sympy: its k -> 0
   moments; zeroth = 0, first = -4 pi G m c^2 D(t), with D = Int (t - t') d(t') dt').
2. The charge response is delta q = lap g, with g_tt = Pi delta phi_b (from S1). g is supported in the
   same ball.
3. The leaf equation gives Xi_hat = K k^2 g_hat/(k.Mt^-1.k) + gamma k^2 g_hat. This is instantaneous.
   Outside supp g, Xi(x) = K Int H(x - x') g(x') with H the inverse transform of k^2/(k.Mt^-1.k). The
   gamma part is local and vanishes outside.
4. At an observer x with |x - y| = r > c t: d_t delta v(x) = grad Xi(x) (delta phi_b(x) = 0 there), and
   d_tt delta q(x) = -Pi lap Xi(x).

The observable: O = Ric(u_T, u_T) along a free test worldline T through x, specified before t = 0
(Raychaudhuri focusing of a test cloud). It is relational, so gauge invariant. With the khronon stress
at leading order Pi u_tau u_tau (A22 D3: anisotropic stress O(rho^2)), O = 8 pi G Pi[(u_tau.u_T)^2 - 1/2]
locally. Its perturbation at x is 16 pi G Pi gamma_rel^4 (v_rel . delta v)/c^2 + 8 pi G (gamma_rel^2 - 1/2)
delta q, and T's own displacement enters only at higher order in G.

Graded per footing (canonical a0 9.3603e-11, alt 1.1312e-10; never pooled), with the record's Galactic
inputs (AZ37 transcription, provisional): Pi = rho0 = 0.0447 / 0.0514 Msun/pc^3, x = 1.15 / 2.6.
Lstar 21.68 / 22.85 pc only enters the local gamma part. Source m = 1000 kg, v_s = 1 m/s. Observer
times t = 1 s, 10 s. Observers at r = 1e9 m and 1e10 m (both > c t) in 6 directions: +-e, two
transverse, and two at 45 degrees. v_rel = 220 km/s along e_s.

## Lines

- A1 (exact): delta phi_b and g vanish identically at every sampled observer (supports checked
  analytically).
- A2: H closed form = -x d_e^2 G_b with G_b = 1/(4 pi sqrt(1-b) S), S^2 = rho_perp^2 + z^2/(1-b), and
  b = x/(1+x). Checked against a direct numerical inverse transform at 3 points to 1e-6 relative. Also
  sympy: L_Mt H = 0 and lap H != 0 off the origin.
- A3 (the verdict): FAIL (criterion A violated) if |delta v(x)| > 0 and |delta O(x)| > 0 at one or more
  sampled observer outside the cone on both footings, with the leading-order expression nonvanishing
  analytically (not a roundoff number: required > 1e6 x the double-precision floor of the evaluated
  expression, computed in mpmath at 50 digits). PASS-AT-THIS-ORDER if the leading term vanishes
  identically for every direction. That would not be a full PASS: the next order would be owed.
- AC2q: the same calculation with AC10 S1's map (charge Pi -> Pi + s^2 in the stiffness; P sees
  Pi - s^2). The s^2 regulator changes the leaf operator by relative O(s^2 K r^2) <= (r H0/c)^2. That is
  bounded and must be < 1e-6 of the leading term, so the label carries. Otherwise AC2q is reported
  separately.

## Known answers (must hold, separate outputs)

- KA1 (isotropic): at x = 0, H is a pure delta (local), so Xi = 0 outside supp g and delta v(x) = 0
  exactly. Elliptic leaf equations with uniform isotropic coefficients give no outside signal.
- KA2 (zero charge, AZ39's GR branch): at Pi = 0, g = 0 and every outside quantity is 0.
- KA3: the retarded moments in item 1 match an independent direct quadrature of the k-space retarded
  solution at small k to 1e-10 relative.

## MUTATE (must bite, separate outputs)

Make the leaf equation hyperbolic: add -(1/c^2) d_tt to L_Mt. Its characteristic speeds are
c/sqrt(eig(Mt)) <= c, so its retarded Green function is supported inside the light cone, and Xi at
every sampled observer must be exactly 0. A3 must then return PASS-AT-THIS-ORDER. If the mutant still
returns FAIL, the test cannot tell elliptic from hyperbolic and no verdict stands.

## Scope stated now

Weak field, leading order in G and in t, frozen local background coefficients, a test source. This
settles the support question AZ39 posed (whether the instantaneous leaf equation reaches a
gauge-invariant observable on a charged background). It does not settle the size of any observable
effect beyond the stated numbers, strong-field leaves, or global existence. The label applies to the
causal structure. No data are graded.
