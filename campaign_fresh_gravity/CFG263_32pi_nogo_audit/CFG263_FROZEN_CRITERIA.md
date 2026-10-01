# CFG263 -- hostile audit of the 32 pi / kappa = 1/2 no-gos: FROZEN CRITERIA

Written 2026-10-01, BEFORE any re-derivation, before any audit script, and before opening any original `.py` or `.out` of the audited lanes.
At freezing time I had read only the claims: `sonnet55_push/puzzle_32pi/README.md`, the lane READMEs of G, E, X1, K, L, N, B3, I (audit),
`L_sds_two_horizon/PREDECLARED_PRINCIPLES.md`, `B3_modified_horizon_equation/PRINCIPLES_DECLARED.txt`, and in `sol61_push/` the files
`CLOCK_BBN_RESULTS.md`, `CLOCK_COEFFICIENT_BOUND.md`, `CANONICAL_CLOCK_RESULTS.md`, plus the gemini section of `campaign_fresh_gravity/STANDING_2026-09-29.md` (lines 332-336).
The sha256 of this file is recorded in `CFG263_FROZEN_CRITERIA.sha256` right after writing. Nothing below may be edited after the first script runs;
any change goes into an appended `## Addendum` with the reason.

Conventions: c = G = 1 unless stated. kappa := a0 / sqrt(G rho_Lambda); the law is kappa = 1/2 FITTED, i.e. Lambda = 32 pi a0^2, G rho_Lambda = 4 a0^2.
H = sqrt(Lambda/3) = 1/L. Z = sqrt(32 pi/3) = c H_Lambda / a0. "Lambda-units": lengths in L; "u-units": lengths in R* = 1/u, u^2 = G rho_Lambda (so Lambda = 8 pi u^2).

## 1. The no-gos audited (8), chosen by how much of "nothing works" rests on each

| id | no-go | why load-bearing |
|---|---|---|
| NG-G | lane G, symmetry | the only lane that closes "a symmetry fixes the ratio"; its pi-dichotomy is reused by E, L, N |
| NG-E | lane E, literature | the basis of "every published route inserts the coefficient"; its pi-parity lemma defines the open target ("a0^2 linear in a density") |
| NG-X1 | lane X1, one generator + Noether/Euler | closes "one D-formula behind the 4's" and the Noether-charge / Euler-unit origin of A Lambda = 32 pi^2 |
| NG-K | lane K, density-linear family | the ONLY family where kappa = 1/2 is expressible without pi (the open target lives here); its verdict says the coefficient moves into an untestable tail |
| NG-L | lane L, SdS two-horizon | closes every "principle that selects a point of the SdS family" |
| NG-N | lane N, Jacobson thermodynamics in dS | closes the thermal/Unruh route that the founding a0 ~ cH/2pi literature uses |
| NG-P12B3 | p12 + B3, horizon equation | closes "a0 is the surface gravity of a horizon"; STANDING 09-29 line 335 uses p12 to reject the gemini reading |
| NG-S61 | sol61 canonical-clock BBN bound | the only no-go on an explicit relativistic action that reaches 32 pi; closes it by observation |

## 2. Exact premises and claimed class, quoted (file:line)

Paths relative to the repository root; `P/` = `sonnet55_push/puzzle_32pi/`, `A/` = `P/agents/`.

### NG-G (symmetry)
- Claim: "SHARP NO-GO for a symmetry-only origin" -- `A/G_symmetry_conformal/README.md:3`; table row "no-go | algebraic vs pi dichotomy: only the pi-free form G rho_Lambda = 4 a0^2 is symmetry-accessible; no symmetry contains it" -- `P/README.md:151`.
- Premises: (G-i) "if a0/H is a de Sitter / conformal representation number (algebraic), kappa is transcendental" -- `A/G.../README.md:4`; (G-ii) "Dilatation acts on (a0, Lambda) with Lambda/a0^2 invariant" -- `:5`, `:34`; (G-iii) "the AQUAL field equation does not contain the additive constant of its Lagrangian (which IS a vacuum energy)" -- `:5`, `:34`; (G-iv) "the dS Killing fields do not contain H" -- `:5`, `:32`; crossover at a = H -- `:6`, `:40`; RAR offset G rho/a0^2 = 1.03 -- `:7`, `:38`.
- Own scope: "A larger algebra ... was NOT investigated" / "Nothing here excludes a *dynamical* selection" -- `:49`, `:51`.
- Claimed class: all symmetries (headline) ; tested: dilatation, Conf(R^3) = so(4,1), dS isometries + Casimirs, scale/trace Ward identities.

