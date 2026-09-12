# Nonlinear clock tilt in the unchanged frozen action

Base: `bba135b36acd2dc40039517ed6038d1e7c37a995`. This directory contains a
new bounded calculation; no action coefficients, matter coupling, or background
history were changed. The computation-audit skill guided the exact and
independent checks and the version 2 run manifest.

**Result:** regular elimination of the responding clock produces an analytic,
even reduced first-derivative action near the aligned zero-gradient state.
It cannot produce the nonanalytic `|p| p` constitutive flux there. On the
clock-critical locus the generic local branch instead produces a cube-root
flux, with precisely identified exceptional cases. This is a frozen flat
clock/scalar result, not a physical MOND force or an on-shell spacetime solution.

## Scope, conventions, and exact variation

Keep the same action, with signature -+++ and positive constant M2:

    EH[M2] + P(X,tau) - V(tau) + s W(Y,tau) + gamma X Box chi + Sm[g,psi].

Freeze the coefficient functions at one epoch and use a local flat stationary
radial ansatz

    tau=t+sigma(r), chi=q t+pi(r), z=sigma'(r), p=pi'(r),
    s=sqrt(1-z²)>0, X=q²-p², Y=(p-qz)²/(1-z²),
    Q=(q-zp)/s, u^r=(p-qz)/(1-z²).

The cubic interaction, P and the Einstein term contain no clock-gradient
dependence. The radial clock equation in this frozen problem is
`(r² J_tau^r)'=0`, where varying z before any restriction gives

    J_tau^r = -z W/s - 2(q-zp) W_Y (p-qz)/s³.

This agrees with `W n^r - 2 Q W_Y u^r` from the covariant variation.
Regular-center stationary zero clock charge sets `J_tau^r=0`. This is a
boundary/charge choice, not a consequence of minimal baryonic coupling.
Nonzero charge, explicit clock-time derivatives, radial shift and metric
equations are outside this reduction.

For the canonical square root, retain its existing completion:

    W(Y)=Wc+2d ell [sqrt(1+Y/ell)-1],
    Wc=U+lambda_W, lambda_W=-2gamma qbar² qbar_dot,
    d>0, ell>0.

Wc is an abbreviation for the fixed history value; it is not a tunable new
coefficient. Define

    k=q²-ell, A=Wc-2d ell, C=Wc-2d q²,
    D=ell+p²-2pqz+kz²=ell(1-z²)+(p-qz)².

The exact clock density and current simplify to

    L_W = s W = A sqrt(1-z²)+2d sqrt(ell) sqrt(D),
    J_tau^r = -A z/s+2d sqrt(ell)(kz-pq)/sqrt(D).

Since D>0 for ell>0 and |z|<1, this rewriting uses the positive roots without
an additional branch choice. The exact zero-current relation is

    2d sqrt(ell)(kz-pq) sqrt(1-z²) = A z sqrt(D).       (1)

Squaring gives a quartic polynomial:

    4d²ell(kz-pq)²(1-z²) - A² z² D = 0.              (2)

Equation (2) must be filtered through the unsquared equation (1); its roots
alone do not solve the clock constraint. Boundary roots |z|=1 are excluded.

On any stationary branch, the envelope derivative gives its exact contribution
to the scalar flux:

    F_W = -(1/2) dL_W,eff/dp
        = -d sqrt(ell)(p-qz(p))/sqrt(D(p,z(p))).       (3)

The code checks both the direct action derivative and the independently
assembled covariant clock current. It also checks (3) by differentiating
numerically re-solved stationary actions.

## Regular clock block C nonzero

At the origin, `partial_z J_tau^r=-C` and
`partial_p J_tau^r=-2dq`. Thus for fixed C nonzero the analytic implicit
function theorem gives a unique real analytic branch with z(0)=0. The joint
symmetry `(p,z)->(-p,-z)` makes this z(p) odd and L_W,eff(p) even. The domain
|z|<1 is open and holds near the origin. In particular,

    z(p) = -2dq p/C
           + d q Wc²(Wc-2d ell) p³/(ell C⁴) + O(p⁵).  (4)

Its linear ratio `z/p=-2qd/(Wc-2q²d)` equals the earlier principal
`sigma/pi` ratio for a nonzero Fourier mode and background clock rate one.
No division by C is allowed on the critical locus below.
The reduced density is

    L_W,eff = Wc+(d Wc/C)p²+H4 p⁴+O(p⁶),

    H4 = -d Wc[Wc³-8Wc d²ell q²+8d³ell q⁴]/(4ell C⁴). (5)

