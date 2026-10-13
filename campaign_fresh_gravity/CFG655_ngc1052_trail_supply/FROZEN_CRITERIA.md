# CFG655 FROZEN CRITERIA: the NGC 1052 trail (DF2, DF4, DF9) and LEDA 4014647 ("Rogue One") as a cold-energy supply test

Committed ALONE, before the script exists and before any prediction is compared with a measured dispersion.

## Honest status of blinding (read first)

- The measured dispersions were read from the abstracts while collecting data (unavoidable: they are in the abstracts).
  No prediction had been computed for DF9 or LEDA 4014647 in this record. DF2 and DF4 were scored once before
  (CFG7 FG001 H6, 2026-09-27: class E "collision debris such as NGC 1052-DF2/DF4" -> Newtonian, PASS at 20 Mpc; the law
  with EFE 2.95 / 3.12 sigma for DF2). CFG58 scored a "blind" version of a different rule (stellar-mass only) that fails
  DF2/DF4 (-3.28 / -1.51). So DF2/DF4 are NOT out-of-sample; DF9 (Keim+2026, 2603.15860) and LEDA 4014647 (Vaz+2026,
  2610.07467) are new to the record.
- The formation-channel label used below was assigned in the literature BEFORE either new dispersion existed:
  van Dokkum+2022 (2205.08552, Nature; read verbatim from the ar5iv HTML) list the 11 trail galaxies by a Hough
  transform, "highlight DF9 ... a galaxy with a bright star cluster that falls on the trail", and state "LEDA4014647 is a
  candidate for an interloper (that is, an unrelated group member) given its brightness and relative compactness."
  That 2022 label came from photometry and position, not from kinematics. It was, however, made by authors whose trail
  hypothesis was motivated by DF2/DF4's low dispersions.

## The framework rule (declared; Theory v2 A5-A8, Theory v1 R1/R7, G9; FG001 class E)

Only real mass gravitates (G9): the law's extra pull is settled cold energy (R1), settled only from the system's own
supply (A6), around its condensed baryons (A5), with no external-field effect (R7/A8). Therefore:

- **Class E (supply ~ 0):** a galaxy whose stars formed from gas that had separated from its cold energy (bullet-dwarf
  collision debris) holds no cold energy -> **sigma_Newton** (baryons only).
- **Class T/A (own supply):** a galaxy that formed normally (an interloper or a progenitor remnant that kept its
  collisionless cold energy) -> **sigma_law** on its present condensed baryons, no EFE (A5: the settled amount is the law
  target M_ph = (nu-1) M_d; a progenitor remnant could hold an unsettled surplus, reported as an upper bracket only).

### Rule P (PRIMARY, the verdict): labels from the pre-kinematic 2022 classification
| galaxy | label | reason (vD+22, verbatim source above) |
|---|---|---|
| NGC 1052-DF2 | E | trail member, DM-free candidate |
| NGC 1052-DF4 | E | trail member, DM-free candidate |
| NGC 1052-DF9 | E | "falls on the trail" (highlighted) |
| LEDA 4014647 | T | "candidate for an interloper" (brightness, compactness) |

### Alternative rules (REPORTED, not the verdict; they show how much the result rests on the label)
- **Rule M (membership only):** every galaxy on the vD+22 trail list is E (LEDA 4014647 is on the list) -> all four Newtonian.
- **Rule A (age only):** E iff the homogeneous SED mass-weighted age (Tang+2025b, 2410.19331 Table 2) is not older than the
  collision epoch (vD+22: "around eight billion years ago"): P(t_M > 8 Gyr) < 0.5 -> E, else T (two-sided Gaussian on the
  quoted asymmetric errors).
- If a rule cannot assign a galaxy (P within 0.4-0.6), that galaxy is AMBIGUOUS under that rule and is scored both ways.

## Inputs (frozen; sources and verbatim status in the README data table)

| galaxy | M_* (Msun) at D_ref | R_e,circ (kpc) at D_ref | D_ref (Mpc) | sigma (km/s), primary | M_* error |
|---|---|---|---|---|---|
| DF2 | 2.0e8 (2 x 1.0e8 within r_1/2) | 2.0 | 20 | 8.5 +2.3/-3.1 (Danieli+19 KCWI stars) | 20% |
| DF4 | 1.5e8 (2 x 7.5e7 within r_1/2) | 1.6 | 20 | 6.3 +2.5/-1.6 (Shen+23 fiducial stars+GCs) | 27% |
| DF9 | 1.4e8 | 1.1 | 20.6 | 6.5 +3.9/-4.3 (Keim+26 KCWI) | 23% |
| LEDA 4014647 | 10^7.98 | 0.601 | 17.7 | 15.8 +/- 2.0 (Vaz+26 KCWI) | 0.06 dex |

