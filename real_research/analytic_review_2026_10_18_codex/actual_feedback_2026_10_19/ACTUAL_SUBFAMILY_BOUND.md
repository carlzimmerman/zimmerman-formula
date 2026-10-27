# A full linear work bound for an actual warm halo subfamily

19 October 2026. Checkpoint ZAR-2026-10-19-10-CX. Parent review LRP-2026-10-19-01; repository base `62bedfa6b6c363eb17ac4a21c24194d847e76f3b`. Analytic work only. This theorem uses the original reciprocal two-species shell kernels and exact smooth density inverse. It concerns the linear field evaluated on equilibrium receiving orbits.

## The theorem and its scope

Fix positive G, a0 and point baryon mass Mb. Put rM=sqrt(G Mb/a0). There exist delta>0 and epsilon_*>0 such that, for every fixed 0<epsilon<epsilon_*, an actual member of the existing smooth halo family with

    ell=epsilon rM,    f=epsilon^2,
    (r0,r1,r2,R)=ell(1,2,3,4)

has positive fixed warmth delta and the following property. For every smooth compact radial fixed-L canonical generator g0 in its open occupied phase region, the full coupled linear solution satisfies

    sup_{t>=0,theta0,i,q in closed occupied actions} |W_i(t;theta0,q)|
       <= C_delta (G Mb/ell) epsilon ||g_hat0||C12.
                                                        (T)

Here L is squared specific angular momentum, dGamma=4pi^2 dr dv dL, and

    W_i=integral_0^t partial_s psi_i(s,r_i(theta0+Omega_i(q)s,q)) ds.

The generator is nondimensionalized by g_hat=g/(ell v_*), v_*^2=G Mb/ell; the C12 norm is on a fixed enlarged dimensionless physical phase box. The constant is independent of t, q, theta0 and sufficiently small epsilon; it can depend on the single fixed positive delta and the fixed cutoff shape. It need not remain bounded as delta tends to zero. The result includes the circular line and flat energy cap, allows both species to gravitate and respond, and includes the complete linear feedback. It assumes no unproved real-frequency inverse or spectral exclusion.

This is an existence theorem for a nonempty **baryon-dominated subfamily**. Its exact M=Ar annulus lies below rM; its total cold mass is at most 4 epsilon Mb. It does not prove (T) for an arbitrary previously selected halo or for an annulus where cold mass dominates. The source files specify a family rather than one parameter-pinned equilibrium. The fixed positive warmth is chosen once, then epsilon is chosen small; no cold-limit argument is used. Nonlinear work along actual characteristics and all-time confinement remain separate targets.

## 1. Scaling in the actual equations

Write x=r/ell, v_hat=v/v_*, lambda=L/(G Mb ell), j=J/(ell v_*), tau=t v_*/ell, and e=E/v_*^2. Let p be exactly the source profile with radii 1,2,3,4:

    p=x S(x-1)                  on [1,2],
    p=x                         on [2,3],
    p=3+integral_3^x [1-S(u-3)]du on [3,4],

continued as zero inside and constant outside. Thus M/Mb=epsilon p, Mt/Mb=epsilon^3 p, and Mf/Mb=epsilon(1-epsilon^2)p. This retains the exact prescribed mass profile.

In units v_*^2 the actual equilibrium potentials are

    phi_f=-1/x + epsilon Vp,
    phi_t=-1/x + epsilon(1-epsilon^2) Vp + epsilon^4 Vp2,
    Vp(x)=-integral_x^infinity p(u)/u^2 du,
    Vp2(x)=integral_x^infinity p(u)^2/u^4 du.

