> **ID NOTE (2026-10-12): this lane is CFG674.** Its directory and commits say CFG669, which collided with another session's same-day use of that number (see LEDGER CFG670–679). Cite it as CFG674. Sealed files and hashes are unchanged.

# CFG669: independent F277W photometry of B1938+666 perturber A — NOT DIAGNOSTIC (the method cannot separate A from the arc)

Criteria 899403b81 (committed alone before any pixel was opened). Scores the sealed CFG668 prediction (9162427f…). Data: JWST
GO 8281 F277W level-3 mosaic (88 ks, public), in `../../../_external_data/cfg668_go8281/` (not committed). `python3 -I cfg669.py`.
κ = ½ FITTED; footings separate; cold energy mass required; not "theory closed"; nothing here says the data favour the framework.

**Label (both footings): NOT DIAGNOSTIC.** CFG668's prediction stands untested; it waits for the PI team's lens + light modelling.

## What happened, in order

1. **Frozen centre rule failed (bug, disclosed).** "Brightest pixel within 1″" locked onto a bright knot of the Einstein ring,
   not the lens nucleus, so A's aperture fell outside the ring (`*_FROZENCENTRE.*`, kept: S = 0.03, limit 25.4 AB, MUTATE not
   recovered). **Deviation:** the nucleus = local maximum nearest the flux-weighted centre of lens + ring (env `CFG669_CENTRE`;
   `frozen` reproduces the original). The corrected cutout (`cfg669_cutout.png`) puts A on the arc, as Vegetti+2012 describe.
