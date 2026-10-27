# A macroscopic wall is a state hypothesis, not yet a vacuum coefficient

FSP-008 conditional global-state discriminator, 2026-10-19. All derivatives follow one fixed renormalized parameter path; u=e² is symbolic. No measured alpha, cosmological coefficient, hadronic mass or QCD wall tension is an input. This self-contained partition model is distinct from the earlier fixed-Q Fourier saddle. It does not identify a wall sector in physical theta=0 QCD.

## 1. The precise extensive term required

On round S4 let H=1/a>0, c3=2 pi², Omega4=8 pi²/3, V=Omega4/H⁴, D=H partial_H, W=-log Z, rho=-DW/(4V). For a contribution satisfying rho=A(u)H exactly,

    partial_H W = -4 Omega4 A H^-4,
    W = (4 Omega4/3) A H^-3 + C(u)
      = (32 pi²/9) A H^-3 + C(u).                 (1)

For rho=A H+o(H), integration gives W=(4 Omega4/3) A H^-3+o(H^-3)+C; conversely the latter asymptotic implies the stress asymptotic only with differentiated remainder control. In particular W=V A H would give rho=3 A H/4. A proposed area contribution must be compared with (1), not identified directly with an energy density.

## 2. Defined wall sector and exact derivatives

Let Z0 be an unspecified background partition function, r=Z1/Z0=kappa(H,u) exp[-s], s=c3 sigma(u)/H³, kappa>0, and L=log kappa. Sigma is independent of H along the metric derivative. All formulas below are differences from the same Z0 and do not evaluate W0. The equatorial wall volume is c3/H³. With B=DL+3s and q=L_u-s_u,

    Delta W_forced = -log r = s-L,
    f := rho_forced-rho0 = B/(4V),
    f_u = [D L_u+3s_u]/(4V).                     (2)

For example kappa=k(u)(H/mu)^nu(u) with a fixed reference scale mu gives DL=nu, D L_u=nu_u. A controlled multiplicative correction 1+O((H/mu)^delta), delta>0, has the same limit if its H, u and mixed derivatives obey that order. Thus

    lim f/H = 9 sigma/16,
    lim f_u/H = 9 sigma_u/16.                    (3)

The conditioning is load bearing: the wall's Boltzmann factor has been divided out of the probability normalization by selecting that sector.

The unconditioned model is instead Z=Z0+Z1=Z0(1+r). Put p=r/(1+r). Direct differentiation gives

    Delta W = -log(1+r),
    Delta rho = p f,
    p_u = p(1-p)q,
    Delta rho_u = p f_u+p(1-p)q f.              (4)

The last term is the change in population, including the tension derivative -s_u. Dropping it is not a charge derivative of the partition function. Equations (2)–(4) hold at finite H without a dilute expansion. In particular the unconditioned stress is not obtained by adding the forced wall stress with unit probability.

## 3. A uniform differentiated positive-tension result

Let u range over a compact interval U. Assume sigma is C¹ on U, sigma>=sigma_*>0, and sigma, |sigma_u| are bounded. Fix mu>0 independently of u and set h=H/mu in (0,h0], h0<=1. Assume L has the displayed mixed derivatives and, uniformly on U,

    0<kappa<=C h^-n,
    |DL|+|L_u|+|D L_u|<=C h^-m,                 (5)

for finite C,n,m>=0. These derivative bounds are separate assumptions: a polynomial bound on kappa alone does not bound an oscillating derivative. Then p<=r<=C h^-n exp[-b/h³], b=c3 sigma_*/mu³>0. Equations (2)–(4), with constants absorbing fixed dimensions, give the sufficient estimate

    |Delta rho/H|+|Delta rho_u/H|
       <=C' h^-(n+2m+6) exp[-b/h³].             (6)

Every power is defeated by the exponential. Explicitly, for any integer K>(n+2m+6)/3, exp(b/h³)>=(b/h³)^K/K!, so the right hand side is bounded by a constant times h^(3K-n-2m-6). Consequently

    A_wall(u)=lim Delta rho/H=0,
    lim Delta rho_u/H=0                         (7)

uniformly on U. The two limits and the u derivative commute on this positive-tension interval. This is a theorem about the defined model with (5); it is not a flat-gap theorem or a QCD exclusion theorem. Under the weaker bounds (5), f/H itself need not have the forced limit (3). For (3) one separately needs H³ DL ->0 and H³ D L_u ->0, uniformly for a differentiated statement.

## 4. Radius entropy and the sign of a wall addition

Polynomial location, orientation and determinant factors are included in kappa. More generally subarea entropy L=o(H^-3), with derivative controls of the corresponding order, does not cancel a fixed positive area action. An area entropy can be parameterized exactly as

    kappa=exp[c3 eta(u)/H³] kappa_poly,
    tau=sigma-eta,
    r=kappa_poly exp[-c3 tau/H³].                (8)

Apply (2)–(7) with sigma replaced by tau, rather than retaining sigma after changing the action. If tau is bounded positive, the contribution vanishes. If tau is bounded negative and kappa_poly has controlled polynomial derivatives, p->1 and

    lim Delta rho/H = 9 tau/16 <0.              (9)

At tau=0 identically on a coupling neighborhood, controlled polynomial kappa_poly gives A_wall=0 and its differentiated limit zero. Merely cancelling the exponential is therefore insufficient to produce a nonzero linear term. Short distance wall entropy may already be included in a renormalized tension; (8) is a bookkeeping model, not permission to count the same entropy twice.

