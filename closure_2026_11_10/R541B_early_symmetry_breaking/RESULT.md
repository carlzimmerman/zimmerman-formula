# R541B RESULT: an early potential V(tau) on the clock moves 5.41 into V's height; it does not fix it. TRADES / TRADES (canonical / alt)

Criteria: FROZEN_CRITERIA.md, commit c5bfd563ed (committed alone, before any script or number). No amendment.
TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. kappa = 1/2 FITTED; not theory closed.
Footings never pooled. Cold dark energy is a field component; no particle was added.

## Label: TRADES / TRADES

- **FIXES fails.** No V built only from rho_DE, a0, mu_K, G and c gives R = 5.41 and passes the gates (family (d), below).
- **R can be reproduced, but only by fitting.** Families (a) exponential, (b) smooth step and (c) power law with n >= 3
  reach R = 5.410 / 5.412 and pass GB2, GB3 and GB5. GB3 passes only for an anchored clock. Each needs:
  - **two new constants, V0 and tau_s** (three for (b) and (c): Delta or n). One combination, about V0 tau_s^(3/2), is
    fitted to R. tau_s is only bounded: it must be in place by z of about 3e5 (GB2a), and it must switch off late enough
    that the made charge is dust, not stiff (z_s below about 4e5 at the CMB Jeans line for mu_K; below about 1e7 at the
    BBN line);
  - **two initial conditions:** no charge before V acts (C_i = 0), and a clock synchronised with the adiabatic time to
    6e-6 to 9e-6 of tau_s (GB3).
- **This is a net loss.** One fitted number (5.41) becomes one fitted combination, plus one or two new constants and two
  initial-condition requirements.
- **The mechanism in one line.** Energy conservation puts V's height at switch-off into the charge: R = V0 a_s^3 / rho_b0.
  So V0 must equal 5.41 times the baryon density at switch-off. The number has moved into V0; it is not explained.

## How the charge is made (KA1, sympy, `kA_charge_equation.out`)

Add -sqrt(-g) V(tau) to action (A). In the expanding background with P = 0:
- The charge equation is dC/dt = -N a^3 V'(tau). Residual against the direct Euler-Lagrange variation: 0. Covariantly this
  is div J = -V', J^m = n^m mu_K^2 (Q - 1)/K: coefficient 1, the same form as AC2q's line in PAPER70.
- A falling V (V' < 0) makes positive charge. A rising V makes negative charge (MU1).
- Energy is conserved on shell (residual 0): d(a^3 (rho_K + V))/dt + (p_K - V) d(a^3)/dt = 0. A decaying potential on
  the clock is a decaying vacuum dumped into the clock's dust.
- While Q stays near 1, integrating by parts gives C = integral of V d(a^3). That yields the step and exponential
  results below (KA3, KA4).
- **Stiff limit (new).** If K V / mu_K^2 is not small, the energy goes into the clock's kinetic term (Q much greater
  than 1, w near 1), which redshifts away as a^-6.
  - Then R cannot be reached with V below the radiation density: at the Jeans line, z_s 1e6 gives at most R = 0.34 with
    V0 already 0.54 of the radiation; at the BBN line, z_s 1e8 gives at most 0.033.
  - This is MK1's dust-onset redshift (1 + z = (4 mu_K^2 / I0)^(1/3)) acting as an upper limit on the switch-off.

## Gate table (canonical; alt within 0.2 % wherever both were run)

