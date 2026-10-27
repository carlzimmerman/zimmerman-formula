# Independent audit of the conditional reduced inverse

Normalized claim: for the fixed actual positive-warmth cold-dominated halo and
the stated no-full-critical-point/finite-simple-circular-extremum geometry,
let `N=ker(I-K_+(nu_0))`, `nu_0!=0`. If every field in `N` satisfies
`phi_j'(s_c)=0` at every fundamental circular threshold
`|nu_0|=kappa_j(s_c)`, then

    (I-K(z))^-1=R_(nu_0)/(z-nu_0)+B_(nu_0)(z),

on a sufficiently small punctured upper closure, where `B` extends boundedly
and in operator-norm `C^alpha` through `nu_0` on `Y=C^gamma(I)^2`,
`0<gamma<1/2`, for any sufficiently small
`0<alpha<min(gamma,1/2)`, and
`R=nu_0 sum phi_a (Q_Gram^-1)_ab ell_b`.

**Primary verdict: proved as written at the corrected revision below.**
This is a proof of the conditional operator statement. It does not establish
the force condition, absence of actual modes, the global work estimate, or a
uniform estimate as warmth tends to zero. The already established energy,
source-pairing, and actual-geometry inputs are retained as the explicit
theorem hypotheses; their whole antecedent proofs were not re-audited here.
The load-bearing extra square-root regularity was reconstructed from the raw
actual-DF source, rather than inferred from generic nonnegative smoothness.

## Revision and provenance

Independent focused subagent review by `/root/audit_reduced_inverse` on
19 October 2026, directly reading the raw proofs. No repository file was
changed. This report is the only written artifact. No scientific script,
numerical calculation, discretized array, integration program, or process
operation was used. Operations were text reads, textual searches, SHA-256
authentication, analytic reasoning, and writing this report.

The initially supplied raw target had SHA-256
`b7250d27338131815ad2ddf87187152efb35eb332606c7f037a591420970770e`.
It said `nu_0!=0` but displayed CF only when `nu_0=+kappa`, leaving the
negative-frequency fundamental uncovered. I reported that exact restriction.
The author subsequently changed the display to `|nu_0|=kappa` and explicitly
named `k=+1,-1`; I reread and reauthenticated the full corrected artifact.
The positive-frequency derivation and its conjugate now cover the advertised
nonzero-frequency scope. This report gives no pass to the earlier literal
all-nonzero-frequency statement.

Final target:

- `real_research/analytic_review_2026_10_18_codex/cold_dominated_feedback_2026_10_19/REDUCED_INVERSE.md`
- SHA-256: `ebc588cbd3fef36295dc355542f5b5344327c6ed1d76af12e777ee36786e93d1`

All relative paths in this report are relative to
`/Users/carlzimmerman/new_physics/zimmerman-formula`.
The proof-audit skill and relevant general/type obligations were read.
No project `AGENTS.md` or `.mathbox` ledger was found by the repository text
inventory used for this focused audit.

## Claim card and dependency graph

The coefficient domain is complex; the source space is the continuous
anti-dual `Y^x`. Source forms are conjugate-linear in their first field and
linear in their second. The species order and actual reciprocal shell
matrix are those in `BOUNDARY_PAIRING.md`; no scalar or positive-shell-matrix
substitution is made. Frequencies have the convention `omega_ik=k Omega_i`.
The actual energy Gram matrix is coercively positive; it is not the shell
matrix. The complete harmonic sum excludes `k=0`. All bounds concern one
fixed strictly positive warmth and a neighborhood of one fixed nonzero mode.

The dependency chain is:

1. Actual reciprocal source theorem + `P:Y^x->Y` smoothing + no full action
   critical point -> compact, locally Holder field pencil and its Fredholm
   complements. [Named internal theorem input.]
2. Weighted energy reconstruction in `REGULAR_INVERSE.md` -> every field in
   `N` is a genuine energy eigenfield and the cokernel is spanned by `ell_a`.
   [Named internal theorem input.]
3. `THRESHOLD_MODES.md` density bootstrap with the cap/endpoint facts in
   `GEOMETRY_AND_CAP.md` -> kernel fields are radial `C^(1,1)`, hence their
   coefficients are `C^(1,1)` in eccentric actions or circular `(a,L)`.
   [Named internal theorem input; its cap contract is supplied for the stated
   actual family.]
4. Quantitative actual-DF estimates in `EXACT_SMOOTH_INVERSE.md` ->
   `sqrt(w)` has bounded first two derivatives in the required charts and
   flat cap/L-end extensions. [Reconstructed below.]
