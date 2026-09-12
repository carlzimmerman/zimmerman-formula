# Static physical metric response of the fixed action

Base revision supplied by the parent: `f59fad6c7`. This directory changes no
coefficient functions or pre-existing source files. The calculation uses
`mathbox:computation-audit` to separate the exact symbolic assertion from the
unsolved physical background and to preserve execution provenance.

For the unchanged action

    S = integral sqrt(-g) [M2 R/2 + P(X,tau)-V(tau)
                          + s W(Y,tau) + gamma X Box chi] + S_m[g,m],

the leading local static potentials in the aligned clock frame are equal,
and their common minimally sourced amplitude is

    Phi_hat = Psi_hat = -rho_hat/(2 M2 k²) * G0/G,
    pi_hat = -b rho_hat/(M2 G k²),
    b = gamma q²,
    G0 = 2 PX - 2 s WY W0/(W0-2q² WY),
    G = G0 - 2b²/M2.

These formulas require `k² != 0`, `W0-2q² WY != 0`, and `G != 0`. They are
obtained by varying the same action and solving its metric/clock/scalar
principal constraints. Neither equality of the potentials nor a scalar
source coupling was imposed. The static ratio `gamma_static=Psi/Phi` is
therefore one where the potential is nonzero. It is not a matched PPN gamma.

## Contract and conventions

The signature is -+++, `M2>0`, `X=-grad(chi)^2`,
`s=sqrt(-grad(tau)^2)`, `n=-grad(tau)/s`, and
`Y=(g+nn)dchi dchi`. The local affine background is `chi=q t`, `tau=s t`
with `q,s>0`; background covariant scalar Hessians vanish in this
calculation. Write perturbations `chi=q t+pi`, `tau=s t+sigma`,
`g00=-(1+2Phi)`, `gij=(1-2Psi)delta_ij` at linear order. Constant coefficients
are evaluated at that jet. Source conventions are
`M2 G_mu nu=T_mu nu`, minimal static dust `T00=rho`, `Tij=0`, and Fourier
`exp(i k.x)` so `Delta=-k²`.

The exact computational surrogate is the quadratic spatial derivative
action and its finite-dimensional Fourier constraints. SymPy performs exact
symbolic differentiation, matrix inversion, and residual simplification;
all control fixtures are rational. There is no sampling or fitting.
Finite-wavelength terms, coefficient derivatives, scalar masses,
cosmological time variation, and background tadpoles are excluded. This is
not a solved asymptotically flat background, an on-shell localized source,
or a global Green function.

## Direct action and spatial stress

Expanding the invariants gives

    Y2 = |grad pi - (q/s) grad sigma|²,
    L_PW,2 = -PX |grad pi|²
             +s WY |grad pi-(q/s) grad sigma|²
             -W0 |grad sigma|²/(2s).

For the cubic term, integration by parts in the original action gives

    sqrt(-g) gamma X Box chi
      = divergence - gamma sqrt(-g) grad X . grad chi.

Staticity and alignment imply `delta X=-2q² Phi`; hence its quadratic
spatial derivative action is exactly

    L_3,2 = 2 gamma q² grad Phi . grad pi.

There is no principal spatial-metric variation in this expression.
Varying the integrated covariant expression with respect to the inverse
metric, using `delta X=-v_mu v_nu delta g^mu nu`, and integrating the
derivative of that variation gives

    T3_mu nu = 2 gamma [ (Box chi) v_mu v_nu
                        -v_mu H_nu a v^a -v_nu H_mu a v^a
                        +g_mu nu v^a H_ab v^b ],

where `v=dchi` and `H=nabla dchi`. The code evaluates this tensor on a
static perturbation Hessian and obtains

    delta T3_00 = 2b Delta pi,
    delta T3_ij = 0                           [principal order].

For the Einstein sector the script independently computes the Christoffel
symbols, Ricci tensor and curvature of
`diag(-exp(2epsilon Phi),exp(-2epsilon Psi),exp(-2epsilon Psi),exp(-2epsilon Psi))`.
After removing quadratic total derivatives it obtains

    L_EH,2 = M2 [ |grad Psi|² - 2 grad Phi . grad Psi ].

It also constructs the full three-dimensional Fourier linearized Ricci and
Einstein tensors from the metric perturbation rather than from this reduced
Lagrangian. The result is

    G00 = 2 Delta Psi,
    Gij = (partial_i partial_j-delta_ij Delta)(Psi-Phi),
    R00 = Delta Phi.

The spatial trace is `-2 Delta(Psi-Phi)`. For nonzero spatial Fourier k it
forces `Psi=Phi`, including wavevectors with some components zero. No
off-diagonal division by `kx ky` or a preassigned slip is used.

## Clock elimination and minimal source normalization

Set

    A=2PX-2s WY, B=2q WY, D=(W0-2q² WY)/s.

The raw scalar gradient matrix is `[[A,B],[B,D]]`. At `D!=0`, `k²!=0`, the
clock constraint gives

    sigma=-(B/D)pi,
    G0=A-B²/D.

The complete leading static quadratic action, now including minimal dust,
is

    L2 = M2[(grad Psi)²-2 grad Phi.grad Psi]
         -G0(grad pi)²/2 + 2b grad Phi.grad pi -rho Phi.

Its equations, together with the independently varied spatial Einstein
equation, are

    2M2 Delta Psi = rho+2b Delta pi,
    Psi = Phi                                  [k²!=0],
    G0 Delta pi-2b Delta Phi = 0.

