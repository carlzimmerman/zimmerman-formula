# Quantum source conversion and neutral-population survival

This continuation uses the existing charged complex-scalar action. It adds a
linear fragmentation calculation and an independently checked, full-tree
neutral number-loss amplitude. It does **not** yet derive a surviving cold
population or provide valid initial data for the identified-medium collapse
solver. No cold seed has been inserted and no damping work was resumed.

## What changed

1. Positive instantaneous curvature of the generated Phi background does not
   imply stability after inflation. Its radial quartic oscillations have a
   strong transverse parametric instability. Under the stated radiation and
   momentum-matching assumptions this occurs much earlier than X oscillation.
2. Neutral cold daughters have a nonzero 4-to-2 loss channel even including
   interference with virtual X. The balanced-channel threshold amplitude is
   an exact negative sum of squares, up to the overall amplitude convention.
   An elastic scattering cancellation cannot protect that population.
3. Consequently the missing calculation is an interacting, spatial field
   evolution followed by kinetics with both number change and heating. A
   vacuum X decay spectrum plus free redshifting is not enough for this source.

## Action and normalization

We use canonical kinetic terms and

\[
 V=m^2|\Phi|^2+M^2|X|^2+g(X^*\Phi^2+X\Phi^{*2})+
 \lambda |\Phi|^4,\qquad M^2=4m^2+\Delta.
\]

The benchmark is m=0.001 GeV, M=2m sqrt(1+0.02^2),
g=2.168e-6 GeV and lambda=0.00881292. Phi has charge one and X charge two.
The inflationary H=1.3445177278709404e10 GeV and duration 60 e-folds remain
external inputs, not quantities selected by this action. The saved stochastic
ensemble starts at zero coarse field and contains 4096 final field samples;
it does not contain quantum-matched conjugate momenta or spatial covariance.

## Oscillating Phi is not a passive background

Write Phi=(f1+i f2)/sqrt(2). In the early radiation era the quartic term
dominates the Phi dynamics. For a radial orbit, rotate f2=0 and set F=a f1.
Neglecting masses and the cubic coupling at this stage,

\[
 F''+\lambda F^3=0,\quad
 F=F_{\max}\operatorname{cn}(z+z_0,1/2),\quad
 z=\sqrt\lambda F_{\max}\eta.
\]

Here the second elliptic-function argument is the parameter, not its square
root. Longitudinal and transverse fluctuations obey respectively

\[
 \delta F_\parallel''+[\kappa^2+3\operatorname{cn}^2(z,1/2)]
 \delta F_\parallel=0,\qquad
 \delta F_\perp''+[\kappa^2+\operatorname{cn}^2(z,1/2)]
 \delta F_\perp=0,
\]

where primes now denote z derivatives and kappa=k/(sqrt(lambda) Fmax).
The background phase does not change the Floquet exponents. The fluctuation
frequencies squared are nonnegative; their periodic variation causes growth.

The numerical monodromy calculation gives:

| Mode | Squared momentum at sampled maximum | Amplitude growth exponent per z |
|---|---:|---:|
| Transverse | 0.2275 | 0.1469914383 |
| Longitudinal | 1.615 | 0.0359791000 |

