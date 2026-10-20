# CFG899: alpha door D08, the charged vector boson in dS_4 with a covariant completion (closes S1)

**Result: CLOSED, NO SELECTION** (structural closure). With the Higgs/Goldstone completion of the charged W in the background-covariant R_xi gauge and a covariant (heat-kernel; Pauli-Villars or point-splitting) regulator, the dS_4 induced current is renormalisable, and its finite part exists. But the finite part depends on the W mass and on the gauge parameter. Nothing selects alpha. **Part D (gauge dependence): NOT ESTABLISHED as frozen, because check D-G4 failed on its g = 1 rows (a wrong pre-registered expectation); GAUGE DEPENDENT at O(1/mu^2) with the post-hoc Amendment A1.**

This was declared in advance as a **structural closure, not a value trial**: e stays a free symbol and no number is compared with 137.036. **N_mech stays 374.** Alpha stays an INPUT; kappa = 1/2 stays FITTED; the SM mass sector is walled (m is a free symbol, mu = m/H); kappa and the record's Z play no part. Not theory closed. Rules and door: `../CFG895_alpha_campaign_ledger/` (door D08). Pre-registration: `CFG899_PREREGISTRATION.md` (frozen e56c96770, Amendment A1 appended after the first run).

## The question (the record's S1 item)

S1 (61f3895cf) put one complex Proca field (unitary gauge, g = 2) in the dS_4 planar patch with the "constant" field F_{tau z} = E a^2 (lambda = eE/H^2). It found no finite renormalised current for the coupled {W_x, W_z} block. The log coefficient was mass dependent (c_inf + a/mu^2, with a = 5.12) and there was a mass-dependent quadratic term (c1/lambda = −(8/3 + 4/(3 mu^2))). Both are non-renormalisable H^2/m^2 divergences. S1's stated next step was a covariant regulator plus a Higgs/Goldstone completion. That is this lane.

## What was found

1. **The current is renormalisable.** Its only divergence is a charge renormalisation with the W running coefficient **b = 1 − 2g^2 = −7 at g = 2**, i.e. 21 times the complex scalar's 1/3. The split is −22/3 for the massless Yang-Mills part plus 1/3 for the Goldstone. This coefficient does not depend on xi (the direct general-xi computation gives −21 at xi = 1/2, 1, 2, 3) or on the mass. There is no Lambda^2 term, because tr E_V = −R carries no F. In S1's c_{-1}/lambda units the log coefficient is exactly 7. S1's exact-mode values, 6.837 (g = 2) and 1.032 (g = 1), sit 2.3% and 3.2% from 7 and 1. S1's mass-dependent pieces are unitary-gauge artefacts.
2. **Why S1 had no finite current.** The operator identity Delta_g(D theta) = D(Delta_0 theta) + (2 − g) Omega.D theta − (nabla^n Omega_nm) theta holds exactly (sympy, in dS). So the longitudinal modes decouple only if g = 2 **and** the background obeys the vacuum Maxwell equations. The dS "constant-E" field does not: nabla_n F^{nz} = −2EH/a ≠ 0. The defect is the same object as S1's constraint source (d_n F^{nm}) W_m.
3. **The two regulators agree up to a constant.** Pauli-Villars and point-splitting (Hadamard) differ by b ln(M^2/mu_PS^2) times the charge-renormalisation current nabla_n F^{nm}. That is a mu-independent constant in G_v, so after the on-shell charge condition they give the same G_v. The door's K = 2 collapses to one.
4. **The finite part in Feynman gauge (xi = 1), heavy mass:** sigma_HFY M^2 = (4g^2 − 4g − 5)/(24 pi^2). At g = 2 this is **1/(8 pi^2)**, so **G_v(mu) → 1/(2 pi mu^2) = 0.15915/mu^2** (scalar 7/(18 pi) = 0.12379, Dirac −1/(9 pi) = −0.03537). At xi = 1 the Goldstone and the two ghosts are exactly minus one AH4 scalar of mass m, at every mu. In Feynman gauge W_y decouples with S1's equation. The remaining {W_tau, W_x, W_z} block (three components, indefinite metric) was not solved, so G_v at mu of order 1 is not computed.
5. **The finite part depends on the gauge parameter (g = 2).** The exact formula **Gamma(xi) − Gamma(1) = Tr ln[1 − (1 − xi)(−box + xi m^2)^{-1} Dop^dag Delta_1^{-1} K]**, with K = −nabla^n Omega_nm, vanishes on vacuum-Maxwell backgrounds and is nonzero here. It agrees **identically** with a direct general-xi computation of the flat q^4 term:

   c4(xi) − c4(1) = (7 − xi)/4 − (7 xi + 2) ln xi/(6(xi − 1))   (units 1/(16 pi^2))

   In dS this gives **G_v mu^2 → 1/(2 pi) − r(xi)/(30 pi)**, with r(xi) = 5[3(xi − 7)(xi − 1) + 2(7 xi + 2) ln xi]/(2(xi − 1)):

