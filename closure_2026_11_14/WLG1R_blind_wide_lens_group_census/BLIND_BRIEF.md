# WLG1R BLIND BRIEF: an independent, blind re-grade of lane WLG1's frozen question (scorecard row 40)

2026-11-14. Written by the lead and committed alone, before the blind builder starts. Adopts nothing. kappa = 1/2
FITTED; X = 5.41 FITTED; not theory closed. Cold dark energy is a gravitating field component, not a particle.

## What is blind

The builder has not seen WLG1's results and must not. FORBIDDEN to open or read, by any tool:
- `closure_2026_11_14/WLG1_wide_lens_group_census/` (every file, including scripts and outputs);
- `closure_2026_11_13/CJ1_candidate_completion/` (the scorecard);
- `qwen_claude_field_theory/papers_2026/` (paper drafts), any `paper72_v1_5_draft` folder;
- `closure_2026_11_14/XJ1R_blind_caustic_junction/` (another blind lane) and `closure_2026_11_14/EUC18_mask_mass_population_gate_reread/` (another session's live lane);
- the assistant's memory folder outside the repository;
- `git log` / `git show` output for any path other than this folder (run git log only as `git log -- closure_2026_11_14/WLG1R_blind_wide_lens_group_census`).

ALLOWED: every other lane folder as an input (LNJ1, EUC6, EUC6R, EUC8, EUC17, EUC17R, ESZ1, EXR2 and the rest);
public data and the repository's `_external_data/` (the untracked photo-z files in `_external_data/wlg1_phz_by_id/`
are data and may be used, but the builder must spot-check at least 10 of them against fresh paced archive queries,
or re-fetch them all, with its own code).

## The frozen question (sections 0 to 7 and 9 of WLG1's frozen criteria, quoted verbatim; its section 8, a hand
## estimate written before WLG1's run, is withheld so it cannot anchor this build)


TEST lane. Adopts nothing, relabels nothing, registers nothing, edits no scorecard. Written and committed alone, before
any script of this lane exists, before any query of this lane is sent and before any number of this lane is computed.
Footings side by side, never pooled: canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2 (the EUC lanes' 1.132e-10
is used only where a known answer reproduces their numbers). Cold dark energy is a gravitating field component of the
record, not a particle and not matter. kappa = 1/2 and the share X = 5.41 are FITTED; nothing here can show the theory
closed or the data favouring the framework over LCDM.

**POST HOC.** The wide-lens ceiling break (EUC4, EUC4R), the richer environments (EUC6, EUC6R), the missing mass (EUC8),
the gas bounds (ESZ1, EXR2) and LNJ1's 1 / 0 of 316 were all seen before this lane, and so was the completed form's rule
6 (CJ1; candidate v2 in `closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface/COMPLETED_FORM_V2_CANDIDATE.md`).
No number of this lane (group stellar mass, photo-z of any neighbour, group speed) has been seen. A favourable word is a
HIT awaiting an independent blind re-grade, never a pass of the theory.

## 0. The question

Row 40 is "DEPENDS ON AN UNTESTED ASSUMPTION": the completed form gives the reference layout (cold share X = 5.41 of the
system's baryons as cold dust in FRZ1's halo shape, Newtonian at every radius) to systems faster than
v*(z) = v*(0) / E(z), v*(0) = a0 / (10 (1 + X) H0) = 668.53 / 807.93 km/s. LNJ1 counted each wide lens's own stars only:
1 / 0 of 316 above v*. Two questions, per footing:
- **(S) Speed.** Counting the baryons of the system that contains each wide lens (its group), is the system faster than
  v*(z_l)?
- **(A) Amount.** If the system is given the reference layout, does stars plus the projected reference halo inside the
  Einstein radius supply the observed Einstein mass, i.e. EUC8's missing mass?

## 1. Which system (the nested-system rule; frozen)

A wide lens sits inside a group; "the system" is otherwise undefined. Fixed here:

