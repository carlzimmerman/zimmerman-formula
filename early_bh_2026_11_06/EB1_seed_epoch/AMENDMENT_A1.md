# EB1 Amendment A1 (before the main run; only the check runs have been done)

Check run (script 0f55942e3a): K1 1.68652 PASS, K3 PASS, K4 PASS, K2 "PASS" but vacuous: on
the frozen K2 cell (B2, M 1e9, nu 3) neither R0 nor R1(a0 -> 1e-30) collapses by z 0, so there was no z_coll to compare.
That result is itself the first physics number seen: a 3 sigma 1e9 Msun baryon clump does not collapse by z 0 under
Newton from the baryons-only start. No R1 number has been seen.

K3 is not vacuous: CLASS's grid reaches 347 / 692 Mpc^-1 at k_max 300 / 600, and d_b is Silk-damped to ~1e-4 of its
peak by k ~ 1 Mpc^-1, so sigma_b(1e6) is converged; it equals sigma at the Silk scale.

**A1 (K2 restated, same intent).** K2 compares the shell's final state at a = 1 (r_end / r_0) between R0 and
R1 with a0 = 1e-30 on the frozen cell; it passes if they agree to 1e-6 relative, or if both collapse and z_coll
agrees to 1e-3. Nothing else changes.
