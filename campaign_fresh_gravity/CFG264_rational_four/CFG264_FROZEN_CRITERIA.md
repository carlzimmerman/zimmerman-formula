# CFG264 -- constrained attempt to DERIVE the rational 4 in G rho_Lambda = 4 a0^2 / c^2: FROZEN CRITERIA

Written 2026-10-01, BEFORE any script of this lane exists and before any number of this lane is computed.
The sha256 of this file goes into `CFG264_FROZEN_CRITERIA.sha256` immediately after writing. Nothing below may be edited after the first
script runs; any change is an appended, dated `## Addendum` with its reason.

Read before freezing (claims only, no scripts of other lanes opened): `sonnet55_push/puzzle_32pi/README.md` (all sections, lane tables A-Z, N1-N3,
B1/B3/B4, section 12); lane READMEs K, E, X1 (full), W (full), N (full), X3 (full), and the bottom lines of G, B4, N3, X2, S, F, N2; `kappa_closure/README.md`
(k01-k04); the first 60 lines of `gemini_pi_puzzle/SPIN2_PROJECTION_DERIVATION.md`; `campaign_fresh_gravity/STANDING_2026-09-29.md` (the 32 pi entries,
lines 194-205 and 332-337); `opus_48_extended_research/reviews/DERIVE_Z_FRESH_RUN_VERDICT_2026-06-15.md` (the entropy-quarter section);
`campaign_fresh_gravity/CFG263_32pi_nogo_audit/CFG263_FROZEN_CRITERIA.md` (sibling audit lane; not edited).

## 0. Target, conventions, standing
- Target (pi-free, density-linear): **G rho_Lambda = 4 a0^2 / c^2**, i.e. a0 = kappa c sqrt(G rho_Lambda) with **kappa = 1/2**; equivalently Lambda = 32 pi a0^2 / c^4.
  rho_Lambda is a MASS density; Lambda c^2 = 8 pi G rho_Lambda; H_Lambda^2 = Lambda c^2 / 3 = (8 pi/3) G rho_Lambda. Scripts keep c (and hbar, k_B where they occur) as symbols.
- Output variable of every route: **k2 := a0^2 / (c^2 G rho_Lambda)** (the target is k2 = 1/4). Report k2 exactly (sympy) and its pi-content.
- kappa = 1/2 is FITTED and stays fitted unless a derivation lands here AND a second, independent re-derivation (a separate script written from the
  README alone) agrees. The README may not say "derived" before that.

## 1. Structural hints taken from the record (not re-derived as results)
- E: only a0^2-LINEAR-in-density forms allow exactly 1/2; horizon-first (a0 linear in H) routes give kappa^2 in pi*Q.
- G: only the pi-free form G rho_Lambda = 4 a0^2 is symmetry-accessible; no symmetry contains it. Lindemann dichotomy.
- X1: the 4 is the only factor of the 28-row ledger with no derivation; the 8 pi is Einstein's coupling, the 3 is spatial dimension.
- K: in the density-linear (AQUAL offset) family the coefficient is set by the far tail: G rho/a0^2 = c[mu]/(8 pi); needs c = 32 pi.
- W (screen): a rational carrier must (a) involve c, (b) involve rho_Lambda through a source, (c) contain a compensating 1/pi.
- N / X3: Jacobson thermodynamics in dS has no crossover (Tolman factors cancel; a0 = H or 2H); extended SdS thermodynamics with P = -rho_Lambda
  lands every rational/algebraic condition on (rational) x pi for a0^2/(G rho_Lambda).

