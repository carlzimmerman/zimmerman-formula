# Audit: "the chassis fails linear cosmology, σ₈ = 18–27" (L341, e9f450b10)

This is a hostile audit run from both sides. It asks whether the L341 failure is real, and whether L341 computed it the way the framework says it should be computed. Nothing in this folder re-scores L341 or changes it. L341's frozen result stands as committed.

## Files

| file | what |
|---|---|
| `L341_rerun_copy.py` | A byte-identical copy of `real_research/g03_audit_2026/L341_chk_frw_gate.py` (sha256 `6bda2d37…b6cc0`). It sits at the same depth below the repo root, so it reads the same data and writes its JSON here, not into L341's folder. |
| `L341_rerun_copy.out`, `L341_rerun_copy_MUTATE.out`, `L341_chk_frw_gate_results*.json` | The re-run. The output differs from the committed `.out` only in the timing line, and the F2 JSON block is identical. MUTATE returns rc = 1, as committed. The run takes about 7 s, so no cheaper configuration was needed. |
| `audit_sigma8_diagnostics.py` / `.out` / `_results.json` | Diagnostics D0–D6. They exec L341's own definitions from the copy (up to its F1 banner) and check the hash first. The values used are fixed and declared; there is no fit and no knob scan, and κ = ½. |

## What the diagnostics show (canonical footing, L341's "rms" field argument)

- **D0 control.** The harness reproduces L341 F2: σ₈ = 23.32 / 27.48 against the committed 23.314 / 27.474. The harness drops the c₂ tracking factor, which F2 shows makes no difference inside the window.
- **D1. The field at L341's start, z = 1000, is NOT fully Newtonian.** y_rms = 4.99 and ν − 1 = 0.13. The declared check (y > 10) FAILS and is kept. So L341 under-counts the boost: it ignores the MOND boost before z = 1000 and uses an EH98 (ΛCDM) transfer function. Correcting this can only raise σ₈. It does not affect the CMB anchor's direction.
- **D2. The history.** The boost turns on gradually: amplitude ratio 1.19 at z = 200, 1.44 at z = 100, 3.1 at z = 20, 6.8 at z ≈ 5.9, 28.8 at z = 0.
  - The amplitude in the σ₈ window crosses 1 (nonlinear at 8 h⁻¹ Mpc) at z ≈ 5.9. The structure level seen today (0.81) is reached at z ≈ 7.
  - The excess is therefore made while δ < 1. Only the quoted z = 0 number, 18–27, is an extrapolation past nonlinearity.
  - The self-consistent rms field holds at y ≈ 0.1–0.3. In ΛCDM it would fall to 0.0035. So the growth self-limits (ν drops to about 3), but it does not switch off.
