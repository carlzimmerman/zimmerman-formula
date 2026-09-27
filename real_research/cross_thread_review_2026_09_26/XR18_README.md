# XR18 -- is the chain's best cell well posed? H_S (FP13) first, H_Y (FP9) second

Review lane of `cross_thread_review_2026_09_26`, 2026-09-27.  An adversarial well-posedness and stability audit, before any
particle-mesh (PM) confirmation, of the derivation chain's separator cells on FP7's AQUAL-type root:

* **H_S** -- FP13's state separator (`derivation_chain_2026/FP13_separator_from_state.py`, 27faacc84), the chain's current
  candidate.  Audited first, after the 2026-09-27 scope update.
* **H_Y** -- FP9's separator (`derivation_chain_2026/FP9_web_galaxy_separator.py`, b510eebfe), the lane's original target,
  superseded by FP13 (FP13 reports H_Y failing KiDS at z = 0.4, +20.6).  Questions (a)-(e) as first assigned.

Five scripts.  Each carries a pre-declared hypothesis block written before its first full run, controls that reproduce
committed numbers exactly, and a MUTATE run that must fail.  Both a0 footings throughout (canonical 9.3603e-11, alt
1.1312e-10 m/s^2).  kappa = 1/2 is fitted (Z = 5.7888); nothing here derives it, and nothing here closes the theory.
Causality is judged by the record's criterion B (FRIED_CHICKEN_SPEC requirement 7 as amended 2026-09-26), used as written.

## Bottom line

**H_S: a particle-mesh run should not proceed as H_S is formulated.**  Varying H_S's action through its state functionals
B[state] and y_th[state] produces O(1) local mean-field terms that FP13's scoring leaves out.  FP13 A1's finding that the
leaf average's derivative is O(1/V) is right, but the action depends on B through an integral over the whole leaf,
dS/dB = O(V), so the variation through B is O(V) x O(1/V) = O(1): a local force with a leaf-averaged coefficient (N1).  On
FP13's own headline state that coefficient, R_B, reaches 6.9-7.5 (canonical) and 7.6-8.1 (alt) at z <= 0.635, so the
linearised psi-constraint's symbol k^2 (1 - R_B) passes through zero and changes sign on k = 0.12-1.62 h/Mpc.  The constraint
is singular there and the linear problem is ill posed (N3; the formula is confirmed independently on a 32^3 lattice to 7.8%,
N3b).  Treating B instead as a prescription that is not varied gives field equations that are not an action's, and the
energy (Bianchi) identity then fails at a rate set by the same leaf integral.  The y-term screens sub-L Newtonian gravity
at z > 0.635 by 1/(1 + kappa); kappa = 1.9-2.7 in FP13's Gaussian reading of the web, where the 1e11 flagship at z = 2.5
moves by -0.10 dex, and about 3e-3 in a halo reading (N4).  The q = 0 ramp itself is well posed, lambda > 0 does its job, and the yield structure
H_S shares with H_Y is healthy.

**H_Y: no linear well-posedness obstruction found.  A PM run could proceed on these grounds, with three caveats, but H_Y is
superseded.**  Criterion B's causal part holds at every background point tested (0 violations in 649,056 root
evaluations).  The yield surface is a degenerate, weakly hyperbolic locus.  Its linearised Cauchy problem is well posed in
the energy norm but not in C^1.  DE12's k^0 mechanism is absent.  The two-depth band-pass adds no mode.  The <K>_h global
terms are (v/c)^2-suppressed (at most 1.6e-5 of rho_bar).  On FRW the crossing of the yield is continuous (a square-root
kink, not a jump).  The caveats a PM run must handle:

1. Cold (pressureless) matter at a yield surface grows faster the finer it is resolved, Gamma ~ d_min^(-1/4).  It reaches
   20-44 H at 1 kpc and 204-451 H at the xi floor (0.024 pc).
2. There is a thin non-adiabatic layer where phi cannot follow the baryons quasi-statically: at most 9.7 kpc at z = 0.25.
3. Finite-amplitude phi waves steepen at the surface.  The nonlinear free-boundary Cauchy problem is open.

## H_S -- FP13's state separator