## 2. Closed or excluded before ranking (not candidates here)
- Everything in lanes A-Z, N1-N3, B1, B3, B4, p01-p12 (README tables), CFG263's audited no-gos.
- The static trace projection P_00,00 = (D-3)/(D-2) = 1/2 (gemini_pi_puzzle SPIN2 file): it is the trace-reversal factor that turns 16 pi G into
  8 pi G in the Newtonian limit (X1's BIA atom, already inside E8 = 8 pi); using it a second time double-counts. Reading only; not scripted here.
- "32 pi = 8 pi x 4 as Einstein x entropy-quarter" as a bare factorisation: killed as numerology in DERIVE_Z (three strikes). The OWNER-DIRECTED
  route below tests the only version that could escape that verdict: an actual equilibrium/extremum/matching condition.

## 3. The five untried routes (mechanism; why not closed; cheapest decisive check; frozen P(derivation); cost)

### R1 -- Deep-MOND virial theorem with the vacuum term (+ declared relativistic closures)
Mechanism. For an isolated, stationary deep-MOND system the exact virial relation is sum r.F = -(2/3) sqrt(G a0) [M^{3/2} - sum m_i^{3/2}]
(continuum limit: -(2/3) sqrt(G a0) M^{3/2}). The vacuum adds the exact weak-field force g_Lambda = +(4 pi/3) G (2 rho_Lambda) r = H_Lambda^2 r
(Tolman active density rho + 3p/c^2 = -2 rho_Lambda), whose virial is + H^2 I, I = alpha M R^2. So 2K = (2/3) sqrt(G a0) M^{3/2} - alpha H^2 M R^2.
The route asks whether a stationarity condition of this combined virial (binding edge, half-binding, marginal mass), closed by ONE or TWO
relativistic identifications that bring in c, outputs k2 = 1/4. It carries the Tolman 2 and the virial 2 in one equation (so it also
contains the "4 = 2 x 2 from vacuum and kinetic factors" reading).
Why not closed. B4 (point-mass, hydrostatic and wall objects), N3 (single-shell fixed point), G's g03 (the virial coefficient, explicitly
"contains no Lambda"), S (field-energy budgets) and W02 (briefed, never run) do not combine Milgrom's many-body virial relation with the
vacuum virial term, and none tests relativistic closures on it.
Cheapest decisive check. (i) Buckingham: the c-free system {G, a0, rho_Lambda, M, R} has 2 Pi-groups, neither containing c, so no c-free
condition can fix k2 (binding for the whole c-free class). (ii) With closures: solve the declared menu (section 5) exactly and read the
pi-content of k2; the Lambda term carries 8 pi/3, so a rational k2 needs a compensating pi from a closure.
Frozen P(derivation) = 0.3 %. Cost 1 h.

### R2 -- Two-sided (in/out-averaged) junction of a MOND-critical wall with the vacuum
Mechanism. For a pure-tension spherical wall separating a de Sitter interior (rho_Lambda) from a Minkowski exterior, the exact Israel conditions
give two signed side accelerations a_in, a_out with jump a_out - a_in = 4 pi G sigma and (record, audit H1) average
abar = (a_in + a_out)/2 = Delta rho c^2 / (3 sigma). The two-sided average removes the wall's own (pi-carrying) self-gravity and leaves an
object that is exactly pi-free in rho_Lambda and carries c. If sigma is fixed by a MOND condition (Milgrom's critical surface density
Sigma_M = a0/(2 pi G) is exactly the tension of a Z2 wall whose proper acceleration is a0), a declared junction condition (abar = a0, a side = a0, ...)
outputs a relation between a0 and rho_Lambda.
Why not closed. p06/p07 + audit H1 derived the side accelerations; J studied the Brown-Teitelboim charge-to-tension ratio e/sigma in the PROBE
limit (Delta P = eE); B4 compared surface densities (Sigma_Lambda = 4 pi Sigma_M, a restatement); W10 (sheet dictionary) was never run. Nobody
used the full-discharge vacuum-bubble wall with sigma fixed by a MOND field condition and the two-sided average.
Cheapest decisive check. Derive abar and the jump from the Israel equations (sympy), then evaluate every declared (condition, sigma-closure) pair
and read the pi-content of k2. A sigma fixed by a Gauss/Israel field condition is expected to carry 1/pi.
Frozen P(derivation) = 0.4 % (highest of the five: its core object is the only pi-free, c-carrying quantity I could find). Cost 1.5 h.

