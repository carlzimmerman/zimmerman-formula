# SYNTHESIS — the non-circular cross-scale a0(z) test

**de Sitter–Unruh MODIFIED-INERTIA framework** (C. P. Zimmerman). Horizon-derived
a0 = cH_Λ/Z = 9.36e-11; own dS-Unruh interpolation g_obs = √(g_bar² + g_bar·a0).
Lanes: `galaxy_a0z.py` / `GALAXY_A0Z.md` (galaxy-side), `confront.py` / `CONFRONT.md`
(confrontation), `VERIFY.md` (adversarial audit). Both scripts **exit 0** (re-run
2026-07-18) and reproduce every banked number. Frozen repo left read-only; all outputs
in `prep_2026/a0z_crossscale/`.

---

## 1. HEADLINE

**The framework FORCES a link ΛCDM has no reason to make — a galaxy's acceleration
scale a0(z) tracking the cosmic dark-energy density ρ_DE(z) through one relation
a0(z) = c²√(ρ_DE(z)/32π). That is a genuinely non-circular cross-scale prediction.
Today's data can only tie the z=0 knot (galaxy-a0 vs cosmic-a0 agree at ~1σ) and
exclude the alt-cH0 rising footing (~2σ via one clean z=3.25 rotator, the Big Wheel).
The distinctive 0.60–0.75 *decline* to z~3 is NEITHER detected NOR excluded:
separability S ≈ 0.8σ → UNDERPOWERED. Not passed, not failed.**

---

## 2. OUTCOME — does galaxy-measured a0(z) track cosmic ρ_DE(z)?

**The z=0 non-circular tie (holds, ~1σ).** Galaxy-side a0(0) from the Λ-blind SPARC
BTFR = 1.181e-10 ±16%; cosmic-side a0(0) = (c/2)√(Gρ_DE0). Ratio = **1.26 (1.44σ)** on
the canonical Planck-H0 footing, **1.17 (0.95σ)** on SH0ES-H0. This is the anchor the
bridge extends from — a0↔Λ at z=0 is definitional, so it is a consistency knot, not an
independent win. It holds.

**The high-z BTFR constraint (UNDERPOWERED).** The galaxy-side a0(z) is the BTFR
zero-point: in deep-MOND V⁴ = a0·G·M_bar, so a0(z)/a0(0) = (V_z/V_0)⁴/(M_bar,z/M_bar,0).
- **z=3.25 Big Wheel** (clean, single object, MC): a0_eff = 1.54(+1.10/−0.61)e-10 →
  ratio **1.31 (+0.93/−0.52)** vs SPARC. Consistent with constant; disfavors the 5×
  rise (~2σ); the ~2× M_bar systematic on one object exceeds the 0.30-dex decline
  signal, so it **cannot resolve the 0.70 decline**.
- **z~0.5–2.3 intermediate (NOT clean a0 probes)**: massive KMOS³D-class rotators sit
  at g ≳ a0, fitted BTFR slopes 3.0–3.85 (not the deep-MOND 4 the a0 map requires).
  The inferred "evolution" **flips sign with the analysis**: Übler+2017 (fixed slope
  3.75) → a0 rising ~2–3×; Sharma+2024 (free slope 3.21) → opposite; Di Teodoro+2016 /
  Tiley+2019 (V/σ>3) → null. Envelope ±0.3 dex, factor ~2–3 either way — not a valid
  a0 readout.

**Flat vs 0.60–0.75 decline.** The two cosmic tracks barely diverge: flat-Λ = 1.0 at
all z; DESI-DR2 evolving (w0,wa)=(−0.75,−0.90) = 0.712 at z=3 (0.685 at z=3.25). The
flat–DESI separation is only **0.147 dex at z=3** — swamped by the ~0.23-dex Big-Wheel
error and the ~0.30-dex intermediate scatter. Joint χ²: **χ²(flat)=1.08 vs
χ²(DESI-decl)=3.05, Δ=−1.97** (mildly prefers flat, |Δχ²|<2 not significant). Decisive
number: **separability S = 0.80σ (all 4), 0.73σ (clean pair), 0.73σ (Big Wheel alone)**.
Every galaxy point sits ≤1.2σ from BOTH tracks.

**Both footings.** Ratios cancel the footing; it re-enters only in the Big-Wheel
absolute: a0(3.25)/a0(0) = **1.31 / 1.65 / 1.37** on SPARC / canonical / alt — all
consistent with constant on their own footing. The alt ρ_tot/cH0 footing (a0 RISING
~5× by z~3, opposite sign) is the ONE thing the data disfavor (~2σ).

**Honest caveats (folded from VERIFY).**
- **a0 is not separable from M_bar evolution with this estimator** — Δlog a0 = −Δlog M_bar
  at fixed V (1:1 degenerate). Rising gas fractions (~10%→~50%), α_CO, dust, IMF all
  mimic an a0 shift. The scripts state this; the only a0-separable observable (full-RC /
  RAR transition) is not used by this lane.
