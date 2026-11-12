# TR1 FROZEN CRITERIA: which baryon tracer does the cluster missing mass follow? (dated 2026-11-09)

Lane TR1, a GRADING lane of the adopted law (owner decision `closure_2026_11_09/OWNER_DECISION_2026-11-09_SK1_TR1_LAUNCH.md`).
It specifies the radial profile the cluster missing mass must have, for the closing statement of PAPER70 v2.0. It adopts
nothing. kappa = 1/2 FITTED; not theory closed. No particle is named: the component is "the missing mass". This file is
committed and pushed ALONE, before tr1.py or any TR1 number exists. Nothing below is changed after a number exists; any
reading fixed later goes in a dated amendment committed before the graded run, or is disclosed in RESULT.md.

## Law, footings, units

- The law: g_N = g^2 / (g + a0), inverted g_law(g_N) = g_N/2 + sqrt(g_N^2/4 + a0 g_N) (the loaders' glaw).
- Footings, graded SEPARATELY, never pooled: canonical a0 = 9.3603e-11 m/s^2 and alt a0 = 1.1312e-10 m/s^2, the values
  every loader on this path carries (HL3 AMENDMENT A1 item 1; the owner decision allows the loaders' hosted-path values
  where the record uses them). The KA2 replay of QX29 runs on its own loaders, which carry the same two values.
- Radii in r/R500. Bins: edges 0, 0.25, 0.5, 0.75, 1.0, 2.0 (HL3's).

## The missing mass: two readings, both graded

At each radius with baryon mass M_bar(<r) (g_bar = G M_bar / r^2) and dynamical mass M_dyn(<r) (g_dyn = G M_dyn / r^2):

- **Reading D (the brief's definition, PRIMARY):** M_miss(<r) = M_dyn(<r) - M_law(<r), with M_law(<r) = r^2 g_law(g_bar) / G.
  The deficit after the law has acted on the baryons (the missing mass taken as an extra Newtonian term, not boosted).
- **Reading S (source reading, co-graded):** M_src(<r) = r^2 g_N(g_dyn) / G - M_bar(<r), with g_N(g) = g^2 / (g + a0).
  The extra source mass that, added to the baryons INSIDE the law, gives g_dyn (the reading under which QX29 B1, NA2's F
  and QX33's M_need were computed).
Each reading gets its own label per footing. If D and S name different tracers, RESULT.md says so in its first lines;
neither is dropped.

## Data and samples

- **X-COP hydrostatic leg (PRIMARY leg).** `real_research/data/xcop/<cluster>/`: M_dyn = M_FORW (`*_hydro_mass.fits`),
  M_gas = MGAS (`*_fgas_profile.fits`), M_star = MSTAR (`*_mstar.fits`), R500 from `xcop_r500_ettori2019.json`, radii =
  the gas-profile grid where all three are tabulated, log-log interpolation, exactly HL3's construction (restated in
  tr1.py, checked by KA1). PRIMARY sample = the 7 clusters with measured stellar profiles (A85, A644, A1795, A2029,
  A2142, A2319, ZW1215). Brackets: (b1) without A2319; (b2) all 12 with the 5 star-less clusters given HL3's imputation
  (7-sample median M_star/M_gas at r/R500), flagged; (b3) bins inside R500 only (edges 0-1.0, four bins).
- **CLASH lensing leg (second leg).** `real_research/data/clash_rar_tian2020_fig2.tsv`, 84 points, 20 clusters. The
  table carries per-cluster identity (column Name), so CLASH is graded PER CLUSTER, not stacked. g_dyn = g_tot (Umetsu
  lensing), g_bar = gas + BCG (not split in the table). R500 from Umetsu+2016 M500c as HL3 built it (sources already on
  disk under `_external_data/hl3/`, untracked; read only). PRIMARY = the 16 X-ray-selected clusters; bracket = all 20.
  Only two tracers exist on this leg: gas + BCG ("bar") and the lensing total ("tot").
- **HFF member catalogues** (`real_research/data/hff_granata_*.tsv`): member positions and F814W / F160W magnitudes,
  Re, Sersic n. A STELLAR tracer only; no HFF lensing profile is on disk. Used only for a REPORTED (not graded)
  projected member-light profile slope; no download.
- No download in this lane. Anything a download would add is listed in RESULT.md.

## Tracers and the fit (one amplitude per cluster)

Tracers T on X-COP: **gas** (M_gas), **stars** (M_star, BCG + members as the FITS give it), **bar** (M_gas + M_star),
**tot** (M_dyn = M_FORW itself). On CLASH: **bar** (g_bar r^2 / G), **tot** (g_tot r^2 / G).
Fit form, per tracer, per reading, per footing: M_X(<r) = A_T,c * M_T(<r), ONE amplitude per cluster c, no other freedom.

Per cluster c and bin b:
1. per point i: l_i = log10(M_X(r_i) / M_T(r_i)); a point with M_X <= 0 enters as l_i = -1.0 (a fixed marker, counted
   and printed);
2. q_c,b = median of l_i over the cluster's points in bin b;
3. log A_T,c = mean of q_c,b over the bins where cluster c has points (each bin weighted equally);
4. residual delta_c,b = q_c,b - log A_T,c.
A cluster enters the SHAPE statistics only if it has points in >= 2 bins (a one-bin cluster carries no shape; its A is
still tabled). A bin is graded when >= 6 clusters have it (X-COP primary has 7; CLASH shared bins as in HL3).

Statistics per tracer, reading, footing, leg:
- SHAPE_b = median over clusters of delta_c,b, with bootstrap 95 % interval over clusters (B 10,000, seed 1103);
- RMS = sqrt(mean of delta_c,b^2 over every (cluster, graded bin) pair);
- AMPLITUDE: A_T,c per cluster, median, and SPREAD = SD(log10 A_T,c, ddof 1) over clusters.

## Lines (fixed before any number)

- **FOLLOWS T** iff RMS <= 0.10 dex AND max over graded bins of |SHAPE_b| <= 0.15 dex. Otherwise **DOES NOT FOLLOW T**.
- **UNIVERSAL amplitude** iff SPREAD <= 0.10 dex; otherwise **CLUSTER-DEPENDENT** (reported beside the FOLLOWS label).
- **Label per reading per footing (X-COP primary decides; CLASH is the second leg, labelled separately):**
  - the tracers that FOLLOW are listed; the WINNER is the one with the lowest RMS; if a second following tracer is
    within 0.02 dex of the winner's RMS the label is **TIE (T1, T2)**;
  - if no tracer FOLLOWS, the label is **NO TRACER FOLLOWS**, and the tracer with the lowest RMS is named "closest", with
    the sign pattern of its SHAPE (inner high = the missing mass is more concentrated than T);
  - a label is "(bracket-sensitive)" if any bracket b1-b3 gives a different FOLLOWS verdict for the winner (or for the
    closest tracer); brackets never replace the primary;
  - "the specification for the closing statement" = a tracer that FOLLOWS with a UNIVERSAL amplitude on both footings.
    If none does, RESULT.md says the specification is NOT a single-amplitude tracer, and gives the shape it needs.
- A FAIL is verified as hard as a PASS: for every DOES NOT FOLLOW verdict on the winner-candidate tracers (bar, tot),
  the brackets b1-b3 and the CLASH leg are printed, and RESULT.md states whether the verdict survives every one.
- Reported, not graded: (r1) core read inside bin 0 (sub-bins 0-0.05, 0.05-0.10, 0.10-0.25) for X-COP; (r2) a
  two-component non-negative least-squares fit M_X = a M_gas + b M_star per cluster (the mix the missing mass prefers;
  two amplitudes, so never a label); (r3) the HFF projected member-light slope d log L(<R) / d log R over 50-300 kpc
  around the brightest F160W member, beside X-COP's 3D d log M_star / d log r and the missing mass's, with the
  projection difference stated.

## Hand estimates (before any run; from HL3's printed X-COP medians and the record)

From HL3's hydrostatic medians (canonical rho = +0.530, +0.463, +0.372, +0.264, +0.161 by bin) and typical X-COP gas
fractions (f_gas(<r) ~ 0.07, 0.10, 0.12, 0.13, 0.15) and HL3's star/gas ratio (0.40 at 0.1 R500, 0.11 at 0.3, 0.07 at 0.7):
- **HE1 (QX33, three-doors B): gas alone DOES NOT FOLLOW, on both readings, inner bins HIGH** (missing mass more
  concentrated than the gas). Reading D estimate: log M_miss/M_gas falls by ~0.7 dex from bin 0 to bin 4, SHAPE_0 ~ +0.3.
- **HE2: stars alone DOES NOT FOLLOW** on both readings, inner bins LOW (the missing mass is less concentrated than the
  stellar cusp; QX33: does not follow the BCG cusp).
- **HE3 (reading D): bar DOES NOT FOLLOW** (log M_miss/M_bar falls ~0.6 dex over the five bins, SHAPE_0 ~ +0.25);
  **tot is the closest on reading D** (log M_miss/M_dyn = log(1 - 10^-rho) falls ~0.36 dex, RMS ~0.13, failing mainly at
  1-2 R500; inside R500, bracket b3, tot FOLLOWS with RMS ~0.07). Reading D label estimate: NO TRACER FOLLOWS, closest tot.
- **HE4 (reading S): bar FOLLOWS** (QX29 B1, a baryon-traced source at one amplitude, gave X-COP mean -0.003 / rms 0.082
  in g on the canonical footing); tot DOES NOT FOLLOW on reading S (g/(g + a0) - f_b falls ~0.5 dex to R500). Reading S
  label estimate: bar, both footings.
- **HE5: amplitude spread** of the best tracer ~0.10-0.15 dex (borderline UNIVERSAL); the S/bar median A ~3-4 (the
  record's "stars + gas at 3-4x").
- **HE6 (CLASH):** with two shared bins and 2-6 points per cluster, both tracers FOLLOW on both readings (low power:
  rho falls only 0.06 dex between the two bins); CLASH can confirm, not discriminate.

## Known answers (must pass before any label is read; tr1.py prints them first)

- **KA1** HL3's per-bin hydrostatic medians on the 7 (cluster median of the per-cluster median rho per bin): canonical
  +0.530 / +0.463 / +0.372 / +0.264 / +0.161, alt +0.500 / +0.429 / +0.339 / +0.229 / +0.126, each to 0.0015 dex.
- **KA2** QX29 B1 at amplitude f_cap R through QX29's own host rule and QX27's grader (imported read-only): X-COP
  mean / rms -0.003 / 0.082 (canonical), -0.027 / 0.087 (alt), each to 0.0015.
- **KA3** CLASH parse 84 points / 20 clusters; HL3's lensing medians on the 16: canonical +0.578 / +0.516, alt +0.549 /
  +0.485, each to 0.0015.
- **KA4** law round trip g^2/(g + a0) = g_N to 1e-12 over 1e-6..1e6 a0; readings D and S both give M_X = 0 when
  M_dyn = M_law(M_bar) (constructed test, to 1e-9 relative).
If any KA fails, tr1.out says DO NOT READ THE GRADE and no label is issued.

## MUTATE (tr1.py --mutate -> tr1_MUTATE.out/.json; each must bite, both footings, both readings)

Run on the winner of each reading/footing, or on the closest tracer when NO TRACER FOLLOWS.
- **M1 swap:** swap the tracer profile M_T(x) (in r/R500) between the two primary clusters whose log M_T(0.5)/M_T(0.1)
  differ most (data-chosen, no knob), refit. BITES iff the RMS over those two clusters' cluster-bins rises by >= 0.02 dex.
- **M2 plant:** multiply M_X by 10^0.3 at every X-COP point with r/R500 < 0.25, refit. BITES iff a FOLLOWS tracer flips
  to DOES NOT FOLLOW, or (for a tracer that already does not follow) SHAPE_0 rises by >= 0.20 dex.
- **M3 amplitude x2:** (a) each cluster's A_T,c doubled with no refit: every residual moves +0.301 and a FOLLOWS label
  must flip to DOES NOT FOLLOW (the lines are absolute); (b) A doubled for the alphabetically first half of the primary
  clusters (M_X x 2, refit): BITES iff UNIVERSAL flips to CLUSTER-DEPENDENT, or SPREAD rises by >= 0.10 dex if already
  CLUSTER-DEPENDENT.
A MUTATE that does not bite is reported as NO POWER for that check; the label then carries "(NO POWER on Mk)".

## Process

- No knob scans: the amplitude is the one fitted number per cluster; every line above is fixed here.
- Compute: seconds; RSS < 1 GB (printed); 1 thread, nice 10; SIGTERM exits without writing partial outputs (rerun from
  scratch is the checkpoint).
- Reuse read-only: HL3 (`closure_2026_11_08/HL3_lensing_leg_shape/`), NA2 prelude, QX27/QX29 graders, QX33. Nothing is
  written in their folders.
- Committed files: this file, tr1.py, tr1.out/.json, tr1_MUTATE.out/.json, RESULT.md. Explicit-path commits; push via a
  sparse temporary worktree of origin/main. No personal names, home paths or outside text in committed files.

kappa = 1/2 FITTED; not theory closed. Adopts nothing; the owner adopts.
