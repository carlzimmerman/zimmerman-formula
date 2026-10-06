# Independent review of the root EdS kernel

Reviewed actual `../analytic_pressure_kernel/REPORT.md` and `checks.py`, reconstructing equations rather than accepting their test verdict. The two primitives and epoch statistic are correct under the stated common-potential, pressureless-background, Born-growing-mode hypotheses.

Starting with H=H_m a^(-3/2), delta_c=A a and dot U=Q k^4 A/a gives dU/da=Q k^4 A/(H_m sqrt a). A second integration uses dDelta/da=U/(H_m a^(3/2)). It yields exactly the reported initial-U term and logarithmic source term, including both factors of two and the lower-bound square root. Direct differentiation recovers U and dot U; both source terms vanish at the initial epoch. The initial-U term has zero source, not zero relative velocity.

For mixed gas/wave forcing the statistic equals Q k²−v_0² only when the gas unperturbed density uses the same growing amplitude as the cold density. If delta_b=A_b a and delta_c=A_c a differ, the constant gas term instead is −v_0² A_b/A_c; arbitrary scale dependence of that ratio spoils the two-k identification. The report's common growing-mode/Born assumption supplies this restriction. Actual CLASS baryon/cold initial transfers differ and the sibling computation therefore integrates each density separately.

SI dimensions agree: Q has m⁴/s²; k is comoving m^-1; H_m is s^-1; U is s^-1. Converting masses from eV/c² to kilograms and k from Mpc^-1 to m^-1 matches the equivalent c=1 coefficient ell²/4, ell=ħc/(m_eV Mpc_metres). epsilon=Q k⁴/(H_m² a_d) is the wave restoring-frequency-squared/H² and is maximal at the initial EdS epoch. Small epsilon and small integrated correction are necessary controlled-Born checks, not a rigorous universal error theorem. The k1000 benchmark fails this check; it cannot be used as a prediction within this approximation.

The test script's independent quadratures validate these formulas on the declared points. Its deliberately omitted wave k-power is detected. Its two-k coefficient recovery demonstrates a restricted invertible model, not a likelihood or unique wave identity. No missing numerical factor was found.

Smallest missing implication: a tracer/metric observation model that reconstructs A and the two-species velocities with controlled source subtraction. Neither the exact kernel nor the local CLASS null test supplies that observational reconstruction. With an arbitrary differential potential Psi_b−Psi_c=−Q k² delta_c/a², the same wave source is reproduced identically; a positive higher-gradient stress can also reproduce k⁴ without free-wave microscopic identity.

Addendum: the root report now explicitly sets delta_b=delta_c=Aa and records the A_b/A_c exception. I checked that revised text; it resolves the precision point above. The formula verdict remains accepted within that scope. Root's `main_b_explicit_common_mode` is the current explanatory record; `main_a` is historical because its pinned report predates this clarification.
