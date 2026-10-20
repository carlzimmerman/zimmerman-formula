# CFG874 — FROZEN CRITERIA: every isolated Local Group dwarf, pooled, gas counted: satellite or small-system excess?

Frozen before any script (owner block 870–879). κ = ½ fitted; not theory closed.

## Why
CFG873 (5 field dwarfs, gas counted): UNDECIDED, se_D 0.10. CFG860 (stars only, Υ_V = 2) split the isolated dwarfs into
gas-free (6) and gas-bearing (5) groups, each too small. The LVD lists 11 dwarfs with a measured stellar σ at ≥ 300 kpc from
both the MW and M31 (CFG860's groups I0 + IG). That is the full Local Group supply. This lane pools them into one isolated
group, counts gas the same way for every dwarf, and asks one question at about twice CFG873's power.

## Sample (LVD csvs in real_research/data/dsph; nothing downloaded)
- Every LVD dwarf with a measured `vlos_sigma` (not an upper limit), r_h (`rhalf_sph_physical`, else `rhalf_physical`) and
  `M_V`, excluding CFG852's rotating / gas-rich set (LMC, SMC, WLM, NGC 6822, IC 1613, Leo A, Sagittarius dIrr, Pegasus dIrr,
  M 32) — identical to CFG860.
- **I (isolated):** ≥ 300 kpc from BOTH the MW (`distance_gc`) and M31 (`distance_m31`): Eridanus II, Perseus I, Andromeda
  XXVIII, Andromeda XVIII, Cetus, Tucana, Leo T, Antlia B, Aquarius, Phoenix, UGC 4879 (expected N = 11).
- **S (satellites):** < 300 kpc from the MW or M31 with no HI detection (CFG860's S). Satellites with detected HI (LGS 3,
  NGC 185, NGC 205) are not used, as in CFG860.

## Estimators
- Υ_V = 2 for every dwarf (primary; CFG860/852 convention, available for all). L_V = 10^{0.4(4.83 − M_V)}.
- r12 = (4/3) r_h; g_obs = 3σ²/r12; g_bar = G (M*/2 + M_gas,in)/r12²; Δ = log10(g_obs / (g_bar ν_e(g_bar/a0))); footings
  9.3603e-11 (primary) and 1.1312e-10, never pooled.
- Gas (every dwarf with a `mass_HI` detection; an upper limit = 0): M_gas = 1.33 M_HI in an exponential HI disc with
  R_HI = D_HI/2, log D_HI[kpc] = 0.506 log M_HI − 3.293 (Wang+16), R_s from Σ_HI(R_HI) = 1 M_⊙ pc⁻²; M_gas,in = M_gas [1 − (1+x)e^−x],
  x = r12/R_s. **Root rule fixed now:** primary = the extended (larger-R_s) solution; if no solution, R_s = R_HI/2.

## Statistic
Restrict S to log g_bar within [min_I − 0.5, max_I + 0.5]. Fit Δ = a + b (log g_bar + 12.5) + c [I] by unweighted least
squares on S ∪ I. **c** = isolated minus satellites at matched g_bar. **E** = mean Δ over I (isolated excess over the law).
Errors: stratified bootstrap (resample within I and within S), 4000 draws, seed 874.

## Classes (canonical primary; the alternative footing must agree, else UNDECIDED)
- NOT DIAGNOSTIC: se_c > 0.20 dex.
- SMALL-SYSTEM: E/se_E ≥ 3 and |c|/se_c < 2.
- SATELLITE-ONLY: E/se_E < 2 and c/se_c ≤ −3.
- PARTIAL: E/se_E ≥ 2 and c/se_c ≤ −2.
- UNDECIDED: anything else.

## Gas bracket (flag)
Recompute with (i) the compact (smaller-R_s) disc solution and (ii) CFG860's convention, half of 1.33 M_HI inside r12.
If the class differs among primary, (i) and (ii), the verdict carries GAS-SENSITIVE. No gas and all gas inside are printed
for information.

## Reported variants (not graded)
Υ_SFH (CFG827) where available, else 2; strict isolation ≥ 500 kpc from both; Antlia B dropped (satellite of NGC 3109);
satellites restricted to M_V ≤ −6 (fewer binary-inflated ultra-faints); full-range fit as in CFG860 (no g_bar restriction);
+ Leo A and Sagittarius dIrr (stellar σ, gas-rich, excluded from the primary as in CFG852).

## Controls
- K1 (code identity): with gas zero and Υ_V = 2, per-dwarf Δ for the 11 isolated dwarfs must equal CFG860's `d` values
  (cfg860_results.json members I0 + IG) to < 1e-9. FAIL ⇒ INVALID.
- MUTATE (`CFG874_MUTATE=up|down`): isolated σ × 1.45 / ÷ 1.45. The statistic responds if down does not give SMALL-SYSTEM
  and up does not give SATELLITE-ONLY. Outputs written separately by mode.

## Disclosed limits (fixed now)
Stellar rotation is not treated (if present it would raise the isolated Δ). Unresolved binaries inflate some ultra-faint
satellites' σ (lowers c; variant M_V ≤ −6). Distance-only isolation cannot exclude backsplash: Eridanus II, Perseus I,
Andromeda XXVIII, Leo T and Phoenix lie 340–420 kpc from a host. HI non-detections are limits of uneven depth.
This is the whole Local Group supply: no further isolated dwarfs with stellar σ exist in the repo's LVD tables.