### R3 -- Two independent halvings in one equation (4 = 2 x 2)
Mechanism. Collect the DERIVED, D-independent rational 2's of the weak-field/horizon problem (vacuum Tolman -2; kinetic/virial 2; GHY/EH = 2;
two-sided average 1/2; the variational 2 in T_mn) and look for ONE standard equation (Raychaudhuri, Komar/Smarr, junction, virial) that multiplies
two of them with a0 and G rho_Lambda pi-free.
Why not closed. X1 tested candidate origins of the 4 one at a time by D-lift; F tested readings of 1/2 by dimension; p05 listed five origins of 1/2.
None required two derived halvings to multiply inside one equation.
Cheapest decisive check. A ledger of which equations carry which 2's; every equation that carries rho_Lambda carries it as 4 pi G or 8 pi G, so the
pi-weight check is expected to close it at once (R1's equation already contains Tolman x virial).
Frozen P(derivation) = 0.2 %. Cost 2 h.

### R4 -- Extremum of a rho-linear static functional (variational; 4 = 2^2 as a quadratic maximum)
Mechanism. A functional linear in rho_Lambda, E[R] = E_field(a0, M; R) - rho_Lambda c^2 V(R) (+ boundary), extremised over the configuration,
with a0 identified as the acceleration at the stationary point; the generic factor 4 = 2^2 of a quadratic maximum (max_a a(X - a) = X^2/4,
argmax X/2) would supply the 1/2 if X = c sqrt(G rho_Lambda) arose naturally.
Why not closed. S checked 341 budget EQUALITIES, L checked 19 SdS functionals for interior extrema (none), k02 checked a sequestering average.
No lane extremised a rho-linear field-plus-vacuum functional of the MOND sector.
Cheapest decisive check. Point-mass field energies are pi-free (S), the vacuum term carries 4 pi/3 per volume: the stationary point should carry
pi^(-1) in k2 and stay M-dependent; the natural X is c H (pi^(1/2)), not c sqrt(G rho_Lambda).
Frozen P(derivation) = 0.3 %. Cost 3 h.

### R5 -- Dimensional reduction / averaging (vacuum column density, pi-free cell)
Mechanism. Reduce the 4D vacuum energy onto a 2D horizon or a 1D Rindler line (surface density rho V/A = rho r/3, pi-free) or onto a cubic
cell (the only pi-free volume; W09's lattice of horizon-touching holes) and read a0 as the field of that column.
Why not closed. W09 and W10 were briefed, never run.
Cheapest decisive check. Gauss's law gives the field of any surface density as 2 pi G Sigma per side, re-inserting the pi; the cubic lattice is dust
(w = 0), not vacuum.
Frozen P(derivation) = 0.1 %. Cost 4 h.

### Ranking by P / cost (frozen)
| rank | route | P(derivation) | cost (h) | P/cost (%/h) |
|---|---|---|---|---|
| 1 | R1 deep-MOND virial with the vacuum | 0.3 % | 1.0 | 0.30 |
| 2 | R2 two-sided MOND-critical junction | 0.4 % | 1.5 | 0.27 |
| 3 | R3 two halvings in one equation | 0.2 % | 2.0 | 0.10 |
| 3 | R4 rho-linear extremum | 0.3 % | 3.0 | 0.10 |
| 5 | R5 dimensional reduction / pi-free cell | 0.1 % | 4.0 | 0.025 |
**Run: R1 and R2** (the top two). R3's decisive equation is contained in R1 (Tolman x virial), so R1's result is reported against R3 too, without
running R3 separately. P(any derivation from this lane) ~ 1 %.

### OD -- OWNER-DIRECTED route (added at the owner's request before freezing; scored by the same rules; run regardless of rank)
Owner's idea, quoted: "the 1/2 (the 4 in 32 pi) is the ratio between GR's surface boundary normalisation (the 1/4 of S = A/4) and the bulk
Einstein-Hilbert coupling (8 pi): a conversion factor between a 2D horizon's thermodynamic degrees of freedom and the 4D bulk vacuum energy."
Question tested: is there an equilibrium, extremum or matching condition between a horizon's entropy budget S = k_B A c^3/(4 G hbar) and the
vacuum energy it encloses (rho_Lambda c^2 V) that OUTPUTS a0 = (1/2) c sqrt(G rho_Lambda), with hbar cancelling, without assuming the law, 32 pi or
Lambda = 32 pi a0^2/c^4?
Known obstacles, to be addressed explicitly in the README:
(a) README line 65 (quoted): "Its "32π = 8π × 4 as Einstein × entropy-quarter" lead was killed as numerology (a literal second Bekenstein-Hawking
    quarter gives Z = 11.58)." DERIVE_Z strike 3: the single horizon quarter is already spent inside the 8 pi (Jacobson 8 pi = 2 pi x 4).
(b) The GHY boundary term carries 1/(8 pi G) against the bulk's 1/(16 pi G): a factor 2, not 1/4. The 1/4 belongs to the entropy, not the action.
(c) hbar enters through S (and T) and must cancel for a classical a0.
(d) N (local Clausius in exact dS) and X3 (extended SdS thermodynamics, P = -rho_Lambda) found no crossover. Hand expectation: OD overlaps X3's
    part A (TS versus |PV| = rho_Lambda c^2 V) almost completely; its additions are the Rindler sphere, the Komar/holographic-equipartition
    variant (Padmanabhan N_sur vs N_bulk) and an explicit hbar-cancellation lemma.
Cheapest decisive check. hbar-cancellation lemma (the quarter can enter an hbar-free budget only together with the thermal 1/(2 pi), as
1/(8 pi)), then the declared matching menu (section 5).
Frozen P(derivation) = 0.2 %. Cost 1.5 h. Verdict wording: one of DERIVATION / SCOPED NO-GO (binding failure named) / RESTATEMENT.

## 4. Verdict rules (all routes)
- **DERIVATION** iff all hold: (i) k2 = 1/4 exactly (sympy); (ii) the circularity audit passes at every step (no input contains the law, 32 pi,
  Lambda = 32 pi a0^2/c^4, R* used as "the a0 radius", or kappa); (iii) no new tunable constant; (iv) every closure is one declared in section 5
  BEFORE the run; (v) the hit is not a menu selection: among the admissible systems of the route, 1/4 is the unique rational k2 produced, or the
  route's declared principle singles out the hitting system before its value is seen; (vi) the mechanism's own vacuum dynamics is used (MUTATE M2
  of the route changes the hit); (vii) the MUTATE controls change the output. Then: Lean 4 statement sketch + flag for independent re-derivation.
- **RESTATEMENT** iff k2 = 1/4 arises only through an input that is the target in another form (R* = c/sqrt(G rho_Lambda) used as the system's
  radius with the surface-gravity 1/2 -- the gemini reading; a second entropy quarter on top of the TS pairing).
- **SCOPED NO-GO** otherwise; the first binding failure is named (Buckingham / pi-weight (Lindemann) / free parameter / no solution / menu selection).
- Stop rule: a sub-class stops at its first binding failure; the remaining declared systems are still tabulated (they are cheap) but cannot rescue it.
- Menu-selection control (decoys): rational decoys k2 in {1/3, 1/5, 1/6, 1/8, 2/9, 3/8, 1/2, 1}; report how many admissible systems hit each.

## 5. Declared menus (frozen)

### R1 menu
Base relation (always imposed): (V) 2K = (2/3) sqrt(G a0) M^{3/2} - alpha H^2 M R^2, H^2 = (8 pi/3) G rho_Lambda; alpha in {3/5 (uniform sphere), 2/3 (shell)}.
Conditions (pool; a system = (V) + three distinct conditions; unknowns K, M, R and a0):
- S1 binding edge: 2K = 0. S2 half-binding: alpha H^2 M R^2 = (1/2)(2/3) sqrt(G a0) M^{3/2}. S4 marginal mass: d(2K)/dM = 0 at fixed R.
- C1 2K/M = c^2 (virial speed reaches c). C2 R = 2 G M / c^2. C3 R = c^2/a0. C4 R = c/sqrt(G rho_Lambda) (R*, dimensional ansatz; any hit using C4
  is RESTATEMENT). C5 R = c/H. C6 G M a0 = c^4/4 (Schwarzschild hole with surface gravity a0).
- D1 M = (4 pi/3) rho_Lambda R^3. D2 M = (4 pi/3)(2 rho_Lambda) R^3 (zero-force / Einstein-static density).
Admissible for a derivation: contains at least one of S1, S2, S4 (vacuum dynamics used) and no C4.
Checks before the menu: Buckingham rank computation; the deep-MOND virial coefficient 2/3 re-derived in spherical symmetry (W = -int sqrt(G a0 M(r)) dM);
the vacuum force H^2 r from Poisson with the Tolman source; a test-particle limit of the N-body virial relation.
MUTATE (separate outputs): M1 virial coefficient 2/3 -> 1; M2 Tolman factor 2 -> 1 (vacuum as dust-like active density, Lambda term (4 pi/3) G rho);
M3 d = 3 -> 4 spatial dimensions (deep-MOND virial coefficient (d-1)/d with (G a0^{d-2})^{1/(d-1)} M^{d/(d-1)}, vacuum term 16 pi G rho/(d(d-1)) ... as derived
in the script). Each must change the k2 table.

### R2 menu
Junction: pure tension S_ij = -sigma h_ij, D = 4, spherical wall, interior dS (rho_in = rho_Lambda), exterior Minkowski (rho_out = 0). Also the Z2 case
(rho_in = rho_out = rho_Lambda) as a control (abar must then carry no rho_Lambda).
Conditions on a0: J1 abar = a0; J2 a_in = a0; J3 a_out = a0; J4 sqrt(a_in a_out) = a0 (both > 0); J5 2 pi G sigma = a0 (half the jump).
sigma-closures: Sg1 2 pi G sigma = a0 (Sigma_M); Sg2 4 pi G sigma = a0; Sg3 a_in = 0 (wall on the interior's dS horizon); Sg4 a_out = 0;
Sg5 4 pi R^2 sigma = (4 pi/3) rho_Lambda R^3 (wall mass = enclosed vacuum mass); Sg6 4 pi G R sigma = c^2/2 (wall mass = Schwarzschild mass of radius R).
A system = one J + one distinct Sg; unknowns sigma, R, a0. Admissible: every pair (J5 with Sg1 is the same equation and is skipped).
MUTATE: M1 one-sided instead of two-sided (replace abar by a_out in J1); M2 D = 4 -> 5 (abar = Delta rho c^2/((D-1) sigma), jump 8 pi G sigma/(D-2), Friedmann
H^2 = 16 pi G rho/((D-1)(D-2)); derived in the script); M3 control: sigma = q a0/G with symbolic rational q (shows where the pi enters).

### OD menu
hbar-cancellation lemma first (exponents of hbar and k_B in T^a S^b). GHY/EH normalisation ratio and the Euclidean Schwarzschild action
(GHY with flat subtraction) computed to place the 1/4 in the entropy.
Horizons: HdS (de Sitter horizon, r = c/H, kappa_h = c H; a consistency check, no free parameter); HS (Schwarzschild flat probe, kappa_h = c^2/(2r));
HR (Rindler sphere, r = c^2/a, kappa_h = a). T = hbar kappa_h/(2 pi c k_B), S = k_B A c^3/(4 G hbar), A = 4 pi r^2, V = (4 pi/3) r^3.
Budgets: B1 T S = E_vac (= rho_Lambda c^2 V); B2 2 T S = E_vac (Smarr form); B3 T S = E_K (Komar/Tolman, 2 rho_Lambda c^2 V); B4 holographic
equipartition N_sur (1/2) k_B T = E_K with N_sur = A c^3/(G hbar) (Padmanabhan, no quarter); B5 (S/k_B)(1/2) k_B T = E_K (quarter with equipartition);
B6 T dS/dr = dE_vac/dr at the horizon's own T; B7 stationary point of F(r) = E_vac(r) - T S(r) at fixed T, then T = the horizon's own temperature there.
a0 := kappa_h at the selected radius. 3 x 7 = 21 cases. hbar and k_B must cancel in every k2 (checked).
MUTATE: M1 remove the thermal 2 pi (T = hbar kappa/(c k_B)); M2 quarter -> 1/2 (S = A/2); M3 D = 4 -> 5 (Tangherlini kappa = (D-3) c^2/(2r),
A = Omega_{D-2} r^{D-2}, V = Omega_{D-2} r^{D-1}/(D-1); derived in the script).

## 6. Circularity audit (format, every route, every step)
For each step: inputs used; does any input contain kappa, 32 pi, Lambda = 32 pi a0^2/c^4, the law, or R* identified with the a0 scale? (YES = FAIL).
Programmatic guard: a0 and rho_Lambda are independent positive symbols throughout; the target k2 = 1/4 appears only in the comparison step; a function
checks that no single input equation, on its own, already implies k2 = 1/4 (solving it alone must leave k2 undetermined or different).

## 7. Frozen hand estimates (before any computation; disclosed, not criteria)
- HE1 (R1): the c-free sub-class fails by Buckingham; every admissible system gives k2 = (rational) x pi^(+-1) or is inconsistent; rational k2 only with C4.
- HE2 (R2): the MOND-critical wall (Sg1) with abar = a0 gives k2 = 2 pi/3 (kappa = 1.447, a0 = cH/2); a sigma = q a0/G control gives k2 = 1/(3q), so
  kappa = 1/2 needs q = 4/3, which no Gauss/Israel closure supplies.
- HE3 (OD): B1 on the de Sitter horizon is an identity (Friedmann; the entropy budget of the dS horizon equals the enclosed vacuum energy), giving
  kappa_h = cH, k2 = 8 pi/3 (the forced kernel); the flat-probe and Rindler cases give (rational) x pi; removing the thermal 2 pi (M1) makes them
  rational but not 1/4 for the declared budgets.
- HE4: P(at least one route is a DERIVATION) ~ 1 %; expected outcome: three scoped no-gos, the OD conversion-factor reading a restatement.

## 8. Outputs
`cfg264_lib.py` (shared check/guard helpers), `r1_virial_lambda.py`, `r2_two_sided_junction.py`, `od_horizon_quarter.py`, each with `.out`,
`_results.json`, and `_MUTATE.out` / `_MUTATE_results.json` (separate mode outputs); `results.json` (lane summary); `README.md` (verdict per route,
OD labelled OWNER-DIRECTED). No commit, no push.

## Addendum 1 (2026-10-01, before any script of this lane has run)
Error in my own frozen R1 menu: "alpha in {3/5 (uniform sphere), 2/3 (shell)}". The virial uses the POLAR moment I = sum m r^2 about the centre,
which is 3/5 M R^2 for a uniform sphere (correct) but M R^2 (alpha = 1) for a thin shell; 2/3 is the shell's AXIAL moment. Fix: alpha = 2/3 is kept as
declared but relabelled (it is the polar moment of the profile rho ~ r inside R, alpha = (3+p)/(5+p) at p = 1), and alpha = 1 (thin shell) is added.
R1 therefore runs alpha in {3/5, 2/3, 1}. Nothing else changes. The original frozen hash stays the first line of CFG264_FROZEN_CRITERIA.sha256.

## Addendum 2 (2026-10-01, after R1 and R2 ran, BEFORE any OD script or OD number)
Defect in my own frozen OD menu: B7 ("stationary point of F(r) = E_vac(r) - T S(r) at fixed T, then T = the horizon's own temperature there")
is algebraically identical to B6, because dF/dr at fixed T is E_vac' - T S' = 0. B7 is run as frozen and reported as identical to B6. Added:
B7' = stationary point of F(r) = E_vac(r) - T(r) S(r) along the horizon family (T varies with r through kappa_h(r)). Also added, as a
cross-lane consistency check (not a candidate): the HS rows B1 and B2 must reproduce X3's flat-probe entries (TS = |PV| -> 4 pi/3;
2TS = |PV| -> 2 pi/3), since |PV| = rho_Lambda c^2 V. Nothing else changes.

## Addendum 3 (2026-10-01, AFTER the OD results were known; requested by the coordinator after CFG263, commit 35058745f)
Post-run check, not part of the frozen menu and not a change to any verdict rule. CFG263's structural lesson: a mechanism whose only
scales are an acceleration a and H cannot give kappa = 1/2; a derivation must couple the a0 sector's ENERGY DENSITY to gravity with a
rational coefficient. Added to od_horizon_quarter.py as section F: (F1) rewrite every OD budget with rho_L = 3 H^2/(8 pi G) and confirm
that no a0-sector energy density occurs (a0 enters only as the horizon's kappa_h) and that every solved k2 = (8 pi/3) x rational, the
signature of that class; (F2) couple an a0-sector energy density eps = W a0^2/G as the vacuum, on the de Sitter horizon (where TS = E_vac
is an identity) and on the HS probe, and report what the horizon budget fixes. Results are labelled post-run in the README.
