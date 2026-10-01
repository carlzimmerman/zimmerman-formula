# CFG242: a swing at closure (Gaps 1 + 2: one legal owned object that is the law's dark density). PHASE 1: the triage, frozen before anything runs

Lane CFG242, phase 1 only. Intended repo path: `campaign_fresh_gravity/CFG242_FROZEN_CRITERIA.md`, committed before any phase-2 script. Nothing in the repo was edited; no physics script was written or run. The only code run in phase 1 was a few lines of arithmetic (multiplying the estimate factors of section 2 and dividing by the cost) to fill the table of section 5; that arithmetic is reproduced by hand in section 5.

Standing rules applied. kappa = 1/2 is FITTED and is never claimed derived. Nothing here says the theory is closed, and nothing says any data favour the framework. There is NO dark-matter particle and no new species: the cold mass the CMB needs (Omega_c h^2 = 0.12) is still REQUIRED by every route below, and no route supplies it. Ownership must be LEGAL (bound-only and causal) or the failure is named. Failed gates are design constraints. Literature facts not already in a committed file are labelled "from memory, unverified". A scoped no-go is not a theorem.

## 0. What was read, and the not-blind statement

Read in full or nearly so (the first 7,000-9,000 characters of the two longest, which cover their results): `closure_map/TEN_DOORS_RESULT_2026-09-29.md` (with the appended referee note), `closure_map/TEN_DOORS_GATES_2026-09-29.md`, `closure_map/DOOR11_RESULT_2026-09-29.md` (with addenda 1 and 2), `closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md` (with addenda and erratum 1), `closure_map/GAPS_1_2_JOINT_STATUS.md`, `closure_map/WHAT_WOULD_DECIDE_2026-09-29.md`, `CFG230_requirements_synthesis/CFG230_README.md` (R01-R12, the hard core R03-R12, the minimum cover {R03, R06}, the screening), `CFG44_fluid_target/README.md`, and `CFG48_gap1_switch/README.md` and `GATES_FROZEN.md`.

Read in part (the head, the gate or result tables, and every "not tested / untested / open" list, found by grep): `closure_map/GATES_STATUS_2026-09-29.md`, `closure_map/CLAIMS_AUDIT_2026-09-29.md`, `closure_map/SHARED_VS_SPECIFIC_2026-09-29.md` (the three large files were NOT read end to end; I read their heads and searched them for "legal", "bound-only", "Gap 1"), the README of each of CFG117, CFG118, CFG119, CFG120, CFG121, CFG122, CFG123, CFG124, CFG130, CFG131, CFG171, CFG172, CFG172D, CFG173, CFG174, CFG231, CFG232, CFG251, CFG252, CFG253, CFG254 (heads plus the untested lists), the READMEs of CFG49, CFG50, CFG70 and CFG72, and the ChainCert README (`fable_independent_2026/lean_2026/ChainCert/README.md`) by keyword (Dimension, Ownership, no-EFE, CalibrationWall), not end to end. CFG240's own README was not opened; its theorems were read only through the ChainCert table.

**Not-blind statement.** I have read the ten doors' results, door 11's variants, doors 12 and 13, CFG230's requirements and the Gap 1 / Gap 2 lanes before writing any estimate below. Every estimate is therefore informed by the failures it is meant to anticipate. The menu of routes is not a blind sample of the theory space: the listed routes are the record's own untested lists, and the post hoc routes (section 3) were written after reading the doors' failures and are flagged POST HOC. Frozen estimates are hand estimates from the rules of section 2, not probabilities from a model; their only use is to order work.

Two drafting-order facts, disclosed: (a) the eligibility rules (d) and (e) of section 2.4 were written after I had drafted the route paragraphs; I report the ranking with and without them (section 5.3). (b) The two top-ranked routes tie at a ratio of exactly 2.00 under the frozen factors; that came out of the factor structure (the two profiles share every factor but one) and was not engineered, but it is a boundary case and is reported as such.

## 1. The NOT TESTED list, verified against the sources

Line numbers are those of the files at the working tree I read. "TD" = `closure_map/TEN_DOORS_RESULT_2026-09-29.md`; "D11" = `closure_map/DOOR11_RESULT_2026-09-29.md`.

| Item in the brief's list | Source and line | Verified? |
|---|---|---|
| Relativistic completions of doors 1, 3, 5, 6, 10 | TD l.21 ("Relativistic completions (1, 3, 5, 6, 10)"); per lane: CFG120 README l.23 (relativistic completion with its lensing slip), CFG121 l.48, CFG124 l.25, CFG130 l.17 ("a relativistic completion"), CFG118 l.115-122 (hypotheses declared untested) | yes |
| Non-spherical baryons (all doors) | TD l.21 ("non-spherical baryons (all)"); CFG44 l.33 (a thin disc's tidal closure and enclosed-mass form differ 3-15x) | yes |
| Nonlinear / post-caustic cosmology (4, 6, 8, 9, 10) | TD l.21 | yes |
| Non-Lorentz-invariant vacuum or derivative coupling (door 8) | TD l.21; CFG131 l.18-22 (a vacuum with non-Lorentz-invariant stress; Q^mu with a spatial piece or a derivative dependence; a collisionless anisotropic-stress cold component; an action realising Q != 0) | yes |
| Self-interactions (door 7) | TD l.21; CFG119 l.106-118 (self-interactions, the excited-state envelope, non-spherical and time-dependent solutions) | yes |
| Hossenfelder's covariant Lagrangian (door 2) | TD l.21; CFG117 l.97, l.107-108; CFG231 l.106-110 (her Lagrangian term by term: "no offline access"); CFG231 scored a RECONSTRUCTED class V, not her action | yes |
| Whether f(E, L) is reached or stable (door 5) | TD l.21; CFG130 l.17 | yes |
| Boltzmann-code CMB (doors 3, 8) | TD l.21; CFG121 l.48; CFG131 l.18-22 | yes |
| A Schwinger-Keldysh completion (door 9) | TD l.21; CFG123 l.20 | yes |
| Rotational dust (door 10) | TD l.21; CFG124 l.25 | yes |

**Additional NOT TESTED routes found in the lane READMEs (not in the brief's list):**

| ID | Item | Source and line |
|---|---|---|
| (a) | Door 4: a relativistic completion with vortices and rotating cores, full Landau two-fluid hydrodynamics, a UV completion (the thermalisation rate), stream crossing of the core | CFG122 l.38 |
| (b) | Door 8, the "epoch channel": an M-dependence through the formation epoch, needing p proportional to rho_L^s with s >= 18 (about 180 at the flat-a0 limit); "not a route, not excluded in full" | CFG131 l.21 |
| (c) | Door 11: a directional flux treated as a FIELD rather than a fluid or beam; a flow whose constitutive law is derived rather than declared | D11 l.26 |
| (d) | Door 11C remnants: the aether's twist mode and c13 != 0, the projectable Horava class, AeST (vector plus scalar), KM1's nonlinear regime | CFG172 l.92-94 |
| (e) | Door 13 (BIMOND): other interaction scalars; a lapse-free spatial-scalar interaction with a preferred foliation; the DBI khronon dark sector; the nonlinear matching solution of the twin metric around a collapsed region, "the bimetric form of candidate B's Gap 1" | CFG232 l.119 |
| (f) | Gap 1 / Gap 2 open items: a covariant definition of the equipotential-enclosed-mass (ball) functional; the first-variation edge step of the ball gate; a Schwinger-Keldysh doubled-field treatment of the history variable ("untested exit"); screened or non-universal mediators; extended baryons and anisotropic f(E, L) for the exchange; the khronon foliation of every instantaneous-on-leaf coupling | CFG48 README l.69; GAPS_1_2_JOINT_STATUS l.18; CFG50 (relativistic completion, |h| near 1, non-spherical target); CFG72 (other mediators, vertices and operators) |
| (g) | A dynamical gate field beyond the scalar chi and a nonlocal or heat-filtered gate (a new length), gradient repair (DE13's K0) | CFG172D l.116; CFG49 (OPEN row) |
| (h) | Time-dependent inflows, nested systems (door 11A) | CFG171 l.100-106 |
| (i) | Door 3: baryon pressure before recombination, bigravity embeddings, mergers | CFG121 l.48 |
| (j) | Door 1: time-nonlocal or memory kernels; non-translation-invariant (enclosed-mass) kernels; kernels nonlinear or source-dependent | CFG120 l.23 |

Two items on the brief's list are better read as MODIFIERS than as routes (they cannot carry a0 or ownership by themselves): non-spherical baryons, nonlinear/post-caustic cosmology, and the Boltzmann-code CMB. They are given a paragraph in section 3.2 and are excluded from the ranking by rule (b) of section 2.4.

## 2. Rules fixed before any ranking

### 2.1 The target and the standing gates

Target (CFG44): C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r); law g_tot = nu(g_N/a0) g_N with P2 kernel nu = sqrt(1 + a0/g_N) primary and nu_mono reported; a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED; the cold conserved fluid is candidate B's. Point mass: M_c = M_b (sqrt(1+x^2) - 1), x = r/r_M, r_M = sqrt(G M_b / a0). Real cold mass needed at x = 30 is 29.0 M_b against the cosmic share Omega_c/Omega_b = 5.36 M_b (so the target needs cold mass gathered from beyond the baryons' own Lagrangian region; CFG131 D4 puts the limit at x* = 20.2 for vacuum conversion).

The shared gates G1-G5 are copied VERBATIM from `closure_map/TEN_DOORS_GATES_2026-09-29.md` (5ef77ea09):

- **G1 target.** The mechanism reproduces C(r) = rho_c r^3 g_tot = (a0/4pi) M_b(<r) for a point mass and for CFG44's exponential sphere, to within 10% over x = r/r_M in [0.1, 30], for baryon masses 10^9 to 10^12 Msun, with the SAME constants at every mass.
- **G2 CMB and growth.** Linear cold behaviour at z >~ 10 with growth within 5% of LCDM to k = 30/Mpc (CFG43's linear-growth test), and no change to the CMB lensing and TT/TE/EE constraints (CFG4_cosmology): state the perturbation equations.
- **G3 reciprocity and energy.** The reaction on the baryons <= 0.10 g_law over x in [0.3, 30] and the energy the mechanism must supply <= the baryons' orbital energy, in BOTH r_ta conventions (CFG48 G4's pass lines).
- **G4 constants.** No constant beyond kappa and Omega_c h^2; a0's tie to Lambda is the CFG43 tie (P_cap = (kappa^2/8pi) rho_Lambda c^2) or a stated equivalent.
- **G5 well-posedness.** No ghost, no gradient instability, hyperbolic/causal (the DE12/DE13/XC criteria); Solar System safe (Cassini) by an explicit statement.

The door rules also apply: (1) a route's frozen criteria precede its scripts; (2) a door may add gates but may not weaken G1-G5; (3) every constant beyond kappa = 1/2 and Omega_c h^2 = 0.12 is a G4 FAIL unless tied to Lambda or kappa in the same action; (4) a MUTATE control must change the headline; (5) a route that survives G1 gets an independent re-derivation before it is reported.

Legality of ownership (the extra route-level precondition of this lane, section 4.1): the owned object must be **bound-only** (vanish or be inert in unbound and cosmological regions) and **causal** (depend only on data in the past light cone). Top-level ownership (a satellite or an embedded system owns nothing; FG001 and DR4 Arm C) is a further property needed for the Solar-System half of G5 (R09) and is scored as a reported row, because the Lean theorem `ownership_not_field_local` says no function of the local field data at one time reproduces it.

### 2.2 The estimate rule (frozen)

For each route I list the persistent failures it would carry BY CONSTRUCTION (read off the cited lane; counted once per root cause; a failure of R09 that is the consequence of a missing ownership object is counted under R07, not twice):

- T = a persistent THEOREM-grade failure (a CFG230 requirement with a THEOREM core, a Lean-certified statement, a closed-form energy or budget inequality, or a failure by a factor >= 100 in a committed number). Factor 0.25 each.
- S = a persistent SCOPED / DECLARED-grade failure (a gate cell marked F in a committed lane, a new constant (G4), or a gate that passes only as a restatement, "p*"). Factor 0.6 each.
- A **lift** = a counted failure that a source-listed untested premise (section 1) would remove if the route uses that premise. The factor of a lifted failure is the square root of its normal factor (T: 0.5, S: 0.775). A listed hatch that lifts a failure I did not count earns nothing.
- Bonus: x1.5 for each of R05 (cold early) and R07 (a bound-only causal switch) that the route meets in its own definition, not by an argument. R01 and R02 earn no bonus (a scale that is declared is not derived; CFG230 finds only D02 and D04 meet R02 as a mechanism).

P(all) = 0.014 x (product of the factors). The base 0.014 is Laplace's rule for 0 successes in about 70 scored classes (CFG44's tally D = 0 of 54 constructions; ten doors; doors 11-13; the CFG230 screening), i.e. (0 + 1)/(70 + 2). The frozen result is a number to order work, not a probability model. A route with PRE-DEAD status (section 2.4 (c)) gets three T factors.

