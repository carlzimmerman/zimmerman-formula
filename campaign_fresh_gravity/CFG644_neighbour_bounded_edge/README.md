# CFG644: the neighbour-bounded settling edge (H-NB). RULED OUT as a repair of the census-edge fail: with the supply cap kept it can only move edges inward, and on the data it barely bites (KiDS isolated lenses 0%, SPARC 0 real bites, MW slope unchanged, halo-model shear excess 0.00% removed); groups shift by +0.008 dex and still close

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (6a03c0870).
- **Scripts** (1 process, nice 10, no PM, no download):
  - `cfg644_lib.py`: candidate-B point-body profiles and the r_nb solvers.
  - `cfg644_kids.py`: T2 + T3, about 7 min once the node tables exist. The tables are cached outside git in `_external_data/cfg644_work/` and take about 13 min to build. Peak memory footprint 1.51 GB (see the disclosures).
  - `cfg644_local.py`: T1, T4, T5 and the X-COP bracket, about 15 s.
  - `cfg644_halo.py`: T6, CONTEXT ONLY, about 15 s. `CFG644_EXCL=max` writes the reported `_EXCLmax` variant.
- **MUTATE:** `CFG644_MUTATE=1` writes the `*_MUTATE.*` files. The local and halo runs exit 0 (all teeth pass). The KiDS run exits 1, because tooth M2 fails, as described under T3.
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled; CFG513/CFG543 code uses the record's rounded 9.36e-11 / 1.13e-10. The cold energy's mass is still required; no particle species. Not "theory closed". No ΛCDM or standard-MOND yardstick enters a verdict: the T6 halo model and the CFG529 environment term are labelled CONTEXT ONLY.

## The definition (one, declared before any number)

