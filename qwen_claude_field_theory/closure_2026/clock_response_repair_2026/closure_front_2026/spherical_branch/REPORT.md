# Frozen spherical current and exact-exponential discriminants

Base supplied by the parent: `f59fad6c7`. Only this new directory is owned by
this subtask. No fitted coefficient, matter coupling, or background history is
introduced. The full same-action relativistic MOND construction remains open.

**Result:** the exact restricted scalar flux is derived below. Neither its
original logarithm/square-root form nor that form plus a single signed
`beta Y^(3/2)` term equals the exact exponential scalar constitutive flux near
zero: a required fourth-order coefficient is absent. This is a scalar kernel
statement, not a replacement for deriving the physical metric force.
Independently, a physical metric branch with a uniform finite source response
cannot satisfy exact exponential MOND for arbitrarily small isolated sources.
Nonzero local principal coefficients alone do not prove that uniform bound.

## Exact frozen radial variation

Use signature -+++, constant gamma and M2, minimal matter `Sm[g]`, and

    S = integral sqrt(-g) [M2 R/2 + P(X)-V+s W(Y)+gamma X Box chi] + Sm[g].

All clock-time coefficients are frozen at one epoch. For the restricted static
diagonal areal metric

    ds²=-N(r)² dt²+A(r)² dr²+r² dOmega²,
    tau=t, chi=q t+pi(r), p=pi'(r),
    X=q²/N²-p²/A², Y=p²/A², s=1/N,

the scalar variation may be evaluated in this ansatz. It does not supply the
metric, shift or clock equations. For r,N,A>0, omitting 4pi and the time
integral, the unreduced cubic density is

    L3_raw = gamma X (N r² p/A)'.

The first-order density and boundary term are exactly

    L3 = 2gamma q²r²N'p/(A N²)
         -(2gamma/3)r²N'p³/A³ -(4gamma/3)N r p³/A³,
    B3 = gamma X N r²p/A +(2gamma/3)N r²p³/A³,
    L3_raw-L3 = B3'.

Adding `N A r²(P-V)+A r² W` and differentiating with respect to p gives

    dL/dp = -2r² F,
    F = (N P_X-W_Y)p/A -gamma q² N'/(A N²)
        +gamma N'p²/A³+2gamma N p²/(r A³),
    (r²F)'=0.

The script also independently substitutes the metric into the covariant
shift current

    J^mu = -2(P_X+gamma Box chi) grad^mu chi
           -gamma grad^mu X+2s W_Y h^{mu nu} grad_nu chi

and obtains `N A r² J^r=-2r²F`. Thus the cubic sign and the radial factor 1/r
are checked by two forms of the current, not inferred from a MOND equation.

Regular-center zero flux gives `r²F=0` only with stationary enclosed scalar
charge. Freezing makes the current stationary in this ansatz. With the actual
time-dependent coefficient histories, the full equation is instead
`partial_t(sqrt(-g)J^t)+partial_r(sqrt(-g)J^r)=0`; a static metric alone does
not set radial flux to zero. An exterior integration constant is a scalar
charge or boundary datum, not automatically baryonic mass. `delta Sm/delta chi`
vanishes for minimal matter.

At fixed r and simultaneous weak metric/field amplitude, `N=1+Phi`, the
linear flux is `(P_X0-W_Y0)p-gamma q²Phi'`. At exactly N=A=1, retaining the
full scalar gradient nonlinearity, it is

    F_flat=(P_X(q²-p²)-W_Y(p²))p+2gamma p²/r.

Combining the exact flat nonlinear expression with only selected linear
metric terms is not an exact nonlinear gravitational equation. The script
checks the controlled first-order amplitude expansion separately.

## The homogeneous-clock restriction must be checked

Varying a radial clock slope `z=tau'` before setting z=0 gives

    sqrt(-g) J_tau^r = -2q r² W_Y p/A,
    (q r² W_Y p/A)'=0

