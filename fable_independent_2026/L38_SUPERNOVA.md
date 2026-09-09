# L38 — what Type Ia supernovae actually say about this framework

**Script:** `fable_independent_2026/L38_supernova_reexam.py` · **Output:** `L38_supernova_reexam.out`
**Data:** Pantheon+ (1701 light curves, 1590 after the official `zHD > 0.01` cut) with the official
**STAT+SYS covariance**, read read-only from `qwen_claude_field_theory/closure_2026/supernova_reaudit_2026/`
(the same release file is byte-identical in `real_research/data_cache/` and `prep_2026/sne_lambda/`).
**Both footings throughout:** a₀(0) = 9.3619e-11 (canonical, ρ_Λ) / 1.1279e-10 m s⁻² (alt, ρ_total).
**Runtime** ~1 minute. **Nothing committed.**

**Not touched, by instruction and on the record:** the SN host-mass-step lever is CLOSED (two null tests,
`snia_hoststep_sizextmatch.py` and `snia_hoststep_localSB.py`; partial correlation of Hubble residual with
acceleration at fixed mass +0.030 / −0.036 against mass at −0.170 / −0.203). It is not re-opened anywhere here.

**The documented failure mode is guarded, testably.** `GEMINI_MANUFACTURED_WIN_a0z_2026-07-20.md` records an
agent truncating the law at O(z), dropping wₐ, and manufacturing a rise. Check **A5** reproduces that
truncation *as a large error* rather than adopting it, so the guard itself can fail.

---

## Headline

1. **The registered z ≈ 2.5 prediction needs a correction, and it is not small.** "Flat 0.00 dex" holds
   only in the w = −1 limit. Under **every** evolving-dark-energy fork on the record the framework's own
   prediction is **−0.085 to −0.131 dex, ±0.045 within a fork** — 66–101 % of the registered 0.13 dex total
   measurement budget. The deepest fork plus one sigma reaches 0.176 dex, past the budget, which breaks the
   registration's own rule that *"a result inconsistent with both values counts against both"*. **Eight of
   the ten places the frozen pair (0.00 vs +0.33) appears in this repo quote a bare 0.00, and no occurrence
   anywhere carries an error bar.**
2. **Supernovae alone are powerless on the canonical footing.** Δχ² = 0.52 for two extra parameters
   (77 % by chance, 0.29 σ) — *less* than the 2.0 expected from adding two free parameters to noise. The
   SN-only 1σ profile band on a₀(2.5)/a₀(0) is **[0.36, 3.59]**.
3. **On the alt footing the answer flips**, and this is the constructive half: a₀ ∝ H(z) *is* the Hubble
   diagram, so the supernovae pin it to a few per cent — [1.69, 2.15] at z = 1, [3.69, 4.72] at z = 2.5.
4. **The footing fork is split 3–3, and the split falls along measurement *currency*.** Both slope-currency
   points lean toward the branch the record rejects; the ratio-currency points go 3–1 the other way. That is
   the signature of a redshift-dependent systematic in the slope estimators, not of a₀ evolution. Every
   point is under 1.5σ, so it is an observation about the archive's shape, not a measurement.
5. **The lensing angle is dead**, with a number. **The low-z peculiar-velocity bound is new and clean**, and
   confirms the framework's own linear-growth theorem.

**Nothing here favours this framework over ΛCDM.** Nothing here is a win.

---

## PASS/FAIL lines, verbatim

