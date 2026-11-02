# TM2_time_lag_memory: FROZEN CRITERIA (committed alone, before any script or computed map)

Owner's standing go, 2026-11-02. The lane was asked as "TM1"; `TM1_tethered_medium` exists, so this is TM2. **Not blind.** Read before this: UX6 (README, criteria, script, its unfinished "no lagged memory" item), MG1, UX3, CU1, DR4, X32, CFG726, heads of CFG70, CFG120, CFG123, CFG153, CFG349. Web numbers below were read before freezing, so inputs are frozen knowing them; PROVISIONAL, through a summariser. Hand estimates made: c/a0 about 100 Gyr; r/V at 300 kpc about 160-240 Myr; v r/c about 9 kpc per Mpc at 2700 km/s. Geometry argument made by hand (section 3). A description, no action. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Cold sector stays retired; no result reinstates it. No particle. No LCDM yardstick. Not theory closed. Nothing here says the data favour the framework. No downloads.

**Inherited, flagged:** the merger histories come from simulations built with massive collisionless halos, a thing this lane doesn't have. Here they are kinematics only, and a term with this mass need not produce them. A pass would owe its own orbit.

## 1. Inputs
Baryons, frame, k, law kernel, QUMOND-type estimator, regulator a0/1000, Sigma_crit: exactly UX6's. Observables O1, O2, O3 and cell class: exactly UX6's, tolerances unchanged: position sigma 0.195 of the separation, M300 15 %, ratio 0.657 +- 0.14 reported. Those are X32's PROVISIONAL errors, not re-derived. k's real error, from CU1: reported rows at k x 0.65 and x 1.35 (CU1's single-cluster range 8.7-18.1), no label.
Grid 20 kpc, z grid as MG1's, surface masses on UX6's cylinder; K1 ties this to UX6's 10 kpc.

Histories (PROVISIONAL). û along BCG1 to BCG3, n̂ its normal. Straight relative line: rel(s) = D û + (s/t)(b n̂ - D û), D = 849 kpc (model frame), |rel| capped at 3.5 Mpc. s = lookback. COM at BCG1 + q D û; x_main = COM - q rel, x_sub = COM + (1-q) rel. Gas component i: x_group(s) + o_i g(s), o_i its present offset from its BCG, g = (1 - s/t)^p for s < t, 0 before passage. Gas masses constant. History start 10 Gyr.
| Id | t Myr | q | p | b kpc | Source |
|---|---|---|---|---|---|
| P primary | 180 | 0.12 | 1 | 0 | t Springel & Farrar default; q Lage & Farrar 1.91e15, 2.59e14 |
| t150 | 150 | 0.12 | 1 | 0 | Mastropietro & Burkert, about 0.15 Gyr |
| t260 | 260 | 0.12 | 1 | 0 | S&F c = 3 best match, t 1420 vs passage near 1200 Myr, approx |
| q09 | 180 | 0.09 | 1 | 0 | S&F 10:1 |
| q40 | 180 | 0.40 | 1 | 0 | lensing M300 ratio read as dynamical masses, no-halo end |
| p2 | 180 | 0.12 | 2 | 0 | gas lag quadratic, my bracket |
| b256 | 180 | 0.12 | 1 | 256 | Lage & Farrar b 256 +- 35 |
Reported: P with bullet-side gas x 2 before passage only (pre-merger gas isn't measured; sims give f_gas 0.17-0.19 of M200, so the sub's could exceed the model's 2.3e13).

## 2. Forms. No field equation; each is a separate claim
Kernel: K(s) = exp(-s/tau)/tau, s >= 0, renormalised over the history; piecewise constant on nodes. Reported at P: boxcar on [0, 2 tau].
**Fixed frame**, gas at past positions, field read at the same point in a frame. <.> is K's average.
- **F1:** g = ghat_b law(|g_b|)(1 + k <|g_gas|>/a0).
- **F2:** g = ghat_b law(|g_b|) + k (law/a0) <g_gas vector>.
Frames, gas shifted by V_f s: COM (primary); main galaxies' rest; sub galaxies' rest; COM +- 600 km/s along û and along n̂ (cosmic-frame bulk, unknown, PROVISIONAL).
**Along galaxy worldlines**, memory transported with the stellar flow. Delta_c(s) = x_c(0) - x_c(s), BCG track; w_c(x) = rho_star,c/(sum rho_star), present stars.
- **W1:** as F1 with <|g_gas|> = sum_c w_c <|g_gas(x - Delta_c(s), t - s)|>.
- **W2:** as F2 with the same sum over vectors.
- **W3:** UX6's enclosed form about each BCG with own-group gas at offset g(s) o_i, averaged: between N1 (tau to 0) and N2 (tau to infinity). The law factor uses the same memory.
Memory along **gas** worldlines stays on the gas and can't track galaxies; it's L1 again on a steady flow. Stated, not run.
Light-cone retardation (box^-1, DR4): computed by size only.

tau rules:
- **R-a0:** c/a0. **R-a0b:** c/(2 pi a0). Both exceed the history, so they count as the same class, no new constant.
- **R-dyn:** tau(x) = sqrt(r/law(g_near(r))), r distance to nearest BCG, floor 20 kpc, g_near that BCG's group's enclosed baryons, present. **R-dyn2:** 2 pi times that.
- **R-fit:** constant, 5, 10, 20, 40, 80, 150, 300, 600, 1200, 2500, 5000, 10000 Myr. Counted as one fitted constant wherever it is quoted.

## 3. The catch, as a statement to be computed
Galaxies lead their gas. Past gas sits behind present gas in the moving direction. So in any one frame, memory of a subcluster's own gas lies farther from its galaxies than the present gas does, except for the frame moving with those galaxies, and one frame can't move with both. Other-group gas crossing a galaxy's present position is the possible exception; the map decides it.

## 4. Grade on the Bullet
Cell = form x rule x history x footing x k (fit, pi^2), UX6's class. Non-primary histories at k fit only; frames at k fit, canonical and alt, on P.
- **Position/sign DEAD** (form x rule): position or sign fails in every cell on P.
- **BULLET PASS:** PASS at k fit, both footings, on P. **ROBUST** adds PASS or TENSION on at least 5 of the 6 other histories.
- **WOUNDED:** position and sign hold at k fit both footings on P, mass or TENSION not.
- **MIXED:** else, stated.
**Window:** the R-fit values with BULLET PASS, else those WOUNDED, else "none", with the nearest miss and its margin. Margin = worst |Z| across O1, O3 and dkappa's sign, on P.

## 5. Relaxed clusters and discs
Memory factor m = <g_gas>/g_gas applied to UX3's term.
- **X-COP:** UX3's rows, lines |mean| <= 0.05, rms <= 0.10 on all 7 and on the unseen 3. W: Monte Carlo orbits in M_FORW's potential, isotropic Gaussian sigma^2 = v_c^2/2, beta 0 and 0.5, 400 orbits per radius, 7 clusters, 5 radii. F, COM: m = 1 by identity. F, moving: v_pec 300, 600 km/s, gas shifted v s, angle-averaged, enclosed-mass field. Long tau gas growth: M_gas linear in time since 6 Gyr ago, reported. k fixed and k refit on UX3's 4 (counted).
- **Keys:** CU1's build (read only) with m(r/R500) from the median of X-COP's factors injected, both footings, h's as CU1. Rule at R-dyn, R-dyn2, and 300, 1200 Myr; count of 15, G-OUT-all, G-OUT-M3.
- **Discs:** UX3's rows: even SPARC rms <= 1.05 law, |med| <= 0.03, LT |med E| <= 0.10; DISC BREAK if any fails. W, circular: m = 1, must reproduce UX3's unswitched row. W + epicycle: radius oscillating +-10 %. W + long tau: g_gas + g_stars/2 (stars were once gas). F moving: v_pec 100, 300, 600 km/s, R-dyn = R/V, R-fit, R-a0. **WORSE/BETTER** stated against unswitched UX3 and against the law. C1 is not applied, then applied, as a row.
- **Self-force:** F only: acceleration on an isolated moving body from its own memory, stopping time v/a at the centre for a cluster (2e14, 500 kpc, 500 km/s) and a disc (1e10 gas, 10 kpc, 300 km/s). Reported against 10 Gyr. W is Galilean on a steady flow, stated.
- **Causality:** retarded by K, s >= 0. Check |Delta_c(s)| < c s on all nodes. Light-cone size v r/c. Which structure each form needs: a preferred frame (F); a unit timelike flow (W), DR4's and CFG349's cost. No action written here.

## 6. MG1's rows
Pair model as MG1, primary rows and the Bullet control. Forms F2, W2. Age: published where read, Musket Ball 1.1 (+1.3, -0.4) Gyr, Bullet as P; else PROXY t = s/(1000 km/s), bracket 500, 1500. Gas speed in frame PROXY 0.5 s/t. Rules R-dyn at 300 kpc on M_lens, and 50, 200, 1000, 5000 Myr. Rows: dkappa sign and delta. **HOLDS** if dkappa > 0 at >= 2/3 of primary rows at the observed GAL rows; else FAILS. The old-merger question: does memory fade by Musket Ball and ZwCl 0008's age at R-dyn? Sign is close to construction at long tau (MG1's warning); only the fade is new.

## 7. Verdict
Title states, for each of F and W, whether any tau rule gets the Bullet, then relaxed keys and discs. **CANDIDATE** only if BULLET PASS ROBUST and X-COP lines hold and discs don't break, at one rule; a candidate has no action and needs a second implementation. Otherwise: no candidate, nearest miss with margin.

## 8. Checks. A failed K1, K2 or K6 stops the verdict
K1 tau to 0 vs UX6's JSON: F1 = L1, F2 = L2, W1 = L1, W2 = L2, W3 = N1; W3 tau to infinity = N2; k = 0 = law: M300 and dkappa within 2 % (grid differs), peaks within one 20 kpc cell of UX6's. K2 concentric static reduction, 1e-3. K3 nodes x 2 on W2 and F2, 300 Myr, P: M300 1 %. K4 map vs surface M300 8 %. K5 RSS under 4 GB. K6 UX6's controls: on BCG PASS, on gas FAIL. K7 causality check above. K8 orbit integrator energy 1e-3; m to 1 as tau to 0. K9 CU1 build with m = 1 gives 14, 10 keys. K10 W circular reproduces UX3's unswitched even-SPARC rms 0.208, 0.213 at pi^2. K11 rerun byte-identical.
**MUTATE twin, must fail:** gas x 2 in tau-to-0 (K1); F2's memory sign flipped (K2); control on gas (K6); Delta x 1e5 (K7); orbit step x 200 (K8). Separate outputs, exit 1.

## 9. Expectation, mine, on record
F at all rules position or sign DEAD 90 %. W2 and W3 sign holds at tau >= t, 75 %; BULLET PASS at any tau 10 %, since N2's sub/main 0.25 is the limit it interpolates to, and sub mass is the problem. c/a0 rules fail relaxed or disc rows through the whole-history mean 80 %. W discs not better than UX3's unswitched 85 %. F moving discs better than unswitched 60 %, and that's a switch bought with a self-force. Candidate overall 5 %.

## 10. Limits known now
Straight lines; no self-consistent orbit. Plummer baryons, no inclination, a0 at z = 0. M300 a lens reconstruction. Gas masses constant in the map. Star flow as one bulk motion per subcluster on the map; internal orbit smear only in the relaxed check. Field velocities PROVISIONAL. X-COP's k carried into a merger. MG1's pair and proxies as MG1's limits.

Compute: one thread, nice 19, under 4 GB.
