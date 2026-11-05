# CT16 frozen criteria: G6 disc depletion for candidate C''

Written before any number of this lane was computed. Under owner decision D1 and its follow-up ("Yes, grade it"): grading only, nothing adopted, the 2026-11-01 retirement stands, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Not blind: the order of the planar fold time was estimated by hand while reading X14 before this file was written.

## The candidate's dust phase
C'' (CT10, reviewed CT13) = v3s + canonical phi with a0^2 = kappa^2 G (2XP_X - P). Its dust phase is v3s's khronon charge rho_tau, weight alpha = 1 fixed by kinematics (V3_FULL_PICTURE.md section 4.1). Locally C'' shifts a0 by at most 1e-10 dex (CT13), so inside a galaxy the dust obeys v3s's PN system unchanged (V3_FULL_PICTURE.md section 2): hold equation, Poisson with rho_b + rho_tau, D v_tau/Dt = -grad phi + grad Xi. C'' contains no caustic completion (no beta K^2 term; CT10 hand-set list). The dust amount is a fitted initial condition (follow-up).

## The requirement (restated from the record)
MC1 (rebuild_2026_10_22/MC1_minimal_cold_requirement/mc1.out:58, reading N, measured response f_Q 0.872, Upsilon 0.5, canonical): psi, the largest share of the native cold profile (EM1 mass) a disc can hold, is 0.200 at V_flat 150-200 and 0.328 at 200-250 km/s; alt (mc1.out:165) 0.22 and 0.27 (README.md:50). Depletion D = 1 - M_x(<R_last)/M_x,native(<R_last), with M_x the dust mass in excess of what the law already supplies.

Pass line (frozen): D >= 0.80 (150-200) and D >= 0.67 (200-250) canonical; D >= 0.78 and D >= 0.73 alt. Both footings, never pooled. A Milky Way-like disc sits in the 200-250 bin; a G6 pass needs both bins.

## Precondition P0 (decides whether any run can grade G6)
G6 asks for D as an OUTPUT of C''s field equations at z = 0. That needs the dust solution to exist to z = 0 in the disc region. X14 (F2, exact before first crossing, rebuild_2026_10_22/X14_caustic_completion/README.md:75-80): a zero-charge khronon stream crossing a sheet of surface density Sigma_b folds at tau_f = w/(K Sigma_b), K = 4 pi G; a charged (held, rho_tau0 > 0) element folds iff omega_p tau_f <= 1/sqrt(2), omega_p^2 = K rho_tau0 (M_L - 1), M_L = (1+x)^2, otherwise it phase-mixes to crossing (F3); soft elements always fold.

P0 computation (seconds, one thread): tau_f over Sigma_b 10-100 Msun/pc^2 (outer to inner Milky Way disc) and crossing speed w 20-400 km/s; omega_p tau_f for held elements at x = g/a0 0.5-10 and rho_tau0 equal to the law's phantom density bracket 1e-3 to 1e-1 Msun/pc^3.
- P0 FAIL (G6 NOT DECIDABLE in C'') if max tau_f over the frozen range is below 1 Gyr (disc age >= 8 Gyr): every stream that reaches the disc folds well before z = 0, so the z = 0 depletion is not defined by C''s equations. No grid removes a fold (density diverges at finite time; resolution only moves its time, AN1 K10).
- P0 PASS if tau_f exceeds 8 Gyr over the whole range; then the run below is built.

## The run that would decide G6 (built only if P0 passes, or for a completed candidate)
Axisymmetric (R, z), justified because the requirement is an azimuthal average of an axisymmetric disc; it drops non-axisymmetric streams and wakes (X10), stated as a limitation. Lagrangian khronon elements plus the nonlinear Gauss law and Poisson (X8's solver class), baryonic exponential disc grown on a frozen schedule, fitted dust amount, from z = 20. Convergence: N and 2N per axis and dt/2; D must move by < 0.03. Read D in 150-250 km/s cells against the pass line above.

## Resource rules
One thread, < 1 GB RSS, checkpoint on SIGTERM for anything over 10 minutes, about 2 h budget. Do not touch the running khronon_fluid.py session or its directory. Commit nothing.