The actual perturbation kernels, with perturbation mass measured in Mb, are

    P_ff=P_ft=P_tf=-1/max(x,x'),
    P_tt=2 epsilon integral_max(x,x')^infinity p(u)/u^4 du.       (1)

The negative cross kernels have not been discarded. No positivity of the field interaction matrix is used.

The uniform geometry and inverse-DF construction in `GEOMETRY_AND_SCALING.md` gives one fixed delta>0 with dimensionless susceptibilities

    w_f=epsilon(1-epsilon^2) mathfrak_w_f,  w_t=epsilon^3 mathfrak_w_t,
                                                        (2)

whose normalized smooth derivatives of each fixed order are uniformly bounded after zero extension at the flat cap and the L endpoints. This follows from homogeneity of the exact density inverse in its target amplitude, uniform orbital Taylor estimates in the Kepler limit, and the fixed exponential edge weights. The normalized target is always the same p'; division by a vanishing density is not used.

For clarity, the quantifiers in this use of the parent construction are important. First choose a common warmth so the inverse error norm is below 1/2 uniformly on 0<=epsilon<=epsilon_g. Bootstrap higher derivatives through its one-derivative smoothing identity. Only then decrease epsilon for the feedback estimate. The original full exact DF construction is a parent input; the new assertion is its parameter-uniform scaling, with the raw argument supplied in the companion geometry proof.

## 2. Frequency transversality on the whole coarea box

The companion proof directly verifies decreasing epicyclic frequencies throughout both tapers for epsilon<=1/4096. The operator estimate needs a little more than transversality on the occupied set: it needs transversality on the entire fixed action rectangle used for the substitution.

Choose, for example, lambda in [1/2,6] and 0<=j<=j_* with j_*>0 small. On this enlarged box the Kepler limit has

    Omega_K(j,lambda)=(j+sqrt(lambda))^(-3),
    partial_lambda Omega_K=-3/[2 sqrt(lambda)(j+sqrt(lambda))^4]<0.

The box is compact and stays away from lambda=0 and escape. The parameter-dependent Morse-period formulas in the companion geometry proof make Omega_epsilon and its derivatives uniformly continuous there. Consequently there is epsilon_box>0 and d>0 such that partial_lambda Omega_i<=-d on the **whole box**, for both species, after shrinking epsilon<=epsilon_box. Shrink the single fixed delta so every occupied action set lies in this box. All associated orbits in the box stay in a fixed positive radial interval I* containing I=[1,4]. This establishes the extension needed for coarea; it is not inferred from occupied-set transversality alone.

Set a=sqrt(j). The action measure is a fixed constant times 2a da dlambda. The maps r_i(theta,a,lambda) and their theta/lambda derivatives are uniformly bounded up to a=0. In these coordinates (2) gives

    sup_{i,a} (||w_i||infinity+Lip_lambda w_i) <= C_delta epsilon,
                                                        (3)

with zero endpoint traces at the fixed lambda box. The flat cap is already encoded by this zero extension. No singular derivative with respect to j is taken.

## 3. The actual upper-closure feedback bound

Use Y=C^(1/2)(I)^2 and a fixed bounded extension to I*. The physical shell kernels have, for every n!=0,

    ||P^(n)(.,a,lambda)||Lip_x <= C/|n|,
    ||Delta_lambda P^(n)||infinity <= C min(|n|^-1,|Delta lambda|).

Indeed partial_x P is a bounded coefficient times the nth Fourier coefficient of the radial sublevel indicator. That sublevel is one interval on the angle circle, whose coefficient has modulus at most 1/(pi|n|). Integrating from a radius above apocenter bounds P^(n) itself. The Lipschitz source-radius kernel and bounded partial_lambda r give the second estimate. The formula remains regular at the circular line.

For phi in Y, its orbit coefficient satisfies

    |phi_n| <= C|n|^-1/2 ||phi||Y,
    |Delta_lambda phi_n| <= C min(|n|^-1/2,|Delta lambda|^1/2)||phi||Y.

At fixed a substitute nu=n Omega_i(a,lambda). Using (3), the actual symbol becomes

    K(z)phi=sum_{i,n!=0} integral nu c_i,n(.,nu;phi)/(nu-z) dnu,

where

    ||c_i,n||Lip_x <= C_delta epsilon |n|^-5/2 ||phi||Y,
    ||c_i,n(nu)-c_i,n(nu')||infinity
       <= C_delta epsilon |n|^-5/2 min(1,|nu-nu'|^1/2)||phi||Y.

The inverse lambda chart has derivative at most C/|n|. Outside its image, clamp lambda to the endpoint, where w=0; the same estimates continue across the frequency endpoints. The a integration stays fixed. This treats the circular line and cap without a missing boundary term.

Interpolating the last difference with the spatial Lipschitz bound gives a C^(1/4) frequency density in Y. For F_i,n(nu)=nu c_i,n(nu),

    ||F_i,n||C^(1/4)(R;Y) <= C_delta epsilon |n|^-3/2,
    length(supp F_i,n) <= C |n|.                         (4)

The companion `SPECTRAL_OPERATOR.md`, section 3, proves the required elementary Banach-valued Cauchy estimate: for a C^beta density supported in an interval of length D, its upper Cauchy transform has uniform supremum and C^alpha upper-closure norm bounded by C(1+log(2+D)) times the density norm, for 0<alpha<beta<1. Subtract the density value on a symmetric unit interval, bound the remainder by its Holder modulus, and integrate the exterior kernel. Boundary increments use min(u^beta,h^beta); Poisson extension gives the closed-strip bound. Taking beta=1/4, alpha=1/8 and summing (4) therefore proves

    ||K||infinity+B(Y) C^(1/8) seminorm <= C_delta epsilon,
                                                        (5)

on 0<=Im z<=1. The notation in (5) means the operator supremum plus its C^(1/8) seminorm, not a norm of the identity. Each fixed-n term tends to zero at large |z|, and the summable majorant |n|^-3/2 log(2+|n|) proves K(z)->0 there.

Choose epsilon_* no larger than 1/4096, epsilon_box and 1/(2 C_delta), also retaining the uniform DF-existence range. The actual real and complex feedback inverse is then the convergent Neumann series:

    sup_{0<=Im z<=1} ||(I-K(z))^(-1)|| <= 2.             (6)

Its C^(1/8) seminorm is at most four times that of K. This is an established small-equilibrium estimate, not a small-initial-amplitude argument. Embedded and threshold kernels are excluded by (6); none are merely assumed absent.

## 4. Initial-data norms and the missing epsilon factor

Let N=||g_hat0||C12 in a fixed dimensionless physical box, with g0 compactly supported in the occupied region. Uniform smooth orbit maps and repeated theta integration by parts give, including one lambda derivative,

    sup_{i,n!=0}(1+|n|)^6 ||h0_i,n||L_infinity(a;C1_lambda)
       <= C_delta epsilon N,
    h0=-w D g_hat0.                                      (7)

The potential psi0=P h0 is smooth, and its needed radial derivatives are O(epsilon N). The analogous six-harmonic norm of w(psi0)_n is O(epsilon^2 N), hence O(epsilon N). These assertions use at most the twelve stated physical derivatives: one for D, six theta derivatives, one lambda derivative and the finite smooth coordinate/kernel derivatives; there is no derivative of g0 divided by w.

Apply the same coarea/Cauchy estimates to these smooth source coefficients. The two unilateral transforms satisfy

    ||hat(Psi1^0)||C^(1/8)+||K psi0||C^(1/8) <= C_delta epsilon N,
    sup_z (1+|z|)[||hat(Psi1^0)(z)||Y+||K(z)psi0||Y]
       <= C_delta epsilon N.                            (8)

The weighted estimate is not a formal expansion near a resonance. Split source harmonics at |n|=|z|/[2(1+Omega_+)]: the lower range is separated from z and its integrated numerators give O(1/|z|); the tail has six powers of harmonic decay and is smaller. This is the explicit source estimate in the companion spectral proof.

One must not infer the desired epsilon factor from ||h0||Q alone, which is generally O(sqrt(epsilon)N). Instead use the actual weight once more. Uniform parent coercivity gives Q0<=C epsilon N^2 and A[h(t)]<=C epsilon N^2, since integral w=O(epsilon). Therefore

    sup_r |m_i[h(t)](r)|
       <= (integral w_i)^(1/2) A[h(t)]^(1/2)
       <= C_delta epsilon N,
    sup_t ||psi(t)||infinity <= C_delta epsilon N.        (9)

The constants in the parent quadratic coercivity are uniform in this normalized family: its positive B_i and restoring-frequency lower bounds remain positive Kepler perturbations on the fixed shell. The fixed radial field matrix is uniformly bounded, so the second conclusion follows from its integral formula. This is the estimate used for the zero receiving harmonic.

The exact Laplace feedback identity, (6), and (8) give for the **full** derivative-field transform

    hat(Psi1)=(I-K)^(-1)[hat(Psi1^0)+K psi0]

the same C^(1/8) and weighted 1/(1+|z|) bounds, each O(epsilon N). No point modes have been subtracted and no source action band is presumed invariant.

## 5. Uniform work on every closed-set receiver

For any receiving orbit in the closed occupied set, its kth coefficient obeys |phi_k(q)|<=C|k|^-1/2||phi||Y, uniformly including the cap. Put omega=k Omega(q). Apply damped Fourier inversion to partial_t psi and the time interval [0,t]. The nonzero kth work coefficient has the oscillatory integral kernel

    [exp(i(omega-nu)t)-1]/(omega-nu).

On |nu-omega|<1 the constant density cancels symmetrically, and the remaining integral is bounded by its Dini modulus. The density has both a C^(1/8) bound and an O(1/|k|) bound near omega from (8). Splitting the Dini integral where those two bounds coincide yields

    sup_t |W_i,k(t;q)|
       <= C_delta epsilon N |k|^-3/2 log(2+|k|), k!=0.  (10)

The exterior part has the same bound by integrating 1/[(1+|nu|)|nu-omega|]. The estimate is uniform in the Laplace damping parameter; let it decrease to zero on the finite time interval. Summing (10) gives the nonzero-mode contribution. The k=0 contribution is the endpoint difference of the zeroth field coefficient, at most twice (9). This proves the dimensionless form of (T). A circular receiver has all nonzero radial coefficients identically zero and is included directly.

Finally W_physical=v_*^2 W_dimensionless, giving exactly the potential unit in (T). The linear label identity also yields

    sup_t ||u_hat_i(t)||infinity
       <= ||D_hat g_hat0||infinity + C_delta epsilon N.

This is a linear estimate. It neither propagates nonlinear label gradients nor replaces equilibrium receiving trajectories by the actual nonlinear characteristics.

## What remains for the broader target

The current theorem gives a genuine actual-model bound, without an unverified spectral leaf, for the stated small-mass family. The user’s broader fixed-halo target remains open outside that family. In particular a large cold-mass ratio cannot be substituted into (6). The companion critical-frequency work studies bordered inversion and receiver cancellation as alternatives to that smallness. General profiles also need boundary-mode observability: an eigenmode with a nonzero field trace at its resonant eccentric cap would give linear work by the exact mean-ergodic identity in the spectral proof. No such actual eigenmode has been constructed here.
