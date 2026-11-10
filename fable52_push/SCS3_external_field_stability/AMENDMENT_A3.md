# SCS3 AMENDMENT A3 (post hoc, after A2's solver fallback failed on a test matrix; committed alone, before any PL R2 number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.** A2 item 2's fallback solver (CG preconditioned by an incomplete LU) is replaced by the **same direct sparse
LU as frozen, with the MMD_AT_PLUS_A column ordering instead of the default COLAMD**. The LU is exact; only the fill-reducing
permutation changes. It is used for PL R2 only, one PL R2 process at a time, killed at 7 GB RSS (reported). The graded
solver-swap check of A2 stays, with the MMD solver in place of CG: re-solving PL R1 for canonical expo 9.4 at 0.1 a0 and
canonical Kuzmin 10.9 at 0.01 a0, Gamma_L^2 (A2 reading) and min D.P must equal the COLAMD solve's to 1e-3. Everything else
in A2 (the polar-row exclusion, the three-grid rule for PL with R0-R2) is unchanged.

**Why, and what was seen first (post hoc).**
- The frozen probe: one PL R2 solve (canonical expo 9.4, 0.1 a0) by the frozen direct solver passed 4 GB RSS and was killed at
  5.97 GB. So A2's fallback applies.
- A2's fallback does not work. On the R1 matrix of the first Picard step (61,632 unknowns), CG with SuperLU's incomplete LU
  (drop tolerance 1e-5 / fill 10 in the swap check; then 1e-6 / 20, 1e-7 / 30, 1e-8 / 50) did not reach 1e-11 in 5,000 to
  20,000 iterations; the residual grew. SuperLU's incomplete factor is not symmetric, so CG's assumption fails. No result
  of the swap check exists (it stopped at its first solve).
- The same R1 matrix's exact LU has 26.3 M nonzeros with MMD_AT_PLUS_A and 57.8 M with COLAMD. At R2 (208,656 unknowns) the
  MMD factor has 178.5 M nonzeros, built in 14.6 s at 5.3 GB RSS. The 4 GB line was mine; at the time of writing the machine
  had about 28 GB free or inactive memory (swap 5 GB used), so one 5-6 GB process leaves room for the other lanes, which is
  the brief's condition. No PL R2 background has been solved.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
