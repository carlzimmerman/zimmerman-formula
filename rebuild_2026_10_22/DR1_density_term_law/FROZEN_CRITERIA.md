# DR1_density_term_law: FROZEN CRITERIA, committed alone before any script or number

kappa = 1/2 FITTED and unchanged. a0 canonical 9.3603e-11, alt 1.1312e-10 m/s2. No halo, no cold dark energy in any row: a law test. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** Read first: the closure table (law rms 0.054, Upsilon 0.52 / alt 0.44; "no cluster fit"), p33 and p34 (the coefficient-1 term), CFG117 and CFG231 (Verlinde form as mass additivity), X56 (law alone on clusters, G-OUT-all OVER), HS1 (law flat in surface brightness), and the abstract-level content of arXiv:2601.01715.

## Question
Does g_D^2 = a0 [g_b + (4 pi G r / 3) rho_b(r)] beat the plain a0 law on SPARC, and does it reach the law's cluster deficit? Source: an outside AI's text; a claim to test.

## Record check
- Coefficient 1 (Verlinde, g_D^2 = a_V [g_b + 4 pi G r rho_b]) in quadrature: p34 finds SPARC Delta chi2 +1389 (Upsilon fixed), +2216 (free), by its own lane V metric. CFG117/CFG231: mass additivity fails G1.
- Coefficient 1/3, the claim: **not on record.** So this door is new, and the coefficient-1 row is a cross-check on this lane's grader.
- Citation: Yoon, Han, Hwang, arXiv:2601.01715 exists (look-up, PROVISIONAL, preprint; no peer-reviewed version found). It reports 5.2 sigma (Stouffer; Fisher 4.5, binomial 4.0) for Verlinde over MOND in 23 dwarf spheroidals. Its form: g^2 = g_b^2 + g_d^2, g_d^2 = (a/6)(g_b + 4 pi G rho r), a = 5.41e-10. **That is the coefficient-1 form, not the claim's 1/3,** and with a different amplitude. It doesn't support the claim's coefficient. It compares a slope against MOND in dSphs; no dSph profile data here, no download; not regraded.

## Rule, fixed before any number
Definition of rho_b: spherically averaged, rho_b(r) = (dM_b/dr)/(4 pi r^2), with M_b(r) = r^2 g_b(r)/G, the spherical-equivalent mass. Then (4 pi G r/3) rho_b = g_b S/3 with S = dln M_b/dln r. dM_b/dr < 0 (gas dips) sets rho_b = 0. So g_s = g_b (1 + c S/3), with c = 1 the claim, c = 0 the plain law, c = 3 the Verlinde coefficient. No new number: c = 1 is the claim's, c = 3 the record's. No scan. For a true sphere M_b is the enclosed mass. On a disc it is a definition, not the enclosed mass; stated limitation. On SPARC S is by np.gradient of r^2 g_b along the rotmod radii at each Upsilon (as p34 does on log), no smoothing.

Combining with g_b. The claim gives only g_D. Three readings, each against its own c = 0 comparator:
- **R1, PRIMARY:** the record's kernel with the source swapped: g (g - g_b) = a0 g_s, g = g_b/2 + sqrt(g_b^2/4 + a0 g_s). c = 0 is EM1's LAW exactly. Deep limit is the claim's g_D^2 = a0 g_s.
- R2, reported: mass additivity, g = g_b + sqrt(a0 g_s).
- R3, reported: quadrature, g^2 = g_b^2 + a0 g_s (p33, and arXiv:2601.01715's combination).

## Runs
SPARC: 175 galaxies, Upsilon grid 0.30-1.20 per galaxy, EM1's fit_one, read from SL1's cache. Without a halo backgrounds A and B give the same numbers by construction; both footings reported. Tilt as UR1: median Upsilon (V_flat < 100) minus (V_flat > 150), Q <= 2, Inc >= 30. Surface-brightness slope as HS1 (law row, Upsilon 0.50, 2 R_d), reported.
Clusters: 15 keys through NF1's grader, one template, driver with its own cache, Mg500 x 10^0.005 (GS4) primary, 10^0.111 reported as a scale the data don't support, f* 0.034 and 0.0615, Msrc = r^2 g/G on the grader's baryons, canonical; alt reported.
X-COP: rows x <= 0.75, log10(M_HSE / M_law); M_b and S from each cluster's measured rows (gradient in ln r over its rows); HSE masses, as the gate does.
Reach: per row the S_req that would give M_HSE in R1; S_req > 3 cannot be reached at any density at c = 1.
Groups: Hernquist rows, S from M_H, NSG's class_stats, as UR1's _groups.
LITTLE THINGS: rows hold one point (R_max, V, M_b), no baryon profile, so S is undefined: **cannot be graded.** Reported bracket only: median E at S = 0, 1, 3, canonical.
Lensing beyond the discs: g_s = g_b wherever rho_b = 0, exact statement. S at each galaxy's last point reported. Not graded with KiDS.

## Pass lines (the record's)
SPARC rms <= 0.110 and Upsilon 0.50-0.80 at A and B; tilt |.| <= 0.15; 15 keys |Z| <= 2 at +0.005, both f*; X-COP |mean| <= 0.05, rms <= 0.10; groups |Z| <= 2; LITTLE THINGS |median E| <= 0.10 (not gradable).
IMPROVES: R1 c = 1 has lower rms than c = 0 on both footings AND keeps the line wherever c = 0 meets it.
CLUSTERS REACHED: X-COP line and all 15 keys at +0.005, both f*.

## Labels, on R1, c = 1, canonical
DOOR PASSES (all gradable lines) / SPARC HOLDS, CLUSTERS NOT REACHED (SPARC line, tilt hold, clusters not) / SPARC BREAKS, CLUSTERS NOT REACHED / SPARC BREAKS, CLUSTERS REACHED. Tag [READING-DEPENDENT] if R2 or R3 (against own comparator) changes the label. A pass would need smoothing and alt-footing stress before standing.

## Checks (failed check: no verdict)
K1 c = 0 on R1 reproduces P4/EM1's law: rms 0.054087 @ 0.52, 0.053718 @ 0.44, |d| <= 1e-6 in rms.
K2 unmodified grade_clusters reproduces NR1's cached preds at gas +0, f* 0.034, |d| <= 1e-6, and the live one-template against SL1's cached template.
K3 LITTLE THINGS c = 0 canonical against the closure table's median -0.025, |d| <= 0.001. K3b X-COP rows give the cached baseline when fed NR1's halo is not needed: rows are read from the cache unchanged.
K4 exact: uniform sphere, S = 3 at c = 1 equals the plain law at 2 a0, |d| <= 1e-9; point mass, S = 0, equals the plain law.
K5 HS1's law slope reproduced, |d| <= 1e-3.
K6 c = 3, R3 worsens SPARC against c = 0, R3, as p34 reports. If it does not, stop and read why.
MUTATE: S x 0 at c = 1 must return c = 0 exactly (control), and S -> 3 everywhere must drop Upsilon and move X-COP (it bites). Separate outputs.

## Expectation on record
SPARC: 1 + S/3 is 1 to 2, largest in rising inner parts, so Upsilon falls, canonical to about 0.40-0.50, likely off the line, rms slightly worse. Clusters: S about 1 to 1.5 near R500, g_D up about 15-20 %, against a deficit near a factor 2 or more in mass: not reached. Expect SPARC BREAKS, CLUSTERS NOT REACHED; SPARC HOLDS possible if the Upsilon drop is small. No-go ceiling: at c = 1 g_D rises at most sqrt(2).

kappa = 1/2 FITTED. Not theory closed.
