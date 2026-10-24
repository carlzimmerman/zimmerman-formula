# O1_ownership_action — ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY, plus RECORD (a number from
a verified lane, used as written), POSTULATED (a choice of this lane or of the record), NON-VARIATIONAL (no action).

## A. The theory under test

| ingredient | class | note |
|---|---|---|
| v3s PN system: Ξ = Φ − σ̇ + ½\|∇σ\|², 4πGρ_τ = ∇·[(1 − μ)∇Ξ] (μ_K = 0), ∇²Φ = 4πG(ρ_b + ρ_τ), Dv_τ/Dt = −∇(Φ − Ξ) | FRAMEWORK-NATIVE | U1 script header, H5 A1; μ = x/(1+x), x = \|∇Ξ\|/a₀ (AQUAL, not QUMOND) |
| J_x (static limit AQUAL exactly) | POSTULATED (record) | C4 |
| switched stiffness −(γ_L/2)[max(D·P,0)]², γ_L = K L★²/2 | FRAMEWORK-NATIVE (v3s), L★ FITTED lower bound | X3; enters K2 only as a local stiffness U(s) |
| mimetic dust as the cold supply; R1 capacity; R2 ownership | POSTULATED (Z1); R2 NON-VARIATIONAL | the object this lane tries to derive |
| held phase carries Ξ-charge equal to its mass (α = 1) | FRAMEWORK-NATIVE (derived in the record) | X6 X-D1/X-D3, CFG941 D-T, CFG946 D-T′, L-AR |

## B. Record inputs (read-only, reproduced or cited)

| input | class | source |
|---|---|---|
| ε_B = 0.344 / 0.317 (differential acceleration allowed by CFG874's statistic) | RECORD | CFG945 README |
| Z2 fixed-M_V host-field slope −0.05 ± 0.19; v3 static −0.55; AQUAL + EFE −0.76 | RECORD (RAW kinematics + record predictions) | Z2 README |
| U1 N5: satellites B0 +2.00 ± 0.08 / +1.99 ± 0.07; Coma B0 +1.41 dex z_sys 5.4; TDG B0 +0.055 ± 0.114; DF2/DF4 | RECORD | `U1_v3_dust_content/u1_v3_dust_content_results.json` |
| U1 F5 Ursa Major members (12.6–14.4σ if the group's khronon is held) | RECORD | U1 README A2 |
| D10 per-cell Δχ²_Newton, AQUAL; cluster table (σ, r_hl, L_V, R_GC) | RECORD (RAW kinematics; SPS Υ_V prior is SURVEY-CALIBRATION) | `doors_push_2026_10_22/D10_native_Lstar/d10_native_lstar_results.json` |
| H5: Galilean covariance, steady response δρ_τ = δρ_m/[M − 1 + ΘL★²k²/2 − (k·V)²/(Kρ̄)], r_cap = 2GM_b/V², PROXY GC speeds 167–175 km/s, V_apo,10 ≈ 36 km/s | RECORD (verified-pending, 568a6b6709) | H5 README; GC 3-D speeds MISSING on disk (PROXY) |
| Galactic phantom density at the Sun 0.0447 / 0.0514 M☉/pc³ | RECORD (H4 disc solver via X3) | X3 README |
| Hees 9.0e-27 s⁻², Park 5.2e-27 s⁻² Cassini Q₂ lines | RECORD | D7d, C6 READMEs |
| MW baryons 6e10 M☉ (E_mid), bracket 4e10–1.2e11 | RECORD (SURVEY-CALIBRATION masses) | D10 JSON `MW_Mb`, S1 |
| f_s = 5.364 supply ratio | ΛCDM-PROCESSED (abundance) | Z1 ledger; used only for Z★'s supply-edge reading of ε |
| X1 class excesses over the isolated law (+0.28/+0.24, +0.63/+0.59, +0.25/+0.21, +0.64/+0.59) | RECORD | Z1 DESIGN §4, X1 README |
| Sun's speed through the Galactic khronon 220 / 250 km/s | SURVEY-CALIBRATION (v_c bracket) | assumes the held Galactic khronon is static (irrotational, cannot co-rotate: K7) |

## C. Simplifications of this lane (disclosed)

| item | effect |
|---|---|
| satellites treated as compact in the host field (BM-type far field) | exact in 1D (K2); 3D uses the linear far-field identity (K4) and U1's nonlinear N4 check |
| spherical host for ε (Gauss) | exact for spherical hosts; a disc host changes ε at O(flattening) at 50–250 kpc |
| Solar-System tide from the linear wake (H5 A3, V → ∞ limit), order-of-magnitude line-mass estimate | estimate only; the Danby–Camm caustic on the downstream axis is not regularised by γ_L at Mach ≫ 1 (OPEN, also in v3s) |
| (g) uses the deep-limit closed forms | the record's K9 is a "≥" bound in the same limit |
| no PDE evolution of a co-moving bubble | the statement is a momentum/Gauss theorem, not a simulation |
