# TH07 independent release-energy audit

Owner `thermal_energy_audit`, 2026-11-03; exclusive write scope this directory.
No Git mutation, package install, queues or outside-source edits.

Claim: an isolated hidden false vacuum releasing excess energy DeltaV at scale
factor a_release must satisfy DeltaV*a_release^4 <= Kmax if its subsequent
stress has averaged 0 <= w <= 1/3 and it is to meet the declared recombination
rest-mass and pressure budgets. This is a necessary condition, not a sufficient
production history and not an exclusion of all initial states.

Conventions: a_today=1, a_rec=1/1101, Omega_chi=.265, Omega_extra_matter<=.0265,
pressure-equivalent DeltaNeff<=.3, Mp=2.435e18 GeV and the TP04 reference H0.
Visible entropy is conserved, g_s(today)=43/11, and initially xi=T_D/T_SM=.02
at a common high-temperature SM g_s=106.75. A collisionless relativistic dark
bath has T_D*a fixed. An internally equilibrated bath has instead
g_s,D*T_D^3*a^3 fixed before latent-heat injection; both assumptions will be
kept explicit. No SM portal transfers latent heat away.

Finite numerical assertion: reproduce Kmax and high-temperature comoving
visible-radiation energy, compute DeltaV using the global full one-loop CW plus
tree gravity source supplied by thermal worker, report latest release a and
corresponding pre-release T_D, T_SM, H and vacuum-domination ratios for the two
specified preferred canonical/protected points. No finite interpolation will
be extrapolated. All physical ΔV values are conditional on that truncated
global potential and its valley; a thermal false root may replace X=0 where
available.

Each experiment must have a JSON contract and use the installed mathbox v2
runner, wall<=120 s, CPU<=115 s, one numerical thread, actual input hashes,
fresh output directory, measured RSS. No unsupported macOS affinity or memory
limit is requested. Any radial thermal bounce experiment requires a separate
predeclared contract, actual canonical field coordinate and potential source,
false-root subtraction, overshoot/undershoot/convergence controls, and cannot
be replaced by extrapolating a finite fit.

Analytic audit must state: continuity and E-m<=p^2/E assumptions; effect of
visible and hidden entropy changes; false-vacuum domination before release;
limits of equilibrium free energy for a collisionless initial bath; and the
exception of sustained scalar kination, including the actual necessary
weighted-w condition. A claim that thermal trapping alone excludes a history
requires ruling out nucleation before the energy deadline; a spinodal found
later does not establish that stronger result.
