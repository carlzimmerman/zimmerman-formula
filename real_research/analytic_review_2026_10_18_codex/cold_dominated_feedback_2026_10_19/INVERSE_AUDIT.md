# Independent audit: source duality, uniform kernel reconstruction, and the leading inverse pole

19 October 2026. Reviewer `/root/audit_boundary_inverse`, a fresh delegated
proof-audit session. Analytic reasoning and text/hash operations only. This
report is the only file written by this reviewer.

## Normalized claim and primary verdict

Fix one actual, strictly positive-warmth two-species halo. Assume the existing
coercive energy theorem, its selfadjoint energy generator and compact
energy-to-field map, the smooth nondegenerate-well orbit coordinates and flat
susceptibility extension, and the no-full-frequency-critical-point geometry
with finitely many simple circular epicyclic extrema stated in the audited
artifacts. Let `Y=C^gamma(I;C)^2`, `0<gamma<1/2`, and
`sigma=1-gamma>1/2`. The normalized conclusion is:

1. The actual source boundary map `T_+(nu):Y -> Y^x` exists locally in operator
   norm, and the actual reciprocal shell operator makes
   `K_+(nu)=P T_+(nu)` compact on `Y`.
2. Every boundary kernel field reconstructs an actual energy eigenmode,
   with `||h_nu||Q <= C_J ||phi||Y` locally uniformly on every compact real
   frequency interval `J`; conversely every energy eigenfield is a boundary
   kernel field.
3. The exceptional real frequencies are locally finite. The ordinary
   boundary inverse is continuous and bounded on compact sets avoiding them.
4. At each nonzero exception `nu_0`, the upper-closure inverse has norm
   `O(|z-nu_0|^-1)` and the stated finite-rank leading residue determined by
   the positive `Q` Gram matrix. A bounded pole-subtracted inverse is not
   claimed.

**Primary verdict: conditional on the named existing energy/equilibrium
inputs.** The new implications in the two raw proofs pass this audit under
their explicit hypotheses. In particular the weighted square-root-coordinate
argument, local finiteness, and asymmetric Schur estimates do not require an
additional no-mode assumption or a small-susceptibility assumption. The
leading-pole conclusion is correctly limited: it does not supply a bounded,
Dini-continuous inverse after subtraction, or a whole-receiving-set work
theorem. This report does not independently re-audit the older conserved
energy/equilibrium existence proofs.

## Exact artifacts and dependency graph

The following exact raw revisions were read and audited:

- `real_research/analytic_review_2026_10_18_codex/cold_dominated_feedback_2026_10_19/BOUNDARY_PAIRING.md`:
  SHA-256 `5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d`.
- `/private/tmp/cold_inverse_20261019.md`:
  SHA-256 `4830712683b98b46a53b796b4bde109c618a4fd26fa910cd47176ebe9f3ddf80`.
  An earlier draft with hash `1af6c1720362cfbad5819713ad2840bc71b10449ab51e8940d2163b7ab2a7463`
  was also read; this verdict is pinned to the later revision above, including
  its explicit nonresonant differentiated-tail paragraph.

Dependency graph:

`smooth orbit/weight geometry + full frequency submersion`
`-> circular product gain -> regular source pushforward densities`
`-> norm boundary source limits + Parseval tail`
`-> reciprocity and optical zeros`
`-> P smoothing/compactness on the complete source anti-dual`
`-> C^sigma kernel fields`
`-> weighted trace zeros + exact semicircle chart`
`-> uniform energy reconstruction`
`-> actual eigenmodes + compact energy-to-field map + Q orthogonality`
`-> locally finite exceptions and inverse away from them`.

For the local leading pole, append:

`reciprocity -> concrete cokernel functionals`
`+ asymmetric Cauchy increments -> O(d^sigma) off-diagonal blocks`
`+ two-kernel density division -> derivative Q_Gram/nu_0`
`-> Schur correction O(d^(2 sigma))=o(d)`
`-> leading pole and O(1/d) inverse`.

No dependency returns to an assumed boundary inverse. The full work theorem,
global high-frequency decay, and bounded pole-subtracted inverse are not
leaves used to prove this claim.

## Obligation matrix

