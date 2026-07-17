# SYNTHESIS — Beating the M/L (Upsilon) floor on the a0-line

**Question:** Does beating the stellar mass-to-light (Upsilon) floor with EXTERNAL per-galaxy
color/SPS priors DECIDE the dark-energy footing of a0-from-rotation —
canonical a0 = cH_Lambda/Z = 9.355e-11 vs alt a0 = cH_0/Z = 1.1305e-10?

**Answer: NO. Outcome (B): TIGHTENS-BUT-NON-DIAGNOSTIC — the wall shifts to gas-calibration.**
Verified across four independent estimator lanes (quadrature-budget, marginalized-Bayesian,
wall-map, sysU->0 hard limit) + an adversarial both-ways verify pass. UPHELD.

---

## 1. The threshold

Delta = |1.1305e-10 - 9.355e-11| = 1.951e-11 (20.9% gap).
To split the two footings at 2 sigma: sigma_tot <= |Delta|/2 = **9.753e-12**.

## 2. What the Upsilon lever actually does

The current fire_common treatment injects SIG_LNU = 0.23 nat = 0.0999 dex as ONE global,
**fully-coherent** number (sysU = KU*a0*SIG_LNU, KU summed over all points) — so it does NOT
average down with galaxy count; it is a floor. Proven: the same 0.0999 dex applied
fully-per-galaxy-independent gives only 1.66e-12 (ratio 0.17 ~ 1/sqrt(N_gal), N_gal=49).
The banked coherent treatment is the worst case; the honest truth sits between.

The lever = decompose the 0.0999 dex into (i) a **coherent SPS/IMF zero-point floor**
(irreducible, external colors cannot touch it) + (ii) a **per-galaxy reducible part**
(shrinks with external [3.6]+color SPS priors, averages ~1/sqrt(N)).
Two calibration-preserving literature decompositions (quadrature ~ banked 0.0999 dex):
- BALANCED: coherent 0.060 dex + per-galaxy residual 0.040 dex
- NIR-REALISTIC: coherent 0.075 + per-galaxy residual 0.035

**The real gain is recognizing the split, NOT the external prior.** At [3.6] the per-galaxy
reducible signal is intrinsically small (NIR M/L "nearly constant"), so the external color
prior only shrinks an already-sub-dominant residual (0.17x of coherent). sysU drops
**9.57e-12 -> ~5.8e-12** (Ud=0.7 balanced) almost entirely by acknowledging part of the
M/L error already averaged down over ~49 galaxies — not by new data.

## 3. Result — does not cross the line in ANY configuration

New sysU and total error (e-12), banked -> balanced / NIR-realistic:

| Config | sysU banked | sysU balanced | total banked | total balanced |
|---|---|---|---|---|
| Ud=0.7 ALLgas | 9.57 | 5.79 | 19.03 | 17.43 |
| Ud=0.7 TRGB   | 11.18 | 6.83 | 17.12 | 14.65 |
| Ud=0.5 ALLgas | 10.53 | 6.36 | 21.74 | 20.06 |
| Ud=0.5 TRGB   | 11.52 | 7.04 | 18.47 | 16.06 |

**NONE <= |Delta|/2 = 9.753e-12.** a0-hat central shift from the split = exactly 0
(the split touches only the error budget). Convention-robust footing separation never
reaches 2 sigma: best **1.75 sigma** (Ud=0.5 TRGB balanced), 1.72 (Ud=0.7 TRGB),
~1.25 full-gas.

**Where a0 lands:** GLS central 1.181e-10 (Ud=0.7 ALLgas), 1.333e-10 (Ud=0.7 TRGB),
1.363 / 1.490 at Ud=0.5 — sitting **ABOVE both footings**, so it nominally leans ALT
(bans canon < alt everywhere) but does not confirm ALT either. Both footings: canonical
9.355e-11 mildly disfavored (t ~ -3 sigma below central), alt 1.1305e-10 not confirmed
(t ~ -1.4 sigma). The lone >2-ban row (Ud=0.5 TRGB, 2.60 bans) is a same-side lean above
BOTH anchors — it rejects canonical WITHOUT selecting alt (a low-Ud / declining-a0 nu-shape
artifact from the TRGB synthesis), correctly flagged, NOT the banked headline.

## 4. The decisive hard limit — Upsilon is NOT the binding wall

Zeroing sysU **entirely** (perfect external M/L including the coherent floor) gives best-case
tot = **12.96e-12** (Ud=0.7 TRGB, 1.94 sigma), 14.43 (Ud=0.5 TRGB) — still ABOVE 9.753e-12
and UNDER 2 sigma everywhere. Even a perfect M/L measurement does not decide the footing.

## 5. Marginalization cross-check (the a0-Upsilon degeneracy)

