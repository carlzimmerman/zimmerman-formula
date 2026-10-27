# Complete boundary source duality for the actual shell kernels

19 October 2026. Task `/root/boundary_pairing`; supplied base revision
`915b108f82629d3e794a6a3a3b6ad5e793355172`. Analytic derivations only. No
scientific program, numerical integration, discretized scientific array, or
process operation was used. Existing repository files were not modified.
Self-review; no independent proof certificate is claimed.

## 1. Claim and conclusion

The missing source pairing in `SINGULAR_PENCIL_AND_MODES.md`, Section 2, is
valid under the explicit geometric hypotheses below. The circular boundary
needs only the nonvanishing **full** action-frequency gradient. The additional
condition `partial_L Omega(0,L) != 0` is unnecessary for this source-duality
statement. Flat support boundaries cause no loss when the frequency remains a
submersion there. High harmonics are controlled in the source dual norm by
Parseval, without trying to sum the generally divergent scalar bound
`sum |k|^(-2 gamma)`.

The result proves the conditional actual common-kernel/common-cokernel
reduction in the cited note under these hypotheses. It does not prove an
ordinary inverse, a reduced frequency-dependent inverse, energy membership
of threshold responses, or bounded work of all neutral modes.

## 2. Exact hypotheses and spaces

Let `I=[r_0,R]`, `Y=C^gamma(I;C)^2`, and `0<gamma<1/2`. Write `Y^x` for
the continuous anti-dual: `<phi,S>` is conjugate-linear in `phi` and linear in
`S`. All occurrences of `(C^gamma)*` below mean this anti-dual, identified with
the usual dual by conjugation. Species are ordered `(t,f)`. Set

    dm=2*pi*C_Gamma*dJ*dL,  C_Gamma=4*pi^2,
    nu_ik=k*Omega_i(J,L),  w_i=-F_{i,E}.

Assume the following for the fixed, positive-warmth actual equilibrium.

(H1) The occupied action sets are compact subsets of a uniformly nondegenerate
radial-well region, with `0<Omega_-<=Omega_i<=Omega_+`. The orbit map admits
uniformly smooth circular coordinates

    r_i(theta,J,L)=R_i(theta,a,L),  a=sqrt(J)>=0,
    R_i(theta,0,L)=s_i(L),

and is smooth in ordinary actions away from `J=0`. Pericenter is chosen as
angle origin, so orbital extraction at a fixed eccentric point is represented
by a real signed orbital measure. Smooth bounded extensions to a slightly
larger well region are available.

(H2) Susceptibilities `w_i` extend smoothly by zero across the upper energy
cap and the angular-momentum support ends, and are nonnegative. They need not
vanish at `J=0`. All cap/L-end intersections are included in this extension.
These are fixed-warmth regularity assertions, with no uniform cold-limit
claim. They hold for the exact inverse in the sources below.

(H3) Fix a positive frequency `nu_c`. For the finitely many potentially
resonant pairs `(i,k)`, the full gradient of `nu_ik` is nonzero in a neighborhood
of its `nu_c` level on the closed occupied set, except possibly at one specified
point `(j,n,q_c)`, where `n>=1`, `q_c` is eccentric and interior, `w_j(q_c)>0`,
and `Omega_j` has a nondegenerate minimum. A neighborhood of that point
contains no other critical point. There are no other critical points at the
same frequency. If no such exceptional point exists, omit all rank-one
subtractions below. Thus no unexamined saddle or degenerate critical channel
is hidden in (H3).

