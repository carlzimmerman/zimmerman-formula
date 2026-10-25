# X30_sheet_cluster_profile: FROZEN CRITERIA (committed alone, before any script or number of this lane)

κ = ½ FITTED. Footings canonical a₀ 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. The cold sector ("cold energy",
Ω_c/Ω_b = 5.364) is gravitating field mass, never a particle. Theory frozen as v3s
(`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §7–8); target region = X26's scenario-B sheet
(`rebuild_2026_10_22/COLD_SECTOR_SPEC_2026-10-24.md` §2.2, §4 "cluster profile"). Nothing is fitted. Never "theory closed".
Never "the data favour the framework". The X29 low-z S8 test belongs to a peer lane and is not done here.

**Seen before freezing.** COLD_SECTOR_SPEC; V3S verdict §7–8; READMEs, criteria and scripts of X26, X23_late_heated_cold,
X21, X2, X7; X13 README (INNER line); the X26 pass-mask npz and JSON (`A2_direct`, `A3_reported`); the record band values
quoted in §2 (X7 JSON `all` / `bins`, X2 JSON `rows."C* corrected baseline"`, X21 JSON `binned.V1`). No number of this lane's
model exists. The KT-tercile INNER and OUTER values do not exist in the record; they are produced in step 0 by the frozen
procedure of §2 and are not seen before the run.

## 1. Sheet points (inputs, not chosen)

- **All X26 scenario-B allowed (c_*, r, q)**: the AND of X26's `GRADED_B` masks (FP1, FP2, C-forest, C-s8, C-CMB, C-SPARC,
  C-groups, C-T1, C-T2, C-T3, C-KTb, C-dwarfs-c0, C-MW) in `X26_cold_sector_map/x26_pass_masks.npz`, collapsed over p. This is
  19 points (canonical) and 16 (alt), equal to the `allowed: true` rows of X26 JSON `A2_direct`. Read from the npz; asserted
  equal to the JSON list.
- **The 2 MGAS500 survivors** (X26 A3, reported): canonical c_* 10^3.125, r 0, q +0.375; alt c_* 10^3.25, r 0, q +0.5. Both are
  members of the list above; they are flagged, not added.
- Per cluster: c_s = c_* (σ_KT/100 km/s)^r (ρ_b/10⁻³ M☉ pc⁻³)^{q/2}, σ_KT = (kT/0.6 m_p)^½, ρ_b = M_b(<0.548 Mpc)/(4π 0.548³/3)
  per h cell, exactly X26's convention (`family_cs`, `CEL[...]["rho"]`). c_s is X26's z = 0 value (X26 applies no a^{2p−1}
  factor at the cluster redshifts; inherited, stated). p does not enter the cluster grades.

## 2. Measured bands and errors (record sources; bands as F1/X2/X7: INNER bins 0–2 = 0.15–0.46 Mpc, MID 3–5 = 0.46–1.42 Mpc,
OUTER 6–7 = 1.42–3 Mpc; C\* model, boost convention, both h cells 0.672 / 0.686)

Per cluster i and band B: n_i,B = Σ_B W B (D − leakP) and d_i,B = Σ_B W P_C\*·f_red (X21's / X23's construction from X7's
`x7_measure_percluster.npz`); A_B = Σn/Σd over a selection. A_pred,B = Σ d_i,B(C\* + cold) / Σ d_i,B(C\*), the X23/X26 ratio.

**(a) KT selection (106 clusters with KT > 0; X21's tercile edges 1.40 / 2.33 keV): graded at every sheet point.**
- MID terciles + MID slope b (vs log₁₀ KT/median): X21 `binned.V1.terciles` A ± s and `tests.V1.cells` b ± s_b (σ_STAT =
  max(bootstrap 2000, 30-patch jackknife), X21's keys). Canonical h 0.672: 1.10 ± 0.38 / 1.65 ± 0.32 / 2.13 ± 0.25,
  b +2.24 ± 0.74. These are X26's own cuts; re-graded here as a consistency line.
- OUTER all-KT, OUTER terciles, OUTER slope b_OUT; INNER all-KT; INNER terciles: computed in step 0 with X21's code
  (`bin_rows`, `sstat`, `wls`) on the band's n, d; σ_STAT with X21's seeds (terciles key 20100 + k, slope key 5010, all-KT key
  0) per band. Not in the record; frozen procedure, values unseen.
- INNER error: σ_IN = √(σ_STAT² + A_x² + A_RR²), X2's (e) propagation (A_x cross-shear and A_RR random-minus-random band
  offsets on the same selection), because no calibrated INNER systematic exists (X7 stores INNER A only) and X2's (e) INNER
  cross offset is ≈ −1.0 in A units (`rows."C* corrected baseline"`).

**(b) All 326 clusters, MGAS500 terciles (edges 7.37e12 / 1.73e13 M☉): graded only at sheet points with r = 0** (σ needs KT
otherwise; X26 frozen §3).
- OUTER terciles and OUTER all: X7 JSON `bins."terciles|<cell>"[t].OUTER.A_CAL ± s_CAL`, `all."C*|boost|<cell>".OUTER.A_CAL ±
  s_CAL`. Canonical h 0.672: T1 0.488 ± 0.296, T2 0.762 ± 0.135, T3 1.369 ± 0.103; all 0.929 ± 0.098 (alt h 0.672: 0.446 ±
  0.270 / 0.698 ± 0.123 / 1.257 ± 0.095; all 0.851 ± 0.090).
- INNER all-326: A from n/d as above with σ_IN of (a) on all 326 (X2 C\*: A_INNER 2.278 ± 0.284 jk, ± 1.048 with (e),
  canonical h 0.672).
- MID MGAS500 terciles: X26 A3's line (X7 A_CAL ± s_CAL); **reported only**, not re-graded (it is X26's reported line, not
  profile information).

**X13's selection correction does not apply**: this lane never splits sources (as X21).

## 3. Model (no new physics; X23_late_heated_cold / X26 machinery, verbatim)

X2's functions exec'd read-only; X7's npz; C\* potential (law + baryons, CFG814 gas "P", f_* 0.20, noclu EFE, offset, reduced
shear); isothermal hydrostatic cold fluid ρ_c ∝ exp[∫_r^{r_ta} g_b dr′/c_s²] in the baryon C\* field; normalisation
M_c(<r_ta) = min(cosmic mean at r_ta, fair share 5.364 M_b) (X26 `cold_mass`); the cold mass sources AQUAL with the baryons
and lenses. The only change from X26's `dmid` is that the per-bin vector Σ W P f_red is kept for all 8 bins and summed per band.
Derivation stated: hydrostatic equilibrium of an isothermal fluid, c_s² d ln ρ_c/dr = −g_b (self-gravity of the cold fluid
omitted in the profile, as X23/X26; it sources the lensing field).

## 4. Grades (per footing; a constraint passes only if it passes in both h cells)

Graded at every sheet point (KT selection, 106):
- G-MID-T1..T3, G-MID-b: |A_meas − A_pred| ≤ 2 s (consistency; must equal X26's grades);
- G-OUT-all, G-OUT-T1..T3, G-OUT-b: |meas − pred| ≤ 2 s;
- G-IN-all: |A_meas − A_pred| ≤ 2 σ_IN.

Graded additionally at r = 0 sheet points (326, MGAS500): G-OUT-Mall, G-OUT-M1..M3 (X7 CAL errors), G-IN-Mall (σ_IN).

**INNER weighting (frozen; X13: "INNER is too noisy", X2/X7/F1 never grade it).** INNER terciles are reported only. A point
whose only failing graded constraints are INNER ones (G-IN-all, G-IN-Mall) is classed **INNER-ONLY**, neither pass nor fail.

A point is PASS if every graded constraint passes, FAIL if any non-INNER graded constraint fails, INNER-ONLY otherwise.

## 5. Verdict classes (footings never pooled)

- **PROFILE PASSES (sheet survives)**: on both footings every sheet point is PASS.
- **PROFILE NARROWS THE SHEET TO …**: on both footings at least one point is PASS and at least one is FAIL; list the PASS points
  and whether the 2 MGAS500 survivors are among them.
- **PROFILE EXCLUDES THE SHEET (band)**: on both footings no point is PASS and none is INNER-ONLY; name the binding band(s):
  the graded constraint(s) failing at the most points, and every constraint failing at all points.
- **UNDECIDED**: step 0 fails; or the footings fall in different classes; or INNER-ONLY points exist and counting them as PASS
  vs FAIL changes the class (reason stated).

## 6. Step 0 (stop rule: all must pass, else UNDECIDED with no graded number)

- **K0a** X26 A2 direct KT-tercile A_pred and b_pred at every allowed point, both h cells, reproduced ≤ 1e-9 (from the band
  vector's MID sum).
- **K0b** X21 KT MID terciles A, s and slope b, s_b reproduced ≤ 1e-9.
- **K0c** X7 MGAS500 tercile MID and OUTER A_CAL and s_STAT, and X7 all OUTER A_CAL, reproduced ≤ 1e-9; X2 C\* INNER A, s_jk,
  s_tot (X2's `stats`, sysx) reproduced ≤ 1e-9.
- **K0d** X23 A1 KT-tercile A_pred at c_s,need × 3 and × 4 (fair/cosmic normalisation) reproduced ≤ 1e-9.

## 7. Checks, reported lines, MUTATE

- K1 band partition: Σ over the three bands of d equals Σ over all 8 bins ≤ 1e-12 (every cluster, one cell).
- K2 hydrostatic solver: X23's point-mass closed form ≤ 1e-4 and the c_s → ∞ uniform limit ≤ 1e-6.
- K3 zero-cold limit: d with M_c ≡ 0 equals the C\* d exactly.
- K4 peak RSS < 1 GB.
- **Reported only:** per sheet point and KT tercile (median cluster): cold-core radius r_c,cold (ρ_c = ρ_c(0)/2) vs the gas core
  0.15 R500; fraction of the retained cold mass inside 0.15 Mpc and 0.5 Mpc; retained fraction M_c(<r_ta)/fair share;
  M_c/M_b inside R500. INNER terciles (pred vs meas). The A_pred band ratio OUTER/MID vs measured.
- **MUTATE (`X30_MUTATE=1`, outputs `*_MUTATE.*`, exit 1):** m1 INNER and OUTER bin sets swapped on the measurement side;
  m2 hydrostatic sign flipped (ρ_c ∝ exp[−∫ g dr/c_s²]). **K0a and K0c must FAIL.**

## 8. Compute

One thread, `nice -n 15`, `PYTHONHASHSEED=0`, < 1 GB, minutes; no download; never `compute_queue/`. Commit by pathspec only;
no push. README numbers only from the committed `.out` / `_results.json`.
