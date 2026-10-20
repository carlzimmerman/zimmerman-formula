# CFG876 — FROZEN CRITERIA: is the dwarfs' cold component universal? Out-of-sample test on large, cold dwarfs

Frozen before any script (owner block 870–879; owner: "we need to figure out the cold energy equations"). κ = ½ fitted.

## Why (cold-energy equations)
The record's cold-energy kinetic equation (CFG638) relaxes cold energy toward a bath dispersion σ_J², which is POSITED (open).
CFG870's cored component reads physically as a minimum cold-energy temperature: an isothermal cold atmosphere with
V_x = √2 σ0 ≈ 10.65 km/s (σ0 ≈ 7.5 km/s) and core r_c = 104 pc in every dwarf. If σ0 is a universal floor in the equations,
then every dwarf whose r½ lies well outside the core must have σ_pred² = σ_law² + V_x² f(r12)/3, f = r²/(r² + r_c²), i.e.
a line-of-sight floor near V_x/√3 ≈ 6.2 km/s, whatever its environment. CFG870 never used the large dwarfs found since its
calibration set (no SFH-based Υ). They are the decisive test. **Not blind:** Crater II and Antlia II are known in the
literature to be unusually cold; our model's numbers for them have not been computed.

## Sample (LVD csvs; nothing downloaded)
LVD MW + M31 + local-field dwarfs with measured stellar σ (no upper limit), r_h, M_V; CFG852's rotating / gas-rich set excluded;
**not used anywhere in CFG870** (not in CFG828's rows, not in CFG859's literature-σ UFD list).
- **Primary (B):** r12 = (4/3) r_h ≥ 3 r_c = 312 pc (component within 10% of its asymptote). Expected N = 18.
- Secondary (small): r12 < 312 pc, reported only.

## Prediction (no refit; CFG870's numbers)
- V_x = 10.6547 km/s (canonical) / 10.5870 km/s (alt) from cfg870_results.json; r_c = 104 pc.
- σ_law from the law at r12 (Wolf: σ_law² = g_law r12/3), g_bar = G (M*/2 + M_gas,in)/r12², Υ_V = 2 (primary), gas inside r12 from
  CFG874's Wang+16 disc (extended root). σ_pred = √(σ_law² + V_x² f(r12)/3).
- ε_i = ln(σ_obs/σ_pred). Individual significance z_i = (σ_obs − σ_pred)/e_i, with e_i = vlos_sigma_ep if σ_obs < σ_pred, else
  vlos_sigma_em (LVD errors). **For the individual-failure count, σ_pred is recomputed at Υ_V = 1** (the most lenient, lowest
  prediction).

## Classes (canonical primary; the alternative footing must agree, else UNDECIDED)
E = mean ε over B; se_E = bootstrap over B (4000 draws, seed 876). N_fail = number of B dwarfs with z_i ≤ −3 at Υ_V = 1.
- **UNIVERSAL HOLDS:** |E|/se_E < 2 and N_fail < 2.
- **BROKEN:** E/se_E ≤ −3, or N_fail ≥ 2 (the component predicts more than is there in dwarfs it must cover).
- **UNDER-PREDICTS:** E/se_E ≥ +3.
- **UNDECIDED:** anything else.

## Reported (not graded)
Law alone (V_x = 0) on B; the small out-of-sample dwarfs; MW-only and M31-only subsets of B; a **supply-capped** variant:
the component's mass inside r12 limited to the record's largest catchment supply 5.364 M_b / f_ret with f_ret = 0.10
(53.6 M_b; canonical v2 S3), i.e. σ_x² = min(V_x² f/3, G M_cap/(3 r12)); NGC 1052 trail galaxies are not in the LVD and are not used.

## Controls
- **K1 (code identity):** applying this script's predictor to CFG870's T2 list (M31 + field, CFG824 σ, CFG827 Υ, no gas)
  reproduces CFG870's m31_field_E (canonical +0.024706801720, alt +0.004084145870) to < 1e-9. FAIL ⇒ INVALID.
- **MUTATE** (`CFG876_MUTATE=halve`): σ_obs × 0.5 for B. Must give BROKEN.

## Disclosed limits (fixed now)
No external-field effect and no tidal truncation are modelled (the record's law has none; CFG838/839 found no tidal
dependence of the excess). The largest dwarfs are known to be tidally affected (Crater II, Antlia II). M31 distances and
σ for faint M31 satellites carry large errors. Υ_V = 2 for all (no SFH-based values for these objects).
