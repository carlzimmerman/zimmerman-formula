# CFG507: where does the cold energy come from?

**Bottom line: the origin is still an input.** Three new origin mechanisms were tested, one from each of the owner's families. None fixes
the amount Omega_c/Omega_b = 5.364. Two pass the physical constraints only by putting the amount in through a free constant (RESTATEMENT).
The third route's attempt to tie the amount to the baryons is EXCLUDED. There is no PREDICTIVE result. The cold energy's mass is still
required, kappa = 1/2 is fitted, and nothing here closes the theory.

- Criteria: `FROZEN_CRITERIA.md`, committed alone first in cec378664.
- Script: `cfg507_origin.py`. Main run: 5/5 controls, exit 0, ~30 s. `CFG507_MUTATE=1`: 2/2, exit 0, ~3 min.
- Outputs: `.out`, `_MUTATE.out` and the matching `_results.json` files.
- Offline only: the on-disk DESI DR2 w0waCDM chains. Nothing was downloaded.

## 1. Routes already on the record (so nothing was repeated)

| route | status |
|---|---|
| Ghost-condensate dark sector (06-19): one scalar, one mode for MOND, one for a^-3 dust | housed, but the amount is FREE |
| L374: condensate dust through stream crossing | breaks at the first crossing; only a linear wave field passes |
| L319/L320: Lambda-triggered carrier | stopped by the owner |
| L49 D1: primordial black holes | pass clusters, fail the galaxy gate (x1.82) |
| CFG131: interacting vacuum vs the halo target | scoped NO-GO |
| CFG288: one field (wave field or shift charge) | a shared label only, amount FREE (A1: potential height >= 1.5e10 rho_L; A2: the charge is free). Seeding at z <= 1e4 EXCLUDED |
| CFG360 baryon tie | NO-GO: either a 5 GeV particle, or the free number moves into the asymmetry |
| CFG360-DE: late vacuum decay, khronon clock, condensate fraction, a0-rate production, transition tied to rho_L^(1/4) | PARTIAL, no mechanism. Late decay puts ~1e-17 in place by z = 3000; the tied transition fires at z ~ 8.5 |
| CFG362: stochastic misalignment during inflation | CONDITIONAL-TESTABLE (any B-mode detection kills it); the amount moves into H_I |
| CFG368: late cold <-> vacuum flow vs DESI (4 forms) | NOT SUPPORTED |
| Neutrino lane 10-06: m1 = rho_L^(1/4), sum 0.0613 eV | hot, so it is not the cold energy |
| CFG383/384: Bose condensate split / self-interaction | calibration / marginal |
| CFG365/CFG418: supply from the original baryons; R_c from KiDS | bookkeeping. R_c = 4.6-13 contains 5.364, but it rests on a free two-halo term; not an origin |
| CFG494: adiabatic initial conditions | give the amount (as an input), not the selection |
| CFG496: any cold-energy / dark-energy clue | 0/15; every mass-free link runs through a0 |
| PAPER42 (DOI 10.5281/zenodo.23172298): dark energy = the MOND field's zero-field energy | covers the vacuum half only |

The owner's three suggested families were already partly on the record:
- (a) as a late exchange (CFG360-DE, CFG368);
- (b) as an unsourced charge (the ghost-condensate thread, CFG288 road S);
- (c) as a transition at the rho_L^(1/4) scale (CFG360-DE) and as a potential with the rho_L height (CFG288 A1).

This lane therefore tested the variant of each family that had not been run.

## 2. Verdicts

| mechanism | verdict | why |
|---|---|---|
| **M1 (a): early running vacuum feeding cold energy.** rho_vac = rho_L + nu 3H^2/8piG; the energy the vacuum loses goes into cold energy at rest | **RESTATEMENT** | Passes every hard constraint for nu <= 3e-5 (grid), with a switch-on at T_i <~ 4 keV (z_i >~ 2.4e7). But the amount equals nu/a_i: two free constants for one number. Does an exchange that makes the amount also reproduce DESI? **No.** The DESI direction appears only at nu ~ 0.01 (w0 -0.94, wa -0.41; dchi2 +4.2 / +2.9 / +4.1 on PP / U3 / DY5, so Union3 still falls short). At that nu the cold energy only appears at z ~ 6e4 and drifts 6.5% between z = 3000 and 1100, which fails C-PRESENT. |
| **M2 (b): the MOND field's dust charge, sourced by baryons** (the conformal coupling AQUAL/TeVeS use) | **RESTATEMENT; the baryon tie is EXCLUDED** | An identity was verified numerically to 3e-5: the sourced share rho_d,src/rho_b equals Delta ln A, the change of every particle mass since the source switched on. Setting the share to 5.364 at recombination needs a G-variation of 2.9e-5 per yr (x1.5e8 over the LLR bound) and a comoving drift of +4.7 between z = 3000 and 1100. Setting it to 5.364 today still violates the G bound x3.9e3, and the cold energy would then be missing at recombination. The G-variation bound caps the sourced share at 2.6e-4 of 5.364. What remains is the free initial charge (CFG288 A2). |
| **M3 (c): dark-energy seesaw relic.** m* = sqrt(rho_L^(1/4) Mbar_Pl) = 2.34 TeV, thermal freeze-out. **Forces a particle.** | **RESTATEMENT (+ a forced particle); NOT PREDICTIVE** | It passes cold, present, N_eff and adiabatic as a standard WIMP (free-streaming 1e-6 Mpc). Omega h^2 scales as m*^2/(k alpha^2), so the amount is set by the chosen coupling. Across the 144 forms, Omega h^2 spans 2.5e-4 to 112. One form lands in the window: alpha_s, k = 1/4, g = 4, giving 0.1192. In 200 scrambled cosmologies, 34.5% of draws also get a hit (99th percentile = 1), so the hit is the base rate, not a tie. |

### M1 details

- **Isocurvature.** A switch keyed to the local temperature or to proper time is exactly adiabatic. Isocurvature appears only if the trigger
  is a clock with its own fluctuation, and then it needs |dtau/t_i| <= 0.29 zeta.
  - This corrects the frozen hand expectation that a global-time switch would be EXCLUDED.
- **a0 consequence.** a0(z) = kappa c sqrt(G rho_vac(z)) rises into the past: +0.02% at z = 2 and +0.9% at z = 10 for nu = 3e-5.
  - That is the opposite sign to the DESI-tracking decline (~0.86 at z = 2), so this exchange does not produce the a0(z) that evolving
    dark energy implies.
- **MUTATE (wrong sign, cold -> vacuum).** No nu < 0 reaches the amount (0 of 7), as required.

## 3. Disclosures

- **The M3 grammar rule is weak.** The frozen per-form rule p < 0.01 is met by any single hit among 144 forms. The scrambled-cosmology leg is
  the one that decides.
- **The M3 hit is inside the solver's precision.** The Boltzmann solver uses a coarse g* table and drops the d ln g*/d ln T term. Its
  systematics are a few percent, larger than the 0.8% window, so the one hit is not robust in either direction.
- **No dark-matter detection data was used** for M3, so direct and indirect detection limits are untested.
- **M1 runs on assumptions.** Its DESI comparison uses the provisional CPL projection from CFG360/368 (the Omega_m shift is ignored). The
  vacuum perturbations of the nu H^2 term are not modelled.
- **M2 inherits two record results without re-running them:** the extra scale M (CFG288 road S) and the breakdown at stream crossing (L374).
