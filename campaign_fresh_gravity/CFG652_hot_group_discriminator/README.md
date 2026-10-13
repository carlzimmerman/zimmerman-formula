# CFG652: hot-gas groups, Theory v2 (condensed source) vs candidate B (all-baryon source). Verdict on raw KiDS lensing around 131 eFEDS X-ray groups: BOTH EXCLUDED, on both footings and under every frozen variant

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone in 11c7906ef. That was after the theory commit bc0dd7975 and before any source
  was staged, any condensed mass computed or any ESD measured.
- **Settings:** κ = ½ is FITTED. Footings are canonical 9.3603e-11 / alt 1.1312e-10, never pooled. "Cold energy" throughout; its
  mass is still required. No particle species. Not "theory closed". No ΛCDM halo, mass function or standard-MOND yardstick
  enters any verdict.
- **Data:** all read from disk; nothing was downloaded.
  - eFEDS X-ray groups (Bahar+22): measured M_gas500 and the X-ray aperture.
  - KiDS-1000 DR4.1 SOM-gold sources: 1.24 M in the G9 box.
  - KiDS bright sample: LePhare stellar masses.

## 1. Theory: where (a) and (b) differ (`cfg652_derive.out`, no data)

The two models share everything except the phantom's source: the same baryons, catchment, supply and infall (CFG637 Method A).
- (a) Theory v2: the phantom comes from the condensed baryons only. Leftover supply stays as unsettled, collisionless cold
  energy.
- (b) Candidate B: the phantom comes from all baryons.

**What separates them is whether an unsettled reservoir survives in (a).** That depends on the catchment rule and on how far
the gas extends, both inherited inputs.

