# WG1_cmb_lensing_web_gradient: CMB lensing measures a potential inside the law's range, and board row D9 is NOT EVALUABLE for the law alone

**Commits.**
- Criteria: 2971b542c2, committed alone before any script or number.
- Script: 82f5264d33, committed before any run.
- Result: this commit.

**Origin.** Owner 2026-11-04: "Yes, run it". The lane follows Hu (2001, astro-ph/0105424), which shows CMB lensing maps the projected gravitational potential at z ≈ 1-2 on k ≈ few × 10⁻² Mpc⁻¹.

**Standing.** κ = ½ FITTED. The cold sector stays retired. Not theory closed. Nothing here says the data favour the framework. No ΛCDM spectrum, transfer function or background enters any model or verdict.

## Verdict

### V1: TRANSITION
The label holds on both footings and both binning rules. The frozen rule is conservative: it takes the 2σ envelope and a0(z) at the band's 68 % lower edge.

- **R:** 0.219 on canonical and 0.180 on alt.
  - R is set by one corner member (Ω_m 1.0, H0 75, p +0.5, β 2) at z 2.33, where the band's lower edge is 0.33.
  - With the band's centre, R is 0.079 / 0.065, which would read DEEP.
  - With a0 ∝ H(z), R is 0.025 / 0.021.
- **Best fits:** g_web = 0.0035-0.070 of the canonical a0(0), across all 66 accepted members over z 0.5-2.33. Counting every member, footing, a0(z) rule and envelope edge, the measured field lies at 0.003-0.22 a0.
- **Boost:** in the simple form, g/g_N = 1 + a0/g. That is at least 5.5 everywhere on the graded grid, and about 15-290 at the best fits.
- **Comparison with the record:** the same range holds the 0.01-0.03 a0 external fields CFG363 assumed.

### V2: board D9 for the law alone, NOT EVALUABLE
Two inputs are missing.
- **(a) The law's rule on the linear web.** It is required because V1 puts the field CMB lensing measures inside the law's range.
  - PAPER67 v1.0 says "a0 is absent from the linear FRW equations, so the law can't act there". That holds for the background only.
  - At the scales CMB lensing maps, the law, if it acts, acts strongly.
- **(b) A baryon field at z 0.5-3 on k ≈ 0.003-0.2 Mpc⁻¹ that doesn't use a cold term.** The record has none (PAPER67 row 11; CFG363, AUDIT_SIGMA8 and CFG917 all carry the cold mass).

### V3: reported, no label
This compares the deep limit at a fixed source, P_Ψ ∝ a0(z): a0 ∝ H(z) against the ρ_DE tie (band centre).

| a0(z) rules applied | median lever per member (rival / tie) | shape spread S ≥ 0.10 |
|---|---|---|
| to z 1090 (frozen) | 2.06-44 | 66 of 66 (S 0.68-5.4) |
| held beyond z 2.33 (POST-HOC) | 1.37-6.06 | 60 of 66 (S 0.03-1.38) |
| held beyond z 5 (POST-HOC) | 1.55-11.8 | 66 of 66 (S 0.12-2.16) |

- The POST-HOC rows were written into the script before the run but are not in the frozen criteria.
- The frozen lever is dominated by z ≫ 3, where a0 ∝ H(z) grows without bound.
- S ≥ 0.10 means the rival changes the shape of C_L^φφ, not only its amplitude.
  - This does **not** show that C_L^φφ alone separates the two rules.
  - A source with a different z-evolution (p) or k_t was not tried against it.
  - Tomography, meaning CMB lensing crossed with galaxies in z bins (Hu 2001, last section), is still the clean route.

### D1/D2: not graded
The baryon contrast per ln k that the measured potential needs, at k = 0.02 Mpc⁻¹:

| reading | z 1 | z 2 |
|---|---|---|
| law OFF: Newton, baryons only, ω_b 0.021-0.023 | 0.13-1.0 | 0.13-0.74 |
| law ON: simple form, rms mapping, canonical | 0.0009-0.044 | 0.0018-0.045 |
| law ON, alt | 0.0007-0.037 | 0.0015-0.038 |

- At k = k_t the ranges are wider: OFF 0.014-7.8, ON up to 0.33 (`wg1.out`).
- These numbers give the size of input (b) in each reading.
- Neither is compared with a baryon field, because the record has none without a cold term.
- The ω_b bracket is PROVISIONAL, from memory.

## Checks
- **K1** (Limber engine vs the analytic k⁻⁴ case): 8.0e-7, PASS.
- **K2** (gradient integral vs k_t²/2): 1.0e-8, PASS.
- **K3** (round trip on three members, g_web(1.5)): 1.0e-8, PASS.
- **K4** (9 bins, L 8-400 contiguous, covariance positive definite; SHA-256 in `wg1.out`): PASS.
- **MUTATE** (the kernel loses its factor 2): K1 FAILS with relative error 0.75, and every label reads NOT EVALUABLE. The check bites.
- **Member acceptance:** 66 of 90 members per rule pass the p ≥ 0.001 acceptance (χ² 7.2-23.7 on 7 dof).
  - Rejected: p ≥ 0 with β 4, and p +1 with β 3 (χ² ≥ 24.5).
  - The binning rules agree: PACKAGE (W + M − F) and PLAIN (W) differ by under 1 % in R. Hu's point holds here: the fiducial enters as a calibration only.

## What this means for the record
- **Board D9.** It currently reads "no graded number". It can now read: NOT EVALUABLE for the law alone (WG1). The measured web field is 0.003-0.22 a0, inside the law's range, and the law needs a web rule and a baryon field without a cold term.
- **PAPER67 v1.1** (owner's go needed). The sentence "can't act there" holds for the background only. A replacement that fits the record: "a0 is absent from the linear FRW background, but the potential CMB lensing maps at z 0.5-2.3 has gradients of 0.003-0.22 a0 (WG1), inside the law's range; the law needs a rule there and the record has none."
- **Action call** (top-5 item 1). Any action that keeps the law must say what the law does on this field. If the law acts there, CMB lensing (PR4 amplitude to 2-3 %) grades it, and a0(z) enters C_L^φφ with the lever above.

## What this lane can't say
- It is not a test of the law's lensing at galaxy or cluster scales.
- g_web is the web-scale field (k ≤ 400.5/χ). Fields near bound systems are larger.
- It assumes lensing sees the dynamical potential (v3 φ = ψ; AX1 G3).
- The background bracket is not a model. The bare law has no consistent background.
- R near the 0.1 boundary is set by one corner member and the lowest a0(z) edge. The DEEP/TRANSITION line is not a robust distinction; "inside the law's range" is.
- Nothing here reinstates the cold sector.

## Files
- `FROZEN_CRITERIA.md`
- `wg1.py`
- `wg1.out` and `wg1_results.json`: per-member fits, envelopes, labels, D1/D2 and data hashes.
- `wg1_MUTATE.out` and `wg1_MUTATE_results.json`.

**Run:** `python3 wg1.py` and `python3 wg1.py --mutate`. About 75 s each, single thread, under 1 GB. Data: Planck PR4 lensing files under `_external_data/` as used by CFG917, read through `cfg917_lib` (imported read only).