Let Delta=U-2dq²>0. Up to a constant, the canonical frozen P term is

    P(q²-p²) = -(U/2)log[(Delta+2dp²)/Delta]-lambda_X p²,
    lambda_X=3gamma qbar Hbar.

The log numerator is positive for every real p when Delta>0. Consequently,

    L_PW,eff = constant
               +[-Ud/Delta-lambda_X+d Wc/C]p²
               +[Ud²/Delta²+H4]p⁴+O(p⁶),

    F_PW = [Ud/Delta+lambda_X-d Wc/C]p
           -2[Ud²/Delta²+H4]p³+O(p⁵).                (6)

For Wc=U+lambda_W, the first coefficient in (6) equals

    lambda_X + 2d²q² lambda_W/[Delta(Delta+lambda_W)].

This reproduces one half of the canonical `G0` in the sibling principal and
spherical calculations. It cancels for the uncompleted lambda_X=lambda_W=0
case, but the next regular constitutive term is cubic in p, not `|p|p`.
More generally, cancellation of any finite number of regular even action
coefficients leaves an odd analytic flux. A `|p|` stiffness cannot arise from
this regular elimination at zero signed p. This is a local analytic argument;
the finite tests verify its action coefficients and hypotheses, not the
implicit function theorem itself.

The exact flat radial cubic interaction still contributes `2gamma p²/r` to
F, since its first-order density is `-(4gamma/3)r p³`. Thus, at fixed r>0,

    F_flat = F_PW + 2gamma p²/r.

The total regular aligned flat flux still has powers p,p²,p³,p⁵,... and no
p⁴ term. This closes the regular frozen clock-elimination loophole in the
sibling spherical scalar-kernel comparison with the exact exponential law.
It does not identify p with the physical lapse force. Eliminating metric
variables or keeping nonlinear metric corrections is a different calculation;
in particular the flat coefficient `2gamma/r` must not be transferred to a
metric-reduced action without deriving it there.

The coefficients in (4)-(6) are not uniform as C approaches zero. They cannot
be used to control a simultaneous p->0, C->0 limit by substitution.

## Exact regular controls and the zero-Wc interpretation

If q is nonzero and Wc=0, the exact branch through the origin is

    z=p/q, |p|<|q|, Y=0, W=0, L_W,eff=0, F_W=0.     (7)

Its clock block is `C=-2dq²`, which is nonzero. The clock responds by aligning
its gradient with the scalar gradient; it is not an absent or unresponsive
field. The frozen first-derivative W contribution vanishes on this branch.
Neither the P action nor cubic scalar-metric mixing vanishes as a consequence.
Equation (7) alone proves no preferred-frame, PPN, or cosmological safety claim.
The fixed canonical positive-gamma reference patch with qbar_dot<0 in fact has
Wc=U+lambda_W>U>0; zero Wc was not constructed on that patch.

A second exact control is A=0, k nonzero:

    z=pq/k, L_W,eff=2d ell sqrt(1-p²/k),              (8)

with the original timelike condition and positive radicand retained. This is
regular near zero, C=-2dk, and the cubic tilt coefficient in (4) vanishes.
For q=0 and Wc nonzero, z=0 is the regular branch through zero.

## Clock-critical C=0, q nonzero, q² different from ell

This is **clock criticality**, not the separate metric-reduced condition G=0.
At C=0 let k=q²-ell be nonzero and let a be the real number defined by

    a³=-2ell/(kq).

The weighted expansion p~t³,z~t of the exact density is

    L_W = Wc - 2dq pz - d k q² z⁴/(4ell)
          +d p²+d k q pz³/ell
          +d k q²(q²-2ell)z⁶/(8ell²)
          +terms of weight at least eight.          (9)

Its leading clock equation is

    0=-2dq p-(d k q²/ell)z³+terms of weight at least five.

Set t=cbrt(p) and z=t v. After division by t³, the exact current is analytic
in (t²,v) near (0,a). Its derivative in v at that point is
`-3d k q² a²/ell`, which is nonzero. Hence there is a unique nearby real
branch of this scaled equation with

    z = a cbrt(p) + q p/(2k) + O(sign(p)|p|^(5/3)).   (10)

Substituting into (9), or using the independently checked envelope flux,
gives

    L_W,eff = Wc -(3/2)dq a |p|^(4/3)
                 -d q² p²/(2k)+O(|p|^(8/3)),

    F_W = dq a cbrt(p) + d q² p/(2k)
          +O(sign(p)|p|^(5/3)).                     (11)

