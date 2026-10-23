# Cold-branch discrete equilibrium test

Previous goal turn made progress: longer response established an offset/fluctuation distinction and exposed coarse-domain failure. All runs are terminal.

Next test is the scientifically relevant cold branch. Generalize the existing CIC equilibrium solver to occupation A, preserve gamma=.01, mass1, ra1, domain10, and continue from A10 to A10000. Compare 256 and 512 nodes, plus continuum mass1 shooting reference. No fitted parameter is derived by this continuation. A family of equilibria is not a physical evolution; its Casimir invariants differ.

Use the same cap-safe Newton solve and verify residual, mass, quadrature refinement and sampled force-law agreement. The stiff cold reference is distinct from the zero-stiffness algebraic law. Do not infer live stability or near-law formation from equilibrium convergence.

## Live extension

All 14 continuation solves converge below 6e-13 residual. Proceed with A10000 live controls and equal-energy .0008 perturbations through t=40, using the same two particle/grid/time-step combinations as the warm runs. Preserve cap/domain failures and partial trajectories. No live stability claim unless controls and resolution comparison support it. This extension was specified after inspecting equilibrium solves, before live runs.