(H4) The actual real shell matrix is retained:

    P_ff=P_ft=P_tf=-G/max(r,r'),
    P_tt=2*(G^2/a_0)*integral_(max(r,r'))^infinity M_t(s)*s^(-4) ds.

It is jointly Lipschitz on `I x I`, with symmetric species/radius exchange.
No small susceptibility, small cold mass, or inverse of `I-P T_+` is assumed.

## 3. Definition of the boundary source map

For `Im z != 0`, define the bounded sesquilinear form

    B_z(phi,psi)
      =-sum_i sum_(k!=0) integral w_i*nu_ik/(nu_ik-z)
                              *conjugate(phi_ik)*psi_ik dm,
    <phi,T(z)psi>=B_z(phi,psi).

This formula uses no derivative of a `C^gamma` test field. The zero harmonic is
absent and every resulting source has zero total mass in each species.

At the exceptional minimum let

    ell(phi)=phi_jn(q_c)=integral phi de_c,
    beta=4*pi^2*C_Gamma*nu_c*w_j(q_c)
                        /(n*sqrt(det D^2 Omega_j(q_c)))>0,
    Q_c(phi,psi)=beta*conjugate(ell(phi))*ell(psi).

Choose a real smooth frequency cutoff `chi` supported in `[0,eta)`, equal to
one near zero, and set

    Lambda(z)=integral_0^eta chi(s)/(s-(z-nu_c)) ds.

Then there exist bounded maps `T_+,T_-:Y->Y^x` such that, in operator norm,

    T(nu_c +/- i epsilon)
          + beta*Lambda(nu_c +/- i epsilon)*e_c tensor ell
               -> T_+ or T_-                  (epsilon down to zero).

The sign convention is therefore

    T(z)=-beta*Lambda(z)*e_c tensor ell + T_reg(z).

The entire scalar Cauchy term, including its upper/lower imaginary threshold
constant, is removed. Removing only `log(1/epsilon)` would give a different
imaginary finite part and would not give the optical formula stated below.
Changing the real cutoff changes `T_+` and `T_-` by the same **real** rank-one
source term. This preserves reciprocity and the optical identity. An arbitrary
complex rank-one shift need not do so.

## 4. Circular product lemma and regular pushforwards

For each nonzero integer `k`, let `f_k(a,L)` be the orbital coefficient of a
radial field `f in C^gamma(I)`. Smoothness of `R` gives, uniformly on the fixed
compact well family,

    ||f_k||_(C^gamma_(a,L)) <= C ||f||_(C^gamma),
    f_k(0,L)=0,
    |f_k(a,L)|<=C ||f||_(C^gamma)*a^gamma.

No harmonic decay is needed in this lemma. If

    A_k(J,L)=conjugate(phi_k(sqrt(J),L))*psi_k(sqrt(J),L),

then `A_k=O(J^gamma)` and `A_k` is `C^gamma` in the ordinary action variables,
with norm at most `C||phi||_Y||psi||_Y`. Indeed, for `a,b>=0` at the same `L`,

    |A_k(a^2,L)-A_k(b^2,L)|
       <= C (a^gamma+b^gamma)*|a-b|^gamma
       <= C |a^2-b^2|^gamma.

Changes in `L` are `C^gamma` by the first coefficient estimate; splitting a
joint change into these two changes proves the assertion. Extending `A_k` by
zero to `J<0` preserves its `C^gamma` bound, since its boundary value is zero
and `|A_k(J,L)|<=C J^gamma`. This product gain is essential: extending an
individual harmonic gives only `C^(gamma/2)` in `J`.

Multiply by the smooth, zero-extended `w_i`, by `nu_ik`, and by a smooth action
partition. The resulting amplitudes are globally `C^gamma` on regular charts,
including circular/cap corners, with bilinear norm bounds. Near `J=0` one may
extend the orbit map and frequency independently of the physical support;
the product is already zero on the unphysical side. Away from `J=0`, ordinary
smooth action coordinates apply. Multiplication by the flat zero extension
of `w_i` handles the upper cap and support ends.

On a chart where `grad nu_ik != 0`, change coordinates to

    s=nu_ik-nu_c,  t=a complementary smooth coordinate.

Extend the chart amplitude by zero using a compactly supported partition.
Its frequency pushforward density is

    b_phi,psi(s)=integral A(s,t)*Jac(s,t) dt,

and satisfies the operator-valued estimate

    |b_phi,psi(s)-b_phi,psi(s')|
        <= C |s-s'|^gamma ||phi||_Y||psi||_Y.

There is no moving-domain term left: zero extension at `J=0` is justified by
the circular product lemma, and zero extension at a cap by (H2). One can solve
for `L` when `partial_L nu != 0`, or solve for `J` when `partial_J nu != 0`.
Thus arbitrary circular tangencies are covered whenever the full gradient is
nonzero. Compactness and (H3) give finitely many such charts near the level;
regions uniformly away from the level contribute an ordinary bounded form.

For a compactly supported operator-valued `C^gamma` density `b`, the boundary
formula follows directly by writing `b(s)=b(0)+[b(s)-b(0)]` near zero:

    integral b(s)/(s-i0) ds
       =PV integral b(s)/s ds + i*pi*b(0).

The difference term is absolutely integrable because it is `O(|s|^(gamma-1))`.
The same subtraction proves convergence in bilinear operator norm (for example
an `O(epsilon^gamma)` bound on a fixed chart). This is a proof for arbitrary
Holder test fields, rather than an inference from a bound for `P T`.

### Explicit boundary exponents

At a simple circular stationary epicyclic frequency the actual twist identity
in `GEOMETRY_AND_SCALING.md`, Section 6, gives

    nu_ik-nu_c = a J+b (L-L_c)^2+higher terms,
    a*b>0, a!=0, b!=0.

A smooth boundary-preserving coordinate change puts this into the same-sign
normal form, with `J` comparable to the new inward coordinate. Equivalently,
solving for `J` and using the nondegenerate boundary extremum gives
`0<=J<=C|s|`, `|L-L_c|<=C sqrt(|s|)`. Since the dual amplitude is `O(J^gamma)`,
its pushforward density obeys

    |b_phi,psi(s)|<=C |s|^(gamma+1/2)||phi||_Y||psi||_Y

on its occupied side, and vanishes on the other side locally. In particular
its threshold value is zero and its threshold Cauchy integral is absolutely
convergent. More generally a same-sign finite contact of order `m` gives the
pointwise exponent `gamma+1/m` when the detuning has the corresponding
`J+x^m` normal form. None of these finite-order refinements is needed for the
regular-chart `C^gamma` theorem.

At an eccentric cap let `x>=0` be inward distance. Smooth flatness gives
`|w|<=C_N x^N` for every fixed integer `N`. At a same-sign quadratic isolated
cap threshold `s=a x+b y^2`, its local density is `O(|s|^(N+1/2))` for every
`N`. At an opposite-sign cap tangency there are regular resonances approaching
the cap, so the whole local density need not vanish at the tangency frequency;
the newly pinching region has the same `O(|s|^(N+1/2))` bound, while the full
rough-field density has the `C^gamma` bound just proved. Flatness by itself
would not control an arbitrarily degenerate **full** critical frequency; (H3)
explicitly excludes that unproved case.

## 5. The exceptional Morse subtraction

In the eccentric Morse chart, let `s=nu_jn-nu_c>=0`. The pushforward of the
local form has the expansion in bounded sesquilinear-form norm

    b_crit(s)=Q_c + O(s^(gamma/2)).

To see this, use smooth Morse coordinates with `s=|x|^2`; orbital extraction is
`C^gamma` in ordinary eccentric actions, hence its product differs from its
value at the center by `O(|x|^gamma)`. The smooth Jacobian has the same or better
modulus. The limiting coarea factor is

    2*pi/(n*sqrt(det D^2 Omega_j(q_c))),

which, multiplied by `2*pi*C_Gamma*nu_c*w_j(q_c)`, is exactly `beta`.
Subtracting `chi(s)Q_c` leaves a compactly supported density `r(s)` with
`||r(s)||<=C s^(gamma/2)`. Thus `r(s)/s` is norm integrable, its upper/lower
limits agree, and its diagonal integral is real. The local remainder has zero
optical jump at the threshold. The bound
`|s-i epsilon|>=s` gives norm dominated convergence; splitting at `s=epsilon`
also gives an `O(epsilon^(gamma/2))` remainder estimate.

This reconstructs the local Morse finite part and connects it to the global
source form. It does not assume invertibility of the regular field operator.

## 6. High harmonics in the correct dual norm

Choose `N>2(|nu_c|+1)/Omega_-`. For `|k|>N` and `|z-nu_c|<=1`,

    |nu_ik/(nu_ik-z)|<=2.

At each orbit, Parseval and Cauchy-Schwarz give

    sum_(|k|>N) |phi_ik*psi_ik|
       <= (sum_(|k|>N)|phi_ik|^2)^(1/2)
          (sum_(|k|>N)|psi_ik|^2)^(1/2).

The uniform orbit map makes `theta -> phi_i(r_i(theta,q))` a uniformly
`C^gamma` function with norm `C||phi||_Y`. Its Fourier tail satisfies

    sum_(|k|>N)|phi_ik(q)|^2 <= C N^(-2 gamma)||phi||_Y^2.

An elementary proof averages the Parseval identity for
`f(theta+h)-f(theta)` over `0<=h<=2*pi/N`. For `|k|>N`, the averaged multiplier
is

    2-2*sin(2*pi*k/N)/(2*pi*k/N) >= 2-1/pi > 1,

whereas the averaged squared Holder increment is `O(N^(-2 gamma))`.
Consequently the full nonresonant tail has the uniform bilinear norm bound

    ||B_z^(|k|>N)|| <= C N^(-2 gamma) integral sum_i w_i dm.

The susceptibility integral is finite. The same estimates, or the difference
of the scalar multipliers, give continuity at the upper and lower boundary.
Thus the tail converges in `B(Y,Y^x)` and produces no jump. There are only
finitely many resonant low harmonics, to which Sections 4 and 5 apply. This
completes the global source theorem.

If (H3) holds without an exceptional critical point throughout a compact
frequency interval, the same finite chart cover and tail bounds are uniform
there. The regular source map is locally `C^alpha` in frequency in
`B(Y,Y^x)` for every `0<alpha<gamma`. One elementary estimate subtracts the
density at the two evaluation frequencies, splits the principal-value
integral at their separation `h`, and gives
`O(h^gamma*(1+|log h|))`, which is `O(h^alpha)`. Composing with Section 8 gives

    K_+(nu)=P T_+(nu):Y -> C^sigma,  sigma=1-gamma>1/2,

locally uniformly, with local `C^alpha` frequency dependence in that stronger
operator norm. In particular `K_+(nu)` is compact on `Y`. This statement
requires no Lipschitz field estimate. It concerns compact frequency intervals;
it does not assert decay of `K_+(nu)` as `|nu|` tends to infinity. That decay
needs an additional summation argument for the actual potential harmonics.

## 7. Reciprocity, optical form, and vanishing jump

For the regular finite parts just constructed,

    <phi,T_+ psi> = conjugate(<psi,T_- phi>),

because all principal-value and subtraction coefficients are real and the
upper/lower delta terms have opposite signs. The imaginary form is exactly

    Im <phi,T_+ phi>
      =-pi*nu_c*sum_regular integral_(nu_ik=nu_c)
          w_i*|phi_ik|^2 * (2*pi*C_Gamma)
                              d sigma/|grad nu_ik| <= 0.

Here `regular` means all ordinary resonance curves; the isolated subtracted
Morse point contributes zero to the finite-part optical form. Boundary
portions have zero amplitude by the circular lemma or the flat susceptibility.
No boundary optical mass is silently discarded.

The jump source is characterized by the corresponding polarized form:

    <phi,(T_+-T_-)psi>
      =-2*pi*i*nu_c*sum_regular integral_(nu_ik=nu_c)
            w_i*conjugate(phi_ik)*psi_ik dm_coarea.

Therefore if every regular resonant trace of `psi` vanishes wherever `w_i>0`,
then `T_+psi=T_-psi` in the complete source anti-dual. Conversely, zero optical
form implies those traces vanish, by their continuity and positivity of the
regular coarea density. This argument requires no unavailable derivative of
an arbitrary Holder field and no inversion of a regular operator.

## 8. The actual reciprocal kernel on the complete source dual

For `S in Y^x` define `P S` by applying `S` to the real kernel sections. Joint
Lipschitz regularity gives

    ||P(r,.)-P(r',.)||_(C^gamma) <= C |r-r'|^(1-gamma),

by interpolating their `O(|r-r'|)` sup difference and uniform Lipschitz bound.
Thus

    P:Y^x -> C^(1-gamma)(I)^2 -> Y

is bounded and compact. The second inclusion is compact because
`1-gamma>gamma`: uniform convergence plus the stronger Holder bound implies
convergence in the weaker Holder norm by the elementary interpolation
inequality.

Reciprocity holds on all these anti-dual sources, not only finite measures:

    <P S,T> = conjugate(<P T,S>).

For completeness, clamp each radius into `I`, convolve the resulting symmetric
Lipschitz kernel with the same real mollifier in both variables, and call the
symmetric smooth kernel `P_epsilon`. Its error `E` has sup norm `O(epsilon)`
and uniform Lipschitz bounds. Rectangular differences satisfy

    |Delta_h^r Delta_k^s E| <= C min(epsilon,|h|,|k|).

For `gamma<1/2`, division by `|h|^gamma|k|^gamma` bounds this by
`C epsilon^(1-2 gamma)`. The one-variable Holder errors also tend to zero.
Hence `P_epsilon -> P` in the mixed `C^gamma` kernel norm which controls
successive application of any two members of `Y^x`. Smooth symmetric kernels
have the asserted reciprocity (approximate by finite symmetric sums of
separated smooth functions); passing to the mixed-norm limit proves it for
`P`. Density of measures in the full dual is neither asserted nor needed.

With `A=I-P T_+`, this proves compactness/Fredholm index zero and all pairing
inputs of `SINGULAR_PENCIL_AND_MODES.md`, Section 2. Its algebraic proof then
identifies kernel and cokernel and establishes its common-dark-kernel
characterization, under (H1)--(H4). It still supplies no dynamic inverse.

## 9. A nonempty actual cold-dominant family satisfying the boundary geometry

The hypotheses above are compatible with the exact source family even when
the cold mass dominates the baryon. This is an analytic existence statement,
not a claim that an independently selected unpinned member satisfies them.

Take radii `ell*(1,2,3,4)` and the actual dimensionless profile `p` from
`GEOMETRY_AND_SCALING.md`, Section 1. Put `b=r_M/ell>0` and define

    B_p=rho^2*p''-rho*p'-3*p,
    C_p=2*(p')^2+2*p*p''-10*p*p'/rho+5*p^2/rho^2.

Up to positive factors, the free and tethered epicyclic derivatives have
numerators

    N_f=B_p-3*b,
    N_t=(1-f)*B_p-3*b-b*f^2*C_p.

The second formula follows by normalizing the actual circular law as
`rho*[b+(1-f)*p]-b*f^2*p^2/rho`; it is not a tracer replacement.
`B_p<0` on the law annulus and outer taper. On the inner taper it is real
analytic, has limits `0` and `-8` at its two ends, and is positive somewhere:
at `rho=5/4`, Section 7's exact positive `c_0` and positivity of `S',S''` give

    B_p(5/4) > (5/4)*c_0 > 0.

Choose any sufficiently small positive interval `[b_0,2*b_0]` below one third
of this positive value. Points with `B_p` in `[3*b_0,6*b_0]` lie in a compact
subset of the open inner taper. Since the analytic function `B_p'` is not
identically zero, it has finitely many zeros on that compact subset. Avoid
the finitely many values `B_p(rho_*)/3` at those zeros when selecting `b`.
The allowed set is open and nonempty and contains rational choices. Every
zero of `N_f` is then simple. All other portions of the closed shell have
`N_f<0`. Choosing one sufficiently small fixed `f>0` preserves these simple
zeros and creates none: use disjoint monotonic neighborhoods of the finitely
many zeros and the positive minimum of `|N_f|` on their compact complement.
This is ordinary uniform `C^1` perturbation of the displayed exact formula.

At a simple epicyclic extremum, the actual identity gives

    partial_J Omega(0,L_c)=K''/(8*K)=kappa''/(4*kappa) != 0,
    K=kappa^2.

Elsewhere `partial_L Omega(0,L)!=0`. Compactness therefore gives a nonzero
full gradient on the entire circular line. For one sufficiently small,
strictly positive warmth `delta`, smooth action-frequency dependence and
`sup J=O(delta^2)` preserve that property on the complete closed occupied
tube, including the cap. The exact inverse permits making this fixed choice
of `delta`. Thus (H3) holds without any exceptional eccentric Morse point,
although circular stationary epicyclic frequencies are present and are
covered by the dual theorem.

The ratio of law-annulus cold mass to baryon mass is `rho/b`, which can be
arbitrarily large by choosing `b_0` small. The deep and core restrictions are
preserved: `f*r_M/r_0=f*b`, and the core condition reads
`1>2*f^2*b/(1-f)`. Both hold for the small positive choices just described.
No susceptibility smallness is inferred from these facts. This family proves
that the source-pairing hypotheses do not force the small-cold-mass regime.
It does not select a particular rational `b,f,delta` or prove a feedback
inverse for any of these members.

## 10. Limits and exact remaining obligations

The full source pairing is now proved under a concrete geometric condition
which has a nonempty actual cold-dominant subfamily. The originally generic
assertion for every unpinned source member remains unjustified: a degenerate
full critical frequency, an eccentric saddle, or additional coincident
critical channels requires another subtraction theorem. Flatness of `w` at
the cap alone does not supply that theorem.

For an actual isolated eccentric minimum satisfying (H3), the proof supplies
the complete source duality required by the persistent-kernel classification.
It does not prove that such a minimum exists in the narrow cold-dominant
subfamily of Section 9; that subfamily has no full critical points. The
independent questions of persistent threshold responses, their energy
membership, quadratic receiving quotients, and a regular frequency-dependent
inverse remain separate.

Proofreading self-review covered this entire new artifact. Routine notation
and prose were checked; no independent correctness review is represented by
that proofreading step. No scientific verification command is applicable to
this analytic derivation. High-frequency decay of the boundary field operator
is expressly a separate obligation from the fixed-compact-frequency source
tail estimate proved here.

## 11. Source hashes at reading

- `actual_feedback_2026_10_19/CONTINUATION.md`:
  `3ec0ba51d22f172a31a771ec197678a25cd1a49f013c8cfe09a82d3457d63f81`
- `actual_feedback_2026_10_19/SINGULAR_PENCIL_AND_MODES.md`:
  `3c091ca4be949d0bdf3c1657897a962cb7f60b137f03657c23b8af80a25e5c94`
- `actual_feedback_2026_10_19/GEOMETRY_AND_SCALING.md`:
  `1848347266a2254e18fc579c3c6804cd6703895ce9d298f804a69acd977558c9`
- `claude_continuation_2026_10_19/full_feedback/RESULT.md`:
  `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`
- `smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`:
  `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`

All paths in this list are relative to
`real_research/analytic_review_2026_10_18_codex/` in the supplied repository.
