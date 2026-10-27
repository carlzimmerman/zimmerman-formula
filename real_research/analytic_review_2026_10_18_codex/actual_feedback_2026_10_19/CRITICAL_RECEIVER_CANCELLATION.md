# Actual Morse-channel dressing: optical identity and the invariant obstruction

19 October 2026. Owner: `/root/actual_dressed`. Parent checkpoint: `reviews/latest_results_push_2026_10_19_codex`, base HEAD supplied by coordinator `62bedfa6b6c363eb17ac4a21c24194d847e76f3b`. Analytic only; this new scratch file is the entire write scope. No scientific script, numerical integration, array calculation, or process inspection/control was used. No novelty claim.

**Verdict for the requested global actual halo bound: incomplete.** The shell reciprocity gives an optical identity for the *actual* dressed critical scalar. It yields a semidefinite imaginary part, not strict nonvanishing. The main additional result in Section 6 is that strict nonvanishing is unnecessary for local receiving work: if the scalar is zero but the complete regular inverse exists, the actual optical cancellation gives bounded local work uniformly over nearby compact eccentric occupied receivers with regular/Morse frequency geometry. The complete regular inverse, extension to all receiving boundaries, and global frequency control remain open. For a bounded full field, the independent regular-inverse and nonzero-scalar assumptions can instead be replaced by one decomposition-invariant bordered inverse, whose constrained critical-frequency obstruction is displayed below. None of this proves all-time confinement.

## 1. Actual conventions and critical coefficient

