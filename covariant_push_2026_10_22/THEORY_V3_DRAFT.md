# The screened theory, v3 (DRAFT — finish line of the 2026-10-22 pushes)

Status words: DERIVED (from listed premises), COMPUTED, POSTULATED, FITTED, OPEN, PENDING (lane running).
κ = ½ FITTED. Footings: canonical a₀ = 9.36e-11 m/s², alt 1.13e-10 m/s², never pooled. No dark-matter particle.
Never "theory closed". Every line cites the lane whose committed script backs it.

## 1. The action (one line)

The Blanchet–Skordis Khronon theory (arXiv:2404.06584) in its literal healthy form (C4, C5):
- metric g, khronon τ (preferred foliation), an independent spatial covector P,
- free function J chosen so the static limit is AQUAL with μ = x/(1+x) exactly (C4; this J lies outside BS's
  admissible class — POSTULATED),
- β = 0, η = 0 (no P kinetic term; η > 0 is ill-posed, C5),
- Blanchet–Skordis K(Q) dust sector (C4, C5),
- one stiffness term −(γ_L/2)(D·P)², γ_L = K L★²/2 (C1, C3, C4: absent from both AeST and BS; POSTULATED).

DSF-21's A33 is this theory with η > 0, which C5 shows is ill-posed; v3 drops η.

## 2. Parameters

| symbol | status | value | source |
|---|---|---|---|
| a₀ (κ) | FITTED | κ_Λ = 0.417 ± 0.095 (CFG493); Planck-free 0.414 ± 0.094 (E4) | thermal Z/4π is Milgrom's relation, a POSTULATE (A75) |
| L★ | FITTED, new constant (lower bound only) | EFE-aware native floor L★_95 = 21.7 pc (canonical) / 22.9 pc (alt) with the SPS Υ_V prior; 2.9–22.7 / 4.4–23.8 pc across Υ_V priors and the MW bracket (D10). Upper edge ~90 pc (LITTLE THINGS) | D10, E4, C3 |
| dust abundance (Ω_c-like) | FITTED (initial condition) | — | C2, C4 |
| u | measured function of scale, convention-dependent | 0.43–0.50 (E4, E1) | no mechanism (D6) |
| G_cosmo/G_N | bounded | Planck-lite ±0.027 (C2 emulation); BBN | C2 |
| μ_K (K(Q) mass of the BS dust) | FREE, and **no allowed value** (see §3 growth) | BS24 Eq. 39 caps μ_K ≤ 14.8 h/Mpc; keeping σ₈ within 5 % of the dust limit needs μ_K ≥ 361–2542 h/Mpc — a gap of 24–172× | F3 |

## 3. Tests