```
[PASS] A1 the fast distance integrator matches an independent 48-node Gauss-Legendre quadrature (the convention used by the repo's own full-covariance audit) to better than 1e-4 mag on both a LCDM and a DESI-CPL cosmology   (max |dmu| = 4.14e-06 (LCDM), 5.67e-06 (CPL))
[PASS] A2 the fitter reproduces the published Pantheon+ SN-only flat-LCDM constraint to well inside its quoted error   (pull 0.09 sigma, sigma 0.0182 vs 0.018)
[PASS] A3 the cosmology fitter recovers injected (w0, wa) from synthetic supernova data generated with the real STAT+SYS covariance -- the profile-likelihood region covers the truth at the advertised rate   (68% coverage 9/12, 95% coverage 12/12)
[PASS] A4 the exact a0(z) law reproduces its own recorded behaviour -- a bump near z ~ 0.29 and 0.70 at z = 3 for the repo's DESI-DR2 parameters   (z_bump 0.293, ratio(3) 0.6961)
[PASS] A5 the low-redshift expansion matches the exact law to the order claimed (O(z^2)), AND the documented manufactured-win truncation (linear, wa dropped) is reproduced as a large ERROR rather than being silently adopted   (O(z^3) coefficient bound 0.65; truncation error 0.50)
[PASS] A6 PAPER7's stated a0(2.5)/a0(0) = 0.82 is reproduced exactly, and the (w0,wa) fork behind it is identified as DESI DR2 + CMB + Pantheon+   (DESI DR2 + CMB + Pantheon+ -> 0.8217)
[PASS] B1 the two Delta_BTFR sign conventions give the SAME separation between the two hypotheses (so the 20:1 is convention-independent), while the registered central values are quoted in the velocity-side convention and the registered FORMULA is the mass-side one   (separation 0.414 dex both ways)
[FAIL] B2 the registered 'flat 0.00 dex' central value is UNCHANGED once evolving dark energy is propagated through the exact law with the full (w0, wa) covariance   (instead Delta_fw = -0.085 to -0.131 dex +/- 0.045; the registered 0.00 holds only if w = -1)
[PASS] B3 the evolving-dark-energy cross-term in the LCDM-native rival is negligible against the registered 0.13 dex budget, so the +0.33 side of the registered statistic does NOT need revising   (rival shifts -0.0046 dex; reproduces the registered +0.33)
[FAIL] B4 the registered statistic can be applied as frozen without any risk of scoring the framework's OWN evolving-dark-energy prediction as a falsification of the framework   (deepest fork -0.131 dex + 1 sigma 0.045 = 0.176 dex vs the 0.13 dex budget)
[FAIL] B5 every place the registered pair (0.00 vs +0.33) appears on the record carries the evolving-dark-energy value alongside it   (8 of 10 occurrences quote a bare 0.00; the -0.09 survives in 2 of them and no occurrence anywhere carries an error bar)
[FAIL] C3a supernovae ALONE can distinguish the framework's a0(z) from a constant, on the CANONICAL (rho_Lambda) footing   (Delta chi2 = 0.52 for 2 parameters (77% probability by chance); the SN-only 1-sigma profile band at z = 2.5 is [0.36, 3.59], width 3.23, and contains 1.000)
[PASS] C3b the SAME question on the ALT (rho_total) footing -- and here the answer FLIPS: because that branch says a0 is proportional to H(z), the supernovae pin it directly and to a few per cent   (SN-only profile 1-sigma a0(z)/a0(0) = [1.69, 2.15] at z = 1 and [3.69, 4.72] at z = 2.5, both excluding a constant by a wide margin)
[FAIL] D2 the supernova-era a0 measurements already in the repo (MUSE-DARK III, MSA-3D) can separate the rho_Lambda footing from the rho_total footing   (MUSE systematic floor 0.26-0.48 dex vs a 0.26 dex separation; MSA-3D 1.1 sigma on the slope. Formal errors say yes, the stated systematics say no.)
[FAIL] D3 the supernova-era a0 archive leans consistently toward ONE footing, so the fork can at least be given a direction   (it does not: 3 of 6 points sit nearer the alt branch and 3 nearer canonical, and the split is BY MEASUREMENT CURRENCY -- both SLOPE points lean alt, and the ratio points are 3-1 the other way)
[PASS] D4 the rho_Lambda / rho_total footing fork is decidable somewhere inside the supernova redshift range with TODAY's coherent systematic floor   (yes, at z >= 3.0: the branches are 0.77 dex apart against a 0.36 dex coherent floor)
[FAIL] E2 the supernova lensing-magnification signal has ANY discriminating power between a baryons-plus-kernel convergence field and LCDM's   (the effect to be resolved is |A-1| ~ 0.3; Pantheon+ measures A to +/-0.51, 1.7x too coarse, and does not detect the lensing term itself (0.0 sigma from A = 0). Underpowered by a factor 3; stop here -- this is an honest power calculation, not a result)
[PASS] F1 the low-redshift supernova Hubble diagram is CONSISTENT with the framework's own linear-growth theorem (LCDM-like velocities) and independently EXCLUDES the naive kernel-boosted velocity field   (sigma_v < 350 km/s vs 2250 km/s for a naive nu = 9 boost; the framework's OWN prediction (delta Y^(1) = 0 -> LCDM growth) passes, the naive reading does not)
[FAIL] G1 supernova data, ON THEIR OWN, have live discriminating power for this framework -- i.e. some supernova measurement by itself can move a verdict on a0(z), on the footing fork, or on the kernel   (SN-only evolution 0.52 chi2 for 2 params (0.29 sigma); the SN-era a0 measurements cannot separate the footings through their stated systematics; SN lensing is not detected at all. On the canonical footing SNe enter as an INPUT to (w0, wa), never as a test.)
[PASS] G2 supernovae nevertheless SHARPEN a framework prediction that another instrument can then decide -- the constructive half of the same finding   (they pin the alt branch to a0(1)/a0(0) = [1.69, 2.15] and the canonical branch's z = 2.5 zero point to +/-0.045 dex; the two branches separate by 0.66 dex at z = 2.5, which the already-pre-registered object decides for free)
```

