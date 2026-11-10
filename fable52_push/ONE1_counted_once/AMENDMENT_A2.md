# ONE1 AMENDMENT A2: scope cut from the lead (post hoc; committed alone)

Criteria a967a38851, A1 14b25fdd71. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

## Timing, disclosed first

**This amendment was written after graded numbers existed, and after I had read them.** When the lead's instruction arrived:

- `one1.py` had run: row 0 PASS; row 1 PASS; rows 3, 4 and 5 FAIL on both footings (X-COP at prefactor 1/2, mean
  +0.162 / +0.147; groups 0/6 and 0/7 of 20; the Bullet's class TENSION, subcluster M300 Z -2.58); rows 7 and 8 carried.
- `one1_coma.py` had run: Coma UDGs PASS (+0.325 / +0.285 dex against 0.524); dSphs FAIL (bright M31's CI excludes 0).
- `one1_kids.py` had printed the primary reading and the X = 53.64 and 80 brackets. **The KiDS gate at 1.6 R_h reads PASS
  on both footings** (z all / late / early -1.14 / -1.46 / -0.65 canonical, -0.23 / -1.23 / +0.21 alt). X = 80 fails it
  on the canonical footing (z all -2.69).

The narrowing below came from the lead, for coordination with lanes RB1 and RB2. I did not choose it. It takes failing rows
out of this lane's label. So RESULT.md states, in its first lines, that rows 3 to 6 were computed here before the cut and
what they read. Their outputs stay in the folder unchanged.

## What changes

- **Label.** Per footing, for the KiDS host-free row only:
  - **KiDS host-free: PASSES** if the frozen KiDS gate holds (G-K1 for all, late and early; G-K2; G-K3; all at
    1.6 R_h, as frozen);
  - **KiDS host-free: FAILS** otherwise, naming the failing lines;
  - **NO VERDICT** if a known answer that feeds row 2 fails (KA2 to KA7).
  Then one sentence per bracket.
- **Rows 3 to 6 (X-COP, groups, the Bullet, Coma UDGs and dSphs): not graded here.** They are graded in RB1 and RB2
  (other sessions, under `closure_2026_11_09/`). RESULT.md quotes their labels only if their RESULT.md files exist when I
  finish. The numbers computed here before the cut are reported as computed, not as this lane's grades.
- **Rows 1, 7 and 8: carried, no new grading.** Row 1 is PD1's P2, reproduced exactly as a known answer (KA1). The SPARC
  row with this reading's end radius (no turnaround cap), computed before the cut, is reported beside it.
- **Row 0 (conservation)** stays only as the line MUTATE M2 bites on (share x 10 must fail something).
- **New reported brackets, KiDS only:** X = 10.82 (PD1 A2's basin share, 5.41 x 2.0) and X = 5.41 (the cosmic share),
  because the owner's decision table names them. They use the frozen statistic and are computed after this file is
  committed.
- Section 9, the Lean files and the KiDS MUTATE arms stay as frozen.

## Unchanged

Every KiDS statistic, line, tolerance, tie rule, the mass-factor rule, the neighbour model, the known answers and the
MUTATE arms. Nothing graded is recomputed under a new rule.

## Also disclosed

I read the owner's decision file (`closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md`, 1005946f33) after my
criteria were committed, during the KiDS run. Nothing in the criteria conflicts with it. One difference is worth stating:
the decision table carries the Solar System as "B equals the law inside the truncation radius" (PD1 P6). ONE1's reading,
as briefed, is Newtonian for stars, because no star holds a share. Both pass Cassini. For wide binaries they predict
differently: the law gives a boost below a0; ONE1's reading gives none.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
