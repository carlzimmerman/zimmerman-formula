# VERIFY — cluster-member infall-phase EFE sigma-spread (adversarial re-audit)

`prep_2026/cluster_efe_channel/` · 2026-07-17 · both footings (a0 = 9.36e-11 canonical /
1.13e-10 alt) · MI-class-generic (MI-vs-MG), NOT framework-specific · amplitude kernel-hostage ·
a0 value + s = −1 are POSTULATES.

## Re-run status (all exit 0)
`predict.py` ✓ · `mg_efe_zero.py` ✓ · `observable.py` ✓ · `power.py` ✓ · `verify.py` ✓ (this lane).
Every banked assertion still passes. The audit did **not** rebuild the physics; it stressed the
load-bearing claims and reports where they are **softer than banked**, both ways.

## The seven hunts

### (1)+(2) Is MG really 0 for the infall-phase spread? — GRANTED at fixed true field, SOFTER in observation
- **At FIXED TRUE 3D external field: MG = 0 is a genuine theorem** (symbolic `d(σ_MG)/dy = 0`, any
  a0, any interpolation; memoryless — a time-varying potential and retardation shift only the MEAN
  field, add ZERO family spread). Re-verified. This is the sole theorem-grade claim.
- **In OBSERVATION MG is NOT 0.** The projection alias (bin by R_proj, not 3D r) is ~2.2% isotropic
  (banked). **V1 finds the "killed to ~0.01%" claim in `observable.py` [C] is an artifact of binning
  on the SIMULATION's true r, which is not an observable.** The real deprojection is statistical /
  partial (GAP_STATEMENT E2 literally says "deproject statistically"; E3 says classification purity
  p < 1). Applying a realistic purity-p zone tag + per-zone mean-r calibration leaves a residual of
  **~1.3–2.0% at p = 0.5–0.9** (canonical: 2.15% → 1.97% → 1.32% for p = 0.5/0.7/0.9), i.e. 11–35%
  of the MI floor — **not ~0.01%.** The kill is real but PARTIAL and PURITY-DEPENDENT.
- **V2 (new mimic the banked isotropic MC under-counts):** anisotropic / filamentary infall
  (plungers enter along the LOS/major axis) pushes the raw R_proj alias NON-MONOTONICALLY up to
  **~7% (~55% of the MI band top, ~3× isotropic)** at strong alignment. So the banked 2.2% is a
  LOWER BOUND. Magnitude is toy-dependent (a real number needs a triaxial potential + infall-axis
  model), but the direction is adverse. It also exposes a second unpropagated error: the spherical
  caustic mass profile assumed in E2 is orientation-biased for filament-fed clusters → a_ext(R)
  carries an orientation-correlated error the banked lanes never quantify.
- **Verdict:** MG's honest observational floor is **~1–2%, not ~0.01%.** Below the MI 6–13% floor
  **only** at high tag purity AND for relaxed (non-filament-fed, DS-clean) clusters. The mitigations
  (class-aware calibration + DS cut + caustic membership + cluster selection) are **load-bearing, not
  optional** — a detection that skips them measures projection + interlopers, not modified inertia.

### (3) Does the observable isolate the MI history spread, or re-detect the radial gradient / projection?
- The fixed-radius phase-contrast **does** difference out the shared radial EFE gradient as a common
  mode (MG `d/dy = 0` verified) — that part is sound. **But** "fixed radius" means fixed a_ext, and
  a_ext is assigned from R_proj unless deprojected; the deprojection is the partial one above.
- **V4a (manufactured detection):** a pure MG universe, binned by R_proj with 15% uncut mis-tagged
  interlopers, yields a **1.30% phase-contrast (21% of the MI floor)** — a fake signal a large
  fraction of the band from projection + interlopers alone. Confirms the cuts are load-bearing.
- So the observable isolates the history spread **conditionally** — only with the full mitigation
  chain at adequate purity. It is not a clean, mitigation-free separation.

### (4) Can the same-signed tidal/ram/quenching confound fake the full 6–13%? — control is a DESIGN, not a proof
- The banked 4-part fingerprint (F1 fixed-r contrast, F2 sign-flip, F3 outward-rising profile, F4
  baryon-blind) is a **hand-set truth table**; the baryon-split toy in `observable.py` [E](iii)
  recovers the MI intercept **by construction** (linear model with a hardcoded environmental slope).
  It demonstrates the separation IS possible IF the confound is linear in an observable proxy and MI
  is exactly baryon-blind — it does not prove real confounds obey that.
- **Weak point in F4:** a *dry* tidal-heating episode heats stellar σ with only subtle morphological
  marks and no gas/SF signature, so "tides mark the baryons" is not airtight for gas-poor dE — the
  baryon-blind separator degrades for exactly the diffuse carriers that carry the signal. The radial
  slope (F3: MI outward vs tidal inward) is the more robust separator; F4 should be treated as
  corroborating, not decisive.