### NG-E (literature)
- Claim: "No published route derives kappa = 1/2" -- `A/E_literature_a0_coefficient/README.md:4`; "Verdict: SHARP NO-GO (scoped to the published literature and to horizon-first derivations)" -- `:7`; table "horizon-first routes give rational Z; only a0^2-linear-in-density forms allow exactly 1/2" -- `P/README.md:149`.
- Premises: T - T_Lambda family "all give a0 = 2cH" -- `:5`, `:30-33`; Verlinde Z = 6 -- `:34`; van Putten 0.2023 cH0 -- `:35`; pi-parity lemma "Integer powers of pi ... can never make kappa^2 rational ... exactness requires a0^2 linear in a density (or 1/area)" -- `:63-65`; Milgrom naturalness "|F0| = 4" -- `:67`.
- Own scope: "only that none is published in the works listed" -- `:78`.
- Claimed class: the ~35 works opened + every horizon-first route.

### NG-X1 (one generator; Noether/Euler)
- Claim: "SHARP NO-GO (scoped) on two specific ideas: (i) a single generator of the '4's, (ii) a Noether-charge / Euler-unit origin of A Lambda = 32 pi^2" -- `A/X1_one_generator/README.md:6`; table "no-go (scoped)" -- `P/README.md:178`.
- Premises: (X1-i) D-lifts: "graviton's 4 ... constant, Tangherlini 4/(D-3)^2, MacDowell-Mansouri 2(D-2)(D-3)" -- `:7`, `:76-80`; (X1-ii-a) pi-power: "a quantity ~ r^n has pi-power n/2 at r = Z L/2, so no r^3 charge, Noether entropy or Euler number can be a rational multiple of pi^k there" -- `:9`, `:110`; (X1-ii-b) alpha-dependence: "an absolute condition 'Q(r_a0) = unit' is alpha-dependent while a0 = (1/2) sqrt(G rho) is an equation-of-motion statement" -- `:111`; Iyer-Wald charge "Q(r) = -r^3/(2 G L^2)" -- `:9`, `:109`; "A kappa^2 <= pi over all Kerr-Newman horizons" -- `:10`, `:104`.
- Own scope: "the premise that the puzzle's 4 shares an origin with the instance" -- `:82`, `:117`.

### NG-K (density-linear family)
- Claim: "SHARP NO-GO for fixing the coefficient inside the offset family (the coefficient moves into an untested tail exponent)" -- `A/K_density_linear_family/README.md:14`; table "c = int(1-mu)dy is set by the far tail ... untestable" -- `P/README.md:155`.
- Premises: (I1) "the vacuum energy is the constant of the a0-sector Lagrangian" -- `:17`; (I2) "F is normalised so the Newtonian regime carries no vacuum energy" -- `:17-18`; (I3) "mu's whole shape" -- `:18`; offset "G rho/a0^2 = c/(8 pi), c = int_0^inf (1-mu) dy" -- `:5`; OR family "(N-1)(N-2) = 1/(4 pi), N* = 2.0741, kappa* = 0.4821" -- `:11`, `:46-48`; RAR-nu c = 25.976 -- `:37`; "No potential-term principle fixes W_v = 4 (... SUSY vacua have V <= 0 ...)" -- `:13`, `:78`.
- Own scope: "the AQUAL Lagrangian is nonrelativistic" -- `:104`.

### NG-L (SdS two-horizon)
- Claim: "SHARP NO-GO, scoped to principles that select a point of the SdS family" -- `A/L_sds_two_horizon/README.md:3`; "So no SdS-internal principle can produce Z" -- `:6`; table "monotone family, only the endpoints are special" -- `P/README.md:156`.
- Premises: f-normalisation kappa = |f'|/2 -- `A/L.../PREDECLARED_PRINCIPLES.md:4`; monotone bijection -- `README.md:5`; T_b = T_c iff r_b r_c = L^2/3 -- `:5`; pi-count "any principle that selects the point by an algebraic condition in the geometry (Lambda units) gives an algebraic kappa/H" -- `:6`, `:51`; u-units caveat "a principle of that form is NOT excluded by pi-counting" -- `:52`, `:56`.

### NG-N (Jacobson thermodynamics in dS)
- Claim: "SHARP NO-GO (scoped to exact-dS Killing-horizon thermodynamics with Jacobson's inputs)" -- `A/N_jacobson_thermo_dS/README.md:6`; table "heat and T carry the same Killing factor, so G_eff = G for every a/H ... the resulting a0 is H or 2H ... never 1/Z" -- `P/README.md:164`.
- Premises: Tolman cancellation -- `:4`, `:25`; G_eff/G = kappa_heat/kappa_T table -- `:27-34`; (kobs, a) gives a0 = H, T - T_Lambda gives a0 = 2H -- `:36`; pi-parity "every member has a0 = qH with q rational" -- `:44`; inserted premises I1-I4 -- `:47-50`.

