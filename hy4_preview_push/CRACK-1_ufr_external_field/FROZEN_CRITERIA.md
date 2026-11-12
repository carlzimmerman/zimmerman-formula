# CRACK-1 FROZEN CRITERIA: three readings of the ultra-faint / X-COP pair (2026-11-12)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical a0 = 9.3603e-11 and
alt 1.1312e-10 m/s^2, **never pooled**; the same label is required on both. Committed alone, before any CRACK-1
script exists or any CRACK-1 number is computed. The id CRACK-1 was checked free (no `hy4_preview_push/CRACK*`, no
`CRACK-1_ufr_external_field` anywhere, no commit subject naming CRACK or ufr_external_field).

## The question

FRM1 (`fable52_push/FRM1_formation_theory/`, label HOLDS EXCEPT) predicted 14 of 16 class offsets before the table
was read, and missed exactly two: **X-COP +0.496 +- 0.022 (22.3 se) and CLASH +0.553 +- 0.023 (23.9 se)**, both above
the baryon-loss ceiling d_max = +0.320 / +0.227 dex, with 77 % and 98 % of their points carrying more non-baryonic
mass per baryon than a0/g_bar, the absolute ceiling of the only upward channel the theory has. At the same time the
**MW ultra-faints sit at +0.592 +- 0.098 (6.1 se)** — the largest positive offset of any class, and the one FRM1
predicted and got right (+0.30 .. +0.70).

Those two together are the crux, and this lane takes them as one object:

> **The pair.** d(MW ultra-faints) = **+0.592 +- 0.098** and d(X-COP) = **+0.496 +- 0.022** (canonical, LOCO);
> **+0.552 +- 0.098** and **+0.465 +- 0.023** (alt, LOCO). Both are positive at 6.1 se and 22.3 se.

Why it is a crux and not two separate problems: the two systems sit at opposite ends of every variable a formation
map could be built on. The ultra-faints are the smallest, faintest, most hosted, most stripped, earliest-forming and
lowest-field systems in the table (median log10 g_bar = -13.12, M_b of order 10^5-10^7 M_sun, 31 systems at 12 to
372 kpc from the Galaxy, all their gas gone). X-COP is the deepest unhosted well (median log10 g_bar = -10.70,
7 clusters, its hot gas measured inside the aperture, f_ret 1.06-1.10 from RB1). And the transfer-free anchor,
SPARC (median log10 g_bar = -10.60), sits at **+0.004 +- 0.012** — between them in field and at zero in offset. So
the offset is **U-shaped in the field, with its minimum at g_bar ~ a0 and a 0.5 to 0.6 dex rise at both ends**. No
monotone map F(v), with v any variable monotone in field or mass, can do that. That is the claim this lane tests.

Three readings could absorb the pair. Each is stated here as an equation, with a sign and a size in dex for **both**
members of the pair, **before anything is computed**:

1. **STRIPPING-INVERTED** — a formation-set amount plus tidal stripping.
2. **EXTERNAL-FIELD-REGISTERED** — the ambient field at assembly sets the normalisation, with an epoch factor
   kappa = Phi = (1+z_f)^(-3 alpha), alpha ~ 0.5-1 (kappa = 0.42 at z_f ~ 1).
3. **FELL-IN** — the amount is set when the galaxy fell in, at the host's field rather than its own.

## Data

- DD1's frozen table, unchanged: `fable52_push/DD1_deduce_from_data/dd1_table.csv` (main rows only, DD1's loaders,
  apertures and systematics apply). 3419 points, 626 systems, 16 classes.
- The record's host distances for the hosted legs: `real_research/data/dsph/lvd_dwarf_mw.csv`, column
  `distance_host` (kpc) — the same file X1 and RB2 used. Systems are matched by name to DD1's `sys` (case and
  spacing folded). If any of the 31 ultra-faints is unmatched, the lane is NO VERDICT (KA3).
- Nothing else. No new measurement is introduced anywhere in this lane.

## Statistic (DD1's and FRM1's, unchanged)

