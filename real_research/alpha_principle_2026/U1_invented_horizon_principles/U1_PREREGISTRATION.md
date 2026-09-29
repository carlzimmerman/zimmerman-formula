# U1 -- a graveyard of invented horizon-response principles (pre-registration)

Written 2026-09-29 BEFORE any script in this directory was run. (Before writing this file I only READ the committed record: ALPHA_CHAIN_STATUS.md, T1,
AH1/AH4, N5, Q1/Q2/S1/S2 outputs and the lane-D checker. No computation of any quantity below has been executed.)

## Why this lane exists and what counts

T1 stated one invented principle (P1: the de Sitter vacuum sustains a constant electric field), derived its consequence, and it died on the real charged
spectrum. The user asked for invented principles. The rule that governs this lane: inventing a HYPOTHESIS is legitimate; a principle conceived after seeing
1/137 cannot gain credibility by fitting 137. It counts only if (a) it is stated in full BEFORE any comparison (this file), (b) its consequences follow by
derivation from results already in the record, and (c) it makes at least one prediction that it was not built to fit and that can be checked against known
numbers. Solving a principle for a target is an INVERSE MAP, not a test, and is labelled as such below.

Nothing here is tuned to 137.036. No principle below has a free parameter; every "variant" is a convention or integer choice DECLARED HERE, and all variants are
reported (none is dropped after the fact). alpha stays an INPUT; kappa = 1/2 stays FITTED; the SM mass sector is walled (measured masses are INPUTS).

## Units, inputs (declared; measured values are inputs, not derived)

* hbar = c = 1, Heaviside-Lorentz, alpha = e^2/(4 pi), alpha_input = 1/137.035999177 (Thomson). lambda = eE/H^2, M = m/H.
* H = H_Lambda = H_0 sqrt(Omega_Lambda), H_0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685 (T1 used H_0; M changes by 1.2 and nothing below is sensitive to it). ρ_Λ = 3 H^2 / (8 pi G) exactly for this H.
* Planck mass M_P = G^(-1/2) = 1.220890e19 GeV (not reduced).
* Spectrum (PDG-rounded, INPUTS, MeV): e 0.51099895; mu 105.6583755; tau 1776.86; u 2.16; d 4.67; s 93.4; c 1270; b 4180; t 172570 (quark weights Q^2 N_c: u,c,t 4/3;
  d,s,b 1/3; leptons 1); W 80377; pi^+- 139.57039 (composite; used only as a point scalar in the EFT sense and flagged as such).
* SI constants: exact 2019 SI (e, h, c); Z0 = 1/(eps0 c) with eps0 defined by alpha (so alpha = Z0/(2 R_K), R_K = h/e^2, is an identity, as the record states).

## Results reused (source files; nothing is re-derived except where stated)

* dS_4 Dirac fermion: sigma/H = alpha G_f(M), G_f = (4/(3 pi)) [ln M - Re psi(iM) - pi M (4M^2+1)/(3 sinh 2 pi M)] (Q1, validated by S2 in the M -> 0 and M -> infinity limits;
  negative at every M; small M: (4/(3 pi))(ln M + gamma_E - 1/6); large M: -1/(9 pi M^2)). Precision: 250 digits (T1 Amendment 1).
* dS_4 complex scalar: sigma/H = alpha G_s(M), G_s from the AH4 closed form (transcribed, re-gated here against Q1's and AH4's committed tables); positive; large M: +7/(18 pi M^2).
* dS_2: scalar pair factor r = e^{-2 pi rho} cosh(pi(lambda+rho))/cosh(pi(lambda-rho)), rho = sqrt(mu^2 + lambda^2 - 1/4) (AH1); Dirac J/(eH) = (1/pi) rho_f sinh(2 pi lambda)/sinh(2 pi rho_f),
  rho_f = sqrt(mu^2 + lambda^2), g_f(mu) = 2 mu/sinh(2 pi mu) (N5); massless Schwinger model E_tt + H E_t + (e^2/pi) E = 0, critical damping e^2/H^2 = pi/4 (N5-3).
* dS_4 dilution of a homogeneous field: nabla_nu F^{nu z} = -2 E H / a, so a constant E needs |J| = 2 E H (AH4 V3, Q1).
* Q1's zero L*(M) of the fermion current (M = 0.5, 1, 2, 5: L* = 5.67, 2.51, 2.11, 5.39).
* Rate depends on e only through lambda (AH1 C5, Lean AH3). The Landau-pole identity (T1): alpha G_f = -2 <=> ln(H/m) = 3 pi/(2 alpha) + gamma_E - 1/6 (small M).

