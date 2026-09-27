# Compensated gate and canonical carrier: latest evolution audit

This continues `RESULT.md` with two tests that its carrier-free plateau could not answer. The retained weighted gate fails an automatic transition-health claim. The **compensated lapse-independent gate (CP)** repairs its frozen derivative block on an explicit parameter window. Canonical Z elimination has a separate strong-convexity theorem, but positive reduced kinetic energy does not follow from that theorem alone.

## 1. The weighted gate adds an unfiltered lapse term

Work first on a frozen one-dimensional flat leaf, with N=exp(n), a=n_x, w=(SU)_x and

    sigma=J(w)+ell(w_x+a w)−theta,  f=G'(sigma), g2=G''(sigma).

For eta=delta n, v=delta U, s=(Sv)_x, t=(Sv)_xx,

    delta sigma=(J'+ell a)s+ell t+ell w eta_x,
    delta²sigma=J''s²+2ell eta_x s.

The exact lapse-weighted gate second variation is

    delta²[N G]=N[G eta²+2f eta delta sigma+f delta²sigma+g2(delta sigma)²].

Keeping the measure is essential: at frozen principal order, the terms
2f ell eta t and2f ell eta_x s cancel under integration by parts. The rank-one g2 square does not cancel. At high k the heat suppresses s,t but does not suppress the background coefficient multiplying eta_x. For the normalized host it contributes

    (cN/2)g2 ell²w²(eta_x)²,
    alpha_eff,UV=alpha+(cN/2)g2 ell²w²,
    2−alpha_eff,UV=(2−alpha)[1−g2 ell²w²/4].

Thus g2 ell²w²<4 is necessary for this frozen UV scalar block. Convexity of the U problem never imposed that inequality. The exact midpoint C4-ramp control alpha=.1,delta=1,ell w=2 has g2=35/16, alpha_eff=681/160 and the frozen scalar cs²=−361/138243 for c2=.01.

The complete frozen lapse/U Schur gap is also checked. Put A=2cN, R=cN g2/2, L=ell w, B=A f C S_k² and z=(J'+ell a+iell k)S_k. Then

    alpha_eff=2+R L²−|−A+R Lz|²/[A+B+R|z|²],
    2−alpha_eff=[A²−R(2AL Re z+L²(A+B))]/[A+B+R|z|²].

A UV bound alone does not control every finite-k coefficient of this diagnostic.

This is a counterexample to automatic positivity at arbitrary frozen state jets, not a constructed global solution satisfying every gravitational constraint. The leading conformal heat-metric calculation is included: on an affine background, delta(Delta_h S_h U)=S_h delta(Delta_h U), and the apparent unsmoothed first-derivative metric terms cancel. It does not amount to an audit of all quadratic curved-background heat vertices.

## 2. CP removes that lapse-gradient dependence

Replace sigma by the lapse-independent expression

    sigma_h=J(DW)+ell Delta_h W−theta,  W=S_h U,

and add the fixed compensator+cN ell a·DW to the common action. At fixed N,h this compensator is linear in U, so it does not change the positive auxiliary Hessian. On a fully active plateau,

    ∫N ell(Delta_h W+a·DW)=∫div(N ell DW)=0.

Thus the compensated plateau restores the intended static kernel exactly, including the alpha normalization repair. The real constant plateau offset is still present; this cancellation does not discard it.

The leading frozen derivative block has

    h=S_k in[0,1],  f in[0,1],  g2>=0,
    Q=1−(1−f)ell h/4,
    D=1+f C h²+(g2/4)h²[(J')²+ell²k²],
    alpha_eff=2−(2−alpha)Q²/D.

For0<ell<4,0<alpha<2,C>=0 and finite coefficients,

    0<Q<=1,  D>=1,
    alpha<=alpha_eff<2.

Consequently the usual reduced frozen host kinetic coefficient is positive and

    cs²=c2(2−alpha_eff)/[(2+3c2)alpha_eff]>0,  c2>0.

In the UV h→0, Q,D→1 and alpha_eff→alpha. A finite upper bound D<=D_max gives a quantitative positive gap through Q>=1−ell/4. This remains a bounded-state principal result; allowing D→infinity loses a uniform lower speed.

The leading compensation and lapse-measure terms are derived, not assumed. The added+ell a·DW changes the principal lapse/U cross from−4cN to−4cN Q. The N-measure term f eta J' DSv has only one spatial derivative; background curvature, coefficient derivatives and the nonprincipal parts of delta S_h similarly need a separate treatment. They are omitted from this frozen derivative block. The result is therefore **not** a proof that every finite-frequency mode on an arbitrary curved background is stable. In unitary gauge these spatial gate terms add no direct velocities; that fact does not replace the full lapse/shift reduction on an evolving solution.

### Changed inactive-branch prediction

For f=g2=0, the static equations give Q U=U_N and U=Q Phi. Thus

    Phi=Q^−2 U_N,
    G_eff(k)/G_N=[1−ell S_k/4]^−2.

The high-k measured normalization remains G_N=G/cN. The maximum fractional response change is(1−ell/4)^−2−1; at ell=10^−6 this is approximately5.000001875×10^−7. This is a model prediction and a parameter control, not a new observational pass. It must be compared with the operative off-branch requirements. The uncompensated alternative would change the fully-on target instead.

### Fixed-background regularity survives compensation

The active-zero condition now uses Delta_h directly, without a lapse drift: for J(DW)<=theta/2 and f>0, Delta_h W>theta/(2ell). The transverse sublevel proof in `RESULT.md` therefore simplifies. Let kappa_N=N_max/N_min, A_N=||a||_N and r=||DU||_N. The compensated auxiliary energy obeys

    E_CP >= r²/2−[2+ell² kappa_N/2]A_N².

This follows by weighted heat comparison and Young's inequality. It supplies the needed H¹ bound on each fixed-background energy sublevel even though the compensator need not be pointwise positive. The positive gate Hessian is unchanged, so the local forward-source regularity and globally Lipschitz inverse statements retain their fixed-geometry/lapse scope. A coercive conserved energy for the complete gravity/carrier system is still missing.

## 3. Canonical Z elimination has a genuine global variational result

The action's pre-elimination Z terms complete to

    V_a=alpha|a|²−2cN|DZ−(a−DU)|²+2cN|a−DU|².

For the exponential carrier, performing the Legendre transform at fixed canonical momentum gives

    H_d=N sqrt(h) exp(−z) epsilon0,
    epsilon0=Σ pi_A²/(2h)+W_d >=0,
    z=Z−mean_h(Z).

At fixed N,h,U and canonical carrier data, the Z-dependent Hamiltonian is

    H_Z=∫N sqrt(h)[M²cN|DZ−(a−DU)|²+exp(−z)epsilon0].

Assume a compact connected smooth leaf, N bounded above and below by positive constants, a−DU in L², cN>0 and epsilon0>=0 in L¹. Fix mean_h(Z)=0. The gradient square is strongly convex, and the exponential term is convex because its argument is affine in Z. Its formal second variation is

    2M²cN||D delta Z||_N²
       +∫N rho_d[delta Z−mean_h(delta Z)]² >= the gradient floor.

Existence follows by the direct method: Poincare gives coercivity, Z=0 is a finite competitor, a weak H¹ subsequence has an almost-everywhere convergent subsequence, and Fatou controls the nonnegative exponential term. The quadratic term is weakly lower semicontinuous. Strict convexity gives a unique mean-zero variational minimizer. At merely L¹ carrier energy, the weak Euler equation can be tested against bounded smooth variations. Smoothness and a bounded H¹ Hessian or source-Lipschitz map need extra hypotheses: L¹ sources are not automatically H^−1 in three dimensions.

This is a stronger and cleaner canonical constraint statement than reading a fixed-velocity block. It does not prove positivity of the reduced momentum Hessian.

### Why that final distinction is necessary

An exact mean-zero two-cell control has Z=(z,−z), momentum p in the first cell and zero in the second, with

    H(z,p)=kappa z²+exp(−z)p²/2,  kappa>0.

For every p there is a unique minimizing z>=0 satisfying

    p²=4kappa z exp(z),
    H_ZZ=2kappa(1+z)>0,
    H_red=kappa z(z+2).

Yet the reduced momentum Schur complement is

    d²H_red/dp²=exp(−z)(1−z)/(1+z),

negative for z>1. This is a counterexample to the implication from auxiliary convexity to reduced kinetic convexity. It is not a completed gravitational solution, and it does not erase the valid canonical uniqueness result. The actual common action still needs its joint momentum/auxiliary reduction on a consistent background.

## 4. A carefully scoped carrier-background calculation

For a homogeneous massless carrier phi=v t in a flat frozen patch, write d=Z−Phi. Before the mean projection correction, the matter quadratic is

    L_m^(2)=chi_dot²/2+v(d−3psi)chi_dot
             +v²(d−3psi)²/4−v k² beta chi−k²chi²/2.

The h-volume projection adds+3v²<psi Z>/2 at second order for nonzero Fourier perturbations, canceling the naive psi Z density cross. This changes gravitational source terms; it leaves the following(d,U) Hessian unchanged.

After Phi elimination, define K=M²cN k², r=v²/(4K), B=D−1>=0 and T=B−cN Q². The auxiliary quadratic is

    K[(r−1)d²−2dU+T U²] + source terms,
    determinant=(r−1)T−1.

The isolated d diagonal flips at r=1, but the joint constraint matrix need not. A joint pole occurs only for T>0, at r=1+1/T. Eliminating the pair in this fixed-velocity quadratic gives the chi_dot² coefficient

    [1+(r+1)T]/[2(1+(1−r)T)].

It is positive under the sufficient controlled condition

    r<min[1,alpha/(2cN)].

In particular, v²<2alpha M²k² is needed for this simple uniformly controlled expansion. Finite-density poles or signs outside it are **not physical counterexamples by themselves**: flat space with nonzero homogeneous carrier energy is not the required gravitational background, and omitted H-dependent lapse/shift mixing can be as important as the small-alpha terms. The same warning appears in the B=0,Q=1 limit. The consistent FRW or other constrained background is the next required calculation, not an optional detail.

## 5. Perspective carrier repair and its positive-domain cost

An explicit further variant replaces the exponential carrier by

    t=1+P_h Z>0,
    L_d=t K−W_d/t,
    H_d=(|pi|²/2+W_d)/t

in fixed local canonical normalization. This is a changed coupling, not a reinterpretation of the exponential action. At fixed W_d>=0 its joint second variation is

    delta²H_d=|delta pi−(pi/t)delta t|²/t
                  +2W_d(delta t)²/t³ >=0.

This exact identity and nonnegativity are Lean-certified. Adding the positive gradient-Z square makes the joint quadratic form strictly positive for a nonzero mean-zero auxiliary variation, and the reduced momentum Schur is positive on a controlled interior class. A quantitative coercivity bound additionally needs lapse/t and momentum-to-t bounds; the identity alone is not a uniform all-state estimate.

The source identity changes: dL_d/dZ=K+W_d/t²=rho_d/t, rather than rho_d. Its leading weak-field value agrees at t≈1. Beyond that regime the common source, stress and background equations must use the new expression.

The exact two-cell no-floor test gives

    H=kappa z²+p²/[2(1+z)],  t1=1+z,t2=1−z>0,
    p²=4kappa z(1+z)²,
    H_ZZ=2kappa(1+3z)/(1+z),
    H_red,pp=1/(1+3z)>0.

It repairs the exponential negative-Schur example. However, the interior branch reaches z=1 at p²=16kappa. Above that value the infimum lies at the excluded vacuum-cell boundary t2=0. The no-floor variant therefore has a precise positive-domain obstruction; no preservation theorem follows from convexity alone.

### A positive vacuum floor repairs this finite-cell boundary

Adding a fixed V0>0 to W_d gives

    H=kappa z²+(p²/2+V0)/(1+z)+V0/(1−z).

Now H diverges at both boundaries and H_ZZ is strictly positive, so a unique interior minimizer exists for every finite p. Its momentum Schur, even before imposing the stationary equation, is

    [2kappa+2V0/(1+z)³+2V0/(1−z)³] / [(1+z)H_ZZ] >0.

Six 40-digit bracketed controls span p=1,5,50 and V0=10^−6,.1; all preserve t_min>0 and positive Schur. The symbolic checks also verify the matching and f+t f' identity of the parent's proposed positive-domain regularizer. The independent continuum fixed-data barrier proof belongs to the assembled route; this finite calculation does not formalize it or establish global time evolution.

V0 is a new positive vacuum-energy input. On the homogeneous t=1 branch it has epsilon=V0,p=−V0. Its magnitude is not derived by adding the barrier. Even with a fixed-data positive auxiliary solution and positive joint perspective Hessian, the moving common metric/clock/carrier system still needs its constraint-preserving evolution and continuation theorem.
