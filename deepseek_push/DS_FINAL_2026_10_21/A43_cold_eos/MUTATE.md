# MUTATE — three formula slips, each breaks exactly one check

Run: `python3 a43_checks.py --mutate | --mutate2 | --mutate3`. Base run is 23/23 PASS, exit 0.
Each mutation is a *formula* change a careless derivation would make; each is caught by one check
and only one, so the check has teeth and the suite is not one big conjunction.

## M1 — the harmonic tether term dropped

`3p_T/ε_T = n` is replaced by `n−2`, i.e. the n = 2 (harmonic) contribution is lost — the slip you
make if you differentiate `φ_T ∝ ξ²` once too often and land on `ξ·∇φ_T = 2φ_T − 2φ_T = 0`.

```
K4 FAIL 3p_T/eps_T = 0.0000/0.3333/0.6667 n/3 = 0.6667/1/1.3333
A43 COMPLETE: 22/23 checks PASS.
```

Why it matters: with `p_T = 0` at n = 2 the tether contributes nothing to `w`, and the whole
`(A43.6)`–`(A43.7)` chain (`p_T = ρ(σ²+Φ)`, `w = 0` at virial) collapses. K4 is the only check that
pins the coefficient; K6/K7 test the sign and the virial identity independently, so they still pass
— the mutation is localised, as intended.

## M2 — `<w> = u−1` instead of `(u−1)/3`

The A21 K12 slip: forgetting that `u = 1+3⟨w⟩` inverts to `⟨w⟩ = (u−1)/3`, not `u−1`. This
inflates every `|w|` by 3 and, through `1+3w`, sends the required rest-mass factor negative.

```
K20 FAIL f_ret(MID) = -1.768 +- -0.271 (10.2 sigma above 1); f_ret(INNER) = -1.040 +- -0.175
A43 COMPLETE: 22/23 checks PASS.
```

Why it matters: the whole identification argument (`f_ret = 1.035/(1+3w) > 1`) is a function of the
inversion. The negative `f_ret` is the signature: a wrong factor of 3 does not just rescale the
answer, it flips the sign of the required binding. K20 is the only consumer of `W_OF_U` in a
threshold, so only K20 breaks.

## M3 — the tether term with the wrong sign

`p_T = +(n/3)ε_T` becomes `−(n/3)ε_T`, the sign error that would let a *stable* tether produce
tension and would "explain" `u < 1` for free.

```
K6 FAIL min w over (sigma, eps_T/rho c^2 in [0,0.5]) = -3.333e-01 >= 0
A43 COMPLETE: 22/23 checks PASS.
```

Why it matters: this is exactly the claim the lane denies. With the sign flipped, a
positive-definite tether at `ε_T = 0.5ρc²` gives `w = −1/3` and `u = 0`, i.e. the measured anomaly
appears to be explained. K6's grid is the guard: for `ε_T ≥ 0` the minimum over all `(σ, ε_T)` must
be `≥ 0`, and it is not. K7's sympy virial identity is independent of the sign convention and does
not catch it, which is why the two checks are both present.

## What is *not* mutated, and why

The NFW/`X(r)` chain (K13–K15) was tried as a fourth mutation (baryon-only mass in `g/a₀`) and it
does **not** break: dividing `X` by 6.364 moves `r(X=1)` from 0.201 to ≈0.13 Mpc, so the ratio to
the measured crossing grows from 5.30 to 8.2 and the threshold (`> 3`) still passes. That is a
property of the data, not a weakness of the check: route (iii) fails by a factor, and any
normalisation error that keeps the factor above 3 is not the thing being tested. The check with
teeth for route (iii) is K14's shape test (Δχ² = 160), which no monotone rescaling of `X` can pass.
