# CFG644 FROZEN CRITERIA: the neighbour-bounded settling edge (hypothesis H-NB)

Date 2026-10-12. Committed ALONE, before any CFG644 code or any H-NB number exists.

Settings: kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled, every test reported per
footing. "Cold energy" throughout; its mass is required; no particle species. No LCDM or standard-MOND yardstick enters a
verdict (the T6 halo model and the CFG529 environment term are LCDM-built and are labelled CONTEXT ONLY wherever they
appear). Not "theory closed". No PM run (a 1024^3 job is running), no download; 1 process, <= 1.5 GB, nice -n 10.

Pre-freeze disclosure (reasoning only, no script run): (i) with the supply cap kept, H-NB can only move an edge INWARD
(see S1 below); (ii) the KiDS isolation cut (no neighbour with M* > 0.1 M*_lens within 3 Mpc) leaves no neighbour able to
close a lens's basin inside its census edge, so H-NB is expected not to bite on the isolated stacks; (iii) a closed basin needs
a neighbour at least as massive, so the most massive systems (the CFG556 shear drivers) are expected to bite rarely. These
are predictions written before computing; the tests below decide them.

## 0. The hypothesis and the ONE definition of r_nb

H-NB: a system's settled cold energy extends only to its neighbour-bounded radius r_nb (or to the supply edge, whichever is
smaller). Inside r_nb the dynamics are those of candidate B unchanged (R7 kept: no external-field effect on internal forces).
Supply still caps the amount (5.364 x catchment baryons, census f_ret). Zero new constants.

