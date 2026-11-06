# AC18: constraint causality of v3s and AC2q: light-cone causality FAIL, tau-ordering PASS (scoped)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (5ba6bdfd7c), frozen
before any graded number. Script: ac18.py (sympy + mpmath at 50 digits, single thread, about 10 s).
Astra's AZ39 is read only. AC18 does the calculation AZ39 named as its missing link.

## Labels

- **Criterion B (tau-ordering): PASS.** In the record's weak-field system
  (L = P.grad Xi - (gamma/2)(div P)^2 - W(P), Xi = phi - sigma_t + |grad sigma|^2/2), three exact sympy
  identities hold:
  - the sigma equation is charge continuity q_t + div(q v) = 0;
  - no equation contains a time derivative of P, and the P equation is grad(Xi + gamma q) = 2W'P on each
    leaf;
  - the Euler equation follows from Xi's definition.

  Every equation therefore either evolves forward in tau or holds on one leaf. With one preferred time
  there are no closed signal loops.
- **Criterion A (light-cone causality): FAIL, for v3s and AC2q, on both footings.** Take a background
  with nonzero khronon charge and MOND anisotropy. GR's own metric response is made exactly retarded by
  hand. A conserved test source then still changes a gauge-invariant curvature observable at events
  outside its causal future, through the leaf-elliptic Xi.

## The mechanism (AZ39's missing link, computed)

1. The source mass moves at y, and its retarded potential is supported in |x - y| <= c t. Exact: the
   k -> 0 moments are 0 and -4 pi G m c^2 D(t), with D = Int (t - t') d(t') dt'.
2. The local khronon charge near y responds as delta q = lap g, with g_tt = Pi delta phi_b. This is
   inside the cone.
3. The leaf equation sets Xi_hat = K k^2 g_hat/(k.Mt^-1.k) + gamma k^2 g_hat instantly on the whole leaf.
   Off the source, Xi = K Int H g with H = -x d_e^2 G_b, where G_b is the Green function of the scaled
   Laplacian. H is checked against an independent Radon-transform inverse at 3 points (rel diff <= 3e-31).
   L_Mt H = 0 off the origin, but lap H != 0.
4. At an observer outside the cone, the khronon flow accelerates, d_t delta v = grad Xi. Its charge
   changes, d_tt delta q = -Pi lap Xi, and with it Ric(u_T, u_T) along a free test worldline (relational,
   gauge invariant): delta O = 8 pi G/c^2 [delta q (gamma^2 - 1/2) + 2 Pi gamma^4 v_rel.delta v/c^2].

The violation needs two things together. The first is nonzero charge Pi at the source and at the
observer: KA2 checks that at Pi = 0 nothing reaches the observer, which is AZ39's causal GR branch. The
second is anisotropy (x != 0): KA1 checks that at x = 0, H is a pure delta and Xi vanishes off the
source. Isotropic leaf-elliptic equations with a conserved charge give no outside signal; the
anisotropic MOND Hessian (transverse 1 + x, longitudinal (1 + x)^2) does.

## Numbers

Test mass 1000 kg moved at 1 m/s. Galactic Pi = 0.0447 / 0.0514 Msun/pc^3 and x = 1.15 / 2.6 (AZ37's
provisional transcription), v_rel = 220 km/s.

| footing | t, r | ct/r | abs(dv) (m/s) | dO/O_bg |
|---|---|---|---|---|
| canonical | 1 s, 1e9 m | 0.30 | 3.6e-67 to 9.7e-67 | 6e-77 to 3e-76 |
| canonical | 1 s, 1e10 m | 0.03 | 3.5e-72 to 1.0e-71 | 3e-83 to 4e-82 |
| alt | 1 s, 1e9 m | 0.30 | 9.2e-67 to 7.8e-66 | 2e-76 to 4e-75 |
| alt | 1 s, 1e10 m | 0.03 | 8.9e-72 to 8.6e-71 | 3e-82 to 4e-81 |

- All 36 graded observer rows (6 directions) are nonzero on both footings. They sit 4e15 above the
  double-precision floor of the evaluated expression.
- The dipole term dominates: higher moments add 3e-4 to 1e-3 at ct/r = 0.03, and up to 0.1 at
  ct/r = 0.3.
- Scaling: dv grows as t^6 and falls as r^-5.
- AC2q: AC10 S1 maps AC2q's leaf onto v3s's. The s^2 regulator changes the leaf operator by relative
  <= 2.3e-32 (canonical) and 5.8e-32 (alt) at 1e10 m, far below 1e-6, so the label carries to AC2q.

## Known answers and controls

- A1, KA3: the retarded moments match a direct 40-digit quadrature at small k (rel 1.3e-17).
- KA1 (isotropic) and KA2 (zero charge): both give zero outside response.
- MUTATE (`AC18_MUTATE=1`, separate outputs ac18_MUTATE.*): make the leaf equation hyperbolic. Its
  speeds are c/sqrt(1+x) and below, the earliest arrival lands after the sample time on every row, and
  the label becomes PASS-AT-THIS-ORDER. The control bites.
- A rerun gives an identical result JSON (sha1 0cd122c77fab, runtime field excluded).
- Recorded slips:
  - The frozen grid named (t = 10 s, r = 1e9 m), which lies inside the light cone. Those 6 rows are
    printed as excluded, not graded.
  - The first run built a sixth-order symbolic derivative tower and was killed after about 7 hours
    without writing output. The rerun takes the same derivatives with mpmath on the unit sphere (H is
    homogeneous of degree -3). The equations and lines are unchanged.

## What it means, and what it does not show

- This confirms C8's conclusion (a real, non-gauge influence faster than light, ordered in tau) on the
  charged, screened branch that AZ39 required. It now rests on a computed gauge-invariant observable and
  not on the elliptic form alone.
- AZ39's caution was right in one respect: a conserved charge with isotropic coefficients is causal
  (KA1). The violation comes from the anisotropic MOND response, so it is present wherever the theory
  does MOND.
- The effect is tiny: about 1e-67 m/s in the khronon flow for a ton moved at 1 m/s, seen 3 light-seconds
  away. No data constrain it.
- The theory is causal in the sense of criterion B (one global time) and is not light-cone causal. This
  is the khronometric / Horava structure, and no reading of v3s or AC2q removes it.
- Not shown: strong-field leaves, orders beyond leading in G and t (higher moments are reported), a
  non-frozen background, or any observational bound.
