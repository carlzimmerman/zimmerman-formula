# CFG199 — MUSE-DARK: is CFG198's a₀ level real? (the model's own rotation profile, bracketing the pressure term)

- **Criteria:** `FROZEN_CRITERIA.md` (997e5047a), committed before any number. **κ = ½ FITTED, NOT DERIVED.**
- **Data:** CFG198's sample of 109 disc-only galaxies, plus the 126 `true_Vrot.dat` files. The files are outside the repo; their hashes match the data chat's manifest (C1).
- **Run:** `python3 campaign_fresh_gravity/CFG199_musedark_level_pressure/cfg199_musedark_level.py`, about 15 s; `MUTATE=1` runs the control.
- **Controls:** C1–C4 pass. C4 re-derives CFG198's committed primary slope from the copied formulas: +0.78891. MUTATE passes: v × 0.8 shifts the level by −0.1938 dex.

## Bottom line

- **CFG198's against-interest level does not survive.** CFG198 reconstructed the total at R_e as D × (its thin-disc g_bar). That is 3–7 times larger in acceleration than the model's own rotation velocity at R_e gives: median log₁₀(g_⊥/g_obs,CFG198) = −0.75 in reading (a) and −0.49 in reading (b).
  - With the model's own velocity, the no-pressure lower bound on the level at z ≈ 0.52 is **−10.38 [−10.71, −10.12]** in reading (a). That is below both footings.
  - In reading (b) it is **−10.14 [−10.45, −9.94]**, consistent with both footings.
  - CFG198's v22 variant also gave a low-z level below the footings: −10.33.
  - So the "0.25–0.65 dex above both footings" in CFG198 was an artefact of its g_obs scale, not a property of the model. The true level lies between the no-pressure bound and a pressure-corrected value that these files do not give directly.
- **CFG198's slope finding survives and sharpens.** With the model's own velocity:
  - Route (i), III's fitted masses, rises: **+0.65 [+0.25, +1.08]** in reading (a) and **+0.63 [+0.25, +1.00]** in reading (b). This is now consistent with III's law (+0.30) and with E(z), so the closure that CFG198 missed by overshooting passes here.
  - Route (ii), SED + H₂, is **−0.20 [−0.74, +0.36]** in (a) and **−0.22 [−0.77, +0.30]** in (b).
  - The paired change is **Δb = −1.03 [−1.32, −0.75]** in (a) and **−1.03 [−1.34, −0.74]** in (b).
  - In reading (b), route (ii) excludes III's law, only just (its CI's upper end, +0.297, sits below III's +0.300). It does not exclude flat or E(z).
- **Which reading of the file's v.** Reading (b), the projected line-of-sight velocity (v/sin i), is better supported. The ratio to CFG198's v_c shows no trend with sin i in (b) (ρ = −0.01), against ρ = +0.40 in (a). This is reported, not graded.

## What this changes in the record

- **CFG198's level statement is withdrawn** as an artefact of CFG198's g_obs scale. A correction section has been appended to its README.
- **The MUSE-DARK a₀(z) picture after CFG198 and CFG199:**
  - III's rise appears whenever the DC14-fitted masses are used, now also on the model's own velocities.
  - It disappears when the SED stellar mass (+ H₂) is used.
  - With SED masses, flat is never excluded. The rival E(z) is excluded in one gas row of CFG198, and III's law in up to three rows (see CFG198).
  - Which stellar mass is right is not determined, and the level remains uncertain between the no-pressure bound and the pressure-corrected total.
- **Caveats:**
  - Route (i) here uses the model's fDM with the file's velocity. Routes (ii) and (iii) carry CFG198's thin-disc baryon ratios.
  - The share s = 1 − g_⊥/g_obs,CFG198 (median 0.84 in a, 0.75 in b) mixes the pressure term with CFG198's geometry error. It is not a measurement of either.
