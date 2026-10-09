# CFG524 FROZEN CRITERIA: draw the compensation only from the UNSETTLED cold-energy reservoir ("settling" done literally)

Committed alone, before any run.

## Question

CFG521 found a small-scale power deficit once halo interiors are resolved (256^3, matched S0): P/P_S0 = 0.63 at k = 4 (L = 50) and 0.44 at k = 8 (L = 25), growing with time and deepening with resolution (k ~ 4: 0.89 L200, 0.80 L100, 0.63 L50, 0.59 L25). K1 (f_ret = 1) shares it; no compensation (NOCOMP) does not. Diagnosis: CFG424's per-catchment compensation comp = q s_c draws the paid-for cold energy in proportion to the local cold density s_c, i.e. mostly from dense halo cores, including cold energy that has already settled there, while the phantom excess e sits in the outskirts; hosts de-concentrate.

The fix tested here, with no new parameter: settled cold energy is never drawn back. The draw that pays for the phantom excess comes only from the unsettled reservoir in that catchment.

## How the engine represents cold energy and phantom (read from cfg521_pm.py, identical to cfg518_pm.py physics)

- There is no separate cold component. The PM particles carry all matter; delta is the total-matter overdensity. The cold-energy density is the fixed (1 - f_b) share of it, in code source units (lap phi = source): **s_c = 1.5 Om (1 - f_b)(1 + delta)/a** (engine line `s_c = (1.5 * Om * (1.0 - FB) / a) * (1.0 + delta)`).
- The phantom source is **s_ph = -div[(nu - 1) g_b,ret]**, from the retained baryons f_ret(x)(1 + delta) through the MIX-A filter (CFG518).
- The engine's switch weight at that step is **f_sw** = clip(0.5 + (l2 - tau)/(2 eps), 0, 1) times the census-edge mask (refreshed every 10 force calls, as in CFG424/518).
- The engine's RES/T5 reading splits the switched-on phantom f_sw s_ph into two parts: the part the local cold share already carries, and the excess **e = f_sw max(s_ph - s_c, 0)** (inside catchments; capped), which is the only phantom added as an extra source. So the phantom "already assigned" and carried by the cold share in a cell is f_sw x min(s_ph, s_c) (and zero where s_ph < 0). The two parts add back to f_sw max(s_ph, 0).

## The reservoir (definition)

Per cell, at every force call, with the same s_c, s_ph and f_sw the engine uses at that step:

- **settled S = f_sw * clip(s_ph, 0, s_c)**
- **reservoir Rv = s_c - S** (so 0 <= Rv <= s_c).

Per catchment C (CFG424 turnaround-ball components, unchanged): E_C = Sum_C e, R_C = Sum_C Rv, q = E_C / R_C. If q > 1, the existing cap applies unchanged in form: e -> e/q in that catchment and q -> 1 (the whole reservoir is drawn, never more). Draw **comp = q Rv**; source added = e - comp, so Sum_C (e - comp) = 0 (per-catchment mass conservation unchanged). The only change from CFG521 is Rv in place of s_c in the two places s_c enters the draw (the denominator of q and the draw weight).

### Choices, and whether each is forced

1. **Cold density = s_c (the fixed f_b split of the PM matter field).** Forced: the engine has no other cold field.
2. **Settled = the phantom already carried by the cold share, min(s_ph, s_c).** Forced by the engine's own excess definition e = f_sw max(s_ph - s_c, 0): what is not excess is carried by the local cold share.
3. **Lower clip at 0 (s_ph < 0 settles nothing).** Forced: a negative phantom source is not settled cold energy, and without the clip Rv > s_c (a reservoir larger than the cold energy present).
4. **Upper clip at s_c.** Forced: the settled amount cannot exceed the cold energy in the cell; the remainder is e, paid by the draw.
5. **Evaluated at the same step, with the same f_sw/mask refresh as e.** Forced (the same arrays).
6. **Switch weight on the settled part: f_sw (R2) or none (R1).** NOT fully forced. R2 is the literal reading ("phantom assigned by the engine": outside the switch the engine assigns no phantom, and f_sw weighting the settled part makes settled + excess = f_sw max(s_ph, 0)). R1 = clip(s_ph, 0, s_c) everywhere in the catchment (the cold share settles into the phantom profile whether or not the switch is on). **Both are run and each gets its own verdict; no picking.**
   - **R2 (literal):** S = f_sw clip(s_ph, 0, s_c).
   - **R1 (switch-free):** S = clip(s_ph, 0, s_c).

