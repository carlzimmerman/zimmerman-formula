# FA1 / I6 FROZEN CRITERIA: the Galileon-determinant selector, with a field solve

Committed alone, before any script or number for this lane. Owner, in chat, 11-04: "Yes, run both".

**Not blind.** I have read FA1 (I1 killed at gate 1: X-COP zeta_c 0.426; SPARC f_SP 0.425 at Y 0.5), M1_trilemma's
galileon row (cubic and quartic galileons of the AeST scalar for the planets; L5 drops out of the spherical law),
and K1. By hand, before any run: in the deep Vainshtein regime of a cubic galileon, a sphere has
pi' ~ sqrt(M(r)/r), so the Hessian's eigenvalues are y (n, 1, 1) with n = (dlnM/dlnr - 1)/2, and the normalized
determinant is a monotone function of FA1's zeta on the range that matters. So I expect the spherical-equivalent
reading to fail SPARC the way I1 did, and the open question is whether a disc's flat geometry changes that.
kappa = 1/2 FITTED. Footings (canonical 9.3603e-11, alt 1.1312e-10 m s^-2) never pooled. Adopts nothing. The cold
sector stays retired; this lane grades where a selector lets a dust part weigh.

## The action (what Phase 1 wrote, made definite)
Phase 1: "the dust part is switched by the cubic invariant det(d_i d_j pi) of a Galileon-type field ... quintic
Galileon ... with the dust-energy term multiplied by a function of that invariant."
- The quintic term's field equation is proportional to the 4D determinant of d_mu d_nu pi, which vanishes for any
  static field (the time row is zero). The quartic's static equation is det(d_i d_j pi), but with L4 or L5 on a
  cosmological background c_T != c at O(1) (GW170817). So the field's dynamics is taken as L2 + L3 (cubic
  galileon), and det enters only through the selector. This is the reading graded; it is my choice, disclosed.
- S = S_v3s + int sqrt(-g) [ -(1/2)(d pi)^2 - (r_c^2/(3 c^2)) (d pi)^2 box pi + (pi / 2) (8 pi G / c^4) T
  - (1/2) M^2 F(s) (u.d chi - Q0)^2 ], with u the khronon (v3s) frame and
  s = 3 sqrt(3) det(H) / |H|^3, H = the spatial (u-orthogonal) Hessian of pi, |H|^2 = tr H^2.
  s = 1 for an isotropic positive Hessian (FRW, a cored centre), 0 for planar or filamentary, -0.770 around a point
  mass in the deep regime. F non-decreasing, F = 0 at s <= s_Saturn; no form assumed beyond that.
- Static weak-field limit: lap(pi) + (r_c^2/(3 c^2)) [(lap pi)^2 - pi_ij pi_ij] = 8 pi G rho, so pi = 2 Phi_N when
  linear. r_c = c^2/a0 per footing (the framework's own length; about 31 Gpc canonical). Then the Vainshtein radius
  is about 1 Mpc for a MW-mass galaxy and about 30 Mpc for a cluster: every system graded here is deep nonlinear,
  and the solution there does not depend on r_c, so the footing enters through r_c only at the 1e-8 level and
  through the g_b < a0 selection of SPARC points.

## Dust amount when on: as FA1, D = 1.5 x the law's mass (+0.40 dex in g at full weight).

## Gates
- **s_c** = 5th percentile of s over FA1's 35 X-COP rows (7 clusters, 0.1-0.7 R500), spherical solve with the full
  quadratic (r_c per footing), M_b = M_gas + M_star as fa1_zeta.py reads it, slope by the same central log
  difference at r x 1.1^{+-1}.
- **G6-SPH (reported, graded as a reading).** FA1's reading A carried to s: SPARC M_b = r V_b^2 / G
  (V_b^2 = Vgas|Vgas| + Y Vdisk^2 + 1.4 Y Vbul^2), the same spherical solve, f_SP = fraction of g_b < a0 points with
  s >= s_c, Y 0.5, 0.3, 0.7. SEPARATES if f_SP <= 0.046 at all three Y; DOES NOT SEPARATE if > 0.046 at all three.
- **G6-DISC (primary).** Axisymmetric (R, z) solve of the static equation for six SPARC galaxies chosen before any
  run to span gas-rich to massive: DDO154, NGC3741, IC2574, NGC2403, NGC3198, UGC00128. Sources from SPARC Table 1:
  stars an exponential disc of mass 0.5 L[3.6], scale R_d, sech^2 thickness z0 = 0.15 R_d; gas 1.33 M_HI, exponential
  with scale R_g fixed by Sigma_HI(R_HI) = 1 Msun/pc^2 (taking the larger root), sech^2 thickness 0.1 R_g. Bulges
  none (these six have no bulge column). At each SPARC data radius R with g_b < a0 (rotmod, Y 0.5, per footing):
  W(r) = solid-angle fraction of the sphere of radius r with s >= s_c; W_enc(R) = (1/R) int_0^R W dr (dust density
  ~ r^-2, frozen); delta = log10(1 + D W_enc). A model reads ON if the rms of delta over its g_b < a0 radii exceeds
  sqrt(0.110^2 - 0.069^2) = 0.0857 dex (SPARC's whole rms room), else OFF.
  SWITCHES OFF if 0 of 6 read ON; DOES NOT SWITCH OFF if 1 or more of 6 read ON (1/6 > 0.046). Per footing.
  Reported: midplane s(R, 0) and W at the same radii.
- **G6-CL.** The same axisymmetric solver on a spherical X-COP-like source (beta model, r_core = 0.15 R500, beta
  0.7, R500 = 1.3 Mpc, gas mass 1e14 Msun inside R500, plus a central BCG Hernquist 1e12 Msun, a = 30 kpc): ON if
  s >= s_c on 0.1-0.7 R500 at all three polar angles sampled. Also reported: fraction of X-COP rows with s > 0.
- **G6-Q2 (order of magnitude).** (a) s at Saturn's orbit (Sun as a point mass, deep regime, local disc density
  0.1 Msun/pc^3 added to the source) must be < s_c: dust off. (b) pi's own force at Saturn against the planetary
  bound used by the record (Saturn 7e-15 m/s^2), and pi's anomalous tidal term from the MW's pi Hessian against
  Hees's 2-sigma line 9e-27 s^-2 (the record's line). PASS if (a) holds and both (b) ratios are below 0.1.