| Obligation | Status | Decisive reason |
| --- | --- | --- |
| Circular product is `C^gamma` in ordinary actions | Passed | Each factor is `O(a^gamma)` and `C^gamma` in `a`; the product difference is bounded by `(a+b)^gamma |a-b|^gamma=|J-J'|^gamma`. |
| Zero extension at the circular boundary | Passed | The product is `O(J^gamma)` and vanishes at `J=0`; an individual harmonic need not have this regularity. |
| General full-gradient resonance charts | Passed | After product/weight extension there is a fixed smooth chart amplitude. Either action derivative can provide the frequency coordinate. |
| Full source norm, including high harmonics | Passed | Parseval and the uniform orbital `C^gamma` tail estimate give a summable operator tail; no invalid scalar `sum |k|^(-2 gamma)` is used. |
| `P` on the complete source anti-dual | Passed | Mixed kernel approximation controls successive dual applications; no density of measures in the full dual is assumed. |
| Local frequency continuity and compactness | Passed | Finite regular Cauchy charts and a uniform nonresonant tail give norm continuity; `P` gains to `C^(1-gamma)`. |
| Optical zero for an arbitrary kernel field | Passed | The real reciprocal pairing `<P S,S>` makes the optical density vanish, independently of an inverse. |
| Square-root weight is Lipschitz | Passed | Apply the nonnegative `C^2` square-root lemma on signed `a` coordinates; `w(a^2,L)` has the required nonnegative even extension at `a=0`. |
| Exact circular threshold coordinates and Jacobian | Passed | The displayed definitions give exactly `omega-omega_c=epsilon(b^2+x^2)` and `dJ dL=b c(b^2,x)db dx`, with positive smooth `c`. |
| Uniform nearby-level energy estimate | Passed | Subtract at the resonant point on the same half-ray; the resulting one-dimensional majorant has exponent `2 sigma-2>-1`. |
| Flat cap intersections in reconstruction | Passed | The weighted numerator is zero outside support, so no unproved unweighted cap division is needed. |
| Generator-domain membership | Passed | The reconstructed Fourier equation gives `D h=-i nu h-w D phi` in the energy space after the energy-to-`C^1` upgrade. |
| Local finiteness of exceptions | Passed | Uniformly energy-bounded modes at distinct real frequencies are orthogonal; compactness forces their normalized fields to tend to zero, a contradiction. |
| Asymmetric regular-channel estimate | Passed | Split `g f=f(0)g+g(f-f(0))`; the first transform is `C^sigma`, and the remainder changes by `O(d log(1/d))`. |
| Asymmetric circular-channel estimate | Passed | The density is `O(s)` with scaled local increment bounds; its Cauchy increment is `O(d log(1/d))`. |
| Two-kernel derivative and sign | Passed | Divide the zero density by detuning; its positive Hölder exponent makes the derivative converge. The derivative is `Q_Gram/nu_0`. |
| Upper-closure Schur remainder | Passed | Both off-diagonal increments are `O(d^sigma)`, whose product is `o(d)` because `sigma>1/2`. |
| Bounded inverse after pole subtraction | Not addressed, explicitly excluded | An `o(d)` Schur remainder need not be `O(d^2)`; the remaining inverse branch can diverge. |
| Global finiteness from high-frequency decay | Out of scope | The inverse artifact makes this a separate input. |
| Existing coercive energy and actual equilibrium existence | Conditional named inputs | Read for context; not independently re-proved in this focused audit. |

## Independent reconstruction of the critical implications

### Complete duality and actual shell reciprocity

For a source/test pair, the circular numerator is a product of two nonzero
orbital harmonics. If `J=a^2` and `J'=b^2`, then

    |A(a^2,L)-A(b^2,L)|
      <= C(a^gamma+b^gamma)|a-b|^gamma
      <= C|J-J'|^gamma.

This is the needed gain before a full-gradient action-frequency chart is
used. The product vanishes to order `J^gamma`; thus its zero extension to
negative `J` has the same Hölder exponent. Smoothly zero-extended weights
handle cap and angular momentum edges. Integrating a compact chart amplitude
in the complementary coordinate preserves its `C^gamma` modulus. Subtraction
of the density at the resonant frequency gives an absolutely integrable
`|s|^(gamma-1)` remainder and norm boundary convergence.

For the all-dual reciprocal extension, write `E=P_epsilon-P`. Its rectangular
increment satisfies

    |Delta_h Delta_k E| <= C min(epsilon,|h|,|k|).