The transverse unstable band is 0<kappa^2<1/2. The longitudinal band is
3/2<kappa^2<sqrt(3). The scan verifies interiors and exteriors away from band
edges; it is not a numerical proof covering every real momentum.
These are familiar quartic Lamé instabilities, not a newly discovered physical
effect. See [Greene, Kofman, Linde and Starobinsky](https://arxiv.org/abs/hep-ph/9705347).
Our calculation applies this test to the existing generated Phi source.

For a timing diagnostic, match to radiation at a=1 with Hrad=Hinf, so
a=1+Hinf eta. Bracket the unspecified physical initial velocity by zero and
the slow-roll value -lambda f^3/(3Hinf). The exact conserved conformal energy
then fixes

\[
 (F_{\max}/H)^4=(f/H)^4+
 {2\over\lambda}\left(f/H+\dot f/H^2\right)^2.
\]

Twenty asymptotic growth e-folds take z=136.0623. In the median saved patch
this corresponds to a about 335 and H about 1.2e5 GeV for either match.
The 10th--90th percentile H range is about 4.8e4--2.0e5 GeV. Even the
smallest H/M in the sampled ensemble is 3.77e5. At that endpoint, the maximum
cubic/quartic curvature scale ratio is 6.80e-6 and the maximum estimated
X forcing g|Phi|^2/(H^2|X|) is 1.74e-8.

These compare *amplitude scales*, not a pointwise lower bound on quartic
curvature: the radial background crosses zero. Small neglected cubic terms
can matter briefly near those crossings. A rotating orbit with appreciable
charge also changes the fluctuation equations. The stochastic samples do not
determine that charge. Twenty growth e-folds is not an observed fragmentation
time: it does not include the matched seed covariance, nonlinear backreaction
or saturation. It establishes an early instability in the stated radial
limit, not a measured final particle distribution.

**Evidence:** `phi_fragmentation_run` preserves a **failed** overall assertion:
the preregistered condition H/M>1e6 for *every* patch was too strong; the actual
minimum was 3.77e5. We have not weakened that test or relabeled the run as a
pass. The monodromy determinant, tolerance refinement, zero-coupling control,
and both band tests all passed. Its manifest validates as a failed run.

## Full-action neutral 4-to-2 loss

For initially resting daughters, the allowed channels include

\[
 3\Phi_++\Phi_-\longrightarrow2\Phi_+,
 \qquad 2\Phi_++2\Phi_-\longrightarrow\Phi_++\Phi_-,
\]

and the charge conjugate of the first. The final particles have energy 2m
each and speed sqrt(3)/2. These reactions heat the survivors and remove two
particles per event. Total charge is conserved; total particle number is not.

The computation uses the complex-field vertices 2g and 4lambda and enumerates
all tree topologies, including quartic/quartic, quartic/cubic/cubic and four
cubic vertices. It does not replace X by a neutral real mediator. An
independent closed form follows by cutting the internal Phi line and summing
the nine unordered partitions of three positive and three negative external
legs. Define

\[
 K_t=4(\lambda-g^2/\Delta),\quad
 K_c=4\left(\lambda-{g^2\over M^2+2m^2}\right),\quad
 K_h=4\left(\lambda+{g^2\over16m^2-M^2}\right).
\]

With an irrelevant overall sign convention for the amplitudes,

\[
 \mathcal A_{31}={K_t\over m^2}
 \left({3K_h\over8}-{6K_c\over4}\right),
\]

\[
 \boxed{\mathcal A_{22}=
 -{(K_t-K_c)^2+3K_c^2\over4m^2}.}
\]

This gives A31=-931.88646663 GeV^-2 and A22=-966.34558021 GeV^-2.
For lambda=g^2/Delta+lambda_rep with lambda_rep>0, both Kt and Kc are
positive, so A22 cannot vanish. This is a tree-level vacuum threshold
statement; it is not a nonperturbative no-go theorem for cold matter.

For an incoherent nonrelativistic balanced population n+=n-=n/2, with
negligible inverse reactions and final-state occupation, the forward loss is

\[
 \dot n+3Hn=-C n^4,\qquad
 C=1.0181045670\times10^{14}\ {\rm GeV}^{-8}.
\]

Symmetry factors are 3!2! for the 31 channel and 2!2! for the 22 channel;
the integrated final two-body phase space is sqrt(3)/(16 pi). The contact-only
control gives C=45 sqrt(3) lambda^4/(1024 pi m^8), reproduced numerically.
The X diagrams reduce the total C to about 0.697 of the contact-only value;
they do not cancel it.

As a **counterfactual survival diagnostic**, insert the standard target
Y=n/s=4.37e-7 into Cn^3/H. For constant g*=g*s=10.75 its value reaches one
at visible T=6.519 MeV. Holding 106.75 instead gives 2.872 MeV; this second
choice is a sensitivity illustration, not the appropriate thermal history
at that temperature. Neither number is a predicted production temperature.

For constant g*, the forward-only equation integrates exactly to

\[
 {Y_\infty\over Y_i}=\left[1+{3\over7}{C n_i^3\over H_i}\right]^{-1/3}.
\]

This shows why injecting an arbitrary target-sized cold population early and
then ignoring number loss is not justified. It does not solve the actual
source problem: the daughters can be coherent or highly occupied, heating
changes their spectrum, inverse reactions can matter, and momenta comparable
to u*=0.02 probe near-on-shell X exchange. That regime requires a kinetic
treatment with resonant real intermediate states handled consistently, not
substitution into this zero-velocity coefficient. Medium corrections and
other channels also remain to be tested.

**Evidence:** `neutral_four_to_two_v2_run` completed, with all five checks
passing. Six choices of amputated external root agree; the two contact-only
amplitudes and the analytic contact rate agree. `audit_neutral_amplitude_run`
independently verifies the closed forms using exact rational arithmetic and
matches the recursive result. Both manifests validate. The earlier
`neutral_four_to_two_run` is retained as a failed JSON-serialization attempt,
not scientific evidence. These are self-checks, not external replication.

## What can be passed to collapse

There is still no defensible high-H source distribution to pass through the
collapse calculation. The low-H free spectrum remains about 1e-29 of the
standard mass target. The high-H ensemble supplies field amplitudes; the
calculations above show why its later population cannot be inferred by simply
decaying each X into two freely redshifting particles. Its previously recorded
isocurvature problem also remains unresolved.

There is a separate action-level mismatch. The existing scalar carrier gives
ordinary scalar stress-energy. In a valid particle limit its sources are

\[
 \rho_X+\rho_\Phi=\sum_s\int {d^3p\over(2\pi)^3}E_s f_s,
 \qquad \Pi_{ij}=\sum_s\int {d^3p\over(2\pi)^3}{p_i p_j\over E_s}f_s,
\]

plus coherent and interaction contributions when those are appreciable.
It does not by itself derive the collapse solver's identified polarization,
critical gravity cancellation or gradient-pressure coefficient. The
authoritative `MASTER_COLD_ENERGY_EQUATIONS.md` explicitly leaves the bridge
action unspecified. Equating the scalar particle number to that solver's
unit cold mass would add the missing seed and a missing coupling by hand.

Therefore the converged conditional collapse result is unchanged. No new
bound-core survival claim has been made from these quantum sources. The next
formation calculation needs matched spatial quantum data, nonlinear Phi
fragmentation with the X reservoir, and an energy-conserving transition to
number-changing kinetics. A conventional gravitational scalar-collapse
calculation could then use the resulting stress tensor; using the existing
identified-medium solver additionally requires the missing bridge derivation.
