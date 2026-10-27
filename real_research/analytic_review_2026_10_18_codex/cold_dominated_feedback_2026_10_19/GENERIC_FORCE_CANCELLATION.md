# Exact density-null perturbations remove bad circular force traces generically

19 October 2026. Author `/root/cold_inverse`. Continuation of the frozen
inverse artifact, whose SHA-256 remains
`4830712683b98b46a53b796b4bde109c618a4fd26fa910cd47176ebe9f3ddf80`.
Only this new temporary file is written. Analytic text and source metadata
only; no scientific script, numerical integration, scientific array, or
process operation. The argument below is a new derivation and is **pending
independent audit**.

## 1. Result and exact meaning

Fix the actual two-species density, masses, potentials, radii, and a sufficiently
narrow strictly positive warmth in the cold-dominated family already proved
in `cold_dominated_feedback_2026_10_19/GEOMETRY_AND_CAP.md`. Fix one actual
smooth exact distribution supplied by `EXACT_SMOOTH_INVERSE.md`.

There is an arbitrarily small, smooth, exactly density-preserving change of
its distribution functions, within their existing low-energy correction
region, for which every actual eigenmode satisfies the circular fundamental
force-trace condition

    phi_j'(s_c)=0 whenever nu=kappa_j(s_c), kappa_j'(s_c)=0.       (CF)

More precisely an open dense subset of the admissible exact-density parameter
space constructed below has this property. No numerical choice, perturbative
small cold mass, or positive shell-field quadratic form is used. This is an
existence/genericity statement within the free exact-DF choices; it is not an
assertion that an independently fixed unperturbed DF already satisfies (CF).

The essential new claim is scalar transversality: for any actual energy mode
with a nonzero force trace at a simple circular fundamental threshold, some
admissible exact-density-null variation has a nonzero first variation of its
kernel/cokernel quadratic form. A local blow-up proves this claim. Finite
Fredholm nullity then supplies generic (CF), without a matrix-surjectivity
assumption.

## 2. The exact admissible parameter space

