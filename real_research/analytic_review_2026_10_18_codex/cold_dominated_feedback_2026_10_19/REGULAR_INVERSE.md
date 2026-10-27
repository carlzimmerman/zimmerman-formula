# Actual boundary inverse: uniform energy reconstruction and discrete exceptions

19 October 2026. Author `/root/cold_inverse`. Supplied ancestry checkpoint:
`915b108f82629d3e794a6a3a3b6ad5e793355172`. Repository HEAD observed while
reading was `bcba9fc597769b1cd1d838168b909b9a7c9e2677`; no repository file was
modified. Analytic text and metadata operations only: no scientific script,
numerical integration, discretized scientific array, or process operation.

## 1. Exact result and limits

The actual fixed-positive-warmth problem admits the following new
nonperturbative implication. Under the complete boundary-source theorem in
`/private/tmp/boundary_pairing_20261019.md`, with no eccentric frequency
critical points and only finitely many simple circular epicyclic extrema,
every actual boundary kernel is a genuine energy eigenfield. The boundary
kernel frequencies are **locally finite**. Consequently the actual compact
field pencil has a continuous, bounded boundary inverse on every compact set
which avoids those actual eigenfrequencies. This applies to the actual
cold-mass-dominated subfamily constructed in Section 9 of that source; it
does not use the earlier baryon-dominated small-susceptibility family.

The proof closes a real reconstruction issue at circular thresholds, including
flat cap intersections. It does not prove that the exceptional set is empty.
It also does not prove a bounded inverse after subtracting the leading pole
at a circular threshold. The additional local Schur analysis below proves a
simple leading pole and an inverse bound of order `1/|z-nu_0|`, while allowing
an unbounded subleading threshold branch. Thus the requested full work theorem
on the entire closed receiving set is still open.

If the separate high-frequency assertion `||K_+(nu)|| -> 0` is established,
the locally finite exceptional set is finite. That decay is not supplied by
the compact-frequency source-duality theorem and is not assumed silently.

Primary proof status: **conditional on the named complete boundary-source
theorem and the explicitly listed actual geometry**. All implications after
those inputs are derived here. Self-review only; no independent certificate.

## 2. Inputs and theorem contract

Use the actual equilibrium, actual shell matrix `P`, energy Hilbert space
`(H,Q)`, and selfadjoint operator `H_lin=i L` from the full-feedback source.
Write `A_energy[h]=sum_i integral |h_i|^2/w_i dGamma`. The actual energy is
equivalent to `A_energy`, and

    P:H -> C^(1,1/2)(I)^2

is bounded, hence compact into `Y=C^gamma(I)^2`, `0<gamma<1/2`. Put
`sigma=1-gamma>1/2`. No positive definiteness of the shell matrix is imposed.

For the fixed actual halo assume:

* Its occupied action sets are compact nondegenerate-well tubes with a smooth
  orbit map in `(a,L)`, `a=sqrt(J)`, and a common positive frequency lower
  bound. The nonnegative susceptibility `w` is smoothly zero-extended across
  the energy cap and the angular momentum ends.
* `grad_(J,L) Omega != 0` on the closed occupied set. At a circular point
  where `Omega_L=0`, the epicyclic extremum is simple; equivalently
  `Omega_LL != 0`, and the actual twist identity gives
  `Omega_J=kappa''/(4*kappa) != 0`, with `Omega_J` and `Omega_LL` having the
  same sign. There are finitely many such circular points.
* On each compact frequency interval, the complete upper source map
  `T_+(nu):Y -> Y^x` is bounded and continuous in operator norm, has the
  reciprocal optical form, and

      K_+(nu)=P T_+(nu):Y -> C^sigma

  is locally uniformly bounded and continuous. Its upper half-plane version
  has the same boundary limit. These are precisely the no-eccentric-critical
  specialization of the named boundary-pairing artifact, not a new spectral
  assumption or an assumed inverse.

Here `Y^x` is the continuous anti-dual. For `Im z>0`,

    <psi,T(z)phi>
      =-sum_i sum_(k!=0) integral w_i*omega_ik/(omega_ik-z)
                          *conjugate(psi_ik)*phi_ik dm,
    omega_ik=k Omega_i,   dm=2*pi*C_Gamma dJ dL.

