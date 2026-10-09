# CFG507 FROZEN CRITERIA: where does the cold energy come from? Three origin mechanisms not on the record

Committed alone, before any script or machine-computed number. Owner question (2026-10-08): "where does the cold energy come from?"
Terms: COLD ENERGY = the framework's cold clumping component (pressureless, w ~ 0 today, Omega_c/Omega_b = 5.364, adiabatic with the
baryons per the CMB; its mass is required; no particle is assumed). DARK ENERGY = the vacuum component; the law a0 = kappa c sqrt(G rho_DE),
kappa = 1/2 FITTED, a0 tracks rho_DE(z). Never "theory closed". "The origin is still an input" is an acceptable outcome. Offline only:
on-disk DESI DR2 chains (`../_external_data/desi_dr2_chains/{cmb,pantheonplus,union3,desy5}`), no downloads.

## 0. Record read before freezing (not blind; listed so nothing is repeated)

| record item | route | status |
|---|---|---|
| GC thread 06-19 (ghost condensate dark sector) | one scalar: Y-mode = MOND, Q-mode = a^-3 dust | housed, AMOUNT FREE |
| L374 condensate dust | ghost-condensate dust through stream crossing | BREAKS at first crossing; linear wave field passes |
| L319/L320 Lambda-triggered carrier | decay switched on by Omega_Lambda(a) | STOPPED by the owner; not continued |
| L49 D1 | primordial black holes as the cold mass | passes clusters, fails the galaxy gate (x1.82) |
| CFG131 door 8 | interacting vacuum Q(rho_L, rho_c) vs the halo target | scoped NO-GO |
| CFG288 | one field (wave field V = rho_L + m^2 Phi^2; shift charge road S); seeding epochs | label only, AMOUNT FREE (A1: height >= 1.5e10 rho_L; A2: shift charge free); seeding z <= 1e4 EXCLUDED, 1e5/1e6 undecided |
| CFG360 baryon tie | one process fixing charge per baryon | NO-GO (particle at 5 GeV, or the free number relocated to the asymmetry) |
| CFG360-DE | late vacuum decay, khronon clock field, condensate fraction of the vacuum, a0-rate production, phase transition tied to rho_L^(1/4) | PARTIAL: late decay ~1e-17 in place by z = 3000; w = -1 fraction cannot become dust; tied transition fires at z ~ 8.5; untied classes AMOUNT FREE |
| CFG362 | stochastic misalignment during inflation | CONDITIONAL-TESTABLE (H_I <= 83 GeV, 1e21-1e46 e-folds; any B-mode kills it); amount a random draw relocated to H_I |
| CFG368 | late cold <-> vacuum flow (Q ~ rho_vac, rho_c, H rho_vac, H rho_c) vs DESI | OPEN DOOR NOT SUPPORTED (no form improves on LCDM by >= 4 on all SN chains) |
| neutrino lane 10-06 | m1 = rho_L^(1/4), sum 0.0613 eV | hot, not the cold energy; ~3 sigma DESI tension shared with minimal NO |
| CFG383/384 | Bose condensate split / self-interaction | calibration (m ~ 0.8 eV), marginal |
| CFG365/CFG418 | supply from the original baryons; R_c from KiDS via the supply edge | galaxy-level bookkeeping; R_c 4.6-13 contains 5.364 (rests on a free two-halo term); not an origin |
| CFG494 | adiabatic ICs | give the amount (as an input), not the selection |
| CFG496 | any clue linking cold energy and dark energy | 0/15; every mass-free link runs through a0; a single-epoch second check is blind to Omega_L*Omega_m forms |
| PAPER42 (DOI 10.5281/zenodo.23172298) | dark energy = zero-field energy of the MOND field | the vacuum half only; "cosmology still needs the cold mass" |

The owner's three suggested families are partly on the record: (a) as a LATE exchange (CFG360-DE C1, CFG368), (b) as an unsourced
shift charge (GC thread, CFG288 road S), (c) as a transition at the rho_L^(1/4) scale (CFG360-DE C5) and as a potential of the
rho_L height (CFG288 A1). This lane therefore tests the variant of each family that the record has NOT run:

- **M1 (family a): an EARLY exchange, a running (H^2-tracking) vacuum feeding cold energy.** rho_vac = rho_L + nu * 3H^2/(8 pi G),
  energy lost by the vacuum goes into cold energy at rest. Exact background ODE (units rho_crit0, N = ln a):
  d rho_c/dN = -3(1-nu) rho_c + nu (4 Omega_r a^-4 + 3 Omega_b a^-3), with E^2 = (Omega_r a^-4 + Omega_b a^-3 + rho_c + rho_L)/(1-nu).
  No primordial cold energy (rho_c = 0 before the switch-on a_i). Two switch-on variants: S-T (keyed to the local temperature T_i) and
  S-t (keyed to a global time). a0 consequence: a0(z)/a0(0) = sqrt(rho_vac(z)/rho_vac(0)).
- **M2 (family b): the law's own field, with its dust charge SOURCED BY BARYONS.** A shift-symmetric P(X) with an extremum at X0 > 0
  (the ghost-condensate / Scherrer dust branch) and a conformal coupling A(phi) = exp(beta phi / Mbar_Pl) to baryons, as AQUAL/TeVeS
  couple the MOND scalar. The charge J = a^3 P_X phidot obeys dJ/dt = (beta/Mbar_Pl) a^3 rho_b, so J = J_i + J_src(t). This is the only
  route inside "one field" that could tie the cold amount to the baryons. Hand expectation (to be checked numerically): the sourced
  share obeys rho_d,src / rho_b = Delta ln A (the change of every Einstein-frame mass since the source switched on).
- **M3 (family c): a relic whose mass is set by the dark-energy scale, the "dark-energy seesaw" m* = sqrt(rho_L^(1/4) M), M in
  {Mbar_Pl, M_Pl}, frozen out thermally with <sigma v> = k pi alpha^2 / m*^2.** This FORCES A FIELD QUANTUM (a TeV-scale particle);
  it is tested because it is the best-motivated way a single scale could tie Omega_c h^2 to rho_L, and it must be said plainly.

## 1. Hard constraints and pass thresholds (frozen; every mechanism, as applicable)

- **C-AMOUNT.** omega_c = 0.120 +- 0.001 (Planck) reachable; record WHAT fixes it. If it is fixed only by a free constant (rate, switch-on
  scale, initial charge, coupling), the amount is "put in by hand".
- **C-ADIAB.** Isocurvature fraction beta_iso = S^2/(S^2 + zeta^2) <= 0.02 (S = cold-energy entropy perturbation, zeta = curvature),
  computed by separate-universe patches where the mechanism has a free switch-on.
- **C-COLD.** w <= 1e-2 at z = 3000 and negligible free streaming (comoving free-streaming length < 0.1 Mpc for M3; products at rest for M1;
  the inherited c_s^2 condition for M2).
