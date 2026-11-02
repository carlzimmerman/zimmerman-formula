# LW1_law_scorecard: FROZEN CRITERIA, committed alone before any script or new number

kappa = 1/2 FITTED. This is a law scorecard, not a claim of a theory: no action, CMB and cluster cores not accounted for. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, reported separately, never pooled. No halo, no cold sector in any row. Nothing here says the data favour the framework. Not theory closed.

**Not blind.** Known before this freeze: FG1's C4 column; DR1's plain-law row (R1 c0: gas +0.005, f* 0.034, 10 of 15, G-OUT-M3 +4.76, +4.26; X-COP +0.467, 0.476); X5's AQUAL grid; Z2's AQUAL + EFE medians; CFG576/577; UR3, UL1 README rows. I also read the X-COP code of CS2 and DR1 (see part 2).

## The law, fixed
g = nu(g_b) g_b, nu(y) = 1/2 + sqrt(1/4 + 1/y), y = g_b/a0 (mu = x/(1+x)). This is C4's law. CFG576/577 use a different nu (1/(1 - exp(-sqrt y))), so their r values aren't this law's; they are reproduced only as a check.

## Part 1. Keys, measured chain
DR1's path, driven with my own cache: NF1's grader, one template, GS1's measured gas tail, Msrc = r^2 g/G on the grader's baryons. Grid: gas +0.005 (GS4, primary) and +0; f* 0.034 and 0.0615; both h; both footings. Per cell: all 15 Z; keys over 2 in either h; BA1's joint chi^2 (eigenmode cut 1e-3 max, chi2 sf; JOINT PASS p >= 0.05, FAIL p < 0.01) with R from BA1's bootstrap and jackknife definitions recomputed in the same run on that cell's MEAS (seed as BA1). BA1's stored R compared and reported. Z_tot for G-OUT-M3 as M3A1, quadrature, no shift: s, gas term from this law's own dZ/dgas (from +0 and +0.005) times GS4's se 0.017, M3A1's stored slope, m, n(z), leakage terms per (f*, h), seed 0 because the law has no zoom. M3A1 terms were derived on canonical; on alt they are carried and said to be. Z_tot exists for G-OUT-M3 only: M3A1 has no such budget for other keys, so other keys are stat-only and said to be.
Line K: 15 of 15 at gas +0.005, both f*, both h, per footing. +0 reported; if it changes a label, tag [GAS-ZERO-DEPENDENT].

## Part 2. X-COP
FG1's C4 X cell shows CS2's -0.151 / 0.205, DR1 shows +0.467 under what was described as a different sign convention. From reading the code before this freeze: CS2 line `d.append(log10(mh / (mb + mc)))`, DR1 `log10(Mh / Ml)`. **Same sign, log10(M_HSE / M_model).** CS2's mc is a Burkert core law whose cold mass is set to M_HSE - M_b at R500, so CS2's row isn't the a0 law. To be confirmed by computation: I evaluate the law on CS2's own row builder from the FITS files as well as on DR1's cached rows.
Statistic as ZN4/CS2: rows x <= 0.75, mean, rms of log10(M_HSE / M_law), line |mean| <= 0.05, rms <= 0.10. Reported: factor M_HSE/M_law, deficit in mass (M_HSE - M_law, Msun, per x), share of M_HSE missing, by x, by cluster, x = 1 row outside the line. A reported bracket, not a grade: LF1's lensing offset of X-COP HSE, 0.12 dex.
No rule fills the deficit here. It's a size.