The mixed Hölder quotient is at most `C epsilon^(1-2 gamma)`; this follows
by separating the smallest of the three scales. Together with the
one-variable norms this permits successive application of any two complete
source anti-duals. Symmetric smooth finite-rank approximations then pass
reciprocity to the limit. Interpolation of the kernel sections gives
`P:Y^x -> C^(1-gamma)`, compactly into `Y`.

The source artifact's optional isolated eccentric Morse subtraction is also
consistent with its stated hypotheses: its coarea constant is
`2*pi/(n sqrt(det D^2 Omega))`, hence the displayed `beta`; the remainder
density is `O(s^(gamma/2))`. The present inverse claim uses the specialization
without eccentric critical points.

### Weighted Hölder reconstruction at and near circular thresholds

Let `G=sqrt(w) phi_k`. The nonnegative smooth weight has a locally Lipschitz
square root in `(a,L)`. Optical zeros imply `G=0` on every resonant level,
including portions outside support by weight extension. Also `G(0,L)=0`.

The exact coordinates in inverse Section 5 are legitimate smooth half-plane
coordinates: `x` has nonzero derivative at `L_c`, while `b=a` times a smooth
positive function of `(a^2,L)`. Thus the action measure is `b` times a smooth
bounded positive density. In polar coordinates it is comparable to
`rho^2 sin(theta) d rho d theta`.

For an occupied-side nearby level `rho^2=s>=0`, compare `G(rho,theta)` with
its zero at `G(sqrt(s),theta)`. The squared response is bounded by

    C * rho^2/(rho+sqrt(s))^2
        *|rho-sqrt(s)|^(2 sigma-2) d rho.

Its integral over a fixed bounded radial interval is uniform in `s`. For
`s<0`, use `|G|<=C rho^sigma` and bound by
`C rho^(2 sigma-2)d rho`. Both integrals are finite precisely under the
strict inequality used here, `sigma>1/2`. This checks nearby semicircles,
rather than only the exact threshold. Outside a slightly smaller chart the
usual regular charts or separated denominator estimates apply.

The high-harmonic response multiplier is uniformly bounded, so Parseval
completes the energy norm estimate. The off-axis response equals the
reconstructed response times `detuning/(detuning-i eta)`, of modulus at most
one. Energy dominated convergence identifies its field with the boundary
source field, without interchanging a merely formal principal value with a
nonintegrable kinetic expression.

After `phi=P h` gives the known `C^(1,1/2)` estimate, the Fourier equation
`i omega h=i nu h-i omega w phi` has a square-integrable right hand side.
Indeed `w D phi` is in the energy space by the uniformly bounded orbital
angular derivative. This verifies the generator domain step and gives the
actual eigen-equation. All constants in this construction are local in
frequency for one fixed warmth.

### Asymmetric blocks and the actual leading pole

Put `d=|z-nu_0|`. At a regular resonance the weighted kernel factor is
`g in C^sigma`, `g(0)=0`, while a unit test factor is `f in C^gamma`. For
`r=g(f-f(0))`, both `r(t)=O(|t|)` and

    |r(t)-r(x)|
      <= C[d^gamma |t-x|^sigma+d^sigma |t-x|^gamma]
      (|t|,|x|<=C d)

hold because `sigma+gamma=1`. Local Cauchy subtraction contributes `O(d)`;
the exterior kernel difference contributes `O(d log(1/d))`. The remaining
term `f(0)g` has a `C^sigma` Cauchy transform. This proves the asymmetric
`O(d^sigma)` bound uniformly in the test field.

At a circular threshold the coarea density is `q(s)=O(s)`. For nearby
positive `s,t` its increments satisfy, with `h=|s-t|` and
`0<=s,t<=C d`,

    |q(s)-q(t)| <= C[d^gamma h^sigma+d^sigma h^gamma+h].

This follows by first taking differences in `rho=sqrt(s)` and using
`|sqrt(s)-sqrt(t)|=h/(sqrt(s)+sqrt(t))`; the positive powers of the larger
radius compensate for that denominator. It is the scaled increment bound,
together with `q(s)=O(s)`, that justifies the logarithmic Cauchy estimate.
A pointwise `O(s)` bound alone would not suffice. The upper-closure estimate
follows from the Poisson extension, whose `sigma` moment is finite.

