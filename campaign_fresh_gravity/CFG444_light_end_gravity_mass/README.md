# CFG444: the light end via holes with GRAVITY-class (dynamical) masses: STAYS OPEN

Criteria 493ba7b2f (committed before any table was read). Script `cfg444_light_end_gravity.py`: 12/12 checks pass, and MUTATE passes 11/11. It runs CFG367's `cfg367_superradiance.py` from its committed bytes (sha256 d78a3812..., checked), the same way CFG394 did. `fetch_xray.py` is the one-off X-ray lookup. Every number below comes from `cfg444_light_end_gravity.out` / `_results.json`.

## Verdict

**STAYS OPEN.** None of 2.01-4.35e-20 eV is excluded, and no object reaches TIER A or TIER B.

**What was compiled.** 63 holes with central masses of 3e8-3e9 Msun:
- 61 from the van den Bosch 2016 dynamical/RM compilation (VizieR tables 2 and 3);
- J0529-4351 and J0920+0657 from GRAVITY+;
- 3C 273's GRAVITY and SARM masses, merged with its RM row (PG 1226+023).

54 of the 63 have a dynamical mass, and 29 are precise (dynamical, at most 0.15 dex, no disagreement between methods). CFG394's virial-mass spin objects enter only route B, below.

**No precise dynamical mass in 3e8-3e9 has a spin measurement, by any method.**
- The only spin record on a dynamical-mass object is 3C 273 (Gaur+25). Its reflection fits keep the spin *fixed* at 0.998, so it is not a measurement.
- 3C 273's own mass also depends on the method: 2.6e8 (GRAVITY 2018), 3.5e8 (SARM II) and 1.1e9 (SARM model M4). Two of these disagree beyond their errors, so it is not precise.
- With every R2 floor at 0, Omega_H = 0 for every object, and the code excludes nothing.

**GRAVITY masses in the window.**
- Only one GRAVITY-type mass is precise and falls in the window: **J0529-4351** (z = 3.96), at 7.9e8 Msun (+0.11/-0.13 dex, statistical only).
- It has no spin, no XMM or NuSTAR pointing, and an eRASS1 0.2-2.3 keV flux of 2.3e-13 cgs.
- Even with a spin of 0.98 it would exclude **0%**, because a 0.13 dex mass is too wide under CFG367's ±2σ mass range. Mass precision is again the wall.
- The other GRAVITY targets fall outside the window: 3C 273 at 2.6e8 is not precise, and Mrk 509, PDS 456, Mrk 1239, IC 4329A, IRAS 09149-6206 and NGC 3783 are all at or below 1.7e8. J0920+0657 (3.2e8) carries 0.27 dex.
- No maser disc reaches 3e8.

## The decider list (deliverable)

The fraction is the share of the light end excluded under CFG367's `mass_range`/`excluded`, at the object's own mass and errors, for hypothetical spin floors of 0.7, 0.9 and 0.98.

**D1a: precise dynamical mass in 0.8-1.5e9 (8 objects). All are LLAGN or quiescent.**

| # | object | M (Msun) | err (dex) | λ_Edd | frac at a ≥ 0.9 / 0.98 | NuSTAR (ks) | F(2-12 keV), cgs |
|---|---|---|---|---|---|---|---|
| 1 | NGC 4374 (M84) | 9.3e8 (gas) | 0.05 | < 3e-5 | 0.26 / 0.56 | none | 4.7e-13 |
| 2 | NGC 5846 | 1.10e9 (stars) | 0.06 | < 4e-5 | 0.12 / 0.52 | none | 3.8e-13 |
| 3 | NGC 524 | 8.7e8 | 0.05 | < 5e-5 | 0.28 / 0.49 | none | 8.9e-14 |
| 4 | NGC 4751 | 1.41e9 | 0.06 | < 4e-5 | 0.07 / 0.48 | none | none (no XMM) |
| 5 | NGC 3998 (Sy1.9 / LINER) | 8.5e8 | 0.05 | ~2e-5 | 0.28 / 0.47 | 104 | 1.1e-11 |
| 6 | A3565-BCG | 1.29e9 | 0.07 | < 1.4e-4 | 0.00 / 0.38 | none | 1.0e-12 |
| 7 | NGC 3115 | 8.9e8 | 0.09 | < 8e-6 | 0.00 / 0.21 | none | none |
| 8 | NGC 5055 | 8.3e8 | 0.10 | < 7e-6 | 0.00 / 0.11 | 164 | 7.8e-13 |