Per point X = g_obs/g_bar - 1, Y = log10(1 + X); the law's amount X_L(g) = (sqrt(1 + 4 a0/g) - 1)/2,
Y_L = log10(1 + X_L); the offset d = Y - Y_L(g_bar) (dex in g_obs at fixed g_bar). Per system the median over its
points; per class DD1's statistic (median of d_sys, se = max(1.2533 x 1.4826 MAD/sqrt n, sqrt(sum e_sys^2)/n),
se = e_sys for n = 1). Scorings: DD1's A->B, B->A and LOCO. **LOCO is the primary** (the pair's numbers are LOCO
numbers); A->B and B->A must agree for a leg to HOLD.

## The common machinery

All three readings are instances of FRM1's master equation: an amount X_f fixed at some event, then conserved
(f_C = f_b = 1 unless the reading says otherwise), so

    d = log10[ (1 + X_f) / (1 + X_L(g_bar)) ] .

d > 0 means the system carries **more** non-baryonic mass per baryon than today's law grants at its own field. In
the deep regime (X_L >> 1, X_L ~ sqrt(a0/g)) this is d ~ (1/2) log10(g_bar/g_f): **an amount fixed at a field
weaker than the system's own raises it, an amount fixed at a field stronger than its own lowers it.** That single
sentence is what decides all three readings, and it is what the pair is measured against.

## The three readings, pre-registered

