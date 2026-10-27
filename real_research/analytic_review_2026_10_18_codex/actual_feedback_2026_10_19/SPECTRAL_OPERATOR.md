# Actual spherical feedback: a uniform small-susceptibility theorem and a boundary spectral obstruction

19 October 2026. Owner: `/root/actual_spectral`. Assigned base commit: `62bedfa6b6c363eb17ac4a21c24194d847e76f3b`. Analytic only. This new scratch file is the only write. No scientific code, numerical integration, arrays, process inspection/control, prior-file edits, or ledger edits were used.

## 1. Exact target and status

The target is the full self-consistent **linear** field work on every receiving orbit of the closed occupied action set of the actual two-species spherical halo. This is not work along nonlinear characteristics. The definitions of `L,Q,psi,w,Omega,K` and the work `W` are exactly those of the source `full_feedback/RESULT.md`, Sections 1--5. In particular the physical shell kernel is used throughout; the two species are retained.

Two results are proved below.

1. A complete operator/source lemma closes the analytic limiting-absorption estimates for a family satisfying explicit uniform orbit-chart and small **C^1 in L susceptibility** bounds. It includes the circular line and the flat energy cap, and yields a full, whole-occupied-set work bound by a Neumann inverse. These are checkable coefficient assumptions, not an assumption that the desired inverse exists. The geometry/scaling of a proposed weak-cold-mass family is a separate input owned by the coordinator; this note does not independently prove that scaling.
2. For a general fixed halo, an exact spectral-projection identity proves a necessary boundary condition for any proposed mode-projection argument. An eigenmode with a nonzero resonant receiving trace at an eccentric support boundary causes linear receiving work for some arbitrarily small smooth compact canonical data. Interior positivity of `w` does not establish that boundary condition. Existence of such a mode for the actual halo is not proved here.

The general fixed-profile theorem and nonlinear all-time confinement remain open. No eigenmode obstruction is claimed to occur for a specified parameter choice.

## 2. A precise coefficient contract for the positive result

All variables and norms in this section may be nondimensionalized by fixed units for radius, action, time, and potential. The bound concerns physical work after restoring the potential unit. Constants are uniform in the family parameter only when the following bounds are uniform in those chosen units.

For each species use `a=sqrt(J)>=0`. Assume the occupied action set is contained in a fixed box

    B = [0,A] x [La,Lb],       0<La<Lb<infinity,

and its orbital map is defined on that whole box, with radial ranges in a fixed positive compact interval `I*` containing the actual halo interval `I`. The map `r_i(theta,a,L)` is periodic, smooth in theta and L, has uniformly bounded theta and L derivatives needed below, and satisfies the ordinary radial-orbit ordering: after choosing pericenter at theta=0, radius is strictly increasing on (0,pi) and decreasing on (pi,2pi) for a>0. At a=0 radius is constant. Assume

    0<Omega_- <= Omega_i(a,L) <= Omega_+,
    |partial_L Omega_i(a,L)| >= d>0,
    ||Omega_i||C_L^2 <= C_Omega,
    ||partial_L r_i||infinity + ||partial_theta r_i||infinity <= C_r.

The sign of `partial_L Omega_i` is consequently fixed on each species' box. Smoothness up to a=0 is only used through these explicit uniform estimates. No inverse power of a is used.

Extend `w_i(a^2,L)` by zero outside the occupied region inside B. Require that for every a it is Lipschitz in L, vanishes at `La,Lb`, and

    sup_i sup_a (||w_i(a^2,.)||infinity + Lip_L w_i(a^2,.)) <= epsilon.
                                                        (S)

The actual equilibrium's flat cap and flat L edges permit such zero extension; (S) is a quantitative estimate that must still be proved for the chosen family. An estimate on the amplitude of w alone is insufficient.