5. Optical zeros + 3 and 4 -> weighted Hadamard division on every regular
   chart. CF + 3 -> zero first jet on every resonant circular threshold.
   [Internal analytic implications checked below.]
6. Regular and threshold pushforwards -> complete off-diagonal blocks
   `delta B_01,delta B_10`, and kernel/cokernel block
   `delta M+delta^2 C_00`, with Holder coefficient maps.
   [Internal analytic implications checked below.]
7. Positive energy crossing `M=Q_Gram/nu_0` + invertible complementary block
   -> Schur inversion and the asserted bounded Holder remainder.
   [Internal algebra checked below.]

There is no dependency from the desired reduced inverse back into the energy
bootstrap or source theorem in this chain. CF is an explicit unchecked
assumption about actual eigenfields, not a consequence of energy membership.

## Obligation matrix

| Obligation | Status | Reason |
| --- | --- | --- |
| Frequency/sign scope, including `k=-1` | passed after the recorded correction | Final CF uses `abs(nu_0)` and names both fundamentals. |
| Actual energy reconstruction and cokernel | conditional on the named internal input | Used exactly as proved in `REGULAR_INVERSE.md`; no unrestricted energy resolvent estimate is inferred. |
| Kernel radial/action `C^(1,1)` | conditional on the named geometric/bootstrap inputs | The selected actual family supplies the separately named cap/endpoint contract. |
| `sqrt(w)` `C^2` and cap/L-end corners | passed | Uses quantitative relative derivative bounds, positivity, and explicit exponential baseline; generic `w>=0,C^2` is insufficient. |
| Regular weighted Hadamard division | passed | Complete weighted resonance zero and Lipschitz first derivative give a Lipschitz quotient. |
| Regular circular crossing and zero boundary value | passed | Divide with fixed `a` in `L`; the quotient vanishes at `a=0`. |
| Threshold cross quotient | passed | `q_cross/s` has zero-extended `C^gamma` bounds, uniformly in arbitrary test fields. |
| Threshold kernel/kernel quotient | passed | `q_00/s^2` has zero-extended `C^(1/2)` bounds. |
| Complete blocks rather than a local scalar surrogate | passed | Cokernel pairing gives one kernel factor; source duality and `P` control the other block; finite charts and Parseval complete the sum. |
| Crossing matrix and residue | conditional on the named exact crossing input, algebra passed | `M=Q_Gram/nu_0`; it is invertible even when `nu_0<0`. |
| Schur subtraction and all inverse blocks | passed | Every off-diagonal block has a factor `delta`; the finite-dimensional Schur remainder is bounded Holder. |
| CF for actual modes | not addressed | It remains the explicit hypothesis. |
| Smooth-source transform, receiving-harmonic work summation | out of scope | The target explicitly leaves these separate. |
| Global high-frequency finiteness | out of scope | It is a separately named input and is unnecessary for this local conclusion. |

## Decisive regularity checks

### The actual square root, including joint corners

Use `s=s(L)`, `y=x(s)`, `h=h(s)`, `u(y)=mu(s)`, and the source's
`t=(E-E_c)/(kappa(s)^2 h(s)^2)`. Directly from the actual DF definition,

    w=-F_E=(-H_t(t,y))/(D(s) h(s)^4),
    D(s)=C L_c'(s) kappa(s)^3 Z.

`D` is smooth and bounded above and below by positive constants. The fixed
warmth is denoted `delta_w` here to distinguish it from the spectral
increment. On `0<=t<=delta_w^2/4`, the source's relative error estimate and
positivity proof give `-H_t>=c u`, where fixed powers of `delta_w` are included
in `c`. Every fixed mixed `(t,y)` derivative of `H_t` is bounded by `C u`.
The smooth action-energy change and `dy/ds=1/h` introduce only finite inverse
powers of `h` and endpoint distance. Thus, for derivative order up to two,
`w` has upper derivative bounds of the form `C u` times such finite powers,
and its positive lower bound is `c u h^-4`.

Apply the exact identities

    D_i sqrt(w)=D_i w/(2 sqrt(w)),
    D_i D_j sqrt(w)=D_i D_j w/(2 sqrt(w))
                    -(D_i w D_j w)/(4 w^(3/2)).

Their right sides are bounded by `C sqrt(u)` times finite inverse powers of
`h` and endpoint distance. The exact edge estimates are exponential, not
merely arbitrary flatness: `u` is comparable to `d^-2 exp(-D_-/d)` at the
inner end and `exp(-D_+/d)` at the outer end, with positive constants.
Consequently these bounds tend to zero at either end. This proves the
required flat extension, including derivative control, on the region where
the correction is present. It also explains why a generic assertion about a
nonnegative `C^2` weight would not suffice: it gives only a Lipschitz square
root in general.

