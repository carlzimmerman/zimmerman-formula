# CFG677: our own answers to the two GW questions (forecasts; assumptions explicit)

Criteria 0ec641cf5 (committed alone; block CFG670–679). `cfg677.py` → `cfg677.out`, `cfg677_results.json` (uses CFG675 v2's
physics). MUTATE bites (exit 1). κ = ½ FITTED; cold energy mass required; not "theory closed". No data verdict.

## Q1 — "how strongly could LISA bound the dark density at 1e-3 pc?"
**Answer: it can't, directly.** The last 5 years of an IMRI probe the density at **~2e-9 pc (1e3 M☉) to ~1e-8 pc (1e4 M☉)**, not
1e-3 pc. A no-dephasing inspiral (ΔN < 1 cycle) bounds ρ < **6e14 (γ=1) – 6e15 (γ=7/3) M☉/pc³ at the probed radius**; anything at
1e-3 pc is a slope extrapolation:

| profile slope γ | bound extrapolated to 1e-3 pc (ΔN<1, 1e3 / 1e4 M☉) | vs our kill line (1.1e6) |
|---|---|---|
| 1 | 1.1e9 / 7.6e9 | 1000–6500× above it: **cannot test** |
| 3/2 | 3.3e6 / 5.2e7 | 3–44× above: **cannot test** |
| 7/3 (particle-DM spike) | 2.1e2 / 1.3e4 | 2e-4 – 1e-2 of it: **easily tests** |

So a LISA null **does** decisively exclude steep particle-DM spikes (the case that would kill the framework if found), but cannot
probe a shallow profile at the framework's ceiling (which sits at 1e10–1e11 at the probed radius, 4 decades below the bound).
Also: the 1e3+1.4 system's last 5 yr lie at 0.02–4 Hz (deci-Hz band); LISA's best source here is the 1e4+10 system (0.005–0.4 Hz).
→ **Reframe the kill line for the contact:** "a measured γ ≳ 2 density at ~1e-8 pc around an isolated IMBH" kills the framework.

## Q2 — "what σ(w0, wa) from 3G bright sirens alone, out to z ≈ 3?"
Own Fisher forecast (H0, Ωm, w0, wa free; n(z) ∝ z² e^{−z/0.6} to z = 3; σ_inst = 0.05; weak-lensing fit, provisional):

| N bright sirens | GW alone: σ(w0), σ(wa) | + Ωm prior 0.01: σ(w0), σ(wa) |
|---|---|---|
| 100 | 1.05, 5.6 | 0.45, 1.1 |
| 1000 | 0.33, 1.8 (0.31, 1.6 delensed) | 0.15, 0.46 |
| 3000 | 0.19, 1.0 (0.18, 0.90 delensed) | 0.10, 0.35 (0.09, 0.34) |

**Answer: GW alone does not reach CFG676's requirement (σ(w0) ≲ 0.06, σ(wa) ≲ 0.04–0.11) even with 3000 bright sirens**; w0–wa
are 95 % anti-correlated and lensing dominates at z > 1. The a0–siren consistency test needs either far more sirens with redshifts
(dark sirens with galaxy catalogues, or 1e4+), or sirens combined with an independent Ωm. It is a 2040s test, not a 2030s one.

## What to ask the GW contact now (sharpened by these answers)
1. "For a 1e4 + 10 M☉ IMRI at LISA SNR ~ 20–50, what dephasing (cycles or radians) is the practical detection threshold, and how
   well is the slope γ of an environmental density at ~1e-8 pc measured?"
2. "Are there realistic 3G scenarios with ≥ 1e4 sirens with redshifts at z ≥ 2, or is cross-correlation with galaxy surveys the
   only route to ρ_DE(z) at z ~ 3 from GWs?"
