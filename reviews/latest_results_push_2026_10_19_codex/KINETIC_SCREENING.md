# Critical-frequency screening: a bounded analytic route

19 October 2026. Owner: kinetic_route subagent. Base request HEAD: `18a81657e3e77d81f152fa73ca558dbc85ab6414`; newer raw input: commit `25a96db39`, checkpoint ZAR-2026-10-19-09-CL. Scope: analytic only, no scientific code, integrations, array work, process inspection/control, prior-file edits, or shared status edits. This new scratch artifact is the only write. **All-time confinement remains open.**

## Exact change in information

The newest result's B2 proves logarithmic *bare* first-response work at an interior nondegenerate frequency extremum. It explicitly leaves feedback screening open and heuristically mentions possible log-log growth from a 1/log resolvent modulus. A 1/log modulus alone does not establish that growth. The spectral discontinuity and its parity matter.

Below are (i) a proved symmetric frequency-to-work lemma, (ii) a proved rank-one screening algebra with a conditional local work consequence, (iii) an exact positive-energy continuum example in which bare log growth becomes bounded full work, and (iv) the actual shell operator's leading singular coefficient. The example disproves any general inference from the bare logarithm to failure of full work. It is **not** a reduction of the whole halo operator to rank one and is not a confinement theorem.

## 1. A symmetric frequency-to-work lemma

Let 0 < eta < exp(-1), omega real, and let a be a complex-valued density on (omega-eta,omega+eta). Put Lambda(x)=log(1/abs(x)). Suppose

    a(omega+x) = A0 + A1/Lambda(x) + r(x),
    integral_{0<abs(x)<eta} abs(r(x))/abs(x) dx < infinity,

with the *same* A0,A1 for x>0 and x<0. Then

    sup_{t>=0} abs(integral_{-eta}^{eta}
        a(omega+x) (exp(-i*x*t)-1)/x dx) < infinity.

Improper integrals use symmetric truncations for the displayed two even terms; for each fixed t the original integral is ordinary locally integrable because its oscillatory quotient is bounded.

Proof. The r contribution is at most twice its stated weighted integral. The A0 term is -2i*A0*Si(eta*t), uniformly bounded. For the A1 term put b(x)=1/log(1/x), x in (0,eta). Then b(0)=0, b is increasing, and

    integral_0^eta b(x) sin(tx)/x dx
      = b(eta)*Si(t*eta) - integral_0^eta Si(tx) db(x).

The sine integral is uniformly bounded: split at 1 and integrate by parts on [1,T]. Therefore this expression is bounded by 2*C_Si*b(eta). This proves the assertion. In particular, r=O(Lambda^-2)+O(abs(x)^alpha*Lambda^m), alpha>0, any fixed m, satisfies the hypothesis. A plain Dini estimate applied separately to abs(a(omega+x)-a(omega)) would miss this cancellation.

## 2. Rank-one logarithmic screening algebra

Let Y be a complex Banach space, v in Y, ell in Y*, and consider near a real frequency nu_c

    K(z) = L(z) v tensor ell + R(z),
    F(z) = L(z) b v + r(z),
    (I-K(z)) U(z) = F(z).

Here b is scalar. For each boundary side +/- assume R_+/-(nu_c+x), r_+/-(nu_c+x) are alpha-Holder through x=0, alpha>0. Their + and - limits need not agree. Assume A_+/-(x)=I-R_+/-(nu_c+x) is invertible near zero and

    a_+/-(0) = ell(A_+/-(0)^-1 v) != 0.

Suppose L_+/-(nu_c+x) = Lambda(x)+c_+/-(sign x)+O(abs(x)), where the four constants c are bounded. (Changing the sign or scale of Lambda can be absorbed into v.) Then the exact algebra is

    p=A^-1 r, V=A^-1 v, a=ell(V), c=ell(p),
    U = p + V * L*(b+c)/(1-a*L).

