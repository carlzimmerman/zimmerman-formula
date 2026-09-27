# ANSWER-ROWs received from the owning sessions

These are the raw rows the owning sessions sent back under the assembly protocol, copied verbatim apart from line
wrapping. ANSWER_AS_IT_STANDS.md is built from them.

Format: `lane | commit | MODEL TAG | gate(s) | verdict + numbers | scope | controls`. Model M*: the MOND-sector switch
(CV3's constrained form), MS5's κ-form cap, p = 1, x_c0 = 2.5, w ≤ 0.25, ν_mono, σ = 1, and L388's carrier.

## Dark-energy thread

**DE9 | 8c3bfe8f3 (+aa5705194, numbers unchanged)**
- **Model tag:** two switch readings, reported separately:
  - the MOND sector, ρ_b + ρ_ph − f_b ρ̄ (on-branch and static; not CV3's varied form);
  - curvature.
- Cap none. p ∈ {0.5, 1, 1.5, 1.9}; x_c0 scanned; w ∈ {0.1, 0.25, 0.5, 0.75}, plus a near-hard 0.02. ν_mono.
  σ = 1, 1/m = 0.1 Mpc (DE8's operator). No carrier (switch-only). Both footings.
- **Gates:** the KiDS cap and the flagship cap (z = 2.5, 1e11), recomputed with the smooth gate. The forest by a
  dominance bracket. Shear not used.
- **Verdict:**
  - At p = 1 the MOND-sector reading allows w ≤ 0.5: x_c0 ∈ [2.0, 3.35] at w = 0.25 (M*'s 2.5 is inside) and
    [3.0, 3.09] at w = 0.5. The curvature reading allows w ≤ 0.25.
  - The KiDS cap falls from 4.48 to 3.76 as w goes 0.1 → 0.75 on the MOND-sector reading.
  - There is no window at w = 1.
- **Scope:** isolated spherical lenses, and no carrier lensing (that was added in DE10).
- **Controls:** C1/C2 reproduce DE2's hard caps to 0.1% and 0.7%. MUTATE (a hard gate at the midpoint) fails W1,
  rc = 1.

**DE10 | dabce1b73**
- **Model tag:**
  - The switch is the MOND-sector reading, carrier-blind: an on-branch static profile, prescribed rather than varied.
  - The cap is MS3's local |g|²/∇²Φ form, which MS5 withdrew. It does not bind on any KiDS lens (scaling 1.0000), and
    the κ form doesn't bind either for v_f ≤ 247 < 325 km/s, **so the result carries to M* unchanged.**
  - p = 1, x_c0 = 2.5, w ∈ {0.02, 0.25}. ν_mono. σ = 1, 1/m = 0.1 Mpc.
  - The carrier is L375's shell model at L390's settings, kicked at 600 and 650 km/s, amplitude 1. Both footings.
- **Gate:** KiDS-1000 (L352's fit, with a free 2-halo term).
- **Verdict: PASS.**
  - At 600 km/s: −37.0/−34.0 (hard) and −32.3/−29.3 (w = 0.25).
  - At 650 km/s: −36.8/−33.7 and −32.1/−29.0.
  - That beats the curvature branch with the same carrier (L390: −13.1/−7.2).
- **Scope:**
  - Isolated lenses; L375's fiducial accretion history.
  - The carrier masses come from L390's curvature-branch refit, not a refit on M*.
  - The 2-halo amplitude is free, and XR9 reports it.
- **Controls:** C1 reproduces L390 exactly. MUTATE (v_k = 0) fails at +133/+137, rc = 1.

**DE11 | aa6588d56**
- **Model tag:**
  - The switch is the MOND-sector reading x = 1.5 Ω_m(a)[f_b δ + δ_ph], with the phantom lagged one step. No cap
    (it doesn't bind in the IGM).
  - p = 1, x_c0 = 2.5, w ∈ {0.25, 0.02}. ν_mono.
  - The operator is L347's single-fluid particle-mesh QUMOND. Its kernel reads ALL matter, so it OVER-states M*'s
    phantom, which makes it conservative. No carrier. Both footings.
- **Gate:** the Lyman-α 1D flux power, L347's rule: deviation ≤ 0.10 for k_par = 0.2–2 h/Mpc at z = 3 and 2, in both
  boxes.
- **Verdict: PASS.** The worst deviation is 0.0041 (25 Mpc/h, alt, z = 2); it is 0.0009 at 50 Mpc/h. The active
  mesh fraction is 2–5e-4 at z = 2.
- **Scope:** convergence is being tested in DE11b, since the deviation grows ×4.6 from 50 to 25 Mpc/h. One phase per
  box. FGPA.
- **Controls:** C1 reproduces L347 exactly; C2 (never on) is ΛCDM exactly. MUTATE (L358's matter-reading cell)
  reproduces L358's 0.174 and fails, rc = 1.
