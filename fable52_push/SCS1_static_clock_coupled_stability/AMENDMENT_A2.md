# SCS1 AMENDMENT A2 (post hoc; committed alone, before the final route-2 run)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.

**What changes.** Route 2 treats an eigenvalue with |lambda| <= 1e-12 x max|lambda| (of the same solve) as zero, the
rounding level of the dense generalized eigensolver. It counts as negative only below -1e-12 x max|lambda|, and as complex
only with |Im lambda| above the same bound. The raw counts are kept beside the thresholded ones in the output. The bound is
far below the physical spectrum: on the primary grid the smallest physical eigenvalue is 2e-9 to 2e-8 of the largest.
Nothing else changes: no line, grid, known answer, MUTATE arm or label rule.

**What was seen first (post hoc).** The first route-2 run of the primary configuration labelled one canonical row
UNDECIDED. Its smallest eigenvalue at N = 800 was -3.1e-20 kpc^-2, which is 6e-15 of that solve's largest eigenvalue and
five decades below the smallest value of the local WKB band (1.3e-16 to 4.2e-15 kpc^-2). A direct check at N = 400 found
every eigenvalue of all 12 (mass, l) rows positive and inside the band. The same run's local-form check and KA4 gave no
negative eigenvalue. That first output is kept as scs1_radial_run1_partial.out.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