Six controls pass. Eight substantive checks fail; every one of them fails in the direction "this route does
not have the property claimed for it", which is the point of writing them that way.

---

## Target 1 — the registered z ≈ 2.5 prediction *does* change

In deep MOND V_f⁴ = G a₀ M_b exactly, so the baryonic Tully–Fisher zero point moves as log₁₀ a₀, i.e. the
velocity-side zero point moves as ¼ of it. The registered statistic (PAPER7, DOI 10.5281/zenodo.22563139)
scores one lensed rotator at z ≈ 2.5 against **0.00 dex (framework)** and **+0.33 dex (ΛCDM-native)** with a
total zero-point budget of **0.13 dex**, quoted as 20:1.

**A6 reproduces PAPER7's own 0.82 exactly** and identifies the fork behind it as DESI DR2 + CMB + Pantheon+.

### The framework's z = 2.5 value, every fork, with the full (w₀, wₐ) covariance propagated

| (w₀, wₐ) source | a₀(2.5)/a₀(0) | Δ_fw [dex] | σ [dex] |
|---|---|---|---|
| ΛCDM exactly (w = −1) | 1.0000 | **0.000** | — |
| DESI DR2 + CMB + Pantheon+ | 0.8217 | −0.085 | 0.045 |
| DESI DR2 + CMB + DESY5 | 0.7956 | −0.099 | 0.044 |
| DESI DR2 + CMB + Union3 | 0.7752 | −0.111 | 0.058 |
| repo canonical DR2-ish (−0.83, −0.75) | 0.7510 | −0.124 | — |
| DESI BAO+CMB only (SN-free) | 0.7393 | −0.131 | — |
| age-corrected BAO+CMB+P+ (Son 2025) | 0.7782 | −0.109 | — |
| age-corrected BAO+CMB+DES5Y (Son 2025) | 0.7450 | −0.128 | — |

(velocity-side convention, matching the registered numbers; the ratio is footing-independent within the branch)

