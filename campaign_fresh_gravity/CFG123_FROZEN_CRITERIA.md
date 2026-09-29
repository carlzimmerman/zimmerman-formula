# CFG123 (Door 9): Deser-Woodard / Maggiore-Mancarella nonlocal metric gravity as a source of the phantom density. FROZEN CRITERIA (phase 1, written before any script or number)

Status: FROZEN at writing. To be committed by the orchestrating session before any script or output exists in the lane. Nothing in the lane except this file exists at the time of writing; no numerics were run. Every number below marked "hand estimate" is a pre-run expectation from dimensional analysis, not a result, and a hand estimate that turns out wrong is kept and disclosed as wrong.

kappa = 1/2 is FITTED. Both a0 footings apply (9.3603e-11 and 1.1312e-10 m/s^2); every G1 verdict is computed at both. Nothing here says the theory is closed, and nothing here says any data favour the framework. A scoped no-go is a valid result, and a pass would not be the goal.

Shared gates: G1-G5 are taken verbatim from `campaign_fresh_gravity/closure_map/TEN_DOORS_GATES_2026-09-29.md`. This door adds sub-tests but weakens none of them.

---

## (a) Provenance: the menu was written knowing the target

The ten-door menu (TEN_DOORS_GATES_2026-09-29) was written AFTER CFG44 exhibited the target C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r), and the doors were chosen with that target in view. A door that passes G1 is therefore NOT evidence for its mechanism: the target selected the menu, so agreement would have to be paid for by the mechanism's own derivation (no tuned constant, no postulated shape), and even then it would be a coincidence-of-selection risk, not a confirmation. A door that fails is a scoped no-go for that door only.

Consequences fixed here: (1) no constant, function or boundary condition may be chosen after seeing a G1 number; (2) the only tuned quantity allowed anywhere is the MUTATE control's deliberate plant (section (e)), reported as a plant and never as a result; (3) the expected outcome (section (f)) is fixed now.

---

## Where this door sits relative to the record (do not repeat what is excluded)

| lane | what it excluded | door 9's relation |
|---|---|---|
| CFG44 (B2 E3/E4) | a universal barotropic fluid plus ANY fixed-kernel force linear in M_b (fluid-coupled). Not covered: non-linear-in-M_b or non-fixed kernels | Door 9's weak-field response IS a fixed-kernel force linear in M_b, but with NO fluid, so CFG44's exclusion does not apply as written. The present test is a direct test of the linear-kernel class (section (b) linearity lemma) plus the one zone CFG44 marks uncovered: the NONLINEAR static response (ladder N1-N3). |
| CFG43 | a saturating barotropic cap on a conserved fluid (Lambda-tied cap, one action) | not touched (no fluid, no cap). Door 9 offers a different Lambda-tie candidate through the scale m (G4). |
| CFG48 (Gap 1) | bound-only owned switch as a legal term; bilocal exchange reacts 0.06-22 g_law; energy 23-50x | Door 9 has NO switch and NO exchange. It is a metric-side response present around every mass, bound or not (it does not address ownership; the unbound-web pathologies N10/N12 are NOT tested here). Its localisation is a legal local action with auxiliary fields, so GA passes formally, but see G5 (CFG50-type kinetic structure). |
| CFG50 | tidal-tensor fluid coupled to an auxiliary baryon-sourced potential with a multiplier; kinetic matrix [[0,D],[D,0]] (dipole-ghost structure); reaction O(g_law) | STRUCTURAL OVERLAP: the localised RR/DW fields (U,S with multipliers xi1,xi2) are auxiliary potentials sourced by the baryon trace R through multipliers, and their kinetic matrix has the same off-diagonal form. Not the same hypothesis (no fluid stress, the coupling is to the curvature trace, and in a metric theory the reaction is universal). G5 tests this directly. |
| CFG60 | rubric D/P/I/X/U over 54 constructions; none derives the dispersion | Door 9 would enter as a new row: it does not address a cold fluid's dispersion at all (it replaces the fluid by a metric response), so under the rubric it is U for the dispersion question and this lane is the test. |
| CFG70 / CFG72 | causal (time-kernel, then light-cone) versions of the enclosed-mass exchange: any retarded completion whose late-time limit is the static enclosed-mass functional returns CFG48's reaction and energy | Door 9's retarded nonlocal operator (box^{-1}) has a DIFFERENT static limit: a kernel |x-x'| (from nabla^{-4}) that is NOT an enclosed-mass functional and NOT keyed to a0. CFG70/72's verdict therefore does not transfer either way. No Schwinger-Keldysh completion of box^{-1} is built here (NOT tested). |

