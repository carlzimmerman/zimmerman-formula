# HY1 RESULT: the a0 law with kappa free plus the CMB's cold component. NO VERDICT on both footings by the frozen M3 rule; under it, SPARC and X-COP fail at every kappa

Quarantined TEST lane under the owner's 2026-11-08 lift ("Lift it, launch HY1"; OWNER_DECISION_2026-11-08_HY1_RULE_LIFT.md).
The component is the record's cold dark energy (v3s's K(Q) dust); it is never called dark matter and there is no particle.
Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

- Criteria: `FROZEN_CRITERIA.md`, 2fbb41123a, committed alone and pushed before any script or number.
- Scripts: `hy1.py` (subcommands `sparc`, `battery`, `kids`; each column in its own process) writes `parts/*.json`.
  `hy1_grade.py` assembles `hy1.json` / `hy1.out` and the mutation outputs `hy1_MUTATE.json` / `hy1_MUTATE.out`.
  Run logs: `run_sparc.txt`, `run_battery.txt`, `run_kids.txt`.
- One thread, nice 12. Peak RSS: 0.10 GB (SPARC), 0.09 GB (battery), 0.19 GB (KiDS). No Boltzmann code was loaded.
  CMB3 (`python3 cmb3.py`) was running the whole time. Nothing was downloaded.
- f is pinned by F1A: R = 5.409583 (canonical) and 5.412268 (alt). The captured amount is f_cap R = 4.1113 / 4.1133
  times M_b,sys. The dust sits where the record's own dynamics put it: KD1 model P at mu* (8.89e6 Mpc^-1, the only mu_K
  that BBN allows). Its core is 0.35 pc, so in every column it acts as a central point mass. a0(kappa) = a0(1/2) kappa/0.5,
  on 25 grid points from 0 to 2.

## Labels

| | canonical | alt |
|---|---|---|
| **Lane (frozen rule)** | **NO VERDICT** | **NO VERDICT** |
| Why | M3 does not bite, so the brief's rule makes C1 and C2 NO POWER. The other columns with power (C3a, C4, C5) still share a window, [0.05, 0.17] | same; shared window [0.05, 0.13] |
| **Reading under it (brief's kill clause)** | W_SPARC and W_X-COP are both **empty**, so they are disjoint: **FAIL** | both **empty**: **FAIL** |

Per column (window = the grid kappas where the column PASSES):

| Column | canonical | alt | power |
|---|---|---|---|
| C1 SPARC, per-galaxy U refit (rms <= 0.110, median U 0.50-0.80) | FAIL at every kappa: rms 0.465-0.658, U pinned at the 0.30 floor; **window empty** | FAIL at every kappa: rms 0.464-0.680, U 0.30; **empty** | NO POWER (frozen M3); M1 bites |
| C2 X-COP, NA2 per-bin gate | FAIL at every kappa: mean -0.62 to -0.81, rms 0.76-0.88, inner bin (0-0.25 R500) -1.09 to -1.15 dex; **empty** | FAIL at every kappa: mean -0.62 to -0.83, inner bin -1.09 to -1.16; **empty** | NO POWER (frozen M3) |
| C3a groups, step inside UA1's 95 % interval, both f* brackets | PASS for kappa <= 0.17 (edge 0.196) | PASS for kappa <= 0.13 (edge 0.152) | YES |
| C3b Bullet | NOT EVALUABLE (see disclosure 3) | NOT EVALUABLE | n/a |
| C4 KiDS G6 with kSZ gas, KX1's two-sided rule | PASS on [0.05, 0.35] (edges 0.044 / 0.399) | PASS on [0.05, 0.30] (edges 0.037 / 0.330) | YES (law passes; KD1's dust at kappa 1/2 fails) |
| C5 Cassini, planets (c_T and PPN quoted) | PASS on [0, 2] | PASS on [0, 2] | YES (record MUTATE) |
| C6a cosmology at kappa 0 (replays) | PASS: CMB lensing chi^2 8.560 <= 18.48; fsigma8 Rf 1 (CE2 convention, no independent power); forest lambda_J 3.5e-7 Mpc | PASS | YES (KD1 I0 -> 0: chi^2 888.5) |
| C6b law on the linear web, kappa > 0 | NOT EVALUABLE (cmb3.py running) | NOT EVALUABLE | n/a |
| Shared window of the columns with power | [0.05, 0.17] | [0.05, 0.13] | |

## Known answers (all PASS before any graded number; M2 f -> 0 is this set)

