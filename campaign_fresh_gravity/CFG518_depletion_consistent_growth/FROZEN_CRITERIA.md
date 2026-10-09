# CFG518 FROZEN CRITERIA: does structure growth still pass when the PM uses the depletion-consistent (census) placement of cold energy?

Committed alone, before any engine change is run. This is the run CFG515's README specifies ("The essential run").

## Question

CFG424/425 passed growth (16/16 with CFG426/427) with f_ret = 1: the phantom is sourced by all PM baryons and the edge is r_M(M_b)/ln(1/(1 - f_b)). CFG515 found that real galaxies need the census f_ret (about 0.1 of baryons kept), with the edge r_M(M_now)/ln(1 + f_ret f_b/(1 - f_b)), 2.2-3.5x farther out. CFG515 showed the settled AMOUNT per halo is the same (identity) but the PLACEMENT is not. Does growth still pass with the placement that is consistent with depletion?

## Engine (cfg518_pm.py = CFG424's cfg424_pm.py copied, RC = 0 mode; changes listed in full)

1. **Census f_ret per host.** f_ret(host) = CFG416's declared `fret_of(log10 M_ta [Msun/h])`, copied verbatim (0.10 below 10^12.5; ramp to 0.55 at 10^13.5; then +0.30/dex, capped at 0.90). M_ta is the host's own turnaround mass in the PM, (4 pi/3) r_ON^3 Delta_ta(z) rho_m (the same expression CFG416/423/424 already use inside x_supply), so no self-consistent solve is needed. It is applied at every step with the current M_ta(z) and Delta_ta(z), as CFG416's x_supply did.
2. **f_ret field.** Each resolved host (the CFG424 peak finder, unchanged) paints f_ret(host) over its turnaround ball (x = 1, the same balls whose union is the CFG424 catchment). Overlaps: the largest host wins (painted in increasing r_ON). Outside every catchment f_ret = 1 (no host; nothing has been expelled there; the switch is zero there anyway). Recomputed when the catchment is (every 10 force calls, and at each snapshot), as in CFG424.
3. **Phantom source = retained baryons only.** The MOND input field is g_b,ret = f_b x (filtered) gradient of the potential of f_ret(x)(1 + delta) (k = 0 dropped, as for g_b). The phantom is s_ph = -div[(nu(|g_b,ret|/a0) - 1) g_b,ret]. MIX-A filter, T1 switch eps = 0.077, nu_mono, unchanged.
4. **Expelled baryons (declared choice).** The PM baryons are not removed or moved: all matter still gravitates through the Newtonian potential of the full delta, exactly as in CFG424. Only the phantom (MOND) source uses the retained fraction f_ret. The expelled share (1 - f_ret) stays as mass where the particles are; it is not redistributed. This is the simplest consistent choice; it is a declared bookkeeping, not modelled outflow.
5. **Census edge.** The phantom excess is confined to balls of radius r_edge = r_M(M_b,now)/ln(1 + f_ret f_b/(1 - f_b)), M_b,now = f_ret f_b M_ta / h, r_M = sqrt(G M_b,now/a0), capped at r_ON (x <= 1), i.e. CFG423/424's x_supply with f_ret = fret_of(M_ta) instead of the constant 1 (the same edge CFG515 used).
6. **Excess and compensation (unchanged).** e = f_sw max(s_ph - s_c, 0) inside the edge balls; s_c = the cosmic cold share 1.5 Om (1 - f_b)(1 + delta)/a, unchanged (all cold energy is present in the PM). Per-catchment mass conservation: comp = s_c (Sum_C e / Sum_C s_c); source added = e - comp.
7. **Cap on available cold energy.** On a catchment with q = Sum_C e / Sum_C s_c > 1 (more phantom excess than cold energy available), e is scaled by 1/q there, so the drawn-down cold energy never exceeds what the catchment holds. This cap was never active in CFG424 (overdraw 0); in f_ret = 1 mode it is inert unless overdraw occurs. Reported: q_max before the cap, the overdraw mass fraction (catchments with q > 1, before the cap), and whether the cap acted.

Everything else is CFG424's: Lambda-CDM background, EH initial conditions at z_i = 49 (the only Lambda-CDM input), 200 Mpc/h box, step grid, seed 359, NSEED 256 at 256^3 and 512 at 512^3, kappa = 1/2 FITTED in a0 (footings 9.3603e-11 canonical / 1.1312e-10 alt, never pooled), FLAT a0.

## Runs (256^3, seed 359, 4 threads each, nice 10, detached; logs in ../_external_data/cfg518_work/)

- **DC-can:** census, canonical footing.
- **DC-alt:** census, alt footing.
- **MUTATE:** census, canonical, compensation switched off (e added, no cold energy drawn down; as CFG424's MUTATE). It must NOT be GROWTH OK.
- **K1 (engine control):** f_ret = 1 everywhere through the new code path, canonical. It must reproduce CFG424 TA-can (sigma8 ratio 1.0033, max|P - 1| 0.027) to |delta max|P-1|| <= 0.002 and |delta sigma8 ratio| <= 0.001. If K1 fails, the engine change is broken and the lane is INVALID (no growth verdict).

## Growth cuts (CFG361, unchanged), vs CFG359 S0 N256 (cfg359_S0_FLAT_canonical_N256.json)

Over k <= 1 h/Mpc at z = 0: GROWTH OK if |sigma8 ratio - 1| <= 0.05 and max|P/P_S0 - 1| <= 0.10; FAIL if |sigma8 ratio - 1| > 0.2; otherwise TENSION.

## Decision

- **PASS (256^3):** DC-can and DC-alt both GROWTH OK, MUTATE not GROWTH OK, K1 passes.
- **PARTIAL:** exactly one footing GROWTH OK.
- **FAIL:** neither footing GROWTH OK.
- **INCONCLUSIVE:** MUTATE is GROWTH OK (confinement alone would do it).
- **INVALID:** K1 fails.
- **512^3 (only if 256^3 PASS, and only when no other 512^3 job runs and CFG506 is not loading 512^3 snapshots):** DC-can at 512^3, seed 359, NSEED 512, 8 threads, vs CFG411's 512^3 S0 (cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json). **CONFIRMED** if it is GROWTH OK; **NOT CONFIRMED** if it is not. If 512^3 cannot be run in the session, the lane stays PASS (256^3) with 512^3 PENDING.

## Reported (not gating)

q_max, overdraw, cap activity; the mass-weighted mean f_ret in catchments; the total phantom excess Sum e relative to K1 (f_ret = 1); sigma8 ratio and P/P_S0 at k = 0.1/0.3/1. Comparison with the CFG515 argued bracket (0.027 to 0.08-0.10) is reported, not scored.

## Caveats (declared before running)

- The PM hosts are group-scale (r_ON >= 1.56 Mpc/h, M_ta >~ 10^12.9 Msun/h at z = 0), where the census f_ret is 0.28-0.90, not the 0.10 of KiDS lenses and the MW. The run tests the placement the census implies for the hosts the PM resolves.
- The expelled baryons stay as gravitating mass where they are; no outflow is modelled.
- The cold energy is bookkeeping, not moved particle by particle.
- kappa is fitted; f_b and rho_Lambda are not derived; the cold energy MASS is still required. A pass is not "theory closed".
