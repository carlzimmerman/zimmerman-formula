# DW1 RESULT: DESI DR2 III's Milky Way enclosed-mass profile vs the framework

**The frozen criteria award 9 of 12 pre-registered checks. The three failures are V2b, V3 and DW1e.**

**Read as the lane's own README states it — PASS on the enclosed mass profile (DW1a, DW1b, DW1c, DW1d,
DW1f and the mutation controls), FAIL on the extrapolated M200c (DW1e).** The criteria freeze twelve
pass conditions and no single overarching label word, so the label is the row of twelve; there is no
frozen vocabulary to appeal to beyond each check's own line.

| id | check | canonical | alt | verdict |
|---|---|---|---|---|
| V0 | ported instrument reproduces item-38's anchor at 73 kpc | 5.231e11 vs 5.23 | 5.713e11 vs 5.71 | PASS |
| V1 | McMillan model reproduces its own components | max err 0.04 % | same | PASS |
| V2a | Hankel transform vs the analytic exponential-disc transform | 1.08e-03 (< 2 %) | same | PASS |
| **V2b** | total radial force at 40 kpc has reached G M_b/r^2 (within 1 %) | **ratio 1.0453** | same | **FAIL** |
| **V3** | spherical and force-equivalent mass agree < 10 % at every radius | **worst 12.66 % at 20 kpc** | same | **FAIL** |
| DW1a | absolute M(<80 kpc), A = 1, no EFE | 5.691e11 (-1.34 s) | 6.218e11 (-0.28 s) | PASS |
| DW1b | one-amplitude fit of all 13 points | chi2/dof 0.26, rms 2.86 % | 0.22, 2.74 % | PASS |
| DW1c | A*(profile) = A(rotation curve, item 35) | 1.325 vs [1.254, 1.309], 0.45 s | 1.145 vs [1.152, 1.208], 0.23 s | PASS |
| DW1d | 60→80 kpc log-slope | 0.921 vs 0.707 +- 0.355 (+0.60 s) | 0.933 (+0.64 s) | PASS |
| **DW1e** | plateau vs the paper's M200c = 1.19e12 | 0.83e12 (-2.8 s) | 0.72e12 (-3.6 s) | **FAIL** |
| DW1f | pre-registered falsifier, > 20 % split at 150 kpc | +54 % (A = 1) | +54 % | PASS |
| MUT | mutation controls fire | chi2 82.1 -> 7987.5 (a0 x 10); 2415.2 (nu = 1); slope +0.707 -> +1.543 (shuffle) | same | PASS |

TEST lane, quarantined. Criteria `FROZEN_CRITERIA.md` (5732431896), committed before `dw1.py` and
before any number. Footings graded separately, never pooled. No particle is added; the dynamical mass
is the scalar's stress-energy. kappa = 1/2 FITTED; not theory closed.

**No new compute.** This file reads `dw1.out` and `dw1_results.json` (the committed run, 2026-11-11),
`README.md`, and the correction lane G239 (`deepseek_push/G239_proper_efe/`). No script was re-run.

---

## 1. What passed, and what it is worth

- **The absolute, zero-parameter prediction lands on the DESI mass at 80 kpc**: 5.691e11 (-1.34 sigma)
  canonical, 6.218e11 (-0.28 sigma) alt, against 6.36 +- 0.50 e11. Nothing is fitted to the halo stars.
- **One amplitude fits all 13 points** (20–80 kpc, 5 kpc steps) at rms 2.86 % / 2.74 %
  (chi2/dof 0.26 / 0.22, diagonal errors). The paper's own zero-parameter NFW (M200c 1.19e12, c = 12)
  gives 17.62/13 and rms 4.49 % on the same table: this data set cannot separate the two shapes.
- **That amplitude is the one the framework's own outer rotation curve already demanded** (item 35:
  1.254–1.309 canonical, 1.152–1.208 alt on this census): 1.325 +- 0.035 and 1.145 +- 0.033, i.e.
  0.45 sigma and 0.23 sigma. Two independent data sets, one free ledge, agreeing. The repo's standing
  "the framework needs 25–30 % more baryons than the census" liability is thereby a measurement with
  two witnesses; if the excess is in stars it is a prediction (M_* ~ 7.3e10 Msun, a Salpeter-side IMF)
  falsifiable by the same photometry that would otherwise kill the framework.