| KA | canonical | alt |
|---|---|---|
| KA1 F1A R_B2, chi^2 cold (read exactly) | 5.4095831638392, 3740.157 | 5.41226812314077, 3740.301 |
| KA2 SPARC law only at kappa 1/2 vs QX8 exact | rms 0.05604651, U 0.58; abs(d) 1.4e-17 | 0.05582588, U 0.52; abs(d) 6.9e-18 |
| KA3 X-COP law only (GB1 KA20) | +0.467499 (abs(d) 4.9e-8) | +0.434523 (abs(d) 5.6e-8) |
| KA3 KD1 G2 / G1 with KD1's own amount 4.1110 / 4.1121 | -0.702864 / 0.802677; G1 Z -0.718657, rms 0.816510 (abs(d) <= 1.1e-16) | -0.714392 / 0.809485; -0.735136 / 0.827508 |
| KA3 KD1 uniform X-COP need | 4.17860 (abs(d) 0) | 3.78326 (abs(d) 0) |
| KA4 KiDS law vs KX1 E_b, sigma_tot | max abs(d) 0 | 0 |
| KA5 groups law only vs GB1 L0 G3; step | identical; 0 | identical; 0 |
| KA6 Solar System law only vs GB1 L0 G8 | identical | identical |
| KA7 KD1 G9a chi^2 (read) | 8.559852 | 8.560406 |

## MUTATE (`hy1_MUTATE.out`)

- **M1, kappa -> 0 (component only).** C1 FAILS on both footings (rms 0.4647 / 0.4641, U at the 0.30 floor), so M1
  **BITES**. C2 and C4 also fail there. The quarantined fried-chicken numbers (ACDM v2.0) are NOT a known answer for
  this M1. They come from NFW and coreNFW halos with feedback knobs, which are simulation-shaped and cannot be imported,
  and they are not the K(Q) dust's profile. They are cited only to say that.
- **M2, f -> 0.** This is the KA set above. Every value reproduces to 0.
- **M3, f -> 2R at fixed kappa.** It **DOES NOT BITE** on either footing.
  - At every grid kappa, doubling the dust worsens SPARC (rms +0.208 to +0.215) and X-COP (rms +0.240 to +0.254) together.
  - The two moves never point in opposite directions, so by the brief's rule C1 and C2 read NO POWER.
  - The reason is physical, not a lack of resolution. The brief's control assumed that galaxies want less of the
    component and clusters want more. With the dust where the record's own dynamics put it (a central point mass),
    both columns are already over-filled, so both want less.
  - This is the same kind of gap in the control's design as KX1's M1. It fixes the frozen label at NO VERDICT.

## The readings that matter (reported; they do not change the frozen label)

- **SPARC cannot hold the dust at any kappa.**
  - The disc M/L sits at the 0.30 floor at every kappa, and the rms is 4-6 times the line.
  - The largest dust fraction discs can keep and still pass is eps_max <= 0.037 of the captured amount
    (f_ret <= 0.154 of the baryons), canonical, at kappa 0.35. Alt allows <= 0.035 at kappa 0.30.
  - Where the law alone fails SPARC (kappa outside 0.30-0.64 canonical, 0.25-0.53 alt), no amount passes.
  - The cosmic capture is 4.11. Discs would have to shed at least 96 % of it (98.8 % at kappa 1/2, canonical).
- **X-COP cannot be fitted by the point-mass shape at any kappa or any amount.**
  - Fitting the amount F_X freely (0.07-0.72 Mb_last, against the captured 4.11) never passes the per-bin gate. The
    best rms is 0.100 at kappa 2 (alt), but the bins still fail.
  - The cusp over-fills the core by 1.1 dex. This is KQ1's finding again, now at every kappa.
- **KiDS and the groups do open a window, at low kappa.**
  - At kappa 0.05-0.35 a point mass of 4.1 M_* inside a weaker law reproduces the 100-300 kpc lensing. In the deep
    regime, b a0(kappa) ≈ a0(1/2).
  - The groups' step (UA1) is supplied at kappa <= 0.17 / 0.13.
  - So the columns with power share kappa 0.05-0.17 (canonical) and 0.05-0.13 (alt).
  - In that window SPARC sits at rms 0.47-0.50 and X-COP's inner bin at -1.09 dex.
- **Uniform-b bracket (not framework-native, reported only).** Even with the dust tracing the baryons at every radius:
  - SPARC fails at every kappa (best rms 0.226).
  - X-COP passes only at kappa 0.35-0.60 (canonical) or 0.30-0.50 (alt).
  - KiDS passes only at kappa 0.03-0.20 (canonical) or 0.02-0.17 (alt).
  - The three windows are pairwise disjoint or empty. The most generous shape the record could be asked for does not
    give one kappa either.
