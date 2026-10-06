# Source-generated clock toward cosmology: finite shooting has two distinct targets

The conserved epsilon=.01 source now continues to r=.003, approximately34.2 r_cos, at two tolerances for three central clock-lapse values. A finite lapse-zero target and the selected flat deSitter clock-mode target differ. Direct variation gives the outer linear radial modes and identifies the remaining normalization mode; approaching w=1 at finite radius does not complete the cosmological boundary problem.

## Frozen theory and extension contract

The parent REPORT/core.py are untouched. The same logKGB action, detuned P2 response, M=H=A=1, eta=.5, epsilon=.01, proper constant density rho=6e6 and central pressure4 are retained. Central lnN0 is varied through -6e-6,0,+4e-6; for every value the center cubic, fluid surface and source mass are recomputed. The source remains a conserved static Killing perfect fluid with its full ADM momentum source. No exterior scalar charge or material cold mass is added.

For numerical conditioning, shoot.py evolves ell=lnN-lnN0 while retaining absolute lnN=ell+lnN0 in U(N). The lapse normalization cancels from the ratio variables Nprime/N,V/N and matter redshift ratio F/F0; pressure uses rho+p=(rho0+p0)N0/sqrtF. This avoids losing the O(r²) center increment below a finite lnN0 offset. It is a coordinate change in the calculation, not a change of vacuum potential or source normalization.

Every integration phase has200k RHS evaluations/30s cap. The outer runner caps each two-tolerance invocation at60s wall/30s CPU, one cooperative numerical-library thread and1MiB logs. These are per-phase limits, not aggregate200k across all cases. Finite target radii3e-5,3e-4,.003 sample the transition from.342 to34.2 r_cos, all far inside H^-1=1. A failed -4e-6 invocation is preserved: argparse treated a separated negative scientific-notation token as an option. It produced no mathematical result. The replacement negative case has a fresh contract and uses --lnN0=-6e-6. No radius/resource escalation beyond this declaration is claimed.

## Exact constant-clock vacuum benchmark

vacuum_checks.py directly varies the same radial action, using the exact constant ansatz N=Nc,B=beta,V=Nc x r. Acceleration is zero, so detuning has no effect. Dividing E_B by MNc and E_N by M beta gives respectively

    1-beta^-2+r²[3x²+u0],
    1-beta^-2+r²[3x²+6eta Hx+u0+6etaH²],
    u0=-3H²+6etaH²lnNc.

The shift Euler equation vanishes. Their difference forces x=-H; the r² coefficient then forces lnNc=0 for eta>0. The constant coefficient forces beta=1. Thus the selected exact flat deSitter benchmark is N=B=1,V=-Hr. Arbitrary constant lapse with the same fixed U is not another member of this exact ansatz. This does not classify all deSitter slicings, nonconstant-clock vacua or large-radius solutions.

## Directly varied full radial linear modes

Set H=1, N=1+ell, B=1+b, V=-r(1+ell+u), w=-V/(rN)=1+u, and k=dell/dt, t=lnr. linear_checks.py takes the actual first variation of the radial action, including the log vacuum response and kappa=1-epsilon response. Solving its three Euler equations for bprime_t,uprime_t,kprime_t yields

    ellprime=k,
    bprime=(eta-1)k,
    uprime=-3eta ell-b/r²-3u+(r^-2-eta)k,
    kprime=(3eta²r²/kappa)ell+(eta/kappa)b-k.

Thus C_lin=b+(1-eta)ell is conserved by the linearized equations, and

    ellsecond+ellprime+[mu-nu r²]ell=eta C_lin/kappa,
    mu=eta(1-eta)/kappa, nu=3eta²/kappa.

This is the full r-dependent linear equation, not an autonomous frozen eigenvalue approximation. In radial coordinates it is r²ellsecond_r+2r ellprime_r+(mu-nu r²)ell=eta C_lin/kappa. Its homogeneous solutions are r^-1/2 times modified Bessel solutions of order sigma with sigma²=1/4-mu, at argument sqrt(nu)r: substitution yields z²ysecond+z yprime-(z²+sigma²)y=0. This is an elementary reduction, with no source-dependent named theorem used. A real basis is required when sigma is imaginary. A particular regular series has a0=C_lin/(1-eta), a_j=nu a_(j-1)/[(2j)²+2j+mu] for powers r^(2j). These formulas describe the linear system; extending their formal large-r growing/decaying modes beyond the controlled small perturbation/static patch is not a cosmological boundary theorem.

For r<<1, the clock pair has exponents

    lambda_plus/minus=(-1 +/- sqrt(1-4mu))/2,

which here are -.5 +/- .05025189 i. The clock perturbations decay with r^-1/2 in this restricted scale interval, toward the approximately constant C_lin/(1-eta) offset if C_lin is nonzero. The r² correction prevents interpreting that offset as an exact arbitrary-lapse vacuum solution. There is also an independent u_h=c r^-3 mode with ell=b=k=0. Its physical metric change is deltaF=-2c/r: it is a mass-type integration mode in linear vacuum perturbations, not a material cold dust density or cold-particle identity. For general H its coefficient is m/H². Clock-forced flow modes coexist with it, so the computed u is not identified directly with that pure mass mode.

