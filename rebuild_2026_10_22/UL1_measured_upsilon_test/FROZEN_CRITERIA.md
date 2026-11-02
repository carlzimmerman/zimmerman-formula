# UL1_measured_upsilon_test: FROZEN CRITERIA

Committed alone, before any script or graded number of this lane. **Not blind:** NR3's bins, SP3's rows and the estimators' binned medians (SP3 S2) are known to the author, and SP3's question is what prompted this. kappa = 1/2 FITTED, unused. No a0 in the cold sector. Cold dark energy, never a particle. Not theory closed. SPARC's frozen 0.50-0.80 line is NOT moved and no earlier lane's verdict changes; this is a separate question with its own gate. No new data downloaded. Read only: UR3, SP3, NR3, LC1, ZN1, ZN2.

## Question
Does the SPARC-required Upsilon by V_flat, with the response on, agree in LEVEL and in SHAPE with SPARC-independent stellar masses on disk? Same gate for the a0 law as a control. Separately: is SP3's claim that UR3's "NFW c 12.95" row has a definition error real, from raw snapshots?

## Part 1: c and MW cold mass, raw
From z = 0 snapshots of LC1 (no-disc) and ZN1 at 1e12: R200, r_vir by X48's definition (18 pi^2 rho_m(z)), c200 by NFW fit to M(<r) on [max(3 eps, 0.05 R200), R200], c_nfw by X48's fit on [r_conv, r_vir], and M(<x)/M200 at x = R0/R200 for the MW on EM1 (both the cold-mass and the total-mass reading of R200). LABEL DEFINITION ERROR REAL if median c_nfw/c200 >= 1.3 and the direct M(<R0) differs from the c 12.95-on-R200 row by >= 25 %. Corrected weighing rows (DiskMass r, MW class) with my own measured c200, using UR3's code unchanged, off and f_Q 0.872. Note whether R0 lies outside 3 eps. UR3 isn't edited.

## Part 2: estimators
Durbala+20 alfalfa_sdss.csv: hi_code 1, 0.2 <= b/a <= 0.71, V = w50 / (2 sin i), q0 0.2 (SP3's cut, kept so the numbers can be checked). Upsilon_X = 0.45 x 10^(logM_X - logM_McGaugh), X = Taylor, GSWLC, each a separate bracket, never averaged. mu_X = bin median, sigma_X = half of p16-p84 in dex. Reported, not gated, as stresses: W20 for W50; D > 60 Mpc; common sample of both estimators; Upsilon_X vs distance at fixed V (W1 shortfall on extended galaxies, as SP3 S3 suggests); per-galaxy SPARC-L[3.6] ratio for UGC matches; w50/(2 sin i) vs V_flat on those matches. IMF, W1 vs 3.6 micron, bulges and HI selection are discussed in the README; anything from memory is marked PROVISIONAL.

## Part 3: model rows, grid 0.06-2.40 step 0.01 (contains the record's 0.30-1.20)
Own code, EM1's fit_one and data, X39's contract, hand S table from SP3's run of NR2 medians, native shapes zn2_low_shapes. Canonical, backgrounds A and B, sample Q <= 2, inc >= 30, V_flat > 0, as the record.
Hand EM1: off, f_Q 0.872, Blumenthal, Gnedin. Native tot EM1: off, f_Q 0.872, Blumenthal, Gnedin. Native FC1 EM1: off, f_Q 0.872. Law: canonical and alt footing (control).
Reported stress, no label: Mb self-consistent (EM1's line and the response at each trial Upsilon's Mb, instead of Upsilon 0.5's Mb). This attacks the rows, because EM1's lMb is held at 0.5.

Model value in a bin: median over galaxies of Upsilon_tot = U (1 + 0.4 f_b), f_b = Vbul^2/(Vdisk^2 + Vbul^2) at the last point, since catalogue masses are whole-galaxy and the fit's bulge is 1.4 U. U itself also reported. Bins gated: 60-100, 100-150, 150-200, 200-250, 250-400. 20-60 reported only. Constraint width by bin: per galaxy, half-width of U where mse <= mse_min (1 + 1/(n - 1)); median by bin; count at grid ends.

## Gate, stated before grading, from the estimators' spread
For bin k, estimator X: m_k model value, e_k = bootstrap sd of log10 m_k over galaxies (2000 draws, seed 1). h_k^2 = max(e_k, 1.25 sigma_X,k / sqrt(n_k))^2 + 0.04^2. 0.04 dex is a declared pad for W1 vs 3.6 micron, my judgment, PROVISIONAL.
- LEVEL(X): every bin |log10(m_k / mu_X,k)| <= 2 h_k.
- SHAPE(X), all of: (a) with one free log offset, chi2 <= 9.49 (4 dof, p 0.05); (b) weighted log-log slope of m_k on bin median V is > 0 and within 2 sigma of X's slope; (c) every adjacent step: |dlog m - dlog mu| <= 2 sqrt(h_k^2 + h_k+1^2). The free offset means an IMF-like shift doesn't fail SHAPE.
- Row label for X: CONSISTENT (LEVEL and SHAPE on both backgrounds), LEVEL ONLY, SHAPE ONLY, NOT.
- ENVELOPE reported, not a pass: each m_k within [mu_T - 2h, mu_G + 2h].

## Lane labels
RESPONSE CONSISTENT WITH MEASURED UPSILON [X] if native tot EM1 f_Q 0.872 or hand EM1 f_Q 0.872 is CONSISTENT for X. Otherwise NOT CONSISTENT, naming bins. Blumenthal f = 1 and Gnedin are reported, and if only those pass it's said separately. Also: LAW SAME GATE, its label. If the off rows or the law pass or fail alike, say the gate does not discriminate. No wording "pass of route E" at all: the record's lines stand and are reported beside it, unmoved: SPARC rms <= 0.110 and U 0.50-0.80 on the record's grid; tilt <= 0.15; LITTLE THINGS |median E| <= 0.10 (computed here); groups, keys, X-COP, IC 1613, MW, DiskMass from the record where a row exists, otherwise "ungraded".

## Checks (failed check: no verdict)
K1 hand EM1 off and Blumenthal on the record's grid: per-galaxy U equal to SP3's run (NR3's), and bins equal NR3's, |d| <= 1e-6. K2 native tot EM1 f_Q 0.872 on the record's grid: bins equal SP3's cell, |d| <= 0.0051 per bin. K3 law on record grid: rms, U equal EM1's P4 reference within 1e-6, 0.005. K4 LT for hand off, Blumenthal: |d| <= 0.001 from NR3. K5 injection: synthetic curves from the native f_Q row at true U = mu_X(V) with eV noise, refit: must be CONSISTENT with X, 2 realisations; K6 power: same with flat true U 0.50 must NOT be CONSISTENT for Taylor. K7 estimators reproduce SP3's table within 0.001. K8 c12.95 row reproduces 1.090, and c 7.8 off 1.266.
MUTATE: separate output. Reverse the estimator trend: the injected row of K5 must flip to not CONSISTENT. M_b x 2 in the response must move a U bin by >= 0.02.

## Expectation on record
NOT CONSISTENT 65 %, because of NR3's trough at 150-200 and the high dwarf bins against a rising trend. Consistent with one estimator only 25 %. Both 10 %. Definition error real: 85 %.
