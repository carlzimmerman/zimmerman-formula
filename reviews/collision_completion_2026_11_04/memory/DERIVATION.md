# Actual continuum four-state response

Work in mu=1 and tau=mu t. Let G=lambda vv† be the recorded production Gram
(its finite rank-one residual is checked), and Gamma the recorded positive
4×4 neutral absorptive matrix. For a charged pair p1,p2 with angle cosine c,

    P²=p1²+p2²+2p1p2 c, EN=sqrt(M²+P²), Ei=sqrt(mC(x)²+pi²),
    delta(x)=EN-E1-E2, Gamma_lab=M Gamma/EN.

The actual charged mass is mC(x)=.003 sqrt(x²+2/(31*.003))/2. On a recorded
harmonic orbit x=xmid+A_x cos(theta), theta=omega tau,

    delta=delta0-A cos(theta), A=A_x*mC*mC'*(1/E1+1/E2).

The omitted quadratic orbit correction is bounded numerically relative to
the smallest neutral width. Slowly varying WKB normalization of the source
is evaluated at xmid; its fractional mass variation is separately tiny.

The retarded positive-frequency equation is

    da/dtau=-(Gamma_lab/2+i delta(tau) I)a+v.

This is the actual four-state matrix equation of the fixed tree packet, with
an incoherent ensemble of occupied incoming pair modes. Diagonalizing Gamma
is an exact basis change, not four independent replacements of production
branching. In its eigenbasis write c=U†v and gk=M gamma_k/EN. A periodic
phase transformation gives the orbit-averaged density

    rho_pair = lambda/(4 E1 E2 EN) *
       sum_n J_n(A/omega)² R_n v v† R_n†,
    R_n=[Gamma_lab/2+i(delta0+n omega)I]^-1.

Every summand is positive. The neutral exit rate per physical pair is
Tr(Gamma_lab rho_pair). Channel exits use Tr(Gamma_a,lab rho_pair), preserving
coherence. This is a continuum source calculation: integrate q1²dq1 q2²dq2
dc/2 with the actual recorded, cell-constant fC(q1)fC(q2). CT09 fC=2 fS;
the factor cancels in normalized pair averages, and is restored by
n+=n-=12 Tc³/(2pi²) integral q² fS dq. Distinct pair modes are not coherently
summed. The mode's sidebands remain coherent before its time average.

Normalization can be checked against the exact CT09 stationary expression.
With D=[(s-M²)I+iM Gamma]^-1 and lab Moller flux, its Born neutral-exit rate
is sqrt(s)/(E1E2) Tr(G D Gamma D†). Near the positive-frequency pole,
D=(2EN)^-1 R and sqrt(s)=M to leading resonant order. Therefore it becomes
lambda/(4 E1E2 EN) Tr(Gamma_lab R vv†R†), as used here. Incoming charged
width resummation is initially excluded dynamically and is measured as a
separate stationary correction. This is not a claim to have solved the full
threshold retarded self-energy or matched its dispersive part.

The parent density is n+ n- times rho_pair integrated over incoming modes.
Its delayed free evolution is exactly rho(t+dt)=K rho K†, K=exp[-(iH+Gamma/2)dt].
For a positive constant matrix source S the API uses a Van Loan exponential
to integrate the source without erasing coherences. Exact driven injection
is not generally a positive instantaneous population source. A separate
coarse-grained positive source Gamma^(1/2) rho Gamma^(1/2) preserves the total
exit trace; its error relative to {Gamma,rho}/2 is reported. That closure
requires review before using it in a full coupled history.

The incoming continuum characteristic function C(tau)=<exp[-i(delta0-<delta0>)tau]>
is computed explicitly. Its decay is distinct from neutral damping. A finite
time or periodic calculation need not share the stationary local rate even
when production is weak. For the passive fixed-width model, each resolvent
satisfies R† Gamma R <= 4 Gamma^-1. Since sum_n J_n²=1, the period-averaged
rate is bounded by the perfectly tuned static peak (up to the explicitly
retained relativistic prefactor). This bound does not prove a global history
and does not apply to an unspecified occupied/active medium.

## Two distinct local reductions

The completed finite test rejects use of a stationary inverse/BW evaluated at
each field phase as a uniformly accurate source across the late window.
It does **not** reject elimination of the neutral response after averaging a
whole periodic orbit. Gamma_min/omega=.06006 gives exponential forgetting of
initial parent amplitudes, while H/omega is 3.23e-11 at the initial late
endpoint and 3.23e-13 at the final endpoint. The actual retained orbit
modulation is rapid; its slowly drifting envelope is the quantity required
to be adiabatic for a quasi-periodic source table. Using the saved harmonic
amplitude scaling A_x proportional to exp(-3N/2), the envelope diagnostic
1.5*A*H/Gamma_min² is about 2e-7 initially and 6e-11 finally. This is a
conditional rationale for orbit-averaged Floquet rates local in N, subject
to the omitted charged/medium self-energy, not a restoration of the
instantaneous stationary BW approximation.

The actual four-state ODE check starts from an empty parent at a real occupied
pair mode and integrates 32 periods. Its last two-period average agrees with
the corresponding Floquet sum to 2.1e-6 and 2.1e-5 at the two endpoints.
The periodic boundary condition therefore does not artificially assume a
prompt decay; neutral memory is allowed to build and relax over many orbits.

## Numerical checkpoint

`run_response002` is completed and all eleven declared controls pass.
Endpoint finer quadrature gives dynamic/static pair rates 57.757633/63.136784
at Tc=1e-5, and 13920.750705/1977.910730 at Tc=1e-6, in mu^-2. The early
dynamic 3-to-5 radial and 12-to-20 angular refinement changes it by .434%;
the final change is below 1e-10. The exact-s normalization differs from the
analytic stationary leading-resonance value by .0583% initially (its finite
phase quadrature still has error) and below 4e-9 finally. Linearizing the
actual mass detuning costs at most 1.61e-5 of Gamma_min on the endpoint
check; this cannot account for the factor-seven late memory modification.

The actual continuum has |C(Torbit)|=.16660 and .999561 at the endpoints;
its inverse RMS detuning is .33746 and 33.732 orbital periods. Neutral
lifetimes alone would miss this change in continuum phase support.
The fixed-physical-Gamma passive peak bound is 15741.999837 mu^-2.

The CT09 parent basis was aligned independently by the cascades work package.
Its `run_basis002/result.json` daughter-pair matrices sum to the same Gamma.
Their contractions with the computed coherent parent density are positive
and sum to its neutral exit trace. These contractions use rest widths on
the integrated density; their boost discrepancy is bounded by the reported
maximum M/EN difference (6.76e-6 initially, 6.76e-8 finally). The total
dynamic event rate retains the mode-by-mode boost exactly.

`run_response001` is a valid **failed** record, preserved with its original
source files. Its auxiliary detuning test compared opposite phase
conventions, causing a large false residual. The rates and independent ODE
controls are invariant under that phase shift, but only the corrected
separately named v2 source/run supplies the completed evidence. No existing
source or result was silently replaced.
