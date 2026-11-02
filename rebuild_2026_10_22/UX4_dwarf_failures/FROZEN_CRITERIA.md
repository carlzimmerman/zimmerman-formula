# UX4_dwarf_failures: frozen criteria (committed alone, before any script or number of this lane)

Owner's go, 2026-11-02. **Question:** are the law's Local Group and IC 1613 failures physics or data?
kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10: both reported, never pooled. Not a reinstatement of anything; cold sector stays retired. Not theory closed.

## Not blind
Read before freezing: LW1 README + `lw1_dwarfs.py/.out` (E1, plain, E2 class medians), RF2 README + ledger, IN1 README, RT1 README + start of script, OP1 README, Z2 README + ledger (clean-subset +0.693, slopes -0.05, -0.76, member-count split +0.24 to +0.44), FG1's Dw rows, the headers of CFG29/46/51. I know from these that the failures are large and that Z2 implicated no tide. No UX4 number exists yet. Walker per-star data and LVD gas/rotation columns not yet read for values.

## Baseline
LW1's E1: `E = log10(g_obs/g_N) - logG(y, x_e)`, D10 solver, grid (24,16), X1's rows, Arroyo-Polonio b, Z2's host field E_mid, class median, bootstrap + `sdMC` Z exactly as LW1's `grade()`. Classes: MW ultra-faint, bright M31, M31 others (the three failures); MW classical, LG field (reported).
Share of a variant in a class: `(E_base - E_variant)/E_base`. Negative means it makes the miss worse.
Labels per variant and class: **CARRIES** share >= 1 or |Z| < 2 after it; **PARTIAL** 0.25 <= share < 1; **MINOR** |share| < 0.25; **WORSENS** share <= -0.25; **NOT COMPUTABLE** with the missing file named.
Every systematic has a CENTRAL value and a CEILING, both set here. Nothing is fitted to close a gap; required values are reported only as what would be needed.

## Satellite systematics
**B binaries.**
- B0: b = 1 (no correction), showing what the baseline has already removed.
- B1: Arroyo-Polonio f = 0.7 ratios in place of free f; median ratio for unmatched M_V > -7.7.
- B2: own forward mock. Single epoch; true sigma = the law's prediction for that system (E1); members N = Geha N_stars if matched else X1-style N_eff = (sigma/dsigma)^2/2, floor 4; error per star 2.2 km/s (declared); ML Gaussian sigma with no clipping (generous to binaries). Population: log P normal 5.03, 2.28 days (literature, PROVISIONAL, from memory); q flat 0.1-1; e flat 0-0.9; random orientation and phase; primary 0.8 Msun. Central: f 0.5, RGB primary, periastron > 2 x 10 Rsun. Ceiling: f 1.0, periastron > 2 x 1 Rsun. 400 mocks of the whole class. Reported: mock class median E against the b = 1 data, P(mock >= data), and share of E(b = 1).
- B3: Walker multi-epoch cleaned sigma (CFG51 reduction) for the systems it covers; paired change.
- B4: Geha DEIMOS sigma where lower (matched systems); paired change.

**T tides, non-equilibrium.**
- T1: Z2's clean cuts carried onto E1: q_MOND < 0.5; ellipticity < 0.5; both, plus N >= 10. MW only; M31 has no PMs, labelled so.
- T2: exposed q >= 1 against safe q < 0.5 on E1; partial slope of E1 on logT_peri at fixed M_V.
- T3: impulse heating, computed. Host law field gradient Gamma at pericentre; passage time p/V; `dsigma^2 = (Gamma r12 p/V)^2/3` per passage, no adiabatic damping and all heat retained (generous). Passages = 10 Gyr / orbital period. p = Z2's r_peri where PM exists, else d_host/3 central, d_host/5 ceiling. V = sqrt(2) V_c central, V_c ceiling. Variant: sigma^2 - dsigma^2, floored at 1 % of sigma^2.

**M membership.**
- M1: Walker per-star: delete the 1 and 2 most deviant members per system, ML sigma; paired change.
- M2: Gaussian truncation: remove the most extreme 5 % (central), 20 % (ceiling) of each system's stars; truncated-normal sigma ratio. Report the fraction required to close.
- M3: selection: X1 drops systems with only upper limits. Add them, censored, Kaplan-Meier median, class by the same M_V and host rule.
- M4: N >= 10 only.

**L stellar M/L.** E re-solved at Upsilon_V factors of the baseline's 2: 0.5, 1, 1.5, 2 (Upsilon 4, the record's W), 4, 8, 16, 32, 64, x_e held. Central 1 (the baseline), ceiling Upsilon_V 4; 0.5 reported too. Required Upsilon per class by interpolation, reported, not adopted.