P(cheapest gate) is a separate hand estimate with its basis stated in each paragraph.

### 2.3 The cost rule (frozen)

One agent-hour is one agent working one hour, about one committed script with a MUTATE control. C_full = the agent-hours to run G1-G5 to completion plus the legality test: C_full = B + 11.8, where 11.8 = G1 3.0 + G2 3.0 + G3 2.0 + G4 0.3 + G5 2.0 + legality 1.5, and B is the build and control cost (1-5 h; 2-3 when a committed lane's code can be imported read-only). C_full is used for the ranking, not the expected cost under the stop rule, because a pass requires all five gates to be run: ranking by expected cost under the stop rule would put the cheapest-to-kill routes first, which is a ranking of what is cheap to close, not of what is likely to work.

### 2.4 Eligibility and ranking rules (frozen)

A route is ELIGIBLE for phase 2 only if all of the following hold:
- (a) it does not add a dark-matter species or particle (standing rule); routes that do are listed with their score but EXCLUDED;
- (b) it is a route and not a modifier (it contains a mechanism hypothesis for a0 and for ownership, or can carry one);
- (c) it is not PRE-DEAD: a Newtonian-only mechanism with no c and no Lambda-or-H in its field equations is PRE-DEAD, because the Dimension theorem (ChainCert `no_sqrtM_length_GMc`, `sqrtM_length_iff`; CFG230 R02, monomial family and G4 only) gives it the M^(1/3) length (door 6: x_ta spread 3.165, CFG158) and not M^(1/2); the theorem is conditional on its premises, so a route is PRE-DEAD only for as long as it does not insert an acceleration scale by hand;
- (d) the route's model class can be written NOW as a specific set of field equations (CLASS FIXED), and does not reduce on inspection to a class already scored in a committed lane (a family whose members all reduce to scored classes is CLASS NOT FIXED);
- (e) the class contains an ownership candidate, an object that could be bound-only and causal in principle, so that the legality test of section 4.1 is not vacuous. A pure law with no hierarchy datum cannot pass R07 or R09 (Lean `ownership_not_field_local`; CFG188's tail theorem), so running it answers nothing new about Gaps 1 and 2.

**Ranking rule.** Score = P(all) / C_full. Order the eligible routes by score. Ties (scores within 1%) are broken first by P(cheapest gate pass), then by route ID. If the top two eligible routes' scores are within a factor 2 (ratio <= 2.00, inclusive), phase-2 criteria are frozen for BOTH and they are run separately and never pooled. The same rule applied to all routes without (d), (e) is reported as a sensitivity (section 5.3), not used.

## 3. The routes

Each paragraph gives: the mechanism hypothesis in words and the single equation or structural property it rests on; the requirements (CFG230 R01-R12) it would meet or fail BY CONSTRUCTION; the earlier no-go it must escape and why it might; the cheapest decisive gate of G1-G5 with a cost; and the frozen estimates (the profile T / S / lifts / bonus, P(all), P(cheapest gate)). Literature facts are from memory, unverified.

### 3.1 Routes the record lists as not tested (IDs L1-L14a, L18)

**L1. Door 1 beyond fixed kernels: a causal, time-nonlocal law with a nonlinear, source-dependent kernel (the relativistic completion of Mashhoon-type nonlocal gravity; CFG120 l.23).**
Mechanism: the dark acceleration is a retarded memory of the Newtonian field with a Lambda-timed range, a_d(x, t) = integral_{-inf}^{t} K(t - t') F[g_N(x, t')] dt', with K normalised and range tau_L = 1/(kappa sqrt(G rho_Lambda)). Structural property: the nonlinearity of F is what lifts CFG120's linear-response theorem (a fixed kernel gives R proportional to M_b; the LP residual is 31.6228; R01 THEOREM core); the time kernel is what a relativistic completion adds. By construction: R02 only as declared (a0 sits inside F); R01 only as declared; FAILS R07 (the law has no hierarchy datum; `ownership_not_field_local`), hence R09 (isolated tail >= 0.282 a0, CFG188) and G5 Cassini; the Bianchi problem of CFG120 G3 is not resolved by a kernel; the static limit is a declared function of g_N, so G1 can pass only as a restatement (compare CFG171 L4, CFG231 K1). Earlier no-go to escape: CFG120 (R proportional to M_b; fixed kernel). It can escape only by nonlinearity, which makes it AQUAL/QUMOND restated. An enclosed-mass kernel (the non-translation-invariant option in CFG120 l.23) is the Volterra gate that CFG48 G6 found stable but bilocal, and CFG70/CFG72 already scored its retarded exchange form. Cheapest decisive gate: G5 (the tail theorem applied to the static limit), about 1 h; it fails unless an ownership object is supplied, which this class does not contain. Profile T1 (R07), S2 (Bianchi; G4 / G1 restatement), no lifts. P(all) = 0.014 x 0.25 x 0.36 = 1.26e-3. P(cheapest gate) = 0.02 (the theorem applies to any (yq)' >= 0 kernel). Fails eligibility (e).

**L2. Door 3: a relativistic completion of dipolar dark matter / gravitational polarisation (CFG121 l.48).**
Mechanism: dark density as the divergence of a polarisation sourced by g_bar, rho_d = -div P, P = chi_g(g_bar) (from memory, unverified: Blanchet-Le Tiec dipolar DM has a vector-field Lagrangian with this Newtonian limit). By construction FAILS R05 / G2: the medium budget needs Q^2/kappa_I >= about 140 against <= 0.16 (V_U) or 1.2 (V_B) from growth, a gap of 115-860x (CFG121 T1.2, reproduced by CFG157), which is a statement about the Newtonian and cosmological budget and does not depend on a relativistic completion; also FAILS G4 (Q, kappa_I new constants). It adds a polarisable medium with its own constants, which is a new dark species (standing rule). Earlier no-go: CFG121 (medium budget); a completion can only change G5 (the ghost question for V_B). Cheapest decisive gate: G2 (the budget algebra, reusable from CFG121), about 1 h. Profile T2 (budget 115-860x; no single polarisation law), S1 (G4). P(all) = 0.014 x 0.0625 x 0.6 = 5.25e-4. P(cheapest gate) = 0.02. EXCLUDED by (a).

**L3. Door 5: is the f(E, L) with beta = -(3/2) rho_b/rho_b_bar reached, and is it stable (CFG130 l.17)?**
Mechanism: collisionless violent relaxation lands on f(E, L) >= 0 with the Jeans identity d(rho sigma_r^2)/dr + 2 beta rho sigma_r^2/r = -rho dPhi/dr. Structural property: the Newtonian-only scale. By construction FAILS R01 and R02 (no c, no Lambda in the field equations: M^(1/3) from the turnaround, door 6) and G1 as a mechanism (CFG130: f encodes the target, "realisable, not a mechanism"). Stability (radial-orbit and tangential-instability criteria, from memory, unverified) is a side question; even a stable f is not reached with the right scale. PRE-DEAD (c). Cheapest decisive gate: G5 stability (about 2 h), P = 0.40, but it is moot. P(all) = 0.014 x 0.25^3 = 2.19e-4 (PRE-DEAD: three T).

**L4. Door 6: non-spherical, relativistic, post-caustic secondary infall (CFG118 l.109-122).**
Mechanism: cold infall with tidal torques and a distribution of angular momentum onto a baryon core. Structural property: r_ta proportional to M^(1/3) for Newtonian gravity plus Lambda; angular momentum is a dimensionless factor, so the exponent stays 1/3. A relativistic completion adds corrections of order v^2/c^2 (<= 3e-4, CFG44), not a scale. By construction FAILS R01 / R02; CFG158 reproduces the x_ta spread 3.165. PRE-DEAD (c). Cheapest decisive gate: G1 scale exponent (a 3-D shell code, B = 5 h). P(cheapest gate) = 0.03. P(all) = 2.19e-4.

**L5. Door 10: a relativistic mimetic completion with rotational dust (CFG124 l.25).**
Mechanism: the mimetic constraint g^{mu nu} d_mu phi d_nu phi = -1 makes an irrotational dust; relaxing irrotationality (a non-gradient velocity part) might remove the ghost. Structural property: c_s^2 = g t/(2 - 3 g t) is a ghost for every 0 < g t < 2/3 (CFG124 THEOREM S+R, reduced unitary-gauge action). By construction FAILS: no stationary state in the static weak-field limit (T), and G4 (the free time scale t is a new constant unless tied to Lambda, S); the ghost is lifted only if rotational dust removes it (the listed hatch). My unscripted arithmetic note (hand note, unverified): with t = tau_L and g near a0, g t_L / c is of order g/a0, so the MOND regime sits inside the ghost window; if so the mimetic dust is healthy only in the Newtonian regime, the opposite of what is wanted. There is no ownership candidate in the class. Cheapest decisive gate: G5 (the quadratic action of the rotational extension), about 2.5 h; P = 0.15. Profile T1 (no stationary state), S1 (G4), one T-lift (ghost). P(all) = 0.014 x 0.25 x 0.6 x 0.5 = 1.05e-3. Fails eligibility (e).

**L6. Door 4: a relativistic completion of the superfluid, with vortices, rotation, stream crossing and a UV completion (CFG122 l.38).**
Mechanism: the Berezhiani-Khoury P(X) proportional to X^(3/2) EFT (from memory, unverified) with a phonon force. Structural property: the amplitude goes as M^(1/2) while the target's goes as M^0 (spread 31.62; THEOREM S+R, CFG154), and the MOND branch has c_s^2 < 0. By construction FAILS R01 (T) and R11 and G4 (new constants of the EFT; S2). It is a condensate of particles: a new dark species. Cheapest decisive gate: G5 (c_s^2 sign for the rotating background), about 3 h; P = 0.10. P(all) = 0.014 x 0.25 x 0.36 = 1.26e-3. EXCLUDED by (a).

**L7. Door 7: self-interactions and the excited-state envelope of the fuzzy-DM soliton (CFG119 l.106-118).**
Mechanism: Schrodinger-Poisson with a quartic coupling, i hbar psi_t = -hbar^2 lap psi/(2m) + m Phi psi + lambda |psi|^2 psi. Structural property: the soliton core is flat where the target goes as 1/r; growth needs m >= 1.28e-20 eV (CFG119). A boson species and a new constant lambda (G4). By construction FAILS G1 (T), G4 and G2 (S2). Cheapest decisive gate: G4, by counting (0.5 h), P = 0.01. P(all) = 1.26e-3. EXCLUDED by (a).

**L8. Door 8: a non-Lorentz-invariant vacuum, or Q^mu with a spatial piece or derivative dependence (CFG131 l.18-22).**
Mechanism: the vacuum energy density becomes a field with local gradients, T_vac = -rho_L(x) c^2 g, so that nabla_mu T_c^{mu nu} = nabla^nu rho_L (a buoyancy force on the cold fluid); the pressure the target needs is P/P_cap = 1/x^2 with P_cap = kappa^2 rho_Lambda c^2/(8 pi), so the vacuum density would have to vary by about 1% over a halo. By construction: R02 only through the entry of rho_Lambda (no tie derived); FAILS R06/R12 energy: the cold mass the target needs beyond x = 6.29 exceeds the cosmic share, and beyond x* = 20.2 it exceeds all the vacuum energy in the baryons' Lagrangian volume (CFG131 D4; Lorentz-independent because it is an energy-conservation inequality), T; G4 (xi, C, n untied), S. The hatch: a spatial or derivative Q^mu lifts the "p(rho_c) is one function in every halo" theorem (CFG131 D1: required p differs 32-353x across 1e9-1e12 Msun), one T-lift. On inspection every member of the family reduces to a function of baryon-slaved fields, so it is a CFG44 B2/B3 closure (far-shell theorem), the CFG50 tidal closure, or a CFG172 aether stress: CLASS NOT FIXED, eligibility (d) fails. Cheapest decisive gate: G3 energy source (the ledger against the vacuum energy in the available causal region), about 2 h. P(cheapest gate) = 0.01. Profile T1, S1, one T-lift. P(all) = 0.014 x 0.25 x 0.6 x 0.5 = 1.05e-3.

**L9. Door 2 / door 12: Hossenfelder's covariant Lagrangian, term by term (CFG117 l.97; CFG231 l.106).**
Mechanism: an action with a vector field whose elastic energy gives Verlinde's D(E). CFG231 scored a RECONSTRUCTED class V (eight variants, none passes G1; K1 reproduces the point-mass target only because it restates P2, with Q2 = 6.1e3 x the bound and a ghost-sign problem). Her actual terms are not available offline (CFG231's own note). NOT RUNNABLE offline: eligibility fails by a rule I should state: a route whose defining equations cannot be read in this session cannot have its class fixed. No estimate is given (it would be a guess about an unread paper). Not ranked.

**L10. Door 9: a Schwinger-Keldysh completion of the nonlocal operator and a nonlinear embedding (CFG123 l.20).**
Mechanism: replace box^{-1} in the localised Deser-Woodard / RR field equations by the retarded (in-in) Green function. Structural property: the SK completion makes the operator causal; the binding failures are the MAGNITUDE and SIGN of the localised static response (a negative density about 10 orders too small) and the signature (2, 2); a causal propagator does not change a static linear response. By construction FAILS R01 (linear response, T), the Solar System (door 9 G5 F; T), signature (2, 2) and G4 (S2). No ownership candidate: ineligible (e). Cheapest decisive gate: G1 magnitude, about 1.5 h; P = 0.03. P(all) = 0.014 x 0.0625 x 0.36 = 3.15e-4.

**L11. Door 11: a directional flux treated as a field, or a flow with a derived constitutive law (D11 l.26).**
Mechanism: the medium's momentum density as a vector field with a conserved stress-energy. Structural property: a w = -1 medium cannot flow (T^{0i} = (1 + w) rho gamma^2 c v vanishes; SR algebra, Lean-grade L); a massless flow's own gravity is at most 1.2e-6 of the phantom (CFG173 S2); a push is Le Sage gravity. A field has the same stress-energy bound. By construction FAILS R12 (T), the gravity budget (T, 1e6), the Le Sage sign change (T), and G8 / G4 (S). Cheapest decisive gate: G1 own-gravity bound, about 1.5 h; P = 0.02. Profile T3, S1. P(all) = 1.31e-4. Ineligible (e).

**L12. Door 11C remnants: the aether's twist mode and c13 != 0, the projectable Horava class, AeST (CFG172 l.92-94).**
Mechanism: a unit timelike vector or khronon with a Lambda-tied coefficient. Structural property: for any kernel with (yq)' >= 0 inside the +-10% G1 band the isolated tail is >= 0.282 a0 (CFG188, P2), Q2 3.5e3-6.3e3 x the bound without screening or ownership; for a single F(K) the G1 requirement (t <= 1.2e-6) and the G6/G7 requirement (t >= 4e6) differ by 3e12 (R10; CFG172). By construction FAILS R09 / R07 (T, no ownership object), c_s^2 < 0 in 11C-c (S); the R10 pincer is lifted by listed hatches (twist mode, a different action such as AeST, from memory, unverified), one T-lift. Cheapest decisive gate: G5 (the tail theorem), 0.5 h; P = 0.02. Profile T1, S1, one T-lift. P(all) = 1.05e-3. Ineligible (e).

**L13. Door 13 remnants: BIMOND with a lapse-free, preferred-foliation interaction, and the nonlinear matching of the twin metric (CFG232 l.119).**
Mechanism: Milgrom's bimetric theory (from memory, unverified: Milgrom 2009, matter coupled to g, a twin metric g-hat, an interaction M(g, g-hat)); the interaction replaced by a function of the SPATIAL metrics of a shared preferred foliation, which should remove the fourth-order Stuckelberg vector (CFG232 G5a F reproduces WF2/L70) and may supply ownership through how g-hat matches around a collapsed g region (R-static versus R-add, "the bimetric form of candidate B's Gap 1"). Structural property: the twin metric's matching solution decides whether the phantom stays inside the collapsed region; the vacuum tie is native in 13b-ii (kappa^2 = -16 pi beta/(sigma_s M_0), kappa tied to M_0 rather than to nothing). By construction FAILS the canonical energy of the interaction sector (19-254 x the baryons' orbital energy, negative sign; T), the cold-fluid coupling G1-C (g_tot/g_target = nu(g_target), 1.31 at x = 1 to 5.57 at x = 30, and a sign reversal for the g-hat coupling; S), G4 (a0 free; gamma/beta; u1/u0; S); G1-law passes only by inversion (M1-inv, "P-decl"). Lifts: the ghost (S, by the foliation) and the Solar-System tail (T, if the matching supplies ownership). Cheapest decisive gate: G5a ghost / hyperbolicity of the foliated quadratic action, about 3 h (CFG232 A2 reusable); P = 0.15. Profile T1, S2, T-lift 1, S-lift 1. P(all) = 0.014 x 0.25 x 0.36 x 0.5 x 0.775 = 4.88e-4.

**L14a. Gaps 1 and 2 joint remnant: a causal (Schwinger-Keldysh / closed-time-path) ownership latch whose exchange is funded by a vacuum reservoir (CFG48 README l.69; GAPS l.18, "the doubled-field history variable", "unfunded reservoir").**
Mechanism: CFG48 G3 found that a history variable inside an action has an Euler-Lagrange residual depending on the future (advanced dependence 8.5e-4 and 1.7e-2), so the only causal carrier was a prescribed label; the standard cure is a doubled-field action in which the latch obeys a retarded relaxation, tau_n dn/dt = s(-theta_b/3H)(1 - n) - [1 - s(-theta_b/3H)] n, with s a declared smoothstep (from memory, unverified: Galley's closed-time-path action for nonconservative systems). CFG70 found that a causal, reciprocal exchange gives back CFG48 G4's reaction (0.065-22.5 g_law) and energy (57-318 x orbital, B's r_ta; 23-73 x in CFG48's) for every retarded kernel, passing only with an unfunded reservoir (r = 0; N6: reaction met in 5 of 6 cells) or an untied coupling. The untested pair is: a latch that is legal in the doubled-field sense, and an exchange whose reservoir is identified as the vacuum energy through a dynamical vacuum field with a closed ledger, with the memory time tied, tau_bar = tau_L = 1/(kappa sqrt(G rho_Lambda)). Structural property: the heat the target needs is of order (r_e/r_M) x (1/2) M_b V_f^2, which is about 1e-5 of M_b c^2, so in energy terms the vacuum can pay (rho_c sigma^2/(rho_Lambda c^2) of order 1e-4 to 3e-2 in a halo, giving an a0 shift of a few percent at most; this is a hand estimate, unscripted); the open questions are causality of the supply and the 1% flat-a0 line. By construction: R02 is met only through the ledger (a0 enters through rho_Lambda; the target is still SUPPLIED); R07 is the thing tested (legal bound-only, causal); FAILS R06 in the closed class (T, lifted by the funded reservoir), top-level ownership by locality (a latch sourced by theta_b <= 0 alone is CFG251's reading (iii-b) "any collapse": the Sun gets a P2 monopole 1258-1545 x the bound, T, lifted only by an inhibitor field whose reach needs a mediator with an untied beta = 1, CFG72), and G1 as a mechanism (the target is supplied, G1 can pass only as P-declared; S), G4 (the inhibitor coupling; S). Lift: the advanced dependence of the history variable (S, by the doubled field). Cheapest decisive gate: G3 strict (the closed forms of CFG70, a replay, 0.5-1 h) with P = 0.01; the new, decisive content is the legality test (G0 of section 4.1, 1.5 h) and the funded reading of G3. Profile T0, S2, T-lift 2, S-lift 1. P(all) = 0.014 x 0.25 x 0.36 x 0.775 = 9.76e-4 (T-lift twice: 0.5 x 0.5 = 0.25).

**L18. Door 8's epoch channel (CFG131 l.21).**
Mechanism: p = p(rho_c; Lambda) with a dynamical Lambda, so the effective EOS depends on the formation epoch. Structural property: p proportional to rho_L^s with s >= 18 at xi = 0.3 (s about 180 at the flat-a0 limit). By construction FAILS G4 (a tuned new exponent; the CFG131 note itself says "not a route"; T), the a0(z) flat law (the framework's own distinctive law; S), the unmapped M(z_f) (S). The class is not fixed (the map from mass to formation epoch is undefined). Cheapest decisive gate: G4 by counting, 0.5 h; P = 0.02. P(all) = 0.014 x 0.25 x 0.36 = 1.26e-3. Ineligible (d).

### 3.2 Modifiers (not ranked; rule (b))

**M1. Non-spherical baryons (all doors; CFG44 l.33).** A modifier of the G1 target: for a thin disc the tidal closure and the enclosed-mass form differ by a factor 3-15 (CFG44), and QUMOND carries a curl term. It cannot carry a0 or ownership. G1 as frozen tests only the point mass and the exponential sphere, so a non-spherical run would be a new gate, not a route. Carried as the not-covered item N1.

**M2. Nonlinear and post-caustic cosmology (4, 6, 8, 9, 10).** A modifier of G2 (the frozen G2 is a linear-growth gate). Cannot carry a0 or ownership.

**M3. A Boltzmann-code CMB (3, 8).** The completion of G2 for any route that reaches it; for every route here G2's CMB half is UNDEFINED until one is run. Cannot carry a0 or ownership.

### 3.3 POST HOC routes (added after reading the doors' failures; flagged)

The cross-door reading (a READING, not a theorem: the missing object must itself carry an acceleration scale) and the Dimension theorem (a length proportional to M^(1/2) needs one extra constant X that is not a monomial in G and c; r_M^2 = (G M/c) (c/H) / kappa', the geometric mean of the gravitational radius and the Hubble radius) point to the following routes. They are written knowing the failures, and none has been tested.

**H1. Ownership on baryon boundness (binding energy), with the de Sitter term.**
Mechanism: the owned region is where a cold element's energy in the retarded total potential, including the Lambda term, is negative: E = v^2/2 + Phi - Lambda c^2 r^2/6 < 0. It is bound-only by definition, and it is causal if the potential is retarded. Structural property: the boundary of the bound region is the turnaround radius, proportional to M^(1/3). By construction FAILS R01 / R02 (Newtonian plus Lambda, no c; PRE-DEAD, (c)). It is also partly scored: CFG48 G2 puts the boundness edge at sqrt(3) r_M (0.05-0.11 r_e), Sun ON by every monotone gate; XR36's turnaround gate (theta_b <= 0) has a ghost pole on 24 of 24 layers; CFG172D's theta gate is stable only because it is blind. Cheapest decisive gate: G1 edge radius (hand arithmetic from CFG48 G2), about 0.5 h; P = 0.02. P(all) = 2.19e-4.

**H2. A kinematic origin: r_M^2 = (G M/c) t_L, a causal relaxation with D = r^2 g_N / c.**
Mechanism: an auxiliary baryon-slaved scalar relaxes causally (a telegraph or Cattaneo equation) with diffusivity D(r) = r^2 g_N/c over the time t_L = 1/(kappa' sqrt(G rho_Lambda)), so the memory length is l(r) = r sqrt(g_N/a0) = r/x. Structural property: x^2 = c/(g_N t_L), i.e. the deep regime is where the velocity gained in a Hubble time, g t_L, is below c; this is the monomial identity of the Dimension theorem, not a derivation of any dynamics. By construction R01 and R02 would hold as a scale, but no action is written (CLASS NOT FIXED, (d)); the exchange it implies is CFG70's (reaction and energy kernel-independent, with the memory time at or above a free-fall time giving a reaction below 1% but a fluid that cannot track the target, CFG72), T; and a purely local relaxation latches "any collapse", so Cassini fails (T). Cheapest decisive gate: G3 energy source, 1 h; P = 0.05. Profile T2, S1 (the tie of the O(1) factor between D and GM/c is a constant). P(all) = 5.25e-4. Ineligible (d).

**H3. Causal screening of the dark density by the baryonic potential depth.**
Mechanism: the dark density is sourced only where the retarded potential depth |Phi_b|/c^2 exceeds a threshold. Structural property: a depth threshold Phi_b(r_e) = const puts the edge at r_e proportional to M, and the (G, M, c) monomial family has no length proportional to M^(1/2) (ChainCert `no_sqrtM_length_GMc`); a gradient trigger (|g| = a0, R02b) is a different object, the MOND field itself. By construction FAILS R01 by the lemma (PRE-DEAD (c)). Cheapest decisive gate: G1 scale exponent, a one-line check (0.5 h). P(all) = 2.19e-4. P(cheapest gate) = 0.01.

**H4. A gradient-flow reading of the vacuum with an alpha_1-bounded ownership.**
Mechanism (my reading of the brief's "a1-bound": bounded by the alpha_1 preferred-frame limit; if something else was meant, say so before phase 2): the vacuum energy density relaxes along a gradient flow, d rho_vac/dt = -Gamma dF/d rho_vac, where F contains the gravitational field energy density |g|^2/(8 pi G) compared with the cap P_cap = a0^2/(8 pi G) = kappa^2 rho_Lambda c^2/(8 pi) (the CFG43 tie). Structural property: the cap is exceeded where g > a0 (inside r_M; P/P_cap = 1/x^2 for the target pressure, "checked", CFG230 R12) while the dark density is needed where g < a0; the trigger acts on the wrong side. By construction FAILS the trigger side (T), the vacuum energy budget as in L8 (T), and G4 (Gamma; S1). CLASS NOT FIXED (F is unspecified): ineligible (d). Cheapest decisive gate: G1 trigger side (hand), 1 h; P = 0.03. Profile T2, S1. P(all) = 0.014 x 0.0625 x 0.6 = 5.25e-4.

**H5. An emergent-time (relational clock) construction.**
Mechanism: the cosmic time in a0 = kappa c sqrt(G rho_Lambda) is replaced by a clock defined from the baryon congruence, so the "Hubble time" is local. Structural property: unimodular gravity makes the flow gauge (CFG177: "no new content"); the theta-sourced gate of CFG172D is stable only because it is blind. By construction FAILS G4 (a clock field's constants) and R07 (a local clock is a local gate; T, Gauss lemma); S2. CLASS NOT FIXED. P(all) = 1.26e-3 under the rule; I do not regard the number as informative. Ineligible (d).

**H6. Fluid-borne ownership: the switch reads the cold fluid's own multi-stream or dispersion state.**
Mechanism: the law's gate reads the shell-crossing count or the dispersion tensor of the cold Vlasov fluid, which is zero in single-stream cosmological flow (bound-only and cold-early by definition) and causal. By construction it meets R05 and R07 as a definition (x1.5 each); but MS1 (`real_research/mond_sector_gate_2026/MS1_gate_variation_reciprocity.py`) shows a gate reading the carrier leaks the carrier's gravity, -C W' B/(8 pi G), 0.6-60 x the carrier's gravity at L*; the Gauss lemma applies to a gate on the flux (CFG48 G1); G1 is a restatement; and a dust action has no continuation past shell crossing, so the class is not writable as a legal action. Profile T2 (MS1, Gauss), S2 (p*, G4), bonus x2.25. P(all) = 0.014 x 0.0625 x 0.36 x 2.25 = 7.09e-4. Cheapest decisive gate: G3 reciprocity (the MS1 leak size), 1.5 h; P = 0.02. Ineligible (d).


### 3.4 The by-construction requirement profile used for the T / S counts

Legend: F = fails by construction (from the paragraph above, citing the CFG230 requirement and the lane that measured it); M = met by construction as a mechanism; d = met only as a declared choice (a0 or the shape is put in by hand); ? = open or lifted by a listed hatch; blank = not applicable or not decided by the definition. R01 scale, R02 acceleration scale, R03 shape, R04 closure, R05 cold-early, R06 reciprocity and energy, R07 bound-only switch, R08 EFE branch (never an F: a branch choice), R09 Solar tail, R10 preferred frame, R11 stability, R12 medium / tie / constants. This is the hand reading behind the factors of section 2.2, not a CFG230 re-scoring; CFG230's own matrix covers the ten doors and doors 11-13 only.

| Route | R01 | R02 | R03 | R04 | R05 | R06 | R07 | R09 | R10 | R11 | R12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | d | d | d | | | | F | F | | | |
| L2 | | | F | | F | | | | | ? | F |
| L3 | F | F | d | | | | | | | | |
| L4 | F | F | | | | | | | | | |
| L5 | ? | d | | | ? | | | | | ? | F |
| L6 | F | M | | | | | | | | F | F |
| L7 | | | F | | F | | | | | | F |
| L8 | | d | | ? | | F | | | ? | | F |
| L10 | F | | | | | | | F | | F | F |
| L11 | | | | | | F | | | F | | F |
| L12 | | d | | | | | F | F | ? | F | |
| L13 | | d | | | | F | ? | ? | ? | ? | F |
| L14a | | d | d | | ? | ? | ? | ? | | ? | F |
| L18 | | | | | | | | | | | F |
| H1 | F | F | | | | | d | | | | |
| H2 | d | d | | | | F | F | | | | F |
| H3 | F | | | | | | | | | | |
| H4 | | | F | | | F | | | ? | | F |
| H5 | | | | | | | F | | | | F |
| H6 | | | | | M | | M / F | | | | F |

For L14a the R07 cell is "?" because it is the thing phase 2 tests (G0), not an argument; the R12 F is the untied inhibitor coupling beta = 1 (CFG72) in Arm A3 and the tied tau_L in A2 is a candidate pass of G4. For H6 the R07 cell is mixed: bound-only and causal by definition (M), the Gauss lemma and the MS1 leak make the gated law fail (F).

## 4. Phase-2 plan

The two top-ranked ELIGIBLE routes by the rule of section 2.4 are L14a and L13 (section 5): a ratio of 2.00, inclusive of the "within a factor 2" rule. Phase-2 criteria are frozen for both below, they are run separately (separate scripts, separate outputs, separate verdicts) and never pooled.

### 4.0 Common frozen items

- **Footings.** The canonical a0 = 9.3603e-11 m/s^2 and the alt footing 1.1312e-10 (the two footings in CFG48's header). P2 primary, nu_mono reported. Baryon masses 1e9, 1e10, 1e11, 1e12 Msun; x in [0.1, 30]; point mass and CFG44's exponential sphere (imported read-only from CFG44's `Bcommon`, not restated here); both r_ta conventions (CFG48's and B's committed one, the phantom-inclusive law's enclosed mass).
- **Constants ledger.** Allowed beyond the declared function shapes: kappa = 1/2 (FITTED) and Omega_c h^2 = 0.12 only. Declared function shapes are allowed only where this file names them (a smoothstep with its interval, a memory-kernel family, the CFG70 target forms); every other number appearing in a script is a departure and is disclosed.
- **Gates.** G1-G5 as copied in section 2.1, with NO weakening. Each cell is P / F / U / N / p* (p* = passes only as a restatement or trivially).
- **Stop rule.** Stop at the FIRST binding FAIL of each arm, report it as a scoped no-go on the frozen class with the binding failure NAMED (gate, cell, number). A U or p* cell does not stop the run but is never counted as a pass. A failed reproduction control stops the arm and is reported.
- **Scripts.** Route A: `CFG242_A_controls.py`, `CFG242_A_g0_legality.py`, `CFG242_A_g4_ledger.py`, `CFG242_A_g3_exchange.py`, `CFG242_A_g5_solar_stability.py`, `CFG242_A_g1_target.py`, `CFG242_A_g2_growth.py`, `CFG242_A_verdict.py`, `CFG242_A_run_all.sh`. Route B: `CFG242_B_controls.py`, `CFG242_B_g5a_ghost.py`, `CFG242_B_g4_ledger.py`, `CFG242_B_g0_legality_matching.py`, `CFG242_B_g3_energy.py`, `CFG242_B_g5b_solar.py`, `CFG242_B_g1_target.py`, `CFG242_B_g2_frw.py`, `CFG242_B_verdict.py`, `CFG242_B_run_all.sh`. Each physics script reads `MUTATE=<m>` from the environment and writes outputs named by mode (`<script>_MUTATE_<m>.out` / `_results.json`), never overwriting the main run's. Each script under 15 min; exit convention: a main run exits 0 iff its reproduction controls pass; a `MUTATE=<m>` run exits 1 iff the control BITES (the named cell flips), 0 otherwise (a declared control failure, kept). Repo root from `ZF_REPO` or by walking up from `__file__`; every printed path uses `<repo>`; no absolute home path is printed. No existing file is edited; committed lanes (CFG44 `Bcommon`, CFG48 `Gcommon`, CFG70, CFG72, CFG232 `common`) are imported read-only.
- **The mass.** Every arm keeps the cold component as in candidate B; none supplies the cold mass; a pass in any arm would not remove the requirement for it.

### 4.1 The legality test for ownership (G0, route-level, run first for each route; cost about 1.5 h)

G0 is not one of G1-G5. It is mandatory because the lane's object is a LEGAL owned object. A legality FAIL is a binding FAIL for the route (stop).

**Bound-only (tests, each with a numeric line):**
- B1. The cosmological background (FRW, theta_b = 3H > 0): the ownership variable n (or the phantom / g_N ratio for B) stays <= 1e-6 for all t.
- B2. A positive-energy, outgoing baryon shell (unbound): n <= 1e-6; the exchange force on the baryons <= 1e-6 g_law and the fluid heat <= 1e-6 of the target store.
- B3. A bound shell after its own turnaround: n >= 0.99 within one free-fall time and it stays there.
- B4. Inertness: where n < 1e-6, every force and the heat exchange vanish to the same tolerance (the object is inert, not merely small).

**Causal (tests):**
- C1. The discrete closed-time-path (doubled-field) action on N = 200 and N = 400 time steps: the Euler-Lagrange residual R_k depends on the variables of steps j > k + 1 with a Jacobian <= 1e-12 (banded), on the physical shell (the difference fields set to zero), in the CFG48 G3 sense; CFG48's committed advanced dependence for a memory or latch inside an action (8.5e-4, 1.7e-2) is the failing reference.
- C2. Any spatial mediator: characteristic speed <= c (principal symbol), and the retarded Green function outside the cone <= 1e-12 (CFG72 got 2e-18 on the 1+1 half-line, and 0.25 for an elliptic stencil as the failing control).
- C3 (route B): the principal symbol of the foliated system is hyperbolic with all characteristic speeds <= c.

**Hierarchy (reported, never part of the legality verdict):** (i) an embedded, formed-in-place collapse inside a latched host gets n <= 1e-6 (CFG7's tidal dwarf, DR4 Arm C); (ii) an accreted, previously latched satellite keeps n >= 0.99; (iii) the Sun's own latch: the P2 monopole against Q2 <= 5.2e-27 s^-2 (replay of CFG185 / CFG251 (iii-b) 1258-1545 x for a local latch).

**What passes G0:** B1-B4 and C1-C2 (A), or B1-B4 and C3 (B). The frozen hand expectation is in section 4.4.

**What would count as a derived mechanism at G1 (the flag).** A G1 pass is graded: P-declared (the target, or the interaction function, is an input or is solved for by inversion), or P-derived. P-derived requires ALL of: (i) the target profile is not supplied: the enclosed-mass dependence arises from the dynamics (a Gauss-law mediator, or the foliated matching), and a0 enters only through rho_Lambda, c and G with kappa = 1/2; (ii) the selectivity control: the same equations with the target replaced by Verlinde's M_D shape (C_V/C_target = (1 + x)/x, CFG117) do NOT reproduce that shape (a class that reproduces any target handed to it is a restatement); (iii) the same constants at all four masses on both profiles to within 10%. If P-derived is reached, an INDEPENDENT re-derivation from separately written code, by a lane that has not read the route's scripts, is required BEFORE reporting; until then the cell is reported as "pass, independent re-derivation pending", never as closure. A P-declared pass triggers the orchestrator's re-derivation request under rule 5 only if G0, G3 (any arm) and G5 also pass, and is reported as a restatement.

**What counts as a no-go.** A scoped no-go on the frozen class: the first failing cell of the first failing gate of an arm, named, with its number, and with the statement that it covers only the frozen class and its listed hypotheses, not the route in general.

### 4.2 ROUTE A (L14a): a causal ownership latch with a vacuum-funded exchange

**Model class (field equations to be solved).** A reduced, spherical Lagrangian-shell model in the Newtonian weak-field limit (the CFG48 / CFG70 / CFG72 setting), a closed-time-path (doubled-field) action with fields q_+- (probe baryon shell, mass m), theta_+- (heat store of the fluid shell), n_+- (the ownership latch, one per fluid shell), I_+- (the retarded inhibitor mediator, Arm A3 only), and v_+- (a vacuum-energy deficit field, funded arms only). The physical (difference fields zero) equations:

1. (E1, from CFG70) m d2q/dt2 = -m dPhi_N/dq - dF/dq, F = r theta + (c_f/2)(theta - n theta^T(q))^2; r = 1 closed ledger (the heat is paid by the baryons, CFG48 G4's reciprocity), r = 0 funded by the reservoir.
2. (E2, from CFG70) r + c_f(theta - n theta^T(q)) + (Gamma * d theta/dt)(t) = 0, with the retarded kernel K = exp(-s/tau_bar)/tau_bar (declared family), integral K = 1.
3. (E3) tau_n dn/dt = s(-theta_b/3H(t)) (1 - n)(1 - iota) - [1 - s(-theta_b/3H(t))] n, where theta_b is the divergence of the baryon flow, H(t) the background Hubble rate, s the C^1 smoothstep on [0, 1] (declared shape), tau_n = 1/sqrt(G rho_b,loc) (a function of fields, not a constant), and iota in {0, 1} is the inhibition (Arms A1, A2: iota = 0, "any collapse"; Arm A3: iota = Theta(M_L(<r) - m_cand), M_L the enclosed latched baryon mass obtained from the retarded Gauss-law mediator of CFG72, c_m sqrt(1 + beta) = c).
4. (E4, funded arms) the heat paid to the fluid is drawn from a vacuum-energy deficit v(r, t) >= 0 on the half-line with a closed ledger, d/dt integral v dV = -(heat rate), propagating at speed c; the local a0 shift is delta a0/a0 = (1/2) v/(rho_Lambda c^2) (REPORTED, with the frozen line |delta a0/a0| <= 1% from the FLAT a0(z) law).
5. The targets theta^T(q) are CFG70's two forms (pressure-slaved (3/4) a0 and sigma-slaved (3/8) a0 (2 + x^2)/(1 + x^2)), carried and never pooled. They are SUPPLIED: Class A cannot pass G1 as P-derived (section 4.1), by construction.

**Arms (never pooled).**
- A1: iota = 0, r = 1, tau_bar in {0.01, 0.1, 1, 10} t_f (CFG70's grid). The REPRODUCTION CONTROL: late reaction/g_law 0.065 / 0.53 / 2.13 / 7.46 / 22.5 at x = 0.3 / 1 / 3 / 10 / 30 (pressure-slaved) and energy ratio 72.8 / 49.6 / 23.0 (CFG48 r_ta) and 318 / 179 / 57 (B's r_ta) at 1e9 / 1e10 / 1e12 Msun, within 1%. If it does not reproduce, stop and report (a failed control).
- A2 (pass-eligible, amended G3): iota = 0, r = 0 with the vacuum ledger, tau_bar = tau_L = 1/(kappa sqrt(G rho_Lambda)) (tied, no constant).
- A3 (pass-eligible, amended G3): as A2 with the inhibitor; the inhibitor's coupling beta = 1 is an untied constant, so by the frozen G4 rule A3 is a G4 FAIL and is reported to show whether the legality and hierarchy rows can be met at all.

**The amended G3 (a declared departure from the shared G3, fixed NOW, labelled in every output).** The shared G3's energy line (energy supplied <= the baryons' orbital energy) is scored in the STRICT reading for every arm; it is predicted to fail for any exchange that supplies the target's heat (CFG70, kernel-independent). The FUNDED reading is scored for A2 and A3 only: reaction <= 0.10 g_law over x in [0.3, 30] with the reservoir identified inside the action, energy <= the vacuum energy available in the causal region (c t_f ball), and |delta a0/a0| <= 1%. A funded-reading pass is reported as "a pass of the amended G3", never as a pass of the shared G3 and never pooled with the strict reading.

**Gate order (cheapest decisive first; each arm stops at its first binding FAIL).**
0. Controls (A1 reproduction; CFG72 light-cone width -> 0 control).
1. G0 legality (section 4.1), arms A2 and A3 (the new content; 1.5 h).
2. G4 ledger by inspection (0.3 h): A1 and A2 PASS iff tau_bar is the tied tau_L and no other constant appears; A3 FAIL (beta = 1).
3. G3 strict (closed forms, 0.5-1 h), arm A1: predicted FAIL; this is the STRICT arm's stop.
4. G3 funded (A2, A3): reaction, vacuum ledger, a0 shift.
5. G5: Q2 (the Sun's own latch; A2 replays CFG251 (iii-b); A3 uses the inhibitor), stability of the coupled latch-fluid-mediator operator (CFG72 found growing modes for a bath of time tau under its declared operator; the quadratic form is re-derived here and reported), no ghost, hyperbolic.
6. G1 (target on both profiles; P-declared at best), with the selectivity control.
7. G2 (linear growth to k = 30/Mpc with the latch inert in the cosmological background; the Boltzmann CMB half stays UNDEFINED).

**MUTATE controls (each flips a load-bearing cell; exit 1 iff it bites).**
- MA1: symmetrise the memory kernel in time (CFG70 M-a): the G0 causal cell flips PASS -> FAIL (advanced dependence > 1e-12).
- MA2: replace the latch source -theta_b by |theta_b| (sign-blind): the bound-only cells B1 and B2 flip PASS -> FAIL.
- MA3: drop the reaction partner (non-reciprocal): the G3 reaction cell flips to a trivial PASS and the reciprocity-symmetry check FAILS (CFG70 M-b).
- MA4: set tau_bar = 1 t_f (free) instead of tau_L: the G4 cell flips PASS -> FAIL.
- MA5: remove the vacuum ledger (r = 0 unfunded): the funded-G3 cell flips from PASS/FAIL to UNDEFINED (no reservoir).
- MA6: switch off the inhibitor (A3 -> A2): the hierarchy row (i) (an embedded collapse gets n <= 1e-6) flips PASS -> FAIL.
- MA7 (selectivity): replace the target by Verlinde's shape: if the class reproduces it, G1's P-derived cell flips to "restatement".

**Frozen hand expectations (kept if wrong).** A1 control reproduces CFG70 within 1%: 0.9. G0 legality PASS: 0.6 (the retarded structure is causal by construction; the bound-only rows B1-B4 are the risk because a smoothstep never gives exactly zero). G4 PASS for A2: 0.5. G3 strict FAIL: 0.99. G3 funded: reaction PASS 0.5 (CFG70 N6: 5 of 6 cells), ledger PASS 0.7, a0-shift line 0.4. G5 Q2: A2 FAIL 0.95; A3 PASS only if the inhibitor engages at the Sun: 0.3. G5 stability: 0.5 (CFG72's growing modes). G1: P-declared 0.5 conditional on the earlier gates, P-derived 0 by construction. G2: U or p* (inert in the background) 0.7.

### 4.3 ROUTE B (L13): BIMOND with a lapse-free, preferred-foliation interaction

**Model class (frozen at the level of CFG232's frozen class, with one change).** The base is CFG232's frozen class (`CFG232_FROZEN_CRITERIA.md`, commit b31f5e705; code imported read-only): Einstein-Hilbert terms for g and a twin metric g-hat, baryons coupled to g, the Milgrom interaction in the record's tuned five-invariant transcription (direction T4 - T1), sub-variants 13a (Lambda-hat = 0), 13b-ii (M_0 is the vacuum energy), 13c (conformal scalar, the reproduction control). NO twin matter is added (it would be a new species). The one change, 13d: the interaction is a function M_fol of the SPATIAL metrics (gamma_ij, gamma-hat_ij) and their invariants on a shared preferred foliation T(x) (lapse-free), so the diffeomorphism group is reduced to foliation-preserving ones and a khronon scalar mode appears (R10 and CFG172's khronon exclusions are then relevant and are reported). What is solved for what: the weak-field static spherical reduction (as CFG232 A1) for the point mass and the exponential sphere; the flat-space quadratic action of the relative sector (as A2) with the foliation; the nonlinear static MATCHING problem for g-hat around a collapsed g region (the R-static versus R-add question of CFG232 l.119); the FRW reduction (as A4).

**Constants ledger.** kappa = 1/2; a0 through the 13b-ii tie kappa^2 = -16 pi beta/(sigma_s M_0) (CFG232), reported with its status "native but inverted"; the interaction function is a one-parameter monomial family whose exponent is fixed by the action's scaling (M ~ Q^(3/2) at small argument, from memory, unverified: Milgrom 2009), NOT solved from the target; every other number is a departure.

**Arms (never pooled).** B-a: 13a with the foliated interaction; B-b: 13b-ii with it; B-c: 13c, the reproduction control (must reproduce CFG232's 13c row; a failed control stops the route). Cold fluid coupled to g (primary) and to g-hat (reported).

**Gate order.**
0. Controls (13c reproduction, EH calibration C2 of CFG232).
1. G5a ghost / hyperbolicity of the foliated quadratic action (cheapest decisive, 3 h): ghost-free, strongly hyperbolic, all speeds <= c on flat space AND on the exact static MOND background operator.
2. G4 ledger (0.3 h).
3. G0 legality (section 4.1) with C3: the matching problem decides R-static versus R-add; bound-only and hierarchy rows as in 4.1 (a nested configuration, a sub-system inside a host's g-hat region, must get internal/Newtonian = 1 within 5% on the EFE-free branch).
4. G3 energy (the canonical energy of the interaction and relative sectors, both r_ta conventions; CFG232's previous result 19-254 x with sign negative is the failing reference) and reaction.
5. G5b Q2 and gamma (the bare law's 6.3e3-1.6e4 x is the failing reference; it passes only if G0 shows the Sun owns nothing).
6. G1-law, G1-C (cold fluid in g) and the selectivity control; G7 and G6 reported.
7. G2 (FRW; CFG232 could not converge the symmetric-branch background, the same obstruction is expected).

**MUTATE controls.**
- MB1: restore CFG232's lapse-dependent five-invariant interaction: the G5a ghost cell flips PASS -> FAIL (reproduces WF2/L70).
- MB2: flip the overall interaction sign (CFG232's erratum): the kinetic-sign cell flips.
- MB3: give the two metrics independent foliations: the hyperbolicity cell (C3) flips (extra modes).
- MB4: replace the monomial by the function solved from the target (inversion, CFG232 M1-inv): the G1 selectivity cell flips to "restatement".
- MB5: couple the cold fluid to g-hat: G1-C flips (the sign reversal, g_tot/g_C - 1 down to -5.8).

**Frozen hand expectations (kept if wrong).** 13c reproduction control passes: 0.9. G5a ghost-free: 0.2. G4: native tie but a0 free: FAIL strict 0.8. G0 legality PASS: 0.15 (bound-only needs the matching to switch the phantom off in unbound regions). G3 energy FAIL: 0.9. Q2 FAIL unless G0 passes: 0.8. G1-law P-declared (inversion): 0.5; P-derived 0.02. G2 UNDEFINED: 0.8.

### 4.4 What is NOT decided by phase 2 (for both routes)

The Boltzmann-code CMB, nonlinear cosmology, non-spherical baryons, clusters, lensing slip beyond Psi = Phi, the real data, and the physical identity of the vacuum reservoir (route A tests a ledger and a causal supply, not what the vacuum is). A pass of any cell is a statement about the frozen class only.

## 5. Ranking

### 5.1 The table (all routes; scores computed with the factors of section 2.2 and C_full of section 2.3)

Columns: T = persistent theorem-grade failures, S = scoped, Tl / Sl = lifted ones, Bn = bonus count, P(all), C_full (agent-hours), Score = P(all)/C_full, P(cg) = P(cheapest gate pass), cheapest decisive gate, eligibility ((a) species, (b) modifier, (c) pre-dead, (d) class not fixed, (e) no ownership candidate, (f) not runnable).

| Route | T | S | Tl | Sl | Bn | P(all) | C_full | Score | P(cg) | Cheapest decisive gate | Eligible? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L18 door-8 epoch channel | 1 | 2 | 0 | 0 | 0 | 1.26e-3 | 13.8 | 9.13e-5 | 0.02 | G4 (count) | no (d) |
| L1 door-1 memory/nonlinear kernel | 1 | 2 | 0 | 0 | 0 | 1.26e-3 | 14.8 | 8.51e-5 | 0.02 | G5 (tail theorem) | no (e) |
| L7 door-7 self-interaction | 1 | 2 | 0 | 0 | 0 | 1.26e-3 | 14.8 | 8.51e-5 | 0.01 | G4 | no (a) |
| L6 door-4 superfluid completion | 1 | 2 | 0 | 0 | 0 | 1.26e-3 | 15.8 | 7.97e-5 | 0.10 | G5 | no (a) |
| H5 emergent time | 1 | 2 | 0 | 0 | 0 | 1.26e-3 | 15.8 | 7.97e-5 | 0.02 | G4 | no (d) |
| L8 door-8 non-LI / derivative Q | 1 | 1 | 1 | 0 | 0 | 1.05e-3 | 13.8 | 7.61e-5 | 0.01 | G3 (energy source) | no (d) |
| L12 door-11C remnants | 1 | 1 | 1 | 0 | 0 | 1.05e-3 | 14.8 | 7.09e-5 | 0.02 | G5 (tail) | no (e) |
| L5 door-10 rotational dust | 1 | 1 | 1 | 0 | 0 | 1.05e-3 | 15.8 | 6.65e-5 | 0.15 | G5 (ghost) | no (e) |
| **L14a SK latch + funded exchange** | 0 | 2 | 2 | 1 | 0 | 9.76e-4 | 14.8 | **6.59e-5** | 0.01 (strict G3) | G3 strict; new: G0 legality | **yes** |
| H6 fluid-borne ownership | 2 | 2 | 0 | 0 | 2 | 7.09e-4 | 15.8 | 4.49e-5 | 0.02 | G3 (MS1 leak) | no (d) |
| L2 door-3 dipolar completion | 2 | 1 | 0 | 0 | 0 | 5.25e-4 | 14.8 | 3.55e-5 | 0.02 | G2 (budget) | no (a) |
| H2 kinematic relaxation | 2 | 1 | 0 | 0 | 0 | 5.25e-4 | 15.8 | 3.32e-5 | 0.05 | G3 (energy source) | no (d) |
| H4 vacuum gradient flow | 2 | 1 | 0 | 0 | 0 | 5.25e-4 | 15.8 | 3.32e-5 | 0.03 | G1 (trigger side) | no (d) |
| **L13 BIMOND foliated** | 1 | 2 | 1 | 1 | 0 | 4.88e-4 | 14.8 | **3.30e-5** | 0.15 | G5a (ghost) | **yes** |
| L10 door-9 SK completion | 2 | 2 | 0 | 0 | 0 | 3.15e-4 | 14.8 | 2.13e-5 | 0.03 | G1 (magnitude) | no (e) |
| H3 potential-depth screening | PD | | | | | 2.19e-4 | 12.8 | 1.71e-5 | 0.01 | G1 (scale) | no (c) |
| H1 boundness ownership | PD | | | | | 2.19e-4 | 13.8 | 1.59e-5 | 0.02 | G1 (edge) | no (c) |
| L3 door-5 reached/stable | PD | | | | | 2.19e-4 | 14.8 | 1.48e-5 | 0.40 | G5 | no (c) |
| L4 door-6 3-D infall | PD | | | | | 2.19e-4 | 16.8 | 1.30e-5 | 0.03 | G1 (scale) | no (c) |
| L11 door-11 flux as a field | 3 | 1 | 0 | 0 | 0 | 1.31e-4 | 14.8 | 8.87e-6 | 0.02 | G1 (own gravity) | no (e) |
| L9 Hossenfelder action | not runnable offline: no estimate | | | | | | | | | | no (f) |
| M1, M2, M3 modifiers | not routes: no estimate | | | | | | | | | | no (b) |

PD = PRE-DEAD (three T factors).

By hand: L14a = 0.014 x 0.5 x 0.5 x 0.6 x 0.6 x 0.7746 = 9.76e-4; C_full = 3 + 11.8 = 14.8; score 6.59e-5. L13 = 0.014 x 0.25 x 0.6 x 0.6 x 0.5 x 0.7746 = 4.88e-4; C_full = 14.8; score 3.30e-5.

### 5.2 The ranking, by the frozen rule

Eligible routes: L14a (score 6.59e-5) and L13 (3.30e-5). The ratio is 2.00 (exactly, by the factor structure; the profiles differ in one T factor, 0.5 x 0.5 / (0.5 x 0.25)). By the rule of section 2.4 (within a factor 2, inclusive) phase 2 is frozen for BOTH and they are run separately and never pooled. Two lines: **eligible ranking: 1 L14a (6.6e-5), 2 L13 (3.3e-5), ratio 2.00; ineligible, by score: L18, L1, L7, L6, H5, L8, L12, L5 (all within 9.1e-5 to 6.7e-5, a spread of 1.4), then H6, L2, H2, H4, L10, then the PRE-DEAD routes and L11.** **Top route's cheapest decisive gate: L14a's G3 strict (a closed-form replay of CFG70, about 0.5-1 h, predicted FAIL at P = 0.01); the new content is G0 legality of the doubled-field latch and the funded reading of G3. L13's is G5a, the ghost / hyperbolicity of the foliated quadratic action (about 3 h, P = 0.15).**

### 5.3 Sensitivity, and why the ranking should be read as coarse

- Over ALL twenty scored routes the primary score separates the top block from the PRE-DEAD routes by a factor 5-7 (and from L11 by a factor 10), and spreads the top nine by a factor 1.4 (L18 9.1e-5 to L14a 6.6e-5). The ordering inside that block is not informative: the factors are hand estimates and a change of 10% in any of them reorders it. What selects L14a and L13 is the eligibility rules (d) and (e) (written after the paragraphs were drafted), not the score.
- Without (d) and (e) (the primary rule alone), the order is L18, L1 = L7, L6 = H5, L8, L12, L5, L14a (rank 9 of 20), H6, L2, ..., L13 (rank 14). With harsher factors (T 0.1, S 0.5): L14a rank 6, L13 rank 10, L14a/L13 ratio 3.16 (outside a factor 2). With milder factors (T 0.4, S 0.7): ratio 1.58, L14a rank 10, L13 rank 14. With a flat build cost B = 3 for every route: L1, L6, L7, L18 and H5 tie for first (8.5e-5), L14a ranks 9th, L13 14th. So the "both within a factor 2" outcome holds for the primary and mild factors and fails for the harsh ones; it is reported, not tuned.
- The honest reading of the whole triage: no route has P(all) above about 1.3e-3 and no cheapest-gate pass probability above 0.15 (L3's 0.40 is moot). Every untested premise lifts at most one counted failure, and the failure that remains is almost always one the record already measured (the exchange's energy, the tail theorem, the ghost, the budget). Phase 2 is therefore expected to end in named scoped no-gos; what it can add is the closing of two specific untested exits (the legality of a doubled-field latch, and the foliated bimetric interaction), not a pass.

## 6. What is NOT covered

- Every route's physics beyond its paragraph: no script was run; every estimate is a hand estimate; the factors 0.25 and 0.6, the base 0.014 and the cost units are conventions fixed here, not measurements.
- Routes not in the sources' lists and not reached by the cross-door reading: for example screened mediators beyond CFG72's one completion, a UV completion of any route, and quantum or loop-level effects.
- L9 (Hossenfelder's action as written): not runnable offline. The brief's "a1-bound" in H4 was read as the alpha_1 preferred-frame limit; that reading is mine.
- The three large closure_map files (GATES_STATUS, CLAIMS_AUDIT, SHARED_VS_SPECIFIC) and the ChainCert and CFG240 READMEs were read by head and keyword only; any "not tested" entry that lives only inside their bodies would have been missed.
- Non-spherical baryons (M1), nonlinear cosmology (M2), a Boltzmann-code CMB (M3), and the data side of candidate B (SLUGGS, KiDS, ultra-faints, DR4) are untouched; phase 2 does not test whether the data favour any model.
- Whether the twelve requirements are jointly satisfiable: CFG230 says neither sufficiency nor consistency is shown, and nothing here changes that.
- Literature facts (Mashhoon, Blanchet-Le Tiec, Chamseddine-Mukhanov, Deser-Woodard, Verlinde, Hossenfelder, Milgrom's BIMOND, AeST, Horava, Galley's closed-time-path action, Brown-Schutz dust) are from memory and unverified.
- kappa = 1/2 stays FITTED; the cold mass is still required; nothing here says the theory is closed.