Thus `Phi=Phi_GR+(b/M2)pi` and `G Delta pi=b rho/M2`. The exact source
normalization `Phi_GR_hat=-rho_hat/(2M2 k²)` is independently checked using
the trace-reversed minimal dust Einstein source. This reproduces the prior
boosted lapse result at zero source velocity and additionally derives Psi.

The script retains an independent `g0x` perturbation long enough to vary it
in the original invariant action. The static first-gradient momentum
stress is

    T0i = 2q PX partial_i pi + W0 partial_i sigma
          -2 gamma q³ partial_i Phi.

After regular clock elimination this is
`q partial_i(G0 pi-2b Phi)`, which vanishes on the nonzero-k scalar-current
constraint. This control checks the first-gradient momentum relation; it
does not solve the remaining subprincipal equations.

## Connection to scalar propagation

The fixed-metric temporal action gives `K0=2PX+4q² PXX`. Direct contraction
of the cubic stress with the trace-reversed Einstein equation yields the
same gravitational corrections as the earlier boosted calculation:

    K=K0+6b²/M2,
    G=G0-2b²/M2,
    D_scalar(omega,k)=G k²-K omega²,
    c_s²=G/K.

The physical static enhancement is therefore

    E=Phi/Phi_GR=G0/G=1+2b²/(M2 G).

If `K>0` and `G>0`, this enhancement is at least one, and is strictly larger
than one for nonzero b. These two inequalities are conditions on the reduced
scalar principal coefficients; they do not certify the health or degrees
of freedom of the complete theory. The lensing combination
`(Phi+Psi)/2` equals the same common potential at this order.

For finite nonzero b and M2, the formal `G -> 0+` response diverges. This is
the same zero-gradient scalar denominator, not an independently adjustable
static response factor. The omitted lower derivatives and nonlinear terms
need not remain small in this limit. A moving-source pole uses
`omega=w.k` and needs its own retarded prescription, as in the sibling
boosted report; the present result is the stationary aligned specialization.

## Degenerate cases kept separate

Before any clock division, the raw Fourier equations are

    k² [  0    -2M2    2b     0 ] [Phi  ]   [rho]
       [ -2M2   2M2     0     0 ] [Psi  ] = [ 0 ]
       [  2b      0    -A    -B ] [pi   ]   [ 0 ]
       [   0      0    -B    -D ] [sigma]   [ 0 ].

The determinant of the displayed matrix is
`-4M2[M2(AD-B²)-2b²D]`. The code computes it and reinserts the solved vector
into all four source equations.

- At `k=0`, all displayed principal rows vanish. The homogeneous sector is
  a different problem determined by the background and lower derivatives.
- At `D=0`, `B!=0`, the raw matrix is invertible, with determinant
  `4M2² B²`. It gives `pi=0`, `Phi=Psi=Phi_GR`, and
  `sigma=-b rho/(M2 B k²)`. The clock Schur quotient is invalid here;
  invertibility of this static matrix is not a full kinetic health claim.
- At `D=B=0`, the clock principal row is undetermined. For q>0 this is
  `W0=WY=0`; solve the remaining three-field block without a clock quotient.
- At regular `D!=0` and `G=0`, the vector
  `(b/M2,b/M2,1,-B/D)` is an exact null vector. Compatibility with the source
  requires `b rho=0`. Thus nonzero b and nonzero density have no finite
  solution to this leading static system. An exact rational rank control
  separately verifies that source incompatibility.
- If instead `b=G0=0`, the scalar principal row is undetermined and the
  minimally sourced metric still has its GR value.
- At `G0=0`, `b!=0`, the regular solution has `Phi=Psi=0` and
  `pi=rho/(2b k²)`. The field equality survives, but `Psi/Phi` is undefined.
  Here `G=-2b²/M2<0`, so a positive-K reduced scalar has a gradient
  instability. This is not a healthy static suppression mechanism.

## Verification and provenance

Run `derive_static_metric.py` with Python 3.9.6 / SymPy 1.14.0; it prints
JSON by default and writes only an explicit `--output` path. The contract is
`contract.json`. The recorded bounded run is in `run_001/`, with
`result.json`, `stdout.txt`, `stderr.txt`, and a version 2 `manifest.json`.
The exact command and input hashes are recorded in that manifest.
The bounded run completed with exit zero in 5.18 seconds, all 68 exact
checks passed, and `validate_manifest.py .../run_001/manifest.json --root`
accepted the record and its file hashes. The runner recorded the then-current
repository revision `4738604358a312684b259310ba079df8d7a96265` with a dirty
worktree; the dispatched base revision above is retained separately.

The checks compare invariant action expansion, direct curvature expansion,
the full 3D Einstein tensor, the cubic stress, the clock Schur reduction,
the raw sourced four-field inverse, zero-denominator compatibility,
GR decoupling, `WY=0`, `W0=0`, and an exact positive-coefficient control
`PX=2,PXX=0,WY=0,W0=1,q=s=M2=gamma=1`, which gives
`G=2,K=10,E=2`. This fixture tests normalization and algebra; it is not a
claimed solution of the background field equations.

Mathematical proofreading covered this complete report after derivation.
The final self-review changed only explanatory prose; it made no
mathematical-token changes and left no unresolved notation or display issue.

The structural result is an action-derived local susceptibility and static
slip relation. The remaining physical implication is to establish a
solution of the same background and localized-source equations, retain the
terms omitted by the principal approximation, and perform any claimed PPN
or phenomenological matching on that solution. This checkpoint supplies
none of those missing implications.
