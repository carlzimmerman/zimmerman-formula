# Lane N -- a factor-tracked Jacobson (Clausius) derivation in de Sitter: does an acceleration scale appear? (c = hbar = k_B = 1)

## Bottom line
- **With only Jacobson's own inputs (Unruh T, S = A/4G, dQ = T dS on horizons) and the exact de Sitter temperature T = sqrt(a^2+H^2)/2pi, there is NO crossover and NO correction to Newton's law.** Heat and temperature carry the same Tolman/Killing factor 1/sqrt(f0), so it cancels: the field equation is Einstein + Lambda for every a/H (Lambda an integration constant that the null-null equation cannot even see), and the entropic force T_loc dS/dl equals m a exactly, in dS and in Schwarzschild-dS (n03 C3, C4). The temperature structure T^2 = T_U^2 + T_Lambda^2 has exactly one model-free scale, T_U = T_Lambda at **a = H** (theta = 45 deg).
- A crossover appears only if a premise breaks that cancellation. Written as G_eff/G = kappa_heat/kappa_T (n03 C5), the six mismatched normalisations give: the LITERAL insertion (exact T into Jacobson's flat-space heat) is G_eff = G sin(theta): gravity is switched off below g_N = H (a threshold, opposite to MOND); exactly one mismatched pair has a Newtonian limit and enhanced gravity, **G_eff = G/sin(theta)** (= Milgrom's `a dT/da`), giving g_N = a^2/sqrt(a^2+H^2), **a0 = H exactly**, mu = x/sqrt(1+x^2). The other published conversion (`T - T_Lambda`) gives a0 = 2H with a constant extra acceleration H at high g.
- **Verdict: NOT a derivation. SHARP NO-GO (scoped to exact-dS Killing-horizon thermodynamics with Jacobson's inputs).** Four inserted premises (I1-I4 below), one of them selected by outcome. Result once they are granted: a0/H = 1 (or 2), with no free number and no 2 pi or 4 surviving; that is **Z = 5.79 times (or 2Z = 11.6 times) the framework's cH/Z**, 4.5-5.5x (9-11x) the SPARC yardstick, and pi-parity forbids any member of this form from landing on 1/Z. kappa = 1/2 stays FITTED.

## What I did
Read the brief, README sections 12-13 and lane E; opened arXiv gr-qc/9504004 (Jacobson) and gr-qc/9706018 (Deser-Levin, abstract: 2 pi T = sqrt(Lambda/3 + a^2), the 5-acceleration) to fix the inputs. Then four scripts (`run_all.sh` runs them, 3.8 s): **124 checks, 25 controls, all pass, exit 0** (n01 43/43, n02 24/24, n03 27/27, n04 30/30).

## Scripts
| script | what it establishes | result |
|---|---|---|
| `n01_dS_unruh_structure.py` | static-patch proper acceleration from the metric (a = H^2 r0/sqrt(f0)); embedding hyperbola A5^2 = a^2 + H^2; chordal distance -(4/A5^2) sinh^2(A5 tau/2); numerical detector response (w/2pi)/(exp(2 pi w/A5)-1) and detailed balance for four (a,H) pairs including H -> 0 (flat Rindler, T = a/2pi) and a = 0; Tolman T_GH/sqrt(f0) = A5/2pi; kappa_obs = a/sin(theta), tan(theta) = a/H; every geodesic has A5 = H; the horizon of every static observer is the SAME Killing horizon (area 4 pi L^2, entropy pi L^2/G, independent of a); distance to it (pi/2 - theta)/H with a l = 1 - eps^2/3, kappa l = 1 + eps^2/6; kappa_xi = H from the metric | 43/43, 6 controls (a^2 - H^2 sign, wrong Tolman direction, wrong period, a l = 1 exactly, ...) |
| `n02_jacobson_chain.py` | Raychaudhuri on a flat-FRW null congruence (exact, sigma = 0); the chain with symbols T = hbar kappa/c_T, S = A/(c_S G hbar) gives R_kk = c_T c_S G T_kk, **8 pi G iff (2 pi, 4)**; conservation makes Lambda an integration constant and R_00 = chi rho/2 (Poisson 4 pi G); FRW + Lambda from the Einstein tensor of the metric satisfies R_kk = 8 pi G T_kk only; de Sitter has R_kk = 0 for all H | 24/24, 8 controls (pi, 4pi, A/2G, A/8G, 4 pi G, 16 pi G) |
| `n03_dS_clausius_no_crossover.py` | Tolman cancellation Delta S = m/T_loc = 2 pi L m N; exact SdS first law dM = -T_c dS_c with S = A/4G, T = kappa/2pi (pins the '4' given the '2 pi'); entropic force T_loc dS_c/dl = m a for all a/H (naive 2 pi m T = m a/sin(theta) is not); SdS force = GR free-fall acceleration; G_eff/G = kappa_heat/kappa_T and the table of the six mismatched pairs | 27/27, 6 controls |
| `n04_conversion_and_crossover.py` | the two premise-dependent members with closed forms, limits and tails; the literal insertion (threshold at g_N = H); crossover measures; numbers on both footings; pi-parity | 30/30, 5 controls |

## Results, in order of derivation

**R1. Exact facts (n01).** Three things are called "acceleration" and must not be conflated: the proper acceleration a (relative to local free fall; the MOND-relevant one), the embedding/Unruh-effective A5 = sqrt(a^2+H^2) >= H, and the Killing surface gravity kappa (kappa_xi = H for the geodesic normalisation, kappa_obs = H/sqrt(f0) = A5 = a/sin(theta) for the normalisation unit at the observer). Free-falling observers (any geodesic) see T = H/2pi. The horizon of an accelerated static observer in dS is the same cosmological Killing horizon as the geodesic observer's: its area and entropy do not depend on a; only its distance, (pi/2 - theta)/H, and the normalisation of the boost do. The flat Rindler relations a = kappa = 1/l hold with relative corrections O(H^2/a^2).

**R2. Flat limit (n02).** The chain returns 8 pi G exactly; every wrong 2 pi or 4 is rejected. Honest limitation (B2d): the chain detects only the product c_T c_S, so (pi, 8) would pass; the two are fixed separately, 2 pi by the detector check with H -> 0 (n01 A4) and 4 by the exact first law (n03 C2).

**R3. The de Sitter Clausius relation has no acceleration scale (n03 C1-C5).** dQ is measured with the Killing field chi = xi/N0 (kappa_chi = kappa_obs), T with the same one; both scale as 1/N0, G_eff = G for every theta (C5c, all three normalisations). Independently, the entropic force with the exact T and the exact horizon-entropy gradient is m a (C3), and in SdS the GR force (C4). This answers "what replaces Jacobson's flat-space Rindler steps": the horizon (same for all a), its area and entropy (a-independent), its heat flux (Killing energy m N), its temperature (kappa_obs/2 pi): the Tolman factors cancel. Lambda enters only as the integration constant of the conservation step and is invisible to R_kk = 8 pi G T_kk (n02 B5), so thermodynamics does not tie any acceleration to Lambda. Caveat stated plainly: C3/C4 are close to identities (Tolman times E_K = m N); their content is that the Deser-Levin sqrt(a^2+H^2) IS the Tolman factor, so nothing extra is hidden in it.

**R4. Where a crossover can enter (n03 C5, n04 D7).** G_eff/G = kappa_heat/kappa_T with each kappa in {a, kappa_obs, H}:
| (heat, T) | G_eff/G | a >> H | a << H | reading |
|---|---|---|---|---|
| any equal pair | 1 | 1 | 1 | consistent Jacobson |
| (a, kobs) | sin(theta) | 1 | 0 | **literal insertion**: exact T into flat-space heat. Same law as the Verlinde-type screen F = 2 pi m T = m g_N (n04 D7b): a^2 = g_N^2 - H^2, no static solution for g_N < H. Threshold, not MOND |
| (kobs, a) | 1/sin(theta) | 1 | infinity | the only pair with Newtonian limit AND enhancement; = Milgrom's `a dT/da` (n04 D1a) |
| (a,H), (kobs,H), (H,a), (H,kobs) | tan, 1/cos, cot, cos | no Newtonian limit or no enhancement | | rejected |
The filter in the last two rows is by OUTCOME (Newton limit + MOND direction). Nothing in the Clausius chain selects the pair; it is an INPUT.

**R5. The two conversions to a force law (n04 D1-D4).** (ii) G_eff = G/sin(theta): g_N = a sin(theta) = a^2/sqrt(a^2+H^2), a^2 = [g^2 + sqrt(g^4+4g^2H^2)]/2, deep limit a^2 = g H (**a0 = H**), tail a - g -> H^2/(2g) (quadratically small), half-point a = H/sqrt3. (i) `T - T_Lambda`: sqrt(a^2+H^2) - H = g_N, a = sqrt(g^2+2Hg), **a0 = 2H**, but the tail is a CONSTANT extra acceleration a - g -> H (relative correction H/g, linear). The value of a0/H is set by the (input) functional, not by T: slope-defined 1 or 2, half-point 0.577 or 1.333, temperature equality 1. All are O(1) x H because the only ratio available is T_U/T_Lambda = a/H; the framework's 1/Z would sit at theta_0 = arctan(1/Z) = 9.8 deg, an unnatural angle.

**R6. Comparison, made only after R1-R5 were fixed (n04 D5, D6).** c H0 = 6.548e-10, c H_Lambda = 5.420e-10 m/s^2 (H0 = 67.4, Omega_L = 0.685; as lane E). SPARC yardstick 1.2e-10 (as lane E; only a yardstick).
| | a0 (H0 / H_Lambda footing) | / SPARC | / framework cH/Z |
|---|---|---|---|
| member (ii) cH | 6.5e-10 / 5.4e-10 | 5.5 / 4.5 | Z = 5.79 |
| member (i) 2cH | 1.31e-9 / 1.08e-9 | 10.9 / 9.0 | 2Z = 11.58 |
| framework cH/Z | 1.13e-10 / 9.36e-11 | 0.94 / 0.78 | 1 |
In the pi-free variable a0/sqrt(G rho_L): (ii) sqrt(8pi/3) = 2.894, (i) 5.789, framework 1/2. (2 sqrt(8pi/3) = Z is a coincidence of how Z is defined; it does not make member (i) "contain" the framework.) pi-parity (D6): every member has a0 = qH with q rational, so a0^2/(G rho_L) = q^2 (8pi/3) carries one pi; the framework's 1/4 carries none; 1/Z = sqrt(3/32pi) is not rational (PSLQ finds no relation, control passes). The step that would need adding is not a normalisation but a pure number sqrt(pi) in a0/H, which no ratio of temperatures can supply (the 2 pi and 4 cancel between T and dQ; they survive only inside H^2 = 8 pi G rho/3).

## Premise ledger (everything beyond Jacobson's own T, S, dQ = T dS, local flatness, conservation)
- **I1 (acceleration transfer).** The a in T(a) is the test body's own proper acceleration in the galaxy field, and the exact-dS Deser-Levin formula (derived for M = 0, a = acceleration relative to dS geodesics) applies there. In Jacobson's chain the auxiliary observer's a is integrated out (kappa cancels); making it physical is new.
- **I2 (Killing-normalisation split).** Heat with the full kappa_obs, temperature with the acceleration part T_U = a/2pi only (equivalently `2 pi a dT/da`; or, for member (i), only the excess T - T_Lambda acts). Selected among six by outcome.
- **I3 (local G_eff in the Poisson/Gauss law).** a = G_eff(a) M/r^2 with an acceleration-dependent coupling. A coupling that depends on a body's acceleration is not a field of the metric; consistency with the Bianchi/conservation step of the chain was NOT checked.
- **I4 (which H).** T_Lambda = H_Lambda/2pi (event-horizon constant, gives flat a0(z)) versus a Hubble-rate H(z) (the rival). Not derived here.
Count: **4** (three if I3 is granted as part of the Newtonian limit), against 5-6 for Verlinde and van Putten per lane E. Note also unlisted scope limits: static/linear acceleration (circular motion differs by O(1), per lane E) and exact dS only.

## Not established / caveats
- The detector response (n01 A4) assumes the Bunch-Davies Wightman function of a conformally coupled scalar is 1/(chordal distance)^2 (standard; only the chord and the resulting KMS structure are verified). The lemma "R_kk = chi T_kk for all null k implies R_mn - chi T_mn is proportional to g_mn" is standard and not scripted; n02 B3 checks only the algebra after it.
- The linear-response coefficient S_c = S_dS - E_K/T_H (used in C3) is checked only at M = 0 origin (C2c) and assumed for E_K = m N; the SdS extension (C4) uses Tolman with the cosmological-horizon temperature.
- I did not compare the members' Solar-System tails with any ephemeris bound (values quoted in n04: member (i) constant c H0 = 6.6e-10; member (ii) 3.3e-15 m/s^2 at Saturn). That is a follow-up, not a result.
- Nothing here shows that no derivation of kappa = 1/2 exists; it shows that Jacobson's inputs in exact dS contain no such factor, and that the natural conversions land on a0 = cH or 2cH, i.e. off by Z or 2Z.

## Errors fixed openly
First run: 3 checks failed in n01 (sympy could not simplify sqrt of a quantity with unknown sign; fixed by working with the positive root H/sqrt(f0) fixed by A2c/A2d), n04 D1c/D2a failed for the same reason (replaced by the squared identity plus numerical spot checks); an early version of A3 was a single-point evaluation (replaced by three points and the KMS periodicity). n02's B2d records a limitation I discovered while writing the controls (only the product c_T c_S is tested). The literal-insertion result (D7, gravity switched off below g_N = H) was not what I expected when I started; I expected the mismatch to enhance gravity, and only the (kobs, a) pair does.

## Verdict
**SHARP NO-GO** (scoped). Jacobson's chain in exact de Sitter yields Einstein + Lambda for every acceleration, with no crossover and no tie between a and Lambda; every MOND-type law from the T^2 = (a^2+H^2)/4 pi^2 structure needs 4 inserted premises, gives a0 = cH or 2cH (Z or 2Z above the framework's cH/Z, 5-11x above the data yardstick), and is excluded from equalling the framework by pi-parity. kappa = 1/2 stays FITTED.
