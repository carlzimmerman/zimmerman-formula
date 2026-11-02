# RQ3 Amendment A1, 2026-11-02, after a smoke test of the new gates and before any full run

**What happened.** My frozen table in section 4 called the old gates' numbers "law". They aren't this law. The old lanes used FP1's `nu_mono` (CFG4 H5, CFG7 tdg, CFG31, CFG32, CFG34) or the exponential `nu_RAR` (CFG7 H2 globulars, h50 SLUGGS, with a0 9.36e-11, 1.13e-10), not nu = 1/2 + sqrt(1/4 + 1/y). I'd read past that. So on the frozen check the law fails these known answers, by more than tolerance, on a true difference of kernel:

| Row | Frozen target | The law, smoke test | Would fail frozen tolerance |
|---|---|---|---|
| A21 | +0.0077, +0.0533 [1e-3] | +0.0133, +0.0577 | yes |
| A23a field | 10.55, 13.08 [0.02] | 10.78, 13.30 | yes |
| A23a iso | 131.29, 151.85 [0.02] | 131.46, 152.00 | yes |
| A25 | 1.037, 0.988 [5e-3] | 1.016, 0.975 | yes |
| A26a | +0.0795, +0.0646 [2e-3] | +0.0767, +0.0620 | yes |
| A26b | +0.2802, +0.2536 [2e-3] | +0.2722, +0.2466 | yes |
| B2 | listed [2e-3] | within | no |
| A24 | listed [2e-3] | within | no |

**Change.** Those known answers test the wiring, so each now runs with **the source's own kernel and a0**, as a stated candidate (`nu_mono` at the source's a0; `nu_RAR` at 9.36e-11, 1.13e-10), same tolerances, none moved. The law's row is scored and printed as a result, with its difference from the source's kernel; it no longer has a record to match on these rows. This moves no row label, since none had been graded.

**Second change.** `no_halo_Newton` is written only to a CRG1 partial, not committed. So Newton's groups answer runs CRG1's own `crg1_groups.stat(rows, "none", None)` read-only, against the harness's B1, tolerance 0.01.

Also a bug found before any run: RQ2's `is_law` probes with zero gas, so UX3's term would have been taken for the law and handed LW1's solves and the law's READ rows. The probe now has gas in it. RQ2's committed results aren't affected, since it ran no gas-reading g.

kappa = 1/2 FITTED; not theory closed.
