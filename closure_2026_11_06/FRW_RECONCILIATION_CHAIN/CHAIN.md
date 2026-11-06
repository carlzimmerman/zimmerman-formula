# One chain, kept by action: FRW reconciliation and closure ledger (2026-11-06)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing; the owner adopts. This note reconciles the
native-closure packet (`../../theory_closure_2026_11_06/`, read-only here) with the AC/QX record. Every
claim below names its action, background, hypotheses and evidence. Closure is claimed only where the
proof and its check exist. Historical files are not edited; corrections are new evidence in this folder.

Status words: **PROVED** (analytic proof with independent audit on record), **LEAN** (compiled, standard
axioms), **SYMPY** (exact symbolic check run here or pinned), **NUM** (numerical run), **CONDITIONAL**
(valid if a named hypothesis holds), **OPEN**, **FAIL** (preserved failure).

## 0. The actions (do not mix their gates)

| Id | Action | Where defined | Relation |
|---|---|---|---|
| A0 | AC2: canonical clock scalar + P.A - W - (gamma/2)(D.P)^2, unswitched | `action_search_2026_11_05/AC2_single_clock/ACTION.md` | **D is the intrinsic leaf divergence** (stated there) |
| A1 | Native AC2q: A0 with stiffness -(gamma/2) sqrt(-g){[max(D.P+2X,0)]^2 - (2X)^2} | `AC7_charge_switch/FROZEN_CRITERIA.md` ("all else as AC2") | On branch: A0 plus -2 gamma X D.P |
| A1f | First-order auxiliary form of A1 on its on-branch, D=(Ar-1-gamma r^2)/gamma | `theory_closure_2026_11_06/einstein_transfer/auxiliary/DERIVATION.md` | Same equations for regular on-branch solutions; singular weak equivalence NOT claimed |
| A2 | QX19: A1 with AC21 Pi^6 blend, b = X | `closure_2026_11_06/QX19_one_action_scorecard/README.md` | Identical to A1 pointwise on the open set Sigma = D.P + 2X > X (Lean `frw_exact`, `frw_point`, `frw_pert`) |
| A3 | v3s (adopted, scoped) | PAPER68, DOI 10.5281/zenodo.23990944 | Separate action; no gate transfers either way |
| A4 | TC06 vector completion: independent unit timelike U, dynamical P, U.P = 0 | `theory_closure_2026_11_06/vector_completion/CANDIDATE_ACTION.md` | Separate action; no native or QX19 result transfers |
| A5 | CONTROL ONLY: A1 with D replaced by the spacetime divergence nabla.P = D_leaf.P + P.A | this folder | Not proposed. Used to locate where the legacy factor comes from |

## 1. FRW correction: independent verdict

**Claim (A1 and A2, scalar-only FRW, unitary gauge, P = 0 background, D = 0, quadratic order).**
The lapse/polarization mixing is (1 - z) with z = gamma phidot^2 / Nbar^2. Eliminating P gives
(1 - z)^2 times AC2's induced term. The legacy (1 - 2z)^2 is wrong for A1 as defined.

Derivation, short form. With B = sqrt(h) P^x and A_x = d_x ln N:
N sqrt(h)[P.A - 2 gamma X D] = B N_x - gamma v^2 B_x / N. Integrate by parts:
B N_x (1 - gamma v^2/N^2). At N = 1 this is 1 - z.
The legacy code differentiated X alone. The density needs delta(N X) = delta X + Xbar delta N.

Evidence, all independent of the legacy AC7 code:

