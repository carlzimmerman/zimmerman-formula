# UV1_uv_power_truncation: kick NO EFFECT; cut UV-INSENSITIVE. The zooms' shape doesn't depend on the missing P(k) power, and r₋₂'s c_f is mostly noise

Criteria: `FROZEN_CRITERIA.md` (0ae8cbbdab), committed alone first. `uv1_zoom.py`, `uv1_read.py`, `uv1.out`, `uv1_results.json`, `uv1_checks.out`. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework.

Nine same-seed pairs at 10¹⁴, ng 64, against X48's and ZN1's runs.

| | NFW c at z_f, median \|Δ ln\| | η_S, median \|Δ ln\| | c₂₀₀ at z = 0, Δ ln | \|Δ ln m\| at x 0.1, 0.2 | r₋₂ c_f at z_f (unperturbed 10.07) |
|---|---|---|---|---|---|
| **Kick** (band's 2.70 km/s at z_i) | 0.033 | 0.034 | −0.031 | 0.023, 0.029 | 7.01 |
| **Cut** (P(k) zero above k_Nyq/2) | 0.040 | 0.037 | +0.011 | 0.019, 0.025 | 7.50 |

- **Argon's claim fails.** It predicted r₋₂ c_f in 4.5–5.5 and a fake spike removed. The kick does nothing beyond chaos on any stable estimator.
- **Removing half the mode range in k barely moves the shape,** under 3 % at the radii where X-COP is sensitive. So ZN1 and ZN3's shapes aren't an artefact of the mass-scaled cut-off, for this range of k.
- **r₋₂'s c_f fell from 10.07 to 7.0 and 7.5 under perturbations that left every other measure within about 4 %.** The fall appears in both runs, so it's the estimator's scatter, which backs X77's flag: the "A4 spike" isn't a physical measurement.

**Limits:** a test of removing power, extrapolated to adding it. Same particle number throughout, so resolution itself is ZN4's question. One mass. Paired differences include chaos, which I didn't separate. The reported z = 0.25 line and the regrade with these stacks weren't run, because nothing moved enough to matter.

**Checks:** K1 ICs equal X48's |d| 0; K2 constraints 2e-16; K3 kick σ within 1 %. ZK1's K3 stands.
