# Independent audit: conditional full closed-set linear work

19 October 2026. Reviewer `/root/audit_cold_work`.

**Normalized claim.** Fix one actual positive-warmth cold-dominated halo with
the full-gradient, finite simple circular-threshold, flat-cap and endpoint
geometry in the named inputs. Assume (CF) for every member of every actual
kernel, and assume the stated whole-field simple-pole-plus-Hölder reduced
inverse. For every smooth compactly supported radial fixed-L canonical
generator, the actual full linear work along equilibrium orbits is uniformly
bounded in time, angle, species and the entire closed occupied action set.
The linear label has the resulting uniform bound. Constants may depend on
finitely many smooth-source seminorms and the energy norm, and on the fixed
halo. No nonlinear or energy-norm-only assertion is included.

**Primary verdict: proved as written.** This is a verdict on the conditional
theorem and the new implications in this artifact. It does not establish
(CF), remove the explicitly named operator inputs, or independently certify
the complete underlying equilibrium and energy theory.

**Exact artifact audited:** `/private/tmp/conditional_cold_work_20261019.md`,
SHA-256 `b20cefd311eee9e356e1437f5ab6cbe0bb00db19027ebcede0ff374e2bdfab9f`.

## Dependency graph

1. Actual canonical datum, smooth physical weight and actual shell equation
   imply a smooth initial field and rapidly decaying smooth orbital source
   coefficients, each zero at the circle.
2. Actual indicator-harmonic estimate plus the circular product argument and
   full-frequency submersion charts imply the global source transform bound
   (3.4), with separate unweighted Hölder and weighted amplitude bounds.
3. Kernel bootstrap, exact weighted regular division and (CF) imply positive
   Hölder regularity of the scalar left-coupling divided density.
4. The scalar Cauchy identity implies bounded Hölder left-coupling difference
   quotients. Reciprocity and the actual mode formula identify their values
   at the pole with the actual polarized energy pairing.
5. The named reduced inverse and that finite-rank source regularity give the
   Hölder continuous-component derivative transform with amplitude decay
   `O(1/|z|)`.
6. The elementary frequency-to-work inequality, the local amplitude/Hölder
   minimum, the far-frequency integral and angular extraction give an
   absolutely summable work series, uniformly over the closed receivers.
7. Actual damped Fourier identification and finite-time removal of damping
   give continuous-component work. The mode receiving quotients and finite
   mode set give modal work. The exact endpoint identity gives the label bound.

The whole-field reduced inverse is an input, not a consequence of the work
bound. The proof never uses whole-field differentiability of the forcing.
There is no circular dependency among these new implications.

## Obligation matrix

| Obligation | Status | Decisive check |
|---|---|---|
| Exact spaces, data and closed receiving domain | passed | `Y_gamma=C^gamma(I)^2`, `0<gamma<1/2`; boundary label defined by transport |
| Smooth source coefficients and harmonic decay | passed | Physical smoothness and smooth oscillator pullback; integration by parts in angle |
| Circular product in ordinary actions | passed | Two factors vanish at `a=0`, giving `(a+b)|a-b|=|J-J'|` |
| Full-gradient coarea and fixed harmonic support interval | passed | Zero-extended products remove moving domains; use `y=Omega`, not `k Omega` |
| Global Hölder forcing and `O(1/|z|)` amplitude | passed | Interpolation and low/high harmonic split retain output-radius difference |
| Regular/cap weighted modal division | conditional | Exact input supplied by `REDUCED_INVERSE.md`, Section 2 |
| Threshold left-coupling quotient | passed | Under (CF), its density is `O(s^2)` and the divided density is Lipschitz |
| Finite-rank source difference quotient | passed | Cauchy algebra applied to the divided scalar density |
| Energy projection, Gram indices and residue sign | passed | Formula (5.1) and the declared conjugate-linear first argument of `Q` |
| Whole-field simple-pole-plus-Hölder inverse | conditional | Named operator input, with authenticated corrected (CF) version |
| Continuous derivative transform | passed | Pole subtraction matches actual spectral modes and leaves bounded Hölder finite-rank terms |
| Dini estimate without weighted Hölder norm | passed | The local minimum gives `k^(-1-gamma)` times a logarithm |
| Damped reconstruction, angular summation and limit | passed | Time `L^1`/`L^2`, absolute work-series bound, Fourier uniqueness, finite-time dominated convergence |
| Modal work at circle, cap and physical ends | conditional | Named mode/geometry inputs supply the exact closed-set quotients; (CF) handles the fundamental threshold |
| Actual (CF), nonlinear paths and confinement | out of scope | Not asserted by the conditional theorem |

