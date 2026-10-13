# Expansion preserves a small charge-energy surplus

2026-10-11. Continuation of the distinct action in [CHARGED_ACTION.md](CHARGED_ACTION.md).
This is an analytic classical FLRW bound, not a quantum-production simulation.

## Assumptions and exact identities

Use that action minimally coupled to spatially flat FLRW, in a periodic
comoving box. Assume a smooth solution over the interval, m>0, positive
conserved comoving charge Q, and a differentiable background satisfying
0<=H(t)<=H_0<m/3 and dot(H)<=0. No additional exchange with other sectors
is included. The background may be imposed; a Friedmann solution is not
constructed here. All integrals below include a^3 d^3x. Let E be comoving
material energy, G the integrated physical gradient energy, and Pi the
integrated pressure trace divided by three. Exclude any constant vacuum term.

The positive identity D=E-mQ>=0 still holds, with physical gradients
|nabla phi|^2/a^2. Define S=Re integral(phi* dot(phi)+chi* dot(chi)).
The exact conservation and virial identities are

\[
 \dot E=-3H\Pi,\qquad
 \Pi=\dot S+\frac23G+R,\qquad
 R=\operatorname{Re}\int w^*(z+w),
\]

where z=sqrt(Delta) chi, w=g phi^2/sqrt(Delta), as before. In differentiating
S, the derivative of a^3 cancels the field equation's 3H friction term;
there is no leftover 3HS term in the displayed virial identity.

Completing a second square gives a particularly useful lower bound:

\[
 R=\int|w+z/2|^2-\tfrac14\int|z|^2
 \ge-\tfrac14u_*^2 E,
\]

because Delta=4m^2u_*^2 and integral 4m^2|chi|^2<=E.
Also |S|<=sqrt(ED)/m<=E/m since Q>0. None of these inequalities neglects
nonzero source momentum, daughter self-interaction or coherent stress.

## Modified energy and comparison theorem

Set F=E+3HS. Then

\[
 (1-3H/m)E\le F\le(1+3H/m)E,
\]

and the rapid virial derivative cancels:

\[
 \dot F=3\dot H S-2HG-3HR
 \le\left({3|\dot H|\over m}+\frac34Hu_*^2\right)E
 \le {3|\dot H|/m+(3/4)Hu_*^2\over1-3H/m}F.
\]

Integrate this scalar differential inequality. The dot(H) part integrates
exactly to log[(1-3H/m)/(1-3H_0/m)]. For the remaining positive term use
1/(1-3H/m)<=1/(1-3H_0/m) and integral H dt=log(a/a_0). Hence

\[
 \boxed{1\le {E(t)\over mQ}\le
 {E_0\over mQ}{1+3H_0/m\over1-3H_0/m}
 \left({a(t)\over a_0}\right)^{\frac{3u_*^2}{4(1-3H_0/m)}}.}
\]

The initial factor uses a conservative bound on S_0; it need not be saturated.
If the right side is B(t), then eta(t)=1-mQ/E(t)<=1-1/B(t). In particular,
large expansion produces only a logarithmically accumulating small surplus
at this mass splitting. The proof is conditional on the specified smooth
solution and monotone background; it is not a proof of global existence.

## Benchmark and meaning of pressure averaging

Take u_*=0.001, initial eta_0=1-1/sqrt(1+u_*^2), H_0/m=1.3781994828e-11,
and a/a_0=1,000,001. The H_0/m value is an illustrative input inherited from
the earlier epoch normalization, not a fitted cosmology for this new action.
The bound gives

* E/(mQ)<=1.000010861776;
* eta<=1.08616572e-5.

Thus at least 99.9989138% of comoving material energy remains protected by
the charge floor under the assumptions. This is a total-field energy
statement, not a daughter fraction or a relic-abundance prediction.

For a time interval of length T, let B_* bound E/(mQ) throughout and
eta_*=1-1/B_*. Integrating the exact virial identity, with the bounds from
CHARGED_ACTION, gives the precisely defined pressure ratio

\[
 {\left|\int\Pi\,dt\right|\over\int E\,dt}
 \le {2B_*\sqrt{\eta_*}\over mT}
 +\frac23\eta_*+\sqrt{2\eta_*(\eta_*+u_*^2)}.
\]

This is the ratio of time-integrated comoving pressure to time-integrated
comoving energy. It is not an unweighted average of instantaneous P/rho.
At the benchmark the bulk terms sum to 2.32933478e-5; the endpoint term
must also be included for the chosen interval. No averaging interval is
silently assumed. This does not establish a sound speed or halo law.

## Finite check and self-audit

[charged_expansion.py](charged_expansion.py) integrates a homogeneous nonlinear
classical trajectory with m=1, u_*=0.1, g=0.03, H_0=0.003, initial chi=1,
phi=0.02, and positive circular initial velocities. Radiation expansion
runs to t=1000. This deliberately resolvable check uses different parameters
from the analytic cosmological benchmark. It tests the FLRW virial identity,
comoving charge, nonnegative surplus, the differential comparison inequality
at every sampled point, and the resulting energy bound.

The five reported checks pass, with charge drift 5.56e-9 and normalized
virial residual below 3.14e-16. No sampled differential-bound violation occurs.
[Results](charged_expansion_run/results.json) and
[manifest](charged_expansion_run/manifest.json) preserve the run. These finite
checks cannot establish the general spatial theorem; its proof is above.

Self-audit verdict: proved under the stated classical FLRW restrictions.
Load-bearing steps were independently expanded within this self-review:
measure/friction cancellation, sign of pressure work, square completion in
R, positivity of F, and cancellation of the endpoint H factor after
integrating the comparison inequality. No independent reviewer was used.

The production question remains distinct. Exactly vanishing classical
daughters still stay zero. Quantum vacuum seeding, nonlinear depletion with
the required quartic interaction, and a justified classical/quantum matching
remain uncomputed. Initial energy and charge are supplied, and the repo's
acceleration/vacuum relation is not derived. This result closes an expanding
classical survival obligation for the alternative action, not the user goal.
