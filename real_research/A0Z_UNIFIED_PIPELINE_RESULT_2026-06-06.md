# Unified mass-controlled a₀(z) on real IFS data — the existing-data test is REGIME-limited, not pipeline-limited

*C. Zimmerman, 2026-06-06. I built the "missing piece" the recon identified: ONE common pipeline fitting a₀(z) across
SPARC (z=0), KROSS (z~0.85), KMOS³D (z=0.6–2.5) with identical M_bar / velocity / pressure-support treatment, to
resolve the Del-Popolo-declining vs MUSE-rising sign contradiction. **Honest result: unifying the pipeline did NOT
rescue the test.** The data are limited by the *acceleration regime* (the galaxies aren't deep-MOND), which no common
pipeline fixes. This is a partial defeat of the "decide it with existing data" hope — reported straight.
Script+figure: `a0z_unified_pipeline.py` / `.png` (real data on disk, pure numpy).*

## A bug I caught en route (the sanity check earned its keep)
First run gave SPARC anchor a₀(0)=1.5×10⁻¹¹ — ~10× too low. Cause: **SPARC's `L[3.6]` and `M_HI` columns are in 10⁹
units, not 10¹⁰** (CamB at L36=0.075 ⟹ 7.5×10⁷ L☉ confirms it). The 10× error inflated every a₀(z)/a₀(0) ratio 10×.
Fixed ⟹ anchor a₀(0)=1.53×10⁻¹⁰ (✓ right ballpark), SPARC BTFR slope 0.267 (✓ deep-MOND expects 0.25). The whole
"steep rise" of the first run was this bug.

## The two estimators, and why the naive one lies
- **Naive** `a₀ = V⁴/(G M_bar)`, median ratio to SPARC. **Contaminated:** flux-limited samples select more massive,
  higher-acceleration disks at high z, so "a₀" rises with *mass*, not redshift.
- **Mass-controlled BTFR-residual (the clean one):** fit the z=0 SPARC relation `logV=c+b·logM_bar`; for each galaxy
  `dlogV = logV − (c+b·logM_bar)`; at fixed mass `dlog a₀ = 4·dlogV`. Removes the mass-selection bias by construction.

## The real-data result (mass-controlled)

| z_med | sample | N | a₀(z)/a₀(0) | framework | Verlinde |
|---|---|---|---|---|---|
| 0.00 | SPARC | 129 | 1.00 ± 0.06 | 1.00 | 1.00 |
| 0.85 | KROSS | 430 | **0.71 ± 0.07** | 1.03 | 1.64 |
| 1.34 | KMOS³D | 34 | **2.34 ± 0.37** | 0.96 | 2.17 |
| 2.23 | KMOS³D | 52 | **2.40 ± 0.45** | 0.83 | 3.35 |

**The two samples disagree in SIGN inside one identical pipeline:** KROSS (z=0.85) *declines* to 0.71; KMOS³D (z>1)
*rises* to ~2.4. This **reproduces the Del-Popolo-vs-MUSE contradiction as a sample/regime effect**, not a real a₀(z).

**The smoking gun — it's the acceleration regime, not redshift:**
- The **fixed-mass slope** is `+0.184 ± 0.084 dex/z` (leans mildly rising), but the **residual a₀-vs-mass coefficient at
  fixed z is +0.61** — it should be ~0 for clean deep-MOND. A large positive mass-coefficient means the BTFR a₀ still
  tracks mass (hence acceleration) *at fixed redshift* → the galaxies are **not in the deep-MOND regime (g≪a₀)**, so
  `V⁴/(G M_bar)` is a regime proxy, not a₀.
- Restricting to lower baryonic mass (closer to deep-MOND) pulls the slope down (`+0.18 → +0.03` at logM<10.0) — the
  right direction for "the rise is regime bias" — but KMOS³D is too small (N→33) to make this significant. The robust
  evidence is the mass-coefficient (+0.6), stable across all systematic settings.
- The cleaner, **lower-acceleration KROSS sample declines (0.71)**; the regime-biased massive KMOS³D disks rise. *Sign
  follows the acceleration regime, not z.*

## Can the existing data decide it? — quantified NO (for framework-vs-flat)

Varying the two sign-flipping systematics (stellar M/L + gas fraction; asymmetric-drift β) gives a **systematic span on
the fixed-mass slope of 0.337 dex/z** (slope ranges +0.05 to +0.39; sign stays positive only because every setting
inherits the same regime bias). Against that floor:

| hypothesis | predicted slope (z=0.6–2.4) | \|signal\|/floor | decidable with z<2.5 data? |
|---|---|---|---|
| constant | +0.000 | 0.0× | no |
| **framework √ρ_DE** | **−0.064** | **0.2×** | **NO — 5× below the floor** |
| Verlinde cH | +0.228 | 0.7× | no (by slope) |
| matter (1+z)^1.5 | +0.273 | 0.8× | marginal |

The framework's a₀(z) signal at z<2.5 is **≤0.07 dex** (the curve is near-flat there: the +6% bump at z≈0.4, only
−0.066 dex by z=2). The systematic floor is **0.34 dex**. **Signal is ~5× below floor — the existing IFS samples cannot
decide framework-vs-flat, even unified and mass-controlled.** The framework's signal clears a well-controlled 0.05-dex
floor only at **z≥2** (|dlog a₀| = 0.065/0.099/0.133 at z=2/2.5/3).

