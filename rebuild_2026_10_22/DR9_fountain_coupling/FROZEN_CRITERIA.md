# DR9_fountain_coupling: FROZEN CRITERIA (committed alone, before any script or number from this lane)

**Question.** ER1 failed on order: one energy coupling undoes the response in dwarfs first. An outside text claims a coupling that depends on the galaxy, eta_PG = (f_local / (1 + f_local))^2 with f_local = M_b(r0) / M_c0(r0), times a retention factor, has no new parameter, reverses the order and is 10x larger in spirals. Treated as a claim. Its citations (Pontzen & Governato 2012 Eq. 9; Read & Gilmore 2005) are from memory, PROVISIONAL. No download.

**Record check.** ER1 (one epsilon, WRONG SHAPE), CM1 (gas cycles, gravity only, CHANNEL INSUFFICIENT), BE1, DR5, RM1 (no flat f), CL5, OC1, SH1, CFG930/932. A mass-varying coupling was named in ER1's limits as untested. grep finds no eta_PG lane. Not already tested.

**Desk points on record before any number.**
- The form is posited, not derived from an action. As I recall PG12, the impulsive energy gain per cycle is second order in the potential change, which scales with gas actually moved over the mass enclosed, is gravitational, and carries no E_SN. Then the square would take moved gas, M_g(r0), not M_b(r0): stars don't blow out. So the text's form may be a misreading, and in spirals, gas-poor, the true form could run the other way. Reported as a diagnostic, not graded, from memory.
- It is not zero-parameter. DeltaW = C x eta_PG x R x E_SN. C lumps at least: fraction of E_SN reaching gas, gas-to-cold transfer, and number of cycles. Name them; C = 1 is the only zero-number reading and is an upper limit, not a prediction.
- E_SN already scales with M_star, so R = M_star/M_b counts star formation twice.

**Not blind.** ER1, DR5, RM1, NR3, CM1 read. NR3 bins, f 0 and f 1: 1.20, 1.18, 0.90, 0.57, 0.62, 0.77; 0.49, 0.53, 0.46, 0.30, 0.36, 0.47. DR5 flat f 0.25: 0.47 at 150-200. RM1: flat f can't do it. CM1 net work 1.15e57 erg against E_SN 4.06e59 erg. The f_req and C_CM1 below are built from those.

## Rule (Newtonian, NR3's path: EM1, NR2 MEDIAN, Blumenthal, canonical, both backgrounds, UR1 and NR3 read only)
Per galaxy, per Upsilon on the fit grid, on the grader's own radial grid:
- f_local = M_b(r0) / M_c0(r0), M_c0 the uncontracted core profile; **BEFORE response is primary**.
- eta_PG = (f_local / (1 + f_local))^2.
- **R, primary:** f_ret = min(1, (1 + R_nat) M_b/M200), 1 + R_nat = 6.271, M200 from EM1. Chosen because it is what the word retention means, and because M_star/M_b double counts. **Secondary, reported in full:** M_star/M_b.
- E_SN = (M_star / 100 Msun) x 1e51 erg, M_star = Upsilon L36, as ER1.
- E_undo = max(0, [W(M_0) - W(M_f)] / 2), M_f full Blumenthal, W with baryons, CN1's and ER1's.
- DeltaW = C eta_PG R E_SN. **f = 1 - min(1, DeltaW / E_undo)**; E_undo = 0 means nothing to undo, f = 1, counted.
- M_c = M_0 + f (M_f - M_0). Baryons unchanged. No threshold, no a0. M_star for LITTLE THINGS from the cache. Groups: all stars, M_b = M_star, by hand (ellipticals are no fountain system; stated).

## Normalisations, three, one each, no scan
1. **C = 1.** Upper limit.
2. **C_CM1, not fitted to the line.** Epsilon_CM1 = net work into cold / E_SN at CM1 PRIMARY, read from CM1's files; C_CM1 = epsilon_CM1 / median(eta_PG R) over Q <= 2, i >= 30 galaxies within 0.3 dex of CM1's M200, 6.19e11, Upsilon 0.50, background A. CM1's galaxy is a SPARC median by construction, but its coupling comes from a simulation of gas cycles, not from any SPARC grade. This is the one non-SPARC-line source I can state. It softens a cusp rather than undoing contraction, so carrying it over is BY HAND.
3. **C_FIT, FITTED, once, closed form.** f_req at 150-200 = linear interpolation in NR3/DR5's rows, f 0 Upsilon 0.57 and f 0.25 Upsilon 0.47, to Upsilon 0.50: f_req 0.175. C_FIT = median over the 150-200 bin of (1 - f_req) E_undo / (eta_PG R E_SN), Upsilon 0.50, background A. Own C_FIT for each R. Not iterated even if the bin misses 0.50; the miss is reported. Fit bin is one bin of one background.

