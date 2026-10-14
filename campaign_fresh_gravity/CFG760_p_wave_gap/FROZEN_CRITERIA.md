# CFG760 FROZEN CRITERIA: can P-wave radiation export the infall energy of cold energy? (the vacuum gap test)

Date: 2026-10-13. Block CFG760–769 (reserved for this chat by the owner, 2026-10-13). Written and committed ALONE, before any script
or number. Nothing below may be edited after this commit. κ = ½ FITTED; both footings, never pooled; the cold energy's mass is
required; no particle species; not "theory closed".

## Why
CFG749: cold energy must sit nearly at rest in each system's frame; cold energy arriving at infall speeds (~V_flat) must lose most
of its kinetic energy. CFG744: the only damping in the construction is radiation of the light polarization field P, which must
have c_P large enough to relax P itself. Other export routes are astra's (sol61_push cold_final_mile: receiver, selective
cooling, photon bath) and the CFG750 sink lane; this lane tests only P radiation.

**Hypothesis to test (stated before any number).** Linearising CFG696's equation about the law's own static profile v₀ gives
perturbations a position-dependent mass term 2|v₀|/s (the curvature of the cubic W, i.e. of the deep law itself). Motions with
code frequency ω below the local gap ω_g(s) = √(2|v₀|/s + 2/s²) cannot radiate locally; their energy reaches infinity only by
tunnelling. Galaxy-scale motions have ω = (V/c_P)/s₀ with s₀ = r/ℓ_γ ~ 10⁴–10⁸, so they may sit far below the gap.

## Equations (CFG691/696 units; s = r/ℓ_γ, t in ℓ_γ/c_P, ℓ_γ = L*²/(2r_M))
- Static profile v₀ = s q₀ from CFG691's BVP (as in CFG696); v₀ = 1 − 1/s beyond s = 10⁴.
- Linear perturbation: δv_tt = δv″ − 2δv/s² − (2|v₀|/s)δv + J.
- Harmonic point source at s₀: u″ + k²(s)u = J δ(s − s₀), k² = ω² − 2/s² − 2|v₀|/s; u regular at 0 (u ∝ s²), outgoing WKB at
  the outer boundary S_out ≥ 50·max(s₀, 2/ω²) where ω² ≫ |k² − ω²|.
- Radiated power P ∝ ω|u₁(s₀)|² Im(u₂*u₂′)/|W|² (W the Wronskian). **Reference** (no vacuum curvature): k_ref² = ω² − 2/s².
  **Suppression** S(ω, s₀) = P_full/P_ref.
- WKB exponent ΔE = 2∫_{s₀}^∞ κ_full ds − 2∫_{s₀}^∞ κ_ref ds, κ = √max(0, −k²).

## Controls
- **K1.** Static profile reproduces CFG691's S table to ≤ 1e-6 (as CFG696).
- **K2.** Im(u₂*u₂′) (the flux invariant) is constant to ≤ 1e-6 relative across [s₀, S_out], full and reference.
- **K3.** Above the gap (ω = 2ω_g(s₀)), S ∈ [0.3, 3] for every s₀ in G1: radiation is not suppressed there.
- **K4 (time domain, nonlinear CFG696 equation).** s₀ = 20: a small oscillating source added to CFG696's full nonlinear equation
  about the static profile, outgoing boundary. Outgoing flux at ω = 2ω_g vs ω = 0.5ω_g: the below-gap flux must be ≤ 1e-3 of the
  above-gap flux (same source amplitude), and the above-gap flux ratio full/reference must agree with the frequency-domain S within
  30%.

## Tests
- **G1 (the gap).** s₀ ∈ {20, 50, 200}, ω/ω_g(s₀) ∈ {0.5, 0.7}. **PASS iff** for every case with ΔE ≥ 5:
  ln S_num/(−ΔE) ∈ [0.8, 1.25] and S_num ≤ 1e-2.
- **G2 (the physical pincer).** Both footings; L* = 5.754 pc (CFG691 L*_min); M_b ∈ {10⁹, 10¹⁰, 10¹¹, 10¹²} M☉; y ∈ {0.1, 0.01}
  (r = r_M/√y, the outer halo where CFG749 needs dissipation). s₀ = r/ℓ_γ; infall speed V = 2V_f, V_f = (GM_b a₀)^{1/4} (favourable
  bracket: CFG749 infall is ~V_f); ω = (V/c_P)/s₀; v₀ from the profile.
  - Export allowed iff ΔE(ω, s₀) ≤ 1 (favourable: assumes the free problem radiates all the energy per orbit). This gives
    c_P,max(case).
  - P's own relaxation (lenient, exponent-free one-crossing bound of CFG744): r/c_P ≤ 13.8 Gyr, which gives c_P,min = r/13.8 Gyr.
    Also reported: c_P,min from CFG744's frozen law t = 2.56 s₀^{3/2} ℓ_γ/c_P ≤ 4.6 Gyr.
  - **CLOSED iff c_P,max < c_P,min in every case, both footings** (no c_P lets P radiation both export the infall energy and relax
    P). OPEN otherwise, with the open cases listed.
- **G3 (the escape hatch: larger L*).** For each case, L*_open = the smallest L* (log grid 5.754 pc to 1e5 pc) at which
  c_P,max ≥ c_P,min. L*_all = max over cases. SPARC rms is computed at L*_all with CFG691's statistic (code copied, read-only data;
  K5: it reproduces CFG691's rms at L* = 5.754 and 1000 pc to ≤ 1e-4). **The hatch is OPEN iff L*_all exists on the grid and the
  rms is ≤ 0.110 for both footings**; otherwise CLOSED.

**MUTATE** (`CFG760_MUTATE=1`): drop the 2|v₀|/s term (no vacuum curvature). G1 must FAIL (S ≈ 1) and G2 must not be CLOSED.
Exit 1 iff both bite.

## Not tested (stated in advance)
Non-spherical modes (they add ℓ(ℓ+1)/s² barriers, which are only stronger, but are not run); large-amplitude nonlinear effects
(shocks or caustics with timescales far below the orbital one); the saturating W inside r_M; export channels other than P
radiation; whether cold energy is formed at rest instead (a separate question).
