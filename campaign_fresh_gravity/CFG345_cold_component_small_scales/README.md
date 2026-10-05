# CFG345: does candidate B's cold component clump like CDM down to the masses CFG344 needs? CONDITIONAL

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (b4bb12ef3, sha256 07d7e580...f272; every output prints it).
- **Run (repository root):** `python3 campaign_fresh_gravity/CFG345_cold_component_small_scales/cfg345_small_scales.py`; MUTATE: `CFG345_MUTATE=1 python3 ...` (writes `_MUTATE` outputs); Lean: `python3 .../cfg345_lean_gen.py`, then `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/CFG345_certificate.lean`.
- The cold mass (Omega_c h^2 = 0.120) is still required. No dark-matter particle is added. kappa = 1/2 is FITTED.

## Verdict: CONDITIONAL
B as frozen specifies no microphysics for its cold component, so it has no cutoff. The record's only microphysical construction that is still live, CFG288's wave field (= FL1's order parameter), has a cutoff that depends on its undeclared mass m. It clumps like CDM down to M_need = 3.83e7 Msun only if **m >= 2.29e-20 eV**. That bound lies inside CFG288's allowed window [2e-20, 37] eV, so the record does not exclude it. At the window floor (2e-20 eV, the Ly-alpha floor as quoted) the half-mode mass is 4.6e7 Msun, just above M_need, so CFG344 would be marginally suppressed there. The record's L383 dwarf-heating floor (2-5e-19 eV), where it is applied, already satisfies the bound by a factor of about 20 in mass.

## Inventory (record only)
| specification | status for B | small-scale behaviour | parameter, fixed? |
|---|---|---|---|
| B as frozen; CFG4 T5 "identity bookkeeping" (dark mass = max(phantom, cosmic share)) | CURRENT | none specified (bookkeeping only, no microphysics) | none |
| CFG288 road W: linear complex wave field, V = rho_Lambda + m^2 abs(Phi)^2 ("one field") | live CONSTRUCTION, not adopted ("shared label only"; AMOUNT FREE) | quantum-pressure (wave) cutoff: HBG transfer, half-mode M_1/2 = 5.35e10 m22^(-4/3) Msun | m, declared, NOT fixed; window 2e-20 to 37 eV |
| FL1-FL3 / FK1 dark fluid (superfluid order parameter) | same field as road W (CFG288: "FL1's order parameter") | as road W; FL notes work at m = 2e-19 eV | m declared (2e-19 used); FK1's lambda abs(Phi)^4 gives sound speed 22 km/s only at the trigger (not scored here) |
| CFG293 wave-field cores | not a specification: tests road W's solitons for the satellites, NO WINDOW | soliton cores (inner-halo), not linear power | same m |
| CFG288 road S: ghost-condensate P(X) dust | live CONSTRUCTION (AMOUNT FREE; single-scale tie FAILS) | pressure (Jeans) cutoff, c_s^2 = rho_d/(4 M^4) | M, NOT fixed; record needs M >= 4.24 eV (G-DUST) and M >= 3.3 keV (G-ONSET) |
| v9 DBI khronon dust; condensate mu-pincer horns | DEAD (mu-pincer theorem kill) | Jeans suppression 44-100% (record) | never decides |
| GP0-GP5 generated phantom (L319-type kicked carrier) | not B's cold component (fails shear 2-3x; GP4 window withdrawn) | wanted the dark share SMOOTH below ~lambda (Mpc) | lambda free; never decides |

## Numbers
- **M_need** (CFG344 JSON, z_f = 8): 3.83e7 Msun, growing to 5.75e8 by z = 2. Sensitivity: z_f = 10 gives 2.84e7, z_f = 6 gives 5.59e7.
- **Wave field, half-mode mass** (T^2 = 1/2, the decision convention; the T = 1/2 value is in brackets):

  | m (eV) | M_1/2 (Msun) | Jeans M_J at z = 6 / 8 / 10 (Msun) | below M_need? |
  |---|---|---|---|
  | 2e-20 (window floor) | 4.58e7 (3.37e7) | 2.3e4 / 2.8e4 / 3.3e4 | NO |
  | 2e-19 (L383 low) | 2.12e6 | 7e2 / 9e2 / 1e3 | yes |
  | 5e-19 (L383 high) | 6.3e5 | ~2e2 | yes |
  | 37 (window top) | ~0 | ~0 | yes |

  The bound is m >= 2.285e-20 eV (m22 >= 228.5). With the T = 1/2 convention the floor itself passes (3.37e7), so the floor's failure depends on the convention. The halo mass function at M_need is suppressed to 0.54 of CDM at 2e-20 eV and 0.98 at 2e-19 eV (Schive+16 fit, PROVISIONAL, context only).
- **Road S, Jeans mass at z_eq** (conservative: the mode must grow through the whole matter era): CDM-like at M_need iff M >= 43.8 eV. At the record's G-DUST minimum, 4.24 eV, M_J(z_eq) = 4.7e13 Msun, which is strongly suppressing. But the record's own G-ONSET gate already demands M >= 3.3 keV, where M_J is about 0. So road S, taken with all of its own gates, is CDM-like.

## Ly-alpha forest (record only)
- **The record's small-scale-power content from the forest** is the input floor m >= 2e-20 eV (Rogers & Peiris 2021, as quoted in CFG288's merger gate), plus CFG288's loose criteria T^2(10 h/Mpc, z = 3) >= 0.5 and c_s <= 5 km/s.
- **Under B the forest is Newtonian.** Only bound baryons source the kernel (GP / reciprocity notes), so standard forest inferences on P(k) carry over approximately.
- **The forest's reach** is k = 10 h/Mpc, which corresponds to 1.7e10 Msun: 440x M_need. The forest is therefore consistent with CDM-like clustering at z = 2-5 down to about 1e10 Msun. It does not test 3.8e7 directly. Its only bearing at 3.8e7 is through the quoted particle-mass floor, which sits right at the edge (M_1/2 = 4.6e7 at the floor).
- **The b-cutoff lane** concerns diffuse-gas temperatures under the law (withdrawn 6-8 sigma, now 0.4-0.9 sigma on calibration). It says nothing about the cold component's small-scale power.