Proof: substitute into (A-L*v tensor ell)U=L*b*v+r, or apply ell after multiplying by A^-1. Since a(0)!=0, 1-a*L is nonzero near zero and

    U_+/-(nu_c+x) = P_+/- + Q_+/-/Lambda(x)
      + O(Lambda(x)^-2) + O(abs(x)^alpha * Lambda(x)^m),

for some fixed m (m=2 is more than sufficient), where

    P = p0 - V0*(b+ell(p0))/a0,
    Q = -V0*(b+ell(p0))/a0^2.

The constants P_+/-,Q_+/- depend on the boundary side but **not** on sign x. Bounded changes in L only enter at order Lambda^-2. Consequently the jump density (U_+-U_-)/(2*pi*i), and any bounded scalar observation of it times a smooth frequency factor, has exactly the expansion in Section 1. Thus its local contribution to receiving work at omega=nu_c is uniformly bounded.

This is a conditional local theorem: it requires an actual spectral/jump representation, regularity of the dressed remainder on each side, invertibility of A, and nonzero dressed scalar a. It permits other regular open spectral channels, because the +/- limiting remainders may differ. It does not prove those hypotheses for the halo. It treats one critical frequency; global harmonic summation, multiple coincident critical points and arbitrary receiving frequencies are additional tasks.

The important scalar to test is ell((I-R_+/-(nu_c))^-1 v). Bare ell(v)!=0 does not force this dressed scalar to stay nonzero.

## 3. Exact selfadjoint continuum example: complete proof

Fix nu_c>0 and g>0. On H=L2((0,1),dx) let v(x)=1 and

    H0 f(x)=(nu_c+x)f(x),
    H_g=H0+g*|v><v|,
    Phi_g(t)=<v,exp(-it H_g)v>,
    W_g(t)=integral_0^t exp(i*nu_c*s) d_s Phi_g(s) ds.

All operators here are bounded and selfadjoint, H_g>=nu_c*I, and the flow conserves the positive L2 energy. The initial vector v is smooth. It is also of canonical transport form H0 G, with G(x)=1/(nu_c+x) smooth, so this example does not rely on a missing transport-frequency factor.

For g=0,

    W_0(t)=integral_0^1 (nu_c+x)*(exp(-ixt)-1)/x dx.

Hence Re W_0(t)=-nu_c*log(t)+O(1) as t tends to infinity. To see this, substitute y=tx in the nu_c term; integral_0^t (cos(y)-1)/y dy = -log(t)+O(1), using integration by parts for integral_1^t cos(y)/y. The remaining integral and the sine term are bounded.

For g>0 let mu_g be the spectral measure of v for H_g. For z<nu_c the resolvent equation directly gives

    m0(z)=<v,(H0-z)^-1v>
          = log((nu_c+1-z)/(nu_c-z)),
    m_g(z)=<v,(H_g-z)^-1v> = m0(z)/(1+g*m0(z)).

The second equality follows by solving (H0-z)u+g*v*<v,u>=v and taking <v,u>; no perturbation expansion is used. Since H_g>=nu_c*I, positivity and monotone convergence give

    integral dmu_g(lambda)/(lambda-nu_c)
      = limit_{z up to nu_c} m_g(z) = 1/g.

An atom at nu_c is thereby excluded. Also mu_g has total mass ||v||2^2=1. The spectral representation and boundedness of H_g allow integration first on [0,t]:

    W_g(t)=integral lambda*(exp(-i*(lambda-nu_c)*t)-1)
                     /(lambda-nu_c) dmu_g(lambda).

Therefore the exact estimate is

    sup_{t>=0} |W_g(t)| <= 2*(1+nu_c/g).

Thus the full self-consistent rank-one response has bounded work even though its free response diverges logarithmically. The constant deteriorates as g tends to zero, as it must. This is not a perturbative-smallness bound.

For clarity, on lambda=nu_c+x, 0<x<1, the continuous density is

    rho_g(x)=1/((1+g*log((1-x)/x))^2+(g*pi)^2),

