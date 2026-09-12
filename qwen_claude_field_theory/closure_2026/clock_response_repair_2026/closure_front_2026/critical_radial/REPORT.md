# Critical radial response with a responding regular clock

Base revision: `bba135b36acd2dc40039517ed6038d1e7c37a995`. This package introduces
no coefficient function, history, matter coupling, or fitted parameter.

The regular aligned clock does **not** generate a local `p|p|` constitutive
flux. In the explicitly stated short-distance derivative hierarchy, the first
critical sourced balance is

    G p + 4 gamma p²/r = 2 b gN,
    b=gamma q²,  G=G0-2b²/M2,  gN=Menc/(8 pi M2 r²).

Thus at `G=0`, `gamma!=0`, its squared scalar slope is

    p²=q² Menc/(16 pi M2 r),

and its contribution to the physical force is proportional to `r^(-1/2)` in
vacuum. This result is conditional on a separate derivative hierarchy, **not**
a solution of the complete fixed-history sourced equations. The calculation
also identifies a specific omitted metric term at the same amplitude order,
and a lower derivative linear obstruction to a uniform small-source limit.

## Scope and exact static frozen action

Signature is `-+++`, `M2>0`, and

    S = integral sqrt(-g) [M2 R/2+P(X,tau)-V(tau)
                          +s W(Y,tau)+gamma X Box chi]+Sm[g].

All coefficient histories are held at their given epoch values. This is a
frozen auxiliary theory for deriving necessary local terms. The restriction
`tau=t+sigma(r)` selects an epoch whose aligned clock normalization is one;
it is the same normalization used by the canonical history code. It is not a
claim about arbitrary clock normalizations. The independent fields are

    ds²=-N(r)²dt²+A(r)²dr²+r²dOmega²,
    chi=q t+pi(r), tau=t+sigma(r), p=pi', z=sigma'.

For `N,A>0` and a timelike clock, define

    Qlocal=q/N, w=p/A, u=N z/A, |u|<1,
    X=Qlocal²-w²,
    Y=(w-Qlocal u)²/(1-u²).

