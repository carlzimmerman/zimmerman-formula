# CFG59 — is there one universal fraction of the leftover debris? (a frozen consistency question)

Script: `CFG59_universal_debris_fraction.py` (about 12 s). Outputs: `.out`, `_results.json`, and the MUTATE pair. Requested by the coordinating session as a pre-registered look at whether the committed failures share a cause. Written by a delegated agent; the question was frozen verbatim in the docstring before the first run and re-run here. The main run passes 5 of 5; the MUTATE run fails the headline gate as required.

**The question, frozen:** scale the sum rule's debris acceleration by φ ∈ [0, 1] (φ = 0 the bare law, φ = 1 the sum). For each population find φ_needed (the φ at which its declared offset is zero) and the interval of φ within 1σ. **YES only if all ten intervals have a non-empty common intersection.** No φ is selected, fitted or recommended; a YES would be consistency with a universal fraction, not a derived rule.

## Answer: NO, on both footings

| population | offset at φ = 0 | at φ = 1 | φ_needed | 1σ interval |
|---|---|---|---|---|
| MW ultra-faints | +3.77σ | −0.41σ | 0.74 | [0.39, 1] |
| MW classical dSphs | +0.32σ | −1.78σ | 0.05 | [0, 0.39] |
| M31 Collins+13 | +0.78σ | −0.22σ | 0.80 | [0, 1] |
| M31 LVD | +0.60σ | −2.67σ | 0.12 | [0, 0.30] |
| SLUGGS | +3.28σ | +0.39σ | none in [0,1] | [0.81, 1] |
| X-ray ellipticals | +1.70σ | +1.04σ | none | empty |
| Di Teodoro S0/S0a | +0.05σ | −0.80σ | 0.03 | [0, 1] |
| UGC 2487 | +0.90σ | −1.05σ | 0.38 | [0, 0.96] |
| Boötes I (multi-epoch) | +2.46σ | −2.30σ | 0.29 | [0.14, 0.52] |
| Tucana II (multi-epoch) | +3.63σ | −1.29σ | 0.44 | [0.22, 0.84] |

**The binding conflict is SLUGGS (φ ≥ 0.81) against M31 LVD (φ ≤ 0.30): a gap of 0.51** (alt 0.46). Five pairs are disjoint on each footing (LVD–SLUGGS, classical–SLUGGS, SLUGGS–Boötes I, ultra-faints–LVD, ultra-faints–classical; the last two are marginal: gaps 0.09 and 0.001). The X-ray ellipticals have no φ in [0, 1] alone, but only at 1.04σ. **Dropping the ultra-faints, SLUGGS and the X-ray ellipticals leaves [0.22, 0.30]** (alt [0.21, 0.22]): the low-mass classical, LVD, Boötes and Tucana group wants φ ≈ 0.2–0.3, SLUGGS wants at least 0.8, the ultra-faint KM median at least 0.39.

Mass split (descriptive, declared in advance): below log M_* = 7 six populations, empty intersection (non-empty if the ultra-faint KM median alone is dropped); none in 7–10; above 10 four populations, empty only because of the X-ray 1.04σ (without it [0.81, 0.96]). Spearman of φ_needed with log M_*: ρ = −0.57 (p 0.14, n = 8): not significant.

## Controls and fragile assumptions

C1a/C1b pass (φ = 1 reproduces CFG45's S and φ = 0 its L, 100 + 40 comparisons, worst deviation 0); C2 passes (every offset is monotone in φ). MUTATE (collapse masses ÷ 100): the ultra-faint offset stays at +0.32 (2.5σ) at φ = 1, so no φ closes it, and the headline gate fails as required. Fragile: the clamped Moster relation (φ_needed for the ultra-faints, Boötes I and Tucana II is tied to the collapse-mass floor); the NFW cusp; the lane error models unchanged; Boötes I's offset includes its hot component (cold alone ≈ 0, which would move its interval's lower edge to 0); Tucana II may be tidally inflated; the ultra-faint KM median, Boötes I and Tucana II are not independent; the 1σ band is loose and φ = 1 is the sum itself, so a YES would have been weak.

## Standing

**One multiplier of the sum's debris term does not reconcile the lanes.** The low-mass satellites want about a quarter of the debris and the most massive early types want nearly all of it. That is a statement about the sum's mass dependence, not a rule. Nothing here says the theory is closed.

**Kernel note (CFG64).** This lane's estimator uses the exponential RAR kernel (`hunt_lib.nu_s`, ν = 1/(1 − e^{−√y})), not ν_mono as the text above says; the two agree to 3 × 10⁻⁹ for y ≤ 0.1. Swapping the kernel to P2 leaves the headline verdict unchanged (see `CFG64_kernel_robustness/README.md`).

## Referee corrections (09-28 audit of the lane READMEs against their outputs; appended, the text above is unchanged)
- Superseded in part by CFG71: with JAM-calibrated SLUGGS masses no phi in [0,1] brings SLUGGS within 1 sigma, and the binding pair becomes the ultra-faints against the LVD (gap 0.087 | 0.164). 'The most massive early types want nearly all of it' no longer holds. The [0.22, 0.30] group exists only after dropping the ultra-faints (KM median needs phi >= 0.39), SLUGGS and the X-ray ellipticals.

## Referee correction (09-28 audit of the peer lanes; appended)
- The NO holds at the frozen 1 sigma-per-population acceptance. At 2 sigma the ten populations share a common phi (canonical [0.52, 0.71], alt [0.33, 0.66]), see CFG75. A 1 sigma band is the strict criterion, so the remark above that 'the 1 sigma band is loose ... a YES would have been weak' is imprecise: at 1 sigma a YES would have been demanding.
