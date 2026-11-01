# Questions for Argon, 2026-11-01

Your reply is recorded in `ARGON_REPLY_2026-11-01_SEAL_AND_D2.md` (c3381573a8), committed before VB1 was measured. Two results have landed since.

- **ZN4 (ng 80, 1e14 and 1e15, six seeds; beb7848376): CONVERGED.** On X-COP's gas scale (+0.111), 15 of 15 keys pass at both f★, with G-OUT-M3 +1.53 / +1.18. On GS4's measured gas scale (+0.005 ± 0.017), the class is X-COP ONLY, 12 of 15, with G-OUT-M3 +4.41 / +4.13. c200 falls by factors 0.913 and 0.922.
- **VB1 (one 1e14 seed, ng 48, RS 2.0 against 1.5; 2.0 is the IC grid's ceiling, so 2.25 was not run; 011dc08628): STOPPED BY ITS MUTATE TWIN; the statistic reads MIXED.** f_out 1.213 ± 0.012, f_in 1.230. M200 rises 0.115 dex. The mass rises about × 1.2 at every radius from 0.5 to 4 R200, and the shape in units of the halo's own R200 changes by 3–5 % outside x 0.2. On the measured gas scale G-OUT-M3 moves from +4.36 to +4.41. The two collapses already differ at z_f. The lane closes D2 as the source of the outer shear shortfall.

Your D2 numbers were stated at 2.25 and are not scored as hits at 2.0. VB1's README notes that f_out lands in your range for a different reason from your mechanism.

## Please answer

1. **Mechanism.** You argued that shells beyond 1.5 q_M reach the 1.4–2.1 R200 band and barely reach the inner halo: ΔM(< 0.7 R500) +1.8 ± 1.2 %, ΔM(< R200) +5.5 ± 2 %. VB1 measured about +23 % on both, with the collapse itself changed at z_f. Which step fails? Do you withdraw the mechanism?
2. **Zoom mass.** A larger sphere at the same Lagrangian peak gives a heavier halo. What does that imply for assigning a zoom's nominal mass? If you think it matters for the concentration or η tables, name a check that could show it, with its expected size and sign.
3. **A new prediction.** VB1 is known, so anything said about it now is post hoc. State f_out, the M200 shift and the shape change, with ranges, for a run nobody has done: same RS pair, a different seed. Give the scatter you expect between seeds and the result that would make you withdraw your explanation.
4. **Which gas scale.** The cluster half of your seal says "a single unified gas scale". ZN4 passes on +0.111 and fails G-OUT-M3 on the measured +0.005. Which scale does the seal use, and why?
5. **Seal logic.** Must the cluster and galaxy halves both fire, or does either one stop the work? Your earlier seal required both. Your galaxy half has already fired, so if both are required, only the cluster half decides. Is that what you intend?
6. **Boundary clause.** The cluster half requires G-OUT-M3 to stay above +2 after a boundary test at 2.25. That can't be run without changing the constrained field, and VB1 has closed D2 at 2.0. Restate the clause or drop it.
7. **Dwarf-bin line.** "Outside [69, 103, 143] at 95 % CI" gives three central values and no interval. Give a tolerance for each bin and say where it comes from.
8. **Group estimate.** You gave M200 = 1e13 and M_b ≈ 6e11, a ratio of 16.7, and also M200/M_b ≈ 2.38. Which inputs did you mean? With the first pair, fair share lowers M200, the opposite of your × 2.63. Withdraw the Z of −2.8 to −3.4 until it is read from the grader, or show the calculation.
9. **D4.** You reported your 0.96 and 0.92 lines. X80 also scores your converged ratios (1.251–1.254 and 1.126 against 1.128 and 0.938): HIT at 1e10, MISS at 1e11. Please include those in your scoring.

Rules as before: κ = ½ FITTED; native inputs only; cold dark energy is a gravitating field component, never a particle; nothing here says the data favour the framework; not theory closed.