- **Primary rule N-A (outermost virialised system).** The system is the lens galaxy plus every baryon within a projected
  radius R_sys of the lens, where R_sys is the 200 rho_crit(z_l) radius of the system's own total mass
  M_tot = (1 + X) M_b(< R_sys), found self-consistently (iterate R <- (G M_tot / (100 H(z_l)^2))^(1/3) from R = 300 kpc,
  30 iterations or |dR| < 0.1 kpc). This is the record's virial definition: JNT2's model speed
  v_L = (10 G (1 + X) M_b H(z))^(1/3) is the circular speed at the 200 rho_crit radius of M_tot (check KA-7), so the
  baryons counted are those inside that radius. R_sys is clipped to [100, 600] kpc (600 kpc is where the background
  annulus starts); clipped lenses are counted and reported. The lens is taken as the system's centre.
  Speed: s = v_L(M_b, z_l) / v*(z_l). Layout if fast (rule 6 v2: "a system faster than v*(z) keeps the reference layout
  at every radius"): the lens galaxy is part of the fast system, so its stars are Newtonian and the cold share of all the
  system's baryons sits in the reference halo centred on the lens.
- **Bracket rule N-B (the lens keeps its own law).** Same system and speed, but the lens galaxy, which is slow on its own
  stars (LNJ1), keeps law S on its stars; the reference halo is built from the remaining baryons
  M_b - M*_lens and added on top. This is the most generous reading of the nesting.
- **Turnaround.** The group's turnaround radius (about 2 Mpc for the masses at stake) lies beyond the 1 Mpc cones on
  disk; baryons out to turnaround are not counted. Bracket R600 (fixed 600 kpc) is the largest radius this lane can
  count with a background annulus; it is stated as such.

## 2. Data (frozen)

- ECLIPSE key and object catalogues (`_external_data/euclid_dr1_eclipse/`, sha256 against EUC1's frozen hashes).
  Sample S = EUC1's cuts, grades A + B (6,173 lenses). **W** = the 316 lenses of S with theta_E >= 1.7"; **C** = EUC6R's
  249 matched controls (theta_E < 1.0", nearest in z and log M*); **L** = EUC6R's 40 expert-flagged large systems;
  **R** = EUC6R's 60 blank fields (the first 60 W lenses shifted +0.30 deg in Dec, at that lens's z). Target list and pair
  indices from `closure_2026_11_12/EUC6R_blind_regrade/euc6r_targets.csv`.
- Neighbour rows: EUC6R's raw MER cones, `_external_data/euclid_dr1_mer_cones_euc6r/` (665 gzipped CSVs, radius 1.02 x
  1000 kpc, server pre-cut flux_h_templfit > 5.0), hashes from EUC6R's manifest checked before use.
- Neighbour cut (EUC6R's, applied locally, NaN fails): flux_h_templfit > 5.75 uJy (H_E < 22.0), spurious_flag = 0,
  det_quality_flag < 4, point_like_prob < 0.7.
- **New query (this lane):** for every object passing the cut in every cone, Euclid DR1 photo-z and physical parameters
  by object_id lists from the ESA Euclid archive TAP (`dr1.phz_photo_z_wide` LEFT JOIN `dr1.phz_physical_parameters_wide`
  on object_id; columns object_id, phz_median, phz_70_int, phz_flags, phz_classification, phz_pp_median_stellarmass,
  phz_pp_68_stellarmass, phz_pp_median_redshift, quality_flag), at most 1,000 ids per request, one stream, at least
  1.5 s between requests, generic client name, no personal details, retries after 10, 30, 90, 270 s. Raw responses
  gzipped under `_external_data/wlg1_phz_by_id/` (new folder, untracked); a manifest with row counts and sha256 is
  committed. Read with `python3 -I`.
- **Seen before freezing (disclosed):** the two tables' column lists, and one timing probe at a position that is not a
  target (0.60 deg south of W lens L000021, radius 0.02 deg): 75 MER objects, all returned with photo-z and a stellar
  mass in 1.4 s; stellar mass is log10 Msun; the `imf` column reads -99. Nothing around any target was queried.

## 3. Baryons counted (frozen)

**Lens stars.** Primary: EUC17's in-mask correction applied to the catalogue mass, on LNJ1's common scale:
log M*_lens = eclipse_log_survived_mass_med - log10 f_in_mask + 0.036 (f from `closure_2026_11_13/EUC17_mask_aperture_
mass_reread/euc17_per_lens.csv`, rows P and W_B, which cover all of W; controls: rows P where present, else uncorrected,
counted). Bracket B-UNC: uncorrected (log10 f = 0).

**Member stars.** For each target, objects passing the cut with phz_classification = 2 (galaxy), at projected
30 kpc <= R < R_sys (R at z_l in the catalogue cosmology, EUC1's Cosmo / EUC6R's haversine), excluding the lens's own
MER object, with |phz_median - z_l| <= w (1 + z_l), **w = 0.08 primary** (brackets B-W05: 0.05, B-W12: 0.12).
- Stellar mass: phz_pp_median_stellarmass, moved to z_l by 2 log10(D_L(z_l) / D_L(z_pp)), z_pp = phz_pp_median_redshift.
  Objects with no finite positive mass get log M from their H-band luminosity at z_l and the lane-wide median
  log(M / L_H) of window members that have one (counted, reported).
- Scale: one constant Delta added to every member, Delta = median over W and C lenses whose MER object is in its own cone
  with a finite PP mass of [log M*_lens (primary scale) - log M_PP,lens (moved to z_l)]. This puts members on the lens's
  scale. Bracket B-UNC recomputes Delta against the uncorrected lens masses; bracket B-RAW sets Delta = 0.
- **Background:** the same window, cut and class in the annulus 600 <= R < 1000 kpc, as stellar mass per unit area;
  net member mass M*_mem = sum(30 <= R < R_sys) - Sigma_bg x pi (R_sys^2 - 30^2). Negative values are kept (no floor) in
  every statistic.
- Bracket B-STAR+: member stars x 1.4 and lens stars x 1.0 plus 0.4 x M*_mem (faint members below H_E = 22 and
  intragroup light; a generous allowance, not measured).

**Gas (class-level, from ESZ1; per lens).** ESZ1's thermal-SZ stack at 1 keV (2' compensated aperture, about 700 kpc):
W measured 5.2e12 Msun, 2 sigma upper limit 8.3e12; controls measured -0.5e12, upper limit 3.0e12.
- Primary G-MID: W 5.2e12, C 0 (measured, floored at 0 for C), L and R 0.
- Bracket G-0: no gas. Bracket G-HI: W 8.3e12, C 3.0e12 (the most gas the data allow).
- 1 keV is the hydrostatic temperature of a system at v* (kT = mu m_p v_c^2 / 2, about 0.8 to 1.2 keV for
  v_c = 511 to 617 km/s at z 0.5), so ESZ1's conversion is self-consistent at the threshold. Gas mass scales as 1 / T;
  this is stated, not bracketed further.
- EXR2 (reading A1: CUSP EXCLUDED) excludes gas concentrated on the lens; so gas enters the Einstein cylinder only with
  the halo's extended shape (section 4), never as a cusp.

M_b = M*_lens + M*_mem + M_gas.

## 4. Predicted Einstein mass if fast (frozen; LNJ1's code, copied, checked by KA-2)

R_E = theta_E D_A(z_l), M_obs = pi R_E^2 Sigma_cr(z_l, z_s) (EUC1's Cosmo), **z_s = infinity primary** (the least mass
lensing allows; an under-prediction there is robust to real sources). Bracket B-ZS2: z_s = max(2.0, z_l + 0.5) (EUC8's
central case).
- **N-A:** M_ref = M*_lens F_2D(R_E) + C_cyl(R_E; X M_b) + C_cyl(R_E; M_gas), where C_cyl is the Abel-projected cylinder
  mass inside R_E of FRZ1's halo exactly as LNJ1 section 4 (M_ta = X M_b h / (1 - f_b), NFW at 200 x mean density,
  c(M) = 10.14 (M / 2e12)^-0.081 (1 + z)^-1.01, truncated at turnaround), the gas term the same shape normalised to M_gas
  inside turnaround. Member stars are not put in the cylinder.