## Controls (main run: all pass, exit 0)
- C1: HBG k_1/2 (T^2 = 1/2) = 4.584 m22^(4/9) /Mpc vs Hu+00's 4.5 (PROVISIONAL): 1.9%.
- C2: T = 1/2 gives M_1/2 = 3.94e10 m22^(-4/3) vs Schive+16's 3.8e10 (PROVISIONAL): 3.6%.
- C3: the Jeans formula at z_eq gives 9.10 m22^(1/2) /Mpc vs CFG288's 9.
- C4: road S gives k_J(1100, 4.24 eV) = 2.200 h/Mpc vs CFG288's committed 2.2.
- C5: M_need = 3.8327e7 from CFG344's JSON.
- **MUTATE** (m = 2e-20 eV, M = 4.24 eV) FLAGS both. The wave field at the window floor gives M_1/2 = 4.6e7 > M_need. Road S at its G-DUST minimum gives M_J(z_eq) = 4.7e13. That is why the verdict is CONDITIONAL and not CDM-LIKE.

## Lean
`CFG345_certificate.lean`, 7 theorems, Mathlib, no sorry, compiles clean. They certify:
- 2e-20 eV suppresses; m22 = 228 fails and 229 passes; the 2e-19 eV floor passes.
- Road S at 4.24 eV suppresses, while 44 eV and 3.3 keV pass.

All of these use A, B and M_need rounded outward.

## Disclosures
1. The transfer function, the Hu/Schive reference values and the HMF fit are transcribed from memory (PROVISIONAL). C1-C3 agree with them, but the agreement is with my memory of the references.
2. Whether the floor fails depends on the convention: T^2 = 1/2 (decision) fails at 2e-20 eV, and T = 1/2 passes. The bound shifts from 2.29e-20 to about 1.8e-20 eV. The verdict does not change.
3. The half-mode mass is a linear-theory proxy. CFG344's narrow window (~0.4 dex in M_c) means that even a mild delay in collapse near the cutoff could matter. A cold component near the floor would need its own collapse/MAH calculation, which was not done.
4. CFG344's other caveats (LambdaCDM-calibrated MAH, formulas from memory) are untouched by this lane.
5. Which mass the cold component has is a choice the record has not made. The CONDITIONAL verdict is the statement that B needs m >~ 2.3e-20 eV (or, on road S, M >~ 44 eV, which its onset gate already imposes) for CFG344 to stand.
