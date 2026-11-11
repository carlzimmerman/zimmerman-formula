# VSH1 FROZEN CRITERIA: AKS1's estimate T7, computed (2026-11-11)

TEST lane, quarantined. Committed ALONE, before any script or number of this lane. Adopts nothing, relabels nothing
(AKS1's labels stand as recorded), registers nothing. kappa = 1/2 FITTED; not theory closed. Footings canonical
(a0 9.3603e-11 m/s^2) and alt (1.1312e-10), never pooled. The component is cold dark energy, a field, never a particle.
Requested by the owner on 2026-11-11 ("do the AKS1 estimate").

## 0. Question

AKS1 Part T (`toe_2026_11_10/AKS1_acceleration_keyed_sink/`, FROZEN_CRITERIA_T.md lines 84-96) closes its fourth branch,
D-V(h) (action (A) kept whole, frame-free viscosity of the clock, heat kept as entropy), on an ESTIMATE, T7: settling a
halo to CFG461's edge r_e* by today needs a kinematic viscosity nu >= nu_S = r_e*^2/t0, while the record's forest line
allows only nu <= nu_F (141.9 / 142.0 kpc km/s). Margins 0.03 / 0.82 / 8.17 at log M_b 9 / 10.5 / 11.5.

nu_S is a DIFFUSION time across r_e*. A viscous compressible flow that folds does not settle by diffusion: the fold
becomes a shock, and the gas behind an accretion shock is at rest whatever the viscosity (the viscosity sets only the
shock's thickness, about nu/dv). This lane computes the collapse and asks whether a clock with nu = nu_F is settled
inside r_e* by today.

Disclosed before freezing: the reasoning above; the collisional self-similar result that the accretion shock sits at
about 0.35 of the turnaround radius (from memory, PROVISIONAL, not used in grading); FLD1's table (R_fold, R_ta); AKS1's
r_e*, R_cap and nu_F. No VSH1 number exists.

## 1. Model (fixed)

FLD1's shell equation, unchanged (`fable52_push/FLD1_fold_reach/fld1_shells.py`, mode hubble, law on, mu_K = 0, start
z = 10, baryon ramp 1 Gyr, eps = 1 kpc, KD1's cosmology per footing, its Lagrangian grid 0.03 X_M to 15 X_M):

    r'' = -G M_b s(t) r/(r^2 + eps^2)^{3/2} - G M_X/r^2 - (4 pi/3) G rho_b(t) r + Omega_L H0^2 r + U(G [M_X - (4 pi/3) nbar(t) r^3]/r^2)

plus, for the clock's charge treated as a compressible fluid in Lagrangian zones between the shells:
- pressure p = (gamma - 1) rho e, gamma = 5/3, e = 0 at the start ("heat kept as entropy"; no cooling);
- shear viscosity, kinematic nu, traceless: sigma_rr = (4/3) rho nu (dv/dr - v/r), force (1/(rho r^3)) d(r^3 sigma_rr)/dr,
  heating (4/3) nu (dv/dr - v/r)^2 per unit mass. It vanishes identically on a Hubble flow. Solved implicitly;
- a von Neumann-Richtmyer artificial viscosity in compressing zones (quadratic coefficient 2, linear 0.3) for shock
  capture where the grid does not resolve nu/dv. Its heat is kept;
- a regular centre (v = 0 at r = 0), free outer boundary (p = 0).
Graded resolution N = 600 zones. Graded viscosity nu = nu_F of the footing (AKS1's value, read from `aks1_t.json`).
r_e* and R_cap per mass and footing are read from `aks1_t.json`. Masses log M_b 9, 10.5, 11.5 (AKS1's).

Hypotheses, stated: the clock's charge carries the pressure (D-V(h)); FLD1's force law is used as written, including
inside the settled region; spherical symmetry.

## 2. Measured at z = 0 (per mass, footing)

- R_ta: the largest radius among shells with v <= 0.
- Hot zone: (gamma - 1) e >= 0.05 r |g| at the zone, g the gravitational acceleration there.
- R_sh: the largest radius of a hot zone (0 if none).
- S: sqrt( sum dM v^2 / sum dM r |g| ) over zones inside r_e* (0 zones inside: not evaluable).
- SETTLED at that mass: R_sh >= r_e* AND S <= 0.10.

Reported, not graded: the time and redshift at which R_sh first passes r_e*; R_sh/R_ta; R_sh against FLD1's R_fold, AKS1's
R_cap and the KiDS inner window; the charge inside R_sh in units of M_b and as a fraction of the law's halo mass
sqrt(M_b a0/G) R_sh; hydrostatic residual inside r_e*; nu = 0 (artificial only), 0.1 nu_F and 10 nu_F; gamma = 4/3.

## 3. Known answers (all must pass, else NO VERDICT)

- KA1 Noh (spherical, gamma 5/3, rho 1, v -1, cold): shock radius at t = 0.6 within 5 % of t/3; mean post-shock density
  between r = 0.05 and 0.9 r_shock within 15 % of 64; total energy conserved to 2 %.
- KA2 Hubble flow: with M_b = 0 the run stays cold: max (gamma - 1) e <= 1e-6 (km/s)^2 and no hot zone at z = 0.
- KA3 outer infall: R_ta at z = 0 within 3 % of FLD1's table at log M_b 9 (88 kpc) and 11.5 (600 kpc), canonical.
- KA4 resolution: N = 300 against N = 600 at log M_b 10.5 canonical: R_sh within 10 %, same SETTLED verdict.

## 4. MUTATE (separate outputs; each must change its stated outcome, else disclosed)

- M1 heat removed (e set to 0 every step): no mass reads SETTLED.
- M2 no baryons (M_b = 0): no mass reads SETTLED.
- M3 run stopped at z = 6: log M_b 11.5 does not read SETTLED.

## 5. Labels (per footing)

- **SETTLES BY SHOCK**: all three masses SETTLED at nu = nu_F. Then T7's nu_S is not a bound, and D-V(h) does not close
  on T7. This says nothing about whether D-V(h) closes on other items (Gauss, the amount, the reach).
- **DOES NOT SETTLE**: some mass is not SETTLED. D-V(h) closes at that mass by computation.
- **NO VERDICT**: a known answer fails.

Amendments, if any, are post hoc, committed alone and disclosed.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
