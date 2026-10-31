# SI1_spec_isolated_route_e: on spectroscopically isolated lenses, route E's shape is not rejected. S3 NOT POWERED, S1 LAW PREFERRED on amplitude

Criteria: `FROZEN_CRITERIA.md` (ed3c0f8bb1), committed alone before any script or model number. Script `si1_grade.py <kids_source_cache> <work_dir>` execs P2's text unchanged through its verdict loop. Outputs `si1.out`, `si1_results.json`, `si1_MUTATE.*`; shift scan `si1_scan.out`, `si1_results_scan.json`.

## Frozen grade (Δχ² = χ²(route E) − χ²(law), 15 bins, full covariance, Hartlap)
| footing, sample | χ² law (p) | χ² route E (p) | Δχ² | D | class | inner / outer Δχ² |
|---|---|---|---|---|---|---|
| canonical **S3** (2,251, primary) | 17.8 (0.276) | 12.6 (0.631) | −5.1 | 2.51 | **NOT POWERED** | +2.5 / −9.6 |
| canonical S1 (10,620, reported) | 15.8 (0.398) | 24.4 (0.058) | +8.7 | 4.26 | **LAW PREFERRED** | +7.2 / −1.9 |
| alt S3 | 18.5 (0.239) | 12.6 (0.631) | −5.8 | 2.86 | NOT POWERED | +3.8 / −11.6 |
| alt S1 | 16.9 (0.324) | 24.5 (0.057) | +7.6 | 4.88 | LAW PREFERRED | +7.8 / −4.2 |

Inner is R ≤ 0.31 Mpc, outer 0.4–3 Mpc. No parameter is fitted. Halo at lg M★ 10.78: lg M200 11.94, R200 201 kpc, r_ta 851 kpc, S 150, r₀ 14 kpc.

## What it says
**The KiDS result does not carry over to clean lenses as a preference for the law's tail.** On KiDS photometric isolation the law leads by hundreds. Here it leads by +8.7 on S1, and that lead is in amplitude at 120–750 kpc. In the outer range the two are level or route E leads.

**The mass offset does carry over.** Common log M200 shift that minimises χ²(H), reported:

| | best shift | Δχ² = 1 range | χ² at best | χ² at 0 |
|---|---|---|---|---|
| S3 | +0.43 | +0.30, +0.57 | 7.0 | 12.6 |
| S1 | +0.22 | +0.15, +0.32 | 18.6 | 24.4 |

This matches BL1's +0.26 on KiDS (all) and GH1's +0.17 [+0.05, +0.28] on G09 centrals. So three samples ask for about 0.2–0.3 dex at catalogue M★. Mass, not tail shape, is what differs on clean lenses. SI2 tests whether that is a red stellar-mass effect.

**Reported, S1, canonical:** A_in 1.39 ± 0.19, A_O1 2.89 ± 0.60, A_O2 1.67 ± 2.63. M★ +0.2: Δχ² +2.6; M★ −0.2: +14.4. No neighbour term: χ²(H) 26.2, Δχ² +12.4. Cut at R200: χ²(H) 26.5, Δχ² +10.8.

## Checks
K1 (P2's committed Δ and law model reproduced, 0σ), K2 (offset → 0 1.8e-4; uniform sheet 5.7e-3), K3 (M_h(R200) 1.8e-15), MUTATE (halo × 0.5 lowers m_H in every bin, χ²(H) 12.6 → 18.8): all PASS. No saturated r₀ solves.

**Disclosure.** The first run failed K2's sheet test at 1.0e-2, because I had reduced the distance grid to 600 points for speed. Rerun at P2's 1500 points it gives 5.7e-3. S3 and S1 χ² are the same to the printed digit in both runs, and the first run's labels read NOT DECIDED as frozen; the graded run is the second. A single z_ta, S3's weighted median 0.211, is used for S1 too.

## What this does not show
- It does not measure leakage in KiDS's photometric sample. N here is 1–6 % of KiDS's. D is the comparison, not the absolute Δχ².
- The neighbour term counts catalogued GAMA neighbours (r < 19.8) only. Halos of fainter galaxies are in neither model's neighbour term, and that matters more for route E, whose mass sits in halos.
- It says nothing about a cause for EM1's relation, the floor, or X78's alt failure.
- A preference here compares two members of this record. It does not say the data favour the framework over anything else.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