Treating the coherent SPS zero-point as a proper Bayesian nuisance (template / Sherman-Morrison,
C = diag(sig2) + s^2 U U^T) instead of an error bar: the coherent zero-point is only
**PARTIALLY degenerate with a0**, rho = -0.65 to -0.81 (never ->1), because phi (stellar share)
genuinely varies with g_bar so the template U is not proportional to g. Consequence:
marginalization **TIGHTENS** a0 by 2-12% (sig_marg/sig_quad = 0.88-0.98) — the data
self-calibrate the nuisance; fire_common's quadrature sysU was mildly conservative, not
anti-conservative. Marginalization neither rescues nor worsens the footing.

## 6. The residual wall + what beats it

After the Upsilon lever the largest lines are:
- **GAS-CALIBRATION sysG ~9e-12** (coherent global gas-scale, SLNG=0.10) — the single largest
  line on the sharp TRGB set. Does NOT average down and does NOT self-calibrate (1-phi ~ 1 on
  gas-dominated points). Coherent floor hypot(sU_coh, sysG) = hypot(5.75, 8.63)e-12 =
  **1.037e-11 > target at any N** (impossible to beat by count alone at SLNG=0.10).
- **sysEst ~1.04e-11** (estimator-choice / nu-shape spread, |GLS - median|/2) on full-gas —
  alone exceeds the threshold; reducible by narrowing y (the TRGB sets show this).
- stat + inc + distance ~8e-12 underneath.

**What decides it (what-it-takes map, Ud=0.7 full):** at SLNG=0.10 the coherent floor exceeds
target at ANY N. SLNG=0.09 -> N~5300; 0.08 -> ~666; 0.06 -> ~273; 0.05 -> ~222 clean-distance
gas dwarfs. Requires ALL of: (a) independent gas-mass calibration cutting SLNG 0.10 -> ~<=0.08
(interferometric HI + CO, He/metal corrections), (b) SPS coherent floor held <= 0.06 dex
(sig_coh=0.05 still gives 9.87e-12 > target), (c) BIG-SPARC-scale N ~300-670.

**Traps cleared (both ways):** the external color-M/L SWAP trades the SPS coherent zero-point
for a comparable color-M/L/dust/age-metallicity coherent zero-point (~0.10-0.15 dex) — NO net
gain (independent sweep 0.05->0.15 dex never crosses target). A between-galaxy ratio cancels
~83% of the coherent gas-scale but cancels the ABSOLUTE a0 normalization too — it tests
universality, not the value, so it cannot compare 9.36 vs 1.13. No internal estimator both
cancels coherent gas-cal AND keeps absolute a0. KU(Upsilon)=0.352 vs KG(gas-cal)=0.730, so
deeper gas-domination trades the M/L wall for the gas-cal wall.

## 7. Caveats carried (verifier)

- The model-based iterated-GLS guard (biased=False) is active in every lane: honest GLS
  a0 = 1.181e-10 vs the observed-weight fake-deficit trap a0 = 0.455e-10 — the fake-deficit
  direction is reproduced and avoided.
- Per-point a0 = E/g_bar **DECLINES with g_bar** (Ud=0.7 TRGB terciles 1.62 -> 1.24 ->
  0.62e-10): nu-shape leaking into magnitude, so the GLS-weighted central is not a clean
  single a0 — sysEst books this and stays a real binding line. The honest a0 is a **box
  straddling BOTH footings (~0.9-1.5e-10)**, not a single-footing detection.
- No local per-galaxy SPS M/L vector exists for SPARC (L36 is a luminosity; rotmods ship one
  fixed Upsilon); the literature decomposition is used and flagged per ground rules.

## 8. Standing

**a0-from-rotation = the dark-energy density scale remains an honest box straddling both
footings.** Beating the M/L floor with external Upsilon priors is real (sysU ~9.6 -> ~5.8e-12)
but insufficient to decide canonical cH_Lambda/Z vs alt cH_0/Z — no estimator crosses the
2-ban / 2-sigma line, including the sysU->0 perfect-M/L limit. Canonical is mildly disfavored
(~-3 sigma), alt is not confirmed (~-1.4 sigma); the central sits above both. The binding wall
is now GAS-CALIBRATION + the irreducible ~0.06-0.075 dex coherent SPS floor + the estimator /
nu-shape spread. **Deciding needs a better HI/molecular gas-mass calibration (SLNG 0.10 ->
~<=0.08) PLUS BIG-SPARC counts, NOT more M/L work.**

**a0 value and s = -1 remain postulates regardless.** No footing proven; no "proves" language.

Credit: Schombert-McGaugh-Lelli 2019, Meidt+2014, McGaugh-Schombert 2014, Bell-de Jong 2001,
Lelli-McGaugh-Schombert 2016 (SPARC). Kernel = Milgrom 1999 PLA 253:273 Eq.9; the framework's
distinctive content = the cH_Lambda/Z coefficient + the MI completion.