### NG-P12B3 (horizon equation)
- p12 claim: "1 - 2 kappa r_h = 8 pi G rho(r_h) r_h^2 ... (D) so kappa r_h = 1/2 and r_h^2 Lambda = 8 pi cannot hold at one static horizon of one metric. Scope: f-normalised Killing vector (audit H2), static spherical symmetry, GR." -- `P/README.md:197`.
- B3 claim: "Every theory whose static vacuum branch is an Einstein space ... has the identical horizon relation 1-2 kappa r_h = Lambda_e r_h^2, so T=(1/2, 8 pi) is excluded for every coupling" -- `A/B3_modified_horizon_equation/README.md:4`; "with N_h: kappa r = N_h(1-8 pi rho r^2)/2" -- `:13`; NOT computed: Einstein-aether, Horava/khronon, AeST, TeVeS, BIMOND, CA5/V0 -- `:23`, `:32`; summary "a modified horizon equation re-inserts the coefficient (B3)" -- `P/README.md:206`.
- Downstream use: "The p12 horizon identity shows a0 cannot be the surface gravity of a static horizon with rho_Lambda > 0" -- `campaign_fresh_gravity/STANDING_2026-09-29.md:335`.

### NG-S61 (canonical clock + BBN)
- Claim: "proved for the canonical-clock equations and lambda>1; observational interpretation conditional on the source transfer" -- `sol61_push/CLOCK_COEFFICIENT_BOUND.md:3`; "C > (2/3) R/(1-R)^3 ... C > 1197.9 > 11.9 x (32 pi)" -- `:17`, `:23`; "R < 0.8238740919142051 ... entire interval lies below the source's lower endpoint 0.92" -- `sol61_push/CLOCK_BBN_RESULTS.md:18-21`.
- Premises: the action -- `sol61_push/CANONICAL_CLOCK_RESULTS.md:9-15`; H^2 = 2 U0/[3 M^2 (3 lambda - 1)] -- `:25`; G_N = G(1+D)/D, a0_N = [D/(1+D)]/[12 pi G K q0] -- `:59`; Lambda_geom/a0_N^2 = 4D(1+D)^2/[3(3 lambda - 1)] -- `:63`; G_cosm = 2G/(3 lambda - 1) -- `:67`; transfer G_BBN/G_0 := R -- `CLOCK_BBN_RESULTS.md:7`.
- Own scope: "not a rejection of all theories yielding 32 pi" -- `CLOCK_BBN_RESULTS.md:21`.

## 3. Classification scheme (one primary class per no-go; sub-findings flagged separately)
- **CORRECT-GENERAL**: re-derived independently; holds for the whole class its headline wording names, with no unstated premise that narrows it.
- **CORRECT-NARROWER-THAN-WORDED**: the derivation is right, but it holds only under a premise (units, Killing normalisation, theory class, menu, literature set) that the headline wording (lane bottom line or `P/README.md` table row) does not carry.
- **PREMISE-UNVERIFIED**: the conclusion rests on a premise that neither the lane nor this audit verifies (a literature reading not reproducible from formulas, a convention not derived, or a unit-dependent pi-count presented as unit-free).
- **ERROR**: a load-bearing step is false (algebra, arithmetic, logic, sign), shown by an independent re-derivation with a check that can fail.