The existing actual off-axis inverse follows from the conserved coercive
energy. The source theorem proves compactness of `K_+` on `Y`. In Section 9
of its artifact it also supplies a nonempty actual cold-dominated family
with the geometry just listed. All constants below may depend on the one
fixed positive warmth and on that selected member; no uniform cold-limit
assertion is made.

## 3. Optical zeros and a weighted Holder source

It suffices below to take `nu>0`; the negative half-axis follows by the
real-coefficient symmetry. Let `phi=K_+(nu)phi`. Set `S=T_+(nu)phi`, so `phi=P S`.
Actual reciprocity gives `<P S,S>` real. The optical identity therefore gives

    w_i(q)*|phi_ik(q)|^2=0
    whenever omega_ik(q)=nu

on every regular interior resonance. By continuity, the weighted product
also vanishes on its closure. At a point outside the occupied set the product
vanishes because `w=0`; at `a=0` every nonzero radial orbital harmonic is zero.
Thus the globally zero-extended weighted numerator has a zero at every
resonance point in the coordinate domains used below.

A useful elementary fact is that the square root of a nonnegative `C^2`
function is locally Lipschitz, with a bound depending on its `C^2` norm.
Indeed Taylor's inequality in the negative gradient direction gives
`|grad w|^2 <= C w` on a slightly smaller compact chart; integrating the
bound on `grad sqrt(w)` proves the assertion, including through zeros.
One may use the smooth extension to a slightly larger action chart required
by the source theorem. Consequently

    G_ik(a,L)=sqrt(w_i(a^2,L))*phi_ik(a,L)

is `C^sigma` in `(a,L)`, with norm at most `C||phi||C^sigma`. It vanishes at
`a=0`, and is zero on every potentially resonant level. A kernel satisfies

    ||phi||C^sigma <= C ||phi||Y

locally uniformly in `nu`, by the already proved source-to-field smoothing.
No Lipschitz estimate for an arbitrary source boundary field is used.

## 4. Uniform energy reconstruction at regular levels

On a chart away from circular stationary points use a smooth coordinate
`t=omega_ik`, with a complementary coordinate `y`. Away from `J=0` these are
ordinary action charts. At a circular point with `Omega_L != 0`, keep `a`
and solve for `L`; then `dJ dL=2a da dL` and the measure density is bounded.
The numerator `G(t,y)` is `C^sigma`, uniformly, and `G(nu,y)=0`. Hence

    |G(t,y)/(t-nu)| <= C ||phi||C^sigma |t-nu|^(sigma-1).

The square is uniformly integrable because `2*sigma-2>-1`. The same argument
works when the resonant point lies outside the actual support: there
`sqrt(w)=0`, so the zero required for subtraction remains valid. This is why
a flat cap needs no unjustified unweighted division estimate for energy
membership.

## 5. Exact half-plane Morse chart at a circular stationary point

Let `(0,L_c)` be a simple circular extremum, `omega_c=k Omega(0,L_c)` with
`k>0`, and let `epsilon=sign omega_J=sign omega_LL`. Put `a=sqrt(J)`. Define

    x=sign(L-L_c)*sqrt(epsilon*(omega(0,L)-omega_c)),
    b=a*sqrt(epsilon*(omega(a^2,L)-omega(0,L))/a^2).

At `a=0` interpret the second quotient by its smooth positive extension.
These are smooth local coordinates on the half-plane `a>=0`, because the
circular extremum is nondegenerate and `omega_J != 0`. Exactly, not only to
leading order,

    omega-omega_c=epsilon*(b^2+x^2),
    dJ dL=b*c(b^2,x) db dx,

where `c` is smooth, positive, and bounded above and below on a sufficiently
small fixed chart. The transformed `G` is `C^sigma`, is `O(b^sigma)`, and
vanishes on every resonant semicircle lying in the chart.

