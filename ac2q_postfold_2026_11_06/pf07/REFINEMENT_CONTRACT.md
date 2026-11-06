# PF07 late-time refinement with bounded restarts

The t=.5 space/time/padding and raw-constraint checks pass. Longer runs lose
spectral resolution at times that increase with n; that is not a singularity
proof. Refine to n255, dt=.00125, t<=2 in restartable chunks <=.5 scalar time,
each <=120 seconds. Preserve every result as a hashed input to its continuation.
A chunk ending at its target is only a checkpoint, not a postfold solution.

Use odd evaluation grid m=2n+1 (padding sufficient for polynomial cubic products,
not exact for nonpolynomial terms). At n127 compare m=2n+1 and m=3n at t=1
before interpreting the late regime; compare common-time physical fields.
Continue only while X,q,cap/branch, Newton and raw momentum checks pass.
Monitor upper-third spectra for q,N,beta,r,p_beta, and stop if any exceeds 1e-3.
Record both raw lifted and projected momentum. Require normalized raw<=1e-7.
The timestep, discretization and data remain the same on restart; no filter or
artificial stress is inserted. If stronger monitoring stops earlier than legacy
q-only runs, the earlier valid interval supersedes their broad interpretation.