## Critical reconstruction

### Smooth forcing and the circle

The forcing is exactly

`B(z)=-P[sum_(k!=0) w omega_k A_k e^(ik theta)/(omega_k-z)]`,

where `A_k=-(Dg_0)_k+(psi_in)_k`. The sign follows by transforming the free
derivative and adding `K(z)psi_in`. This agrees with the raw Volterra identity.
Since `h_0=-wDg_0` is physical smooth compact data, the actual shell field
equation makes `psi_in` smooth. Its pullback and the pullback of `Dg_0` have
rapid Fourier decay in every fixed finite oscillator seminorm, and all
nonzero harmonics vanish when `a=sqrt(J)=0`.

For a fixed output difference, both the shell harmonic difference `U_k(a,L)`
and `A_k(a,L)` are Lipschitz in `(a,L)` and zero at `a=0`. Thus

`|U_k(a)A_k(a)-U_k(b)A_k(b)| <= C_M(1+|k|)^(-M)(a+b)|a-b|`.

This is the necessary ordinary-`J` Lipschitz bound. The separate indicator
estimate supplies the stronger sup bound `C_M d(1+|k|)^(-M-1)`.
Interpolation gives (3.2). The flat `w` supplies the other support extensions.
The finite submersion charts may therefore push forward on one fixed
`Omega` interval. The Cauchy estimates apply there with constants independent
of `k`; changing to `z/k` introduces the stated `|k|^(-alpha)` in frequency
increments. Low harmonics gain `|k|/|z|` away from support, and the rapidly
decaying complementary tail gives the remaining `O(1/|z|)` bound.

### Left-coupled pole cancellation

Reciprocity gives the scalar numerator

`-sum integral w omega_k conjugate(phi_a,k) A_k/(omega_k-z) dm`.

In regular eccentric charts, the named weighted quotient
`sqrt(w) phi_a,k/t` is Lipschitz. In regular circular charts it is Lipschitz
in `(a,L)`, is zero at `a=0`, and is multiplied by a smooth weighted source
coefficient also zero there. The same two-factor estimate works; alternatively
coarea solving for `L` keeps `a>=0` fixed. No unweighted trace at an exterior
flat cap is inferred from the weight.

At a circular threshold use `t=epsilon rho^2` with measure
`b c(b^2,x) db dx`. Under the kernel bootstrap and (CF), `g=O(rho^2)` and
`grad g=O(rho)`, while the smooth source factor `f=O(rho)` has bounded first
derivatives. The angular integral of `g^* f c` is `O(rho^3)` and its radial
derivative is `O(rho^2)`. Coarea multiplies it by `rho`, so `q=O(rho^4)`.
Consequently `q(epsilon s)/s` is `O(s)` with bounded derivative. Extending it
by zero across the other side is Lipschitz. This proves the positive-Hölder
divided density needed in the scalar Cauchy identity.

Thus the proof establishes `[ell_a B(z)-ell_a B(nu)]/(z-nu)`; it never needs
`[B(z)-B(nu)]/(z-nu)` bounded on all of `Y_gamma`.

At `z=nu`, inserting the actual mode formula gives

`ell_a B(nu)=integral conjugate(h_a)(h_0/w+psi_in) dGamma=Q[h_a,h_0]`.

The Gram inverse therefore gives `R_nu B(nu)=nu P[P_nu h_0]`. With the
declared Laplace convention,

