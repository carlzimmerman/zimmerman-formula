# CFG677 FROZEN CRITERIA: answering the two GW questions ourselves (forecasts, assumptions explicit)

Date: 2026-10-12. Block CFG670–679. Committed ALONE before any CFG677 code or number. Forecast lane: no data verdict.
κ = ½ FITTED; cold energy mass required; not "theory closed". Seen: CFG675 band radii (last 5 yr probe 3e-10–5e-8 pc).

## Q1 — how strongly does a no-dephasing IMRI bound the dark density?
- CFG675's inspiral model (GW + dynamical friction, last 5 yr to ISCO), systems 1e3+1.4 and 1e4+10 M☉.
- Profiles ρ = ρ_p (r/r_p)^−γ, γ ∈ {1, 3/2, 7/3}, r_p = geometric mean of the 5-yr band radii (the radius actually probed).
- Detectability thresholds (stated assumptions, not derived): ΔN_th = 1 and 10 cycles.
- Report ρ_p at ΔN = ΔN_th, its extrapolation to 1e-3 pc for each γ, and the ratio to the CFG675 framework ceiling and kill line
  (10 × ceiling) at the same radius.
## Q2 — what σ(w0, wa) from 3G bright sirens alone?
- Own Fisher forecast, parameters (H0, Ωm, w0, wa), flat, radiation neglected, no external priors ("GW alone").
- Events: N ∈ {100, 300, 1000, 3000} bright sirens with redshift, n(z) ∝ z² e^{−z/0.6} truncated at z = 3 (assumption: counterpart-
  limited, peaking near z ≈ 1); per-event σ_lnD = √(σ_inst² + σ_lens²), σ_inst = 0.05 (assumption), σ_lens(z) = 0.066
  [(1 − (1+z)^−0.25)/0.25]^1.8 (the commonly used weak-lensing fit; recalled form, labelled provisional), and a 50 %-delensed variant.
- Report σ(w0), σ(wa) and their correlation, and whether CFG676's z = 3 requirement (σ(w0) ≲ 0.06, σ(wa) ≲ 0.04–0.11) is met.
- Variant (context): + a Planck-like Ωm prior σ = 0.01 (not GW-alone).
## MUTATE (`CFG677_MUTATE=1`)
Q1: ρ_p → 0 gives ΔN = 0; Q2: σ_lnD halved must shrink σ(w0) by 2 (exit 1 iff both bite).
