# IC11: explicit transition repair, followed by a scalar kinetic failure

2026-09-08. Base commit `347950889570a839af41f6bef0c8bcba7531d02a`.
**Constructive partial completion; full theory OPEN.** This report gives an
explicit action correction, its preserved restrictions, and a failed necessary
scalar kinetic test. It is neither a global impossibility theorem nor a claim
that the corrected candidate meets the requested physical theory.

## Full IC10 transition, with the omitted spatial block restored

Use the complete [IC10 action](IC10_LOCAL_CLOCK.md) and the definitions and
boundary prescription of [IC5](IC5_ACTION.md). Numerical units are
`m=h0=1`, `kappa=6`, with the same fixed `a0²` and `Lambda`. At barred unit
volume, set `rho=pi/V`, `q=(xi,u)`, `w=(u-1)xi`, and

    E=exp((4-3u)xi),  J=exp(-2w-1/6),  p=exp(-3w)rho,
    r=-E rho/3,  A=1+eta(r)(J^-1-1),
    Z=p² F/a0²,  C_R=1+eta(r)(J-1)+(1-eta(r))Z.

Here `J` is IC10's exponential `J9`, not IC5's gradient invariant. The
homogeneous Hamiltonian density is

    h=-E rho² A/3 + exp((3u-2)xi)[Lambda+a0² U(u²)]
                     -3 exp((3u-4)xi).

The code differentiates this full expression, including both switch jets.
It solves `h_xi=h_u=0` at every sample. With `M=h_qq`, the spatial auxiliary
constraint pencil is `Q(k)=M+k²G`, where

    ell=ln(9/5),  Tcal=-27/16+54/(5ell),
    alpha=81/(8 Tcal²),  d=-9/(8 Tcal),
    beta=2d-1/3-3alpha/4,
    gamma=1/16+9alpha/64-3d/4,

    W = [[0,u xi],[u xi,xi²]]
        + 3p²/(8a0²ell²) [[alpha,beta/2],[beta/2,gamma]],
    G=-2(1-eta)exp(u xi)W.

Indeed the gradient Hamiltonian is
`-(1-eta)exp(u xi) (Dbar q)^T W (Dbar q)`: the second term in `W` follows
from IC5's `D Jbar` term. It cannot be omitted. The code also checks this
matrix against numerical second derivatives of the uncollected IC5 density.
The wavenumber is a barred Fourier wavenumber in the unit-volume convention;
the displayed poles are values of `k²`, not physical frequencies.

Start on the independently solved IC10 pressure branch at `S=0.2`, giving
`rho0=-2.39031634450677167`, and solve the actual auxiliary equations for
`rho=rho0+n/1000`, `n=0,...,500`, by continuation from the previous root.
The geometric switch boundary `r²=5/4` is first crossed on this grid at
`n=63`. Close to it, `eta` rounds to one at 60 decimal digits; `1-eta` is
therefore evaluated separately with a cancellation-free logistic formula.
This matters for very large finite auxiliary poles.

At all 501 samples `M` is negative definite; its largest eigenvalue never
exceeds approximately `-3.55249`. The largest auxiliary residual is below
`7.4e-51`. This is floating-point evidence at these roots, not an interval
bound between them. The background is expanding: for example at `n=200`,
`Hphysical=0.851398687653` and `rhodot=1.20707256281`.

| n | xi | u | eta | original cT² | original positive k² pole |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 200 | 0.219572836054 | 0.622175269506 | 0.998521679441 | 0.999973381600 | 14564.3070333 |
| 220 | 0.225471115191 | 0.625545200865 | 0.997219397004 | 0.999990352791 | 22674.5230510 |
| 500 | 0.308586741029 | 0.666131555711 | 0.995740599822 | 1.000746122737 | none |

Poles are computed from the actual polynomial `det(M+xG)`, not a sign flag.
For example, substitution of the `n=200` positive root gives a normalized
determinant residual below `1e-45`. A singular auxiliary pencil obstructs
this elimination at that Fourier scale; it alone does not establish a
physical degree-of-freedom count or a propagating instability.

## Explicit new trial action

Define `S11=integral sqrt(-g)[2P:Q-H11]+Sm[g,psi]`, with the same fields and
ordinary matter coupling as IC10, and set

    H11=H10+deltaH,
    deltaH= -m/2 (A^-1-C_R) Rhat
            -m eta(1-eta)(1+tr(W²)) (|Dxi|²+|Du|²).

All spatial contractions use the physical leaf metric. The displayed `W`
uses `m=1`; to retain an arbitrary `m` in dimensional units its second term
has `m²a0²` in the denominator. Likewise `Z=p² F/(m²a0²)` and
`r=-Np/(3mh0)`. This is a local phase-space action with no derivatives of
the momentum. Since `J>0` and `0<=eta<=1`, `A>0`, so its reciprocal is
defined. The coefficients are specified functions, not new fitted constants.

