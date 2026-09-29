# Lane H -- string / heterotic gauge-gravity relations: pre-registration

Written 2026-09-28 BEFORE any script in this directory was run. Amendments are appended at the bottom, never edited in place.
Target if a value were forced: alpha = 1/137.035999177 (Thomson limit). Every relation below is a tree-level relation at the string / unification scale;
the scale statement for each claim is part of the claim.

## Sources read BEFORE registering (what was actually read)
FULL TEXT (pdftotext of the arXiv PDF, read in the sections used):
* arXiv:hep-th/9602045 (Dienes, "String theory and the path to unification", Phys. Rept.): Sect. 2 (tree-level relation, Eq. 2.6, 2.10), Sect. 5 (k_Y, Eq. 5.1-5.23),
  Sect. 6.3-6.4 (thresholds, Eq. 6.16-6.23), Sect. 8.3 (dilaton runaway), Sect. 10 (Type I and M-theory relations, Eq. 10.1-10.6).
* arXiv:hep-th/9602070 (Witten, "Strong coupling expansion of Calabi-Yau compactification"): Introduction, Eq. 1.1-1.15 (tree-level and strong-coupling relations, bounds).
* arXiv:hep-th/9205068 (Kaplunovsky, ERRATA to Nucl. Phys. B307 (1988) 145): the corrected Eq. (26) for the unification scale and the tree-level relation k_a g_a^2 = 32 pi/(alpha' M_P^2);
  the erratum text only -- the 1988 paper itself is NOT on arXiv and was NOT read.
ABSTRACT ONLY: hep-th/9605136 (Banks-Dine), hep-th/0105097 (Giddings-Kachru-Polchinski), hep-th/0301240 (KKLT), hep-th/0404116 (Denef-Douglas), hep-th/9402002 (Sen S-duality).
NOT READ, RECALLED (labelled RECALLED wherever used): Ginsparg 1987 (Phys. Lett. B197, 139), Green-Schwarz 1984, Dixon-Kaplunovsky-Louis 1991 (only via Dienes 6.19-6.21),
Dine-Seiberg 1985 dilaton-runaway theorem (only via Dienes' citation), Font-Ibanez-Luest-Quevedo 1990 duality-invariant condensation, racetrack literature.

## Hypotheses (to be checked, not assumed)
H1 (structure): in weakly coupled heterotic string theory the tree-level relation ties alpha_G to G_N and the STRING SCALE, alpha_G = c * G_N * M_s^2 with a convention-dependent O(1) constant c
   and level factor k. It therefore converts the dimensionless alpha_G into the dimensionful ratio M_s/M_P; alpha_G itself is the 4D dilaton (one real modulus). Free: (dilaton, V/alpha'^3, alpha').
   Forced: only the integer/rational levels k_a and the one relation M_s(G_N, alpha_G). At strong coupling (Type I, Horava-Witten) the M_s relation is lost too (Jacobian rank 3).
H2 (levels): k_Y = 2 sum a_i^2 is a discrete, embedding-dependent rational (5/3, 77/48, 11/3, 14/3 ...), not a number chosen by a principle; changing it changes alpha_em(M_s)/alpha_G by an O(1) factor.
H3 (data count): with k_a fixed and Lambda = 5.27e17 GeV * g_string tied to g_string, the three low-energy couplings have ONE unknown (g_string): two predictions. Those predictions are known to fail
   (Dienes: about 7 sigma at k=(5/3,1,1)); the freedom needed to repair them is three model-dependent threshold constants Delta_{Y,2,3}, i.e. as many unknowns as data: no prediction of alpha survives.
H4 (the decisive question): NO string mechanism on the declared list forces the dilaton or the volume to a number that reproduces alpha at 1e-3. Specifically: (a) T-duality/fermionic self-dual points fix Kahler/complex-structure
   moduli, never the 4D dilaton; (b) S-duality fixed points give alpha_G^-1 = O(1); (c) gaugino-condensation/racetrack fix S only through non-universal prefactors that are free;
   (d) flux stabilisation fixes tau through integers with a huge number of choices; (e) Horava-Witten replaces the equality by an inequality (critical G_N).
Expected overall outcome: NO forced principle. The lane converts the freedom in alpha into freedom in (dilaton vev, threshold constants, discrete embedding).

## Scripts, declared checks, pass/fail (each: python3, exit 0; MUTATE argv ends in MUTATE and must exit 1; .out saved)
### h1_tree_relations.py (sympy, mpmath)
* R1 Reproduce Witten Eq. 1.4 -> 1.5 (G_N = alpha_G alpha'/4) and the strong-coupling forms (Eq. 1.10-1.11 Type I, Eq. 1.13 Horava-Witten) from the printed formulas; sympy Jacobian rank of the maps
  (phi, V, alpha') -> (G_N, alpha_G, M_KK = V^(-1/6)): heterotic, Type I, Horava-Witten (kappa, V, rho). PASS if ranks are (3,3,3) i.e. no EQUALITY among (G_N, alpha_G, M_KK) in any regime;
  the only tree-level equality is the definition of alpha' (M_s) in terms of G_N and alpha_G (heterotic, Type I); Horava-Witten has no such relation (M_s not defined).
* R2 Convention table: kappa^2/alpha' = 8 pi G_N/alpha' as a multiple of g^2 in three sources: Kaplunovsky erratum (1/4), Witten Eq. 1.5 (1/2), Dienes Eq. 2.6 (1). Report ratios; state that they are
  convention (generator normalisation and alpha' definition) offsets that this lane could NOT resolve from the papers alone. Effect on the alpha prediction is computed in h3.
* R3 Kaplunovsky's corrected Eq. (26): Lambda = 2 e^{(1-gamma)/2} 3^{-3/4}/sqrt(2 pi alpha') = e^{(1-gamma)/2} 3^{-3/4} g M_P/(4 pi) = 5.27e17 GeV * g (with M_P = 1.2209e19 GeV, and k g^2 = 32 pi G/alpha').
  PASS if the numerical coefficient equals 5.27e17 within 0.3 percent (from the closed form) AND the algebra 2c/sqrt(2 pi alpha') with alpha' = 32 pi G/g^2 reproduces c g M_P/(4 pi) symbolically.
* R4 Witten's inequalities G_N >= alpha_G^(4/3)/M_GUT^2 (1.7), G_N >= alpha_G^2/M_GUT^2 (1.14) evaluated with alpha_G = 1/25, M_GUT = 2e16 GeV, O(1) factors dropped as printed. REPORTED, not scored.
* MUTATE: drop the factor 2 in Lambda (the pre-erratum form); R3 must fail.

### h2_hypercharge_levels.py (sympy)
* L1 Build the 16 of SO(10) from the spinor weights (+-1/2)^5 with an even number of minus signs; hypercharge Y = a.q with a = (1/3,1/3,1/3,1/2,1/2); PASS if the SM multiset is reproduced
  (Y_eR = 1 normalisation) and k_Y = 2 sum a_i^2 = 5/3 exactly.
* L2 The Dienes Eq. 5.18/5.19 embedding a = (5/12,5/12,5/12,3/8,3/8): PASS if k_Y = 77/48 (and its charges reproduce Eq. 5.18's rows through Y = a.Q; the multiset check is done on the given rows).
* L3 tree-level ratios: sin^2 theta_W(M_s) = k_2/(k_2+k_Y), alpha_em(M_s) = alpha_G/(k_2+k_Y): tabulate for k_Y in {5/3, 77/48, 11/3, 14/3}, k_2 = 1. Declared list = 4 values, NOT scored against alpha (these are not hit searches);
  PASS if k_Y = 5/3 reproduces 3/8 exactly.
* L4 Modular-invariance / no-fractional-charge condition k_3/3 + k_2/4 + k_Y/4 = 0 mod 1 (Dienes 5.22): list the allowed k_Y for (k_2,k_3) in {(1,1),(2,2)}, k_Y < 6. Minimum equals 5/3 and 10/3.
* L5 Green-Schwarz counting: dim SO(32) = dim E8 x E8 = 496; STATEMENT of structure: the counterterm is quantised in integers and has no free continuous coupling (RECALLED, not derived; flagged in the .out).
* MUTATE: k_Y = sum a_i^2 (missing factor 2): L1 must fail.

### h3_string_unification_running.py (numpy/mpmath; inputs declared MEASURED, not derived)
Inputs: m_Z = 91.1876 GeV; alpha_em^-1(m_Z)_MSbar = 127.955; sin^2 theta_W(m_Z)_MSbar = 0.23122; alpha_s(m_Z) = 0.1179; M_P = 1.2209e19 GeV.
Equations (Dienes 5.8, one-loop, MSSM from m_Z; b = (11, 1, -3) in Y/2/3 normalisation):  alpha_i^-1(m_Z) = k_i/alpha_G + (b_i/2 pi) ln(Lambda/m_Z) + Delta_i/(4 pi),
Lambda = 5.27e17 GeV * sqrt(4 pi alpha_G).  k = (5/3, 1, 1).
* S1 (V1 pure one-loop, Delta=0): three single-input solves (input alpha_em, or sin^2 theta_W, or alpha_s; predict the other two). 3 solves x 2 predictions = 6 numbers. Declared expectation: predictions miss by >> 1e-3 (score: relative offset from measured).
* S2 (V2): same with the model-independent two-loop+Yukawa+scheme corrections quoted in Dienes Eq. 5.12 (Delta_Y, Delta_2, Delta_3) = (11.6, 13.0, 7.0). 6 more numbers. Trial count for S1+S2 = 12 predictions.
* S3 (data count): with Delta_Y, Delta_2, Delta_3 free, the 3 equations determine (alpha_G, Delta-combinations): report the required Delta_Y - Delta_2 etc. and that any measured triple is fitted exactly. Check the counting by sympy rank of the linear system.
* S4 alpha at Thomson: with a predicted alpha_em^-1(m_Z) (each variant) run to q^2 = 0 using one-loop QED with the measured lepton masses (m_e, m_mu, m_tau) and the measured hadronic piece
  Delta alpha_had^(5)(m_Z) = 0.02766 (RECALLED from the standard e+e- compilations; an input, not derived); report alpha^-1(0) and its offset from 137.036 for each variant (no score threshold beyond the 1e-3 rule).
* S5 requirement statement: the alpha_G^-1 precision (+-0.048 for 1e-3 in alpha(0) at fixed spectrum) versus the threshold uncertainty. REPORTED.
* S6 convention sensitivity: change c (R2) by the factor between sources (x2, x4) -> the shift of alpha_em^-1(m_Z); PASS (as a sensitivity statement) if the shift exceeds the 1e-3 window (so the tree-level relation cannot be scored at 1e-3 without a fixed convention and a computed threshold).
* MUTATE: flip the sign of b_2 (declared): the S1 alpha_s-input solve must then fail the self-consistency residual check.

### h4_dilaton_volume_fixers.py (sympy, mpmath, numpy)   -- THE DECISIVE QUESTION
Declared candidate list (8 handles, no additions after seeing results):
* D1 T-duality self-dual radius / free-fermionic point: sympy shows alpha_G(S,T) at tree level is independent of T (Re S universal), so the fixed point fixes threshold pieces only; compute the fixed-point values of
  ln(Im T |eta(T)|^4) for T = i and T = exp(i pi/6) (numbers, Dienes 6.19) and compare with the required threshold size (6.18: 28-58): PASS(no-go) if the achievable moduli-dependent piece is smaller than the required by >5x
  for any reasonable b' coefficient (|b'| <= 10 declared) -- the constant X in 6.19 is model dependent and stays free. Also show that at a literal self-dual torus (2 pi sqrt(alpha'))^6 the weak-coupling relation gives alpha_G <= 3e-7
  (Witten convention, e^{2 phi} <= 1) -- a REPORTED statement about (2 pi)^6 factors, convention-dependent.
* D2 S-duality fixed points S = i and S = exp(2 pi i/3) (SL(2,Z), Im S = 1 and sqrt(3)/2), two conventions (alpha^-1 = Im S with S = 4 pi/g^2 + i theta/2pi; alpha^-1 = 4 pi Im S with S = 1/g^2): 4 numbers alpha_G^-1;
  also alpha_em^-1(M_s) = (8/3) alpha_G^-1: 4 more. Scored (1e-3) against the h3-solved alpha_G^-1 (one-loop MSSM crossing at levels (5/3,1,1), input alpha_em(m_Z)) and against 137.036: 8 x 2 = 16 comparisons.
* D3 Gaugino condensation / racetrack: sympy: single condensate W = A e^{-a S}, K = -ln(S+Sbar): no finite SUSY minimum (runaway); two condensates: S_0 = ln(a_2 A_2/(a_1 A_1))/(a_2 - a_1) (real S; conventions RECALLED, derived here by sympy);
  a_i = 8 pi^2/N_i. Report dS_0/d ln(A_2/A_1) and the required precision of A_2/A_1 to hold alpha_G^-1 to 0.048 (needed for 1e-3): FAIL(no forced number) if the prefactors A_i are free (they are: threshold-dependent, not computable in this lane).
* D4 Flux stabilisation of the dilaton (GKP/KKLT class; abstract-level only): STRUCTURAL counting only: alpha is a function of flux integers; number of vacua needed for one chance hit in the 1e-3 window = 1/8.7e-4 = 1150. No model is computed.
* D5 Horava-Witten critical G_N (Witten 1.15): alpha_G^crit(I) = 4 pi M_GUT sqrt(G_N/I) (Witten convention, I the integral of Eq. 1.15 in units M_GUT^-2): evaluate at I = 1; UNSCORED order-of-magnitude, it is an inequality.
* D6 Dilaton runaway theorem (Dine-Seiberg; via Dienes 8.3, RECALLED): potentials vanish as <phi> -> infinity; a quantitative toy: V = A e^{-a S} single term: dV/dS != 0 for all finite S with a A != 0. Statement-level, from D3's sympy.
* D7 Type I self-duality: the 10D SO(32) heterotic <-> Type I map phi_I = -phi_h exchanges DIFFERENT theories; no fixed point exists; e^{phi} = 1 is not selected (statement; Jacobian rank result from h1).
* D8 Vacuum-independent uniqueness: heterotic dilaton is the only modulus multiplying tr F^2 at tree level (universality); nothing in the internal CFT (Gepner/fermionic points) depends on it: sympy on the tree-level gauge kinetic function f_a = k_a S.
TRIAL COUNT for scored comparisons: D2 = 16, h3 S1+S2 = 12 predictions => 28 scored comparisons. Chance-hit probability per comparison at the 1e-3 rule (log-uniform prior over one decade): 2e-3/ln 10 = 8.7e-4;
expected chance hits = 28 x 8.7e-4 = 0.024. A hit would be reported as a hit inside a 28-trial family and NOT as a derivation (no forced M_s threshold, no forced spectrum).

## Overall pass/fail (declared now)
The route "yields a forced principle that fixes alpha" only if some handle on the h4 list forces the dilaton (or the combination V e^{-2 phi}) to a definite number that, with fixed integer levels and the standard one-loop spectrum
and measured charged masses, reproduces alpha(0) at 1e-3, with no free constant, no choice made after seeing the target, the declared trial count and the scale stated. DECLARED EXPECTED OUTCOME: NO.

## Scope / not tested
Two-loop string thresholds beyond Dienes 5.12, actual orbifold model building, moduli stabilisation with fluxes (no vacuum computed), the SM mass sector (walled), kappa = 1/2 (fitted), non-supersymmetric strings, the Horava-Witten nonlinear terms.
No dark-matter species is introduced. Amendments below.

## Amendment 1 (appended after the first run of h1; nothing above was edited)
* h1 R4 was pre-registered as REPORTED, not scored. The first version of the script nevertheless contained an unregistered `chk` with guessed thresholds ("weak-coupling bound > 100x, strong-coupling bound < 100x");
  it FAILED (the printed order-of-magnitude bounds are 5100x and 600x G_N, because the printed forms drop the 1/(16 pi^2) that Witten's Eq. 1.15 carries). The check was REMOVED (not tuned); R4 now reports the numbers, including
  the Eq. 1.15 value (integral set to 1, an unknown O(1) factor): 3.8x measured G_N. Nothing in the verdict depends on R4.
* h1 first run crashed on an mpmath format string (not a check failure); fixed to plain floats. The MUTATE run was repeated after the fix (a crash is not a valid failure of a control).

## Amendment 2 (appended BEFORE the first run of the committed h3; nothing above was edited)
* I ran a throw-away exploration of the h3 equations (scratchpad, not committed) before finalising h3, to see whether the system has a unique root. What it showed, declared here so it cannot influence scoring:
  the alpha_s-input solve at k = (5/3,1,1), Delta = 0 predicts alpha_em^-1(m_Z) = 137.0, numerically close to the Thomson value 137.036. THIS IS A DIFFERENT SCALE (the measured MSbar value at m_Z is 127.955) and is a coincidence
  of the accidentally-close one-loop numbers; it is scored against 127.955 (a 7 percent miss), never against 137.036. The Thomson step (S4) adds the measured 9.081 and gives about 146, a 6.6 percent miss.
  The 137.0 is NOT counted as a hit and is flagged in the .out. No handle, criterion or trial count was changed by this.
* S4 design: the M_Z -> Thomson step is NOT derived to 1e-3 here. The measured difference alpha^-1(0) - alpha^-1_MSbar(m_Z) = 137.035999 - 127.955 = 9.081 is used as the low-energy SM input; the script also decomposes it
  (one-loop leptons with measured masses = 4.836; hadronic from the RECALLED Delta alpha_had^(5) = 0.02766 with the OS->MSbar constant 55/(27 pi)) and reports that the decomposition reaches 9.275, the difference (0.19, about 1.5e-3 of alpha^-1)
  being the W/top and scheme conventions of the quoted MSbar value. So the Thomson step itself carries an irreducible ~1.5e-3 scheme ambiguity in this lane; the verdict never depends on it.

## Amendment 3 (appended after the runs of h2, h3 and h4; nothing above was edited)
* h4 was pre-registered WITHOUT a MUTATE control (an omission against the lane rules). Declared now, before any claim rests on h4: `python3 h4_dilaton_volume_fixers.py MUTATE` uses K = -2 ln(S+Sbar) in D3 and a wrong Type I volume map (V_I = e^{-2 phi} V_h) in D7;
  checks D3b and D7a must FAIL (they do; exit 1). The .out of that run is saved.
* D1: the pre-registered second SL(2,Z) fixed point "T = exp(i pi/6)" is a typo/convention slip (in the upper half plane the fixed points are i and exp(2 pi i/3)). The script uses exp(2 pi i/3) and prints exp(i pi/6) only for transparency; D1 is not a hit search, so no trial count changes.
* D1c pre-registered criterion (required threshold size exceeds the reachable moduli-dependent piece by >5x for |b'| <= 10): NOT MET. Ratio 3.3 (required >= 35.04 units of 16 pi^2/g^2 from h3 S3; reachable |b'| |ln(Im T |eta|^4)| <= 10.5 at T = i, 10.3 at exp(2 pi i/3)).
  The script asserts that the criterion was evaluated and not met; it does not pretend a no-go on size. The route is excluded on a different ground (D1a: tree-level alpha does not depend on T; the constant X of Dienes 6.19 is free), which is structural, not numerical.
* D3 racetrack: the illustrative pair (N1, N2) = (9, 8) and r = 4, 8, 16 were chosen by hand after noticing that r ~ 8 reaches alpha_G^-1 ~ 25. It is an illustration of the sensitivity dalpha_G^-1/d ln r = 11.5, NOT a trial and NOT evidence. The unbiased statement is the 36-pair requirement table:
  only 2 of the 36 (N1 > N2, 2..10) pairs need r in [0.1, 10] for alpha_G^-1 = 25.640 (the pairs (9,8) and (10,9)), and for the rest the required prefactor ratio ranges up to 1e27.
  The racetrack conventions (a = 8 pi^2/N, 1/g^2 = Re S, K = -ln(S+Sbar)) are RECALLED, not read.
* D4: the count needed for one expected chance hit is 1/8.69e-4 = 1151 (the pre-registration wrote 1150); the check allows +-3.
* Several checks are descriptive markers chosen by me, not registered thresholds: h3 S3b (">3"), S5 (">10x"), S6, S4a (0.3). They are labelled as descriptive in the scripts; the verdict rests on the printed numbers, not on those cuts.
* FINAL TRIAL COUNT: scored comparisons = h3 S1+S2 (12 predictions) + h4 D2 (16) = 28; expected chance hits at the 1e-3 rule = 28 x 8.69e-4 = 0.024; hits = 0. All runs exit 0; every MUTATE run exits 1.