## Part 3. Dwarfs with an external field
C4's X51 path: same rows, gobs, gN, s, classes, bootstrap, seed. Rows:
- **plain**: reproduces FG1's C4 Dw.
- **E1, PRIMARY**: the record's established EFE form: D10's Solver2D on S1's grid as Z2's `logG`, y from Z2's y0_of, L* = 0 (MOND flavour), xe = g_host(d_host)/a0, Z2's g_host (S1's Hernquist, MHOST, E_mid), for every system with a host field as X1 and Z2 define it. E = log10(gobs/gN) - logG.
- **E0**: the same solver, xe = 0 (its isolated virial answer), so solver offset against plain is separate from the field's effect.
- **E2**: 1-D algebraic QUMOND on X51's estimator: g = nu(|gN + gNe|)(gN + gNe) - nu(gNe) gNe, same xe, reported.
- Bracket E_lo / E_hi host on E1, reported.
LG field gets xe as X1 has it; the owner's question is about satellites, so if field's class differs from plain I say why.
Line Dw: every class |Z| < 2, per footing, on E1. If E1 and plain disagree on the label, say so. Tides: read from Z2, not recomputed. Stated beside the cell, with Z2's host-field slope.

## Part 4. DiskMass and Milky Way
The law gives only the in-plane force. **With no action its vertical force needs a form, so each is graded by form.**
- **Form A, field equation:** AQUAL for MW (X5's P4 solver, L* = 0, plain law; X5's graded row was L* 24 pc, i.e. v3, which I report as a correction to FG1's label if numbers show it matters). QUMOND-style B = nu(hypot(gb, KN)/a0), CFG576's PD one-zone, for DiskMass.
- **Form R, round rule:** extra force g_c = (nu - 1) g_b at R, vertical component g_c z/R: CFG576's RM. Both.

DiskMass, UR3's estimator and gate at 1.5 h_R, CFG576's data, UR3's K_V: Upsilon_K solved so nu(g_b) g_b = V^2/R, in-plane; r median, n fitted. **Line: r 0.90-1.10 and n >= 27.** 2.2 h_R reported. CFG577's Jeans 5-7 % stated, not recomputed: NOT COMPUTABLE here for this nu without its grid solver being rerun, and a pass that relies on it is flagged. Median Upsilon_K shown. CFG576/577's own gates failed; this lane's gate is UR3's, not theirs. OD1 (read) on old-star dispersions: stated beside.

Milky Way, UR3's gate on RG1/GD3's grade and X5's 175 cells, same priors, same tags: L1 v_c, L2a chi2_Kz, L2b K_z(R0) 66.4 +- 4.4, L3 Ou chi2; FEASIBLE IN PRIORS / WIDE PRIORS ONLY / V+K ONLY / INFEASIBLE by GD3's `classify`. **Line: FEASIBLE IN PRIORS.** Baryon-side only: Newton fields from P4's solver at each footing's grid. Form R: g_c from the Newton in-plane speed at each radius, K from g_c(R) 1.1/R. UL1's c correction concerns NFW starts: no halo here, so it doesn't apply, which I state. FG1's X5 gate (chi2_Kz + v_c only) printed beside.
Per-line label PASS, FAIL, NOT COMPUTABLE, with [FORM-DEPENDENT] if A and R disagree.

## Part 5
UL1's measured Upsilon gate already includes the law. Carried, not redone.

## Scorecard
Eleven lines as FG1's, per footing. S, Tl, LT, G, Ln, IC carried from FG1 C4 (tag [READ FG1]); K, X, Dw, DM, MW from this lane. Labels: PASS, FAIL, NOT COMPUTABLE. No overall pass claim: output is the table. Nothing is a verdict on a theory. No line moved.

## Checks (failed check: no verdict on that part)
K1 plain dwarfs reproduce FG1's C4 Dw class medians and Z, both footings, |d| <= 1e-6.
K2 keys: R1 c0 canonical, gas +0.005, f* 0.034 and 0.0615, and +0 at 0.034; alt at 0.005, 0.034: Z and preds against DR1's JSON, |d| <= 1e-6. Groups Z against DR1's, and against FG1's C4 (rounded).
K3 X-COP on cached rows reproduces DR1's +0.467, 0.476, |d| <= 1e-6; FITS row builder reproduces CS2's -0.151, 0.205 with CS2's law, then the a0 law on those rows against the cached value, disclosed if over 1e-3.
K4 solver E1 inputs: Z2's stage table emb0 and iso0 for Z2's systems, |d| <= 1e-6; xe against X1's x_e_mid, |d| <= 1e-6.
K5 DiskMass: no extra force reproduces UR3's K1 (1.494, 0.821); CFG576's nu and a0 through my code reproduce RM 1.250, PD 1.475, |d| <= 1e-3 (CFG576 prints 3 places).
K6 MW: AQUAL L* = 0 cells reproduce X5's stored L0 chi2_kz, K_R0, v_c, |d| <= 1e-6 relative; Newton McMillan V_b(R0), K_z,b against GD3's .out literal.
K7 BA1's method: R recomputed on this cell against BA1's stored R reported; R = I gives sum Z^2, |d| <= 1e-9.
K8 joint chi^2 against M3A1's ZN4 row: its stored Z through this joint function, using M3A1's own... if M3A1's R isn't stored, this check is NOT RUN and said to be.
**MUTATE** a0 x 1.5 in the law (canonical and alt), separate outputs: must move keys, X-COP, dwarfs, DiskMass, MW. A part that doesn't move has failed its check. Reported whether grades flip; a flip to PASS under the mutation isn't a result.

## Expectation on record
K FAIL, about 10 of 15, M3 Z_tot about +3.5, joint fail. X-COP FAIL, +0.47 and a factor near 3, same convention as CS2. Dw FAIL, with E1 worse than plain on UFD (Z2's +1.1 against +0.56). DiskMass round FAIL about 1.2-1.3, form A FAIL about 1.45. MW FAIL: X5's feasible cells fail L2b, so V+K can't hold; expect INFEASIBLE under UR3's gate, form R unknown. Overall: same or worse than FG1's C4 on every line touched.

One thread, nice 15. Local commits only. kappa = 1/2 FITTED. Not theory closed.
