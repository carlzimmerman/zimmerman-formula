# A39 MUTATE — do the checks have teeth?

`a39_checks.py --mutate NAME` injects one defect at a time into the **geometry or the operator**,
never into the check logic. A defect that left the suite green would mean the corresponding check is
vacuous.

Baseline: `python3 a39_checks.py` → `A39 COMPLETE: 21/21 checks PASS.` (exit 0, 5.3 s).

| mutation | defect injected | checks that break | tally |
|---|---|---|---|
| `inverse_linear` | inverse metric truncated to first order, `g^ij = δ^ij − h^ij` (the `h^{ik}h_k{}^j` term dropped) | C0, C1, C2, C3, C4, C8, C11, C20 | 13/21 |
| `no_sqrtg` | volume element set to 1, `√g → 1` (the `−¼ tr h²` piece of `√g` dropped) | C2, C3, C4, C8, C11 | 16/21 |
| `W_sign` | sign of the potential flipped, `W → −W` | C2, C3, C4, C8, C9, C10, C11 | 14/21 |
| `no_running` | `δP` relaxation ignored — the frozen coefficient used at every frequency | C10 | 20/21 |
| `a31_coefficient` | A31's `3Kp/8` used as the `h²` coefficient of the action (i.e. `d²u/dh²` read as the mass) | C2, C2b, C3, C20 | 17/21 |

Recorded stdout of each run (only the failing lines and the tally):

```
=== inverse_linear ===
C0_inverse_metric_correct_to_O_h2              FAIL  value=g g^{-1} - I = diag(-c**2*h**2, -c**2*h**2, 0)
C1_u_expansion_coefficients                    FAIL  value=u/Kp = 1 + (-c/2) h + (-1/8) h^2
C2_closed_form_literal_expansion               FAIL  value=residual = 4*x**2/(x - 1)
C3_volume_piece_is_the_Lambda_coupling         FAIL  value=c_hh - c_shape - Wbar/4 = -x**2/(4*x - 4)
C4_general_direction_and_polarization          FAIL  value=residual = 4*x**2*sin(theta)**2/(x - 1) ; k||Pbar residual 0
C8_static_elimination_screens_the_shape_term_to_O_u3 FAIL  value=c_eff(0) - W/2 = x**2*(x - 4)/(8*(x - 1))   (= -u^2 x/(8(1-x)) = -x^3/(8(1-x)))
C11_running_mass_closed_form                   FAIL  value=max rel. deviation = 1.66e+01
C20_A31_coefficient_is_d2u_dh2_not_the_action  FAIL  value=d2u/dh2 = 3Kp/8 ; d2W/dh2 = K**2*a0*p**3/(4*(K**2*p**2 - 2*K*a0*p + a0**2))
A39 COMPLETE: 13/21 checks PASS.

=== no_sqrtg ===
C2_closed_form_literal_expansion               FAIL  value=residual = -4*x - 4*log(1 - x)
C3_volume_piece_is_the_Lambda_coupling         FAIL  value=c_hh - c_shape - Wbar/4 = x/4 + log(1 - x)/4
C4_general_direction_and_polarization          FAIL  value=residual = -4*x - 4*log(1 - x) ; k||Pbar residual -4*x - 4*log(1 - x)
C8_static_elimination_screens_the_shape_term_to_O_u3 FAIL  value=c_eff(0) - W/2 = (x**3 + 4*(x - 1)*(x + log(1 - x)))/(8*(x - 1))   (= -u^2 x/(8(1-x)) = -x^3/(8(1-x)))
C11_running_mass_closed_form                   FAIL  value=max rel. deviation = 8.01e+00
A39 COMPLETE: 16/21 checks PASS.

=== W_sign ===
C2_closed_form_literal_expansion               FAIL  value=residual = 2*(-x**3 - 4*x**2*log(1 - x) + 4*x**2 + 8*x*log(1 - x) - 4*x - 4*log(1 - x))/(x**2 - 2*x + 1)
C3_volume_piece_is_the_Lambda_coupling         FAIL  value=c_hh - c_shape - Wbar/4 = x**2*(4 - 3*x)/(8*(x**2 - 2*x + 1))
C4_general_direction_and_polarization          FAIL  value=residual = 2*(-4*x**3*sin(phi)**4*sin(theta)**4 + 4*x**3*sin(phi)**2*sin(theta)**4 - x**3*sin(theta)**4 + 4*x*
C8_static_elimination_screens_the_shape_term_to_O_u3 FAIL  value=c_eff(0) - W/2 = -x**3/(8*x - 8)   (= -u^2 x/(8(1-x)) = -x^3/(8(1-x)))
C9_P_field_mass_is_sqrt2_over_Lstar            FAIL  value=m_Y^2 = -2 c_YY/(K L*^2/2) = -2/(L_**2*(x**2 - 2*x + 1))
C10_running_mass_interpolation                 FAIL  value=max rel. deviation over 8 (x, omega) points = 3.31e+00
C11_running_mass_closed_form                   FAIL  value=max rel. deviation = 2.00e+00
A39 COMPLETE: 14/21 checks PASS.

=== no_running ===
C10_running_mass_interpolation                 FAIL  value=max rel. deviation over 8 (x, omega) points = 1.77e+00
A39 COMPLETE: 20/21 checks PASS.

=== a31_coefficient ===
C2_closed_form_literal_expansion               FAIL  value=residual = (x**2*(3*x - 4) + (-10*x - 4*log(1 - x))*(x - 1)**2)/(x - 1)**2
C2b_finite_difference_confirms_the_series      FAIL  value=max rel. error of d2/dh2 = 5.66e+00
C3_volume_piece_is_the_Lambda_coupling         FAIL  value=c_hh - c_shape - Wbar/4 = (-3*x**3 + 4*x**2 + 2*(5*x + 2*log(1 - x))*(x**2 - 2*x + 1))/(16*(x**2 - 2*x + 1))
C20_A31_coefficient_is_d2u_dh2_not_the_action  FAIL  value=d2u/dh2 = 3Kp/8 ; d2W/dh2 = -a0*p*(-K*a0*p + 3*a0*(K*p - a0) + 3*(K*p - a0)**2)/(4*(K*p - a0)**2)
A39 COMPLETE: 17/21 checks PASS.
```

