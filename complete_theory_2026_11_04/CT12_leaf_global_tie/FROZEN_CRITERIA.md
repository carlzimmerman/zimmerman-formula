# CT12: leaf-global, time-local tie (a0 set by the leaf average of rho_DE), FROZEN CRITERIA

Written before any CT12 script or number. Grading lane under owner decision D1 ("Yes, grade it", `../OWNER_DECISION_2026-11-04_D1.md`) and `../CT_GATES_COMMON.md`. A go to GRADE, not an adoption: nothing here is adopted, the cold sector retired on 2026-11-01 is not reinstated, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2, never pooled. Commit nothing (the parent commits). CT10 and CT11 run beside this lane; their folders are not read or touched.

## 0. Record check (grep, git log) before claiming anything new

- Spacetime-global (sequestering) constraints are on record, in the OTHER direction (Lambda fixed by an average of the MOND sector): K206 = `kappa_closure/k02_global_constraint_average.py` (misses rho_Lambda by five orders, `.out`:19-22), K279 four-form sequestering (boundary flux free), K303 Gauss-Bonnet sequestering (16 pi and 32 pi both valid) (`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_ATTEMPTS_LEDGER.md`:301, 320, 600). ARGON01 REPORT:66, 77-83 names the global class as the only route its no-go leaves open, for kappa, not for the tie.
- Leaf-mean SUBTRACTIONS are on record as constructions: L350's -c2(K - <K>)^2 (STANDING.md:206), CFG172D's zeta(eps_b - <eps_b>) (`campaign_fresh_gravity/CFG172D_FROZEN_CRITERIA.md`:65). astra's heat-field action carries a whole-leaf mean-one constraint (`FRESH_AND_CRISPY_ASTRA_IDEAS.md`:39; astra's, read only).
- Not found on record: a0 set dynamically by the leaf average of the dark-energy density. CT12 grades that.
- Literature (memory, PROVISIONAL, nothing fetched): Henneaux-Teitelboim / unimodular Lambda as a global integration constant; Kaloper-Padilla 2014 sequestering (global variables, needs finite spacetime volume); projectable Horava gravity, whose Hamiltonian constraint holds only integrated over each leaf ("dark matter as an integration constant", Mukohyama 2009).

## 1. The action graded

Signature (-,+,+,+), unitary gauge tau = t where useful. v3s (`covariant_push_2026_10_22/V3_FULL_PICTURE.md`:25-35) with its bare Lambda removed from J_x, the dark energy carried by a minimally coupled sector with stress tensor T^DE (canonical phi as the worked case), and a0 promoted to a function of khronon time:

    S = (c^3/16 pi G) ∫ sqrt(-g) [R - 2 J(Y; a0(tau)) + 2 K(Q)] - (gamma_L/2) ∫ sqrt(-g) [max(D.P, 0)]^2
        + S_DE[g, phi] + S_m[g, matter]
        + ∫ d^4x sqrt(-g) lambda(tau(x)) [ sigma(tau(x)) - T^DE_{mu nu} n^mu n^nu ],      a0(tau)^2 = xi G sigma(tau)

  (SI: sigma is an energy density, so a0^2 = kappa^2 c^2 G rho_DE gives xi = kappa^2.)

- sigma(tau) and lambda(tau) are functions of the khronon time only (one number per leaf; tau is a scalar, so S is diffeomorphism invariant and invariant under tau -> f(tau) with sigma, lambda relabelled). Neither has a time derivative in S.
- Varying lambda(tau) gives, leaf by leaf, sigma = <T_nn>_leaf with the measure sqrt(-g) delta(tau - tau0) = N sqrt(h) d^3x (lapse-weighted volume average). For an infinite leaf the average is the limit over growing balls (statistical homogeneity assumed, stated); for a compact leaf it is exact.
- Varying sigma(tau) gives lambda = -<dL_J/d sigma>_leaf. With the weak-field J Lagrangian L_J = (a^2/4 pi G) f(g/a), f(s) = s - ln(1+s) (as CT5 FROZEN_CRITERIA section 2), dL_J/d(a0^2) = h(x)/(8 pi G), h = 2f - s f'. So lambda = -eps <h(x)>_leaf, eps = kappa^2/(8 pi) = xi/(8 pi), x = |khronon acceleration|/a0 = sqrt(Y)/a_g. (To be re-derived symbolically in the script.)
- Reciprocity (expected by hand, to be derived): the term +eps<h> T_nn changes the DE field's quadratic action to (1/2)(1 + epsbar) phi_n^2 - (1/2)(1 - epsbar)|D phi|^2 - (1 - epsbar) V, epsbar(tau) = eps <h>_leaf. This is CT7's C' energy portal (CT7_REPORT.md:179, unhealthy where the LOCAL h > 8 pi/kappa^2) with h replaced by its leaf average.