For two kernel factors on a regular chart, `q(t)/t` is
`C^(2 sigma-1)`; on a circular chart it is `C^(sigma-1/2)`, extended by zero
on the absent side. Both exponents are positive. Therefore

    Cq(z)-Cq(0)=z C(q(t)/t)(z)

has a first-order limit with a positive remainder exponent. The exact
crossing matrix is

    ell_a(A'(nu_0)phi_b)
      =sum_(i,k!=0) integral
          w_i omega_ik conjugate(phi_a,ik) phi_b,ik
                         /(omega_ik-nu_0)^2 dm
      =Q[h_a,h_b]/nu_0.

The last identity follows directly from
`h=-w omega phi/(omega-nu_0)` and
`h/w+phi=-nu_0 phi/(omega-nu_0)` in the energy form. Alternatively, pairing
the positive and negative harmonics gives the positive expression printed
in the proof. Their equality is valid here because the turning-point angle
origin makes radial orbital extraction a real signed measure and hence
`phi_-k=phi_k`, also for complex radial fields.

The nonresonant differentiated tail is bounded by Parseval, since its
multiplier is `O(1/|k|)`. Thus it does not spoil the finite-chart estimates.
The concrete cokernel functionals are independent by `P h=phi` and the mode
formula. Both off-diagonal Fredholm blocks change by `O(d^sigma)`, so the
Schur correction is `O(d^(2 sigma))=o(d)`. The Schur matrix consequently has
the stated invertible leading coefficient `Q_Gram/nu_0`. This gives precisely
the displayed inverse norm and residue, including upper-boundary approach.

## Exact remaining gap and strongest safe statement

There is no additional missing implication in the locally uniform kernel
reconstruction, local finiteness, or leading-pole statements under their
listed inputs. The main unresolved implication beyond that claim is:

    actual exceptional mode geometry
      -> bounded receiving detuning quotient
         and sufficiently regular pole-subtracted/reduced boundary inverse.

At a simple fundamental circular threshold a mode can locally have numerator
`phi_1~c sqrt(J)`. Its weighted energy is finite with the actual action
measure, but its receiving quotient can diverge. The two proofs do not claim
an actual self-consistent mode with this behavior, or its exclusion. An
inverse with Schur expansion `d G+O(d^(1+theta))`, `0<theta<1`, can retain an
unbounded `O(d^(theta-1))` term after the leading pole is subtracted. Thus the
strongest safe conclusion remains an ordinary inverse away from locally
finite actual neutral modes, plus the correctly qualified leading pole.

The cheapest further check is the actual circular force-trace/divisibility
condition, or an expansion proving the required reduced inverse estimate.
Global high-frequency decay is a separate analytic obligation assigned
outside this audit.

## Additional source checks, commands, and provenance

Supporting raw source hashes checked:

- `actual_feedback_2026_10_19/SINGULAR_PENCIL_AND_MODES.md`:
  `3c091ca4be949d0bdf3c1657897a962cb7f60b137f03657c23b8af80a25e5c94`.
- `actual_feedback_2026_10_19/GEOMETRY_AND_SCALING.md`:
  `1848347266a2254e18fc579c3c6804cd6703895ce9d298f804a69acd977558c9`.
- `actual_feedback_2026_10_19/SPECTRAL_OPERATOR.md`:
  `52c042ff02f04c0e6917e2591d9527fbf07952ce64b6f674b240f83e4c9fb47c`.
- `cold_dominated_feedback_2026_10_19/GEOMETRY_AND_CAP.md`:
  `c40c5f63e533fe19e41b996e292d21892160bf2b4aa31ffb499313b64f54fc0d`.

These paths are relative to
`real_research/analytic_review_2026_10_18_codex/` in the supplied repository.
The full-feedback `RESULT.md` energy statements and threshold-mode artifact
were read for context. No external literature claim was needed to adjudicate
the new implications; the older energy theorem is retained as a named input.

Operations were `cat`, `rg`, `sed`, `pwd`, existence checks, `shasum -a 256`,
and this report's `apply_patch`. No scientific program, numerical integration,
scientific array, or process inspection/control was used. No ledger or
repository file was changed. No applicable `AGENTS.md` was found along the
audited repository paths. The proof-audit skill and its relevant obligation
checklist were read. The audit is independent of the author's self-review,
but remains a same-model delegated analytic review rather than a formal
proof certificate.
