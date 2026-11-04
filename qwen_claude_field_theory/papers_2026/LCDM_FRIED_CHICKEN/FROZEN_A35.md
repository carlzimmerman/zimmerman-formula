# FROZEN A35: new uses of the LCDM ingredients that genuinely carry rho_DE, and the c-barrier

Frozen before any A35 number. Script `scripts/recipe36.py`, output `scripts/recipe36.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing: no A35 number computed. Order-of-magnitude reasoning done while designing, written here so it is not mistaken for a result: V200 of a 1e12 Msun halo is a few 1e-4 c; NFW central accelerations are of order a0 (A13, A15); in flat Lambda with no radiation, rho_m(a_DE) = rho_DE at a_DE, so rho_crit(a_DE) = 2 rho_DE and c H(a_DE) = sqrt(16 pi/3) c sqrt(G rho_DE) (algebra). From the record: A13 T2, A14 T7, A15 U1, A26, A27, A29 (no tracking; Lambda coincidence fails G5).

## Question
LCDM contains rho_DE (or Lambda) in its structure in several places. (a) List them with equations. (b) Build galaxy-radius accelerations a rival could write from them, in combinations not graded before, and grade each on G1 to G5 and GT. (c) The c-barrier: the tie a_T = kappa c sqrt(G rho_DE) is proportional to c; which LCDM constructions carry c at all, how, and by what factor does a halo construction miss it?

## Setup
Base cosmology lib.py (flat, H0 67.4, Om0 0.315, Ob0 0.0493, sigma8 0.811, ns 0.965, no radiation). Backgrounds B0 to B5 and footing P (primordial amplitude fixed at z = 30) taken unchanged from recipe31 (A29) by code slice; footing P is primary. Reference host M200c = 1e12 Msun. Diemer19 c(M, z) via colossus with the current cosmology set explicitly (A1 bug).

## (a) Inventory, printed with base values (no gate)
- I1 growth: D(z) and f(z) = d ln D/d ln a (colossus ODE); Lambda suppression g = D/a today against EdS (= 1).
- I2 freeze-out / maturity: collapse-epoch rule (NFW97, Bullock et al. 2001 type, FROM MEMORY): halo of mass M collapses at z_c with D(z_c) sigma_0(F M) = 1.686, F = 0.01, z_c >= z_obs; central density rho_s = C rho_crit(z_c). Once DE dominates, rho_crit(z_c) -> rho_crit(z_obs) and growth stops: the late-time floor. Printed: z_c(M), rho_crit(z_c)/rho_DE.
- I3 turnaround / zero-gravity: r_0 = (3 M/(4 pi rho_DE |1 + 3w|))^(1/3) (= (3 G M/Lambda c^2)^(1/3) for w = -1).
- I4 splashback (More, Diemer & Kravtsov 2015, FROM MEMORY): R_sp/R200m = 0.54 [1 + 0.53 Om(z)] [1 + 1.36 exp(-Gamma/3.04)], M_sp/M200m = 0.59 [1 + 0.35 Om(z)] [1 + 0.92 exp(-Gamma/4.54)], Gamma = 1.5 held fixed (provisional); M taken as M200m (stated approximation).
- I5 virial overdensity (Bryan & Norman 1998, FROM MEMORY): Delta_c = 18 pi^2 + 82 x - 39 x^2, x = Om(z) - 1, used also in w0wa backgrounds with that background's Om(z) (stated approximation).
- I6 Lambda force: (4 pi G/3) rho_DE |1 + 3w| r (= c^2 Lambda r/3 for w = -1) at 1, 10, 30 kpc.
- I7 DE-domination epoch: a_DE where rho_m(a) = rho_DE(a) (brentq), H(a_DE).

## (b) Constructions, M = 1e12 unless stated; prefactor knobs counted
- K1 g200 at a_DE: G M/R^2, R from 200 rho_crit(a_DE). 0 knobs.
- K2 NFW with rho_s = C rho_crit(a_DE) ("halos mature at DE onset"): c solves (200/3) c^3/mu(c) rho_crit(z) = rho_s; g_s = 2 pi G rho_s r_s. C calibrated once so c(1e12, z 0, base) equals Diemer19 (1 knob).
- K2b collapse-epoch NFW (I2): rho_s = C rho_crit(z_c), z_c from colossus sigma and D in each background; C calibrated as K2 (1 knob). This is the one native LCDM route where rho_DE reaches rho_s (through the floor).
- K3 V200 sqrt(G rho_DE): the tie with c replaced by the halo velocity. 0 knobs.
- K4 c H(a_DE) x p, p = 1/8 (the lattice element closest to giving kappa 0.5 analytically; 1 chosen knob).
- K5a g at the zero-gravity radius r_0 (A14 T7 in evolving DE). 0 knobs. K5b Lambda force at 30 kpc. 0 knobs.
- K6 g at splashback, G M_sp/R_sp^2 (I4). 0 knobs (+ Gamma held).
- K7 g at R_vir with Delta_c (I5) times rho_crit(z). 0 knobs.
- K8 MMW98 disc: V200^2/R_d, R_d = lambda R200/sqrt 2, lambda = 0.035 (j_d = m_d, f_c = 1, from memory). 0 knobs. K8b the same with R200, V200 at a_DE.
- K9 hybrid sqrt(g_s x c^2 sqrt(Lambda/3)), g_s Diemer19 NFW central, c^2 sqrt(Lambda/3) with rho_DE(z). 0 knobs.
- K10a c H(z) (1 - f(z)) x p; K10b c H(z) Om_DE(z) x p; p fitted so G1 is centred (1 knob each). Growth-suppression forms.
- Controls: TIE a_T itself; T2g Lambda coincidence (A29); g_s Diemer19 NFW central (A13 T3).

## Gates (fixed now; same as the brief)
- G1 kappa_eff = a(z 0, base)/(c sqrt(G rho_DE0)) within 0.05 dex of 0.5.
- G2 slope d ln a/d ln rho_DE0 = 0.50 +- 0.05, Lambda, f in {0.5, 0.71, 1, 1.41, 2}, A26 C1 physical footing, footing P (recipe31 mkP), M fixed.
- G3 a(z)/a(0) in [0.76,1.03], [0.71,1.12], [0.33,1.21] at z 1, 1.5, 2.33, base Lambda, M fixed.
- G4 rms of log a over log M200 11 to 12.5 (0.25 steps), z 0, base, <= 0.1 dex. Mass-free forms pass by construction (stated).
- G5 operative at 1 to 30 kpc in a typical disc host: (i) halo or disc gravity evaluated at a radius inside 1 to 30 kpc of the 1e12 host (K2, K2b, g_s at r_s; K8 at R_d): PASS if >= 0.1 a0 and the radius is printed inside 1 to 30 kpc; (ii) scales evaluated at R200, R_vir, R_sp, r_0 (K1, K5a, K6, K7, K8b at a_DE): FAIL, the scale lives at the halo edge or at another epoch, unless the radius is inside 30 kpc; (iii) Lambda/Hubble forms (K4, K5b, K10, T2g): the background force at 10 kpc (Lambda pull, or |q| H^2 r) must be >= 0.1 a0; (iv) products no LCDM force produces (K3, K9): FAIL.
- GT |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE0]| <= 0.05 dex at z 1, 1.5, 2.33 in B1 to B5 (footing P); B0 control. Epoch-fixed constructions (K1, K2, K4, K8b) are a single number, so a(z)/a(0) = 1 identically.
- A construction TIES only if G1, G2, G3, G4, G5 and GT (all of B1 to B5) pass; then, if it alters curves, E1 to E3 and holdout (fit on GS[::2], grade GS[1::2]) on SPARC by lib.grade.
- SPARC grade run regardless for the two curve-altering constructions K2 and K2b (NFW with that rho_s at each galaxy's SHMR M200, (1 - f_b) dark share, C fitted to the law: 1 knob), reported whether or not they pass the tie gates.

## (c) The c-barrier (fixed now)
- c1 dimensional statement: Newtonian structure formation (Vlasov-Poisson in a Friedmann background with rho_m, rho_b, rho_DE) contains no c. c enters LCDM structure only through (1) the horizon in the primordial normalisation, delta_k = (2/5) (c k/(a H))^2 R_k D T in the matter era, so P(k) proportional to c^4 at fixed dimensionless A_s; (2) horizon lengths in the transfer function (equality horizon, sound horizon), T(k) -> T(lambda k) under c -> lambda c at fixed densities. Together P_lambda(k) = lambda^(4 - ns) P_0(lambda k), hence sigma_lambda(M) = lambda^((1 - ns)/2) sigma_0(M/lambda^3): a halo of mass M behaves as a halo of mass M/lambda^3 does now (derived here; checked numerically by direct sigma integration on colossus's P(k)).
- c2 c-scaling test, gate reading GC (reported, not part of the tie verdict): d ln a/d ln c at fixed G, rho_i, H, A_s, ns, M, from lambda in {0.5, 2}. The tie, T2g, K4, K10 have GC = 1 identically (explicit c, rho_DE fixed). Halo forms: R200, V200 at fixed M carry no c (GC = 0: K1, K3, K5a, K6, K7, K8, K8b); concentration-dependent forms (g_s Diemer19, K2b, K9) through c(M) -> c_0(M/lambda^3) in a cosmology with sigma8 x lambda^((1 - ns)/2). Disclosed variant: amplitude channel alone (sigma8 x lambda^2, transfer held). A construction could be the tie identically only if GC = 1 +- 0.05 and it is a halo force at galaxy radii.
- c3 missing factor: V_eq = a/(kappa sqrt(G rho_DE)) is the velocity that replaces c; print V_eq/c and c/V200 for the 1e12 host, and factor g_s/a_T = (V200/c) x 10 sqrt(8 pi/3) x sqrt(rho_crit/rho_DE) x c^2/(2 mu(c)) / kappa, showing what makes up the c/V200 deficit.
- Also stated: if Lambda (not rho_DE) is held fixed, rho_DE = Lambda c^2/(8 pi G) and the tie scales as c^2; the halo forms then pick up c only through rho_DE.

## Expected in advance
K1 slope 2/3 (G2 fail), M^(1/3) (G4 fail), G5 fail. K2 G4 fail (g_s ~ r_s ~ M^(1/3)). K2b G3 fail (rises with H), G4 lean fail, GT fail. K3 kappa ~1e-3 (G1 fail). K4 passes G1 (0.51), G2 (0.5 exactly), G3 (flat), G4; fails GT in B1, B1u, B3 (flat while rho_DE moves) and G5 (Lambda pull 1e-5 a0): the Lambda coincidence again. K5 fails G4, G5. K6, K7 fail G4 and G5. K8 G2 near 0.46 (g200 ~ rho_crit^(2/3) at fixed M: (2/3) Om_DE), G3 fail (H^(4/3)), G4 fail. K8b flat, G4 fail. K9 G2 fail, G5 fail. K10 G3 fail. No construction TIES. c-barrier: halo GC between 0 and about 0.5, never 1; the c deficit c/V200 ~ 2e3 is made up by the overdensity and concentration factors, a numerical coincidence at our c and A_s. K2 and K2b fail E1 on SPARC (cusp, ~0.1 dex).

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

One run, 2 s, peak RSS 76 MB, single thread; no bug found, no wrong output to keep. Line numbers refer to `scripts/recipe36.out`. Controls: base c-grid equals lib's exactly, B0 footing-P sigma8 0.8110 (l.2); the TIE row returns kappa 0.5000, slope 0.5000, GT 0.000 everywhere (l.44-46); T2g reproduces A29 (0.4607, l.47); g_s Diemer19 reproduces A29 T3 (0.436, a(2.33)/a(0) 1.78, l.50).

(a) Inventory (l.5-23). I1 f(0) 0.531 (Om^0.55 0.530), Lambda suppression of D/a today 0.788 against the matter era. I2 collapse epochs (F 0.01): z_c 2.66, 1.90, 1.20, 0.54 at log M 11 to 14; rho_crit(z_c)/rho_DE 23, 12, 5.9, 2.7, so the DE floor only reaches cluster masses, not disc hosts. I3 zero-gravity radius of 1e12 at 1114 kpc (5x R200), g 1.2e-3 a0. I4 splashback 359 kpc, g 0.013 a0. I5 Delta_c 103.2 (EdS 177.7). I6 Lambda force 1.1e-6, 1.1e-5, 3.2e-5 a0 at 1, 10, 30 kpc. I7 z_DE 0.2956, rho_crit(a_DE) = 2.0000 rho_DE, c H(a_DE) = 4.0928 c sqrt(G rho_DE) (analytic sqrt(16 pi/3) 4.0933).

(b) Constructions (l.44-94; verdict table l.137, flags G1 G2 G3 G4 G5 GT). None TIES.
- K1 g200 at a_DE: 0.041 a0, slope 0.667, G4 0.167, edge at 190 kpc, GT fails B1/B1u/B3. Fails G1, G2, G4, G5, GT.
- K2 rho_s = 21423 rho_crit(a_DE): 0.872 a0 (kappa 0.436), slope +0.640, a(2.33)/a(0) 1.32, G4 0.167, G5 pass (r_s 25 kpc), GT fails. SPARC: E1 0.159 calibrated, 0.140 with C fitted, holdout 0.135. Fails.
- K2b collapse-epoch rho_s = 3498 rho_crit(z_c): kappa 0.436, slope +0.082, a(2.33)/a(0) 1.61, G4 0.081 (pass), G5 pass, GT fails by +0.07 to +0.30 at z 2.33. SPARC: E1 0.143 calibrated, 0.094 fitted (C 1358), holdout 0.092. Fails G1, G2, G3, GT, E1 to E3.
- K3 V200 sqrt(G rho_DE): 0.0010 a0 (kappa 0.0005): the tie with c -> V200 misses by about c/V200 (V_eq 9.5e-4 c).
- K4 c H(a_DE)/8: kappa 0.512, slope 0.500 exactly, flat in z, mass-free: passes G1 to G4; fails G5 (Lambda pull 1.1e-5 a0) and GT (a single epoch: B1 +0.088, B1p +0.076, B1u +0.096, B3 -0.154 at z 2.33). It is the Lambda coincidence with H(a_DE) = sqrt 2 H_Lambda and a chosen 1/8.
- K5a zero-gravity edge 0.0012 a0; K5b Lambda force at 30 kpc 3.2e-5 a0, slope 1. Fail.
- K6 splashback 0.013 a0, K7 R_vir 0.021 a0: rise 7.5 to 8x by z 2.33; fail every gate.
- K8 MMW98 V200^2/R_d: 1.34 a0 at R_d 5.2 kpc, kappa 0.672 (G1 fail), slope +0.453 (G2 PASS, as expected (2/3) Om_DE), a(2.33)/a(0) 5.33, G4 0.167, GT fails +0.6 to +0.8. K8b at a_DE: kappa 0.829, slope 0.667, flat, G4 fail, GT fail.
- K9 sqrt(g_s c^2 sqrt(Lambda/3)): kappa 1.12, slope +0.316, G4 0.044 pass, G5 fail (no process makes the product).
- K10a c H (1 - f), K10b c H Om_DE: G1 by construction (p 0.305, 0.209 fitted), slopes +0.770, +0.660, a(2.33)/a(0) 0.23, 0.29, G5 8.3e-6 a0. Fail.

(c) c-barrier (l.122-135 and the GC lines).
- c1 checked numerically: sigma_lambda(M) from direct integration of lambda^(4 - ns) P_0(lambda k) equals lambda^((1 - ns)/2) sigma_0(M/lambda^3) to 1e-4 at M 1e10, 1e12, 1e14, lambda 0.5 and 2 (l.123-125). So c enters LCDM halos only as the horizon (c/aH)^2 in the primordial normalisation and c/H in the transfer function, and together these act as a pure relabelling of halo mass in horizon units, M -> M/lambda^3.
- c2 GC = d ln a/d ln c at fixed G, densities, H, A_s, ns: TIE, T2g, K4, K10 = 1.000 (explicit c, all fail G5 or z gates); every R200/V200/edge/a_DE halo form (K1, K2, K3, K5, K6, K7, K8, K8b) = 0 exactly; concentration forms g_s 0.51, K2b 0.55, K9 0.76 (half explicit). Amplitude channel alone (disclosed variant) 2.7 to 2.8. No halo construction is proportional to c; the only GC = 1 forms are background (Hubble or Lambda) scales that act on nothing at galaxy radii.
- c3 missing factor (l.126-134): at 1e12, V200 142.6 km/s, c/V200 2102. g_s/a_T = (V200/c 4.76e-4) x 10 sqrt(8 pi/3) 28.9 x Om_DE^-1/2 1.208 x c_conc^2/(2 mu) 26.2 / kappa = 0.872: the c deficit of 2102 is met by 1832 from the overdensity definition, Om_DE and the concentration, none of which carries c. Over log M 11 to 12.5 c/V200 runs 4529 to 1432 while g_s/a_T runs 0.58 to 1.06, so the near-equality is a numerical coincidence at our A_s and our epoch, not a c sqrt(G rho_DE) law.

Verdict: NO CONSTRUCTION TIES. The places rho_DE enters LCDM structure (growth suppression, collapse-epoch floor, turnaround, splashback, Delta_vir, Lambda force, a_DE) either give galaxy-radius accelerations near a0 with the wrong rho_DE, z and mass scaling (K2, K2b, K8), or the right rho_DE scaling at the wrong place (K4, the Lambda coincidence again; Lambda force 1e-5 a0). The c-barrier holds: halo accelerations scale with c as 0 (virial forms) or about 0.5 (concentration forms), never 1; c reaches them only through horizon lengths acting as a mass relabelling. The one row passing G1 to G4 (K4) needs a chosen 1/8, fails GT in four of five evolving backgrounds and fails G5.

Deviations: (1) the frozen text listed K2 among the epoch-fixed single numbers; it is not, because its concentration is solved against rho_crit(z_obs), so a(z)/a(0) moves (1.11 to 1.32). Gates were applied as computed. (2) Expected K2b "G4 lean fail": it passes (0.081). (3) K8b passes G5 by the frozen rule (evaluated at R_d 5 kpc) although its halo is taken at another epoch; the row fails G1, G2, G4, GT anyway. (4) The TIE control fails G5 under the background-force rule, as the Lambda coincidence does: the law posits that its scale acts; LCDM supplies no force that does.

Provisional (from memory, not looked up): Bullock et al. 2001 / NFW97 collapse-epoch rule with F = 0.01; More, Diemer & Kravtsov 2015 splashback coefficients and Gamma 1.5; Bryan & Norman 1998 Delta_c, applied to w0wa with that background's Om(z); MMW98 lambda 0.035 and R_d = lambda R200/sqrt 2; DESI-like w0, wa as in A29. No web look-ups, no downloads.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
