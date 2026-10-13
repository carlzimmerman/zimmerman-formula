# CFG625: merger baryon-input sensitivity (criteria 9afb3f44b) — RESULT: NO VARIANT TESTED (MUTATE M3 fails in all three)

Runs: detached driver (one ~2 GB process at a time), 2026-10-11 13:10 → 2026-10-12 09:09. Variants B1 (Famaey 2026 Plummer
stars/gas), B2 (concentrated Hernquist BCG, R_e = 30 kpc bracket), B3 (all measured), each calibrated to CFG623's K1/G1
targets; controls → MUTATE → grid → summary as frozen.

- **MUTATE (frozen gate): FAIL in every variant → all variants VOID.** M1 (α = ∞) passes (f 1.02–1.10); M2 (α = 0) passes in
  B1/B2 (β̄ 0.075 / 0.045) but fails in B3 (f 0.30, β̄ 0.21); **M3 (roles swapped, α = ∞: lensing must sit on the collisionless
  baryons, f ≤ 0.25) fails in all three (f 1.79 / 0.97 / 1.02).** With data-based (less concentrated) stars, swapping roles no
  longer moves the lensing peak onto the stars — the M3 tooth assumed CFG597's provisional NFW c=4 stars. So the α verdicts
  under measured baryons are NOT TESTED; CFG623's α results remain provisional.
- **M-RAW anchor (projected M(<250 kpc) at the Bullet epoch, α = 0): NOT MET anywhere.** Main 0.54–0.69, sub 0.35–0.43 of
  Paraficz+16 (PROVISIONAL, recalled). These are case-L progenitors (unsettled reservoir = 0); CFG629 showed the reservoir
  closes most of the main-cluster gap and that the sub's simulation-line input mass is too small.
- Disclosure (from the build agent): CFG597's τ density-floor rule reads the stellar density at r = 0.5 kpc, so the floor
  factor depends on the stellar cusp (324 BASE, ~26–33 B1/B3, 2099 B2); kept literal as frozen.
Outputs: cfg625_{static,calib_B*,controls_B*,MUTATE_B*,grid_B*,c16,summary}.out/_results.json. κ = ½ fitted; cold energy
mass required; not theory closed.
