# Calibration assumptions and limits

The finite calibration changes one declared relation: the switch uses the same mass-dependent collapse column that sets the core. It does not add a fitted threshold. L remains an externally chosen/calibrated normalization, tested only at the three previously used values. Kappa=1/2 remains fitted.

- S9 is the existing ng48 nine-seed median concentration curve in the X48 A2 summary; interpolation is linear in concentration versus log mass, clamped below1e12 and above1e14 exactly as CL2/CL3. The transfer to continuum or ng64/cluster mass is untested here.
- CLASS/EPS/background A and B, primordial input and background fit remain model inputs, not independently validated by this calibration. SPARC background B uses its own exact EPS collapse function when evaluating the basin switch.
- BS1 primary basin geometry, matcher, member list and sum of members' EM1 own M200 are unchanged. Own mass is used where BS1 has no measured basin. This remains a nonlocal phenomenological basin posit without an action.
- SPARC core amplitude uses own M200; only the flag uses selected basin mass. Groups/clusters and isolated lenses preserve their existing mass assignments; the GS1 measured gas slope and GC2 budget extension are preserved.
- X53's five-node log-log collapse table, linear edge extrapolation, radius grid and profile projection remain primary. Its direct sc>floor uses exactly its core column in its units; this representation differs numerically from exact EPS, and the finite diagnostic states that difference without silently replacing X53.
- MW/dwarf claims belong to the separate heldout package and are not inferred from calibration pass/fail.
- Baseline reproduction is computational agreement, not independent physical validation. Source slicing inherits the original integrators and observational estimators. Transformations are unique-count checked and saved as executed source copies.
- One numerical thread is requested in all standard library environment variables. Observed RSS is recorded per process. macOS RLIMIT_AS is deliberately omitted; nice15 was attempted on initial startup but denied by sandbox. No global memory cap is claimed.
