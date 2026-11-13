# Independent review of the compression-entry experiment

**Verdict: computationally verified only in the stated finite leading-NR range.**
The supplied trajectories start with positive charge and nonpositive D, satisfy
the actual nonlinear polarization constraint, and reach D>0 while the
fixed-charge P Hessian remains positive. This is substantive evidence against
automatic invariance of that proposed protected region in the reduced model.
It is not a full-GR trajectory, a cosmological initial condition, a continuum
convergence theorem, or a resolved growing high-frequency wavepacket.

Reviewed driver SHA-256:
`dea99af6c1f837d14502a00bb3807fd75e1b278ec9139cf50095d10bdb560bbe`.
Driver and all three endpoint/result pairs are pinned in compression_sources;
their hashes still matched the live files at the end of this audit.

## Construction and equations

The experiment changes the literal gate to the distinct clamped repair
`S=exp[-max(Pi,0)^3]`, with K=a0=Pic=1, C=10^6 and original one-sided
`Gamma=gamma Pi_+²/2`, gamma=10^-8. The periodic Poisson equation subtracts the
mean source; it is a compatibility-background reduction, not a static
homogeneous Einstein solution.

Writing h=n-Pi and f=1/S, direct differentiation gives

    e=h² f/(4C)+W(P)+Gamma,
    e_Pi=f[-2h+3Pi_+² h²]/(4C)+gamma Pi_+,
    e_PiPi=f[2-12Pi_+²h+(6Pi_++9Pi_+^4)h²]/(4C)
                +gamma 1_(Pi>0).

These agree with the executable residual `-d_x e_Pi+W_P` and its Jacobian
`-d_x e_PiPi d_x+W_PP`. They are derivatives of the actual gated internal
energy, not an inserted pressure proxy.

The initial divergence uses disjoint compact bump functions: positive peak.86
and broad compensating negative bump, with zero mean. P is its periodic
antiderivative. The construction sets

    e_Pi = inverse_derivative(W_P)-.15/C,
    target=4C S(e_Pi-gamma Pi_+),
    h=-target/[1+sqrt(1+3Pi_+² target)],  n=Pi+h.

This is the numerically stable lower root of the exact quadratic equation
`3Pi_+²h²-2h=target`; the formula also has the correct Pi_+=0 limit. Symmetry
removes the antiderivative's zero-mode obstruction. The subsequent nonlinear
constraint solve checks the actual discrete state.

The disjoint bumps avoid a transversal initial Pi=0 stiffness kink. They do
not make the entire original W action analytic: W contains |P|³ and its force
is C¹ at P=0. Thus C-infinity should describe the bump functions, not every
constructed charge field or constitutive derivative.

## Independent checks from raw arrays

The audit imports no candidate code. It reconstructs the initial state from
the specified formula, differentiates P using direct FFT rather than the
driver's dense derivative matrix, computes the original Hamiltonian including
Gamma, and checks both endpoint constraints and principal signs.

| Quantity | Independent result |
|---|---:|
| initial charge reconstruction error, all runs | <=2.22e-14 |
| endpoint polarization residual, all runs | <=1.96e-14 |
| identity `A e_PiPi=c²-A D` error | <=4.45e-16 |
| relative Hamiltonian drift, N=256 | 2.90e-14 |
| relative Hamiltonian drift, N=512 | 2.00e-15 |
| relative Hamiltonian drift, N=512 half timestep | 2.23e-16 |
| total mean-charge drift | <=5.56e-17 |

Here A=H_QQ, c=1+H_QPi, and D=H_PiPi-gamma on the positive branch. The local
large-k charge response is `h_eff=-D/(A e_PiPi)`. All initial D are nonpositive.
At the fine final state, Pi_max=.896111142533, D_max=3.8895335e-11>0,
minimum e_PiPi=2.3813691e-7>0, and the peak principal coefficient
`n h_eff=-1.8406851e-10<0`. Minimum charge remains.08753256>0.

The finer timestep brackets the first discrete entry in
**[.001735,.001740]**. Halving the fine-grid timestep changes final charge by
at most5.59e-11 and velocity by5.09e-14. Spatial refinement is less sharp:
the maximum common-grid final-charge difference is2.035e-4. Both resolutions
agree on entry and its sampled bracket, but that difference must not be hidden
behind the excellent time-step agreement.

The negative coefficient is a **local principal diagnostic**. At the first
entry, its positive-D spatial region can be narrower than a well-resolved
unstable wavepacket. The run does not demonstrate the growth of that packet;
the characteristic calculation supplies the instability interpretation.

## Independent tangent-direction test

I also differentiated the nonlinear constraint itself, without integrating
past the entry:

    [-d_x e_PiPi d_x+W_PP] Pdot = d_x(e_Pi_n ndot),
    ndot=-d_x(nv),     Pi_dot=d_x Pdot,
    xdot=(ndot-c Pi_dot)/A,
    Ddot=2C x S'' xdot+C x² S''' Pi_dot       (Pi>0).

The tangent constraint residual is below5.73e-13. At the fine-grid peak,

    Pi_dot=21.87161366,
    Ddot=9.77447996e-6 >0.

The half-timestep value agrees, and the coarse Ddot is9.78077839e-6. Thus the
actual reduced vector field points toward increasing D at entry. This check
does not infer the direction from a mislabeled plot or prescribed Pi(t).

## Audit correction and provenance

The first reviewer energy calculation accidentally omitted Gamma from the
Hamiltonian and failed its energy check, while the other nine checks passed.
That failed audit and its manifest are preserved. The corrected reviewer
script includes Gamma and all ten checks pass. This was an audit-script error,
not an error in the candidate's evolution equations. Accepted evidence is
`compression_v2_run/results.json`; the first `compression_run` is not a passing
record. No thresholds were relaxed.

The accepted scope is entry into the local negative-response region of this
specified clamped-gate NR system under constructed smooth compression. The
clock-charge transport, elliptic constraint and moving state are actually
computed. The experiment supplies no selected kappa, halo mass normalization,
cosmic formation history, or full-relativistic instability trajectory.
