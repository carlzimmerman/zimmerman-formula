# IC17: conserved pressureless baryons in the same action

2026-09-08. **Positive finite background witnesses; full theory OPEN.** This
calculation adds actual pressureless dust to the existing IC17 action. It does
not replace its auxiliary potential with IC14 or IC15, change the pole
pressure, or substitute vacuum-envelope derivatives for matter-dependent
derivatives. Carl's retained-clock hypothesis motivates the continuing
construction; the formulas below are this investigation's calculation.

## Matter coupling and conserved initial data

On the active `eta_up=1` domain, let

    P(X,w)=P0(X,w)+f17(X),   X=exp(-2S)/2,
    f17=(5/64)(2X)^16+epsilon (2X)^2/(1-2X),
    epsilon=10^-5,    mstar=exp(-1/6).

P0 and all other constants are those of IC10, as used by
`ic17_pole_clock.py`. Ordinary massive particles follow the physical metric
`g=exp(2w)gtilde`. Their action gives the Einstein-frame homogeneous dust
term `-b exp(w)`, where `b=m ntilde` is the conserved proper number density
times particle mass. Consequently

    L=P(X,w)-b exp(w),
    P_w-b exp(w)=0,
    rho_total=-P_S-P+b exp(w).

The dust continuity equation is `bdot=-3Htilde b`. Clock shift symmetry
gives conserved positive charge density

    qclock=P_X sqrt(2X)=-P_S exp(S),
    qclock_dot=-3Htilde qclock.

Thus `b=k qclock`, with constant `k=.2`, is a choice of the dust-to-clock
charge ratio as initial data in the frozen units, not a fit to a measured
cosmology. Substitution into the auxiliary equation gives the actual branch
condition

    G(S,w)=P_w+k exp(w+S)P_S=0.

P and all its derivatives in this equation are evaluated before auxiliary
elimination. In particular the pole's large negative P_S near S=0 affects
the dust root even though the pole has no explicit w dependence.

## Chart, root coordinate, and clock probe

The inherited chart is `0<u<1`, with

    w=S(u-1)/(2-u),    tau=-ln(1-u²)>0.

The code brackets the root in tau, computes
`u=sqrt(-expm1(-tau))`, and obtains the small positive number `1-u` from
`exp(-tau)/(1+u)` when forming w. The derivative evaluator is the original
IC17 action evaluator. It explicitly rejects points where that evaluator
cannot resolve the interior chart at the current precision; a rounded
boundary is not accepted as a root. The claimed numerical range stops at
S=10^-8.

At fixed dust number b, define

    Bmatter=P_ww-b exp(w),
    Qbare=(P_SS+P_S)/(2X),
    Q=[P_SS+P_S-P_Sw²/Bmatter]/(2X),
    FX=-P_S/(2X),
    Acan=Bmatter-P_Sw²/(P_SS+P_S)=Bmatter Q/Qbare.

Q is the actual fixed-b auxiliary Schur complement of the clock velocity
Hessian. Acan holds the canonical clock momentum fixed. The homogeneous
resting-particle momentum block adds no auxiliary/particle-velocity mixing.
The code constructs `[[0,Acan],[-Acan,0]]` and computes its singular values
and rank. None of these quantities is borrowed from the vacuum branch.

The ratio `FX/Q` is a clock probe with the dust-number perturbation frozen.
Positive values at most one do not constitute the full coupled dust
velocity/density characteristic analysis, and no such claim is made here.

## Evolution comes from both conservation equations

The positive Einstein-frame Hubble rate follows from
`3mstar Htilde²=rho_total`. Differentiating the clock charge and preserving
the auxiliary equation, including `bdot=-3Htilde b`, gives

    [[P_SS+P_S, P_Sw], [P_Sw, Bmatter]] [Sdot,wdot]^T
        = -3Htilde [P_S,b exp(w)]^T.

The code solves this system and then computes

    Hphysical=exp(-w)(Htilde+wdot),
    r=exp(S-2w-1/6)Htilde.

The latter is the inherited phase activation variable, recomputed on this
matter background. `eta_up(r)` is evaluated from the existing IC17 action.
The vacuum expression for Hphysical is not reused.