- NGC 4374 + NGC 4751 at a ≥ 0.98 would exclude **97%** of the light end. This is the best real pair.
- The catch: every one of these is a radiatively inefficient nucleus, with λ < 1.5e-4 from Swift/BAT detections or non-detections. **A reflection spin is not expected from any of them** (frozen rule D4).
- The 4XMM fluxes of cluster central galaxies include cluster gas.

**D1b: precise masses at 3e8-3e9, outside 0.8-1.5e9 (21 objects).**
- Cygnus A (2.6e9, radiatively efficient, NuSTAR 64 ks) is too heavy: 0% even at a = 0.98.
- J0529-4351 also scores 0%, as above.
- NGC 1332, NGC 5813 and NGC 4594 reach 18-27% at a = 0.98, but all are LLAGN.

**D1c: dynamical masses of 0.15-0.3 dex in 0.8-1.5e9 (6 objects).**
- NGC 1275 (λ ~ 3e-3, beamed) and NGC 6240 S (Compton-thick) are the radiatively efficient ones.
- All six score 0% at their own mass errors.

**Route B (departure; hypothetical masses, see below): spin-record AGN at 0.5-2e9, *if* a GRAVITY mass at ±10% existed.**

| rank | object | spin status now | GRAVITY-feasible? | frac at a ≥ 0.9 / 0.98 | X-ray |
|---|---|---|---|---|---|
| **1** | **PG 1426+015** (9.1e8 RM) | model-dependent: R2 floor 0; broadband 0.69-0.99 | **yes**: z = 0.087, Paα/Brγ in K, dec +1.3 | 0.34 / 0.56 | F 7.6e-12; NuSTAR 128 ks; BAT detected |
| 2 | Q2237+305 (1.2e9 virial) | a ≥ 0.71 (CFG394 TIER B) | no: z = 1.695, no K-band line | 0.28 / 0.69 | no NuSTAR; F 2.2e-13 |
| 3 | PG 2112+059 (1.0e9 virial) | a ≥ 0.83 | no: no K-band line | 0.33 / 0.67 | F 1.3e-13 |
| 4 | NGC 1275 (9.5e8 gas) | none | no: dec +41.5 | 0.33 / 0.61 | F 2.3e-10 (cluster-contaminated) |
| 5 | PG 0804+761 (5.3e8) | upper limits | no: dec +76 | 0 / 0 | |

- No pair closes the light end. 0 of all pairs reach 99%.
- The best pair with both members radiatively efficient reaches 87%: PG 1426+015 + Q2237+305, both hypothetical at ±10%.

**Bottom line for the decider.** No real, named AGN today has both a precise dynamical mass in 0.8-1.5e9 and the accretion state that a reflection spin needs.
- **The single actionable target is PG 1426+015.** It needs a VLTI/GRAVITY(+) Paα/Brγ BLR mass at about ±10%, plus a deeper broadband XMM+NuSTAR spin whose lower edge is ≥ 0.9-0.98 under every soft-excess treatment. Together these would exclude 34-56% of the light end (about 2.8-4.35e-20). That narrows it; it does not close it.
- **Closing it needs a second radiatively efficient hole at about 1.4-1.5e9.** It must have a K-band broad line (z ≲ 0.31 for Paα) and dec ≲ +30. No such object is in this compilation.

