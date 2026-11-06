# Exact off-constraint propagation: independent PF09 audit

**Verdict: proved for the explicitly defined promoted off-constraint
system below.** All six residuals obey a homogeneous normal-transport
system, with no spatial residual derivatives or independent source.
Zero constraints therefore persist while the promoted strong solution
has the bounded coefficients/transport regularity stated below. This
calculation does not assume that Bianchi propagation closes the system.

Base 6bacc5401c; source clock-system SHA-256
adfc42d3431206d9b96dbab1c6eeff61e1c2a34be52c5c46cc8f131358622751.
The author clarified that n(a) uses fully algebraically substituted spatial
gradients and that the u,v inverse uses promoted a, not the literal e(log r).
That distinction is essential off constraint.

## Definitions and exact off-constraint extension

Write E=e(beta) only on the constraint surface; E is otherwise an independent
promoted field. Let

    H=r^2/2-V-W(P)+(Ar-1-gamma r^2)^2/(2gamma),
    h=H_r, R=H_rr, c^2=h/(rR),
    D=(Ar-1-gamma r^2)/gamma, D_r=(A-2gamma r)/gamma,
    rho=rh-H, p=H, p_perp=H+P W_P,
    J=h+P W_P/r,
    S=-(r^2 D_r u+W_P v+2B J)/R,
    Vrate=n(r)/r=-c^2 K+S/r.

The symbol Vrate is a rate, not the constant potential V. Partial derivatives
of Vrate below hold u,v,K and the other displayed independent variables
fixed; Vrate_P includes the derivative W_PP of W_P.

The six residuals are

    Ca=e(log r)-a,
    Cbeta=e(beta)-E,
    CA=e(A)-W_P/r,
    CP=e(P)-D+2P E,
    Cm=e(B)-(K-B)E,
    CH=e(E)-KB-(B^2-3E^2)/2+rho/(2M).

The actual geometric commutator is [n,e]=-(a+Ca)n-Ke. The uniform-
arclength gauge in the candidate local proof gives this identity exactly.
K is fixed by its shift/length equations, not merely assumed to equal the
metric expansion off constraint.

Define e_star by the substitutions

    e_star r=ra, e_star A=W_P/r, e_star P=D-2PE,
    e_star B=(K-B)E,

and by the actual spatial inverse equations for u,v, retaining actual e(K).
Then the promoted acceleration equation is compactly

    n(a)=e_star(Vrate)-(Vrate+K)a.

The inverse can equivalently be written before eliminating n(r)=r Vrate:

    e(u)=W_PP v/r-W_P n(r)/r^3+W_P K/r^2,
    e(v)=D_r n(r)/r+(r/gamma)u-2Ev
            +K(D-2PE)/r+2PB(a+E)/r.

The last term uses promoted a. Replacing it instead by literal e(log r)
would define a different off-constraint system and add 2PB Ca to n(CP).

## Complete residual system

Direct commutation and differentiation give

    n(Ca)=(r Vrate_r-Vrate-K)Ca
              +Vrate_A CA+Vrate_P CP+Vrate_B Cm,

    n(Cbeta)=-K Cbeta+Cm-B Ca,
    n(CA)=-K CA,
    n(CP)=-K CP,

    n(Cm)=-(K+3B)Cm+(E-a)CH
       +(3B^2-E^2+2aE-rho/M)Ca/2
       -(rD/(2M))CA+(W_P/(2M))CP,

    n(CH)=-(K+B)CH-(a+E)Cm+B(a+E)Ca.

These are exact coefficients, not estimates. Vrate's formula above defines
its derivatives explicitly; fully expanded rational versions are retained
in matter_result.json. There is no hidden Cbeta source in the other five
equations for this choice of extension.

For a shorter explicit derivative description, let R_r=H_rrr and
R_A=2D_r-2r, h_A=D+rD_r. Then

    S_r=-[(2rD_r-2r^2)u+2B(R-PW_P/r^2)]/R-S R_r/R,
    S_A=-[(r^2/gamma)u+2B h_A]/R-S R_A/R,
    S_P=-[W_PP v+(2B/r)(W_P+P W_PP)]/R,
    S_B=-2J/R,
    (c^2)_r=(1-c^2)/r-c^2 R_r/R,
    (c^2)_A=h_A/(rR)-c^2 R_A/R.

