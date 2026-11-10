# KL1 PART C FROZEN CRITERIA: the remaining Legacy gap: the box's random draw, gas from a stellar-mass-selected stack, the cold component's response, and (against form B) the alignment

Committed alone, before any Part C script exists and before any Part C number is computed. TEST lane; relabels nothing, adopts
nothing, not registered. **kappa = 1/2 FITTED; not theory closed.** Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2),
graded separately, never pooled. Cold dark energy is a gravitating field component, never a particle. Nothing in Parts A or B
is relabelled. No download: everything used is on disk (CFG596's, CFG411's and CFG424's S0 runs; GH10 / GH11's published DESI
DR2 x ACT DR6 kSZ numbers; RB1's ladder; the KiDS-Legacy release fetched for Part B). The folders `_kl1_rerun_tmp/` and
`KL1R_blind_legacy_regrade/` are other sessions' and are not touched. Part A / B scripts are not edited; Part C has its own files.

## 1. Why

The owner (relayed by the closure chat, 2026-11-10) asked to attack the remaining gap at Part B's BALL: Legacy prefers sigma8
0.788 / 0.786 +- 0.012 against form B's neutrino-floor 0.812, 2.13 / 2.30 Legacy widths. DES Y3 at Part A's ALL:
2.83 / 3.02 DES widths. Three things a survey or we assumed that the record can measure or compute were not in the graded rows
(C0 to C2), and one goes against form B (C3).

## 2. Base

Base = Part B's BALL on Legacy and Part A's ALL on DES Y3 and KiDS-1000. That is A1's target sigma8 (0.8121 / 0.8120), A2's
covariance at the model (gamma 2, A2's fiducial and area per survey), A3's gas (RB1's ladder, edge r_ta), and Part A / B's support
cut, nuisances and scan rule.

## 3. The pieces

**C0. The box's known random draw.** CO2's post hoc corrections enter the graded rows. They are copied from `co2_posthoc.py`, apply
to the S0 nodes before the amplitude move, and leave the response unchanged.
- **Primary: R1.** Divide by the run's own starting ratio r(k) = P(z_i) / (D_i^2 P_lin), with weight 1 for k <= 0.3 falling
  linearly in ln k to 0 at k 1.
- **Edges:** R1b (1 to k 0.2, 0 at 0.5); R2 (CFG411's L200 run below k 0.5); R2b (CFG424's, seed 360).
- A2's covariance at the model is recomputed from the corrected spectrum. The fiducial stays A2's.

**C1. Gas where a stellar-mass-selected stack measures it.**
- *Input.* The stack is GH10 / GH11's published DESI DR2 x ACT DR6 kSZ bin, CIGALE log M_star 10.5 to 11, corrected to
  log M_star 10.971. The primary amplitude is GH11's realistic-miscentring A(1.8) = 0.54 +- 0.13; the edge is GH10's 0.45 +- 0.11
  with no miscentring.
  - Zhang's gas profile at that mass (beta 0.43, r_c 6 kpc, 1.84 M_star inside R_vir = 285 kpc from GH7's table, cut at 1.8 R_vir)
    holds M_Z = 4.9e11 Msun inside R_m = 1.8 x 285 kpc = 513 kpc (GH11's number).
  - Measured baryons inside R_m: M_b = M_star + A x M_Z (the central's stars; satellites' baryons not counted).
- *Caveats carried.* Satellite fraction 0.28 (the paper, via a summariser; GH11's miscentring model is the primary). Two-halo
  signal is unsubtracted and adds signal, so the true central gas could be lower. The points inherit the paper's velocity
  reconstruction (r_fid 0.64, sigma_true 300 km/s).
- *Fig. 8 of the paper (kSZ over CMB lensing)* divides by an HOD-emulator fit to the lensing. That is model-calibrated machinery,
  so it is quoted as context only, never in a row.
- *The conversion and its choice.* f_kSZ = M_b / (f_b x M_tot(<R_m)), with f_b the halo model's om_b / (om_b + om_c) and M_tot
  from an NFW halo with the halo model's concentration. Two frozen ways to get the halo:
  - (a) the layout's own stellar-to-halo relation (CFG556's `mstar`, inverted at M_star = 10^10.971);
  - (b) Zhang's own R_vir read as R200c = 285 kpc.
  - Error sigma_f is propagated from A's error (the larger of the two halo choices).
  - **Decision rule:** if |f_a - f_b| > sigma_f, the conversion is choice-dominated, and **C1 is graded as a BRACKET (both edges
    reported), not a row.** Otherwise C1 is a row at the mean of (a) and (b).
- *Into the layout (both regimes).* For a halo of mass M, the stack's rule acts at R_m(M) = (R_m / R200c of the anchor halo) x
  R200c(M), separately for each choice.
  - The rule: the gas inside R_m is scaled so that stars + gas inside R_m = f x the layout's own baryons inside R_m.
    - Cluster regime: stars and gas inside R200c, plus f_b x the reference mass between R200c and R_m.
    - Galaxy regime: the condensed baryons, kept, plus the uncondensed baryons, which are the removable gas.
  - The removed mass goes between R_m and r_ta with M(<r) rising linearly in r.
  - Mass dependence:
    - f = f_kSZ (capped at 1) from the halo of log M_star 10.0 up to the anchor halo (log M_star 10.971), through the same SHMR
      choice.
    - Between the anchor and log M500 = 13.25 [Msun], the stack's rule acts with f linear in log M500 from f_kSZ to RB1's
      0.674 at 13.25.
    - At and above log M500 13.25, A3's RB1 rule at R500 applies unchanged.
    - Below the log M_star 10.0 halo, nothing changes.
  - The cold component follows C2's edge.

**C2. The cold component's response** (DG1's two edges).
- NR (no response): A3 as graded.
- **AD (slow loss): every cold shell keeps r M(<r).** For each shell, r_f [c_i + b_f(r_f)] = r_i [c_i + b_i(r_i)], where c_i is
  the cold mass inside the shell (layout total minus layout baryons) and b_i, b_f are the baryons before and after the move.
  - Shells cannot cross r_ta, because b_f(r_ta) = b_i(r_ta), so M(<r_ta) is conserved.
  - The new M(<r) = c(<r) from the inverted shell map + b_f(r).
- **Graded edge: AD**, the physical response of collisionless mass to slow loss. NR is the other edge, reported.
- AD applies to whatever gas move the row carries (A3's, or C1's if C1 is a row).

**C3, against form B: the alignment held to Legacy's own model.**
- The model: a mass-dependent NLA, per-bin A_i = a x f_r,i x 10^(beta (log M_i - 13.5)). f_r,i comes from `KiDS_Legacy_values.ini`
  (0.158, 0.198, 0.206, 0.258, 0.207, 0.026). (a, beta, log M_1..6) have a correlated Gaussian prior: decorrelated parameters
  with unit widths about the `KiDS_Legacy_priors.ini` means, mapped linearly.
- That map's matrix is not on disk (CosmoPipe), so it is solved from the release's own chain, which records both the
  decorrelated and the physical parameters for every sample. Known answer: the solved map reproduces every chain sample to 1e-6.
- Per-bin amplitudes enter through a KL1 copy of CFG592's C_ell. Known answer: equal A_i return CFG592's C_ell to 1e-12.
- Rows on Legacy, on the gate's settings:
  - **C3b (graded for the label rule below):** the 8 alignment parameters free under Legacy's own prior, with their decorrelated
    unit-width priors added to the chi^2 as for delta-z.
  - C3a (reported): held at the prior mean.
  - C3c (reported, context only, a survey posterior): held at the chain's posterior mean.

**Legacy's own fiducial statistic** (COSEBIs, 2 to 300 arcmin, n <= 6; band powers) is **not graded in this lane.** The COSEBI
filters' roots and norms are not on disk. Recomputing them is new code whose normalisation convention I would have to recover from
the very published E_n it should be validated against. Band powers need the release's apodised filters, which are also not on disk.

## 4. Known answers (before any graded number; a failed KA makes the rows that use it NO VERDICT)

- **KC1:** C0 off, C1 at RB1's ladder, C2 at NR return Part B's BALL on Legacy (198.33 / 199.49) and Part A's ALL on DES Y3
  (64.62 / 64.70) and KiDS-1000 (135.60 / 136.06), to 0.01.
- **KC2:** C0's R1 / R2 on the A0 settings reproduce CO2's post hoc KiDS-1000 best sigma8 (0.7391 / 0.7373 and 0.7454 / 0.7435)
  to 0.0005.
- **KC3:** the AD response with no gas moved returns the layout to 1e-9; every AD layout conserves M(<r_ta) to 1e-9 and is
  non-decreasing; a point-mass test (cold shell around a central mass that drops by half, r M conserved) is solved to 1e-9.
- **KC4:** the C1 layout with f = 1 returns CO1's / A3's R_tot to 2e-3.
- **KC5:** the C3 map reproduces the chain to 1e-6; equal per-bin A_i reproduce CFG592's C_ell to 1e-12.

## 5. MUTATE (separately named outputs)

- **MC0:** the correction applied the wrong way (S0 x r^w) must move the KiDS-1000 best sigma8 against R1's direction, by at least
  half of R1's move.
- **MC1:** f = 0.2 across the stack's mass range (choice (a)) must move R_tot at k 1 by at least 0.02.
- **MC2:** AD against NR at f_ret = 0.2 (A3's rule, all groups and clusters) must move R_tot at k 1 by at least 0.01.
- **MP5:** sigma8 0.90 on the gate settings must give Legacy p < 0.0027.

## 6. The gate and the labels (two-sided)

**Gate row:** C0 (R1) + C1 (if a row) + C2 (AD) on the base. Per survey (Legacy, DES Y3), per footing: g = (form B's
neutrino-floor sigma8 - the survey's best sigma8) / the survey's width, from the scan with the covariance at each sigma8 (A2's
graded rule), and p at the target. Per survey:
- **CONSISTENT** if |g| <= 2 and p >= 0.05;
- **GAP STAYS** if g > 2;
- **OVERSHOOT** if g < -2 (counts against form B exactly as a gap does);
- **POOR FIT** if |g| <= 2 and p < 0.05.

**Overall, per footing:**
- AMPLITUDE CONSISTENT if both read CONSISTENT;
- otherwise GAP STAYS or OVERSHOOT if either reads so (both named if they differ);
- POOR FIT if that is the worst;
- NO VERDICT if a known answer guarding the gate fails or a MUTATE arm does not bite.

KiDS-1000 is graded the same way and reported beside the label (not the newest release).

**What C3 must do to take the label away (stated before any number):** if C3b, Legacy's own alignment model with its own prior on
the gate's settings, gives Legacy g > 2, g < -2 or p < 0.05, the Legacy reading becomes C3b's and the overall label is re-read with
it. C3a and C3c are reported and cannot change the label alone. If C3b leaves Legacy CONSISTENT, the label stands.

**If C1 is a bracket:** the gate is C0 + C2 (on A3's gas). The C1 edges are reported with their own gate reading on top, labelled
BRACKET, and cannot set the label.

Edges reported beside the gate: C0's R1b / R2 / R2b; C2's NR; A2's gamma 0 / 3; the full Gaussian likelihood (ln det) gap.

## 7. Hand estimate (before any code; unverified)

- **C0 (R1):** +0.002 to +0.005 in Legacy's best sigma8, so 0.2 to 0.4 Legacy widths. R2 up to about 0.8.
- **C2 (AD on A3's gas):** adds about half of A3's effect again, 0.15 to 0.25 Legacy widths.
- **C1:** almost surely a BRACKET. The halo choices differ by about a factor of 4 in halo mass: (a) about 1e13 Msun, (b) about
  2.4e12. So f_kSZ is about 0.15 to 0.3 on (a) and about 0.6 to 0.8 on (b), against sigma_f of about 0.05 to 0.1.
  - Strong edge (a): 0.8 to 1.5 widths.
  - Weak edge (b): 0.1 to 0.3 widths.
- **Gate:** Legacy g from 2.13 / 2.30 to about 1.6 to 1.9 (CONSISTENT, p about 0.13 to 0.18). DES g from 2.83 / 3.02 to about
  2.4 to 2.7 (GAP STAYS).
  - **Overall most likely GAP STAYS (driven by DES), 60 %; AMPLITUDE CONSISTENT 30 %; POOR FIT or OVERSHOOT 10 %.**
  - On the strong C1 edge both surveys may fall inside 2.
- **C3b:** Legacy's prior is likely to hold the alignment amplitude below the 0.64 to 0.74 our one-amplitude fit takes in the
  low-redshift bins (f_r about 0.16 to 0.2), widening the Legacy gap by 0.3 to 1 width. 40 % that it takes Legacy above 2.
- **The closure chat's guess** (C0 about 0.3, C1 0.5 to 1, C2 a third more on top; 1 to 1.5 left on Legacy, about 2 on DES) is
  close to mine for C0, more generous for C1 as a row, and the same for DES.

## 8. Disclosures

- **Seen before this freeze:**
  - every Part A and B number;
  - GH10 / GH11 / GH7's committed numbers (A(k), M_Z, Zhang's R_vir table);
  - the paper's Fig. 8 definition and Table 1 (mean log M_h 13.336, f_sat 0.279), via a web read, PROVISIONAL;
  - the Legacy chain's header;
  - Legacy's one-amplitude A_IA at B1 / BALL (0.71 / 0.64 canonical, 0.74 / 0.67 alt).
- No Part C number exists.
- C1's two halo choices differ by an amount I could estimate by hand before writing this; the decision rule is frozen anyway, and
  its outcome is computed, not assumed.