2. **With the correct centre the frozen rule fires "SURVIVES" (S = 9.9, m_A = 23.4 AB). It is rejected, not claimed:**
   - 23.4 AB is ~3 mag brighter than the predicted bright end (26.4) — it would mean ~1e10 M☉ of stars inside a 1e8 M☉ lens mass;
   - the MUTATE tooth fails: an injected 28.0 AB point source changes E by only 2% and is "recovered" at 23.35, i.e. the aperture
     is dominated by something ~100× brighter;
   - the image shows the aperture on the brightest ridge of the lensed arc; the local annulus cannot remove a curved arc, and A's
     position (the arc's brightest part) ranks highest among the same-radius references for that reason.
   The excess is lensed source light, not A.
3. Per the record's rule (a measurement whose tooth fails is not diagnostic), the lane is NOT DIAGNOSTIC.

## What it takes

A full lens + source + lens-light model (pixelated source reconstruction) so the arc is predicted and subtracted, then the
residual at A tested against the sealed 26.4–29.6 AB band. That is what GO 8281 was designed for; the PI team's paper, or an
independent forward model (e.g. PyAutoLens), is the scorer. CFG668's sealed numbers and rules are unchanged.

---

# Part 2 (criteria 83f30af17): full lens + source + light model — NOT DIAGNOSTIC (tooth fails)

`python3 -I cfg669_lensmodel.py` → `cfg669_lensmodel.out/.log`, `cfg669_lensmodel_results.json`, `cfg669_lensmodel.png` (~5 min).
Empirical PSF from 22 stars; Sérsic lens light; SIE + shear; 24² pixelated source with evidence-set regularisation; PSF point
component at A. Frozen method, run once.

| quantity | value |
|---|---|
| fit | χ² 2.23e6 on 1681 pixels (χ²_ν 1337); λ_rel at the grid edge (1e-3); Sérsic R_e and q at their bounds |
| A amplitude | 7.2e-7 Jy (24.25 AB), σ_tot 4.7e-7 Jy (stat 2.4e-7, same-radius 3.7e-7, sys 1.7e-7); **S = 1.5** |
| 2σ limit | **23.96 AB** (needed for a test: 29.6–30.8) |
| tooth | 28.0 AB injected: recovered 28.00 (linear) / 27.55 (refit) but **S = 0.05 / 0.07 → FAILS** |
| **verdict** | **NOT DIAGNOSTIC (tooth fails), both footings** |

**Why, and what it means (diagnostic, no verdict weight):** the model reproduces the ring by eye, but the residuals are ±5σ
everywhere (sky level not modelled, single Sérsic too simple at S/N ~400 per pixel). More important, even a perfect model would not
reach the exclusion line here: the statistical error on A's amplitude at χ²_ν = 1 is 2.4e-7/√1337 = **6.6e-9 Jy, a 2σ floor of
≈ 28.6 AB**, set by the degeneracy between a point source at A and the reconstructed arc at 0.063″ pixels. So in F277W this data
could at best **confirm** A if it sits at the bright end of the sealed band (26.4–28.6 AB) but **cannot exclude** it (exclusion
needs a limit fainter than 30.8). The F115W mosaic (0.031″ pixels, 2.4 GB, not downloaded) and the PI team's dedicated modelling
are the remaining routes. CFG668 stays sealed and untested.

*Correction 2026-10-12:* the first version of this section said the perfect-model floor was 28.1 AB; the computed value is 28.60 AB (2σ of 6.56e-9 Jy). Conclusion unchanged.

---

# Part 3 (criteria 621ff3964): improved model (sky, 2 Sérsic, 30² source), F115W + F277W — NOT DIAGNOSTIC (both teeth fail)

`CFG669_BAND=f115w|f277w python3 -I cfg669_lensmodel_v3.py` → `cfg669_v3_<band>.log/.out/_results.json/.png`.

| band | fit | A amplitude | σ_tot (stat / same-radius / sys) | 2σ limit | χ²_ν = 1 floor | tooth | verdict |
|---|---|---|---|---|---|---|---|
| F115W (0.031″) | χ²_ν 16.9, λ 1e-4 | 4.8 ± 6.2 nJy (S 0.78; 29.69 AB) | 2.0 / 2.6 / 5.2 nJy | 28.67 AB | **31.43 AB** | 29.0 AB recovered, S 1.48 → FAILS | NOT DIAGNOSTIC |
| F277W (0.063″) | χ²_ν 631, λ at grid edge 1e-6 | 1.4 ± 1.2 µJy (S 1.2) | 0.36 / 0.98 / 0.48 µJy | 23.00 AB | 27.75 AB | 28.0 AB, S 0.02 → FAILS | NOT DIAGNOSTIC |

**Label: NOT DIAGNOSTIC, both footings, both bands.** No light is detected at A (F115W S = 0.78); this is not a limit that tests
the prediction either, because the injection tooth fails. The point estimate (29.7 AB) happens to fall inside the sealed band; at
S < 1 it carries no weight and must not be cited.

**What the fits establish about GO 8281 itself (diagnostic, no verdict weight):**
- F115W is far better modelled (χ²_ν 17 vs 631) and its perfect-model floor is **31.4 AB**: fainter than the sealed faint end
  (30.9/31.0), so a professional model of this data **can test the whole predicted band** — a ≥ 3σ detection anywhere in
  26.9–30.9 AB would make CFG668 SURVIVE.
- But the floor is brighter than the exclusion line (32.1/32.2): **under the frozen CFG668 rules this dataset cannot EXCLUDE the
  framework at A, only confirm it or return TENSION.** Stated now, before anyone scores it.
- The remaining gap between this model (limit 28.7) and the floor (31.4) is systematics: source-regularisation and grid choice
  dominate σ (5.2 nJy). Closing it needs a production lens code (adaptive source grids, multi-band joint fit, PSF from the exact
  dithers): the PI team's analysis, or PyAutoLens-class work.

---

# Part 4 RESULT (criteria c29c55493): PyAutoLens production model, F115W — NOT DIAGNOSTIC (tooth fails), with a 3.8σ excess at A

Stage 1 (Nautilus) ran; **stage 2 Nautilus NOT RUN** (2,000 evaluations in 11 h, ≈ 20 s each in-search; frozen 12-h rule);
stage 3 ran at the stage-2 **maximum-likelihood** model found by Nelder–Mead on the identical likelihood (disclosed substitute;
`cfg674_stage2_ml_nm.json`). Deviations, all disclosed: one core and numpy mode (macOS spawn deadlock; JAX preflight), Hilbert
image-plane mesh for Delaunay, positions likelihood (library standard), A's amplitude with the positive-only solver OFF (sign free).

| quantity | value |
|---|---|
| model at A | χ²_ν 4.30 (vs 16.9 own model); slope 2.234, θE 0.474″, m3/m4 small |
| **A light** | **13.2 nJy = 28.60 AB, σ_tot 3.46 nJy (stat 1.70, same-radius 2.87, mesh 0.92) → S = 3.82** |
| same-radius controls (11) | −6.3 … +8.6 nJy, median −0.6; **A exceeds all 11; 4.8σ vs controls alone** |
| 2σ limit / χ²_ν=1 floor | 29.30 / 30.86 AB |
| tooth (29.0 AB injected) | recovered 29.00 AB but **S = 2.63 < 3 → FAILS** |
| **verdict (both footings)** | **NOT DIAGNOSTIC (tooth fails)** |

**Reading, stated once and not upgraded:** the frozen rule makes this NOT DIAGNOSTIC. The excess at A (28.6 AB) lies inside the
sealed CFG673 band (26.9–30.9) and above every control, which is suggestive, but it is **not a detection** under our rules, and it
has an obvious mimic: **A's own mass (the perturbation that made A famous) is not in the lens model**, so arc residuals at A can be
absorbed by a point of light there. Required next (Part 5, frozen before running): include A's mass at its published position and
mass, and re-measure. Never cite the 28.6 AB number as a detection.