obtained from the imaginary part of m_g(nu_c+x+i0). It behaves as 1/(g^2*log(1/x)^2) near x=0. The possible atom above nu_c+1 is harmless in the work because it is separated from the receiver frequency. This explains spectrally why a 1/log resolvent modulus is compatible with bounded work: its boundary *jump* is 1/log^2 at the one-sided threshold.

### Extension to arbitrary Holder sources in this example

For real f in C^alpha([0,1]), alpha>0, the cross resolvent is

    <v,(H_g-z)^-1 f> = m_f(z)/(1+g*m0(z)),
    m_f(z)=integral_0^1 f(y)/(nu_c+y-z) dy.

Its continuous cross density is

    rho_{g,f}(x)=[f(x)-g*R_f(x)]/
       ((1+g*log((1-x)/x))^2+(g*pi)^2),
    R_f(x)=integral_0^1 (f(y)-f(x))/(y-x) dy.

The identity follows by multiplying boundary values by 1+g*conjugate(m0); the f(x)*log terms cancel. The numerator is uniformly bounded because |R_f| <= 2*[f]_alpha/alpha. Consequently integral_0^1 |rho_{g,f}(x)|/x dx is finite. The sole off-band eigenvalue is separated from nu_c, so its atomic cross measure is harmless. Complex f follows by splitting into real and imaginary parts. Therefore endpoint work is bounded for every Holder source f, including smooth sources compactly cut off near x=1 but nonzero at x=0. This is proved for this model only.

## 4. The actual shell feedback has a rank-one leading singularity

Use the actual checkpoint-09 notation. Suppose q_c is an eccentric interior nondegenerate minimum of Omega_j, w_j(q_c)>0, n>=1 and nu_c=n*Omega_j(q_c). Let P^(n)_{ij}(r,q) be the source-angle Fourier coefficient of the physical shell kernel. On a sufficiently small Morse chart, define the piece of the feedback operator supported there by

    K_c(z) phi = integral_chi [-w_j(q)]*nu(q)*
       P^(n)_{.j}(r,q)*phi_{j,n}(q)/(nu(q)-z) dm(q),
    nu(q)=n*Omega_j(q), dm=2*pi*C_Gamma*dJ*dL.

Then on Y_gamma=C^gamma(I)^2, 0<gamma<1,

    K_c(z) = L(z) B0 + R_c(z),
    L(z)=log(nu_c+eta-z)-log(nu_c-z),
    B0 = -[4*pi^2*C_Gamma*nu_c*w_j(q_c)
           /(n*sqrt(det(D2 Omega_j(q_c))))] * v tensor ell,
    v=P^(n)_{.j}(.,q_c), ell(phi)=phi_{j,n}(q_c).

The cutoff is one near q_c; changing its outer boundary only changes the regular remainder. The one-sided coarea density of R_c vanishes at nu_c with some positive Holder exponent, so R_c has continuous boundary values at nu_c and its jump there is O(abs(nu-nu_c)^a) for some a>0. A maximum gives the analogous reversed interval and logarithm.

Derivation. In Morse coordinates the pushforward of smooth action measure by nu has limiting density 2*pi/(n*sqrt(det(D2 Omega_j(q_c)))). Multiplication by dm gives the constant 4*pi^2*C_Gamma above. At q_c the operator-valued integrand factors as v*ell. The physical P is Lipschitz in both radial arguments, and orbits depend smoothly on actions on this eccentric chart. Uniform radial Lipschitz bounds plus sup-norm action continuity imply Holder action dependence into C^gamma_r by the inequality ||u||Cgamma <= C*||u||infty^(1-gamma)*||u||Lip^gamma. The functional ell_q(phi)=phi_{j,n}(q) is gamma-Holder in q. Hence their product is beta-Holder in operator norm for beta=min(gamma,1-gamma)>0. Restriction to a Morse circle gives O(abs(nu-nu_c)^(beta/2)) variation of its coarea density. Subtract B0; the remainder density is zero at the endpoint. Its Cauchy transform has a finite boundary value there because integral_0^eta x^(beta/2)/x dx converges; the jump is 2*pi*i times that density. Splitting at x=2*abs(z-nu_c) and subtracting the value at the local pole gives Holder boundary continuity with any exponent below beta/2. These are local compact eccentric estimates, with no circular-edge assertion.

