# CFG353: a turnaround-density reader from a leaf-elliptic auxiliary potential

Criteria: `FROZEN_CRITERIA.md` (commit c9d9a1d7b, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; no DM particle (the cold MASS is still required). Owner decision 2026-10-06: the switch may read the cold
component (MS1 relaxed for exploration). **Under the original MS1 this reader is NOT ADMISSIBLE.**

**Verdict (frozen rule, route E0): NO-GO.** Legality passes; (a), (a'), (b), (c) and (d) fail, with 0 fitted constants.
The obstruction is the ZERO POINT of Phi_d. The estimator is exact only when Phi_d = 0 at the host's own infinity. A
leaf-defined Phi_d has a leaf-global zero point. The E0 part of this is a theorem (Lean T9); the size of the
large-scale offset is a measured number. This is a scoped result, not a closure.

## Estimator and action
- Leaf constraint: lap Phi_d = 4 pi G (rho - <rho>_Sigma), with rho = cold + baryons.
- Estimator: rho_est = 3 |grad Phi_d|^2 / (4 pi G |Phi_d|). The source is the overdensity, so it estimates
  rho_enc - rho_bar.
- Switch: f = H_strict(3 |grad Phi_d|^2 - (Delta_ta - 1) 4 pi G rho_bar |Phi_d|). It is written without division,
  so 0/0 gives OFF.
- Action:
  S ⊃ Int_Sigma sqrt(h) N [ mu (lap Phi_d - 4 pi G (rho - <rho>)) + nu Phi_d ] + Int sqrt(-g) f(Phi_d, grad Phi_d) L_MOND
  (multipliers as for the record's U, L, lambda_0).
- **Exact form (spherical):** rho_est = (rho_enc - rho_bar) eta, with eta = r|Phi_d'|/|Phi_d| = -dln|Phi_d|/dln r.
  - eta = 1 iff there is no overdensity outside r and Phi_d is zero at infinity.
  - Controls: K1 point mass, exact (2e-16). K2 uniform sphere, exact outside; inside the ratio is 2r^2/(3R^2 - r^2),
    which is 0 at the centre.
- **Zero-point routes:**
  - E0, <Phi_d> = 0: the only smooth leaf-scalar choice with no constant. Scored.
  - E1, Phi_d - sup Phi_d: non-smooth; the sup is modelled as 4.5 sigma_Phi. Reported with the same lines.
  - Einf, zero at the host's local infinity: the estimator's premise. No leaf construction exists, so it is reported
    only.

## Legality: PASS
- L1: sympy Euler-Lagrange for Phi_d and mu.
- L2: every term is a leaf scalar density; <rho> is treated as CFG329's <K>.
- L3: no d_t of Phi_d, mu or nu appears, so there are no momenta and no growing conjugate (contrast CFG349's
  lambda = C/(1-m)).
- L4, on a 1D periodic leaf with a smoothed switch: the adjoint gradient matches finite differences to 2.3e-8, and the
  translation Noether sum is 5.4e-12 (momentum conserved).
- For the sharp H, df/dgrad Phi is a surface delta. So mu has a finite jump and matter crossing the edge sees a finite
  potential jump: 0.05-4.8 V_c^2 at the Einf edge. This is bounded but O(1), the same class as CFG351's front
  impulse.

## Results
**(a) FRW / linear: FAIL (E0).** FRW itself is OFF.
- In the linear Lambda-CDM field the E0 Phi_d has a nodal surface, and rho_est diverges there (T9).
- ON volume fraction: 1.7e-2 at z = 0, 2.1e-2 at z = 1, 4.8e-3 at z = 10 and 5e-5 at z = 1000 (R = 8 h^-1 Mpc,
  k_min = H0/c). The maximum is 5e-2 with a 1 Gpc IR cutoff. It scales with the amplitude D(z).
- E1 gives 0 (pass).

**(a') sheets and filaments: FAIL (both routes).** The cells are compensated; void contrasts below -1 are excluded.
- E0, false-ON cell fraction:
  - sheets: 0.10-0.44 (delta_w 0.5-3);
  - filaments: 0.04 (delta_f 1) to 0.42 (delta_f 10, cell x5);
  - max rho_est/rho_bar inside a filament: 16 at delta_f = 10.
- E1, false ON:
  - filament delta_f 5 (x5): 3.7%;
  - filament delta_f 10: 21.8% (x5) and 1.6% (x10);
  - in-filament max est 6.4-12.8 against a threshold of 4.55.
- Near the E1 zero, rho_est tends to 6|delta_v|/d (T7). So planar voids fire for |delta_v| > 0.759 (T6), and 3D voids
  never fire (T5).
- Einf: line and plane potentials have no local infinity, so the estimator is undefined there.
- Under the z = 0 threshold (11.8) there are fewer false ONs, but E0 still has 2-41%.

**(b) bound hosts (24 DE12): FAIL (E0, E1).**
- The host's own Phi_d(r_ta) is 4e-8 to 4e-6 c^2. The linear LSS potential offset sigma_Phi is 4.6-5.4e-5 c^2,
  1-3 dex larger.
- So |Phi_d| at a host is set by its large-scale environment (T11).
- E0, P(ON at 30 kpc): 0.29-0.48 on the 1e10 hosts at z 2.5/4, 0.82 at z 1, and >= 0.99 elsewhere.
- E1, P(ON at 30 kpc): 0.00-0.06 on the 1e10 hosts.
- Einf passes: the margin at 30 kpc is >= 36. A 10% gas compression changes ln rho_est by at most 0.12, so there are
  0 flips.

**(c) edge: FAIL (E0, E1).** Edge within 100 kpc of r_ta:
- E0: medians 0-0.45 r_ta, 0/24 within 100 kpc;
- E1: 0-0.20 r_ta, 0/24;
- Einf: 0.93 r_ta (eta(r_ta) = 0.853 from the EdS infall overdensity beyond r_ta), 20/24 within 100 kpc. It misses
  the M_b 1e12 hosts at z 0.25 and 1 (174 and 130 kpc).

Phi_d, mu and nu are elliptic (no characteristics). The edge is a level set of a smooth field, so it has zero width for
the sharp H.

**(d) data: FAIL (E0).** The CFG352 harness was copied with its scoring unchanged. The edge fractions come from the
KiDS-like lens bins at z = 0.25 with the isothermal law mass.

| row | edge | KiDS d chi2 (can / alt) | SPARC | growth |
|---|---|---|---|---|
| control | 1.0 | -9.18 / -9.30 pass | pass | pass |
| Einf (not constructible) | 0.907 | -10.65 / -11.98 pass | pass | pass |
| E0 median, best bin | 0.164 | +264.6 / +260.0 FAIL | pass | pass |
| E0 median, worst bin | 0.068 | +584.6 / +579.8 FAIL | pass | pass |
| E1 median, best bin | 0.064 | +609.0 / +603.9 FAIL | pass | pass |

The edge is not at 1.0 r_ta in any route, so the CFG352 control row does not apply as-is.

## Constants
- 0 fitted.
- Delta_ta is derived from a Lambda-CDM shell ODE. It matches CFG4_switch exactly (11.806 at z = 0, 8.893 at z = 0.25)
  and depends on the background (Omega_m, Lambda) and on z: 9 pi^2/16 = 5.552 in EdS, 5.61 at z = 4, 5.72 at z = 2.5,
  6.41 at z = 1.
- E1's sup = 4.5 sigma_Phi is a modelling assumption for the leaf maximum, not a theory constant.

## Ownership and the UFD link (reported)
- Under E0/E1 a subsystem's |Phi_d| is dominated by the host's and the large-scale potential. So class A satellites
  and UFDs (own Phi far below 1e-5 c^2) are switched by their environment, not by their own boundedness. That is
  inconsistent with CFG344's own-clump reading.
- Under Einf, class E sits inside the host ON region and still needs CFG333's R2.

## Pointer (analytic remark, NOT computed or scored here)
The tangential tidal eigenvalue g/r = (4 pi G/3) rho_enc is exact for any spherical distribution and is shift-invariant
(no zero point). In ideal geometry the middle eigenvalue is 0 outside a line mass and in a sheet. Inside a uniform
filament it is 1.5 delta_f rho_bar, so it would fire for delta_f > 3.03. This would need its own frozen lane.

## Controls
- K1, K2, K3 (FRW OFF) and K4 (Delta_ta vs CFG4) all pass.
- MUTATE (CFG353_MUTATE=1, threshold Delta = 1): false ON in filaments and sheets under E0 and E1, so the mutation is
  detected (rc 1).

## Lean
`CFG353_estimator_certificates.lean`: 12 theorems, no sorry, standard axioms only, rc 0 (`.out`). They cover:
- point-mass and sphere identities, and the inside ratio <= 1;
- 9 pi^2/16 > 1;
- 3D void never fires; planar void fires;
- near-max value 6k;
- strict-H FRW-off;
- **E0 unboundedness at a zero of Phi_d** (the theorem behind (a));
- eta <= 1;
- offset suppression;
- MUTATE ON for any gradient.

## Scope
- Linear LSS: Gaussian, Eisenstein-Hu no-wiggle, sigma_8 = 0.81. Phi and grad Phi are independent at a point. The host
  is treated as uncorrelated with the LSS field (real hosts sit in wells, which makes |Phi| larger).
- The exterior infall is the EdS self-similar (delta_lin ∝ M^-1) profile, scaled to the Lambda-CDM Delta.
- The KiDS lens r_ta uses the deep-MOND isothermal law mass.
- The 1D cells are idealised.

## Run
```
python3 campaign_fresh_gravity/CFG353_turnaround_density_switch/cfg353_turnaround_density.py > campaign_fresh_gravity/CFG353_turnaround_density_switch/cfg353_turnaround_density.out   # rc 0, ~10 s
CFG353_MUTATE=1 python3 campaign_fresh_gravity/CFG353_turnaround_density_switch/cfg353_turnaround_density.py > campaign_fresh_gravity/CFG353_turnaround_density_switch/cfg353_turnaround_density_MUTATE.out   # rc 1 (mutation detected)
python3 campaign_fresh_gravity/CFG353_turnaround_density_switch/cfg353_edge_harness.py > campaign_fresh_gravity/CFG353_turnaround_density_switch/cfg353_edge_harness.out   # rc 0, ~10 s, after the main script
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG353_turnaround_density_switch/CFG353_estimator_certificates.lean
```