The construction is specieswise in its fixed actual target potential. Use the
notation of `EXACT_SMOOTH_INVERSE.md`:

    F_H(E,L)=H(t,y)/[C_Gamma L_c'(s) kappa(s) h(s)^2 Z],
    t=(E-E_c(L))/[kappa(s)^2 h(s)^2],  y=x(s),
    mu_F(r(x))=A_den H(x),  u(x)=mu_target(r(x)).

The exact source proof constructs

    A_den R_delta=I+E_delta,
    B_den=R_delta (I+E_delta)^(-1),
    A_den B_den=I.                                          (2.1)

This is an actual right inverse for arbitrary signed weighted targets, not
only for the one baseline residual. Write `X_infty=intersection_(m>=5) X_m`
with its weighted Sobolev Frechet topology. The proof's one-derivative gain
for `E_delta` makes `(I+E_delta)^(-1)` continuous on `X_infty`: use its bounded
inverse on `X_5`, then induct on `q=e-E_delta q`. The Fourier reconstruction
estimates make `B_den` continuous into the smooth weighted source space below.

Let `H_low` be the real Frechet space of smooth source functions supported
physically in `0<=t<=delta^2/4`, flat at the upper endpoint, with seminorms

    p_m(V)=sup_(t,y) u(y)^(-1)
                   sum_(a+b<=m) delta^(2a)|partial_t^a partial_y^b V(t,y)|

finite for every `m`. A smooth extension through `t=0` is understood; it does
not impose a physical lower-edge cutoff. The exact source estimates imply
`A_den:H_low->X_infty` and `B_den:X_infty->H_low` are continuous. Local compact
smooth physical `(E,L)` variations near any interior circular orbit belong
to this space after the displayed invariant change of variables.

Consequently

    N_den=ker A_den subset H_low,
    Pi_null=I-B_den A_den:H_low->N_den                    (2.2)

are a closed Frechet subspace and a continuous projection, respectively.
This is the explicit perturbation dictionary: choose a real smooth low-tube
seed `V`, form `Pi_null V`, and convert it to `delta F` by the same fixed
prefactor as in `F_H`. Each species can be varied independently.

Let `H_*` denote the original exact source. On the entire low-tube correction
region the source proof supplies strictly positive relative margins

    H_*>=c u delta^(-2),  -partial_t H_*>=c u delta^(-4).

A sufficiently small ball in the first weighted seminorm, after a fixed
rescaling of its radius, preserves these margins. Above `delta^2/4` the DF
is unchanged. Therefore every parameter in an open neighborhood `U` of zero
in the product of the two spaces `N_den` produces two positive smooth DFs
with negative physical energy derivative, the same occupied support, the
same exact individual densities, and hence the same actual potentials and
frequencies. The flat support ends are retained by the same quantitative
weight used in the exact inverse. The variation is not required to be
compact in intrinsic `y`; its correction has the controlled relative weight
`u` and so remains smooth and flat at the physical radial ends.

The variation of `w=-F_E` is relatively small on its support. The old and new
energy norms are equivalent. Taking the neighborhood smaller if needed
preserves the original coercive energy bound by comparing `1/w` pointwise.
The complete boundary operator is norm-continuous in this parameter topology
and affine in `w`; its coefficient estimates use finitely many weighted
seminorms. The geometry in the preceding actual theorems is fixed throughout.

## 3. Exact scalar kernel variation

Fix one actual DF in `U`, a real positive threshold frequency
`nu=kappa_j(s_c)`, and an energy mode `h`, with actual field `phi=P h`. Suppose

    kappa_j'(s_c)=0,  kappa_j''(s_c)!=0,  d=phi_j'(s_c)!=0.

The actual mode bootstrap gives `phi in C^(1,1)`. Vary only species `j` with
an exact-density-null `delta F_j`. Its potential and all orbit maps remain
fixed. With `omega_k=k Omega_j`, `dm=2*pi*C_Gamma dJ dL`, the derivative of
the boundary Fredholm kernel/cokernel pairing is exactly

    B_phi(delta F_j)
      =sum_(k>0) integral 2*(-partial_E delta F_j)
                 *omega_k^2/(omega_k^2-nu^2)*|phi_jk|^2 dm.       (3.1)

This is obtained from `ell_h(delta A phi)`, where `A=I-P T_+` and
`ell_h(f)=integral conjugate(h) f dGamma`, using actual reciprocity and
pairing the positive and negative radial harmonics. Its coefficients are
real, and it is a real linear functional of a real variation. At regular
resonances the original mode's trace is zero; at the selected circular
threshold its numerator is `O(J)` and denominator comparable to `J+x^2`.
Thus the form is a genuine locally integrable functional, not an unassigned
principal value. The nonresonant tail is controlled by Parseval and the
mode's radial `C^(1,1)` bound.

Define for this species

    C_phi(J,L)
       =2*sum_(k>0) omega_k^2*|phi_jk|^2
                              /[Omega_j*(omega_k^2-nu^2)],
    S_phi=partial_J C_phi.                                  (3.2)

For compact low-tube tests, integration by parts in `E`, using
`dJ=dE/Omega_j`, rewrites (3.1) as

    B_phi(delta F_j)=integral delta F_j*S_phi dm.              (3.3)

This equation is also valid distributionally. The circular lower boundary
term vanishes after integration in `L`: locally
`C_phi=O(J/(J+x^2))`, whose integral in `x` is `O(sqrt(J))`. Away from circular
resonances it vanishes as `J->0` directly. The low-tube test vanishes before
the energy cap. No derivative of `phi` beyond `C^(1,1)` is assumed in (3.2).

## 4. What annihilating the density nullspace would imply

Assume for contradiction that `B_phi` vanishes on **all** admissible
exact-density-null directions of species `j`. Because arbitrary small
scalar multiples are admissible, it then vanishes as a linear functional on
the whole `N_den`. Applying (2.2) gives, for every smooth low-tube seed `V`,

    B_phi(F_V)=B_phi(F_(B_den A_den V)).

The continuous functional on radial targets

    rho -> B_phi(F_(B_den rho))

restricts on compactly supported radial tests to a distribution `chi(r)`.
The intrinsic/radial change of variables only changes its smooth positive
Jacobian. The preceding identity says exactly that the functional of an
arbitrary local physical variation factors through its radial density.

The adjoint of radial density extraction is orbital averaging. Indeed direct
change of variables gives

    integral chi(r)*delta mu(r) dr
      =integral delta F(E,L)*chi_bar(J,L) dm,
    chi_bar(J,L)=(2*pi)^(-1) integral chi(r(theta,J,L)) dtheta.   (4.1)

For a distribution this identity defines the average by duality. On a
sufficiently small circular chart `partial_s r` stays bounded away from zero
for each angle; changing `s` to `r` defines the pullback without any
distributional ambiguity. Therefore annihilation of the density nullspace
forces

    S_phi(J,L)=chi_bar(J,L)                                 (4.2)

as distributions on the low tube with `J>0`.

## 5. Circular limit identifies the radial distribution off the circle

Use the physical circular center `s`, so `L=L_c(s)`, and write
`x=s-s_c`, `kappa_c=nu`. On a punctured neighborhood of `s_c` there is no
other fundamental circular resonance. The oscillator expansion and the
radial `C^(1,1)` bound give uniformly there

    phi_j1(J,s)=phi_j'(s)*sqrt(J/(2*kappa_j(s)))+O(J),
    sum_(k>=2)|phi_jk(J,s)|^2=O(J^2).

The second estimate follows in `L^2_theta` by subtracting the constant and
linear cosine Taylor polynomial of the radial field; Parseval controls the
entire tail at once. The nonresonant multipliers for `k>=2` are bounded.
Consequently, for `s` away from `s_c`,

    C_phi(J,s)/J -> |phi_j'(s)|^2/[kappa_j(s)^2-nu^2]        (5.1)

uniformly on compact subintervals.

Average (4.2) over `0<J<eta`. Its left side is
`C_phi(eta,s)/eta`. On the right, the orbital averages converge to `chi(s)`
in distributions as `J->0`: the smooth orbital maps tend to the identity in
`s`, uniformly in angle, so their dual test-function pullbacks tend to the
identity. Using (5.1) proves

    chi(s)=|phi_j'(s)|^2/[kappa_j(s)^2-nu^2]                 (5.2)

as a distribution off `s_c`, hence as the displayed continuous function
there. Any additional distribution supported at `s_c` is irrelevant for
orbits that avoid that radius. Since `phi_j'` is Lipschitz,

    chi(s_c+x)=C_0/x^2+O(1/|x|),
    C_0=|d|^2/[kappa_c*kappa_j''(s_c)] != 0.              (5.3)

No derivative of this radial function is taken in the argument below.

## 6. Exact blow-up contradiction

The actual twist identity, in `(J,s)`, is

    Omega_j(J,s)-nu
       =alpha J+beta x^2+O(J^2+J|x|+|x|^3),
    alpha=kappa_j''(s_c)/(4*kappa_c),
    beta=kappa_j''(s_c)/2,
    alpha/beta=1/(2*kappa_c).                              (6.1)

In particular the two leading coefficients have the same sign. Rescale

    J=epsilon^2 T,  s=s_c+epsilon X.

On compact subsets with `T>=0` and `T+X^2>0`, the `C^(1,1)` radial field and
smooth orbital map yield

    phi_j1=epsilon*d*sqrt(T/(2*kappa_c))+O(epsilon^2),
    C_phi(epsilon^2 T,s_c+epsilon X)
        -> C_0*T/[X^2+T/(2*kappa_c)]                      (6.2)

uniformly. All higher harmonics contribute `O(epsilon^4)` before division by
their bounded denominators. Differentiation of (6.2) is taken only in the
distributional sense, so requires no unproved higher mode regularity:

    epsilon^2*S_phi(epsilon^2 T,s_c+epsilon X)
        -> C_0*X^2/[X^2+T/(2*kappa_c)]^2.                 (6.3)

Choose a compact open set with `T>0` and
`|X|>sqrt(2*T/kappa_c)` by a fixed positive margin. These orbits avoid the
critical physical radius. Their actual radial expansion is

    r(theta)=s_c+epsilon*[X+sqrt(2*T/kappa_c)*cos(theta)]
                       +O(epsilon^2),

uniformly in angle and the compact parameter set. Equation (5.3) is therefore
an ordinary continuous-function asymptotic along every one of these orbits.
It gives the uniform limit

    epsilon^2*chi_bar(epsilon^2 T,s_c+epsilon X)
      -> C_0*(2*pi)^(-1) integral
                 [X+sqrt(2*T/kappa_c)*cos(theta)]^(-2) dtheta
       =C_0*|X|/[X^2-2*T/kappa_c]^(3/2).                 (6.4)

The scalar integral follows by differentiating the elementary identity
`average (X+a cos(theta))^(-1)=sign(X)/sqrt(X^2-a^2)` on `|X|>|a|`.
It can equivalently be obtained by the tangent half-angle substitution.

The limits (6.3) and (6.4) cannot agree. For `X=1` and any sufficiently small
`T>0`, after division by the nonzero `C_0`, the first is
`[1+T/(2*kappa_c)]^(-2)<1`, whereas the second is
`[1-2*T/kappa_c]^(-3/2)>1`. They differ on an open parameter set. This
contradicts their equality as distributions in (4.2).

Thus `B_phi` cannot annihilate the exact density nullspace. Some real smooth
seed `V` has

    B_phi(F_(Pi_null V)) != 0.                            (6.5)

The construction in Section 2 makes a sufficiently small multiple of this
an admissible actual DF perturbation. This proves scalar transversality for
every bad-force-trace mode. It is not a heuristic genericity assertion.

## 7. Scalar transversality suffices for generic (CF)

The fixed actual potentials have finitely many simple circular extrema.
Let `C_freq` be the finite set of their positive **fundamental** frequencies
`kappa_j(s_c)`; higher harmonics need no additional (CF) condition. Frequencies
in this set, and the circle locations themselves, do not move under the
exact density-null perturbations.

For each `nu_c in C_freq`, define on `U`

    d_c(F)=dim ker[I-K_F,+(nu_c)].

Each value is finite by compact Fredholm theory. Operator-norm continuity
makes `d_c` upper semicontinuous. Its locally constant locus is open dense:
in any nonempty open parameter set choose a point attaining the minimum
integer value of `d_c`; upper semicontinuity supplies a smaller open set on
which that value is constant. The finite intersection of these open dense
loci is again open dense; no infinite-dimensional Baire assertion is needed.

At a point of this intersection, fix `nu_c` and its kernel dimension `m`.
Choose fixed Fredholm complements there. Along every admissible null-DF line
the complementary block is invertible for sufficiently small parameter,
and the remaining Schur matrix is `m by m`. Local constancy of the full
kernel dimension means that this matrix has nullity `m` and is identically
zero for all sufficiently small real parameters. Hence its first derivative
is zero, including every quadratic kernel/cokernel entry (3.1).

If any of its actual kernel modes had a nonzero force trace at a circle with
this frequency, scalar transversality (6.5) would give an admissible direction
for which that derivative entry is nonzero. This is impossible. Every such
mode therefore satisfies (CF). The argument is repeated for the finite list
of threshold frequencies. Real-coefficient symmetry covers the negative
ones.

This establishes actual generic (CF) within the specified exact-density DF
choices. It does not assert generic absence of all modes. Modes with zero
force trace may remain. In particular it does not need a perturbation matrix
which is invertible on the entire old eigenspace.

## 8. Consequences, audit leaves, and precise limits

If this new scalar transversality argument passes independent audit, combine
it with the already proved actual cold geometry, boundary pairing,
kernel-to-energy reconstruction, global finite exceptional set, mode
`C^(1,1)` bootstrap, and the (CF)-conditional reduced-inverse theorem. This
removes (CF) as an extra assumption for an open dense set of the admissible
actual exact DFs. The standard smooth-source transform and work summation
must still be invoked in their exact reviewed form before declaring the
whole-set linear work theorem. Nonlinear actual-path and label-gradient
control remain outside this result.

The potentially load-bearing new leaves are explicit: continuity of the
exact right inverse in the stated weighted smooth topology; the distribution
factorization through density; the weak circular limit; and the local
noncrossing blow-up comparison. Sections 2 and 4--6 provide their arguments.
The proof neither differentiates a merely Lipschitz force twice nor infers
an actual eigenmode from a formal local asymptotic.

## 9. Source pins and separate high-frequency review

Repository sources below are under
`real_research/analytic_review_2026_10_18_codex/`.

* `smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`:
  `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.
* `cold_dominated_feedback_2026_10_19/HIGH_FREQUENCY_INVERSE.md`:
  `6111b7f0f2e2ea0ef1ea80b81c1a1227374bedc270614c50698db830ade8d49c`.
* `cold_dominated_feedback_2026_10_19/THRESHOLD_MODES.md`:
  `40304ae8d1c0495cdd7482202aa9dcdfa494f12287754b7e648dd2adf26a77b5`.
* `cold_dominated_feedback_2026_10_19/REDUCED_INVERSE.md`:
  `b7250d27338131815ad2ddf87187152efb35eb332606c7f037a591420970770e`.

The high-frequency source received a separate bounded colleague review:
the actual weak output derivative gives `|Delta_r P_n|<=C|Delta r|/|n|`;
the source radial interpolation gives `|Delta r|^(1-gamma)`; the circular
product lemma and action interpolation give the displayed
`|Delta r|^(1-beta)|n|^(-1-p)`; fixed `Omega` submersion charts preserve that
bound and introduce no missing factor of `n`. No issue was found in those
specific raw-proof steps. This review is not represented as a review of the
new transversality theorem.