`hat[partial_t(e^(-i nu t)Phi)](z)=nu Phi/(z-nu)`.

Both the sign and the finite-rank projection are correct. Combining this
left-coupling regularity with the given reduced inverse proves (6.2) for the
actual projected solution.

### Why amplitude decay suffices for harmonic summation

There is no missing weighted Hölder assumption. At a large receiving
frequency `omega=k Omega(q)`, the separate bounds already proved imply, on
its unit neighborhood,

`|a_k| <= C M |k|^(-1-gamma)`,

`omega_(a_k)(s) <= C min(M |k|^(-1-gamma), H |k|^(-gamma) s^alpha)`.

Direct integration of this minimum divided by `s` is bounded by

`C_alpha M |k|^(-1-gamma)[1+log(1+|k|H/M)]`.

The far-frequency integral is bounded by
`C M |k|^(-1-gamma)log(2+|k|)`. Since `gamma>0`, both sequences are summable.
Moreover `log(1+kH/M)<=log(1+k)+log(1+H/M)` and
`M log(1+H/M)<=H`, so the summed bound is linear in `M+H`. The finitely many
small harmonics use the original Dini estimate. The zero harmonic is an
integration-by-parts endpoint estimate.

For fixed damping, bounded continuous derivative fields give time `L^1`
and `L^2`; the frequency representation is justified by the `L^2` Fourier
pairing. Its far-frequency integral is absolutely convergent using the
amplitude decay. The summable work coefficients define a uniform Fourier
series, and Fourier uniqueness identifies it with the continuous actual
damped work as a function of initial angle. Letting damping tend to zero at
each fixed finite time is legitimate and leaves the uniform bound. Every
estimate is uniform over the closed action set, so no receiver-boundary
limit or receiving-frequency separation is hidden.

## Exact remaining gap and strongest safe statement

There is **no additional missing implication in this conditional theorem**.
The unresolved model-specific step for an unconditional theorem is proving
(CF) for every actual mode, or finding an actual mode violating it. The
whole-field reduced-inverse statement remains a named mathematical
dependency of this audit. Its source version uses `|nu_0|` and has the hash
recorded below. The theorem makes the same negative-frequency requirement
by conjugation, so there is no sign-scope mismatch.

The strongest safe conclusion is the stated conditional full linear
closed-set work/label bound for smooth canonical data, with source seminorm
dependence. A cheaper next check than revisiting this forcing argument is
the actual spectral implication (CF); that is a separate research task.

## Source authentication and provenance

The following SHA-256 values were checked by `shasum -a 256` against the
files actually read. The first six are in
`real_research/analytic_review_2026_10_18_codex/cold_dominated_feedback_2026_10_19/`:

- `BOUNDARY_PAIRING.md`: `5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d`
- `HIGH_FREQUENCY_INVERSE.md`: `6111b7f0f2e2ea0ef1ea80b81c1a1227374bedc270614c50698db830ade8d49c`
- `REGULAR_INVERSE.md`: `4830712683b98b46a53b796b4bde109c618a4fd26fa910cd47176ebe9f3ddf80`
- `THRESHOLD_MODES.md`: `40304ae8d1c0495cdd7482202aa9dcdfa494f12287754b7e648dd2adf26a77b5`
- `GEOMETRY_AND_CAP.md`: `c40c5f63e533fe19e41b996e292d21892160bf2b4aa31ffb499313b64f54fc0d`
- `REDUCED_INVERSE.md`: `ebc588cbd3fef36295dc355542f5b5344327c6ed1d76af12e777ee36786e93d1`
- `../claude_continuation_2026_10_19/full_feedback/RESULT.md`: `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`

This is a fresh isolated-agent focused audit, independently reconstructing
the new forcing, left-coupling, residue and summation implications from their
raw formulas. It is not a second derivation of every named input theorem.
The proof-audit skill and relevant general/sign/duality checklist were read.
No external mathematical source is needed by the new implications. No
scientific script, numerical calculation, scientific array, or process
manipulation was used. Repository sources were not edited; this report is
the only file written by this reviewer.
