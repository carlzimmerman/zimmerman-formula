# QX12 iter_3: isothermal sector in contact with the sea. FAIL (class dead on cluster shape, for every c_s0)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane.
- Criteria: FROZEN_CRITERIA.md (b605c9fd7c), plus Amendment A1 (9c7497b4cc), committed before any graded number.
- Script: qx12_i3.py (4 workers, about 1 min). Logs: run_main.txt, run_mutate.txt; MUTATE in qx12_i3_MUTATE.*.

The sector is p = c_s0^2 rho, with rho = A exp(H/c_s0^2) in each host. A is the sea density, capped at
f_cap R M_b. The fit is self-consistent with the a0 law, and only the excess over the sea gravitates. The single
constant c_s0 is fixed by the galaxy gates alone (G5/G6/G7), and clusters are then predicted.

| | canonical | alt |
|---|---|---|
| c_min (galaxy gates only) | 246.5 km/s | 246.5 km/s |
| X-COP at c_min | **-0.713 / 0.812**, FAIL (over) | **-0.724 / 0.819**, FAIL (over) |
| groups at c_min | [-0.398, -0.207], FAIL | [-0.427, -0.240], FAIL |
| best X-COP rms anywhere on the 100-6000 km/s scan | 0.463 (c 1135) | 0.436 (c 1216) |
| c passing X-COP and the groups band (CLUSTER-SET context) | none | none |
| variant host (core r^max(s0, 1.2)) | FAIL, same numbers | FAIL |

Label: **FAIL**, on both footings and both hosts. No c_s0 passes X-COP, so this is a class no-go, not only a miss at
c_min.

Why: Boltzmann retention exp(D/c_s0^2) is exponentially sharp in depth.
- For c_s0 up to about 800 km/s, every cluster fills its capture cap (4.2 M_b), and the sector collapses into the
  core. The enclosed mass is far too high at 0.1-0.7 R500.
- Above about 1200 km/s, clusters keep nothing and the plain law's deficit returns: +0.47 / +0.43.
- The transition is too abrupt for any c_s0 to give an extended cluster profile. An extended profile needs
  c_s0 ≈ the cluster's own dispersion, and that varies from cluster to cluster.
- Groups pass the band only at 325-529 km/s, where X-COP has collapsed.
- So one sound speed can't serve every host: the sector's temperature has to track each host's virial temperature.

Known answers and controls:
- **KA1 FAIL as frozen**: the uniform sea comes back with max relative error 3.94e-5 against the 1e-6 line. That is
  the quadrature error of the mass integral on a 900-point log grid. It is 1e-4 of the 0.4-0.8 dex misses that set the
  label, so the label stands, but the known answer is on the record as missed.
- KA2: at c = 6000 km/s the galaxy shifts are <= 1e-3, PASS.
- KA3: R = 0 gives X-COP +0.4676 / +0.4347, against QX2's +0.4675 / +0.4345 (offset 1-2e-4, PASS).
- M1: c = 30 km/s fails the galaxy gates (G5 4.23, G6 -0.36), BITES.
- M2: M_cap = 0 returns the plain law, BITES.
- Every solve converged (conv 1.00).
- Smoke-test fixes are disclosed in A1: the sea's own gravity, and singular host centres.