Two readings of the door (declared now, both reported):
- R-A (primary): the nonlocal term REPLACES Lambda (as in the published RR model), so m is fixed by the background (m replaces rho_Lambda). No separate cosmological constant.
- R-B: the nonlocal term is ADDED to Lambda + CDM, m free. Then m is a new constant (G4 FAIL by rule 3). The G1 linearity lemma below is independent of m, so R-B changes G4 only.

---

## (b) The exact model and the known facts

### b1. Maggiore-Mancarella RR model (primary)

Nonlocal action (c = 1, mostly-plus signature, matter S_m minimally coupled to g):

    S_RR = (1/16 pi G) int d^4x sqrt(-g) [ R - (m^2/6) R box^{-2} R ] + S_m[g, psi],   m = one constant with dimension 1/length.

Localisation with auxiliary fields U = -box^{-1} R, S = -box^{-1} U (so box U = -R, box S = -U, and box^{-2} R = S), enforced by multipliers xi1, xi2:

    L_loc = (1/16 pi G) sqrt(-g) [ R (1 - (m^2/6) S) - xi1 (box U + R) - xi2 (box S + U) ].

Signs and coefficients are DERIVED in the script by sympy variation (T0a below), not asserted here. Elimination is expected to give xi1 = (m^2/6) S, i.e. the metric equation carries a factor (1 - (m^2/3) S) on G_mu nu plus derivative terms of S and U. The known prescription is used and declared: vary as if box^{-1} were symmetric, then impose retarded boundary conditions (U = S = 0 in the radiation era, no free initial data).

### b2. Deser-Woodard model (secondary, linear response only)

    S_DW = (1/16 pi G) int sqrt(-g) R [1 + f(X)],   X = box^{-1} R (box X = R),   f a FREE function.