## The test battery (declared now, applied identically to every principle)

* T-SPEC. A principle that demands sigma_X/H = c (X = Dirac fermion or complex scalar) is SATISFIED by a known species i iff sign(S_i) = sign(c) and 1/2 <= |S_i/c| <= 2, where
  S_i = alpha Q_i^2 N_c,i G_X(M_i) (T1's factor-2 criterion), tested for each single species AND for the total over the 9 charged fermions. If c = 0 the variant is reported VACUOUS if |S| < 1e-30
  (it then holds for every alpha and fixes nothing). Otherwise the shortfall factor |c|/max|S_i| is reported.
* T-SIGN. The sign of c must be the sign of G_X (fermion G_f < 0, scalar G_s > 0). A wrong sign is a kill whatever the magnitude.
* T-BACK (field-value principles). The field lambda*_i the principle demands of species i must satisfy rho_E <= rho_Lambda, i.e. lambda*_i <= lambda_max = e M_P sqrt(3/(4 pi)) / H
  (E = lambda H^2/e, rho_E = E^2/2 in HL). Beyond lambda_max the assumed fixed-H background is inconsistent. Reported also as the energy ratio rho_E/rho_Lambda = (4 pi/3) lambda^2 H^2/(e^2 M_P^2).
* T-NUM (principles that return a number for alpha or 1/alpha). delta = |(1/alpha_pred)/137.035999177 - 1|; lane D's bar (`alpha_bar_checker.assess`, declared family size below, zero fitted
  reals, scale stated as Thomson): pass iff it clears (P < 1e-3 and delta <= 5e-10). A negative alpha_pred fails outright.
* T-INERT. If the principle's equations contain e only through lambda = eE/H^2 (the AH1/AH3 structure) then it cannot determine alpha: it fixes E* = lambda* H^2/e only.
* T-IND. A principle can only be marked SURVIVES if it passes every applicable test above AND names one prediction it was not built to fit that is checked against a known number.

## Verdict rules (declared)

* DEAD: fails T-SPEC, T-SIGN, T-BACK or T-NUM, i.e. contradicts the known spectrum or a known number.
* UNDECIDED: passes every applicable test but needs an untested ingredient or is inert (T-INERT); the ingredient is named.
* SURVIVES: passes everything applicable and passes T-IND.
* Expected outcome, stated in advance: NO principle SURVIVES. Every sigma-type principle is killed by the hierarchy m/H ~ 1e38-1e44 (|S_e| ~ 1e-81 for the electron); every field-value principle
  that demands lambda ~ M^2 is killed by T-BACK; the two that demand O(1) fields (P10, P11) pass T-BACK and are UNDECIDED (inert). The sign of the fermion conductivity kills every principle that needs sigma > 0 from a fermion.

## The principles (each stated in full; equation on (alpha, M, lambda); test; expected verdict)

Convention for sigma-type: sigma/H = c with c a pure number; equation alpha Q^2 N_c G_X(M) = c.

