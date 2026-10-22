# A60 — mutation records

Every mutation alters a **term or an assumption in the computation**, not a boolean. Each is run as
`python3 a60_checks.py --mutate NAME`; each exits 1. The baseline is 20/20 PASS, exit 0.

| mutation | what it changes | checks that break | the measured failure |
|---|---|---|---|
| `flat_background` | sets the galactic background to zero (`ubar = 0`, `Pbar = 0`), i.e. puts the Sun back in empty space | K3, K9, K10, K20 | `K W'(0)/g - 1 = -1` (the background is no longer on-shell); `u_sun/u_gal = 2.42e14`; the `u` table loses its 0.566 a0 plateau |
| `slaved_sun` | forces the solar field onto the slaved branch, `u_sun = a0` (A36 K12's counterfactual) | K9, K10, K20 | `u_sun/u_gal = 1.77` (a 1.77 a0 total field, above the cap); table spread 3.9e5; the gradient cost would be `2 gamma a0/(K r^2) = 2.3e3 m/s^2`, 3.9e5 x `g_sun` |
| `eps_r_only` | drops the `g_gal/g_sun` factor from the expansion error, i.e. assumes `eps_bg = r/R_gal` | K5 | `eps_bg(1 pc) = 1.25e-4` instead of 0.11: the claim "controlled to 1 pc" would be wrong by three decades |
| `alpha1_k0` | applies the **galactic** limit `4u'/(1-u')` at 1 AU (as if `k L* -> 0` in the Solar System) | K12, K20 | `alpha_1(1 AU) = 0.928` instead of `1.63e-13` — seven orders above the bound; this is the error the lane exists to rule out |
| `alpha1_prefactor2` | uses the 2-prefactor `2u'/(D-u')` (A36 K11's expression) as the answer | K12, K20 | `alpha_1(1 AU) = 8.16e-14` against the exact `1.63e-13` |
| `pioneer_visible` | sets `a_P = a_Pioneer = 8.74e-10 m/s^2`, i.e. identifies the P-sector anomaly with the Pioneer anomaly | K17, K20 | `a_P/a_Pioneer = 1` and the preferred-frame signal `2w^2 a_P = 1.0e-9 m/s^2`, 7.5x the thermal residual — the theory would be excluded by Pioneer instead of being 1.8e11 below it |

Notes.

* `flat_background` is the mutation that tests the lane's premise: with the Galaxy switched off, the
  configuration collapses to A22's isolated hedgehog and `u_gal/u_sun` has no meaning. K3, K9 and K10
  all catch it; K12 does **not**, because `alpha_1(1 AU)` is insensitive to the background — which is
  itself the lane's main result.
* `alpha1_prefactor2` is deliberately *inside* the safe direction: it makes `alpha_1` smaller than the
  exact value. It still breaks K12, because K12 compares three independent routes rather than checking
  a bound. A mutation that only breaks a bound check would not test the arithmetic.
* `slaved_sun` does not break K11: K11's gradient-balance residual is computed from the exact profile,
  which the mutation does not touch. K9 and K10 carry it. This is recorded rather than patched — the
  mutation is a statement about `u_sun`, and `u_sun` is what K9's table measures.
* All six mutations leave `a60_results.json` unwritten (`--json-out` is suppressed when a check fails),
  so a mutated run can never masquerade as a result file.