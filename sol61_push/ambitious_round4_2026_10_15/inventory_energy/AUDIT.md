# Independent binding-energy and finite-start budget audit

15 October 2026. Primary verdict: **proved as written at the declared
zero-stiffness, fixed-point-baryon, critical-charge Newtonian scope**. The
closed binding-energy identity, finite uniform-start series and remainder,
strict excess energy, and conditional conserved-energy obstruction all
survive independent reconstruction. This does not promote the gamma-zero
profile to a finite-gamma or dynamical-baryon equilibrium.

Audited revisions:

- PROOF.md: `27e8c237f7099c25cd6cb908ca829fb1b5016caf3bda54ba7e972e266e34c16b`.
- inputs/DYNAMICAL_LIFT.md: `5e34946670364a2563c7c7d9a300e6c281975a1fa3ab0f69f90af10881d51280`.
- check_energy_v2.py: `8611e6562addc8ac9a715d45cbaa5407c48493cafe12667ed872cffbb39a4136`.
- run_v2/results.json: `a4aec20a026daf57dd49a3ff043076c1efe7fe83df73455d18cd5ac456fcb282`.

Claim card: every stock s>0 in the specified gamma-zero mechanical
functional, including the fixed baryon interaction and excluding its fixed
infinite self-energy; every admissible initially resting uniform start with
L>0, a=s/L^2<1; energy is in E0=Mb a0 rM. The full angular constrained
minimum is a pinned theorem of DYNAMICAL_LIFT, while the new calculation
evaluates its spherical representative. The finite physical-unit examples
assign their constants and initial radii; they do not fit or derive them.

## Independent derivation

With F'(x)=x^2/(1-x), differentiation of the exterior integrand gives

    partial_s[y^2F(s/y^2)-s/y^2]
       =s^2/[y^2(y^2-s)]-1/y^2
       =-(s+1)/y^2+s/(y^2-s).

The moving-edge terms cancel because the two enclosed-mass branches agree
at Y=sqrt[s(s+1)]. On compact positive s intervals the edge stays away from
the exterior electric pole, and the tail derivative is integrable. The
interior profile does not depend on s. Integration gives

    V_*'(s)=-(s+1)/Y+sqrt(s) atanh(sqrt(s)/Y)
            =-sqrt[(s+1)/s]+sqrt(s) asinh(1/sqrt(s)).

Differentiating the claimed closed formula reproduces this exactly. The
integration constant is zero: as s tends to zero, the interior baryon
contribution is O(sqrt(s)), its interior electric term is
O(s^(3/2)|log s|), and the exterior electric term is O(s^(3/2)). For the
latter use y=sqrt(s)z; the limiting logarithmic singularity at z=1 is
integrable. The exterior baryon contribution is s/Y=O(sqrt(s)). All terms
therefore tend to zero. This verifies the endpoint without extrapolating
from the finite examples.

For a uniform sphere, x=a y/L inside and x=a(L/y)^2 outside. Expanding
F(x)=sum_(n>=3) x^n/n gives the two integrated electric coefficients
L^3 a^n/[n(n+3)] and L^3 a^n/[n(2n-3)]. Positivity justifies monotone
termwise integration at every admissible a<1. For n>=3 each coefficient
bracket is at most 2/n^2, so the remainder after n=N is at most
2L^3a^(N+1)/[(N+1)^2(1-a)]. The baryon term is exactly -3s/(2L).
No factor from the Maxwell/gravity cancellation is counted twice.

The pinned minimum is unique among the stated arbitrary-angle admissible
fields. Its central enclosed mass scales as y^2; the uniform start scales
as y^3, so they cannot agree almost everywhere for any s>0. Strict
minimality therefore gives a strictly positive excess energy for every
admissible uniform start, without needing a finite numerical scan.

For an existing sufficiently regular closed solution, the inherited
Hamiltonian conserves K+E0 V with K>=0. Starting at rest above the minimum
cannot converge strongly to the exact resting minimum in the conserved
energy topology unless the excess is present in another counted channel or
leaves the modeled subsystem. This is an energy obstruction, not a proof
of a cooling law or a radiation equation. Weak/coarse convergence is
correctly left unrestricted. The fraction Eexcess/(Mc c^2) reduces to
(a0 rM/c^2)(Delta/s), with the stated energy units.

## Computation and limits

I inspected the actual v2 code and the authoritative scientific output,
including its separate direct-integral substitutions and positive-series
remainder. The version-2 manifest validates with repository-root hash
checking. I did not rerun the identical finite suite. Its nine symbolic
checks, three high-precision direct-integral comparisons and nine starts
support their stated finite assertions. The unbounded identity and
positivity statement rest on the analytic argument above. The decimal
entries named lower bounds are rounded high-precision evaluations of an
analytically lower truncation; no interval enclosure of every printed last
digit is claimed by this audit.

The first failed run is an unresolved CAS positive-root simplification,
not a counterexample to the root or energy formula. Its v2 squared-root
identity plus positive branch check is a valid exact replacement.

The nonradial-minimum theorem is an inherited input at exactly gamma=0;
the new binding formula cannot be applied to the nonzero canonical stiffness
or the newly constructed Einstein body without re-solving their energy
problem. The singular fixed point baryon and the cold central cusp remain
part of this theorem's domain. Assigned catchment factors, retention
calibration, physical receivers and formation rates are not established.

Coverage: this audit covers the mathematical energy formula and finite-start
budget. The ancillary ownership/retention source-unit paragraph was not
independently audited as an empirical census or transport model here.
No mathematical gap remains in the audited energy statements.