On every flat homogeneous background both correction terms vanish for all
`rho,xi,u`; the full homogeneous Hamiltonian and all its derivatives thus
remain exactly the ones just solved. On the entire `eta=1` plateau,
`A=J^-1`, `C_R=J`, and the correction and its first jets vanish. At the
static `p=0` restriction, `eta=0` on a neighborhood and `Z=O(p²)`, so the
correction and its first jets also vanish, even for nonzero spatial
curvature or auxiliary gradients. Consequently the stated static equations
and the IC10 local plateau result transfer under the same boundary
prescription. This does not transfer unproved galaxy matching or lensing.

On an isotropic flat background a transverse-traceless perturbation has no
linear trace momentum or scalar curvature perturbation. Its momentum and
curvature coefficients therefore give

    original cT²=A C_R,
    corrected cT²=A [C_R+(A^-1-C_R)]=1.

The positive tensor kinetic sign follows from `A>0`. This is an exact
isotropic tensor identity; no anisotropic or matter-coupled characteristic
theorem is asserted.

The corrected spatial auxiliary matrix is

    W11=W+eta[1+tr(W²)]I,
    G11=-2(1-eta)exp(u xi)W11.

For any real symmetric `W`, an eigenvalue `lambda` of `W11` obeys

    lambda(W11)>=lambda+eta(1+lambda²)
                  >=eta-1/(4eta)>0,  if eta>1/2.

Thus this correction gives an exact positive-definiteness guarantee in
that activation range. At the sampled roots, `eta>=0.9957405998` and `M<0`;
hence `M+k²G11<0` for every real `k`, including `k=0`. This last assertion
is an all-wavenumber matrix argument at each sampled background, conditional
on its numerically evaluated `M<0`, not a continuum background theorem.
All corrected positive auxiliary poles disappear from the computed sample.

## The next scalar obstruction is exposed, not repaired

For `0<eta<1` in the positive-definite `W11` range, the two auxiliary
gradient directions have full rank. At fixed scalar geometry their response
to the scalar momentum falls as `k^-2`. In the scalar momentum normalization
used by the IC8 reduced block, the remaining ultraviolet momentum Hessian is

    aUV=E A/6+h_rhorho/4.

The first term is the scalar trace-free momentum contribution after the
spatial shift constraint; the second is the trace Hamiltonian Hessian.
At fixed `q`, `r` is linear in `rho`, and differentiating the displayed `h`
gives the independent identity

    aUV=-E(J^-1-1)[4r eta_r+r² eta_rr]/12.

The `-2EA/3` part of `h_rhorho` cancels `EA/6`; the remaining terms are the
switch derivatives. The code checks the identity symbolically with an
arbitrary two-jet of `eta`, and separately checks `h_rhorho` by numerical
differentiation of the raw Hamiltonian. No expected numerical values are
entered into the model.

| n | corrected aUV | corrected minimum eigenvalue of W11 |
| ---: | ---: | ---: |
| 200 | +0.0451910585191 | 1.04637237245 |
| 220 | -0.237588597863 | 1.04575844538 |
| 500 | -7.10895574195 | 1.07779900041 |

The first sample with `aUV<-1e-30` is `n=205`. The negative sign also
persists in the finite-wavenumber momentum Schur complement
`aUV-(h_rhoq/2) Q11^-1 (h_qrho/2)` at `k²=1e12` and `1e16` for `n=220`,
and its difference from the UV limit decreases as expected. It fails a
necessary local positive kinetic condition for this scalar block. The
construction has repaired the isotropic tensor coefficient and auxiliary
inversion, but it has not produced a stable full transition theory.

On `eta=1`, the gradient rank drops to zero and this full-rank UV reduction
does not apply. Its formal zero there does not contradict IC10's healthy
plateau clock after algebraic elimination. Limits `k->infinity` and
`eta->1` cannot be exchanged without a separate analysis.

The next constructive task is a homogeneous trace/shear redesign that
keeps a positive reduced scalar kinetic coefficient while preserving the
required restrictions, followed by the full characteristic and constraint
calculation. This report rules out only this trial as a healthy completion;
it does not rule out that redesign or other actions.

## Reproduction and scope

From this directory, run:

    python3 -m unittest test_ic10_transition test_ic11_transition_completion
    python3 ic10_transition.py
    python3 ic11_transition_completion.py
    python3 ic10_transition.py --require-full-closure
    python3 ic11_transition_completion.py --require-full-closure

The ordinary reports emit JSON and exit zero. Both strict reports emit the
same scientific result and exit **2** because full closure remains open.
The tests first failed for the absent transition/repair functions, then were
run against the implementation. Checks cover switch derivatives, direct
Hamiltonian derivatives, plateau matching, auxiliary preservation, the full
spatial variation, actual poles, repair identities and first jets, and the
negative scalar UV limit. Selected roots are repeated at 85 decimal digits.

Numerical results concern a finite, deterministic 501-point vacuum family,
using mpmath at 60 decimal digits and SymPy for the identity checks. They
are not interval-certified, do not count global field-theory modes, do not
establish all-background causality or strong coupling, and do not prove the
baryon-only AQUAL equation, PPN limits, lensing, the a0 normalization, or a
realistic cosmological history. The repository was already dirty; only the
two transition scripts, their two test files, and this report were assigned
for this construction.
