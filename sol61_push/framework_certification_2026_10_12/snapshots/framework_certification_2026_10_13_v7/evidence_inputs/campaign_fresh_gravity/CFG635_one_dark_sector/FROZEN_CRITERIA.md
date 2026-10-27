# CFG635 frozen criteria: one dark sector (one field as dark energy AND cold energy)

Written and committed alone before any script. Date 2026-10-11. κ = ½ is FITTED. The two footings are never pooled (nothing
here depends on the footing except through a₀, which cancels in every ratio used). The cold energy's mass is required. No
dark-matter particle species is added to the framework; where a candidate amounts to one, the README says so. Not "theory closed".

## Question
Can ONE field play both roles: its smooth part is the dark energy that sets a₀ = κ c √(G ρ_DE), and its slow, lumpy excitations
are the cold energy (Ω_c/Ω_b = 5.364, collisionless, not heated, settles into the law's phantom and hands the settling energy
to the smooth part), without new tuned constants?

## Gates (requirements from the record)
- G1 smooth part: homogeneous w ≈ −1 today; its ρ_DE fixes a₀ (A2/A3).
- G2 cold part: dilutes as a⁻³, c_s² ≲ 1e-6 on linear scales, multi-streams (stream crossing, mergers; CFG288/L374),
  collisionless at Bullet level.
- G3 hand-off: a channel that moves settling (binding) energy from the cold part to the smooth part, regular (no division by a
  vanishing receiver velocity, CFG542 K10; no stall at receiver rest, astra regular_receiver_lift), with a local four-current
  (astra local_sink_reaction), and able to run in the direction required (astra collective_energy_lower: both signs occur).
- G4 no ghost / gradient instability on the side of the state the channel actually uses.
- G5 causal (CFG542 K9 spirit: no superluminal transport on the scales where the channel acts).
- G6 constants: count every mass/coupling/scale not fixed by a₀, ρ_DE or Ω_c. Each is a knob. Ω_c/Ω_b = 5.364 is an input
  unless derived.
- G7 relation: does the candidate predict 5.364 or a ρ_c–ρ_DE relation?
- G8 distinctive observable, if any.

## Verdict rule (per candidate)
- VIABLE AS A SKETCH: G1–G5 pass structurally and G6 knob count = 0.
- KNOB-DEPENDENT: G1–G5 pass structurally, knob count ≥ 1.
- OBSTRUCTED: any of G1–G5 fails structurally; the failing gate is named. The knob count is reported alongside.
- A partial component (e.g. a receiver that works but no cold part) is labelled for that component only and the candidate as a
  whole gets the label of its weakest gate.

## Checks (script cfg635.py; sympy + tiny numerics; one process, < 1 GB, nice -n 10)
- K1 single-real-field mass theorem: fluctuations have m² = V''(φ̄); G1 (frozen/thawing) needs V'' ≲ H₀², G2 needs
  m ≥ 2e-20 eV (CFG288 floor). PASS of the theorem = the ratio of required masses ≥ 1e10.
- K2 adiabatic exchange (complex field, radial cold mode + phase): sympy identity Q_{r→θ} = ṙ (∂_r V_b − r θ̇²); for a
  shift-symmetric phase the exchange is a total time derivative at fixed p_θ. Numerics: secular drift of the phase energy,
  mean over the last 10 radial periods vs the first 10, must be < 1e-3 (relative) for the shift-symmetric and the slow-pNGB
  cases. MUTATE: a resonant explicit breaking (ω_θ = m_r/2) must give relative growth > 0.5 (the control bites).
- K3 C1 numbers: f, λ = (m_r/f)², radial amplitude needed for Ω_c (scaled from CFG288's committed 0.0147 M̄_Pl at
  2e-20 eV), over-production for an O(1) amplitude, r → θθ decay rate vs H₀, self-scattering σ/m vs 1 cm²/g.
- K4 ghost-condensate receiver: sympy (i) w = −1 at P′(X₀) = 0 with θ̇₀ = √(2X₀) ≠ 0, (ii) H′(π = 0) = θ̇₀,
  (iii) the pair bracket M = m w wᵀ with w = (H′(π), −D) gives M∇E = 0, Ė = 0, Ṡ ≥ 0, and q̇(π = 0) = m θ̇₀² s ≠ 0.
  MUTATE: canonical receiver (H′(0) = 0) must give q̇(π = 0) = 0 (the astra stall returns).
  (iv) a deposit δX gives δp = 0 at first order (w_deposit = 0) and c_s² = δX/(2X₀) at leading order.
- K5 phantom-side stability vs causality for K4: γ_max = |c_s²| M_k / 2 from ω² = c_s² k² + k⁴/M_k²; stability over a Hubble
  time needs M_k < 2H₀/|c_s²|; phonons are superluminal for k > M_k/2. Report the superluminal length for the cosmic and local
  excursions.
- K6 local deposit relation: R(y) = ρ_ph V_c² / (ρ_DE c²) for a point mass, from the law and a₀ = κc√(Gρ_DE) only.
  sympy: deep limit R = κ² y/(4π) = κ² g²/(4π a₀²). Numerics: both kernels (exponential; repaired ν_mono read-only from
  CFG4_common). Report R at y = 1, 10, 30 and where R = 1.
- K7 Landau channel (superfluid two-fluid candidate): v_L = min ω/k = c_ph for Bogoliubov phonons (sympy); linear growth of
  the cold part with a uniform drag Γ = γ H₀ (framework-own linear equation, cold energy is cold matter outside bound
  systems): D(γ)/D(0) at a = 1 for γ = 0.1, 1, 10. Internal comparison only; no external yardstick.

## Candidates (at most three, chosen to avoid the record's closed constructions; see README section 1)
- C1 complex field: weakly broken U(1). Phase (pNGB, m_θ ~ H₀) = dark energy; radial oscillation (wave dust) = cold energy.
- C2 ghost-condensate receiver: P(X) phase at P′(X₀) = 0 (w = −1 with θ̇₀ ≠ 0) = dark energy; cold part from the same field.
- C3 superfluid two-fluid: condensate = dark energy; gapped normal component = cold energy; settling via Landau drag.
