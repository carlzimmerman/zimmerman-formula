# VERIFY — a0-line M/L-prior lever (external Upsilon), adversarial re-check

Scope: re-ran all four scripts in `a0_line_mlpriors/` (exit 0), re-derived the load-bearing
algebra from `../a0_line/fire_common.py` READ-ONLY, and hunted BOTH ways for a manufactured
footing detection AND a manufactured deficit. Frozen repo untouched (only stray file is the
pre-existing `real_research/papers/MI_FIELD_THEORY_RESULTS_2026.tex`, unrelated).

Footings: canonical a0 = cH_L/Z = 9.3548e-11 vs ALT = cH0/Z = 1.1305e-10 (20.9% apart).
2-sigma split target: sigma_tot <= |Delta|/2 = **9.753e-12**.

## Re-run status
setup_mlpriors.py / est_indep.py / est_marg.py / est_wall.py all exit 0. Numbers reproduce.

## Adversarial checks (both ways)

**(1) Does external color-M/L trade the Upsilon systematic for a color-M/L ZERO-POINT / dust /
age-metallicity systematic of comparable size?** YES — and the lanes handle it correctly.
Replacing the [3.6] SPS Upsilon with an external color-M/L (Bell-de Jong 2001) does NOT remove
the coherent floor; it REPLACES the SPS coherent zero-point with a color-M/L coherent zero-point
of comparable size (BdJ quote ~0.10-0.15 dex, IMF-driven, coherent). Independently swept the
traded-in coherent floor (Ud=0.7 ALLgas): 0.05 dex -> tot 17.13; 0.075 -> 17.95; 0.10 -> 19.03;
0.15 -> 21.84 e-12 — **never <= 9.753e-12**. The lanes correctly hold the coherent floor at
0.060-0.075 dex and shrink ONLY the per-galaxy residual; the external prior buys a sub-dominant
piece. No net gain from the swap. CONFIRMED, no manufactured win.

**(2) Is the per-galaxy averaging-down LEGITIMATE, or is there a hidden coherent component that
should NOT average?** Bounded on both sides, so the question is moot for the verdict. The split
assumes the per-galaxy part (0.080 dex pre) is independent across galaxies and RSS-averages over
~49 (18-20 TRGB) galaxies. If part of it is secretly coherent (correlated with type/color), it
migrates INTO the coherent floor and sysU rises toward the banked FULLY-COHERENT value. Verified
bracket: fully-coherent sysU = 9.57e-12 (= the current treatment, the worst case) vs
fully-independent = 1.66e-12 (ratio 0.173 ~ 1/sqrt(49)). The split (5.8e-12 balanced) sits
between. **Neither endpoint decides**: even the fully-coherent banked budget does not cross, and
the sysU->0 hard limit (best possible) also does not cross. So the averaging-legitimacy debate
cannot flip the outcome.

**(3) Is the coherent Upsilon zero-point DEGENERATE with a0?** PARTIALLY. Proper Bayesian
marginalization (template/Sherman-Morrison, C = diag + s^2 U U^T) gives rho(a0,alpha) =
-0.65 .. -0.81 across scenarios — never ->1. Because phi varies with g_bar, U is not proportional
to g, so the data self-calibrate the coherent nuisance and marginalization TIGHTENS a0 by 2-12%
vs quadrature (marg/quad = 0.88-0.98), rather than widening it. So (a) fire_common's quadrature
sysU was mildly conservative, not anti-conservative; (b) the residual degeneracy is still high
(|rho|~0.8), so the gain is small and does NOT rescue the footing. Honest.

**(4) Weight-noise fake-deficit guard.** CONFIRMED active in every lane (biased=False). Direct
check on Ud=0.7 gas-dom: honest model-based iterated GLS a0 = 1.181e-10; the biased observed-error
weighting collapses to a0 = 0.455e-10 — the same downward trap that once faked the 3.3e-11
deficit. All lanes use the model weights. No fake deficit is being carried.

