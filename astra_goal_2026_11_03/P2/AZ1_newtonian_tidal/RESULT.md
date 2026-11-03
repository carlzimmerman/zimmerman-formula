# AZ1 result: FAIL on both-footing requirement

κ = ½ FITTED; not theory closed

This Newtonian tidal estimator is distinct from KT28 and reconstructs the point-source mass exactly, without seeing an added uniform Newtonian acceleration. It therefore also reproduces the problematic constant r_M/2 solar filter. In results.json, canonical Q2/ceiling = 0.480594078612 (margin +0.519405921388); alt = 1.056745464443 (margin -0.056745464443). Canonical PASS and alt FAIL refer only to the inherited Cassini quadrature. Numerical refinement changes the ratios by less than 1e-9, far below the alt miss. This is not a full Cassini field-equation solve.

Known-answer mass/length identities are exact at the six tested synthetic points per footing; the doubled-coefficient MUTATE has relative mass error 1 and is rejected; the Newtonian quadrupole is zero. Ten checks pass. No astrophysical knob scan was made. The only free physical coefficient is κ=1/2 FITTED. The point-mass normalization 27/sqrt(6) follows algebraically from the Hessian identity.

The rule also remains undefined when grad ||T_N|| = 0, including a homogeneous core. No clip or extension was fitted after seeing that singularity. This is a separate unclosed obligation, not a data grade. MW, dwarfs, SPARC and the other RQ3 rows are NOT EVALUABLE in this lane because the necessary joint-footing screen already failed. No twelve-row credit is claimed.

Continuation: a physically derived environmental-tide dependence could alter the solar result, but adding a coefficient to lift xi is a new fitted rule. A regular local differential operator is a distinct route; investigate its conservation and action variation before observations. Do not rerun this isolated estimator unchanged.

Command: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 astra_goal_2026_11_03/P2/AZ1_newtonian_tidal/run.py