## Runs
Energy table, Upsilon 0.50, background A, by V_flat, same cut as DR5, on DR5's 400-point grid: f_local, M_star/M_b, f_ret, eta_PG, E_SN, E_undo, epsilon_full = E_undo/E_SN, DeltaW/E_undo at C = 1 for each R. Diagnostic: eta_gas = (M_g(r0)/(M_b + M_c0)(r0))^2 with M_g from the Upsilon-linear split of GB, and DeltaW_PG = N M_c0(r0) G(M_b + M_c0)(r0)/r0 x eta_gas, N = 40 (CM1's), order unity BY HAND, against E_undo.
Rows, each with Upsilon, rms, tilt, bins both backgrounds, groups, LITTLE THINGS: C0; CINF; RET_C1, RET_CM1, RET_FIT; STAR_C1, STAR_CM1, STAR_FIT; RET_FIT_AFTER, f_local read after full response with RET_FIT's C. Reported difference BEFORE vs AFTER.
**Clusters:** not regraded. Keys, X-COP stay NR3's EM1|blum: 14 keys, G-IN-Mall -2.05, X-COP -0.097, 0.146. X-COP fails there, so **no row here can be a full pass**. Reported: f_local at 0.05 Mpc with and without the BCG, median over ALLI[::4], and with BCG, DeltaW/|W change| at each C using the cluster's stars. The response there runs outward, so "undo" has no plain meaning; say so. NR3's X-COP row carries no BCG (XH1), the keys' do.

## Pass lines (the record's)
SPARC rms <= 0.110 and Upsilon 0.50-0.80 both backgrounds; |tilt| <= 0.15; groups |Z| <= 2; LITTLE THINGS |median E| <= 0.10. 15 keys and X-COP as above, read.

## Labels, on RET rows
- **NOT DECIDED:** any check fails.
- **SPARC SIDE CLEARS AT C = 1, CLUSTERS FAIL** / **... AT C_CM1 ...** / **... AT C_FIT (FITTED) ...:** first row clearing every SPARC-side line, in that order. Never a pass.
- **FAILS AT ALL THREE:** none clears; name the gate per row.
Separate, frozen: **ORDER REVERSED** if median DeltaW/E_undo, 150-250 over 20-100, Upsilon 0.50, RET, is above 1, else NOT REVERSED. **TEN TIMES** claim: eta_PG R, same ratio, read against 10. STAR rows never set the label; if one clears where RET fails, reported and said to be the double-counted form. **REDUCES TO CM1:** if C_FIT / C_CM1 >= 10, say the rule needs that factor over the measured channel.

## Checks
K0 C0 vs NR3 EM1|blum: Upsilon, rms, tilt, LITTLE THINGS, groups Z, |d| <= 1e-6. K1 CINF vs NR3 EM1|off: SPARC and LITTLE THINGS |d| <= 1e-5, since DR5 A1 found 5.6e-6 from the 300-point grid, disclosed; K0 carries the 1e-6 rule. K2 1 + R_nat = 6.271 to 0.001. K3 every f within [0, 1]. K4 energy table's T_rot/E_undo by bin vs DR5, |d| <= 1e-6. K5 epsilon_CM1 reproduces CM1's 1.15e57 / 4.06e59 within 1 %. MUTATE, separate output: eta_PG with f_local inverted, (1/(1 + f_local))^2 at RET's C_FIT; must move Upsilon by more than 0.02. Failed check: no verdict.

## Expectation on record, mine
Order reverses, mostly from eta_PG. C = 1 undoes almost everything, near NR3's off row, tilt about +0.5, fail. C_CM1 barely moves NR3's response row, Upsilon about 0.36, fail. C_FIT lifts Upsilon onto the line, but dwarfs lose a good share too, tilt +0.2 to +0.45, LITTLE THINGS above 0.10, fail. C_FIT is tens of times C_CM1. Label FAILS AT ALL THREE.

## Limits
Outflow removes gas; held fixed. No a0 in the cold sector. kappa = 1/2 FITTED, unused. One thread, nice 15; rows checkpoint to files and resume. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
