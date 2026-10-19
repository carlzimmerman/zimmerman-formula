# Strictly radial canonical confinement remains open

19 October 2026. Checkpoint ZAR-2026-10-19-08, continuing [checkpoint 07](../initial_reserve_2026_10_19/README.md). This checkpoint uses strictly radial canonical data with the same original initial full phase-space supports, exact masses/Casimirs and a prescribed negative initial energy gap. It does not use angular-current data or an added outer population.

**All-time confinement for this class is not proved.** The work now supplies a uniform finite protection theorem, exact canonical rigidity results, and a bounded resonant first response. The remaining implication is full self-consistent and nonlinear control of signed work at the moving support boundary.

For small canonical energy defect Delta H, the proved stability estimate becomes

\[
\sup_{t\ge0}X(f(t)-F)\le
\epsilon_H=C_X\left(\sqrt{\Delta H/\gamma}+\Delta H/\gamma\right).
\]

It gives the protected enclosing radius and time

\[
R_H=4G(M_b+T+U)/\beta_0,
\qquad T_H=\beta_0/(4\Gamma\epsilon_H),
\]

where beta_0 is the equilibrium binding cap and gamma,C_X,Gamma are the named fixed analytic constants. Every sufficiently small datum satisfying the initial conditions stays inside this same R_H until T_H. The guaranteed time grows on the scale (Delta H)^(-1/2). This is not an escape prediction after T_H, and choosing smaller neighborhoods for longer intervals does not prove an infinite-time neighborhood. [FINITE_TIME_CONFINEMENT.md](FINITE_TIME_CONFINEMENT.md) gives the proof and constants.

Canonicality also gives a decisive rigidity distinction. If both original density fields stayed exactly fixed for a nontrivial time interval, the global inverse entropy and virial identity would force f=F. If the original complete phase-space supports were required to remain exactly unchanged for all time, boundary tangency would force those same fields and again f=F. In contrast, initial support equality is compatible with nonstationarity: an explicit arbitrarily small canonical perturbation, equal to F on a boundary collar and retaining a fixed initial negative gap, immediately moves the old orbital boundary. This does not prove unbounded expansion or escape. [CANONICAL_RIGIDITY_AND_SUPPORT.md](CANONICAL_RIGIDITY_AND_SUPPORT.md) separates these statements.

The resonant calculation now goes beyond a failed denominator bound. A Dini estimate handles the actual resonant integral. For smooth finite-harmonic canonical generators on explicit compact eccentric frequency bands, the actual gravitational kernels make the full receiving-angle first-response work uniformly bounded for all time. An exact nonlinear advected-energy label also removes division by F_E at the flat edge. [RESONANT_WORK_PROGRESS.md](RESONANT_WORK_PROGRESS.md) proves these advances and identifies the remaining feedback and boundary estimates. The first response is not the full linear solution; feedback remains order one as the initial amplitude tends to zero.

Nonlinear bulk stability, cumulative-mass/force-law control and integrated radial pressure remain uniform for all time under the same smallness. Positive averaged radial dispersion at every fixed resolution follows as before. Pointwise annulus warmth persists on each finite time interval for genuine smooth canonical data; no all-time pointwise floor is added. A general nonstationary solution is not asserted to preserve the exact density law.

[AUDIT_AND_HANDOFF.md](AUDIT_AND_HANDOFF.md) records the exact target, the initial-support versus all-time-support distinction, and the next mathematical implication. [CHECKPOINT.json](CHECKPOINT.json) pins the inputs and reviewed revisions. Only this new directory was written. No scientific scripts, simulations, numerical integrations or process inspection/control were used; Claude's calculations and all prior artifacts were left untouched.
