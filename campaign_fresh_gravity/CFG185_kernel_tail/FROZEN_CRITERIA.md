# CFG185 — the high-g tails of ν_mono and P2 against the Solar System, reconciled with GATES 4.01. FROZEN CRITERIA

Written 2026-09-29 at the orchestrator's request, before any CFG185 script or number.

- **What is being checked:** a spin-off reported, but not scored, by the orchestrator's CFG171 agent. It has not been verified independently.
  - The record's ν_mono kernel has a NON-DECAYING high-g tail. The anomalous acceleration never falls below 0.648 a₀, and is 1.18 a₀ at Earth: 2.9–3.6 × 10³ times the planetary bound.
  - P2's own a₀/2 tail is 1257–1540× that bound.
  - GATES 4.01 quotes the strict law at 4.0–5.7× its Q₂ ceiling.
- **What I have already seen:** the relayed numbers, and FP1's construction of ν_mono: a floor 0.05 H_P/(y + Y_P) on dh/dy.
- **So my hand expectation, disclosed:** above the RAR peak Y_P ≈ 2.54, the phantom h(y) = y(ν − 1) rises logarithmically from H_P ≈ 0.648, roughly as h ≈ H_P[1 + 0.05 ln((y + Y_P)/(2Y_P))], and is about 1.18 at Earth.

## Questions

- **Q1 — the tail, re-derived with my own code.**
  - I rebuild ν_mono from its definition (FP1's _h_rar, and the floored derivative integrated on the same grid) and compare it with CFG4_common's ν_mono. That comparison is C1.
  - I derive the high-y behaviour analytically, from the floor, and check it numerically.
  - I report h(y) at the Sun's photosphere, at Mercury through Neptune (the Sun's point mass, g_N = GM☉/r²), and at the table's clamp y = 10¹⁴.
  - I report the same for P2 (h → ½), and for the exponential RAR kernel (h → 0).
- **Q2 — against the planetary bounds.** The anomalous radial acceleration a_anom = h(y) a₀ at Earth and at Mars is compared with the record's verified bounds, δA_R ≤ 3.66 × 10⁻¹⁴ (Earth, 2σ) and 3.72 × 10⁻¹⁴ m s⁻² (Mars) (Sereno & Jetzer 2006 via Pitjeva EPM2004, in STANDING.md). Both footings, for ν_mono and P2.
- **Q3 — the reconciliation.** State which quantity each number is:
  - the monopole a_anom against δA_R;
  - GATES 4.01's Q₂, the tidal quadrupole of the strict law's EFE-modified field against Q₂ ≤ 5.2 × 10⁻²⁷ s⁻².
  - Also state which applies to candidate B. B passes via ownership: the host-phantom tide.
- **Q4 — the record.** A committed grep for statements that ν_mono (or P2) is Solar-System-safe as a bare law, listed by file and line. A note is appended to STANDING and GATES only if Q1 holds.

## Pass lines

- **Q1 holds** if both are true:
  - my ν_mono equals CFG4_common's to 10⁻⁶ in h over y ∈ [10⁻⁶, 10¹⁴];
  - h(y) ≥ H_P − 10⁻³ for every y ∈ [Y_P, 10¹⁴].
- **"1.18 at Earth" is confirmed** if h(Earth) lies within 0.02 of 1.18 (canonical footing).
- **Q2's ratios are reported as computed.** The relayed "2.9–3.6 × 10³" and "1257–1540×" are confirmed if my values fall within 5% of their ranges.

## Controls and MUTATE

- **C1:** as above (my rebuild against CFG4_common).
- **C2:** P2's h(y) = y(√(1 + 1/y) − 1) → ½ − 1/(8y) (sympy).
- **C3:** the RAR kernel's h(y) = y/(e^√y − 1) decays for y > Y_P.
- **MUTATE:** remove the floor (the pure RAR kernel). The tail must then decay, and Q1's "non-decaying" line must fail.

κ = ½ and Ω_c h² stay fitted. Nothing here changes candidate B's verdicts; it concerns bare kernels.