The bare scalar ell(v)=K_{jj,nn}(q_c,q_c) is nonzero by the actual diagonal-kernel identity in B2. The corresponding local singularity of the free forcing has the same output vector v, because its numerator at q_c is P^(n)_{.j}(.,q_c)*h_{j,n}(0,q_c). Thus this is the singular alignment required in Section 2, not merely an unrelated rank-one analogy.

What is NOT established: the regular remainder of the complete operator may contain other critical channels; invertibility of I-R_+/- and nonvanishing of the dressed scalar have not been proved for the actual equilibrium. Nor has the full spectral density been reconstructed globally or summed over n. Those are the next leaves. Coincident critical frequencies give a finite-rank matrix version, not the scalar lemma as written.

## 5. Self-review, scope, and next discriminator

Primary verdict: **conditional on a named input** for the actual critical-frequency work bound (the regular dressed inverse and nonzero scalar); **proved as written** for Sections 1-3 and the local leading-coefficient statement of Section 4. Self-review only; this has not received a fresh independent mathematical audit.

Dependency checks:

- Oscillatory work cancellation: directly proved, no absolute-value Dini inference.
- Rank-one inversion signs: checked by substitution, with denominator 1-L*ell(A^-1v).
- Model spectrum and work: the main bound needs only positive selfadjoint spectral representation and the explicitly solved resolvent; it does not depend on the displayed density formula or a claimed absence of singular spectrum.
- Holder-source extension: depends on the explicit scalar rank-one boundary formula; endpoint denominator behaves as log^2 and the sole gap atom stays separated.
- Halo singularity: uses only the actual shell kernel, an eccentric interior Morse extremum, positive w, and the displayed action measure; it does not assert such an extremum occurs for a specified equilibrium.
- Nonlinear paths and label gradients: not addressed.

Priority change: retain an alternative to imposing global (ND). First determine the actual frequency critical geometry analytically. If an isolated Morse extremum is present, do not reject full work from the bare log; isolate its rank-one singularity, then test the regular dressed inverse and scalar. If no extrema occur, the existing regular limiting-absorption route remains natural. This route does not remove the nonlinear all-time confinement gap.

## 6. Actual inputs and hashes at reading

- `CLAUDE_HANDOFF_KINETIC_CONFINEMENT_2026-10-19.md`: `2af7be5626d3c90b7fe646f1cab4ff60fdb3bab15eefcbd644250f809823de71`.
- `real_research/analytic_review_2026_10_18_codex/claude_continuation_2026_10_19/full_feedback/RESULT.md`: `a69a6cfde21ccdd1a9a2fbced2e0613ac99ba1bc6fe3571dbb377d645756d4fb`.
- `real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/RESONANT_WORK_PROGRESS.md`: `e74737fe9f1f5bda5635560e76f86f4978549d403d2a516235afd401ac797c5d`.
- `real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/README.md`: `0b11424ddc82e9dcceff74b606ac75c760174b9fe084e5cc399ebad9ea1c7f9d`.
- `real_research/analytic_review_2026_10_18_codex/canonical_confinement_2026_10_19/AUDIT_AND_HANDOFF.md`: `b93da5f8e8f564b5994d5c067cc441e8953710677f795635752d158d15df4324`.
- `real_research/analytic_review_2026_10_18_codex/nonlinear_radial_2026_10_19/NONLINEAR_COERCIVITY.md`: `ec85b126c078e00f9cd5f364c08f78e9022c83f55228d06a7db1b3279bfe4c92`.
- `real_research/analytic_review_2026_10_18_codex/smooth_exact_2026_10_18/CLASSICAL_RADIAL_STABILITY.md` was read as additional context; its current hash is recorded in the return message after this artifact is written.

Commands used: text-only `cat`, `sed`, `rg`, `git show --stat/--name-only`, and `shasum`; no supplied identity script or scientific code was run. No external mathematical source was used or novelty claim made.