for the frozen theory. On a regular center connected to a region with
q nonzero and W_Y nonzero this forces p=0. The zero-flux scalar equation
then forces N'=0 when gamma q is nonzero. This excludes a nontrivial response
within that restricted frozen, diagonal, homogeneous-clock branch; it is not
a no-go for the action. A static diagonal coordinate system may require a
radially tilted clock, or clock gauge may require a radial shift. Restoring
time-dependent coefficients also changes the clock equation. All independent
metric variations must be kept before such gauge specialization.

The unrestricted spherical current in `../../spherical_baryon_bridge/action/`
provides a consistency check: its zero-shift, static, areal specialization
agrees with the flux above. No full spherical evolution was rerun here.

## Original and canonically completed constitutive functions

For the original L205 frozen subcase,

    P0(X)=-(U/2)log[(U-2dX)/m0],
    W0(Y)=U+2d ell [sqrt(1+Y/ell)-1],
    U,d,ell,m0>0, Delta=U-2dq²>0.

At p>0, optionally replacing W0 by `W0+eta beta Y^(3/2)` with eta=+1 or -1
and beta>0, the exact flat scalar flux is

    F = p[Ud/(Delta+2dp²)-d/sqrt(1+p²/ell)]
        -(3eta beta/2)p²+2gamma p²/r.

Beta is only a separately labelled proposal, not an edit to the original
action. At q=0 and beta=gamma=0 its leading term is

    F = [d/(2ell)-2d²/U]p³+O(p⁵).

Its leading scalar stiffness is positive for U>4dell, but vanishes at p=0.
The tuned U=4dell term is `-d p⁵/(8ell²)`, with the wrong local energy sign.
These statements agree with `../health/REPORT.md`.
For q=0, gamma=0 and p>0 sufficiently small, the +beta proposal contributes
negative transverse stiffness `-3beta p`, while the -beta proposal contributes
positive `3beta p`; the latter still tends to zero at p=0. Neither sign
creates a strictly positive constant stiffness at the origin. Cubic Hessian,
clock and metric effects must be included before making a full health claim.

The canonical current action in `../../nonlinear_evolution_2026/constitutive.py`
also includes its fixed history completion:

    P_gamma=P0+lambda_X(X-qbar²), lambda_X=3gamma qbar Hbar,
    W_gamma=W0+lambda_W, lambda_W=-2gamma qbar² qbar_dot.

The script includes these terms. In the flat scalar flux they add only
`lambda_X p`; the W constant does not change W_Y. They do affect the clock
constraint and therefore the physical response. The symbols lambda_X and
lambda_W here abbreviate the existing histories; they are not fitted or
independent parameters.

## Exact exponential mismatch for the restricted scalar kernel

For either original or completed functions and either beta sign, at each fixed
r>0 the positive-p Taylor jet has the form

    F=c1 p+c2 p²+c3 p³+c5 p⁵+O(p⁷).

There is exactly no p⁴ term. The linear-X completion changes c1; beta and the
spherical cubic term change c2. For any fixed positive normalization A0 and
a0>0, the target scalar flux would instead be

    A0[1-exp(-p/a0)]p
      =A0 p²/a0-A0 p³/(2a0²)+A0 p⁴/(6a0³)-A0 p⁵/(24a0⁴)+O(p⁶).

The fourth coefficients differ for every such A0,a0. Consequently no choice
of these constants makes the displayed scalar kernels identical on an interval
touching zero. This conclusion follows from the displayed analytic one-sided
expansions, not from a numerical fit. It does not exclude a nonlinear metric
map or clock elimination from generating other powers in the physical force.
No identification `p=Phi'` or `pi=Phi` is made.

Even assigning a direct scalar source hypothetically does not repair the
cubic-only radial scaling: `2gamma p²/r=C/r²` yields
`p=sqrt(C/(2gamma r))` for C,gamma>0, a radius power -1/2. The deep-MOND
point-source force instead has radius power -1. This toy source is expressly
absent from minimal matter. It only distinguishes the cubic mechanism from
the required radial law.