- **G6-GW (order of magnitude, reported with a label).** L2 + L3 leave c_T = c. The selector term shifts the
  tensor kinetic coefficient on FRW by O(Omega_d F'(1)), since s is extremal at the isotropic point and a tensor
  mode perturbs H at first order. GW170817: -3e-15 < dc/c < +7e-16 (Abbott et al. 2017, ApJL 848, L13; recalled,
  PROVISIONAL). PASS (CONDITIONAL) if the bound can hold with an F flat near s = 1; FAIL if no F can.
- **Action status (reported).** F depends on second derivatives of pi, so where F' != 0 on the dust's support the pi
  equation is fourth order (Ostrogradsky). Written as: action writable; healthy only for F flat on the dust's
  support. If the solve or the action cannot be made definite, the label is UNDECIDED (no action).
- **G6-BUL: NOT COMPUTED** (needs a 3D nonlinear solve; superposition fails in the deep regime).
  **Keys: NOT COMPUTED** (as FA1).

## Labels for the lane
- **I6 KILLED AT THE SPARC NULL** if G6-DISC reads DOES NOT SWITCH OFF on both footings and all checks pass.
- **I6 ALIVE AT GATE 1** if G6-DISC SWITCHES OFF on both footings, G6-CL is ON and G6-Q2 passes, all checks
  passing. Alive means only that a necessary condition holds.
- FOOTING-SPLIT or UNDECIDED otherwise; UNDECIDED (no action) as above.

## Checks (a failed check means no clean label)
- **K0:** F = 0 reproduces the law to 1e-12 (as FA1).
- **K1:** analytic: a uniform sphere gives s = 1; the deep point mass gives s = -3 sqrt(3)/(2 (9/4)^1.5) to 1e-9; the
  spherical full-quadratic pi' matches a direct ODE integration of the static equation to 1e-6.
- **K2:** the axisymmetric solver on a spherical Plummer source reproduces the spherical s(r) within 0.02 at
  r = 0.3-5 a and three polar angles, at the finest grid.
- **Ladder:** grids N = 48, 96, 192 per model; W_enc at the data radii changes by <= 0.03 between 96 and 192 and
  every ON/OFF reading is the same at 96 and 192. Box size x2 and the numerical regulator x10 (the solve uses a
  regulator in place of the physical, far smaller linear term) each change W_enc by <= 0.03.
- **MUTATE (must bite):** s -> -s. G6-DISC must read DOES NOT SWITCH OFF and G6-SPH's f_SP must change.
  Separate `_MUTATE` outputs.
- **Rerun:** the result JSON from two runs must be byte-identical.

Compute: one thread, nice 19, < 1 GB, minutes. No downloads. Literature values marked PROVISIONAL are recalled,
not fetched.
kappa = 1/2 FITTED; not theory closed.