- **Distance–cosmology dependence is mild, quantified**: M_bar∝D², and D(DESI)/D(flat)
  moves M_bar by ≤0.015 dex (z=1) — ~15× below the error. Testing a0-tracks-ρ_DE does
  not assume the DE evolution (a wrong background shifts all points together, it does
  not manufacture a decline) → **not circular in the fatal sense**.
- **Conservative at every fork**: keeps the adverse rising z=2.3 point in the fit; uses
  the M_dyn-capped Big-Wheel stellar mass (ratio 1.27, anti-framework) when full-SED
  (ratio 0.86) would sit right on the DESI decline. No deck-stacking either way.
- a0 magnitude inherits the posited Z; only the ratio/tracking is tested.

**Verdict: UNDERPOWERED-CONSISTENT-WITH-BOTH.**

---

## 3. PAPER VERDICT — is the non-circular cross-scale a0(z) test a paper?

**Yes, as a *method + forecast* paper — NOT yet as a detection.** The genuinely novel,
non-circular content is real and worth publishing: **the framework forces galaxy
kinematics (the Λ-blind BTFR zero-point) to track cosmic distances (SNe/DESI ρ_DE(z))
through a single relation — a cross-scale link ΛCDM structurally lacks.** No new
supernova formula, no a0↔Λ circularity (that is a z=0 definition); the test is the
*z-tracking of two independent measurements*. That framing is the paper's spine.

**Real strength (in hand today):**
- The **z=0 tie** — galaxy-a0 vs cosmic-a0 agree at ~1σ on the canonical footing.
- The **DIRECTION result**: the Big Wheel (one clean z=3.25 deep-MOND rotator) excludes
  the alt-cH0 ~5× *rise* at ~2σ. The framework's own canonical footing (declining) and
  flat both survive; the rising alternative does not. That is a genuine, if modest,
  discriminating datum.

**What is ELT/JWST-gated (honest limits):**
- The distinctive **0.60–0.75 decline** is unreachable now: S≈0.8σ, M_bar systematics
  exceed the 0.157-dex signal, intermediate-z is sign-contested and not deep-MOND.
- **Forecast, corrected two ways (both temper the future, not the present):**
  (a) the Big-Wheel error is *wider* than 0.23 dex — asym-drift α is fixed at 3.4, not
  MC'd (α:0→3.4 moves the ratio 0.95→1.27, ~0.1–0.15 dex); (b) the naive N≈24 for 3σ
  assumes independent errors, but the dominant M_bar error (α_CO/IMF/dust applied to a
  sample) is **common-mode** — with a ≥0.08-dex correlated floor the test **never
  reaches 3σ at any N** (0.05-dex floor → N≈362). **The decisive lever is M_bar
  CALIBRATION to <~0.05 dex common-mode, not raw rotator count**; and clean deep-MOND
  z~2–3 disks like the Big Wheel are rare, so assembling 20–40 is itself optimistic.

**Recommendation — honest title, publish as method+forecast:**
> *"Does the galaxy acceleration scale track cosmic dark energy? A non-circular
> cross-scale a0(z) test of de Sitter–Unruh modified inertia — the z=0 tie, the
> high-z BTFR forecast, and why M_bar calibration (not rotator count) is decisive."*

Frame it as: (1) the non-circular bridge ΛCDM lacks; (2) the z=0 tie + the Big-Wheel
direction (rise excluded); (3) an honest "underpowered today (S≈0.8σ)" with a
*calibration-limited* forecast. This is a legitimate stand-alone short paper OR a strong
section folded into the a0(z)-hostage / evolving-w front. **No "proves"; declining
neither detected nor excluded; M_bar and mild distance dependence stated up front.**

---

## 4. NEXT

1. **Fold the two VERIFY corrections into the scripts** before any submission:
   (a) propagate asym-drift α in the Big-Wheel MC (widen the 0.23-dex error);
   (b) add the common-mode M_bar floor to the forecast (report N-for-3σ vs floor
   table, headline the ~0.05-dex calibration requirement, not the N≈24 count).
2. **Chase clean deep-MOND high-z rotators**, not more massive g≳a0 disks: JWST/ALMA
   gas-traced outer RCs (Big-Wheel-like), ELT/HARMONI individual deep-MOND RCs. Target
   the a0-separable observable (RAR transition / full-RC shape), which breaks the
   BTFR M_bar degeneracy this lane cannot.
3. **Attack α_CO / IMF common-mode calibration** as the actual decisive lever — a
   uniformly-calibrated M_bar ladder to <~0.05 dex is worth more than 40 noisy rotators.
4. **Couple to the evolving-w front**: if DESI-w0wa firms up (declining ρ_DE), the
   *cosmic* track sharpens the target and the galaxy side becomes the live hostage;
   if w→−1 (flat), the distinctive signal vanishes and only the z=0 tie remains.

*No "proves." a0 magnitude inherits the posited Z; only the ratio/tracking is tested.
Both footings run. Honest both ways: the lane takes the anti-framework option at every
fork and still lands consistent-with-both.*