- **C-PRESENT.** >= 99% of today's comoving cold amount in place by z = 1e5 (CFG288's seeding bound), AND the comoving amount changes by
  <= 1% between z = 3000 and z = 1100 (Planck's 1% on omega_c).
- **C-NEFF.** Extra early energy (as Delta N_eff equivalent at BBN, T ~ 1 MeV) <= 0.3.
- **C-LATE (M1).** Background vs the four DESI DR2 w0waCDM chains via CFG360/368's DECLARED, PROVISIONAL CPL projection (fit of ln E over
  0 <= z <= 2.5 at the observer's Omega_m; Gaussian (w0, wa); Omega_m shift ignored). Not excluded = not worse than LCDM by dchi2 > 4 on
  any SN chain. "REPRODUCES DESI" = improves on LCDM by >= 4 on all three SN chains (Pantheon+, Union3, DESY5) at a parameter value that
  ALSO passes C-PRESENT and C-NEFF. The interacting-vacuum (w0, wa)_eff and a0(z)/a0(0) at z = 1, 2, 2.5, 10 are reported.
- **C-GDOT (M2).** |Gdot/G| today <= 2e-13 per yr (lunar laser ranging, declared), with G_J proportional to A^-2 so Gdot/G = -2 d ln A/dt;
  BBN/CMB: |Delta ln A| since z = 1e9 <= 0.05 (declared).
- **C-PARTICLE.** State whether the mechanism forces a field quantum.

## 2. Verdicts (frozen order)

1. **EXCLUDED** (name the constraint) if no allowed parameter value passes every hard constraint.
2. **RESTATEMENT** if it passes the constraints but the amount maps one-to-one onto a free constant (put in by hand).
3. **VIABLE-CONDITIONAL** if the amount is fixed by the framework's own quantities but an auxiliary assumption is untested.
4. **VIABLE** if all constraints pass with the constant count stated and the amount is not put in by hand.
5. Bonus **PREDICTIVE** only if it fixes 5.364 (or omega_c) from something else AND, for any ratio/number match, the match survives the
   look-elsewhere and scrambled-cosmology tests below.

Per-mechanism specifics:
- M1: verdict on the best variant; S-t is scored on C-ADIAB separately. The question "does an exchange that produces the observed amount
  also reproduce DESI?" is answered YES only per the C-LATE definition.
- M2: the sourced tie is scored (C-AMOUNT with R_src = 5.364 at z = 1100, then C-PRESENT and C-GDOT); if the tie is EXCLUDED and only
  the free J_i remains, the mechanism is RESTATEMENT (CFG288 A2) with the tie EXCLUDED.
- M3: grammar m* = sqrt(rho_L^(1/4) M), M in {Mbar_Pl, M_Pl}; alpha in {1/137.036, 1/128, 0.0338 (alpha_W), 1/(4 pi), 0.118, 1};
  k in {1/4, 1/2, 1, 2}; g_dof in {1, 2, 4}: 144 forms. A hit = omega_c within 0.120 +- 0.001. Per-form base rate p = hits/144.
  Look-elsewhere: PREDICTIVE needs p < 0.01 AND the real-cosmology hit count above the 99th percentile of the scrambled draws.

## 3. Numerics (declared)
- M1: solve the exact ODE above from a_i to today; shoot rho_L for flatness at h = 0.674, omega_b = 0.02237, omega_r = 4.18e-5; a_i fixed by
  omega_c(a = 1e-3) = 0.120. Scan nu >= 0 (vacuum -> cold) on a log grid 1e-8 .. 0.1. Separate-universe isocurvature in pure radiation
  plus production, patches shifted by delta t (adiabatic), S compared at equal radiation density.
- M2: integrate the sourced field equation with an explicit P(X) = -rho_L + (M^4/2)(X/X0 - 1)^2 on a LCDM background; read rho_d,src/rho_b
  and Delta ln A; then the required beta phidot0 for R_src(z = 1100) = 5.364 and the implied drift and Gdot/G.
- M3: numerical Boltzmann equation for Y(x), x = m/T, with a declared coarse SM g*(T) table (g*s = g*), Omega h^2 = 2.744e8 (m/GeV) Y_inf.

## 4. Controls (main run must pass; exit 0)
- K1: M1 nu = 0 gives no cold energy and (w0, wa) = (-1, 0) to 1e-5.
- K2: M1 pure radiation, numerics vs the analytic x = rho_c/rho_r = 4 nu/(1-nu) ... closed form, to 1e-6 relative.
- K3: M2 numeric rho_d,src/rho_b vs Delta ln A to 1e-2 relative in the linear regime.
- K4: M3 Boltzmann: m = 100 GeV, <sigma v> = 2.2e-26 cm^3/s gives Omega h^2 in [0.10, 0.13].
- K5: the DESI Pantheon+ chain mean w0 within 0.01 of -0.838 (CFG368's printout).

## 5. MUTATE (CFG507_MUTATE=1; separate `_MUTATE` outputs; must flip)
- M1: the wrong sign (nu < 0, cold -> vacuum). It must FAIL C-AMOUNT (negative or zero produced cold energy) or C-LATE.
- M2: coupling removed (beta = 0): the sourced share must vanish (|R_src| < 1e-12).
- M3: the scrambled-cosmology false-positive test from CFG496: 200 draws R' uniform in [3, 8], omega_b and h fixed, flat; rho_L' from
  flatness; the same 144-form grammar scored against omega_c' = R' omega_b. Hits per draw reported; the real count is compared.
- MUTATE exit 0 only if the M1 wrong sign fails as required and the M2 identity control vanishes.

## 6. Expectations (hand, before machines; the scripts decide)
M1 RESTATEMENT (amount = nu / a_i; DESI-sized nu fails C-PRESENT; S-t variant EXCLUDED by isocurvature). M2 tie EXCLUDED by C-GDOT and
C-PRESENT; RESTATEMENT on the free J_i. M3 RESTATEMENT plus a forced particle; hits at the base rate. No PREDICTIVE result expected.

No dark-matter particle is assumed (M3 forces one and is labelled so). kappa = 1/2 fitted. The cold energy's mass is still required.