## Controls

| control | result |
|---|---|
| C0: CFG367 code sha256 | identical |
| C1: CFG367 CSV byte copy | reproduces CFG367's committed intervals exactly, and equals CFG394's committed control run |
| C2: CFG367 internal checks | pass in all runs |
| C3: CFG394 decider row (1.0e9, ±10%, a ≥ 0.98) | 0.670, reproduced exactly |
| MUTATE (frozen form): all 63 window objects with CFG367_MUTATE = 1 | union empty |
| MUTATE (extra, `_MUTATE` outputs): hypothetical a = 0.98 list with spins set to 0 | union empty |

**Positive control (hypothetical).** RUN_HYP098 gives every dynamical window mass a ≥ 0.98. It then excludes 2.09-4.35e-20, so the code would bite if the spins existed.

## Departures (disclosed)

1. **Route B is outside D1.** It uses non-dynamical masses with a hypothetical ±10% GRAVITY mass. It is labelled as such and decides nothing.
   - It adds a GRAVITY-feasibility flag that was not frozen: a broad line (Brγ, Paα, Paβ, Hα, Hβ) inside 1.95-2.45 μm, and dec ≤ +30.
   - Route B redshifts come from SR26 Table 2; NGC 1275's comes from BAT.
2. **D3's "fewer than 20,000 counts" test was not computed.** "Lacks spectra" is reported as "no NuSTAR pointing within 3′". NuSTAR ks, XMM ks within 10′ and the 4XMM 2-12 keV flux are listed for each object.
3. **D4's λ uses an estimator the frozen file did not name:** L_bol = 8 × L(14-195 keV).
   - For BAT non-detections the limit is F_lim = 1e-11 cgs; 24% of BAT105 sources lie below it.
   - Every D1a object sits at least 7× below λ = 1e-3, so the flag does not hinge on the factor 8.
4. **The MUTATE run also produces a positive control.** I added the hypothetical a = 0.98 list (RUN_HYP098) and its spins-0 MUTATE, on top of the frozen spins-0 run on all objects.
5. **Mass errors.**
   - IRAS 09149-6206 (~1e8, outside the window) is entered at 0.3 dex.
   - J0529-4351's ±0.13 dex is statistical only; the paper quotes no systematic term.
   - 3C 273 SARM M4: the paper prints both +0.21/-0.27 and +0.27/-0.21. The abstract's order is used; this changes nothing, since 3C 273 is imprecise either way.
6. **Post-2016 ALMA/HST masses not in van den Bosch 2016 were not compiled** (e.g. NGC 315, NGC 3258, NGC 4261 revisions). All are LLAGN radio galaxies, so they would add to D1a/b, not to the radiatively efficient set.
7. **Spin searches for J0529-4351, Cygnus A and NGC 1275 found nothing.** The NGC 1275 Hitomi narrow-Fe-K remark is a search pointer only, and no number from it is used.

## Owner items

1. **Proposal-grade target: PG 1426+015.** It needs a GRAVITY(+) BLR mass (VLTI-accessible, Paα/Brγ in K) and a deep broadband XMM+NuSTAR spin. That would narrow the light end by up to about 56%; it would not close it.
2. **The second hole (about 1.4-1.5e9, radiatively efficient, z ≲ 0.31, dec ≲ +30) is not in hand.** Finding it needs a BASS-DR2-style compile of broad-line BAT AGN with M ~ 1.2-2e9. That would be a new lane, if wanted.
3. **J0529-4351 is the only precise GRAVITY mass in the window.** It is useless for this test unless its mass error drops to about 0.04 dex and a z = 4 reflection spin becomes feasible (eRASS1 soft flux 2.3e-13). Not recommended.

## Scope

- A gravity-only test. It bounds where the field's mass can be and detects nothing.
- The cold-fluid amount stays free. κ = ½ is fitted.
- No dark-matter particle species is claimed. The theory is not closed.