**R estimator.** Solver field unchanged, prediction changed:
- R1: predicted global virial sigma^2 instead of Wolf.
- R2: constant beta +0.5, -0.5, apertures R < R_h and R < 2 R_h, luminosity weighted; numerically projected Plummer; beta 0 as the control.
- R3: Walker (2.5 sigma^2 R_e/G at R_e) and Errani (3.5 x 1.8 R_h sigma^2/G at 1.8 R_h) against the solver's g at that radius.
- R4: circularised radius R_h sqrt(1 - ell) if LVD's rhalf is major axis; re-solved. Central for this term is R4 itself. Ceiling for R is the most favourable of R1-R4 per class.

## Stack and closure
**CENTRAL stack:** B2 central, T3 central, M2 5 %, Upsilon 2, R4. **CEILING stack:** B2 ceiling, T3 ceiling, M2 20 %, Upsilon 4, best R. Sigma terms combine by subtraction in sigma^2 after the mock's inflation; systems floored as in T3. Stacks aren't independent or likely; the ceiling is an upper limit.

**Satellite verdict, both footings separately:**
- **CLOSED BY COMPUTED EFFECT:** central stack, or one central term, gives |Z| < 2 for all three failing classes.
- **CEILING ONLY:** only a ceiling does.
- **FAILURES STAND:** the ceiling stack leaves any failing class at |Z| >= 2.
Reported per class as well.

## Environment
Sample: X1's rows with a host-field value, satellites (all MW, M31 classes) against LG field. OLS with bootstrap over systems; residual E0 (isolated) and E1, separately.
- A: raw satellite minus field.
- B: + M_V; C: + log y; D: restricted to the overlap in M_V, 1:1 nearest matches.
- F: reproduce the slope on log x_e at fixed M_V (record -0.05 +- 0.19; AQUAL's -0.76), per class of host.
- G: field dwarfs' gas added to M_b and rotation to g_obs where LVD has the columns, since the field class's pass was on stars alone.

Labels (on E0, which contains no environment term):
- **ENVIRONMENT:** satellite coefficient > 2 sigma positive under both B and C.
- **LUMINOSITY OR ACCELERATION:** raw difference >= 2 sigma, and |coefficient| < 2 sigma under B or C.
- **NOT SEPARATED:** coefficient's sd > 0.3 dex, or fewer than 5 matched field systems.
- **NO RAW DIFFERENCE:** otherwise.
A flat data trend with an EFE prediction falling is reported as such, not as a detected environment.

## IC 1613
Base RT1: E -0.593, HI V 16.9 at 2.71 kpc, i 48, M_star 2.88e7, M_gas 5.93e7, sigma_E 0.075. Each term, both footings, with share as above:
- I1 inclination: RF2 medians 34.4 and 37.9 central; RF2's 16th percentile 24.5 ceiling; required i reported.
- I2 pressure support: V_c^2 = V^2 + sigma_HI^2 R/R_d-type term; check whether Oh+15's V already includes it, and if so say so and don't double count. sigma_HI 9 km/s central, 12 ceiling unless the tex gives one; scale from Oh+15's table or RF2.
- I3 baryon geometry: enclosed exponential discs and thin-disc g_N at R_max, against RT1's all-inside point mass. Central scale from on-disk values; ceiling gas scale = R_max.
- I4 external field: Z2-type x_e for IC 1613, solver.
- I5 baryon mass: M_star 0 lower bound; gas as tabulated.
- I6 distance +-10 %.
- I7 velocity error 15 %: changes Z only.
- I8 stacks: central (I1 at 37.9, I2, I3, I4), ceiling (I1 at 24.5, all ceilings).
Labels as satellites; stellar sigma tracer E reported alongside from IN1's formula. IN1's falsifier isn't changed. This lane may say that a term falls inside RF2's allowed range; it may not move RF2's class.

## Checks
K1 E1 and plain reproduce `lw1_dwarfs.json` to 1e-6. K2 factor-1 re-solve equals E1 exactly. K3 mock with f = 0 returns input sigma within 3 % at N = 1000. K4 mock orbit rms against a Kepler analytic case within 3 %. K5 beta 0, wide aperture against solver's `vir`, 1 %. K6 IC 1613 base reproduces -0.5928; K7 Z2's slope reproduced to 0.02. K8 Walker reduction reproduces CFG51's stored Bootes I sigma. Failed checks reported, not hidden.
**MUTATE twin (must fail):** M_star x 10 before E; K1, K2, K6 fail, exit 1, separate outputs. Rerun must be byte-identical.

## Limits declared
Binary population is solar-neighbourhood. Mock N is partly a proxy. T3 is impulsive only. M31 systems have no PMs or per-star data on disk. No downloads: if needed, a file is named instead. Compute one thread, nice 15, under 4 GB, cached and resumable.
