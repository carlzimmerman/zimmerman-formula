# CFG230 -- what the missing object must be: requirements synthesis (phase 2 results)

Criteria frozen and committed before any script: `campaign_fresh_gravity/CFG230_FROZEN_CRITERIA.md` (commit b31f5e705, sha256 452829e6...110f3, identical to the file I wrote). Run as frozen; every departure is listed in section 9. kappa = 1/2 is FITTED. Nothing here says the theory is closed, and nothing here says any data favour or disfavour the framework. A scoped no-go is not a theorem; a referee reproduction is not a proof; a Lean certificate certifies its stated premises only. Every entry is a necessary condition read off failures of classes that were scored; none is shown sufficient, and the set is not shown jointly satisfiable or unsatisfiable.

**Re-run (about 6 s):** from the directory that holds these files, `ZF_REPO=<repo root> bash CFG230_run_all.sh` (inside the repository the root is found by walking up, so `bash CFG230_run_all.sh` suffices). It runs scripts A-H (each exits 0), then every MUTATE control and prints the frozen expected exit code next to the observed one (`CFG230_run_all.out`). No output prints an absolute home path (`<repo>` and `<scratch>` are substituted).

## 1. Bottom line

- **Twelve requirements survive, none stated above its evidence** (section 3). Three rest as whole statements on a THEOREM (R02 dimensional, R04 local-closure exclusion, R08 the pointwise-law dichotomy); five have a THEOREM core plus scoped or declared parts; four (R03, R05, R10, R11) have no THEOREM core. R10 is FRAGILE by the frozen definition (two rows, no theorem).
- **Hard-core set** (requirements no scored row meets as a mechanism): H = R03-R12 (10 of 12). Only R01 and R02 are met by any scored row as a mechanism (D02 for R01, D02 and D04 for R02), and D02's R01 is only the deep-limit exponent.
- **No known class meets all of these.** In the screening no class has M on every requirement of H. The ranking is coarse: after the post-freeze Amendment 2 the top six classes tie at S = 0 and are ordered alphabetically, which carries no information. The one class that led the frozen ranking (a Galileon or Vainshtein-screened scalar) led on a single memory-labelled cell, and its own record in this repository contains a scoped scaling no-go that I had not read at freezing; after Amendment 2 it is rank 5 (tied). The rule's "exactly one open class" branch is not triggered: four classes carry no F, only because their cells are undecided.
- **Three of my frozen hand expectations were wrong or imprecise** (minimum cover size, the energy-scaling exponent, a kernel-dependence claim) and are kept in section 8.

## 2. What was audited (script A) and what did not match

119 CITATION-AUDIT checks; 7 MISS, listed here. The sections-2.4 candidates first.

