# Independent absorption-selection audit — 2026-09-22 11:34 UTC follow-up

Candidate074426e26bd749f39880562a75140d89 now calls both pinned solvers correctly,
uses the prescribed killed-only half-alpha negative, and computes distinct
influence standard errors. However it applies abs(D), changes killed variance
to ddof1, omits some finite/geometry predicates, and requires H signs to pass.
Those remain contract defects. Original code is preserved as candidate.py.

verify.py independently computes raw-D statistics using the two unchanged,
previously audited transport implementations. It replays main32k and positive64k
seeds and adds a declared fresh32k sample. Variance uses the prescribed ddof0;
H signs are results only. All27 audit checks pass, manifest validates.
Raw conservative minD=-4.440892098500626e-16 in all three batches: numerical
roundoff, not physical negative delay. Raw D is retained, not abs/clipped.

At alpha .5,2,4 main weighted H=.15424962,.04763502,.02026541 and killed
H=.15488238,.04889898,.01972082. Fresh weighted H=.15715339,.04772516,.02018759;
fresh killed H=.15753530,.04183576,.01424872. Main/positive/fresh mean,variance,
escape agreements all pass5SE; maximum absolute discrepancy2.1393SE.
Main half-alpha negative escape z=-74.4681,-75.0077,-49.5862. It fails the
same cross-estimator certificate. Alpha0 calibration is a valid independent
mean identity (.5 at M1), not circular. Altering both absorption rates together
would destroy the intended mismatch control. Referee048ba0dc is wrong on
those points; concern about abs masking failures is valid in principle but
not material to these actual outputs. No selected cap violation detected.

This closes a FINITE test at uniform M1, alpha .5,2,4. It does NOT prove the
absorption extension for other parameters/profiles, observational applicability
or novelty. Reused conservative paths correlate alpha cases. Influence SEs
are asymptotic estimates. No source or physical model changed by this audit.

Path candidate8f6a6b44 still seeds each photon with seed+i and loops both
adjacent seeds per profile. Main and positive seed intervals overlap, so its
replication is not disjoint. Checks for the first seed are overwritten by the
second; finite geometry/completion tests are absent. The genuine T residual
negative is useful, but it uses different seeds and does not change the mean
observable. Referee a6330d3e advancement is premature. Candidatef79c3eeb
replaces transport with independent exponentials; reject as wrong process.
Absorption78af36b changes control to1.1D;80232d9c omits rate change;d52fb7eb
only changes seed. da9d607c's prescribed control correctly fails selection,
but its negative_checks also demand an unchanged alpha0 calibration fail.
These are specification errors, not evidence against the physical identities.

Next finite falsification task: uniform M4/alpha3 and M8/alpha4, with the actual
cap coefficient C_M=4sqrt2/(9sqrtM), larger prespecified counts and disjoint
seeds. No observed result for these new cases has been used to choose them.
The conservative proof remains unchanged; selected-distribution bound unproved.

Late records through f96b5b5b:67b173d9 counts unscattered photons by T=1,Z=0
(which is wrong: an unscattered central ray exits with Z=1). 6a2a9b0b repairs
its atom proxy to near T1 and uses independent per-batch default_rng streams,
so the earlier per-photon overlap criticism does NOT apply to this version.
It still doubles the specified per-profile samples, uses a time proxy instead
of actual collision count, lacks completion/geometry certification and exits
silently on small discriminants. Needs work, not rejected physics. Referee
163c1aa9 incorrectly objects to exact d rather than sample mean in R: exact
centering is correct and avoids a fitted target. T substitution is an intended
wrong-observable control. Retain those tests; do not adopt an implicit-Euler
approximation or alter Thomson physics just to satisfy this referee.
