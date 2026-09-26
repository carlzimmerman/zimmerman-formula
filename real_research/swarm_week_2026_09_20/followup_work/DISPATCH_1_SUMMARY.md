# Follow-up work dispatch 1 (2026-09-25): R01, R02, R03, R06, R10 landed

Landed by the Hermes lane on 2026-09-25, against the followup work order
(baseline `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`; repo HEAD at run time
`29b5c74ff` / `52a294431` for concurrent lanes).  All results reproducible
from the scripts in this directory; exit codes 0 and per-check PASS/FAIL in
each lane's `.py`.

| Card | Verdict | The result |
|---|---|---|
| R01 | 7/7 PASS | The exact factorization (w−1)ρ = (2/3)(2−K)D u³ holds for every u (Lean N1, zero sorry). **L304 V4's "M_act ~ r^0.58 = sqrt(r)" is a pure-log window artifact**: a C/r³ shell integrated from the cutoff with zero interior mass fits r^0.578 on L304's exact window. The asymptote is rho_act ~ C/r³, M_act = M0 + 4πC ln(r/r0). M0(<1 Mpc) = 2.5×10⁴² kg. Remainder bound certified (N7). |
| R02 | 4/4 PASS | Shell-mass theorem M(r) = M(r0) + 4πC ln(r/r0) certified to 2×10⁻¹². The apparent exponent is cutoff-controlled: 0.578 (1 Mpc) → 1.175 (2 Mpc) → 1.345 (5 Mpc) → 1.820 (10 Mpc), outer sample fixed. **L311 V2's r^{1/8} outer-rise prediction is built on the misread sqrt law and must be re-derived on the log law.** |
| R03 | 4/4 PASS | Curvature invariant C_β = dβ/d ln r + 4β²: **= 0 identically for the log continuation, = β/2 for sqrt** (both machine- and algebra-checked; matching amplitude+slope does not erase the difference). Observability gate FAILS at galactic data quality: σ(C_β) ≈ 4.9×10³ × the separation at 12 points × 1% over Δln r = 1.1 — precision-gated, not ready (R18 note). |
| R06 | 3/3 PASS + Lean | m1√m2 = m2√m1 ⟺ m1 = m2 certified in Lean (PairObstruction.lean, zero sorry, axioms = standard three). PD20's per-body ansatz at (1, 4) gives opposing forces 2 and 4 — **unequal-mass momentum violation; PD20's √2 two-body factor is conditional algebra, not a derived amplitude for m1 ≠ m2**. Test-particle limit = the only consistent limit. |
| R10 | 4/4 PASS | The rational aux response, the PD21 quadrature g² = gN² + a0 gN, and L311's deep-active law are THREE inequivalent full laws: g/a0 at gN = a0 is 1.488 / 1.414 / 1.000; exact symbolic residual mu_aux − mu_quad ≠ 0; Newtonian-side corrections 1.7×10⁻⁴ vs 5.0×10⁻⁴ a0 at gN = 100 a0. Assign distinct model IDs; do not mix quarter-slope/normalization predictions across them. |

**Consequences for the record (proposed, not yet integrated):**
1. L304 V4's "sqrt(r)" reading is a window artifact — do not quote
   M_act ~ √r as an asymptotic law.
2. L311 V2's r^{1/8} rise shape should be re-derived from M = M0 + 4πC ln r
   (β → 0, not 1/8); the RAR-stability conclusion survives (log grows slower).
3. PD20/PD21: equal-mass √2 factor stays; unequal-mass amplitude not
   importable; R07 must derive the two-body force from the action.
4. R18: treat C_β as precision-gated.

Pending: R04–R05, R07–R09, R11–R20 remain open in the registry. R01–R03
chain is the audit that corrects L304/L311; the PR/patch to clock_2026
scripts is proposed in each RESULT.md.