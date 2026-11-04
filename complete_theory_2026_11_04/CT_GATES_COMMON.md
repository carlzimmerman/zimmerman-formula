# Common rules for the CT grading lanes (CT5 onward), after owner decision D1

Read first: README.md, OWNER_DECISION_2026-11-04_D1.md, CT0_ROADMAP.md, and the CT1 to CT4 reports in this folder (they hold the frozen numbers and the record tables). This is a go to GRADE, not to adopt: never write that anything is adopted, that the cold sector is reinstated, or "theory closed"; never say data favour the framework. kappa = 1/2 FITTED.

Gates (fastest death first; numbers from the CT reports, restate them in your frozen file before computing):
- G0 health: count degrees of freedom; no ghost or gradient instability on FRW and static backgrounds; W4b status (CT2).
- G1 weak field: the static, quasi-spherical limit reproduces g_obs = (g_b + sqrt(g_b^2 + 4 g_b a0))/2 within 0.01 dex over 1e-12 < g_b < 1e-8 m/s^2.
- G2 local constancy: a0 varies by at most 0.015 dex between void, field and cluster environments (CT1 gate 2).
- G3 tie: d ln a0 / d ln rho_DE = 0.5 +- 0.01, and a0(z) tracks sqrt(rho_DE(z)) within 0.05 dex at z 1, 1.5, 2.33 in an evolving background; state what fixes kappa and whether it is derived.
- G4 local gravity: Cassini Q2 below the Park line on both conventions for the Galactic field, planets, PPN, |c_T - 1| inside [-3e-15, 7e-16] (CT2 numbers).
- G5 CMB: raw Planck TT H3/H2 = 0.979 +- 0.010 with omega_x/omega_b 4.9 to 5.4 coming from the theory, not fitted (CT3).
- G6 disc depletion: discs 66 to 82 % empty of the dust phase (CT3, requirement 4).
- G7 lensing and clusters as grading rows: KiDS near-lens amplitude, X-COP factor 2.7-2.9, Bullet sign (CT4).

Rules: write FROZEN_CRITERIA.md in your lane dir before any number; a candidate stops at its first failed gate (record it, do not tune around it, no knob scans: derive); count every hand-set constant (L*, kappa, couplings); check the record (grep the repo, git log, STANDING.md) before claiming anything new; never edit astra's files or frozen pre-registrations; no personal names in files; web reading (abs/ar5iv HTML only, never a PDF link) is provisional, no downloads; compute single-threaded, under about 1 GB RSS, checkpoint anything over 10 minutes (another session runs heavy jobs); commit nothing (the parent commits). Report to the parent in under 350 words: gate by gate, with file:line for every number, and the hand-set constants.