Above `delta_w^2/4` the correction vanishes identically. Put
`tau=1-t/delta_w^2`. Up to fixed smooth positive factors the actual baseline
has

    sqrt(w)=sqrt(u) h^-2 tau^-1 exp(-1/(2 tau)), tau>0.

Every needed physical/action derivative adds only finite inverse powers of
`h`, endpoint distance, and `tau`. The product of the endpoint exponential
and `exp(-1/(2 tau))` dominates these powers jointly. It therefore also
controls a sequence approaching an L end and the top cap simultaneously;
separate one-boundary estimates are not being substituted for this corner
check. The correction is smoothly zero at the interface with the baseline
region. The same argument gives the required regularity in `(a,L)` after
`J=a^2`. Only physical `a>=0` is used; no monotonicity of the arbitrary
inaccessible negative-`t` extension is assumed.

These are consequences of the actual DF's quantitative estimates in its
sections “Exact density with positivity and monotonicity” and “Removal of
the ridge and exact self consistency.” They establish the square-root input
needed by the target. No additional weight regularity hypothesis is missing.

### Regular weighted division

On an eccentric submersion chart let `t=omega-nu_0`. The extended coefficient
`G=sqrt(w) phi_k` is `C^(1,1)` and is zero on the whole `t=0` chart slice:
optical zeros give this in positive weight, and the weight gives it outside
support. Hence

    G(t,y)=t v(t,y),
    v(t,y)=integral_0^1 partial_t G(lambda t,y) d lambda.

The quotient is uniformly Lipschitz. This argument crosses a cap using the
weighted extension and never presumes an unweighted optical zero on an
exterior resonance.

At a regular circular crossing solve for `L` with `a` fixed. The same formula
gives `v` Lipschitz in `(a,t)`. Since `G(0,L)=0` for every `L`, the quotient
vanishes at `a=0` (including the resonance value by continuity). A cross
quotient is a product of `v` with a `C^gamma` test coefficient, times smooth
factors. The coarea integral in this chart runs over fixed `a>=0` with the
bounded measure factor from `dJ=2a da`, so its frequency density is
`C^gamma`. For two kernel fields, both coefficients divide and the quotient
density is Lipschitz. This requires no false `C^(1,1)` assertion for a single
orbital coefficient in the ordinary variable `J` at zero.

In the exact source cross form, the second `sqrt(w)` and the factor `omega`
must be retained: one may include the former in the test coefficient and the
latter in the smooth coarea factor. The displayed schematic cross density
in the target suppresses these smooth factors; retaining them preserves all
the stated estimates. At the interior circular threshold `w` is smooth and
positive. At regular support charts the square-root check above supplies
the same conclusion. No unbounded source factor is suppressed.

### Circular coarea quotients

The exact boundary-preserving chart gives `t=epsilon rho^2`,
`dJ dL=b c(b^2,x) db dx`. CF for `k=+1,-1`, and the oscillator expansion for
`abs(k)>=2`, make every resonant kernel coefficient satisfy

    g=O(rho^2),   |grad g|<=C rho.

These bounds follow from its zero first jet and `C^(1,1)` regularity. Put
`rho=sqrt(s)`. With `f=O(rho^gamma)` and `f` uniformly `C^gamma`,

    q_cross(s)/s = integral sin(theta) (g/rho) f c dtheta.

`g/rho=O(rho)` and is uniformly Lipschitz along each fixed ray. If
`h=|s-t|<=s/2`, then `|sqrt(s)-sqrt(t)|<=C h/rho`. The two product
increments are bounded by

    C rho^(1-gamma) h^gamma,
    C h rho^(gamma-1),

respectively; both are `O(h^gamma)` on the fixed chart. For `h>s/2` both
arguments are `O(h)`, and the value bound
`q_cross(s)/s=O(s^((1+gamma)/2))` proves the same estimate because
`(1+gamma)/2>gamma`. The zero extension to the unoccupied side is therefore
`C^gamma`, including at zero.

For two kernel fields the quotient integrand is

    g_a^* g_b/rho^3.

It is `O(rho)`. Its radial derivative is bounded because
`g=O(rho^2)` and `partial_rho g=O(rho)`: differentiating the product gives
`O(rho^3)/rho^3`, and differentiating `rho^-3` gives
`O(rho^4)/rho^4`. The smooth coarea factors obey the same bound. It is thus
Lipschitz in `rho`, and composition with `sqrt(s)` proves zero-extended
`C^(1/2)` for `q_00/s^2`. Angular integration is over the fixed compact
half-circle and does not alter these uniform estimates.

