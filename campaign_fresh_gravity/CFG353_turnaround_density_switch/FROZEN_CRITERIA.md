# CFG353 FROZEN CRITERIA: a turnaround-density reader from a leaf-elliptic auxiliary potential

Frozen before any script. kappa = 1/2 fixed (fitted); nu_mono; no DM particle (the cold MASS is still required).
Owner decision 2026-10-06 (recorded in CFG351's frozen file): the switch may read the cold component (MS1 relaxed for
exploration). Under the original MS1 this reader (it sees cold + baryon density) is NOT ADMISSIBLE.

## 1. Object
- On each khronon leaf Sigma: lap Phi_d = 4 pi G (rho - <rho>_Sigma), rho = cold + baryons (total matter).
- A compact/homogeneous leaf fixes Phi_d only up to a constant. Zero-point routes:
  - **E0 (primary, scored):** <Phi_d>_Sigma = 0, imposed by a global multiplier nu. The only smooth leaf-scalar choice
    with no new constant.
  - **E1 (scored, reported second):** Phi_d - sup_Sigma Phi_d (zero at the leaf maximum; non-smooth).
  - **Einf (reported only):** zero at the host's own local infinity (the estimator's premise). Scored only if a leaf
    construction with no new constant is exhibited.
- Estimator: rho_est = 3 |grad Phi_d|^2 / (4 pi G |Phi_d|). The source is the OVERDENSITY, so rho_est estimates the
  enclosed mean overdensity rho_enc - rho_bar. The switch is therefore
  f = H_strict( 3 |grad Phi_d|^2 - (Delta_ta - 1) 4 pi G rho_bar |Phi_d| ),
  i.e. (rho_bar + rho_est)/rho_bar > Delta_ta, written without division (0/0 -> OFF).
- Delta_ta(z): the spherical-collapse turnaround contrast rho_enc/rho_m: 9 pi^2/16 in EdS; Lambda-CDM value at z
  computed by a shell ODE (must match CFG4_switch's D1 one_plus_delta_ta within 1% at z = 0, 0.25).
- Action: S = S_chassis + S_matter + Int_Sigma sqrt(h) N [ mu (lap Phi_d - 4 pi G (rho - <rho>)) + nu Phi_d ]
  + Int sqrt(-g) f(Phi_d, grad Phi_d) L_MOND.

## 2. Exact form to derive (reported)
Spherical symmetry: rho_est = (rho_enc - rho_bar) * eta(r), eta = r |Phi_d'| / |Phi_d| = -dln|Phi_d|/dln r.
eta = 1 iff no overdensity outside r (Keplerian exterior) with zero at infinity. The exterior infall region is
modelled by the exact EdS spherical-collapse (pre-turnaround) shells with delta_lin ∝ M^-1 (B's / Bertschinger's seed).

## 3. Tests and pass lines (route E0 scores the verdict; E1 also reported with the same lines)
- **L legality:** L1 EOM derivable (sympy, reduced action); L2 every term a leaf scalar density (CFG329 method;
  <rho> treated as CFG329's <K>); L3 multipliers mu, nu carry no time derivative (elliptic, determined by sources), so
  no unbounded multiplier energy; mu finite for a smoothed f, finite potential jump for the sharp H; L4 momentum:
  on a 1D periodic leaf the adjoint gradient matches finite differences to 1e-5 relative and the translation Noether
  sum Sum_i (dE/drho_i) d_x rho_i vanishes to 1e-8 relative.
- **(a) FRW / linear:** PASS iff (i) FRW (delta = 0) is OFF and (ii) in the linear Lambda-CDM Gaussian field (sigma_8
  0.81 at z = 0, and scaled by D(z) to z = 1, 3, 10, 1000) the ON volume fraction is < 1e-6 at every amplitude, for
  Gaussian smoothing R = 8, 20, 50 h^-1 Mpc, and IR cutoff k_min = H0/c (also reported at 2 pi/1000 Mpc).
- **(a') unbound sheets and filaments:** compensated planar walls (delta_w = 0.5, 1, 2, 3) and cylinders
  (delta_f = 1, 2, 5, 10) in cells of size ratio 3, 5, 10. PASS iff the ON fraction of the cell is 0 for all of them
  (none is turned around in all directions). The false-ON fractions and max rho_est/rho_bar are the key numbers.
- **(b) bound hosts (CFG347's 24: z 0.25/1/2.5/4, M_b 1e10/1e11/1e12, both footings, DE12 NFW):** PASS iff ON at
  30 kpc on 24/24 with probability >= 0.99 over the linear LSS ensemble at the host (route gauge), AND a 10% gas
  compression at 30 kpc (all baryons inside, CFG351's bound) moves rho_est by less than the margin to threshold (no
  flip) on 24/24.
- **(c) edge:** PASS iff |r_e - r_ta| <= 100 kpc on 24/24 (r_ta = B's edge with the same Delta_ta(z)) and the switch
  stress is bounded (finite multiplier jump). Characteristics, edge width and the jump/V_c^2 impulse reported.
- **(d) data:** CFG352's harness copied. KiDS d chi2 <= +9 both footings, SPARC A3 and growth pass, at the actual edge.
  If the edge fraction is realisation-dependent, scored at the median; the 16th percentile reported. If the edge is
  at 1.0 r_ta, the CFG352 control row applies.
- Ownership (classes A/E) and CFG344 UFD consistency: reported.

## 4. Verdict rule (route E0)
- SWITCH DOES BOTH: L, a, a', b, c, d all pass, 0 fitted constants.
- WITH COST: all pass with n >= 1 constants.
- PARTIAL: at most one failure.
- NO-GO: two or more failures; state the obstruction; certify in Lean if it is a theorem.

## 5. Controls
- K1 point mass: rho_est = 3M/(4 pi r^3) to 1e-12 relative.
- K2 uniform sphere: equal outside; inside rho_est/rho_enc = 2 r^2/(3R^2 - r^2).
- K3 FRW: OFF.
- K4 Delta_ta: EdS 9 pi^2/16 to 1e-6; Lambda-CDM vs CFG4_switch within 1%.
- MUTATE (CFG353_MUTATE=1, outputs *_MUTATE): threshold Delta = 1 (any overdensity). Must turn ON in filaments and
  fail (a'); the run exits 1.

## 6. Lean
Estimator identity (point mass, sphere outside, sphere inside ratio), 9 pi^2/16 > 1, the strict-H FRW-off fact, the
E0 unboundedness at a zero of Phi_d, near-maximum bound 6|delta|/d, eta <= 1 with positive exterior overdensity, the
LSS-offset suppression inequality. Lean 4 + Mathlib, no sorry.
