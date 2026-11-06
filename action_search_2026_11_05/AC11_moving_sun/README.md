# AC11: the moving Sun in AC2q's clock frame — NO VERDICT (as AZ37); no exact GR branch, resonance survives

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (8649eb6d06), frozen
before any graded number. Script: ac11.py (sympy + mpmath + DOP853, about 1 min, one thread, below 0.3 GB).
This is the AC2q analogue of astra's AZ37, which is read and reproduced here, never edited.

## Results (both footings, never pooled)

- **B1: AC2q has no exact P = 0 GR branch around a mass.** At P = 0 the P equation reads
  A(1 + 2 gamma X) + 2 gamma D X = 0. A scalar clock has A = -D X/(2X), an identity checked in sympy for general
  phi. Together these give D X (2 gamma X - 1)/(2X) = 0, so D X = 0 and the clock must be geodesic,
  phi = f(tau). The clock's own Klein-Gordon equation, -f'' - f' theta = V'(f), then requires theta = div n to be
  constant on each leaf unless s = f' = 0. On AZ37's Schwarzschild congruence family,
  theta = -(3M + 2r(E^2-1))/(r^{3/2} sqrt(2M + r(E^2-1))) varies along every leaf (E = 1, 13/12, 5/3).
  **BRANCH ABSENT** on the tested family. This is not a theorem about every congruence. The argument via
  Raychaudhuri: d theta/d tau would have to be uniform on a leaf across the Sun's own density jump.
  In v3s (s = 0) there is no Klein-Gordon obstruction, which is why AZ37's branch exists. The miss is small:
  it sources P through 2 gamma D X, of relative size gamma s^2 = 2.4e-17 / 4.0e-17. So AC2q has an approximate
  GR branch, good to that order, but not an exact one.
- **B2: the forced oscillator on AC2q's own linear system is AZ37's, to a few parts per million.** I used AC7's
  hand-built on-region system with a baryon source in the Poisson equation and solved it exactly (Cramer).
  The transfer is single-pole, T = F'/(Omega'^2 - omega^2), with no instantaneous part. At s = 0 it is
  AZ37's K rho0/(Omega^2 - omega^2) identically (B2a).
  - Phase speeds are 753.51-938.42 m/s (canonical) and 851.62-916.84 m/s (alt). The largest relative change
    from s = 0 is 1.9e-6 / 2.5e-6. The clock's s^2 terms add no fast sound speed.
  - **The resonance survives:** pole cosines 0.00204-0.00427 / 0.00231-0.00417, below 1 on every cell.
  - Finite-time response, worst case |rho_tau/rho_source| (B2c): 5.383395e-15 / 6.190140e-15, a relative change of
    3.9e-6 / 4.9e-6 from AZ37's 5.383374e-15 / 6.190110e-15. DOP853 pairs agree with the exact solution to 5.4e-12.
- **B2d: X stays positive.** At the Sun's Fourier amplitude (M k^3/2 pi^2), the linear moving response gives a
  khronon velocity of at most 8.6e-6 c and |dX/X| <= 1.3e-8, far from X = 0, on both footings.
- **B2e: the frozen Galactic background is not the local background at planetary distances.** The Sun's own
  static linear charge is q_sun = Phi_N/gamma. It exceeds the Galactic rho0 by 1.0-1.6e3 at 1 AU and by 105-163
  at 9.58 AU, and the two are equal at 1,000-1,560 AU (Lstar sets, both footings). So for v3s (AZ37) and AC2q
  alike, the AU-scale forced-oscillator test is outside its own validity. The physical problem is the Sun's
  co-moving charged halo matched to the Galactic flow at about 10^3 AU.
  Side effect: AC7 Q3/Q4 used the Galactic 0.045 Msun/pc^3 as the Solar-System D.P. The Sun's own charge is
  larger, so 2 gamma D.P <= 2 Phi_N (4e-6 at the solar surface, under the 1e-3 line), and the Q4 shift
  2 phidot^2/D.P is smaller. Both AC7 bounds still hold, in the conservative direction.
- Off-region (not at the Sun): Omega^2 is k-independent, as in AC7 Q2c, so its phase speed falls with k and a
  resonance exists there too.

**Label: NO VERDICT** on the complete moving-Sun prediction, by AZ37's frozen definitions. There is no
physical inconsistency (Omega'^2 > 0 everywhere, X > 0), no exact branch, and no metric PPN alpha_1 or alpha_2:
a frozen linear response cannot give them, and no static potential is divided into a gravitomagnetic
coefficient. **Compared with v3s:** AC2q is the same at this order (resonance, sizes) and loses v3s's exact
conditional GR branch, keeping it only to about 1e-17.

## Checks, known answers, control

Main: B1a_Peq, B1a_accel, B1b, B2a, B2b_known_canonical, B2c_known (both), B2_resonance, B2_convergence and
B2d_Xpositive all PASS.

**B2b_known_alt FAILS as frozen:** 916.84 m/s against the reference "916.9". That reference was transcribed from
AZ37's README, which rounds its own stored 916.8403359 to 916.9. A comparison against AZ37's stored JSON, added
after the run (B2b_json_*_postrun), agrees to 2.2e-16 on both footings. The frozen check is kept as a FAIL in
the record. The script therefore exits 1, and the label is unaffected.

The first run's B1b also failed. The code had used M = 0 as a known answer, which the criteria did not state,
and that was wrong: a flat radial congruence with E > 1 is itself non-uniform. It was corrected to M = 0, E = 1
(static observers, theta = 0) before any B2 number existed. The first run was also too slow (sp.solve); the
longitudinal 4x4 block is now solved by Cramer's rule, which is exact because the transverse P rows decouple.

MUTATE (AC11_MUTATE=1, gamma -> -gamma, ac11_MUTATE.*): Omega'^2 < 0 on every cell. The control bites.

## Still open

The nonlinear moving solution: the Sun's co-moving charged halo (q_sun >> rho0 inside about 10^3 AU) matched to the
Galactic khronon flow, downstream regularity, and the metric response that would give alpha_1 and alpha_2. The
same calculation is open for v3s in AZ37.