An independent derivative along the fixed-k root family is

    G_S=P_Sw+k exp(w+S)(P_SS+P_S),
    G_w=P_ww+k exp(w+S)(P_Sw+P_S),
    w_S=-G_S/G_w.

The independently obtained rate must satisfy `wdot=w_S Sdot`. Notice both
the minus sign and the terms from the varying dust charge. Differentiating
only the vacuum root or holding b fixed along this cosmological family
would give a different trajectory.

## Numerical witnesses

At 70 decimal digits and k=.2:

| S | u | conserved-number density b | clock probe FX/Q | physical H |
| --- | ---: | ---: | ---: | ---: |
| .1 | .495874881316 | .352041851080 | .217275674422 | .900663611766 |
| .01 | .307997548089 | .711563234386 | .064830554332 | 1.30644087720 |
| 10^-4 | .190955539000 | 92.5696591647 | .00004633880566 | 14.7982922435 |
| 10^-8 | .970844866678 | 9.94366092543e9 | 4.992437284e-9 | 153277.833755 |

At all four points the charge is positive, `b=.2 qclock`, the root is
strictly inside `0<u<1`, and FX, Q, Qbare, Bmatter and Acan are positive.
The computed auxiliary block has rank two and the physical metric is
expanding. The activation values r are approximately
`1.08935114, 1.22054103, 12.52916183, 129746.8866`, so all four points
have `eta_up=1`. Their raw auxiliary residuals are below `5e-49`.

A separate logarithmic grid of 51 S values from 10^-8 to .1 checks the
same root, clock signs, physical expansion, activation, and conservation
residuals. The report preserves every row and explicitly records
`interval_certified=false`. This is finite evidence for a locally regular
expanding dust-background family, not a continuous interval proof or a
complete cosmological history. No radiation was needed for this bounded
test, and none has been included.

## Early-pole balance and the next numerical limitation

For fixed k>0, the constitutive expression can be written using

    U(u²)=exp(-tau)(tau²+2tau+2)-2,
    a0²=27 exp(-1/2)/(8 ln(9/5)²).

As S approaches zero on a branch tending to u=1, the pole gives
`P_S~-epsilon/(2S²)`, while the dominant auxiliary term is
`P0_w~2a0² tau²/S`. Balancing G gives the self-consistent leading behavior

    tau²~k epsilon/(4a0² S),
    1-u~exp(-tau)/2,    w~-S exp(-tau)/2,
    qclock~epsilon/(2S²),    b~k epsilon/(2S²),
    Q~epsilon/S³,    FX/Q~S/2.

The original P0_S correction is exponentially suppressed relative to the
pole in this balance. The auxiliary curvature grows approximately as
`8a0² tau exp(tau)/S²`; the Schur correction to Q becomes relatively small.
The Einstein-frame dust-to-clock energy ratio tends to k, and

    Htilde~sqrt[(1+k)epsilon/(6mstar)]/S,
    Hphysical/Htilde -> 1.

These are dominant-balance deductions, not a certified continuation theorem
to S=0. They identify the numerical issue: for still smaller S, exp(-tau)
requires substantially more precision or a direct constitutive evaluator
that retains tau throughout. The present code does not pretend that its
coordinate change alone solves that deep-boundary problem. The pole and
u=1 boundary remain excluded; energy diverges and the clock probe speed
tends to zero. No strong-coupling conclusion follows from positive finite
kinetic coefficients.

## Verification and remaining physical work

Run from this directory:

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_ic17_baryon_background -v
    PYTHONDONTWRITEBYTECODE=1 python3 ic17_baryon_background.py

Seven tests were written first and observed failing before the module was
implemented. They check the four matter roots and vacuum limit, independently
differentiate the raw fixed-b velocity action, verify clock-charge flow and
auxiliary preservation, compare w_S to a five-point derivative along fixed k,
run the 51-point grid, and test reporting failure status. Normal mode returns
1 on failed required numerical checks; otherwise it returns 0. Strict
`--require-full-closure` mode returns 2 when these checks pass.

The independent next obligations are the full coupled dust perturbation
system, radiation and thermal matter evolution, recombination and CMB
observables, strong coupling, sourced MOND and measured gravity, and the
global activation transition. Four baryon points or the supplementary grid
do not supply any of those results.
