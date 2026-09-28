# CFG35 — the cold-matter rule, derived from B's own conservation law

Script: `CFG35_cold_mass_conservation.py`, about 3 s.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. Collapse masses are divided by 10, and H1b fails (rc = 1).
- The main run exits 1 because H2 failed. That is reported as run.

## The derivation

T4 makes B's cold fluid pressureless and conserved, and CDM-like before turnaround. Feedback pushes gas, not a pressureless fluid. So a bound system keeps the cold mass it collapsed with, M_c = (1 − f_b) M_coll. T5's "cosmic share of today's baryons" is only a floor, which is why CFG34's groups fall short by the baryons they lost.

With T5's identity (the cold fluid first *is* the law's phantom), the **conservation form** follows:

dark(<r) = M_ph(<r) + f_ex (1 − f_b) M_NFW(<r; M_coll), with f_ex = max(0, 1 − M_ph,edge / [(1 − f_b) M_coll]).

- M_coll comes from the stellar-to-halo relation (Moster+13, h48's committed function). B inherits it because its pre-turnaround dynamics are ΛCDM's.
- The collapse profile is Dutton–Macciò NFW.
- The edge is x_e = 0.40.
- No new constant enters. Groups and clusters are not scored, because every collapse estimate available for them uses the hydrostatic mass itself.

## Disclosures

The first MUTATE run showed the declared H1 ("within 2σ") has no bite, because the law alone already sits at 1.7σ. H1 is kept and reported. H1b ("better than 1σ") was declared before the main run and is the headline.

The same run exposed a bug: the Salpeter variant fed Salpeter masses into the SHMR. M_coll now always comes from the Kroupa-like mass that the relation is calibrated on.

## Results

**C1 (control):** CFG32's offsets under the law are reproduced (1e-16).

**H1b passed: the rule closes the X-ray ellipticals.** The mean per-galaxy offset is −0.013 ± 0.135 dex (−0.1σ) canonical and −0.024 (−0.2σ) alt, against +0.28 under the law alone. Five of seven galaxies get a leftover (f_ex 0.78–0.92, M_coll 0.6–2.4 × 10¹⁴). NGC 720 gets none and stays at +0.57, the Kroupa M/L outlier. Across the edge window the result barely moves (−0.019 to −0.008).

**H2 failed: the same rule breaks the most massive spirals.** Over SPARC, f_ex is zero in only 88% of galaxies, below the 90% declared. Where it is not zero, the leftover raises v_c at the HI radius by up to **+0.30 dex**:

| galaxy | log M_* | Δlog v at R_HI |
|---|---|---|
| UGC 2885 | 11.4 | +0.30 |
| UGC 2487 | 11.5 | +0.24 |
| ESO563-G021 | 11.3 | +0.24 |
| UGC 11455 | 11.4 | +0.24 |
| NGC 6195 | 11.4 | +0.23 |

Their rotation curves follow the law.

## Standing

**The derivation holds: a pressureless cold fluid keeps its collapse mass.** Its most direct form fixes the ellipticals, but only by giving every galaxy of the same stellar mass the same collapse mass. The colour-blind SHMR puts log M_* ≈ 11.4 galaxies in ~10¹⁴ M☉ collapses, and massive spirals show no such mass.

B can adopt the rule only if, at fixed stellar mass, spirals sit in smaller collapse masses than ellipticals: small enough for the phantom to use all their cold fluid (M_coll ≲ 10¹³ at log M_* ≈ 11.4). Weak lensing points that way qualitatively. Testing it needs a morphology-split stellar-to-halo relation, which is not in the repository.

Until then, B's cold sector has no single rule that fits massive spirals and massive ellipticals together. That is the old MOND-versus-halo split, now located precisely inside B.

Nothing here says the theory is closed.
