# FRW block for the closure statement (SE3): what to cite, in one place

For the Field equations session (SE3 owner), from the FRW reconciliation. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
Full chain: CHAIN.md (commit 8d075bf20f). Write the equation once in SE3; cite this block, not AC7 Q1.

## The statement (scalar FRW, AC2q and the QX19 blend on Sigma > X)

- **Mixing:** the lapse/polarization mixing is (1 - z), with z = gamma phidot^2 / N^2, given that D is the intrinsic leaf
  divergence (AC2 ACTION.md).
- **Quadratic action:** the induced factor in the scalar quadratic action is f = (1 - z)^2. The legacy (1 - 2 gamma phidot^2)^2
  is a coefficient error. It is the exact factor only if D were the spacetime divergence (control action A5), which is not AC2q.
- **UV speed:** c^2 = z / (1 - z + z^2), equal to 1/H_rr of the auxiliary Hessian.
- **Health is independent of the coefficient:** for any f >= 0, 0 < c_g <= c_ph <= 1. So "healthy on FRW" stands. Only the
  coefficient identity and the numbers quoted from it change.
- **Coupling:** the P block couples to the lapse only (no zeta, no shift) on any P = 0 FRW background, dust included.
- **Static limit (AC8):** the exact full-measure P-equation offset is gamma v^2 grad phi/(1+phi)^2, half the stated value. The
  bound is 1.1e-10 (was 2.2e-10), and the transfer to v3s is unchanged.

## Verification

| Item | File | Result |
|---|---|---|
| ADM reduction, both divergence conventions (sympy) | FRW_RECONCILIATION_CHAIN/frw_adm_check.py / .out | leaf D gives (1-z)^2; spacetime D gives (1-2z)^2; P block free of zeta and shift |
| Static P equation (sympy) | static_p_equation.py / .out | offset gamma v^2 grad phi/(1+phi)^2 |
| Dispersion signs | dispersion_signs.py / .out | 0 < c_g <= c_ph <= 1 |
| Lean, 11 theorems, standard axioms only | fable_independent_2026/lean_2026/FRW_correction.lean / .out | p_block_bound, p_block_attained, uv_denominator, legacy_discrepancy, legacy_ne_corrected_stress, legacy_eq_iff, aux_hessian, aux_uv_speed, phase_speed_bounds, group_le_phase, group_pos |
| Lean MUTATE twin | FRW_correction_MUTATE.lean / .out | 3/3 planted false claims fail |
| AC23 rerun, corrected insertion | reruns/ac23_main_corrected*, ac23_regrade_GRADE.json | PASS (HARMLESS, scoped) reproduced: max R 2.70011 vs 2.70014; control bit-exact |
| AC13 stress row, 0.81 for 0.64 | reruns/ac13_stress* | R 1.00-2.5257, det K >= 0.0251, label unchanged |
| Hashes | SHA256SUMS | 66 lines |

The Lean file covers the algebraic leaves only. The calculus steps (first variation, ADM reduction, Fourier averaging) are the
sympy scripts.

## Errata already filed (fix-forward, original rows kept)

- 0cbca2a4f2: closure_2026_11_05/CLOSURE.md (AC7 Q1 row); closure_2026_11_06/EQUATIONS_IN_ORDER.md rows 3.4 and 5.2, plus the end
  erratum; QX19 scorecard CONDITIONAL; CLOSURE_FINAL.md.
- c465b63f4b: AC8 2.2e-10 rows (the CLOSURE.md static-limit row, EQUATIONS row 8.5) marked 1.1e-10; the erratum cites 8d075bf20f.

## Still open (keep visible in SE3)

- The AC7 Q2 / AC10-AC15 post-Newtonian chain still carries the literal legacy factor and needs a full rederivation. It is
  not rerun.
- J3: the TC03 finite-time gradient catastrophe transfers to the QX19 action if its bootstrap box sits inside Sigma > X (the TC1
  session is deciding this).
- PAPER68 (deposited) is unaffected: it cites AC2 only.