| # | Route | Result | Status |
|---|---|---|---|
| E1 | `theory_closure_2026_11_06/einstein_transfer/frw_independent/` (other agent; hashes re-checked here and match its IMPACT table) | (1-z)^2; UV c^2 = z/(1-z+z^2) | SYMPY (pinned) |
| E2 | `frw_adm_check.py` (this folder): general ADM Christoffels, K_ij with shift, full N sqrt(h), Fourier average, shift/lapse constraints, time integration by parts | f = (1-z)^2; gradient -eps q^2; UV c^2 = z/(z^2-z+1); P block couples to the lapse only | SYMPY |
| E3 | Same script, control action A5 | f = (1-2z)^2; UV c^2 = z/(4z^2-3z+1) | SYMPY |
| E4 | Fixed-A native auxiliary Hessian at D = 0 | H_rr = 1+(1-gamma r^2)^2/(gamma r^2); 1/H_rr = z/(z+(1-z)^2) | LEAN `aux_hessian`, `aux_uv_speed` |
| E5 | `ac2q_postfold_2026_11_06/NATIVE_DYNAMICS.md` on-branch flat block at d = 0 | C = (1-gamma s^2)/s, UV coefficient gamma s^2/[gamma s^2+(1-gamma s^2)^2] | earlier record, agrees |
| E6 | AC17 full-measure static kinetic coupling 1+gamma divP-2gamma X | 1 - z at divP = 0, N = 1 | earlier record, agrees |

Five routes agree: two ADM reductions with gravity, the auxiliary Hessian, the flat block and AC17.

**Classification: coefficient error.** It is not a convention choice. AC2 fixes D as the intrinsic
divergence, and AC7 inherits that. E3 shows (1-2z)^2 is the exact factor of a different action (A5).
The legacy number belongs to A5 or to the unweighted density, not to A1.

**What survives (LEAN).** For any mixing factor f >= 0 and eps > 0, l >= 0, the frozen dispersion
w^2/H^2 = E x^2 (1+l x^2)/(E(1+l x^2)+f x^2) has 0 < c_phase^2 <= 1 and 0 < c_group <= c_phase.
Theorems: `phase_speed_bounds`, `group_le_phase`, `group_pos`. So AC7 Q1's **signs** hold for the
legacy and the corrected factor, at every z. What fails is the exact coefficient identity and every
number computed from it. The two squares differ by z(3z-2) (`legacy_discrepancy`). They agree only at
z = 0 and z = 2/3 (`legacy_eq_iff`). At z = 0.1 they are 0.64 vs 0.81 (`legacy_ne_corrected_stress`).

**Generalisation used below.** The P block contains only p and the lapse. Its p-terms are free of
zeta, zetadot and the shift (assert in E2). The same holds for any FRW background with P = 0 whose other
sectors couple only to the metric, dust included. So A1's quadratic operator is AC2's with the
induced lapse term multiplied by (1-z)^2. AC5's rolling operator multiplies cY by `pol_on`. That is the
right insertion point; only the number was wrong.

**Physical background relation.** On the scalar-only background, z = eps * ell^2, with ell^2 = H^2 Lstar^2 / 2.
Independent (eps, ell, z) scans are formal coefficient scans. Positivity on the formal set covers the
physical subset (the theorems above hold for all f >= 0).

## 2. Every affected dependency (repo-wide grep for the factor and its uses)

