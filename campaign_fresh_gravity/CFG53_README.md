# CFG53 — massive passive disks by shape: does the outer rotation curve of a red disk rise as the derived rule says?

Script: `CFG53_passive_disk_shapes.py` (both footings; about 20 s). Its MUTATE control exits 1 as required. Outputs: `CFG53_passive_disk_shapes.out` / `_results.json`, and the `_MUTATE` pair.

## Why

CFG41 scored Di Teodoro+2023's 15 massive HI disks (four S0/S0a) by the **amplitude** of the flat part and could not tell the bare law from B's derived cold-mass rule. Two things set its floor:

- the 0.2-dex stellar-mass systematic, which enters the rule steeply through the collapse mass;
- the sample's cut on HI width, which biases every amplitude high.

This lane tests the **shape** instead. The rule's debris is an NFW component of the collapse mass. Inside 30–97 kpc its circular speed rises, while the law's outer curve is flat or gently falling.

- **Robust to CFG41's limits.** The outer logarithmic slope barely moves with the law's stellar-mass normalisation, does not move at all with distance under the law, and a cut on speed does not select on it directly.
- **A built-in control.** The rule gives debris to red disks only (f_ex = 0 for every blue galaxy here). So the red-minus-blue slope difference cancels what both colours share: tilted-ring fitting, warps, the beam, the estimator and the width cut.

## Method (declared before the first run)

- **Machinery:** CFG41's, executed read-only. That covers the data, the colour convention (RC3 T ≤ 0 is red), CFG36's collapse masses, the conservation form at x_e = 0.40, ν_mono, and point-mass baryons with sphere/Freeman brackets.
- **Outer slope:** a weighted least-squares fit of ln V on ln R over the points with R ≥ R_max/2. Weights are (V/dV)². The formal error is multiplied by √2 because adjacent rings share the beam.
- **Predicted slopes:** the same estimator, with the same weights, applied to the law's and the rule's speeds at the same radii.
- **Statistic:** D_obs = ⟨s_obs − s_law⟩_red − ⟨s_obs − s_law⟩_blue. The rule predicts D_rule; the law predicts 0.
- **Systematics:** each applied to every galaxy at once, as half the spread of the tested quantity. They are the baryon model, M_* ± 0.2 dex, M_gas ± 0.1 dex, and distance ± dD.

## Result

| | canonical | alt |
|---|---|---|
| red disks (4): observed slope minus law | +0.014 ± 0.124 | +0.005 ± 0.124 |
| red disks: the rule predicts | +0.155 | +0.128 |
| blue disks (11): observed slope minus law | +0.052 ± 0.041 | +0.044 ± 0.040 |
| (D_obs − D_rule)/σ | **−1.22** | **−1.04** |
| power, D_rule/σ | 0.98 | 0.80 |

- **Controls:** C1–C3 passed. CFG41's committed four-S0 numbers are reproduced exactly, the radius-resolved speeds match CFG41's to 0 km/s, and the slope estimator is exact to 7e-17.
- **H1 passed.** The law fits the blue shapes (+0.93σ).
- **H2 failed.** The red disks' outer slopes sit on the law, not on the rule: −1.22σ (canonical) and −1.04σ (alt) against the rule, short of the declared −2σ.
- **H3 failed.** The rule's predicted red-blue difference is only 0.98σ, so the shape cannot decide. This is the declared reading.
- **MUTATE**, where the data are given the rule's shape: (D_obs − D_rule)/σ moves to −0.24σ and the script exits 1.
- **Reported rows:**
  - the absolute red test is −0.96σ against the rule and +0.11σ against the law;
  - with WISE colours (six red disks) the rule's predicted difference shrinks to +0.013, and the power to 0.14;
  - with the two flagged galaxies removed it is −1.10σ, with power 0.74;
  - amplitude (CFG41) and shape combined (Stouffer) give **−1.25σ against the rule**.

### Error budget (canonical, on D_obs − D_rule)

| Source | Size |
|---|---|
| statistics (four red disks, 4–6 outer points each) | 0.131 |
| stellar mass ± 0.2 dex, applied to all galaxies at once | 0.083 |
| distance | 0.032 |
| baryon model | 0.015 |
| gas mass | 0.001 |
| **total σ** | **0.159** |

The stellar-mass term alone caps this test at 0.155 / 0.083 = 1.9σ, however many red disks are added. A decisive shape test needs stellar masses known to about 0.1 dex (dynamical M/L) as well as more massive red disks with extended HI.

## Reading

**The shape cannot decide, which is the declared reading.** All the massive-passive-disk measurements lean the same way: the red disks show no sign of the rule's debris and sit on the bare law. None reaches 2σ.

| Measurement | Result |
|---|---|
| UGC 2487 (CFG36) | +0.14 dex over-predicted by the rule |
| amplitude of the four (CFG41) | −0.8σ against the rule |
| shape (this lane) | −1.0 to −1.2σ against the rule |
| amplitude and shape together | −1.25σ against the rule |

A post-hoc contrast, which is not a test: the SLUGGS massive ellipticals (CFG38) prefer the rule, with the law 3.3σ short and the rule at 0.4σ. If both results hold up, the debris would follow morphology (merger-built ellipticals) rather than colour, whereas the rule as derived uses colour. That is not established.

Hypotheses and scope:

- The analysis is spherical and uses point-mass baryons at 17–97 kpc, with sphere/Freeman brackets at R_d = 8 kpc.
- The curves are Di Teodoro+2023's as read from their atlas (CFG41's file).
- No ΛCDM comparison is made.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.


## Corrections from the referee sweep (appended 2026-09-29; no result changed)

- **The SLUGGS contrast above is stale.**
  - It used CFG38's population-mass result: the law 3.3σ short, the rule at 0.4σ.
  - With each galaxy's own JAM-calibrated stellar mass (CFG55, 791083f7f), the law is 4.0σ short and the rule still leaves +0.046 dex (2.6σ).
  - The measured hot gas does not change that. CFG57 (9b071a024) is non-diagnostic: the gas shifts the mean by 0.01 dex.
  - So SLUGGS no longer prefers the rule, and the remark about morphology versus colour loses its SLUGGS support.
- **"Its MUTATE control exits 1 as required" says nothing here.** The main run also exits 1, failing the same two checks (H2 and H3). What the control shows is the statistic moving (to −0.24σ when the data are given the rule's shape), not the exit code.