## 4. What counts as a RE-OPENED DOOR (decided before any computation)
A door is re-opened iff EITHER
- (D-a) an ERROR in a load-bearing step such that the corrected statement no longer excludes some named route; OR
- (D-b) the true class is narrower than claimed AND a SPECIFIC route exists that (i) lies outside the true class, (ii) is not computed anywhere in `P/`, `sol61_push/`, `campaign_fresh_gravity/closure_map/` (searched, not assumed), (iii) is stated as one mechanism with one equation to compute, and (iv) could output the rational 4 (equivalently a rational G rho_Lambda / a0^2, a "u-algebraic" output) WITHOUT inserting 4, 1/2, 32 pi or Z by hand.
NOT a door: "some other theory might"; "a dynamical principle" with no named mechanism (that is the record's known open target); a route that needs a free coupling set to a target value; a route that outputs only rational multiples of a0/H (excluded by Lindemann whatever the mechanism).
A re-opened door is reported in a HANDOFF section and NOT run here (CFG264 is the sibling lane for untried routes).

## 5. Planned independent re-derivations (my own sympy/numpy; original scripts not opened until these have run)
- G: kappa = (a0/H) sqrt(8 pi/3); the dichotomy in BOTH unit systems; F -> F + C invisible to the Euler-Lagrange equation but visible to T_00; dilatation covariance of the deep-MOND equation; dS Killing algebra in conformal coordinates with symbolic H (structure constants H-free); Tolman T_loc; RAR offset in closed form.
- E: T - T_Lambda slope (2H); Verlinde (d-3)/((d-2)(d-1)); van Putten 2/(1 + 2 pi sqrt2); pi-parity for Z = q pi^j; the area form a0^2 A_dS at kappa = 1/2; Milgrom naturalness Lambda = -8 pi F0 a0^2.
- X1: Iyer-Wald / Komar-type charge Q(r) = r^2 f'/4 for static f, evaluated in dS; its pi-content at the a0 radius in Lambda-units AND u-units; alpha (Euler) rescaling; A kappa^2 <= pi for Kerr-Newman; the D-lift slots I can recompute (Tangherlini, Euler coefficient on dS_D).
- K: F(0) = int (1 - mu) dy; c for sharp, exponential, Milgrom mu_n (closed form vs quadrature), OR family 2N^2/((N-1)(N-2)), RAR-nu; N*; AQUAL vs QUMOND offset; w_off formula.
- L: SdS roots, kappa_b, kappa_c (f-norm), monotonicity, T_b = T_c locus, a0-point closed form, K_Sigma = rho bound, Smarr point, pi-count in both units.
- N: static-observer a and Tolman T; G_eff = G kappa_heat/kappa_T table; the two crossover members' a0; pi-parity.
- P12B3: G^t_t for f = 1 - 2m(r)/r from the Ricci tensor; the horizon identity; the identity with a lapse N(r); whether (D) survives a general Killing normalisation (my own question, see disclosure); B3's SdS-form statement.
- S61: Friedmann constraint of the projectable lambda-action; Lambda_geom/a0_N^2; G_cosm/G_N; the elimination C = (2/3) R (1+D)^3; the bound C > (2/3)R/(1-R)^3; R < 0.8239 at C = 32 pi.
Every check prints PASS/FAIL and can fail. Outputs: `*.out` next to each script, `results.json`.

## 6. MUTATE controls (declared now)
- M-ERR-1: copy the p12 re-derivation, plant a wrong Einstein-tensor coefficient (8 pi -> 4 pi in the horizon identity); the audit's independent Ricci check must FAIL on the copy.
- M-ERR-2: copy the K offset re-derivation, plant c(N) = 2N^2/((N-1)(N+2)); the quadrature check must FAIL on the copy.
- M-ERR-3: copy the X1 charge re-derivation, plant Q = r^2 f'/(2G); the vacuum-mass cross-check must FAIL on the copy.
- M-PREM-1: change a premise and show the CLASS shifts: (a) for G/L/X1, switch the held-fixed variable Lambda -> G rho_Lambda; (b) for p12, drop the null energy condition between the normalising observer and the horizon. The classifier (a function of the verified premise flags, written before any run) must return a different class.

## 7. Frozen hand estimates (before any computation)
| no-go | P(error in a load-bearing step) | P(correct but narrower than worded) | P(re-opened door) |
|---|---|---|---|
| NG-G | 0.10 | 0.70 | 0.05 |
| NG-E | 0.10 | 0.80 | 0.05 |
| NG-X1 | 0.25 | 0.70 | 0.05 |
| NG-K | 0.10 | 0.75 | 0.08 |
| NG-L | 0.08 | 0.60 | 0.03 |
| NG-N | 0.08 | 0.60 | 0.03 |
| NG-P12B3 | 0.10 | 0.60 | 0.07 |
| NG-S61 | 0.10 | 0.90 | 0.03 |
Overall P(at least one re-opened door) ~ 0.25; P(an actual derivation of kappa = 1/2 from this audit) ~ 0.

## 8. Disclosure of what I suspected while reading the claims (before computing; not part of the criteria)
- X1's pi-power statement (`A/X1.../README.md:110`) is written in Lambda-units; the section-12 H3 correction (`P/README.md:134`) says pi-counting is unit-dependent. I suspect X1-ii-a fails in u-units (hence its higher P(error)); its alpha leg is separate.
- p12 states its scope as the f-normalisation; I suspect (D) may survive any static-patch normalisation if the null energy condition holds, which would make it MORE general than worded.
- The RAR-nu offset may have a closed form (Bose-Einstein shape).
- B3 lists the record's own preferred-frame theories as NOT computed; that is the most likely place for a narrower-than-worded class.
These are guesses; the scripts decide.

## 9. Standing
This audit can find errors and scope; it cannot derive. kappa = 1/2 stays FITTED unless a derivation actually lands, and none is expected from an audit.