`inverse_linear` also exposes the coefficient directly: `u/Kp = 1 − (c/2)h − (1/8)h²` instead of
`+3/8`, and its metric product is `−h²c²·diag(1,1,0)`, not `O(h³)`.

## Why these mutations are the right ones

* `inverse_linear` and `no_sqrtg` are the two transcription errors that would silently change the
  coefficient: the second-order inverse metric and the volume element. Both are *required* for the
  `h²` term — dropping either changes `m_T²` by an `O(1)` factor, so a coincidence cannot rescue a
  wrong expansion. `inverse_linear` is the mistake A31's `1/√(1+h)` shorthand invites: `1/√(1+h)` is
  exact for one mode, but the general `g^ij` needs the `h²` term, and the general-direction check C4 is
  the one that sees it.
* `W_sign` is the tachyon mutation: if the potential entered with the other sign, the mass would be
  imaginary. C5 (positivity) is *not* the check that catches it — C5 tests the closed form, not the
  symbolic derivation — C2/C3/C4 do. That is deliberate: C5 is a scan of the final formula, and the
  formula is protected upstream by the identities.
* `no_running` is the physical-content mutation: it asserts that the `δP` relaxation does not happen.
  Only C10 breaks, which is correct — the frozen and running masses agree to `10⁻²⁴` at every
  observable frequency, so nothing else *should* notice.
* `a31_coefficient` is the mutation that reproduces the defect under review: the `h²` coefficient of
  `u` used as the `h²` coefficient of the action. It breaks the closed form, the finite-difference
  cross-check and the A31 identification check.

## Deliberately not mutated

C5–C7, C12–C19 are numeric or structural evaluations of the closed form (positivity on a grid, a limit,
the observed-frequency numbers, the bound comparisons). They are protected by C2/C3/C4: if the closed
form were wrong, those three break first. C12 (`c_T² = 1`) is algebraic in `ω² = k² + m_T²` and cannot
fail without the mass term acquiring a `k`-dependence, which the operator cannot produce (`W` carries no
derivative of `h`).