| Item | Literal dependency | Disposition | Evidence here |
|---|---|---|---|
| AC7 Q1 | `Q1_factor` (1-2gamma s^2)^2; README "FRW exact" | **Coefficient identity FAILS**. Signs re-established for all z, as new evidence. Stored fixture numbers stay as the record of the density actually coded | E2, LEAN sign theorems |
| AC7 frozen prediction | "(1 + 2 gamma s^2)^2" | Also wrong (sign and size); historical | E2 |
| AC7 Q2, AC10 S1 | Unweighted PN density | Internal checks valid for that density. Covariant order-z mapping OPEN. Frozen labels kept | not rerun |
| AC7 Q3 | 2 gamma D.P sizes | No dependency | n/a |
| AC7 Q4 | -2 gamma X D.P static shift | Not this factor. The full-measure static coefficient is smaller (AC8 row), so the bound is conservative | `static_p_equation.py` |
| AC8 | P eq offset 2 gamma s^2 grad phi/(1+phi)^3; Poisson s^2(1-2gamma divP)/(1+phi)^3 | Full measure: P offset is **gamma v^2 grad phi/(1+phi)^2**, half the stated size. The Poisson factor (1-2gamma D) is confirmed; the power of N differs. TRANSFERS stands a fortiori; bound 2.2e-10 becomes 1.1e-10 | SYMPY `static_p_equation.py` |
| AC11, AC12, AC15 | (1-2gamma s^2) in continuity/Poisson (AC7 PN) | Covariant identification OPEN. Frozen NO VERDICT labels unchanged. At physical z ~ 1e-17 the factor equals 1 to 1e-16 | not rerun |
| AC13 | `POL main` (1-2*4e-17)^2 = 0.9999999999999998; stress 0.64 | Corrected main is 1.0 in double. Stress rerun at 0.81: see section 3. NO VERDICT (no power on eps_phi = 2) does not depend on pol_on | NUM `reruns/ac13_stress*` |
| AC23 | imports AC13 POL | **Rerun with the corrected main pol_on: PASS (HARMLESS, scoped) reproduced** by AC23's own frozen grade.py | NUM `reruns/ac23_*` |
| AC19 | "2 gamma s^2 <= 2.2e-10 (AC8)" | Exact gamma s^2 <= 1.1e-10. FN6 FAIL label does not depend on it | AC8 row |
| AC20 iter_2/iter_3, AC21 criteria/README | Literal (1-2gamma s^2)^2 "AC7's exactly" | Literal factor wrong. Structural equality with A1 near FRW valid; Lean `frw_exact` is constitutive and untouched. Equality is now with the **corrected** A1 | E2 + `frw_exact` |
| QX19 C4 | "AC7 Q1 carries unchanged" | Algebraic CARRY valid (A2 = A1 near FRW). FRW health **PASS stands on new evidence**: corrected reduction + sign theorems. Evidence column must cite those, not Q1 | E2, LEAN |
| QX19 C7 | AC23 PASS carries | Holds: AC23 reproduced with the corrected coefficient | NUM |
| `closure_2026_11_05/CLOSURE.md` l.79; `closure_2026_11_06/EQUATIONS_IN_ORDER.md` rows 3.4, 5.2 | Display (1-2gamma phidot^2)^2 and AC8's 2 gamma s^2 | Need a dated erratum line (not written here; historical files untouched) | this note |
| AC9 tensor/slip | builds N sqrt(h) T_on/T_off itself | No Q1 dependency; neither revoked nor newly passed | read only |
| TC03 formation (A1f) | Derived from the full auxiliary action | Consistent with E1-E4; no legacy import | E4 |
| PAPER68 (deposited) | Cites AC2 only (factor 1) | **Unaffected**; no deposited DOI carries the wrong factor | grep |

## 3. Corrected-coefficient reruns (post-hoc evidence, not frozen regrades)

AC23 main rows: 32 runs (16 witnesses x 2 rtol). pol_on goes from 0.9999999999999998 to 1.0.
`reruns/ac23_main_corrected.py`. Control: the same rows rerun with the legacy value reproduce the stored
outputs exactly (max relative difference 0.0, `ac23_main_control_summary.json`). So the run is
deterministic and the differences below are real sensitivity.

| Quantity | Stored | Corrected |
|---|---|---|
| label | PASS (HARMLESS, scoped) | PASS (HARMLESS, scoped) |
| max R_main at N_obs | 2.700138 | 2.700110 |
| min det K/a^6 at N_obs | 0.05001912 | 0.05001912 |
| powered / converged / Omega | 16 / yes / yes | 16 / yes / yes |
| det K discriminator bites | 16 | 16 |