Omitting `4pi` and time integration, the frozen radial action has the exact
first-order representative

    L_EH = M2[N(A+1/A-2)+2rN'(1/A-1)],
    L_PW = N A r²[P(X)-V]+A r² sqrt(1-u²)W(Y),
    L_3  = 2gamma q² r²N'p/(A N²)
           -(2gamma/3)r²N'p³/A³-(4gamma/3)N r p³/A³.

The EH representative differs from the curvature action by a radial boundary
term; its quadratic part is `M2[a²-2r n'a]` for `N=1+n,A=1+a`. The exact
cubic representative is the independently checked one in
`../spherical_branch/REPORT.md`. Neither representative fixes `z=0` before
variation. The scalar and clock conserved fluxes are taken to vanish, as
required by a regular center in this frozen stationary problem. Nonzero clock
flux would require a different Routh reduction and boundary data.

The off-diagonal Einstein equation is also relevant. For stationary scalars
and a diagonal static metric, the frozen action obeys

    T_0r = -q J_chi,r - J_tau,r.

The first derivative sectors obey this algebraically. For the cubic sector,
`H_ta v^a=0` by stationarity of `v²`, and `X'=-2H_ra v^a`, which gives the
same identity directly from the cubic stress in the metric-response report.
Consequently the two zero-current conditions are consistent with the shift
equation on this frozen branch. The actual time-dependent histories do not
inherit the zero-current assumption without checking their time divergence.

## Regular clock reduction, including the lapse dependence

Write `Wc=W(0)`, `d=W_Y(0)`, and `C(Qlocal)=Wc-2d Qlocal²`. Varying the
clock before elimination gives the stationarity equation of

    f(Qlocal,w,u)=sqrt(1-u²) W((w-Qlocal u)²/(1-u²)).

At `u=w=0`, `f_uu=-C(Qlocal)`. If `C(Qlocal)!=0`, the local implicit
function branch exists, is analytic for the given analytic `W`, and obeys
`u(-w)=-u(w)`. The equality `f(Qlocal,-w,-u)=f(Qlocal,w,u)` then makes the
eliminated function even in `w`. Explicitly,

    u=-2d Qlocal w/C(Qlocal)+O(w³),
    f_eff(Qlocal,w)=Wc+[d Wc/C(Qlocal)]w²+O(w⁴).

The reduced flat scalar current is therefore odd and analytic: `p,p³,p⁵,...`.
It cannot equal a nonzero radius-independent `p|p|` flux on a neighborhood of
zero. A one-sided analytic continuation cannot supply the missing quadratic
coefficient either. This statement is confined to the regular branch through
alignment, and does not settle singular-clock or disconnected branches.
The sibling `../nonlinear_clock/` package supplies the higher clock jet and
independent checks; this script independently expands the invariant action
through the needed cubic metric/field order.

At arbitrary nearby lapse, the coefficient of `p²` in the reduced radial
action is

    L_PW,p² = -r² H(N)p²/(2A),
    H(N)=2N P_X(q²/N²)-2d Wc/[Wc-2dq²/N²].

Here `P_X(q²/N²)` means the derivative evaluated at zero spatial scalar
slope. Thus, with `C=Wc-2dq²`,

    G0=H(1)=2PX-2d Wc/C,
    G0_N=H'(1)=2PX-4q²PXX+8d²q²Wc/C².

This lapse derivative is essential: using only a flat scalar kernel loses it.

## Retained hierarchy and the induced source

First retain the quadratic spatial derivative action plus the unique cubic
term with an extra spatial derivative. A minimal static source contributes
`-r²rho n` at its leading order. The radial action is

    L_ret = M2[a²-2r n'a] + 2b r²n'p
            -G0 r²p²/2 -(4gamma/3)r p³-r²rho n.

Its equations give, with regular-center source normalization,

    a=r n',
    n'=gN+(b/M2)p,
    G0 p-2b n'+4gamma p²/r=0.

The scalar flux has zero integration constant; the baryonic source appears
only after the metric equation is inserted. No scalar charge is assigned to
the mass. Eliminating `n'` gives the balance at the start of this report.
At criticality the linear metric/scalar derivative action is a square,

    L_2=-M2 r²[n'-(b/M2)p]²,

after elimination of `a`. The sourced leading nonlinear response has
`n'=(b/M2)p+gN`. For constant exterior mass, the retained solution has
`p~r^(-1/2)` and

    g=n'=gN+(b/M2)p.

Its scalar contribution has exponent `-1/2`; the sum contains both `-2` and
`-1/2` powers. The attractive scalar branch requires the sign of `p` to make
`b p>0`. Real squared slopes exist for positive mass, `q²>0`, `M2>0` and
nonzero gamma because the same gamma occurs in the source mixing and cubic
coefficient. This sign cancellation does not establish stability or global
branch matching. In particular, the `r^(-1/2)` exterior profile has a scalar
potential growing as `sqrt(r)` and cannot itself define an asymptotically
weak solution at arbitrarily large radius.

## The first omitted metric term is explicit

Weak source amplitude alone does not justify the retained action. Expand the
full derivative action to cubic amplitude, and project onto its critical
quadratic null direction, with `alpha=b/M2`:

    n=alpha pi,  a=alpha r p,  n'=alpha p.

At cubic order, corrections of second order in the eliminated fields do not
alter the projected derivative action: their coupling to the first-order
fields is the stationary quadratic null equation, up to the prescribed
boundary terms. This argument applies to the displayed derivative action;
it does not dispose of the excluded lower derivative quadratic sector.
The exact cubic jet of that derivative action is

    L_der,critical,3 = -(4gamma/3)r p³ + Qmetric r² pi p²,
    Qmetric=-(alpha/2)(G0_N+3G0),   G0=2b²/M2.

The `r³p³` terms from EH, metric braiding and `P,W` cancel. The surviving
`pi p²` term does not cancel in general. SymPy and a separate hand audit
agree on this coefficient. Its Euler operator, with convention
`E=dL/dpi-d/dr(dL/dp)`, is

    E_Q=-Qmetric[r²p²+2pi(r²p)'].

This is not a constitutive `p|p|` term: it depends on the potential and its
radial derivatives. Nor is it legitimate to call the retained quadratic
flux equation exact after keeping a full flat nonlinear kernel.

For a quantitative local bound, consider an annulus `L<=r<=2L`, with
`|p|<=p_*`, `|p'|<=c1 p_*/L`, and `|pi|<=c0 L p_*`. Then

    |E_Q|/r² <= |Qmetric| p_*² [1+2c0(c1+2)].

The Galileon equation has characteristic scale `|gamma|p_*²/L²`; thus
`|Qmetric| L²/|gamma| << 1` is a sufficient coefficient-level ordering
condition for this bound when `c0,c1` are controlled. It is not necessary
for every special profile with additional cancellations. This is a
comparison of operators or integrated flux errors, not division by the
vacuum Galileon residual, which vanishes on the leading exterior solution.
An additive potential fixed by distant matching can invalidate the bound on
`pi`; the matching prescription must supply it.

If the flat eliminated first derivative action has quartic coefficient
`H4 p⁴`, its flux contributes `-4H4 p³`. Suppression relative to the cubic
Galileon flux requires `|H4| p_* L/|gamma| << 1`. Clock regularity also
requires staying away from `C=0`, and scalar/metric expansions require
`p_*/q<<1`, `|u|<<1`, and `|alpha|p_*L<<1`, in consistent units. The
derivative expansion must hold for coefficient derivatives as well.

## Lower derivative terms prevent an unsupported small-source claim

Before any background subtraction, the frozen `P,W` action itself contains
the exact quadratic potential sector

    L_pot,2/r² = (q²PX+2q⁴PXX)n²
                 +(P0-V-2q²PX)a n,
    P0=P(q²).

On the critical null direction and after a radial integration by parts, its
projected coefficient is

    L_pot,2 = Bpot r²pi² + boundary,
    Bpot=alpha²[4q²PX+2q⁴PXX-(3/2)(P0-V)].

This is an explicit term absent from the pure principal reduction. It is not
being interpreted as the physical mass of the actual cosmological
background: the frozen affine background has unsolved tadpoles, and actual
curvature, Hessian and time-history terms must be combined on shell. It
demonstrates exactly why dropping all lower derivatives needs justification.
Its projected Euler operator is `2Bpot r²pi`, which has characteristic size
`|Bpot|p_*L`. To place it below the critical Galileon equation requires

    |Bpot| L³/(|gamma|p_*) << 1.

Any surviving lower derivative coefficient of this type defeats a uniform
`p_* -> 0` limit at fixed radius. Background Hessians can also shift `G` at
linear derivative order, and actual `tau` dependence produces nonstationary
clock and scalar currents. Tuning the affine symbol `G` to zero does not
cancel these terms. No fixed history is retuned in this package.

A two-parameter formal local hierarchy can make these inequalities mutually
consistent: take dimensionless slope amplitude `epsilon`, choose a shrinking
length `L~epsilon^a` with `1/3<a<1`, and keep finite coefficient scales away
from the clock singularity. The displayed ratios then scale as
`epsilon^(2a)`, `epsilon^(1+a)`, and `epsilon^(3a-1)`. This changes the source
length scale and mass along with amplitude. It is **not** the isolated-source
small-amplitude limit at fixed source shape used in a universal force law,
and does not certify an effective-theory ultraviolet range.

The precise remaining task is to derive the on-shell lower derivative
operator and boundaries for the given histories, verify a nonempty radial
window satisfying these inequalities and the theory's validity range, and
solve the coupled sourced system there. Without that work, the first sourced
term is known in the specified hierarchy, but an actual critical branch of
the complete theory is not established.

## Canonical completion is retained

For `Delta=U-2dq²>0`, the existing history code has

    PX=Ud/Delta+lambda_X,  PXX=2Ud²/Delta²,
    Wc=U+lambda_W,
    lambda_X=3gamma qbar Hbar,
    lambda_W=-2gamma qbar² qbar_dot.

These symbols abbreviate fixed histories. They are not independent fit
parameters. Substitution gives

    G0=2lambda_X+4d²q²lambda_W/[Delta(Delta+lambda_W)],
    G0_N=2(Ud/Delta+lambda_X)-8Ud²q²/Delta²
          +8d²q²(U+lambda_W)/(Delta+lambda_W)².

The constant `Wc` therefore affects both clock elimination and the first
nonlinear metric correction. A calculation retaining only `W_Y` misses these
effects. Clock regularity requires `Delta+lambda_W!=0`.

## Computation and certificate contract

`derive_critical.py` uses exact rational symbolic arithmetic in SymPy, with
formal amplitude jets through degree three, polynomial differentiation, and
identities of rational functions on their stated nonzero-denominator domain.
It compares the invariant clock/scalar action expansion with an independent
lapse-coefficient derivative, varies the retained radial action, checks the
critical cubic cancellation and the potential boundary identity, and checks
three rational radius fixtures of the explicitly retained model. It performs
no sampling, nonlinear field integration, fitting, or source reconstruction.
The coefficient `H4` is used only to state a remainder criterion; this script
does not claim its exact fourth-order value.

`CriticalRadial.lean` proves four algebraic statements: the metric-induced
source elimination without division by `G`, its critical specialization, the
cubic metric cancellation, and the incompatibility of a nonzero linear term
with a uniform arbitrarily small quadratic bound. It does not formalize the
covariant action, the analytic implicit-function theorem, existence of
solutions, asymptotic remainders, or the source-to-field interpretation.

Reproduction uses the repository's pinned Lean environment:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/critical_radial/derive_critical.py
```

From `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

```sh
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/critical_radial/CriticalRadial.lean
```

The final symbolic run is `run_001/manifest.json`: all 25 exact checks passed,
exit zero, elapsed 3.007 seconds, Python 3.9.6 and SymPy 1.14.0. The final Lean
run is `lean_run_001/manifest.json`: all four declarations compiled, exit zero,
elapsed 1.858 seconds, Lean 4.34.0-rc2. Each printed axiom set consists exactly
of `propext`, `Classical.choice` and `Quot.sound`; no sorry or custom axiom is
used. Both version 2 manifests passed `validate_manifest.py --root` with
current file hashes. Execution success certifies the bounded algebra/code
assertions, not the physical remainder assumptions.

The computation-audit skill guided the contract and provenance. Mathematical
proofreading covers the newly written report and certificate. It corrected a
prose line-joining artifact in this report, made no mathematical-token change,
and left a harmless plus character inside the certificate's already-hashed
introductory comment. An initial exploratory Lean compile lacked a tactic
import; the final source adds the explicit imports and passes as recorded.