| regime | where it holds | (a) vs (b) |
|---|---|---|
| **No reservoir** | M_b ≲ 10^13, or gas truncated at R_X | (a) is **lower** than (b) beyond the members: ratio 0.35–0.9 at 0.25–1.7 Mpc, outer-band A_out −0.08 to −0.29 dex. The inner profile is identical. (b)'s phantom ∝ √M_b is cut at 0.3–0.5 r_ta; (a)'s ∝ √M_cond runs on to r_ta |
| **Reservoir** | M_b ≳ 10^13.3 with extended gas | (a) is **higher**, ×2–8 at 0.1–0.8 Mpc. The leftover cold energy is core-concentrated (CFG637's shape): "plain cold matter" piles into the centre |

- **Brackets** on M_b 10^13.3, f_hot 0.8: the outer-band contrast spans −0.13 to +0.57 dex.
  - The gas extent decides the sign: 1 R_X gives −0.12, 4 R_X gives +0.57.
  - The catchment rule shifts it too: P2 gives −0.01.
  - Angular momentum q, ε, N, the BCG fraction and the member radius move it by at most 0.07.
- **At fixed M_cond (2e12) with rising hot gas:**
  - (b) rises smoothly (dA_out/dlog M_b = +0.26).
  - (a) stays flat (+0.02 per step) until the reservoir switches on, then jumps (+0.6 overall).
- **The discriminating observable** is therefore ΔΣ at 0.25–1 Mpc as a function of hot gas at fixed condensed mass. Its sign
  is set by the reservoir threshold, so it cannot be quoted as a single number.
- **Forecast** (shape noise only):
  - groups at M_b ≈ 10^13.5 need 3–6 for 3σ (11–25 with a ×4 allowance);
  - groups at 10^13 with f_hot 0.6–0.8 need 340–1070 (1400–4300 with the allowance).
- **MUTATE M1** (hot gas relabelled as condensed): (a) collapses onto (b) exactly.

## 2. Test on raw lensing (`cfg652_test.out`)

**Sample.**
- 148 groups pass the frozen cuts (0.1 ≤ z ≤ 0.5, measured gas, source coverage ≥ 0.6).
- 17 have M_cond = 0 under the frozen recipe (no bright-sample mass in the window); see section 3.
- That leaves 131 groups. Medians: z 0.31, M_cond 2.1e11, M_hot 7.5e12, f_hot 0.967. These are hot-gas-dominated systems.

**Measured stack** (boost-corrected, randoms subtracted):

| R (kpc) | 53 | 78 | 115 | 169 | 248 | 363 | 533 | 783 |
|---|---|---|---|---|---|---|---|---|
| obs | 100 ± 102 | 126 ± 131 | 88 ± 69 | 57 ± 59 | 133 ± 39 | 72 ± 26 | 71 ± 15 | 43.5 ± 6.1 |
| (a) can | 300 | 302 | 212 | 159 | 97 | 61 | 42 | 26.5 |
| (b) can | 54 | 36 | 27 | 26 | 25 | 25 | 23 | 22 |

**Verdicts (frozen rule).**

| footing | variant | χ²_a (8 dof) | p_a | χ²_b | p_b | Δχ² (b−a) | label |
|---|---|---|---|---|---|---|---|
| can | primary | 22.9 | 0.0035 | 28.7 | 0.0004 | +5.8 | BOTH EXCLUDED |
| can | M_cond +0.2 / −0.2 dex | 23.7 / 21.6 | | 27.4 / 29.7 | | +3.8 / +8.1 | BOTH EXCLUDED |
| can | gas 1 R_X / 4 R_X | 36.2 / 49.2 | | 27.8 / 30.1 | | −8.4 / −19.1 | BOTH EXCLUDED |
| alt | primary | 22.3 | 0.0043 | 25.2 | 0.0015 | +2.8 | BOTH EXCLUDED |
| alt | M_cond ±0.2 dex | 23.4 / 21.5 | | 23.8 / 26.1 | | +0.4 / +4.6 | BOTH EXCLUDED |
| alt | gas 1 / 4 R_X | 37.1 / 49.2 | | 25.0 / 26.7 | | −12.1 / −22.5 | BOTH EXCLUDED |

**PRIMARY VERDICT: BOTH EXCLUDED.** All ten cells agree, so the label is not fragile.

**Why each model fails.**
- Beyond the members (248–783 kpc), the lensing mass is larger and more extended than either model predicts.
  - Outer-band A_out (obs/pred) is +0.16 ± 0.08 dex for (a) and +0.43 ± 0.07 dex for (b).
  - (b) falls short by ×2.7 throughout 0.25–0.8 Mpc.
- (a) is closer, with two problems:
  - it is short by about 40% in the outer band;
  - inside 200 kpc it predicts its concentrated reservoir at 160–300 Msun/pc². The data sit at 57–126, but with large errors.
- The gas-extent variants trade one problem for the other:
  - with gas to 4 R_X, (a)'s reservoir overshoots everywhere (A_out −0.08, χ² 49);
  - with gas to 1 R_X, (a) has no reservoir and is short everywhere (A_out +0.46).
- No frozen variant gives an extended halo of the observed amplitude.

**How hard the fail was checked.**
- **K1 cross-shear:** χ² 1.8/8, p 0.99, PASS.
- **Random-point signal** is −7 to +8 Msun/pc² (subtracted).
- **Boost:** the boost is 1.18–1.31 over the band and falls smoothly to 1.07 at 2.5 Mpc, which looks like real member
  contamination.
  - Unboosted, the band still reads 104 / 57 / 59 / 37 against (a) 97 / 61 / 42 / 26.5 and (b) 25 / 25 / 23 / 22.
  - Renormalising the boost to 1 at 1.7–2.5 Mpc lowers the band by 6–7%.
  - So the outer shortfall of both models does not come from the boost.
- **Missing 2-halo term:** neither model has one, and its omission raises the data relative to both. It could plausibly cover
  part of (a)'s 17 Msun/pc² gap at 783 kpc, but not (b)'s ×2.7. This is flagged, not quantified framework-natively.

**MUTATE.**
- **M1 PASS (bites):** (a) re-derived with the hot gas relabelled as condensed reproduces (b)'s χ² exactly (28.716 / 25.162).
- **M2 FAILED as designed.** Shuffling M_hot does not kill the split trend: the median shuffled D is −0.18 against σ_D 0.125.
  - Reason: f_hot = M_hot/(M_hot + M_cond) is dominated by M_cond here (f_hot median 0.97), so a shuffled f_hot still sorts the
    groups by condensed mass.
  - The split is secondary and carries no verdict weight. M2 shows it does not isolate hot gas.

**Secondary split** (reported only). At median f_hot = 0.967, D_obs = −0.09 ± 0.13, against predictions of +0.19 / +0.20 for (a)
and +0.06 for (b). It is not interpretable, for the reason given under M2.

## 3. Disclosures and post-hoc diagnostics (no verdict weight)

**Changes after the freeze.**
- 17 groups with M_cond = 0 were excluded. The models are undefined at zero condensed mass, and the frozen text did not foresee
  this case.
- 66 of the 148 groups have no bright-sample galaxy inside 0.2 R_X in the photo-z window. The frozen M_cond recipe is
  therefore noisy: an incomplete flux-limited sample, plus photo-z misses.
- Staging read the 17.7 GB catalogue through a memmap. The peak RSS reached 14 GB of file-backed (reclaimable) pages, above
  the ≤ 1.5 GB budget. Later stages ran at < 0.3 GB.

**POSTHOC=1** (`cfg652_test_POSTHOC.out`). Restricting to the 75 groups with a detected central and M_cond ≥ 1e11 gives:
- (a) χ² 6.7 / 6.6 (p 0.56 / 0.58) and (b) 20.4 / 18.5;
- Δχ² +13.6 / +12.0, which would read "(a) FAVOURED".
- It is FRAGILE under gas extent: 1 R_X gives NOT DIAGNOSTIC; 4 R_X gives BOTH EXCLUDED (can) / (b) FAVOURED (alt).
- The cut was chosen after the primary result was seen. It is a hint that the primary fail is partly driven by the noisy
  condensed masses, not a result.

## 4. What this means

**The lensing.**
- In the hot-gas-dominated eFEDS groups, the mass beyond the galaxies is more extended and more massive than candidate B's
  all-baryon phantom (short ×2.7).
- It is also more than Theory v2's condensed-source phantom plus the CFG637-derived reservoir (short about 40% in the band, and
  over-concentrated inside 200 kpc).