**The correction, stated in one line:** the framework's z = 2.5 prediction is **not 0.00 but a band,
0.00 (w = −1) to −0.15 dex (DESI DR2, 1σ low), with a recommended combined value of
−0.097 [−0.148, −0.049] dex (68 %)**.

Three consequences, all of them checked:

- **Against interest (B4).** The registration's rule *"a result inconsistent with both values counts against
  both"* is unsafe as frozen. The deepest fork (−0.131) plus one within-fork sigma (0.045) is 0.176 dex —
  past the 0.13 dex budget. A measurement landing there is *the framework's own prediction* and would be
  scored as evidence against it.
- **In favour, and it must be reported too (B4).** Because the two hypotheses move apart, the discrimination
  improves: separation 0.328 → 0.408 dex, 24:1 → 82:1 with the theory error folded in. The correction cuts
  both ways.
- **The cross-term is clean (B3).** The ΛCDM-native rival contains E(z)^{4/3}, and
  `a0z_lcdm_native_hypothesis_2026.py` hardcodes E(z) at w = −1. Propagating the *same* (w₀, wₐ) through the
  rival moves it by only **−0.0046 dex**. The +0.33 side does not need revising. (The concentration–mass
  relation's own w-dependence through the growth history is flagged, not computed.)

### Two documentation hazards found on the way

- **B1, sign convention.** PAPER7's *prose* defines Δ_BTFR = log M_b − 4 log V_f − C₀ = −log₁₀[scale ratio];
  its *displayed* numbers (0.00 / −0.09 / +0.33) are the velocity-side quantity +log₁₀[scale ratio]. The
  separation, and therefore the 20:1, is identical either way — but an observer who applies the prose formula
  and compares to "+0.33" scores ΛCDM with the wrong sign.
- **B5, provenance.** Live grep over README.md, STANDING.md, PAPER7.tex, the MNRAS cover letter,
  TEN_HARDEST_QUESTIONS and FRAMEWORK_VS_LCDM_TEST_2026.md: **10 occurrences of the frozen pair; 2 carry the
  −0.09; 8 are bare; 0 carry an error bar.** The qualified ones are `STANDING.md:49` and PAPER7's
  introduction. The bare ones include PAPER7's own **abstract**, `STANDING.md:18`, `README.md:60` and `:162`,
  and the MNRAS cover letter.

**Recommended (not applied — frozen files are untouchable and amendments are the user's call):** an
append-only amendment registering the framework side as a band with the decision rule stated over the band.

---

## Target 2 — the SN-only pipeline

Fit (Ω_m, w₀, wₐ) from Pantheon+ alone with the official STAT+SYS covariance and an analytically
marginalised magnitude offset; 182 628-point grid; profile-likelihood bands (prior-free) reported as primary,
marginal bands reported with the prior box stated and a prior-sensitivity test.

- **Control:** flat ΛCDM SN-only Ω_m = **0.3316 ± 0.0182** vs published 0.334 ± 0.018 (0.09 σ).
  Independently reproduces the repo's own full-covariance audit to 6 digits in χ².
- **SN-only best fit:** Ω_m = 0.22, w₀ = −0.85, wₐ = **+0.50** — note the *sign* of wₐ is opposite to DESI's.
- **Δχ² = 0.523 for two extra parameters** (p = 0.77, 0.29 σ). Less improvement than the 2.0 expected from
  adding two free parameters to pure noise. **Supernovae alone see no dark-energy evolution.**

### The band (canonical footing, profile-likelihood Δχ² ≤ 1, prior-free)

| z | SN-only | DESI DR2+CMB+P+ propagated | repo record (DR1 chains) |
|---|---|---|---|
| 0.25 | [0.962, 1.149] | — | — |
| 0.50 | [0.885, 1.324] | — | — |
| 1.00 | [0.707, 1.760] | 0.989 [0.957, 1.022] | — |
| 1.50 | [0.558, 2.288] | — | — |
| 2.00 | [0.446, 2.890] | 0.874 [0.807, 0.946] | — |
| 2.50 | [0.362, 3.588] | 0.822 [0.742, 0.911] | — |
| 3.00 | [0.299, 4.368] | 0.775 [0.684, 0.878] | 0.710 [0.594, 0.833] |

Absolute values follow by multiplying by the footing: a₀(2.5) ∈ [3.4e-11, 3.4e-10] m s⁻² canonical.

**The SN-only band is 10–40× wider than the band the record quotes.** The record's band is BAO+CMB geometry
that supernovae only help to close. Even with Ω_m pinned to CMB precision (0.315 ± 0.007), the supernovae do
not exclude a constant a₀ (Δχ² = 0.66 for two parameters; z = 2.5 band [0.654, 1.354]). **Stated against
interest: the framework's distinctive prediction is hostage to a BAO+CMB preference that the supernovae, on
their own, do not corroborate.**

The marginal (Bayesian) band is **prior-dominated** — halving the prior box moves the z = 2.5 median from
0.672 to 0.922, more than the band's own width. Reported, and not used as the headline.

---

## Target 3 — the footing fork inside the supernova range

The headline equation a₀ = κ c √(Gρ) is ambiguous in ρ, and the two readings are **not two normalisations of
one curve** — they are two different functions of redshift. At z = 0 they differ by a fixed 0.0809 dex
(1/√Ω_Λ = 1.2048, which is exactly the 9.3619e-11 / 1.1279e-10 footing pair). Above z = 0 they diverge:

| z | canonical (ρ_Λ) | alt (ρ_total) | separation [dex] |
|---|---|---|---|
| 0.33 | 1.035 | 1.215 | 0.069 |
| 0.50 | 1.032 | 1.339 | 0.113 |
| 1.00 | 0.989 | 1.786 | 0.257 |
| 1.44 | 0.938 | 2.276 | 0.385 |
| 1.68 | 0.910 | 2.575 | 0.452 |
| 2.00 | 0.874 | 3.005 | 0.536 |
| 2.50 | 0.822 | 3.737 | **0.658** |
| 3.00 | 0.775 | 4.536 | 0.767 |

**D2 — can the existing SN-era measurements separate them? No, on the systematics.** MUSE-DARK III's formal
error on a₀(z~1)/a₀(0) is 0.027 dex, 10× smaller than the 0.257 dex separation. But a₀ = V⁴/(G M_b) means
d log a₀ = −d log M_b **exactly**, so the authors' own disowned-but-required stellar-mass offset of
+0.20 to +0.45 dex propagates 1:1 and is 0.8–1.8× the separation. With the quoted 0.17 dex intrinsic scatter
the floor is **0.26–0.48 dex against a 0.26 dex separation.** MSA-3D's controlled slope separates the
branches at **1.1 σ**. Neither decides.

**D3 — which way does the archive lean? It is split 3–3, by measurement currency.**

A first pass in this lane used only the two *slope* measurements the brief named and produced a clean lean
toward the rejected footing. **That was one-sided and is withdrawn.** The repo's own committed placement
script, `prep_2026/a0z_crossscale/highz_a0z_fork_placement_2026.py` (re-run 2026-09-08, exit 0), already puts
six points on this fork, and the ratio-currency points go the other way:

| point | currency | σ from canonical | σ from alt | nearer |
|---|---|---|---|---|
| MSA-3D selection-corrected, z 0.58–1.68 | slope | 1.45 | 0.32 | alt |
| MUSE-DARK III / Ciocan, z 0.33–1.44 | slope | 4.10 | 1.50 | alt |
| MUSE-DARK II / Jeanneau, z ~ 0.9 | ratio | 0.00 | 1.10 | canonical/flat |
| Übler+17 KMOS3D, z ~ 0.9 | ratio | 0.79 | 0.48 | alt |
| Übler+17 KMOS3D, z ~ 2.3 | ratio | 0.68 | 1.05 | canonical/flat |
| Amvrosiadis+25 DSFG, z ~ 2.4 | ratio | 0.79 | 1.40 | canonical/flat |

**Tally 3–3.** Every point is under 1.5σ except Ciocan's slope on inflated systematics. The script's own
verdict on each is *underpowered, excludes no branch* — this lane reproduces that and adds only the pattern:

**the split falls along measurement currency, not along redshift or sample.** A genuine a₀(z) would move
slope and ratio estimators together. A redshift-dependent *systematic* in the slope estimators — pressure
support, beam smearing, an M/L drift, all of which grow with z and all of which the systematics-floor script
already prices — would move the slopes and leave the ratios alone. The observed split is the second
pattern's signature, not the first's. But at <1.5σ per point this is an observation about the archive's
shape, not a measurement of anything, and it is **not** new evidence for the ρ_total footing, which the
coefficient-footing audit rejects on independent z = 0 grounds. The MUSE confrontation document already
records the sign match and calls the rejected branch an undershoot.

**D4 — the constructive consequence.** Against the repo's own coherent (non-averaging) systematic floor for a
gas-dominated deep-MOND dwarf, read live from `highz_systematics_floor_results.json`:

| z | separation | TODAY floor | FUTURE floor | decidable (>2× floor)? |
|---|---|---|---|---|
| 0.5 | 0.113 | 0.215 | 0.141 | no |
| 1.0 | 0.257 | 0.253 | 0.160 | no |
| 2.0 | 0.536 | 0.315 | 0.197 | yes, future |
| 3.0 | 0.767 | 0.365 | 0.231 | **YES today** |

**The z ≈ 2.5 object already pre-registered for the 0.00-vs-+0.33 test settles the internal footing fork as a
free by-product** — 0.66 dex of separation against the registered 0.13 dex budget (5×), or against the
generic uncurated-dwarf coherent floor of ~0.34 dex (2×). Worth adding to the pre-registration's stated
deliverables by amendment; it costs no extra observing time.

---

## Target 4 — the lensing angle, closed with a number

Pantheon+ models lensing scatter as σ_lens = A × 0.055 z mag (A = 1, Jönsson et al. 2010). Lensing is
0.5 % of the per-SN variance at z ∈ [0.1, 0.4), rising only to 5.6 % at z > 1.2 — and Pantheon+ has just
**56 SNe at 0.7 < z < 1.2 and 19 above 1.2**.

Profile likelihood on A with a free intrinsic floor, 960 SNe at z > 0.1: **Â = 0.00, 1σ upper 0.52, 95 %
upper 1.02; A = 0 disfavoured at 0.0 σ.** The **1σ-equivalent width on A is 0.51**. Read as a degeneracy,
not a tension — Pantheon+'s own survey-dependent floor and z-dependent bias-correction scatter absorb a
rising term, and allowing that freedom would only widen this interval.

What would have to be resolved: the kernel is *calibrated* to reproduce galaxy-galaxy lensing on these
scales (the KiDS radial-acceleration test, 0.601 σ on the record), so the framework's convergence field is
constructed to sit close to ΛCDM's where the data already are. A generous allowance for the residual
difference — all matter clumped with baryons instead of 85 % in smooth haloes — is |A − 1| ~ 0.3.

**Underpowered by a factor 3. This angle is dead; stop here.** That is an honest power calculation, not a
result.

---

## Bonus — the low-z Hubble diagram as a peculiar-velocity bound (new)

The angle the repo's supernova work has never used. `hunt_2026/h85_bulk_flow_null.py` records that the
kernel, applied naively to the linear velocity field, boosts it by ν ~ 9 at the Local Group acceleration —
while the framework's own relativistic completion carries a theorem (δY⁽¹⁾ = 0) making linear growth ΛCDM's.
Supernova magnitudes below z ≈ 0.06 are peculiar-velocity dominated, so the Hubble diagram bounds the boost
independently of any reconstruction.

567 SNe at 0.01 < z < 0.06; Pantheon+ assumes 250 km/s residual after its 2M++ correction. Fitted multiplier
**A_pec = 1.08, 95 % upper 1.40 → residual σ_v < 350 km/s**, with a simultaneously fitted intrinsic floor of
0.103 mag. A naive ν = 9 boost gives σ_v ~ 2250 km/s and 0.81 mag of scatter at z = 0.02 — **6× the bound.**

The obvious objection is answered in the script: the 2M++ correction is v_pred = β × (reconstructed density)
with β calibrated in ΛCDM, so a boosted velocity–density relation has a larger true β, the ΛCDM β removes
only ~1/ν of the flow, and ~8× the ΛCDM residual survives — which is exactly what the Hubble scatter
measures. The bound applies in the boosted world too.

**Both ways: a PASS for the framework's own relativistic completion, a KILL for the naive modified-gravity
reading of the velocity field, and a second independent route to h85's null on a dataset h85 never touched.
It is NOT evidence for the framework over ΛCDM — ΛCDM makes the identical prediction and the test cannot
separate them.**

---

## Three-sentence verdict

1. Supernovae are an **input** to this framework, not a test of it: on their own they show no dark-energy
   evolution at all (Δχ² = 0.52 for two extra parameters, 0.29 σ), the canonical-footing SN-only a₀(z) band
   at z = 2.5 is [0.36, 3.59], and the record's much tighter band is BAO+CMB geometry that the supernovae
   only help to close — so the framework's distinctive prediction is hostage to a preference the supernovae
   do not corroborate on their own.
2. The one place supernovae bite hard is the **registered prediction**: because the deep-MOND zero point goes
   as a₀^{1/4} and a₀ tracks ρ_DE, "flat 0.00 dex at z ≈ 2.5" holds only in the w = −1 limit — under every
   evolving-dark-energy fork the framework's own value is −0.085 to −0.131 dex ± 0.045 (66–101 % of the
   registered 0.13 dex budget; the deepest fork plus 1σ reaches 0.176 dex, past it), it appears bare in 8 of
   10 places on the record, and it should be registered by append-only amendment as a **band**, −0.148 to
   0.00 dex, not as a point.
3. Nothing here favours this framework over ΛCDM and nothing here is a win: the lensing angle is dead on
   arrival (Pantheon+ does not detect its own lensing term, and is 1.7× too coarse for the effect), the
   supernova-era a₀ archive is split 3–3 on the internal footing fork with the split falling along
   measurement **currency** rather than redshift — the signature of a z-dependent systematic in the slope
   estimators, not of a₀ evolution — and the one clean new result, the low-z Hubble diagram bounding any
   residual peculiar-velocity boost to under 1.4×, 6× below a naive kernel-boosted field, confirms the
   framework's own linear-growth theorem while making exactly the same prediction as ΛCDM.

---

## What another lane should pick up

- **The amendment.** Two append-only items for `PREREGISTRATION`-class documents, if the user wants them:
  the framework's z ≈ 2.5 band in place of the point, and the Δ_BTFR sign convention stated once,
  unambiguously. **Not done here — frozen artefacts are untouchable and amendments are the user's call.**
- **The footing fork as a registered deliverable.** D4 shows the already-pre-registered object decides it for
  free at 5× the budget. It should be named as an output of that observation.
- **Out of scope by instruction (lane L37):** the same footing fork at recombination and at nucleosynthesis.
  Nothing in this lane goes above z = 3.
- **Not attempted:** the w-dependence of the ΛCDM-native concentration–mass relation through the growth
  history (flagged in B3, second-order); a non-Gaussian (skewed) lensing likelihood for E, which would not
  change a verdict that is underpowered by 3×.
