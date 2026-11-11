# SRH1 AMENDMENT A1 (post hoc): more tilt cases, reported only

**Post hoc.** Written after these SRH1 numbers were seen: G2 and G3 on the primary grid (`srh1_rc.out`), G4 on the primary
grid, the comparators and MU4 (`srh1_lens.out`), and the halo-model R_cold rows of the G1 cases in the run log. The G1
forest Delta chi^2 of the primary grid had not been computed when this was written.

**What it changes.** Nothing graded. The labels, the window W, the gates, the grid, the known answers and MUTATE stay as
frozen in FROZEN_CRITERIA.md (5ed8a37ec6). A1 only adds reported tilt cases.

**Why.** On the primary grid G4 passes only at f >= 1.25 (both footings), while the frozen tilt grid has f0 <= 1.0.
- With f = f0 (1 + z)^beta, the KiDS lenses sit at z about 0.31 and the forest's failing bins at z 2.2 to 2.8. So a tilt
  with beta < 0 can put f above G4's edge at the lenses and below G1's edge in the forest.
- The frozen tilt grid cannot reach that region. It cannot say whether a tilted history opens a window.

**Added cases (reported, never graded):** beta = -1 with f0 = 1.25, 1.5, 2.0; beta = -0.5 with f0 = 1.25, 1.5.
- Each is evaluated on G1 (FZS1's pipeline: halo model plus forest gate), G2 and G3 (coverage lines), and G4 (ONE1's gate,
  the same machinery as the primary).
- The frozen tilt cases (section 1 item 4) also get G4 here, as FROZEN_CRITERIA requires when G4 fails somewhere on the
  primary grid.

**How to read it.** A tilt case that passes all four is a window that exists only with the tilt. That counts against the
family (FROZEN_CRITERIA section 7). It would also be a statement about shape: the settled radius would have to grow faster
than FLD1's R_fold toward z = 0. Neither is a derivation. Neither is in PAPER72.

Script: `srh1_tilt.py` -> `srh1_tilt.json` / `.out`.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