## 2. Gates (fastest death first; stop at the first FAIL; numbers restated from the CT reports)

**G0 health** (CT_GATES_COMMON.md:6). PASS iff all of (a)-(e):
- (a) DOF: v3s's 3 (V3_FULL_PICTURE.md:184) + 1 (phi) = 4 local DOF; sigma and lambda add no local DOF and no global DOF (no momenta; primary p_sigma, p_lambda ~ 0 and the two leaf equations form a second-class set). Checked symbolically: no derivative of sigma or lambda in S.
- (b) No ghost: DE kinetic coefficient 1 + epsbar > 0.
- (c) CT5's instability absent: a0 cannot respond to the local field. The local slaving derivative d ln a0 / d ln g at a point is bounded by the leaf-volume fraction of the region changed; with a0 leaf-uniform the khronon/dust coefficients are the unslaved M_T = 1 + x, M_L = (1 + x)^2 >= 1 (V3_FULL_PICTURE.md:61, `switched_stable_where_positive`), checked on the CT5 grid x in [1e-3, 106.8 / 88.4]. Finite-leaf bound with V_leaf = the Hubble ball (c/H0) and a 1 Mpc region with delta T_nn / rho_DE = 1 (worst case): |d ln a0| <= 0.5 V_loc/V_leaf.
- (d) No gradient instability of the DE field on any leaf: 1 - epsbar(z) > 0, i.e. <h>_leaf < 8 pi / kappa^2 (= 100.53 at kappa = 1/2; reported beside at the alt footing's tied kappa 0.6043, ungraded). Evaluated:
  - (d1) exact FRW: Y = 0, h(0) = 0, epsbar = 0.
  - (d2) today (late-time static backgrounds): upper bound on <h> from (i) the diffuse peculiar field, Maxwellian with sigma_g0 = 0.0104-0.0125 a0 (k02 `.out`:11-13, v_rms 600 km/s, the larger bracket), and (ii) all cosmic baryons placed in point masses of one mass M (law S, unscreened h, which bounds v3s's screened one: CT7_REPORT.md:217), M in {1, 1e9, 1e10, 6e10, 1e12, 1e14, 1e15} Msun, integrated out to half the mean separation; take the largest.
  - (d3) every earlier leaf back to BBN (z = 4e8), in v3s's own cosmology: the khronon acceleration on a leaf is sourced by the khronon charge through the hold equation (V3_FULL_PICTURE.md:54), whose flux is capped, j = a0 x/(1+x) < a0 (X14), so x >= g_lin/a0, where g_lin is the Newtonian acceleration of the charge perturbation (the y of X18 README:15). Lower bound, horizon-scale, order of magnitude: g_lin = 4 pi G rho_tau delta_tau / k_phys with k_phys = H/c and delta_tau = 2 Phi, Phi = (2/3) sqrt(A_s) (A_s 2.1e-9, CT8's CLASS base; neutrino factor ignored), rho_tau = the dust phase at omega_x/omega_b = 4.9 (low end of CT3's requirement), raw inputs as CT8 (SN Omega_L 0.666, native h 0.6789, BBN omega_b 0.0224, omega_r from T_CMB and N_eff 3.046). Bracket g_lin by x/÷ 10 for the O(1) factors. Since h is convex (to be shown: h'' > 0), Jensen gives <h> >= h(<x>), <x> = sqrt(8/(3 pi)) x_rms for a Maxwellian field.
  - PASS (d) iff epsbar < 1 in (d1), (d2), and in (d3) at the ÷10 end of the bracket for every z <= 4e8. If (d3) fails only at the central or x10 end, label "G0 CONDITIONAL". If (d3) fails at the ÷10 end: G0 FAIL. If x is undefined because g_lin >= a0 (no held solution, X18 README:158), that leaf is counted as epsbar unbounded (FAIL), not skipped.
- (e) W4b: inherited from CT2_REPORT.md:7, UNDECIDED; reported, not graded.

**G1 weak field** (CT_GATES_COMMON.md:7). With a0 leaf-uniform, v3s's static limit is law S unchanged (V3_FULL_PICTURE.md:47-49). PASS iff max |log10 g - log10 g_law| <= 0.01 dex over 1e-12 < g_b < 1e-8 m/s^2, both footings, with a0 shifted by the (c) finite-leaf bound.

**G2 local constancy** (CT_GATES_COMMON.md:8). Void / field / cluster spread of log10 a0 <= 0.015 dex, both footings, including a local DE perturbation: worst case delta T_nn / rho_DE = 1 over a 1 Mpc ball, Hubble-ball leaf; plus the lapse weighting (Phi/c^2 <= 1e-4 over the same ball).

**G3 tie** (CT_GATES_COMMON.md:9). (a) symbolic: on FRW, <T_nn>_leaf = rho_DE(t) c^2 including kinetic energy (T_nn = phi_n^2/2 + |D phi|^2/2 + V). (b) a0(z)/a0(0) vs sqrt(rho_DE(z)/rho_DE(0)) at z 1, 1.5, 2.33 (<= 0.05 dex) and the least-squares slope over z {0, 1, 1.5, 2.33} (0.5 +- 0.01) in CT7's realisable backgrounds (B2 thawing -0.9/-0.1, B3 -0.95/+0.35, CT7_candidate_C/FROZEN_CRITERIA.md:232), with the corrections: frame (1 + w) v^2/c^2 at v = 1e-3 c, the O(epsbar) difference between the tied and the gravitating DE density, lapse weighting. (c) What fixes kappa: kappa^2 = xi by inspection; rename test.

**G4 local gravity** (CT_GATES_COMMON.md:10): only if G0-G3 pass; inherited from v3s (CT2_REPORT.md:7: Q2 <= 3.6e-8 of Park, Mars 0.173, gamma - 1 <= 1.3e-13, |dv/c| <= 5.1e-32) iff phi stays minimally coupled and a0 is leaf-uniform; new item reported: a0's secular drift d ln a0/dt = -(3/2)(1 + w) H.

## 3. If a gate fails

The candidate stops there. G1-G3 values computed from the same equations may be printed as UNGRADED READINGS, labelled, with no gate verdict. No retuning of xi, L*, mu_K, J_x or the tie measure; no knob scan. Escapes that change the candidate (tie on V only, a turned-off J) are named, not graded.

## 4. Hand-set constants to count

xi (kappa^2 = xi), the tie measure (lapse-weighted volume; T_nn in the khronon frame), the DE sector's own constants (V0, shape, initial data), L*, mu_K, J_x's form (POSTULATED), the dust abundance (v3s initial condition), and the averaging prescription for an infinite leaf.

## 5. Hand expectations (worked before freezing; disclosed)

- (c) passes exactly: CT5's band came from a0 slaved to the local g; here a0 sees only leaf integrals.
- (d2) passes by a wide margin (epsbar today ~ 1e-6-1e-4).
- (d3) is the danger: in the radiation era the horizon-scale acceleration is ~ Phi c H(z), and c H0 / a0 ~ 7, so x grows like E(z) Omega_dust(z), i.e. like (1 + z); expected crossing of <x> ~ 110 near z ~ 1e4, and far above it at BBN. Expected G0 FAIL at (d3).
- G1-G3 readings expected exact (G3 slope 0.5 to < 1e-3), kappa a TRADE.

Compute: one python/sympy script, single thread, seconds, < 1 GB.

kappa = 1/2 FITTED; not theory closed.