The largest per-snapshot change is 0.15 relative, in a subsampled intermediate `detK_over_a6_min`; final
values agree to 4 digits. A one-ulp coefficient change moves R by about 1e-5. That is inside the
run's own rtol convergence band (2.0e-4). Re-grade: `reruns/ac23_regrade.py` (reproducible, byte-identical
GRADE). Scope is unchanged: AC5's constant-pol_on operator, frozen-root fixtures, not sourced, not
nonlinear, time dependence of z neglected.

AC13 stress rows (z = 0.1, pol_on 0.81 instead of 0.64). 16 runs: 8 witnesses x 2 rtol, all completed
(`reruns/ac13_stress_corrected.py`, `ac13_stress_compare.json`). R at N_obs, over AC13's stored gr rows:
1.000 to 2.5257, against the stored 1.000 to 2.5253. The largest single shift is 1.664 to 1.677 (eps_phi = 2,
k = 10). Min det K/a^6 is 0.0251 (stored 0.0251), positive on every row. The reported stress reading
"R stays at 1.0-2.53" is unchanged. AC13's NO VERDICT (no power on eps_phi = 2) is unchanged.
AC13 main and plant rows were not rerun, because AC23 already measures the one-ulp main change.

## 4. The chain, by action

### 4.1 A1 / A1f, native: plane Einstein-native sector, constant V0, on-branch half-range

| Step | Equation / implication | Hypotheses | Evidence | Status |
|---|---|---|---|---|
| N0 | Action, dictionary K = 1/(2M), gamma = K Lstar^2/2 | xi, kappa inputs | auxiliary/DERIVATION.md | definition |
| N1 | First-order reduction, full metric variation, Hilbert stress | on-branch, q = D + r^2 > 0, delta = 1-2gamma D > 0 | geometry/DERIVATION.md + reviews | PROVED; Lean leaves only |
| N2 | Fixed-A H_rr, corner/sign certificates | half-range domain | lean/, formal_followup/ (89 scoped results at TC06) | LEAN (not recompiled here) |
| N3 | FRW/P response: (1-z)^2, UV z/(1-z+z^2) | scalar-only FRW, P = 0 | section 1 (E1-E4) | SYMPY + LEAN leaves |
| N4 | Einstein initial data, local H2/H1 evolution, constraint propagation | periodic plane, compact admissible box | initial_data/, evolution/PROOF.md | PROVED (analytic, audited) |
| N5 | Classical clock-gradient catastrophe T_k <= C_eps/k; bounded curvature | constructed family, small eps | evolution/FORMATION.md | PROVED. The file's header still says "proposed until independent audit". Two later reviews (`initial_data/REVIEW_FORMATION.md`, `geometry/REVIEW_EVOLUTION_FORMATION.md`) give "proved as written" at pinned revisions. Not re-audited here |
| N6 | Terminal BV state, spacelike graph, regular constraints | same | postbreak_trace/PROOF.md, GEOMETRIC_TRACE.md | PROVED |
| N7 | Stress balance iff D^j v = 0 (no clock-gradient jump) | weak class of WEAK_CLASS.md, half-range | NATIVE_WEAK_BOUNDARY.md | PROVED |
| N8 | Unique physical postbreak continuation | n/a | n/a | **OPEN** |
| N9 | Clock regulator family has an immediate physical-curvature tail | that reference family only | khronon_regulator/ | FAIL (preserved, scoped) |

### 4.2 A2, QX19 action: the empirical scorecard

The QX19 scorecard stands as recorded, with one evidence repair (C4, section 2). It **passes** SPARC/RAR
(both footings), PPN/Cassini, GW speed/tensor mass, galaxy lensing = dynamics, PN sign (scoped),
well-posedness across the switch (local), FRW health (now on corrected evidence), galaxy linear
health, slow roots (scoped; rerun here) and the static limit. It **fails**: FG1 Upsilon tilt (canonical
+0.170 vs 0.15), X-ray ellipticals (G7 line), clusters/groups (no-go over static terms and every
extension tried), CMB lensing / linear growth (cold window killed), AGC 114905, Malin 1, FN6 window
source. Nonlinear fold, moving Sun and constraint causality were RUNNING/NO VERDICT in that README.
kappa FITTED.