| xi | 0.1 | 0.5 | 1 (Feynman) | 2 | 3 | 10 |
|---|---|---|---|---|---|---|
| G_v mu^2 (heavy limit, g = 2) | 0.342 | 0.272 | 0.159 | −0.031 | −0.193 | −1.057 |

   The sign changes between xi = 1 and xi = 2. So beyond its log coefficient, the W-loop current in this off-shell background is not a gauge-invariant observable. In the unitary limit r(xi) grows like (15/2) xi + 35 ln xi, so the heavy coefficient diverges there. These terms are the R_xi images of S1's quadratic and logarithmic unitary-gauge terms; that reading is qualitative only.
6. **No selection.** sigma/H = alpha G_v(mu, xi). Finiteness, regulator independence, on-shell gauge independence and g = 2 all hold for every e. e and E enter every operator only through e A, i.e. through lambda (the AH3 premise, check A7). A tie sigma/H = c therefore gives alpha = c mu^2/C(xi): a function of the mass and the gauge, not a number.

## Setup and equations (H = 1, planar patch a = −1/tau, signature −+++, MTW curvature)

* **Fields.** W (complex, charge e, gyromagnetic ratio g; the Pauli term is p = g − 1, and g = 2 is the Yang-Mills value), the charged Goldstone phi, and FP ghosts. The action is sqrt(−g)[−(1/2)|W_mn|^2 − m^2|W|^2 + p Wbar Omega W − |D phi − m W|^2 − (1/xi)|D.W − xi m phi|^2], with Omega = −ieF. The neutral fields do not couple to the background at one loop. A zeta R |H|^2 coupling only shifts m (Goldstone theorem).
* **Operators.** The W-phi mixing cancels for every xi (A3). At xi = 1 the W operator is Laplace type, Delta_1 = −box + Ric + m^2 − g Omega (A2), so E_V = −Ric + g Omega. The bundle curvature is Riem + Omega 1. The Goldstone and ghost operators are −box + xi m^2. One loop gives Gamma = Tr ln Delta_xi − Tr ln(−box + xi m^2), i.e. 4 + 1 − 2 = 3 degrees of freedom.
* **a_2.** The F^2 part is (1/360)(30 tr Omega Omega + 180 tr E^2). Ratios to a complex scalar: Delta_1 4 − 6g^2, Dirac 4, R_xi 3 − 6g^2.
* **a_3 (recalled, the coefficient set validated in S2).** An explicit trace code was used: matrices for E and the bundle curvature in the dS chart, covariant derivatives with the tangent-bundle connection, all 20 terms of the 1/360 group, and the F^2 part extracted with a scaling parameter (the linear part vanishes). It was followed by S2's `current_from_L`. Reduced to S2's structures, Delta_1(g) has coefficients (−32 + 30g^2, −8, −48 + 60g^2, 24 − 60g, 16, 10 − 15g^2). The per-structure dS currents are u = (1/360, −1/720, −1/360, 1/360, −1/240, −1/60)/pi^2.
* **Route D (flat Euclidean, general xi).** O(a abar) for the background a e^{iqx} + c.c., with the vector propagator delta/(k^2 + 1) − (1 − xi) k k/((k^2 + 1)(k^2 + xi)) and vertices from −D^2, (1 − 1/xi) D D. and −g Omega, minus one scalar of mass xi. The integrand is Taylor-expanded in q, angle-averaged in 4D, and integrated radially with an exact partial-fraction integrator. The q^4 term converges and is scheme independent.