## Engine (cfg524_pm.py = cfg521_pm.py copied; changes listed in full)

1. Draw rule from the environment CFG524_DRAW = `R2` (default) | `R1` | `SC`. `SC` is the old core-weighted draw comp = q s_c, i.e. cfg521_pm.py exactly (the MUTATE control).
2. Diagnostics only (no effect on the dynamics): reservoir fraction Sum_catch Rv / Sum_catch s_c; number and mass fraction of catchments with q > 1 (cap use), fraction of Sum e removed by the cap; the draw-weighted mean density Sum comp (1 + delta) / Sum comp versus the s_c-weighted mean (how core-weighted the draw is).
3. Bookkeeping: environment names CFG524_*, outputs to ../_external_data/cfg524_work/, file tags carry _draw<R2|R1|SC>.

Unchanged from CFG518/521: census fret_of (CFG416) painted per turnaround ball, largest wins; f_ret = 1 outside catchments; phantom from retained baryons f_ret(x)(1 + delta); census edge (capped at r_ON); expelled baryons kept as gravitating mass; MIX-A filter; T1 switch eps = 0.077; nu_mono; FLAT a0; kappa = 1/2 FITTED (footings 9.3603e-11 canonical / 1.1312e-10 alt, never pooled); Lambda-CDM background; EH ICs at z_i = 49 (the only Lambda-CDM input); step grid; seed 359, NSEED 256 at 256^3 (512 at 512^3); resolved r_ON >= 2 cells of the 256^3 mesh (RMIN = 2L/256 at L = 50/25/100; 1.56 at L = 200, as CFG518).

## Runs (256^3, nice 10, at most 8 threads each, at most 2 at once, detached with nohup; logs in ../_external_data/cfg524_work/)

At **L = 50** and **L = 25** Mpc/h:
- R2-can, R2-alt, R1-can, R1-alt (census);
- K1: f_ret = 1, canonical, draw R2 (reported, not gating);
- MUTATE: census, canonical, draw SC (= CFG521 DC-can exactly).

At **L = 200**: R2-can, R2-alt, R1-can, R1-alt (census).
At **L = 100** (reported, for the convergence trend only): R2-can, R1-can.

**Matched S0 controls (reused, not rerun):** the S0 code path of cfg524_pm.py is byte-for-byte cfg521_pm.py's (the change touches only the RES / RC = 0 / compensation branch); this is checked by the MUTATE reproduction (the whole engine minus the new branch) and by recording the sha256 and config fields of each reused S0 JSON:
- L = 50 / 25 / 100: CFG521's cfg521_S0_..._N256_L50/L25/L100.json (same engine, seed 359, NSEED 256, 256^3);
- L = 200 (256^3): CFG359's cfg359_S0_FLAT_canonical_N256.json (as CFG518; CFG521 showed cfg521 S0 reproduces CFG359 S0 exactly at 128^3);
- L = 200 (512^3): CFG411's cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json (as CFG518).

**512^3:** only if a draw rule PASSES at 256^3 (below): ONE L = 200 canonical run of that rule (R2 first if both pass; R1 afterwards only if time allows), NSEED 512, 8 threads, and only when no other 512^3 job runs. Gated by the CFG361 cuts at k <= 1 vs CFG411's S0 N512: CONFIRMED if GROWTH OK, else NOT CONFIRMED. If not run in the session: PENDING.