- **D4. Anchor sensitivity.** Changing the initial amplitude by ×0.958 / ×1.042 (about 3σ of Planck's A_s) gives σ₈ 23.20 / 23.44. Changing it by ×0.1 / ×10 gives 19.4 / 37.9. The result is close to an attractor, because a smaller seed sits deeper in MOND and is boosted more. The ΛCDM-derived A_s anchor is not what makes the failure.
- **D5. Start-time sensitivity.** With the boost on only below z = 200 / 50 / 10 / 3, σ₈ = 22.5 / 19.8 / 13.0 / 6.2. Even MOND acting only since z = 3 fails by about 8×.
- **D6. Field scale from data, framework-neutral.** The Local Group's 600 km/s motion implies a linear peculiar acceleration of about 1.2e-12 m/s², or 0.010–0.013 a₀, where ν_mono ≈ 9.5–10.3. The real large-scale field is deep in MOND. Any rule that applies ν to all matter at linear scales boosts growth strongly. The chassis's self-consistent field, about 0.1 a₀, is roughly 8× the field implied by the measured motion, so it would also predict bulk flows far above those measured. This is an order-of-magnitude estimate only.

## Audit table

| # | item | what was done (record) | framework-correct? | effect |
|---|---|---|---|---|
| 1a | action / kernel | L341 uses ν_mono, L340's monotone kernel, with κ = ½ on both footings. It applies a phenomenological growth ODE (L142's machinery) with the chassis's tracking weight 1/(1+(H/c_s k)²). It does NOT use the action's own perturbation equations. | Kernel: yes. Equations: approximate. The action-derived system (FP7 B5, re-done in FP22 B0–B4) is strictly linear and ill-posed (σ₈ = ∞ at λ_eff = 3, 10¹¹¹ at 277: the zero-field k² runaway). On the "physical-amplitude yardstick" it gives 8–24×, the same as L341. | The headline survives both routes. The strict linear theory is worse than L341, not better. |
| 1b | heat filter | Not applied in L341. | Yes, it is negligible: C_eff = e^{−ξ²k²}C (FP2) with ξ ≥ 0.03–0.05 pc. Any ξ that keeps galaxy MOND (ξ ≪ kpc) gives e^{−(kξ)²} > 0.999 at k ≤ 20 h/Mpc. | ~0 |
| 1c | cold component | Included at Ω_c h² = 0.120. It sources and feels the MOND boost (the source is Ω_m δ). | Yes for the chassis. FP22 A2 derives from the action as written that ALL matter sources and feels the scalar (reading a). The kinder reading (b), where the dark component is MOND-blind, is a choice (FK1 on g̃) and costs a dark–baryon WEP violation. It still fails σ₈ at 1.45–2.2× (FP22 L22g). | Reading (a) gives 18–27; reading (b) gives 1.45–2.2. Both fail. |
| 1d | initial conditions / normalisation | EH98 ΛCDM spectrum normalised to σ₈ = 0.811 today, then scaled back to z = 1000 with ΛCDM growth. That is equivalent to Planck's A_s through the ΛCDM transfer function. | A fair anchor in direction: Ω_c is present, so pre-recombination transfer is close to ΛCDM. It is not exact: ν − 1 = 0.13 already at z = 1000 (D1), and MOND before z_i is ignored. | Negligible on the verdict: ×0.1 to ×10 on the anchor gives σ₈ 19–38 (D4). The z_i truncation biases σ₈ low, not high. |
| 2a | is σ₈ the right observable? | L341 compares its z = 0 "linear" σ₈ with 0.81. | Partly mis-stated. The ODE is quasi-linear (ν depends on amplitude), the σ₈ window goes nonlinear at z ≈ 5.9, and 0.81 is itself a ΛCDM-inferred number. "Linear σ₈ = 18–27" is an extrapolation, not a prediction for a survey. | The number is not quotable as an observable. The failure is: the boost is ×6.8 in amplitude by z ≈ 6, still in the linear regime. |
| 2b | raw-observable form | FP22 L22j: in reading (a), web MOND is excluded by the Planck 2018 lensing (8–400) and ACT DR6 band powers even with separators. In reading (b) it passes on the linear base and fails ACT on the halofit base (undecided). CFG4 holds the Planck MV band powers. | Yes. That is a raw two-point observable (C_L^φφ). | With no separator, the D2 growth ratio of 7–13 at z = 2–5, where CMB lensing gets its weight, means lensing power about 50–170× ΛCDM, against 1.011 ± 0.028. This is an estimate and was not run. The failure survives in raw form. |
| 2c | saturation (CFG321/322) | CFG321: the zero-field Hadamard mode saturates at 0.2–0.3 y*, with y* = (α_c/2)² ≤ 2.6e-18. The median field is 5–8e-29 m/s², a gravitational spectator. | Saturation applies to the khronon's zero-field instability, not to matter growth. It sits about 17 orders of magnitude below the perturbation field (y_rms 0.1–5). | It cannot cap clustering. L341 does not assume unsaturated Hadamard growth. It uses the full amplitude-dependent ν, which already self-limits (y stays near 0.1–0.3). The excess growth is physical in the chassis. |
| 3 | chassis or B? | The tile reads "chassis alone". B has no action ("No committed action produces candidate B"). B's growth is GATES 3.03 "met by allowance" (CFG4_cosmology: the ΛCDM P(k) is taken as given, a₀ enters no linear coefficient, and ownership means the linear web carries no phantom). The gated lanes (L359, DE2) restore growth only with a prescribed gate that is unstable as an action (DE12/13). FP22 C2: a separator is needed in either reading. | The failure does not transfer to B as stated. B is not passed either: its growth is assumed, not computed. | B's growth is UNTESTED. No committed lane derives it. |
| 4 | re-run | The verbatim copy was re-run. Output is identical except the timing line; MUTATE rc = 1 is identical. The diagnostics harness reproduces F2 to 0.03%. | — | 18–27 confirmed (17.7–27.5 across the per-mode and rms field arguments). |
| 5a | ΛCDM use: transfer function | EH98, a ΛCDM fit with no MOND before z = 1000. | Approximate (D1: ν − 1 = 0.13 at z_i). | Biases σ₈ low. |
| 5b | ΛCDM use: amplitude | σ₈ = 0.811 normalisation, equivalent to Planck A_s. | A fair anchor. | ≤ 1% for ±4% on A_s; the attractor holds (D4). |
| 5c | ΛCDM use: parameters | Planck 2018 h, ω_b, ω_c, n_s, so f_b = 0.157. | ω_c is what B requires anyway. h and n_s come from Planck under ΛCDM. | Small next to ×29. |
| 5d | ΛCDM use: background | ΛCDM Friedmann. | Yes. FP2 D1–D2: with the leaf average, Friedmann is GR's. | 0 |
| 5e | ΛCDM use: comparison target | 0.811 (Planck ΛCDM). | A ΛCDM-inferred number. Weak-lensing S8 of about 0.76–0.8 gives the same verdict. | None on the verdict. |