| gate | number | verdict |
|---|---|---|
| **GB1 background** | (a) R = Gamma(5/2) V0 a(tau_s)^3 / rho_b0 in the dust regime. d ln R / d ln V0 = 1.00-1.01 and d ln R / d ln tau_s = 1.50-1.53 (radiation: a^3 ~ t^(3/2)); 0.75 at the Jeans line, z_s 3e5, where the stiff part begins. (b) R within 3 % of V0 a_s^3 / rho_b0 for Delta / tau_s <= 0.3. (c) d ln R / d ln n = -2.2 to -6.6. Initial charge adds straight on: C_i / rho_b0 = 1 and 5.41 give R = 6.41 and 10.81 (Delta R +1.00, +5.40). Clock offset tau_i / tau_s = -0.1 / +0.1 gives R = 5.98 / 4.89 | **NO ATTRACTOR**: every frozen threshold exceeded by a factor of 10 to 80. Constants: 2 (a), 3 (b, c); 1 combination fitted |
| GB1 (d) zero new constants | p = q = 0 (no free number at all): R from 0.019 to 21.7 (exponential); 0 (step: it switches off in the future). Every one makes its charge now: at most 2.8e-16 of it exists by z 3000. Nearest to target: R 6.03 (beta 4 pi, T = c / a0, exponential; canonical) and 5.86 (beta 4, T = 1/sqrt(G rho_DE); alt). The other 324 forms per footing need a chosen mu_K. In 41 per footing some mu_K gives R, and every such mu_K is <= 6e2 per Mpc (Jeans line 2.512e4) with the switch at z <= ~1e4: none passes. Two families checked with the full ODE: p = 3/2, q = 1 gives R independent of mu_K, R = 0.2417 beta / 0.3213 beta (step / exponential; alt 0.2660 / 0.3536). Hitting 5.41 would need beta = 22.4 / 16.8, and no beta in the grammar comes within 10 widths (best: 8 pi step, 6.08 to 6.11, 10.3 to 10.8 widths). p = 2, q = 1 (the K term's own scale) gives R >= 414 at every mu_K at or above the Jeans line | **no FIXES**. The p = q = 0 near hits are EXCLUDED by GB2a by about 1e15 |
| **GB2a in place** (99 % by z 1e5; z50 <= 1e4 excluded, CFG288) | (a) z_s 3e5: z99 = 1.13e5 / 1.08e5 (Jeans / BBN): PASS. z_s 1e6 at the BBN line: z99 3.63e5: PASS (both footings). z_s 1e5: z99 3.6e4, undecided. z_s 1e4: z50 6.3e3, EXCLUDED. (b) z_s 1e6 at the BBN line: PASS. (c) n = 3, 4 at the BBN line: PASS; n = 1, 1.5: EXCLUDED | PASS for parameters that exist |
| GB2b cold (\|w\| <= 0.01 to z 3400, V counted) | max \|w\| 5e-12 to 6e-7 at the passing points. 1.6e-2 at z_s 1e4 (fails). 0.70 / 0.43 for power law n = 1 / 1.5 | PASS |
| GB2c BBN ((rho_K + V) / rho_rad <= 0.067 at 1 MeV; PROVISIONAL) | <= 7e-16 at every point computed. V0 / rho_rad at switch-off is 8e-4 to 8e-3 | PASS by about 1e14 |
| **GB3 isocurvature** (\|S\| <= 9e-6; INDICATIVE) | d ln C / d(tau_i / tau_s) = -1.00 (exponential), -1.50 (step, power law) in the dust regime, so the clock must agree with the adiabatic time to \|delta tau_rel\| <= 6.0e-6 to 9.0e-6 tau_s. An offset is not damped before generation: its ratio at the 50 % point is 1.000-1.007 in the dust regime, since (A) has no restoring force on the clock's phase. Crude inflationary estimate with c_s = 1: H_inf <= 6e12 to 4e16 GeV depending on mu_K and z_s. (A) has c_s = 0 at Q = 1, so this vacuum estimate is not well defined | **PASS only with an anchored clock** (frozen rule); counted as an extra initial condition |
| **GB4 coincidence** | MU3: omega_b x 2 at fixed V gives R 5.410 -> 2.706 (ratio 0.5002). Nothing in V knows about baryons | **UNTIED**: the nearness of 5.41 to 1 stays unexplained |
| **GB5 late safety** (\|Delta C/C\| <= 1 % after z 3000; \|V'(t0)\| <= 1e-2 H0 rho_d0; V <= 0.02 rho_DE for z <= 5) | (a), (b): Delta C/C = 0 to double precision, V(t0) = 0. (c) n = 3: 1.3e-5 (Jeans), 2.4e-7 (BBN); n = 4: <= 9e-9. n = 2: 2.5e-2 to 6.0e-2 (fails); n = 1, 1.5: 0.95-1.0 (fail) | PASS for (a), (b), (c) n >= 3 |

## Known answers and mutations (all pass / all bite)

- KA1 charge equation, symbolic: residual 0; with V = 0, C is conserved; energy conservation residual 0.
- KA2 V = 0: C(1) / C_i - 1 = 0.
- KA3 sharp step (pure radiation): C / (V0 a_s^3) - 1 = 2.7e-4 (line 1e-3).
- KA4 exponential (pure radiation): C / (Gamma(5/2) V0 a(tau_s)^3) - 1 = 5.7e-4 (line 1e-3).
- KA5 energy conservation along a numerical solution: 1.9e-9 (line 1e-6).
- KA6 radiation clock: tau / (1/(2H)) - 1 = 7.7e-11.
- KA7 isocurvature, sharp step: d ln C from a +1e-3 t_s offset is -1.50054e-3 against the analytic -1.5e-3 (ratio
  1.0004; line 2 %).
- Mutations, each bites:
  - MU1 rising V: R = -5.42. At the Jeans line the negative charge drives Q through 0 and the integration ends: the
    clock's foliation ends there.
  - MU2 switch at z 1e3: z50 = 444, GB2a EXCLUDED.
  - MU3 omega_b x 2: R halves.
  - MU4 power law n = 1: Delta C / C after z 3000 = 1.0, GB5 FAIL.
  - MU5 offset 1e-3 tau_s: \|S\| about 1e-3, GB3 FAIL.

## What is new relative to the record

- CFG360-DE C1 drained rho_Lambda late; C2 put a separate field's minimum on the clock. Here the potential acts on the
  clock itself, inside (A), and the made quantity is (A)'s own charge.
- The exact law dC/dt = -a^3 V'(tau) and the step result R = V0 a_s^3 / rho_b0 are new.
- So is the stiff limit: generation before MK1's dust-onset redshift goes into a^-6 kinetic energy, not dust.
- The (d) family shows something the record had not stated. A vacuum of order rho_DE decaying over the dark-energy time
  makes dust of order rho_DE today (R of 0.02 to 22). That is the known late coincidence (cold over dark energy 0.389),
  made at the wrong time by about 1e15 in the made fraction.

## What was not checked, and known weaknesses

- **Background only.** The CMB was not run in Boltzmann; GB2a uses CFG288's sudden-conversion lines. Points between
  z 1e4 and 1e5 stay undecided, and every passing point has z99 >= 1.08e5, close to that edge for z_s 3e5.
- **GB3** rests on a bound fitted inside the standard model (indicative). The clock's own primordial fluctuation cannot
  be computed in the framework: there is no early-universe sector, and c_s = 0 at Q = 1. The pass is conditional on an
  anchored clock.
- **Perturbations while V is on** were treated only on scales outside the horizon (separate universes). Modes inside
  the horizon during the V phase, V''-driven growth, and the P sector and stiffness during that phase were not
  analysed (the background has P = 0).
- **The BBN line** (Delta N_eff <= 0.5) is from memory, PROVISIONAL. The margin is about 1e14.
- **The (d) grammar is finite**, and the subset re-run with the full ODE (p = 3/2 and p = 2 with q = 1) was chosen after
  reading the quadrature output. A continuous beta would hit 5.41 by construction (beta = 22.4 / 16.8), so a hit would
  be a choice, not a derivation.
- The quadrature in `gbd_zero_constant.py` keeps the cold share in the background at all times. This is inconsistent
  for late-conversion forms, but they fail by about 1e15.
- In its "closest" line, `gbd_zero_constant.out` prints "factor X short"; X is target / R, so a value below 1 means R
  is above target.
- mu_K has no value in the record. Results are given at its two record lines only (2.512e4 and 8.89e6 per Mpc).
- A pre-result run of `gb_background.py` used Q^2 - 1 for rho_K, which cancels to zero at late times. It was fixed
  (rho_K = (C/a^3)(1 + x/2)) and everything was re-run before any number was graded. Only the corrected outputs are
  committed.

## Files

`FROZEN_CRITERIA.md`, `r541b_core.py`, `kA_charge_equation.py/.out`, `gb_background.py` with
`gb_background_{ka,a,b,c,mu}.out` (run as `python3 gb_background.py <part>`), `gb3_isocurvature.py/.out`,
`gbd_zero_constant.py/.out`, `gbd_ode_check.py` with `gbd_ode_check_{P,S}.out`.
