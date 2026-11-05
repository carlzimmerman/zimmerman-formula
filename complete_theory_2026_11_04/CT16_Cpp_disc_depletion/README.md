# CT16: G6 disc depletion for C''. NOT DECIDABLE in C'' (P0 FAIL): the khronon dust folds at the disc within 4-724 Myr, so C''s equations give no z = 0 depletion. Not a resource limit. G6 NOT PASSED; no D computed

Criteria `FROZEN_CRITERIA.md` (written first). Script `ct16_p0_fold.py` -> `ct16_p0_fold.out`, `ct16_p0_fold.json` (seconds, one thread, 39 MB RSS). Graded under D1's follow-up ("Yes, grade it"): grading only, nothing adopted, the 2026-11-01 retirement stands, no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework.

## Step 1: what AN1/AN2 established
- AN1 v3 (`rebuild_2026_10_22/AN1_aest_nonlinear_dust/README_V3.md`): spherical, baryons stopped by hand, no disc. 61 of 68 rows fold first, 5 never collapse, 2 oscillate; none settles. At z = 0 the field holds at most about 3 % of the law's phantom mass. A static branch exists at mu 0.1 and holds against a 1 % kick, but collapse never reaches it. NO VERDICT because K11 (single-shell runaway) missed, and a fold ends every row.
- AN2 (`AN2_aest_3d_fold/README.md`): 3D, 128^3, no disc. Five frozen checks miss and KG misses. Diagnostic SL puts the sphere lag down to grid resolution (15.6 % at 128^3); about N 440 per side is needed for 3 %, and RSS was 1.6-2.3 GB. Its rows only measure fold times.
- Neither one had a baryonic disc, so neither measured depletion.

## Step 2: reduction and P0
- The disc is a sheet. X14's exact planar result (F2) applies: tau_f = w/(4 pi G Sigma_b).
- Over Sigma_b 10-100 Msun/pc^2 and w 20-400 km/s, tau_f runs 3.6-724 Myr (out:6), against a disc age of 8 Gyr or more.
- Held, charged elements fold by F2 in 10 of 81 cells (out:17). The rest oscillate with periods of 7.6-748 Myr (out:8-16) and phase-mix to crossing (X14 F3).
- C'' has no caustic completion, so its equations have no continuation past the fold. The P0 line is breached (out:18). No grid fixes this: resolution only moves the fold time.

## The deciding run (needs a new constant)
- It needs C'' + beta K^2 (X14 C1, beta 2.0e-6 to 1.0e-5 at mu_K 0.1), which is a different candidate.
- Axisymmetric (R, z), stretched grid of about 512 x 1024 with dz 75 pc, X8-class solver, a frozen disc-growth schedule and a fitted dust amount.
- Cost: dt of about 0.09 Myr gives about 1.5e5 steps; at roughly 1 s per step that is about 40-80 CPU h. The convergence pair (2N, dt/2) adds about 8x more. RSS is about 0.2-0.5 GB.
- That is far over the 2 h budget, and it is not run.

## Cross-gate note (record read)
At the mu_K galaxies allow, v3s's khronon is radiation-like until z 35-78 (V3_FULL_PICTURE.md:108-109). The CMB needs dust by z 3e4 or earlier (V3S_FINAL_VERDICT:492). So G5's fitted-amount pass assumes a dust that this dust phase is not.

## Hand-set constants
kappa^2 (= xi), V0, V's shape, phi_i, L*, mu_K, the dust amount (fitted). P0 adds none. Its Sigma_b, w and rho_tau0 ranges are frozen brackets, not fits.

kappa = 1/2 FITTED; not theory closed.
