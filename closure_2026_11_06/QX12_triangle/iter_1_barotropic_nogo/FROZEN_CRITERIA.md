# QX12 iter_1 frozen criteria: universal-density no-go for barotropic sectors

Frozen before any script. Kappa = 1/2 FITTED; not theory closed.

## Theorem (analytic, Lean core)

Assume a barotropic sector, p_X = p_X(rho_X, t) with dp/drho > 0, in hydrostatic equilibrium in a static total
potential Phi(r) and in contact with the cosmic sea (density rho_sea(t)) at the system's boundary r_b. Then
h(rho_X(r)) - h(rho_sea) = Phi(r_b) - Phi(r) = D(r) (the depth). Here h is the enthalpy, h' = p'/rho > 0, so h is
strictly increasing. Hence:

1. rho_X(r) = H_t(D(r)) is the same nondecreasing function of depth D for every system at the same epoch t.
2. Inside one system D decreases outward (g > 0), so rho_X(r) is nonincreasing in r. Therefore rho_X(r) <=
   3 M_X(<r) / (4 pi r^3) (local <= enclosed mean), and for r1 < r2,
   rho_X(r1) >= [M_X(<r2) - M_X(<r1)] / [(4 pi/3)(r2^3 - r1^3)] (local >= shell mean outside).

**No-go:** an "allowed" point A (galaxy) with upper bound rho_X(A) <= u_A and a "required" point B (group/cluster)
with lower bound rho_X(B) >= l_B, at depths D_A >= D_B and with l_B > u_A, contradict item 1. If such a pair exists,
no barotropic sector in equilibrium can satisfy T2 and T3 together.

## Data bounds (both footings, never pooled)

- u_A: KiDS isolated-galaxy RAR points (QX5's LE: 4 mass bins, point-mass baryons) and the Humphrey ellipticals at
  2, 4, 8 Re. u_A = 3 M_X,max(<r)/(4 pi r^3), with M_X,max from T2 (KiDS g_obs + 2 sigma; ellipticals g_tot 10^0.15).
- l_B: X-COP consecutive radius pairs (0.1-0.7 R500) and the Lovisari shell [R2500, R500]. The lower bound uses
  M_X,min(r2) from M_obs - 2 eM and M_X,max(r1) from M_obs + 2 eM (independent errors, conservative). Groups use
  both stellar allowances (f_st 0 and 1) and the label takes the weaker. Only l_B > 0 enters.
- Depth, conservative in the no-go's direction (galaxy depth LOW, group/cluster depth HIGH):
  - D_A,low: the integral of max(g_obs - 2 sigma, 0) over the galaxy's own data from r to min(r_last, r_ta), no tail.
    Ellipticals: the integral of g_tot(r) from r to 8 Re only.
  - D_B,high: the integral of G (M_obs + 2 eM)/r^2 over the data from r to the last point, plus a law tail with
    point mass M_obs,last + 2 eM from the last point to r_ta.
  - r_ta = (M_b,tot (1 + R) / ((4 pi/3) 5.55 rho_m0))^(1/3), QX10's turnaround rule. For the tail, M_b,tot is
    replaced by M_obs,last / (1 + R) if that is larger.
- Epoch: KiDS lenses sit at z ~ 0.2-0.3, everything else at z < 0.1. The primary label assumes H_t is constant over
  0 < z < 0.3, and that assumption is frozen here. A same-epoch subset (ellipticals vs groups/X-COP only) is reported
  separately, with its own label.

## Labels

- DEAD (barotropic class): at least one violating pair (D_A,low >= D_B,high and l_B > u_A) on both footings in the
  primary set.
- DEAD (same-epoch): the same, using ellipticals as the only allowed points.
- ALIVE: no violating pair on at least one footing. Then the triangle does not exclude the class by this test.
Report the number of violating pairs and the largest l_B / u_A among them.

## Known answers

- KA1: the inverse is exact. glaw(inv(g)) = g to 1e-12 on a grid (and Lean).
- KA2: zero sector. With M_obs = M_law(M_b), the computed M_X is 0 to 1e-9 relative (X-COP rows).
- KA3: reproduce QX2/QX5's plain-law X-COP mean (+0.4675 canonical / +0.4345 alt) from the loaded tables.

## MUTATE (separate outputs)

- M1 (power): plant a barotropic sector that does satisfy item 1 (rho_X = rho_0 (D/D_0)^2 for all systems, with
  rho_0 set so that KiDS is unchanged) by replacing the groups' and X-COP's M_obs with the planted sector's
  prediction. Then the no-go must find 0 violations. If it still finds violations, the test has no specificity and
  the label is NO VERDICT.
- M2 (sensitivity): multiply the KiDS and elliptical allowed bounds by 1e3. The violation count must drop, which
  shows that the label responds to the galaxy side.
