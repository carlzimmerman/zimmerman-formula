# Independent review of the M6 patch-capacity calculation

Reviewer: selector/gate-correction agent, independent of the capacity implementer.
Read-only audit, 2026-10-27. No capacity source or output was modified or rerun.

**Verdict:** exact two-phase bookkeeping passes; interpretation remains
conditional on the inherited X57 variance prescription. No calibrated forest
confidence limit is established.

For inside baryon contrast d>0 and patch volume fraction f, mean conservation
gives d_out=-fd/(1-f), F=f(1+d), and point variance

    V = f d^2 + (1-f) d_out^2 = d^2 F/(1+d-F).
    F = V(1+d)/(d^2+V), capped at F<=1 by outside-density positivity.

These are the expressions in `patch_capacity.py:13–28`. A separate Decimal
calculation at 50-digit precision reproduced the saved budget, fractions,
patch masses, number densities and baryon densities to 2.23e-16 relative.
Both phases also satisfy baryon+cold compensation on the saved native inputs,
with positive densities. The inferred quantities are:

| Quantity | canonical | alt |
|---|---:|---:|
| inherited variance budget | 0.2101459632 | 0.2101459632 |
| exact fraction F | 0.06061499359 | 0.04856637289 |
| baryon density in patches, Msun/Mpc^3 | 375286508.6 | 300689704.7 |

`rho_b=(2.77536627e11)*Omega_b*h^2`, the Mpc/h-to-Mpc radius conversion,
`M_patch=rho_b V_patch(1+d)`, and `n_patch=F rho_b/M_patch` are dimensionally and
numerically consistent. Efficiencies multiply the reservoir capacity and are
not measured. The population condition remains necessary only for the stated
closed-reservoir model.

The code docstring, output status and non-claims distinguish the inherited
variance budget from a flux likelihood. Exact V here is a two-phase **point
variance**; the algebra does not certify smoothing, spatial covariance, flux
conversion or nonlinear evolution. Those remain separate obligations.
No load-bearing defect was found within the declared accounting scope.

Provenance:

- `patch_capacity.py` SHA256:
  `5e3f9bc672396da94f6c5632a4b99c499360b54d489a66555b30ba46dd8f50a6`.
- `capacity_run/results.json` SHA256:
  `7c9bddc3a7ce6167b7cab221375c12e496a7b4384dd97010d90604f2e3cd68ee`.
- `capacity_run/manifest.json` validated against the current declared inputs:
  valid evidence record, run status `completed`.
- Independent check used only Python standard-library Decimal, JSON and
  arithmetic on the saved inputs; no original output paths were opened to write.