## Checks (`cfg899_d08.out`, second execution; exit 0)

| Check | Result |
|---|---|
| A1 geometry, nabla Riem = 0, abs(nabla_n F^{nz}) = 2E (AH4 V3, S2 D0c) | PASS |
| A2 operator identity (generic W, g = 1, 2) | PASS |
| A3 W-phi mixing is a total derivative (symbolic xi) | PASS |
| A4 intertwining identity (generic theta, g = 1, 2); A4b on-shell defect vanishes at g = 2, dS defect −2iEe/tau | PASS, PASS |
| A5 Goldstone/ghost mode equation = AH4's (index 9/4 − lambda^2 − mu^2) | PASS |
| A6 W_y decouples in Feynman gauge, S1's equation (index 1/4 − lambda^2 − mu^2) | PASS |
| A7 e and E enter only through e A (AH3 premise) | PASS |
| B1 b = −7, split −22/3 + 1/3, Dirac 4 | PASS |
| B1b K-tests: AH4 V3 b_s = 1/3; Q1 4 b_s; S1 B3 −21/−7; S1 E4 c_inf within 5% | PASS |
| B2 no Lambda^2 (tr E_F = 0), a_2 has no m, dS a_2 ratio = flat | PASS |
| B3 PV − PS is m-independent (a charge renormalisation) | PASS |
| B4 proper-time factor: 3 polarisations, x^2 ratio −21, electric pair-rate weight 3 (S1 B4/B5) | PASS |
| C0 positive controls: scalar (7/18 − 2 xi_R)/(4 pi^2) with this lane's trace code; Dirac −1/(36 pi^2); **AH4 closed form → 7/(18 pi) (rel 5.2e-8, new)**; Q1 closed form → −1/(9 pi) (1.2e-11) | PASS |
| C1 trace code = hand reduction for g = 0, 1, 2; linear part 0; u_i = hand | PASS |
| C2 R_xi heavy coefficient 1/(8 pi^2), tau-independent | PASS |
| D-G1 Ward identity (longitudinal background: no q^2 log, no q^4) | PASS |
| D-G2 scalar control c4/cL = −1/10 | PASS |
| D-G3 Feynman-gauge q^4 ratio −37 (g = 2), −7 (g = 1) = the a_3 flat ratio | PASS |
| **D-G4 as frozen (both g)**: log ratio xi-independent | **FAIL** (g = 1 rows: −9/2, −3, 0, 3 = 3 xi − 6; g = 2 rows −21) |
| D-G4(A1), post hoc, graded g = 2 only | PASS |
| D-G5 route D = exact formula H4 at O(q^4), symbolic xi; H4 has no q^2 log | PASS |
| E1 classifier: spread 44.4 → NOT SELECTED; planted constant → SELECTED, planted 1/(2 pi mu^2) → NOT SELECTED | PASS |
| E2 no condition constrains e | PASS |

All 18 closure gates (A, B, C, E) pass, giving **CLOSED, NO SELECTION**. Part D: NOT ESTABLISHED as frozen; GAUGE DEPENDENT at O(1/mu^2) as frozen + A1. The run took 10.7 s on one core, with a peak of 118 MB.