Write `rho=sqrt(b^2+x^2)` and `s=epsilon*(nu-omega_c)`. For `s>=0`, the
point at radius `sqrt(s)` on the same half-ray is resonant. The Holder zero
there yields

    |G| <= C ||phi||C^sigma |rho-sqrt(s)|^sigma.

Thus the squared quotient has, after angular integration, the majorant

    C ||phi||C^sigma^2
      *rho^2*|rho-sqrt(s)|^(2*sigma-2)/(rho+sqrt(s))^2 d rho
    <= C ||phi||C^sigma^2 |rho-sqrt(s)|^(2*sigma-2) d rho.

Its integral on a fixed radial interval is bounded uniformly in `s>=0`.
At `s=0`, use `G=O(b^sigma)` directly; the same integrability follows.
For `s<0`, there is no local resonance, and

    integral |G|^2/(rho^2+|s|)^2 *b db dx
       <= C ||phi||C^sigma^2
             integral rho^(2+2*sigma)/(rho^2+|s|)^2 d rho
       <= C ||phi||C^sigma^2 integral rho^(2*sigma-2) d rho.

This is again finite uniformly as `s` approaches zero. The chart is taken
slightly larger than the region being estimated, so all required resonant
semicircles remain in the chart. Weight zero extension handles portions
outside the occupied tube.

## 6. Boundary kernels are genuine modes, uniformly

Define, almost everywhere,

    h_nu,ik=-w_i*omega_ik*phi_ik/(omega_ik-nu),
    h_nu,i0=0.

Only finitely many harmonics can resonate near a fixed compact frequency
interval. The estimates in Sections 4--5 control those harmonics uniformly.
For all remaining harmonics `|omega_ik/(omega_ik-nu)|<=C`; Parseval gives
their energy bound. Therefore, locally uniformly in real `nu`,

    ||h_nu||Q <= C ||phi||C^sigma <= C ||phi||Y.       (6.1)

This is the crucial bound on **kernel elements**, not a false boundary bound
for the unrestricted energy resolvent.

For fixed `phi`, the upper source reconstructed at `nu+i eta` equals
`h_nu,ik*(omega_ik-nu)/(omega_ik-nu-i eta)`. The multiplier is bounded by one
and converges almost everywhere to one. Energy dominated convergence gives
`h(nu+i eta)->h_nu` in `H`. Hence `P h_nu=K_+(nu)phi=phi`.

Now the actual energy-to-field estimate upgrades `phi` to `C^(1,1/2)`.
Its angular derivative is square integrable uniformly over the compact
orbital family. The Fourier reconstruction then gives `h_nu in Dom(L)` and
the mode equation `L h_nu=-i nu h_nu`. Conversely any energy eigenmode has
this same Fourier formula, and the preceding dominated convergence shows
its field is a boundary kernel element. Thus kernels and energy eigenfields
coincide, including these circular thresholds.

The existing zero-mode exclusion handles `nu=0` separately.

## 7. Local finiteness and the regular boundary inverse off the modes

Suppose distinct boundary kernel frequencies `nu_j` tend to a finite `nu_0`.
Choose kernel fields with `||phi_j||Y=1`, and reconstruct `h_j` by Section 6.
They are bounded in `Q` by (6.1). Since `H_lin` is selfadjoint, eigenvectors
at distinct frequencies are `Q`-orthogonal. A bounded orthogonal sequence
converges weakly to zero: normalize its nonzero elements and apply Bessel's
inequality. Compactness of `P:H->Y` therefore implies `phi_j=P h_j -> 0` in
`Y`, contradicting their normalization. No finite accumulation is possible.

The singular set is also closed locally: norm continuity and Fredholm index
zero make the invertibility set open. Therefore it is a locally finite
closed subset of the real axis. On its complement the Fredholm alternative
gives the ordinary actual inverse. The inverse is continuous there by the
resolvent identity, so is uniformly bounded on compact subsets avoiding the
singular set. The corresponding upper-closure inverse has the same property
by the known off-axis injectivity and norm boundary continuity.

