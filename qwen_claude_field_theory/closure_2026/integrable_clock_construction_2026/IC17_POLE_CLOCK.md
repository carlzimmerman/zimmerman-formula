# IC17: a pole clock with an early radiation-to-clock history

2026-09-08. **New explicit action; constructive early-time result; full
theory OPEN.** The fixed choice `epsilon=10^-5` passes the stated finite
checks without retuning. This construction changes the low-S pressure
itself. Its eight-e-fold history ends at `S=.1`, well before the late
zero-pressure-gradient endpoint; it does not obtain the expansion by
tuning a final state extremely close to that endpoint.

## Phase action and its actual open domain

Retain IC10's covariant first-order fields, constants, primitive, physical
matter metric and boundary prescription. Replace its compact activation
window by the one-sided activation

    eta_up(r)=E(r²-1/2)/[E(r²-1/2)+E(3/4-r²)],
    E(t)=exp(-1/t) for t>0 and E(t)=0 otherwise.

Thus `eta_up=0` for `r²<=1/2` and `eta_up=1` for `r²>=3/4`. This is an
explicit action choice, not an empirical determination. With
`Xtilde=exp(2w)Xphysical`, the new Hamiltonian is

    H17=H10[eta_up]-eta_up exp(-4w) f17(Xtilde),
    f17(X)=(5/64)(2X)^16+epsilon (2X)^2/(1-2X),
    epsilon=10^-5,  m=h0=1,  kappa=6.

The full phase action is `integral sqrt(-g)[2P:Q-H17]+Sm[g,psi]`.
Numerical constants use the existing normalized units. The correction is
defined on the open set

    U={r²<1/2, finite Xtilde>0}
       union {0<2Xtilde<1, finite r}.

On the first, inactive neighborhood it is defined directly as zero before
any pole is evaluated. On the active chart it is the displayed rational
function. These definitions agree smoothly on their overlap because the
activation is flat there. The point `r²=1/2, 2Xtilde=1` is excluded, as is
an active point with `2Xtilde>=1`; no `0 times infinity` is used. The code
enforces this domain and includes invalid-domain controls.

At `p=0`, an entire neighborhood is inactive, so the correction and all
its first jets vanish even when the inactive static state is outside the
pole's active X chart. The previously stated static equations therefore
remain unchanged under the same boundary prescription. This is not a new
proof of baryon-only MOND, lensing, PPN, or global matching.

On `eta_up=1` the same stationary Legendre and conformal transformation
as IC10 gives Einstein gravity with `mstar=exp(-1/6)` and pressure

    P17(S,w)=P0(S,w)+f17(exp(-2S)/2),   S>0.

The addition has no w dependence at fixed Xtilde. Hence `P17,w=P0,w`,
and the original auxiliary root is solved again, not fitted. All pressure
derivatives and energies below are newly differentiated from `P17`.

## Exact pole identities and the small-S auxiliary asymptotics

Put `delta=1-2X`. For the pole term alone, exact differentiation gives

    FX=2epsilon(delta^-2-1),
    Q=FX+2X FXX=epsilon(8delta^-3-6delta^-2-2),
    rho=2X FX-F=epsilon(2delta^-2-3delta^-1+delta),
    wfluid=F/rho=delta/(2+delta),
    cs²=FX/Q=delta(1+delta)/(delta²+delta+4).

Thus `wfluid~delta/2` and `cs²~delta/4`: they both tend to zero but
are not equal. The exact identities are checked symbolically.

The original auxiliary sector cannot overturn the pole's leading signs.
Write `a02=a0²`, `Lambda=C(0)`, and
`kappa0=(4Lambda-6)/(8a02)>0` for the existing constants. Here `kappa0`
is an asymptotic coefficient, not the action's fixed `kappa=6`.
Since `U(u²)=-u^6/3+O(u^8)`, the root equation has leading form

    P0,w=-4Lambda+6+8a02 u^5/S+lower-order terms=0,
    u=(kappa0 S)^(1/5)+O(S^(2/5)),
    w=-S/2+(kappa0^(1/5)/4)S^(6/5)+O(S^(7/5)).

Substitution into the original eliminated pressure yields

    F0=3-Lambda+(2Lambda-9)S
          -(5a02/3)kappa0^(6/5)S^(6/5)+O(S^(7/5)),
    Q0=-(2a02/5)kappa0^(6/5)S^(-4/5)+O(S^(-3/5)).

This identifies the old negative divergence; it does not replace it with
a different model's fitted scaling. Since `delta~2S`, the new positive
pole kinetic coefficient behaves as `Qpole~epsilon/S³`, and dominates
that old divergence. The power-sixteen correction stays finite as S tends
to zero. Therefore the new total pressure has, asymptotically,

    FX~rho_clock~q~epsilon/(2S²),
    Q~epsilon/S³,  cs²~S/2,  P/rho_clock~S,
    q=FX exp(-S).

These signs establish a healthy small-S clock principal part on a
sufficiently small punctured neighborhood. They do not prove that every
intermediate S is healthy; that gap is tested numerically below.

The algebraic root is also controlled asymptotically:
`P0,ww~160a02 kappa0^(4/5)S^(-6/5)>0`. Its fixed-canonical-momentum
Schur correction is subleading when the pole dominates `PSS+PS`.
The auxiliary pair stays nondegenerate on the tested positive-S states;
the excluded pole `S=0` itself is not asserted to be regular.