**r_nb is the radius of the largest sphere about the system that lies inside its CLOSED gravitational basin.**
- The basin edge toward neighbour j is the equal-pull point g_own(r) = g_j(D_j − r), using both bodies' candidate-B profiles: baryons plus min(law phantom, 5.364 M_b/f_ret,census).
- Only a neighbour at least as massive (M_tot,j ≥ M_tot,own) closes the basin. For inverse-square pulls the equal-pull surface is an Apollonius sphere around the smaller body, so a satellite does not bound its host.
- r_nb = min over closing neighbours.
- The literal "summed pull" (every neighbour's pull added collinearly, collective closure) is kept as the maximal-bite **bracket S**. Pull magnitudes from different directions do not add, so S has no verdict weight.
- Settled cold energy is truncated at r_eff = min(r_edge, r_nb).
- The unsettled remainder stays in the catchment: U0 (primary) spreads it uniformly inside r_ta; the U-drop bracket removes it.
- Supply cap and R7 are kept, and there are zero new constants.
- Where only projected separations exist (KiDS photometric pool, KT2017), D is the projected separation, a strict lower bound on the 3-D distance. So r_nb is a lower bound and the bite is maximal.

**S1 (structural): r_eff ≤ r_edge.** H-NB cannot move any edge outward or raise any outer lensing signal. The brief's "edge moves outward for isolated lenses" needs the supply cap lifted. That is variant T2-U, which violates A6 and is reported only.

## Results (pairs are canonical / alt)

| test | statistic | canonical | alt | label |
|---|---|---|---|---|
| **T1 SPARC** (138 matched to KT2017; 37 have no environment data) | galaxies with r_nb < R_last | 1 (NGC 3109, r_nb 6.2 kpc vs R_last 6.5) | 1 (NGC 3109) | BITES by the frozen rule. The bite is a **projection artefact**: the closing body is the PGC 29166 group at 18 Mpc (V 920 km/s, inside the ±750 km/s window), 20 kpc away in projection and 17 Mpc in 3-D. Δrms +0.0005 dex; sample mean rms 0.09920 → 0.09920. With KT2017 3-D distances (reported) there are **0 bites**. Bracket S: 23 galaxies (projection plus collinear summing over hundreds of window bodies) |
| **T2 KiDS f30** (isolated, raw ESD, native own-profile χ², 15 bins) | lens weight with r_nb < r_edge; Δχ² H-NB − B | **0.000** (min r_nb/r_edge 1.61); Δχ² **0.000** | **0.000** (min 1.77); Δχ² **0.000** | **NO CHANGE** on both footings. U-drop 0.000. Bracket S: weight 0.26% / 0.20%, Δχ² +0.11 / +0.09. Stack P is identical (0 bite). Native absolute χ² of the census own profile: 97.9 / 78.7. CONTEXT (CFG529 ΛCDM-built environment): census 45.57 / 35.84 (A), unchanged |
| T2-U (reported; supply cap lifted, edge = min(r_nb, r_ta)) | Δχ² vs census | f30 +6.53 (84–87% of the weight has r_nb ≥ r_ta, so this is the law to r_ta) | f30 +1.84 | worse on the clean sample; stack P −118 / −142 (own-only, with no environment term, so not meaningful) |
| **T3 KiDS ALL** (605,531 lenses), dense (r_nb < r_edge; 65,037 / 57,283 lenses) vs isolated, neighbour-clear zone, band OUT | A_data (relabel σ); A_pred × purity (p 0.935 / 0.945) | −0.067 ± 0.082 (Z −0.8); +0.004 (Z +0.05) | −0.230 ± 0.073 (Z −3.2; jackknife σ 0.146); +0.004 | **WEAK / NOT DIAGNOSTIC** on both footings. The frozen statistic is also **invalidated by tooth M2** (see below) |
| **T4 MW** (M31 at 780 kpc closes the basin; the LMC does not) | r_nb; Δ slope 15–27.5 kpc | 323 kpc; +3.8e-5 | 323 kpc; +2.9e-5 | **UNCHANGED**. The CFG532b miss is −0.164 / −0.176. Bracket S (LMC summed): r_nb 40.5 kpc, Δ slope +9e-5, V_c(60 kpc) 171.6 → 143.6 / 179.3 → 149.8 km/s |
| T4 context: LG timing (CFG515 strict statistic) | v_pred, z | −168.7 (z +13.5) → −159.1 (z +11.3) | −168.8 (+13.5) → −160.9 (+11.7) | helps by about 16%; does not resolve |
| **T5 Tian groups** (57/63 with KT2017 environment; 20 with a closing neighbour; 16 with r_nb < 5 Re) | CFG543 P2 | +0.0596 → **+0.0687** (Z 1.65 → 1.89) | +0.0435 → **+0.0517** (Z 1.20 → 1.42) | **CHANGED** by the frozen rule (some r_nb < 5 Re), but still **CLOSES**. Canonical moves toward the |Z| = 2 line. With 3-D KT distances (reported): +0.0601 / +0.0437 |
| T5 X-COP | separation D_crit at which an equal-mass neighbour puts r_nb at R500 | 1.81–2.86 Mpc | same | BRACKET. The nearest X-COP pair (A3158–A3266) is 42 Mpc apart. No neighbour catalogue is on disk |
| **T6 halo model** (CONTEXT ONLY) | E = max(R − 1), k 0.05–1; share of the excess removed | +0.7151 → +0.7151; **0.00%** | +0.8829 → +0.8829; **0.00%** | **NEGLIGIBLE**. P(r_nb < r_e) is 0.6–1.0% (canonical) and 0.2–0.4% (alt) at log M_ta 10–13, and 0 at 13 and above. With overlapping catchments allowed (reported `_EXCLmax`) it is at most 1.4%, still 0.00% |

## Plain reading

1. **H-NB cannot repair the KiDS isolated-lens fail.**
   - With the supply cap kept, the edge can only move inward (S1).
   - The isolation cut leaves no lens whose basin closes inside its edge: the nearest is at 1.6–1.8 r_edge, even with projected (lower-bound) distances.
   - The only way the edge moves outward is to lift the cap, which breaks A6. That reported variant makes f30 worse.
2. **Where H-NB does bite, the neighbour's own lensing swamps it.**
   - T3 unmasked (reported): dense lenses carry +0.55 dex more raw signal than isolated ones (Z +31 / +48), while H-NB's own-term prediction there is −0.14 / −0.16 dex.
   - Where the neighbours contribute nothing (the clear zone), H-NB predicts only +0.004 / +0.004 dex. It truncates exactly where the neighbour's mass begins.
   - A framework-native neighbour-lensing model, or a spectroscopic group catalogue, is needed to isolate the own term.
3. **Massive systems are almost never bounded.** A closed basin needs a neighbour at least as massive. So the cluster- and group-scale halos that drive the shear excess (log M_ta 14–15) never bite in the halo model, and the X-COP clusters have no measured neighbour within D_crit. **H-NB is not the cure for the cosmic-shear excess.**
4. **The local data barely notice it.**
   - SPARC: one bite, and it is a projection artefact.
   - MW: r_nb 323 kpc ≫ 27.5 kpc, so the slope tension is untouched.
   - Groups: +0.008 dex, still closing.
   - It does lower the LG timing mass by about 16%, which helps a little.
5. **The data pattern that motivated H-NB is not explained by it.** That pattern is isolated lenses wanting a farther edge and crowded massive systems wanting less mass at large radius. The first needs more supply (CFG557 already showed growth wants less). The second sits in systems that H-NB's closure rule leaves unbounded.

## MUTATE

- **M1 (r_nb → ∞) reproduces candidate B exactly** in every arm:
  - T2: f30 and stack-P stacks, max relative change 0.
  - T1: SPARC rms identical.
  - T4: MW profile identical.
  - T5: P2 = CFG543's +0.05961 / +0.04349 (d 0).
  - T6: R(k) = CFG556 primary (max |dR| 0).
- **M3 (r_nb = 0.5 r_edge for every f30 lens) bites:** native Δχ² +57.4 / +61.9. CONTEXT: CFG529 A 45.6 → 80.3, 35.8 → 71.2.
- **M2 (shuffled neighbour sets within cells) FAILS as a tooth, and that failure is the finding.**
  - With neighbours shuffled, the frozen clear-zone statistic still shows a strong "trend": A_data −0.442 (Z −9.4) / −0.478 (Z −7.7). The frozen T3 statistic therefore manufactures a negative amplitude from the mask itself.
  - The cause: dense lenses keep only their inner bins (18% vs 80% kept), and the pooled data/B ratio changes with radius.
  - So the T3 data amplitudes (including bracket S's −0.18 / −0.27, Z −4.9 / −5.3) are mask artefacts and carry no physical weight.
  - On the unmasked statistic M2 behaves as required: shuffled +0.012 ± 0.021 / +0.005 ± 0.023, so the real environment trend (+0.55) is removed.
- **Post hoc (written after the first T3 run, no verdict weight).** A bin-matched amplitude (dense and isolated per-bin ratios combined with the same weights):

  | | real | shuffled |
  |---|---|---|
  | canonical | +0.138 ± 0.062 | −0.103 ± 0.048 |
  | alt | −0.007 ± 0.096 | −0.112 ± 0.048 |

  Even this is not fully free of the selection. The real-minus-shuffled difference is ≥ 0, so there is no H-NB-like deficit, but H-NB predicts essentially zero there anyway.

## Verdict (frozen order)

- **H-NB is RULED OUT as a repair of the census-edge fail.** T2 is NO CHANGE on both footings.
- It is not SUPPORTED: T3 is WEAK / NOT DIAGNOSTIC, and its frozen statistic fails M2.
- T1 is not WORSENS: one spurious bite, +0.0005 dex.
- T4 is UNCHANGED.
- T5 is CHANGED: +0.009 / +0.008 dex, still CLOSES.
- T6 (CONTEXT ONLY) is NEGLIGIBLE.
- The fail was verified as hard as a win:
  - Bracket S (maximal bite) and U-drop give the same T2 class.
  - The T1 bite was traced to a background group.
  - The T6 result holds with overlapping catchments allowed.

## Native PM spec (written, NOT run)

At each census refresh of the cfg596/cfg640 engine (same cadence, no new constant):
1. Take the catchment list the engine already builds: turnaround-ball systems with centre x_i, retained baryons M_b,i, census f_ret,i, supply S_i = 5.364 M_b,i/f_ret,i, and M_tot,i = M_b,i + S_i.
2. Build a periodic KD-tree on the centres. For each i, query the systems j with M_tot,j ≥ M_tot,i within R_s,i = r_edge,i (1 + sqrt(M_tot,j,max / M_tot,i)), using exact 3-D distances (no projection).
3. Find r_j by bisection on g_i(r) = g_j(D_ij − r), with both candidate-B profiles (`cfg644_lib.r_pair`; on the mesh, the systems' spherically averaged baryon profiles replace point masses). Set r_nb,i = min_j r_j.
4. Set the phantom-source radius to r_eff,i = min(r_edge,i, r_nb,i). The settled mass is phantom_i(<r_eff,i). Only that amount is drawn from the R5 shell; the remainder stays as unconverted cold particles in the catchment (R3 conserved).
5. r_nb is computed from the census (un-truncated) profiles. A fixed-point iteration with truncated profiles is a declared variant.
6. Diagnostics: r_nb/r_edge by mass decade; settled mass removed; P_grav/P_S0 with CFG636's scorer.
7. MUTATE: r_nb ≡ ∞ must reproduce the engine bit for bit. Shuffling the centres within mass bins must remove any environment dependence of the removed mass.

Cost is O(N_sys log N_sys) per refresh. Expected from T6: a negligible change. A PM run is not recommended unless a new closure rule is posited.

## Disclosures (dated 2026-10-12)

- **Implementation choices not spelled out in the criteria:**
  - KiDS query radius 7 Mpc comoving, enough for the outermost bin's R plus a neighbour edge.
  - Purity annulus 4–6 Mpc comoving (the CFG502/509 values).
  - T1/T5 projected separation = D_s sin θ, the strict lower bound. The first local run used the arc D_s·θ; switching to D_s sin θ changed the closing counts slightly and moved T5's P2 by 2e-5, with no class changed.
  - r_nb below the node range is clamped at x = 0.01 r_ta. No f30 lens is affected.
- **First T3 run:** it crashed in the null (log of a negative pooled ratio in a noisy band). I made the null nan-safe, restricted relabelling to lenses with kept bins, chunked the r_nb solver over owners to cut memory, and added the reported (post-hoc) bin-matched and unmasked amplitudes. All T2 numbers were identical between the runs.
- **Memory:** the KiDS run's peak footprint was 1.51 GB, about 0.5% over the 1.5 GB budget; RSS including the memory-mapped FITS read about 6 GB.
- **Label errors in the output:**
  - The key `rnb_over_redge_weighted_pct` in `cfg644_kids_results.json` holds unweighted lens percentiles (f30: 1/5/16/50% = 2.03/2.40/3.08/5.60 canonical, 2.23/2.63/3.38/6.15 alt).
  - The first printed "reported:" line in each footing's T3 block belongs to the `primary` split; the second belongs to `bracket_S`.
- **Neighbour masses:** KT2017 bodies use Υ_K = 0.6 + the SPARC gas fit (the CFG4/CFG11 convention). KiDS neighbours use the CFG525 M_gal rule. Hot gas is not included, so neighbour masses are low and closure is less likely. Projection works the other way (more bite).
- **Needs (no download made):**
  - a spectroscopic group catalogue overlapping KiDS (for example GAMA groups), to isolate the own term at r > r_nb;
  - an X-ray or SZ cluster catalogue with masses (for example MCXC), for the X-COP environment;
  - Local Volume distances (for example CF4) for the T1/T5 3-D variant.

## Run
```
OMP_NUM_THREADS=1 nice -n 10 python3 cfg644_kids.py ; CFG644_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg644_kids.py
nice -n 10 python3 cfg644_local.py ; CFG644_MUTATE=1 nice -n 10 python3 cfg644_local.py
OMP_NUM_THREADS=1 nice -n 10 python3 cfg644_halo.py ; CFG644_MUTATE=1 ... ; CFG644_EXCL=max ...
```
