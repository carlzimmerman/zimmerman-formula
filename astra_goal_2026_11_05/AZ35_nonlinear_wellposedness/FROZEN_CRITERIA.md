# AZ35 — nonlinear well-posedness, lane 5(a)

Freeze before graded computations. Base b754fe2bc2; sources X3, H4, C8 and
AZ34 inspected, not blind. Kappa = 1/2 FITTED; not theory closed. Adopt nothing.
Canonical a0=9.3603e-11 and alt1.1312e-10 m/s^2 remain separate. This is an
analytic dimensionless health test, not an astronomical fit.

## Target and verdict contract

The actual target is local existence, uniqueness and continuous dependence
for the nonlinear, constrained v3s evolution, including interfaces D.P=0.
A proof must specify admissible constraint data, function spaces, gauge,
positive lapse/timelike khronon, cap margin, interface transmission, and an
existence time controlled by initial norms. A counterexample to that full
target must obey the full equations and constraints in the claimed spaces.
Neither a frozen symbol nor an isolated caustic in a principal truncation is
such a counterexample. If no full proof/counterexample is obtained: NO VERDICT.

Three routes are examined: (1) the soft-branch evolution operator, rather
than eigenvalues alone; (2) nonlinear characteristic evolution in the exact
pressureless principal truncation; (3) the missing static/interface bridge,
using AZ34's exact energy witness without rerunning its old quadrature.

## Route 1: regularity and the frozen PN evolution

Derive from X3's continuity/Bernoulli/Poisson system at mu_K=0:
rho_t=-i k rho0 v, v_t=-i [K(M-1)/k + gamma Theta k] rho.
Use K=1, M=2, t=1, rho0=-1/2, gamma=1, Theta=0 (soft branch).
The general principal matrix in (rho,v) has entries (v0,rho0;c²/rho0,v0).
At c²=0 and rho0 nonzero, test its eigenvector dimension and Jordan block.
Do not identify absence of exponential UV growth with a uniform propagator.

Derive the exact 2x2 exponential from B²=-omega² I. Test k=8,16,32,64,128,256.
Compare its spectral norm with direct scipy expm and an independent50-digit
matrix exponential to relative1e-10. Numerically evolve the two basis vectors
with RK4 at4096/8192 steps, t=1; relative Frobenius error to exact and pair
change <=1e-4 (fourth-order phase error bound at the largest declared mode).
The numerical result is a finite assertion; the exact large-k formula must
establish or refute frequency-uniform control in the stated norm.

The proposed diagnostic witness is norm growth proportional to k: the last
doubling ratio in[1.95,2.05], and norm/k within1e-3 of the derived large-k
coefficient at k256. These are asymptotic-numerics checks, not observational
tolerances. Independently transform by D=diag(1/k,1), i.e. use polarization
rho/(ik) and velocity, and test the main propagator's k-independence to1e-10.
If it holds, explicitly preserve this possible regularity repair: failure
in equal-order density/velocity norms is not failure in all physical norms.

Known answer: M=1, Theta=0 gives the exact pressureless shear I+tB.
Zero time gives I. Verify the characteristic polynomial symbolically.

MUTATE is a positive stiff-branch control, rho0=+1/2, Theta=1, same gamma
and M. It is a physically distinct admissible frozen branch, not a solution
of the original negative-density state. Its propagator has the energy-norm
bound sqrt(2+2/k²)<1.5 for k>=8. It must defeat the proposed linear-in-k
diagnostic. The shared zero-time/shear known answers should still pass.
Both output trees retain every check; controls need not fail invariants.

## Route 2: nonlinear principal truncation

Derive pressureless transport characteristics X(a,t)=a+t v0(a),
v(X,t)=v0(a), rho(X,t)=rho0(a)/(1+t v0'(a)). Use v0=-sin(a), rho0=-1/2
on a2pi periodic domain. Verify both PDE residuals by chain rule exactly,
the Jacobian's first zero t=1 at a=0, and smooth invertibility for0<=t<1.
This supplies a precise finite-time breakdown in a truncation, not failure
of local well-posedness or a full-v3s solution. MUTATE uses uniform v0=1:
no compression/caustic, defeating the caustic witness. No numerical PDE
claim is graded here; the expressions and checks are exact.

## Route 3 and scope

Audit how the leaf/interface argument would complete the nonlinear proof.
AZ34 already disproves energy coercivity in H(div); do not confuse this with
nonexistence. State the remaining relaxed-domain, trace and moving-interface
obligations. In particular a nonlinear evolution cannot be declared proved
merely by c²>=0 on either open branch. No full-v3s counterexample may be
claimed from the characteristic truncation or the density-variable norm.

Units: choose L=24pc and T=sqrt(L/a0) separately for each footing; all test
times and modes above are dimensionless illustrative choices. Give their
SI time scales, but do not interpret t=1 as a galaxy's actual lifetime.
Results are invariant under this invertible change of units, not pooled.

Execution: single thread, <1GB, minutes, no downloads. Separate main/mutate
JSON, script/input hashes, exact derivation, known answers and convergence
records. If an analytic route remains open, preserve its precise next lemma.
