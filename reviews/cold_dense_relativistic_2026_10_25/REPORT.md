# Dense relativistic branch: full oscillator EOS and vacuum-inclusive TOV

## Outcome

The dense oscillation branch has positive averaged pressure, but this calculation
has not produced a physical compact star. With the action's positive vacuum
retained, none of the 61 tested central excitation densities reaches a
zero-pressure surface: 56 hit the static areal-coordinate metric cutoff first,
and five do not have a central pressure maximum. Refining the EOS table and ODE
tolerances preserves every terminal classification.

There is also a distinct closure problem. Near its zero-pressure surface the
homogeneous oscillator EOS has dP/dE about 1.074335. Interpreting that derivative
as a perfect-fluid sound speed would exceed c². Independent quadrature derivative
checks confirm it. This invalidates a naive causal perfect-fluid interpretation
of the whole surface branch; it does not prove acausal propagation or nonexistence
of solutions of the underlying canonical real scalar.

This work tests a relativistic, time-averaged fluid approximation to the dense
branch. It is not a full Einstein-real-scalar evolution or a proof excluding all
dense configurations. Formation, radial field stability, abundance, the cluster
profile and the galaxy law remain unresolved. No extra action constants or
population parameters were fitted.

## 1. Full-amplitude oscillations, without a quartic truncation

Continue e8b0beff16 with the same r=1, s=1/4 and eta. For an isolated vacuum
configuration use d=0; the scalar's own density is not inserted into external
baryonic d. The canonical excitation potential is

    U(q)/D=10[sec²(q/2)-6/5]².

The vacuum term W_min/D=1.6 is subtracted only from excitation energy, and retained
in gravity. The two minima are separated by a barrier .4 D. For E>.4, a homogeneous
oscillation crosses both wells, with turning amplitude

    q_max=2 acos{[6/5+sqrt(E/10)]^(-1/2)}.

Its cycle averages define

    dt=dq/sqrt[2(E-U)], K=E-U,
    P(E)=2<K>-E.

The symmetric quarter-cycle suffices. The substitution q=q_max sin(theta)
regularizes the turning-point integral. The numerical pressure crosses zero at

    E_s=0.4968367368, P(E_s)=0.

This is a genuine dense branch of the full potential, not the earlier dilute
normal-form expansion. It has finite excitation density at zero averaged pressure.
Matching it to a scalar vacuum requires an interface calculation; a fluid surface
condition alone does not provide that matching.

Quadrature comparisons at E_s, 1, 10, 1e3, 1e6, 1e10 using 256 and 512 nodes meet
the declared 1e-6 E pressure tolerance. The independently evaluated oscillator
virial relation <K>=<q U_q>/2 passes the declared relative 1e-7 tolerance. This
checks the homogeneous averages, not spatial stability of a dense clump.

## 2. The sound-speed gate fails near the proposed surface

The initial run halted before stellar integration because the interpolated EOS
had dP/dE>1. We investigated rather than silently accepting that result as a
causal fluid. Direct 512-node quadratures with relative finite-difference steps
1e-3, 1e-4 and 1e-5 at E_s give

    1.07433818, 1.07433520, 1.07433330.

Thus the failure is not merely a coarse interpolation artifact. The derivative
falls through one at approximately E=0.51680078, where P=0.02066421, still positive.
A star reaching the zero-pressure dense-branch surface would pass through this
problematic interval. Stopping instead at that positive pressure would require
a physical interface or confining stress which has not been derived.

The exact scalar has a canonical kinetic term. A questionable sound speed in a
barotropic averaging scheme is not a license to declare the original scalar
acausal. It means spatial gradients, phase dynamics, interface structure or the
averaging prescription need a field-level treatment. Positive dP/dE elsewhere
is likewise not proof against gravitational radial modes, fragmentation or
scalar radiation.

The original failed run and check_initial.py are preserved. FOLLOWUP.md explicitly
changes the task to a formal diagnostic continuation. The diagnostic output is
not relabeled a successful causal-star calculation.

## 3. Relativistic equilibrium with the same vacuum

The Einstein-frame scalar is minimally coupled to gravity in the vacuum region.
As a provisional slowly varying, time-averaged approximation, use its homogeneous
E and P as a perfect fluid. This neglects spatial-gradient anisotropy, interface
stress, fast metric oscillations and radiation; those are substantive omissions.

Define

    ell=c/sqrt(4pi G D_mass), x=r/ell,
    mu=G M_exc/(c² ell), v_vac=1.6.

The dimensionless equilibrium equations are

    mu'=x² E,
    P'=-(E+P)[mu+x³(P-2 v_vac/3)]/[x² F],
    F=1-2mu/x-2 v_vac x²/3.

Here M_exc excludes the vacuum mass; its gravitational effect is explicit.
These equations are the vacuum-inclusive TOV equations. We checked the convention
against Böhmer and Harko, arXiv:gr-qc/0504075v3, equations (13)–(14):
https://arxiv.org/pdf/gr-qc/0504075 . Their radial stability analysis is not being
imported as a stability result for our EOS.

An independent local check adds vacuum to both total density and pressure:
(E+v_vac)/3+(P-v_vac)=E/3+P-2v_vac/3. Flipping the vacuum-force sign fails this check
in the mutation run. No scalar self-density is double counted as baryonic matter.