Gas: none (all four are gas-poor early-type dwarfs; M_b = M_*). Secondary dispersions (reported, not verdict): DF2
Emsellem+19 stars 10.8 +3.2/-4.0, DF2 GC system (arXiv 2503.03404) 8.63 +2.88/-2.14 and 14.86 +3.89/-2.83; DF4 stars 8.0 +2.3/-1.9,
DF4 GCs 4.2 +4.4/-2.2.

## Estimator (declared; the record's CFG7 sigma_pred/sigma_newt form)

r_1/2 = (4/3) R_e,circ; M_b(<r_1/2) = M_b/2; g_N = G M_b(<r_1/2)/r_1/2^2; g = nu_mono(g_N/a0) g_N (the record's XC4 repaired
kernel, nu_RAR to y* then monotone log splice); sigma^2 = g r_1/2 / 3 (Wolf-type, isotropy-insensitive at r_1/2).
sigma_Newton: nu = 1. Both footings a0 = 9.3603e-11 and 1.1312e-10 m/s^2, never pooled. Prediction error from the M_*
error only (sigma_N ~ M^1/2; the law uses the propagated nu). Distance scaling: M_* ~ D^2, R_e ~ D.

**Z = (sigma_obs - sigma_pred) / sqrt(e_obs^2 + e_pred^2)**, e_obs = the upper error if sigma_pred > sigma_obs, else the lower.

## Distances

Primary: DF2 20 Mpc (reference) with the verdict REQUIRED to hold at both TRGB values 17.6 (JWST, Tang+2026 2606.05144) and
21.7 (HST, as quoted in Tang+2026); DF4 20.0; DF9 20.6; LEDA 17.7. Reported bracket: every galaxy at 13 and at 20 Mpc; DF2
also at 16.2 (GC internal-sigma distance, arXiv 2503.03403).

## Class rules (the verdict, per footing; the lane verdict needs both footings)

- **PASS:** under Rule P every galaxy |Z| <= 2, AND sigma_law fails DF2 and DF4 at |Z| >= 3 (the test discriminates), AND
  the same holds with DF2 at 17.6 and at 21.7 Mpc.
- **NOT DIAGNOSTIC:** Rule P all |Z| <= 2 but sigma_law is within 3 sigma for DF2 or DF4.
- **TENSION:** Rule P max |Z| in (2, 3].
- **FAIL:** Rule P any |Z| > 3.
- **Qualifier (mandatory in any verdict line):** the framework does NOT derive the formation channel; the label is
  an external, pre-kinematic astrophysical classification. If PASS, the verdict reads "PASS CONDITIONAL ON THE
  FORMATION-CHANNEL LABEL". If the label is replaced by any rule from framework-internal observables and the result
  changes, report it.

## Reported (not verdict)

- R1 Rule M and Rule A outcomes (counts within 2 sigma; AMBIGUOUS galaxies).
- R2 Partial supply (Theory v2 eq. 2-3, CFG634 static form): for an E galaxy with supply fraction f_s of the law target,
  sigma^2 = sigma_N^2 [1 + f_s (nu - 1)]; report the largest f_s allowed at Z = +2 (upper measured bound).
- R3 LEDA 4014647 progenitor-remnant bracket: a remnant may hold unsettled cold energy beyond the target; the law value is
  then a floor. Reported qualitatively plus the measured Mdyn/M_* vs nu.
- R4 Secondary dispersions scored under Rule P.
- R5 Context only (never a verdict): the bullet-dwarf scenario (gas separates from collisionless dark matter) and tidal
  stripping. The framework's account here is structurally the same as the bullet-dwarf account with cold energy as the
  collisionless component; it is distinct from a no-EFE modified-gravity law (sigma_law), not from the dark-matter account.

## MUTATE (must be reported)

- M1: all 16 E/T label assignments over the four galaxies are scored at primary distances; N_pass = number passing every
  galaxy at |Z| <= 2 on both footings. The rule's success is SPECIFIC iff N_pass <= 2 (chance <= 1/8). The random-label
  pass rate N_pass/16 is reported.
- M2: MUTATE=1 run cyclically shifts Rule P's labels (DF2<-LEDA's, etc.); the headline must FAIL (exit 1).
- Distance bracket (13 vs 20 Mpc) reported for every model.

## Compute

One process, < 100 MB, nice -n 10, seconds. No data download (all inputs from abstracts / arXiv HTML).

kappa = 1/2 fitted; cold energy mass required; not theory closed.