The nonlinear vacuum equation gives exactly

    d[b+(1-eta)lnN]/dt=eta k(1/w-1).

Consequently C_lin is only a linear diagnostic, not an exact nonlinear invariant. It is a necessary mode diagnostic for the specifically declared flat N=B=1,w=1 benchmark, not a universal condition for every asymptotically locally deSitter slicing. Near the source, w differs strongly from1 and the diagnostic varies appreciably; by3e-4 and.003 the tabulated change is only a few1e-12.

## Recomputed source and finite residual map

At the finer tolerance3e-8, all three source radii are8.77305426e-7 within their small differences; leading source m≈6.75231115e-13. The coupled rho,p source and mass are recomputed for each lnN0; neither is held as an independently imposed exterior parameter. Every case reaches.003 at both tolerances. The tighter exterior call counts are186659,186148,186007 for the negative,zero,positive offsets, below the declared200k per phase. Two-tolerance endpoint lnN differences are about1e-12 or less and w differences about1e-12 at.003, despite larger phase differences earlier.

| ln N0 | r | ln N | C_lin | w−1 |
|---:|---:|---:|---:|---:|
| -6.0e-06 | 3.0e-05 | -2.416651171e-06 | -5.328115158e-07 | -3.625563560e-01 |
| -6.0e-06 | 3.0e-04 | -1.361677818e-06 | -4.220460336e-07 | -3.080886482e-03 |
| -6.0e-06 | 3.0e-03 | -1.006413318e-06 | -4.220419443e-07 | 9.784610118e-05 |
| 0.0e+00 | 3.0e-05 | 3.583348860e-06 | 2.467188575e-06 | -3.625566080e-01 |
| 0.0e+00 | 3.0e-04 | 4.638323165e-06 | 2.577954978e-06 | -3.083157738e-03 |
| 0.0e+00 | 3.0e-03 | 4.993595301e-06 | 2.577959485e-06 | 9.545329978e-05 |
| 4.0e-06 | 3.0e-05 | 7.583348880e-06 | 4.467188635e-06 | -3.625567718e-01 |
| 4.0e-06 | 3.0e-04 | 8.638323819e-06 | 4.577955652e-06 | -3.084671960e-03 |
| 4.0e-06 | 3.0e-03 | 8.993601047e-06 | 4.577960438e-06 | 9.385809627e-05 |

The .003 lapse residual brackets zero. Secant interpolation gives lnN0≈-4.99358813e-6 for lnN(.003)=0. The C_lin residual also brackets zero, but its interpolated target is lnN0≈-5.15591651e-6. Their difference≈1.6233e-7 is resolved well above tolerance differences. A finite lapse zero retains b≈8.1e-8 and hence C_lin≈8.1e-8; it does not cancel the clock offset mode of the declared flat benchmark. These are interpolated residual targets, not executed exact roots. The nonlinear C variation and finite-radius decay require an actual boundary-value construction before interpreting either as a global condition.

The finer .003 physical F values are .99998898543,1.00000098543,1.00000898551 for negative,zero,positive offsets. Sampled Qaa remains positive (smallest near the source≈.119); no full perturbation health or continuous positivity certificate follows from sampled values. At .003 a/A≈2.74e-5, below epsilon=.01: this reaches the Newtonian infrared regime of the changed response, so extrapolating exact deep MOND there would be incorrect. The former weak MOND flux diagnostic is no longer constant to source-mass precision; for lnN0=0 its .003 value is about.699 times m. That leading approximation assumes an intermediate regime and is not an exact conserved relativistic mass. The exact numerical Euler equations remain the integrated system.

## Evidence, remaining boundary problem and horizon scope

Authoritative numeric manifests: zero_b,plus_b,minus6_a. vacuum_a6/6 and linear_a7/7 check direct action variation. vacuum_control_a rejects deletion of the absolute log-vacuum offset in the candidate identity; linear_control_a rejects treating b alone as the conserved normalization diagnostic. The failed argparse record is retained and not counted as a physical failed continuation. All run manifests validate with their actual frozen inputs. boundary_map.json is a transparent extraction from the finer raw results, not a separately authenticated integration.

No source clock shooting root has been integrated at the interpolated target, and no boundary condition at a cosmological horizon/time-dependent domain has been imposed. A full solution must define that boundary, separate clock and mass-type modes, and show physical health on the actual background. The present material() guard rejects F<=0 even in vacuum; a future horizon-crossing ADM extension would need a declared vacuum guard change. F=0 is a static Killing horizon and does not itself invalidate an ADM clock beyond it. This phase stays at.003 and draws no horizon/global exclusion from that guard.

The continuation changes no A/H input and supplies no vacuum selector. Its new information is constructive source-to-outer-clock continuation plus a directly derived mode diagnostic showing why a finite lapse-zero shoot alone is insufficient for the selected flat vacuum matching.