## Engine integrity (MUTATE reproduction)

MUTATE (draw SC) at L = 50 and L = 25 must reproduce CFG521's DC-can JSONs: |d sigma8|/sigma8 <= 1e-8 and max|dP/P| <= 1e-8 at every snapshot. If it fails, the lane is INVALID. MUTATE must also show CFG521's deficit (it must NOT be GROWTH OK in either small box; if it is, the lane is INCONCLUSIVE).

## Growth gates (frozen)

Each run vs its matched S0 at z = 0:
- **Small boxes (L = 50, 25): CFG521's gate.** GROWTH OK if |sigma8 ratio - 1| <= 0.05 AND |sigma(4 Mpc/h) ratio - 1| <= 0.05 AND max|P/P_S0 - 1| <= 0.10 over all bins k <= k_Nyq/4 (4.02 h/Mpc at L = 50, 8.04 at L = 25); FAIL if either sigma ratio is off by > 0.2; TENSION otherwise. sigma(R) is CFG518/521's box-mode estimator.
- **L = 200: CFG361 cuts.** Over k <= 1 h/Mpc: GROWTH OK if |sigma8 ratio - 1| <= 0.05 and max|P/P_S0 - 1| <= 0.10; FAIL if |sigma8 ratio - 1| > 0.2; TENSION otherwise.

## Decision (per draw rule D = R2 and D = R1, separately)

- **INVALID:** the MUTATE reproduction fails.
- **INCONCLUSIVE:** MUTATE is GROWTH OK in either small box.
- **PASS (256^3):** D-can and D-alt GROWTH OK at L = 50 AND at L = 25, AND D-can and D-alt GROWTH OK at L = 200 (CFG361 cuts).
- **FAIL:** none of the four small-box runs (L = 50/25, can/alt) is GROWTH OK.
- **PARTIAL:** anything else (each failing run named).

**Lane verdict:** PASS if both R2 and R1 pass; SPLIT (each named) if exactly one passes; otherwise both verdicts are stated as they are (neither is chosen over the other).

## Reported (not gating)

- P/P_S0 at k = 0.3 / 1 / 3 / 4 / 8 (where in range) and max|P - 1| for k <= 1; sigma(2) ratio.
- **Convergence trend:** P/P_S0 at k = 4 h/Mpc (z = 0, nearest bin) across L = 200 / 100 / 50 / 25 for R2-can, R1-can, next to CFG521/518's old-draw values (0.89 / 0.80 / 0.63 / 0.59).
- z-growth of P/P_S0 at k = 4 (z = 1 / 0.5 / 0) at L = 50.
- **Halo concentration ratio (post-hoc, declared now):** from the saved z = 0 positions, for the 100 highest CIC density peaks (256^3 mesh, 3^3 maximum filter) of each run and of its matched S0, c = M(< 2 cells) / M(< 8 cells) from top-hat FFT convolution of 1 + delta evaluated at the peak cells; reported as the median c of the run over the median c of S0 (at L = 50 and 25; L = 200 too).
- q_max (all snapshots, before the cap), overdraw mass fraction (catchments with q > 1), cap use (number of catchments and snapshots where it acted, fraction of Sum e removed), reservoir fraction, draw-weighted vs s_c-weighted mean density; Sum e relative to K1; catchment mean f_ret.

## Caveats (declared before running)

- One seed at 256^3. Small boxes lack modes with k < 2 pi/L; only ratios to the matched S0 are scored.
- PM forces are softened below about one cell; the deficit's size at the true galaxy scale is not resolution-converged.
- The reservoir is bookkeeping of the cold share s_c, not a separate cold fluid moved particle by particle. The cold energy MASS is still required.
- CFG521's census rule paints group f_ret over galaxies inside group turnaround balls (its "NOT ACHIEVED"); that is unchanged here. This lane tests only the draw.
- kappa = 1/2 is fitted; f_b and rho_Lambda are not derived. A pass is not "theory closed".