There is a useful exact sign constraint. With positive sector weights and a present background 1, Delta W=-log(1+r)<=0. If Delta rho=A H+o(H) exists, equation (1) forces A<=0. A positive nonzero A would require Delta W to diverge positively as H^-3. Positive finite-H wall stress in (4) is consistent with this constraint because its coefficient in the limit is zero. This argument also applies to any positive sum of wall sectors normalized to the same Z0. It does not constrain an unknown area term already in W0. Complex weights or a different reference/state are outside this model.

## 5. Multiple walls and degenerate vacua

For finitely many wall sectors n=1,...,N with r_n=kappa_n exp[-n s], let r_0=1, p_n=r_n/(sum_j r_j), B_n=D log r_n, q_n=partial_u log r_n, B_0=q_0=0. Exactly,

    Delta rho = <B>/(4V),
    Delta rho_u = [<B_u>+Cov(B,q)]/(4V).         (10)

Each fixed n has a positive tension cost. A finite family obeying uniform analogues of (5) is exponentially suppressed, including its u derivative. A forced n-wall sector instead has A=9 n sigma/16 when the prefactor derivatives are subarea. Finite wall degeneracy only changes kappa_n.

For M fixed independent binary wall opportunities, Z/Z0=(1+r)^M and Delta rho=M p f. If a smooth effective M(H,u) is used, differentiation must also act on it:

    Delta rho=[(DM)log(1+r)+M p B]/(4V).         (11)

Polynomial bounds on M and its H,u,mixed derivatives preserve suppression. An integer M(H) with jumps has no ordinary radius derivative at a jump; (11) describes a stated smooth effective model or an interval of constant integer M, not a silent differentiation of an integer count. A Poisson gas has Z/Z0=sum_n r^n/n!=exp(r), hence Delta rho=r B/(4V), with the analogous derivative r(B_u+qB)/(4V). Any polynomial increase of the expected number remains suppressed. An exponentially growing number of opportunities may invalidate (5); it is an extra physical entropy input, and in this positive-weight model a nonzero resulting area term has the sign constraint above. Nonintersecting global walls on S4 need not be independent: these examples specify partition models, not their geometric realizability.

A finite radius-independent number g(u)>0 of exactly degenerate background vacua contributes -log g to W and no stress. Relative wall weights are divided by g. A radius-dependent polynomial degeneracy with controlled logarithmic H and mixed derivatives contributes O(H⁴), hence no A. Bulk-nondegenerate vacua require their actual bulk free energies in Z0; degeneracy alone does not provide an area action.

## 6. Tensionless and critical limits require a new analysis

Zero tension invalidates the uniform lower bound. If sigma=0 on an interval and the remaining prefactor is polynomial with bounded logarithmic radius and mixed derivatives, equations (2),(4) still imply Delta rho/H and its u derivative vanish. This does not describe an interacting critical wall theory, whose fluctuation measure might violate the assumptions.

A particularly simple noncommuting derivative is kappa=k>0, sigma(u)=a u, a>0, u>=0. At each u>=0, A_wall=0, but exactly at u=0,

    lim_{H->0} partial_u(Delta rho/H)|u=0
       = 9 a k/[16(1+k)].                       (12)

Thus the derivative of the limiting zero function differs from the limit of the derivatives at the critical endpoint. It cannot be imported as a physical charge slope without uniform control. More generally for kappa=k h^nu and tau(u_c)=0, tau_u(u_c)=a, one obtains

    lim partial_u(Delta rho/H)|u_c
       = (9a/16) p_*,
    p_*=0 (nu>0), k/(1+k) (nu=0), 1 (nu<0).    (13)

This follows because the additional population term at criticality is proportional to nu p(1-p), which vanishes for nu!=0, and nu=0 kills it directly. It illustrates dependence on the independently unspecified measure. Varying tension as an explicit function of H changes D sigma and must be differentiated in the action; substituting sigma(H) into the fixed-parameter result is invalid. Wall interactions, a critical continuum limit and its measure require microscopic input and are not settled here.

## 7. The equatorial saddle is itself a physical obligation

The round metric is ds²=a²[dchi²+sin² chi ds²_(unit S3)]. A displaced latitude wall has area c3 a³ sin³ chi. At chi=pi/2 its first derivative vanishes and its second derivative is -3 c3 a³. A positive pure-tension equatorial wall therefore has a decreasing-action homogeneous displacement, rather than being a stable minimum of this area functional. Keeping it as a positive semiclassical sector requires an explicit constraint, state prescription, additional stabilizing terms, or an analysis of that unstable mode. The partition ansatz above is conditional even before identifying microscopic wall parameters. This geometry calculation neither forbids other wall saddles nor identifies physical QCD walls.

## 8. Scope and first missing physical input

The conditional model supplies an exact way in which an enforced global three-dimensional defect would make an H-linear stress: its coefficient is 9 sigma/16. It also proves why inserting that cost into an ordinary unforced positive-tension vacuum sum gives a different answer, zero. An unforced model needs failure of the positive-tension/prefactor bounds, a compensating exponential population, or a critical global state to yield any nonzero coefficient; a positive coefficient relative to Z0 additionally conflicts with the positive-sum sign constraint. These alternatives need their own absolute background normalization and state definition.

Nothing here proves that physical theta=0 QCD has such walls, fixes sigma or sigma_u, supplies W0, or computes the full A_rho, proton mass response, R(alpha) or a principle selecting alpha. Theta=pi QCD walls and axion walls are not used as evidence for the physical theta=0 vacuum. The next discriminating input is a microscopic, globally normalized partition/state prescription on S4 establishing whether a macroscopic wall sector is forced or populated, with its tension, measure and mixed derivative under the same parameter matching. The prior sphere/proton/sea calculations do not supply that input.
