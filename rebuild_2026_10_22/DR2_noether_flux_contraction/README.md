# DR2_noether_flux_contraction: ARGUMENT FAILS. Charge conservation is a premise of Blumenthal, not an obstacle to it

Criteria: `FROZEN_CRITERIA.md` (6c46933963). Script `dr2.py`, output `dr2.out`, `dr2_results.json`; `dr2_MUTATE.out`. No profile was graded, as frozen. kappa = 1/2 FITTED, unused. Cold dark energy is a gravitating field component, no particle. Not theory closed. Nothing here says the data favour the framework. Newtonian toys, one mass, no feedback.

**Claim tested** (outside text, not adopted): static spherical div J = 0 gives 4 pi r^2 J^r = Q0 fixed at turnaround, so central condensation of baryons forbids Blumenthal pile-up while w ~ 0 clustering stays intact. Record check: no lane had tested it. X6 X-D1/X-D2, X14 and the mu-pincer (X17) already held the ingredients.

## Derivation
L = P(X), X = -(1/2) g^{mn} d_m phi d_n phi, Q = sqrt(2X), matter coupled to g alone. Metric: ds^2 = -e^{2A(t,r)} dt^2 + e^{2B(t,r)} dr^2 + r^2 dOmega^2.

1. **Current.** J^m = -P_X g^{mn} d_n phi, n = P_X Q, u_m = -d_m phi/Q. The equation of motion is d_t(sqrt(-g) J^t) + d_r(sqrt(-g) J^r) = 0. That is continuity: 4 pi r^2 J^r(r,t) = -d_t N(<r,t), weak field. It isn't a statement that the flux is constant, unless the system is already static, which is what the claim wanted to conclude. (S1)
2. **Static.** sqrt(-g) J^r = C. The flux through a small sphere is C for every radius, and the integral of div J over a ball is 4 pi C. Finite J^r at a regular centre forces **C = 0**, then P_X chi' = 0. Nothing is "fixed at turnaround"; the static flux is zero. C != 0 needs a source at r = 0. (S2)
3. **J^0 is not constrained by charge.** Exponentials with scales a and a/3 have the same charge and C = 0, central density ratio 27. The homologous n = F(r/s(t))/s^3, v = s' r/s solves continuity exactly for any s(t): any compression, charge exact. (S5) Blumenthal's own premise is M_i(<r_i) = M_f(<r_f): shell charge conserved, plus r M(r) invariant. Conservation is what lets the pile-up be computed.
4. **Trajectories.** Exact in the general metric, symbolic residual 0: **u^n nabla_n u_m = -h_m^n d_n ln Q**. (S3) For K = mu^2 (Q-1)^2: n = 2 mu^2 (Q-1), so at fixed n and mu -> infinity, grad ln Q -> 0: geodesics, with no pressure term to hold anything. c_s^2 = (Q-1)/Q, w = (Q-1)/(Q+1). (S3b) This is the record's X-D1/X-D2 in the scalar's terms.
5. **A static dust does not exist.** A static fluid has phi = Q0 t, Q = Q0 e^{-Phi}, so grad ln Q = -grad Phi, order the gravity itself. That needs Q - 1 ~ |Phi|, not Q -> 1. And w ~ 1e-7 there, so **"w ~ 0" doesn't separate dust from a held fluid**: the claim's two limbs use two different states. The static fluid isn't the clustering dust; the dust isn't static.
6. **AeST.** On C1's static Lagrangian (from the literature, per C1, not verified on disk), the chi flux with C = 0 is Psi' = (1 + J') chi': the algebraic law relation, and it has no rho in it. J^0 = 2 K_2 (chi_t - Q0 Psi), so static J^0 is set locally by the well: deeper well, more charge. AeST's Q0 is dphi/dt, not a flux constant. (S6) Baryons don't enter div J = 0, since they couple to g only. A term sourcing J from baryons would be a new coupling, with a new number or a broken shift symmetry, and the claim doesn't have one.

## Numbers (toy: NFW 1e12, R200 200 kpc, c 10; LC1's M_d 6.72e10, R_d 3.565 kpc; softening 1 kpc)

| r/R_d | 1 | 2 | 3 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|
| N2 Q, circular shells, charge exact | 2.537 | 2.011 | 1.689 | 1.494 | 1.299 | 1.200 | 1.145 |
| Blumenthal | 2.719 | 2.045 | 1.696 | 1.501 | 1.300 | 1.202 | 1.145 |
| N2b response, L = 0.1 L_circ, over same-time control | 1.391 | 1.184 | 1.059 | 1.024 | 1.011 | 1.003 | 0.997 |
| N3 Q, static fluid (Blumenthal on that flat start: 210 to 4.5) | 12.65 | 10.99 | 9.61 | 8.54 | 7.02 | 6.00 | 5.26 |

- **N2, the label's test:** mean (Q-1)/(Q_B-1) at 2, 3, 4 R_d = **0.981** (line 0.8), charge drift 0. With softening 0: 0.997. LC1's live f_Q is 0.872.
- **Flux:** peak about -1.8e9 Msun/Gyr at 2 R_d and -2.7e9 at 4 R_d at mid-growth, about 0 before and after. Not fixed in time, not uniform in r. Identity with -dN/dt good to 5e-4 of peak.
- **N1:** pressureless single-stream field equals geodesic shells, dv/v 3.7e-4, dn/n 4.6e-5 before the caustic. First caustic 23 Myr for a stream started at rest at 2-60 kpc in the fixed well (X14's result: generic).

## Real differences from a collisionless N-body run (none of them is the claim)
- **No angular momentum and caustics.** A single-valued scalar flow is irrotational, so it has no Blumenthal circular orbits and folds early. Past the caustic it needs a completion. Near-radial shells (N2b, one run, not in a label, control still phase-mixing) still pile up: above Blumenthal at 1-2 R_d, weaker at 3-4 R_d (1.06 and 1.02 against 1.10 and 1.08). That reduced response at 3-4 R_d comes from orbit shape. No graded profile has been run with it.
- **Finite sound speed (N3).** Central density rises × 13.7, so nothing is forbidden; Q stays far below Blumenthal at small r because the fluid starts with a core. It costs a new scale (k here set by R = R200, demonstration only). c_s runs from 147 to 543 km/s, the record's mu-pincer territory ("pressure cannot keep the cold mass out of galaxies"), and v_c at 6 R_d is 28 km/s before baryons. This is pressure, not charge, and the record has already closed it for density-keyed pressure.
- **C != 0 steelman (N4).** A true sign exists: at fixed C and r, n = C/(4 pi r^2 v), so a deeper well raises v and lowers n (× 0.897 at 8 kpc). It needs a sink. Holding a flat 220 km/s curve this way takes 6.4e12 Msun/Gyr, 64 × M200 into the sink in 10 Gyr, and r < 8 kpc drains in 14 Myr. With Mdot = M200/10 Gyr, density at 8 kpc is 1.6 % of the need. Point mass: rho ~ r^-3/2, a cusp.

## Labels (frozen)
F1 true, F2 true, F3 true, F4 true: **ARGUMENT FAILS.** No amendment, nothing graded.

## Checks: 12/12
K1 own Blumenthal vs X39 contract, max |d| 6.8e-7. K2 M_d 0 stays at Q 1, 7e-16. K3 charge 0. K4 flux residual 5e-4. S1-S6 sympy, residuals 0. N1 as above. MUTATE: sign flip in S3's connection fails S3; a 1e-3 per step leak fails K3 and K4 (`dr2_MUTATE.out`, 7/10, exit 1).

Disclosed: the first run failed K2, K4 and S6, all script faults, and N3 stopped on a bracket: L wasn't set for the softened circular orbit, the flux identity had the wrong sign, sympy's substitution of J'(y) failed, and the bracket was too narrow for a well deeper than the fluid's. They were fixed before any verdict; N2's ratio went 0.966 to 0.981. N1 runs in a fixed potential with final baryons, a detail the criteria left open. N3's Blumenthal comparison is for a flat start, so it isn't comparable to the row above in size. Not blind.