**P01 Stationarity (T1's P1, reproduced under the common battery).** The vacuum sustains a constant field: J = -2EH, sigma/H = -2. Variants: 1. Species: fermion (scalar excluded by T-SIGN).

**P02 Impedance matching of the horizon membrane.** The horizon membrane has sheet resistance R_H = Z0 (4 pi/c Gaussian = 376.7 ohm). The vacuum's induced sheet conductance across one Hubble length
l = c/H is G = sigma_SI l. The vacuum is impedance-matched to the membrane: R_H G = 1. In HL units R_H G = sigma/H (sigma_SI = eps0 sigma_HL), so the equation is |sigma/H| = 1 (this is also "the conductivity
equals the Hubble rate"). Variants (the length convention, declared): l = c/H x {1, 2 pi, 1/(2 pi), 4 pi, 1/(4 pi)} i.e. |c| in {1, 2 pi, 1/(2 pi), 4 pi, 1/(4 pi)}. 5 variants. The sign is not fixed by matching (magnitude condition), so each species type is
tested at its own sign.

**P03 Critical damping of the 4D de Sitter plasma oscillator.** Homogeneous field: E_t + n H E = -J (n = D-2 = 2; dilution, AH4 V3). Current relaxation ansatz (INVENTED, the dS_2 memory relation J_t + H J = (e^2/pi) E generalised
by the conformal weight q = D-1 of a spatial current): J_t + q H J = q H sigma E. Then E_tt + (n+q) H E_t + q H (n H + sigma) E = 0 (sympy-derived; reduces to N5-3 at n = 0, q = 1, sigma H = e^2/pi). Critical damping:
(n+q)^2 = 4 q (n + sigma/H), i.e. sigma/H = (n-q)^2/(4q). Primary (n,q) = (2,3): sigma/H = 1/12. Variants q in {1,2,3,4}: c = 1/4, 0, 1/12, 1/4 (see Amendment 1: the first draft wrote 1/8 for q = 4, a hand-arithmetic slip). 4 variants. Untested ingredient: the dS_4 memory kernel (q). Reported also as a
scan over q in [1e-3, 1e3]: the electron can satisfy the equation only within |q - 2| < ~1e-40 (the vacuous window) and, since (n-q)^2/(4q) >= 0 for q > 0, never with a fermion's negative sigma.

**P04 Plasma resonance with the Gibbons-Hawking frequency.** The oscillator of P03 has frequency squared q H (n H + sigma) (the coefficient of E). Resonance with the Gibbons-Hawking angular frequency 2 pi T_H = H: q(n + sigma/H) = 1,
sigma/H = 1/q - n. Primary (2,3): -5/3. Variants q in {1,2,3,4}: c = -1, -3/2, -5/3, -7/4. 4 variants.

**P05 Conductance quantum.** The vacuum conductance across the Hubble radius, G_vac = sigma_SI c/H, equals n e^2/h with n = +-1 (a "one-channel" vacuum). Because e^2/h = 2 alpha/Z0 and G_vac = alpha G(M)/Z0, the ratio is
G(M)/2: ALPHA CANCELS. Equation G_X(M) = 2 n. Variants n = +1, -1. 2 variants. (This principle is alpha-blind by construction; it can only test the spectrum.)

**P06 Vacuum neutrality (supertrace sum rule).** The net induced conductivity of the whole charged spectrum vanishes: sum_i sigma_i = 0. In the heavy limit sigma_i/H = alpha Q_i^2 N_i g_i / M_i^2 with g_f = -1/(9 pi) (Dirac),
g_s = +7/(18 pi) (complex scalar), g_W unknown (the W was not computed; S1's W_y coefficient is scheme-incomplete). alpha factors out: the condition is on masses and multiplicities only. Test (criterion declared here, still before any run): the cancellation must be reachable with coefficients of the size the record has
computed: DEAD iff it needs |g_W| > 100 (the largest heavy-mass |g| in the record is 0.124; margin 800) or more than 100 pi^+--like scalars per electron-like fermion; the required g_W* and multiplicity are reported. 1 variant.

**P07 Landau pole at the horizon.** The one-loop running coupling of the lightest charged fermion diverges at mu = H: 1/alpha_eff(mu) = 1/alpha - (2/(3 pi)) ln(mu/m) = 0, i.e. alpha = 3 pi/(2 ln(mu/m)) (the T1 identity read as a prediction of alpha from m). Variants mu = H, mu = H/(2 pi) (the Gibbons-Hawking
temperature). 2 variants. Test T-NUM (and T-SIGN: alpha must be positive). Structural remark to be checked: below the lightest charged mass the coupling does not run at all.

**P08 Marginality of the pair-production factor.** The out-frequency rho vanishes, where the dS_2 scalar factor r -> 1 (pair number diverges): mu^2 + lambda^2 = 1/4 (dS_2 scalar) or, for the dS_4 scalar mode index mu_w = sqrt(9/4 - lambda^2 - mu^2), lambda^2 + mu^2 = 9/4.
Variants: dS_2, dS_4. 2 variants. Demands M <= 1/2 (resp. 3/2). Test: T-SPEC on the mass window (no real lambda for the known masses); anchor: r -> 1 as rho -> 0 (dS_2, numerical).

**P09 Saturation at the Schwinger critical field.** The vacuum sits where the pair-production exponent is O(1): eE = m^2, lambda = M^2 (anchor: -ln r -> pi at lambda = mu^2, large mu, within 10% at mu = 80, dS_2 scalar). 1 variant. Demands lambda* = M_i^2. Test T-BACK.

**P10 Conformal threshold as the horizon field.** The vacuum field is the fall-to-the-centre threshold of Q2, lambda = 1/2 (E* = H^2/(2e)). 1 variant. Test T-BACK, T-INERT.

**P11 Schwinger-Unruh (a0) matching.** The field-driven acceleration equals the framework's a0 = kappa c H: eE/m = kappa H, lambda = kappa M (AH1 tie T1; at kappa = 1/2 the flat-space Schwinger exponent pi m^2/eE equals the Gibbons-Hawking exponent 2 pi m/H). Variants kappa in {1/2 (fitted), 1/(2 pi) (Milgrom footing)}.
2 variants. Test T-BACK, T-INERT; E* = kappa m H/e reported for every species.

**P12 Self-sustained field at FINITE field (nonlinear T1).** J(lambda, M) = 2EH with the full (nonlinear) J. Equation |alpha G_eff(lambda, M)| = 2 with alpha G_eff = J/(E H) (which reduces to sigma/H as lambda -> 0); alpha enters explicitly through J/(EH) = alpha f/(pi lambda) (scalar, AH4 normalisation). Variants: fermion, scalar. 2 variants. The known-spectrum test uses
the ceiling lambda <= lambda_max: (i) perturbative part |alpha Q^2 N G(M)|/2 (1 + (lambda_max/M^2)^2) (EFT expansion parameter (eE/m^2)^2), (ii) non-perturbative part bounded by exp(-pi M^2/lambda_max) (the AH1-C3 exponent, dS_2 scalar, ASSUMED to carry to dS_4 and to fermions).
P12 is satisfiable within the ceiling iff (i) + (ii) >= 1. For information: the flat-space Schwinger estimate of lambda* (J ~ e Gamma/H, Gamma = (eE)^2/(4 pi^3) e^{-pi m^2/eE} fermion, /(8 pi^3) scalar).

**P13 Zero of the renormalized current.** The vacuum sits at the field L*(M) where the induced current changes sign (Q1 Q4b; HFY's stable point). Variants: fermion, scalar (the scalar has no sign change in the range Q1 scanned; reported as computed if a zero exists). 2 variants.
Known-spectrum test: a sign change needs the positive non-perturbative part to match the negative perturbative one, lambda e^{-pi M^2/lambda} ~ pi^2 |G_f|; with lambda <= lambda_max the exponent >= pi M^2/lambda_max, so none exists below the ceiling
(same assumption as P12). Estimate of L*_e reported for information.

**P14 Schwinger-Unruh point that carries the dark energy.** P11's field also carries the dark-energy density: E^2/2 = rho_Lambda (the "electromagnetic vacuum energy is the cosmological constant") with lambda = kappa M. Then e = kappa m/(M_P sqrt(3/(4 pi))) and
alpha = kappa^2 m^2/(3 M_P^2) (derived; alpha = m^2/(12 M_P^2) at kappa = 1/2). Variants kappa in {1/2, 1/(2 pi)}, species: the electron is the lightest charged fermion (the 9 fermions are reported). 2 variants (x 9 reported species). Test T-NUM.

**P15 Nariai-reduced critical damping.** Take the 4D geometry dS_2 x S^2 with Nariai radii R_S = R_dS = Lambda^(-1/2) so R H_2 = 1 (H_2 = sqrt(Lambda)); a charged massless fermion with N 2D Dirac zero-modes (uniform LLL density 1/(4 pi R^2))
has 2D coupling e_2^2 = e_4^2/(4 pi R^2) = alpha/R^2 each; the 2D photon mass^2 is N e_2^2/pi (N Dirac flavours) or N e_2^2/(2 pi) (N Weyl zero-modes). Critical damping (N5-3): m_gamma^2 = H_2^2/4.
Then alpha = pi (R H_2)^2/(4N) = pi/(4N) (Dirac variant, 1/alpha = 4N/pi) and alpha = pi/(2N) (Weyl variant, 1/alpha = 2N/pi); the script re-derives both symbolically.
2 variants. Inputs outside the record (declared): Nariai radii, uniform LLL density, N an integer. It is NOT our dS_4. Test: T-NUM with the nearest integer N (an inverse map for N*).

**P16 Membrane quantum Hall.** The horizon membrane resistance is quantised against the resistance quantum: Z0 = R_K/N (N a positive integer) [variant a: 1/alpha = 2N] or Z0 = 2 R_K/N (two edge channels, variant b: 1/alpha = N).
Variants a, b. 2 variants. Test T-NUM (the integer candidates floor/nearest/ceiling are all reported).

**P17 Electric-magnetic self-duality.** The horizon vacuum sits at the S-dual coupling e = g_m, with the Dirac quantisation e g_m = 2 pi n (HL): alpha = n/2, n = 1 gives 1/2; the tau = i convention (e^2 = 4 pi) gives alpha = 1. Variants alpha_sd in {1/2, 1}. 2 variants. Test T-NUM.

**P18 Self-dual maps of the response functions.** A "self-dual point" exists iff a response function is exactly invariant under a map, F(lambda') = F(lambda), for ALL lambda. Maps declared: lambda -> c/lambda with c in {1, 1/2, 1/4, 1/pi, 1/(2 pi), 1/(4 pi), 2, 4, pi} (9 maps) and the swap
(lambda, mu) -> (mu, lambda) (1 map): 10 variants. Functions: r(lambda, mu) (dS_2 scalar pair factor) and J_f/lambda (dS_2 Dirac), grid mu in {0.3, 1, 2}, lambda in {0.4, 0.7, 1.3, 2, 3.5} (where the image is defined). Invariance threshold |F'/F - 1| < 1e-6 at all points.
(A fixed point lambda = sqrt(c) of the map exists trivially for ANY function and selects only a field value, so it is not a test.) Expected: no invariance except the trivially constant massless dS_2 fermion.

## Aggregation rule (declared)

Each (principle, variant) gets its own verdict. A principle is DEAD iff every non-vacuous variant is DEAD. A VACUOUS variant (c = 0, holds for every alpha) is listed as such: it imposes no condition, fixes no alpha, and is
not counted as a survival. If variants differ (some DEAD, some UNDECIDED) the principle is reported with the per-variant verdicts and its headline is the least severe non-vacuous variant.

## Count of everything that will be tried (declared)

* 18 principles, 47 (principle, variant) pairs: P01 1, P02 5, P03 4, P04 4, P05 2, P06 1, P07 2, P08 2, P09 1, P10 1, P11 2, P12 2, P13 2, P14 2, P15 2, P16 2, P17 2, P18 10.
* Known-spectrum evaluations: 9 charged fermions + total + pi^+- = 11 targets for sigma-type variants (16 variants -> 176 evaluations); 10 species for field-type variants (P08-P14).
* Bar calls (T-NUM): P07 (2), P14 (2 kappa x 9 species reported, family log2size = log2(18)), P15 (2 x candidates), P16 (2 x 3 integers), P17 (2). Look-elsewhere family for the whole graveyard when pooled: 47 variants x 10 species (log2 ~ 8.9); no principle is
  expected to come near 5e-10 so the family size is immaterial to every verdict.
* Nothing else is tried. If a variant is added later it goes in an Amendment below and is counted.

## Scripts (argv declared in each docstring; every one has a MUTATE control that must FAIL and give exit 1, the campaign standard)

1. `u1_0_gates.py` -- gates: the reused functions reproduce the committed numbers (G_f, G_s, dS_2 r, J_f, g_f, Z0, alpha = Z0/(2 R_K), the sympy oscillator derivation). `python3 u1_0_gates.py`; control `--mutate` (sign of G_f flipped).
2. `u1_1_sigma_class.py` -- P01-P07. `python3 u1_1_sigma_class.py`; control `--mutate` (P01 requirement flipped to +2 as in T1).
3. `u1_2_field_class.py` -- P08-P14 (fields, back-reaction ceiling, Schwinger estimates, combination P14). `python3 u1_2_field_class.py`; control `--mutate` (the back-reaction ceiling removed: lambda_max -> infinity; P09's T-BACK kill must FAIL).
4. `u1_3_numbers_duality.py` -- P15-P18 and the bar calls. `python3 u1_3_numbers_duality.py`; control `--mutate` (the measured 1/alpha replaced by 4*108/pi: the miss must vanish and the bar's precision check must then be met, i.e. the DEAD expectation fails).
5. `u1_9_graveyard.py` -- reads the four result files and prints the verdict table. `python3 u1_9_graveyard.py`; control `--mutate` (one verdict record corrupted; the consistency check must FAIL).

Run environment: `PYTHONDONTWRITEBYTECODE=1`; no absolute paths and no personal names in any file; no PDFs.

## Scope and reading rules

* The responses used are linear (sigma) or the published dS_2 closed forms; dS_4 scalar closed form transcribed from a PDF (AH4) and re-gated. The non-linear dS_4 fermion current and vectors are NOT recomputed; where a principle needs them (P12, P13, P06's W) the
  ceiling argument and the flagged assumption are used.
* Field-value principles (P08-P13) are inert on alpha in the AH1/AH3 sense unless combined with a second, independent condition on E (P14 is one such combination, invented here, and it is the only one of that kind).
* "DEAD" here means: contradicts the known charged spectrum or a known number under the stated scope. It does not mean the vacuum response is uninteresting.

## Amendments (visible)

**Amendment 1 (2026-09-29, after the first run of u1_0_gates.py, disclosed; FIRSTRUN output kept as `u1_0_gates_FIRSTRUN.out`).** Gate G6e failed: the
pre-registration states for P03 that q in {1,2,3,4} gives c = 1/4, 0, 1/12, 1/8. Diagnosis (run before any change): the gate's sympy value for q = 4 is 1/4, and by hand
(n-q)^2/(4q) = (2-4)^2/16 = 1/4, not 1/8. The error was MY hand arithmetic in this file (the formula c = (n-q)^2/(4q) itself was right and is unchanged; it is symmetric under q -> 4/q, so q = 4 must equal q = 1).
Change made: the declared P03 values are c = 1/4, 0, 1/12, 1/4 (q = 1, 2, 3, 4); the gate's expected list was corrected accordingly. No variant was added or removed (still 4), no criterion or threshold was changed,
and the P04 values (-1, -3/2, -5/3, -7/4) were unaffected (gate G6f passed). Every other gate (22 of 23) passed on the first run.

**Amendment 2 (2026-09-29, after the first run of u1_1_sigma_class.py; FIRSTRUN output kept as `u1_1_sigma_class_FIRSTRUN.out`).** Check B3 ('every solvable fermion M* satisfies its equation to 1e-6 with the exact G_f') failed
for one entry, P05 n = -1 (M* = 10^-2.2 = 6e-3), and every verdict was unaffected. Diagnosis (before any change): the solver used the small-M identity ln M = (3 pi/4) t - gamma_E + 1/6, which has an
O(M^2) correction (Q1's c1 = -0.772: relative size ~6e-6 at M = 6e-3), so a residual of order 6e-6 against a 1e-6 tolerance is expected; for all other entries M* <= 10^-11 and the identity is exact to 1e-20.
The B checks were not among the pre-registered verdict tests; they are implementation gates. Change made: the small-M identity is used as the starting point and the root is refined with the exact 250-digit G_f (`mp.findroot`);
the 1e-6 tolerance is unchanged. Only P05 n = -1 moves (M* at the 1e-5 level); no verdict, shortfall factor or count is affected.

**Amendment 3 (2026-09-29, after the first run of u1_2_field_class.py; FIRSTRUN output kept as `u1_2_field_class_FIRSTRUN.out`).** Check E7 (P13 scalar variant: f > 0 at every scanned point) failed at the single scan point
(lambda, M) = (1.0, 1.0), where the closed form returned exactly -46.0000. Diagnosis (before any change): mu_w^2 = 9/4 - 1 - 1 = 1/4, so sin(2 pi mu_w) = sin(pi) = 0, a REMOVABLE singularity of the transcribed closed form (the
0/0 evaluates to garbage); evaluating at lambda = 0.999, 0.9999, 1.0001, 1.001 gives 1.1352, 1.1361, 1.1362, 1.1371, smooth and positive. Change made: scan points with |sin(2 pi mu_w)| < 1e-6 are evaluated at lambda(1 + 1e-4).
No threshold or criterion changed; the scan grid (15 points) is the same.

**Amendment 4 (2026-09-29, after the first run of u1_3_numbers_duality.py, which had passed; FIRSTRUN output kept as `u1_3_numbers_duality_FIRSTRUN.out`).** The pre-registration says the P18 invariance test is done
'where the image is defined', but the first implementation counted an undefined image (scalar factor with mu^2 + lambda'^2 <= 1/4) as a deviation of 1.0. Change made: undefined images are skipped and a verdict needs >= 6 defined points.
This can only make invariance easier to find (it removes a penalty), never harder; the result is reported whatever it is.
