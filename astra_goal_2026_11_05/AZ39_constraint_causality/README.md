# NO VERDICT — full v3s constraint causality

The conditional GR branch has a causal, nonzero tidal response for the
conserved planar probe tested here. This does not establish the response
of the charged, screened branch. C8's inference from a leaf-elliptic
equation to a physical instantaneous signal omits that calculation.
Kappa = 1/2 FITTED; not theory closed.

Criteria committed first in b0061761eb. Main29/29 checks pass; deliberately
instantaneous MUTATE25/29. Both footings are recorded separately and are
exactly identical on this branch, which does not depend on a0 or Lstar.

## Derivation and scope

For P=0,Q=1, with a unit geodesic clock, the extra terms and their first
variations vanish. W(0)=W'(0)=0, the switched stiffness F and F' vanish
from both sides at s=0, and the clock potential and derivative vanish
at Q=1. The P.A variation vanishes because both P and acceleration A
are zero. A normalized gradient with constant norm is geodesic. Thus a
GR metric admits this branch locally while a regular geodesic foliation
exists. This is not a global foliation, uniqueness, or branch-selection
theorem; AZ37 gives an explicit warning about congruence focusing.

Use eta=(-,+,+,+), Box=-dt²+Laplacian and 8*pi*G=1. For
T_ab=(d_a d_b-eta_ab Box)f, conservation is an identity. A harmonic
retarded response is h_ab=-2*d_a*d_b*u-eta_ab*f, Box u=f, with zero
incoming u. Its trace reverse has divergence -d_b(Box u-f).
The Hessian term is pure gauge: all256 linear Riemann entries vanish.
The remaining Einstein tensor is exactly T_ab, and for example
R0101=(f_tt-f_xx)/2. This special probe is nonradiating outside its
support; it is not evidence that generic radiation vanishes.

To test an actual nonzero delayed signal, take the separately conserved
planar stress T12=T21=b(t)c(z), all other components zero, with the
compact polynomials in FROZEN_CRITERIA. The TT Einstein equation is
(dt²-dz²)h12=2*T12. Its zero-data solution is

    h12(t,z) = integral_0^t ds integral_[z-t+s,z+t-s] dq b(s)c(q).

At z=3, the tidal observable is

    R0102 = 1/2 integral_[max(0,t-4),min(1,t-2)] b(s)c'(3-t+s) ds,

with empty intervals set to zero. Independently differentiating the
piecewise exact displacement twice gives the same expression. The source
occupies -1<=z<=1 and 0<=t<=1; no causal response at z=3 can arrive before
t=2. The three frozen early probes give exactly zero curvature. A later
probe is nonzero, with sampled peak magnitude0.296947496947497.

The probes are conserved signed linear stresses, not a model of a
positive-energy isolated material source. The TT source extends across
the transverse plane; its support test concerns the z light cone. The
general retarded GR operator supplies the causal-support statement on
this branch; this calculation does not transfer it to other branches.

## Numerical evidence and mutation

Every numerical integral is checked against an exact rational polynomial
integral and a split16/32 Gauss-Legendre pair. No PDE simulation is claimed.
Main max pair difference3.47502e-17; exact-answer discrepancy5.55112e-17,
both below the frozen1e-10. The mutant's respective values are0 and
3.55272e-15. Both runs take about2seconds in the recorded environment.

MUTATE changes the TT operator to h12,zz=-2*T12, using
h12=-integral|z-q|b(t)c(q)dq. Its curvature at the early probes has peak
39.00952380952381, failing the1e-12 outside-cone line. It also has zero
response at the sampled delayed times, failing the nonzero-delayed-signal
check on both footings. Those are the four failed checks. This proves
the test detects the deliberately instantaneous response; it does not
identify that response with v3s.

## Retained failures and reproducibility

The first attempt reached JSON output with a SymPy BooleanTrue instead
of a native bool. Its script and path-sanitized traceback are preserved
in serialization_failure/. The next run's Einstein and gauge checks
passed, but two check formulas had a factor/sign error: the harmonic
residual used2*d(Box u-f) instead of d(Box u-f), and the expected tidal
component had its sign reversed. Those scripts, results and logs remain
in check_formula_failure/. Only the check formulas were corrected;
the response, criteria and tolerances were unchanged. Both production
runs were then repeated with their current script hashes.

From the repository root:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ39_constraint_causality/run.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ39_constraint_causality/run.py --mutate

Expected exits0 and1. Results are in main/ and mutate/ respectively.
SymPy derives the exact identities; NumPy supplies the independent
quadrature. The script records input hashes, runtime and native RSS.

## Exact missing link

For an on-shell nonzero-charge background, derive the full lapse, shift,
polarization and clock response to a conserved source with specified
initial and boundary data. Compute gauge-invariant curvature from the
retarded constrained system, retaining the switched interface. Test its
support, not just its static spatial inverse or a frozen dispersion
factor. Neither C8's asserted permanent instantaneous signal nor full
light-cone causality is established by the calculations audited here.
No existing board tile or adopted action was changed in this lane.