### R1 STRIPPING-INVERTED

    X_f = X_L(g_bar)          (the amount is fixed at the system's own assembly field)
    X   = X_f * f_C / f_b     with f_C <= 1 the charge the host left, f_b <= 1 the baryons it left

The reading's claim: the ultra-faints are satellites of the Galaxy, the deepest and most stripped in the sample,
and the extended non-baryonic charge is what a host removes first. So f_C < 1 with the baryons (stars) largely
kept, i.e. f_C/f_b < 1.

**Pre-registered prediction.**
- MW ultra-faints: **d < 0**, in the band **[-1.05, -0.30]**, central about **-0.7**. The band is the one FRM1
  pre-registered (and confirmed) for the record's own stripped family — the tidal dwarfs at -0.687 +- 0.115 and
  DF2 / DF4 at -0.843 — because the reading asserts the ultra-faints belong to that family, and more so. The
  floor is d = -Y_L(g_bar) (X = 0).
- X-COP: **d = 0.00**, in the band **[-0.30, +0.30]**. An unhosted cluster has nothing to strip, and RB1 measures
  its baryons still in the aperture (f_ret 1.06-1.10), so f_C = f_b = 1.
- Differential d(UFD) - d(X-COP): **<= -0.30**, central about **-0.70**.

### R2 EXTERNAL-FIELD-REGISTERED

    X_f = kappa(z_f) * X_L(g_amb,f) ,   kappa(z_f) = Phi = (1 + z_f)^(-3 alpha) ,   alpha in [0.5, 1]

with g_amb,f the ambient field at assembly. Pre-registered: **g_amb,f = g_bar** — the field the assembling system
presents, with no contraction and no transfer — so that the only new ingredient this reading carries is the epoch
normalisation kappa. (Any contraction is folded into the reported parameter phi = g_amb,f/g_bar, below.)

Formation epochs, pre-registered from the record's assembly picture, not fitted:
- MW ultra-faints: **z_f = 8**, range [4, 12] (reionization-quenched, ancient stellar populations).
- X-COP: **z_f = 1**, range [0.3, 2] (massive low-z clusters).
- alpha: primary **0.5**, edge **1.0**. At z_f = 1: kappa = 0.354 (alpha 0.5) and 0.125 (alpha 1). The value
  0.42 quoted for "z_f ~ 1" is alpha = 0.5 at z_f = 0.78; both are inside the pre-registered range.

**Pre-registered prediction.** kappa < 1 for every z_f > 0 and every alpha > 0, and kappa is decreasing in z_f, so
- MW ultra-faints: **d < 0**, about log10 kappa(8) = **-1.4** (alpha 0.5) to **-2.9** (alpha 1); the band over
  z_f in [4,12] and alpha in [0.5,1] is **[-2.9, -1.1]**.
- X-COP: **d < 0**, about log10 kappa(1) = **-0.45** (alpha 0.5) to **-0.90** (alpha 1); band over z_f in [0.3,2],
  alpha in [0.5,1]: **[-1.1, -0.19]**.
- Differential d(UFD) - d(X-COP): **negative**, about **-0.98** (alpha 0.5, z_f 8 vs 1). The reading is monotone
  in z_f, so the earlier-forming class must be the lower one.

### R3 FELL-IN

    X_f = X_L(g_host(R_f)) ,   f_C = f_b = 1 afterwards

the amount fixed when the satellite fell in, at the host's field at the infall site rather than the satellite's
own. Host field, pre-registered from RB2's SE2 A1 convention: **g_host(d) = V_c^2 / d with V_c = 200 km/s** for
the Galaxy, d = the LVD `distance_host`. (That is M_host(<d) = V_c^2 d / G, the flat-rotation-curve host RB2 and
X1 used.) Reported edges: V_c = 180 and 220 km/s; the host less massive at infall (M_host(z_f) = f_M M_0 with
f_M = 0.5 and 0.25); and infall at twice the present distance.

**Pre-registered prediction.**
- MW ultra-faints: **d < 0**, strongly. At the median host distance (64 kpc) g_host = 2.0e-11 against the UFD's
  own g_bar = 7.6e-14 — the host's field is ~270 x the satellite's — so the amount is fixed at a far stronger
  field and the offset is about **-1.1 dex**; the band over the measured 12 to 372 kpc is **[-1.37, -0.80]**.
- Within the class, R3 predicts an ordering: **d increases with the host distance** (a satellite that fell in
  closer sat in a stronger field and must be lower today). Rank correlation of d_sys against log10 d_host over
  the 31 ultra-faints: predicted **positive**.
- X-COP: there is no host and no infall, so the reading reduces to X_f = X_L(g_bar) and **d = 0.00**, band
  **[-0.30, +0.30]** — unless the cluster's ambient field at assembly was below its own present field, which is
  the reading's one free parameter phi = g_amb,f/g_bar <= 1 (reported, not graded).
- Differential d(UFD) - d(X-COP): **negative**, about **-1.1**.

## Tests (per reading, per footing; each HOLDS / FAILS)

- **G1 the ultra-faint leg.** The measured LOCO offset of the MW ultra-faints lies inside R's pre-registered band
  for it, and A->B and B->A agree (both inside, or both on the same side of the band's nearer edge). HOLDS if so.
- **G2 the X-COP leg.** The same for X-COP's band.
- **G3 the differential.** The measured Delta = d(UFD) - d(X-COP) must be consistent with R's pre-registered
  central Delta within 3 se, se_Delta = sqrt(se_UFD^2 + se_XCOP^2) = 0.100 dex (canonical) / 0.101 (alt); and it
  must lie inside the Minkowski difference of the two bands. HOLDS if both.
- **G4 the pair.** **SURVIVES THE PAIR** if G1, G2 and G3 all HOLD; **FAILS THE PAIR** otherwise. Every miss is
  reported in dex and in se, for both members, on both footings.

Reported for each reading, graded by nothing: the value of the reading's own free parameter that would be needed
to close each miss —
- R1: the ratio f_C/f_b the master equation needs at fixed formation field (FRM1's budget: 4.08 for the
  ultra-faints, 4.52 for X-COP), against the reading's allowance f_C/f_b <= 1;
- R2: the kappa that would reproduce each measured offset, against kappa <= 0.354 from the epoch factor;
- R3: the field g_f at which each class's amount would have had to be fixed (solve X_L(g_f) = X_obs), against
  the host's field g_host the reading supplies; and for X-COP the contraction factor phi = g_amb,f/g_bar.

Also reported, and the reason the lane exists: **X1 the U-shape.** The LOCO offsets of the classes ordered by
their median g_bar — faint rotators, LG field dwarfs, MW ultra-faints, MW bright dwarfs, SPARC, ATLAS3D, groups,
KiDS, X-COP, CLASH — tested for monotonicity in g_bar, with the position and depth of the minimum and the size of
the two rises. This is the statement "no monotone formation map survives the pair", made as a measurement.

## Labels (per reading, per footing)

- **SURVIVES THE PAIR** — G1, G2, G3 all HOLD.
- **FAILS THE PAIR** — at least one of G1, G2, G3 fails. The label is followed by the leg that failed, the size
  of the miss in dex and in se, and the parameter the reading would need.
- **NO VERDICT** — a known answer fails, or the two footings disagree.
- The lane's headline is the three-reading verdict: which of R1, R2, R3 survives the pair, on both footings.

## Known answers (must pass, else NO VERDICT)

- **KA1** FRM1's LOCO offsets for the pair reproduced to 1e-9, both footings: canonical +0.5920 +- 0.0977 and
  +0.4955 +- 0.0222; alt +0.5520 +- 0.0979 and +0.4650 +- 0.0229.
- **KA2** the readings' algebra, on the real points: (a) with kappa = 1 and g_amb,f = g_bar, R2's d is 0 to 1e-12
  on every point; (b) with f_C = f_b = 1 and g_b,f = g_bar, R1's d is 0 to 1e-12 on every point; (c) R3's d with
  g_f = g_bar is 0 to 1e-12 on every point.
- **KA3** the host-distance data: 31 of 31 ultra-faints matched in the LVD table, every `distance_host` finite and
  positive.
- **KA4** synthetic truths on the real points, noise free, se from the real errors — each reading's own truth must
  make that reading's G1, G2, G3 HOLD, so that a FAIL is a finding and not a machinery artifact:
  (i) **stripping truth**: X := X_L(g_bar) x 0.05 on the 31 ultra-faints, everything else on the law. R1's G1 must
  HOLD and its G3 must HOLD.
  (ii) **fell-in truth**: X := X_L(g_host(d_host)) on the 31 ultra-faints, everything else on the law. R3's G1 must
  HOLD.
  (iii) **epoch truth**: X := kappa(z_f) X_L(g_bar) with the criteria's z_f (8 for the ultra-faints, 1 for X-COP,
  1 elsewhere) and alpha = 0.5. R2's G1 and G2 must HOLD.
- **KA5** the U-shape is not an artifact of the offset's definition: with every system put on the law (X := X_L at
  its own g_bar) every class offset is 0 to 1e-9 in all three scorings, both footings.