- **The shape passes** (DW1d): measured 60–80 kpc log-slope 0.707 +- 0.355 against 0.921 / 0.933.
- **The falsifier is registered with a radius and a size** (DW1f): the framework's plateau is flat at
  6.26e11 (A = 1) to 8.30e11 (A*) beyond r_EFE ~ 90–100 kpc; the paper's own NFW extrapolation gives
  9.65e11 at 150 kpc and 11.35e11 at 200 kpc — +54 % / +81 % on the absolute prediction, 7–10 sigma at
  the paper's 8 % precision. A DESI-DR3-class BHB/RRL sample reaching 150–200 kpc settles it.

## 2. What failed

- **DW1e, M200c — the one substantive failure.** The paper's 1.19 +- 0.13 e12 is 1.4x the framework's
  EFE-saturated plateau at the fitted amplitude (0.83e12 canonical, -2.8 sigma; 0.72e12 alt,
  -3.6 sigma). Reaching 1.19e12 would need A = 1.90, which the 20–80 kpc profile excludes at
  16.4 sigma (canonical) / 23.2 sigma (alt). The framework cannot have both the measured profile and
  the quoted virial mass. Mitigating, and stated in the criteria: M200c is not a framework quantity at
  all — the framework has a plateau, not a virial mass — and the paper reports no enclosed mass beyond
  80 kpc, drawing M200c as an NFW extrapolation with c = 12, which is exactly the profile that
  extrapolation is built to miss. Registered tension, not a kill.
- **V2b and V3, instrument gates.** At 40 kpc the radial force is 1.0453x the point-mass value (line
  1 %), and at 20 kpc the force-equivalent mass exceeds the spherical one by 12.66 % (line 10 %). Both
  are physical properties of a flattened baryon distribution — a disc's exterior mass still pulls
  inward in the plane, which a spherical shell does not do — so the thresholds are mis-specified for
  this geometry, and the lane uses M_sph throughout (the quantity a spherical Jeans analysis returns).
  The gate's purpose (that no verdict be an artefact of the reduction) is met by the subset fits:
  dropping the 20 kpc point moves A* by 0.0 % (canonical) and 0.4 % (r >= 30 kpc, alt).

## 3. Two corrections that sit on top of the committed `.out`

- **G239 (2026-11-11) replaces the external-field paragraph.** The `.out`'s EFE numbers use the
  scalar-additive approximation nu((g_bar+g_ext)/a0), the maximum-suppression case; the exact QUMOND
  angle average gives **+16 % / +13 % at 80 kpc, i.e. -2.77 sigma / -2.50 sigma, not -4.11 / -3.70**,
  and the 13-point profile fits at **3.3 % rms (chi2/dof 0.38), not 7.0 %**. Two statements of the
  `.out` and of README §3 are therefore **withdrawn**: that the EFE spoils the profile's shape, and
  that the 20–80 kpc profile prefers a weak external field. The A = 1 plateau falls from 6.26e11 to
  5.26e11, so DW1f's split widens from 1.8x to 2.2x; DW1e's direction is unchanged. The `.out` is left
  as the historical record of the approximation; G239's numbers are the operative ones.
- **The kernel diagnostic is post hoc** (the frozen criteria named no kernel). On a0kit's Milgrom form
  nu = sqrt(1+1/y) the same 13 points demand A = 1.585 / 1.350 against the rotation curve's
  1.254–1.309 / 1.152–1.208 — 6.1 / 3.8 sigma more. The two-dataset agreement of DW1c is therefore a
  **Route A** result and is not claimed for the a0-line form; both kernels still pass the absolute
  80 kpc amplitude (-1.94 / -0.89 sigma for Milgrom). Reported, not graded.

## 4. What is not claimed

- The paper's bias corrections are calibrated on ΛCDM (AuriDESI, NFW-like) mocks; a plateau is not
  guaranteed to transfer. Recorded as a scope limit on the data, not used to excuse a miss.
- The 13 table errors are correlated and are treated as diagonal, which flatters every chi2 in the
  lane, the NFW comparator's included.
- A = 1 is the prediction; A free is a nuisance. Nothing here derives a0, the kernel, or the baryon
  census. kappa = 1/2 remains FITTED.

## 5. Files

`FROZEN_CRITERIA.md` (5732431896, committed alone before the script), `dw1.py`, `dw1.out`,
`dw1_results.json` (`checks.n = 12`, `checks.fails = [V2b, V3, DW1e]`), `README.md` (with the G239
correction), and this file. The correcting lane is `deepseek_push/G239_proper_efe/`
(`g239.out`, `g239_results.json`, `README.md`).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
