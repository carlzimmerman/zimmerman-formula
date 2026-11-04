# FROZEN A37: modified inertia from the de Sitter Unruh effect (rival modified-inertia route, not LCDM)

Frozen before any A37 number. Script `scripts/recipe38.py`, output `scripts/recipe38.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. This is NOT a LCDM route: it is a rival modified-inertia route, graded because it is the one route on record with a claimed mechanism tying a0 to Lambda. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing: only the source equations below and the folder constants from earlier lanes (A24 l.1-2: c sqrt(G rho_DE) = 1.8727e-10 = 2.000 A0; cH_inf = c^2 sqrt(Lambda/3) = sqrt(8 pi/3) c sqrt(G rho_DE)). The kappa_eff values written under "Expected" are those constants multiplied out by hand, not run. No SPARC number of this lane was computed or seen. Known from the record: the g_b + sqrt(a g_b) family with one knob gave E1 0.0392, E2 0.0546, E3 0.0660, holdout 0.0378 (A22 (a), A23 (a), A24 V4p).

## Sources (PROVISIONAL: WebFetch summaries of ar5iv/arXiv HTML, 11-04; no PDF downloaded)

- R1 Milgrom 1999, Phys. Lett. A 253, 273, astro-ph/9805346 (cited as milgrom99). Units hbar = c = k = 1. Eq. 6: T(a) = (1/2 pi)(a^2 + Lambda/3)^(1/2), the temperature seen by a uniformly accelerated observer in de Sitter space; T_Lambda = T(0) (the text prints (Lambda/3)^(1/3), read as a typo for 1/2). Eq. 8: 2 pi (T - T_Lambda) = a mu^(a/a^0). Eq. 9: mu^(x) = [1 + (2x)^-2]^(1/2) - (2x)^-1 with a^0 = 2 (Lambda/3)^(1/2). Eq. 10-11, a second form: a dT/da gives mu(x) = x/(1 + x^2)^(1/2) with a0 = (Lambda/3)^(1/2); the paper does not reconcile the factor 2 between the two. Eq. 5: for circular orbits a mu(a/a0) = g_N, a = v^2/r, with the remark that mu for circular orbits "need not take the same form" as for linear motion. The paper gives no numerical Lambda, does not compare a^0 numerically with the observed a0, works in de Sitter only, and states that in a general Friedmann universe the expansion rate, curvature and Lambda differ.
- R2 McCulloch 2017, Astrophys. Space Sci. 362, 149, arXiv 1709.04918 (quantised inertia, MiHsC; separate row). Eq. 1 m_i = m (1 - 2c^2/(|a| Theta)); Eq. 7 a^2 = a_bar^2 + a_bar 2c^2/Theta; Eq. 8 a = a_bar sqrt(1 + 2c^2/(a_bar Theta)), used on SPARC with no knob; Theta = 8.8e26 m, the co-moving cosmic diameter (earlier papers 2.6e26 m); Eq. 9 Theta(z) = Theta_now/(1 + z) (linear-expansion assumption). Eq. 5 to 6 (the step from Eq. 1 to Eq. 7) is a heuristic cancellation stated in the paper, not derived from Eq. 1 algebraically; solved literally, Eq. 1 gives a = a_bar + 2c^2/Theta (reported as a diagnostic row).
- R3 follow-up, arXiv 2602.14515 (2026; title not recorded): Eq. 21 v^2/r = sqrt((a_N + a_bg)^2 - a_bg^2), a_bg = sqrt(Lambda/48), "a0 ~ 2 a_bg = sqrt(Lambda)/(2 sqrt 3)"; also a_bg^2 ~ -(1/16) q0 H0^2. No SPARC test in the paper; it quotes 2 a_bg ~ 2.6e-10 against a fitted 1.2e-10.
- Pikhitsa 2010, "MOND reveals the thermodynamics of gravity" (listed in R3's references, no arXiv id found): not found; not graded.

As implemented (SI, c restored, accelerations): a_L = c^2 sqrt(Lambda/3) = c H_inf, Lambda = 8 pi G rho_DE/c^2, rho_DE = Ode0 rho_crit of lib's cosmology.
- Shape S9 (R1 Eq. 8-9, R2 Eq. 7, R3 Eq. 21 are all this one shape): g_N = sqrt(g^2 + (A/2)^2) - A/2, i.e. g = sqrt(g_b^2 + A g_b), with deep limit sqrt(A g_b) (A is the MOND-equivalent a0, compared with the law's a0) and high limit g_b + A/2.
- Shape S11 (R1 Eq. 10-11): g mu(g/A) = g_b with mu = x/sqrt(1 + x^2), i.e. g^2 = (g_b^2 + sqrt(g_b^4 + 4 g_b^2 A^2))/2; deep sqrt(A g_b), high g_b + A^2/(2 g_b).
- The law: g = (g_b + sqrt(g_b^2 + 4 a0 g_b))/2, i.e. g^2 = g g_b + a0 g_b ("simple" mu); deep sqrt(a0 g_b), high g_b + a0.
- The A22-A24 family: g = g_b + sqrt(a g_b).
Grading on SPARC's g_b directly is the modified-inertia circular-orbit relation (algebraic in the Newtonian field); its use of R1's linear-motion mu for circular orbits is imposed (R1 says it need not hold).

Values of A, 0 knobs: M9 A = 2 a_L (R1 Eq. 9); M11 A = a_L (R1 Eq. 11); QI A = 2c^2/Theta with Theta = 8.8e26 m (R2 as published), QIe Theta = 2.6e26 m (earlier value, disclosed), QIc Theta = 2 x comoving particle horizon of lib's cosmology (no radiation, colossus) (my reading of "co-moving diameter", disclosed); F26 A = 2 a_bg = a_L/2 (R3).

Derived in the sources: the T(a) formula (a known de Sitter result), and the form of the temperature difference. Imposed: that inertia is proportional to the temperature difference (R1's posit); which of Eq. 9 or Eq. 11 applies; the linear-motion mu for orbits; R2's Eq. 5-6 cancellation and Theta's identification; R3's 1/48.

## Rows on SPARC (lib.load, 171 galaxies, 3373 points, Upsilon 0.5/0.7; lib.grade E1 <= 0.02, E2 <= 0.04, E3 <= 0.02; rms to observed reported against the law's 0.1951)

(a) 0 knobs: M9, M11, QI, QIe, QIc, F26; diagnostic QIlin g = g_b + 2c^2/Theta (R2 Eq. 1 solved literally).
(a') 1 knob, A free (log bounds 1e-12 to 1e-8): S9 (covers M9, QI, F26 with free scale) and S11, tuned on all; holdout tuned on GS[::2], unseen rms to law on GS[1::2] <= 0.025. Side by side, same machinery: the g_b + sqrt(a g_b) family (expected to reproduce 0.0392 / 0.0378) and the law form itself (control, 0). Also reported: fitted A against A0 and the A fitted to observed g (lib's ALLO).

## Tie gates for each source's A (A13 G1 to G5, as A24 applied them)

- G1 kappa_eff = A/(c sqrt(G rho_DE)) within 0.05 dex of 0.5.
- G2 slope d ln A / d ln rho_DE over the three J cosmologies (OL, H0) = (0.70, 67.4), (0.685, 73), (0.65, 73), flat, Om = 1 - OL: 0.50 +- 0.05. Lambda rows: 0.5 by construction. QI rows: Theta recomputed in each J cosmology (QIc), Theta fixed for QI (slope 0, stated).
- G3 a(z)/a(0) inside [0.76,1.03], [0.71,1.12], [0.33,1.21] at z 1, 1.5, 2.33. Lambda rows flat in lib's LCDM (pass by construction); QI rows by R2 Eq. 9 (1 + z).
- G4 per-galaxy effective a = lib.fit_a of the law form to that galaxy's route curve (0-knob curve), rms of log over hosts with lib SHMR log M200 11 to 12.5 <= 0.1 dex (A24's rule). The route constant itself is universal; this grades what the shape does to the effective constant.
- G5 operative at galaxy radii: boost g - g_b at 10 kpc for a 1e10 Msun point mass >= 0.1 a0. Modified inertia acts on all motion by its posit: "pass by posit", as in A24.
- Solar system (relevant here: an inertia law acts at every acceleration): anomalous radial acceleration g - g_N at Saturn (g_N = G Msun/(9.537 AU)^2) against A9's frozen threshold 1e-3 a0 (recipe11 A3 line). Control row: the bare law's own g - g_N at Saturn, reported with the same threshold (the framework is not graded bare here; stated, not a verdict on it).

## (c) GT in A29's backgrounds (B0 to B5, recipe31 definitions, rho_DE(z), H(z), w(z) from colossus; amplitude footing irrelevant here)

R1 is derived in exact de Sitter space; replacing Lambda by 8 pi G rho_DE(z)/c^2 is a HAND generalisation (R1 says Lambda, H and curvature differ outside de Sitter and does not let Lambda vary). Readings graded with GT |log10[A(z)/A(0)] - 0.5 log10[rho_DE(z)/rho_DE0]| <= 0.05 dex at z 1, 1.5, 2.33, plus G2z (A29 rule) and G3:
- L1 hand generalisation, a_L(z) = c sqrt(8 pi G rho_DE(z)/3): tracks identically (it is A29's T2g times a constant).
- L2 the FRW reading where the observer's horizon temperature is H(z)/2 pi (apparent-horizon temperature, my choice of the natural FRW analogue, imposed): a_L(z) = c H(z); A29's T1 times a constant.
- QIz R2 Eq. 9 as published: A(z) = A(0)(1 + z) in every background.
- QIp physical particle-horizon diameter at z in each background, Theta(z) = 2 a(z) c int_z^inf dz'/H(z') (my reading, disclosed).
- F26q R3's deceleration form a_bg(z) = sqrt(-q(z)) H(z)/4: reported; undefined where q(z) > 0.

## Expected in advance

(a) Every 0-knob row fails E1 by a wide margin: A/A0 about 11.6 (M9), 5.8 (M11), 2.9 (F26), 2.2 (QI), so the deep limit is too high by sqrt of those. (a') One knob: S9 matches the deep limit but sits at sqrt 2 = 1.41 A against the law's 1.62 at g_b = A (-0.06 dex) and goes to g_b + A/2 against g_b + A at high g_b, so a fitted A compromises; expected E1 0.025 to 0.04, FAIL, with holdout also failing; S11 (standard mu) worse. No shape here is the law's. G1: M9 kappa_eff 5.79 (+1.06 dex), M11 2.89, F26 1.45, QI about 1.1: all FAIL; Milgrom's numerical coincidence 2 pi a0 ~ c^2 sqrt(Lambda/3) (A13 T2, kappa 0.461) is not the value R1's formula gives. G2, G3 pass by construction for Lambda rows, QI fails G3 via (1 + z). G4 at or near the A24 point-mass value (~0.07 dex). G5 pass by posit. Solar system: S9 rows carry a constant A/2 anomaly at Saturn (~1e3 times A9's threshold, FAIL); S11 tiny (pass); the bare law control also carries ~a0 (FAIL bare). GT: L1 tracks (0 dex); L2 and QIz fail by ~+0.5 dex at z 2.33; QIp fails; F26q undefined at z >= ~0.6.

## RESULTS (written after the run; criteria above unchanged)

Runtime 38 s, peak RSS 86 MB, single thread. Line numbers refer to `scripts/recipe38.out`.

BUG, disclosed: the first run printed F26q's "today 2 a_bg" as 0.000 A0 because c was left out of a_bg = sqrt(-q) c H/4 (only that number; the z ratios and every other line are unchanged). Kept as `scripts/recipe38_before_fix.out`; fixed and rerun. The same rerun added a post-hoc diagnostic (l.67-68), labelled as such, because S9 passed three of four shape gates against the expectation.

(a) 0 knobs, all FAIL E1 to E3 (law to observed 0.1951): M9 (R1 Eq. 9, A = 11.58 A0) E1 0.4095 (l.6-7); M11 (Eq. 11, 5.79 A0) 0.2674 (l.11-12); QI (Theta 8.8e26, 2.18 A0) 0.0920, E2 0.1339, E3 0.1379 (l.16-17); QIe 0.3203 (l.21-22); QIc (Theta 8.885e26 from lib cosmology) 0.0903 (l.26-27); F26 (R3, 2.90 A0) 0.1426 (l.31-32); QIlin (Eq. 1 solved literally) 0.6813 (l.36-37). All sit high at low g_b, as expected: each source's A is 2 to 12 times A0.

(a') 1 knob:
- S9 sqrt(g_b^2 + A g_b), the shape shared by R1 Eq. 9, R2 Eq. 7-8 and R3 Eq. 21: A 1.3014 A0, not at bound; E1 0.0189 PASS, E2 0.0256 PASS, E3 0.0273 FAIL (bins +0.027 at log g_b -12, -0.027 at -10.0) (l.43-45); holdout unseen 0.0195 PASS (l.47); to observed 0.1973, A fitted to observed +0.111 dex vs A0. NOT EXPECTED: I expected E1 0.025 to 0.04. Checked: post-hoc scan of A over 0.8 to 2 A0 gives minimum worst bin 0.0270 and no A passes E1+E2+E3 together (l.67). So S9 is the closest one-knob shape on record in this folder, but it is NOT EXACT: it fails E3 by 0.007 dex, with a residual that changes sign across g_b (the shape at equal deep constant runs to -0.061 dex at g_b/A 0.3, l.69-73).
- S11 standard mu (R1 Eq. 11): A 1.416 A0, E1 0.0384, E2 0.0541, E3 0.0653, holdout 0.0390, all FAIL (l.49-53).
- g_b + sqrt(A g_b) (A22-A24 family): reproduces E1 0.0392, E2 0.0546, E3 0.0660, holdout 0.0378, A 0.673 A0 (l.55-59).
- Law form control: 0.0000 (l.61-65).
How the shapes compare (l.69-73, equal deep constant): all three share the deep limit sqrt(A g_b). The law goes to g_b + A at high g_b; S9 to g_b + A/2 (below the law at every g_b, worst -0.061 dex near g_b ~ 0.3 to 1 A); S11 to g_b + A^2/(2 g_b) (worst -0.104 dex); g_b + sqrt(A g_b) lies above (worst +0.096). S9 halves the law's transition miss of the A22-A24 family, which is why one rescaled A brings E1 under 0.02; the rescale (1.30 A0) is the price, and the sign-changing residual is what E3 sees.

Tie gates for each source's own A (l.77-82): G1 FAILS everywhere: kappa_eff M9 5.789 (+1.064 dex), M11 2.894 (+0.763), QI 1.091 (+0.339), QIe 3.692, QIc 1.080, F26 1.447 (+0.462). The fitted S9 A gives kappa_eff 0.651 (+0.114 dex, FAIL G1) and is 0.112 of R1's 2 a_L, 0.60 of R2's 2c^2/Theta, 0.45 of R3's a_L/2 (l.68). G2: Lambda rows 0.500 by construction (PASS); QI 0 (Theta fixed), QIc +0.722, +1.667 (FAIL). G3: Lambda rows flat by construction (PASS); QI rows (1 + z) 2.0, 2.5, 3.33 (FAIL). G4 per-galaxy effective a rms 0.029 to 0.053 dex over 79 hosts (PASS). G5 pass by posit (boost 0.44 to 1.17 a0 at 10 kpc). Solar system against A9's 1e-3 a0: every S9 row carries a constant anomaly A/2 at Saturn, 1.1 to 5.8 a0 (FAIL), 0.65 a0 at the fitted A (l.68); S11 2.4e-5 a0 (PASS). Control: the bare law at A0 also carries 1.00 a0 at Saturn (l.84), so this test does not separate the bare forms from the law; stated, not a verdict on the framework. Verdict: NO TIE for any source. Milgrom's numerical coincidence 2 pi a0 = c^2 sqrt(Lambda/3) (kappa 0.461, l.85, A13 T2) is not what R1's formula gives: R1's Eq. 9 a^0 is 4 pi times larger.

(c) GT in A29 backgrounds (l.87-135). L1, Lambda replaced by rho_DE(z) by hand (R1 does not allow this; derived in de Sitter only): GT 0.0000 in all eight backgrounds, G2z +0.5000 where measurable; G3 fails in B1u, B2, B3 only because rho_DE itself leaves A13's band (as A29 T2g). L2 (FRW horizon, A ~ H(z)): GT dev +0.40 to +0.64 dex at z 2.33 (FAIL everywhere). QIz (R2 Eq. 9, 1 + z): +0.37 to +0.62 (FAIL). QIp (physical horizon): +0.59 to +0.84 (FAIL). F26q (R3's deceleration form): q(z) > 0 at z 1, 1.5, 2.33 in every background, so a_bg is undefined there; today 2 a_bg 1.5 to 2.8 A0. So the only reading that tracks is the hand generalisation, by construction, and it carries G1 off by +0.34 to +1.06 dex.

Verdict A37: NOT EXACT and NO TIE. With the published constants (0 knobs) every source fails E1 by 0.09 to 0.41 dex. With one free constant the shared S9 shape comes closest of any one-knob shape in this folder (E1 0.0189, E2 0.0256, holdout 0.0195) but fails E3 (0.0273, no A passes all three); the free constant then has kappa_eff 0.65 and matches none of the sources' A (0.11 to 0.60 of them). The route's tie to Lambda passes G2 and G3 by construction (de Sitter), fails G1 by a factor 2.2 to 11.6 in a0, and tracks evolving rho_DE only by a hand generalisation the source does not make.

Deviations: none from the frozen rows. Post-hoc additions: the S9 A scan and the fitted-A gate line (l.67-68), and the F26q fix. Rival modified-inertia route, not LCDM.

Provisional: all source equations are WebFetch summaries of ar5iv/arXiv HTML (R1 astro-ph/9805346; R2 arXiv 1709.04918; R3 arXiv 2602.14515), not checked against the PDFs; R1's printed T_Lambda exponent 1/3 read as a typo; R3's title not recorded; Pikhitsa 2010 not found. The use of R1's linear-motion mu for circular orbits, the L2 horizon reading, and the QIc/QIp horizon readings are my choices, stated above. No downloads.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