H_S (per 1/16 pi G, c = 1): chi = (S_xi - S_B) phi, with B = L^2/2 fixed by <(S_B delta_m)^2>_h = delta_c^2 (delta_c = 1.686);
delta_m = D_i(a^i - D^i chi)/(<K>_h^2/6 - Lambda/2); J_Y = J_P2 + 2 y_th sqrt(Y) with
y_th = c_y <|g_bp|^2>_h^(1/2)/a0 x max(0, 2q), 2q = 1 + Omega_r - 9 Lambda/<K>_h^2, c_y = 1.  The yield switches off at q = 0
(z = 0.635), and FP7's lambda > 0 is required.  Script: `XR18_state_separator.py`.

### The terms the variation produces (derived in the script's docstring, weak field)

In the weak field delta_m = lap psi/(4 pi G rho_bar), with psi = Phi - chi the chassis's Newtonian combination.

* **B-term.**  d^2 S = E_B Int (S_B d delta_m)^2 d^3x, with E_B = <dL/dB>/(2 <|grad S_B delta_m|^2>) > 0.  In the psi-equation:
  psi_k = -4 pi G rho_k/(k^2 (1 - R_B)), where
  R_B(k) = [Int Delta^2 h C^Q e^(-B k'^2) dln k' / Int k'^2 Delta^2 e^(-2B k'^2) dln k'] k^2 e^(-2B k^2).
  This enhances Newtonian gravity at k ~ 1/L and is singular at R_B = 1.  In words: added variance raises B, which lets more of
  the web's MOND potential into chi, which binds all matter deeper.  Its size is the web's MOND response at scale L,
  C^Q ~ 1/sqrt(y_rms) ~ 10.
* **Y-term.**  d^2 S = -(a0 <x> c_y 2q/(8 pi G g_rms)) Int |d g_bp|^2 d^3x.  In the psi-equation:
  psi_k = -4 pi G rho_k/(k^2 (1 + kappa h^2 - R_B)), with kappa = c_y 2q <x>/y_rms.  This screens sub-L Newtonian gravity while
  the ramp is on (z > 0.635).  The MOND scalar's own source is not screened.

### 1. Nonlocality, conservation, dependence on the whole leaf

* **The local term exists (N1, PASS).**  On periodic leaves of fixed cell size (N = 8, 16, 32), N^3 |dB/d delta| = 0.200 at
  every N, which reproduces FP13 A1's O(1/V).  But the action's gradient per cell, rms dS/d delta = 1.9986, is the same at
  every N and matches the derived 2 E_B (S_B^2 delta)(x) to <= 9.9e-7.
* **Which field equations.**  B and y_th read psi = Phi - chi, and chi = (S_xi - S_B) phi.  So the mean-field terms enter every
  equation that contains psi: the lapse's and phi's.  The khronon's equation receives the <K>_h terms: the ramp, and the
  denominator of delta_m.  Those reach the Newtonian equations only through the khronon, at O(v^2/c^2).  That is the argument
  of XR18_nonlocal_dof C1, which sized it for H_Y; it was not recomputed for H_S.
* **Conservation.**  If B and y_th are varied, the action stays diffeomorphism invariant, because the leaf averages are
  covariant functionals of (g, tau).  The Noether identity then gives matter conservation on shell, global terms included.
  The translation part is checked on leaves (N2, PASS): the net mean-field force is 6.3e-17 of the sum of its magnitudes.  The
  MUTATE run's position-weighted window breaks it (2.2e-3).  If B is not varied, the equations are not an action's
  Euler-Lagrange equations.  The Newtonian limit then keeps total momentum, because the smoothing kernel stays translation
  invariant, but it loses energy conservation at the rate (dS/dB)(dB/dt).  That rate is set by the same leaf integral dS/dB
  that produces the mean-field term.  This last statement is structural and was not separately computed.
* **Dependence on distant structure.**  R_B(k) and kappa are leaf averages: of the power spectrum times the MOND response, and
  of the one-point distribution of |g_bp|.  They are intensive, O(1) coefficients.  One distant structure changes them by its
  share of those leaf integrals.  Contrast H_Y, whose only global channel, <K>_h, is weighted by (v/c)^2.
* **max(0, 2q) (R2, reported).**  The ramp is Lipschitz in <K>_h, so the action is well defined.  Its <K>-derivative jumps at
  q = 0 by the finite amount 2/(3 sqrt(Lambda)).  That is a coefficient jump in the (v/c)^2-suppressed khronon channel, with no
  delta-function force.

### 2. Can an action read the matter density?

* **No new mode.**  delta_m reads D_i a^i with a_i = D_i ln N, which contains spatial derivatives only.  The lapse stays
  non-dynamical: no Ostrogradsky mode and no new velocity (R1).
* **The constraint changes.**  The psi-constraint's symbol becomes k^2 (1 + kappa h^2 - R_B).  Wherever it vanishes, the
  lapse's second-class pair degenerates: the Hamiltonian form of the singular constraint, so the Dirac count is not constant
  on FP13's state.  This follows structurally from the symbol; it was not separately computed.
* **DE12's UV mechanism is absent.**  The read is smoothed by S_B, so its k^0-type second variation carries e^(-2Bk^2).  At
  k = 1/kpc it underflows to 0 against 1e6 K gas pressure.  The leaf average evades DE12's UV growth, but not its sign: the
  same kind of destabilising term appears at k ~ 1/L, multiplied by the web's MOND response.
* **N3b (added after the first run found R_B ~ 8; pre-declared before its own run).**  The exact second derivative of the
  linearised reduced action on a 32^3 leaf, with B re-solved at every step, has a positive B-part.  It matches R_B(q) to 7.8%
  for q = 2 pi j/32, j = 1..6.  At q ~ 1/L the B-part is 3.07 times the Newtonian part.
* **N3 (pre-declared HS3, FAIL).**  Maximum R_B by epoch:

  | z | canonical (per-mode chord) | alt (per-mode chord) | R_B >= 1 on k (h/Mpc) |
  |---|---|---|---|
  | 0 | 7.47 | 8.13 | 0.12-1.03 |
  | 0.25 | 7.12 | 7.78 | 0.14-1.24 |
  | 0.5 | 7.10 | 7.80 | 0.17-1.48 |
  | 0.635 | 6.92 | 7.62 | 0.19-1.62 |
  | 0.8 | 2.60 | 2.87 | 0.39-1.62 |
  | 1-3 | 0 | 0 | none |

  The rms chord gives up to 9.8.  Above z ~ 1 the yield freezes phi on the linear modes, so R_B = 0.  The expectation written
  before the run was R_B ~ 0.5 at z = 0.25 (HS3 was marked uncertain); the measured value is about 7.  sigma_8 with the B-term
  in the growth yardstick is not meaningful where R_B >= 1: the floored yardstick returns 127-749.
* **N4 (pre-declared HS4, PASS).**  kappa at z = 1-3 is 1.94-2.67 in the Gaussian (Maxwell |g|) reading, which FP13's
  per-mode yardstick implies.  The 1e11 flagship then moves by -0.101 to -0.105 dex.  In a halo reading (Press-Schechter halos,
  FP9's yield-law bubbles) kappa is 2.6e-3 to 3.3e-3 and the shift is -4e-4 dex.  Which reading holds is a property of H_S's
  own nonlinear web, and only a run that carries the y-term can decide it.

### 3. The q = 0 ramp and the role of lambda > 0

* **Q1 (pre-declared HS5, PASS in the final runs).**  With the ramp smoothed (softplus width eps), sigma_8 converges
  monotonically: |d sigma_8| = 7.0e-4 / 2.5e-5 / 1.1e-7 at eps = 0.05 / 0.01 / 0.002.  Every sigma_8 mode crosses the yield at
  most once.  Their first above-yield epochs lie at z = 0.619-0.876.  Through z_q0 the chord's largest epoch step shrinks x9.9
  under 10x refinement, so it is smooth.  FP13's y_th(a) is a linearly interpolated table whose zero sits about 0.010 below
  z_q0 (y_th = 9.8e-5 at z_q0).  That is harmless for sigma_8, but a PM run that implements the ramp analytically will switch
  off at z = 0.635 rather than about 0.624.  Also because of the table, FP13's "step" variant is itself a linear ramp across one table cell: its step
  shrinks x2.6, which is a sqrt onset, not a jump.  The first recorded main run reported Q1 as FAIL; that failure was an
  artefact, explained under "Development record".
* **Q2 (pre-declared HS6, PASS).**  On exact FRW with the band-pass closed, FP7's determinant is proportional to lambda, so at
  lambda = 0 phi has no equation (K2 reproduces FP13 A1).  With structure, phi un-freezes at omega_r = c k sqrt(C_L/lambda_eff).
  For c_2 = 7.29e-3 the slowest sub-L sigma_8 mode gives omega_r = 127 / 127 / 79 / 10 H at lambda = 0 / 1 / 100 / 1e4.  For
  c_2 -> oo it gives 1220 / 781 / 100 / 10 H.  lambda > 0 keeps phi determined where the yield vanishes, and the quasi-static
  yardstick holds through z = 0.635 unless lambda >~ 1e4.

### Shared yield structure at H_S's surfaces (Y1, PASS)

At H_S's z >= 1 yield surfaces on DE12's hosts, every root of the exact block is real and >= 0: 0 violations in 138,240
evaluations.  The exponents are C_L ~ d^(0.5000-0.5001) over 18 surfaces.  Below z = 0.635 there is no yield, and the zeros of
the band-passed field carry the plain-P2 y^(-1/2) susceptibility.  Parts (a), (b) and (d) below therefore carry over to H_S's
yield surfaces.

### What would repair H_S (directions only, not tested here)

* **Make the depth stationary.**  Fix B by dS/dB = 0 instead of the variance condition.  The first-order mean-field term
  then vanishes identically, and what remains is O(1/V) per mode.  This is a different L(z) law and would need FP13's gates
  re-run.
* **Read the state only through (v/c)^2-suppressed quantities.**  <K>_h is the example (C1: <= 1.6e-5).  Newtonian-order reads
  (delta_m, g_bp) feed O(1) mean-field terms back.

Either way, re-run this script's N1-N4 on the new state before any PM run.

## H_Y -- FP9's separator: questions (a)-(e)

### (a) The yield surface: speeds, criterion B, the Cauchy problem -- `XR18_yield_surface.py`

* **Speeds.**
  * Principal part (k >> 1/xi): phi's own cone U = C(theta)/lambda, the BPS khronon U_K = c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)),
    and light.
  * Effective (h ~ 1): the coupled roots of FP7's block with sigma -> h.
  * At the surface: C_L ~ d^(1/2) (fitted 0.5000-0.5006) and C_T ~ d^(-1/2) (-0.5000 to -0.4997) on all 24 hosts.  So
    c_par -> 0 as d^(1/4): 37 km/s at d = 1e-6 r_Y for 1e10 at z = 0.25, about 930 km/s at z = 4.  And c_perp -> oo as
    d^(-1/4).
  * In the plug: phi is rigid (no phi characteristic), and the khronon sits at E = alpha_c.
* **Criterion B (A1, PASS).**  All roots are real and >= 0 at every background point: yielded side, approach to
  d/r_Y = 1e-12, plug, zero field.  This holds for every angle, alpha_c in {9.62e-14, 3.2e-9}, c_2 in {7.29e-3, 0.1},
  lambda in {0, 1, 100} and h in {0, 0.3, 1}: 0 violations in 649,056 evaluations.  The cones are centred on the khronon's
  normal, and the divergent speeds lie in the leaf, which criterion B allows.
* **A2 (FAIL, on its third clause only).**  The exponents hold.  The declared lambda = 0 limit does not: the transverse root
  there is U = U_K C_T alpha_c/(C_T alpha_c + (2 - alpha_c) h^2), approximately c_2 C_T/((2 + 3 c_2) h^2).  The closed form
  matches the block's root to 5.6e-16, and the fitted slope is -0.500, so the root diverges like the lambda > 0 speed.  It would
  reach U_K only at d/r_Y ~ 2e-25 to 1e-18, i.e. 3 cm to 1 km from the surface.  That is far inside the xi floor
  (7.5e14 m), below which the band-pass smooths phi.  At d = 1e-10 r_Y, U/U_K <= 1.1e-4.  The clause was mis-stated.  The
  lambda = 0 roots are all real and >= 0 (A1).
* **A3 (PASS).**  The linearised phi-sector across the surface, lambda u_tt = (C_L u_x)_x with a rigid plug, is a non-negative
  degenerate Sturm-Liouville problem:
  * minimum eigenvalue 0.750 > 0;
  * observed convergence order 0.510, as expected for the d^(1/2) eigenfunction;
  * the order-1/2 Richardson limit matches a shooting reference started on the exact local solution
    u ~ d^(1/4) J_(1/3)((4/3) kappa d^(3/4)) to 3.4e-5;
  * the eigenfunction's gradient diverges as d^(-0.500).

  On the 1e11 flagship's radial profile at z = 2.5, omega_1/H = 905, converging to 1.8e-3.  The problem is well posed in the
  energy norm but not in C^1, with no linear growth.
* **A4 (reported).**  A 1-D nonlinear slab under slow loading (eps-regularised yield, energy-conserving AVF steps): the surface
  advances into the plug, and the solution converges in N and eps (energy residual 1.3e-13).
* **A5 (reported).**
  * Characteristics reach the surface in finite time (~ d^(3/4)), and linear amplitudes focus mildly (~ d^(-1/8)).
  * F_P2'' > 0, so finite-amplitude phi waves steepen there and caustics are generic.  The action supplies no dissipation, so
    weak-solution uniqueness is open.
  * The layer where c_par < 300 km/s (phi lags a quasi-static solve) is at most 9.7 kpc at z = 0.25 (r_Y ~ 2-4 Mpc), about
    0.1 kpc at z = 1, and below 6.5e-5 kpc at z >= 2.5.

### (b) A DE12-type second variation of the full H_Y action -- `XR18_second_variation.py`

* **B1 (PASS): no k^0 term.**  Every term of the full action was counted by WKB order in sympy: EH, Lambda, alpha_c a^2,
  c_2 (K - <K>_h)^2, the band-passed chassis, J_Y with y_th(<K>_h), phi's inertia, the heat pair with L(<K>_h), and matter.  None
  has a k^0 part except the gas's own c_s^2/rho, and the phi-phi block has no mass term.  The same engine, given DE12's gate,
  returns DE12's S identically (K1).  DE12's obstruction needs a read of a second derivative of a constraint-slaved potential;
  H_Y reads first derivatives and leaf averages only.
* **B2 (PASS).**  In DE12's own convention (k = 1/kpc, 1e6 K gas, 1 kpc-20 Mpc) the growth is 0 on all 24 hosts.  DE12's gate
  gives 1.3e3-4.9e4 H there.
* **B3 (PASS).**  The exact radial (l = 0) sector around each yield surface, with gas at 1e6 K and 1e5 K:
  * growth at most 31.2 H;
  * converged: 0.0% under grid doubling, 1.2% under the regularised yield;
  * the yield raises it over plain band-passed P2 by at most x1.53.
* **B4 (FAIL as declared) and B4b (PASS).**  Cold matter at the surface feels the (y - y_th)^(-1/2) susceptibility.  The isolated
  surface mode grows as d_min^(-p) with p = 0.238-0.250.  It saturates at the xi filter (xi/3 vs xi/10 within 0.2%) at
  204-451 H.  B4's whole-domain fit mixed in an interior dense-gas mode at z >= 2.5, which pushed p down to 0.045, so B4b was
  added and pre-declared before its own run.  This is bounded by xi but resolution-dependent: a PM run of cold particles is
  capped only by its cell size.
* **B5 (reported).**  On DE12's own layers H_Y's exact radial growth is at most 2.93 H (median 0), against DE12's 2e4-5e4 H.
* **B6 (reported).**  The heat pair's metric coupling is 3.6e-47 of gas pressure at 1/kpc.

### (c) Nonlocality through <K>_h -- `XR18_nonlocal_dof.py`

* **C1 (PASS).**  H_Y's <K>_h global term is (v/c)^2-suppressed.  Its effective extra density in the psi-equation is at most
  1.6e-5 of rho_bar in the Gaussian reading and 3.7e-7 in the halo reading, at z = 0.25, 1 and 2.5, on both footings.
* **D2 (PASS).**  The correction to the scale factor's kinetic coefficient is at most 3.9e-6 of GR's, so the Legendre map
  stays invertible.
* **C2 (reported).**  The leaf average is a covariant functional of (g, tau), so conservation holds on shell with the global
  terms included.  One distant structure changes <K>_h by its share of the leaf's volume, weighted by (v/c)^2.

### (d) Degrees of freedom with two heat depths -- `XR18_nonlocal_dof.py` (FP5 confirmed)

* **D1 (PASS).**  Explicit two-segment heat chains (n1, n2) = (1,1), (1,2), (2,1), (2,2) on FP7's unitary-gauge block:
  * the heat block's determinant is nonzero and free of omega, C_phi, lambda, c_2 and alpha_c (second class);
  * its Schur complement is exactly FP9's block with h = sigma_b (1 - (1 + (B - b) k^2/n2)^(-n2));
  * the full scalar determinant has deg_omega = 4 at lambda > 0 and 2 at lambda = 0.

  So N = 2 tensor + 2 scalar (+1 at lambda = 0): the band-pass adds no mode.
* **D3 (reported).**  The Dirac count per point is 4 (2 tensor + khronon + phi) in both the unitary-gauge and the covariant
  conventions, independent of n1 and n2.  In a plug it is 3.
* **For H_S.**  The same count holds wherever the lapse's constraint symbol k^2 (1 + kappa h^2 - R_B) is nonzero (item 2 above).

### (e) FRW about the frozen phi, and the crossing of the yield -- `XR18_frw_yield_crossing.py`

* **E1 (PASS).**  With phi frozen, the scalar block's only root is the BPS khronon's U_K > 0, and the static response is
  Psi/Psi_N = 1/(1 - alpha_c/2) exactly.  FP7's marginal zero-field root omega^2 = 0 is gone.
* **E2 (FAIL, on its absolute threshold only).**  The measured behaviour at the crossing:
  * the chord C^Q = x/y switches on as (y - y_th)^(1/2), fitted 0.5000;
  * the tangent diverges as (y - y_th)^(-0.5000);
  * every sigma_8 and forest mode crosses the yield at most once;
  * the chord's step at a crossing shrinks x3.1-3.5 under 10x refinement (~ sqrt 10), as a continuous sqrt onset should.

  The declared continuity threshold, |jump| < 1e-5 at d <= 1.8e-13 y_th, does not scale with y_th.  At y_th = 1e-6 the chord
  there is 4.2e-4 = O(sqrt(d)/y_th), and it tends to 0 as sqrt(d).
* **E3 (FAIL, on its forest tolerance only).**  With the yield regularised, sigma_8 converges monotonically: |d sigma_8| =
  2.5e-4 / 2.7e-5 / 2.6e-6 at eps/sqrt(y_th) = 0.1 / 0.01 / 0.001.  Its sensitivity to the initial amplitude is unchanged
  (0.9896 vs 0.9894).  The forest proxy converges only linearly in eps (3.8e-2 / 3.7e-3 / 3.7e-4 against 2.8e-7), because the
  regularised plug leaks x ~ eps y/y_th below the yield.  The 1e-6 tolerance ignored that.
* **E4 (PASS).**  FP9's z ~ 2 lumps (0.1, 0.3 and 1 Mpc/h) cross once, and the chord's step shrinks x2.4-5.3 under
  refinement.  From z = 3 to 1.5, cold matter inside a lump gets 3.7-4.0 e-folds under H_Y's tangent response, against
  4.8-5.9 for plain P2 and 1.8 for Newton.  The largest excess over plain P2 is +0.16 (1e4 K gas at k = 10/R).
* **Result.**  No jump in G_eff and no instability at the crossing on the tested yardsticks.

## For any PM run of these cells

1. **H_S.**  Do not run it as formulated (above).
2. **Carry the global terms the variation produces**, or show that they are negligible.  For H_Y they are (C1); for H_S they
   are not (N3, N4).
3. **Cold matter at yield surfaces.**  Show convergence under refinement, or give the matter a physical width (pressure or
   dispersion).  Otherwise the surface growth is set by the cell size (B4b).
4. **phi's solver.**  The yield surface is degenerate and genuinely nonlinear (A3, A5).  A quasi-static solve lags in a layer
   of at most 10 kpc at z = 0.25.  Incoming finite-amplitude waves steepen, and the nonlinear Cauchy problem is open.
5. **Implement the ramp as FP13 scored it**, or note the 0.010 shift in z of the switch-off (Q1).

## Controls and MUTATE

| Script | Control | Reproduces | Result |
|---|---|---|---|
| XR18_state_separator | K1: FP13's machinery exec'd read-only | FP13's committed H_S headline: L(z), y_th(z), sigma_8 x4, forest x4, flagships x4, SPARC, KiDS at 0.25/0.4/0.7 (35 numbers) | max rel. dev. 0 |
| XR18_state_separator | K2: FP7's det M at sigma -> 0, C_phi = 0 | FP13 A1's determinant, proportional to lambda | exact (sympy) |
| XR18_yield_surface | K1: the lane's own unitary-gauge second variation | FP7's committed det M | exact |
| XR18_yield_surface | K2: C_T and C_L of J_Y | FP9 Y1's expressions | exact |
| XR18_second_variation | K1: DE12's gate through the lane's WKB engine | DE12's S identically; DE12's committed c_gate on all 24 layers | 4.4e-16 |
| XR18_second_variation | K1b: AQUAL/QUMOND amplification | d(y nu)/dy | 6.7e-16 |
| XR18_second_variation | K2: gradient of the reduced energy E[M] | FP9's spherical H_Y law | 7.5e-4 (FP6 grid), 5.8e-6 (20x) |
| XR18_second_variation | K3: radial operator | analytic Jeans rate | 3.9e-7 |
| XR18_frw_yield_crossing | K1: FP9's machinery exec'd read-only | FP9's committed headline (24 numbers) | max rel. dev. 0 |
| XR18_nonlocal_dof | K1: single-depth heat chain, Schur complement | FP7's committed det M with sigma -> sigma_n (n = 1, 2) | exact |

| Script | MUTATE (pre-declared) | Must fail | Outcome (final runs) |
|---|---|---|---|
| XR18_state_separator | leaf average replaced by a position-weighted window w = 1 + 0.5 cos(2 pi x/N) | N2 | N2 FAIL (net force 2.2e-3), rc = 1 |
| XR18_yield_surface | yield term's sign flipped (J_P2 - 2 y_th sqrt(Y)) | A1, A2 | A1 FAIL (4,320 of 865,536 root evaluations violate criterion B: the flipped yield gives C_T -> -oo, a Hadamard instability), A2 FAIL (no degenerate surface: fitted exponents 0); rc = 1 |
| XR18_second_variation | DE12's local density-read gate inserted | B1, B2, B3 | B1 FAIL (the k^0 term is DE12's S), B2 FAIL (Gamma(1/kpc) up to 4.87e4 H), B3 FAIL (628% grid change, Gamma up to 2.1e4 H); B4 fails as in the main run; rc = 1 |
| XR18_frw_yield_crossing | hard switch at the yield (MOND jumps fully on) | E2, E4 | E2 FAIL (jump 1.0e3, step shrink x1.00), E4 FAIL (x1.00-1.01), E3 FAIL too; rc = 1 |
| XR18_nonlocal_dof | second heat segment made dynamical (tau_h d_t W) | D1 | D1 FAIL (heat determinant omega-dependent; deg_omega 6/8), rc = 1 |

Main runs: `XR18_nonlocal_dof` rc = 0.  The other four have rc = 1, from the load-bearing failures listed above: H_S N3; H_Y
A2, B4, E2 and E3.  They are kept as run.

## Development record and disclosures

* **Exploratory runs made before the hypotheses were written** (scratch, not in the repository):
  * a map of r_Y and the local dx/dy on DE12's 24 hosts, which showed the divergent susceptibility and local pressureless
    rates of about 20-60 H at 1 kpc from r_Y (before (a) and (b));
  * a 1-D wave-packet prototype for (a), abandoned because its Newton iterations and energy balance failed at eps = 1e-6;
  * prototypes of A3's spectral test and A4's loading ramp.

  None for (c), (d), (e) or H_S beyond reading committed outputs.
* **Fixes after each script's first (MUTATE) run, before the recorded runs** (each listed in its docstring):
  * r_Y is located by brentq on the exact field: a grid locator's ~1e-7 relative error had flattened the d/r_Y = 1e-10 fits
    and blurred B4's saturation.
  * K2 of (b) uses the exact energy derivative: finite differences of the total energy were quadrature noise, up to 10%.
  * B4b was added; B4 is kept as declared.
  * H_S N1 tiles one base leaf: independent random leaves scattered the N^3 scaling from 0.31 to 0.68.
  * Q1, E2 and E4 test continuity by refinement.  A one-grid step comparison fails for any sqrt onset.
  * N3b was added after the first run found R_B ~ 8.
  * The DOF script's Schur comparison is made only when the heat block is omega-free.  Its first MUTATE attempt stalled in a
    symbolic Schur complement and was stopped.
* **Changes after the first recorded main runs.**  These were found while reviewing the outputs.  All five scripts were then
  re-run, MUTATE first and main last, one process at a time.  XR18_state_separator was re-run once more, MUTATE then main,
  after a last verdict-text edit that included the z = 0.635 epoch in the printed k-range.
  * *H_S Q1 artefact.*  The refinement test took its epochs from `growth_aq`'s output keys, which always include an appended
    z = 0.  The recorded "largest step" (18.15, not shrinking) was therefore the change between z = 0.615 and z = 0, not a
    step at the switch.  Restricting the epochs to the declared window gives shrink x9.9, and Q1 passes as declared.  The
    earlier FAIL was an artefact of the test, not a finding.
  * *H_Y A2.*  The check still fails as declared.  A reported block was added giving the lambda = 0 closed form, its slope and
    its saturation distance.
  * *D3 (reported).*  The first version kept tau in phase space and also treated the lapse pair as second class, mixing the
    covariant and unitary-gauge rules, and printed 5.  Both conventions are now counted consistently and give 4 (plug 3).  The
    load-bearing count is D1's determinant degree, which was right throughout.
  * *Verdict texts.*  Several claimed results the checks did not show.  For example, H_Y's verdict said the lambda = 0
    transverse speed "tends to the finite BPS khronon speed", and H_S's said "the q = 0 ramp is well posed" next to a FAIL.
    The "checks pass" counts skipped failed reported checks.  All five verdicts now print measured numbers, name the clause
    a FAIL rests on, and read correctly in the MUTATE outputs too.  Readings printed under a failed MUTATE check are labelled
    as written for the unmutated theory.
* **Expectations stated before the runs.**  H_S: HS3 (R_B < 1) was marked uncertain, with a rough estimate of R_B ~ 0.5 at
  z = 0.25; HS4 was uncertain in both parts.  H_Y: all hypotheses were expected to pass.  The failed pre-declared checks are
  kept as run: N3 (a physics finding), and A2, B4, E2 and E3 (mis-specified clauses; the reasons are given above).
* **Threads.**  The first recorded round ran two scripts at a time (up to 4 threads in total).  The final round ran one
  script at a time (at most 2 threads).  Each script takes under 3 minutes; the longest is XR18_yield_surface at about 140 s.

## Files (all in `real_research/cross_thread_review_2026_09_26/`)

| File | Content |
|---|---|
| `XR18_state_separator.py` (+ `.out`, `_results.json`, `_MUTATE.out`, `_results_MUTATE.json`) | H_S: items 1-3, the mean-field terms, the ramp, lambda, the shared yield structure |
| `XR18_yield_surface.py` (+ outputs) | H_Y (a): speeds, criterion B, the degenerate Cauchy problem, nonlinear slab, WKB |
| `XR18_second_variation.py` (+ outputs) | H_Y (b): WKB order count of the full action, exact radial sector on DE12's 24 hosts |
| `XR18_nonlocal_dof.py` (+ outputs) | H_Y (c) + (d): <K>_h channel sizes, two-depth heat chains, Dirac count |
| `XR18_frw_yield_crossing.py` (+ outputs) | H_Y (e): FRW about the frozen phi, the crossing of the yield, lumps |
| `XR18_README.md` | this file |

Run any script from the repository root, e.g. `python3 real_research/cross_thread_review_2026_09_26/XR18_state_separator.py`.
Set `MUTATE=1` for the control run; it writes `*_MUTATE.out` and `*_results_MUTATE.json` and never touches the main outputs.
