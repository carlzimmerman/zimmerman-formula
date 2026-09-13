# Independent audit of Claude L223

The fresh commit `aeae2b650` runs `L223_end_to_end.py` and reports 11/11
checks.  Re-running the executable succeeds, but the run is a consolidation of
previous lanes, not a derivation from one action.

The independent parser `L223_independent_audit.py` finds that the gate table
inserts literal measured values for the preferred-frame/gamma entries (zero),
the alpha-alignment entry (one), and other gate quantities.  It also confirms
that the reach used in the forest and criticality gates is explicitly a
`KAPPA = 3.2e4` stand-in after the earlier cutoff result was withdrawn.  The
script contains no Euler--Lagrange variation or common covariant field equation.

Consequently, “11/11 pass” means only that the chosen post-audit parameter point
is numerically consistent with the imported inequalities.  It does not derive
\(\gamma_{PPN}\), \(\alpha_1\), \(\alpha_2\), or \(\alpha_3\); in fact the
run does not expose separate \(\alpha_2\) and \(\alpha_3\) gates.  It also does
not perform a Boltzmann/CMB calculation, an N-body galaxy calculation, or the
full nonlinear metric/Dirac analysis.

Run:

```text
python3 fable_independent_2026/L223_independent_audit.py
```

The result is intentionally diagnostic and exits 0.  The correct status of the
underlying relativistic construction remains **OPEN**.