Hence Vrate_A=-(c^2)_A K+S_A/r,
Vrate_P=S_P/r, Vrate_B=S_B/r, and
r Vrate_r-Vrate-K=(c^2-1)K-2S/r-r(c^2)_r K+S_r.

## Decisive derivation steps

The actual acceleration derivative satisfies

    n[e(log r)]=e(Vrate)-(Vrate+K)[a+Ca].

Subtracting the promoted equation leaves
(e-e_star)Vrate-(Vrate+K)Ca. Since the actual inverse fixes e(u),e(v)
identically, their derivatives contribute no residual difference. The only
differences in this composite derivative are rCa, CA, CP, Cm, proving
the first equation without a discarded derivative term.

The rescaling u=n(A)/r, v=n(P)/r cancels the actual commutator coefficient
against e(r) in n[e(A)] and n[e(P)]. The specified inverse then leaves
exactly -K CA and -K CP. For beta,

    n(Cbeta)=e(B)-(a+Ca)B-K(E+Cbeta)-n(E),

which gives the stated -K Cbeta term as well as Cm-B Ca.

For the geometric equations use exactly

    n(E)=-aB-BE,
    n(B)=-aE+(-3B^2+E^2-p/M)/2,
    n(K)=-e(a)+a^2-K^2+Z,
    Z=B^2-E^2+(p-rho-2p_perp)/(2M).

The native algebra gives two identities needed in this off-constraint
calculation:

    n(rho)=-(rho+p)K-2(rho+p_perp)B,
    e(p)=(rho+p)(a+Ca)+2(p_perp-p)E+rD CA-W_P CP.

The first follows from rho_r=rR, rho_A=r^2 D_r, rho_P=W_P and the
promoted scalar/auxiliary rates. These are algebraic identities of the
extension, not an assumed physical Bianchi law off constraint. Substitution
in n(Cm),n(CH) cancels all e(a),e(K), independent terms and remaining
potential terms, yielding the last two equations.

## Principal character and preservation

In uniform-arclength gauge n=r(partial_tau-w partial_x), every residual
has the same transport speed -w. There is no residual wave block, no
uncontrolled derivative, and no ill-posed residual principal symbol.
If r stays positive and the coefficients above are bounded, with spatially
Lipschitz w, the divided system is a finite-dimensional homogeneous linear
ODE along each shift characteristic. Zero initial residuals remain zero
by Gronwall/ODE uniqueness.

For a joint Lipschitz promoted solution, the calculation is distributional:
first derivatives are bounded, mixed derivatives commute, and the necessary
chain rules involve W_P and W_PP but no W_PPP. Initial zero residuals are
taken as the weak spatial-derivative trace of the compatible initial data.
One must retain this trace in an approximation proof rather than require
the unconstrained smooth approximants to have zero residual themselves.

On zero residuals, the clock/spatial definitions, matter equations, and all
Einstein constraints are restored. The four independent planar Einstein
components are accounted for by CH, Cm, n(B), and the curvature/n(K)
equation. The switch relation is algebraic on the chosen open on-branch
domain; its positivity margins are domain assumptions, not additional
differential constraints. No extra residual is missing for this stated
periodic planar/constant-potential system.

## Off-constraint inverse: two valid safeguards

Weighted coercivity off constraint acquires the quadratic term

    c u^2+b v^2+2 Cbeta u v.

Thus it remains uniformly positive if, for example, b,c>=m and
|Cbeta|<m with a uniform margin (more sharply Cbeta^2<bc). This gives
an explicit off-constraint extension without assuming Cbeta=0.

However a small C0 neighborhood of the fields alone does not control
beta_x and hence Cbeta. For general off-constraint iterates the candidate's
C0 Neumann-operator argument is valid and should be retained unless a
small W1,infinity residual neighborhood is imposed. On constrained
solutions the stronger weighted coercivity bound is automatic.

## Raw checks and provenance

`derive_matter.py` checks the compact Ca identity, CA/CP/Cbeta transport,
zero independent source and absence of spatial residual derivatives;
all six checks pass in `matter_result.json`. Its rational coefficient
output preserves the raw expanded result. `derive_geometry.py` directly
differentiates Cm,CH using the actual commutator; both zero-source and
spatial-derivative cancellation checks pass in `geometry_result.json`.

Commands were `python3` on those two scripts, with stdout preserved in
the corresponding JSON files. No numerical trajectory or sampled
identity was used. Independent delegated audit, 2026-11-06.
