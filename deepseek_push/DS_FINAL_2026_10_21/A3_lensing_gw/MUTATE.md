# A3 MUTATE — do the checks have teeth?

`a3_checks.py --mutate NAME` injects one defect at a time. A defect that leaves the
suite green would mean the corresponding check is vacuous. All five mutate the
**action or the derived quadratic coefficient**, not the check logic.

Baseline: `python3 a3_checks.py` → `A3 COMPLETE: 15/15 checks PASS.` (exit 0, 2.3 s).

| mutation | defect injected | check that must break | measured |
|---|---|---|---|
| `r3_sign` | sign of `R3` flipped in the Lagrangian only | `K0_lapse_eq_is_hamiltonian_constraint` | FAIL, residual `(21F′²f¹⁷ − 24F′f¹⁸ − 28f″f¹⁸)/(12 f^{37/2})` |
| `k_factor` | Einstein–Hilbert coupling doubled inside the Lagrangian (`4K → 8K`) | `K0_lapse_eq_is_hamiltonian_constraint` | FAIL, same residual /4 |
| `tt_gradient_sign` | TT gradient term sign flipped (`R3^{(2)} → +p²h²/4`) | `K5_TT_gradient_term_is_exactly_curvature`, `K7_cT2_equals_one_exactly` | FAIL `+kz²/(4a²)` vs `−kz²/(4a²)`; FAIL `c_T² = −1` |
| `naive_stiffness` | Hodge pair `−(γ/2)(D·P)² − (γ/4)F²` replaced by the non-Hodge `−(γ/2)|D_iP_j|²` | `K7_cT2_equals_one_exactly` | FAIL `c_T² = 1 + 2K|P|²` |
| `cs_equal_eta` | de Sitter gap dropped from the scalar restoring term (`V → γp⁴`) | `K9_scalar_causality_inequality` | FAIL, quadratic becomes `−p²(3Kβ+2K+βηp²−βγp²)/β` |

Recorded stdout of each run (only the failing lines and the tally):

```
=== r3_sign ===
K0_lapse_eq_is_hamiltonian_constraint    FAIL  value=(21*FP**2*FV**17 - 24*FP*FV**18 - 28*FPP*FV**18)/(12*FV**(37/2)) threshold=0
A3 COMPLETE: 14/15 checks PASS.

=== k_factor ===
K0_lapse_eq_is_hamiltonian_constraint    FAIL  value=(21*FP**2*FV**17 - 24*FP*FV**18 - 28*FPP*FV**18)/(48*FV**(37/2)) threshold=0
A3 COMPLETE: 14/15 checks PASS.

=== tt_gradient_sign ===
K5_TT_gradient_term_is_exactly_curvature FAIL  value=kz**2/(4*a**2)                 threshold=-k^2/(4a^2)
K7_cT2_equals_one_exactly                FAIL  value=-1                             threshold=1
A3 COMPLETE: 13/15 checks PASS.

=== naive_stiffness ===
K7_cT2_equals_one_exactly                FAIL  value=2*K*PV**2 + 1                  threshold=1
A3 COMPLETE: 14/15 checks PASS.

=== cs_equal_eta ===
K9_scalar_causality_inequality           FAIL  value=-p**2*(3*K*beta + 2*K + beta*eta*p**2 - beta*gamma*p**2)/beta threshold=(gamma-eta)p^4-Bp^2+2BH^2
A3 COMPLETE: 14/15 checks PASS.
```

## Why these mutations are the right ones

* `tt_gradient_sign` and `naive_stiffness` are exactly the two ways the GW gate can actually fail in
  this class of theory: a wrong sign of the tensor gradient term (tachyonic graviton,
  `c_T² = −1`) and a non-Hodge stiffness (luminality violation `c_T² = 1 + 2K|P̄|²`). Both are the
  physically motivated breakers listed in report §3.2.
* `r3_sign` and `k_factor` are the two transcription errors that matter for the static sector: the
  overall sign of the 3-curvature and the normalisation of `K` (the brief's `8πG` vs the action's
  `4πG`). Both break the Hamiltonian identity, so the identity is not tautological.
* `cs_equal_eta` tests the scalar dispersion: dropping the `2BH²` gap changes the causality quadratic,
  so K9 is sensitive to the whole dispersion relation and not only to its high-`p` limit.

## Deliberately *not* mutated

`K1` (Schwarzschild solves the constraint) and `K3` (the anisotropic stress) are already
inhomogeneity-sensitive: `K1` is evaluated in exact rational arithmetic on an exact solution, and `K3`
compares two closed forms in `u`. A sign error in either is caught by the identity itself. `K2`
(`P = 0` is not a solution) is a strict non-zero test, so it cannot be satisfied by a wrong sign.
