# CK1 amendment A2 (criteria f6f15f9e05 + A1 ecde71eaff), committed before any graded CK1 number

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

**KA4 reference corrected.** The criteria quoted NA2's baryon-traced X-COP line "-0.0017 / 0.0818 and -0.0017 / 0.0835"
as the value at KD1's need F = 4.1786 / 3.7833. Those means are NA2's at its own fitted F (4.206 / 3.811). At KD1's
need the uniform (baryon-traced) amount zeroes the X-COP mean by construction (that is how KD1 defined the need). The
first MUTATE launch stopped at KA (nothing graded) with mean +7e-17 / +1.3e-16 and rms 0.08181 / 0.08351: the rms
matches NA2's line and the mean is 0. KA4 now reads: mean 0 and rms 0.0818 / 0.0835, each to 1e-3.

**KA5 implementation fix (no criteria change).** The same stopped launch showed RM's v_k = 0 branch returning
C_f M_b interpolated through its internal log grid (max relative error 2.5e-3 against the 1e-6 line). The v_k = 0 branch
now evaluates the baryon profile at the requested radii directly. Nothing else in the script changed.

Kappa = 1/2 FITTED; not theory closed.
