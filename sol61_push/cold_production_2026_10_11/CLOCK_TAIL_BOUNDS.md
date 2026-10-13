# Conditional analytical bounds on the uncomputed momentum tails

Status: an analytical reduction and numerical evaluation give very small
conditional infrared and ultraviolet energy bounds for the J=10 clock pulse.
The duration and crossing assumptions are supported by the stored numerical
trajectory, not an interval-certified background solution. This distinction
is separate from the finite-band numerical quadrature in CLOCK_ENERGY.md.
No nonlinear, primordial-fluctuation or cosmological-origin claim is made.

## Assumptions and background bounds

Use the exact homogeneous classical action and initial data in
AUTONOMOUS_CLOCK.md, with J=10, delta=0.01 and initial total energy 6 in
units M^2 L^2. Assume the pulse exits within T<=2. For the infrared bound
also assume s'>=0.8 during each edge. The computed trajectory has exit time
1.58116461 and sampled minimum speed 0.83666788, supporting these assumptions
with a margin. These sampled values are not a mathematical proof of them.

Let H be the 2-by-2 fluctuation Hessian and U=H-diag(1,0). U is compactly
supported in time, continuous, and piecewise twice differentiable. Its first
derivative can jump at the four edge boundaries. Positive energy implies

    |y|, |y'| <= sqrt(12),    |y''| <= 4 sqrt(12),
    |s'| <= sqrt(12/10),
    |s''| <= (3/20) max|W'| * 12.

The quintic ramp obeys

    |W|<=1, |W'|<=1.875/delta, |W''|<=6/delta^2,
    |W'''|<=60/delta^3, |W''''|<=360/delta^4

on each smooth piece. The W'' bound is deliberately larger than its actual
maximum. These follow by differentiation of the polynomial; finite-grid
checks in the script are supplementary, not the proof of the inequalities.

Bounding a symmetric matrix's operator norm by the sum of absolute diagonal
bounds plus twice the off-diagonal bound gives

    ||U|| <= u0 = 109235.376,
    ||U'|| <= u1 = 118957920.985,
    ||U''|| <= u2 = 115291915934.096   on smooth pieces.

Each boundary jump in U' is bounded by 118308072.422. Only the clock-clock
entry jumps: W'' is continuous and W''' jumps. Thus usable integral bounds are

    I0 = T u0 >= integral ||U|| dt,
    I1 = T u1 >= integral ||U'|| dt,
    I2 = T u2 + 4 jump >= total variation of U'.

Also set U2=T u0^2, UU1=T u0 u1, U3=T u0^3 to bound the respective integrals
of ||U||^2, ||U|| ||U'|| and ||U||^3. The script evaluates the entrywise
derivative formulas directly, including y'', s'' and all four jumps.

## Ultraviolet reduction

Take k>=K=10000. The exterior frequencies are Omega=diag(sqrt(k^2+1),k),
with ||Omega-kI||<=1/(2k). In the free oscillator interaction representation,
remove the number-preserving Hermitian generators by unitary transport.
The remaining matrix amplitudes have the form

    a' = exp(2ikt) B(t) b,
    b' = exp(-2ikt) C(t) a,
    a(0)=I, b(0)=0,

with unimportant sign conventions absorbed into B,C. Their norms obey
||B||=||C||<=||U||/(2k). The final b is the Bogoliubov beta up to unitary
factors, so it has the same singular values. Gronwall gives
||a||,||b|| <= G=exp(I0/(2k)).

For completeness, write the untransported pair generator F as the normalized
U multiplied by residual frequency phases. If D is the number-preserving
generator, then

    ||F'||, ||D'|| <= ||U'||/(2k)+||U||/(2k^2),
    ||F''|| <= ||U''||/(2k)+||U'||/k^2+||U||/(2k^3).

Unitary transport gives

    ||C'|| <= ||F'||+2||D||||F||,
    TV(C') <= integral [||F''||+4||D||||F'||
                       +2||D'||||F||+4||D||^2||F||] dt,

where distributional jumps are included in the first term. Since C vanishes
outside the pulse, integrate the equation for b by parts once, and integrate
the term containing C'a a second time. Extend C' by zero so its endpoint
terms are included in its total variation. Taking norms yields

    ||b(T)|| <= G { [TV(C') + integral ||C'|| ||B|| dt]/(4k^2)
                   + integral ||C|| ||B|| dt/(2k) }.

Substitution gives the explicit bound ||beta||op <= C_K/k^3 for every k>=K,
where

    C_K = exp(I0/(2K)) * {
          (I2+U2)/8
          + (I1/4+7 UU1/16)/K
          + (I0/8+7 U2/16+3 U3/16)/K^2 }.

Using K instead of k increases every positive coefficient. Numerically
C_K=1.83080e15. There are two species, so the total occupation is at most
2 C_K^2/k^6. The energy tail consequently satisfies

    rho_UV/M^4 <= C_K^2 sqrt(1+K^-2)/(2 pi^2 K^2)
                = 1.69805e21.

This is deliberately much looser than the observed tail. Its purpose is to
control arbitrarily high momenta without extrapolating a sampled power law.
The conclusion depends on the specified classical linear equations and the
finite duration assumption; it does not supply a UV completion of the action.

## Infrared reduction

For 0<k<=k0=0.001 choose nu=sqrt(1+u0+k0^2). In the fixed phase-space scaling
(q,p)->(sqrt(nu)q,p/sqrt(nu)), the generator norm on an edge is at most nu.
The two edges together last at most 2 delta/0.8=0.025 under the crossing
assumption. On the plateau the constant-frequency transfer has norm at most
1+nu T: its diagonal cosines have norm <=1, and each off-diagonal block
has norm <=nu T. Returning to unscaled canonical coordinates gives

    ||S|| <= nu (1+nu T) exp(nu * 0.025) = 8.48228e8.

For the incoming two-oscillator vacuum the covariance trace is
(omegaY+1/omegaY+k+1/k)/2 <=2/k in this band. Its outgoing excitation energy
is no larger than its total oscillator energy, so

    rho_IR/M^4 <= (1+k0^2) ||S||^2 k0^2/(4 pi^2)
                = 1.82249e10.

The exact massless zero mode is not assigned a vacuum. The bound applies to
the continuum limit k approaching zero and proves integrability there under
the stated assumptions. A coherent classical zero mode is a separate input.

## Physical consequence and evidence status

With the inherited example M=2.00000099999975e-12 eV and source density
9.71510619e6 eV^4, the conditional fractions are

    UV tail <= 2.79656e-33,
    IR tail <= 3.00151e-44.

The finite-band envelope estimate was 1.43404e-47. Thus even the very loose
conditional tails are far below the initial eta about 5e-7 budget. Within
this linear vacuum model, the analysis strongly supports negligible heating
from preparation. It does not bound an arbitrary primordial classical
spectrum or nonlinear growth.

`clock_tail_bounds.py` evaluates these constants and checks numerical support
for the duration/crossing premises. Its three declared checks pass; polynomial
sample assertions also pass. `clock_tail_bounds_run/manifest.json` pins the
inputs and result. The analytical argument is self-reviewed, not independently
refereed, and the numerical premises are not interval certified. The broad
cold-energy goal remains open: supplied displacement/phase, autonomous cosmic
history, abundance, carrier transport and galaxy-law selection are unresolved.
