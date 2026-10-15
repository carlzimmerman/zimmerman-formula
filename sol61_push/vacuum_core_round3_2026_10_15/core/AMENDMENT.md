# EOS endpoint and admissible path clarification

15 October 2026. This supplements the frozen `PROOF.md` after its `run_v3`; it does not alter a pinned input.

The inverse charged EOS was specified only on 0<rho<=rho_*. The statement that bounded eta/rho makes a two-sided positive-density path admissible needs this extra EOS-domain qualification: at the center the displayed trial has eta_c(0)=rho_*, so positive path parameter would raise the density above rho_*.

For the negative-energy counterexample, choose a sufficiently small **negative** path parameter tau and rho_a(tau)=rho_a+tau eta_a. At the origin the charged density decreases. The unperturbed profile has a strict quadratic central maximum; the perturbed profile retains that maximum for sufficiently small tau. Away from the center on each compact annulus there is a strict gap below rho_*, and the tail perturbation is bounded relative to the vanishing density. Therefore a one-sided interval -tau_0<tau<=0 stays in the specified charged EOS domain and keeps both densities positive. Both total masses are unchanged, because the trial enclosed masses vanish at both ends. Gauss is solved along the path; its background field has a strict margin from the pole, preserved for small tau.

The constrained first variation vanishes. Thus E(tau)=E(0)+(tau^2/2)Q+o(tau^2) decreases along this one-sided admissible path because Q<0. This already refutes constrained local-minimum/positive-energy closure for the declared candidate. A two-sided linearized PDE interpretation would additionally require a chosen thermodynamically admissible continuation of the EOS above rho_*, for example a C1 pressure continuation with positive derivative; that would be a further continuum input, not derived microphysics. No such continuation is silently assumed in the counterexample.

The independent reviewer supplied an explicit global interval. In normalized units,

\[
 {\eta_c\over\rho_c}={25(25-8r^2-r^4)\over\sqrt{1+r^2}(25+r^2)^2},
 \quad \left|\eta_c/\rho_c\right|\le25,\quad
 {\eta_s\over\rho_s}={8\over5}{\eta_c\over\rho_c}.
\]

Choose -1/40<tau<0. Both densities stay positive. Where eta_c>=0, the charged density decreases and stays below rho_*. Where eta_c<0, r^2>sqrt(41)-4>1; hence the original density is below rho_*/4, and its path factor is below two, so it remains below rho_*/2. Finally delta D/D=Y/M_c(<r)=25/[sqrt(1+r^2)(25+r^2)] lies in (0,1], so the negative-parameter Gauss path stays between zero and the background field. This gives an explicit admissible one-sided path without any extension of the EOS.

The independent reviewer also corrected the draft displacement asymptotic before the final frozen run: Y~25r^-3, while rho r^2~const*r^-3, so xi=O(1), not O(r^-2). The kinetic integral remains finite. The final proof and `check_core_v3.py` contain the corrected statement and exact tail check.
