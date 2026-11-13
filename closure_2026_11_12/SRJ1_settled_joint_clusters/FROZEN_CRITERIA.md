# SRJ1: the settled-radius joint on groups and clusters. FROZEN CRITERIA

Committed alone, before any SRJ1 script exists and before any number of the joint on a cluster or group has been computed.
TEST lane: relabels nothing, adopts nothing, registers nothing. **The joint under test is post hoc to the forest row's fail
(FRZ1, then FZS1). A HOLDS here is not a pass of form B or of the joint: it is one-sided, and it would need an independent
blind re-grade.** A FAILS here kills the joint at f = 1 whatever the forest lanes (SRF1, SRF1R; not opened by this lane) find.
Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a
gravitating field component; no particle anywhere. kappa = 1/2 FITTED; not theory closed.

## 0. The question

With the settled-radius joint at f = 1.00 exactly (f = 0.75 and f = 1.25 reported beside it as two fixed brackets, not a scan),
do the record's group and cluster rows, graded with RB1's frozen gates (`closure_2026_11_09/RB1_form_b_hot_systems/`, criteria
ef53f5512f, A1 12504fe611), still hold? The only new ingredient is where the cold dark energy sits inside R_set.

## 1. The rule, per system j (frozen)

All machinery not named here is RB1's, copied (not imported): its X-COP builder (HYD points, the 7 clusters with measured
stars), its Lovisari loader, `fret`, `li`, `kvm18`, `xcop_last`, `class_stat` (10,000 resamples, seed 1109), `cl_bin_median`,
`m_native` (ZN4's z = 0 native shape), `solve_R200`, `rho_crit` (h 0.7, Omega_m 0.3). R = 5.41, f_c = R / (1 + R).

1. **Reference (joint off) = RB1's.** C_R(r) = f_c M200 m_native(r/R200, log M200), anchored at the system's aperture A by
   C_R(A) = R M_b,obs(<A) (RB1's `solve_R200`). So with the joint off, q(A) below equals RB1's f_ret(A) exactly.
   Apertures: X-COP graded A = r_last (RB1 gate 1 and gate 3); X-COP bracket A = R500 (RB1's `xcop_last(at="R500")`, anchor at
   R500); groups A = R500.
2. **Baryons M_b(r) that source the law.**
   - X-COP: the cluster's own HYD points (measured gas + measured stars), log-log interpolated; proportional to r^3 inside the
     innermost point; proportional to r beyond the outermost point up to R200; constant beyond R200.
   - Groups (no profiles on disk): FRZ1's `bar_cum` shapes (stars Hernquist with a = 0.015 R200 / (1 + sqrt 2); gas cored,
     r_c = 0.1 R200), with R200 the reference's, each normalised at R500 to the graded baryons (Mgas500; KVM18 stars),
     constant beyond R200.
   - Graded: gas + stars. Bracket: gas alone sources the law (the model's baryons and the anchor stay gas + stars).
3. **The law's layout C_B(r)** = FRZ1's cluster-regime form-B rule (`frz1_hm.py`, `layout`, mode "B"), transposed with the
   reference's shape in place of FRZ1's NFW:
   - share = C_R(R200); m_in(r) = m_native(min(r, R200)/R200) / m_native(1); outside(r) = C_R(r) - C_R(R200) for r > R200, else 0;
   - v = sqrt(G M200 / R200) (physical); fc = clip(0.5 (1 - (v_stiff / v)^2), 0, 1), v_stiff 265.8 / 288.1 km/s (FRZ1's);
     W = 1.5 v^2 / (1.5 v^2 + 15^2); E = (1 - fc) share;
   - ph(r) = min(W phi(M_b(min(r, R200)), r), E), phi(M, r) = sqrt(M^2/4 + M r^2 a0 / G) - M/2 (the law's phantom, footing's a0);
   - rem = max(E - ph(r_ta), 0); C_B(r) = fc share m_in(r) + ph(r) + rem min(r, r_ta)/r_ta + outside(r).
   The cluster rule is used for every system; the number with v <= v_stiff (fc = 0) is reported.
4. **R_set = f x R_fold(z_j, M_b,fold).** R_fold from FLD1's primary run files (`fable52_push/FLD1_fold_reach/runs/
   hubble_<footing>_M<logMb>_zi10_N2400.json`) with FZS1's `rfold_kpc` copied: linear in z on each stored series, log R linear
   in log M_b between the 12 table masses, scaled as M_b^(1/3) beyond the ends (FZS1's rule; no clamp). **z_j = the system's
   own redshift** (X-COP: Ettori 2019 json; Lovisari: its table), because the joint asks what has settled by the epoch at which
   the system is observed. **M_b,fold = M200 / (1 + R)**, the baryons that come with the reference's cold inside R200: the
   transposition of FZS1's cluster-regime FB M200c. r_ta = FLD1's stored R_ta series at the same z and M_b,fold, same
   interpolation and extrapolation. R_set is capped at r_ta (FZS1's rule). Reported (no label): M_b,fold = M_b,obs(<A).
5. **The joint (FZS1's junction):** C_S(r) = s C_B(r) for r <= R_set, C_S(r) = C_R(r) for r > R_set, s = C_R(R_set) / C_B(R_set).
   Model mass M_S(r) = M_b,obs(r) + C_S(r).

## 2. Gates (RB1's, unchanged in statistic and line)

- **(a) Amount, X-COP (RB1 gate 1, class C-X).** q_j(A) = C_S(A) / (M_HSE(A) - M_b,obs(A)): the joint's minimum cold over the
  measured cold (= RB1's f_ret when the joint is off; +inf if M_HSE <= M_b). Graded: A = r_last, M_HSE = M_FORW, 7 clusters.
  Class median with RB1's bootstrap; **FAILS iff the lower 95 % bound > 1**, else CONSISTENT. Printed per cluster: q, the joint's
  factor C_S(A)/C_R(A), and M_S(A) / M_HSE(A).
- **(b) Shape, X-COP (RB1 gate 3).** Delta = log10(M_FORW / M_S) on HYD's points, anchor r_last, per-cluster medians in r/R500
  bins [0, 0.25, 0.5, 0.75, 1, 2], median over clusters; a bin is graded with >= 5 clusters; **CONSISTENT iff |median| <= 0.10
  dex in every graded bin**, else FAILS.
- **(c) Groups (RB1 gate 1, class G-H).** q at R500 for Lovisari's 20 groups, Mgas500 + KVM18 stars; same statistic and line.
- **(d) The Bullet: NOT GRADED, stated now.** RB1's graded Bullet row places each cluster's cold as R_j times its galaxy Plummer
  field; the cold reference layout never enters it (ZN4's shape entered only a reported M300 row). The law's layout needs the
  phantom of a merging, non-spherical gas distribution, which that machinery does not have. Moving it would be a new model,
  not RB1's gate.
- Not re-graded: RB1 gates 2 (trend) and classes G-DB / G-DF. Reported only: the gate-2 slope with q at R500 in place of f_ret.

## 3. Words, per footing (canonical / alt, never pooled)

- **NO VERDICT** if any check of section 4 fails or a twin of section 5 does not bite.
- **JOINT FAILS ON CLUSTERS** if (a), (b) or (c) FAILS.
- **JOINT HOLDS ON CLUSTERS (ONE-SIDED)** if (a), (b) and (c) are all CONSISTENT. Never a pass: gate 1 is one-sided (it cannot
  fail from below) and the two-sided amount gate stays FAIL as PD1 graded it.
- **FRAGILE** is appended when a frozen bracket gives a different label on any graded row, naming the bracket and saying
  whether the reference (joint off) crosses there too. Frozen brackets: f = 0.75; f = 1.25; M_NFW (fgas file's NFW-fit
  hydrostatic mass, RB1 A1's bracket) in place of M_FORW on (a); gas alone sourcing the law; (a) at A = R500 (RB1's aperture
  bracket; stated now: RB1 found the reference itself above the line there on M_FORW, 1.057 [1.046, 1.072]).

## 4. Checks before any graded number (any failure: NO VERDICT)

- **K1 joint off reproduces RB1** (f = 0, both footings) against `rb1.json`: C-X at r_last and at R500 (median, bounds,
  per-cluster), the two M_NFW rows, G-H (median, bounds), gate 3's five bins; tolerance 1e-6 absolute.
- **K2 FZS1's diagnostic.** Executing `fzs1_hm.py` up to its run marker (read-only, as `fzs1_diag.py` does), z 2.2 canonical,
  the halo nearest 1e13: my transposed C_B fed FRZ1's own inputs (NFW m_in, `bar_cum`, comoving a0, r_ta) equals FRZ1's
  `layout(mode="B")` cold to 1e-9 relative at every grid point; the settled fractions cold(<0.25 / 0.5 R_set)/cold(<R_set) equal
  fzs1_diag.out's law 0.128 / 0.373 and reference 0.175 / 0.458 to 0.0006; R_set 0.4106 and s 1.058 to their printed digits.
- **K3 R_fold:** FZS1's KA-F values from my copy (canonical z 0 / 2 / 4: 62.2 / 21.3 / 7.59; 139.3 / 47.8 / 17.24; 168.8 / 57.9 /
  20.96; 196.9 / 67.6 / 24.51 for log M_b 9.4 / 10.45 / 10.7 / 10.9) to 0.06 kpc.
- **K4 junction:** in every system, both footings, every f: |C_S(R_set)/C_R(R_set) - 1| <= 1e-12; C_S non-decreasing (1e-9).
- **K5 parsers:** 20 groups; 12 X-COP, 7 with stars.

## 5. Mutation twins (separate outputs `*_MUTATE_<twin>.*`; a twin run exits with status 1 by design)

- **TW-N, Newtonian inside R_set:** phi = 0 (no phantom; C_B = fc share m_in + E min(r, r_ta)/r_ta + outside). Must move X-COP's
  shape bins by >= 0.05 dex rms against the graded f = 1 joint, both footings.
- **TW-0, f = 0:** must return the reference: K1's numbers to 1e-6.
- A twin that does not do this does not bite: NO VERDICT.

## 6. Seen before freezing (disclosed)

- The lead's brief: FZS1's rule and fractions (0.13 / 0.37 against 0.18 / 0.46), R_set about 0.8 r200m at z 2.2, FLD1's 0.52 R_ta,
  RB1's X-COP at about 1.06 (M_FORW) / 0.96 (M_NFW) at R500, and **the lead's unverified estimate: about 20 % less cold dark
  energy inside half of R_set, so the joint pushes X-COP over the line at R500 or misses the shape line, a likely FAILS.**
- Read: RB1's criteria, A1, RESULT (all its numbers), `rb1.py` (loaders, gates 1 and 3, Bullet machinery), the keys of `rb1.json`;
  FZS1's criteria, RESULT, `fzs1_diag.py` / `.out`, the first 90 lines of `fzs1_hm.py`; FRZ1's `frz1_hm.py` (first 120 lines:
  `bar_cum`, `phantom`, `layout`); FLD1's RESULT table, `at_z` / `rfold`, the keys of one run file (log M_b 12: R_fold 458.7 kpc,
  R_ta 880.7 kpc at z 0); ZN4's shape keys (x_edge 7.4 / 7.8). SRH1's folder: names only. SRF1 / SRF1R: not opened.
- No q, Delta, R_set, s or C_S/C_R of any X-COP cluster or group has been computed.

## 7. My hand estimate (before any number; may be wrong)

At z 0.05 X-COP's Newtonian baryon acceleration near R500 is about 0.01 to 0.03 a0, so the phantom is several times the
baryons and reaches the cap E inside R500. Then the law's layout here is **cuspier** than the reference, the opposite of FZS1's
z 2.2 halo. M_b,fold is near 1e14, so R_fold is extrapolated about 2 dex in mass and comes out near 1 to 1.2 R200: r_last and
R500 lie inside R_set, s is near 1. I expect C_S/C_R about 1.1 to 1.25 at R500 and 1.0 to 1.1 at r_last. Then C-X's q at
r_last rises from 1.095 and its lower bound from 0.885 toward 1: about 40 % FAILS on (a). The inner shape bins go negative: about
50 % FAILS on (b). Groups stay well below 1: 90 % CONSISTENT. Overall about 60 % JOINT FAILS ON CLUSTERS, through more cold in
the centre, not less as the brief expects. f = 1.25 more likely to fail than f = 0.75.

## 8. Operational

`srj1.py` -> `srj1.out` / `srj1.json` (graded, both footings, all brackets and checks); `python3 srj1.py --twin newton` and
`--twin f0` -> `srj1_MUTATE_<twin>.out` / `.json`, exit 1. One process, OMP_NUM_THREADS=1, nice 10, under 2 GB. Other lanes'
folders read only; their code copied or executed read-only. No network. Explicit-path commits; not pushed by this lane.
Any change after numbers are seen goes in `AMENDMENT_A1.md`, committed alone, with the frozen word kept beside the amended one.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