## Physical metric source scaling and its exact remaining hypothesis

The sibling metric calculation gives, on its aligned frozen local principal
branch with regular clock elimination, b=gamma q² and

    G0=2P_X-2W_Y W(0)/(W(0)-2q²W_Y),
    G=G0-2b²/M2,
    G0 p=2b g,  g=gN+(b/M2)p,
    p=2b gN/G,  g=(G0/G)gN.

Here g=Phi' is the physical lapse force and gN the Einstein baryonic force.
These equations are independently solved algebraically by this script; the
metric action derivation belongs to the sibling calculation. They are leading
principal equations only, with no global boundary or lower-derivative claim.
For the uncompleted P0,W0, G0=0 exactly, and the affine G is negative if b is
nonzero. This specific statement must not be transferred to the completed
action. Its frozen aligned coefficient is instead

    G0_gamma=2lambda_X+
      4d²q²lambda_W/[Delta(Delta+lambda_W)].

The clock elimination requires Delta+lambda_W nonzero. A non-affine background
also contributes the known cubic Hessian terms to G. None can be dropped
uniformly near a vanishing denominator.

The source-amplitude obstruction is simpler and more general than the scalar
kernel comparison. Fix r, source shape, the background and the boundary
prescription, and write gN=epsilon n with n>0. Suppose the actual nonnegative
physical force obeys a uniform bound `g(epsilon)<=C epsilon` for all small
epsilon>0. Exact exponential MOND requires

    epsilon n=[1-exp(-g/a0)]g <= g²/a0 <= C²epsilon²/a0,
    hence a0 n <= C²epsilon.

It therefore fails below the stated finite-gain threshold. A regular local
principal response has this scaling at its linear order. A uniform bound for
the full sourced problem additionally requires a controlled solution family
and a bounded inverse including boundary and lower derivative effects. This
subtask does not prove either. A zero mode, nonuniform inverse, amplitude-
dependent boundary data, or a separate nonlinear branch can evade the premise.
Those are concrete remaining bridges; merely keeping G nonzero at each
nonzero source amplitude does not prove uniformity as epsilon tends to zero.

## Executed evidence and non-claims

`derive_spherical.py` performs 26 exact SymPy checks. Python 3.9.6 and SymPy
1.14.0 were used. The final provenance record is `run_002/manifest.json`, with
the exact stdout in `run_002/stdout.txt`. The earlier `run_001` records the
pre-completion refinement and is superseded for current-code reproduction.
The canonical constitutive source is hashed as an input and is not imported
or executed. No external theorem lookup was necessary for these elementary
variations, series coefficients and inequalities.

From the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/spherical_branch/derive_spherical.py
```

`SphericalScaling.lean` checks the fourth entries of explicit coefficient jets, their
inequality for positive target normalization and a0, and the unique-radius
overlap of the hypothetical cubic and MOND squared radial laws. The analytic
functions' action-to-jet interpretation is outside Lean; no analytic Taylor
theorem or polynomial-library reduction is claimed. The physical
finite-gain certificate is maintained by the parent in `../principal_gate/`.
The Lean command uses the existing pinned environment:

```sh
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/spherical_branch/SphericalScaling.lean
```

Run it from `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`.
The final file compiled with exit 0. Each of its four printed axiom sets is
exactly `[propext, Classical.choice, Quot.sound]`, with no sorry or custom
axiom. An earlier direct polynomial-library proof failed to compile; that
failure is preserved in the parent's `../principal_gate/run_001/` output.
The successful final certificate uses the explicitly stated coefficient-vector
representation. No numerical galaxy solution, exact physical exponential force
law, global regularity, full characteristic health, or Dirac completion is
claimed by this package.

Mathbox computation-audit guided the computational contract, independent
current check and provenance. Proofread-math self-review is limited to this
report and the new certificate's declarations; no mathematical-token correction
was needed during that proofreading pass.