## Principal matrix and actual canonical auxiliary check

At each solved root, the script computes

    PSS_eff=PSS-PSw²/Pww,
    FX=-PS/(2X),  Q=(PSS_eff+PS)/(2X),
    Qbare=(PSS+PS)/(2X),
    Acan=Pww-PSw²/(PSS+PS)=Pww Q/Qbare.

It evaluates the actual bracket `[[0,Acan],[-Acan,0]]`, its singular
values and numerical rank; it does not enter rank two as a premise.
The clock's principal time and space coefficients are `Q` and `FX`.
On this Einstein plateau there are the two Einstein tensor modes and
the one first-derivative effective clock when the auxiliary elimination
is regular, as in the IC10 action argument. This is not a global Dirac
certificate for the activation transition.

At 80 decimal digits, 241 logarithmically spaced S values from `10^-12`
to `.3` all satisfy the stated positive kinetic, subluminal, expanding,
chart and one-sided activation conditions:

| Quantity | Computed bound on this finite grid |
| --- | ---: |
| minimum FX | 1.10024214433 |
| minimum Q | 5.76320221226 |
| maximum cs² | 0.270909727142 |
| minimum r² | 1.08843898761 |
| computed auxiliary ranks | 2 at every sample |

At `S=10^-12`, `cs²=5.00000000000e-13` and
`rho_clock=4.999999999995e18`; the previously negative low-S clock
kinetic coefficient is now approximately `1.0000000000015e31`.
The ordinary pressure derivatives are independently checked by branch
differences. The exact rational identities and canonical Schur identity
provide separate checks on the computation.

The later root `FX=0` occurs at
`S=0.5196273678992145595072762228`. A separate 81-point continuation
from `.3` to `10^-10` below that root is checked. The endpoint itself
has zero spatial clock coefficient and is not called strictly healthy;
the early-universe example below does not approach it.

## Same-action radiation history and cold-clock scaling

The explicit radiation action used for this restriction is the IC16
isentropic fluid `Srad=integral sqrt(-g) c_rad Zg²`, with `c_rad>0` and
`Zg=-g^{mu nu}theta_mu theta_nu/2>0`; its independent variation and
physical matter Ward identity are in [IC16](IC16_RADIATION_HISTORY.md).
For this classical conformal radiation, the physical stress trace vanishes.
Its auxiliary conformal variation is zero, so it does not change the
vacuum root `w0(S)`. In Einstein variables the actual equations are

    3mstar Htilde²=rho_clock+rho_rad,
    Abar³ q=constant,
    Abar^4 rho_rad=constant,
    Sdot=3Htilde cs²,
    Hphysical=exp(-w)Htilde(1+3cs² wS).

The radiation density can therefore be written `rho_rad=C_R q^(4/3)`.
Since `rho_clock~q`, the early clock scales as `Abar^-3` while radiation
scales as `Abar^-4`. Also `w0->0`, so the same leading exponents hold
for the physical scale factor. For every fixed positive radiation charge,
`rho_rad/rho_clock` tends to infinity toward the pole. The one-sided
activation is then exactly one because r² grows without an upper cap.
This is a constructive radiation-dominated asymptotic regime of the new
action, with a cold clock component, not an extrapolation of IC11's old
compact window.

For a finite witness set `S_final=.1` and
`rho_rad/rho_clock=.001` there, and solve backward for eight physical
e-folds using

    Delta ln aphysical=ln(q_initial/q_final)/3+w_final-w_initial.

The resulting early endpoint is
`S_initial=9.55403458394977083886577e-9`, with
`C_R=.00120282546730715462221615007`. At the endpoints:

| Quantity | Earlier endpoint | Later endpoint |
| --- | ---: | ---: |
| S | 9.55403458395e-9 | .1 |
| radiation fraction | .820405236221 | .000999000999001 |
| clock cs² | 4.77701731512e-9 | .226262908743 |
| clock P/rho | 9.53904846596e-9 | -.389313872782 |
| physical H in h0 units | 346562.792495 | .867373320184 |
| eta_up | 1 | 1 |

All 81 logarithmically spaced history samples meet the checked conditions.
The clock and radiation charges are conserved to the reported precision.
Independent quadrature in log S of
`S[1/(3cs²)+wS]` reproduces the same eight physical e-folds. These
are genuine background equations, not a specified external expansion
history or a reassignment of the old IC11 energy.

## Scope and reproduction

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_ic17_pole_clock
    PYTHONDONTWRITEBYTECODE=1 python3 ic17_pole_clock.py --require-full-closure

Tests were written first and observed failing before implementation. The
program returns exit 1 if a declared identity, health scan, or charge/
quadrature check fails. If those finite checks pass, the ordinary mode
returns zero and strict full-closure mode returns **2**. Eight e-folds
are not an observational fit to recombination or a normalization of the
late endpoint to today.

The new pole is singular at S=0, where its energy diverges. It does not
prove a nonsingular cosmology. Small clock sound speeds require an actual
interaction/strong-coupling analysis; positivity of the quadratic principal
part is not that analysis. Ordinary baryons, recombination microphysics,
photon-baryon perturbations, matter growth, transfer functions, the
activation-transition equations, and MOND/PPN/lensing normalization remain
open. No interval-certified all-S theorem, global novelty claim, or
full-theory PASS is asserted. The concrete result is a new same-action
early cold-clock/radiation regime and a verified finite history reaching
it without the old small-S ghost or late-condensate tuning.