## What IS robust (the one positive)
**Verlinde / QI's steep rise is excluded by the cleanest intermediate-z point.** KROSS (z=0.85, lower-acceleration,
least regime-biased) gives a₀/a₀(0)=0.71; Verlinde predicts 1.64. Even with *zero* gas (unphysical, M_bar=M_star, the
maximum upward push on a₀) KROSS only reaches ~1.36 — still below 1.64, and AD corrections push it lower. So the
rising-a₀ rival is robustly disfavored by the cleaner sample, consistent with the multi-probe finding
(`A0Z_KERNEL_STANDING_2026-06-06.md`).

## Honest verdict
1. **Unifying the pipeline did not rescue the test** — and that is the finding. The blocker was never only the
   non-standard pressure-support/gas treatment (I standardized it); it is that **KROSS/KMOS³D galaxies are not in the
   deep-MOND regime** (mass-coefficient +0.6), so their BTFR a₀ measures the acceleration regime, not a₀(z). No common
   pipeline fixes that with integrated, high-acceleration IFS data.
2. **The apparent "rise" is regime bias**, the cleaner low-acceleration sample declines, and the sign of any reported
   a₀(z) from these data tracks which sample/regime you weight — exactly the Del-Popolo-vs-MUSE split, now explained.
3. **The framework's decline is NOT excluded** (the nominal +0.18 slope is regime-contaminated and systematic-dominated,
   span 0.34 ≫ the 0.06 framework signal), but it is **not measurable here either** — the data are at the systematic/
   regime floor.
4. **Quantified requirement:** the decision needs **deep-MOND (g≪a₀) rotation curves at z≳2**, where the framework
   signal (≥0.05 dex) first clears a controlled floor — *not* more integrated IFS at z<2.5. This sharpens the repo's
   standing conclusion from "need a clean z~3 curve" to a numerical floor: the existing-data test is regime-limited and
   the signal only emerges at z≳2.
5. **Verlinde is the casualty**, robustly, via the cleaner KROSS point.

**Bottom line:** the unified re-analysis is done, on real data, with a real bug caught — and its honest payoff is a
*negative* one that matters: the existing IFS samples are regime-limited, so the much-hoped "decide a₀(z) without new
telescopes" is **not available** for framework-vs-flat; what *is* available is the robust exclusion of the rising
(Verlinde) branch and a quantified z≳2 deep-MOND requirement.

*Numbers reproduced in `a0z_unified_pipeline.py`; figure `a0z_unified_pipeline.png`.*