**Controls (exit 1 each, as required).**
* `MUTATE_SPIN` (g 2 → 1): B1 (b = −1), A4b (on-shell defect ≠ 0), B4 (weight −1) and D-G5 (H4 holds only at g = 2) all FAIL. The L-checks equal the real run's g = 1 values: b −1, weight −1, sigma_HFY M^2 = −5/(24 pi^2), flat ratio −7.
* `MUTATE_DIM` (D 4 → 6 in the multiplicity count): B1 (ratio −19, b = −19/3) and B4 (weight 5) FAIL. The L-checks give D − 25 = −19 and D − 1 = 5.

## Disclosures

* **Wrong pre-registered expectations.** (1) D-G4 included g = 1. But g = 1 is not a gauge theory: A4's (2 − g) defect survives on-shell, so its "R_xi" family is not a family of gauges, and its log coefficient varies with xi (3 xi − 6). As frozen this is a FAIL, and Part D is NOT ESTABLISHED. Amendment A1, written post hoc, restricts D-G4 to the graded g. (2) H10's "r ~ ln xi as xi → infinity" was wrong; the actual behaviour is (15/2) xi + 35 ln xi. "r singular as xi → 0" holds (r ≈ −10 ln xi).
* **Runs.** The first execution (`cfg899_d08_FIRSTRUN.out` / `.json`) is kept unchanged; it gave the same numbers and verdicts. The second execution adds only the A1 check and fixes a reporting-only 0/0 at xi = 1. Development runs (scratch drivers, not committed) came before the first full run. They found one check-code bug: A5 called `coeff` on an unexpanded expression, which gave 0/0. They also showed that the symbolic radial integral via `together`/`apart` tripped the 900 MB watchdog, which aborted the run as designed; it was replaced by a partial-fraction integrator.
* **Finite q^2 parts are not graded (as frozen).** In the 4D symmetric-integration scheme, route D gives (xi − 1)(7 xi − 1)/(3 xi) and the H4 formula gives (xi − 1). They differ, which is what a non-gauge-invariant scheme does to finite parts left after log divergences cancel. In a consistent regularisation H4 makes this coefficient zero. The convergent q^4 parts agree exactly.
* **Recalled, not read here.** Vassilevich's a_3 coefficients: S2 recalled and validated the set on Dirac and scalar, and here it also passes C0, C1 and the flat gate D-G3. The curved-space cross term (linear in g) rests on the operator identity A2 and on its Dirac analogue in S2. Also recalled: the DeWitt-Schwinger and Hadamard facts (B3 checks the expansions numerically); the background-field-method literature on gauge-parameter dependence off-shell (named only; this lane's own result agrees with it); the Goldstone theorem in a constant-curvature background. Nothing was downloaded.
* **Not done.** The finite-mu current of the 3-component Feynman block (G_v at mu of order 1), O(1/mu^4), the non-linear response in lambda, the dS pair-production factor for the vector, backreaction, other charged species, and S1's g = 2 strong-field dynamical instability (this lane is linear response).
* **Compute and hygiene.** One core, `nice -n 10`, OMP_NUM_THREADS=1, bytecode disabled, watchdog at 900 MB. S2's and Q1's modules were imported read-only, and no file of another lane was written. A 1024^3 run was live; nothing heavier ran.
* This is the first result on D08 (stop rule, rules §6).

## Files

| File | Contents |
|---|---|
| `CFG899_PREREGISTRATION.md` | Frozen criteria (e56c96770), with Amendment A1 appended post hoc |
| `cfg899_d08.py` | Parts A–E, the MUTATE modes and the JSON output |
| `cfg899_d08.out`, `cfg899_d08.json` | Real run (second execution, with A1) |
| `cfg899_d08_FIRSTRUN.out`, `.json` | First execution, unchanged |
| `cfg899_d08_MUTATE_SPIN.out`, `.json` | Control g 2 → 1 (exit 1) |
| `cfg899_d08_MUTATE_DIM.out`, `.json` | Control D 4 → 6 (exit 1) |

Run commands: `OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 nice -n 10 python3 -B cfg899_d08.py` (real), then the same with `MUTATE_SPIN` (reads the real run's JSON) or `MUTATE_DIM`.
