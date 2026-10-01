# FGF-022: bounded offset, derivation before code

Retain the exact binary-rational H, L and baseline from reviewed FGF-021.
Let s=stored binary64 1e-5 and u=(q_0,...,q_14,b), with p/s=Tq,
q_i=(p_i-p_(i+1))/s>=0, final physical node p(5)=0. The offset is s*b,
independent of that final node. E=H diag(T,1), c=L diag(T,1), d=H baseline/s.
The baseline offset is zero. The changed premise is |s*b|<=beta. Synthetic
beta is a design parameter, not a measurement uncertainty or confidence band.

For beta=0 use the exact equality b=0. The stored baseline already proves
feasibility before optimization; its 15 increments are strictly positive.
For beta>0 append b<=beta/s and -b<=beta/s. Minimize c.u and -c.u under the
unchanged equations E u=d and increment inequalities. Restore dp/dx by s.
Use the prior checked primal/dual pattern: for Eu=d, Au<=a, prove c=E^T y+A^T z,
z<=0, then c.u>=y.d+z.a. Exact rational feasible vertices attaining the dual
bound certify finite global optima, independently of a solver success flag.

The feasible sets are nested in beta, so the minimum is nonincreasing and
maximum nondecreasing. Convex mixing of feasible points at beta1,beta2 is
feasible at their interpolated beta, proving the minimum is convex and the
maximum concave. These structural statements do not locate all breakpoints.
We report only a small declared selected set: zero, 1e-6, half each old optimum
offset magnitude, and each full magnitude, sorted. No complete curve claim.

The unrestricted extrema have four nonzero negative inequality multipliers
each. Complementarity forces those four pressure increments to vanish at
*every* unrestricted optimum. If E plus those four active rows is invertible,
that optimum is unique. Exact elimination then proves its offset magnitude
is the necessary as well as sufficient beta threshold for recovery of that
unrestricted endpoint. This check is separate from merely observing matching
solver answers at a chosen beta. The old dual certificate remains valid when
extra inequalities are assigned zero multipliers.

Strict positive/decreasing pressure endpoints are limits: mix any optimizer
with the strictly feasible baseline, which preserves the offset bound and
exact synthetic observations. Nonzero width at beta=0 would refute the claim
that fixing the offset alone makes the finite gradient identifiable. It would
isolate remaining outer-pressure freedom without modifying the observation
operator or assigning it a physical interpretation.

Controls: baseline feasibility including beta=0; exact primal/dual conditions
for both extrema at each selected beta; nested extrema; old unique endpoint
thresholds; old unrestricted witnesses rejected just below those thresholds;
direct conversion back to H p=d; damaged dual rejected. Reuse prior vetted
Gaussian-elimination/certificate code explicitly, with all source hashes.
Selection tolerance 1e-9, active tolerance 1e-7, final exact checks tolerance 0.

No force or source discrepancy is computed. Q, RAR and registered M remain
separate, a0=9.3619e-11 and 1.1279e-10 m/s^2 remain separate, constant-vacuum
and a0 E(z) histories remain separate. An eventual MOND bridge requires the
actual density/composition and P_total'=-rho F(B;a), not these synthetic
gradient bounds alone. No metric/photon coupling or continuum theorem follows.
One process <=120 s wall, 110 s CPU, one cooperative library thread, 1 MiB
logs, no memory cap, deterministic input and no random sampling.
