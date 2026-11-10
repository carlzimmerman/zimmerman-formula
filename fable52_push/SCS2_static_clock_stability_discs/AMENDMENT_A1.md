# SCS2 AMENDMENT A1 (committed alone; NOT post hoc: before any script, Lean file or number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.** For backgrounds with an external field, route 2's domain crop is r <= max(30 R_d, 3 r_e), with
r_e = sqrt(G M a0)/g_e. For isolated backgrounds it stays at 30 R_d. Route 1's frozen points and the D.P maps already use the
whole solver domain.

**Why.** With an external field the expected negative-D.P region lies near the null of the total field, at a distance of
order r_e from the disc: 1.5 to 7 r_M for 0.1 a0, and 15 to 70 r_M for 0.01 a0. That is outside 30 R_d for every mass, so
the frozen crop would have kept the region out of route 2's eigenproblem. I noticed this while planning the solver, before
writing any code.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