**The two models.**
- (a) is the closer of the two in the primary cell (Δχ² +6 / +3), but not by the frozen margin.
- The sign of the (a)–(b) contrast depends on inherited inputs (gas extent, catchment). The test therefore really constrains
  the reservoir's amount and placement, the CFG637 open question, more than the choice of source.

**What it does not say.**
- It does not say the data favour any other model.
- The CFG637 statement stands: no derived reservoir rule passes the cluster scale.

## 5. Data needs (for a decisive version; owner's approval, not fetched)

The forecast says the M_b ≈ 10^13.5+ regime decides with tens of groups. What limits this test is M_cond, not the lensing.
- **Spectroscopic member stellar masses for the eFEDS groups:** the GAMA G09 DR4 StellarMasses + G3C tables.
  - The G3C files are already on disk (CFG471 fetch). StellarMassesLambdar is about 100–200 MB (estimated), from Data Central.
- **A larger X-ray sample with measured gas overlapping KiDS/DES/HSC:**
  - eRASS1 cluster catalogue (on disk: `erass1cl_primary_v3.2.fits`). Its gas masses are not in the primary table, so a
    gas-mass value-added table would be needed (VizieR, < 10 MB, estimated).
  - XXL-100/365 gas masses (VizieR, < 1 MB) with HSC/CFHTLenS overlap.
- **Optional:** HSC-SSP PDR3 shear for eFEDS. It is several GB, the deepest overlap, and needs registration.

## Files

- `cfg652_model.py` holds the model library (sha256 04352d4e…, unchanged since the freeze).
- `cfg652_derive.py` (theory, about 15 min) writes `cfg652_derive.out` and `_results.json`.
- `cfg652_stage.py` stages the sources to `_external_data/cfg652_work` (not committed).
- `cfg652_test.py` runs in stages:
  - `CFG652_MODE=inputs`, then `measure`, then `models` (about 3 h, one process, about 50 MB), then `score`;
  - the score stage also runs with `MUTATE=1` and with `POSTHOC=1`.
- Outputs: `cfg652_test{,_MUTATE,_POSTHOC}.out` and `_results*.json`.