| Item | Finding | Verdict |
|---|---|---|
| Door 8 spread 32-353x (CFG131) vs 32-272x (CFG156) | CFG131's README labels 32-272x as the point mass (exact) and 32-353x as the h = 2 kpc exponential sphere. CFG156's frozen criteria declare the exponential-sphere range out of scope; its 32.17-271.71 is the point mass. | RECONCILED, not a disagreement. The LEDGER row and the frozen R04 line quote 32-353x without the geometry label. |
| GATES_STATUS row 5.12 "nu_mono departs by up to 2%" vs 1.46 | The row still carries the "up to 2%" wording; CFG44's README carries the appended correction (R(x = 1) = 1.46) and its body line 9 also still says "up to 2%". Script C recomputes R(x = 1) = 1.4565 from a transcription of the construction (CFG44 prints 1.4629; 0.4% apart, not bit-exact) and max\|R-1\| = 1.021 over x in [1e-3, 1e3] (CFG44 1.021). | DISAGREEMENT CONFIRMED: the row is stale as worded (CFG44's own correction says so). |
| Cap-excluded window (CLAIMS_AUDIT) | CLAIMS_AUDIT and the CFG43 README carry "convention-dependent, from about 11x up to 1e4-1e5 in mass". GAPS_1_2_JOINT_STATUS line 13 still says "about one decade in mass" (and the closure_map README carries the same phrase once). | Stale wording found in two closure_map files; the frozen R12(b) followed the corrected reading. Not re-derived. |
| Shared commits | b7d41c302 holds CFG122 (door 4) and CFG109; 9e4757627 holds CFG120, CFG123 and CFG124. The lane-prefix check passes for all 39 (lane, commit) pairs (each commit touches its lane's files). | CONFIRMED. |
| Anchors | 86 anchor strings in cited files; 3 absent on the first run (`CFG230_A_evidence_audit_firstrun.out`): 'Hees' (wrong file), 'c_s^2<0' and '\|xi\| < 0.0275' (formatting of the ledger row). Anchors were corrected to the sources' own strings; no source disagreed. | Audit-tool typos, kept in the first-run file. |
| Matrix vs the gate cells of TEN_DOORS_RESULT / DOOR11_RESULT | 4 flags, all hand-coding choices, none a transcription error: D01 G3 is "F (Bianchi); a,b p*" and I coded R06 p* because R06 is reaction and energy (the Bianchi failure is carried by no requirement cell; a mapping gap); D08 G3 is "p* (trivial; energy F beyond x=6.29)" and I coded R06 F for the explicit energy failure; D11Ca and D11Cb G4 are "F strict / P inert window" and I coded R12 U (two readings, the strict count is called overstated by CFG188). | Kept as coded; the four cells are the ones to re-read first. |
| Lean statements | All 20 statement names exist at HEAD and at b8d8b1ba5 (40 checks); the README at b8d8b1ba5 states 219 theorems, standard axioms only; nine premise statements (pointwise laws only, near-definitional, postulate, cap exceeded for r < r_M, and so on) match. | CONFIRMED. |
| Pending batch (Action, Dimension, FluidLink) | Committed since (a288aad86, 281 theorems, `verify_chain.out` PASS, standard axioms only). The frozen file's "pending" was true of the working tree when I read it; note the freeze commit b31f5e705 itself is a descendant of a288aad86, so at the freeze commit the batch was already committed. | AMENDMENT 1 (section 9). |

## 3. The requirements list (each with class and evidence grade; wording never stronger than the grade)

Grades: L Lean-certified (committed certificate, stated premises only); S+R symbolic in the lane and re-derived by a referee; S symbolic in the lane only; N+R numerical, independently reproduced; N lane only; D declared choice. Script H recounts these from the encoded sub-claims and checks each headline verb against them (12/12 pass).

| Req | Statement (necessary condition, inside the stated hypotheses) | Class and grade |
|---|---|---|
| R01 SCALE | Over 1e9-1e12 M_sun with the same constants, the radial scale goes as M^p with \|p - 1/2\| <= 0.0291 (outer) / 0.0145 (inner) at +-10%; a fixed-kernel linear response gives R proportional to M_b (LP reproduces the universal-kernel residual 31.6228) | THEOREM core (lemma S+R; window arithmetic S), SCOPED-NUMERICAL (per-door exponents N+R), DECLARED (band, "same constants" clause; control M6). Stated as moving with those declarations. |
| R02 ACCELERATION SCALE | In the monomial family with G4's constant inventory, the only length proportional to M^(1/2) is (GM/(cH_Lambda))^(1/2), and a Newtonian-only (G, M, H) mechanism has only the M^(1/3) length; so an acceleration scale built from (G, c, X) must enter. R02b (gradient-type trigger, not a potential) is separate | THEOREM (monomial statement grade L after Amendment 1, conditional on the monomial family and G4; Newtonian half S, this lane's derivation); R02b SCOPED N. Not claimed: that X itself must be an acceleration, or which variable is compared. |
| R03 SHAPE | The cumulative dark mass follows the declared kernel's profile (P2: M(sqrt(1+x^2)-1), inner column 106.88 M_sun/pc^2); a linear sum such as Verlinde's fails by (1+x)/x | DECLARED-CHOICE (kernel). The P2 point-mass identity is Lean-certified for P2 only. |
| R04 CLOSURE | No closure that is a function of local fields works (barotropic P(rho), far-shell theorem); the required c_s^2 at fixed density scales as M^e with e in [1/2, 1] (CFG44's closed form reproduced), spread >= 1e3 over 1e8-1e14 | THEOREM for the stated closure classes, grade S (CFG44 has no referee lane; point-mass Gamma(x) monotone is grade L); constraint-action row SCOPED N. |
| R05 COLD-EARLY | Cold at z >~ 10 to k = 30/Mpc and hot only after collapse: c_s^2 <= 4.608e-12 against halo sigma^2/c^2 of 1.96e-8 to 6.2e-7 (ratio 4.26e3 to 1.35e5, reproduced) | SCOPED-NUMERICAL (N+R for the bound), growth convention DECLARED. In the frozen fluid classes the mechanism fails. |
| R06 RECIPROCITY | A baryon-tracking exchange has reaction (3/4) a0 (P-slaved) or (3/8) a0 (2+x^2)/(1+x^2) (sigma-slaved), ratio to g_law 0.062 / 0.398 / 11.26 and 0.53 / 22.49 (reproduced from the closed forms); passing the 0.10 line needs a 225x smaller coefficient or an untied coupling or an unfunded reservoir | THEOREM for the CFG48-G4 exchange form (S+R; algebra L), SCOPED (memory kernel, light cone), DECLARED (r_ta convention, 0.10 line). Energy: see section 8 (my scaling claim was wrong). |
| R07 BOUND-ONLY SWITCH | Gauss lemma for a gated shift-symmetric field; no field function reproduces the ownership rule (Lean, conditional on the postulated rule and the input hierarchy); local gates unstable 44/48 while a nonlocal enclosed-mass gate is stable 48/48 (CLAIMS_AUDIT row 158) | THEOREM 07a (S+R; algebra L) and 07b (L, conditional); 07c SCOPED N+R; 07d DECLARED (r_ta convention). |
| R08 EFE BRANCH | A pointwise continuous law with MOND's square-root pull must show an external-field effect; no-EFE forces a linear law | THEOREM, grade L for pointwise laws only (PDE theories not formalised; referee CFG191 reproduces the sympy version). Which branch is candidate B's own choice (DECLARED). Zero door rows show an F. |
| R09 SOLAR TAIL | For a kernel with (yq)' >= 0 inside a +-10% band the isolated tail is >= 0.28205 a0 (P2; simple 0.46754, nu_mono 0.42405 by my transcription); Q2 at Saturn 6.28e3 (a0/2) and 3.54e3 (minimal), so a screening factor >= 3.5e3 or ownership | THEOREM inside the aether-channel class, conditional on the band and the premise (S+R, cross-checked here); ratios SCOPED N+R and kernel/g_ext dependent. |
| R10 PREFERRED FRAME | The coefficient setting the MOND force must not also set alpha_1, alpha_2 and the frame dependence: D11Cb G1 wants t <= 1.2e-6, G6/G7 want t >= 4e6 (gap 3.3e12 arithmetic; 3.0e12 as printed) | SCOPED-NUMERICAL (N), DECLARED (branch, dressing). FRAGILE: support two rows, no theorem. |
| R11 STABILITY | (yq)' >= 0, c_s^2 > 0, no ghost in the MOND-carrying and gating sector; violated in 8 door rows | SCOPED-NUMERICAL (N) tally; one THEOREM item inside the mimetic class (ghost for every 0 < g t < 2/3, S+R); the shared "negative stiffness" reading is not a theorem. |
| R12 MEDIUM, TIE, CONSTANTS | A w = -1 vacuum cannot flow (special-relativistic algebra, grade L; GR extension S, no referee); the tie enters a stress cap with the entry postulated; the cap P_cap = a0^2/(8 pi G) is exceeded by the target pressure for x < 1 (P/P_cap = 1/x^2, checked); no constant beyond kappa and Omega_c h^2 | THEOREM (a) L/S; SCOPED (numbers, DESI-dependent); DECLARED (tie, cap window 11x up to 1e4-1e5 convention-dependent). |

Encoded recount (script H, section 8 of the frozen file): whole-statement THEOREM 3 (R02, R04, R08; estimate 3); core plus parts 5 (R01, R06, R07, R09, R12; estimate 5); no core 4 (R03, R05, R10, R11; estimate 4); referee-reproduced cores 5 (estimate 4, MISS inside the range 3-5); Lean-certified cores 4 sub-claims in R07, R08, R12 (estimate 4), 5 in R02, R07, R08, R12 after Amendment 1 (R02's monomial statement).

## 4. The table of rows (schema of the frozen file 3.2; full records in section 3.6 of the frozen file, audited by script A)

| Row | Lane @ commit | Binding obstruction (property level) | Class / grade | Referee (status) | Referee did NOT test |
|---|---|---|---|---|---|
| D01 kernel | CFG120 @ 9e4757627 | fixed-length linear response: C ~ M_b^2 vs target M_b, R ~ M_b; residual 31.6228 | THEOREM S+R (LP reproduces 31.6228 here) | CFG151 db335c0e7 (R) | memory kernels, relativistic completion |
| D02 Verlinde | CFG117 @ bb504274c | linear sum: C_V/C_target = (1+x)/x exactly (reproduced) | DECLARED (kernel), grade S | none | covariant Lagrangian (door 12, in flight) |
| D03 dipolar | CFG121 @ 16fca9acd | medium budget vs growth 860x / 115x; no single polarisation law | SCOPED N (T1.2 N+R) | CFG157 0bbd62cd7 (Q) | T1.3, T1.4, Q1, G1c B2-B4, G2-G5, O1 |
| D04 superfluid | CFG122 @ b7d41c302 | amplitude ~ M^(1/2), spread 31.62; X<0 branch c_s^2<0 | THEOREM S+R (exponent), SCOPED N | CFG154 2f6845de3 (R) | nonlinear cosmology |
| D05 f(E,L) | CFG130 @ c1d719fbf | realisable but encodes the target | SCOPED N+R | CFG155 bdbcf3fe1 (R) | reachability, stability |
| D06 infall | CFG118 @ d0baef700 | scale follows turnaround M^(1/3): x_ta spread 3.165 (reproduced) | SCOPED N+R; explanation R02 (S) | CFG158 c868ad276 (Q) | non-spherical, mergers |
| D07 fuzzy DM | CFG119 @ 435cb43e9 | cored where target ~1/r; m >= 1.28e-20 eV | SCOPED N+R (growth bound MEMORY input) | CFG159 a1fb4a128 (R) | excited states, self-interaction |
| D08 vacuum | CFG131 @ aa0d95aef | forced EOS (32-272x point mass, 32-353x sphere); c_s^2 bound 4.26e3 | SCOPED N+R | CFG156 bb7bd135d (R) | non-Lorentz-invariant vacuum, formation history |
| D09 Deser-Woodard | CFG123 @ 9e4757627 | negative response, spread 1000, signature (2,2) | SCOPED N+R | CFG153 9ce8b61c5 (R) | nonlinear embedding, SK completion |
| D10 mimetic | CFG124 @ 9e4757627 | ghost for every 0 < g t < 2/3 | THEOREM S+R, rest SCOPED | CFG152 7cb9ba39e (R) | relativistic completion |
| D11A | CFG171 @ 1c91164e9 | only AQUAL restatement; conserved sink needs c_s^2<0 | SCOPED N | none | perturbations, growth |
| D11B | CFG173 @ e415659c7 | w=-1 cannot flow (SR algebra, L); Le Sage push | L (algebra) + SCOPED N | none | field treatment of a flux |
| D11Ca, b, c | CFG172 @ f1585212e | tail >= 0.282 a0 (theorem in class); G1 x G6/G7 gap 3e12; c_s^2<0 | THEOREM S+R (tail) + SCOPED | CFG188 058296d6f (R with conditionals) | R3-S (KM1 solve), alpha_1/alpha_2 re-derivation |
| D11Cd1, d2 | CFG172D @ 249fa4ec8 | d1 blind; d2 no zeta both selective and stable | SCOPED N | none (orchestrator re-run only) | criterion B, KM1, MW tide |
| S174/S176/S177/S179, P43-P72 | see frozen 3.6 | supporting rows and pre-door gap rows | see frozen 3.6 | CFG181 (R), CFG191 (Q), CFG48 ref (R), CFG101 (R), CFG94 (R) | see frozen 3.6 |

## 5. Incidence matrix results (script F)

- Hard-core set H = R03, R04, R05, R06, R07, R08, R09, R10, R11, R12 (|H| = 10, as expected).
- 16 of 17 rows have at least one F (D05 has none: every cell p* or N).
- **Exhaustive minimum cover** (2^12 subsets): size **2**, the single cover {R03, R06} (hand expectation 3-4: MISS, kept). Restricted to requirements with a THEOREM core the minimum is 3 (for example {R01, R04, R09}, {R01, R06, R09}, {R02, R06, R09}, {R04, R06, R09} and three more); excluding R03 it is 3. Reading: this is a statement about which labels explain the scored failures, not about which are necessary; a cover of two shows heavy overlap between R03 and R06 across rows, and R03 is a declared-kernel item.
- Support (rows with F): R01 11, R02 5, R03 10, R04 5, R05 11, R06 10, R07 4, **R08 0**, R09 10, **R10 2**, R11 8, R12 10. R08 has no F in any row: it rests on its theorem, not on door failures. No requirement is the only F of any row.
- FRAGILE (support <= 2, no theorem core): R10 only. The frozen stop condition (more than three UNSUPPORTED or FRAGILE) is not met.

## 6. Pairwise pincers (documentary; gaps as printed by the lanes)

| Pair | Statement | Gap |
|---|---|---|
| R05 x R04 | cold at z >~ 10 versus hot in halos | 4.3e3 to 1.3e5 (reproduced) |
| R05 x R04 (D03) | medium budget versus growth | 860x and 115x |
| R01/R03 x R10 (D11Cb) | G1 t <= 1.2e-6 versus G6/G7 t >= 4e6 | 3.3e12 (arithmetic) / 3.0e12 (branch) / 8.7e9 (mirrored) |
| R09 x R11 | (yq)' >= 0 forces the tail >= 0.282 a0 | 3.5e3 to 6.3e3 in Q2 |
| R03 x R09 | the P2 shape carries the a0/2 tail | 6.28e3 in Q2 |
| R07 x R06 | nonlocal gate stable but bilocal; exchange 23-318x orbital energy | 1.4 to 2.5 dex |
| R05 x R12(d) | Q != 0 makes a0 flow; flat only for \|xi\| < 0.0275 | (bound) |
| R12(b) x R04 | cap P_cap = a0^2/(8 pi G) versus target pressure | ratio 1/x^2 = 100 at x = 0.1, 1 at x = 1 (new, checked) |
| R01 x R06/R02 | formation-funded gets M^(1/3); r_M needs c through an acceleration scale | x_ta spread 3.165 over 1e9-1e12 (M^(-1/6), reproduced from the CFG158 table) |

## 7. Screening (script G; rule frozen before ranking; prioritisation only, not a scoring)

Labels are the frozen ones (from memory, unverified). In flight elsewhere and neither labelled nor ranked: CFG231 (door 12), CFG232 (door 13), CFG250, CFG251, CFG252.

Tier X (F[T], excluded by theorem for a class matching the requirement's hypotheses): C07 scale-dependent G, C14 Weyl/conformal gravity (and the control C15 Mashhoon).

Tier Y as frozen (S over H, then fewer F, more M, name): 1 C13 Galileon/Vainshtein (S = 1, one M cell, R09); 2 C10 disformal; 3 C04 Einstein-aether; 4 C03 khronon (all S = 0, no M, no F, alphabetical); 5 C02 AeST (S = 0, M on R05, F on R12); 6 C08 MOG; 7 C12 modified inertia (-1); 8 C09 Cuscuton (-1); 9 C05 TeVeS (-1); 10 C06 nonlocal MOND (-2); 11 C11 AQUAL/QUMOND (-2; M on R01, R02, R11; F on R07, R09, R12).

**Amendment 2** (post-freeze, allowed by the frozen note on C13): I ran the record's two Galileon scripts (`galileon_mond_scaling_nogo.py`, `galileon_scaling_theorem.py`; in-lane sympy, not refereed): no single dominant Galileon power gives the deep-MOND law (the mass exponent needs n = 2 and the radius exponent needs n = 3/2), the helicity-0 spherical scaling never gives r^-1, and the nonlinearity acts near the source (inward screening) where MOND needs it far away. C13 R03 U -> F[s]. C13 falls from rank 1 to rank 5; the top three become C10, C04, C03, all tied at S = 0.

Sensitivities (reported, not chosen among): doubling THEOREM-core weights leaves the order unchanged; using all twelve requirements changes the order of C08, C12, C11 only. The top three are the same set under all three weightings.

Rule item 5: **no known class meets all of these.** Four tier-Y classes have no F (C13 before Amendment 2, C10, C04, C03): because most of their cells are U or N, not because they were shown to meet anything. The "exactly one open class" branch is not triggered. Controls reproduce their door rows (C15 tier X; C16 Verlinde S = -2; C17 superfluid -6; C18 Deser-Woodard -5).

## 8. MUTATE controls and failed or wrong expectations (kept)

| # | Control | Result |
|---|---|---|
| M1 | drop D02 (and D04) | BITES (exit 1): H 10 -> 11 (D02), 10 (D04 alone: R02 stays through D02), 12 (both) |
| M2 | drop D06 (placebo) | does not bite (exit 0), as frozen: H and the requirement list unchanged; R01's support falls |
| M3 | R02a THEOREM -> DECLARED | BITES (exit 1): whole-THEOREM count 3 -> 2. Tier X did NOT change (C07, C14 keep an F[T] on R01): the frozen expectation held per cell, not per class (partly wrong, kept) |
| M4 | target kernel P2 -> simple | BITES in C (exit 1): required phantom mass moves by 0.99 between kernels; and in E: tail 0.282 -> 0.468 a0 (+66%), Q2 3.54e3 -> 5.87e3. The Verlinde ratio does NOT move (C_target is kernel-independent): my frozen expectation that it moves was WRONG |
| M5 | band +-10% -> +-20% | BITES in B (window 0.0291 -> 0.0587) and E (tail 0.282 -> 0.200) |
| M6 | drop "same constants at every mass" | BITES (exit 1): LP residual 31.62 -> 1.0000 (a per-mass kernel fits every mass), so R01 is conditional on that clause |
| M7 | fictitious "AQUAL relabelled" row | BITES (exit 1): without the target-as-input detector H shrinks to R05-R12; with it H is unchanged |
| M8 | flip AeST R05 M -> F | BITES (exit 1): rank changes; tier membership does not |
| M9 | cite the pending Lean batch as grade L | BITES (exit 1) when evaluated at the parent of a288aad86 (the pending state); see Amendment 1 for why the freeze commit is not that state |
| M9b | same citation at HEAD (added after the freeze) | does not bite (exit 0): the batch is committed, so the audit allows grade L for the monomial statement |

Wrong or imprecise frozen expectations, kept: (1) minimum cover size 3-4; found 2. (2) E11: energy demand "scales as x_e^2" with a coefficient about 0.05-0.10: the coefficient range holds (0.053, 0.065, 0.095) but is not constant (spread 1.80) and the lanes' exponent is -0.249 against -0.334 for x_e^2; the baryons' orbital energy is set by their own radius, so E_int/E_orb goes as x_e times a compactness, not x_e^2. No number-level reproduction of the 23-318x is claimed (conventions not recoverable from the READMEs). (3) The Verlinde ratio was expected to move under the kernel swap; it does not. (4) M3's tier-X expectation, per class. (5) Referee-reproduced THEOREM cores: recount 5 against 4. (6) "This lane's own derivation with no referee": the frozen phrase is not the same as "grade S"; by grade S the encoded count is 4 (R01, R02, R04, R12) against 2. (7) The frozen M9 premise (the batch pending) is not true at the freeze commit.

## 9. Departures, amendments and corrections after the freeze

- **Amendment 1.** The Lean batch is committed (a288aad86; 281 theorems). R02a is re-encoded as a Lean-certified monomial statement (grade L: no (G, M, c) length goes as M^(1/2); with one extra constant X iff an acceleration scale; the hbar length exists but is 1.5e-11 m at 1e10 M_sun) plus the Newtonian-only half (grade S, no Lean statement, checked by my sympy nullspace). The conditions and non-claims of the Lean module are kept: monomials only; X need not itself be an acceleration; nothing about which acceleration nature uses. Counts are reported in both encodings.
- **Amendment 2.** C13 R03 U -> F[s] (section 7).
- **Encoding correction before any H run.** The frozen 3.6/4.2 text gives R07a's algebra grade L (Gauss module); my first data file had only the S+R sub-claim. The L sub-claim was added; H had not run.
- **Anchor corrections after the A first run** (3 strings; first-run outputs kept).
- **M9 reference state** corrected to the parent of the peer's commit; M9b added (labelled).
- Scripts B, C, E use transcriptions where the lanes' code is the only definition: nu_mono (CFG44 construction, not imported, 0.4% from the printed R(1)) and the CFG188 definition of the tail bound (band on g at fixed g_N; s(y_g) non-decreasing). The tail bound is a CROSS-CHECK of CFG188, not a new derivation.
- Every check is labelled CITATION-AUDIT, CROSS-CHECK, NEW-DERIVATION or EXPECT in the outputs. New derivations: the fixed-kernel scaling exponent, the tolerance window, the LP universal-kernel residual, the Buckingham nullspaces, the exchange closed forms (P and sigma slaved), the barotropic exponent e(x), P/P_cap, the P2 free function check.

## 10. Not covered

Unscored classes beyond the memory labels; sufficiency and joint (in)consistency of the requirements; non-spherical baryons and relativistic completions; Boltzmann-level cosmology; the pointwise-law statements for field-equation (PDE) versions; door rows without a referee (D02, D11A, D11B, D11Cd) and R3-S of CFG172; the data-side rows of candidate B; the merger and Harvey lanes; the tie candidates beyond one-line status; CFG231, CFG232, CFG250, CFG251, CFG252 (in flight); all literature statements in section 7 (memory, for the data chat to check). The Bianchi failure of D01 (G3c) is carried by no requirement cell.

## 11. Files

`CFG230_FROZEN_CRITERIA.md` (in the repository at the freeze commit), `CFG230_README.md`, `CFG230_run_all.sh`, `CFG230_run_all.out`, `CFG230_common.py`, `CFG230_data.py`, `CFG230_kernels.py`, scripts `CFG230_A_evidence_audit.py`, `CFG230_B_scaling_lemma.py`, `CFG230_C_shape_kernel.py`, `CFG230_D_reaction_energy_cold.py`, `CFG230_E_tail_bound.py`, `CFG230_F_incidence_pincers.py`, `CFG230_G_screening.py`, `CFG230_H_claims_audit.py`, each with `.out` and `_results.json`; MUTATE outputs `CFG230_<script>_MUTATE_<k>.out` and `_results.json`; `CFG230_A_evidence_audit_firstrun.out` and its json (the first audit run, kept).

## In-place re-run (orchestrator)

`bash CFG230_run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`; about 6 s): all eight main runs (A-H) exit 0 and all twelve MUTATE runs match their frozen expected exit codes (`unexpected outcomes: 0`; M2 and M9b are the two controls that do not bite, as frozen). Every `.out` and `_results.json` is identical to the author's, although the repository had advanced by several commits in between. The frozen criteria are `../CFG230_FROZEN_CRITERIA.md` (b31f5e705). The 17-row matrix and all row records are hand transcription, audited by script A against the cited commits and documents; that audit checks lane and commit citations, not the physics of each row.