Candidate-B profile of a body with baryons M_b (point mass at the radii used; the MW uses the record's CFG513 `Prof`):
M_B(<r) = M_b + min(M_b [nu_mono(G M_b / r^2 a0) - 1], S), S = 5.364 M_b / f_ret, f_ret = CFG515 `fret_census(M_b)`.
Its total is M_tot = M_b (1 + 5.364 / f_ret). Pull g(r) = G M_B(<r) / r^2.

DEFINITION (declared, not tuned): r_nb is the radius of the largest sphere about the system that lies inside its CLOSED
gravitational basin.
- Pairwise watershed: for a neighbour j at separation D_j, r_j solves g_own(r) = g_j(D_j - r), 0 < r < D_j (the equal-pull
  point on the line of centres; unique because the left side falls and the right side rises).
- Closure: neighbour j closes the basin only if M_tot,j >= M_tot,own. (For inverse-square pulls the equal-pull surface is an
  Apollonius sphere around the LESS massive body; the more massive body's basin is all space minus that sphere, so a smaller
  neighbour or a satellite does not bound it.)
- r_nb = min over closing neighbours of r_j; r_nb = infinity if none closes.
- Why not the literal scalar sum of all neighbours' pulls: magnitudes of pulls from neighbours in different directions do not
  add (an isotropic shell exerts no net pull), and a satellite inside the halo would truncate its host. The summed form is
  kept as the MAXIMAL-BITE BRACKET "S": g_own(r) = sum_j g_j(D_j - r) over every listed neighbour (all masses, all placed
  collinearly on the far side), applied if sum_j M_tot,j >= M_tot,own. Bracket S is reported everywhere; it carries no
  verdict weight unless stated.
- Distances: where only projected separations exist (KiDS photometric pool, KT2017 local catalogue) D = projected physical
  separation, a LOWER bound on the 3-D distance, so the measured r_nb is a lower bound (maximal bite). This is stated with
  every number.

H-NB settled profile: settled(<r) = min(phantom(<r), S) for r <= r_nb, frozen at its r_nb value beyond. Effective edge
r_eff = min(r_edge, r_nb). The unsettled remainder M_u = S - settled(<r_nb) (> 0 only if r_nb < r_edge) stays in the
catchment (R3 mass conservation): PRIMARY U0 = uniform density inside the turnaround sphere r_ta (record's r_ta_law);
bracket U-drop = removed from the own profile. (Halo model T6: the remainder goes into CFG556's own drained-shell term, its
native convention.)

S1 (structural statement, no number): r_eff <= r_edge always, so H-NB cannot move any edge outward and cannot raise the
outer lensing of any system. The reported variant T2-U (supply cap lifted, edge = min(r_nb, r_ta), law profile) is the only
way an edge moves outward; it violates A6 and is reported, never a verdict.

## 1. Tests (each per footing; data on disk only)

T1 SPARC. Own M_b = SPARC (0.5 L36 + 1.33 M_HI). Neighbours: KT2017 (kt2017_galaxies / kt2017_groups_full) matched to
SPARC positions (sparc_positions_merged.json, <= 1 arcmin); bodies = the other members of the galaxy's own KT2017 group
(individually) plus every other KT2017 group (one body at its principal galaxy, baryons from total K luminosity), window
|delta cz| <= 750 km/s, projected <= 5 Mpc at the SPARC distance. Baryons from K: Upsilon_K = 0.6 (the record's CFG4/CFG11
convention), M_sun,K = 3.28, SPARC gas-fraction fit (CFG4/CFG11 `cfit`), distances V/75 (CFG11 convention).
Rule: H-NB BITES SPARC for a galaxy if r_nb < R_last (outermost rotmod radius). Verdict: UNCHANGED if no galaxy bites;
otherwise list every galaxy that bites, recompute its law curve with settled mass frozen beyond r_nb, and report Delta rms
(dex) per galaxy and for the sample. Unmatched galaxies are listed as "no environment data".

T2 KiDS isolated lenses (the census-edge fail). Lenses: stack P (lr_lenses.npz) and its f30 subset (cfg96_isoflags); f30 is
primary. Neighbours: the CFG525 photometric pool (r < 20, 0.1 < z < 0.5, unmasked, M_gal = M*(1 + f_cold)), |delta chi| <
10 Mpc (W10), self excluded, projected separation / (1 + z_l). Census edge = CFG515 `r_edge_pm`, r_ta = `r_ta_law` (as
CFG525). Own profiles: CFG503 `kids_Md` / `kids_fin` (read-only), per group on a node grid in x = r/r_ta (control: equal to
CFG525's nodes), interpolated per lens; the census row is used exactly for lenses with r_nb >= r_edge.
Statistics (raw ESD; esd_full_loo, 50-patch jackknife, Hartlap): (a) bite fraction = lens weight with r_nb < r_edge;
(b) NATIVE chi2 (15 bins) of the own profile (no environment term) for B and H-NB, Delta chi2 = H-NB - B;
(c) CONTEXT ONLY: CFG529's committed CENSUS model vectors (A and B, f30) + the H-NB stack change, its covariance and SHMR delta.
Verdict per footing: IMPROVES if Delta chi2_native <= -4; WORSENS if >= +4; NO CHANGE otherwise. The question "does the edge
move outward for isolated lenses" is answered by S1 (NO, by construction) plus (a).

T3 KiDS dense vs isolated (sign test). Lenses: the CFG502 ALL parent sample (cfg502_stage.npz, 605,531 lenses, own WG/WW,
patches). r_nb from the same pool and window. DENSE = r_nb < r_edge (H-NB bites), ISO = otherwise.
Neighbour-clear zone: per lens, keep bin k only if R_k < s_n - r_edge,n for every window neighbour n with M_gal,n >=
0.1 M_gal,lens (Brouwer's own significance threshold; r_edge,n = the neighbour's census edge, the larger B extent), so the
counted neighbours contribute exactly zero DeltaSigma in kept bins under either model.
Band OUT = bins 0-8 (primary); K-out (6-8), outer6 (0-5) reported.
Q = sum(WG m)/KG / sum(WW m model_B) per subset; A_data = log10(Q_dense/Q_iso); A_pred = same with model_HNB in the numerator
model (i.e. log10[(H_dense/B_dense)/(H_iso/B_iso)]). Purity: A_pred,corr = p A_pred, p = 1 - n_bg/n_raw for the closing
neighbours of DENSE lenses (raw count within each lens's bite distance vs the area-scaled 4-6 Mpc annulus, the CFG502/509
method); A_pred,corr remains an upper bound on |A| (projected distances).
sigma: 200 within-cell relabellings of DENSE/ISO (cells = 10 log M* deciles x z bins 0.1/0.2/0.25/0.3/0.35/0.4/0.5);
jackknife reported.
Verdict per footing: SUPPORT if A_data <= -2 sigma and |A_data - A_pred,corr| <= 2 sigma; NOT SUPPORTED (sign) if A_data >= 0;
WEAK if -2 sigma < A_data < 0; NOT DIAGNOSTIC if |A_pred,corr| < 2 sigma (stated together with the data class). Caveat
stated with the result: neighbours outside the window (photo-z scattered members, chance projections) and leaked satellites
are not in the clear-zone mask and push A_data UP.

T4 MW outer slope. MW = CFG513 `Prof` (M_b 6.0e10, census f_ret) and the CFG553 baryons bracket (edge 287/261 kpc) where
used by the record; M31 = point Prof (1.2e11, census), D = 780 kpc (CFG513 D_LG); LMC = point baryons 3e9 at 50 kpc
(the record's CFG522 value). r_nb primary (LMC does not close the MW's basin) and bracket S (LMC + M31 summed).
Rule: the 15-27.5 kpc slope changes only if r_nb < 27.5 kpc or if the U0 remainder inside 27.5 kpc moves V by >= 0.001 dex.
Report r_nb, Delta slope (dlnV/dlnR, 15-27.5 kpc), V(20), V_c(60 kpc) both footings; the data side is CFG532b's committed
slope (read from its JSON, not re-fitted). Verdict: UNCHANGED / RESCUES (slope moves toward the CFG532b data by >= half the miss) / WORSENS.
Reported (context): MW and M31 settled masses and the mass inside 780 kpc under B vs H-NB.

T5 groups and clusters. Tian+26 groups (CFG543 data, J_A_A_710_L39, 63 groups, own logMbar and Re): neighbours from KT2017
(as T1, own KT group excluded by CFG543's `kt_match` rule), window |delta cz| <= 750 km/s. Since settled(<r) truncated at
r_nb equals the census profile with supply S' = phantom(<r_nb), the CFG543 P2 statistic is recomputed with its own
`sigma_log` and smult = min(1, phantom_point(<r_nb)/S) per group (r_nb >> Re point-mass phantom, declared).
Verdict: UNCHANGED if every group has r_nb >= 5 Re (P2 change < 0.005 dex), else report P2 and Z vs CFG543 (+0.060/+0.043).
X-COP (CFG4/CFG634): no neighbour catalogue on disk. Bracket: the separation D_crit at which an equal-total-mass neighbour
would put r_nb at R500 (data extent), and the X-COP clusters' mutual separations from their own positions and redshifts (a
partial measured environment). Labelled BRACKET, needs listed.

T6 growth / shear proxy (CONTEXT ONLY, LCDM halo model labelled). CFG556's halo model exec'd read-only up to its run block.
Per halo M_ta, the r_nb distribution from the halo model's own neighbour statistics: closing neighbours = halos with M_ta' >=
M_ta, number density from Tinker08, clustering 1 + b b' xi_lin(s) (Tinker10 bias, xi from the same P_lin), separations
s >= r_ta + r_ta' (non-overlapping catchments), pairwise watershed with the framework's census profiles (M_ta beyond r_ta);
P(r_nb < x) = 1 - exp(-N(<s_x)). U(k|M) averaged over that distribution with the H-NB truncation (remainder in CFG556's
drained shell). Report E = max(R-1) over 0.05 <= k <= 1, R at k 0.35 / 1, sigma8 ratio vs CFG556 primary (+0.715 / +0.883),
the fraction of halos biting per log M_ta decade, and the fraction of the excess removed: MATERIAL >= 50%, PARTIAL 10-50%,
NEGLIGIBLE < 10%. Direction and size only; no verdict on shear.
Native PM spec (written, NOT run): how a PM would compute r_nb per catchment at each census refresh.

## 2. MUTATE (CFG644_MUTATE=1, separate *_MUTATE outputs)

- M1 r_nb -> infinity must reproduce the supply-edge (candidate B) numbers: T2/T3 stacks = census stacks exactly; T4 profile
  = Prof; T5 P2 = CFG543 +0.05961/+0.04349; T6 R(k) = CFG556 primary (max |dR| <= 1e-12).
- M2 shuffled neighbours: each lens gets the neighbour set (offsets, masses) of a random lens in its own T3 cell; the DENSE/
  ISO split from shuffled r_nb must remove any environment trend: |A_data| < 2 sigma. (If the primary A_data is itself within
  2 sigma of 0 the tooth is reported as "nothing to remove".)
- M3 tooth: r_nb = 0.5 r_edge for every f30 lens must move T2's native chi2 by |Delta| >= 4 (the machinery can see an edge).

## 3. Overall verdict (frozen order)

H-NB is SUPPORTED only if T3 is SUPPORT on both footings, T1 and T4 are not WORSENS, and T2 is not WORSENS. It is RULED OUT
as a repair of the census-edge fail if T2 is NO CHANGE or WORSENS (it cannot fix the isolated-lens fail). Otherwise
INCONCLUSIVE. T5 and T6 are reported with their own labels (T6 CONTEXT ONLY). A fail is verified as hard as a win: every
fail is re-run with bracket S (maximal bite) and U-drop before it is reported.