- **KA6** Lean: the algebra below compiles (see `CRACK-1.lean`), and its false twin fails.

## MUTATE (separate outputs `crack1_MUTATE.*`; each must change its stated outcome, else disclosed)

- **M1** the ultra-faints stripped: X := X_L(g_bar) x 0.10 on the 31 ultra-faint points (g_obs rebuilt). R1's G1
  must flip from FAIL to HOLD. If it does not, the G1 line is too strict and is disclosed.
- **M2** the host distances reversed across the ultra-faints (d -> d_max + d_min - d, i.e. the closest satellite
  given the farthest host field). R3's predicted UFD offset must move by >= 0.15 dex, and its within-class rank
  correlation must change sign.
- **M3** alpha = 0 (kappa = 1): R2's predicted offsets must all become 0.000 to 1e-12, and R2's G1 must still
  FAIL (the epoch factor is not what makes R2 fail by itself; the sign is).
- **M4** a0 x 2 on both footings: no reading's label may change (the verdict must be footing-robust), and G3's
  sign may not change.

## Lean (`CRACK-1.lean`, with a false twin that must fail to compile)

`XL_anti` (X_L decreases with the field: a stronger formation field grants less); `d_weaker_field_raises`
(g_f <= g_bar gives d >= 0 — the only way a formation-set amount lifts a system above today's law);
`d_stronger_field_lowers` (g_bar <= g_f gives d <= 0 — infall into a host's field can only lower);
`kappa_pos_le_one` (0 < kappa <= 1 for z_f >= 0, alpha >= 0) and `kappa_antitone_z` (decreasing in z_f for
alpha > 0); `d_of_kappa_le_one_nonpos` (kappa <= 1 with g_amb,f = g_bar gives d <= 0 — the epoch factor can only
lower); `strip_lowers` (f_C <= 1, f_b >= f_C gives d <= 0); `pair_needs_source` (d > 0 for a class implies
X_f > X_L(g_bar): a positive offset is a source, not a transfer); `u_shape_not_monotone` (if d at the two ends of
an ordered field range both exceed d in the middle, no monotone function of the field reproduces all three).

## Record checked first (quoted, not redone)

- FRM1 (criteria 462eaa806d + fed1bc94a4; result 04f69b8b6f): the pair's LOCO offsets above; the baryon-loss
  ceiling d_max = +0.320 (X-COP) and +0.227 (CLASH); 77 % / 98 % of cluster points above a0/g_bar; the transfer
  budgets (UFD f_b 0.053, f_C 4.080; X-COP f_b 0.111, f_C 4.515); the tidal dwarfs -0.687 +- 0.115 and
  DF2 / DF4 -0.843 as the record's calibration of what stripping does; SPARC +0.004 +- 0.012; the free rule N1
  (law + free F(system depth)) at 0.213 dex against the 0.284 dex reference, failing 10 of 16 classes.
- DD1 (origin 91c159b746): NO RULE AMONG THE CANDIDATES; reference scatter 0.284 dex; P3 the best full-cover rule
  at 0.219 dex failing 12 classes; the MW ultra-faints the worst class under 10 of 13 candidates.
- RB1: X-COP last-radius f_ret 1.095 [0.885, 1.259]; at R500 1.057 [1.046, 1.072].
- RB2 (closure_2026_11_09): B FAILS HIGH on the MW ultra-faints, +0.634 [+0.433, +0.865] canonical; the host
  mass convention M_host(<d) = V_c^2 d / G, V_c = 200 km/s (MW) used by X1 and RB2; the LVD `distance_host`.
- DG1: the hosted classes' offsets do not follow a predicted per-system history (rank +0.06 in the ultra-faints).
- X1: the external field puts DF2 / DF4 at -0.558 / -0.536 (canonical) — the EFE lowers, it does not raise.

## Disclosures (seen before this file)

- Every FRM1, DD1, RB1, RB2, DG1 and X1 number quoted above, from their RESULT.md files and outputs.
- The DD1 table's column list, its 3419 / 626 / 16 counts, and the ultra-faints' per-point field range
  (log10 g_bar -14.17 to -12.51, one point per system, 31 systems).
- The existence and column list of `real_research/data/dsph/lvd_dwarf_mw.csv` (`distance_host` present for all 31
  ultra-faints, 11.8 to 371.6 kpc), used by X1 and RB2 before this lane.
- No CRACK-1 number of any kind. No prediction in this file was computed; the sizes quoted in the pre-registration
  are hand estimates from the deep-regime limit d ~ (1/2) log10(g_bar/g_f) and from FRM1's quoted numbers, and are
  marked as such. They will be replaced by the computed values, and any disagreement will be reported.
- Hand estimate of the outcome: all three readings FAIL THE PAIR. R1 and R3 fail the ultra-faint leg by 1.3 to
  1.7 dex with the wrong sign, and inherit X-COP's +0.50 dex with no channel; R2 fails both legs, and fails the
  differential because it is monotone in z_f while the measurement has the earlier class HIGHER. If the lane
  returns anything else, the hand estimate is reported as wrong.

## Operational

One thread, small memory, minutes. `crack1.py` -> `crack1.json` / `crack1.out`; `crack1.py --mutate` ->
`crack1_MUTATE.json` / `crack1_MUTATE.out`. Lean via `lake env lean` in the record's build
(`fable_independent_2026/lean_2026`); `compile.txt` with no home paths. Commit with explicit paths; push by a
temporary sparse worktree.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
