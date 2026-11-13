# Independent audit of the perspective compensation class

**Verdict: correct only after a stated restriction.** The proposed action is
indeed convex in Q and concave in positive Pi at every finite Q>0. Positive
enthalpy, and hence the claimed healthy scalar-principal branch, requires an
additional domain condition; it holds on Q>=1, Pi>=0 away from the empty
degenerate point. It does not hold on all Q>0. The class-specific pressure
intercept obstruction is valid. No unconditional impossibility theorem for
all nonmultiplicative H follows.

This review is independent of the author's checker. Twenty-two exact checks
are retained in repair_run. The original reviewed derivation is snapshotted
in sources/repair_DERIVATION.md; the author subsequently incorporated the
Q<1/enthalpy qualification. The separate static-lane reviewer owns the
numerical target-pressure comparison; I do not claim to have independently
rerun that galaxy-target calculation here.

## Construction and joint domain

Let C,L,Pic>0, x=Q-1, u=Pi/Pic>=0, S=exp(-u³),

    t=x²/(L²Q),
    B=CL²Q(1-exp(-t)),
    H=F-B+BS-Q Gamma(u),     F=Cx²,
    Gamma(0)=Gamma_u(0)=0,
    Gamma_uu=9CL²u^4 S.

The inequality `0<=1-exp(-t)<=min(t,1)` proves
`0<=B<=min(F,CL²Q)`. Independent differentiation gives

    B_QQ=C exp(-t)[2-(Q²-1)²/(L²Q³)] <=2C,
    H_QQ=2C-(1-S)B_QQ >=2CS>0,
    H_PiPi=S[9u^4(B-CL²Q)-6uB]/Pic² <=0.

At finite u>0 the last inequality is strict. At u=0, H=F and
H_Pi=H_QPi=H_PiPi=0. These are genuinely joint-domain inequalities, not tests
along a selected Q(Pi) path. Extending S=1,Gamma=0 to negative Pi gives a C²
clamped action with the same algebraic inequalities, but changes that branch
of the theory. Original one-sided stiffness, if retained separately, makes
D=H_PiPi-gamma more negative on positive Pi.

There is no uniform positive lower bound for H_QQ: at Q=1 and u increasing
without bound it approaches zero. Thus strict positivity at each finite point
is not a uniform coercivity or nonlinear well-posedness theorem.

## Positive enthalpy has an exact branch condition

Convexity and concavity alone do not prove physical health. At Pi=0,

    n_eff=Q H_Q=2C Q(Q-1),

which is negative for0<Q<1. The full Q>0 statement must therefore be restricted.
There is a constructive positivity proof on Q>=1. Write R=F-B. Since
`R_QQ=2C-B_QQ>=0` and R_Q(1)=0, R_Q>=0 there; the explicit B_Q formula also
gives B_Q>=0. Then

    n_eff = Q(R_Q+S B_Q)+Pi-uB S_u+Q(u Gamma_u-Gamma).

Every term is nonnegative: S_u<=0, and convex Gamma with Gamma(0)=0 has
`u Gamma_u-Gamma>=0`. Away from Q=1,Pi=0 the relevant branch has positive
enthalpy. Separately retained original stiffness adds gamma Pi², also positive.
Together with H_QQ>0 and D<0 at positive Pi, this removes the particular local
positive-D principal obstruction on that branch. It does not prove that the
domain is invariant or that every finite-wavelength mode is healthy.

## The QPi slope is exactly a boundary

The identity is covariant, not merely an artifact of unitary gauge:

    sqrt(-g) Q Pi = partial_mu[sqrt(-g) Q P^mu],

using the tangent QX17 definition `Pi=divP+P.partial lnQ`. A **constant**
multiple of QPi is a spacetime boundary; in unitary gauge tangency makes it
a spatial boundary on each time slice. Q-dependent or Pi-dependent
coefficients would not have this property.

Under H -> H-lambda QPi with constant lambda, H_Q shifts by -lambda Pi,
H_Pi by -lambda Q, and B_current=1+Gamma_original'-H_Pi shifts by +lambda Q.
The two shifts cancel in the exact conserved density
`rho_Q=H_Q+div(B_current P)/Q`; B_current/Q changes only by a constant, so
the exact leaf flux is unchanged as well. The full principal coefficient
`c=B_current+Q H_QPi`, clock energy `QH_Q-H`, and pressure `H-Pi H_Pi` are
also invariant. This verifies that the asymptotic linear slope really is
harmless in this Q-dependent compensation, unlike a term proportional to Pi
alone.

## The pressure intercept bound is valid and sharp within the class

For any Gamma(u) independent of Q that preserves Gamma(0)=Gamma_u(0)=0 and
enforces H_PiPi<=0 for all Q>=1,

    Gamma_uu >=0                             from Q=1, B=0,
    Gamma_uu >=CL² S_uu when S_uu>0          from sup B/Q=CL².

The latter supremum is approached as Q tends to infinity. Consequently, if
Gamma has an asymptotically linear part with a finite intercept,

    Gamma=lambda_u u-J+o(1),
    J=integral_0^infinity u Gamma_uu du
      >=CL² integral_(2/3)^(1/3)^infinity u S_uu du
      =3 exp(-2/3)CL².

The lower bound is sharp for non-strict concavity: choose
`Gamma_uu=CL² max(S_uu,0)`, which is continuous and yields a C² Gamma. Strict
concavity at every positive-Pi point can be imposed with an arbitrarily small
extra positive curvature; then the lower bound is an infimum rather than an
attained minimum. The author's explicit smoother choice has J=3CL².

Changing Gamma's initial linear slope adds only a QPi boundary and cannot
change J. Changing its constant term can shift the intercept, but changes the
FRW clock action/pressure unless separately compensated. The requirement of
unchanged FRW endpoint is therefore load-bearing. Allowing an arbitrary new
Q-dependent compensation or extra stress sector changes the class and is not
excluded by this argument.

## Consequence and limits

After removing the boundary slope, the off-gate remainder is `R(Q)+QJ`.
The QJ term has zero lapse energy and positive pressure QJ; it is not a
cosmological constant. This mathematical consequence and the exact suppression
identity

    QH_Q-H=C(Q²-1)[1-(1-S)exp(-t)]

both check independently. A small Q-1 does not by itself make the remaining
large-pressure state Newtonian. The numerical incompatibility with a specific
weak-field matching target remains conditional on that target, its pressure
budget, and the supplied constants; the static-lane audit checks those numbers.

The repair is a valid counterexample to a broad mathematical claim that no
convex-Q/concave-Pi nonmultiplicative action can exist. It does not evade its
own class's pressure cost. Further counterterms, extra fields, a restricted
state domain, or a changed asymptotic target would require a new joint
variation and health/matching calculation; they are not silently covered by
this class-specific result.