With the existing normalization,

    ell=5088.8704 Mpc,
    c² ell/G=1.0633802e23 solar masses.

These large natural scales must be retained when interpreting dimensionless
solutions. The scalar oscillation mass does not by itself set a compact fluid
star radius once gradients are omitted in this averaging approximation.

## 4. Sequence and terminal conditions

Test 61 logarithmically spaced central excitation densities from 1.001 E_s to
1e6 D, using an EOS table extending to 1e10 D. Start from the regular center
expansion. A centrally decreasing pressure requires

    E_c/3+P_c-2v_vac/3 > 0.

Failure of this condition is classified as no central pressure maximum, not as
exclusion of every possible shell-like solution. For the remaining states,
integration stops at P=0, F=1e-5, the EOS upper cap, or x=3. The same finite test
is repeated with 800/1600 EOS points and relative ODE tolerances 2e-8/2e-10.

| Gravity used | P=0 surfaces | Metric cutoff | No central pressure maximum |
|---|---:|---:|---:|
| Physical v_vac=1.6 | 0 | 56 | 5 |
| Artificial comparison v_vac=0 | 61 | 0 | 0 |

All statuses agree on refinement. For the artificial comparison, surface radii
and masses also agree within the declared 1% tolerance. That comparison gives
radii 577.45–6172.25 Mpc and excitation masses 2.5742e19–4.1685e22 solar masses.
These are formal solutions of the diagnostic equations, not viable compact
objects in the physical model: vacuum gravity has been removed and the surface
EOS closure issue remains.

The diagnostic solver emitted overflow warnings in RHS evaluations near the
metric cutoff. All stored terminal quantities are finite, every solve reports
successful event termination, and classification agrees on refinement. These
warnings limit interpretation of the near-cutoff integration; we do not claim
a precise horizon location or a regular continuation through it. The independent
uniform-density checks have no such warnings.

F approaching zero is a failure of this static areal-coordinate integration
before a fluid surface is reached. It is not proof of dynamical black-hole
formation. A coordinate equator or another extension may require different
coordinates and a different global boundary problem. Nor does a finite scan up
to E_c=1e6 establish a no-go theorem at every central density or for anisotropic
and time-dependent scalar configurations.

## 5. Independent stellar-integrator check

To distinguish a physical diagnostic from a sign or normalization error, solve
a uniform-density control with E=10 and prescribed surface radius R=.2 in the
same dimensionless units. Let B=(E-2v_vac)/3, a=2(E+v_vac)/3,
f(x)=sqrt(1-a x²), f_s=f(R). The analytic pressure is

    P(x)=B E [f(x)-f_s]/[E f_s-B f(x)],
    mu(x)=E x³/3.

For both v_vac=0 and 1.6, numerical integration agrees with these profiles to
about 1.1e-15 in pressure and 1.4e-17 in mass over the sampled interval. These
small errors corroborate this smooth benchmark; they do not imply the same
absolute accuracy near the diagnostic metric cutoff. The finite stellar-sequence
refinement remains the relevant convergence check there.

## 6. Why formation and abundance have not followed

The field equations have not supplied a regular, causally interpretable compact
endpoint in this approximation. Consequently this calculation cannot assign a
stable-object formation rate, lifetime, or cosmological abundance. It also has
not calculated a radial eigenmode spectrum: an equilibrium and suitable boundary
conditions are prerequisites, and local dP/dE positivity is insufficient.

For any surviving real-field dense branch, one must derive how it forms from the
available reservoir, the fraction lost as outgoing radiation, and how it survives
a cluster's external baryonic source. Picking E_c selects a member of a trial
sequence, not an abundance prediction. Replacing the real scalar with a stationary
complex scalar would be a change of theory, not a completion of this test.

Even successful compact objects would require a predicted population N(<r) to
reproduce M_c(<r). Clumping does not erase the enclosed gravitational mass that
perturbs galaxies. The earlier spherical selective-CCT allowance remains an
obligation in that bookkeeping; the Palatini model needs its own force/lensing
calculation. No galaxy tolerance or environment-dependent occupation was chosen
here to force agreement.

## Evidence and remaining route

The preserved initial run is an expected scientific gate failure after inspection,
not evidence of a physical star. Its original script hash can be checked against
check_initial.py; the current script intentionally differs. run_diagnostic/ and
verification/ contain completed bounded runs. mutation/ records the expected
vacuum-sign assertion failure. Criteria, follow-up rationale, EOS data and each
terminal result are retained. Results are self-reviewed, not independently
certified.

Reproduce the diagnostic and independent checks from repository root:

    python reviews/cold_dense_relativistic_2026_10_25/check.py --output /tmp/cold-dense-diagnostic
    python reviews/cold_dense_relativistic_2026_10_25/verify.py --output /tmp/cold-dense-verification

The remaining live route is a direct real-scalar, metric and interface calculation
that resolves the limitations of the fluid closure and tests a bound endpoint's
perturbations and radiation. This checkpoint supplies no sufficient abundance
or galaxy-safe cluster profile and does not claim to have excluded that broader
route. Extending a barotropic TOV scan alone would not resolve the demonstrated
surface-closure issue.