| test | result | lane |
|---|---|---|
| galactic law (RAR) | the law itself (AQUAL μ = x/(1+x)) | E2, C4 |
| health (ghosts, gradients) | CONDITIONALLY HEALTHY in literal form; tensor modes at c | C5 |
| instantaneous constraints / well-posedness | WELL-POSED (weak-field leaf problem: one strictly convex functional, elliptic for all u < a₀, unique for γ_L > 0) + UNCONSTRAINED (binary pulsars: no radiative channel, ≤ 3e-14 of the double-pulsar error; GW speed exactly c). Violates criterion A by a real but tiny signal; meets criterion B. OPEN: infinite-volume theorem, coupled GR + leaf + dust, strong fields | C8 |
| Cassini Q₂ | healthy literal form (γ_F = 0): all 24 cells pass Hees and Park; Q₂ 0.93–1.86e-34 s⁻² at 24 pc, 1.8–3.5e-36 at 90 pc (2.8e7–5.1e9 inside); hedgehog has no quadrupole. Frozen rule reads UNDECIDED on one float-cancellation check (identity exact in sympy). Unscreened law fails 2.4–5.2× (E2) | C6, D7d, E2 |
| planets | hedgehog GM/L★²: at 24 pc Mars 0.17, Saturn 0.035, Earth 0.028 of their bounds | C6 |
| wide binaries 20 kAU | screened γ_v − 1 ≈ 8e-6 vs law-first 1.167/1.199; DR4 decides (σ_sys rule A3) | D2, D7d, E2 |
| outer globulars | unscreened law (L★ = 0) excluded in all 18 cells (Δχ² 4.9–22.8); no finite L★ beats Newton; sets the L★ lower bound (Pal 4, Pal 14 dominate; Υ_V-limited) | D10 |
| dwarf satellites | +0.89 dex above screened prediction (E3). Pre-infall retention rule (PAPER36, ζ = 1 inside r_tidal; G2): FAILS on native inputs (+0.92 / +0.89 dex; the retained cold energy pays the phantom first, nothing is left over); it closes only with ΛCDM's subhalo mass put in by hand (Moster+13 + NFW), still overshooting 8 systems, and DF2/DF4 do not get ζ = 0 from the rule. Supply: the framework's dynamics cannot fix a satellite's catchment (it needs the patch's initial overdensity and infall epoch — UNDECIDABLE); the satellites' own [Fe/H] (leaky box, no ΛCDM input) gives ≥ 38× present baryons, enough (median need 0.21 of supply), with 6/36 short at central values and none at 2σ — CONDITIONAL on ζ = 1 winds and no pre-enrichment | E3, E6 |
| CMB / linear P(k) | a₀ absent at linear order (tests dust + G ratio only); native spectra PENDING | C2, C7 |
| cosmic shear (native PM) | canonical settling rules excluded by raw KiDS (CFG596); CFG960 rerun PENDING | CFG596, CFG960 |
| **linear growth of the v3 theory** | **FAILS as written.** With J_x, J′(0) = −1 exactly, so the Newtonian term vanishes on FRW; GR-on-dust growth holds only for k < aμ_K. Inside BS's allowed μ_K (≤ 14.8 h/Mpc) linear σ₈ is 0.03–0.32 (0.04–0.39 of the dust limit); above it the dust forms galaxy halos and double-counts against the law (CFG946). Whether the cubic deep-MOND term restores growth needs a Khronon-native PM (spec in F3 §6). In the μ_K → ∞ limit, linear S₈ = 0.814–0.845 is CONSISTENT with raw KiDS on k ≤ 0.3 h/Mpc points (0.9–1.5σ). The earlier 15–19 % excess and CFG596's Δχ² +68.7 belong to the settling rules and QUMOND phantom, which v3 does not contain | F3 |
| isolated-galaxy lensing, outer (F2 rebuild) | **frozen verdict REAL FAILURE, not robust → UNDECIDABLE.** The record's Δχ² +100 came from the catchment supply edge, which v3 does not have; without it the far-outer amplitude is 0.96–1.04 of the data (1.1–2.6 Mpc). The 0.4–1.1 Mpc range is short (A 1.39) in the frozen photo-z-isolated sample, but a wider host veto removes it (1.25 ± 0.25 / 0.82 ± 0.16) and opens an isolation hole beyond 1.1 Mpc; the 'isolated' stack's outer signal moves 8.6σ with the isolation cut. The external field makes the outer prediction much worse (A_O2 4.5–12 with on-disk fields; data tolerate y_e ≲ 3e-5). All record two-halo terms are ΛCDM-built or knob-carrying. Decidable only with a native many-body stack or a large spectroscopic isolated sample | F2 |
| cluster cores (F1 rebuild, 326 eRASS1 × raw KiDS, re-extracted and reproduced) | **REAL FAILURE of the law on baryons.** A_MID (0.3–1 Mpc, data/law) 1.68–1.85 canonical / 1.54–1.70 alt, Z ≈ +5–6; most favourable corner still +2.5–4σ. Field equation (AQUAL vs QUMOND), native h, gas calibration, R500 and miscentring each move it ≤ 4 %. Any added cold profile that fixes MID overshoots the outskirts (incl. the record's settled c* = 0.40, which is ΛCDM-built). The theory's dust inside 1 Mpc is NOT DERIVED | F1 |
| old engine's growth excess (G1) | grows with grid resolution (0.040 / 0.077 / 0.163 at 128³ / 256³ / 512³) — the old 256³ pass was not converged; a smooth cap makes it worse; not inherited by v3 | G1 |
| ALMA U4/GS4 | expected unscorable (S/N 0.04–0.58); sealed, all three kernels harness-ready | D4, CFG942 |

## 4. Sealed predictions for data still to come

- **Gaia DR4 wide binaries (20 kAU):** screened γ_v − 1 = 8.1e-6 / 1.9e-6 / 5.8e-7 at L★ = 24 / 50 / 90 pc (C6) vs law-first AQUAL 1.167 / 1.199 (canonical / alt, primary g_ext; E2); scored on whole-catalogue γ̂ under σ_sys rule A3 (owner decision 3d82af0a7e).
- **ALMA U4 (2026-11-06) / GS4 (2026-11-28):** CFG806/CFG809 frozen plans + addendum E (ffb14e40bc); nu_mono verdict, n1/n2 parallel readings (harness 92fa9f9471); expected unscorable (D4).
- **Native CMB:** PENDING C7 (AeST patch; tests the dust sector and G_cosmo/G_N only).

## 5. What this is not

**Growth is the open wound:** as written, v3 has no μ_K that gives both the law and normal structure growth (F3). Not a UV completion. Not derived constants: κ, L★ and the dust abundance are fitted. The CMB cannot test
the galactic law at linear order. Dwarf satellites are an open tension.
