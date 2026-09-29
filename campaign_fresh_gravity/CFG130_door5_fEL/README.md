# CFG130 (Door 5): does a non-negative f(E, L) exist for the CFG44 target? Yes, kinematically. That is not a mechanism.

Frozen question and criteria: `FROZEN_QUESTION.md` (written before any script; the menu of doors was written knowing the target; CFG44's B1 N6 had already reported an isotropic f(E) >= 0 on a 5-85% potential-quantile window, disclosed there). Scripts: `D5_A_eddington_pointmass.py` (Eddington inversion and the entropy test on the point-mass target), `D5_B_orbit_lp.py` (a general orbit-superposition linear programme for any beta(r)), shared `D5common.py`. Each has a MUTATE control that exits 1. Units a0 = G = M_b = 1 (r_M = 1); no constant is introduced.

## Bottom line

1. **Point mass: beta is exactly 0** (M_b(<r) = M for r > 0, so beta = -(1/2) dlnM_b/dlnr = 0; the anisotropic question is the isotropic one). Eddington's f(E), computed analytically over E = Phi(r_E), r_E in [1e-5, 1e5] r_M (E from -1e5 to +11), is **strictly positive everywhere**: the integrand d^2 rho/dPhi^2 is positive at every point (f/Int|integrand| = 1), it reproduces the analytic Kepler-cusp limit (8 sqrt2 pi^3)^-1 (-E)^(-1/2) to 4 digits, and it round-trips to rho_c to 4e-4. No region with f < 0.
2. **Extended baryons (exponential sphere, h/r_M = 0.03 ... 3): the orbit-superposition LP is FEASIBLE** for the density alone (V1), for density plus beta(r) = -(3/2) rho_b/rhobar_b (V2, the question as asked) and for density plus beta plus sigma_r^2 = V_c^2/2 (V3, CFG44's full restatement), at two resolutions, with residual 0.0000 to the printed digits. The same holds for the isotropic-moment reading (beta = 0). The answer is a non-negative MEASURE on the (E, L) grid; a smooth f is guaranteed only for the point mass (Eddington). CFG44's open item "f(E,L) >= 0" is therefore CLOSED in the positive direction on its own hypotheses: the target is kinematically realisable.
3. The test is not vacuous: the LP rejects a Jeans-inconsistent target (Plummer with sigma_r^2 doubled: eps* = 0.26), a cored sphere with imposed beta = +0.5 (eps* = 0.15-0.16), and the CFG44 target itself with the SIGN of beta flipped to +(3/2) rho_b/rhobar_b (eps* = 0.53 at h = 0.3): the tangential bias is required, and is allowed.
4. **Not a Lynden-Bell / maximum-entropy extremum** (for the Boltzmann and Fermi-Dirac entropies at fixed mass and energy): d ln f/dE for the point mass runs from +0.3 to -2.0 (an extremum needs one constant), the best isothermal fit of rho_c over x in [0.1, 30] is off by a factor 19, the best 3-parameter Fermi-Dirac fit by 34%, and the extended target has |beta| up to 1.5 where the stationary f depends on E alone (beta = 0). Scoped to those entropies.
5. **What the door does and does not settle.** A positive f(E, L) is a NECESSARY condition for a collisionless-fluid mechanism, not one. It says nothing about why C(r) = (a0/4 pi) M_b(<r): in the exponential sphere f is determined by the target density and the potential, so it encodes the enclosed-mass dependence rather than deriving it. Gates: **G1 (mechanism reproduces the target) not addressed** (the same dimensionless target is realisable at every mass because only h/r_M enters; no mechanism); **G2 not addressed; G3 not addressed; G5 not addressed; G4 passes trivially** (zero new constants: the inputs are a0, G, M_b, h). The door cannot pass the shared gates as a mechanism whatever the outcome.
6. MUTATE controls: D5_A (a shell bump on rho_c) gives f < 0 at r_E in [1.6, 2.6] r_M and exits 1; D5_B (sigma_r^2 pinned at V_c^2, a Jeans-inconsistent target) turns every V3 result infeasible and exits 1. The round trip A5 does NOT fail under the mutation (it is an identity that holds for a negative f as well; declared in the script).

## Hypotheses used and not tested

Used: spherical symmetry; static, Newtonian; the potential is the target's own P2 total potential (kernel P2, not nu_mono); a collisionless fluid whose f depends on (E, L) only; beta prescribed as a function of r; the fluid density is the target by construction (self-consistency is automatic); the LP window is finite (a two-decade-plus radial window, checked against a wider window for the point mass) and orbits leaving the window are unconstrained outside it.
Not tested: whether the DF is REACHED (formation history, violent relaxation, secondary infall: Door 6), stability of the equilibrium (radial-orbit and tangential instabilities), non-spherical baryons, nu_mono, the potential re-solved from f, evolution through recombination and linear growth (G2), reaction on the baryons (G3), a relativistic completion, entropies other than Boltzmann and Fermi-Dirac (Tsallis; entropy maximisation at fixed density profile, whose extremum would be a different DF, not the target's), a smooth f for the anisotropic case beyond the measure-valued LP solution.

## Caveats stated

- The interior-margin supplement (added after the first LP result, not frozen) gives a positive but tiny floor (min weight / mean weight ~1e-9 to 1e-6) because f spans many orders of magnitude; it is not evidence of a smooth solution.
- The LP feasibility is at a finite grid: eps* = 0 means an exact non-negative solution of the discretised constraints exists (1.4-7.6 thousand orbits against 100-350 rows, so the system is underdetermined); the controls show it can fail, and L1 versus L2 agree.
- Constraints are integrated per radial bin; a bin-scale departure smaller than the bin width is not tested.

Nothing here says the theory is closed.

## Referee note (CFG155, lane bdbcf3fe1; appended 2026-09-29, nothing above edited)

An independent re-derivation reproduces the headline: Eddington's isotropic f(E) for the point-mass target in its own P2 potential is strictly positive at all 1201 energies from x_E = 1e-6 to 1e6, one decade past this lane's window at each end. It holds analytically (d²ρ/dΦ² = x⁵/(π(1+x²)^(7/2)) > 0, no boundary term); three routes agree to 1.8e-8 and every f printed here agrees within 2e-5; its MUTATE (a cored tracer) gives f < 0 at 515 energies. Five minor findings about this lane, none changing the headline:
1. the script's window is r_E = 1e-5 to 1e5, not the frozen 1e-6 to 1e6;
2. the t-integral is cut at Φ(1e7 r_M) with no tail, which lowers f by 1.8e-5;
3. the isothermal control checks only the shape;
4. d ln f/dE comes from np.gradient, 3.4% off at r_E = 1;
5. the lambdified ρ'' cancels catastrophically below r ≈ 1e-4 and returns negative noise there (effect on f under 2.2e-12), so 'the integrand is positive at every point' holds analytically, not as this code evaluates it at small r.
The extended-baryon orbit-superposition LP was not re-derived by CFG155. Independence in CFG155 stops at the read targets and CFG44's target definition.