The species order is `(t,f)`. Put `c=G^2/a_0`, `C_Gamma=4*pi^2`, `q=(J,L)`, `dm=2*pi*C_Gamma*dJ*dL`, `w_i=-F_{i,E}>0` on the open occupied actions, and `nu_{ik}(q)=k*Omega_i(q)`. Here `L` in `q` is squared specific angular momentum. Below, the logarithmic scalar is denoted `Lambda(z)` to avoid collision with it. Potentials vanish at infinity. The physical shell kernels are

    P_ff=P_ft=P_tf=-G/max(r,r'),
    P_tt=2*c*integral_{max(r,r')}^infinity M_t(s)*s^-4 ds.

They are real and reciprocal: `P_ij(r,r')=P_ji(r',r)`. Their field matrix is

    H(r) = [[h(r),-g(r)],[-g(r),-g(r)]],
    h=2*c*M_t/r^4 > 0,  g=G/r^2 > 0,
    delta a=H*m,  (P rho)'=-H*m_rho.

Take an eccentric interior nondegenerate **minimum** `q_c` of `Omega_j`, with `w_j(q_c)>0`, `n>=1`, and `nu_c=n*Omega_j(q_c)>0`. Work on a compact Morse chart, and suppose this is the only singular critical channel at `nu_c`; other channels at this frequency are regular. A maximum has the reversed interval and the corresponding logarithm. Coincident critical channels require a larger matrix.

Choose the orbit angle origin at a turning point. Then `r_j(-theta,q)=r_j(theta,q)`. Define the real signed radial measure `e_c`, in species `j` only, by

    ell(phi) := integral phi de_c
             = (1/(2*pi))*integral_0^(2*pi)
                   phi_j(r_j(theta,q_c))*exp(-i*n*theta) dtheta.

Its reality follows from evenness of the radial orbit; its total mass is zero since `n!=0`. Define `v=P e_c`. This is exactly the source-angle coefficient `P^(n)_{.j}(.,q_c)`, without a change of model. In particular

    ell(v) = -G*integral |A_n(s;q_c)|^2*s^-2 ds <0  if j=f,
    ell(v) = 2*c*integral |A_n(s;q_c)|^2*M_t(s)*s^-4 ds >0 if j=t,

where `A_n=(1/(2*pi))*integral 1_{r(theta,q_c)<s} exp(-i*n*theta)dtheta`.

The actual feedback has the form

    K(z) phi = P T(z) phi,
    T(z) phi = radial pushforward of
        -w_i(q)*sum_{k!=0} [nu_{ik}(q)/(nu_{ik}(q)-z)]
                      *phi_{i,k}(q)*exp(i*k*theta),

with measure `dm*dtheta/(2*pi)`. On the critical chart,

    K(z) = Lambda(z)*v_0 tensor ell + R(z),
    Lambda(z) = log(nu_c+eta-z)-log(nu_c-z),
    beta = 4*pi^2*C_Gamma*nu_c*w_j(q_c)
                /(n*sqrt(det D^2 Omega_j(q_c))) >0,
    v_0 = -beta*v.

The coefficient follows by applying the two-dimensional Morse coarea formula: the limiting pushforward of `dJ*dL` by `n*Omega_j` is `2*pi/(n*sqrt(det D^2 Omega_j(q_c)))`. Multiplication by `dm` and by `-w*nu` gives `-beta`. On `Y_gamma=C^gamma(I)^2`, `0<gamma<1`, the isolated local remainder is Holder through the threshold with a positive exponent, as in Section 4 of the pinned screening source. Existence and regularity of the **complete** regular remainder still require handling every other channel and boundary; they are not proved here merely by naming `R`.

For a boundary value at the threshold put `A=I-R_+(nu_c)`. The scalar used in the previous screening lemma, if `A` is invertible, is

    a_0=ell(A^-1 v_0)=-beta*a,
    a=ell(A^-1 P e_c).

Thus `ell(v)!=0` is the actual bare sign identity; it is not yet the dressed identity `a!=0`.

## 2. Actual field reciprocity is indefinite

For two radial vector measures of zero species masses, let `m_rho` be their cumulative masses. Integration by parts and symmetry give

    integral conjugate(rho) . P sigma
       = integral conjugate(m_rho)^T H m_sigma dr.

Equivalently, on fields in the range of `P`, the reciprocal form is

    B(phi,psi)=integral conjugate(phi')^T H^-1 psi' dr,
    B(P rho,P sigma)=integral conjugate(rho) . P sigma.

The exact inverse matrix gives

    B(phi,phi) = integral [ |phi_t'-phi_f'|^2/(h+g)
                               - |phi_f'|^2/g ] dr.

Indeed `det H=-g(h+g)<0`. This is a genuine indefinite field form for the actual two-species kernel. It is distinct from the positive total perturbation energy `Q=A_energy+integral m^T Hm`. Therefore a proof that replaces `B` by a positive inner product would fail on the actual model. The signs of the two bare diagonal entries above do not repair this: regular dressing mixes the two field directions.

This is an obstruction to that positivity proof, not a counterexample to a halo work bound.

## 3. Optical identity for the actual dressed scalar

Here is the exact sign consequence of reciprocity. Assume the complete finite-part operator `R(z)` has a norm-continuous upper boundary at `nu_c`, is compact on `Y_gamma`, and `A=I-R_+(nu_c)` is invertible. Assume all noncritical resonances at `nu_c` are regular and their coarea traces exist. These are explicit domain/limit assumptions, not consequences of shell reciprocity. Set

    V=A^-1 v,  a=ell(V).

Then

    Im a = -pi*nu_c*sum_regular_(i,k)
                    integral_{nu_{ik}=nu_c}
                       |V_{i,k}(q)|^2*w_i(q)
                       *(2*pi*C_Gamma)*d sigma/|grad nu_{ik}| <=0.       (OI)

The critical isolated minimum is excluded from this sum, since its full leading endpoint density is subtracted into `Lambda`. For the lower boundary, the sign is reversed. For `a_0=-beta*a`, the upper-boundary sign is `Im a_0>=0`.

**Derivation without an unproved field inverse.** Write

    T_reg(z)=T(z)+beta*Lambda(z)*e_c tensor ell,
    R(z)=P T_reg(z).

For `z=nu_c+i*epsilon`, small positive `epsilon`, norm continuity and invertibility of `A` give

    V_epsilon=(I-R(z))^-1 v,
    V_epsilon=P S_epsilon,
    S_epsilon=e_c+T_reg(z)V_epsilon.

All these sources have zero species masses. At positive epsilon they are finite signed measures, so the continuous reciprocal kernel makes `integral conjugate(S_epsilon).P S_epsilon` real. Expanding it, with scalar pairings anti-linear in their first argument, gives the exact identity

    Im ell(V_epsilon)
      = -sum_(i,k) integral
          w_i*nu_{ik}*epsilon*|V_epsilon,i,k|^2
                /((nu_{ik}-nu_c)^2+epsilon^2) dm
        + beta*Im Lambda(nu_c+i*epsilon)*|ell(V_epsilon)|^2.       (OI-eps)

There is no definiteness assumption here. For the critical chart, the coarea density of `w*nu*|V_epsilon,n|^2 dm` equals

    beta*|ell(V_epsilon)|^2 + O(s^alpha),  s=nu-nu_c>0,

uniformly in small epsilon, for some `alpha>0`, using boundedness of `V_epsilon` in `Y_gamma` and the smooth eccentric action map. Its constant part contributes

    -beta*|ell(V_epsilon)|^2*integral_0^eta
                      epsilon/(s^2+epsilon^2) ds.

This cancels the displayed subtraction term exactly because

    Im Lambda(nu_c+i*epsilon)
                   = integral_0^eta epsilon/(s^2+epsilon^2) ds.

The `O(s^alpha)` term tends to zero. Other regular positive-frequency resonances converge to their ordinary Poisson-kernel traces. Negative `k` have no resonance at `nu_c>0`; their contribution tends to zero. The tail is bounded by a constant times `epsilon*sum |k|^(-1-2*gamma)`, using the actual radial Fourier estimate. This proves (OI).

**What it decides.** If one regular resonant trace of `V` has positive weighted square integral, then `a!=0`; the logarithmic channel is screened at that side, subject to the other stated representation/regularity assumptions. If `a=0`, (OI) forces all regular resonant traces of `V` to vanish. This is a precise actual-system obstruction: a dressed source can evade the optical test only as a transparent critical-frequency field. The identity does not prove that the positive sum is strictly positive.

## 4. The invariant bordered threshold lemma

The regular inverse is partly a finite-part convention. The correct invariant object is the bordered operator

    B_0 : Y_gamma x C -> Y_gamma x C,
    B_0(phi,eta) = (A*phi-v_0*eta, ell(phi)),
    B_0 = [[A,-v_0],[ell,0]].

Since `R` is compact, `B_0` is Fredholm of index zero: it differs from `diag(I,1)` by a compact operator. Its injectivity therefore suffices for a bounded inverse. Its actual threshold obstruction is exactly

    A phi=v_0*eta,  ell(phi)=0,  (phi,eta)!=(0,0).                 (BT)

Because `ell(v_0)!=0`, hence `v_0!=0`, a solution of (BT) necessarily has `phi!=0`.

**Lemma (bordered logarithmic screening).** Suppose on each boundary side `R_+/-(nu_c+x)` and the regular forcing `r_+/-(nu_c+x)` are Holder through zero, and the leading forcing is aligned:

    (A(z)-Lambda(z)*v_0 tensor ell) U(z)
                    = Lambda(z)*b*v_0+r(z).

If the two limiting bordered operators `B_0,+/-` are invertible, then

    U_+/-(nu_c+x)=P_+/-+Q_+/-/log(1/|x|)
                      +O(log(1/|x|)^-2)+O(|x|^alpha),           (BE)

for a possibly smaller positive `alpha`. On each boundary side, `P_+/-` and `Q_+/-` are the same from `x<0` and `x>0`. No separate inverse for `A` is required.

**Proof.** Put `tau=1/Lambda`, `eta=Lambda*(ell(U)+b)`. The equation is exactly the bordered system

    [[A(z),-v_0],[ell,-tau]] [U;eta] = [r(z);-b].

At the threshold this is `B_0`. Its inverse has a norm-convergent first-order expansion in `tau`, by the elementary Neumann expansion about the bounded inverse `B_0^-1`; variation of `A` and `r` contributes `O(|x|^alpha)`. Moreover `tau=1/log(1/|x|)+O(log^-2)` on both sides of zero. This proves (BE). The jump density therefore satisfies the symmetric frequency-to-work lemma from the screening source. Given an actual jump representation, its contribution to work at `nu_c` is uniformly bounded. This conclusion remains local in frequency and does not perform the global receiver/harmonic summation.

**Agreement with the earlier scalar lemma.** If `A` is invertible, the Schur complement is `ell(A^-1 v_0)`. Thus `B_0` is invertible exactly when that scalar is nonzero. The statement above is strictly better because it also covers singular `A` with an invertible border.

**Independence from the finite-part convention.** Replacing `Lambda` by `Lambda+d`, with a finite scalar `d`, sends

    R -> R-d*v_0 tensor ell,
    A -> A+d*v_0 tensor ell.

The corresponding border is obtained by adding `d*v_0` times the second row to the first; it is invertible exactly when the old border is. If `B_0` is invertible, write its inverse as `[[E,f],[g,h]]`. For `A_d=A+d*v_0 tensor ell`, solving `A_d x=y` gives

    x=E*y-f*g(y)/(d+h),

whenever `d+h!=0`. Thus an invertible regular `A_d` exists for every finite-part shift except at most one value. When both regular inverses exist, the dressed scalars obey `a_0,d=a_0/(1+d*a_0)`. In particular a zero dressed scalar cannot be fixed by changing the finite part, whereas singularity of `A` sometimes can. This is why (BT), not the particular inverse of `A`, is the physical remaining leaf of this rank-one route.

## 5. What (BT) means in the actual halo

Applying the reciprocal derivation to `A phi=v_0 eta` and `ell(phi)=0` makes the scalar forcing term vanish. The resulting optical identity forces every regular resonant trace of `phi` to vanish. It does **not** give `phi=0`: only a positive weighted sum of those traces has vanished, while the actual field form in Section 2 is indefinite. Establishing injectivity of this trace map on the solution set of (BT) would close the local screening leaf. It is an actual forced field equation with the physical shell kernel, not a generic rank-one example.

There is another precise reason that the already proved positive `Q` does not dispose of (BT). At a two-dimensional Morse minimum,

    nu(q)-nu_c is comparable to |q-q_c|^2.

Even in the favorable case that `phi_{j,n}` is continuously differentiable in `q`, the constraint `ell(phi)=phi_{j,n}(q_c)=0` gives only a possible linear zero. If its gradient at `q_c` is nonzero, the corresponding kinetic amplitude

    u_n(q)=nu(q)*phi_{j,n}(q)/(nu(q)-nu_c)

has logarithmically infinite local `L^2(w dm)` norm:

    integral |u_n|^2*w dm  is comparable below to integral_0 dr/r.

The proof is polar integration on an angular sector where the nonzero linear form is bounded below by a multiple of `r`. Thus the critical trace cancellation that suffices at a regular resonance does not even guarantee an energy-space vector at a Morse threshold. Positive `Q` excludes growing/zero **energy-space eigenmodes**, not these possible threshold fields. If the gradient also vanishes and the numerator is `C^(1,alpha)`, the local norm is finite; that stronger cancellation is not supplied by (OI). Moreover `eta!=0` in (BT) describes a forced critical source rather than a homogeneous eigenmode, so even finite energy alone would not contradict skew-adjointness.

This identifies the smallest additional actual-system statement needed here: the only physical field satisfying (BT), with vanishing traces in all other open channels, is zero. No argument above proves or refutes that statement for the fixed smooth halo. Bare diagonal definiteness, shell reciprocity, and the existing `Q` coercivity do not by themselves imply it.

## 6. A further actual result: zero scalar still permits bounded receiving work

A zero scalar does **not force failure of receiving work**. In fact the actual optical identity removes the zero-scalar obstruction for a compact family of nearby eccentric occupied receivers, assuming the regular inverse exists. This is a different conclusion from a bounded full field norm.

Here are the precise local assumptions. Use the actual source-aligned equation in Section 4, with both complete regular boundaries `R_+/-(nu_c+x)` and `r_+/-(nu_c+x)` uniformly `C^alpha` through zero, and assume `A_+/-=I-R_+/-(nu_c)` are invertible. Assume one isolated critical source channel as above and regular coarea traces for all other channels at `nu_c`. Let `Q_rec` be a compact family of actual eccentric receiving orbits, with harmonics `k` whose frequencies can meet a small fixed neighborhood of `nu_c`. There are only finitely many such `k` because `Omega_->0`. Put `omega(q)=k*Omega_i(q)`, `delta(q)=omega(q)-nu_c`, and `Z={q:delta(q)=0}` on each receiving chart. Require

1. orbit extraction `m_q(phi)=phi_{i,k}(q)` is uniformly `gamma`-Holder in `q` as a functional on `Y_gamma`;
2. every regular point of `Z` lies where `w_i>0` (or is a limit of such points on the same regular resonant set), and the only singular point of `Z` is the designated Morse point with its matching harmonic;
3. the geometric error bound `dist(q,Z)<=C*|delta(q)|^(1/2)` holds near `Z`.

These are actual geometric conditions, not a frequency gap. Conditions 1 and 3 follow on compact eccentric charts from smooth action dependence and a regular/Morse level-set description, respectively. For a regular level the stronger distance bound is `C*|delta|`; for the Morse extremum it is `C*sqrt(|delta|)`. The theorem below does not assert these conditions at the entire circular line or at a flat support boundary where no positive-weight resonances approach.

**Theorem (projected local work in the zero-scalar case).** Under these assumptions, if

    a_0,+ = ell(A_+^-1 v_0)=0,

then the contribution of a sufficiently small fixed frequency neighborhood of `nu_c` to receiving work is bounded uniformly in time and in `q in Q_rec`. No strict nonzero dressed scalar is required. The advanced scalar is also zero, since the real physical operator gives `A_-=conjugate(A_+)`, with `v_0` and `ell` real.

**Step 1: source-aligned boundary expansion, including the jump.** Put

    p_+/-=A_+/-(x)^-1*r_+/-(x),
    V_+/-=A_+/-(x)^-1*v_0,
    a_+/-=ell(V_+/-), c_+/-=ell(p_+/-).

The exact rank-one formula is

    U_+/- = p_+/- + V_+/-*Lambda_+/-(x)*(b+c_+/-)
                                      /(1-a_+/-*Lambda_+/-(x)).

Since `a_+/-(0)=0` and `a_+/-` are `C^alpha`, the denominator tends to one and is bounded away from zero on a small fixed neighborhood. Define constant field vectors

    D_+/- = V_+/-(0)*(b+c_+/-(0)).

For any fixed `0<alpha'<alpha`, subtraction of the leading field gives

    U_+/-(nu_c+x)
        = p_+/-(0)+Lambda_+/-(x)*D_+/-+E_+/-(x),
    E_+/- in C^(alpha'),  E_+/-(0)=0.                            (ZE)

This is stronger than the pointwise error `O(|x|^alpha*log^2(1/|x|))`. To justify it, write every error as a sum of a Holder coefficient vanishing at zero times `Lambda` or `Lambda^2`, multiplied by a bounded Holder inverse of `1-a*Lambda`. A `C^alpha` function vanishing at zero, multiplied by any fixed power of `log(1/|x|)` or by its bounded one-sided imaginary constants, extends as `C^(alpha')` for every `alpha'<alpha`. The elementary proof splits `|x-y|` at half `min(|x|,|y|)`; in the near case use the derivative of the logarithm, and in the far case use the vanishing Holder bound. This proves the asserted uniform Holder remainder without differentiating `R`.

On the minimum chart,

    Lambda_+/-(x)=lambda(x)+log(eta-x)+/-i*pi*1_{x>0},
    lambda(x)=log(1/|x|).

Consequently the receiving jump density, if the field is represented by that jump, has the exact local structure

    m_q(U_+-U_-)/(2*pi*i)
       = C(q)+A(q)*lambda(x)+B(q)*1_{x>0}+rho(q,x),             (JD)

where `rho` has a uniformly positive Holder exponent and

    A(q)=m_q(D_+-D_-)/(2*pi*i),
    B(q)=m_q(D_++D_-)/2.

The smooth variation `log(eta-x)-log eta` is included in `rho`. The constant `C(q)` is bounded. Formula (JD) allows `D_+!=D_-`; no unjustified equality of the leading logarithmic boundary vectors is assumed. The same proof works directly with the causal upper boundary used by the damped Parseval formula in Theorem C of the source: its density has `A(q)=m_q(D_+)` and `B(q)=i*pi*m_q(D_+)`, up to the fixed transform normalization. Thus local work can also be defined from the actual causal boundary, without inferring a spectral jump merely from an operator norm.

**Step 2: actual optical cancellation on the receiving level.** If `q in Z` is regular, (OI), applied on each boundary side, gives

    m_q(V_+(0))=m_q(V_-(0))=0.

The weights are positive there, and continuity turns zero weighted square integral into pointwise zero on the regular resonant curve. At the designated critical receiver, this is exactly the assumed scalar zero `ell(V_+/-(0))=0`. Therefore

    A(q)=B(q)=0 on Z,
    |A(q)|+|B(q)|<=C*dist(q,Z)^gamma
                      <=C*|delta(q)|^(gamma/2).               (RC)

This is the actual receiver-adapted cancellation that bare diagonal arguments miss. It uses the physical reciprocal kernel and the sign `w>0` at the open resonances. It does not assert that `V_+(0)` or `V_-(0)` is the zero field.

**Step 3: uniform shifted logarithm/step work estimate.** Fix a smooth cutoff `chi`, equal to one near zero and supported in `(-eta,eta)`. For `0<d=|delta|<eta/4`, direct integration estimates give

    sup_t |integral chi(x)*lambda(x)
              *(exp(-i*(x-delta)*t)-1)/(x-delta) dx|
                   <=C*(1+log^2(1/d)),

    sup_t |integral chi(x)*1_{x>0}
              *(exp(-i*(x-delta)*t)-1)/(x-delta) dx|
                   <=C*(1+log(1/d)).                         (SL)

For the logarithm, split first at `|x-delta|=d/2`. On the inner interval subtract its value at `delta`; the derivative is bounded by `C/d`, the remainder has bounded quotient integral, and the constant term is bounded by `C*(1+log(1/d))` through the sine-integral cancellation. On the exterior, the portion `|x|<=2d` contributes `C*(1+log(1/d))`, while `|x|>2d` is bounded by `C*integral_(2d)^eta log(1/x)/x dx`, which is `C*(1+log^2(1/d))`. The cutoff terms have uniform constants. For the step the same split uses a constant on the inner interval and `integral_(2d)^eta dx/x` on the outer interval. This proves (SL) for either sign of `delta`.

Multiplication by (RC) makes both bounds uniform down to `delta=0`, since `d^(gamma/2)*log^2(1/d)` is bounded. At `delta=0` the two coefficients are exactly zero, so their contribution is zero without any `0*infinity` convention. The bounded constant term times `chi` and the uniformly Holder remainder have uniformly bounded work by the ordinary Dini/sine-integral lemma. This proves the theorem.

**Exact critical receiver without the optical step.** A simpler identity already shows the scalar cancellation at `q_c`:

    ell(U_+/-)=(c_+/-+b*a_+/-*Lambda_+/-)
                            /(1-a_+/-*Lambda_+/-).

When `a_+/-(0)=0`, this is `c_+/-(0)+O(|x|^alpha*log(1/|x|))`, hence locally Dini. The optical theorem is needed to make the conclusion uniform over *other nearby receiving orbits*, since their receiving functional differs from `ell`.

**What this changes.** In this compact eccentric, isolated-Morse setting, failure of strict scalar screening need not stop a receiving-work proof. The unscreened logarithmic field direction is invisible to every receiving trace at its own critical frequency and loses its possible logarithmic growth fast enough at nearby receivers. The theorem remains conditional on the complete regular inverse and regularity, and on the stated receiving geometry. It is not the global actual-halo work bound, and it does not fill the circular/support-edge leaves or nonlinear path control. It shows that zero `a_0` alone is insufficient to obstruct bounded local receiving work.

## 7. Self-audit and continuation

Claim card: for the actual two-species shell operator at one isolated positive Morse minimum, prove the finite-epsilon reciprocal identity, its boundary flux consequence under stated regularity, the bordered inverse expansion under its stated invertibility, and the zero-scalar projected local work theorem under a complete regular inverse and explicit receiving geometry. No universal invertibility, no actual equilibrium critical point existence, no absence/existence of an embedded mode, no global-in-frequency work bound, and no nonlinear confinement theorem are claimed.

Dependency/obligation audit:

| Obligation | Status |
|---|---|
| Species, feedback sign `-w*nu/(nu-z)`, and action measure | Passed against raw full-feedback definitions |
| Morse coefficient and sign `v_0=-beta*P e_c` | Passed by direct coarea derivation |
| Reciprocity and indefinite actual field form | Passed by integration by parts and explicit inverse of `H` |
| Finite-epsilon optical identity | Passed by symmetry of the actual continuous kernel; no field inverse used |
| Boundary optical identity | Conditional on complete finite-part norm continuity/invertibility and regular coarea traces |
| Bordered expansion and finite-part invariance | Passed by exact block algebra/Neumann expansion |
| Actual bordered injectivity | Incomplete: equation (BT) has not been excluded |
| Passage from spectral jump to local bounded work | Conditional on actual jump representation; parity matches pinned lemma |
| Zero-scalar source-aligned expansion (ZE) | Passed under the stated complete regular inverse/Holder assumptions |
| Receiver-adapted cancellation (RC) | Passed using the actual optical identity and the stated positive-weight receiving geometry |
| Uniform moving-receiver estimate (SL) | Passed by direct shifted-kernel split; gives the local projected theorem |
| Global/harmonic summation and nonlinear actual paths | Out of scope |

Review provenance: self-review only, after reading the proof-audit skill; coordinator should independently check (OI-eps), the sign in `a_0=-beta*a`, the border convention, and the receiver-adapted expansion/shifted logarithm estimate. The primary audit verdict for an **unconditional actual-halo bound** is incomplete: the complete regular inverse and the global receiving/boundary extension have not been established. Equation (BT) remains the precise obstruction for the stronger full-field screening criterion, but Section 6 proves that its scalar-zero branch need not obstruct local receiving work.

Continuation: first exploit the projected theorem rather than requiring strict scalar screening for receiving work. Prove a complete regular inverse, including a suitable projected version if ordinary `A` is singular, and extend the joint receiving geometry to circular/support-edge cases. For a bounded full field rather than receiving work, pursue injectivity of (BT) via actual orbit-transform/radial unique continuation, or construct an actual transparent solution. The exact (OI) shows what a strict optical theorem would have to prove. Merely quoting `ell(Pe_c)!=0`, the positivity of total `Q`, or a general passive rank-one model would repeat an already identified gap. This route stays open.

## 8. Sources and freshness

Hashes are SHA-256 at reading. All paths below are relative to `/Users/carlzimmerman/new_physics/zimmerman-formula`.

- `reviews/latest_results_push_2026_10_19_codex/KINETIC_SCREENING.md`: `2e5c6fa7d535b64b4e4c6188a5a8d1a70d59aa40dfe8808f468227a646214ddd`.
- `real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`: `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
- `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`: `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.
- `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md`: `ff33f52fb33a7166a10ae5ba0c99b873ae581916286c6eefca2f70f86b880cb4`.
- `CLAUDE_HANDOFF_KINETIC_CONFINEMENT_2026-10-19.md`: `2af7be5626d3c90b7fe646f1cab4ff60fdb3bab15eefcbd644250f809823de71`.

Raw sections read: complete screening memo; full-feedback Sections 1-3 and relevant source statements; exact-smooth model definitions/profile; classical stability definitions and quadratic. No external source was needed for the elementary identities, and no literature/novelty inference was made. Commands used were text-only reads/searches and `shasum`, plus creation of this single new scratch artifact.