Localised: L = sqrt(-g) [ R (1 + f(X) - xi) - g^{mu nu} d_mu xi d_nu X ]. The script treats f as an unspecified analytic function about the cosmological background value Xbar and carries (fbar, fbar', fbar'') as symbols. DW is tested ONLY at the level of the linearised static response and the constants count; no fit of f to an expansion history is built (NOT tested).

### b3. What the known structure says about the phantom density (hand derivation, pre-run; to be verified by T0c and G1)

Static, weak field, flat background (the Kehagias-Maggiore setting), point mass M. At linear order R = 8 pi G rho. Then nabla^2 U = -8 pi G rho gives U = 2 G M/r; nabla^2 S = -U gives S = -G M r (plus homogeneous pieces A + B/r; the r-growing piece from U's homogeneous part is fixed by the boundary condition and enters as an O(1) coefficient). The nonlocal terms are m^2 x (S-type terms), so the potential the baryons feel gets

    delta Phi ~ c1' m^2 G M r   (relative correction ~ (m r)^2),   rho_eff = (1/4 pi G) nabla^2 delta Phi ~ c1 m^2 M / (4 pi r),

with c1 a pure number of order one fixed by the action (sign to be derived). This is a linear response with M-independent constants: rho_eff proportional to M, to 1/r.

The target (CFG44, P2 point mass, x = r/r_M, r_M = sqrt(G M/a0)):

    rho_c^target = a0 / (4 pi G r sqrt(1 + x^2)),   M_c(<r) = M (sqrt(1 + x^2) - 1),   g_law = sqrt(g_N^2 + a0 g_N).

So x << 1: rho_c -> a0/(4 pi G r), M-INDEPENDENT and 1/r. x >> 1: rho_c -> a0 r_M/(4 pi G r^2), proportional to sqrt(M) and 1/r^2.

**Linearity / mass-dependent-scale lemma (the core argument of this door; exact, kernel-independent).** Any response linear in the baryon density with constants that do not depend on M (G, c, H0, m, a0 as a fixed number, and any kernel built from them) has rho_eff(r; M) = M k(r) at fixed profile shape. The target at fixed r goes as M^0 (r << r_M) to M^{1/2} (r >> r_M). So the ratio rho_eff/rho_target scales as M^1 (x << 1) down to M^{1/2} (x >> 1). Over M_b = 1e9 to 1e12 that is a spread of at least 31 and up to 1000, against a G1 requirement of 1.2. G1 with "the SAME constants at every mass" is therefore impossible for ANY linear response, whatever its kernel, amplitude or scale. The target's r_M = sqrt(G M/a0) depends on the mass; a fixed length 1/m cannot reproduce it. G1 could be met only by (i) a nonlinear-in-M response (a nonanalytic sqrt(M)), or (ii) an M-dependent constant (a new field or a postulate). Equivalent statement: the length 1/m_req that would reach the target amplitude at x << 1 is sqrt(c1) r_M(M), which changes by a factor 31.6 between 1e9 and 1e12.

Hand estimates (to be checked): r_M = 1.2 kpc (1e9 M_sun), 39 kpc (1e12); c/H0 = 4.45 Gpc (H0 = 67.36), so c/(H0 r_M) = 3.6e6 (1e9) to 1.1e5 (1e12). With m = mu H0/c, mu of order 0.3-0.6 (value to be solved in the script; not quoted from the literature): amplitude ratio at x << 1 is R_A = rho_eff/rho_target = c1 m^2 G M / a0 = about 1e-14 (1e9) to 1e-10 (1e12), times mu^2 c1 (order 0.1-1), times sqrt(1+x^2) (up to 30 at x = 30). Ten to fourteen orders below the 0.9-1.1 line. The uniform background dark-energy density is also about 5 orders below rho_c(r_M) for a 1e11 M_sun galaxy (hand estimate).

**Nonlinear suppression (hand estimate).** The action is polynomial in m^2; the auxiliary fields have canonical O(1) kinetic terms (box U = -R, box S = -U), so nothing carries 1/m^2 (no Vainshtein-type enhancement is expected). The nonlinearity parameter is eps = G M/(r c^2) = sqrt(G M a0)/(c^2 x): eps(r_M) = 4e-8 (1e9) to 1.2e-6 (1e12); over the whole G1 grid (x in [0.1, 30], M in 1e9-1e12) eps runs from about 1e-9 to 1.2e-5, i.e. 5 to 9 orders below 1; the second nonlinear parameter m^2 S ~ (m r) eps (m r) is smaller still. Then the second-order response relative to the linear one is R_NL ~ eps. To be verified, not assumed (ladder N1-N3), because the alternative scaling R_NL ~ eps/(m r)^2 (Vainshtein-like, r_V = (r_s/m^2)^{1/3}, about 0.45 Mpc for 1e11 M_sun) would reach O(1) inside r_V and would reopen the door. This is a pre-registered decision fork (section (f)).

**Deser-Woodard, weak-field expectation (hand estimate).** The perturbation of the argument X is deltaX ~ eps (potential-sized) plus cosmological pieces ~ (H0 r/c)^2, so at analytic order the local response is a mass-independent rescaling of G and of the slip (proportional to fbar', fbar''), plus H0^2 M r-type terms of the same form as RR. Neither has the sqrt(M) structure; a constant rescaling cannot supply M_c/M = sqrt(1+x^2) - 1 up to 29 at x = 30, and Solar System bounds it at about 1e-5. A function f with a branch point at Xbar(t) for all t would postulate the target and is NOT tested.

### b4. Known constraints and literature facts to test against (memory, UNVERIFIED; the data chat owes the literature status before results are read)

- RR replaces Lambda by one parameter m (m of order H0/c is fixed by Omega_Lambda). The published fits (Dirian, Foffa, Kunz, Maggiore, Pettorino and later) report a background near LCDM with phantom-like effective dark energy, a reduced growth at late times, and no galaxy-scale phenomenology. The last point is stated in the door brief; treated as a claim to be confirmed.
- Kehagias-Maggiore (2014): static spherically symmetric RR solutions show corrections of relative order (m r)^2; no Vainshtein screening claimed. To be reproduced by T0c, not cited as evidence.
- Ghost status: the localised RR form has auxiliary fields with mixed-signature kinetic structure; Foffa-Maggiore-Mitsou argue they are not independent propagating degrees of freedom once retarded (zero-data) conditions are imposed. DW localisations have been argued to carry a ghost (Nojiri-Odintsov, Koivisto). Both to be confirmed by the data chat. Under the programme's criterion (DE12/DE13/XC), zero-data-by-prescription is scored PARTIAL (ownership-as-initial-data analogue, CFG48 GA), never PASS.
- Gravitational-wave speed: the RR tensor sector is claimed to have c_T = 1 with a modified friction term; DW unknown to me. NOT tested here.
- Solar System (Cassini): |gamma - 1| = 2.3e-5.

---

## (c) The tests. Numeric pass lines. Scripts in the lane; each has a MUTATE mode and writes its own `.out` and `_results.json` next to itself.

Common set-up (declared): Planck-like canonical values as used by CFG48 (H0 = 67.36 km/s/Mpc, Omega_m = 0.3153, Omega_Lambda-equivalent = 0.6847), radiation included, CDM density Omega_c h^2 = 0.12 inserted by hand as in LCDM. Masses M_b = 1e9, 1e10, 1e11, 1e12 M_sun. x = r/r_M grid: 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5, 10, 20, 30. Extended baryons: CFG44's exponential sphere read from CFG44 `Bcommon` (imported read-only, scale-height rule as CFG44 B1 uses, never restated); r_ta in both conventions read from CFG48 `Gcommon` / CFG70 `cfg70_common` (read-only). Every script path-independent: repository root from environment variable ZF_REPO, else derived from `__file__`; outputs beside the script.

### T0. Model integrity (`A1_localised_action.py`, sympy)

- T0a: eliminating xi1, xi2 from the localised action reproduces the variation of the nonlocal RR action under the symmetric-box^{-1} prescription, on (i) a static spherically symmetric metric ansatz and (ii) an FRW ansatz. PASS: exact residual 0.
- T0b: the Bianchi/conservation identity nabla^mu E_mu nu = 0 for the nonlocal stress once the U,S equations hold. PASS: residual 0.
- T0c: linear static flat-space solution for a point mass: report S, U, delta Phi, delta Psi (both metric potentials, so the slip is reported), the exponent of r in delta Phi (hand estimate +1), and the sign and value of c1. PASS (literature-consistency check only): exponent +1.0 exactly.
- Same for DW (`A1b_DW_localised.py`): localised equations with (fbar, fbar', fbar'') as symbols; residuals as T0a/b.

### G1. Target (`A2_static_linear_response.py`, `A3_nonlinear_static.py`)

Definitions (declared): in a metric theory the "effective dark density" is the density that, through the Poisson equation, sources the extra potential the baryons feel: rho_eff = (1/4 pi G r^2) d/dr [ r^2 (g_tot - g_N) ] with g_tot = g_N + delta g the acceleration of the baryons from the metric. Then C_eff(r) = rho_eff r^3 g_tot is compared with (a0/4 pi) M_b(<r) (CFG44 target, P2 charge). Cross-check: delta g_eff versus g_P2 - g_N.

- G1-A amplitude: R_A(x, M) = rho_eff / rho_target. PASS line: 0.90 <= R_A <= 1.10 at every grid point and every mass (point mass and exponential sphere), with the same constants at every mass.
- G1-S shape: at fixed M, max over x of R_A / min over x of R_A. PASS line <= 1.20 (after allowing an overall constant). Hand estimate: proportional to sqrt(1 + x^2), i.e. about 300 over the grid.
- G1-M mass scaling: at fixed x in {0.1, 1, 10, 30}, max over M of R_A / min over M. PASS line <= 1.20. Hand estimate: exactly M^1 for a point mass in the linear response, i.e. 1000.
- G1-sign: rho_eff > 0 (attractive, phantom-like) at every grid point. Sign reported.
- G1-X extended: G1-A/S/M repeated on CFG44's exponential sphere with C_eff(r)/[(a0/4 pi) M_b(<r)].
- G1-req (diagnostic, not a gate): m_req(M) needed for R_A = 1 at x = 0.1, its ratio to (H0/c), its scaling exponent in M (hand estimate -1/2), and rho_DE^bg / rho_c(r_M).
- G1 as a whole passes only if ALL of G1-A, G1-S, G1-M, G1-X pass. G1 FAIL is recorded per sub-line.

Nonlinear ladder (decides whether a nonlinear-in-M escape exists):
- N1 (`A3_nonlinear_static.py`): second-order static response by perturbation theory in eps for the localised RR (and DW-linear) equations with mpmath at the TRUE galactic parameters (extended precision, since eps ~ 1e-9): R_NL(x, M) = |delta Phi^(2)| / |delta Phi^(1)| on the grid.
- N2: the full nonlinear static spherically symmetric localised equations (regular at the origin, extended source) solved numerically at INFLATED parameters (eps = 1e-3, 1e-2, 1e-1; m r = 1e-2, 1e-1, 1), and compared with the N1 series (agreement through O(eps^2)).
- N3: fit the exponents of eps and of m r in R_NL over the inflated grid; extrapolate to galactic parameters and compare with N1.
- Decision lines (pre-registered): the nonlinear route is CLOSED-in-scope if R_NL <= 1e-3 at every grid point and the fitted exponent of (m r) is >= 0 (no 1/m^2 enhancement); UNDECIDED if 1e-3 < R_NL < 0.1; OPEN if R_NL >= 0.1 anywhere (then full nonlinear static solutions at galactic parameters are the next phase, and G1-M/G1-S would be re-tested with them).
- Quantification stated as a gate line: the linear response falls short of the target by the factor 1/R_A (hand estimate 1e10-1e14); the nonlinear terms add at most R_NL (hand estimate 1e-9-1e-5) of the linear response. G1 can then only be met by the linear response, which is excluded by the lemma; the report gives both numbers and the shortfall after the nonlinear correction.

### G2. CMB and growth (`A4_cosmo_background_growth.py`)

Perturbation equations to be stated in the output header (sympy-derived): Newtonian-gauge metric (Phi, Psi), delta U, delta S, delta xi1, delta xi2 on the RR background; sub-horizon quasi-static reduction k^2 Phi = -4 pi G mu(a, k) rho_m delta, slip eta = Psi/Phi; growth delta'' + (2 + H'/H) delta' = (3/2) Omega_m(a) mu delta; U, S initial data zero in the radiation era (retarded prescription, declared). CDM (Omega_c h^2 = 0.12), baryons and radiation are inserted exactly as in LCDM, so the door adds no cold component.
- G2-a: solve the RR background (H0 fixed, Omega_m = 0.3153): report m/H0 (the one fitted number that replaces Lambda), rho_DE^eff(z), w_DE(z = 0).
- G2-b: |H_RR/H_LCDM - 1| <= 5e-3 for all z >= 10, and the theta_* shift at fixed (H0, Omega_m h^2): PASS if it can be removed by an H0 shift <= 0.54 km/s/Mpc (Planck 1-sigma).
- G2-c: growth ratio D_RR(k, z = 10) / D_LCDM(k, z = 10) (normalised at z = 1100, k = 0.5, 2, 10, 30 /Mpc): PASS within [0.95, 1.05]; also |mu - 1| <= 0.05 and |eta - 1| <= 0.05 for z >= 10. Ratio at z = 0 reported (informational, no gate; late-time growth suppression is the literature's claimed RR feature).
- G2-d (statement): a G2 pass here is UNINFORMATIVE about the door, since the cold component is inserted by hand and the nonlocal term is negligible at z >= 10 (hand estimate: rho_DE^eff/rho_tot < 1e-3 at z = 10). It is recorded as "PASS (vacuous)" and may not be cited as support.

### G3. Reciprocity and energy (`A5_reciprocity_energy.py`)

Which pass line applies: in a diffeomorphism-invariant metric theory with universal minimal coupling there is no baryon-fluid exchange term and no separate "reaction"; the Bianchi identity (T0b) makes the total stress conserved and the baryons and the cold species feel the SAME metric. CFG48 G4's reaction line (<= 0.10 g_law over x in [0.3, 30]) is scored as follows: reaction := | g_baryon - g_tot,mechanism |, the part of the force on baryons that is not the mechanism's own metric force. PASS line 0.10 g_law; by construction 0. Note the trap this avoids: reading "reaction" as delta g itself would make G3 (<= 0.10 g_law) mutually exclusive with G1 wherever delta g / g_law = 1 - 1/sqrt(1 + x^2) exceeds 0.10 (x >= 0.5); the metric-theory reading is declared here, before running, and the incompatibility is disclosed instead of hidden.
- G3-a: T0b residual 0 (conservation).
- G3-b: energy. E_eff = integral of rho_eff c^2 dV out to r_ta, compared with (1/2) M_b V_f^2, in BOTH r_ta conventions (CFG48's and B's committed r_ta with the phantom-inclusive mass, via the read-only commons). PASS line: E_eff <= (1/2) M_b V_f^2 in both.
- Statement: expected PASS (vacuous): the mechanism is negligible (hand estimate E_eff/E_orb ~ 1e-10 or smaller), so the pass is a consequence of G1's failure, not support; recorded as such.

### G4. Constants (`A6_constants_tie.py`)

- G4-a count: constants beyond kappa and Omega_c h^2. R-A: m replaces Lambda and is fixed by the background (net new = 0, but flagged that the framework's Lambda-tie candidates T1-T5 are then not the RR mechanism). R-B: m is new (FAIL by rule 3). DW: the free function f (at least fbar, fbar', fbar'' locally) is new constants (FAIL by rule 3 unless f is fixed by an action-level tie; none is).
- G4-b tie: a0 does not appear in either action, so the door cannot derive a0. Diagnostic a_mech = c^2 m against a0 = kappa c sqrt(G rho_Lambda) = kappa c H0 sqrt(3 Omega_Lambda/8 pi) (kappa = 1/2 gives 9.3603e-11): report a_mech/a0 at both footings. A tie as "a stated equivalent" requires this to be a pure number produced by the action (0.9-1.1 with kappa = 1/2, no new number) AND the linear response's scale to be a0 (fails by the G1 lemma, since the amplitude needs G M m^2 = a0/c1: M-dependent).
- G4-c implied evolution: if the tie is read as a0(z) proportional to sqrt(rho_DE^eff(z)) (the RR "Lambda" is not constant), report a0(z)/a0(0) for z <= 5. PASS line: within 1% (the framework's flat a0(z) law; the rival is a0 proportional to H(z)). If instead a0 is pinned to its z = 0 value, the tie is postulated, not RR's.
- A G4 PASS requires G4-a (R-A) AND G4-b AND G4-c. Hand expectation: FAIL on G4-b (and G4-c if RR's dark energy is phantom-like: a0 proportional to sqrt(rho_DE) would be about 0.7 of its z = 0 value at z = 5 for w near -1.15; hand estimate).

### G5. Well-posedness (`A7_wellposed.py`)

- G5-a ghost (kinetic-matrix signature): quadratic action of the localised model about flat space (and about the FRW background, sub-horizon), Fourier space; find the poles of det K(omega, k) and the sign of the residue of every propagating mode beyond the two tensor polarisations. PASS: no negative residue among modes with free initial data. Scoring: if the (U, xi1), (S, xi2) sector has off-diagonal kinetic structure with opposite-sign residues, the localised action with free data is FAIL (the CFG50 dipole-ghost structure); the retarded zero-data prescription is scored PARTIAL and never PASS.
- G5-b hyperbolicity: all characteristic speeds of the localised system equal c (each auxiliary field obeys a box-type equation). PASS: no superluminal characteristic, no gradient instability of the homogeneous solutions r^n (report the static growth of S ~ r as a feature of the source, not an instability).
- G5-c Solar System (explicit statement): RR: |gamma - 1| and |beta - 1| from T0c's static solution at 1 AU, PASS line 2.3e-5 (hand estimate ~ (m r)^2 ~ 1e-30). DW: |gamma - 1| as a function of (fbar', fbar''), reported as an upper bound on the constants; DW passes only for the range it reports, and that range is compared with what the door would need (none needed: the door has no target amplitude to hit).
- G5-d GW speed and tensor propagation: NOT tested (literature status requested).

---

## (d) Hypotheses TESTED and NOT tested

TESTED: the localised RR action's field equations and conservation (sympy); the linear static weak-field response of RR and (DW, generic analytic f) about flat space for a point mass and CFG44's exponential sphere; the mass, shape and amplitude scaling against the target (the lemma plus numbers); the second-order (and inflated-parameter full nonlinear) static response of the localised RR equations, spherical, regular at the origin; the RR background and quasi-static linear growth for z >= 10; the kinetic-matrix signature and characteristic speeds; the Solar System static correction; the m and f constants count; the implied a0(z) if the tie reads rho_DE^eff(z).

NOT tested (each leaves the verdict UNDECIDED there, and no statement below claims anything about them): full nonlinear static solutions at galactic parameters if the ladder returns UNDECIDED or OPEN; non-spherical baryons; the relativistic sector beyond the weak field; homogeneous-solution freedom in U and S beyond the retarded prescription (only scanned as a bounded O(1) coefficient); the cosmological embedding beyond carrying Ubar, Sbar values as constants in the quasi-static local solution (time-dependent, retarded embedding is not solved); f with a branch point at Xbar(t) (a postulated target); other nonlocal models (Mashhoon-type is Door 1, Verlinde is Door 2; f(box^{-1}R) with other arguments, box^{-1} of the Gauss-Bonnet, transverse-projector variants of RR); a Schwinger-Keldysh completion of box^{-1}; the web, mergers, lensing slip data, KiDS, clusters; gravitational-wave propagation and the GW luminosity distance; the CMB temperature and lensing spectra beyond the background-shift line; ownership (bound-only) since Door 9 acts around all matter; the T5 max rule and double counting with a separate cold component (N13); the fit of DW's f to an expansion history.

---

## (e) MUTATE controls (each must change the headline and exit 1; declared control failures are kept)

Each script accepts `MUTATE=a|b|c|d|e`. The main run exits 0 iff every pre-registered claim P1-P8 of section (f) holds; a falsified prediction is kept and the run exits 1 as it falls.

- MUTATE a (planted match): replace m by the tuned value m_req(M_ref = 1e11, x = 0.1). Headline that must change: G1-A at (M_ref, x = 0.1) flips from FAIL to PASS, while G1-M (spread about 100 across masses) and G1-S (about sqrt(1 + x^2)) STAY FAIL and G4-a flips to FAIL (a tuned constant). Purpose: shows the harness can return a G1-A pass, so the main-run failure is real, and separates amplitude from scaling failure. Reported as a plant, never as a result.
- MUTATE b (sign flip): m^2 -> -m^2. The G1-sign line flips (repulsive), and |R_A| is unchanged.
- MUTATE c (inflated nonlinearity): eps = 0.05, m r = 0.5. R_NL must rise to O(0.1-1) and the decision flips from CLOSED to OPEN, showing the N1-N3 machinery detects nonlinearity and does not return small numbers by construction.
- MUTATE d (target injection): feed the target's rho_c in place of rho_eff. The comparator must return R_A = 1 to numerical precision and all G1 lines PASS (false-negative control for the comparison code, including the exponential-sphere C(r) integrals).
- MUTATE e (kinetic sign): replace the off-diagonal kinetic block by a positive-definite diagonal one. G5-a must flip from FAIL to PASS (ghost detector responds).

---

## (f) Expected outcome, stated BEFORE running (pre-registered predictions)

Honest expectation: Door 9 fails G1 on all three sub-lines, by scaling arguments that need no numerics (the linearity lemma) plus a huge amplitude gap; the correct report is a scoped no-go for the weak-field static response of RR and generic DW. G2 and G3 pass vacuously. G4 fails on the tie (and on the implied a0(z) if RR's dark energy is phantom-like, and on constants under R-B and DW). G5 fails on the localised action with free data (CFG50-type kinetic structure) and is PARTIAL under the retarded prescription. Solar System is passed trivially. No branch of this expectation says the door is closed against unlisted hypotheses.

Pre-registered claims (each is checked by a script line; any false one is kept and disclosed):
- P1 (amplitude): R_A is in [1e-17, 1e-7] at every grid point (hand estimate 1e-14 to 3e-9 including the sqrt(1 + x^2) growth, with mu^2 c1 uncertain by 1-2 orders); no point is within 10% of 1.
- P2 (shape): the G1-S spread is > 1.2 and matches sqrt(1 + x^2) (about 300 over x in [0.1, 30]) within 10%.
- P3 (mass scaling): the G1-M spread at fixed x is 1000 within 2% for the point-mass linear response.
- P4 (nonlinear ladder): R_NL <= 1e-3 at every grid point (hand estimate eps ~ 1e-9 to 1e-5), fitted exponent of eps within 1.0 +/- 0.15, fitted exponent of (m r) >= 0. DECISION FORK: if instead R_NL scales with 1/(m r)^2 and reaches >= 0.1 inside r_V, the verdict "nonlinear route closed" is withdrawn and the full nonlinear solutions at galactic parameters become the next phase; this is the one branch of the experiment whose outcome I do not consider excluded.
- P5 (G2): growth ratio and mu, eta within 5% at z >= 10 and H within 5e-3; recorded as vacuous.
- P6 (G3): reaction 0 by construction; E_eff / E_orb <= 1e-6 in both r_ta conventions; recorded as vacuous.
- P7 (G4): net new constants = 0 only under R-A; the tie is not produced by the action (G4-b FAIL); implied a0(5)/a0(0) departs from 1 by more than 1% if RR's w_DE < -1 (hand estimate about 30%).
- P8 (G5): a mixed-signature (ghost-like) sector exists in the localised action with free data; all characteristic speeds = c; |gamma - 1| <= 1e-25 for RR at 1 AU.

What would change this expectation: a nonlinear response with R_NL >= 0.1 (P4 fork); a homogeneous-solution or cosmological-embedding coefficient that is not O(1) (it would have to be about 1e10 to 1e14 to matter, which the retarded zero-data prescription forbids, so this is judged very unlikely); an f with a branch point (a postulated target, not a derivation). None of these has been run.

Process notes: no constant, function or prescription may be changed after the first G1 number is seen; scans over Ubar, Sbar coefficients (bounded, O(1)) are declared exploratory and reported as such; the script for each test is committed before its output. Independent re-derivation (rule 5) is requested by the orchestrator only if a door survives G1; the expected result here does not call for one, except a hostile re-derivation of the linearity lemma's numbers and of the N1 second-order series if the fork in P4 is not cleanly closed.