The analytic P term adds `(Ud/Delta+lambda_X)p+O(p³)` to F. The flat radial
cubic term adds `2gamma p²/r`. Neither changes the leading cube-root term
in (11) for fixed finite parameters and fixed r>0. Thus this particular
singular clock branch does not produce the deep-MOND scalar flux `|p|p`.

For p positive, the leading sign of F_W is opposite the sign of k:
`k>0` gives negative local differential flux, and `k<0` gives positive but
divergent differential flux as p->0. These are signs of this frozen reduced
gradient contribution, not a full characteristic or Hamiltonian assessment.
The nonzero coefficient cannot be removed by choosing q nonzero, d>0,
ell>0 and k finite nonzero. The response is singular in its derivative:
`dz/dp` scales as `|p|^(-2/3)`.

The branch itself remains timelike sufficiently near zero since z->0, and
the canonical log remains in its domain if Delta>0. C=0 requires
`lambda_W=-Delta`; the calculation does not establish that the fixed
cosmological history reaches this value. In particular it is unavailable on
the positive-gamma, qbar_dot<0, positive-Delta reference patch described above.

## Exceptional critical cases

If C=0 and q²=ell>0, then A=k=0 and exactly

    L_W=2d sqrt(ell) sqrt(ell+p²-2qpz),
    J_tau^r=-2d sqrt(ell) q p/sqrt(ell+p²-2qpz).

There is no zero-current solution with p nonzero and |z|<1. At p=0 every
timelike z is stationary; no regular elimination through nonzero p exists.
The cube-root formula must not be used at k=0.

If C=0 and q=0, necessarily Wc=0. The exact density is

    L_W=2d ell [sqrt(1-z²+p²/ell)-sqrt(1-z²)].

For p nonzero, its zero current forces z=0; at p=0 all timelike z are
stationary. The z=0 branch is analytic and reduces to
`2d ell[sqrt(1+p²/ell)-1]`. It gives the previously known analytic q=0
kernel and does not itself supply a nonanalytic MOND constitutive term.

These cases exhaust the C=0 possibilities for d,ell>0 near the specified
aligned zero-gradient state. Other boundary data, a nonzero clock charge,
timelike-boundary limits, different tilted backgrounds and time-dependent
coefficients are not classified here.

## Executed evidence and provenance

`derive_nonlinear_clock.py` passed 39 exact symbolic assertions and 28 bounded
parameter/slope controls at both 60 and 90 decimal digits. The numerical
family is d=q=1 with (ell,Wc) equal to
`(1/2,3),(1/2,1),(2,0),(2,4),(1/2,2),(2,2),(1,2)`, and p equal to
`1/100,1/1000,1/1000000,-1/1000`. U=5 supplies Delta=3 for a log-domain
control. These are algebraic benchmarks, not fitted or cosmologically
realized histories.

Each control first isolates all real roots of the exact rational squared
polynomial in intervals of width at most `10^-70`, rejects non-timelike and
unsquared-spurious roots, and compares the selected root with a direct
unsquared solve initialized by the independently derived asymptotic branch.
All 24 nonexceptional cases have one admitted unsquared timelike root in
this sample; the four q²=ell critical cases have none. This count is bounded
numerical evidence, not a global parameter classification. The same direct
branch is checked by a symmetric finite difference of the re-solved action.
No fitting, randomness, continuation from a different theory, or new operator
is used. Unsquared filtering is performed numerically and is not an interval
proof; the exact exceptional-case exclusion follows separately from its
displayed nonzero current.

The complete results, input hashes, logs, exact command, dirty-state snapshot,
software versions and enforced resource limits are in
`run_001/manifest.json` and `run_001/results.json`. The command completed with
exit status zero and its manifest validated against the workspace. The
bounded runner enforced a 180-second wall limit, 150-second per-process CPU
limit and 1 MiB combined log cap. The one-thread numerical-library cap is
cooperative; no hard memory or CPU-affinity cap was requested. Run software:
Python 3.9.6, SymPy 1.14.0, mpmath 1.3.0.

Direct reproduction from the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/nonlinear_clock/derive_nonlinear_clock.py
```

Manifest verification:

```sh
python3 -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/nonlinear_clock/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The durable argument for regular analyticity is the open constitutive domain,
nonzero clock derivative and symmetry; the durable critical argument is the
nonzero derivative of the scaled clock equation. The code verifies the
load-bearing algebra and bounded branch controls. Neither replaces the full
Einstein-clock-scalar equations, a global boundary problem, fixed-history
accessibility, or nonlinear physical response/health gates.

Mathbox proofread-math self-review covers only this new report and the script's
notation/prose. No mathematical-token correction was needed in that pass.
