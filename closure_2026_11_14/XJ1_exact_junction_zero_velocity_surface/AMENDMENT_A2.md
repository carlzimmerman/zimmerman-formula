# XJ1 AMENDMENT A2 (2026-11-14, written 11:01 EST by the clock): rotation curves under the record's junction, added after the s table was read

Post hoc: written after the two reported chains of section 7 were run and read (matter level; lensing G4 and the s
table), and before any flux-level number of this lane has been read (build B is still running; no part has been
opened except the first, for the identity of its R and J5 fields with FWN1R's stored part). It adds one reported item
to section 7. It changes no case, gate, known answer, twin, bracket or label rule of the flux-level run.

**What was seen.** The s table (`xj1_lens.out`): at z = 0 under FZS1's junction the law's halo inside R_set is
multiplied by s = 0.47 to 0.93 at f = 1.25, 0.57 to 0.78 at f = 2, 0.69 to 0.72 at f = 3 and 0.56 to 0.79 at R_zv for
log M_b 8 to 10.45 (canonical; alt 0.47 to 0.84, 0.57 to 0.70, 0.68 to 0.72, 0.56 to 0.72); it passes 1 near log M_b
10.7 to 11.2. The scorecard's row 1 (SPARC rotation curves) reads EQUALS THE LAW under rule 6 from membership alone
(no galaxy above v*, every last point inside the settled radius). That is exact only where s = 1.

**The added item (reported, not a label of this lane; no row is relabelled here).** PD1's P2-SPARC statistic, its code
copied (QX8's loader and exact-field term, the per-galaxy best mass-to-light ratio on QX8's grid, the pooled weighted
rms and mean, all 175 galaxies and the massive tail with V_flat >= 250 km/s), with the model inside the settled radius

    g = g_N + s (glaw(g_N) - g_N),

s = FZS1's factor for that galaxy at z = 0 from SRH1's lens `profile` (the same function the s table used) at the
galaxy's M_b (PD1's: the largest enclosed baryon mass at mass-to-light 0.5), for f = 1.25, 2, 3 and R_zv, both
footings. PD1's gate (SS1 G5) is quoted beside each number: rms <= L0 + 0.010 and |mean| <= 0.05, for all galaxies and
for the massive tail, L0 the law's own value (0.05605 / 0.05583; massive 0.03751 / 0.03260).

- Known answer (or nothing is quoted): s = 1 for every galaxy reproduces PD1's stored L0 (all and massive, rms and
  mean, `pd1.json`) to 1e-9.
- Containment: every galaxy's last measured radius lies inside R_fold(z = 0; M_b) (FLD1 found 175 of 175); if any does
  not, it is named and its outer points keep the law (this favours the junction).
- The exact junction equals the law at every SPARC radius by construction (s = 1 inside R_set), so its SPARC numbers are
  L0; stated, not recomputed.
- Limits stated now: the mass-to-light ratio is free per galaxy on QX8's grid (0.30 to 1.20), so a heavier disc can
  absorb part of a lighter halo; the fitted median mass-to-light ratio is reported beside each case. s is the lens
  chain's (a point baryon mass, the galaxy-regime reference with share X), applied to an extended galaxy as one
  number per galaxy.

**A correction to the headers of this lane's frozen files.** FROZEN_CRITERIA.md says "written about 11:40 EST" and
AMENDMENT_A1.md says "about 12:10 EST". Both times were guesses and are wrong. The commit times are the record:
criteria ef8ccdde98 was committed at 10:40 EST and amendment 38c6539631 at 10:43 EST. The frozen files are not
edited.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