## Bottom line

- **Verdict.** The failure is a genuine framework-native failure, but its observable is mis-stated.
  - In the chassis, the MOND sector acts on all matter, including the required cold component. FP22 derives this from the action as written.
  - The real large-scale field is about 0.01 a₀, so the boost is physical. It is made while δ < 1: ×6.8 in amplitude by z ≈ 6. It does not depend on the ΛCDM-derived CMB anchor (an attractor, D4) or on when MOND switches on (×8 even from z = 3).
  - CFG321's saturation is a different mode at a field 17 orders of magnitude lower, and cannot cap it.
  - The number "σ₈ = 18–27" is a quasi-linear extrapolation past nonlinearity at z ≈ 6. The strictly linearised action is ill-posed (infinite σ₈), so neither number is an observable.
  - The excess growth itself is real, and it is excluded in raw form by the CMB-lensing band powers (FP22 L22j). This is not an artefact, and no redefinition rescues it.
- **Honest tile text:** "Chassis alone (all matter feels ν_mono, as its action implies): structure grows ~7× faster than ΛCDM by z ≈ 6 while still linear and is excluded by CMB lensing. 'σ₈ 18–27' is an extrapolation, not an observable. FAIL stands; the MOND-blind dark reading still fails (1.45–2.2×); candidate B's growth is assumed, not tested."
- **The framework-native lane that would test it against raw data:** evolve the chassis's amplitude-dependent growth, in reading (a) and in reading (b), to C_L^φφ with CLASS (installed) and Limber. Score it against the Planck 2018 lensing MV band powers 8–400, which are already typed into CFG4 / XR26 and on disk. Add a velocity-field check against the 6dFGS fundamental-plane peculiar velocities (`real_research/data/fp_6dfgs_campbell2014.tsv`, on disk) and the 2M++ density field (`twompp_density.npy`, on disk).
  - KiDS-1000 cosmic-shear ξ± and the ACT DR6 band powers are not on disk. Fetching them would need the owner's go.
  - In reading (b), the deciding step is the nonlinear phantom (FP22 L22k, a particle-mesh run), which is not available yet.
  - For B, a growth test needs an action, or at least a declared ownership rule for the linear web. It cannot be scored until one exists.