Use the actual shell kernels

    P_ff=P_ft=P_tf=-G/max(r,r'),
    P_tt=2c integral_{max(r,r')}^infinity M_t(s)s^-4 ds,

with their coefficients uniformly bounded on I*. No smallness of the kernel itself is required. Smooth sources and fields may be extended from I to I* with a fixed bounded extension operator; for C^gamma fields, constant endpoint extension suffices.

## 3. Uniform full-feedback operator lemma

Fix `0<gamma<1`, let `Y_gamma=C^gamma(I)^2`, and put `beta=gamma(1-gamma)`. For every `0<alpha<beta`, the actual feedback operator obeys

    sup_{0<=Im z<=1} ||K(z)||Y_gamma->Y_gamma <= C_gamma epsilon,
    [K]C^alpha({0<=Im z<=1};B(Y_gamma)) <= C_gamma,alpha epsilon,
    ||K(z)|| -> 0 as |z| -> infinity, 0<=Im z<=1.          (3.1)

The constants depend only on the coefficient contract and gamma,alpha. The boundary values are genuine limits of the upper-half-plane operator. In particular, if `C_gamma epsilon<1/2`,

    sup_{0<=Im z<=1} ||(I-K(z))^-1|| <= 2,               (3.2)

and its alpha-Holder seminorm is at most `4 C_gamma,alpha epsilon`. Thus there are no exceptional real frequencies in this argument, and no mode-removal hypothesis is imposed.

### Proof: physical kernel estimates

For n nonzero define

    P_ij^(n)(r,a,L)=(2pi)^-1 integral P_ij(r,r_j(theta,a,L))e^(in theta)dtheta,
    phi_j,n(a,L)=(2pi)^-1 integral phi_j(r_j(theta,a,L))e^(-in theta)dtheta.

The actual shell derivative is a bounded radial coefficient times the Fourier coefficient of `1_{r_j(theta)<r}`. Because the radial sublevel set is one interval on the circle,

    |(2pi)^-1 integral 1_{r_j(theta)<r} e^(in theta)dtheta| <= 1/(pi |n|).

This remains true at turning radii and at a=0. The nonzero harmonic of P is zero above the orbit's apocenter, so integration in r gives

    ||P_ij^(n)(.,a,L)||Lip_r <= C/|n|.                  (3.3)

The physical kernels are uniformly Lipschitz in their source radius. Uniform `partial_L r` therefore gives

    ||P_ij^(n)(.,a,L)-P_ij^(n)(.,a,L')||infinity
        <= C min(|n|^-1,|L-L'|).                       (3.4)

The half-period shift argument in source theta and the uniform bound on `partial_theta r` give

    |phi_j,n(a,L)| <= C |n|^-gamma ||phi||Y_gamma,
    |phi_j,n(a,L)-phi_j,n(a,L')|
        <= C min(|n|^-gamma,|L-L'|^gamma)||phi||Y_gamma.
                                                        (3.5)

### Proof: coarea without a circular-coordinate singularity

Keep a fixed and change L to `nu=n Omega_j(a,L)`. Monotonicity makes this an ordinary one-dimensional substitution, with Jacobian `1/(|n| |partial_L Omega_j|)`. Since `dJ=2a da`, write

    K(z)phi = sum_{j,n!=0} integral nu c_j,n(.,nu;phi)/(nu-z) dnu,

where, up to the fixed factor `2pi C_Gamma`,

    c_j,n(r,nu;phi) = integral_0^A
       [-2a w_j(a^2,L) P_.j^(n)(r,a,L) phi_j,n(a,L)]
       /[|n| |partial_L Omega_j(a,L)|] da,
       L=L_j(a,nu/n).

The integrand is zero when nu/n is outside the image of the L interval. One may clamp the inverse L to the nearest endpoint and multiply by the zero-extended w; since w vanishes at the endpoints, this gives the same coefficient and preserves the estimates across those frequency endpoints. A moving cap causes no moving a integration domain: it is already encoded by the zero-extended w. At a=0 the factor 2a is regular and integrable. In particular no derivative with respect to J, and no a^-1 factor, is introduced.

Equations (S),(3.3)--(3.5), the bounded inverse map
`|Delta L|<=C|Delta nu|/|n|`, and the C_L^2 frequency bound imply

    ||c_j,n(.,nu;phi)||Lip_r <= C epsilon |n|^-2-gamma ||phi||Y_gamma,
    ||c_j,n(.,nu;phi)-c_j,n(.,nu';phi)||infinity
      <= C epsilon |n|^-2-gamma min(1,|nu-nu'|^gamma)||phi||Y_gamma.
                                                        (3.6)

For example the P difference contributes `min(1,|Delta nu|)` after factoring out `1/|n|`, the phi difference contributes `min(1,|Delta nu|^gamma)` after factoring out `|n|^-gamma`, and the w/Jacobian difference is smaller. These estimates also hold across the clipped endpoints because w=0 there and its zero extension is Lipschitz.

Use the elementary interpolation estimate

    ||f||C^gamma <= C ||f||infinity^(1-gamma) ||f||Lip^gamma.

Consequently, with beta as above,

    ||c_j,n||C^beta_nu(Y_gamma) <= C epsilon |n|^-2-gamma.

The support lies in `n[Omega_-,Omega_+]`. Thus `f_j,n(nu)=nu c_j,n(nu)` has

    ||f_j,n||C^beta(R;Y_gamma) <= C epsilon |n|^-1-gamma,
    length(supp f_j,n) <= C|n|.                         (3.7)

The last Holder estimate uses increments at most one, where multiplication by nu costs `C|n|`; larger increments use the sup norm.

### Proof: elementary Banach-valued Cauchy estimate

If a Banach-valued f is C^beta, 0<beta<1, supported in an interval of length D, then

    Cf(z)=integral f(nu)/(nu-z)dnu

has boundary values `PV integral f(nu)/(nu-x)dnu+i pi f(x)` and satisfies

    ||Cf||infinity <= C_beta(1+log(2+D))||f||C^beta,
    [Cf]C^alpha({0<=Im z<=1})
       <= C_beta,alpha(1+log(2+D))||f||C^beta, alpha<beta.
                                                        (3.8)

For completeness, subtract f(x) on the symmetric region `|nu-x|<1`. The remainder integral is bounded by `2[f]_beta/beta`, the subtracted constant contributes a bounded multiple of f(x), and the exterior integral is bounded by `C||f||infinity log(2+D)`. This proves the sup bound uniformly before or after taking a boundary limit. For horizontal boundary increments h with 0<h<1, the difference of the near remainders is bounded by

    C[f]_beta integral_0^1 min(u^beta,h^beta)/u du
      <= C[f]_beta h^beta(1+log(1/h)).

The exterior difference is at most `C[f]_beta h^beta log(2+D)`, and the explicit `i pi f` term is C^beta. This gives C^alpha for every alpha<beta. The same bounds extend throughout the upper closure: the upper Cauchy value is the Poisson convolution of its boundary value, obtained by inserting the scalar Poisson kernel `eta/[pi(x^2+eta^2)]` and using its elementary Cauchy-kernel convolution identity. Horizontal increments contract under this convolution. For vertical increments use the Poisson semigroup and `integral P_eta(x)|x|^alpha dx=C_alpha eta^alpha`, valid because alpha<1. This proves (3.8) for arbitrary pairs of points in the closed strip.

Applying (3.8) to (3.7) and summing the convergent series

    sum_{n!=0} |n|^-1-gamma log(2+|n|)<infinity

proves the two uniform bounds in (3.1), with convergence in operator norm including the boundary. Each fixed n term tends to zero at infinity; the summable uniform majorant proves the final assertion. The Neumann series and the resolvent identity prove (3.2) and the stated inverse seminorm. QED.

## 4. Complete source estimate and the resulting whole-set work bound

Let `h0=-w Dg0` with `g0` a smooth radial canonical generator compactly supported in the open occupied phase region. Let `psi0=P h0`. Define the explicit initial-data quantity

    B6(h0) = sup_{i,n!=0} (1+|n|)^6 [
        ||h0_i,n||L^infinity_a(C_L^1)
       +||w_i (psi0_i)_n||L^infinity_a(C_L^1) ],
    N6(h0) = ||h0||Q + B6(h0).

It is finite for every such generator. To see this directly, compose the smooth physical generator with the smooth orbital map and integrate by parts repeatedly in theta. This also controls one L derivative. The factors w and Omega are smooth and fixed, and `h0_n=-i n Omega w g0_n`. Finally psi0 is a smooth radial field because h0 is smooth and compact. The claim concerns finiteness and uniform estimates in this stated norm; it does not assert uniform bounds in a low C^k generator norm.

Repeating the fixed-a coarea argument with source `h0_n` instead of `-w phi_n` gives

    hat(Psi1^0)(z) = sum_n integral nu b_n(.,nu)/(z-nu)dnu.

Repeating it with source `w(psi0)_n` gives `K(z)psi0`. The same calculation, now with source and one L derivative bounded by `B6(1+|n|)^-6`, gives for the numerator coefficients `f_n=nu b_n`

    ||f_n||C^beta(R;Y_gamma) <= C B6 (1+|n|)^-6,
    supp f_n subset n[Omega_-,Omega_+].

There is actually one additional n^-1 from the shell/coarea factors, but it is unnecessary. By (3.8) both transforms are uniformly C^alpha on the upper closure. They also obey the needed weighted decay:

    sup_{0<=Im z<=1} (1+|z|)
       [||hat(Psi1^0)(z)||Y_gamma+||K(z)psi0||Y_gamma]
       <= C B6.                                        (4.1)

Here is the explicit high-frequency argument. Set Z=|z|>=2 and split at `|n|=Z/[2(1+Omega_+)]`. On the smaller n range the support satisfies `|nu|<=Z/2`, so direct integration gives `C Z^-1 ||f_n||infinity |n|`, whose sum is `O(B6/Z)`. On the larger range use (3.8) and sum `(1+|n|)^-6 log(2+|n|)`, giving `O(B6 Z^-5 log(2+Z))`. Bounded Z is covered by the uniform Cauchy estimate. Thus (4.1) holds without a formal asymptotic expansion or a parity assumption.

If `C_gamma epsilon<1/2`, Sections 3--4 prove hypotheses (K) and (F) of the source Theorem C, with exceptional set E empty. Therefore for the actual linear solution

    sup_{t>=0,theta0,(i,q) in closed A_i} |W_i(t;theta0,q)|
        <= C_(gamma,alpha,coefficient contract) N6(h0),
    sup_t ||u_i(t)||L^infinity(closed A_i)
        <= ||Dg0||infinity + C N6(h0).                  (4.2)

The receiving set is the **entire closed occupied set**, rather than a smaller eccentric band. Its positive frequency lower bound and bounded velocities are already in the contract. At J=0 all nonzero receiving harmonics vanish exactly, and the zero harmonic is controlled by the field endpoint difference. The cap and flat L edges enter the source integral by the zero extension explained above and enter the receiving estimate through the uniform orbit bounds. None are discarded. The constant is uniform for a family only when every stated coefficient bound and the smallness margin are uniform.

This proves the small-susceptibility implication completely. To obtain a nonempty actual family one must separately establish the uniform dimensionless orbit box, monotonicity, and estimate (S) for the particular exact equilibria. The original source's existence theorem by itself did not state that quantitative family estimate.

## 5. Exact boundary obstruction to a general mode-projection argument

This section does not assume Section 2's smallness contract. Take the actual halo energy Hilbert space `(H,Q)` and the selfadjoint operator `H=iL` from source A1. Write `E` for its spectral projections, `P_omega=E({omega})`, and

    ell_i,k,q(h)=psi_i[h]_k(q),       omega=k Omega_i(q).

The field estimate A3 makes ell a bounded functional even when q is on the support boundary. For every smooth canonical h0, hence h0 in Dom(H),

    lim_{t->infinity} W_i,k(t;q;h0)/t
       = -i omega ell_i,k,q(P_omega h0).                (5.1)

Proof. Since `h(t)=exp(-itH)h0`,

    W_k/t = ell_k [ (1/t) integral_0^t
                        exp(i omega s) exp(-isH)(-iHh0) ds ].

For spectral parameter lambda the averaging multiplier is
`(1/t) integral_0^t exp(i(omega-lambda)s)ds`. Its modulus is at most one and its limit is `1_{lambda=omega}`. Applying dominated convergence to the spectral measure of Hh0 proves strong convergence to `-i P_omega Hh0=-i omega P_omega h0`. Boundedness of ell proves (5.1). QED.

Consequently, a uniform whole-closed-set work theorem for every smooth compact canonical datum necessarily implies

    ell_i,k,q P_(k Omega_i(q)) = 0
    for every q in closed A_i and k!=0.                 (5.2)

This condition is about the **actual** spectral projector. It is not assumed to follow from positive energy.

To prove necessity in the stated canonical class, smooth canonical data compactly supported in the open occupied phase region are dense in H. One direct density construction is to truncate actions away from their boundary and away from J=0, approximate the zero-average angle function by finitely many smooth Fourier modes, and solve `g_n=h_n/[F_E i n Omega]` on the resulting compact interior action set. There w>0 and Omega>0. These are smooth compact physical generators. Weighted truncation is valid by dominated convergence in `A=integral |h|^2/w`, and Q is equivalent to A. Thus if an eigenvector e at omega has `ell(e)!=0`, choose a smooth compact canonical h0 with

    ||h0-e||Q < |ell(e)|/(2||ell||).

Because P_omega is Q-orthogonal and `P_omega e=e`,
`|ell(P_omega h0)|>|ell(e)|/2`. Equation (5.1) gives

    liminf_{t->infinity} sup_theta0 |W_i(t;theta0,q;h0)|/t
       >= |omega| |ell(e)|/2.                           (5.3)

Indeed the modulus of a Fourier coefficient is at most the sup norm in theta0. Arbitrary small amplitude follows by scaling h0 and its generator. For a real eigenvalue pair and real physical data, use the real or imaginary part of h0; at least one has a nonzero projected observation, with at most another factor two in the lower bound.

### Why interior resonance cancellation does not prove (5.2) at the cap

The eigenmode equation gives `u_k=k Omega psi_k/(k Omega-nu)`. If w>0 and the resonant level is regular in the interior, weighted square integrability forces psi_k to vanish along that interior resonant curve. Continuity also gives its closure. This does not cover a boundary resonant level that merely touches the occupied set and has no interior resonant branch. At a flat cap w vanishes to all orders, and a nonzero smooth numerator divided by the normal detuning can still lie in L^2(w). For example in local inward normal coordinate x>=0, `w=exp(-1/x^2)` and detuning x give `integral_0^eta w/x^2 dx<infinity`. This is a local integrability illustration only, not a constructed self-consistent halo eigenmode.

The circular line itself is safe from this particular problem: every nonzero radial receiving Fourier coefficient is identically zero there. At an eccentric cap, the radial observation need not vanish.

For a single eigenmode of frequency nu!=0 there is an even sharper necessary condition for a uniform bound as the receiver varies. For a nonresonant receiving harmonic,

    sup_t |W_k(t,q)| = 2 |nu psi_nu,k(q)|/|k Omega(q)-nu|.

At exact resonance it is `|nu psi_nu,k(q)|t`. Hence bounded mode work on the entire closed set requires a bounded detuning quotient, not merely a zero value at a boundary point. Interior trace-zero plus transverse regularity supplies this quotient near interior resonances; a cap tangency requires an additional argument.

The source A5(c) proves its trace-zero assertion on regular **interior** resonances. Its advertised extension to all closed-set resonances is therefore incomplete unless boundary divisibility is supplied. The source's global (NM_Sigma) hypothesis excludes the corresponding threshold kernels and avoids this gap, whereas a proposed extension that simply projects all real eigenmodes needs (5.2) and the detuning quotient explicitly checked.

## 6. Why an absolute squared-resolvent source norm cannot close the general route

For a selfadjoint H and a vector h define, with value infinity when appropriate,

    R_h(omega)^2 = integral |lambda-omega|^-2 dmu_h(lambda),
    mu_h(B)=||E(B)h||Q^2.

Let Sigma be the actual receiving-frequency set, a locally finite union of nondegenerate closed frequency intervals. If R_h is uniformly finite on Sigma, then `mu_h(Sigma)=0`. In fact it is enough that `integral_J R_h(omega)^2 domega<infinity` on each compact receiving band J. Tonelli gives

    integral_J R_h(omega)^2 domega
       = integral [integral_J |lambda-omega|^-2 domega] dmu_h(lambda),

and the inner integral is infinite at every lambda in J, including its endpoints. Cover Sigma by compact bands. This proves the claim. (Degenerate point bands, if present, are handled directly at their exact omega.)

Thus a source estimate requiring a uniform energy norm of `(H-omega)^-1 h` at every receiving frequency discards all of the source spectral mass in the receiving continuum and can only retain gap spectral components. Smoothness of h in physical variables does not change this exact spectral fact. Oscillatory or signed cross-measure cancellation, such as Sections 3--4 capture through Cauchy densities, is indispensable for general continuum data. This rules out that specific squared-resolvent proof strategy; it does not refute bounded full work.

## 7. Self-review and continuation handoff

Primary verdict for Sections 2--4: **proved as written under the explicit coefficient contract**. Primary verdict for a claim that these hypotheses already hold for an arbitrary exact halo: **not addressed**. The positive result is a sufficient theorem and the quantitative family geometry is its separate remaining leaf.

Primary verdict for (5.1)--(5.3) and Section 6: **proved as written**, self-review. Primary verdict for absence or existence of actual boundary-coupled eigenmodes: **not addressed**.

Checks performed analytically: the coarea Jacobian is `1/|n partial_L Omega|`; the action measure becomes `2a da dL`; the physical shell indicator gives the additional n^-1 essential for summation; the C^gamma output interpolation exponent is beta=gamma(1-gamma); both Cauchy support-length logarithms and the weighted high-frequency forcing estimate are summable; canonical approximation uses only compact regions with w>0; the spectral average applies to Hh0, avoiding an unjustified interchange of the time derivative and a nonsmooth data vector.

Next actions: (i) reconcile the coordinator's actual weak-mass family bounds with the exact contract in Section 2, then independently audit the resulting combined theorem; (ii) for a general fixed profile, seek a projected limiting-absorption theorem with explicit boundary divisibility rather than assuming all eigenmodes harmless; (iii) nonlinear work along actual paths and label gradients remain separate obligations.

## 8. Actual source hashes and allowed operations

- `real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`: `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
- `reviews/latest_results_push_2026_10_19_codex/KINETIC_SCREENING.md`: `2e5c6fa7d535b64b4e4c6188a5a8d1a70d59aa40dfe8808f468227a646214ddd`.
- `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md`: `ff33f52fb33a7166a10ae5ba0c99b873ae581916286c6eefca2f70f86b880cb4`.
- `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/EXACT_SMOOTH_INVERSE.md`: `490b137269ea5c918dae517085974752a3e1bc3d9df4f3e88b99eeccde41a55b`.
- `real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/CANONICAL_RIGIDITY_AND_SUPPORT.md`: `87962d02facb0db1a884423331203c0e78ba5a3b214ab3f35f3bcc03d1ebe466`.

Source operations were text-only `cat`, `rg`, and `shasum`. One `rg --files` discovery was piped to `head`; it did not inspect or control processes. No external mathematical source or novelty claim was used. Research-program and proof-audit skill instructions were read. No available research-attempt skill was listed, so the direct route record above follows the research-program protocol.