### (5) MI-class-generic, not framework-specific? — HELD
All lanes state repeatedly and correctly: this discriminates MI-class (ANY history-dependent
inertia, incl. Milgrom's linear no-EFE MI, arXiv:2503.07106) vs MG(=0). It is **NOT** this-framework
vs Milgrom. Amplitude is kernel-hostage (6–13% fiducial, cone ~3–20%). Both footings ~identical at
fixed dimensionless depth (a0 cancels). Consistent throughout.

### (6) The SIGN — a real internal inconsistency (V3)
- **GAP_STATEMENT E4/E7** predict the sign statistic NEGATIVE ("plungers less boosted") and make
  POSITIVE the pre-registered KILL condition. **`predict.py` §2 baseline** says "plungers/backsplash
  HOTTER" (positive). V3 confirms these are genuinely opposing branches: **raw adiabatic loading**
  (high-current-ω_ex plunger vs low-ω settled at same r) gives **+6.7% (HOTTER, positive)**, while
  the **memory branch** (first-infall pre-peri, memory of cold past) gives **−3.0% (DEFICIT)**.
- The observed sign is the COMPETITION between raw loading (+) and memory-of-cold-past (−), set by
  τ_M and the y_hist contrast. **If memory is weak (t ≫ τ_M), the sign is POSITIVE and would fire
  GAP E7's own KILL condition.** The two banked documents assert opposite baselines for the mixed
  "infalling" class. **The SIGN is therefore not theorem-grade** — it rides on the s = −1 postulate
  AND on τ_M/y_hist. The pre-registration must define the sign statistic on a SINGLE phase zone
  (e.g. first-infall pre-peri only) before firing, or it risks self-tripping its kill switch.

### (7) Does the powered dataset exist? — NO clean 2026 bite (V5); SDSS number is load-bearing and sound
- **SDSS single-fiber σ reliable only for σ ≳ 90–100 km/s** (instrumental floor 69, resolution ~90;
  Sohn+2017 ApJS 229:20, Zahid+2016). The diffuse deep-MOND carriers (σ 15–50, f ~10–14%) are
  **exactly the members SDSS excludes** → the stack measures adiabatic-dead E. `power.py`'s finding
  that the SDSS stack is **systematics-limited, not statistics-limited** (~1% signal slope under a
  1–5% σ-systematic + 2–8% C6 tidal floor) is SOUND.
- **V4b (manufactured null):** in an MI universe, survey-bright E (σ 150–230) carry max f ≈ 1.9% — a
  NULL even though MI is true. A null on the wrong (bright) population kills nothing.
- **MaNGA/SAMI IFU** (σ down to ~20; Law+2021) is the only 2026 route whose ~4% signal clears its
  resolved-σ systematic floor, but diffuse cluster members with reliable σ AND Rhee tags number
  **~few hundred (SAMI 8 clusters, Owers+2017), not ~1000** — `power.py`'s N ~800–1000 is optimistic;
  ~300–500 is defensible → z ~2–3 EXPLORATORY, hint-grade only. Clean detection needs ELT-HARMONI
  UDG σ (~2032) or a dedicated wide nearby-cluster IFU dwarf survey.

## VERDICT

**The channel is a genuine MI-vs-MG discriminator in principle, but it is MITIGATION-HEAVY, and its
three sharpest banked claims are softer than advertised:**

1. **MG's observational floor is ~1–2%, not ~0.01%.** The projection alias is killed only PARTIALLY
   (purity-dependent) by observable deprojection — the ~0.01% figure came from binning on
   non-observable simulation-true-r. Filamentary/triaxial infall can push the raw mimic to ~7%
   (band-sized) and is unquantified by the banked isotropic MC. The mitigation chain + relaxed-cluster
   selection is load-bearing; the residual clears the MI floor only at high tag purity.
2. **The SIGN is not theorem-grade and is internally inconsistent across the banked docs** (GAP E4/E7
   negative vs predict.py positive). Raw loading and the memory branch oppose; the sign rides on the
   s = −1 postulate + τ_M. The pre-registration must pin the sign statistic to a single phase zone or
   risk self-tripping its KILL condition. **Only MG = 0 (at fixed true field) is theorem-grade** —
   the sign and the sign-flip are postulate + kernel contingent.
3. **The clean-detection dataset does not exist in 2026.** SDSS is systematics-limited and excludes
   the carriers; MaNGA/SAMI gives an exploratory ~2–3σ hint at N ~300–500. Underpowered today.

**Held correct:** MG = 0 at fixed true field (theorem); the fixed-radius phase-contrast differences
out the shared radial gradient; MI-class-generic scope; kernel-hostage amplitude; both footings
near-identical; the SDSS systematics-limit finding; the honest "prediction, not confrontation" stance.

**Not fatal, but not clean.** Honest bottom line: a real MG-impossible discriminator whose realization
is **UNDERPOWERED + MITIGATION-DEPENDENT + sign-postulate-contingent**. No "proves" for the framework.
Files: `verify.py`, `verify.out`, this `VERIFY.md`.
