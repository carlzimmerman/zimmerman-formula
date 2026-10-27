# X59 AMENDMENT A2 (coordinator's band gate, added AFTER the first graded numbers; disclosed as post-hoc)

**Timing.** The coordinator's gate arrived after the A1 run had printed its graded numbers, but before anything was
committed. It is recorded here as an amendment. It does not replace the frozen §2 verdict, which is still computed and
reported unchanged. The band gate is reported alongside it, and its post-hoc status is disclosed.

**The question (from the coordinator, after X58 c3b4f2c7d9).** X58 found the needed pattern is non-monotone in mass:
dwarfs need halos, L* lenses need the law, clusters need halos. FE is keyed on formation epoch, not purely on mass. Does it
reproduce that pattern?

**Band gate.** Evaluated per footing, on a mass grid at z_obs = 0 (step 0.05 dex), each mass at its own EPS z_c:
- **dwarfs, M200 10⁸–10¹⁰ M☉: must RETAIN.** FE must hold at every grid mass. Reported only: the fraction, and z_c = 8
  (X51's cooling epoch).
- **L* lenses, M200 10^11.35–10^12.05 M☉: must be EXCLUDED.** At every grid mass, the object itself must fail FE
  (f_self = 0). Under the frozen sticky persistence (§0), the early-capture fraction must also stay within tolerance,
  f_EC ≤ X22 f_max. f_EC is interpolated from the Monte Carlo host grid. Reported only: the re-keyed reading, which uses
  f_self alone.
- **groups and clusters, M200 10¹³–10¹⁵ M☉: must RETAIN.** FE must hold at every grid mass.
- The gate **PASSES** only if all three bands hold on each footing. Otherwise it is **FE BAND GATE FAILS (<bands>)**.
  Footings that disagree give **UNDECIDED**.

**c_f for the band gate.**
- **PRIMARY: c_f = 4 (X43, η = 14.83), with the M-DEC F(z).**
- Variants:
  - c_f = 4 with flat F;
  - X48's 3-seed ng 48 table (the §0 primary);
  - **X48 A2's nine-seed table**, 11.63 / 8.22 / 7.31 at 10¹² / 10¹³ / 10¹⁴ (`x48_regrade_A2.json`, c218c10add), held
    flat outside, as the other tables are.
  Each variant is run with both M-DEC and flat F.

**Implementation notes (no number changed).**
- The Monte Carlo now runs in blocks of 200 walks instead of 1000, to keep peak RSS under 1 GB. The first A1 run peaked
  at 1.21 GB and failed K6. The random stream is row-major and identical, and every graded line is unchanged (diffed).
- Under MUTATE a0x10 the K1b crossover has no root in 10⁸–10¹⁶. The script now records NaN there, so K1b fails, instead
  of crashing.
- The new η modes add Monte Carlo tables for the same walks. The existing numbers do not move.
