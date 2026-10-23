# Derivative weighting keeps kinetic absorption in play

The small mass-weighted resonance-power fraction in ORBIT_COUPLING_RESULT.md must not be interpreted as negligible kinetic absorption. Correct distribution-derivative weighting gives a nonzero third-harmonic absorptive contribution for the prescribed dilation potential. This is a finite-broadening forced-response calculation, not a self-consistent mode, physical damping rate, or demonstration of halo formation.

## Linear-response derivation

Use the finite-A equilibrium f0=F[Q]+, Q=Ecut-E-L²/2 with anisotropy radius1. At fixed angular momentum, partial_E f0=-F inside the occupied region. No delta function appears from differentiating Q Theta(Q), since Q delta(Q)=0.

In radial action-angle variables, partial_J f0=-F Omega_r. For a prescribed perturbation phi(r) exp(-izt), the linearized kinetic equation gives

    delta f_n = n partial_J f0 phi_n / (n Omega_r-z).

Pair n and -n, integrate against phi, and evaluate with samples drawn from f0/M. The scalar susceptibility is

    Pi(z) = -M mean_f[sum_(n>=1)
               2(n Omega_r)² |phi_n|² /
               {Q[(n Omega_r)²-z²]}].

The extra1/Q factor is essential. The earlier mass-weighted coupling statistic omitted it intentionally and therefore was not a susceptibility. The radial n=0 harmonic does not enter this collisionless time-dependent response. With the exp(-izt) convention and z=omega+i epsilon, epsilon>0, this expression has -Im Pi>=0 at positive omega. The finite epsilon represents analytical regularization, not a physical friction constant.

The trial phi is the finite-A dilation potential from the previous checkpoint, normalized to maximum absolute value1. It is not a kinetic eigenmode. The reference omega=.827760 is from the exactly cold-fluid fundamental.

## Independent sum rule

At large |z|,

    Pi(z) ~ C/z²,
    C = integral rho |grad phi|² dV.

To see this, the harmonic sum equals the orbit average of (d phi/dt)² by Parseval. The remaining phase-space integral is integral F vr² (phi')² dGamma. Velocity integration by parts, using -partial_vr f0=F vr and zero distribution at the cutoff, gives integral F vr² dv=integral f0 dv=rho. This identity also holds for this anisotropic f0 because L is independent of vr at fixed r.

In the normalized radial convention used here, C=integral r²rho(phi')²dr. This provides a spatial check independent of orbit Fourier sampling and catches normalization/sign/factor errors. The computed spatial value is .43760395. The sampled moment is .40753661 at1024 orbits (6.87% deficit), and .42718813 at4096 orbits (2.38% deficit). This improves but is not converged to high precision. Rare low-Q samples and finite-harmonic truncation remain possible error sources; improvement alone does not isolate them.

## Forced response

Use A10000, harmonics1–16, the same continuum equilibrium, and1024/4096 deterministic phase samples. Fourier quadrature1024/2048 and orbit-period quadrature64/128 agree within their numerical gates.

| epsilon | -Im Pi,1024 samples | -Im Pi,4096 samples | n=3 contribution,4096 |
|---|---:|---:|---:|
| .1 | .23828 | .25512 | .01087 |
| .03 | .08950 | .09570 | .01367 |
| .01 | .04260 | .04440 | .01538 |
| .003 | .02681 | .02634 | .01633 |
| .001 | .01687 | .01802 | .01364 |

These values refer to a prescribed unit-normalized trial potential. They cannot be converted into a mode lifetime without its self-consistent response and normalization. For example, at epsilon=.01, the4096-orbit contributions are .01565 from n=1, .01129 from n=2, .01538 from n=3 and .00184 from n=4. The low-order contributions shrink strongly with epsilon; broadening lets nonresonant orbits contribute. The third harmonic remains visible but the narrowest-width values are not stable enough to infer a zero-width limit. Sending epsilon to zero at fixed finite sampling would produce isolated poles rather than establish continuum damping.

The real part at epsilon=.01 changes from .74330 to .78715 between sample counts. This residual sensitivity is material for locating any self-consistent mode. The measured susceptibility should not yet be used as a precision dielectric function.

## Mechanism consequence

The last checkpoint's weak high-harmonic coupling remains a valid geometric diagnostic, but does not eliminate a kinetic absorption channel. The derivative-weighted calculation now supplies the appropriate response object and an independent sum rule. The next obligation is a self-consistent response calculation with basis and sampling convergence, or a justified restricted projection explicitly labeled as such. A complex response to an externally prescribed potential is not itself proof that the medium's free oscillation damps at any particular rate.

Neither initial occupation selection nor cold halo formation has been explained. No new sector, friction term, or complete parent action has been introduced. Novelty remains unestablished.

## Evidence

The two original orbit calculations are direct runs saved as kinetic_weight_1024.json and kinetic_weight_4096.json, including the per-orbit Q, frequency and16 coefficients. kinetic_weight_run audits those artifacts and independently reevaluates the width scan. Six audit checks pass and its manifest validates. The direct calculations each pass seven numerical gates, including a deliberately loose10% sampling sum-rule gate whose actual errors are reported above. Passing that gate does not certify convergence. Inputs and code are hashed; interpretation is self-reviewed.