This proves a genuine regular boundary inverse away from a discrete set of
**actual** neutral modes. Neither a hypothetical positive shell matrix nor
an assumed no-mode condition enters the argument. If high-frequency decay
of `K_+` is separately proved, there are no large-frequency exceptions and
the exceptional set is finite globally.

## 8. A sharper local statement: nondegenerate leading poles

This section uses the complete reciprocal source pairing, in addition to the
preceding reconstruction. Let `nu_0 != 0` be one exceptional frequency and
choose a basis `phi_a=P h_a` of its kernel, with the matching energy modes.
The bounded functionals

    ell_a(f)=sum_i integral conjugate(h_a,i)*f_i(r) dGamma

span the cokernel of `A_0=I-K_+(nu_0)`. They annihilate its range by the
reciprocity of `P` and `T_+`. They are independent: if their linear combination
were zero on all radial fields, the corresponding mode would have zero
radial shell densities, hence zero potential and then zero mode. Fredholm
index zero supplies the dimension count.

Here is the asymmetric Cauchy estimate needed to control frequency coupling.
On a regular resonance chart, let `g in C^sigma`, `g(0)=0`, and
`f in C^gamma`. The density of a kernel/test pairing has this form, with
smooth factors absorbed. Split

    g(t)f(t)=f(0)g(t)+g(t)*(f(t)-f(0)).

The Cauchy transform of the first term is `C^sigma`. For the remainder `r`,
`r(t)=O(|t|^(sigma+gamma))`. On `|t|,|x|<=C d`,

    |r(t)-r(x)| <= C[d^gamma*|t-x|^sigma
                         +d^sigma*|t-x|^gamma].

Subtract at `x`, integrate the local Cauchy kernel, and use the exterior
kernel difference `O(d/t^2)`. Since `sigma+gamma=1`, this gives a remainder
`O(d*(1+|log d|))`, which is `O(d^sigma)`. Consequently the whole Cauchy
transform differs from its value at zero by `O(d^sigma)`, uniformly in the
unit `C^gamma` test field. The same estimate holds in the upper closure by
the Poisson representation.

At a circular threshold the coarea density has the form

    q(s)=sqrt(s)*integral_0^pi sin(theta)
             g(sqrt(s) sin(theta),sqrt(s) cos(theta))
             f(sqrt(s) sin(theta),sqrt(s) cos(theta)) c(...) dtheta,

on its one-sided support. Since the two harmonics vanish like `b^sigma` and
`b^gamma`, respectively, `q(s)=O(s)`. Its local increments obey the same
two scaled Holder bounds as the preceding remainder, plus an `O(|s-t|)`
term from the smooth coefficient. The identical Cauchy split gives
`O(d*(1+|log d|))`, hence `O(d^beta)` for every `beta<1`.
Thus both kernel-to-complement and complement-to-cokernel frequency blocks
are `O(d^sigma)`.

Only finitely many harmonics are resonant on this local frequency interval.
The remaining source tail has locally bounded analytic frequency derivatives:
the differentiated multiplier is `O(1/|k|)`, and Parseval with
Cauchy--Schwarz bounds its full bilinear sum. Thus it does not reduce any of
the local exponents in this section.

For two kernel fields the regular-chart density is a product of two
`C^sigma` functions both zero at the resonance. Dividing that density by
`t` gives a `C^(2*sigma-1)` function. At a circular threshold its density is
`O(s^(sigma+1/2))`, and division by `s` is `C^(sigma-1/2)`. These statements
follow by the same local increment estimate, splitting increments smaller
and larger than the distance to zero. The identity

    Cq(z)-Cq(0)=z*C(q(t)/t)(z)