## Complete operator blocks and Schur remainder

The compactly supported density identities in target equation (2) are exact
algebraic identities with the same boundary convention. In particular the
second coefficient is the Cauchy transform of `q/t^2`, rather than an
uncontrolled second derivative of `K` on arbitrary Holder fields. The
regular and threshold quotient estimates give bounded operator-norm Holder
Cauchy transforms (using any smaller positive exponent than the density
exponent). Partitions and finitely many resonant harmonic charts preserve
the estimates.

For all sufficiently large `abs(k)`, detuning is uniformly separated and
the first and second multiplier derivatives are `O(1/abs(k))` and
`O(1/k^2)`. At each orbit, Parseval and Cauchy--Schwarz bound
`sum abs(phi_k psi_k)` by the two orbital `L^2` norms. Integration against
the finite susceptibility measure proves the required complete dual-norm
sum. The tail is analytic on the common local disk, with the required
derivatives; it cannot add a hidden singular off-diagonal or kernel block.

The cokernel functionals are the actual `ell_a(f)=integral conjugate(h_a) f`.
Reciprocity gives

    ell_a(A(z)f)=-<phi_a,(T(z)-T_+(nu_0))f>.

Thus the cokernel/complement block indeed has a kernel field on one side;
the kernel-to-complement block is controlled by
`P(T(z)-T_+(nu_0))phi_b` in the complete source dual norm. These facts justify
both `A_01=delta B_01` and `A_10=delta B_10`, not merely their scalar
pairing against a fixed test. Two kernel factors give
`A_00=delta M+delta^2 C_00`. The exact energy crossing input identifies
`M=Q_Gram/nu_0`. Fixed Fredholm complements make `A_11(0)` a bounded
isomorphism; local Holder continuity gives a bounded Holder inverse.

With `D(z)=M+delta C(z)` and
`C=C_00-B_01 A_11^-1 B_10`, finite-dimensional inversion gives the exact
identity

    S^-1=delta^-1 M^-1-M^-1 C(z) D(z)^-1.

The second term is bounded `C^alpha` through zero. The top-right and
bottom-left inverse blocks have respectively the forms
`-D^-1 B_01 A_11^-1` and `-A_11^-1 B_10 D^-1`; the bottom-right correction
is `delta A_11^-1 B_10 D^-1 B_01 A_11^-1`. All are bounded Holder.
Consequently subtracting the stated residue removes the sole pole of the
full inverse on `Y`. No commutation of the matrices in this calculation is
used. The residue is independent of the chosen fixed complements and has
exactly the normalization already identified by the energy crossing.

## Remaining gap, safe statement, and next check

There is no remaining local analytic gap in this corrected conditional
reduced-inverse implication under its stated actual-geometry and source
inputs. In particular the generic-square-root concern is resolved for the
specific DF rather than left as an extra unproved regularity assumption.

The strongest safe statement is precisely the conditional operator theorem
at the top of this report. The missing physical/spectral implication is
still whether every actual fundamental circular eigenfield has zero radial
force at its resonant stationary circle. This audit supplies neither that
implication nor a counterexample. The next mathematical check for a work
theorem must also retain the separate smooth-source transform and receiving
harmonic summation requirements; they do not follow merely from this local
operator expansion.

## Source authentication and verification record

Raw sources read, SHA-256 at audit:

- `cold_dominated_feedback_2026_10_19/BOUNDARY_PAIRING.md`:
  `5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d`.
- `cold_dominated_feedback_2026_10_19/REGULAR_INVERSE.md`:
  `4830712683b98b46a53b796b4bde109c618a4fd26fa910cd47176ebe9f3ddf80`.
- `cold_dominated_feedback_2026_10_19/THRESHOLD_MODES.md`:
  `40304ae8d1c0495cdd7482202aa9dcdfa494f12287754b7e648dd2adf26a77b5`.
- `cold_dominated_feedback_2026_10_19/GEOMETRY_AND_CAP.md`:
  `c40c5f63e533fe19e41b996e292d21892160bf2b4aa31ffb499313b64f54fc0d`.
- `smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`:
  `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.

These source paths have prefix
`real_research/analytic_review_2026_10_18_codex/`.
The target was read fully at both recorded hashes. Commands used were `cat`,
`rg`/`rg --files`, `pwd`, `shasum -a 256`, and the text patch operation that
wrote this file. No external mathematical citation or load-bearing
computation is used by this focused implication; no scientific verification
command was run.
