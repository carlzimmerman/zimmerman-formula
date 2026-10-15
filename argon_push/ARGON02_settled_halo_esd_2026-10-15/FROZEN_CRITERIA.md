# ARGON02 FROZEN CRITERIA — the settled-halo lensing edge: parameter-free ESD from the law + supply rule

Written and committed ALONE, before any script. Date 2026-10-15.
Home: `argon_push/ARGON02_settled_halo_esd_2026-10-15/`. κ = ½ FITTED. Footings never pooled (canonical
a₀ = 9.3603e-11 m s⁻² used throughout; the k01-era 9.3619e-11 differs by <0.02% and is never mixed in).
No particle species added. Lensing-to-mass coupling is taken as the repo's established working assumption
(minimal metric coupling certification 2026-10-13; CFG723 E2/E3: cold energy gravitates, Bullet lensing
follows galaxies, cosmic shear) — the relativistic completion itself stays open (canonical §3); the ESD
prediction below is the sharpest testable content of that coupling together with the settled phantom.
Not "theory closed".

## Question
The canonical law g_N = g²/(g+a₀) + the settled phantom (GF2 static branch, σ² = √(GM_b a₀)/2) + the supply
rule (each halo settles its own cold supply, Ω_c/Ω_b = 5.364) fix the projected lensing signal of an
isolated disk halo COMPLETELY — shape, amplitude and truncation — with zero free halo parameters. What
exactly is the predicted excess surface density ΔΣ(R), where does it break, and which data kill it?

## Derived quantities (to be computed, not assumed)
- Exact enclosed cold mass M_c(r)/M_b = (√(1+4r²/r_M²) − 1)/2 from the law (deep limit r/r_M − ½;
  Newtonian limit → 0).
- Exact 3D settled density ρ_c(r) = M_b/(2π r_M² r √(1+4r²/r_M²)) (deep limit √(a₀M_b/G)/(4πr²) =
  σ²/(2πGr²), σ² = √(GM_b a₀)/2 — GF2's derived dispersion, amplitude LOCKED).
- Projected Σ_c(R) and ΔΣ(R) = Σ̄(<R) − Σ_c(R) (numeric Abel projection); deep-regime check
  ΔΣ(R) → σ²/(2GR) = √(GM_b a₀)/(4GR) = v⁴/(4G v²R) — the standard isothermal ESD with the amplitude
  fixed by (M_b, a₀) alone.
- Supply-rule truncation: M_c(r_e) = 5.364 M_b ⇒ r_e = √(((2·5.364+1)²−1)/4)·r_M = 5.84 r_M — the
  settled halo EDGE. Prediction: the ESD breaks at 5.84 r_M for merger-free isolated disks; beyond it
  only baryons + any S4-freed debris contribute.
- Transition regime (r < r_M): ESD suppressed below the r⁻¹ extrapolation (phantom density cored as
  ρ_c ∝ 1/(r√(1+4r²/r_M²))); inner ESD dominated by baryons (model-dependent, stated as caveat).

## Gates (all required)
- G1 Amplitude locking: ΔΣ(R)·4GR/√(GM_b a₀) → 1 in the deep window (checked numerically to <1%).
- G2 Edge: r_e/r_M = 5.84 ± 1e-3 from the supply ratio; M_c(r_e) = 5.364 M_b exactly by construction.
- G3 Exactness: ρ_c from the closed form matches dM_c/dr/(4πr²) and the deep SIS check.
- G4 Projection honesty: Σ_c, Σ̄, ΔΣ computed numerically (Abel + cumulative), deep-window SIS identity
  ΔΣ = Σ checked.
- G5 Kill tests (data): (a) GGL ESD of isolated late-type disks in [1, 5] r_M must follow ΔΣ = √(GM_b a₀)/(4GR)
  with no NFW concentration freedom; (b) log-slope must break (|dlnΔΣ/dlnR| > 1.05 beyond ~5.8 r_M) for
  merger-free disks; (c) inner transition shape [0.2, 1] r_M from the exact formula; (d) MW/LG outer mass:
  the settled halo of M_b = 6.5e10 is 3.5e11 (M_c = 5.364 M_b) ending at ~57 kpc — any enclosed-mass
  requirement ≫ 4.1e11 at 100–300 kpc must be carried by the S4 free component (merger debris), never by
  the settled halo.
- G6 Mutation (must fail the claim if it fails): (i) supply ratio ±10% ⇒ r_e moves to 5.55/6.12 r_M —
  the ESD break shifts (reported, not pooled); (ii) alt footing a₀ = 1.1312e-10 ⇒ amplitude and r_M scale
  together, reported separately; (iii) an NFW-like continuation beyond 5.8 r_M (ΛCDM) must be EXCLUDED by
  the ESD data, else the edge prediction dies.

## Verdict
- PASS: G1–G4 hold with the stated residuals; the ESD law + edge + kill tests are committed as the
  framework's lensing prediction (conditional on the minimal metric coupling).
- FAIL: any gate miss; the prediction is then not made and the obstruction is named.