**(5) Manufactured footing detection AND manufactured deficit — equally?** NEITHER.
- No detection: no (Ud, set, scenario) crosses BOTH >=2 bans AND tot<=|Delta|/2. Best separations
  1.72-1.94 sigma (TRGB), <=1.35 sigma (full-gas). The one >2-ban row (Ud=0.5 TRGB, 2.60 bans) has
  tot=16.06e-12 > HALF and is a SAME-SIDE lean (central 1.49e-10 above BOTH anchors) — it disfavours
  canonical WITHOUT selecting alt, correctly flagged as a low-Ud/nu-shape artifact, not a footing pick.
- No deficit: central a0-hat (1.18-1.49e-10) sits ABOVE both anchors; canonical is at most mildly
  disfavored (~-3 sigma at TRGB), ALT is not confirmed (~-1.4 sigma). Straddle preserved.

**(6) Both footings.** Target depends only on |Delta|/2, symmetric; both anchors carried in every
lane from `anchor_values.json`. Verdict identical on both footings.

**(7) nu-shape / magnitude degeneracy (per-point a0 declines with g_bar) still confounding the
central?** YES — carried. Ud=0.7 TRGB gas-dom terciles: per-point a0 = E/g_bar = 1.62 -> 1.24 ->
0.62 e-10 (declines). The GLS-weighted central is therefore weighting-dependent, not a clean single
a0; sysEst = |GLS-median|/2 (1.04e-11 on full-gas — alone exceeding the threshold) is the honest
line that books this. The honest a0 remains a BOX straddling both footings.

## Binding wall after the Upsilon lever
Even with Upsilon beaten (or zeroed), the terminal lines are: coherent gas-cal sysG (~8.6-9.5e-12,
KG ~2x KU so it beats sysU despite SIG_LNG being smaller in dex), the estimator-choice / nu-shape
spread sysEst (~1.04e-11 on full-gas), and the stat+geometry floor. Coherent floor
hypot(sU_coh, sysG) ~ 1.04e-11 > 9.75e-12 at ANY N. Deciding the footing needs an independent
gas-mass calibration (sig_lnG 0.10 -> <=0.08 nat), the SPS coherent floor held <= 0.06 dex, AND
BIG-SPARC counts — NOT external M/L alone. a0's value and s=-1 remain postulates.

## VERDICT
**TIGHTENS-BUT-NON-DIAGNOSTIC (outcome B), both footings — UPHELD.** Beating the per-galaxy Upsilon
with external color/SPS priors is real (sysU ~9.6 -> ~5.8e-12 balanced Ud=0.7, mostly from the
coherent/per-galaxy split, not the external prior) but NEITHER necessary-and-sufficient NOR
misleading: the total error never drops below |Delta|/2 and the convention-robust footing
separation never reaches 2 sigma (max 1.94) in ANY configuration, including the sysU->0 hard
limit. The swap to external color-M/L trades the SPS coherent floor for a comparable color-M/L
zero-point (adversarial #1) and the per-galaxy averaging is bounded by the fully-coherent worst
case (adversarial #2), so no error treatment of Upsilon decides it. Marginalization shows the
coherent zero-point is only partially degenerate with a0 (rho -0.65..-0.81) and tightens by 2-12%
(adversarial #3), insufficient. The binding wall is now gas-calibration + the coherent SPS floor +
the nu-shape/estimator spread. No manufactured detection, no manufactured deficit; the model-based
GLS guard is active (adversarial #4). Honest a0 is a box straddling BOTH footings; a0 value + s=-1
remain postulates. No "proves". Credit: Schombert-McGaugh-Lelli 2019, Meidt+2014, McGaugh-Schombert
2014, Bell-de Jong 2001, Lelli-McGaugh-Schombert 2016; kernel nu=sqrt(1+1/y) = Milgrom 1999 PLA
253:273 Eq.9, distinctive content = the cH_L/Z coefficient + MI completion.