**Joins between A1 and A2:**

| Join | Statement | Status |
|---|---|---|
| J1 | A2 and A1 have identical field equations wherever the state stays in the open set Sigma > X | PROVED (pointwise equality of densities on an open set; Lean `frw_exact`, `frw_point`, `frw_pert`) |
| J2 | FRW scalar quadratic action of A2 = corrected A1 result | PROVED via J1 + section 1 |
| J3 | N4-N5 (finite-time classical gradient catastrophe with bounded curvature) hold for A2 | **CONDITIONAL**: the formation data start at D = O(eps), Sigma/X = 2 + O(eps). The bootstrap keeps the state in "a fixed enlarged compact box". J3 holds if that box can be chosen inside Sigma > X. The proof appears to allow it, but no audit has checked this. If J3 holds, QX19's local well-posedness PASS coexists with finite-time breakdown. There is no contradiction, but "well-posed" must not be read as global |
| J4 | N7 for A2 | CONDITIONAL on J3's region condition for the whole weak class |

### 4.3 A4, TC06 candidate: separate column

Reviewed scoped results, per `CLAUDE_HANDOFF.md` section 3, not re-checked here: nine positive
polarizations, the de Sitter reference 3 M_cos H^2 = V0, the recoil mode, the qualified cold window and
flat finite propagation. The **V0 = 0 fixture relaxes a0^2 = xi G V0**, so it is not a positive-V0 pass.
TC07 is a draft: five Lean statements are UNCOMPILED and excluded. The coupling choice is designed,
not derived. **No gate from A1, A2 or A3 transfers to A4.**

## 5. Ledger

**Closed, with exact scope:** AC13 stress reading unchanged at 0.81 (reported only). the A1/A2 FRW scalar-quadratic coefficient (1-z)^2 and its health signs,
at the sign level, for all z and f >= 0. The A1 native plane-sector results N1-N7 (per the existing
audits). J1 and J2. AC23 PASS (HARMLESS, scoped) on the corrected coefficient.

**Failed, preserved:** the legacy AC7 Q1 coefficient identity. QX19's seven FAIL rows. The clock
regulator family's curvature tail. TC06 `plane/check001` (a valid failed run). Every frozen NO VERDICT label.

**Open:** N8 native continuation and selection. J3/J4 region condition. Covariant (full-measure)
rederivation of the AC7 Q2/AC10/11/12/15 PN chain. Clusters, CMB/growth and the hot-system gates for A2.
A4's coupled positive-V0 Cauchy problem, cosmology, abundance, perturbations, envelope coupling and all
same-action empirical gates. Errata lines in CLOSURE.md and EQUATIONS_IN_ORDER.md. kappa/xi (FITTED).

**Nothing here earns an all-gates label for any action.**

## 6. Files

- `frw_adm_check.py` / `.out`: E2 and E3 (both divergence conventions).
- `static_p_equation.py` / `.out`: AC8 full-measure P and lapse variations.
- `dispersion_signs.py` / `.out`: sign identities for general f.
- `../../fable_independent_2026/lean_2026/FRW_correction.lean` / `.out`: 11 theorems, standard axioms, 0 errors.
  MUTATE twin `FRW_correction_MUTATE.lean` / `.out` fails on exactly its 3 planted claims.
- `reruns/`: AC23 corrected main rows, legacy-value control, re-grade; AC13 stress rows.
- `SHA256SUMS`.

Not done here: re-auditing the TC PDE/BV proofs, recompiling the 89 TC Lean results, checking A4's
results, running `verify_tc06.py` (it rewrites a mutable file in the other agent's tree). The TC06
checkpoint SHA256 9e4e04c4...0f7b was re-checked and matches.