- **Solar System.** Cassini use rises as kappa/0.5: 2.8e-8 at kappa 1/2 and 1.1e-7 at kappa 2 (canonical). The worst
  planet use goes from 0.21 / 0.19 at kappa 1/2 to 0.85 / 0.76 at kappa 2, still inside the line of 1.
  - c_T: the principal part is GR's at any kappa. The mass-term bound (5.1e-32 / 6.2e-32 at kappa 1/2) stays below
    1e-30 even if it scales as kappa^2.

## Disclosures

1. **Push and run tree.** The shared checkout's local main is diverged from origin (187 behind, 79 ahead), and lanes
   UA1 and F1A's JSONs are on origin only. So HY1 ran in a sparse detached worktree at origin/main, outside the repo.
   - KX1's KiDS data (Brouwer+2021, gitignored) were reached through an untracked symlink to the main checkout's copy.
     The symlink is not committed.
   - The first battery run stopped on that missing file before any number. It was rerun unchanged, and its log was
     overwritten.
2. **C1 constants.** C1 uses QX8's rounded footing a0 (9.3603e-11 / 1.1312e-10), as the record's SPARC grade does.
   The battery and KiDS columns use QX5's unrounded values. Each column scales its own a0(1/2) by kappa/0.5.
   - The dust uses QX10 iter_3's total M_b,sys and GK = 4.30091e-6 with QX8's kpc.
   - T was carried and T = 0 agreed on PASS/FAIL at every kappa, so no C1 cell was NOT EVALUABLE. At kappa != 1/2,
     carrying T is QX10 iter_3's stated approximation.
3. **C3b Bullet was not run.** The frozen rule called for it because the shared window is non-empty, under 1 GB.
   - The only Bullet machinery on disk (DB1/UX6, through NA2's child) is measured at 1.19 GB (NA2) and 1.48 GB (CE2).
   - Running it would have breached the RSS line while CMB3 ran on the same machine. It is NOT EVALUABLE under the
     frozen RSS clause.
   - It cannot change the label: PASS was already impossible with C1 and C2 at NO POWER.
4. **C6b was not run.** `python3 cmb3.py` was running at grading (pids 14241, then 15905), so the frozen rule makes C6b
   NOT EVALUABLE. It cannot change the label either.
5. **C3a step is law-relative.** HY1 compares the hybrid's step over the kappa = 1/2 law, not UA1's SPARC-anchored step.
   The anchor (+0.027 / -0.0006) is far smaller than the interval. GB1's strict per-group rule, reported, never passes
   (at most 9 of 20).
6. **C4 capture base.** The KiDS dust base is the lens stellar mass (KX1's sector convention), not stars plus hot gas.
   This is generous to the hybrid.
7. **Groups and C5 at kappa 0.** C3a and C5 pass at kappa 0 because the component alone supplies the groups' step, and
   with no law there is no Solar-System anomaly. That is why their windows start at 0.
8. **M3 and power.** By the frozen rule, C1 and C2 are NO POWER. Other controls show they do discriminate:
   - SPARC passes for the law alone at kappa 0.30-0.64.
   - X-COP fails the law alone.
   - The uniform-b bracket passes X-COP at kappa 0.35-0.60.
   - That is the reading. The label stays as frozen.
9. Every number in this file is read from `hy1.json`, `hy1_MUTATE.json` and `parts/*.json`. The edges are 30-step
   bisections, reported only.

## In plain words

The owner lifted the no-cold-component rule to ask one question: can the a0 law, with its strength kappa left free, live
alongside the cold component the CMB demands (5.41 times the baryons), so that one setting fits galaxies, clusters,
lensing and the Solar System together? The record's own dust physics decides where that component sits: it falls into
every galaxy and cluster and collapses to a tiny central lump of about four times the baryons. Put there, it wrecks
every disc rotation curve at every kappa (four to six times the allowed scatter, even at the lowest stellar
mass-to-light), and it over-fills every X-COP cluster core by about a factor of twelve at every kappa and at any amount.
Weakening the law (kappa 0.05-0.17) does let the lump reproduce the KiDS lensing around isolated galaxies, the group
masses and the Solar System. But discs would have to throw away at least 96 % of what the CMB puts there, which is fact F2
again. Even smearing the component along the baryons, which the record's physics does not do, leaves SPARC failing
everywhere and the cluster and lensing windows apart. The lane's frozen label is NO VERDICT on both footings. The reason
is the brief's own control: it expected galaxies and clusters to pull the amount in opposite directions, but here both
are over-filled. Under that label the answer is plain: no single kappa makes the law plus the CMB's component work. The
hybrid does not cross the measured boundary; it restates it.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
