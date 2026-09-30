# Lane X2: gravitational analogues of collective frequencies and screening lengths (c = 1; Lambda = 8 pi G rho_Lambda; a0 = (1/2) sqrt(G rho_Lambda) = c^2/(2R*), R* = c/sqrt(G rho_Lambda))

## Bottom line -- verdict: SHARP NO-GO (scoped to the declared menu and to linear/hydrostatic response). Nothing derived; kappa = 1/2 stays FITTED.
1. None of the 20 pre-declared collective scales (plasma/Jeans frequency, Hubble/ESU/Nariai rates, free-fall, Jeans and Debye-type accelerations, omega^2 x length) equals a0; only the planted control hits. The two nearest are c H_Lambda/(2 pi) = 0.921 a0 (Milgrom's form with H_Lambda; Z/2 pi) and c^2/lambda_J = 1.128 a0 (Jeans length with c_s = c; = (2/sqrt(pi)) a0). Both are ordinary 2 pi/sqrt(pi) factors away, and a 'nearest entry within 13%' happens for about half of randomly rescaled menus, so it is not evidence. Every collective entry carries pi^(+-1/2, 1) relative to sqrt(G rho_Lambda) while a0 carries pi^0, so an exact match is impossible (Lindemann): a0/omega_J = 1/(4 sqrt(pi)), a0/H_Lambda = 1/Z.
2. The vacuum has NO Jeans/plasma frequency: gravity enters a fluid's own perturbations only through (1 + w); the Jeans wavenumber is k_J^2 = 4 pi G (rho+p)/c_s^2, which is exactly 0 at p = -rho. 4 pi G rho_Lambda = (3/2) H_Lambda^2 is not an eigenfrequency of anything in the vacuum. The point-mass field in the vacuum is exactly Kottler; its O(M) part is unmodified (no screening or anti-screening); the only exact numbers fixed by p = -rho are {0, -2, -1, 2/3} and none is a length.
3. A linear response cannot give a MOND-like force: it makes the force exactly linear in M (baryonic Tully-Fisher slope 2, MOND needs 4). For a 1/r force at r_M = xi R* at one mass it needs (rho+p)/(c_s^2 rho_Lambda) = 1/(4 pi xi^2) (= 1/pi at xi = 1/2: a chosen input containing pi, with w != -1). a0 is a nonlinearity scale; the plasma nonlinear scale (wave breaking) dictionary gives c omega_J = 4 sqrt(pi) a0.
4. Literature: no accepted analogy yields c^2/(2R*) (searched; sources below). The only place 4 pi G rho and Lambda meet in the literature I opened is the Einstein static universe (4 pi G rho_m = Lambda, rho_m = 2 rho_Lambda), which fixes a matter density, not a0.

## What I did (scripts here; `./run_all.sh` reruns everything, exit 0; 92/92 checks pass, each claim with at least one mutation/control that must fail)
Written FIRST: `PREDECLARED_MENU.md` (sha256 `62c23434...50b1fb`, stored in `PREDECLARED_MENU.sha256`, re-verified by every script): 22 entries (family V: c*omega for six rates; W: c^2/lambda with lambda = 2 pi c/omega; P: omega^2 x ell for four omega^2 and ell in {R*/2, R*}; R: reference c^2/R* and the planted target), the hit rule, decoy design. Disclosed there: the menu was written knowing the target.
| script | content | pass |
|---|---|---|
| `x01_fluid_perturbations_dS.py` | sub-horizon Newtonian-gauge fluid equations for general (w, c_s^2); known limits; gravity coupling only via (1+w); vacuum with chosen c_s^2; Heath growth; dust exponents in dS; vacuum active mass; ESU and Nariai rates | 36/36 |
| `x02_point_mass_in_vacuum.py` | SdS exactness; O(M) linear response of the vacuum (delta T = -rho h); exact TOV at p = -rho; Jeans/Yukawa Green's functions; M-scaling; exact-number inventory | 24/24 |
| `x03_what_it_would_take.py` | (target-known, labelled INPUT) what a linear response needs; 1/k susceptibility; wave-breaking dictionary; look-elsewhere check on a numerical coincidence | 20/20 |
| `x04_final_table.py` | the declared menu evaluated once, ranked, pi-classified, decoy sweep, shuffled-menu control (writes `x04_final_table.json`) | 12/12 |

## 1. Linearised dynamics (x01): where the vacuum can and cannot have rates
- Equations: delta' = -v - 3H(c_s^2 - w) delta, v' = -H(1 - 3 c_s^2) v + c_s^2 k^2 delta - (1+w) S delta, v := (1+w) theta, S = 4 pi G a^2 rho (Ma-Bertschinger form, rest-frame sound speed, sub-horizon, k^2 psi = -S delta). Derived symbolically to delta'' + A delta' + B delta = 0 (A = H(1-3w) and B = w k^2 - (1+w) S for c_s^2 = w). Checks: dust (B1b); radiation, the Hu-Sugiyama form (B1c); an exact clustering solution delta_X/delta_m = (1+w)/(1-3w) for c_s = 0 in matter domination (B2b), which reduces to 1 at w = 0 and 0 at w = -1. The (1+w) factor matches the clustering-quintessence continuity-equation factor in the abstract of arXiv:1101.1026 (opened); the ratio itself is my derivation, not a literature check.
- **Gravity enters only through (1+w)** (B3): d det(M)/dS = -(1+w), the matrix is S-independent at w = -1. Frozen dispersion omega^2 = c_s^2 k^2 - 4 pi G a^2 (rho + p), k_J^2 = 4 pi G (rho+p)/c_s^2. So the plasma analogy has the enthalpy rho+p where the plasma has n e^2/m; for the vacuum it is zero.
- The vacuum treated as a fluid with a chosen sound speed (B4): c_s^2 = -1 (delta p = -delta rho) is gradient-unstable at every k with rate k (real eigenvalues +-k), c_s^2 = +1 oscillates at +-i k; neither contains G rho. No acceleration scale.
- Dust in dust + vacuum (C1): Heath's D(a) satisfies the growth equation to 1e-29; the vacuum enters only through H(a); in pure dS growth is frozen (exponents {0, -2H}). Local exponent of a dust component in dS (C2): s = -H + sqrt(H^2 + 4 pi G rho_c), i.e. s/H = -1 + sqrt(1 + 3X/2), X = rho_c/rho_Lambda, a FREE ratio (coefficients are frozen; rho_c dilutes as a^-3). X = 2 (the mean density inside a zero-gravity radius) gives s = H_Lambda exactly.
- Task correction (D1): 4 pi G (rho + 3p) = -8 pi G rho_Lambda = **-Lambda**, not -2 Lambda (that needs Lambda = 4 pi G rho). The vacuum's Newton-Hooke field is g = +H^2 r, Poisson: laplacian Phi = -Lambda.
- ESU (D2): 4 pi G rho_c = Lambda (rho_c = 2 rho_Lambda), instability rate sqrt(Lambda) (= menu V2). Nariai (D4): f'' = -2 Lambda at r_N; the Kantowski-Sachs radius mode grows at sqrt(Lambda) (also V2); the static radius perturbation on dS_2 obeys box(dr) = -2 Lambda dr, i.e. the task's sqrt(2 Lambda) is the tachyonic MASS of that mode (V3), not a growth rate. (D4c checks one exact static solution; reading it as the l = 0 tachyon is the standard picture, not derived from the full linear system here.) V2 = sqrt(3) H_Lambda, V3 = sqrt(6) H_Lambda.

## 2. Static point mass in the vacuum, and what a response would do (x02)
- Kottler is exact (E1: G_mn + Lambda g_mn = 0 for f = 1 - 2GM/r - Lambda r^2/3; a wrong Lambda coefficient fails). Linearising in M (E2): the O(M) perturbation solves the equation exactly, and without the vacuum's covariant co-variation the residual is exactly -Lambda h_mn, so the vacuum's exact linear response is delta T_mn = -rho_Lambda h_mn (delta rho = delta p = 0). Newtonian reading: Phi = -GM/r - Lambda r^2/6, the 1/r coefficient is exactly GM for all Lambda. Exact TOV at p = -rho (E3): the hydrostatic equation is 0 = 0 and f is the SdS function with Lambda = 8 pi G rho.
- The Jeans swindle is exact and sign-reversed for the vacuum (E4): the background field is -2 x the field the same density would have as dust ((rho+3p)/rho = -2).
- For (rho + p) != 0 (E5): hydrostatic response c_s^2 delta rho = -(rho+p) phi with Poisson gives (nabla^2 + k_J^2) phi = 4 pi G M delta^3, k_J^2 = 4 pi G (rho+p)/c_s^2. c_s^2 > 0: phi = -GM cos(kr)/r (anti-screening); force GM[cos(kr)/r^2 + k sin(kr)/r], whose far field is a 1/r envelope of amplitude GMk oscillating in sign. c_s^2 < 0: Yukawa, m^2 = 4 pi G (rho+p)/|c_s^2|, but by x01 (B4a) a c_s^2 = -1 fluid is dynamically unstable at all k, so the static Yukawa is not a stable medium. Both reduce to -GM/r as (rho+p) -> 0.
- E6: both forces scale exactly as M^1 (d ln g/d ln M = 1); deep MOND is M^(1/2).
- E7, exact numbers fixed by p = -rho: rho + p = 0, (rho+3p)/rho = -2, c_s^2 = w = -1, H^2/(4 pi G rho) = 2/3. Only (rho+p)/c_s^2 = 0 enters a static field equation together with a length. So no exact number fixed by p = -rho makes a length, hence no 1/r force. (Honest note: (rho+3p)/rho = -2 numerically resembles the 4 = 1/(1/2)^2 in G rho = 4 a0^2 only as (1+3w)^2 = 4; that is a numerical resemblance of a rational, not a mechanism, and I do not use it.)

## 3. What it would take (x03; computed after the target is known; every entry is an INPUT)
- Anti-screening medium matched to deep MOND at ONE mass M_xi with r_M = xi R*: G M_xi = xi^2 R*/2, r_s = xi^2 R*; the envelope G M k = sqrt(G M a0) needs k = 1/(xi R*), i.e. **(rho+p)/(c_s^2 rho_Lambda) = 1/(4 pi xi^2)**, = 1/pi at xi = 1/2 (with c_s^2 = 1 that is w = -0.68 as an illustration). At xi = 1/2 the deep-MOND radius is 2 r_s, outside the weak-field hydrostatic derivation. The Yukawa force has no 1/r term ((1+mr)e^{-mr} = 1 - (mr)^2/2 + ...), and the anti-screened force has none at small kr.
- A chosen long-range susceptibility eps^{-1}(k) = 1 + 1/(k ell) gives g = GM/r^2 + (2/pi) GM/(ell r) (the 2/pi is a 3-D Fourier factor); matching MOND at one mass needs ell = (2/pi) r_M, which scales as sqrt(M): no fixed ell works.
- Nonlinear scale: cold-plasma wave breaking (Lagrangian density n0/(1 + d xi/dx0) diverges at kA = 1, so eE_wb/m = omega_p v_ph; I derived this rather than citing it), with the gravity dictionary omega_p^2 -> 4 pi G rho and v_ph = c (an input: the only speed of a Lorentz-invariant vacuum): a_wb = c omega_J = 4 sqrt(pi) a0 = 7.09 a0. The dictionary flips the sign (like charges attract), so the plasma oscillation becomes Jeans collapse and wave breaking becomes shell crossing.
- A numerical coincidence I found and calibrated: the dust exponent s = a0 needs rho_c/rho_Lambda = (2Z+1)/(16 pi) = 0.25022, within 0.09% of 1/4. Calibration (G5): about 2.2% of target multipliers t in [0.3, 3] have their X_t that close to a fraction with denominator <= 8; it is a target-known inversion of one of several possible criteria, and rho_c dilutes, so it is a coincidence, not a hint.

## 4. The table (x04; pre-declared menu, evaluated once). ratio = entry / a0; e = pi exponent relative to sqrt(G rho_Lambda) (a0 has e = 0)
| rank | id | entry | ratio to a0 | e |
|---|---|---|---|---|
| 1 | R2 | c^2/(2R*) (PLANTED target) | 1.0000 (hit) | 0 |
| 2 | W1 | c H_Lambda/(2 pi) = c^2/lambda, lambda = 2 pi c/H_Lambda | 0.9213 (-7.9%) | -1/2 |
| 3 | W4 | c^2/lambda_J, lambda_J = c sqrt(pi/(G rho_Lambda)) | 1.1284 (+12.8%) | -1/2 |
| 4 | W5 | c^2/(2 pi c/omega_K) | 0.6515 | -1/2 |
| 5 | W2 | sqrt(Lambda)/(2 pi) | 1.5958 | -1/2 |
| 6 | W6 | 1/(2 pi t_ff) | 0.5865 | -3/2 |
| 7 | R1 | c^2/R* (reference) | 2.0000 | 0 |
| 8 | W3 | sqrt(2 Lambda)/(2 pi) | 2.2568 | -1/2 |
| 9 | V6 | c/t_ff | 3.6853 | -1/2 |
| 10 | V5 | c sqrt(4 pi G rho/3) | 4.0933 | 1/2 |
| 11 | P3 | omega_K^2 R*/2 = (4 pi/3) G rho R*/2 | 4.1888 | 1 |
| 12 | V1 | c H_Lambda | 5.7888 (= Z) | 1/2 |
| 13 | V4 | c omega_J = c sqrt(4 pi G rho) (wave-breaking dictionary) | 7.0898 | 1/2 |
| 14-15 | P4, P5 | (4 pi/3) G rho R*;  H_Lambda^2 R*/2 | 8.3776 | 1 |
| 16 | V2 | c sqrt(Lambda) (ESU and Nariai growth rate) | 10.0265 | 1/2 |
| 17 | P1 | 4 pi G rho R*/2 | 12.5664 | 1 |
| 18 | V3 | c sqrt(2 Lambda) (Nariai tachyon mass) | 14.1796 | 1/2 |
| 19 | P6 | H_Lambda^2 R* | 16.7552 | 1 |
| 20-21 | P2, P7 | 4 pi G rho R*;  Lambda R*/2 | 25.1327 | 1 |
| 22 | P8 | Lambda R* | 50.2655 | 1 |
(Full table with all pi exponents: `x04_final_table.out`, `x04_final_table.json`.)
Calibration: exact hits {R2} only (planted control passes); mutating 4 pi -> 8 pi in V4 moves 7.09 -> 10.03, no hit; entries within 13% of a0 (excluding the planted one): W1, W4 (not independent: omega_J = sqrt(3/2) H_Lambda, both are c omega/(2 pi)). Decoy sweep: 14.7% (t in [0.2, 5]) to 17.4% (t in [0.1, 10]) of decoy targets have as many entries within 13% as a0 does (a0 at about the 83rd-85th percentile: not significant); shuffled-menu control: 53% of randomly rescaled menus have an entry within 13% of a0. Milgrom's coefficient appears as W1 (2 pi versus Z = 5.789), consistent with the known 2 pi versus sqrt(32 pi/3) comparison in the rest of the campaign; nothing here selects one of them.

## What is NOT established
- Only the declared 22 entries and hydrostatic/quasi-static linear response were examined. A different medium (nonlinear equation of state, an inertial vacuum such as a khronon/aether or a scalar with rho+p = phi-dot^2, collisionless Landau-type response with a Gaussian normalisation that could supply a pi^(-1/2)) is not excluded; the task's 'Landau damping' and 'Bohm-Gross' items give dimensionless functions of k lambda_D, no new acceleration scale, and are not in the menu.
- c_s = c is an input for every Jeans/Debye-type entry (the vacuum's only speed); c_s^2 = w = -1 would make lambda_J imaginary. The dS Hubble/ESU/Nariai rates need no such input.
- The pi-class argument is stated with G rho_Lambda as the held-fixed variable (audit H3). Ratios of physical accelerations are unit-independent: a0/H_Lambda = sqrt(3/32 pi) and a0/omega_J = 1/(4 sqrt(pi)) are transcendental; the puzzle asks for a mechanism that strips a factor sqrt(pi) (relative to omega_J) or supplies it (relative to the Jeans acceleration).
- The static Yukawa screening at c_s^2 = -1 is not a stable medium (x01 B4a); I did not treat time-dependent or nonlinear versions.
- Nothing bears on why kappa = 1/2.

## Literature (arXiv IDs opened; summaries mine)
- astro-ph/9910247 (Kiessling, abstract): a mathematically clean derivation of the Jeans dispersion relation by a limiting procedure that the abstract says vindicates the swindle; the matching of Lambda with 4 pi G rho_m is my D2, not read from the abstract. This is the only place I found where the plasma-like 4 pi G rho and Lambda meet; it fixes rho_m = 2 rho_Lambda, not a0.
- 1101.1026 (Sefusatti and Vernizzi, abstract): clustering of a zero-sound-speed quintessence enters through (1+w) Omega_Q/Omega_m, consistent with x01's (1+w) coupling.
- 0804.3518 (Blanchet and Le Tiec, abstract): dipolar-medium 'gravitational polarization' model; the abstract says Lambda is of the order of a0^2/c^4, an order-of-magnitude statement with no coefficient. 1403.5963 (Blanchet and Bernard, abstract): MOND as gravitational polarization, dielectric analogy; no a0 coefficient in the abstract.
- 2111.01700 (Roscoe, abstract): a characteristic acceleration a_F = 4 pi G Sigma_F from a mass surface density (the 'omega^2 x length' form of family P with rho ell = Sigma); Sigma_F is taken from galaxy data, no relation to rho_Lambda.
- 1110.2580 (Bernal et al., abstract): a0 'coincidence relations'; 1802.05670 (Mukherjee and Sengupta, abstract): wave breaking and phase mixing in relativistic plasma waves; its abstract does not state E_wb. The cold-plasma formula E_wb = m v_ph omega_p/e came from a search-result summary only (not an arXiv paper I opened), so I derived it (x03 G4).
- No opened source gives an acceleration equal to c^2/(2R*) from a collective analogy.

## Corrections of my own errors (kept visible)
- `x02`: first run failed 2 checks (E5e/E5f) because I took g = -dPhi/dr (signed) for the attractive magnitude; fixed to g = +dPhi/dr. A placeholder check (E5g) that could not fail was replaced by the actual hydrostatic+Poisson substitution.
- `x03`: G4a first evaluated the Jacobian at a phase where sin = 0 (wrong); fixed to the most compressive phase. G5b first asserted 'at least 3% of decoys do as well' with an arbitrary threshold; the measured fraction is 2.2%, so I restated it as a measurement (check band 0.5-10%, which is loose; the interpretation is in the text, not in the band).
- `x04`: my a-priori expectation that a0 is not special in the decoy sweep was WRONG (14.7-17.4% of decoys do as well, not >= 25%), so a0 sits around the 83rd-85th percentile; the check was rewritten to the measured statement 'above 5% in both sweeps', a threshold chosen after seeing the numbers (not significant either way). A placeholder mutation check was replaced by a real one.
- The task's '4 pi G (rho+3p) = -2 Lambda' is a slip: it is -Lambda (D1a).
- A web-fetch summary claimed that 0804.3518 'derives rather than fits' a coefficient; the abstract says only 'of the order of', so I use that.

## Verdict
SHARP NO-GO (scoped). The gravitational-plasma/Jeans/Debye/de Sitter family supplies no acceleration equal to a0; the vacuum's own Jeans frequency is exactly zero (rho+p = 0), its exact static response is the covariant contact term (Kottler, no screening); linear response cannot reproduce the M^(1/2) MOND scaling; and the plasma nonlinear scale is 4 sqrt(pi) a0 (the Jeans acceleration is (2/sqrt(pi)) a0), neither equal to a0. The collective analogy adds nothing to where the factor 1/2 can live beyond the campaign's earlier narrowing (a nonlinearity scale of an inertial medium, or a coefficient that must be supplied). kappa = 1/2 stays FITTED.
