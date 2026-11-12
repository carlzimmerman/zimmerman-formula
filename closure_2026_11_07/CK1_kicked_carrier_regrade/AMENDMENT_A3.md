# CK1 amendment A3 (criteria f6f15f9e05 + A1 ecde71eaff + A2 17dbf6d9e8): POST-FREEZE, committed before the rerun

Adopts nothing. Kappa = 1/2 FITTED; not theory closed. The carrier is the "cold dark energy" carrier (kicked carrier),
never cold dark matter.

## Why this is post-freeze, and what already exists

The coordinator relayed the paper session's sourcing (origin f68fe972ee; disclosures D1-D7 in RESOLUTION and
FRAMEWORK_CANDIDATE, commit 996d194c85) after CK1's first full run had finished. Graded numbers therefore exist:
`ck1_FIRSTRUN_preA3.out` (committed with the RESULT, unedited). First-run label: "FAILS (rows) at every v_k; binding
gate T (fails both footings at 7 of 7 kicks)", with G1, T, G5, G6 FAIL at every kick on both footings, MW FAIL at
500-550, G2 / G3 on the L388 path NO VERDICT at 500-550 and FAIL at 600-650 (canonical). The first run also had a bug,
found while preparing this amendment: the Milky Way evaluation grid was not sorted, so every number interpolated on it
(rho_c(R0), Delta K_z, Delta v_c(R0), the dSph host densities, the carrier inside 9.58 AU) is wrong in the first run;
the inner-30-kpc Delta log g used the sorted part and is unaffected. Fixed now (sorted grid). The rerun replaces
ck1.json / ck1.out; nothing else in the frozen gates, lines or cell rules changes except as listed.

## Changes (each from the coordinator's D1-D7 relay)

1. **L388 is not evidence and not a KA.** Its eps is a ratio to a LCDM run (CLASS omega_cdm 0.12 boxes). X-COP and
   groups are now graded from CK1's own resolution run, the RM of criteria section 4, applied to each X-COP cluster's
   own baryon profile (QX7 iter_5) at the X-COP radii and to each Lovisari group's two-point gas profile (both f*),
   with the same 4 bracket cells and cell rule. RM is framework-native: the law at today's footings, KD1's own-terms
   capture, on-disk baryons, one phantom setting (the law's). The reference is named in the JSON. b = 1 + M_c(<r)/M_b
   at each graded point. L388's amounts are kept only as a labelled reading ("LCDM-referenced, not evidence").
   KA1/KA2 become code checks of L388's machinery on its own inputs (disclosed as such), not known answers about the
   carrier. A1's bracket rule for 500-550 no longer applies to graded rows (RM runs every kick directly).
2. **Footings.** Every graded number uses today's footings (a0 9.360324825e-11 / 1.131203541e-10 m/s^2, Lstar 21.7 /
   22.9 pc, as loaded from GB1/QX7). L388's old canonical-only footing enters only the reading.
3. **Radii and phantom.** X-COP is measured at its own points and at 0.25 / 0.7 R500 (profile vs NA2's band:
   concentration M(<0.25 R500)/M(<0.7 R500) of the RM carrier against gas, HSE and stars per cluster), on the law only.
4. **Bullet: OPEN.** DB1's Bullet machinery peaks at 1.19 GB (NA2 disclosure 1), above this lane's 1 GB line, so it is
   not run. L370's "0.000" was its kernel-off MUTATE; the main run reads +0.001 to +0.072 with the carrier intact.
5. **"Cosmic 5.4" is not used.** The native numbers are QX12's R = omega_d/omega_b = 5.562 and QX15's omega_d 0.1209
   (KD1's footing fit). CK1's amount is KD1's capture C_f = f_cap x omega_d/omega_b = 4.1110 / 4.1121 (kd1.json),
   unchanged. The criteria's 5.40 reading is dropped.
6. **Label ceiling.** v_k is hand-set and CK2 found no release term, so the strongest label is "CANDIDATE ON G1-G8
   WITH A POSTULATED KICK (G9 pending GL1/GL3)".
7. **MUTATE M1/M2 moved to the graded (RM) path.** M1: RM at v_k = 0 gives F = C_f at every X-COP point (KD1's
   capture, within 5 % of 4.111); L388's v_k = 0 runs reported only. M2: v_k = 2000 km/s is run and reported; in the
   law's field the clusters' escape speeds are several thousand km/s (the first MUTATE run's reading: 4800-6300 km/s
   at r_F), so 2000 km/s need not empty X-COP and that is reported as physics, not as a bite. The bite is a kick
   above every cluster's escape speed, v_k = 20000 km/s: it must leave f_ret <= 0.1 in every cluster and fail G2 on
   both footings. M3 unchanged.

Kappa = 1/2 FITTED; not theory closed.