- **N-B:** M_ref = M_law,S(M*_lens) + C_cyl(R_E; X (M_b - M*_lens)) + C_cyl(R_E; M_gas).
- Concentration brackets B-C07, B-C14: c x 0.7, x 1.4.
- r = log10(M_obs / M_ref). **EUC8's missing mass** in the fast layout is M_obs - M*_lens F_2D(R_E); reported beside r is
  the median ratio of what the halo terms supply to it, and EUC8's own law-based excess.

## 5. Statistics and words (per footing, per configuration)

Lenses graded: every W lens whose cone passes the edge rule (EUC6R's: N_bg >= 0.4 x the median N_bg of W, C and L) and
whose cut objects have photo-z rows for at least 80 % (counted). Bootstrap: 2,000 resamples of lenses,
numpy default_rng(20261114), 2.5 / 97.5 percentiles.

- **(S) Speed.** s_i per W lens; median s with its interval. **FAST** if the lower bound >= 1; **SLOW** if the upper
  bound < 1; **MIXED** otherwise. Reported: fraction of W with s >= 1, and the same for C.
- **(A) Amount.** r_i for every graded W lens, each treated as fast (so (A) does not depend on (S)); median r with its
  interval: **FITS** if the interval overlaps [-0.10, +0.10]; **UNDER** if its lower bound > +0.10; **OVER** if its upper
  bound < -0.10 (LNJ1's lines). Reported: the same on the W lenses with s >= 1.
- **Control condition (for the pass word only).** C lenses with s >= 1 under the same rule, if at least 20: their median r
  interval must overlap [-0.10, +0.10] (the rule must not break the small lenses it hands to the reference layout). Fewer
  than 20: condition met trivially (stated).

Word, first that applies:
1. (S) SLOW: **GROUPS TOO SLOW: ROW 40 FAILS**.
2. (A) UNDER: **HALO SHORT: ROW 40 FAILS** (whatever the speed, the reference halo at the 5.41 share does not supply the
   missing mass inside R_E).
3. (S) FAST, (A) FITS, control condition met: **WIDE LENSES ARE FAST GROUPS: ROW 40 PASSES** (a HIT, post hoc, awaiting
   a blind re-grade; not a pass of the theory).
4. Otherwise **NO VERDICT** (MIXED speed with FITS; any OVER, which z_s = infinity cannot make robust; control condition
   failed).

**FRAGILE** if any frozen bracket gives a different word: G-0, G-HI, B-UNC, B-RAW, B-W05, B-W12, R300 (R_sys fixed at
300 kpc), R600 (fixed 600 kpc), N-B, B-C07, B-C14, B-ZS2, B-STAR+. Each bracket changes one thing.

**NOT EVALUABLE** if any known answer or instrument check fails, a twin does not bite, or fewer than 150 W lenses are
graded.

## 6. Known answers (all must pass)

- **KA-1 (LNJ1, lens stars only).** For the 316 W lenses, s on the lens's stars alone (catalogue mass + 0.036, no EUC17
  correction, no members, no gas) equals `lnj1_per_lens.csv` s_model_can / s_model_alt to 1e-4, and the count with s >= 1
  is **1 / 0**.
- **KA-2 (LNJ1's projections).** logM_obs_inf, logM_law_can, logM_law_alt and logM_joint_X5.41_can of the 316 W lenses
  reproduced to 1e-3 dex with this lane's copy of LNJ1's code.
- **KA-3 (EUC6R's neighbour excess).** From the cone files with this lane's code, every target's n_in and n_bg equal
  `euc6r_counts.csv` exactly, and the paired median richness difference W - C is +3.59 on 242 pairs (to 0.01).
- **KA-4.** v*(0) = 668.53 / 807.93 km/s (to 0.01).
- **KA-5 (EUC8).** The W lenses' far-source excess M_obs - M_law,S(M*_cat) with EUC1's footings (alt 1.132e-10) equals
  `euc8_wide_per_lens.csv` excess_far_canonical / _alt per lens to 1e-3 relative (median).
- **KA-6 (photo-z coverage).** At least 90 % of W and C lenses have their own MER object (ECLIPSE MER_object_id) in their
  cone with a photo-z row.
- **KA-7 (virial definition).** sqrt(G M / R_200c(M)) = (10 G M H(z))^(1/3) to 1e-9 on three masses.

## 7. Instrument checks and twins

- **N1 blank fields.** R positions (edge rule applied to each), net member mass inside a fixed 300 kpc at the paired W
  lens's z: |median| <= 1.0e11 Msun.
- **N2 positive control.** Median net member mass inside 300 kpc of L minus that of C: bootstrap lower bound > 0.
- **TW-ZS (photo-z shuffle; must bite).** Each W lens's window centred on the redshift of another W lens (permutation,
  seed 20261114, no fixed points kept). The median net member mass of W inside 300 kpc must fall to at most half the main
  value; otherwise the photo-z window is not selecting members: NOT EVALUABLE. Outputs under separate names; exit 1.
- **TW-INJ (amount; must bite).** M_obs replaced by M_ref per lens: (A) must read FITS on both footings; exit 1.
- **Reported twins (no gate):** TW-H (v*/2) and TW-D (2 v*): the speed reading at each; controls C through the whole
  pipeline (speed, amount, member mass), paired with W where both are graded.

## 9. Outputs

`wlg1_fetch.py` (queries), `wlg1.py` (everything else), `wlg1.out`, `wlg1.json`, `wlg1_per_lens.csv`,
`wlg1_fetch_manifest.csv`, twins `wlg1_MUTATE_ZS.*`, `wlg1_MUTATE_INJ.*`, `RESULT.md`. No home paths, no personal names.
Light compute (`nice -n 19`, one thread). Not pushed.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## What the blind builder does

1. Write `FROZEN_CRITERIA.md` in this folder: its own reading of the question above, the same words, the same
   lines, the same brackets and known answers, plus at least one twin of its own that must bite. Commit it alone.
2. Write its own code from the definitions (it may import shared library code that lanes other than WLG1 use, e.g.
   LNJ1's lensing helpers, and must say which). Commit the scripts before any graded run.
3. Run, both footings (canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s^2), side by side, never pooled.
4. `RESULT_BLIND.md`: frozen word per footing and configuration first, post hoc readings marked. Lane words as in
   section 5 above, each suffixed ", BLIND".
5. Commit path-limited (`git commit -m ... -- <paths>`; shared index; never `git add -A`). No outcome word in any
   commit subject. Do not push. Do not edit the scorecard. No personal names or home paths in files.
