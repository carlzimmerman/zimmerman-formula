# XJ1 AMENDMENT A5 (2026-11-14, written at 11:20 EST by the clock): the clock's inner caustics as settled radii with no free constant

Post hoc: written after the reported chains (matter level, lensing G4, rotation curves) were read for the frozen cases
and for A3's two radii, and after the first five rows of the shell computation below were read. Written before any
flux-level number of either build has been read. The second pass of A3 had started no part; it is stopped and relaunched
with the two cases below added. Nothing of the frozen cases or of A3's cases changes.

**What was computed and seen (shell dynamics only; no gate, no data).** `xj1_shells.py` executes FLD1's
`fld1_shells.py` with three text insertions and nothing else changed: a per-shell count of passages through the centre,
and three series columns, the largest current radius among shells that have passed the centre at least 1, 2 and 3
times (R_1, R_2, R_3). Its first five series columns reproduce FLD1's stored runs exactly. For log M_b 8, 9.4, 10.45
and 11.5 (canonical) and 10.45 (alt):

- R_1 = R_fold exactly (ratio 1.000 at every redshift): the fold radius is the first caustic.
- R_2 / R_fold = 0.68 at z 0, 0.65 at z 2.2, 0.61 at z 3.0, 0.65 at z 4.4, the same within 0.01 for log M_b 9.4 to
  11.5 (0.59 to 0.64 at log M_b 8 beyond z 2).
- R_3 / R_fold = 0.535 at z 0, 0.49 at z 2.2, 0.47 at z 3.0, 0.505 at z 4.4 (0.40 to 0.47 at log M_b 8 beyond z 2).
- For comparison, the self-similar collisionless infall onto a point mass in an Einstein-de Sitter background has its
  second and third caustics at 0.65 and 0.49 of the first (from memory of the published solution; not looked up; not
  used anywhere).

Also seen: with the exact junction the matter-level number is 3.43 / 7.65 at 0.5 R_fold and 14.2 / 33.9 at 0.75 R_fold;
every SPARC last point lies inside 0.47 R_fold today.

**Why.** A3 re-opened f as a number read from data for the exact junction. The shell dynamics that define R_fold also
define these inner surfaces, with no number to choose except the integer k: the region where every shell has passed
the centre at least k times. Behind the first caustic the clock is many streams; "settled" plausibly means more than
one passage. The choice of k is a choice, said plainly; it is an integer, not a constant read from data.

**Added cases (exact junction, section 1's definition unchanged):**
- **Ec2:** R_set = R_2(z, M_b), the second caustic.
- **Ec3:** R_set = R_3(z, M_b), the third caustic.

Both are read from this lane's shell runs (`shells/xj1_shells_<footing>_M<logMb>.json`, FLD1's 12 masses and both
footings, N 2400, start z 10, law on), with FZS1's interpolation, M_b (`Mb_fold`) and unit conversion unchanged, capped
at the halo's r_ta.

- Flux level, build B, the second pass of A3 with two more fields: R, E0.5, E0.75, Ec2, Ec3 and TWB2 = R + 2 (E0.75 - R)
  at the anchors; brackets for the four cases. Known answers, twin and label rule as A3 states them for its two cases,
  applied to all four; KA-E extended to the two new radii on the tables.
- **KA-K (the caustic tables):** (i) every shell run's first five series columns equal FLD1's stored run to 1e-9
  relative (all 24); (ii) this lane's reader on the `R_fold_kpc` column of the shell files times 3 equals FZS1's
  `rset_com(hb, foot, z, 3.0)` to 1e-9 relative for every halo, z and footing; (iii) R_3 <= R_2 <= R_fold at every
  stored time of every run.
- **Lane word added, per footing: Q4, a settled radius with no free constant, inside the fold.** For each of Ec2 and
  Ec3: "HOLDS WITH NO FREE CONSTANT (the second / third caustic)" if it reads HOLDS (a hit awaiting a blind re-grade,
  not a pass), "FAILS (...)" if it reads FAILS, otherwise "NOT RESOLVED (...)".
- Reported: matter level and lensing G4 for Ec2 and Ec3 (the two scripts with the case list extended, new output
  files); and the containment of rotation curves today: the number of SPARC galaxies whose last measured radius lies
  beyond R_3(z = 0; M_b) and beyond R_2(z = 0; M_b), with the largest ratio and its galaxy. Inside the settled radius
  the exact junction is the law, so a galaxy wholly inside keeps PD1's rotation-curve numbers; one that is not is named.
- Hand estimate (before any number of these two cases): matter level Ec3 3 to 5 / 7 to 10, Ec2 7 to 12 / 16 to 28
  (canonical / alt); flux level Ec3 HOLDS 60 %, Ec2 HOLDS 45 %; lensing G4 passes for both (65 %); SPARC: none beyond
  R_3 today (the worst sits at 0.47 against 0.535), 80 %.

**What counts against, added.** The search for a surface went: R_zv (frozen), then, after the matter-level numbers, 0.5
and 0.75 R_fold, then these. A hold of Ec2 or Ec3 would therefore be a hit found by looking, from a family of two; it
needs a frozen, blind lane before it means anything. Behind the fold FLD1's shell equation is not exact and the action
gives no answer (COL1): R_2 and R_3 come from FLD1's reflecting-centre device, as R_fold itself does.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