therefore proves a first derivative for the kernel/cokernel block, with a
positive remainder exponent. Pairing the positive and negative radial
harmonics gives the exact crossing identity

    ell_a(A'(nu_0)phi_b)=Q[h_a,h_b]/nu_0.              (8.1)

For clarity, with `omega=k Omega>0`, the actual mode formula gives

    Q[h_a,h_b]
      =4*nu_0^2*sum_i sum_(k>0) integral
          w_i*omega^2*conjugate(phi_a,ik)*phi_b,ik
                              /(omega^2-nu_0^2)^2 dm,

whereas the paired derivative of `T` is `-1/nu_0` times this expression.
No indefinite field pairing is being declared positive: the positivity in
(8.1) is exactly the already established coercive kinetic-plus-field energy.

Choose fixed Fredholm complements at `nu_0`. The complementary block remains
invertible by continuity. Its Schur correction to the kernel block is
`O(d^(2*sigma))=o(d)`. The remaining finite-dimensional matrix is therefore

    (z-nu_0)*(Q_Gram/nu_0)+o(|z-nu_0|).

The Gram matrix is positive definite. Hence, in a sufficiently small
punctured upper-closure neighborhood,

    ||(I-K(z))^-1|| <= C/|z-nu_0|,
    (z-nu_0)*(I-K(z))^-1
       -> nu_0*sum_(a,b) phi_a*(Q_Gram^-1)_ab*ell_b.

This conclusion also reproves local isolation. It is a simple **leading**
pole statement. It does not assert that subtracting this rank-finite pole
leaves a bounded function. A Schur remainder of order
`(z-nu_0)^(1+theta)`, `0<theta<1`, can leave a pole-subtracted term of order
`|z-nu_0|^(theta-1)`. The potential circular threshold branch is precisely
where further mode divisibility or a stronger expansion is needed.

## 9. Remaining obstruction and falsification checks

The actual shell matrix has negative determinant. Neither the optical zero
nor the coercive energy forbids a nonzero circular-threshold force trace.
In the exact chart a radial Lipschitz field can have
`phi_1~c b`; then at the threshold the energy integral contains
`b^2/(b^2+x^2)^2` with measure `b db dx`, which is finite, while the receiving
quotient `b/(b^2+x^2)` is unbounded. This is a local admissible asymptotic,
not an actual self-consistent eigenmode construction. The inverse result
above proves that such a threshold response, if present in the actual
kernel, is a genuine energy mode; it does not exclude it.

Executed routes and exact outcomes:

1. Small cold-dominant scaling does not supply a small susceptibility. It
   was not reused from the earlier baryon-dominated proof.
2. Direct radial shell unique continuation does not follow from the optical
   trace zero: that zero is an orbital integral constraint, not a pointwise
   zero of the potential. No unsupported shell sign argument was used.
3. Uniform weighted reconstruction succeeds and excludes accumulations of
   actual neutral modes. Reciprocal Schur analysis yields a nondegenerate
   leading pole at every remaining mode under the stated geometry.

What remains for an everywhere regular inverse or the desired whole-set work
bound is to exclude the actual exceptional modes, or to prove sufficient
receiving divisibility and a bounded, suitably Dini-continuous reduced
frequency inverse at each one. The leading-pole result alone does not meet
that obligation. Uniform high-frequency decay is a separate global leaf.

## 10. Source authentication and review

Read sources, SHA-256 at reading:

* `actual_feedback_2026_10_19/CONTINUATION.md`:
  `3ec0ba51d22f172a31a771ec197678a25cd1a49f013c8cfe09a82d3457d63f81`.
* `actual_feedback_2026_10_19/GEOMETRY_AND_SCALING.md`:
  `1848347266a2254e18fc579c3c6804cd6703895ce9d298f804a69acd977558c9`.
* `actual_feedback_2026_10_19/SPECTRAL_OPERATOR.md`:
  `52c042ff02f04c0e6917e2591d9527fbf07952ce64b6f674b240f83e4c9fb47c`.
* `claude_continuation_2026_10_19/full_feedback/RESULT.md`:
  `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
* `/private/tmp/boundary_pairing_20261019.md`:
  `5b5f2f73d54b034fa014b6efbeeb9acb5cadd9a30f2f40340745569610bba23d`.

Repository-relative sources are under
`real_research/analytic_review_2026_10_18_codex/`. No external mathematical
source or novelty claim is used. Research-program and proof-audit skill
instructions were read; no scientific verification computation was run.
The geometry, complete source duality, reciprocal shell extension, and the
original energy theorem are named inputs. The reconstruction, orthogonality,
and local Schur implications are new derivations here, self-reviewed.
