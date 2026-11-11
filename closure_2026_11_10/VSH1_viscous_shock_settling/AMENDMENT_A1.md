# VSH1 AMENDMENT A1 (post hoc; committed alone; written AFTER the first full run of every mode was seen)

Disclosure: the first run's outputs (known answers, the six graded runs, MUTATE, the reported scan) were all read before
this was written. They are kept unchanged in `first_run/`. As frozen the label is **NO VERDICT / NO VERDICT**: KA3 fails,
and the two graded log M_b 11.5 runs stopped at the script's step cap before z = 0.

1. **KA3 was mis-specified.** It assumed the turnaround radius is untouched by the fluid terms. It is not. At nu_F the
   viscous stress and the heated gas change the outer flow: R_ta(z 0) is 57.9 kpc at log M_b 9 against FLD1's 88, and
   259.6 at 10.5. The 11.5 run had also not reached z = 0. KA3 is replaced by **KA3'**: the lane's force law and initial
   conditions with every fluid term off (independent shells, leapfrog, FLD1's time step rule, shells inside the wall
   max(1.2 sqrt(G m_ex/a0), 0.3 kpc) held at the wall) give R_ta(z 0) within 3 % of FLD1's table at log M_b 9 (88 kpc)
   and 11.5 (600 kpc), canonical. This tests what KA3 was meant to test: the force law and the starting state.
2. **The step cap is a script guard, not a criterion.** It was 6e6 steps or 3000 s. It stopped the graded log M_b 11.5
   runs on both footings (at the stop: R_sh 156.0 / 155.9 kpc against r_e* 127.9 / 116.4, S 0.0066 / 0.0051, shock past
   r_e* at z 1.46 / 1.65). It is raised to 6e7 steps or 4 h, and the redshift at which a run stops is now recorded. A run
   that still stops at the cap reads not SETTLED, as frozen.
3. Nothing else changes: the model, the masses, nu = nu_F, N = 600, the SETTLED rule, KA1, KA2, KA4, MUTATE, the labels.
   The reported scan is re-run for nu = 0 and 0.1 nu_F at the three masses and for gamma = 4/3 and 10 nu_F at 11.5 only.

Also seen in the first run and reported here so that it is on the record before the amended run: at nu_F the hot region
at log M_b 9 and 10.5 reaches beyond the turnaround radius (R_sh/R_ta 2.66 and 1.58). There the frozen "hot" rule is met
by viscous heating of the whole converging flow, where r|g| is small, not by a thin shock. With shock capture only
(nu = 0) the hot region ends at 0.36 to 0.47 of R_ta at the stop. The charge inside R_sh is 1 to 7 % of the law's halo
mass at that radius in every first run.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
